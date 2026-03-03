# 033 — Fix Missing Alt Attribute on Homepage Lightbox Image

## Problem

The homepage has 9 `<img>` tags, but only 8 have meaningful `alt` text. The
lightbox placeholder image (`<img class="lightbox-img" src="" alt="" />`) has an
empty `alt` attribute. After Hugo's `--minify` pass, this renders as a bare
`alt` attribute without `=`, which accessibility scanners flag as missing alt
text.

The same issue exists in `layouts/photography/list.html`.

## Solution

Replace the empty `alt=""` with a descriptive placeholder `alt="Photo"` on the
lightbox `<img>` in both:
- `layouts/index.html`
- `layouts/photography/list.html`

The JavaScript lightbox code already sets `img.alt = photo.alt || ''`
dynamically when a photo is selected, so this placeholder is only visible to
screen readers before a photo loads.

## Files Changed

- `layouts/index.html` — line 75: `alt=""` -> `alt="Photo"`
- `layouts/photography/list.html` — line 29: `alt=""` -> `alt="Photo"`

## Test Plan

- [x] `hugo --minify` builds without errors
- [x] All `<img>` tags in `public/index.html` have `alt=` with a value
- [x] All `<img>` tags in `public/photography/index.html` have `alt=` with a value
- [x] Lightbox JS still overrides alt text when a photo is opened
