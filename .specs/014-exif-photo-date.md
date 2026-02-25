# 014: Extract EXIF Date for Photo Uploads

**Branch**: `feature/exif-photo-date`
**Created**: 2026-02-24

## Summary

When photos are uploaded via the PWA upload tool or added via the `/photo` skill, the date is hardcoded to today's date. This causes photos to appear out of order in the gallery. This feature extracts the actual capture date from JPEG EXIF metadata (`DateTimeOriginal`) and uses it for the front matter `date` field and folder name, falling back to today's date when EXIF data is unavailable.

## Requirements

- Extract `DateTimeOriginal` (or `DateTime` fallback) from JPEG EXIF metadata in the PWA upload tool
- Use the extracted date for both the folder name (`YYYY-MM-DD-slug`) and front matter `date` field
- Fall back to today's date when EXIF data is not available (PNGs, WebP, or JPEGs without EXIF)
- No external JavaScript libraries — implement a minimal EXIF parser inline
- Update the `/photo` skill to attempt EXIF date extraction via shell command before falling back to today's date

## Design

### PWA Upload Tool (`static/upload/app.js`)

Add a function `extractExifDate(file)` that:

1. Reads the file as an `ArrayBuffer`
2. Checks for JPEG SOI marker (`0xFFD8`)
3. Scans for APP1 marker (`0xFFE1`) containing EXIF data
4. Parses the TIFF header (handles both big-endian `MM` and little-endian `II` byte orders)
5. Walks IFD0 entries looking for the ExifIFD pointer (tag `0x8769`)
6. In the Exif IFD, looks for `DateTimeOriginal` (tag `0x9003`), falling back to `DateTime` (tag `0x0132`) in IFD0
7. Converts EXIF date format `YYYY:MM:DD HH:MM:SS` to `YYYY-MM-DD`
8. Returns `null` if no date found or file is not JPEG

The submit handler calls `extractExifDate(file)` before building the folder name. If it returns a date string, use it; otherwise use `new Date().toISOString().slice(0, 10)`.

### `/photo` Skill (`.claude/commands/photo.md`)

Update Step 3 to instruct Claude to:
1. Try extracting the EXIF date using `exiftool` or `python3` (whichever is available)
2. If extraction succeeds, use that date instead of today's date
3. If extraction fails, fall back to today's date

## Files to Modify

| File | Change |
|------|--------|
| `static/upload/app.js` | Add `extractExifDate()` function; update submit handler to use EXIF date |
| `.claude/commands/photo.md` | Update Step 3 to extract EXIF date before falling back to today |

## Test Plan

- [ ] Upload a JPEG photo with EXIF data via the PWA — verify the date matches the photo's capture date, not today
- [ ] Upload a PNG (no EXIF) — verify it falls back to today's date
- [ ] Verify the folder name uses the correct date prefix
- [ ] Verify the front matter `date` field uses the correct date
- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
- [ ] Gallery ordering is correct (photos sorted by actual capture date)
