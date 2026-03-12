# 054: The Membrane — New Blog Post

**Branch**: `feature/the-membrane-post`
**Created**: 2026-03-11

## Summary

New blog post exploring a biological cell metaphor for the expanding boundary between human and AI capabilities. Includes a hand-drawn illustration that needs CSS dark mode support via filter inversion.

## Requirements

- Post content from user's draft (preserved as-is with minimal tweaks)
- Hand-drawn illustration (`new_membrane.png`) embedded in the post
- Image works in both light and dark mode (CSS `filter: invert(1)` in dark theme)
- Post marked as `draft: true` — not published yet
- Tags: `software-development`, `azure-ai`
- Proper YAML front matter matching site conventions

## Design

- Image stored at `static/images/the-membrane.png`
- Dark mode handled via a `.dark-invertible` CSS class that applies `filter: invert(1)` under `[data-theme="dark"]`
- Image centered in post with appropriate alt text
- Post follows existing front matter pattern: date, draft, title, slug, description, tags, summary

## Files to Modify

| File | Change |
|------|--------|
| `content/posts/2026-03_the-membrane.md` | New post file |
| `static/images/the-membrane.png` | Copy illustration from Desktop |
| `assets/css/extended/custom.css` | Add `.dark-invertible` dark mode invert rule |

## Test Plan

- [ ] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
- [ ] Image displays correctly in light mode
- [ ] Image inverts correctly in dark mode
- [ ] Post appears in draft mode only with `-D` flag
