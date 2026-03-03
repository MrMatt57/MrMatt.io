# 038: Fix Gallery Progressive Loading on Wide Viewports

**Branch**: `feature/fix-gallery-progressive-loading`
**Created**: 2026-03-03

## Summary

The photography gallery's progressive rendering breaks on wider viewports. Items are loaded in batches of 16 via IntersectionObserver watching a scroll sentinel. On wide screens (6-8 columns), 16 items fills only 2-3 rows, so the sentinel stays within the viewport+rootMargin after a batch loads. Since IntersectionObserver only fires on state transitions, if the sentinel never leaves the observed area, no further batches load. On narrow screens (2-3 columns), the same 16 items fills more rows, pushing the sentinel out of range so subsequent scrolling properly triggers more batches.

## Requirements

- All gallery thumbnails must render at every viewport width, not just narrow ones
- Progressive batch loading must continue chaining until the sentinel leaves the viewport or all items are shown
- Thumbnails must remain lazy-loaded (`loading="lazy"` on `<img>`) for browser-native image loading optimization
- No behavioral regressions: lightbox, deep linking, keyboard navigation must all continue working
- No new external dependencies

## Design

**Fix the IntersectionObserver re-fire issue** in `layouts/photography/list.html`:

After each `showBatch()` call inside the observer callback, unobserve the sentinel then re-observe it (via `requestAnimationFrame` to let the DOM update first). This forces a fresh intersection check. If the sentinel is still within the viewport+rootMargin, the observer fires again, loading another batch. The chain continues until:
- All items are shown (observer disconnects in `showBatch`)
- The sentinel moves outside the viewport+rootMargin

```javascript
observer = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting) {
        showBatch();
        if (shown < allItems.length) {
            observer.unobserve(sentinel);
            requestAnimationFrame(function() {
                observer.observe(sentinel);
            });
        }
    }
}, { rootMargin: '400px' });
observer.observe(sentinel);
```

This is a minimal, targeted fix. The existing progressive rendering architecture (batch size of 16, 400px rootMargin, gallery-item/visible CSS classes, sentinel element) all remain unchanged.

## Files to Modify

| File | Change |
|------|--------|
| `layouts/photography/list.html` | Update IntersectionObserver callback to unobserve/re-observe sentinel after each batch, forcing chain loading on wide viewports |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
- [ ] All thumbnails appear at wide viewport (1400px+)
- [ ] All thumbnails appear at narrow viewport (375px)
- [ ] Progressive loading still works (items appear in batches as you scroll on narrow viewport)
- [ ] Lightbox opens, navigates, and closes correctly
- [ ] Deep linking via URL hash still works
- [ ] Keyboard navigation (arrows, escape) still works
