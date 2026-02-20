# 006: Update About Page

**Branch**: `feature/update-about-page`
**Created**: 2026-02-19

## Summary

Rewrite the About Me page from a single-paragraph placeholder to a richer, more polished personal bio. Cover work (enterprise data & AI, agentic engineering, spec-driven development), hobbies (RC planes, amateur radio, RV travel, hiking, rowing, coffee), and keep the boat photo and contact links.

## Requirements

- Replace the thin one-liner intro with a more expressive opening — not just "software engineer and technology enthusiast"
- Frame work around enterprise data platforms, AI, agentic engineering, semantic data models — without naming an employer or job title
- Mention spec-driven development and agentic engineering as a personal methodology (not vibe coding)
- Describe hobbies with enough color to feel real: RC planes, amateur radio, hiking, RV camping/travel, rowing (Concept2), coffee (roasting, single origin, Gaggia Classic with Gagiuino, V60, Moccamaster, AeroPress)
- Keep the boat photo (`/img/boat.jpg`)
- Keep the Contact section with GitHub and LinkedIn links
- Tone: polished but personal — first person, warm, confident, not corporate
- Update the front matter date to 2026-02-19

## Design

Structure the page as:

1. **Opening paragraph** — who Matt is, what drives him. Something better than "software engineer and technology enthusiast." Think along the lines of someone who builds data and AI platforms by day and is a serial hobbyist the rest of the time.

2. **Work paragraph** — enterprise data platforms, AI-capable infrastructure, agentic automation, semantic data models. Mention spec-driven development as an approach. Keep it conversational, not a resume. No employer name, no job title.

3. **Hobbies section** — a paragraph or two covering the range: RC planes, amateur radio, hiking, RV camping and travel, rowing on a Concept2, and coffee. Coffee should get a sentence or two — roasting single-origin beans, dialing in espresso on a Gagiuino-modded Gaggia Classic, brewing on a V60, Moccamaster, AeroPress. Frame it as a full-on coffee nerd, discovered later in life.

4. **Boat photo** — keep as-is.

5. **Contact section** — keep GitHub and LinkedIn links as-is.

## Files to Modify

| File | Change |
|------|--------|
| `content/about/index.md` | Rewrite page content as described above |

## Test Plan

- [ ] Hugo builds with no errors (`hugo --minify`)
- [ ] About page renders correctly on localhost (`hugo server -D`)
- [ ] Boat photo still displays
- [ ] Contact links still work
