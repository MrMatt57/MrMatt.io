# 035: Photo Optimization with Hugo Image Processing

## Problem
Photography images are served as raw JPEGs (up to 8.9MB per photo, 39 photos total).
Gallery thumbnails are processed via `$img.Fill "300x300 q85"` but remain JPEG format.
Lightbox full-size images link directly to unprocessed originals (`photo.jpg`).
This causes slow page loads and excessive bandwidth usage.

## Solution
Use Hugo's built-in image processing to generate WebP versions at responsive sizes:
- **Thumbnails (gallery grid):** 300x300 WebP at q80 (was JPEG q85)
- **Lightbox full-size:** 1600px wide WebP at q85 (new — was raw original)
- **Homepage strip thumbnails:** 300x300 WebP at q80 (was JPEG q85)

Both the photography list template and the homepage template will be updated.

## Changes

### 1. Photography list template (`layouts/photography/list.html`)
- Thumbnail: `$img.Fill "300x300 webp q80"` (WebP format)
- Full-size link (`href`): `$img.Process "resize 1600x webp q85"` instead of raw original
- Add `loading="lazy"` (already present)

### 2. Homepage template (`layouts/index.html`)
- Photo strip thumbnails: `$img.Fill "300x300 webp q80"` (WebP format)
- Lightbox full-size (in photo JSON `src`): `$img.Process "resize 1600x webp q85"`
- Photo strip links (`href`): point to processed full-size WebP

### 3. CSP script hashes (`static/_headers`)
- Recompute SHA-256 hashes for inline scripts if photo JSON structure changes

### 4. Hugo config (`hugo.toml`)
- Add `[imaging]` config for WebP quality defaults

## Test Plan

- [x] Hugo builds successfully with `hugo --minify` (78 processed images)
- [x] WebP thumbnail files are generated in `public/` output (39 thumbnails)
- [x] WebP full-size files are generated in `public/` output (39 full-size)
- [x] Thumbnail file sizes are significantly smaller than original JPEGs (e.g. 8.9MB -> 31KB thumb)
- [x] Full-size WebP files are smaller than original JPEGs (e.g. 8.9MB -> 805KB, 11MB -> 428KB)
- [x] Photography gallery page renders correctly (0 raw JPEG refs, 78 WebP refs)
- [x] Homepage photo strip renders correctly (0 raw JPEG refs, 53 WebP refs)
- [x] Lightbox opens and displays optimized full-size images (JSON has 39 WebP entries)
- [x] CSP hashes are valid (8 hashes all match between build output and _headers)
- [x] No broken image references in HTML output (0 missing files)
