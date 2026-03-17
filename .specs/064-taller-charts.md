# 064: Taller Chart Aspect Ratios Across All Posts

**Branch**: `feature/taller-charts`
**Created**: 2026-03-16

## Summary

Charts across all three data-visualization posts are vertically compressed, making them less impactful. This sweep updates CSS aspect ratios on all chart containers to give them more vertical space, making the data easier to read and more visually striking.

## Requirements

- Increase vertical height of all `5/2` (2.5:1) aspect-ratio chart containers — these are the most compressed
- Increase vertical height of `4/3` grid chart containers
- Increase vertical height of `2/1` chart containers
- Leave already-tall charts alone (`1/1` timeline, `5/6` category in camera gear post)
- Leave custom canvas elements (heatmap, sparklines) unchanged
- No changes to Chart.js config — only CSS container aspect ratios

## Design

All charts use the same pattern: a `<div>` wrapper with inline `style="... aspect-ratio:X/Y ..."` containing a `<canvas>`. Chart.js has `maintainAspectRatio: false` so it fills whatever container size CSS gives it. We only need to change the `aspect-ratio` values in the inline styles.

**New aspect ratios:**

| Old ratio | New ratio | Context |
|-----------|-----------|---------|
| `5/2` (2.5:1) | `16/9` (~1.78:1) | Full-width charts — ~40% taller |
| `4/3` (1.33:1) | `1/1` (1:1) | Grid charts — 33% taller, square |
| `2/1` (2:1) | `3/2` (1.5:1) | Top wins horizontal bar — 33% taller |
| `1/1` | `1/1` | No change (camera timeline) |
| `5/6` | `5/6` | No change (camera category) |

## Files to Modify

| File | Change |
|------|--------|
| `content/posts/2026-03_autoresearch-webperf.md` | Update aspect ratios on 7 chart containers |
| `content/posts/2026-03_photography-by-the-numbers.md` | Update aspect ratios on 11 chart containers + heatmap |
| `content/posts/2026-03_camera-gear-timeline.md` | No changes needed (already 1/1 and 5/6) |

## Test Plan

- [ ] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
- [ ] Autoresearch post: all 7 charts render taller, no overflow or clipping
- [ ] Photography post: all 11 charts + heatmap render taller, grid layouts still work
- [ ] Camera gear timeline post: unchanged, still renders correctly
- [ ] Charts remain responsive on narrow viewports
