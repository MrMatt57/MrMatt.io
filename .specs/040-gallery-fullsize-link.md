# 040: Gallery Full-Size Image Link

**Branch**: `feature/gallery-fullsize-link`
**Created**: 2026-03-03

## Summary

Add a magnifying glass (🔍+) icon to the photography lightbox view, positioned on the same row as the title but right-aligned within the image width. Clicking it opens the original full-resolution image in a new browser tab. This feature only appears in the lightbox on the photography gallery page — not on the homepage photo strip or in the thumbnail grid.

## Requirements

- Add a magnifying glass + icon to the lightbox title row
- Icon appears to the right of the title, within the image width boundary
- Title shifts to left-aligned (currently centered) to accommodate the icon
- Clicking the icon opens the original full-resolution JPG in a new browser tab
- Icon has a tooltip explaining its purpose (e.g., "View full-size image")
- Icon styling matches the gallery's dark aesthetic (white, subtle opacity)
- Does NOT appear on the homepage photo strip lightbox
- Does NOT appear in the thumbnail grid view
- Accessible: proper aria-label on the button

## Design

### Layout Change

Current lightbox metadata layout:
```
        Title (centered)
  ─────────────────────────
     Description (centered)
```

New lightbox metadata layout:
```
  Title                  🔍+
  ─────────────────────────
     Description (centered)
```

The title and magnifying glass share a flex row container constrained to the lightbox image width. The title is left-aligned and the icon is right-aligned.

### Image URL Strategy

Hugo will publish the original source image by referencing `$img.RelPermalink` (the unprocessed resource). This URL is stored in a `data-original` attribute on each gallery thumbnail link. When the magnifying glass is clicked, JavaScript opens this URL in a new tab via `window.open()`.

### SVG Icon

An inline SVG magnifying glass with a + sign inside the lens:
```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <circle cx="10" cy="10" r="7"/>
  <line x1="16" y1="16" x2="22" y2="22"/>
  <line x1="7" y1="10" x2="13" y2="10"/>
  <line x1="10" y1="7" x2="10" y2="13"/>
</svg>
```

## Files to Modify

| File | Change |
|------|--------|
| `layouts/photography/list.html` | Add `data-original` attr to thumbnail links; wrap title + icon in `.lightbox-title-row`; add magnifying glass button; update JS to set original URL and handle click |
| `assets/css/extended/custom.css` | Add `.lightbox-title-row` flex container; style `.lightbox-fullsize-btn`; adjust `.lightbox-title` alignment |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [ ] Magnifying glass icon appears in lightbox view on the photography page
- [ ] Icon is right-aligned on the same row as the title, within image width
- [ ] Clicking the icon opens the original full-resolution image in a new tab
- [x] Icon does NOT appear on the homepage photo strip lightbox
- [ ] Icon has proper hover effect and tooltip
- [ ] Keyboard navigation still works (arrows, Escape)
- [ ] Title row width syncs with the image width on resize/navigation
