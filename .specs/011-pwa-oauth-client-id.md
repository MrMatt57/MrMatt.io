# 011: PWA OAuth Client ID from Environment

**Branch**: `feature/pwa-oauth-client-id`
**Created**: 2026-02-24

## Summary

The PWA upload page hardcodes `GITHUB_CLIENT_ID` as a placeholder in the login button's `data-client-id` attribute. Since the upload page is static HTML served from `static/upload/`, it cannot read Cloudflare Pages environment variables directly. Add a small API endpoint that returns the client ID so the JavaScript can fetch it at runtime.

## Requirements

- Remove the hardcoded `data-client-id="GITHUB_CLIENT_ID"` placeholder from the login button
- Create a Cloudflare Pages Function (`functions/api/oauth-client-id.js`) that reads `GITHUB_CLIENT_ID` from the environment and returns it as JSON
- Update `app.js` to fetch the client ID from the API before building the OAuth redirect URL
- Handle the case where `GITHUB_CLIENT_ID` is not configured (show an error)

## Design

New API endpoint: `GET /api/oauth-client-id` returns `{ "client_id": "..." }`.

The login button click handler fetches the client ID from the API, then redirects to GitHub OAuth. If the fetch fails or the client ID is missing, show an error status message.

## Files to Modify

| File | Change |
|------|--------|
| `functions/api/oauth-client-id.js` | CREATE — New endpoint returning `GITHUB_CLIENT_ID` from env |
| `static/upload/index.html` | Remove `data-client-id` placeholder from login button |
| `static/upload/app.js` | Fetch client ID from API instead of reading `data-client-id` |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Login button no longer has hardcoded placeholder client ID
- [ ] `/api/oauth-client-id` endpoint returns JSON with client_id from environment
- [ ] Clicking "Log in with GitHub" fetches client ID and redirects to correct GitHub OAuth URL
