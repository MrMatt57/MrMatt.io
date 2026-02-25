---
title: "Stack"
date: 2026-02-19
layout: "single"
---

*Source available on GitHub: [MrMatt57/MrMatt.io](https://github.com/MrMatt57/MrMatt.io)*

### Design Philosophy

- Minimal and fast — no JS frameworks, no bloat, static HTML/CSS
- Content-first — the site publishes writing and serves as a professional presence
- Zero dependencies — vanilla JS, no npm, no external libraries anywhere
- Own your stack — static files you control, no platform lock-in
- Low maintenance — no comment systems, no dynamic backends
- AI as a collaborator — Claude generates, the human reviews and refines
- Spec-driven development — plan before you build, every feature documented
- Automation where it matters — AI and APIs handle the tedious parts so publishing stays frictionless

### Static Site

- [Hugo](https://gohugo.io/) (extended) with [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme (git submodule)
- Custom CSS with [Roboto Slab](https://fonts.google.com/specimen/Roboto+Slab) typography
- No npm, no build tools — Hugo's built-in asset pipeline handles everything

### Development

- Spec-driven workflow — every feature starts with a numbered spec in `.specs/` before any code is written
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) for interactive development — `/feature` creates a spec + git worktree, `/ship` commits, pushes, opens a PR with auto-merge, and cleans up
- Git worktree isolation keeps the main checkout clean while features are in progress

### Serverless Backend

- [Cloudflare Pages Functions](https://developers.cloudflare.com/pages/functions/) (three endpoints)
- `/api/describe-photo` — Claude Vision proxy with CORS locked to mrmatt.io
- `/api/oauth-exchange` — GitHub OAuth token exchange
- `/api/oauth-client-id` — serves the OAuth client ID to the frontend

### CI/CD

- [GitHub Actions](https://github.com/features/actions) — builds Hugo with submodules, compiles Cloudflare Functions, and deploys on every push to main
- Concurrency controls cancel in-progress deploys when a new push arrives
- Branch deploys for PR previews

### Hosting & DNS

- [Cloudflare Pages](https://pages.cloudflare.com/) (free tier)
- Cloudflare DNS
- Cloudflare Web Analytics — server-side, no JavaScript tag

### Automated Publishing

- GitHub OAuth authentication scoped to the repo owner
- Upload creates a feature branch (`photo/YYYY-MM-DD-slug`), commits the image and Hugo content file, opens a PR, and enables auto-merge — all from the phone
- GitHub REST API for branches, blobs, trees, and commits; GraphQL API for the auto-merge mutation
- Photo goes from camera roll to live on the site with no terminal, no laptop

### Photo Upload

- Vanilla JS progressive web app at [`/upload`](/upload) — no frameworks, no dependencies
- Android share target — share a photo directly from the camera roll to the site
- Service Worker with network-first caching and IndexedDB for offline queuing
- Native EXIF parsing from raw JPEG bytes to extract photo dates — no libraries
- Client-side image conversion and resizing via Canvas API before sending to AI

### AI-Powered Descriptions

- [Anthropic Claude](https://www.anthropic.com/) Haiku 4.5 vision model generates photo titles, alt text, and descriptions from uploaded images
- Cloudflare Pages Function proxies requests to the Anthropic API, keeping the API key server-side
- Feedback loop — review the AI output, provide guidance, and regenerate until it's right
- Structured JSON output parsed directly into Hugo front matter fields

