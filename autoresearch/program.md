# Autoresearch: Web Performance

You are an autonomous experiment agent optimizing the Hugo site at MrMatt.io
for web performance. You will run an infinite loop: hypothesize → modify →
evaluate → keep or discard → repeat.

Read this entire file before starting. Then follow the setup phase, then loop.

---

## Setup Phase

1. **Create a run tag** (e.g., `mar15a`) and branch: `autoresearch/<tag>`
2. **Read context files** to understand the site:
   - `hugo.toml` — site config
   - `layouts/partials/extend_head.html` — resource loading (critical)
   - `layouts/_default/baseof.html` — base template
   - `layouts/_default/single.html` — blog post template
   - `layouts/index.html` — homepage
   - `layouts/photography/list.html` — gallery (heaviest page)
   - `layouts/partials/footer.html` — scripts
   - `assets/css/extended/custom.css` — custom styles
3. **Run baseline evaluation**:
   ```
   python autoresearch/evaluate.py 2>&1 | tee autoresearch/run.log
   ```
4. **Record baseline** in `autoresearch/results.tsv`:
   ```
   commit	worst_lcp_ms	total_size_kb	structure_hash	status	description
   <hash>	<lcp>	<size>	<hash>	baseline	initial baseline
   ```

---

## The Experiment Loop (INFINITE)

Repeat these steps forever. Never stop. If stuck, re-read this file for ideas.

### 1. Check state
- `git log --oneline -1` — current commit
- Read the last few rows of `results.tsv` — what worked, what didn't

### 2. Form hypothesis
Think about what optimization to try next. Consider:
- What has worked so far (build on successes)
- What hasn't been tried yet
- The optimization ideas list below
- Combine multiple small wins

### 3. Modify files
Edit one or more ALLOWED files (see constraints below).
Make a single, focused change per experiment. Keep diffs small and reviewable.

### 4. Commit
```
git add -A && git commit -m "exp: <brief description of change>"
```

### 5. Evaluate
```
python autoresearch/evaluate.py 2>&1 | tee autoresearch/run.log
```
Extract from output:
- `worst_lcp_ms` (lower is better) — PRIMARY METRIC, like val_bpb in autoresearch
- `total_size_kb` (lower is better) — SECONDARY / FALLBACK
- `structure_hash` — MUST match baseline

Lighthouse runs with **mobile throttling** (4x CPU slowdown, simulated 4G
network, 412×823 viewport). This gives realistic scores with continuous
resolution — even small improvements in LCP milliseconds count.

If Lighthouse is unavailable, use `total_size_kb` as the primary metric
(lower is better).

### 6. Decide: keep or discard

```
IF structure_hash != baseline_hash:
    → DISCARD (visual regression detected)
    → git reset --hard HEAD~1

ELIF build failed:
    → Log as "crash"
    → git reset --hard HEAD~1

ELIF worst_lcp_ms < best_worst_lcp_ms:
    → KEEP (improvement — lower LCP is better!)
    → Update best_worst_lcp_ms

ELIF worst_lcp_ms == best_worst_lcp_ms AND total_size_kb < best_size_kb:
    → KEEP (tie-break on size)

ELSE:
    → DISCARD (no improvement)
    → git reset --hard HEAD~1
```

Note: Lighthouse scores can be noisy (±100ms between runs). If a result
is within 50ms of the best, consider running the evaluation a second time
to confirm before keeping or discarding.

### 7. Log result
Append to `autoresearch/results.tsv` (do NOT commit this file):
```
<commit>	<worst_lcp_ms>	<total_size_kb>	<structure_hash>	<keep|discard|crash>	<description>
```

### 8. Repeat
Go to step 1. Never stop.

---

## CRITICAL CONSTRAINTS

### What you CANNOT change (EVER)

These rules are non-negotiable. Violating them means the experiment is invalid.

**Visual properties — DO NOT TOUCH:**
- Colors, backgrounds, gradients, shadows, opacity
- Font families, font sizes, font weights, line heights, letter spacing
- Margins, padding, gaps, spacing
- Widths, heights, min/max dimensions
- Borders, border-radius, outlines
- Display, position, float, flex, grid layout rules
- Text alignment, decoration, transforms
- Z-index, visibility, overflow
- Transitions and animations (timing, easing, properties)

**Structural HTML — DO NOT TOUCH:**
- Adding or removing HTML elements
- Changing element types (e.g., div → section)
- Changing class names or IDs used for styling
- Reordering visible content
- Changing text content or alt text

**Off-limits files:**
- `autoresearch/evaluate.py` — the evaluation harness is sacred
- `content/**` — all markdown content
- `themes/**` — PaperMod submodule
- `static/fonts/**` — font files
- `static/images/**` — image files

### What you CAN change

**Resource loading (in `<head>` via `extend_head.html`):**
- `<link rel="preload">` — add/remove/reorder preload hints
- `<link rel="preconnect">` — add/remove preconnect hints
- `<link rel="dns-prefetch">` — add DNS prefetch hints
- `<link rel="modulepreload">` — preload scripts
- Critical CSS inlining (inline above-fold styles)
- Resource hint ordering (put critical resources first)

**Script loading (in templates and `footer.html`):**
- `defer` / `async` attributes on `<script>` tags
- Script placement (head vs. body, order)
- `type="module"` for modern loading

**Image loading attributes (in templates):**
- `loading="lazy"` / `loading="eager"` — control lazy loading
- `fetchpriority="high"` / `fetchpriority="low"` — priority hints
- `decoding="async"` / `decoding="sync"` — decode strategy
- `sizes` attribute tuning
- `srcset` optimization (image size breakpoints)
- IntersectionObserver `rootMargin` and `threshold` tuning
- Batch/chunk sizes for progressive loading

**CSS performance properties (in `custom.css`):**
- `content-visibility: auto` — skip rendering off-screen content
- `contain: layout style paint` — containment hints
- `will-change` — compositor hints for animated elements
- `aspect-ratio` — prevent layout shift (CLS reduction)
- `@media print` — optimize print stylesheets

**Hugo config (in `hugo.toml`):**
- `[minify]` — minification settings for HTML/CSS/JS/XML
- `[build]` — build configuration
- `[caches]` — Hugo cache settings
- `[imaging]` — image processing defaults (quality, resampling)
- `[outputs]` — output format optimization
- `enableInlineShortcodes` and related build toggles

---

## Optimization Ideas

Start with high-impact, low-risk changes. Move to creative experiments later.

### Tier 1 — Quick wins
- [ ] Add `fetchpriority="high"` to LCP images (avatar, hero photos)
- [ ] Add `decoding="async"` to non-critical images
- [ ] Optimize `<head>` resource order (preloads before stylesheets)
- [ ] Add `content-visibility: auto` to below-fold sections
- [ ] Tune IntersectionObserver `rootMargin` for earlier image loading
- [ ] Add `contain: layout style paint` to independent sections

### Tier 2 — Moderate effort
- [ ] Inline critical above-fold CSS, defer the rest
- [ ] Add Hugo minification config (`[minify]` section)
- [ ] Optimize image processing quality settings in Hugo
- [ ] Add `aspect-ratio` to image containers to reduce CLS
- [ ] Reorder `<head>` elements: charset → viewport → preconnect → preload → styles
- [ ] Script consolidation: merge small inline scripts

### Tier 3 — Creative experiments
- [ ] Experiment with different image srcset breakpoints
- [ ] Tune progressive loading batch sizes (currently 16)
- [ ] Add `<link rel="prerender">` for likely next pages
- [ ] Experiment with CSS `@layer` for parsing performance
- [ ] Use Hugo's `resources.PostProcess` for late-bound assets
- [ ] Experiment with `importance` attribute on fetch requests

---

## Tips

- **One change at a time.** Small, isolated experiments are easier to evaluate.
- **Build on what works.** If an optimization helped, try variations of it.
- **Track patterns.** Note which categories of changes help most.
- **Don't repeat failures.** Check results.tsv before trying something similar.
- **Quick mode exists.** Use `python autoresearch/evaluate.py --quick` for
  fast iteration on build-size optimizations, then validate with full
  Lighthouse runs.
- **If Lighthouse scores are noisy**, run the same evaluation 2-3 times and
  use the median. Local Lighthouse can vary ±3 points between runs.
- **Read the Lighthouse JSON** in `run.log` for specific audit details
  that suggest what to optimize next.
