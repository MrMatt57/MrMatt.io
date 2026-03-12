# 058: Bing SEO Fixes

**Branch**: `feature/bing-seo-fixes`
**Created**: 2026-03-12

## Summary

Fix SEO issues flagged by Bing Webmaster Tools: multiple h1 tags per page, missing/short meta descriptions on two photography pages, and identical meta descriptions on taxonomy (tag) pages.

## Requirements

- Fix double h1 tags: site title in header should be `<span>`, not `<h1>`, on interior pages
- Add proper title, alt, and description to 2 incomplete photography pages
- Generate unique meta descriptions for taxonomy pages instead of falling back to site description

## Files to Modify

| File | Change |
|------|--------|
| `layouts/partials/header.html` | Change site title from `<h1>` to `<span>` |
| `layouts/photography/baseof.html` | Change site title from `<h1>` to `<span>` |
| `content/photography/2025-06-18-photo-mm30fzuo/index.md` | Add title, alt, description |
| `content/photography/2025-08-15-photo-mm30excl/index.md` | Add title, alt, description |
| `layouts/partials/extend_head.html` | Add unique meta description override for taxonomy pages |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] No pages have multiple h1 tags (verified: 1 h1 per post page)
- [x] Both photo pages have proper meta descriptions
- [x] Tag pages have unique meta descriptions (includes post count and sample titles)
- [ ] Site renders correctly on localhost (`hugo server -D`)
