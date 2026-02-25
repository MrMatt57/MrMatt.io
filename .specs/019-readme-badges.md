# 019: README Badges

**Branch**: `feature/readme-badges`
**Created**: 2026-02-24

## Summary

Add a collection of status and technology badges to the top of the README.md, right below the `# MrMatt.io` heading. This gives the repo a polished, professional look and provides at-a-glance information about build status, hosting, tech stack, and activity.

## Requirements

- Add 8 badges in a single row below the H1 heading
- Badges should use shields.io and GitHub native badge URLs
- Badges should link to relevant destinations where applicable
- Maintain the existing README content below the badges unchanged

## Design

Badges will be inserted as a single line of inline Markdown images between the `# MrMatt.io` heading and the description paragraph. Each badge is a linked image using shields.io or GitHub's native badge endpoints.

### Badge List (in order)

1. **Deploy** — GitHub Actions workflow status badge for `deploy.yml`, links to workflow runs
2. **Website** — shields.io `website` badge checking `https://mrmatt.io`, links to site
3. **Hugo** — Static shield with Hugo logo (`ff4088`), links to gohugo.io
4. **Cloudflare Pages** — Static shield with Cloudflare logo (`f38020`), links to Cloudflare Pages docs
5. **Dependabot** — Static shield indicating Dependabot is enabled (`025E8C`), links to dependabot config
6. **License** — CC BY 4.0 badge (`lightgrey`), links to Creative Commons license
7. **Last Commit** — Dynamic GitHub last-commit badge, links to commit history
8. **Repo Size** — Dynamic GitHub repo-size badge, links to repo

### Badge URLs

```
Deploy:      https://github.com/MrMatt57/MrMatt.io/actions/workflows/deploy.yml/badge.svg
Website:     https://img.shields.io/website?url=https%3A%2F%2Fmrmatt.io&style=flat
Hugo:        https://img.shields.io/badge/Hugo-Extended-ff4088?logo=hugo&logoColor=white&style=flat
Cloudflare:  https://img.shields.io/badge/Cloudflare%20Pages-Deployed-f38020?logo=cloudflarepages&logoColor=white&style=flat
Dependabot:  https://img.shields.io/badge/Dependabot-Enabled-025E8C?logo=dependabot&logoColor=white&style=flat
License:     https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey?style=flat
Last Commit: https://img.shields.io/github/last-commit/MrMatt57/MrMatt.io?style=flat
Repo Size:   https://img.shields.io/github/repo-size/MrMatt57/MrMatt.io?style=flat
```

## Files to Modify

| File | Change |
|------|--------|
| `README.md` | Add badge row between H1 heading and description paragraph |

## Test Plan

- [ ] All 8 badges render correctly in GitHub's README preview
- [x] Badge links point to correct destinations
- [x] Existing README content is unchanged below the badges
- [x] Hugo builds with no errors (`hugo --minify`)
