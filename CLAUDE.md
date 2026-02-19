# MrMatt.io — Claude Code Project Instructions

## Project Overview

Personal website for Matt Walker at [mrmatt.io](https://mrmatt.io). Rebuilding from a 2017-era Hugo + Gulp + Travis CI + S3/KeyCDN stack into a modern Hugo site with GitHub Actions CI/CD and Cloudflare Pages hosting.

## Target Stack

- **SSG:** Hugo (latest, extended) — use built-in asset pipeline
- **Theme:** Hugo PaperMod (git submodule, not vendored)
- **CI/CD:** GitHub Actions → Cloudflare Pages
- **Hosting:** Cloudflare Pages (free tier)
- **Comments:** None
- **Analytics:** Cloudflare Web Analytics (no JS tag)

## Repo Structure (Target)

```
.github/workflows/deploy.yml
content/posts/           # Blog/journal posts
content/about/index.md
content/now/index.md
content/gear/index.md
content/stack/index.md
static/images/
assets/                  # Hugo Pipes (custom CSS overrides)
themes/PaperMod/         # Git submodule
hugo.toml
```

## Design Philosophy

- Minimal and fast — no JS frameworks, no bloat, static HTML/CSS
- Content-first — the site publishes writing and serves as a professional presence
- Low maintenance — no comment systems, no dynamic backends
- Dark mode support — clean light/dark toggle via PaperMod

## Constraints

- **No npm/node dependencies.** Hugo's built-in pipeline handles everything.
- **No client-side JavaScript** beyond what PaperMod ships (theme toggle, search).
- **Submodule for theme.** Use `git submodule`, not vendored copy.
- **All content in Markdown.** No HTML pages, no shortcode abuse.
- **Accessibility matters.** Verify contrast ratios and semantic HTML.

## Git Conventions

- Use conventional commits: `feat:`, `chore:`, `fix:`, `docs:`, `refactor:`
- Keep commit history clean
- Branch: `v2026` is the working branch for the rebuild
- Base/main branch: `master` (will rename to `main` at ship time)

## Content Notes

- Old content uses `+++` TOML front matter — migrate to `---` YAML front matter for PaperMod
- Old posts use custom shortcodes (`gallery`, `galleryimage`, `galleryinit`, `widecontent`) that won't exist in PaperMod — replace with standard markdown or remove
- Existing tags to preserve: `software-development`, `travel`, `r/c-planes`, `photography`
- New tag taxonomy for future posts: `azure-ai`, `homelab`, `coffee`, `cooking`, `rowing`, `infrastructure`

## Development Commands

```bash
hugo server -D          # Local dev server with drafts
hugo --minify           # Production build
hugo new posts/my-post.md  # New post
```

## Phase Tracking

Phases are executed via Claude Code commands:
1. `/setup` — Initialize repo, remove legacy files, install theme, verify Hugo builds
2. `/feature content-migration` — Migrate content, update front matter, clean up pages
3. `/feature cicd` — Create GitHub Actions workflow
4. `/feature polish` — README, .gitignore, verification checklist
5. `/ship` — Merge, rename branch, final verification
