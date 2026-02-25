# 013: Upload Feedback Polish

**Branch**: `feature/upload-feedback-polish`
**Created**: 2026-02-24

## Summary

Polish the photo upload PWA's AI feedback/regenerate flow. The feedback input is too small (single-line `<input>` crammed in a flex row), the regenerate button may not work due to SW cache staleness, the AI status during regeneration isn't visible enough, and the separate "Caption" field is redundant. Make AI results directly editable and remove the caption field.

## Requirements

- Change the feedback input from `<input type="text">` to a `<textarea>` (2-3 rows, full width of the AI section)
- Move the Regenerate button to its own row below the textarea
- Make AI title, alt text, and description fields editable (text inputs / textarea) instead of read-only `<span>` elements
- Remove the separate "Caption (auto-filled by AI, editable)" field — use the editable AI title directly for Hugo front matter and slug
- Show clear status text during AI calls: "Analyzing photo..." on initial, "Regenerating with your feedback..." on regenerate
- Bump service worker cache from v2 to v3 to force fresh assets
- Update `app.js` to read from the editable AI fields for upload, not from the `aiMeta` object

## Design

### HTML changes (`static/upload/index.html`)
- Replace `<span id="ai-title">` with `<input type="text" id="ai-title">`
- Replace `<span id="ai-alt">` with `<input type="text" id="ai-alt">`
- Replace `<span id="ai-description">` with `<textarea id="ai-description" rows="2">`
- Change feedback `<input type="text">` to `<textarea id="ai-feedback" rows="2">`
- Move Regenerate button out of the `.ai-feedback` flex row — put it below the textarea
- Remove the caption field div entirely (lines 59-62)

### JS changes (`static/upload/app.js`)
- Remove `captionInput` references
- Update `describePhoto` to populate editable inputs via `.value` instead of `.textContent`
- Change initial status to "Analyzing photo..." and regenerate status to "Regenerating with your feedback..."
- In the regenerate click handler, pass feedback text
- In the submit handler, read title from `aiTitle.value`, alt from `aiAlt.value`, description from `aiDesc.value`
- Derive slug from the AI title input value
- Remove `aiMeta` object — read directly from DOM inputs

### CSS changes (`static/upload/style.css`)
- Change `.ai-feedback` from `display: flex` to `display: block` (stack textarea + button)
- Style `.ai-feedback textarea` full width, matching the section aesthetic
- Style editable AI field inputs inside `.ai-field`
- Remove `.field input[type="text"]` styles that targeted the caption field (these are generic, keep them)

### SW changes (`static/upload/sw.js`)
- Bump cache `photo-upload-v2` → `photo-upload-v3`

## Files to Modify

| File | Change |
|------|--------|
| `static/upload/index.html` | Editable AI fields, textarea for feedback, remove caption field |
| `static/upload/app.js` | Read from editable inputs, better status messages, remove captionInput |
| `static/upload/style.css` | Style editable AI fields and stacked feedback layout |
| `static/upload/sw.js` | Bump cache to v3 |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Feedback area is a multi-line textarea spanning full width of AI section
- [x] Regenerate button sits below the textarea on its own row
- [x] AI title, alt, and description are editable input fields pre-filled by AI
- [x] Status shows "Analyzing photo..." during initial AI call
- [x] Status shows "Regenerating with your feedback..." when regenerating
- [x] Editing AI title directly changes the uploaded Hugo page title
- [x] No "Caption" field visible — removed entirely
- [ ] Upload succeeds using values from the editable AI fields
- [x] Service worker cache is v3
