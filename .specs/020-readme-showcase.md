# 020: README Showcase Transformation

**Branch**: `feature/readme-showcase`
**Created**: 2026-02-24

## Summary

Transform the README from a developer-focused setup guide into a technology showcase and personal brand piece. Move all developer documentation (local dev, deployment, photo PWA setup) to `docs/dev-setup.md`. Add a homepage screenshot hero image and new badges (AI-powered, PWA). The README should impress visitors and showcase the tech stack, not onboard contributors.

## Requirements

- Add a homepage screenshot as a hero image below the badges
- Add two new badges: Anthropic Claude (AI-powered) and PWA
- Rewrite the intro to be more personal/promotional
- Add a "Technology Showcase" section with highlight-reel summaries (1-2 lines each) covering: Static Site, Photo Upload PWA, AI-Powered Descriptions, Serverless Backend, CI/CD, and Development Workflow
- Link to the live `/stack` page for full details
- Keep the License section
- Move Local Development, Adding a New Post, Deployment (secrets), and Photo Upload PWA setup to `docs/dev-setup.md`
- Link to `docs/dev-setup.md` from the README (brief mention, not prominent)

## Design

### README Structure

```
[badges row — existing + AI + PWA]

[hero screenshot of mrmatt.io]

# MrMatt.io

Brief personal intro — who Matt is, what the site is, link to live site.

## Built With

Highlight reel of each tech area (1-2 lines each):
- Hugo + PaperMod (static, no JS frameworks, no npm)
- Vanilla JS PWA (share photos from phone, offline-capable)
- Claude AI Vision (auto-generates titles, alt text, descriptions)
- Cloudflare Pages Functions (serverless API endpoints)
- GitHub Actions CI/CD (auto-deploy on push)
- Claude Code (spec-driven dev workflow, git worktrees)

→ See the full stack breakdown at mrmatt.io/stack

## License

CC BY 4.0 (keep existing)

[small link to docs/dev-setup.md for development instructions]
```

### Screenshot

Capture a screenshot of the mrmatt.io homepage using a screenshot API service and save to `docs/screenshot.png`. Reference it in the README with a relative path.

### New Badges

- `![AI Powered](https://img.shields.io/badge/AI%20Powered-Claude-d97706?logo=anthropic&logoColor=white&style=flat)` — links to Anthropic
- `![PWA](https://img.shields.io/badge/PWA-Enabled-5A0FC8?logo=pwa&logoColor=white&style=flat)` — links to /upload page or PWA spec

### docs/dev-setup.md

Move these sections verbatim from current README:
- Local Development (clone + hugo commands)
- Adding a New Post
- Deployment (secrets, GitHub Actions details)
- Photo Upload PWA (full setup instructions)

Add a title and brief intro noting this is for development/setup reference.

## Files to Modify

| File | Change |
|------|--------|
| `README.md` | Complete rewrite — showcase format with screenshot, badges, highlight reel |
| `docs/dev-setup.md` | New file — developer documentation moved from README |
| `docs/screenshot.png` | New file — homepage screenshot for README hero |

## Test Plan

- [x] `README.md` renders correctly on GitHub (badges, screenshot, links)
- [x] `docs/dev-setup.md` contains all moved developer documentation
- [x] All badge URLs resolve and display correctly
- [x] Screenshot image displays in README
- [x] Link to `/stack` page is correct
- [x] Link to `docs/dev-setup.md` works
- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
