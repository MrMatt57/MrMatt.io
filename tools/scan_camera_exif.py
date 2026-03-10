"""Scan EXIF camera data from all photos in Google Takeout zips into SQLite.
Processes zips in parallel for speed. Reads only first 64KB per file for EXIF."""
import zipfile
import json
import sqlite3
import os
import io
import re
import time
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image
from PIL.ExifTags import TAGS

ZIPS_DIR = "F:/Photos"
ZIP_PATTERN = "takeout-20260307T015246Z-3-{:03d}.zip"
DB_PATH = "F:/Photos/pipeline/camera_timeline.db"

PHOTO_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".tif", ".tiff"}
SKIP_EXTS = {".json", ".html", ".css", ".js", ".zip", ".mp4", ".mov",
             ".avi", ".mts", ".mkv", ".wmv", ".gif", ".dng", ".raw",
             ".cr2", ".nef", ".arw"}

EXIF_READ_SIZE = 65536  # 64KB


def parse_exif_date(s):
    """Convert EXIF date 'YYYY:MM:DD HH:MM:SS' to ISO 8601."""
    if not s or not isinstance(s, str):
        return ""
    s = s.strip().rstrip("\x00")
    m = re.match(r"(\d{4}):(\d{2}):(\d{2})\s+(\d{2}):(\d{2}):(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}T{m.group(4)}:{m.group(5)}:{m.group(6)}"
    return ""


def parse_sidecar_date(s):
    """Parse Google Takeout sidecar date like 'Jun 20, 2015, 11:18:30 PM UTC'."""
    if not s or not isinstance(s, str):
        return ""
    # Remove non-breaking spaces and unicode
    s = s.replace("\u202f", " ").replace("\xa0", " ").strip()
    from datetime import datetime
    for fmt in [
        "%b %d, %Y, %I:%M:%S %p %Z",
        "%b %d, %Y, %I:%M:%S %p",
        "%b %d, %Y %I:%M:%S %p %Z",
        "%b %d, %Y %I:%M:%S %p",
    ]:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    return ""


def date_from_filename(filename):
    """Try to extract date from filename patterns."""
    # PXL_20260301_214715733
    m = re.match(r"PXL_(\d{4})(\d{2})(\d{2})_", filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    # IMG_20161210_134431
    m = re.match(r"IMG_(\d{4})(\d{2})(\d{2})_", filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    # 20150623_192417
    m = re.match(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}T{m.group(4)}:{m.group(5)}:{m.group(6)}"
    return ""


def date_from_album(album):
    """Extract year from album name like 'Photos from 2019'."""
    m = re.search(r"Photos from (\d{4})", album)
    if m:
        return f"{m.group(1)}-01-01"
    return ""


def safe_float(v):
    """Convert EXIF value to float safely."""
    if v is None:
        return None
    if hasattr(v, "numerator"):
        try:
            return float(v)
        except (ZeroDivisionError, OverflowError):
            return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def safe_int(v):
    """Convert EXIF value to int safely."""
    f = safe_float(v)
    if f is None:
        return None
    try:
        return int(f)
    except (ValueError, OverflowError):
        return None


def extract_exif(data):
    """Extract EXIF fields from image bytes."""
    try:
        img = Image.open(io.BytesIO(data))
        exif_raw = img._getexif()
        if not exif_raw:
            return {}
        exif = {TAGS.get(k, k): v for k, v in exif_raw.items()}

        result = {}
        result["make"] = (exif.get("Make", "") or "").strip().rstrip("\x00")
        result["model"] = (exif.get("Model", "") or "").strip().rstrip("\x00")
        result["date_taken"] = parse_exif_date(exif.get("DateTimeOriginal", ""))
        if not result["date_taken"]:
            result["date_taken"] = parse_exif_date(exif.get("DateTime", ""))
        result["f_number"] = safe_float(exif.get("FNumber"))
        result["focal_length"] = safe_float(exif.get("FocalLength"))
        result["focal_length_35mm"] = safe_int(exif.get("FocalLengthIn35mmFilm"))
        result["iso"] = safe_int(exif.get("ISOSpeedRatings"))
        result["exposure_time"] = safe_float(exif.get("ExposureTime"))
        result["lens_model"] = str(exif.get("LensModel", "")).strip() if exif.get("LensModel") else None
        result["software"] = str(exif.get("Software", "")).strip() if exif.get("Software") else None
        result["image_width"] = safe_int(exif.get("ExifImageWidth"))
        result["image_height"] = safe_int(exif.get("ExifImageHeight"))
        result["has_gps"] = 1 if "GPSInfo" in exif else 0
        result["exif_source"] = "exif" if result["make"] else "partial"
        return result
    except Exception:
        return {}


def infer_camera_from_filename(filename):
    """Infer camera type from filename patterns."""
    fn = filename.upper()
    if fn.startswith("PXL_"):
        return "Google", "Pixel (unknown model)"
    elif fn.startswith("IMG_") and fn.endswith(".HEIC"):
        return "Apple", "iPhone (unknown model)"
    elif fn.startswith("DSCN"):
        return "NIKON", "Unknown Nikon"
    elif fn.startswith("DSC") and not fn.startswith("DSCN"):
        return "SONY", "Unknown Sony"
    return "", ""


def scan_zip(zip_num):
    """Scan a single zip file and return list of photo records."""
    zip_path = os.path.join(ZIPS_DIR, ZIP_PATTERN.format(zip_num))
    if not os.path.exists(zip_path):
        return []

    records = []
    zf = zipfile.ZipFile(zip_path, "r")

    # Build sidecar map
    meta_map = {}
    for name in zf.namelist():
        if name.endswith(".supplemental-metadata.json"):
            photo_name = name.replace(".supplemental-metadata.json", "")
            meta_map[photo_name] = name

    for info in zf.infolist():
        if info.is_dir():
            continue

        name = info.filename
        ext = os.path.splitext(name)[1].lower()

        if ext in SKIP_EXTS or ext not in PHOTO_EXTS:
            continue

        parts = name.split("/")
        if len(parts) < 3:
            continue

        album = parts[2]
        filename = parts[-1]

        # Extract EXIF
        record = {
            "zip_num": zip_num,
            "filename": filename,
            "album": album,
            "ext": ext,
            "file_size": info.file_size,
            "make": "",
            "model": "",
            "date_taken": "",
            "f_number": None,
            "focal_length": None,
            "focal_length_35mm": None,
            "iso": None,
            "exposure_time": None,
            "lens_model": None,
            "software": None,
            "image_width": None,
            "image_height": None,
            "has_gps": 0,
            "exif_source": "unknown",
            "has_people": 0,
            "people_count": 0,
        }

        try:
            with zf.open(name) as f:
                data = f.read(EXIF_READ_SIZE)
                exif_data = extract_exif(data)
                record.update(exif_data)
        except Exception:
            pass

        # Fallback: infer camera from filename
        if not record["make"]:
            make, model = infer_camera_from_filename(filename)
            if make:
                record["make"] = make
                record["model"] = model
                record["exif_source"] = "filename"

        # Fallback: get date from sidecar / filename / album
        if not record["date_taken"]:
            meta_key = name
            if meta_key in meta_map:
                try:
                    meta = json.loads(zf.read(meta_map[meta_key]))
                    pt = meta.get("photoTakenTime", {})
                    record["date_taken"] = parse_sidecar_date(pt.get("formatted", ""))

                    # Also grab people info
                    people = meta.get("people", [])
                    record["has_people"] = 1 if people else 0
                    record["people_count"] = len(people)

                    # GPS from sidecar if not in EXIF
                    if not record["has_gps"]:
                        geo = meta.get("geoData", {})
                        if geo and (geo.get("latitude", 0) != 0 or geo.get("longitude", 0) != 0):
                            record["has_gps"] = 1
                except Exception:
                    pass

        if not record["date_taken"]:
            record["date_taken"] = date_from_filename(filename)

        if not record["date_taken"]:
            record["date_taken"] = date_from_album(album)

        # Also get sidecar people data even if we already have EXIF date
        if record["exif_source"] == "exif" and name in meta_map:
            try:
                meta = json.loads(zf.read(meta_map[name]))
                people = meta.get("people", [])
                record["has_people"] = 1 if people else 0
                record["people_count"] = len(people)
                if not record["has_gps"]:
                    geo = meta.get("geoData", {})
                    if geo and (geo.get("latitude", 0) != 0 or geo.get("longitude", 0) != 0):
                        record["has_gps"] = 1
            except Exception:
                pass

        records.append(record)

    zf.close()
    return records


def init_db():
    """Create SQLite database and tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS photos")
    c.execute("DROP TABLE IF EXISTS cameras")
    c.execute("DROP TABLE IF EXISTS camera_aliases")
    c.execute("DROP TABLE IF EXISTS scan_progress")

    c.execute("""
        CREATE TABLE photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip_num INTEGER NOT NULL,
            filename TEXT NOT NULL,
            album TEXT,
            ext TEXT NOT NULL,
            file_size INTEGER,
            make TEXT,
            model TEXT,
            date_taken TEXT,
            f_number REAL,
            focal_length REAL,
            focal_length_35mm REAL,
            iso INTEGER,
            exposure_time REAL,
            lens_model TEXT,
            software TEXT,
            image_width INTEGER,
            image_height INTEGER,
            has_gps INTEGER DEFAULT 0,
            exif_source TEXT,
            camera_id INTEGER,
            has_people INTEGER DEFAULT 0,
            people_count INTEGER DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE cameras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canonical_make TEXT NOT NULL,
            canonical_model TEXT NOT NULL,
            display_name TEXT NOT NULL,
            category TEXT,
            first_seen TEXT,
            last_seen TEXT,
            photo_count INTEGER DEFAULT 0,
            median_iso REAL,
            median_aperture REAL,
            median_focal_length REAL,
            median_focal_length_35mm REAL,
            min_aperture REAL,
            max_aperture REAL,
            pct_with_gps REAL,
            image_file TEXT
        )
    """)

    c.execute("""
        CREATE TABLE camera_aliases (
            raw_make TEXT NOT NULL,
            raw_model TEXT NOT NULL,
            camera_id INTEGER NOT NULL,
            FOREIGN KEY (camera_id) REFERENCES cameras(id),
            PRIMARY KEY (raw_make, raw_model)
        )
    """)

    c.execute("""
        CREATE TABLE scan_progress (
            zip_num INTEGER PRIMARY KEY,
            photo_count INTEGER,
            completed_at TEXT
        )
    """)

    conn.commit()
    return conn


def insert_records(conn, records):
    """Batch insert photo records."""
    c = conn.cursor()
    c.executemany("""
        INSERT INTO photos (zip_num, filename, album, ext, file_size,
            make, model, date_taken, f_number, focal_length, focal_length_35mm,
            iso, exposure_time, lens_model, software, image_width, image_height,
            has_gps, exif_source, has_people, people_count)
        VALUES (:zip_num, :filename, :album, :ext, :file_size,
            :make, :model, :date_taken, :f_number, :focal_length, :focal_length_35mm,
            :iso, :exposure_time, :lens_model, :software, :image_width, :image_height,
            :has_gps, :exif_source, :has_people, :people_count)
    """, records)
    conn.commit()


def main():
    max_workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    print(f"Initializing database at {DB_PATH}")
    conn = init_db()

    print(f"\nStarting EXIF scan of 15 zips with {max_workers} parallel workers...")
    t_start = time.time()

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_zip, z): z for z in range(1, 16)}

        for future in as_completed(futures):
            zip_num = futures[future]
            try:
                records = future.result()
                if records:
                    insert_records(conn, records)

                    # Track progress
                    c = conn.cursor()
                    c.execute(
                        "INSERT INTO scan_progress VALUES (?, ?, datetime('now'))",
                        (zip_num, len(records)),
                    )
                    conn.commit()

                    exif_count = sum(1 for r in records if r["exif_source"] == "exif")
                    print(
                        f"  Zip {zip_num:03d}: {len(records):,} photos "
                        f"({exif_count:,} with EXIF) - done",
                        flush=True,
                    )
                else:
                    print(f"  Zip {zip_num:03d}: no photos found", flush=True)
            except Exception as e:
                print(f"  Zip {zip_num:03d}: ERROR - {e}", flush=True)

    # Create indexes after bulk insert
    print("\nCreating indexes...")
    c = conn.cursor()
    c.execute("CREATE INDEX idx_photos_camera ON photos(camera_id)")
    c.execute("CREATE INDEX idx_photos_date ON photos(date_taken)")
    c.execute("CREATE INDEX idx_photos_make_model ON photos(make, model)")
    conn.commit()

    # Print summary
    c.execute("SELECT COUNT(*) FROM photos")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM photos WHERE exif_source = 'exif'")
    with_exif = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT make || '|' || model) FROM photos WHERE make != ''")
    unique_cameras = c.fetchone()[0]

    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"SCAN COMPLETE in {elapsed/60:.1f} minutes")
    print(f"{'='*60}")
    print(f"Total photos: {total:,}")
    print(f"With EXIF camera data: {with_exif:,}")
    print(f"Unique camera make/model combos: {unique_cameras}")
    print(f"Database: {DB_PATH}")

    # Quick camera breakdown
    print(f"\nTop 20 cameras by photo count:")
    for row in c.execute("""
        SELECT make, model, COUNT(*) as cnt
        FROM photos WHERE make != ''
        GROUP BY make, model
        ORDER BY cnt DESC LIMIT 20
    """):
        print(f"  {row[0]} {row[1]}: {row[2]:,}")

    conn.close()


if __name__ == "__main__":
    main()
