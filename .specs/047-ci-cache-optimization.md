# 047: CI Cache Optimization

**Branch**: `feature/ci-cache-optimization`
**Created**: 2026-03-09

## Summary

Hugo build times are 8-10 minutes because it reprocesses ~450+ image variants from scratch on every CI run. The `resources/_gen/` directory (219MB locally) contains cached processed images but is gitignored, so CI always starts cold. Adding `actions/cache` for the resources directory and pinning the Hugo version will cut most builds from ~9 minutes to ~1-2 minutes.

## Requirements

- Cache Hugo's `resources/` directory between CI builds using `actions/cache@v4`
- Cache key based on photography content hash so new/changed images trigger reprocessing
- Restore-keys fallback ensures partial cache hits for incremental processing
- Pin Hugo version to `0.157.0` instead of `latest` for reproducibility
- PR builds share the same cache for fast validation
- No changes to site content or build output — purely CI pipeline optimization

## Design

### Root Cause Analysis

The `hugo --minify` build step takes 8m39s (91% of total build time). This is because:
- 90 photography pages each generate 5+ image variants (.Fill, .Process, .Filter operations)
- Templates in `layouts/photography/list.html` create 3 thumbnail sizes + full-res + watermarked versions
- `layouts/partials/extend_head.html` generates OG and JSON-LD images for every photography page
- With no cached `resources/` directory in CI, all ~450+ transforms run from scratch every time

### Solution

1. **`actions/cache@v4`** for `resources/` directory:
   - Primary key: `hugo-resources-${{ hashFiles('content/photography/**') }}`
   - Restore key: `hugo-resources-` (falls back to most recent cache)
   - On cache hit: Hugo skips already-processed images, build drops to ~1-2 min
   - On cache miss (new photos): restores partial cache, processes only new images, saves updated cache

2. **Pin Hugo version** to `0.157.0`:
   - Avoids unpredictable version changes that could invalidate caches
   - Ensures reproducible builds

### Build step timings (current)

| Step | Time | % |
|------|------|---|
| Checkout | 13s | 2% |
| Setup Hugo | 1s | <1% |
| **Hugo Build** | **8m 39s** | **91%** |
| CSP Headers | <1s | <1% |
| Wrangler | 32s | 5% |
| Release | 1s | <1% |

## Files to Modify

| File | Change |
|------|--------|
| `.github/workflows/deploy.yml` | Add `actions/cache@v4` step for `resources/`, pin Hugo version to `0.157.0` |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`) — 203 pages, 721 processed images
- [x] Workflow YAML is valid (no syntax errors)
- [x] Cache step is placed before the Build step
- [x] Cache key uses `hashFiles('content/photography/**')` with restore-keys fallback
- [x] Hugo version pinned to `0.157.0` instead of `latest`
- [x] PR builds and main builds both benefit from caching (no `if:` condition on cache step)
- [x] No changes to build output or site content (only deploy.yml modified)
