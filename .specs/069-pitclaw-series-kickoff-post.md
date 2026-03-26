# 069: PitClaw Series Kickoff Post

**Branch**: `feat/pitclaw-series-kickoff-post`
**Created**: 2026-03-25

## Summary

Publish the first PitClaw build-log post: a kickoff entry explaining why the project exists, how spec-driven development and agentic engineering made it practical to build, and where the project stands today.

## Plan

1. Draft the first PitClaw post in Matt's voice with a clear series arc.
2. Ground the story in the HeaterMeter -> Billows -> PitClaw progression without bashing prior tools.
3. Show the software velocity with one lightweight interactive chart sourced from real repo history.
4. Make the draft preview-friendly in both Hugo and local markdown editors by bundling the image with the post.
5. Verify the draft in a live Hugo server preview.

## Requirements

- Create and publish the first PitClaw build-log post
- Keep the tone honest about the project being in progress without sounding like a failure post
- Explain the role of spec-driven development and agent-assisted engineering in making the project feasible
- Include at least one real image from the PitClaw repo
- Include one interactive chart showing the early software sprint versus later hardware work
- Make the post render correctly in Hugo and show the bundled image in local markdown preview

## Design

Use a page bundle for the draft so the screenshot lives next to the post content and can render in editor previews. Structure the post around five beats:

- Backstory: HeaterMeter as the project that taught Matt what good smoker control feels like
- Commercial detour: trying Billows first before deciding to build
- Why now: spec-driven development and agentic engineering as the thing that made the project practical
- Software sprint vs hardware reality: one chart plus narrative contrast
- Current status: weekend side project cadence, WSM 18 as the immediate target, and clear next stretch

## Files to Modify

| File | Change |
|------|--------|
| `content/posts/2026-03_building-pitclaw-why-im-building-my-own-smoker-controller/index.md` | Publish the kickoff post as a page bundle entry |
| `content/posts/2026-03_building-pitclaw-why-im-building-my-own-smoker-controller/pitclaw-ui.png` | Bundle the PitClaw UI screenshot with the post for preview |
| `static/data/pitclaw-velocity.json` | Add chart data for commit velocity buckets |

## Test Plan

- [x] `hugo --minify` builds without errors
- [x] `hugo server -D --port 1314` serves the draft locally
- [x] Draft renders at `/posts/building-pitclaw-why-im-building-my-own-smoker-controller/`
- [x] Bundled screenshot displays in the rendered post
- [x] Interactive chart data loads from `static/data/pitclaw-velocity.json`
