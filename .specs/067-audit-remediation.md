# 067: Audit Remediation

**Branch**: `codex/067-audit-remediation`
**Created**: 2026-03-23

## Summary

Resolve the concrete issues found in the website audit: tighten CI so Pages Functions are validated before merge, make the photo upload flow editable and collision-safe, bring public stack documentation back in line with the implementation, and clean up broken legacy post content from the migration.

## Requirements

- Validate Cloudflare Pages Functions in pull request CI before merge
- Keep deploy/release steps limited to `main`
- Make AI-generated upload metadata editable before publish:
  - Title editable
  - Alt text editable
  - Description editable
- Make upload folder/branch naming collision-safe without sacrificing readable slugs
- Update public stack/docs copy so it matches the actual implementation:
  - No claim of PR preview deploys unless implemented
  - No claim of IndexedDB offline queue unless implemented
  - CodeQL claim must match repo reality
- Clean up obvious legacy content migration defects:
  - Broken apostrophe/punctuation substitutions
  - Clearly malformed legacy embed/code markup
  - Preserve original meaning and voice

## Files in Scope

- `.github/workflows/deploy.yml`
- `static/upload/index.html`
- `static/upload/app.js`
- `content/stack/index.md`
- `README.md`
- Selected legacy files under `content/posts/`

## Test Plan

- [x] PR workflow still builds Hugo and now validates Pages Functions
- [x] Main branch still performs deploy/release-only steps
- [x] Upload UI allows manual edits to title, alt text, and description
- [x] Duplicate same-day photo titles produce a unique folder/branch instead of a hard failure
- [x] Stack/README documentation matches the implemented behavior
- [x] Cleaned legacy posts render without obvious punctuation corruption or broken embed scaffolding
