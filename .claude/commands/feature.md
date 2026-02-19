# Feature: $ARGUMENTS

Execute the specified feature phase for the MrMatt.io rebuild. The feature name is provided as the argument.

---

## content-migration

**Phase 2: Migrate and clean up all site content.**

### Steps

1. **Migrate content files** from `hugo/content/` to `content/`:
   - Posts go to `content/posts/`
   - Pages (`about`, `now`, `gear`, `stack`) become Hugo page bundles: `content/<page>/index.md`
   - Skip `not-found.md` and `regex.md` (not needed)

2. **Update front matter** in every migrated file:
   - Convert from `+++` TOML to `---` YAML format
   - Ensure `title`, `date`, `tags`, `draft` fields are present
   - Add `summary` or `description` where missing
   - Remove Staticman-related front matter
   - Remove `keywords` field (not used by PaperMod)

3. **Fix shortcodes and HTML**:
   - Replace `gallery`, `galleryimage`, `galleryinit`, `widecontent` shortcodes with standard markdown images or remove them
   - Convert inline HTML (icon lists, etc.) to markdown where possible
   - Ensure image paths point to `/images/` (new location)

4. **Migrate static assets**:
   - Copy `hugo/static/img/` contents to `static/images/`
   - Copy `hugo/static/favicon.ico` if it exists
   - Update image references in content to use `/images/` path

5. **Remove the old `hugo/` directory** entirely

6. **Update page content**:
   - `/now/` — Replace with placeholder: "This page is a snapshot of what I'm focused on right now. Inspired by [nownownow.com](https://nownownow.com)." Add a few placeholder sections.
   - `/about/` — Keep the bio, remove outdated contact info (phone, PGP), keep GitHub and LinkedIn links in markdown format
   - `/gear/` — Placeholder for refresh
   - `/stack/` — Update to reflect the new stack (Hugo + PaperMod + GitHub Actions + Cloudflare Pages)

7. **Verify build**: Run `hugo` and confirm no errors

8. **Commit** with appropriate conventional commit messages as you go

---

## cicd

**Phase 3: Set up GitHub Actions CI/CD pipeline.**

### Steps

1. Create `.github/workflows/deploy.yml` with:
   - Trigger on push to `main` and PRs to `main`
   - Checkout with submodules and full history
   - Setup Hugo (latest, extended) using `peaceiris/actions-hugo@v3`
   - Build with `hugo --minify`
   - Deploy to Cloudflare Pages using `cloudflare/wrangler-action@v3` (only on main branch push)
   - Required secrets: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`

2. **Commit**: `feat: add GitHub Actions workflow for Cloudflare Pages deployment`

3. Document the required GitHub secrets in a brief comment in the workflow file

---

## polish

**Phase 4: Final polish and verification.**

### Steps

1. **Create `.gitignore`** for Hugo:
   - `public/`
   - `resources/`
   - `.hugo_build.lock`
   - `node_modules/` (just in case)

2. **Create `README.md`** with:
   - Project description (personal site of Matt Walker)
   - Local dev instructions (`hugo server -D`)
   - Deployment notes (automatic via GitHub Actions on push to main)
   - Content authoring guide (how to create a new post)
   - Required secrets for deployment

3. **Verify**:
   - Run `hugo` and confirm clean build
   - Check that RSS feed is generated (`public/index.xml`)
   - Check that JSON search index is generated (`public/index.json`)
   - List any build warnings

4. **Commit** with appropriate conventional commit messages

5. Report verification results and any remaining issues
