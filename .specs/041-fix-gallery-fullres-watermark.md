# 041: Fix Gallery Full-Res Watermark

**Branch**: `feature/fix-gallery-fullres-watermark`
**Created**: 2026-03-03

## Summary

The "Full Resolution" link in the photography lightbox serves the raw, unwatermarked source image. All images except thumbnails should have the watermark in the bottom-right corner. This fix creates a full-resolution watermarked version for the download link.

## Requirements

- Full Resolution link must serve a watermarked image (not the raw source)
- Watermark positioned in bottom-right corner with 15px padding (matching existing lightbox behavior)
- Full-res image resized to max 2400px wide (original dims cause WebP OOM), converted to WebP q90
- Raw source images must not be published/accessible
- Thumbnails (300x300) remain unwatermarked
- Lightbox display image (1600px) remains watermarked as-is

## Design

### New Partial: `fullres-image.html`

Create `layouts/partials/photography/fullres-image.html` that:
1. Takes an image resource as input
2. Resizes to max 2400px wide, converts to WebP at q90 quality
3. Overlays `assets/images/watermark.png` in bottom-right corner with 15px padding
4. Returns the processed image resource

### Template Change

In `layouts/photography/list.html`, replace:
```go
data-original="{{ $img.RelPermalink }}"
```
with:
```go
{{- $fullres := partial "photography/fullres-image.html" $img }}
data-original="{{ $fullres.RelPermalink }}"
```

This ensures `$img.RelPermalink` is never called, so Hugo won't publish the raw source.

## Files to Modify

| File | Change |
|------|--------|
| `layouts/partials/photography/fullres-image.html` | **New** — full-res watermark partial |
| `layouts/photography/list.html` | Replace `data-original` to use watermarked full-res |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
- [ ] Full Resolution link opens a watermarked image (not raw source)
- [ ] Watermark visible in bottom-right corner of full-res image
- [ ] Lightbox display image still watermarked at 1600px
- [ ] Thumbnails remain unwatermarked
- [ ] Homepage photo clicks still deep-link to gallery lightbox
- [ ] Gallery prev/next navigation works correctly
