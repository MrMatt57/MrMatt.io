# 055: Journal Tag Restructure

**Branch**: `feature/journal-tag-restructure`
**Created**: 2026-03-11

## Summary

Restructure the homepage journal navigation and simplify the site-wide tag taxonomy. Replace the current "Everything | Software Dev | Travel" nav with "Everything | Photography | Reflections | This Site | Travel" to better reflect the site's evolving content pillars. Retag all 56 posts with a simplified, consistent tag set.

## Requirements

- Update homepage journal nav links to: Everything | Photography | Reflections | This Site | Travel
- Introduce new tags: `reflections`, `this-site`
- Retire/consolidate legacy tags: `building-mrmatt-io` → `this-site`, `ai` → absorbed into existing tags, `infrastructure` → `this-site`, `Website` → `this-site`, `Review`/`Camping`/`Hiking`/`Cruise`/`Social`/`Music`/`Home Automation`/`SmartThings`/`Tutorial`/`Time-lapse`/`Video`/`Cars`/`Performance` → removed
- Normalize all tag casing to lowercase-hyphenated (e.g., `R/C Planes` → `r/c-planes`, `Software Development` → `software-development`)
- Keep `software-development` as a tag (just not in homepage nav)
- Keep `r/c-planes` as a tag (8 posts, coherent collection)
- Posts that don't fit any category cleanly get no tags (that's fine)

## Design

### New Tag Set

| Tag | Purpose | Nav link? |
|-----|---------|-----------|
| `photography` | Photo posts, gear, data analysis | Yes |
| `reflections` | Thought pieces, paradigm shifts, observations | Yes |
| `this-site` | Building/evolving mrmatt.io across all eras | Yes |
| `travel` | Travel, camping, hiking, cruises | Yes |
| `software-development` | Technical/code posts | No (too broad for nav) |
| `r/c-planes` | RC airplane hobby | No |

### Complete Post → Tag Mapping

| # | Post | New Tags |
|---|------|----------|
| 1 | Getting Started With RC Airplanes (2007-06) | `r/c-planes` |
| 2 | AirHogs are a blast! (2007-06) | `r/c-planes` |
| 3 | AirHogs Just Not Enough Anymore (2007-06) | `r/c-planes` |
| 4 | Soarstar RC Video (2007-07) | `r/c-planes` |
| 5 | Terminal Velocity Pentax Optio S6 (2007-07) | `r/c-planes`, `photography` |
| 6 | Building a LiPo Charging Station (2007-08) | `r/c-planes` |
| 7 | Coosa Backcountry Trail (2007-09) | `travel` |
| 8 | Life after Lasik! (2007-09) | *(none)* |
| 9 | IronKey USB (2007-10) | *(none)* |
| 10 | Peaks of Otter (2007-10) | `travel` |
| 11 | Swans HiVi M10 Speakers (2007-11) | *(none)* |
| 12 | 1994 Honda Accord (2007-12) | *(none)* |
| 13 | My Computing Equipment (2007-12) | `software-development` |
| 14 | Live Music (2007-12) | *(none)* |
| 15 | December is for Cynics (2007-12) | *(none)* |
| 16 | Google Chart API (2007-12) | `software-development` |
| 17 | How Projects Really Work (2007-12) | `software-development` |
| 18 | RC Plane Hanger (2007-12) | `r/c-planes` |
| 19 | Hello World new server (2008-01) | `this-site` |
| 20 | Pet Fish Archive (2008-01) | *(none)* |
| 21 | Funny IT Voicemail (2008-01) | *(none)* |
| 22 | QOS for SOHO VOIP (2008-01) | `software-development` |
| 23 | Don't forget about DNS (2008-01) | `software-development` |
| 24 | Into the Wild (2008-02) | *(none)* |
| 25 | RC Airplane Flight Box (2008-02) | `r/c-planes` |
| 26 | Vista SP1 is Nice (2008-02) | *(none)* |
| 27 | Old Technology Meets New (2008-02) | `software-development` |
| 28 | Printing on paper (2008-03) | `reflections` |
| 29 | MOO Business Cards (2008-04) | *(none)* |
| 30 | CSS Naked Day (2008-04) | `this-site` |
| 31 | Happy Earth Day (2008-04) | *(none)* |
| 32 | Remote Control Extender (2008-07) | *(none)* |
| 33 | Amazon Cloudfront CDN (2008-12) | `software-development`, `this-site` |
| 34 | Honda Slow Window (2009-01) | *(none)* |
| 35 | Mind Control Tea (2009-02) | *(none)* |
| 36 | Freedom of the Seas (2009-03) | `travel` |
| 37 | Loch Raven Hike (2009-04) | `travel` |
| 38 | LaCie iamaKey (2009-06) | *(none)* |
| 39 | Canoe Camping Penobscot (2009-08) | `travel` |
| 40 | Carnival Pride (2009-12) | `travel` |
| 41 | Canon Time Lapse CHDK (2010-05) | `photography` |
| 42 | WordPress > Ghost (2014-12) | `this-site`, `software-development` |
| 43 | Ghost > Hugo (2016-12) | `this-site`, `software-development` |
| 44 | Looking Back on 2016 (2017-01) | `reflections` |
| 45 | Accessibility Testing (2017-01) | `this-site`, `software-development` |
| 46 | Static Site Caching (2017-01) | `this-site`, `software-development` |
| 47 | SmartThings Pantry (2017-02) | `software-development` |
| 48 | Version 2026 (2026-02) | `this-site`, `software-development` |
| 49 | Spec-Driven Development (2026-03) | `this-site`, `software-development` |
| 50 | The Migration (2026-03) | `this-site`, `software-development` |
| 51 | Photography Pipeline (2026-03) | `this-site`, `photography`, `software-development` |
| 52 | Curating 100K Photos (2026-03) | `photography`, `software-development` |
| 53 | Performance & Security (2026-03) | `this-site`, `software-development` |
| 54 | Camera Gear Timeline (2026-03) | `photography` |
| 55 | 94,000 Photos (2026-03) | `photography` |
| 56 | The Membrane (2026-03) | `reflections`, `software-development` |

## Files to Modify

| File | Change |
|------|--------|
| `layouts/index.html` | Update journal nav links from "Software Dev \| Travel" to "Photography \| Reflections \| This Site \| Travel" |
| `content/posts/*.md` (56 files) | Update `tags:` front matter per mapping above |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Homepage journal nav shows: Everything \| Photography \| Reflections \| This Site \| Travel
- [x] `/tags/photography/` shows 6 posts
- [x] `/tags/reflections/` shows 3 posts (Printing on paper, Looking Back on 2016, The Membrane)
- [x] `/tags/this-site/` shows 12 posts
- [x] `/tags/travel/` shows 6 posts
- [x] `/tags/software-development/` shows 19 posts
- [x] `/tags/r-c-planes/` shows 8 posts
- [x] No legacy mixed-case tags remain (no `Software Development`, `R/C Planes`, `Travel`, etc.)
- [x] No retired tags remain (`ai`, `building-mrmatt-io`, `infrastructure`, `Website`, `Review`, etc.)
- [x] Posts with no matching category have empty tags array or no tags field
- [x] Site renders correctly on localhost (`hugo server -D`)
