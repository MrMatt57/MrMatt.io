# Ship — Phase 5: Merge and Go Live

Execute the final shipping phase for the MrMatt.io rebuild.

## Pre-flight Checklist

Before proceeding, verify:
- [ ] `hugo` builds with no errors
- [ ] All content pages render (posts, about, now, gear, stack)
- [ ] `.github/workflows/deploy.yml` exists and is valid YAML
- [ ] `.gitignore` is in place
- [ ] `README.md` exists
- [ ] No legacy files remain (gulp/, src/, .travis.yml, etc.)
- [ ] PaperMod submodule is properly configured

Report the checklist results to the user before proceeding.

## Steps

1. **Show the full diff** against master: `git diff master --stat`
2. **Show the commit log** for the branch: `git log master..HEAD --oneline`
3. **Ask for confirmation** before merging

### On confirmation:
4. Rename `master` to `main` if requested
5. Merge the working branch into main
6. Report next manual steps:
   - Push to GitHub
   - Configure GitHub secrets (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)
   - Set up Cloudflare Pages project
   - Verify deployment
   - Update DNS if needed
   - Archive old S3 bucket contents
