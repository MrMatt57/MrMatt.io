# 051: Add 18 Photos to Gallery

**Branch**: `feature/add-photos`
**Created**: 2026-03-10

## Summary

Add 18 photos from C:\Photos to the photography gallery. These are old Flickr uploads (2006-2011) covering travel, nature, tech, and personal subjects. Each photo gets an AI-generated title, alt text, and description following the existing `/photo` pipeline conventions.

## Requirements

- Create 18 new page bundles under `content/photography/`
- Each bundle follows the `{YYYY-MM-DD}-{slug}/` naming convention
- Each bundle contains `photo.jpg` (original image) and `index.md` (front matter)
- Front matter includes: title, date (from EXIF), alt, description, draft: false
- Titles are 2-5 words, title case
- Alt text is one factual sentence for screen readers
- Description is 1-2 natural sentences about the photo
- No duplicate slugs with existing gallery entries

## Photos

| # | Source File | EXIF Date | Title | Slug |
|---|-----------|-----------|-------|------|
| 1 | 2198610538_9ab535ba80_o.jpg | 2006-12-22 | Blue Backlit Keyboard | blue-backlit-keyboard |
| 2 | 3399808913_d497b8cb6a_o.jpg | 2009-03-30 | Underwater Snorkeling | underwater-snorkeling |
| 3 | 3416309694_17d4546a59_o.jpg | 2009-04-05 | Trail Marker | trail-marker |
| 4 | 3416337426_7e304d4f26_o.jpg | 2009-04-05 | Forest Floor Moss | forest-floor-moss |
| 5 | 3416340706_fae461c210_o.jpg | 2009-04-05 | Moss on Stone | moss-on-stone |
| 6 | 3416366820_3ebedc3289_o.jpg | 2009-04-05 | Woodland Waterfall | woodland-waterfall |
| 7 | 3804037385_d487ffea71_o.jpg | 2009-08-02 | Lichen on Bark | lichen-on-bark |
| 8 | 3804664115_0090092555_o.jpg | 2009-08-05 | Mountain Ridgeline | mountain-ridgeline |
| 9 | 3805509162_3cefa22968_o.jpg | 2009-08-06 | Herring Gull Portrait | herring-gull-portrait |
| 10 | 3805578204_6aeb12eb9c_o.jpg | 2009-08-07 | Rockweed at Low Tide | rockweed-at-low-tide |
| 11 | 3805578776_0786d9c340_o.jpg | 2009-08-07 | Coastal Boulders | coastal-boulders |
| 12 | 4196859385_da6921deb6_o.jpg | 2009-11-27 | Cruise Ship Departure | cruise-ship-departure |
| 13 | 4196859669_54eb7cbe68_o.jpg | 2009-11-26 | Turquoise Shoreline | turquoise-shoreline |
| 14 | 4196860021_d434fec97f_o.jpg | 2009-11-26 | Atlantis Resort | atlantis-resort |
| 15 | 4196860741_173052c874_o.jpg | 2009-11-27 | Sun Deck at Port | sun-deck-at-port |
| 16 | 4197614034_54aaabbc15_o.jpg | 2009-11-25 | Nassau Lighthouse | nassau-lighthouse |
| 17 | 4484999190_927a198c8b_o.jpg | 2010-04-02 | Mountain Dew Stash | mountain-dew-stash |
| 18 | 5446364000_ff2f75239b_o.jpg | 2011-02-14 | John Deere Snowblower | john-deere-snowblower |

## Design

Follow the existing `/photo` pipeline:
1. Copy each source JPG to `content/photography/{date}-{slug}/photo.jpg`
2. Create `index.md` with YAML front matter (title, date, alt, description, draft: false)
3. AI vision generates title (2-5 words), alt text (one sentence), and description (1-2 sentences)

No changes to layouts, CSS, or Hugo config needed — existing gallery infrastructure handles everything (responsive grid, lightbox, watermarking, LQIP).

## Files to Modify

| File | Change |
|------|--------|
| `content/photography/2006-12-22-blue-backlit-keyboard/` | New page bundle |
| `content/photography/2009-03-30-underwater-snorkeling/` | New page bundle |
| `content/photography/2009-04-05-trail-marker/` | New page bundle |
| `content/photography/2009-04-05-forest-floor-moss/` | New page bundle |
| `content/photography/2009-04-05-moss-on-stone/` | New page bundle |
| `content/photography/2009-04-05-woodland-waterfall/` | New page bundle |
| `content/photography/2009-08-02-lichen-on-bark/` | New page bundle |
| `content/photography/2009-08-05-mountain-ridgeline/` | New page bundle |
| `content/photography/2009-08-06-herring-gull-portrait/` | New page bundle |
| `content/photography/2009-08-07-rockweed-at-low-tide/` | New page bundle |
| `content/photography/2009-08-07-coastal-boulders/` | New page bundle |
| `content/photography/2009-11-27-cruise-ship-departure/` | New page bundle |
| `content/photography/2009-11-26-turquoise-shoreline/` | New page bundle |
| `content/photography/2009-11-26-atlantis-resort/` | New page bundle |
| `content/photography/2009-11-27-sun-deck-at-port/` | New page bundle |
| `content/photography/2009-11-25-nassau-lighthouse/` | New page bundle |
| `content/photography/2010-04-02-mountain-dew-stash/` | New page bundle |
| `content/photography/2011-02-14-john-deere-snowblower/` | New page bundle |

## Test Plan

- [x] All 18 page bundles created with photo.jpg and index.md
- [x] No PENDING placeholders in any front matter
- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`) — http://localhost:61882
- [ ] New photos appear in gallery grid at `/photography/`
- [ ] Lightbox works for new photos
- [ ] Home page shows updated photo grid
