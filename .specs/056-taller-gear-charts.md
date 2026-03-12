# 056: Taller Gear Charts

**Branch**: `feature/taller-gear-charts`
**Created**: 2026-03-11

## Summary

The timeline and category (phone vs. dedicated camera) charts in the camera gear timeline post need much more vertical height. Both charts should be doubled in height from their current values. Sparklines on camera cards must remain unchanged.

## Requirements

- Increase the timeline chart height: `aspect-ratio: 1/2` → `aspect-ratio: 1/1`
- Reduce the category chart from oversized: `aspect-ratio: 5/16` → `aspect-ratio: 5/6`
- Do NOT change sparkline heights (20px mobile / 32px desktop)
- Do NOT change any other chart behavior or styling

## Design

Both charts use inline `aspect-ratio` on their container `<div>`. Change the ratio values so the height doubles while keeping width at 100%.

## Files to Modify

| File | Change |
|------|--------|
| `content/posts/2026-03_camera-gear-timeline.md` | Change timeline container `aspect-ratio` from `1/2` to `1/1` |
| `content/posts/2026-03_camera-gear-timeline.md` | Change category container `aspect-ratio` from `5/16` to `5/6` |

## Test Plan

- [x] Timeline chart renders ~2x taller than before
- [x] Category chart renders ~2x taller than before
- [x] Sparkline histograms on camera cards are unchanged (20px / 32px)
- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
