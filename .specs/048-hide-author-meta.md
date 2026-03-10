# 048: Hide Author from Post Metadata

**Branch**: `feature/hide-author-meta`
**Created**: 2026-03-09

## Summary

The post metadata line shows `map[name:Matt Walker]` due to the author being configured as a TOML table instead of a plain string. Since this is a personal site with a single author, the author display should be hidden entirely.

## Requirements

- Hide the author name from post metadata (date · reading time line)
- Remove the `[params.author]` table and replace with a simple string for schema/SEO purposes

## Design

Set `hideAuthor = true` in `[params]` and change `[params.author]` from a TOML table to a simple string value. PaperMod respects `hideAuthor` to suppress author display in post metadata.

## Files to Modify

| File | Change |
|------|--------|
| `hugo.toml` | Set `hideAuthor = true`, change `[params.author]` table to string |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
- [ ] Post metadata no longer shows author name or `map[name:]` text
