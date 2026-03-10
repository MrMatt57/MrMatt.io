"""Export normalized camera timeline data as JSON for the blog post.
Outputs to static/data/camera-timeline.json for inlining into the post."""
import sqlite3
import json
import os
from collections import defaultdict

DB_PATH = "F:/Photos/pipeline/camera_timeline.db"
OUTPUT_PATH = "static/data/camera-timeline.json"


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Summary stats
    c.execute("SELECT COUNT(*) FROM photos")
    total_photos = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM photos WHERE camera_id IS NOT NULL")
    assigned_photos = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM photos WHERE exif_source = 'exif'")
    exif_photos = c.fetchone()[0]
    c.execute("SELECT MIN(date_taken), MAX(date_taken) FROM photos WHERE date_taken != '' AND date_taken >= '2000'")
    row = c.fetchone()
    min_date = row[0][:4] if row[0] else "?"
    max_date = row[1][:4] if row[1] else "?"

    summary = {
        "total_photos": total_photos,
        "assigned_photos": assigned_photos,
        "exif_photos": exif_photos,
        "year_range": [int(min_date), int(max_date)],
        "scan_date": "2026-03-09",
    }

    # Cameras (ordered by first_seen)
    cameras = []
    for row in c.execute("""
        SELECT id, canonical_make, canonical_model, display_name, category,
               photo_count, first_seen, last_seen,
               median_iso, median_aperture, median_focal_length,
               median_focal_length_35mm, min_aperture, max_aperture,
               pct_with_gps
        FROM cameras WHERE photo_count > 0
        ORDER BY first_seen
    """):
        cam = dict(row)
        # Trim first/last to year-month
        cam["first_seen"] = cam["first_seen"][:7] if cam["first_seen"] else None
        cam["last_seen"] = cam["last_seen"][:7] if cam["last_seen"] else None
        # Round floats
        for k in ["median_aperture", "min_aperture", "max_aperture", "median_focal_length", "pct_with_gps"]:
            if cam[k] is not None:
                cam[k] = round(cam[k], 1)
        for k in ["median_iso", "median_focal_length_35mm"]:
            if cam[k] is not None:
                cam[k] = int(cam[k])
        cameras.append(cam)

    # Timeline: photos per year per camera
    timeline = defaultdict(lambda: defaultdict(int))
    for row in c.execute("""
        SELECT substr(p.date_taken, 1, 4) as year, c.display_name, COUNT(*) as cnt
        FROM photos p
        JOIN cameras c ON p.camera_id = c.id
        WHERE p.date_taken != '' AND year >= '2003' AND year <= '2026'
        GROUP BY year, c.display_name
        ORDER BY year
    """):
        timeline[row["year"]][row["display_name"]] = row["cnt"]

    # Monthly timeline (for the detailed chart)
    monthly = defaultdict(lambda: defaultdict(int))
    for row in c.execute("""
        SELECT substr(p.date_taken, 1, 7) as month, c.display_name, COUNT(*) as cnt
        FROM photos p
        JOIN cameras c ON p.camera_id = c.id
        WHERE p.date_taken != '' AND month >= '2003-01' AND month <= '2026-12'
        GROUP BY month, c.display_name
        ORDER BY month
    """):
        monthly[row["month"]][row["display_name"]] = row["cnt"]

    # Yearly totals
    yearly_totals = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 4) as year, COUNT(*) as cnt
        FROM photos
        WHERE date_taken != '' AND year >= '2003' AND year <= '2026'
        GROUP BY year ORDER BY year
    """):
        yearly_totals[row["year"]] = row["cnt"]

    # Category by year (phone vs compact vs dslr vs drone)
    category_by_year = defaultdict(lambda: defaultdict(int))
    for row in c.execute("""
        SELECT substr(p.date_taken, 1, 4) as year, c.category, COUNT(*) as cnt
        FROM photos p
        JOIN cameras c ON p.camera_id = c.id
        WHERE p.date_taken != '' AND year >= '2003' AND year <= '2026'
        GROUP BY year, c.category
        ORDER BY year
    """):
        category_by_year[row["year"]][row["category"]] = row["cnt"]

    # ISO trend by year
    iso_by_year = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 4) as year,
               AVG(iso) as avg_iso,
               COUNT(*) as cnt
        FROM photos
        WHERE date_taken != '' AND iso IS NOT NULL
              AND year >= '2003' AND year <= '2026'
        GROUP BY year ORDER BY year
    """):
        iso_by_year[row["year"]] = round(row["avg_iso"], 0)

    # Resolution trend by year (megapixels)
    resolution_by_year = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 4) as year,
               AVG(image_width * image_height / 1000000.0) as avg_mp
        FROM photos
        WHERE date_taken != '' AND image_width IS NOT NULL AND image_height IS NOT NULL
              AND year >= '2003' AND year <= '2026'
        GROUP BY year ORDER BY year
    """):
        resolution_by_year[row["year"]] = round(row["avg_mp"], 1)

    # Build output
    output = {
        "summary": summary,
        "cameras": cameras,
        "timeline": dict(timeline),
        "monthly": dict(monthly),
        "yearly_totals": yearly_totals,
        "category_by_year": dict(category_by_year),
        "iso_by_year": iso_by_year,
        "resolution_by_year": resolution_by_year,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"Exported to {OUTPUT_PATH}")
    print(f"  Total photos: {total_photos:,}")
    print(f"  Cameras: {len(cameras)}")
    print(f"  Years: {min_date}–{max_date}")
    print(f"  JSON size: {os.path.getsize(OUTPUT_PATH) / 1024:.1f} KB")

    conn.close()


if __name__ == "__main__":
    main()
