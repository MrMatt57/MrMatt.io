---
date: "2026-03-07"
draft: false
title: "Building MrMatt.io: The Migration"
slug: "building-mrmatt-io-migration"
description: "Replacing seven services and a deprecated npm ecosystem with Hugo, GitHub Actions, and Cloudflare Pages."
tags:
  - "software-development"
  - "building-mrmatt-io"
  - "infrastructure"
summary: "Replacing seven services and a deprecated npm ecosystem with Hugo, GitHub Actions, and Cloudflare Pages."
---

> **Building MrMatt.io** — a series on rebuilding this site from scratch.
> 1. [Spec-Driven Development](/posts/building-mrmatt-io-specs/)
> 2. **The Migration** (you are here)
> 3. [The Photography Pipeline](/posts/building-mrmatt-io-photography/)
> 4. [Performance & Security](/posts/building-mrmatt-io-performance/)

---

### The old stack

When I last [rebuilt this site in 2016](/posts/website-update-2016/), the stack made sense.  Here's what was running:

- **Hugo** — static site generator
- **Gulp** — task runner for the build pipeline
- **SASS** — CSS preprocessing
- **npm** — dependency management
- **Travis CI** — continuous integration
- **s3cmd** — deployment to S3
- **Amazon S3** — file hosting
- **KeyCDN** — CDN in front of S3
- **Let's Encrypt** — TLS certificates via cron
- **DNS Made Easy** — DNS
- **Staticman** — comment system processing GitHub PRs

Eleven moving parts for a blog.  Each one justified at the time— Gulp because Hugo didn't have an asset pipeline yet, SASS because raw CSS was painful, KeyCDN because S3 alone was slow, Let's Encrypt because HTTPS wasn't free on CDNs, Staticman because I wanted comments without a database.

By 2026, half the npm packages were deprecated and the other half had security advisories.  Travis CI's free tier was gutted.  Staticman hadn't processed a comment in years.  I was paying for four services to host what amounts to some HTML and a few photos.

### The new stack

Hugo stays.  Everything else goes.

**Hugo + PaperMod** — Hugo's built-in pipeline handles CSS minification and fingerprinting now.  No Gulp, no SASS, no npm.  PaperMod is actively maintained with dark mode, search, and solid accessibility defaults.  One git submodule instead of a custom theme.

**GitHub Actions** — One workflow file replaces Travis CI and the deployment scripts.  Checkout, build, deploy.

![GitHub Actions— a stream of green checks, the entire CI/CD pipeline in one workflow](/images/building-mrmatt-io/github-actions.png)

**Cloudflare Pages** — This is the big one.  Free tier, global CDN, automatic TLS, HTTP/3, preview deployments on PRs.  Replaces S3, KeyCDN, Let's Encrypt, and DNS Made Easy.  Four services collapsed into one.

**Cloudflare Functions** — Three lightweight serverless endpoints for the [photo upload tool](/posts/building-mrmatt-io-photography/): OAuth exchange, client ID lookup, AI photo descriptions.  Runs on Cloudflare's edge at no cost for my usage.

### Content migration

48 posts from 2007 to 2017, all preserved.

**Front matter** — Every post used TOML (`+++` delimiters).  PaperMod expects YAML (`---`).  Mechanical conversion, but each post needed review because some custom fields didn't map cleanly.

**Shortcodes** — The old theme had `gallery`, `galleryimage`, `galleryinit`, `widecontent`.  None of those exist in PaperMod and I didn't want to recreate them.  Most got replaced with standard markdown.  The gallery shortcodes were removed entirely— photography now has its [own section](/photography/) with a proper implementation.

**Legacy embeds** — A few posts had raw HTML iframes for YouTube and Google Maps.  Still work fine (Goldmark allows unsafe HTML), but they needed CSP `frame-src` directives to permit those origins.

The words are the same.  The RC planes, the fishing trips, the [camping photos](/posts/canoe-camping-penobscot-river-maine/), the tech reviews— all still here.  Cleaner markup is all.

### What I left out

Every rebuild is a chance to add things.  I was more interested in what I could remove.

**No npm.**  Hugo handles everything natively now— minification, fingerprinting, image resizing, WebP.  The only JavaScript in the build is a 50-line post-build script for CSP hash generation, and it has zero npm dependencies.

**No comments.**  Staticman was clever— comments as GitHub PRs, stored in the repo as data files.  In practice I got maybe ten real comments over four years, plus a steady stream of spam.  If I bring comments back it'll be something like Giscus backed by GitHub Discussions.

**No client-side analytics.**  Cloudflare Web Analytics runs at the edge— no JS tag, no cookie banners.  Page views and referrers without adding anything to the site.

**No build complexity.**  The Hugo config is 96 lines.  No webpack, no PostCSS, no Tailwind.

### Three services

The whole site runs on:

- **GitHub** — source, CI/CD, PRs, releases
- **Cloudflare** — hosting, CDN, DNS, TLS, analytics, functions
- **Anthropic** — AI photo descriptions via Claude Haiku

Monthly hosting cost: $0.  The only spend is Anthropic API usage for photo descriptions— fractions of a cent per photo.

The old stack had S3 ($1-2/mo), KeyCDN ($5-10/mo), DNS Made Easy ($3/mo), plus Travis CI's increasingly restricted free tier.  Not a lot of money, but a lot of billing dashboards.

### What I learned

The 2016 stack was best-of-breed assembly.  S3 was the best static host.  KeyCDN was a solid CDN.  Travis CI was the standard for open-source CI.  Each choice was defensible in isolation.  But the integration surface— the Gulp tasks, the deployment script talking to three APIs, the cron job renewing certificates— that's where the maintenance burden lived.

The 2026 stack is platform convergence.  Cloudflare Pages isn't the best CDN, or the best host, or the best DNS.  But it's good enough at all three, and the integration cost is zero.  Same with GitHub— not the best CI, but Actions plus source hosting plus PR workflows in one place eliminates a whole category of glue.

![The current site— Hugo + PaperMod, clean and minimal](/images/building-mrmatt-io/homepage.png)

Faster, more secure, easier to maintain.  I didn't have to be clever— I just had to be willing to delete things.

*Next: [The Photography Pipeline](/posts/building-mrmatt-io-photography/)— phone to published gallery, end to end.*
