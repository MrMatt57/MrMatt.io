# 029 — Site Meta Description & Open Graph Image

## Problem

The homepage `<meta name="description">` tag is empty and there is no `og:image` tag.
This means social sharing previews (Twitter/X, LinkedIn, Slack, iMessage, etc.) show
blank cards with no description or image.

## Solution

Add two params to `hugo.toml` under `[params]`:

1. **`description`** — PaperMod's `head.html` renders `site.Params.description` into
   `<meta name="description">` for the homepage, and `opengraph.html` uses it for
   `og:description` as a fallback.
2. **`images`** — PaperMod's `_funcs/get-page-images.html` uses `site.Params.images`
   as the default OG image when a page has no cover image or `images` front matter.
   The existing file `static/images/MattWalker-avatar.png` will be referenced.

## Changes

- `hugo.toml`: Add `description` and `images` to `[params]`

## Test Plan

- [x] `hugo --minify` builds without errors
- [x] `public/index.html` contains `<meta name="description" content="Personal site...`
- [x] `public/index.html` contains `<meta property="og:description" content="Personal site...`
- [x] `public/index.html` contains `<meta property="og:image" content="https://mrmatt.io/images/MattWalker-avatar.png">`
- [x] Avatar file exists at `static/images/MattWalker-avatar.png`
