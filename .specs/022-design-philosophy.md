# 022: Promote and Expand Design Philosophy

**Branch**: `feature/design-philosophy`
**Created**: 2026-02-24

## Summary

Move "Design Philosophy" from the bottom of both the README and stack page to the top (above "Built With" in README, above all tech sections in stack page). Expand from 4 to 8 bullets, adding points about zero dependencies, owning your stack, AI as a collaborator, and spec-driven development — all demonstrated by the actual site.

## Requirements

- Move Design Philosophy to the top of the stack page (after the GitHub source link, before Static Site)
- Add a new "## Design Philosophy" section in README.md, positioned between the intro and "## Built With"
- Expand to 8 bullets total:
  1. Minimal and fast — no JS frameworks, no bloat, static HTML/CSS
  2. Content-first — the site publishes writing and serves as a professional presence
  3. Zero dependencies — vanilla JS, no npm, no external libraries
  4. Own your stack — static files you control, no platform lock-in
  5. Low maintenance — no comment systems, no dynamic backends
  6. AI as a collaborator — Claude generates, the human reviews and refines
  7. Spec-driven development — plan before you build, every feature documented
  8. Automation where it matters — AI and APIs handle the tedious parts so publishing stays frictionless
- Remove the old "Design Philosophy" section from the bottom of the stack page (it's been moved, not duplicated)
- README version should use the same bold-label format as Built With items (one-line summaries)
- Stack page version keeps the bulleted list format

## Design

### README.md

Add between the `**[mrmatt.io](https://mrmatt.io)**` line and `## Built With`:

```markdown
## Design Philosophy

**Minimal and fast** — no JS frameworks, no bloat, static HTML/CSS.
**Content-first** — the site publishes writing and serves as a professional presence.
**Zero dependencies** — vanilla JS, no npm, no external libraries anywhere.
**Own your stack** — static files you control, no platform lock-in.
**Low maintenance** — no comment systems, no dynamic backends.
**AI as a collaborator** — Claude generates, the human reviews and refines.
**Spec-driven development** — plan before you build, every feature documented.
**Automation where it matters** — AI and APIs handle the tedious parts so publishing stays frictionless.
```

### Stack page

Move the `### Design Philosophy` section from the bottom to just after the GitHub source link (before `### Static Site`). Update from 4 bullets to 8 bullets matching the content above.

## Files to Modify

| File | Change |
|------|--------|
| `README.md` | Add "## Design Philosophy" section between intro and "## Built With" |
| `content/stack/index.md` | Move Design Philosophy to top, expand from 4 to 8 bullets |

## Test Plan

- [x] README has Design Philosophy section above Built With
- [x] Stack page has Design Philosophy as the first section (after GitHub link)
- [x] Both have all 8 philosophy points
- [x] Old Design Philosophy section removed from bottom of stack page
- [x] Hugo builds with no errors (`hugo --minify`)
- [x] Site renders correctly on localhost (`hugo server -D`)
