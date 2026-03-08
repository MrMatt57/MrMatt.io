# Photo Scorer

AI-powered pipeline to find your best photos from a large library (e.g., Google Photos) and rank them for your website portfolio.

## Pipeline

| Stage | What it does | Speed | Cost |
|-------|-------------|-------|------|
| **1. Scan** | Extract EXIF metadata from all photos | ~5K photos/min | Free |
| **2. Filter** | Pre-filter by resolution, camera, dedup | Instant | Free |
| **3. Score** | Claude Haiku rates each photo 1-10 | ~500 photos/min | ~$0.70/1K photos |
| **4. Rank** | Claude Sonnet deep-analyzes top candidates | ~60 photos/min | ~$10/1K photos |

Typical 200K library: **Scan** 200K → **Filter** ~25K → **Score** ~25K ($18) → **Rank** top 500 ($5) = **~$23 total**

## Setup

### 1. Install dependencies

```bash
cd tools/photo-scorer
pip install -r requirements.txt
```

### 2. Set your Anthropic API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Get your photos locally

#### Option A: rclone (recommended — incremental, selective)

```bash
# Install rclone: https://rclone.org/install/
# Windows: winget install Rclone.Rclone

# Configure Google Photos remote (one-time)
rclone config
# → New remote → name: gphotos → type: google photos → follow OAuth prompts

# List your albums
rclone lsd gphotos:album

# Sync everything (will take a while for 200K photos)
rclone sync gphotos:media /path/to/local/photos --progress

# Or sync a specific year folder / album
rclone sync gphotos:media --max-age 365d /path/to/local/photos/2025 --progress
rclone sync "gphotos:album/Vacation 2024" /path/to/local/photos/vacation-2024 --progress
```

**Recommended rclone strategy for large libraries:**
```bash
# Start with recent photos (most likely to be your best)
rclone sync gphotos:media /mnt/photos --max-age 730d --progress

# Run the scorer pipeline on those first
# Then expand to older photos if needed
```

#### Option B: Google Takeout (bulk one-time export)

1. Go to https://takeout.google.com
2. Deselect all, then select only **Google Photos**
3. Choose export format: **.zip**, max size **50GB**
4. Download all parts and extract to a folder
5. The script will automatically parse Takeout JSON sidecar metadata

### 4. Run the pipeline

```bash
# Full pipeline (scans, filters, pauses for cost approval, then scores + ranks)
python score_photos.py pipeline /path/to/local/photos

# Or run stages individually for more control:
python score_photos.py scan /path/to/local/photos
python score_photos.py filter --min-mp 6 --cameras "Canon" "Sony"
python score_photos.py costs                          # check costs before scoring
python score_photos.py score
python score_photos.py rank --top 1000
```

## Output

All output goes to `<photo_dir>/.photo-scorer/`:

| File | Description |
|------|-------------|
| `1_scan.json` | Full metadata for every photo |
| `2_filtered.json` | Pre-filtered candidates |
| `3_scored.json` | All photos with AI quick scores |
| `4_ranked.json` | Top photos with detailed scores |
| `4_ranked.csv` | Spreadsheet-friendly ranked list |

### Reading results

Open `4_ranked.csv` in Excel/Sheets — it has columns for every score dimension, category, description, tags, and file path. Sort by "Overall" to see your best photos.

## Resumability

Every stage saves progress incrementally. If the script crashes or you stop it, just run the same command again — it picks up where it left off.

## Filter options

```
--min-mp 4          Minimum megapixels (default: 4, increase to 8+ to be more selective)
--min-file-size     Minimum file size in bytes (default: 500KB)
--cameras "Canon"   Only include photos from these cameras
--exclude-cameras   Exclude photos from these cameras
--keep-screenshots  Don't auto-exclude detected screenshots
--no-dedup          Skip duplicate detection
```

## Scoring options

```
--batch-size 5      Photos per API call (default: 5, max ~10)
--model             Claude model for scoring (default: claude-haiku-4-5-20251001)
--rate-limit 0.1    Seconds between API calls
--top 500           How many top photos to send to detailed ranking
```

## Tips

- **Start small**: Run on a subset first (one album or one year) to calibrate
- **Use camera filter**: If you have a dedicated camera, filter to just that for portfolio shots
- **Adjust thresholds**: The default 4MP filter is conservative — raise to 8+ if you shoot high-res
- **Review the CSV**: The AI scores are a starting point — your eye is the final judge
- **Iterate**: Re-run rank with `--top 1000` if you want more candidates
