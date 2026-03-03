# 027: Security Hardening — A+ Score, security.txt, Stack Page

**Branch**: `feature/security-hardening`
**Created**: 2026-03-02

## Summary

Harden the site for an A+ score on Mozilla Observatory and SecurityHeaders.com by adding HSTS, replacing `'unsafe-inline'` in CSP script-src with SHA-256 hashes, creating an RFC 9116 `security.txt`, and adding a Security section to the /stack page.

## Requirements

- Add `Strict-Transport-Security` header (HSTS with preload)
- Replace `'unsafe-inline'` in CSP `script-src` with SHA-256 hashes of all 8 inline scripts
- Keep `'unsafe-inline'` in `style-src` only (0 penalty on Observatory)
- Create `/.well-known/security.txt` per RFC 9116
- Add Security section to `/stack` page showcasing headers, CSP, and practices
- Target: Mozilla Observatory score 110+ (A+)

## Design

### HSTS Header
`Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
- 2-year max-age (exceeds 6-month minimum for full marks)
- `includeSubDomains` + `preload` for HSTS preload list eligibility

### CSP Script Hashes
Replace `script-src 'self' 'unsafe-inline'` with `script-src 'self'` plus SHA-256 hashes of all 8 inline scripts found in the production build. This moves the Observatory CSP test from -20 to 0 (style-src-only unsafe-inline).

### security.txt
RFC 9116 format at `static/.well-known/security.txt`:
- Contact: GitHub security advisories URL
- Expires: 1 year from creation
- Preferred-Languages: en
- Canonical URL

### Stack Page Security Section
Add after "Hosting & DNS" section, covering:
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Observatory grade
- security.txt
- CORS policies and API key isolation

## Files to Modify

| File | Change |
|------|--------|
| `static/_headers` | Add HSTS, replace unsafe-inline with script hashes |
| `static/.well-known/security.txt` | **Create** — RFC 9116 security contact file |
| `content/stack/index.md` | Add Security section |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] `_headers` file appears in `public/` with HSTS and script hashes
- [x] `.well-known/security.txt` appears in `public/` output
- [x] security.txt contains required RFC 9116 fields (Contact, Expires)
- [x] CSP script hashes match actual inline scripts in build output (8 hashes, 159 pages)
- [ ] Site renders correctly on localhost (`hugo server -D`)
