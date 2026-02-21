# 007: Home Page Responsive Text Wrap

**Branch**: `feature/home-responsive-wrap`
**Created**: 2026-02-20

## Summary

On the home page, the avatar and bio text sit side by side using flexbox. On desktop this looks great, but on smaller screens the text gets squeezed next to the 175px avatar. Add a responsive breakpoint so the layout stacks vertically (avatar on top, text below) on mobile/small screens.

## Requirements

- On viewports >= 550px: keep current side-by-side layout (avatar left, text right)
- On viewports < 550px: stack avatar above text, center the avatar
- Use the existing 550px breakpoint already established in `custom.css`
- Works in both light and dark mode
- No changes to HTML template

## Design

Add a `@media (max-width: 549px)` query targeting `.home-about` to switch `flex-direction` to `column` and center the avatar. This is a CSS-only change — no template modifications needed.

## Files to Modify

| File | Change |
|------|--------|
| `assets/css/extended/custom.css` | Add responsive media query for `.home-about` section |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Desktop (>= 550px): avatar and text remain side by side
- [ ] Mobile (< 550px): layout stacks vertically, avatar centered above text
- [ ] Dark mode: layout behaves the same
- [ ] No horizontal overflow on small screens
