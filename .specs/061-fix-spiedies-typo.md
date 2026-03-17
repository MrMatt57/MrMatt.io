# 061: Fix Spiedies Typo

**Branch**: `feature/fix-spiedies-typo`
**Created**: 2026-03-15

## Summary

The most recent photography gallery entry misspells "spiedies" as "speedies" in the folder name, title, and description. Spiedies are a regional dish from Binghamton, NY — the correct spelling is "spiedies."

## Requirements

- Rename the photo directory from `2026-03-15-binghamton-speedies-grilling` to `2026-03-15-binghamton-spiedies-grilling`
- Fix the title from "Binghamton Speedies Grilling" to "Binghamton Spiedies Grilling"
- Fix the description text from "Speedies" to "Spiedies"

## Design

Simple find-and-replace across one `index.md` file plus a directory rename. No other files reference this photo entry since it was just added.

## Files to Modify

| File | Change |
|------|--------|
| `content/photography/2026-03-15-binghamton-speedies-grilling/` | Rename directory to `2026-03-15-binghamton-spiedies-grilling/` |
| `content/photography/2026-03-15-binghamton-spiedies-grilling/index.md` | Fix "Speedies" → "Spiedies" in title and description |

## Test Plan

- [x] Directory renamed correctly
- [x] Title reads "Binghamton Spiedies Grilling"
- [x] Description reads "Spiedies, a local Binghamton specialty..."
- [x] No other references to old folder name remain
- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
