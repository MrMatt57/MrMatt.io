---
date: "2026-03-09"
draft: false
title: "Building MrMatt.io: Performance & Security"
slug: "building-mrmatt-io-performance"
description: "Self-hosted fonts, auto-generated CSP hashes, security headers, accessibility, and the caching strategy for a static site."
tags:
  - "software-development"
  - "building-mrmatt-io"
  - "infrastructure"
summary: "Self-hosted fonts, auto-generated CSP hashes, security headers, accessibility, and the caching strategy for a static site."
---

> **Building MrMatt.io** — a series on rebuilding this site from scratch.
> 1. [Spec-Driven Development](/posts/building-mrmatt-io-specs/)
> 2. [The Migration](/posts/building-mrmatt-io-migration/)
> 3. [The Photography Pipeline](/posts/building-mrmatt-io-photography/)
> 4. **Performance & Security** (you are here)

---

A static site should be fast and secure by default.  In practice, "by default" gets you most of the way there.  The last 20% is where it gets interesting.

### Fonts

PaperMod pulls its heading font from Google Fonts (Roboto Slab).  That means two DNS lookups, a CSS fetch, then the font download— all before the first meaningful paint.

I self-hosted instead.  Downloaded the WOFF2 files (Latin and Latin Extended), dropped them in `static/fonts/`, wrote `@font-face` with `font-display: swap` and variable weight:

```css
@font-face {
    font-family: "Roboto Slab";
    font-weight: 100 900;
    font-display: swap;
    src: url("/fonts/roboto-slab-latin.woff2") format("woff2");
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, ...;
}
```

Two external connections eliminated.  The browser shows a system font immediately, swaps to Roboto Slab when it loads from the same origin.  Brief flash of unstyled text, but barely noticeable— and far better than invisible text waiting on a third-party server.

Font files get one-year immutable cache headers.  A font update means a new URL, not a cache invalidation.

### Images

Every photo in the gallery uses `srcset` with three thumbnail sizes in WebP:

```html
<img srcset="/photo_200.webp 200w, /photo_300.webp 300w, /photo_450.webp 450w"
     sizes="(max-width: 500px) 45vw, (max-width: 900px) 22vw, 14vw"
     loading="lazy"
     alt="...">
```

The `sizes` breakpoints match the CSS grid— 2 columns on mobile (~45vw each), 4 on tablet (~22vw), 6-8 on desktop (~14vw).  The browser picks the smallest image that covers the rendered size.  A phone never downloads a 450px thumbnail when 200px fills its grid cell.

Everything uses `loading="lazy"`.  Combined with IntersectionObserver progressive loading in the gallery, the initial page load only fetches the first 16 visible thumbnails.

Hugo generates all of this at build time.  Output filenames are content-addressed, so unchanged images reuse cached versions across deployments.

### The CSP story

This is my favorite part of the whole rebuild.

**Phase 1:** Started with a strict Content Security Policy.  `default-src 'none'`, explicit allowances for self-hosted scripts, styles, fonts, images.  Clean, secure, immediately broken— PaperMod uses inline `<script>` and `<style>` tags for theme toggle initialization.

**Phase 2:** `'unsafe-inline'`.  The pragmatic fix.  Works, but defeats the purpose of CSP for XSS protection.  The site is static so the practical risk is low, but it felt wrong.

**Phase 3:** Manual hashes.  CSP supports `'sha256-...'` directives that allow specific inline content by hash.  I computed the SHA-256 of each inline block, added them to the `_headers` file, removed `'unsafe-inline'`.  Precise.  Secure.  Satisfying.

**Phase 4:** Production breaks.  I changed the lightbox JavaScript— added touch swipe support— and forgot the hashes.  They went stale.  CSP blocked the updated scripts.  Gallery lightbox stopped working in production.  The dev server doesn't enforce CSP, so I didn't catch it locally.

**Phase 5:** Auto-generated hashes.  A 50-line post-build script that runs after `hugo --minify`:

1. Scans every HTML file in `public/`
2. Finds all `<script>` and `<style>` tags
3. Computes SHA-256 hash of each
4. Reads `_headers.template` with `{{SCRIPT_HASHES}}` and `{{STYLE_HASHES}}` placeholders
5. Replaces placeholders with collected hashes
6. Writes `public/_headers`

Now the CSP hashes are always in sync.  I can change any inline script and the next build updates the policy automatically.  No more stale hashes, no more broken production.

The pattern keeps repeating— the correct solution isn't always the first one, and the maintenance-free version is worth the extra iteration.

### Security headers

The full set, via Cloudflare Pages' `_headers` file:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

HSTS with preload (two-year max-age).  X-Frame-Options DENY to block clickjacking.  Permissions-Policy denying camera, mic, and geolocation— a blog has no business requesting those.  Referrer-Policy that shares the origin but not the full URL path.

The CSP rounds it out: `default-src 'none'` with explicit allowances for scripts, styles, fonts, images, GitHub API connections, YouTube/Maps frames, service worker, and PWA manifest.  Everything else denied.

![Mozilla Observatory— A+ score, 125/100, all 10 tests passed](/images/building-mrmatt-io/observatory.png)

[A+ on Mozilla Observatory](https://observatory.mozilla.org/analyze/mrmatt.io).  Plus a `/.well-known/security.txt` with contact info for responsible disclosure.

### Accessibility

I've been interested in [web accessibility](/posts/broadening-horizons-in-web-accessibility/) since the 2016 rebuild.  This time I went further.

**Skip links.**  A hidden "Skip to content" link appears on Tab focus before the header.  Keyboard users jump straight to content without tabbing through nav.

**Focus trapping.**  The photo lightbox is a modal.  Tab and Shift+Tab cycle through its interactive elements without escaping to the page behind it.  Find all focusable elements, intercept Tab on the last (wrap to first) and Shift+Tab on the first (wrap to last).

**ARIA.**  The lightbox has `role="dialog"`, `aria-modal="true"`, `aria-label`.  Nav buttons and close button all have descriptive labels.  Screen readers can actually navigate it.

**Reduced motion.**  A global CSS rule kills all transitions when the OS says to:

```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        transition: none !important;
    }
}
```

The lightbox JavaScript checks the same preference— if reduced motion is on, photo transitions happen instantly instead of the 150ms fade.

![The 404 page— avatar, "Nothing's deployed here," and a monospace "cd ~" button](/images/building-mrmatt-io/404-page.png)

**Semantic HTML.**  `<main>`, `<nav>`, `<article>`, `<header>`, `<footer>`, `<section>` used appropriately.  Logical heading hierarchy.  Alt text on all images— AI-generated for photos, manual for everything else.  Descriptive link text.

### Caching

Static sites have an advantage: content doesn't change between deployments.  The strategy is aggressive.

**Fingerprinted assets** — Hugo puts a content hash in CSS and JS filenames.  `Cache-Control: public, max-age=31536000, immutable`.  Cached forever— a change produces a new URL.

**Fonts** — One-year immutable.  They don't change.

**Photos** — One-year immutable for thumbnails and full-size.  Content-addressed by Hugo's pipeline.

**HTML** — No explicit cache headers.  Always fresh, always pointing to the latest fingerprinted assets.

```
/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/photography/*/photo*
  Cache-Control: public, max-age=31536000, immutable
```

A repeat visitor downloads almost nothing— just the HTML, which tells the browser everything else is already cached.

### Adding up

None of this is individually groundbreaking.  Self-hosted fonts, responsive images, CSP, semantic HTML— these are documented best practices.  What matters is applying all of them.

First visit loads fast because images are correctly sized and lazy-loaded.  Second visit loads faster because everything is immutably cached.  Security works because CSP, HSTS, frame protection, and permissions policy reinforce each other.  Accessibility works because skip links, focus trapping, semantic HTML, and motion preferences all contribute.

A static site built with care is better than most dynamic sites.  There are just fewer things to get wrong.

*This is the last post in the [Building MrMatt.io](/tags/building-mrmatt-io/) series.  Start with [Spec-Driven Development](/posts/building-mrmatt-io-specs/) if you haven't read the others.*
