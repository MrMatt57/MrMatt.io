# 062: Autoresearch Web Performance

**Branch**: `autoresearch/<run-tag>`
**Created**: 2026-03-15

## Summary

Adapt Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) pattern — an autonomous AI experiment loop — to optimize MrMatt.io's web performance. Instead of training a neural network, the agent iteratively modifies Hugo templates and config, evaluates with Lighthouse, keeps improvements, and discards regressions. The experiment produces a log of every attempt and a measurably faster site.

## Background

Autoresearch (released March 2026) lets an AI agent autonomously run ML experiments: modify `train.py` → run 5-min training → check `val_bpb` → keep/discard → repeat. The key insight is that the human writes strategy in `program.md` while the agent handles all code changes and evaluation. We apply this same loop to web performance optimization.

## Hard Constraint

**Zero visual or functional changes.** The site must look and behave identically before and after. Only performance characteristics (load time, resource efficiency, rendering speed) may change. This is enforced by a structural DOM hash — if the body's tag tree changes, the experiment is auto-discarded regardless of perf gains.

## Architecture

```
autoresearch/
├── program.md        # Agent instructions (human-editable strategy)
├── evaluate.py       # Fixed evaluation harness (DO NOT MODIFY)
├── results.tsv       # Experiment log (gitignored)
├── run.log           # Latest evaluation output (gitignored)
└── .gitignore
```

### Mapping to autoresearch

| autoresearch        | webperf equivalent                        |
|---------------------|-------------------------------------------|
| `train.py`          | Hugo layouts, partials, config, CSS       |
| `prepare.py`        | `evaluate.py` (fixed harness)             |
| `program.md`        | `program.md` (agent strategy)             |
| `val_bpb` (lower=better) | `worst_lcp_ms` (lower=better)         |
| 5-min training run  | Hugo build + Lighthouse w/ mobile throttle (~2 min) |
| `results.tsv`       | `results.tsv`                             |

### Evaluation pipeline

1. `hugo --minify --gc` → build the site
2. Measure build output (total size, HTML/CSS/JS/image sizes)
3. Compute structural DOM hash of key pages (visual regression gate)
4. Serve locally → run Lighthouse CLI → extract performance scores
5. Print all metrics to stdout (agent reads and decides)

### Keep/discard rules

1. **Structure hash changed** → AUTO-DISCARD (visual regression)
2. **Build failed** → CRASH, fix or skip
3. **`worst_lcp_ms` decreased** → KEEP (lower LCP = faster page)
4. **`worst_lcp_ms` same/worse** → DISCARD
5. If Lighthouse unavailable, use `total_size_kb` (lower=better) as fallback

Lighthouse runs with mobile throttling (4x CPU slowdown, simulated 4G, 412px viewport) for realistic scores with continuous millisecond resolution.

## Files the agent CAN modify

| File | Allowed changes |
|------|-----------------|
| `layouts/partials/extend_head.html` | Resource hints, preload order, critical CSS |
| `layouts/_default/baseof.html` | Script loading strategy (defer/async) |
| `layouts/_default/single.html` | Image loading attrs, fetchpriority |
| `layouts/index.html` | Image loading, resource hints |
| `layouts/photography/list.html` | IntersectionObserver tuning, batch sizes, loading attrs |
| `layouts/partials/footer.html` | Script optimization, loading strategy |
| `hugo.toml` | Minification, build optimization settings |
| `assets/css/extended/custom.css` | ONLY perf CSS: `content-visibility`, `contain`, `will-change` |

## Files the agent CANNOT modify

- `autoresearch/evaluate.py` — fixed evaluation harness
- `content/**` — all content
- `themes/**` — PaperMod submodule
- `static/**` — fonts, images
- Any CSS affecting: colors, fonts, margins, padding, layout, positioning, sizing, borders, backgrounds, text properties, opacity, visibility, z-index, display, flex/grid

## Requirements

- [ ] `autoresearch/program.md` — complete agent instructions
- [ ] `autoresearch/evaluate.py` — fixed evaluation harness with structural hash + Lighthouse
- [ ] `autoresearch/.gitignore` — ignore results, logs
- [ ] Spec checked into `.specs/`
- [ ] Can run a full evaluation cycle: `python autoresearch/evaluate.py`
- [ ] Quick mode available: `python autoresearch/evaluate.py --quick`
- [ ] Structure hash detects body DOM changes
- [ ] Lighthouse scores extracted and printed

## Test Plan

- [ ] `python autoresearch/evaluate.py --quick` completes in <5s
- [ ] `python autoresearch/evaluate.py` completes with Lighthouse scores
- [ ] Structure hash is stable across identical builds
- [ ] Structure hash changes when body HTML is modified
- [ ] Results printed in grep-friendly `key: value` format
- [ ] Agent can be pointed at `program.md` and loop autonomously
