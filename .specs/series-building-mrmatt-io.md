# Building MrMatt.io — Blog Post Series Plan

## Context

The site has undergone 44 specs worth of technical work — from a complete migration off the 2017 stack, to a photography pipeline with AI descriptions, to CSP hardening and accessibility. This plan captures a four-post series documenting the rebuild.

## Approach: Tag-Based Series

Uses a shared tag `building-mrmatt-io` to tie the series together:
- PaperMod's `[related]` config weights tags at 100, so series posts automatically appear in each other's "Related Posts"
- `/tags/building-mrmatt-io/` gives a free listing page via existing taxonomy config
- Manual series navigation block at the top of each post

## Series Navigation Block

```markdown
> **Building MrMatt.io** — a series on rebuilding this site from scratch.
> 1. [Spec-Driven Development](/posts/building-mrmatt-io-specs/)
> 2. [The Migration](/posts/building-mrmatt-io-migration/)
> 3. [The Photography Pipeline](/posts/building-mrmatt-io-photography/)
> 4. [Performance & Security](/posts/building-mrmatt-io-performance/)
```

## Posts

| # | File | Title |
|---|------|-------|
| 1 | `content/posts/2026-03_building-mrmatt-io-specs.md` | Spec-Driven Development |
| 2 | `content/posts/2026-03_building-mrmatt-io-migration.md` | The Migration |
| 3 | `content/posts/2026-03_building-mrmatt-io-photography.md` | The Photography Pipeline |
| 4 | `content/posts/2026-03_building-mrmatt-io-performance.md` | Performance & Security |

## Post 1: Spec-Driven Development (~1500-1800 words)
Tags: `software-development`, `building-mrmatt-io`

- Why I started building again — nine years without a post, AI-assisted development collapsed the gap
- The problem with feature frameworks — heavyweight spec tools vs. thinking and starting immediately
- Plans as specs — Claude Code plan mode produces structured plans that read like specs
- The commands — `/feature` creates spec + worktree + implements; `/ship` commits + PR + auto-merge + cleanup
- 44 features and counting — categorized list of everything built
- The superpower — going fast without cutting corners, every feature has a spec and test plan
- Tee up remaining posts

## Post 2: The Migration (~1200-1500 words)
Tags: `software-development`, `building-mrmatt-io`, `infrastructure`

- The old stack honestly — Hugo + Gulp + SASS + Travis CI + s3cmd + S3 + KeyCDN + DNS Made Easy + Let's Encrypt + Staticman
- The new stack — Hugo + PaperMod + GitHub Actions + Cloudflare Pages
- Content migration — 48 posts, TOML→YAML, shortcode cleanup
- What I deliberately left out — no npm, no comments, no client-side analytics
- Three-service reality — GitHub + Cloudflare + Anthropic, $0/month hosting

## Post 3: The Photography Pipeline (~1500-2000 words)
Tags: `software-development`, `building-mrmatt-io`, `photography`

- The problem — photos on phone, gallery on site, enormous gap
- The upload PWA — vanilla JS, Android share target, EXIF parsing, Canvas resizing, GitHub OAuth
- AI descriptions — Claude Haiku vision, Cloudflare Function proxy, feedback loop
- Automated publishing — feature branch + PR via GitHub API, auto-merge
- The gallery — dark-mode CSS grid, custom lightbox with keyboard/touch/focus-trap/ARIA, IntersectionObserver, deep linking
- Image processing — Hugo pipeline: WebP thumbnails (200/300/450px srcset) + 1600px full-size, watermarking
- Lessons learned

## Post 4: Performance & Security (~1500-1800 words)
Tags: `software-development`, `building-mrmatt-io`, `infrastructure`

- Font loading — Google Fonts → self-hosted WOFF2, variable weight, font-display: swap
- Responsive images — srcset, WebP, lazy loading
- CSP journey — deny-by-default → unsafe-inline → manual hashes → hashes broke production → auto-generated hashes
- Security headers — HSTS, X-Frame-Options, Permissions-Policy, security.txt → A+ Observatory
- Accessibility — skip links, focus trapping, ARIA dialog, prefers-reduced-motion
- Cache strategy — immutable content-addressed assets, 1-year fonts/images
