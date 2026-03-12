# 053: Tighten Blog Post Screenshots

**Branch**: `feature/tighten-blog-screenshots`
**Created**: 2026-03-11

## Summary

The "Building MrMatt.io: Spec-Driven Development" blog post has two screenshots with excess blank space and unchecked checkboxes. Crop the dead space and replace the PR screenshot with an updated version showing all test plan checkboxes checked.

## Requirements

- Crop `specs-directory.png` to remove ~260px of blank dark space below the last file listing
- Replace `pr-test-plan.png` with a new screenshot from GitHub PR #5340 showing all test plan checkboxes checked, with no excess blank space
- No changes to blog post markdown — image filenames stay the same

## Design

Both images are referenced in `content/posts/2026-03_building-mrmatt-io-specs.md` by path. Since we keep the same filenames, only the image files need to change.

1. **specs-directory.png** — crop from 900x700 to 900x440, removing blank space below row ~410
2. **pr-test-plan.png** — replace with a cropped screenshot of PR #5340 (all checkboxes now checked via `gh pr edit`), cropped to show title + merged badge + full body including "Generated with Claude Code"

## Files to Modify

| File | Change |
|------|--------|
| `static/images/building-mrmatt-io/specs-directory.png` | Crop bottom blank space |
| `static/images/building-mrmatt-io/pr-test-plan.png` | Replace with updated screenshot (checked boxes, no blank space) |

## Test Plan

- [x] `specs-directory.png` has no excessive blank space below file listing
- [x] `pr-test-plan.png` shows all test plan checkboxes checked
- [x] `pr-test-plan.png` has no excessive blank space
- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Both images render correctly in the blog post on localhost (`hugo server -D`)
