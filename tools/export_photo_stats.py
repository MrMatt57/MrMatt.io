"""Export photo statistics data as JSON for the 'Photos by the Numbers' post."""
import sqlite3
import json
import os
from collections import defaultdict

DB_PATH = "F:/Photos/pipeline/camera_timeline.db"
OUTPUT_PATH = "static/data/photo-stats.json"

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Hourly distribution
    hourly = {}
    for row in c.execute("""
        SELECT CAST(substr(date_taken, 12, 2) AS INTEGER) as hour, COUNT(*) as cnt
        FROM photos WHERE length(date_taken) >= 13 AND date_taken >= '2003'
        GROUP BY hour ORDER BY hour
    """):
        hourly[row['hour']] = row['cnt']

    # Day of week
    day_of_week = {}
    day_names = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    for row in c.execute("""
        SELECT CAST(strftime('%w', date_taken) AS INTEGER) as dow, COUNT(*) as cnt
        FROM photos WHERE date_taken != '' AND length(date_taken) >= 10 AND date_taken >= '2003'
        GROUP BY dow ORDER BY dow
    """):
        day_of_week[day_names[row['dow']]] = row['cnt']

    # Hour x Day heatmap
    heatmap = defaultdict(lambda: defaultdict(int))
    for row in c.execute("""
        SELECT CAST(strftime('%w', date_taken) AS INTEGER) as dow,
               CAST(substr(date_taken, 12, 2) AS INTEGER) as hour,
               COUNT(*) as cnt
        FROM photos WHERE length(date_taken) >= 13 AND date_taken >= '2003'
        GROUP BY dow, hour
    """):
        heatmap[day_names[row['dow']]][row['hour']] = row['cnt']

    # Monthly volume
    monthly_volume = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 7) as month, COUNT(*) as cnt
        FROM photos WHERE date_taken != '' AND month >= '2003-01' AND month <= '2026-12'
        GROUP BY month ORDER BY month
    """):
        monthly_volume[row['month']] = row['cnt']

    # People by year
    people_by_year = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 4) as year,
               SUM(CASE WHEN has_people = 1 THEN 1 ELSE 0 END) as with_people,
               COUNT(*) as total
        FROM photos WHERE date_taken != '' AND year >= '2003' AND year <= '2026'
        GROUP BY year ORDER BY year
    """):
        people_by_year[row['year']] = {
            'with_people': row['with_people'],
            'total': row['total']
        }

    # GPS by year
    gps_by_year = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 4) as year,
               SUM(CASE WHEN has_gps = 1 THEN 1 ELSE 0 END) as with_gps,
               COUNT(*) as total
        FROM photos WHERE date_taken != '' AND year >= '2003' AND year <= '2026'
        GROUP BY year ORDER BY year
    """):
        gps_by_year[row['year']] = {
            'with_gps': row['with_gps'],
            'total': row['total']
        }

    # Aperture distribution (top 20)
    aperture_dist = {}
    for row in c.execute("""
        SELECT ROUND(f_number, 1) as aperture, COUNT(*) as cnt
        FROM photos WHERE f_number IS NOT NULL AND f_number > 0
        GROUP BY aperture ORDER BY cnt DESC LIMIT 20
    """):
        aperture_dist[str(row['aperture'])] = row['cnt']

    # ISO by year
    iso_by_year = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 4) as year,
               AVG(iso) as avg_iso
        FROM photos WHERE date_taken != '' AND iso IS NOT NULL
              AND year >= '2003' AND year <= '2026'
        GROUP BY year ORDER BY year
    """):
        iso_by_year[row['year']] = round(row['avg_iso'], 0)

    # ISO distribution buckets
    iso_dist = {}
    for row in c.execute("""
        SELECT CASE
            WHEN iso <= 100 THEN '0-100'
            WHEN iso <= 200 THEN '101-200'
            WHEN iso <= 400 THEN '201-400'
            WHEN iso <= 800 THEN '401-800'
            WHEN iso <= 1600 THEN '801-1600'
            WHEN iso <= 3200 THEN '1601-3200'
            ELSE '3200+'
        END as bucket, MIN(iso) as min_iso, COUNT(*) as cnt
        FROM photos WHERE iso IS NOT NULL
        GROUP BY bucket ORDER BY min_iso
    """):
        iso_dist[row['bucket']] = row['cnt']

    # Focal length distribution (35mm equiv, top 15)
    focal_dist = {}
    for row in c.execute("""
        SELECT CAST(focal_length_35mm AS INTEGER) as fl, COUNT(*) as cnt
        FROM photos WHERE focal_length_35mm IS NOT NULL AND focal_length_35mm > 0
        GROUP BY fl ORDER BY cnt DESC LIMIT 15
    """):
        focal_dist[str(row['fl'])] = row['cnt']

    # Exposure time distribution
    exposure_dist = {}
    for row in c.execute("""
        SELECT CASE
            WHEN exposure_time < 0.001 THEN '<1/1000s'
            WHEN exposure_time < 0.004 THEN '1/250-1/1000'
            WHEN exposure_time < 0.017 THEN '1/60-1/250'
            WHEN exposure_time < 0.1 THEN '1/10-1/60'
            WHEN exposure_time < 1.0 THEN '0.1-1s'
            ELSE '>1s'
        END as speed, MIN(exposure_time) as min_exp, COUNT(*) as cnt
        FROM photos WHERE exposure_time IS NOT NULL AND exposure_time > 0
        GROUP BY speed ORDER BY min_exp
    """):
        exposure_dist[row['speed']] = row['cnt']

    # Resolution by year
    resolution_by_year = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 4) as year,
               ROUND(AVG(image_width * image_height / 1000000.0), 1) as avg_mp
        FROM photos WHERE date_taken != '' AND year >= '2003' AND year <= '2026'
              AND image_width IS NOT NULL AND image_height IS NOT NULL
        GROUP BY year ORDER BY year
    """):
        resolution_by_year[row['year']] = row['avg_mp']

    # Yearly totals
    yearly_totals = {}
    for row in c.execute("""
        SELECT substr(date_taken, 1, 4) as year, COUNT(*) as cnt
        FROM photos WHERE date_taken != '' AND year >= '2003' AND year <= '2026'
        GROUP BY year ORDER BY year
    """):
        yearly_totals[row['year']] = row['cnt']

    # Top camera per year
    top_camera_by_year = {}
    for row in c.execute("""
        SELECT substr(p.date_taken, 1, 4) as year, c.display_name, COUNT(*) as cnt
        FROM photos p JOIN cameras c ON p.camera_id = c.id
        WHERE p.date_taken != '' AND year >= '2003' AND year <= '2026'
        GROUP BY year, c.display_name
        ORDER BY year, cnt DESC
    """):
        if row['year'] not in top_camera_by_year:
            top_camera_by_year[row['year']] = row['display_name']

    # Active cameras per year
    active_cameras_by_year = {}
    for row in c.execute("""
        SELECT substr(p.date_taken, 1, 4) as year, COUNT(DISTINCT c.id) as cam_count
        FROM photos p JOIN cameras c ON p.camera_id = c.id
        WHERE p.date_taken != '' AND year >= '2003' AND year <= '2026'
        GROUP BY year ORDER BY year
    """):
        active_cameras_by_year[row['year']] = row['cam_count']

    # Busiest months with top camera
    busiest_months = []
    for row in c.execute("""
        SELECT month, cnt, top_cam FROM (
            SELECT substr(p.date_taken, 1, 7) as month,
                   COUNT(*) as cnt,
                   (SELECT c2.display_name FROM photos p2 JOIN cameras c2 ON p2.camera_id = c2.id
                    WHERE substr(p2.date_taken, 1, 7) = substr(p.date_taken, 1, 7)
                    GROUP BY c2.display_name ORDER BY COUNT(*) DESC LIMIT 1) as top_cam
            FROM photos p
            WHERE p.date_taken != '' AND month >= '2003-01'
            GROUP BY month ORDER BY cnt DESC LIMIT 10
        ) ORDER BY cnt DESC
    """):
        busiest_months.append({
            'month': row['month'],
            'count': row['cnt'],
            'top_camera': row['top_cam']
        })

    # Summary
    c.execute("SELECT COUNT(*) FROM photos")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT camera_id) FROM photos WHERE camera_id IS NOT NULL")
    unique_cameras = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM cameras WHERE category = 'phone' AND photo_count >= 10")
    phone_count = c.fetchone()[0]

    summary = {
        'total_photos': total,
        'unique_cameras': unique_cameras,
        'year_range': [2003, 2026],
        'total_phones': phone_count,
    }

    output = {
        'summary': summary,
        'yearly_totals': yearly_totals,
        'monthly_volume': monthly_volume,
        'hourly': hourly,
        'day_of_week': day_of_week,
        'heatmap': {k: dict(v) for k, v in heatmap.items()},
        'people_by_year': people_by_year,
        'gps_by_year': gps_by_year,
        'aperture_dist': aperture_dist,
        'iso_by_year': iso_by_year,
        'iso_dist': iso_dist,
        'focal_dist': focal_dist,
        'exposure_dist': exposure_dist,
        'resolution_by_year': resolution_by_year,
        'top_camera_by_year': top_camera_by_year,
        'active_cameras_by_year': active_cameras_by_year,
        'busiest_months': busiest_months,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)

    size = os.path.getsize(OUTPUT_PATH)
    print(f"Exported {OUTPUT_PATH} ({size/1024:.1f} KB)")
    print(f"  Total photos: {total:,}")
    print(f"  Unique cameras: {unique_cameras}")
    print(f"  Phones: {phone_count}")
    conn.close()

if __name__ == "__main__":
    main()
