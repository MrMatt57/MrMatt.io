# 070: Prevent Future-Dated Content Deploy Surprises

**Branch**: `codex/future-content-deploy-guard`
**Created**: 2026-04-08

## Summary

Prevent photo uploads and manual content changes from silently disappearing after deploy when Hugo treats them as future content. The fix should make uploader dates explicit and site-timezone-aware, and it should make CI fail fast when `main` contains published pages that Cloudflare Pages will not render yet.

## Requirements

- Late-evening uploads must not default to the next UTC day when the site timezone is still the previous day.
- The photo upload flow must show the effective publish date before submission and prevent obviously future-dated publishes to `main`.
- PR and push CI must fail with a clear message when non-draft future content exists anywhere the site build would omit it.
- The validation must protect manual content edits and scripted uploads, not only the browser uploader.
- The solution must not globally enable future-content builds; intentionally scheduled content should stay an explicit workflow decision instead of publishing early by accident.

## Design

Use a two-layer guard. First, update the uploader to compute dates in the site timezone (`America/New_York`) instead of UTC, prefill an editable date field from EXIF or the site-local current day, and block submit when the chosen date is in the future for the site timezone. Second, add a CI validation step before deploy that runs Hugo's future-content listing and fails if any published page would be excluded from the build. This keeps the deploy semantics aligned with Hugo instead of reimplementing date parsing.

Do not switch the Pages build to `--buildFuture`. That would hide the problem by publishing content early, and it still would not create a true scheduled-publishing system because Cloudflare Pages does not rebuild itself at midnight. If scheduled publishing is needed later, handle it as a separate automation or publish-date workflow.

## Files to Modify

| File | Change |
|------|--------|
| `static/upload/index.html` | Add an explicit publish date control and inline validation/help text in the uploader UI |
| `static/upload/app.js` | Replace the UTC date fallback with site-timezone date logic, prefill and validate the date field, and block future-dated auto-merge uploads |
| `scripts/check-future-content.sh` | Wrap `hugo list future` with actionable failure output for CI and local verification |
| `.github/workflows/deploy.yml` | Run the future-content validation before the build and deploy steps on PRs and `main` pushes |
| `README.md` | Document that future-dated published content is rejected because static deploys do not auto-publish at midnight |

## Test Plan

- [x] Uploading a photo without EXIF after 8 PM ET uses the ET calendar date, not the next UTC day
- [x] The upload UI surfaces the publish date and blocks submission when that date would be future content in the site timezone
- [x] `scripts/check-future-content.sh` passes for normal content and fails with a clear error for a temporary future-dated test page
- [ ] The next successful deploy includes the previously missed bonsai photo in `/photography/`
- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
