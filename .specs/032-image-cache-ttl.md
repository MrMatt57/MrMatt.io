# 032: Image Cache TTL Headers

**Branch**: `feature/image-cache-ttl`
**Created**: 2026-03-02

## Summary

Photography images are served with `Cache-Control: public, max-age=14400` (4 hours) via Cloudflare's default. These are immutable content that should be cached much longer. Add path-specific cache headers for photography assets and other static resources.

## Requirements

- Add `Cache-Control: public, max-age=31536000, immutable` for photography photo.jpg files
- Add long-lived cache headers for static image assets (favicons, legacy blog images)
- Do NOT modify the existing `/*` security headers block or CSP header
- Use Cloudflare Pages `_headers` file path-pattern syntax

## Files to Modify

| File | Change |
|------|--------|
| `static/_headers` | Add path-specific cache rules for photography and static assets |

## Test Plan

- [x] Existing `/*` security header block is unchanged
- [x] CSP header SHA-256 hashes are untouched
- [x] Photography images get 1-year immutable cache
- [x] Favicon files get 1-year immutable cache
- [x] Legacy blog images get 1-year immutable cache
- [x] Hugo build succeeds and `public/_headers` contains new rules
