# 046: Google Takeout Gallery Batch Import

**Branch**: `feat/google-takeout-gallery-batch`
**Created**: 2026-03-08

## Summary

Batch import 51 curated photos from a Google Takeout archive into the site's photography gallery, with AI-generated descriptions. Accompanied by a blog post documenting the curation process.

## Context

A full Google Takeout export (15 zips, ~723GB, ~100K photos spanning 2003-2025) was processed through a multi-pass Python pipeline to identify gallery-worthy landscape, nature, travel, and hobby photography. The pipeline used metadata scoring, image quality analysis, perceptual hash deduplication, OpenCV face/skin detection, and manual contact sheet review to reduce 98,312 candidates down to 51 final picks.

## Pipeline Stages

| Stage | Method | In | Out |
|-------|--------|-----|-----|
| Pass 0 | JSON sidecar metadata scoring | 98,312 | 98,312 (scored) |
| Pass 1 | Thumbnail extraction + quality scoring (sharpness, colorfulness, contrast) | 85,876 | 85,876 (scored) |
| Pass 2 | Perceptual hash dedup (hamming distance <= 8) | 67,392 | 44,404 |
| Pass 2b | OpenCV Haar cascade face detection + screenshot detection | 44,404 | 32,074 |
| Pass 2c | HSV skin tone detection + nature/outdoor classification | 32,074 | 12,812 |
| Pass 3 | Contact sheet generation + manual visual review | 12,812 | ~143 |
| Pass 4 | Final strict curation by category | 143 | 51 |

Pipeline scripts live at `F:/Photos/scripts/pass*.py` (local, not committed).

## Requirements

### Gallery Import
- Create Hugo page bundles for all 51 photos in `content/photography/`
- Directory format: `{YYYY-MM-DD}-{kebab-slug}/` with `photo.{ext}` and `index.md`
- Extract EXIF dates where available, fall back to filename-encoded dates
- Correct Maine 2009 photos that have wrong EXIF dates (2011 upload date vs 2009 capture date)
- Generate title, alt text, and description for each photo matching existing gallery tone
- Descriptions: conversational, 1-2 sentences, personal voice

### Blog Post
- File: `content/posts/2026-03_google-takeout-gallery-curation.md`
- Documents the pipeline process with data table showing reduction at each stage
- Covers scoring methodology, people filtering approach, and visual review process
- Tags: `software-development`, `photography`, `ai`

### Spec Files
- Number the existing `series-building-mrmatt-io.md` spec as `045`
- Add this spec as `046`

## Implementation

1. `tools/batch_gallery_import.py` — EXIF extraction, directory creation, photo copying
2. `tools/rename_bundles.py` — Rename timestamp-based dirs to descriptive slugs
3. AI vision (Claude Opus) reads each photo and writes index.md with title/alt/description
4. Blog post written from pipeline data and process documentation

## Test Plan

- [ ] `hugo --minify` builds without errors
- [ ] All 51 new photos appear in `/photography/` gallery
- [ ] Blog post renders at `/posts/google-takeout-gallery-curation/`
- [ ] No broken images or missing metadata
- [ ] Existing 40 gallery photos still render correctly
- [ ] Dates are correct (especially Maine 2009 photos)
