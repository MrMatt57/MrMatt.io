# 024: Fix Brew Photo Date

**Branch**: `feature/fix-brew-photo-date`
**Created**: 2026-03-02

## Summary

The "Backyard Brew Station" photography entry is incorrectly dated 2026-02-25 when the photo is actually from mid-2015. Update the date in the front matter and rename the content folder to reflect the correct date.

## Requirements

- Change the date in `index.md` front matter from `2026-02-25` to `2015-06-15`
- Rename the content folder from `2026-02-25-backyard-brew-station` to `2015-06-15-backyard-brew-station`
- No other changes to the file content (title, alt, description remain the same)

## Design

Simple date correction: rename the folder and update the front matter date field. The folder naming convention `YYYY-MM-DD-slug` is used throughout the photography section, so the folder must be renamed to keep it consistent.

## Files to Modify

| File | Change |
|------|--------|
| `content/photography/2026-02-25-backyard-brew-station/index.md` | Update `date` field from `2026-02-25` to `2015-06-15` |
| `content/photography/2026-02-25-backyard-brew-station/` | Rename folder to `content/photography/2015-06-15-backyard-brew-station/` |

## Test Plan

- [x] Folder renamed to `2015-06-15-backyard-brew-station`
- [x] Front matter date reads `2015-06-15`
- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [ ] Photo appears in the gallery sorted by the corrected 2015 date
