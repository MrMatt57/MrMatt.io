# 037: Fix Tropical Beach Day Photo Date

**Branch**: `feature/fix-beach-photo-date`
**Created**: 2026-03-03

## Summary

The "Tropical Beach Day" photography entry is incorrectly dated 2026-02-25 (when it was uploaded) but the EXIF data shows the photo was taken on 2018-04-18. Update the date in the front matter and rename the content folder to reflect the correct date so it sorts chronologically in the gallery.

## Requirements

- Change the date in `index.md` front matter from `2026-02-25` to `2018-04-18`
- Rename the content folder from `2026-02-25-tropical-beach-day` to `2018-04-18-tropical-beach-day`
- No other changes to the file content (title, alt, description remain the same)

## Design

Simple date correction: rename the folder and update the front matter date field. The folder naming convention `YYYY-MM-DD-slug` is used throughout the photography section, so the folder must be renamed to keep it consistent. This follows the same pattern as spec 024 (fix-brew-photo-date).

## Files to Modify

| File | Change |
|------|--------|
| `content/photography/2026-02-25-tropical-beach-day/index.md` | Update `date` field from `2026-02-25` to `2018-04-18` |
| `content/photography/2026-02-25-tropical-beach-day/` | Rename folder to `content/photography/2018-04-18-tropical-beach-day/` |

## Test Plan

- [x] Folder renamed to `2018-04-18-tropical-beach-day`
- [x] Front matter date reads `2018-04-18`
- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [x] Photo appears in the gallery sorted by the corrected 2018 date
