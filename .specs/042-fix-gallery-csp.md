# 042: Fix Gallery Lightbox (CSP Hash Mismatch)

**Branch**: `feature/fix-gallery-csp`
**Created**: 2026-03-05

## Summary

The photography gallery lightbox is completely broken on production. Clicking thumbnails navigates to the raw image instead of opening the lightbox, and homepage photo links go to the gallery without opening the specific image. The root cause is that inline script SHA-256 hashes in the Content Security Policy (`static/_headers`) became stale when recent commits modified the lightbox JavaScript. The browser blocks the script, killing all lightbox functionality.

## Requirements

- Fix the immediate lightbox breakage by ensuring CSP hashes match the current inline scripts
- Auto-generate CSP script hashes as part of the build so this never happens again
- Include pending local improvements: touch swipe navigation, mobile nav arrow visibility, lightbox click area fix, and image max-height tweak
- Remove the fragile manual hash maintenance from `static/_headers`

## Design

**Root cause**: `static/_headers` has a `Content-Security-Policy` with `script-src` listing SHA-256 hashes. When commits changed the lightbox JS (fullsize link, touch swipe, click handler), the script content changed but the CSP hashes weren't updated. Browsers block scripts whose hashes don't match → no click handlers → lightbox broken.

**Fix approach**: Replace the static `_headers` file with an auto-generated one:

1. Create `_headers.template` in the project root with a `{{SCRIPT_HASHES}}` placeholder in the CSP `script-src` directive
2. Create `scripts/generate-headers.js` that:
   - Scans all HTML files in `public/` for `<script>` tags (excluding `type="application/ld+json"`)
   - Computes SHA-256 hashes of each script's content
   - Reads `_headers.template`, replaces the placeholder with the computed hashes
   - Writes the final `public/_headers`
3. Remove `static/_headers` (it would be copied by Hugo and overwritten anyway)
4. Add a post-Hugo build step in the deploy workflow to run the script
5. Include uncommitted local changes (touch swipe, mobile nav, click fix, max-height)

## Files to Modify

| File | Change |
|------|--------|
| `static/_headers` | Delete (replaced by auto-generation) |
| `_headers.template` | New file — headers template with `{{SCRIPT_HASHES}}` placeholder |
| `scripts/generate-headers.js` | New file — post-build script to compute hashes and generate `_headers` |
| `scripts/check-csp-hashes.js` | Delete (temporary diagnostic script) |
| `.github/workflows/deploy.yml` | Add Node.js setup and `node scripts/generate-headers.js` after Hugo build |
| `assets/css/extended/custom.css` | Include uncommitted changes (mobile nav arrows, max-height) |
| `layouts/photography/list.html` | Include uncommitted changes (touch swipe, click area fix) |

## Test Plan

- [x] `hugo --minify` builds without errors
- [x] `node scripts/generate-headers.js` generates `public/_headers` with correct hashes
- [x] Generated CSP contains all inline script hashes from the build
- [x] No stale hashes remain in the generated CSP
- [ ] Lightbox opens when clicking a gallery thumbnail (not navigating to raw image)
- [ ] Homepage photo links open the specific image in the lightbox
- [ ] Touch swipe navigation works in the lightbox
- [ ] Mobile nav arrows are visible on touch devices
- [ ] Site renders correctly on localhost (`hugo server -D`)
