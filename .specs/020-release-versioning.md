# 020: CalVer Release Versioning

**Branch**: `feature/release-versioning`
**Created**: 2026-02-24

## Summary

Add calendar-based versioning (CalVer) and GitHub Releases to every production deployment. Each merge to `main` that triggers a deploy will also create a GitHub Release tagged `YYYY.MM.DD.N` where N increments per day. This gives full deployment history with auto-generated release notes in GitHub.

## Requirements

- Every successful deploy to Cloudflare Pages creates a GitHub Release
- Version format: `YYYY.MM.DD.N` (e.g., `2026.02.24.1`, `2026.02.24.2`)
- N starts at 1 for the first release of a day and increments for subsequent releases
- Release includes auto-generated notes from commits/PRs since the last release
- Only production deploys (pushes to `main`) create releases, not PR builds

## Design

Modify `.github/workflows/deploy.yml` to:

1. **Upgrade permissions**: Change `contents: read` to `contents: write` so the workflow can create tags and releases.
2. **Add a release step** after the Cloudflare Pages deploy step that:
   - Fetches all existing tags
   - Computes today's date in UTC (`YYYY.MM.DD`)
   - Finds the highest existing tag for today (if any)
   - Determines the next version (`DATE.1` or `DATE.(N+1)`)
   - Creates a GitHub Release with `gh release create` which also creates the git tag
   - Uses `--generate-notes` for automatic release notes from conventional commits

The `gh release create` command handles both tag creation and release creation in one step, targeting the exact commit SHA that was deployed.

## Files to Modify

| File | Change |
|------|--------|
| `.github/workflows/deploy.yml` | Upgrade `contents` permission to `write`; add "Create Release" step after deploy |

## Test Plan

- [x] Workflow YAML is valid (no syntax errors)
- [x] Release step only runs on `main` branch pushes (has `if` condition)
- [x] Version format matches `YYYY.MM.DD.N` pattern
- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
