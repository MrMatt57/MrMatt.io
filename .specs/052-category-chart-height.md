# 052 — Increase category chart height

## Summary

The "Phone vs. dedicated camera" stacked bar chart in the camera gear timeline post is too short to read comfortably. Change the container aspect ratio from `5/2` (very wide and flat) to `5/4` (more square) so the chart is roughly 2.5x taller and the category breakdown is easier to interpret.

## Changes

- `content/posts/2026-03_camera-gear-timeline.md`: Change the `category-chart` container `aspect-ratio` from `5/2` to `5/4`

## Test plan

- [x] Category chart ("Phone vs. dedicated camera") renders visibly taller
- [x] Timeline chart ("The timeline") is unaffected
- [x] Sparkline histograms on camera cards are unaffected
- [x] Chart remains responsive on narrow viewports
