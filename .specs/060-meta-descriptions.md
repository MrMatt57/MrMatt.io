# 060: Expand Short Meta Descriptions

**Branch**: `feature/meta-descriptions`
**Created**: 2026-03-12

## Summary

Expand 6 blog post meta descriptions from under 120 characters to the 120-160 character range recommended by Bing Webmaster Tools. Longer descriptions improve search result snippets and click-through rates.

## Files to Modify

| File | Change |
|------|--------|
| `content/posts/2009-02_mind-control.md` | Expand description from 63 to ~131 chars |
| `content/posts/2017-01_2016-looking-back.md` | Expand description from 74 to ~142 chars |
| `content/posts/2026-02_website-update-2026.md` | Expand description from 83 to ~150 chars |
| `content/posts/2026-03_the-membrane.md` | Expand description from 89 to ~148 chars |
| `content/posts/2009-03_freedom-of-the-seas.md` | Expand description from 92 to ~145 chars |
| `content/posts/2008-04_happy-earth-day.md` | Expand description from 94 to ~142 chars |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] All 6 updated descriptions are between 120-160 characters
- [ ] Site renders correctly on localhost (`hugo server -D`)
