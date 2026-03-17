# 063: Autoresearch Web Performance Blog Post

**Branch**: `feat/autoresearch-blog-post`
**Created**: 2026-03-16

## Summary

Publish the blog post documenting the autoresearch web performance experiment (spec 062). The post analyzes 200 automated Lighthouse experiments, presents results with interactive Chart.js visualizations, and distills findings about resource loading, CSS containment, and measurement noise.

## Requirements

- [x] Blog post at `content/posts/2026-03_autoresearch-webperf.md`
- [x] Title: "Autoresearch for Web Performance: 20% Faster Overnight"
- [x] Tags: `software-development`, `this-site`
- [x] `draft: false`
- [x] Hero illustration at `static/images/ai-experiment-rig.png` (cropped, responsive figure)
- [x] 7 Chart.js visualizations with dark mode support:
  - LCP timeline (scatter + best-so-far trendline)
  - Experiment outcomes (doughnut)
  - Experiments by category (grouped horizontal bar)
  - Biggest LCP improvements (horizontal bar)
  - Preload impact (vertical bar, positive/negative)
  - Build size over time (area line)
  - Noise demonstration (grouped bar)
- [x] All chart data verified against raw `autoresearch/results.tsv`
- [x] Summary table with verified metrics
- [x] Description and summary meta fields populated

## Data Accuracy

All numbers in the post were audited against the raw experiment log:

- Kept: 147 (74%), Discarded: 47 (23%), Crashed: 4 (2%), Reverted: 1
- Structure hash violations: 6
- Top wins verified as deltas from previous best LCP
- Preload impact deltas verified against best LCP at time of each experiment
- Noise range: up to +/-370ms (not +/-150ms)
- Build sizes converted correctly from KB to MB

## Test Plan

- [ ] `hugo server` builds without errors
- [ ] Post renders at `/posts/autoresearch-webperf/`
- [ ] All 7 charts render in both light and dark mode
- [ ] Chart tooltips display correct data
- [ ] Hero image displays with caption
- [ ] Post appears in homepage journal list and RSS feed
