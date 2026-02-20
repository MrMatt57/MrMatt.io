---
date: "2026-02-19"
draft: false
title: "Version 2026 (Hugo > Hugo, but better)"
slug: "website-update-2026"
description: "Nine years later, the site gets a proper rebuild. Same engine, new everything else."
tags:
  - "software-development"
  - "infrastructure"
summary: "Nine years later, the site gets a proper rebuild. Same engine, new everything else."
---

It has been nine years since my last [website update](/posts/website-update-2016/). Nine. Years. In that time my kids have grown up, I've picked up new hobbies, and somehow never got around to writing about any of it. The site has been sitting here since early 2017, faithfully serving its blog posts and fishing photos to the handful of people who stumble across it.

The irony is not lost on me that this is now my third post about rebuilding the site.

### The pattern

If you've been here before, you know the drill:

- **2014** — [WordPress to Ghost](/posts/website-update-2014/). Chasing the full-stack JavaScript dream.
- **2016** — [Ghost to Hugo](/posts/website-update-2016/). Static sites, Gulp, Travis CI, S3, KeyCDN. A proper devops toolchain.
- **2026** — Hugo to... Hugo. But everything around it is different.

Hugo was the right call in 2016 and it's still the right call now. It's fast, it's simple, and it gets out of the way. What needed to go was everything I bolted onto it — the Gulp pipeline, the SASS compilation, the Travis CI config, the S3 deployment scripts, the KeyCDN cache purging, the Staticman comment processing. All of it served its purpose, but none of it aged well. Half the npm packages were deprecated and the other half had security advisories.

### What's new

The rebuild strips it all back:

- **Hugo + PaperMod** — A clean, minimal, actively maintained theme with dark mode, search, and good accessibility out of the box. No custom theme to maintain.
- **GitHub Actions** — One workflow file replaces Travis CI, Gulp tasks, and the deployment script.
- **Cloudflare Pages** — Replaces S3 + KeyCDN + Let's Encrypt + DNS Made Easy. Free tier, global CDN, automatic TLS, HTTP/3. One service instead of four.
- **No build dependencies** — No npm, no node_modules, no Gulp. Hugo handles asset processing natively now. The repo is just content and config.
- **No comments** — Staticman was clever but I never got meaningful engagement from it. If I bring comments back it'll be something like Giscus backed by GitHub Discussions.

### What stayed

The content. All the posts from 2007 through 2017 are still here. The photos, the RC plane builds, the fishing trips, the tech reviews — it's all migrated over. Some of the old shortcodes needed cleanup but the words are the same.

### What's actually different this time

This rebuild was pair-programmed with [Claude Code](https://claude.ai/). The entire migration — deleting legacy files, scaffolding the new Hugo structure, converting front matter, fixing broken shortcodes, writing the CI/CD pipeline — was done conversationally in the terminal. I wrote the spec, Claude executed it phase by phase, and we iterated on the details together. It's a genuinely different way to work on a project like this.

Going forward, every change to the site is spec-driven. I run `/feature`, which creates a numbered spec in `.specs/`, spins up a git worktree, and implements the change. When it's ready, `/ship` commits, pushes, opens a PR, waits for CI, merges, and cleans up the worktree. Each spec is a self-contained record of what changed and why — the whole history lives in the repo.

### What's next

The site exists to publish writing again, and I have things to write about. Azure AI and the work I'm doing there. The homelab I've been building with Proxmox and Tailscale. Coffee roasting. Rowing. Maybe some cooking. The stack page will stay current this time — it's a lot easier to maintain when the stack is three things instead of fifteen.

### Homage

Here's the progression, for tradition's sake:

**WordPress era (2007–2014)**
![MrMatt57.org WordPress Screenshot](/images/MrMatt57org-Wordpress.jpg)

**Ghost era (2014–2016)**
![MrMatt57.org Ghost Screenshot](/images/MrMatt57org-Ghost.jpg)

**Hugo v1 era (2016–2026)**
![mrmatt.io Hugo v1 Screenshot](/images/mrmatt-io-hugo-v1.png)
