# 001: Update Profile Image

**Branch**: `feature/update-profile-image`
**Created**: 2026-02-19

## Summary

Replace the existing rectangular profile photo (`MattWalker.png`) on the home page with a new circular cartoon/illustrated avatar. Adjust CSS so the circular image displays cleanly with text flowing to the right.

## Requirements

- Replace the current profile image with the new illustrated avatar
- Image should be positioned on the left with all text to the right
- Image should display as a clean circle (the source image already contains a circular frame)
- Sizing should be balanced with the text — approximately 175x175px
- The background of the image should blend with the page background in both light and dark mode
- Maintain the link to `/about/` on the image
- Update alt text appropriately

## Design

The current layout already uses `float: left` on the `.avatar` class, which positions text to the right. The main changes are:

1. **Image file**: Copy the new image to `static/images/` as `MattWalker-avatar.png`. Keep the old `MattWalker.png` in case it's needed elsewhere.
2. **Layout**: Update `layouts/index.html` to reference the new image filename.
3. **CSS**: Adjust `.home-about .avatar` dimensions from 175x216 (rectangular) to 175x175 (square) since the new image is circular/square. Add `border-radius: 50%` to clip to a perfect circle and `object-fit: cover` for clean rendering. The image has an off-white background, so adding `border-radius: 50%` will clip away the corners and show only the circle.
4. **Min-height**: Reduce `.home-about` min-height from 216px to 175px to match.

## Files to Modify

| File | Change |
|------|--------|
| `static/images/MattWalker-avatar.png` | Add new avatar image file |
| `layouts/index.html` | Update image `src` to new filename |
| `assets/css/extended/custom.css` | Adjust avatar dimensions to square, add border-radius |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
- [x] Image displays as a circle on the home page
- [x] Text flows to the right of the image
- [ ] Image looks correct in both light and dark mode
- [x] Image links to `/about/`
