# 050: Fix Camera Sparkline Height on Mobile

**Branch**: `feature/fix-sparkline-height`
**Created**: 2026-03-10

## Summary

The sparkline bar charts in the "Every Camera I've Ever Owned" post are too tall on mobile devices. On desktop the 32px height is proportional, but on phones the sparklines dominate the camera cards. Fix by moving inline styles to CSS classes with responsive breakpoints.

## Requirements

- Sparkline bar charts should be shorter on mobile (≤549px): 20px
- Desktop (≥550px) keeps current 32px height
- Camera card images should scale down on mobile for better proportions
- No functional changes to the chart rendering logic

## Design

Replace the inline `height:32px` on the sparkline container div with a CSS class `.camera-sparkline` defined in `custom.css`. Add responsive rules at the existing 550px breakpoint. Move canvas inline styles to the CSS class too.

## Files to Modify

| File | Change |
|------|--------|
| `assets/css/extended/custom.css` | Add `.camera-sparkline` class with responsive height |
| `content/posts/2026-03_camera-gear-timeline.md` | Replace inline styles with `.camera-sparkline` class |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [ ] Sparklines are 20px tall on mobile viewport (≤549px)
- [ ] Sparklines are 32px tall on desktop viewport (≥550px)
- [ ] Camera card images scale down on mobile
