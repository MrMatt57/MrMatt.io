# Spec: Photography EXIF Data Blog Posts

## Goal

Create two companion blog posts that analyze 22 years of personal photography through EXIF metadata extracted from ~94,000 Google Photos (Google Takeout export). The posts turn raw camera metadata into visual, data-driven narratives about gear evolution and shooting patterns.

## Data Source

- **Input:** 15 Google Takeout zip files (~723GB total) on `F:/Photos`
- **Format:** `takeout-20260307T015246Z-3-{001..015}.zip`
- **Extraction target:** EXIF headers (first 64KB per JPEG) + Google sidecar `.supplemental-metadata.json` files
- **Fields extracted:** make, model, date_taken, f_number, focal_length, focal_length_35mm, iso, exposure_time, lens_model, software, image_width, image_height, has_gps, has_people, people_count
- **Storage:** SQLite database at `F:/Photos/pipeline/camera_timeline.db` (not committed to repo)

## Pipeline (4 Python scripts in `tools/`)

### Step 1: `scan_camera_exif.py`
- Scans all 15 zips in parallel (3 workers, ~30 min runtime)
- Reads only first 64KB per file for EXIF extraction (uses Pillow)
- Falls back to Google sidecar JSON for date, GPS, and people metadata
- Falls back to filename patterns (PXL_, IMG_, timestamp) for dates
- Falls back to album name ("Photos from 2019") as last resort for dates
- Can infer camera make from filename prefix (PXL_ → Google Pixel, DSCN → Nikon)
- Creates `photos` table with all extracted fields, plus `cameras`, `camera_aliases`, `scan_progress` tables

### Step 2: `normalize_cameras.py`
- Maps raw EXIF make/model strings to canonical names (e.g., `"SM-N910V"` → `"Samsung Galaxy Note 4"`)
- ~130 explicit mappings in `CAMERA_MAP` dict covering Samsung model codes, Canon doubled prefixes, Kodak verbose names, etc.
- Assigns category: phone, compact, dslr, mirrorless, drone, action, tablet
- Resolves "Pixel (unknown model)" entries by date range (filename-inferred Pixels without EXIF model)
- Computes per-camera aggregate stats: photo_count, first_seen, last_seen, median ISO/aperture/focal length, GPS percentage
- Skips non-cameras: scanners (Canon MX860), apps (Hipstamatic), gimbals (Osmo Mobile), too-few entries

### Step 3: `export_camera_timeline.py` → `static/data/camera-timeline.json` (72KB)
Exports for Post 1:
- `summary`: total_photos (94,507), assigned_photos, exif_photos, year_range, scan_date
- `cameras[]`: per-camera objects with display_name, category, photo_count, first/last_seen, median stats
- `timeline{}`: year → camera_name → count (for stacked area chart)
- `monthly{}`: month → camera_name → count
- `yearly_totals{}`: year → total count
- `category_by_year{}`: year → {phone, compact, dslr, drone, action, tablet} counts
- `iso_by_year{}`, `resolution_by_year{}`

### Step 4: `export_photo_stats.py` → `static/data/photo-stats.json` (17KB)
Exports for Post 2:
- `yearly_totals{}`: year → count
- `monthly_volume{}`: YYYY-MM → count (heartbeat chart)
- `hourly{}`: hour (0-23) → count
- `day_of_week{}`: day name → count
- `heatmap{}`: day → hour → count (for canvas heatmap)
- `people_by_year{}`: year → {with_people, total}
- `gps_by_year{}`: year → {with_gps, total}
- `aperture_dist{}`: f-stop → count (top 20)
- `focal_dist{}`: focal length mm → count (top 15)
- `iso_by_year{}`, `iso_dist{}`: ISO trends and buckets
- `exposure_dist{}`: shutter speed buckets → count
- `resolution_by_year{}`: year → avg megapixels
- `top_camera_by_year{}`, `active_cameras_by_year{}`, `busiest_months[]`

### Supporting: `download_camera_images.py`
- Downloads product images for each camera (GSMArena for phones, Wikimedia Commons for cameras)
- Processes to consistent style: 200x150px, white background, grayscale, WebP
- ~65 camera images in `static/images/camera-timeline/`
- Has retry logic, rate limiting, fallback URLs per camera

## Blog Posts

### Post 1: "Every Camera I've Ever Owned" (`content/posts/2026-03_camera-gear-timeline.md`)
- **Slug:** `camera-gear-timeline`
- **Tags:** photography, software-development
- **Narrative arc:** 22-year gear timeline from Kodak floppy-disk camera to Pixel 10 Pro XL
- **Key data points:** 40 owned cameras, 24 phones, 75 total cameras detected (including friends' shared photos)
- **Charts (Chart.js, inline `<script>`):**
  1. **Timeline stacked area:** cameras stacked by year, filtered to owned cameras with 50+ photos
  2. **Category stacked bar:** phone vs compact vs DSLR vs drone by year — shows the phone takeover around 2013
  3. **Camera cards:** per-camera cards with product image, date range, photo count, median stats, sparkline histogram showing activity across full timeline
- **Filtering logic:** `NOT_OWNED` array excludes friends' Apple iPhones, Canon 5D series, Sony A6000, DJI Phantom 4, etc. from the "my cameras" narrative
- **Theme awareness:** charts detect `data-theme` attribute for dark/light mode; page reloads on theme toggle via MutationObserver
- **Cross-links to:** Post 2 ("94,000 Photos by the Numbers")

### Post 2: "94,000 Photos by the Numbers" (`content/posts/2026-03_photography-by-the-numbers.md`)
- **Slug:** `photography-by-the-numbers`
- **Tags:** photography, software-development
- **Narrative arc:** what EXIF metadata reveals about shooting habits over 22 years
- **Charts (Chart.js + canvas, inline `<script>`):**
  1. **Yearly totals bar:** bell curve peaking at 2015 (13,816 photos)
  2. **Hour of day bar:** peaks at 10am
  3. **Day of week bar:** weekends dominate
  4. **Heatmap (raw canvas):** day × hour grid, custom-drawn (not Chart.js)
  5. **People percentage line:** drops from 70% (2016) to <2% post-2020
  6. **GPS percentage line:** rises with smartphones, peaks 91% (2017), then declines
  7. **Aperture horizontal bar:** top 10 f-stops, dominated by f/2.0
  8. **Focal length horizontal bar:** top 10, dominated by 27mm (phone sweet spot)
  9. **ISO over time line:** climbing as phones push into low-light
  10. **Resolution line:** megapixel plateau after 12MP
  11. **Exposure distribution horizontal bar:** shutter speed buckets
  12. **Monthly volume area (heartbeat):** 22 years of monthly photo counts, spikes = trips/events
- **Cross-links to:** Post 1 ("Every Camera I've Ever Owned")

## Static Assets

| Path | Description | Size |
|------|-------------|------|
| `static/js/chart.umd.min.js` | Chart.js v4 UMD bundle (self-hosted) | 207KB |
| `static/data/camera-timeline.json` | Post 1 chart data | 72KB |
| `static/data/photo-stats.json` | Post 2 chart data | 17KB |
| `static/images/camera-timeline/*.webp` | ~65 camera product images | ~2-8KB each |

## Design Decisions

1. **Self-hosted Chart.js** — no CDN, no npm, just a single JS file per CLAUDE.md constraints ("no client-side JavaScript beyond what PaperMod ships" — exception made for data posts)
2. **Inline `<script>` blocks** — charts live inside the markdown posts themselves, not in separate JS files; `fetch()` loads JSON at runtime
3. **Dark/light theme support** — all charts read `data-theme` attribute and adjust colors; MutationObserver triggers page reload on toggle
4. **Grayscale + accent palette** — monochrome charts with `#4c81b2` accent, matches PaperMod aesthetic
5. **Font: Roboto Slab** — consistent with site typography
6. **Camera cards with sparklines** — raw canvas sparkline histograms (not Chart.js) showing each camera's activity across the full 22-year span
7. **Owned vs. not-owned filtering** — front-end `NOT_OWNED` array filters friends' cameras from the timeline chart and camera cards
8. **No animations** — `animation: false` on all charts for performance and reduced motion preference
9. **Responsive** — aspect-ratio containers, responsive Chart.js, grid layouts for side-by-side charts

## Remaining Work (as of 2026-03-10)

- Posts are `draft: true` — need final review before publishing
- Consider whether the self-hosted Chart.js exception needs a note in CLAUDE.md
- Verify all camera images render (onerror handler hides missing ones)
- Test dark mode chart rendering
- Potential: add alt text / accessibility for chart data (screen readers can't read canvas)
