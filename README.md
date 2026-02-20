# MrMatt.io

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

## License

Content is licensed under [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/).
