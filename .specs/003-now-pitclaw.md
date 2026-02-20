# 003: Add PitClaw to Now Page

**Branch**: `feature/now-pitclaw`
**Created**: 2026-02-19

## Summary

Add a link to the PitClaw side project on the /now/ page. PitClaw is an ESP32-S3 BBQ temperature controller with a touchscreen and Wi-Fi, hosted at https://github.com/MrMatt57/pitclaw.

## Requirements

- Add PitClaw as a linked item in the "Side Projects" section of `content/now/index.md`
- Link to the GitHub repo: https://github.com/MrMatt57/pitclaw
- Keep the description brief and consistent with the page's tone
- Keep the existing site rebuild bullet point

## Design

Add a second line to the "Side Projects" section with a short description of PitClaw and a link to the repo. The description should be concise — something like "PitClaw — an ESP32-based BBQ temperature controller" with a link on the project name.

## Files to Modify

| File | Change |
|------|--------|
| `content/now/index.md` | Add PitClaw entry to the Side Projects section |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] /now/ page renders correctly on localhost (`hugo server -D`)
- [x] PitClaw link points to https://github.com/MrMatt57/pitclaw
