# 065: Writing & Illustration Style Guides

**Branch**: `feat/style-guides`
**Created**: 2026-03-16

## Summary

Create two style reference documents that capture Matt's personal writing voice and the site's editorial illustration style. These guides serve as references for AI-assisted content creation, ensuring future blog posts sound like Matt and future illustrations maintain visual consistency.

## Motivation

As AI-assisted writing becomes a regular part of the blog workflow, it's important to have a codified reference for Matt's actual voice. Analysis of the 2007–2017 corpus revealed clear differences between human-written and AI-written posts (ellipses vs em dashes, casual imperfection vs polished parallelism, playful humor vs restrained self-awareness). The writing guide captures what makes Matt's voice distinctive so AI tools can match it.

Similarly, the pen-and-ink editorial illustrations from the "Membrane" and "Autoresearch" posts established a visual language worth preserving across future posts.

## Requirements

- [x] `WRITING-STYLE.md` at repo root — comprehensive writing style guide covering:
  - Voice and tone
  - Sentence structure patterns
  - Punctuation habits (especially the ellipsis as signature mark, and avoidance of em dashes)
  - Vocabulary (colloquialisms Matt uses, words to avoid)
  - Recurring verbal patterns and openers/closers
  - Formatting conventions
  - Content structure templates by post type
  - The "imperfection factor" — how Matt's posts differ from AI polish
- [x] `ILLUSTRATION-STYLE.md` at repo root — illustration style guide covering:
  - Medium (monochrome pen-and-ink)
  - Technique (cross-hatching, stippling)
  - Compositional elements (small human figure, conceptual metaphors, labels)
  - Tone (technical but approachable, editorial not corporate)
  - Image specifications (format, size, naming)
  - Reference illustrations with descriptions
- [x] Spec file at `.specs/064-style-guides.md`

## Source Analysis

The writing style guide was derived from close reading of all human-written posts (2007–2017 plus the 2026 website update), excluding the AI-written 2026-03 series. Key differentiators identified:

1. Matt uses ellipses (...) where AI uses em dashes (—)
2. Matt's sentences are loose and varied; AI writes careful parallelism
3. Matt's posts have typos and comma splices; AI posts are immaculate
4. Matt's sections are unevenly sized; AI sections are perfectly balanced
5. Matt uses words like "sweet," "stout," "floored"; AI uses "durable," "converge," "orchestrating"
6. Matt ends with "More to follow..." or "I am quite happy."; AI ends with thematic callbacks

The illustration style guide was derived from the two editorial illustrations: `ai-capability-membrane-model.png` and `ai-experiment-rig.png`.

## Test Plan

- [ ] Both files render correctly on GitHub
- [ ] Writing guide is referenced in future blog post workflows
- [ ] Illustration guide is referenced when creating new post illustrations
