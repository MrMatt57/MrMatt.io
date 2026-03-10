# 048: Photography RSS Feed

**Branch**: `feat/photography-rss-feed`
**Created**: 2026-03-09

## Summary

Add a dedicated RSS feed for the photography section at `/photography/index.xml` with media enclosures for each photo, and a subtle RSS icon on the photography gallery page for feed discovery.

## Background

The site already has a main RSS feed at `/index.xml` using a custom template (`layouts/_default/rss.xml`). The photography section uses a custom layout (`layouts/photography/`) with its own `baseof.html` and `list.html`. Photo pages are page bundles under `content/photography/` with `photo.jpg` image resources.

A dedicated photography RSS feed lets subscribers follow new photos without the blog post noise, and the `<enclosure>` tag enables photo-aware feed readers to display thumbnails inline.

## Changes

### 1. Enable RSS output for photography section (`hugo.toml`)

Add `section` to the `[outputs]` block so Hugo generates `index.xml` for sections:

```toml
[outputs]
  home = ["HTML", "RSS", "JSON"]
  section = ["HTML", "RSS"]
```

### 2. Photography-specific RSS template (`layouts/photography/rss.xml`)

Hugo resolves section-level RSS templates by looking for `layouts/{section}/rss.xml` before falling back to `layouts/_default/rss.xml`. The photography template:

- Reuses the same channel metadata pattern as the default RSS template
- Adds `xmlns:media` namespace for `<media:content>` tags
- Each `<item>` includes:
  - `<title>` — photo title
  - `<description>` — photo description from front matter
  - `<pubDate>` — publication date
  - `<link>` / `<guid>` — permalink to the photo page
  - `<enclosure>` — thumbnail image (300x300 webp) with URL, type, and length
  - `<media:content>` — same thumbnail with width/height for richer feed reader support

### 3. RSS icon on photography gallery page (`layouts/photography/baseof.html`)

Add a small RSS icon link next to the "Photography" subtitle in the gallery header. The icon uses an inline SVG (standard RSS icon) styled to be subtle — low opacity, small size, matching the existing muted subtitle color.

### 4. CSS for RSS icon (`assets/css/extended/custom.css`)

Minimal styles for the RSS link:
- Positioned inline next to the subtitle text
- Small size (~14px), low opacity (0.4), slightly brighter on hover (0.7)
- No border/underline to match the photography page's clean aesthetic

## Test Plan

- [ ] `hugo --minify` builds without errors
- [ ] `/photography/index.xml` exists and is valid RSS XML
- [ ] Feed items include `<enclosure>` tags with thumbnail URLs
- [ ] Feed items include `<media:content>` tags
- [ ] RSS icon appears on photography page, subtle and tasteful
- [ ] RSS icon links to `/photography/index.xml`
- [ ] Main site RSS at `/index.xml` still works and does NOT include photography pages
- [ ] Blog section RSS at `/posts/index.xml` unaffected
