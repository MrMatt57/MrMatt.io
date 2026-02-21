# 008: Fix List Bullet Text Indent on Wrap

**Branch**: `feature/fix-list-bullet-indent`
**Created**: 2026-02-20

## Summary

When list items in the `.posts` bullet list wrap to a second line, the wrapped text aligns with the bullet character instead of with the text start. This affects the home page journal list, tag pages, and the archives page. The fix adds a hanging indent so wrapped text stays aligned with the first line's text.

## Requirements

- Wrapped text in `.posts li` items must align with the text start, not the bullet
- The square bullet (`\25AA`) must remain visually in the same position
- Fix must apply globally to all `.posts` lists (home page, tags, tag, archives)
- Dark mode styling must continue to work correctly
- No changes to HTML templates — CSS-only fix

## Design

The current CSS uses a `::before` pseudo-element for the bullet with `margin-right: 0.5em`, but the `<li>` has no left padding to create a hanging indent. When text wraps, it flows back to the left edge (position 0), under the bullet.

**Fix approach:** Use `padding-left` on the `<li>` with `position: relative`, then absolutely position the `::before` bullet in the reserved left padding space. This creates a proper hanging indent where wrapped text aligns with the first line's text.

Changes to `assets/css/extended/custom.css`:

1. Add `padding-left: 1.2em` and `position: relative` to `.posts li`
2. Change `.posts li::before` to use `position: absolute; left: 0` and remove `margin-right`

## Files to Modify

| File | Change |
|------|--------|
| `assets/css/extended/custom.css` | Update `.posts li` and `.posts li::before` rules for hanging indent |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [ ] Home page journal list: long titles wrap with text aligned to text start, not bullet
- [ ] Tag page list: same wrapping behavior
- [ ] Archives page list: same wrapping behavior
- [ ] Dark mode: bullets and text still styled correctly
- [ ] Short titles that don't wrap are unaffected visually
