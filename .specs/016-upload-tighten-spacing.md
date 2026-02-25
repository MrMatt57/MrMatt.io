# 016: Tighten Upload AI Field Heights

**Branch**: `feature/upload-tighten-spacing`
**Created**: 2026-02-24

## Summary

Reduce the row count on the read-only alt text and description textareas in the photo upload page. Since these are no longer editable, the large heights (`rows="4"` and `rows="8"`) waste space. Shrink them to fit typical AI output while keeping the feedback textarea at its current size.

## Requirements

- Reduce alt text textarea from `rows="4"` to `rows="2"`
- Reduce description textarea from `rows="8"` to `rows="3"`
- Keep feedback textarea at `rows="4"` (unchanged)
- Bump cache-bust query params to `?v=6` and SW cache to `photo-upload-v6`

## Design

### HTML changes (`static/upload/index.html`)
- Line 46: `rows="4"` → `rows="2"` on `#ai-alt`
- Line 50: `rows="8"` → `rows="3"` on `#ai-description`
- Update `?v=5` → `?v=6` on style.css and app.js references

### SW changes (`static/upload/sw.js`)
- Bump `photo-upload-v5` → `photo-upload-v6`

## Files to Modify

| File | Change |
|------|--------|
| `static/upload/index.html` | Reduce textarea rows, bump cache-bust to v6 |
| `static/upload/sw.js` | Bump cache to v6 |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Alt text area is compact (2 rows)
- [x] Description area is compact (3 rows)
- [x] Feedback textarea unchanged (4 rows)
- [x] Service worker cache is v6
