# 059: Auto-Generated OG Images

**Branch**: `feature/og-images`
**Created**: 2026-03-12

## Summary

Auto-generate Open Graph social preview images for blog posts that don't have custom images. Uses Hugo's `images.Text` to render post title and description on a dark background with Roboto Slab font, matching the manually created style of "The Membrane" OG image. Posts with existing `images:` or `cover:` front matter keep their custom images.

## Files to Modify

| File | Change |
|------|--------|
| `assets/images/og-background.png` | 1200x630 dark background (#2e2e33) |
| `assets/fonts/RobotoSlab-Bold.ttf` | Bold weight for titles |
| `assets/fonts/RobotoSlab-Regular.ttf` | Regular weight for descriptions |
| `layouts/partials/og-image.html` | Partial that generates OG images with text overlay |
| `layouts/partials/extend_head.html` | Wire auto-generated OG images for posts without custom images |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Posts without custom images get auto-generated OG images
- [x] Posts with `images:` (The Membrane) keep their custom OG image
- [x] Posts with `cover:` keep their cover image
- [x] Generated images have correct title, description, and branding
- [x] Long titles wrap correctly across multiple lines
- [ ] Site renders correctly on localhost (`hugo server -D`)
