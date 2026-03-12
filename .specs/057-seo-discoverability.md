# 057: SEO & AI Discoverability

**Branch**: `feature/seo-discoverability`
**Created**: 2026-03-11

## Summary

Improve search engine and AI crawler discoverability by adding `llms.txt` / `llms-full.txt` for AI models, IndexNow integration for instant Bing notification on deploy, and Google sitemap ping.

## Requirements

- Generate `llms.txt` and `llms-full.txt` automatically via Hugo output formats
- Add IndexNow key and post-deploy ping to notify Bing/Yandex of new content
- Add Google sitemap ping after deploy
- Keep robots.txt permissive for all crawlers (already the case)

## Files to Modify

| File | Change |
|------|--------|
| `hugo.toml` | Add LLMS/LLMSFull output formats, sitemap defaults |
| `layouts/index.llms.txt` | Custom llms.txt with site description |
| `layouts/index.llmsfull.txt` | Full version with post summaries |
| `static/{key}.txt` | IndexNow verification key |
| `.github/workflows/deploy.yml` | Add sitemap ping + IndexNow step |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] `llms.txt` is generated at site root with correct content (14KB, all posts with descriptions)
- [x] `llms-full.txt` is generated at site root with post summaries (49KB, tags + dates + descriptions)
- [x] IndexNow key file exists in build output
- [ ] Site renders correctly on localhost (`hugo server -D`)
