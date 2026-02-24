# 010: Photography Gallery Redesign & PWA Upload

**Branch**: `feature/photo-gallery-pwa`
**Created**: 2026-02-23

## Summary

Redesign the photography experience across the site: immersive dark-mode gallery page, enhanced homepage photo strip with CSS grid layout, full-featured lightbox with navigation and metadata, real photo content, and a PWA-based upload tool for sharing photos from Android.

## Completed Work

### Homepage Photo Strip
- Converted from horizontal flex scroll to **4-column CSS grid** (`repeat(4, 1fr)`)
- Shows first 7 photos + "Gallery →" link card = 2 rows of 4
- Gallery link uses `box-shadow: inset` border style with dark mode variants
- Thumbnails use `aspect-ratio: 1` with `object-fit: cover` for responsive sizing
- Photo links carry `data-title` and `data-description` attributes for lightbox metadata

### Enhanced Lightbox (Homepage)
- Solid `#0a0a0a` background (fully opaque, not semi-transparent)
- Full viewport flex column layout (`width: 100%; height: 100%; padding: 15px 0`)
- "Matt Walker / Photography" header at top (`.lightbox-site-title` + `.lightbox-subtitle`)
- Image wrapper with `margin-top: auto; flex-shrink: 1; min-height: 0` for vertical centering
- Left/right navigation via invisible 50% overlay zones (appear on hover, `opacity: 0 → 1`)
- Photo title and description displayed below image with subtle `rgba(255,255,255,0.2)` rule
- Keyboard support: ArrowLeft, ArrowRight, Escape
- Rule width syncs to image width via JS `img.onload`

### Immersive Photography Page (`/photography/`)
- Custom `baseof.html` overrides theme shell — forces `data-theme="dark"`, no footer, no theme toggle
- Inline script prevents PaperMod's localStorage theme restore from overriding dark mode
- Custom "Matt Walker / Photography" header matching lightbox aesthetic
- Responsive CSS grid: `repeat(auto-fill, minmax(160px, 1fr))`, max-width 1400px
  - ~375px phone: 2 columns
  - ~768px tablet: 4 columns
  - ~1024px desktop: 5 columns
  - ~1400px wide: 8 columns
- Existing lightbox with close/escape support

### Real Photo Content
- Removed 3 sample placeholder photos
- Added 4 real photos: cast-iron-breakfast, snow-clearing-duty, snow-slope-lights, valley-sunset-panorama
- Each as a Hugo page bundle with `index.md` front matter (title, date, alt text)

### PWA Upload Tool (`static/upload/`)
- Installable PWA registered as Android share target
- GitHub OAuth authentication via Cloudflare Pages Function (`functions/api/oauth-exchange.js`)
- Commits images as Hugo page bundles via GitHub Contents API
- Vanilla JS, self-contained in `static/upload/`

## Files Modified/Created

| File | Action | Purpose |
|------|--------|---------|
| `layouts/index.html` | MODIFIED | 4-column grid photo strip, Gallery link, enhanced lightbox with nav/title/description |
| `layouts/photography/baseof.html` | CREATED | Custom dark-mode page shell, no footer/toggle |
| `layouts/photography/list.html` | MODIFIED | Responsive grid layout, simplified (header in baseof) |
| `assets/css/extended/custom.css` | MODIFIED | Photo strip grid, lightbox layout, photography page styles, gallery link |
| `content/photography/2026-02-23-*/` | CREATED | 4 real photo page bundles |
| `content/photography/sample-*/` | DELETED | Removed placeholder photos |
| `static/upload/*` | CREATED | PWA upload tool (index.html, manifest.json, sw.js, app.js, style.css) |
| `functions/api/oauth-exchange.js` | CREATED | Cloudflare Pages Function for OAuth token exchange |
| `README.md` | MODIFIED | Added Photo Upload PWA section |
| `.specs/010-photo-gallery-pwa.md` | MODIFIED | This spec, updated to reflect completed work |

## Remaining Work

- [ ] Tune `/photography/` page lightbox to match homepage lightbox (full nav, title, description)
- [ ] Test PWA upload flow end-to-end with real GitHub OAuth app
- [ ] Verify responsive behavior across devices
- [ ] Final dark mode polish pass

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Homepage photo strip shows 4-column grid with 7 photos + Gallery link
- [x] Gallery link navigates to `/photography/`
- [x] Lightbox opens with solid dark background and "Matt Walker / Photography" header
- [x] Lightbox left/right navigation works (click and keyboard)
- [x] Lightbox shows photo title, rule, and description
- [x] `/photography/` page loads with dark background, custom header, no theme toggle
- [x] Photography page grid is responsive across viewport sizes
- [ ] PWA upload page loads with login prompt
- [ ] OAuth flow works end-to-end
- [ ] Navigating from photography page to homepage preserves user's theme preference
