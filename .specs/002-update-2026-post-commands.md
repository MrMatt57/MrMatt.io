# 002: Update 2026 Post — Custom Commands Section

**Branch**: `feature/update-2026-post-commands`
**Created**: 2026-02-19

## Summary

Update the "What's actually different this time" section of the 2026 website update post to reflect the current spec-driven development workflow. The old text references a "spec document with five phases" and custom commands; the new text should describe the `/feature` and `/ship` commands and how each change gets a spec file in `.specs/`.

## Requirements

- Update the paragraph on line 45 of the post that mentions custom commands and phases
- Describe the spec-driven workflow: `/feature` creates a numbered spec in `.specs/`, sets up a worktree, implements, then `/ship` commits, pushes, creates a PR, and cleans up
- Keep the tone consistent with the rest of the post — conversational, concise
- Do not change any other sections of the post

## Design

Replace the single paragraph (line 45) that currently reads:

> I have a spec document with five phases and custom commands (`/setup`, `/feature`, `/ship`) that walk through the rebuild step by step. The whole thing is in the repo if you're curious.

With updated text that describes:
1. Spec-driven development — each change gets a numbered spec in `.specs/`
2. The `/feature` command — creates the spec, sets up a git worktree, implements the feature
3. The `/ship` command — commits, pushes, creates a PR, waits for CI, merges, cleans up
4. That this is an ongoing workflow for all future site changes, not just the initial rebuild

## Files to Modify

| File | Change |
|------|--------|
| `content/posts/2026-02_website-update-2026.md` | Update the custom commands paragraph in "What's actually different this time" section |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Post renders correctly on localhost (`hugo server -D`)
- [x] Only the target paragraph is changed; rest of post is untouched
