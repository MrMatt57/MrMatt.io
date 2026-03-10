# 047: Curation Post Gallery Link & Preview Image

**Branch**: `feat/curation-post-gallery-link`
**Created**: 2026-03-09

## Summary

Add a gallery preview collage and call-to-action link to the "Curating 100K Google Photos" blog post, directing readers to the photography gallery.

## Requirements

- Generate a preview collage image from gallery photos (grid of best shots)
- Add the collage to the blog post as a clickable image linking to `/photography/`
- Include a text CTA encouraging readers to visit the gallery
- Image stored in `static/images/` following existing convention

## Test Plan

- [ ] Collage image renders in the blog post
- [ ] Image links to `/photography/`
- [ ] Post still builds without errors
- [ ] Image is reasonably sized (< 500KB)
