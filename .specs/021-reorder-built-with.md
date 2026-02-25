# 021: Reorder Built With Sections

**Branch**: `feature/reorder-built-with`
**Created**: 2026-02-24

## Summary

Reorder the "Built With" sections in both `README.md` and the `/stack` page (`content/stack/index.md`) to lead with the core site and development workflow, then infrastructure, then the photo pipeline features. This puts the most broadly impressive tech (spec-driven AI dev workflow, serverless, CI/CD) before the domain-specific features (photo PWA, AI descriptions).

## Requirements

- Reorder README.md "Built With" section to this order:
  1. Static Site
  2. Spec-Driven Workflow (renamed from "Development")
  3. Serverless Backend
  4. CI/CD
  5. Automated Publishing
  6. Photo Upload PWA
  7. AI-Powered Descriptions
- Reorder stack page sections to match:
  1. Static Site
  2. Development (spec-driven workflow)
  3. Serverless Backend
  4. CI/CD
  5. Hosting & DNS
  6. Automated Publishing
  7. Photo Upload
  8. AI-Powered Descriptions
  9. Design Philosophy
- Content of each section stays the same — only the order changes
- In the README, rename "Development" to "Spec-Driven Workflow" for the bold label (content stays the same)

## Design

Pure reorder of existing content blocks. No content changes, no new sections. Just cut-and-paste the blocks into the new order in both files.

## Files to Modify

| File | Change |
|------|--------|
| `README.md` | Reorder "Built With" items and rename "Development" to "Spec-Driven Workflow" |
| `content/stack/index.md` | Reorder sections to match new priority order |

## Test Plan

- [x] README "Built With" sections are in the correct new order
- [x] Stack page sections are in the correct new order
- [x] No content was lost or changed — only ordering
- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
