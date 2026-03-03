# Spec 030: Font Preconnect Hints

## Summary

Add `<link rel="preconnect">` hints for Google Fonts domains to speed up font loading by ~100-300ms. The site uses Roboto Slab loaded via `@import` in CSS, which means the browser must first download the CSS, parse it, find the `@import`, then start the font connection. Preconnect hints let the browser establish the connection earlier, in parallel with CSS loading.

## Implementation

- Create `layouts/partials/extend_head.html` (PaperMod override hook) with preconnect links for:
  - `https://fonts.googleapis.com` (serves the CSS)
  - `https://fonts.gstatic.com` with `crossorigin` attribute (serves the font files)

## Files Changed

- `layouts/partials/extend_head.html` (new) — preconnect link elements
- `.specs/030-font-preconnect.md` (new) — this spec

## Test Plan

- [x] `hugo --minify` builds without errors
- [x] `public/index.html` contains `<link rel="preconnect" href="https://fonts.googleapis.com">`
- [x] `public/index.html` contains `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`
- [x] Preconnect links appear in `<head>` section of built HTML
