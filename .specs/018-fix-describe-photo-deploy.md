# 018: Fix Cloudflare Functions Deployment

**Branch**: `feature/fix-describe-photo-deploy`
**Created**: 2026-02-24

## Summary

The AI photo description endpoint returns HTML (404 page) instead of JSON because the `wrangler pages deploy` command in the GitHub Actions workflow doesn't include the `functions/` directory. Fix by adding `--functions-directory=functions` to the deploy command and improve client-side error handling for non-JSON responses.

## Requirements

- Add `--functions-directory=functions` to the wrangler deploy command so Cloudflare Pages Functions are deployed
- Add `r.ok` check in the client-side `describePhoto` fetch to catch non-JSON responses gracefully
- Bump SW cache to v8 and cache-bust to `?v=8`

## Design

### Workflow changes (`.github/workflows/deploy.yml`)
- Line 49: Add `--functions-directory=functions` to the `pages deploy` command

### JS changes (`static/upload/app.js`)
- In `describePhoto`, after the fetch, check `r.ok` before calling `r.json()`. If not OK, throw an error with the status code instead of trying to parse HTML as JSON.

### HTML changes (`static/upload/index.html`)
- Bump cache-bust `?v=7` → `?v=8`

### SW changes (`static/upload/sw.js`)
- Bump `photo-upload-v7` → `photo-upload-v8`

## Files to Modify

| File | Change |
|------|--------|
| `.github/workflows/deploy.yml` | Add --functions-directory=functions to deploy |
| `static/upload/app.js` | Better error handling for non-JSON responses |
| `static/upload/index.html` | Bump cache-bust to v8 |
| `static/upload/sw.js` | Bump cache to v8 |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Deploy workflow includes `--functions-directory=functions`
- [ ] AI description endpoint returns JSON (verify after deploy)
- [x] Non-JSON error responses show meaningful error message
