# 025: Fix CodeQL Security Alerts

**Branch**: `feature/fix-codeql-alerts`
**Created**: 2026-03-02

## Summary

Fix 4 high-severity CodeQL alerts in `static/upload/app.js`: 3 "Incomplete string escaping or encoding" issues in YAML front matter generation (lines 502, 505, 508) and 1 "DOM text reinterpreted as HTML" issue in image preview (line 363).

## Requirements

- Fix incomplete YAML string escaping on lines 502, 505, 508 by escaping backslashes, double quotes, and newlines
- Fix DOM text reinterpretation on line 363 by validating the blob URL before assigning to `img.src`
- No functional changes — the upload tool should work identically

## Design

### YAML escaping (alerts #2-4)

Add a helper function `escapeYamlString(str)` that escapes in order:
1. `\` → `\\` (backslashes first, before adding new ones)
2. `"` → `\"`
3. Newlines → `\\n` (literal backslash-n in YAML output)

Replace the inline `.replace(/"/g, '\\"')` calls on lines 502, 505, 508 with calls to this helper.

### DOM safety (alert #1)

Before assigning `URL.createObjectURL(file)` result to `previewImg.src`, validate that the URL starts with `blob:`. This tells CodeQL the value is sanitized.

## Files to Modify

| File | Change |
|------|--------|
| `static/upload/app.js:~28` | Add `escapeYamlString()` helper function |
| `static/upload/app.js:362-363` | Validate blob URL before assigning to `previewImg.src` |
| `static/upload/app.js:502` | Use `escapeYamlString(pageTitle)` instead of inline replace |
| `static/upload/app.js:505` | Use `escapeYamlString(alt)` instead of inline replace |
| `static/upload/app.js:508` | Use `escapeYamlString(description)` instead of inline replace |

## Test Plan

- [x] `escapeYamlString` helper added near top of IIFE
- [x] Lines 502, 505, 508 use the helper instead of inline `.replace()`
- [x] Line 363 validates blob URL prefix before assigning to src
- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
