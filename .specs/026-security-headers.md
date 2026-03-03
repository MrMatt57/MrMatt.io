# 026: Add Security Headers

**Branch**: `feature/security-headers`
**Created**: 2026-03-02

## Summary

Add a Cloudflare Pages `_headers` file to set security response headers across the site. This addresses the missing Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, and Permissions-Policy headers — the highest-priority finding from the security scan.

## Requirements

- Add `X-Content-Type-Options: nosniff` to prevent MIME-type sniffing
- Add `X-Frame-Options: DENY` to prevent clickjacking
- Add `Referrer-Policy: strict-origin-when-cross-origin` to limit referrer leaks
- Add `Permissions-Policy` to restrict unused browser features
- Add `Content-Security-Policy` that allows all current site functionality:
  - Inline scripts (PaperMod theme toggle, lightbox, footer scripts) via `'unsafe-inline'`
  - Google Fonts from `fonts.googleapis.com` / `fonts.gstatic.com`
  - YouTube embeds via `frame-src`
  - Upload PWA: blob/data URIs for image previews, service worker, GitHub API calls
  - `upgrade-insecure-requests` to auto-upgrade old HTTP embeds

## Design

Create `static/_headers` — Hugo copies this to the build output root, where Cloudflare Pages reads it.

### CSP Policy Breakdown

| Directive | Value | Reason |
|-----------|-------|--------|
| `default-src` | `'none'` | Deny-by-default, allowlist everything explicitly |
| `script-src` | `'self' 'unsafe-inline'` | PaperMod inline scripts for theme toggle, search, etc. |
| `style-src` | `'self' 'unsafe-inline' https://fonts.googleapis.com` | Site CSS + Google Fonts stylesheets + inline style attrs |
| `font-src` | `'self' https://fonts.gstatic.com` | Google Fonts font files |
| `img-src` | `'self' data: blob: https://i.ytimg.com` | Local images, canvas data URIs, blob previews, YT thumbs |
| `connect-src` | `'self' https://api.github.com` | Upload PWA GitHub API + same-origin Cloudflare Functions |
| `frame-src` | `https://www.youtube.com https://www.youtube-nocookie.com https://maps.google.com` | YouTube embeds + legacy Google Maps embed |
| `frame-ancestors` | `'none'` | Modern clickjacking protection (supplements X-Frame-Options) |
| `worker-src` | `'self'` | Upload PWA service worker |
| `manifest-src` | `'self'` | Upload PWA manifest.json |
| `base-uri` | `'self'` | Prevent base tag injection |
| `form-action` | `'self'` | Restrict form submissions to same origin |
| `upgrade-insecure-requests` | (flag) | Auto-upgrade HTTP to HTTPS for old embeds |

### Why `'unsafe-inline'` for scripts

Hugo is a static site generator — it has no server-side rendering to inject CSP nonces into `<script>` tags. PaperMod's theme toggle, the lightbox gallery, and footer scripts all use inline `<script>` blocks. Refactoring all of these into external files would be a large change for minimal benefit on a single-author static site. `'unsafe-inline'` is the pragmatic choice here.

## Files to Modify

| File | Change |
|------|--------|
| `static/_headers` | **Create** — Cloudflare Pages security headers file |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] `_headers` file appears in `public/` build output
- [x] Header syntax is valid per Cloudflare Pages `_headers` format
