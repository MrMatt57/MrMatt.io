"""Normalize camera Make/Model strings and compute aggregate stats.
Run after scan_camera_exif_v2.py has populated the photos table."""
import sqlite3
import re

DB_PATH = "F:/Photos/pipeline/camera_timeline.db"

# Map raw (make, model) → (canonical_make, canonical_model, display_name, category)
# None values mean "skip this camera" (scanners, video cameras, etc.)
CAMERA_MAP = {
    # Sony
    ("SONY", "DSC-V1"): ("Sony", "Cyber-shot DSC-V1", "Sony Cyber-shot DSC-V1", "compact"),
    ("SONY", "DSC-P100"): ("Sony", "Cyber-shot DSC-P100", "Sony Cyber-shot DSC-P100", "compact"),
    ("SONY", "DSC-W150"): ("Sony", "Cyber-shot DSC-W150", "Sony Cyber-shot DSC-W150", "compact"),
    ("SONY", "DSC-RX100"): ("Sony", "RX100", "Sony RX100", "compact"),
    # Canon — strip redundant "Canon " prefix from model
    ("Canon", "Canon PowerShot SX110 IS"): ("Canon", "PowerShot SX110 IS", "Canon PowerShot SX110 IS", "compact"),
    ("Canon", "Canon PowerShot A2000 IS"): ("Canon", "PowerShot A2000 IS", "Canon PowerShot A2000 IS", "compact"),
    ("Canon", "Canon PowerShot SX200 IS"): ("Canon", "PowerShot SX200 IS", "Canon PowerShot SX200 IS", "compact"),
    ("Canon", "Canon PowerShot SD400"): ("Canon", "PowerShot SD400", "Canon PowerShot SD400", "compact"),
    ("Canon", "Canon PowerShot SD1000"): ("Canon", "PowerShot SD1000", "Canon PowerShot SD1000", "compact"),
    ("Canon", "Canon PowerShot A75"): ("Canon", "PowerShot A75", "Canon PowerShot A75", "compact"),
    ("Canon", "Canon PowerShot A520"): ("Canon", "PowerShot A520", "Canon PowerShot A520", "compact"),
    ("Canon", "Canon PowerShot A640"): ("Canon", "PowerShot A640", "Canon PowerShot A640", "compact"),
    ("Canon", "Canon EOS DIGITAL REBEL XTi"): ("Canon", "EOS Rebel XTi", "Canon EOS Rebel XTi", "dslr"),
    ("Canon", "Canon EOS REBEL T3i"): ("Canon", "EOS Rebel T3i", "Canon EOS Rebel T3i", "dslr"),
    ("Canon", "MX860 series"): None,  # scanner
    # Nikon
    ("NIKON CORPORATION", "NIKON D3100"): ("Nikon", "D3100", "Nikon D3100", "dslr"),
    ("NIKON CORPORATION", "NIKON D5200"): ("Nikon", "D5200", "Nikon D5200", "dslr"),
    # Samsung
    ("samsung", "SPH-L900"): ("Samsung", "Galaxy Note II", "Samsung Galaxy Note II", "phone"),
    ("SAMSUNG", "SPH-L900"): ("Samsung", "Galaxy Note II", "Samsung Galaxy Note II", "phone"),
    ("samsung", "SM-G920V"): ("Samsung", "Galaxy S6", "Samsung Galaxy S6", "phone"),
    ("SAMSUNG", "SM-G920V"): ("Samsung", "Galaxy S6", "Samsung Galaxy S6", "phone"),
    ("samsung", "SM-N910V"): ("Samsung", "Galaxy Note 4", "Samsung Galaxy Note 4", "phone"),
    ("SAMSUNG", "SM-N910V"): ("Samsung", "Galaxy Note 4", "Samsung Galaxy Note 4", "phone"),
    ("SAMSUNG", "SM-T710"): ("Samsung", "Galaxy Tab S2", "Samsung Galaxy Tab S2", "tablet"),
    ("samsung", "SM-T710"): ("Samsung", "Galaxy Tab S2", "Samsung Galaxy Tab S2", "tablet"),
    # Motorola
    ("Motorola", "XT1096"): ("Motorola", "Moto X (2nd Gen)", "Motorola Moto X (2nd Gen)", "phone"),
    ("Motorola", "XT1056"): ("Motorola", "Moto X (1st Gen)", "Motorola Moto X (1st Gen)", "phone"),
    # LG / Huawei / Asus
    ("LGE", "Nexus 5X"): ("LG", "Nexus 5X", "LG Nexus 5X", "phone"),
    ("Huawei", "Nexus 6P"): ("Huawei", "Nexus 6P", "Huawei Nexus 6P", "phone"),
    ("asus", "Nexus 7"): ("Asus", "Nexus 7", "Asus Nexus 7", "tablet"),
    # Google Pixels
    ("Google", "Pixel XL"): ("Google", "Pixel XL", "Google Pixel XL", "phone"),
    ("Google", "Pixel 2 XL"): ("Google", "Pixel 2 XL", "Google Pixel 2 XL", "phone"),
    ("Google", "Pixel 3 XL"): ("Google", "Pixel 3 XL", "Google Pixel 3 XL", "phone"),
    ("Google", "Pixel 5"): ("Google", "Pixel 5", "Google Pixel 5", "phone"),
    ("Google", "Pixel 6a"): ("Google", "Pixel 6a", "Google Pixel 6a", "phone"),
    ("Google", "Pixel 6 Pro"): ("Google", "Pixel 6 Pro", "Google Pixel 6 Pro", "phone"),
    ("Google", "Pixel 8 Pro"): ("Google", "Pixel 8 Pro", "Google Pixel 8 Pro", "phone"),
    ("Google", "Pixel 8a"): ("Google", "Pixel 8a", "Google Pixel 8a", "phone"),
    ("Google", "Pixel 9 Pro XL"): ("Google", "Pixel 9 Pro XL", "Google Pixel 9 Pro XL", "phone"),
    ("Google", "Pixel 10 Pro XL"): ("Google", "Pixel 10 Pro XL", "Google Pixel 10 Pro XL", "phone"),
    # DJI
    ("DJI", "FC7203"): ("DJI", "Mavic Mini", "DJI Mavic Mini", "drone"),
    # Kodak
    ("EASTMAN KODAK COMPANY", "KODAK C875 ZOOM DIGITAL CAMERA"): ("Kodak", "EasyShare C875", "Kodak EasyShare C875", "compact"),
    ("EASTMAN KODAK COMPANY", "KODAK DX4900 ZOOM DIGITAL CAMERA"): ("Kodak", "EasyShare DX4900", "Kodak EasyShare DX4900", "compact"),
    # Pentax
    ("PENTAX Corporation", "PENTAX Optio S6"): ("Pentax", "Optio S6", "Pentax Optio S6", "compact"),
    ("PENTAX Corporation", "PENTAX Optio S5z"): ("Pentax", "Optio S5z", "Pentax Optio S5z", "compact"),
    ("PENTAX Corporation", "PENTAX Optio 30"): ("Pentax", "Optio 30", "Pentax Optio 30", "compact"),
    ("PENTAX Corporation", "PENTAX Optio S"): ("Pentax", "Optio S", "Pentax Optio S", "compact"),
    # Casio
    ("CASIO COMPUTER CO.,LTD.", "EX-S2"): ("Casio", "Exilim EX-S2", "Casio Exilim EX-S2", "compact"),
    ("CASIO COMPUTER CO.,LTD", "EX-S2"): ("Casio", "Exilim EX-S2", "Casio Exilim EX-S2", "compact"),
    # Konica Minolta
    ("KONICA MINOLTA", "MAXXUM 5D"): ("Konica Minolta", "Maxxum 5D", "Konica Minolta Maxxum 5D", "dslr"),
    # Sony Ericsson
    ("Sony Ericsson", "Z750a"): ("Sony Ericsson", "Z750a", "Sony Ericsson Z750a", "phone"),
    # Apple
    ("Apple", "iPhone 3GS"): ("Apple", "iPhone 3GS", "Apple iPhone 3GS", "phone"),
    ("Apple", "iPhone 4"): ("Apple", "iPhone 4", "Apple iPhone 4", "phone"),
    ("Apple", "iPad"): ("Apple", "iPad", "Apple iPad", "tablet"),
    # Additional Canon (strip "Canon Canon" prefix)
    ("Canon", "Canon PowerShot SD600"): ("Canon", "PowerShot SD600", "Canon PowerShot SD600", "compact"),
    ("Canon", "Canon PowerShot SD450"): ("Canon", "PowerShot SD450", "Canon PowerShot SD450", "compact"),
    ("Canon", "Canon PowerShot A640"): ("Canon", "PowerShot A640", "Canon PowerShot A640", "compact"),
    ("Canon", "Canon EOS 5D Mark II"): ("Canon", "EOS 5D Mark II", "Canon EOS 5D Mark II", "dslr"),
    ("Canon", "Canon EOS 5D Mark III"): ("Canon", "EOS 5D Mark III", "Canon EOS 5D Mark III", "dslr"),
    ("Canon", "Canon EOS 5D Mark IV"): ("Canon", "EOS 5D Mark IV", "Canon EOS 5D Mark IV", "dslr"),
    ("Canon", "Canon EOS REBEL T3i"): ("Canon", "EOS Rebel T3i", "Canon EOS Rebel T3i", "dslr"),
    # Additional Nikon
    ("NIKON CORPORATION", "NIKON D3000"): ("Nikon", "D3000", "Nikon D3000", "dslr"),
    # Additional Kodak
    ("EASTMAN KODAK COMPANY", "KODAK EASYSHARE M893 IS DIGITAL CAMERA"): ("Kodak", "EasyShare M893", "Kodak EasyShare M893", "compact"),
    ("EASTMAN KODAK COMPANY", "KODAK EASYSHARE C533 ZOOM DIGITAL CAMERA"): ("Kodak", "EasyShare C533", "Kodak EasyShare C533", "compact"),
    # Additional Apple
    ("Apple", "iPad Air"): ("Apple", "iPad Air", "Apple iPad Air", "tablet"),
    ("Apple", "iPhone"): ("Apple", "iPhone (1st Gen)", "Apple iPhone (1st Gen)", "phone"),
    ("Apple", "iPhone 3G"): ("Apple", "iPhone 3G", "Apple iPhone 3G", "phone"),
    ("Apple", "iPhone 4S"): ("Apple", "iPhone 4S", "Apple iPhone 4S", "phone"),
    ("Apple", "iPhone 5c"): ("Apple", "iPhone 5c", "Apple iPhone 5c", "phone"),
    ("Apple", "iPhone 5s"): ("Apple", "iPhone 5s", "Apple iPhone 5s", "phone"),
    ("Apple", "iPhone 6"): ("Apple", "iPhone 6", "Apple iPhone 6", "phone"),
    ("Apple", "iPhone 6s"): ("Apple", "iPhone 6s", "Apple iPhone 6s", "phone"),
    ("Apple", "iPhone 6s Plus"): ("Apple", "iPhone 6s Plus", "Apple iPhone 6s Plus", "phone"),
    ("Apple", "iPhone 7"): ("Apple", "iPhone 7", "Apple iPhone 7", "phone"),
    ("Apple", "iPhone 8"): ("Apple", "iPhone 8", "Apple iPhone 8", "phone"),
    ("Apple", "iPhone X"): ("Apple", "iPhone X", "Apple iPhone X", "phone"),
    ("Apple", "iPhone XR"): ("Apple", "iPhone XR", "Apple iPhone XR", "phone"),
    ("Apple", "iPhone 11"): ("Apple", "iPhone 11", "Apple iPhone 11", "phone"),
    ("Apple", "iPhone 12 mini"): ("Apple", "iPhone 12 mini", "Apple iPhone 12 mini", "phone"),
    ("Apple", "iPhone 16"): ("Apple", "iPhone 16", "Apple iPhone 16", "phone"),
    ("Apple", "iPhone 16 Pro"): ("Apple", "iPhone 16 Pro", "Apple iPhone 16 Pro", "phone"),
    ("Apple", "iPhone (unknown model)"): None,  # too few to matter
    # Additional Sony
    ("SONY", "ILCE-6000"): ("Sony", "A6000", "Sony A6000", "mirrorless"),
    ("SONY", "Unknown Sony"): None,
    # Additional DJI
    ("DJI", "FC330"): ("DJI", "Phantom 4", "DJI Phantom 4", "drone"),
    # Additional Google
    ("Google", "Pixel 4 XL"): ("Google", "Pixel 4 XL", "Google Pixel 4 XL", "phone"),
    # Additional Samsung
    ("samsung", "Galaxy S24"): ("Samsung", "Galaxy S24", "Samsung Galaxy S24", "phone"),
    ("samsung", "SM-G930V"): ("Samsung", "Galaxy S7", "Samsung Galaxy S7", "phone"),
    # GoPro
    ("GoPro", "HERO5 Session"): ("GoPro", "HERO5 Session", "GoPro HERO5 Session", "action"),
    # Skip entries
    ("Hipstamatic", "226"): None,  # iOS app, not a camera
    ("http://photogrid.org", ""): None,  # app
    ("Fast Burst Camera Lite for Android ghost_sprint", "Fast Burst Camera Lite for Android ghost_sprint"): None,
    ("Google", "Osmo Mobile"): None,  # gimbal, not a camera
    ("Google", "Osmo Mobile 2"): None,  # gimbal
    ("HTC", "PB99400"): None,  # too few
    ("Nokia", "Lumia 635"): None,  # too few
    ("OLYMPUS IMAGING CORP.", "FE310,X840,C530"): None,  # too few
    ("ASUS", "P01M"): None,  # tablet, too few
    # Filename-inferred (will be resolved by date range)
    ("Google", "Pixel (unknown model)"): None,  # resolved below
    # Skip entries
    ("QCOM-AA", "QCAM-AA"): None,
    ("Panasonic", "HDC-SD1"): None,  # video camera
}

# Pixel model date ranges for resolving "Pixel (unknown model)"
PIXEL_DATE_RANGES = [
    ("2016-10-01", "2017-10-01", "Google", "Pixel XL"),
    ("2017-10-01", "2018-10-01", "Google", "Pixel 2 XL"),
    ("2018-10-01", "2020-09-01", "Google", "Pixel 3 XL"),
    ("2020-09-01", "2021-10-01", "Google", "Pixel 5"),
    ("2021-10-01", "2022-07-01", "Google", "Pixel 6 Pro"),
    ("2022-07-01", "2023-10-01", "Google", "Pixel 6a"),  # or 6 Pro overlap
    ("2023-10-01", "2024-08-01", "Google", "Pixel 8 Pro"),
    ("2024-08-01", "2025-08-01", "Google", "Pixel 9 Pro XL"),
    ("2025-08-01", "2030-01-01", "Google", "Pixel 10 Pro XL"),
]


def resolve_pixel_model(date_taken):
    """Resolve 'Pixel (unknown model)' to a specific model based on date."""
    if not date_taken:
        return None, None
    for start, end, make, model in PIXEL_DATE_RANGES:
        if start <= date_taken < end:
            return make, model
    return "Google", "Pixel 9 Pro XL"  # default to latest


def get_or_create_camera(conn, make, model, display_name, category):
    """Get existing camera ID or create new one."""
    c = conn.cursor()
    c.execute("SELECT id FROM cameras WHERE canonical_make=? AND canonical_model=?",
              (make, model))
    row = c.fetchone()
    if row:
        return row[0]
    c.execute("""INSERT INTO cameras (canonical_make, canonical_model, display_name, category)
                 VALUES (?, ?, ?, ?)""", (make, model, display_name, category))
    conn.commit()
    return c.lastrowid


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Clear previous normalization
    c.execute("DELETE FROM cameras")
    c.execute("DELETE FROM camera_aliases")
    c.execute("UPDATE photos SET camera_id = NULL")
    conn.commit()

    # Get all unique make/model combos
    c.execute("""SELECT DISTINCT make, model, COUNT(*) as cnt
                 FROM photos WHERE make != ''
                 GROUP BY make, model ORDER BY cnt DESC""")
    raw_cameras = c.fetchall()

    print(f"Found {len(raw_cameras)} unique raw make/model combinations\n")

    # Phase 1: Map known cameras
    unmapped = []
    for raw_make, raw_model, count in raw_cameras:
        # Strip trailing null bytes and whitespace
        clean_make = raw_make.strip().rstrip("\x00")
        clean_model = raw_model.strip().rstrip("\x00")

        key = (clean_make, clean_model)
        if key in CAMERA_MAP:
            mapping = CAMERA_MAP[key]
            if mapping is None:
                if key == ("Google", "Pixel (unknown model)"):
                    continue  # handled in phase 2
                print(f"  SKIP: {clean_make} {clean_model} ({count} photos)")
                continue
            make, model, display_name, category = mapping
            cam_id = get_or_create_camera(conn, make, model, display_name, category)
            c.execute("""INSERT OR REPLACE INTO camera_aliases (raw_make, raw_model, camera_id)
                        VALUES (?, ?, ?)""", (raw_make, raw_model, cam_id))
            c.execute("UPDATE photos SET camera_id=? WHERE make=? AND model=?",
                      (cam_id, raw_make, raw_model))
            print(f"  MAP: {raw_make} {raw_model} -> {display_name} ({count} photos)")
        else:
            unmapped.append((raw_make, raw_model, count))

    conn.commit()

    # Phase 1b: Auto-map unmapped cameras with simple heuristics
    for raw_make, raw_model, count in unmapped:
        clean_make = raw_make.strip().rstrip("\x00")
        clean_model = raw_model.strip().rstrip("\x00")

        # Try case-insensitive match
        found = False
        for key, mapping in CAMERA_MAP.items():
            if (key[0].lower().strip() == clean_make.lower() and
                    key[1].lower().strip() == clean_model.lower()):
                if mapping is None:
                    print(f"  SKIP (fuzzy): {clean_make} {clean_model} ({count} photos)")
                    found = True
                    break
                make, model, display_name, category = mapping
                cam_id = get_or_create_camera(conn, make, model, display_name, category)
                c.execute("""INSERT OR REPLACE INTO camera_aliases (raw_make, raw_model, camera_id)
                            VALUES (?, ?, ?)""", (raw_make, raw_model, cam_id))
                c.execute("UPDATE photos SET camera_id=? WHERE make=? AND model=?",
                          (cam_id, raw_make, raw_model))
                print(f"  FUZZY MAP: {raw_make} {raw_model} → {display_name} ({count} photos)")
                found = True
                break

        if not found:
            # Auto-generate mapping for unknown cameras
            category = "other"
            if any(kw in clean_model.lower() for kw in ["phone", "pixel", "galaxy", "iphone", "nexus", "moto"]):
                category = "phone"
            elif any(kw in clean_model.lower() for kw in ["powershot", "cyber", "optio", "coolpix", "dsc"]):
                category = "compact"
            elif any(kw in clean_model.lower() for kw in ["eos", "d3", "d5", "d7", "rebel"]):
                category = "dslr"

            display_name = f"{clean_make} {clean_model}"
            cam_id = get_or_create_camera(conn, clean_make, clean_model, display_name, category)
            c.execute("""INSERT OR REPLACE INTO camera_aliases (raw_make, raw_model, camera_id)
                        VALUES (?, ?, ?)""", (raw_make, raw_model, cam_id))
            c.execute("UPDATE photos SET camera_id=? WHERE make=? AND model=?",
                      (cam_id, raw_make, raw_model))
            print(f"  AUTO: {raw_make} {raw_model} -> {display_name} [{category}] ({count} photos)")

    conn.commit()

    # Phase 2: Resolve "Pixel (unknown model)" by date
    c.execute("""SELECT id, date_taken FROM photos
                 WHERE make='Google' AND model='Pixel (unknown model)'""")
    unknown_pixels = c.fetchall()
    print(f"\nResolving {len(unknown_pixels)} 'Pixel (unknown model)' entries by date...")

    resolved = 0
    for photo_id, date_taken in unknown_pixels:
        make, model = resolve_pixel_model(date_taken)
        if make and model:
            # Find the camera_id for this model
            c.execute("SELECT id FROM cameras WHERE canonical_make=? AND canonical_model=?",
                      (make, model))
            row = c.fetchone()
            if row:
                c.execute("UPDATE photos SET camera_id=? WHERE id=?", (row[0], photo_id))
                resolved += 1

    conn.commit()
    print(f"  Resolved {resolved}/{len(unknown_pixels)} unknown Pixels")

    # Phase 3: Compute aggregate stats per camera
    print("\nComputing aggregate stats...")

    c.execute("SELECT id, display_name FROM cameras")
    cameras = c.fetchall()

    for cam_id, name in cameras:
        # Photo count
        c.execute("SELECT COUNT(*) FROM photos WHERE camera_id=?", (cam_id,))
        photo_count = c.fetchone()[0]

        # Date range
        c.execute("SELECT MIN(date_taken), MAX(date_taken) FROM photos WHERE camera_id=? AND date_taken != ''",
                  (cam_id,))
        first_seen, last_seen = c.fetchone()

        # Median ISO
        c.execute("""SELECT iso FROM photos WHERE camera_id=? AND iso IS NOT NULL
                     ORDER BY iso LIMIT 1 OFFSET (
                         SELECT COUNT(*)/2 FROM photos WHERE camera_id=? AND iso IS NOT NULL
                     )""", (cam_id, cam_id))
        row = c.fetchone()
        median_iso = row[0] if row else None

        # Median aperture
        c.execute("""SELECT f_number FROM photos WHERE camera_id=? AND f_number IS NOT NULL
                     ORDER BY f_number LIMIT 1 OFFSET (
                         SELECT COUNT(*)/2 FROM photos WHERE camera_id=? AND f_number IS NOT NULL
                     )""", (cam_id, cam_id))
        row = c.fetchone()
        median_aperture = row[0] if row else None

        # Min/max aperture
        c.execute("SELECT MIN(f_number), MAX(f_number) FROM photos WHERE camera_id=? AND f_number IS NOT NULL",
                  (cam_id,))
        min_ap, max_ap = c.fetchone()

        # Median focal length (35mm equiv)
        c.execute("""SELECT focal_length_35mm FROM photos WHERE camera_id=? AND focal_length_35mm IS NOT NULL
                     ORDER BY focal_length_35mm LIMIT 1 OFFSET (
                         SELECT COUNT(*)/2 FROM photos WHERE camera_id=? AND focal_length_35mm IS NOT NULL
                     )""", (cam_id, cam_id))
        row = c.fetchone()
        median_fl35 = row[0] if row else None

        # Median focal length (native)
        c.execute("""SELECT focal_length FROM photos WHERE camera_id=? AND focal_length IS NOT NULL
                     ORDER BY focal_length LIMIT 1 OFFSET (
                         SELECT COUNT(*)/2 FROM photos WHERE camera_id=? AND focal_length IS NOT NULL
                     )""", (cam_id, cam_id))
        row = c.fetchone()
        median_fl = row[0] if row else None

        # GPS percentage
        c.execute("SELECT COUNT(*) FROM photos WHERE camera_id=? AND has_gps=1", (cam_id,))
        gps_count = c.fetchone()[0]
        pct_gps = (gps_count / photo_count * 100) if photo_count > 0 else 0

        c.execute("""UPDATE cameras SET
                     photo_count=?, first_seen=?, last_seen=?,
                     median_iso=?, median_aperture=?, median_focal_length=?,
                     median_focal_length_35mm=?,
                     min_aperture=?, max_aperture=?, pct_with_gps=?
                     WHERE id=?""",
                  (photo_count, first_seen, last_seen,
                   median_iso, median_aperture, median_fl,
                   median_fl35,
                   min_ap, max_ap, pct_gps, cam_id))

    conn.commit()

    # Print final summary
    print(f"\n{'='*60}")
    print("NORMALIZATION COMPLETE")
    print(f"{'='*60}")

    c.execute("SELECT COUNT(*) FROM cameras WHERE photo_count > 0")
    active = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM photos WHERE camera_id IS NOT NULL")
    assigned = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM photos")
    total = c.fetchone()[0]

    print(f"Active cameras: {active}")
    print(f"Photos assigned to a camera: {assigned:,} / {total:,}")

    print(f"\nCamera Timeline:")
    for row in c.execute("""SELECT display_name, category, photo_count, first_seen, last_seen,
                                   median_iso, median_aperture, median_focal_length_35mm
                            FROM cameras WHERE photo_count > 0
                            ORDER BY first_seen"""):
        name, cat, count, first, last, iso, ap, fl = row
        first_y = first[:4] if first else "?"
        last_y = last[:4] if last else "?"
        stats = []
        if iso: stats.append(f"ISO {int(iso)}")
        if ap: stats.append(f"f/{ap:.1f}")
        if fl: stats.append(f"{int(fl)}mm")
        stats_str = " · ".join(stats) if stats else ""
        print(f"  {first_y}-{last_y}  {name} [{cat}] — {count:,} photos  {stats_str}")

    conn.close()


if __name__ == "__main__":
    main()
