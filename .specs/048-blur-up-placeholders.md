# 048: Blur-Up Placeholder Images

**Branch**: `feat/blur-up-placeholders`
**Created**: 2026-03-09

## Summary

Add blur-up placeholder images to the photography gallery so that lazy-loaded photos show a tiny blurred preview instead of empty space, transitioning smoothly to the sharp image once loaded.

## Context

The photography gallery currently uses `loading="lazy"` for thumbnail images and an IntersectionObserver-based progressive rendering system that reveals photos in batches as the user scrolls. When images are revealed but not yet loaded, the user sees empty space until the full thumbnail downloads. A blur-up placeholder improves perceived performance by immediately displaying a tiny, blurred version of each image.

## Requirements

### Hugo Image Processing (Build-Time)
- Generate a tiny (20px wide) version of each gallery thumbnail using Hugo's image processing pipeline
- Encode the tiny image as a base64 data URI for inline embedding
- No additional npm/node dependencies — use Hugo's built-in `Resize` and `base64Encode` only

### Gallery Grid (photography/list.html)
- Add a `background-image` CSS inline style on each `<img>` tag with the base64 LQIP data URI
- Apply CSS `background-size: cover` so the tiny image fills the thumbnail space
- When the real image loads, it naturally covers the blurred background
- Must work with the existing IntersectionObserver progressive rendering system

### Homepage Photo Strip (layouts/index.html)
- Apply the same blur-up treatment to the 7-photo strip on the homepage

### CSS
- Add a blur filter on the placeholder background using a wrapper element
- Smooth transition from blurred placeholder to sharp image via opacity fade
- Respect `prefers-reduced-motion` — skip animations for users who prefer reduced motion

### Constraints
- No npm/node dependencies
- No external JS frameworks — vanilla JS only, minimal additions
- Must not break existing lazy loading or lightbox functionality
- Must work with existing WebP image pipeline

## Implementation

### Approach
Use a CSS-based blur-up technique:
1. Hugo generates a tiny ~20px base64 image at build time
2. Each gallery thumbnail gets wrapped in a container that has the LQIP as a background image with CSS `filter: blur(20px)` and `background-size: cover`
3. The real `<img>` starts with `opacity: 0` and fades in via CSS transition when loaded
4. A small inline `onload` handler on each `<img>` adds a `loaded` class to trigger the opacity transition
5. Fallback: `<noscript>` isn't needed since the existing gallery already requires JS for progressive rendering

### Files Changed
- `layouts/photography/list.html` — wrap thumbnails with LQIP container, generate base64 placeholders
- `layouts/index.html` — same treatment for homepage photo strip
- `assets/css/extended/custom.css` — blur-up container styles and transitions

## Test Plan

- [ ] Gallery grid shows blurred placeholders before images load
- [ ] Smooth fade transition from placeholder to sharp image
- [ ] Homepage photo strip has same blur-up effect
- [ ] Lightbox still works correctly (click to open, navigation, close)
- [ ] Progressive rendering (IntersectionObserver) still works
- [ ] `prefers-reduced-motion` disables transition animations
- [ ] `hugo server` runs with no errors
- [ ] `hugo --minify` production build succeeds
- [ ] No npm/node dependencies added
