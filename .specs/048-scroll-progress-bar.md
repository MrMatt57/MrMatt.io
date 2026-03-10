# 048: Scroll Progress Bar

**Branch**: `feat/scroll-progress-bar`
**Created**: 2026-03-09

## Summary

Add a thin scroll progress indicator bar at the very top of the viewport on single blog post pages. As the user scrolls through a post, the bar fills from left to right showing reading progress (0% at top, 100% at bottom).

## Requirements

- Thin colored bar (3px tall) fixed at the very top of the viewport
- Fills from 0% width to 100% width as user scrolls from top to bottom
- Uses a complementary accent color that works in both light and dark mode
- Only appears on single blog post pages (not homepage, list pages, photography, etc.)
- Respects `prefers-reduced-motion: reduce` (hidden entirely when motion is reduced)
- No npm/node dependencies, no external JS frameworks
- Minimal vanilla JS to track scroll position and update bar width

## Design

### Progress Bar Element
A `<div class="scroll-progress">` element added to the single post layout (`layouts/_default/single.html`), positioned fixed at the top of the viewport with `z-index` above the header.

### Colors
- Light mode: `#4c81b2` (the site's existing accent blue, used for link hover states)
- Dark mode: `rgba(76, 129, 178, 0.8)` (slightly transparent version of the same blue)

### JavaScript
A small inline `<script>` at the end of the single template that:
1. Gets the `.scroll-progress` element
2. On scroll, calculates `scrollTop / (scrollHeight - clientHeight)` as a ratio
3. Sets the bar width as a percentage via `style.width`
4. Skipped entirely when `prefers-reduced-motion: reduce` is active

## Files to Modify

| File | Change |
|------|--------|
| `layouts/_default/single.html` | Add progress bar `<div>` and inline scroll tracking script |
| `assets/css/extended/custom.css` | Add `.scroll-progress` styles and reduced-motion hiding |

## Test Plan

- [ ] Hugo builds with no errors (`hugo --minify`)
- [ ] Progress bar appears on blog post pages
- [ ] Progress bar does NOT appear on homepage, list pages, or photography pages
- [ ] Bar fills from 0% to 100% as user scrolls through a post
- [ ] Works correctly in both light and dark mode
- [ ] Bar is hidden when `prefers-reduced-motion: reduce` is enabled
- [ ] Bar is positioned above the header, at the very top of the viewport
