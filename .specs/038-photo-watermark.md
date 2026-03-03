# 038: Photography Watermark

**Branch**: `feature/photo-watermark`
**Created**: 2026-03-02

## Summary

Add a subtle "MrMatt.io" text watermark to all full-size photography images using Hugo's built-in `images.Text` filter. The watermark appears in the bottom-right corner with semi-transparent white text (~50% opacity). It applies only to the 1600px full-size images used in the lightbox — thumbnails (300x300) remain clean and unwatermarked.

## Requirements

- Watermark text: "MrMatt.io"
- Position: bottom-right corner with padding
- Style: white text, semi-transparent (~50% opacity), size ~20px
- Scope: full-size lightbox images only (not thumbnails)
- Applies to: all photography images (existing and new) — no per-image opt-in needed
- Works in both the gallery page (`/photography/`) and homepage photo strip lightbox
- No external tools or dependencies — uses Hugo's built-in `images.Text` filter
- No changes to content files — watermark is applied at build time via templates

## Design

Hugo's `images.Text` filter draws text directly onto images during the build pipeline. The watermark is applied after the image is resized to 1600px width, using the processed image's dimensions to calculate bottom-right positioning.

### Image Processing Pipeline (before)

```
photo.jpg → Process "resize 1600x webp q85" → full-size WebP
```

### Image Processing Pipeline (after)

```
photo.jpg → Process "resize 1600x webp q85" → Filter images.Text → watermarked full-size WebP
```

### Template Logic

Create a reusable partial `layouts/partials/photography/full-image.html` to encapsulate the watermark logic, keeping both templates DRY:

```go
{{- $img := . -}}
{{- $full := $img.Process "resize 1600x webp q85" -}}
{{- $full = $full.Filter (images.Text "MrMatt.io" (dict
    "color" "#ffffff80"
    "size" 20
    "x" (sub $full.Width 130)
    "y" (sub $full.Height 35)
)) -}}
{{- return $full -}}
```

Parameters:
- `color: "#ffffff80"` — white at 50% opacity (RRGGBBAA hex format)
- `size: 20` — font size in pixels, readable but not dominant
- `x: width - 130` — positions text ~10px from right edge (accounting for ~120px text width)
- `y: height - 35` — positions text ~15px from bottom edge (accounting for ~20px text height)

### Fallback Plan

If `images.Text` doesn't support alpha in the color hex (some Hugo versions may not), the fallback is to use `images.Overlay` with a pre-made semi-transparent PNG watermark stored in `assets/images/watermark.png`. This would be created with Python/PIL or ImageMagick.

## Files to Modify

| File | Change |
|------|--------|
| `layouts/partials/photography/full-image.html` | **New file** — partial that takes an image resource and returns a watermarked 1600px WebP |
| `layouts/photography/list.html` | Replace inline `$img.Process "resize 1600x webp q85"` with call to the watermark partial |
| `layouts/index.html` | Replace inline `$img.Process "resize 1600x webp q85"` (in both the photo strip `<a>` href and the `$photoJSON` loop) with call to the watermark partial |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [ ] Full-size images in gallery lightbox show "MrMatt.io" watermark in bottom-right
- [ ] Full-size images in homepage lightbox show "MrMatt.io" watermark in bottom-right
- [ ] Thumbnails in gallery grid do NOT have watermark
- [ ] Thumbnails in homepage photo strip do NOT have watermark
- [ ] Watermark is semi-transparent and subtle (not distracting)
- [ ] Watermark is readable against both light and dark photo backgrounds
