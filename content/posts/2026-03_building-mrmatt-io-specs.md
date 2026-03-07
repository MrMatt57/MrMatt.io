---
date: "2026-03-06"
draft: false
title: "Building MrMatt.io: Spec-Driven Development"
slug: "building-mrmatt-io-specs"
description: "How plan-as-spec methodology and two commands turned a stale personal site into 44 shipped features."
tags:
  - "software-development"
  - "building-mrmatt-io"
summary: "How plan-as-spec methodology and two commands turned a stale personal site into 44 shipped features."
---

> **Building MrMatt.io** — a series on rebuilding this site from scratch.
> 1. **Spec-Driven Development** (you are here)
> 2. [The Migration](/posts/building-mrmatt-io-migration/)
> 3. [The Photography Pipeline](/posts/building-mrmatt-io-photography/)
> 4. [Performance & Security](/posts/building-mrmatt-io-performance/)

---

### Getting started again

Nine years without a blog post.  It wasn't for lack of things to say— life just got in the way and the site's toolchain aged out from under me.  Changing anything meant relearning Gulp, npm, Travis CI, and a bunch of deployment scripts I hadn't touched since 2017.

What changed was AI-assisted development.  Not "AI built my website"— I'll get to that— but the distance between having an idea and shipping it collapsed.  The stuff that used to eat a weekend (configuring build tools, writing boilerplate, wiring up deployments) now happens at conversation speed.  The decisions are still mine.  The tedious parts just got fast enough that building was fun again.

So I rebuilt the whole thing.  And then I kept going.

### Why not a framework

There are plenty of tools for structured feature development— GitHub's SpecKit, Heavy, various RFC and ADR templates.  They all follow the same pattern: write a document in a specific format, get it reviewed, track its status, implement against it.

For a team, that makes sense.  For a solo project on a personal site, it's overhead.  I don't need an approval workflow for adding dark mode to my photo gallery.  I need to think through what I'm building, capture the decisions, and start.

### Plans as specs

Claude Code has a plan mode.  You describe what you want to build and it produces a structured plan— context, requirements, design decisions, files to modify, test plan.  These are detailed enough to implement against and easy to review in a terminal.

I leaned into it.  Every feature gets a plan, the plan becomes the spec, the spec drives the work.

![A spec file showing the structured format— summary, requirements, design, files to modify, and test plan](/images/building-mrmatt-io/spec-example.png)

The format is simple markdown:

```
# Feature Name
Branch: feature/feature-name

## Summary
One paragraph on what and why.

## Requirements
- What the feature must do

## Design
Technical approach, trade-offs considered.

## Files to Modify
- path/to/file.html — what changes

## Test Plan
- [ ] Verification step one
- [ ] Verification step two
```

No YAML metadata, no status fields, no approval gates.  Just enough structure to think clearly.

### Two commands

The whole workflow is two commands: `/feature` and `/ship`.

**`/feature`** kicks things off.  It checks that git is clean, has a conversation about what I want to build, then:

1. Scans `.specs/` for the next number
2. Writes the spec as a numbered markdown file
3. Creates a git worktree on a fresh branch
4. Implements the feature in the worktree
5. Starts a Hugo dev server so I can review

Everything happens in isolation— main stays clean.  I review the running site, ask for changes, iterate.

**`/ship`** finishes it.  Stages, commits, pushes, creates a PR with the spec's test plan as checkboxes in the body.  Enables auto-merge, waits for CI, cleans up the worktree, pulls the merged changes back to main.

![A merged pull request showing the spec's summary and test plan as the PR body](/images/building-mrmatt-io/pr-test-plan.png)

One command to start, conversation in the middle, one command to ship.

### 44 features

![44 numbered spec files in the .specs directory](/images/building-mrmatt-io/specs-directory.png)

Here's what came out of this process:

**Photography pipeline** — PWA upload tool with Android share target, EXIF date parsing, Canvas resizing, GitHub OAuth.  AI-powered photo descriptions via Claude Haiku.  Automated branch/PR creation with auto-merge.  Responsive CSS grid gallery with a custom lightbox— keyboard nav, touch swipe, focus trapping, ARIA, deep linking, progressive loading.  Hugo image pipeline generating WebP thumbnails at three sizes plus watermarked full-res downloads.

**Security** — Content Security Policy that went from `'unsafe-inline'` to manual hashes to auto-generated hashes via a post-build script.  A+ Mozilla Observatory score.  HSTS, X-Frame-Options, Permissions-Policy, security.txt.

**Performance** — Self-hosted WOFF2 variable-weight fonts replacing Google Fonts.  Responsive `srcset` images in WebP.  Content-addressed caching with immutable headers.

**Accessibility** — Skip links, focus trapping, ARIA roles, `prefers-reduced-motion` support, semantic HTML.

**Infrastructure** — GitHub Actions replacing Travis CI.  Cloudflare Pages replacing S3 + KeyCDN + Let's Encrypt + DNS Made Easy.  Cloudflare Functions for OAuth and AI.  Automated releases.

**Content** — 48 posts migrated from TOML to YAML front matter.  Profile updates, homepage photo showcase, custom 404 page, RSS enhancements, related posts.

Each one was a spec → implement → ship cycle.  Most took a single session.  Some took two— like the CSP auto-hash generation, where the first approach broke production.  That story is in the [Performance & Security](/posts/building-mrmatt-io-performance/) post.

### The real artifact

The `.specs/` directory is what makes this work.  Forty-four documents that capture every decision— what I considered, what I chose, why.  When the lightbox JavaScript changed and the manually maintained CSP hashes went stale, I could look at the original spec, understand the intent, and fix it properly instead of hacking around the symptom.

This isn't "AI generated my website."  I make every architectural call.  I review every line.  I decide what gets built and how.  What changed is that the mechanical parts— file creation, boilerplate, rote refactoring— happen at conversation speed.  The ratio of thinking to typing shifted, and that's the ratio that matters.

### The rest of this series

- [**The Migration**](/posts/building-mrmatt-io-migration/) — the old stack, the new stack, what I cut
- [**The Photography Pipeline**](/posts/building-mrmatt-io-photography/) — phone to published page, end to end
- [**Performance & Security**](/posts/building-mrmatt-io-performance/) — fonts, CSP, headers, accessibility, caching
