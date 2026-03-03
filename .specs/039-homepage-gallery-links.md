# 039: Homepage Photos Link to Gallery

**Branch**: `feature/homepage-gallery-links`
**Created**: 2026-03-03

## Summary

Homepage photo thumbnails currently link to raw WebP files with a duplicated inline lightbox. Replace this with simple links to `/photography/#slug` so clicking a homepage photo navigates to the photography gallery page, where the existing deep-link hash system auto-opens the lightbox for that photo. This eliminates ~130 lines of duplicated lightbox code and provides the full gallery experience.

## Requirements

- Clicking a homepage photo thumbnail navigates to `/photography/#slug` (the photo's content basename)
- No lightbox HTML or JavaScript on the homepage
- No-JS fallback: thumbnails link to the gallery page (not raw WebP files)
- The photography page's existing hash-based deep linking handles opening the correct photo
- The "Gallery ->" link at the end of the photo strip remains unchanged

## Design

1. **Simplify homepage thumbnail links**: Change `href="{{ $full.RelPermalink }}"` to `href="/photography/#{{ .File.ContentBaseName }}"` on each `<a class="photo-thumb-link">` element
2. **Remove data attributes**: The `data-slug`, `data-alt`, `data-title`, `data-description` attributes are no longer needed on homepage thumbnails since the lightbox is on the photography page
3. **Remove full-size image processing**: The `$full` variable is no longer needed on the homepage since we're not linking to the WebP file
4. **Remove lightbox HTML block**: Delete the entire `<div id="lightbox">` block from `index.html`
5. **Remove lightbox JavaScript**: Delete the entire `<script>` block and the `$photoJSON` construction from `index.html`

## Files to Modify

| File | Change |
|------|--------|
| `layouts/index.html` | Remove lightbox HTML, JS, and photo JSON; simplify thumbnail links to `/photography/#slug`; remove full-size image processing |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Homepage renders correctly with photo strip thumbnails visible
- [ ] Clicking a homepage photo navigates to `/photography/#slug`
- [ ] The photography page lightbox auto-opens for the deep-linked photo
- [ ] Arrow key / button navigation works in the gallery after entering from homepage
- [ ] "Gallery ->" link still works
- [x] No-JS fallback: thumbnail links go to `/photography/#slug` (not raw WebP)
- [x] No console errors on the homepage
