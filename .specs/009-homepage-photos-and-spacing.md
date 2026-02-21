# 009: Homepage Photography Section & Spacing Fix

**Branch**: `feature/homepage-photos-and-spacing`
**Created**: 2026-02-20

## Summary

Add a new Photography section to the home page below the Journal, featuring horizontally-scrolling thumbnails that open high-res images in a lightbox modal. Also fix spacing inconsistency between the Journal heading, tag filters, and post list, and simplify the tag filter links from 5 to 3.

## Requirements

- **Tag simplification**: Reduce home page tag filters from 5 (Everything, Software Dev, Travel, R/C Planes, Photography) to 3 (Everything, Software Dev, Travel)
- **Spacing fix**: Make the gap between "Journal" heading → tag filters equal to the gap between tag filters → post list (currently 0.5rem vs 1.5rem — normalize to ~1rem each)
- **Photography section**: Add a new section below the Journal separated by a horizontal rule divider, with:
  - "Photography" heading (same style as "Journal")
  - Horizontally-scrolling row of square thumbnail images
  - Clicking a thumbnail opens the full-res image in a lightbox modal overlay
  - Smooth scroll behavior, no scrollbar (or minimal styled scrollbar)
- **Photography content structure**: Use Hugo page bundles under `content/photography/` — each photo is its own folder with an `index.md` and the image file as a page resource
- **Lightbox**: Minimal inline JavaScript (~30-40 lines) for the modal — no external dependencies, no npm packages
- **Dark mode**: Photography section and lightbox must work in both light and dark themes
- **Accessibility**: Lightbox must be dismissible via Escape key and clicking outside the image; images must have alt text from front matter

## Design

### Content Structure

Each photo is a Hugo page bundle:

```
content/photography/
├── sunset-over-harbor/
│   ├── index.md          # front matter: title, date, image alt text
│   └── photo.jpg         # the actual photo (any filename works)
├── morning-coffee/
│   ├── index.md
│   └── photo.jpg
└── _index.md             # section list page (optional, for /photography/ URL)
```

**Front matter for each photo's `index.md`:**
```yaml
---
title: "Sunset Over Harbor"
date: "2026-02-20"
alt: "Orange sunset reflecting over the Inner Harbor"
draft: false
---
```

The template will use `.Resources.GetMatch "*.jpg" | default (.Resources.GetMatch "*.png")` to find the image file regardless of its exact name.

### Home Page Layout

The photography section mirrors the journal structure:

```
[Journal]
  h2 "Journal"
  tag filter links (Everything | Software Dev | Travel)
  post list (5 recent)

[hr divider]

[Photography]
  h2 "Photography"
  horizontal scroll container with thumbnail grid
```

### Thumbnail Strip

- Container: `overflow-x: auto` with horizontal scroll, `display: flex`, `gap: 0.75rem`
- Thumbnails: Square aspect ratio (e.g., 150×150px), `object-fit: cover`, `border-radius: 4px`
- Hide scrollbar on webkit/Firefox for clean look, but allow touch/mouse scroll
- On mobile, thumbnails shrink slightly (e.g., 120×120px)

### Lightbox Modal

- Full-viewport overlay with semi-transparent dark background (`rgba(0,0,0,0.85)`)
- Centered image scaled to fit viewport with padding (`max-width: 90vw`, `max-height: 90vh`)
- Close on: click overlay background, press Escape, click X button
- Minimal inline `<script>` at the bottom of the home page template
- No prev/next navigation (keep it simple for v1)

### Spacing Fix

Current CSS spacing chain for Journal section:
- `.home-journal h2` → `margin-bottom: 0`
- `.header-list` → `margin-top: 0.5rem`, `margin-bottom: 1.5rem`

Fix: Set `.header-list` margin to `1rem 0 1rem` to equalize spacing above and below the tag links.

### Sample Content

Create 3 placeholder photo page bundles with small sample JPEG images (or placeholder images) so the section is visible during development. These can be replaced with real photos later.

## Files to Modify

| File | Change |
|------|--------|
| `layouts/index.html` | Remove R/C Planes and Photography tag links; add Photography section with thumbnail strip and lightbox markup below Journal |
| `assets/css/extended/custom.css` | Fix `.header-list` margin for equal spacing; add `.home-photography` section styles, `.photo-strip` horizontal scroll, `.photo-thumb` thumbnail styles, `.lightbox-overlay` modal styles; dark mode variants |
| `content/photography/_index.md` | Create section index page for `/photography/` |
| `content/photography/sample-1/index.md` | Placeholder photo bundle 1 |
| `content/photography/sample-1/photo.jpg` | Placeholder image 1 |
| `content/photography/sample-2/index.md` | Placeholder photo bundle 2 |
| `content/photography/sample-2/photo.jpg` | Placeholder image 2 |
| `content/photography/sample-3/index.md` | Placeholder photo bundle 3 |
| `content/photography/sample-3/photo.jpg` | Placeholder image 3 |
| `hugo.toml` | Add "Photography" to menu (weight 15, between Journal and Now) |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [ ] Home page shows simplified tags: Everything, Software Dev, Travel (no R/C Planes, no Photography)
- [ ] Spacing between "Journal" heading → tags equals spacing between tags → post list
- [ ] Photography section appears below Journal with horizontal thumbnail strip
- [ ] Thumbnails scroll horizontally on overflow
- [ ] Clicking a thumbnail opens the lightbox with the full-res image
- [ ] Lightbox closes on Escape key, clicking outside image, and clicking X button
- [ ] Dark mode: photography section and lightbox render correctly
- [ ] Mobile: layout is responsive, thumbnails are appropriately sized
- [ ] `/photography/` URL shows a list/gallery page
