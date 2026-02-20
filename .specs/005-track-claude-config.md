# 005: Track .claude/ and CLAUDE.md in Git

**Branch**: `feature/track-claude-config`
**Created**: 2026-02-19

## Summary

Remove `.claude/`, `CLAUDE.md`, and `node_modules/` from `.gitignore` so that Claude Code commands and project instructions are version-controlled. Also removes the stale `node_modules/` entry since the project has no npm dependencies.

## Requirements

- Remove `.claude/` from `.gitignore`
- Remove `CLAUDE.md` from `.gitignore`
- Remove `node_modules/` from `.gitignore` (no npm deps in project)
- Commit `.claude/commands/` (feature.md, ship.md, setup.md) so they're tracked
- Commit `CLAUDE.md` so project instructions are tracked
- Do NOT commit `.claude/settings.json` or other local config — only commands

## Design

Edit `.gitignore` to remove the three entries. Then `git add` the command files and CLAUDE.md. Add a selective ignore for `.claude/` local state files that shouldn't be tracked (settings, cache, etc.) by only tracking `.claude/commands/`.

Updated `.gitignore`:
```
public/
resources/
.hugo_build.lock
```

## Files to Modify

| File | Change |
|------|--------|
| `.gitignore` | Remove `.claude/`, `CLAUDE.md`, and `node_modules/` entries |
| `.claude/commands/feature.md` | Now tracked (already exists) |
| `.claude/commands/ship.md` | Now tracked (already exists, includes recent bug fixes) |
| `.claude/commands/setup.md` | Now tracked (already exists) |
| `CLAUDE.md` | Now tracked (already exists) |

## Test Plan

- [x] `.claude/commands/` files are tracked in git
- [x] `CLAUDE.md` is tracked in git
- [x] Hugo builds with no errors (`hugo --minify`)
