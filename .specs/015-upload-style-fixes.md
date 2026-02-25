# 015: Upload Page Style Fixes & Regression Fix

**Branch**: `feature/upload-style-fixes`
**Created**: 2026-02-24

## Summary

Fix regressions in the photo upload PWA where AI-generated title/alt/description aren't displaying, the regenerate button doesn't work (both caused by SW caching stale HTML), and restyle the entire upload page to match the main site's aesthetic.

## Requirements

- Revert AI title, alt text, and description from editable `<input>`/`<textarea>` back to read-only text (`<span>`) — use `.textContent` in JS
- Keep the feedback `<textarea>` and Regenerate button
- Fix the submit handler to read from `.textContent` instead of `.value`
- Restyle upload page to match main site: same heading weight/size, max-width `40em` at `width: 90%`, consistent border colors (#e1e1e1), spacing
- Clean up the AI section layout: results as label+value pairs, feedback textarea full-width below with Regenerate button
- Bump service worker cache from v3 to v4
- Add `?v=4` cache-bust query params to `style.css` and `app.js` script/link tags in `index.html` so the SW can't serve stale files

## Design

### HTML changes (`static/upload/index.html`)
- Revert AI result fields from `<input>`/`<textarea>` to `<span>` elements:
  - `<span id="ai-title"></span>` (was `<input type="text" id="ai-title">`)
  - `<span id="ai-alt"></span>` (was `<input type="text" id="ai-alt">`)
  - `<span id="ai-description"></span>` (was `<textarea id="ai-description">`)
- Keep labels as `<span class="ai-label">` (not `<label>` since they're not for inputs)
- Keep feedback `<textarea id="ai-feedback">` and `<button id="regenerate-btn">`
- Add cache-bust `?v=4` to style.css and app.js references

### JS changes (`static/upload/app.js`)
- Change `aiTitle.value`, `aiAlt.value`, `aiDesc.value` → `.textContent` everywhere
- In `describePhoto`: set `.textContent = ''` to clear, `.textContent = data.title` to populate
- In submit handler: read `aiTitle.textContent.trim()` etc.
- In reset after upload: set `.textContent = ''`

### CSS changes (`static/upload/style.css`)
- Match main site layout: `max-width: 40em; width: 90%` on body (was `max-width: 500px`)
- Match heading style: `h1 { font-weight: 300; font-size: 2rem; letter-spacing: -0.1rem; }`
- Use site's border color `#e1e1e1` for section borders and separators
- AI results section: clean label:value pairs on a subtle background
- AI field values displayed as text (no input borders/boxes)
- Feedback area: full-width textarea with Regenerate button right-aligned below
- Remove input/textarea styles from `.ai-field` (no longer inputs)
- Match button styles to site conventions

### SW changes (`static/upload/sw.js`)
- Bump cache `photo-upload-v3` → `photo-upload-v4`

## Files to Modify

| File | Change |
|------|--------|
| `static/upload/index.html` | Revert AI fields to spans, cache-bust asset URLs |
| `static/upload/app.js` | Use .textContent instead of .value for AI fields |
| `static/upload/style.css` | Restyle to match main site aesthetic |
| `static/upload/sw.js` | Bump cache to v4 |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] AI title, alt, and description display as text (not editable inputs)
- [x] AI results populate after photo selection
- [x] Feedback textarea is full-width, multi-line
- [ ] Regenerate button works — calls API with feedback, updates results
- [x] Upload page heading and layout match main site style
- [x] Service worker cache is v4
- [ ] Upload succeeds with AI-generated metadata in front matter
