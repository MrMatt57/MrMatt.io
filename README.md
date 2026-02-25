# MrMatt.io

[![Deploy to Cloudflare Pages](https://github.com/MrMatt57/MrMatt.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/MrMatt57/MrMatt.io/actions/workflows/deploy.yml)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fmrmatt.io&style=flat)](https://mrmatt.io)
[![Hugo](https://img.shields.io/badge/Hugo-Extended-ff4088?logo=hugo&logoColor=white&style=flat)](https://gohugo.io/)
[![Cloudflare Pages](https://img.shields.io/badge/Cloudflare%20Pages-Deployed-f38020?logo=cloudflarepages&logoColor=white&style=flat)](https://pages.cloudflare.com/)
[![Dependabot](https://img.shields.io/badge/Dependabot-Enabled-025E8C?logo=dependabot&logoColor=white&style=flat)](https://github.com/MrMatt57/MrMatt.io/blob/main/.github/dependabot.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey?style=flat)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub last commit](https://img.shields.io/github/last-commit/MrMatt57/MrMatt.io?style=flat)](https://github.com/MrMatt57/MrMatt.io/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/MrMatt57/MrMatt.io?style=flat)](https://github.com/MrMatt57/MrMatt.io)

Personal website of Matt Walker — [mrmatt.io](https://mrmatt.io)

## Stack

- **SSG:** [Hugo](https://gohugo.io/) (extended) with [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme
- **CI/CD:** GitHub Actions
- **Hosting:** Cloudflare Pages

## Local Development

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/MrMatt57/MrMatt.io.git

# Run dev server with drafts
hugo server -D

# Production build
hugo --minify
```

## Adding a New Post

```bash
hugo new content/posts/YYYY-MM_post-slug.md
```

## Deployment

Pushes to `main` automatically build and deploy via GitHub Actions to Cloudflare Pages.

**Required GitHub secrets:**
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

## Photo Upload PWA

The site includes a Progressive Web App at `/upload/` that lets you share photos directly from your phone to the photography gallery. It authenticates via GitHub OAuth and commits images as Hugo page bundles. Photos are automatically described by Claude AI (title, alt text, and a personalized description).

**Setup:**

1. Create a GitHub OAuth App at https://github.com/settings/developers
   - **Homepage URL**: `https://mrmatt.io`
   - **Callback URL**: `https://mrmatt.io/upload/`
2. In the Cloudflare Pages dashboard, add **encrypted** environment variables (use the "Encrypt" toggle):
   - `GITHUB_CLIENT_ID` — from the OAuth App
   - `GITHUB_CLIENT_SECRET` — from the OAuth App (must be encrypted)
   - `ANTHROPIC_API_KEY` — for AI photo descriptions (must be encrypted)
3. Update the `data-client-id` attribute in `static/upload/index.html` with your Client ID

**Security:** Only the GitHub user `MrMatt57` can upload. OAuth uses CSRF protection via the `state` parameter. CORS is locked to `https://mrmatt.io`. API keys are never exposed to the client.

## License

Content is licensed under [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/).
