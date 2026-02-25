# 012: Smooth Lightbox Resize Transitions

**Branch**: `feature/smooth-lightbox-resize`
**Created**: 2026-02-24

## Summary

When navigating between photos in the lightbox, the image size changes cause a visible jolt — the title, rule, and description jump as the image wrapper resizes. Fix this by fading the entire content area (image + metadata) together so all layout shifts happen while the content is invisible.

## Requirements

- When navigating between photos, the entire image+metadata area should fade out, swap content, then fade in
- Title, description, and rule text should update during the invisible phase (not before)
- No visible layout shift during the transition
- First-open (clicking a thumbnail) should still fade in cleanly without an unnecessary fade-out delay
- Works on both the homepage lightbox and the /photography/ page lightbox

## Design

Currently only the `<img>` element fades via `.lightbox-img-loading`. The title/description update immediately (visible jump) and the image wrapper resizes at opacity 0 but the text below is still visible.

**Fix**: Fade the `.lightbox-img-and-meta` wrapper instead of just the image. This contains the image, title, rule, and description — everything that changes between photos. Move all content updates (src, alt, title, description, rule width) into the post-fade callback so they happen while invisible.

### CSS Changes
- Add `transition: opacity 0.15s ease` to `.lightbox-img-and-meta`
- Add `.lightbox-img-and-meta.lightbox-transitioning { opacity: 0; }`
- Remove `transition` from `.lightbox-img` (no longer needed for navigation)
- Remove `.lightbox-img.lightbox-img-loading` (replaced by wrapper class)

### JS Changes (both `layouts/index.html` and `layouts/photography/list.html`)
- Get reference to `.lightbox-img-and-meta` element
- In `showPhoto()`: move title/description/rule updates into the `applyImage` callback
- Replace `img.classList.add/remove('lightbox-img-loading')` with `imgAndMeta.classList.add/remove('lightbox-transitioning')`
- Nav visibility and hash updates can stay immediate (invisible during fade)

## Files to Modify

| File | Change |
|------|--------|
| `assets/css/extended/custom.css` | Add transition to `.lightbox-img-and-meta`, add `.lightbox-transitioning` class, remove image-level loading styles |
| `layouts/index.html` | Update lightbox JS to fade wrapper instead of image |
| `layouts/photography/list.html` | Update lightbox JS to fade wrapper instead of image |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Clicking a thumbnail opens lightbox with smooth fade-in (no delay)
- [ ] Navigating between photos fades entire content area (no visible layout jump)
- [ ] Title, description, and rule update during invisible phase
- [ ] Keyboard navigation (arrow keys) also transitions smoothly
- [ ] Close/escape still works correctly on both pages
