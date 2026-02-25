# 019: Update Stack Page

**Branch**: `feature/update-stack-page`
**Created**: 2026-02-24

## Summary

Overhaul the /stack page to showcase the full technical stack behind mrmatt.io, including the photo upload PWA, Claude AI-powered image descriptions, automated GitHub publishing workflow, Cloudflare Functions backend, and spec-driven development workflow with Claude Code.

## Requirements

- Keep the existing items (Hugo, PaperMod, GitHub Actions, Cloudflare Pages, Cloudflare DNS, Web Analytics)
- Add section for the Photo Upload PWA (vanilla JS, Service Worker, IndexedDB, Android share target, native EXIF parsing)
- Add section for AI-powered photo descriptions (Claude Haiku 4.5 Vision API, feedback loop, Cloudflare Functions proxy)
- Add section for automated publishing workflow (GitHub OAuth, REST + GraphQL API, feature branches, auto-merge PRs)
- Add section for serverless backend (Cloudflare Pages Functions for OAuth and AI proxy)
- Add section for development workflow (spec-driven development with Claude Code, worktree isolation, /feature + /ship commands)
- Update design philosophy to reflect the "minimal but smart" approach
- Maintain the existing tone — concise, list-driven, no bloat
- No code snippets or deep technical prose — keep it scannable

## Design

Update `content/stack/index.md` with expanded sections. Each section gets an h3 heading with bulleted details underneath. The page should read like a curated technical resume of the site itself — what powers it and why those choices were made.

Structure:
1. Static Site (Hugo + PaperMod — existing)
2. Photo Upload (PWA with vanilla JS, Service Worker, share target)
3. AI Descriptions (Claude Vision API via Cloudflare Functions)
4. Automated Publishing (GitHub API workflow from mobile to live)
5. Serverless Backend (Cloudflare Pages Functions)
6. CI/CD (GitHub Actions — existing, expanded)
7. Hosting & DNS (Cloudflare Pages + DNS + Analytics — existing, consolidated)
8. Development (spec-driven with Claude Code)
9. Design Philosophy (updated)

## Files to Modify

| File | Change |
|------|--------|
| `content/stack/index.md` | Rewrite with expanded sections |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [ ] Stack page displays all new sections with correct formatting
- [ ] All external links are valid
- [ ] Page reads well on mobile viewport
