# 036: Add Bing Site Authentication

**Branch**: `feature/bing-site-auth`
**Created**: 2026-03-02

## Summary

Add Bing Webmaster Tools site verification XML file to the Hugo static directory so it is served at the site root. This allows Bing to verify ownership of mrmatt.io for search indexing and webmaster tools access.

## Requirements

- Place `BingSiteAuth.xml` in `static/` so Hugo serves it at `/BingSiteAuth.xml`
- File contains the verification token `45C5F87EC0A55FA695AD2153029D2032`
- File must be served as-is with no transformation

## Design

Hugo copies files from `static/` to the site root during build. Place the XML file there alongside existing root-level files (favicons, `_headers`, `_redirects`). No config changes needed.

## Files to Modify

| File | Change |
|------|--------|
| `static/BingSiteAuth.xml` | Add Bing site verification XML file |

## Test Plan

- [x] File exists at `static/BingSiteAuth.xml` with correct content
- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [x] `BingSiteAuth.xml` is accessible at `http://localhost:1313/BingSiteAuth.xml`
