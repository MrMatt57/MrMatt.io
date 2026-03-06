# 044: Custom 404 Page & Prefers-Reduced-Motion

**Branch**: `feature/404-and-reduced-motion`
**Created**: 2026-03-05

## Summary

Add a branded 404 page with the site avatar and a friendly message instead of the generic Cloudflare 404. Also add `prefers-reduced-motion: reduce` support to disable all CSS transitions and the lightbox JS transition, respecting users who have motion sensitivity.

## Requirements

- Custom 404 page with avatar, "Page not found" message, and link home
- 404 page should use the same layout/styling as the rest of the site (header, footer)
- `prefers-reduced-motion: reduce` disables all CSS `transition` properties
- Lightbox JS fade transition (150ms setTimeout in `showPhoto`) should be skipped when reduced motion is preferred
- The existing `prefers-reduced-motion` check in PaperMod's footer.html smooth scrolling should remain untouched

## Design

### 404 Page
Override PaperMod's minimal `layouts/404.html` with a branded version that:
- Uses Hugo Pipes to process the avatar (same as homepage: `Fit "350x350 webp q85"`)
- Shows the avatar at a smaller size (120x120), "Page not found" heading, friendly message, and a "Go home" link
- Styled via a small `.not-found` section in `custom.css`, centered layout

### Reduced Motion
Add a single `@media (prefers-reduced-motion: reduce)` block at the end of `custom.css` that sets `transition: none !important` on all animated elements (or use `*` selector for simplicity since there are no CSS animations to preserve).

In `layouts/photography/list.html`, check `window.matchMedia('(prefers-reduced-motion: reduce)')` and skip the 150ms fade timeout in `showPhoto` when true.

## Files to Modify

| File | Change |
|------|--------|
| `layouts/404.html` | Create — branded 404 page with avatar and home link |
| `assets/css/extended/custom.css` | Add `.not-found` styles and `prefers-reduced-motion` media query |
| `layouts/photography/list.html` | Skip lightbox fade transition when reduced motion preferred |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] `node scripts/generate-headers.js` succeeds
- [x] 404 page renders at any non-existent URL (e.g., `/nonexistent/`)
- [x] 404 page shows avatar, heading, message, and home link
- [ ] 404 page works in dark mode
- [ ] With `prefers-reduced-motion: reduce` enabled in OS/browser, no CSS transitions occur on hover or lightbox
- [ ] Lightbox photo switching is instant (no fade) with reduced motion enabled
- [ ] With reduced motion disabled, all transitions work as before
