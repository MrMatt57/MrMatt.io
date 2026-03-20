---
date: "2026-03-16"
draft: false
title: "Autoresearch for Web Performance: 20% Faster Overnight"
slug: "autoresearch-webperf"
description: "Adapting Karpathy's autoresearch pattern to web performance: an autonomous AI agent ran 200 Lighthouse experiments on my Hugo site, reducing worst-page LCP by 20%."
summary: "Adapting Karpathy's autoresearch pattern to web performance. An autonomous AI agent ran 200 Lighthouse experiments overnight, cutting my worst-page LCP from 2,638ms to 2,109ms."
tags:
  - "software-development"
  - "this-site"
---

<figure class="post-figure">
  <img
    src="/images/ai-experiment-rig.png"
    alt="Illustration of an autonomous AI experiment loop modifying, building, measuring, and evaluating website performance under human-defined constraints"
    loading="lazy"
  />
  <figcaption>
    Human strategy. Autonomous execution. Measured results.
  </figcaption>
</figure>

Andrej Karpathy released [autoresearch](https://github.com/karpathy/autoresearch) in March 2026 -- a pattern for letting an AI agent autonomously run ML experiments in a loop. The human writes strategy in `program.md`, the agent handles all code changes and evaluation. Modify → train → check loss → keep or discard → repeat.

I adapted this to web performance. Instead of training a neural network, the agent modifies Hugo templates and CSS, builds the site, runs Lighthouse with mobile throttling, and keeps or discards each change based on whether Largest Contentful Paint improved. The hard constraint: **zero visual changes** -- enforced by a structural DOM hash that auto-rejects any experiment that alters the page structure.

Over one session, the agent ran 200 experiments. Here's what happened.

### The setup

The evaluation harness (`evaluate.py`) does four things per experiment:

1. Build the site with `hugo --minify --gc`
2. Measure output file sizes by category
3. Compute a structural hash of the body DOM across three pages (homepage, about, photography)
4. Run Lighthouse CLI with mobile throttling (4x CPU slowdown, simulated 4G, 412px viewport)

The primary metric is `worst_lcp_ms` -- the highest Largest Contentful Paint across those three pages. Lower is better, same as `val_bpb` in the original autoresearch. Each experiment takes about two minutes.

The agent was allowed to modify eight files: `extend_head.html` (resource hints), `baseof.html` (base template), `single.html` (post template), `index.html` (homepage), `photography/list.html` (gallery), `footer.html` (scripts), `hugo.toml` (config), and `custom.css` (performance-only CSS properties). It could not touch content, the theme, fonts, images, or any visual CSS.

### LCP over 200 experiments

<div style="position:relative; width:100%; aspect-ratio:3/2; margin:2rem 0;">
<canvas id="lcp-timeline"></canvas>
</div>

The trajectory tells the story. The first few experiments delivered the biggest gains, then returns diminished. The downward staircase pattern is characteristic of optimization -- early wins are large and obvious, later wins are marginal and noisy. The spikes are failed experiments that got discarded.

Baseline was 2,638ms. The agent got it to a stable 2,109ms -- a **20% reduction** in worst-page LCP on simulated mobile 4G.

### Experiment outcomes

<div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin:2rem 0;">
<div style="position:relative; width:100%; aspect-ratio:1/1;">
<canvas id="outcomes-chart"></canvas>
</div>
<div style="position:relative; width:100%; aspect-ratio:1/1;">
<canvas id="category-chart"></canvas>
</div>
</div>

Of 200 experiments, 147 were kept (74%) and 47 discarded (23%). Four crashed the build entirely (usually by invalidating Hugo's image cache, triggering a rebuild timeout). The keep rate is deceptively high -- many "kept" changes were neutral on LCP but improved secondary metrics like FCP or build size, and about 70 were quick-mode CSS commits that skipped the full Lighthouse evaluation entirely. Only about 15 experiments delivered a measurable LCP improvement.

### What actually moved the needle

<div style="position:relative; width:100%; aspect-ratio:3/2; margin:2rem 0;">
<canvas id="top-wins"></canvas>
</div>

The biggest single improvement was **adding `content-visibility: auto`** to gallery thumbnails (-222ms). This told the browser to skip rendering off-screen images entirely, which freed up main-thread time during the initial paint.

The most *surprising* win was **removing a font preload** (-146ms). The font `<link rel="preload">` was competing with the LCP image for bandwidth on simulated 4G. Without it, the browser loaded the font just fine via the CSS `@font-face` -- slightly later, but freeing up the critical path for the image that actually determined LCP.

Image quality reduction (q80 → q60 on thumbnails) and matching the preload to the new quality level delivered another -76ms by shrinking the LCP image's byte size.

### The surprise: preloads can hurt

<div style="position:relative; width:100%; aspect-ratio:3/2; margin:2rem 0;">
<canvas id="preload-chart"></canvas>
</div>

Resource preloading was the most volatile optimization category. The agent discovered that **removing** the font preload saved 146ms, while **removing** the gallery image preload cost 527ms. Preloading three thumbnails instead of one caused contention and added 72ms. Adding `fetchpriority=high` to the font preload added 149ms.

On a throttled 4G connection, every preload competes for the same limited bandwidth. The optimal strategy turned out to be: preload exactly one critical image, preload zero fonts, and let the browser's native priority system handle everything else.

### Build size vs. LCP

<div style="position:relative; width:100%; aspect-ratio:3/2; margin:2rem 0;">
<canvas id="size-chart"></canvas>
</div>

Build size and LCP had almost no correlation. The site grew from ~700MB to ~949MB (from accumulated experimental CSS and config), then dropped to ~689MB after a clean rebuild -- with no effect on LCP. Most of the size is in processed images, which Hugo caches aggressively. The LCP improvements came entirely from resource loading strategy and rendering hints, not from reducing bytes.

### The noise problem

<div style="position:relative; width:100%; aspect-ratio:3/2; margin:2rem 0;">
<canvas id="noise-chart"></canvas>
</div>

Lighthouse scores on localhost are noisy. The same unchanged site can swing up to ±370ms between runs. The agent dealt with this by noting when results seemed noisy (e.g., "1961/2333 noisy") and sometimes running a second evaluation to confirm. Several experiments were kept or discarded on what was likely noise.

This is the same problem ML researchers face with `val_bpb` -- the signal-to-noise ratio drops as you approach the optimum. Late in the run, the difference between a "keep" and a "discard" was often within the measurement error. The chart above shows pairs of back-to-back evaluations on the same commit, demonstrating the typical variance.

### CSS containment: death by a thousand cuts

The agent added `contain: layout style paint` or `content-visibility: auto` to over 40 elements. Individually, none of these moved LCP by more than a few milliseconds. Collectively, they may have contributed to the overall improvement, but it's impossible to isolate their effect from the noise floor.

This is the long tail of web performance -- dozens of tiny optimizations that are individually unmeasurable but might compound. The autoresearch pattern is ideal for this kind of work because the cost of trying (and discarding) a micro-optimization is near zero.

### The structural hash saved the day

The DOM hash caught six experiments that would have changed the site's appearance:

- `keepEndTags=false` -- removed closing tags, breaking structure
- Photography template script removal -- altered the page layout
- `scroll-to-top` disabled -- removed a DOM element
- Code copy button disable -- changed the about page structure
- Photo count changes on homepage -- altered the grid structure
- JSON metadata block -- added a new script element

Without the hash, these changes would have been kept (some improved LCP) and the site would have silently broken. The hash acts as an automated visual regression test -- crude but effective.

### What I learned

**Resource contention is everything on mobile.** On a fast desktop connection, adding preloads is free. On simulated 4G with 1.6 Mbps bandwidth, every preload steals from everything else. The optimal strategy is ruthless prioritization: exactly one preload for the LCP element, nothing else.

**The autoresearch pattern generalizes.** Karpathy designed it for ML training loops, but the structure -- `program.md` for strategy, a fixed evaluator, keep/discard decisions, a results log -- works for any optimization problem with a measurable objective. Web performance, bundle size, build time, query latency -- anything with a number you want to move.

**200 experiments is overkill for web performance.** The agent had essentially exhausted the search space by experiment 50. The remaining 150 experiments were increasingly marginal CSS containment hints and configuration toggles. An ML model has millions of parameters to explore; a Hugo site has maybe 30 meaningful performance levers.

**Noise is the limiting factor.** By experiment 30, the remaining opportunities were smaller than the measurement noise. A proper setup would use multiple Lighthouse runs per experiment and compare medians. The agent tried this occasionally but not systematically.

**The best optimization was a deletion.** Removing the font preload, removing JSON output format, removing unused srcset breakpoints -- the three cleanest wins were all about doing less. The browser's defaults are heavily optimized. Fight them at your peril.

### The numbers

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Worst LCP (mobile 4G) | 2,638ms | 2,109ms | -20% |
| Lighthouse perf score | - | 99 | - |
| Homepage FCP | - | 904ms | - |
| Experiments run | - | 200 | - |
| Experiments kept | - | 147 | 74% |
| Experiments discarded | - | 47 | 23% |
| Build crashes | - | 4 | 2% |
| Structure hash violations | - | 6 | 3% |

The full experiment log, evaluation harness, and agent instructions are [on GitHub](https://github.com/MrMatt-io/mrmatt.io).

<script src="/js/chart.umd.min.js"></script>
<script>
(function() {
    /* ── Raw experiment data ── */
    var experiments = [
        {n:1,lcp:2638,size:715984.2,status:'baseline',desc:'initial baseline'},
        {n:2,lcp:2563,size:715985.9,status:'keep',desc:'fetchpriority=high on avatar'},
        {n:3,lcp:2341,size:716018.1,status:'keep',desc:'content-visibility auto on gallery'},
        {n:4,lcp:2334,size:716050.4,status:'keep',desc:'contain layout style paint on gallery'},
        {n:5,lcp:2335,size:716082.6,status:'keep',desc:'Hugo minify config'},
        {n:6,lcp:2340,size:716082.6,status:'discard',desc:'rootMargin 400->800px'},
        {n:7,lcp:2709,size:716082.6,status:'discard',desc:'batch 16->32'},
        {n:8,lcp:2332,size:716082.6,status:'discard',desc:'batch 16->8 noisy'},
        {n:9,lcp:2480,size:716082.8,status:'keep',desc:'preload first gallery thumbnail'},
        {n:10,lcp:2856,size:716082.8,status:'discard',desc:'eager load first 4 thumbs'},
        {n:11,lcp:2333,size:716072.3,status:'keep',desc:'LQIP 20x20->10x10'},
        {n:12,lcp:2406,size:716071.7,status:'discard',desc:'LQIP on homepage'},
        {n:13,lcp:2332,size:716071.7,status:'keep',desc:'defer lightbox to rIC'},
        {n:14,lcp:2260,size:721838.9,status:'keep',desc:'thumbnail q80->q70'},
        {n:15,lcp:2258,size:726939.3,status:'keep',desc:'thumbnail q70->q60'},
        {n:16,lcp:2258,size:726939.3,status:'keep',desc:'homepage thumbs q80->q60'},
        {n:17,lcp:2182,size:726939.3,status:'keep',desc:'preload quality matched to q60'},
        {n:18,lcp:2257,size:726937.7,status:'discard',desc:'removed decoding=async'},
        {n:19,lcp:2186,size:726971.6,status:'discard',desc:'will-change transform'},
        {n:20,lcp:2255,size:727003.9,status:'discard',desc:'content-visibility on homepage sections'},
        {n:21,lcp:2256,size:727036.2,status:'discard',desc:'contain-intrinsic-size'},
        {n:22,lcp:2184,size:727036.4,status:'discard',desc:'responsive preload with imagesrcset'},
        {n:23,lcp:2331,size:727039.6,status:'discard',desc:'fetchpriority=high on font preload'},
        {n:24,lcp:2257,size:727039.4,status:'discard',desc:'fetchpriority=low on font preload'},
        {n:25,lcp:2036,size:727020.3,status:'keep',desc:'remove font preload'},
        {n:26,lcp:2563,size:727020.2,status:'discard',desc:'removed gallery preload'},
        {n:27,lcp:2108,size:727020.5,status:'discard',desc:'preload 3 thumbs'},
        {n:28,lcp:2033,size:727020.3,status:'discard',desc:'preload 200w vs 300w'},
        {n:29,lcp:2033,size:727010.9,status:'discard',desc:'keepEndTags=false'},
        {n:30,lcp:2033,size:727020.3,status:'keep',desc:'keepDefaultAttrVals=false'},
        {n:31,lcp:2723,size:727014.7,status:'discard',desc:'keepDocumentTags=false'},
        {n:32,lcp:2034,size:727039.3,status:'discard',desc:'keepWhitespace=true'},
        {n:34,lcp:2034,size:728935.5,status:'discard',desc:'photography script removal'},
        {n:35,lcp:2111,size:728942.2,status:'discard',desc:'fetchpriority=high on gallery preload'},
        {n:38,lcp:2033,size:945864.4,status:'keep',desc:'dns-prefetch for external domains'},
        {n:39,lcp:1960,size:945863.7,status:'keep',desc:'disable enableGitInfo'},
        {n:40,lcp:2032,size:945863.7,status:'keep',desc:'remove LLMS outputs'},
        {n:41,lcp:1959,size:945864.1,status:'keep',desc:'inline critical CSS for photography'},
        {n:42,lcp:2035,size:945864.3,status:'keep',desc:'inline critical CSS for homepage'},
        {n:43,lcp:2034,size:945893.7,status:'keep',desc:'avatar q85->q75'},
        {n:44,lcp:2033,size:945925.9,status:'keep',desc:'contain on .main'},
        {n:45,lcp:1961,size:945926.0,status:'keep',desc:'fetchpriority=low on photo strip'},
        {n:47,lcp:2027,size:970623.3,status:'discard',desc:'contain:strict FCP regression'},
        {n:48,lcp:2033,size:970655.6,status:'keep',desc:'content-visibility on footer'},
        {n:49,lcp:2033,size:970676.0,status:'keep',desc:'disable PaperMod scrollbar CSS'},
        {n:50,lcp:1960,size:970643.3,status:'discard',desc:'scroll-to-top disabled'},
        {n:51,lcp:2037,size:970707.4,status:'discard',desc:'CSS @layer'},
        {n:52,lcp:1957,size:970707.3,status:'keep',desc:'remove JSON output'},
        {n:53,lcp:2033,size:970707.2,status:'discard',desc:'remove section RSS'},
        {n:54,lcp:2035,size:970707.3,status:'discard',desc:'decoding=sync on avatar'},
        {n:55,lcp:1957,size:970707.4,status:'keep',desc:'prerender hint'},
        {n:56,lcp:1958,size:970707.6,status:'keep',desc:'expanded photography critical CSS'},
        {n:57,lcp:2034,size:970707.7,status:'keep',desc:'speculation rules'},
        {n:58,lcp:2035,size:970717.1,status:'keep',desc:'auto DNS prefetch'},
        {n:59,lcp:1958,size:970748.6,status:'keep',desc:'content-visibility on post footer'},
        {n:60,lcp:2033,size:970780.2,status:'keep',desc:'content-visibility on lightbox'},
        {n:61,lcp:2034,size:970780.2,status:'keep',desc:'noJSConfigInAssets'},
        {n:62,lcp:2032,size:970785.0,status:'keep',desc:'defer scroll progress to rIC'},
        {n:63,lcp:2034,size:970793.0,status:'keep',desc:'color-scheme meta tag'},
        {n:64,lcp:2184,size:970793.0,status:'discard',desc:'goldmark block attributes'},
        {n:65,lcp:2335,size:970793.0,status:'discard',desc:'related threshold 80->90'},
        {n:66,lcp:2033,size:970824.6,status:'keep',desc:'contain on photo-thumb-wrap'},
        {n:67,lcp:2029,size:970856.2,status:'keep',desc:'minimize scroll-sentinel'},
        {n:68,lcp:1960,size:970887.9,status:'keep',desc:'containment on blur pseudo'},
        {n:70,lcp:2551,size:970888.0,status:'discard',desc:'prefetch from about page'},
        {n:71,lcp:2033,size:970919.6,status:'keep',desc:'aspect-ratio on lightbox'},
        {n:72,lcp:2034,size:970919.6,status:'keep',desc:'remove categories taxonomy'},
        {n:73,lcp:1959,size:970919.5,status:'keep',desc:'disable Hugo generator meta'},
        {n:75,lcp:2034,size:970951.2,status:'keep',desc:'contain on header'},
        {n:76,lcp:1959,size:970983.1,status:'keep',desc:'containment on post elements'},
        {n:77,lcp:2033,size:970983.1,status:'keep',desc:'explicit loading=eager on avatar'},
        {n:79,lcp:2033,size:971015.0,status:'keep',desc:'contain on photo-strip grid'},
        {n:80,lcp:2034,size:971013.5,status:'keep',desc:'simplified gallery sizes'},
        {n:81,lcp:2035,size:971004.9,status:'keep',desc:'remove 200w srcset'},
        {n:82,lcp:2034,size:971003.6,status:'keep',desc:'remove srcset from photo strip'},
        {n:83,lcp:2034,size:971003.6,status:'keep',desc:'gallery sizes 160px->175px'},
        {n:84,lcp:2107,size:971003.7,status:'discard',desc:'LQIP blur in critical CSS'},
        {n:86,lcp:2711,size:971003.6,status:'discard',desc:'sizes on avatar'},
        {n:87,lcp:2109,size:971013.6,status:'keep',desc:'referrer policy meta tag'},
        {n:88,lcp:2108,size:971045.5,status:'keep',desc:'containment on TOC'},
        {n:89,lcp:2264,size:971081.0,status:'discard',desc:'disableSVG'},
        {n:90,lcp:2787,size:971045.5,status:'discard',desc:'reorder preloads before CSS'},
        {n:91,lcp:2183,size:971054.5,status:'keep',desc:'format-detection meta tag'},
        {n:93,lcp:2034,size:971086.4,status:'keep',desc:'containment on home-photography'},
        {n:94,lcp:2035,size:971118.3,status:'keep',desc:'containment on home-journal'},
        {n:95,lcp:2033,size:971150.4,status:'keep',desc:'content-visibility on sections'},
        {n:96,lcp:2033,size:971182.5,status:'keep',desc:'containment on post-entry cards'},
        {n:97,lcp:2108,size:971184.4,status:'discard',desc:'fetchpriority=low on all gallery thumbs'},
        {n:98,lcp:3230,size:971214.6,status:'discard',desc:'contain inline-size on grid'},
        {n:99,lcp:2108,size:971246.7,status:'discard',desc:'rAF LQIP application'},
        {n:100,lcp:2108,size:971246.7,status:'discard',desc:'removing grid contain'},
        {n:101,lcp:2486,size:971262.7,status:'discard',desc:'font prefetch'},
        {n:102,lcp:2107,size:971278.8,status:'keep',desc:'containment on wrapper elements'},
        {n:103,lcp:2033,size:971311.0,status:'keep',desc:'containment on photo-thumb-link'},
        {n:106,lcp:2108,size:971334.9,status:'keep',desc:'full eval check'},
        {n:107,lcp:2033,size:971334.9,status:'discard',desc:'batch 16->12'},
        {n:109,lcp:2108,size:971367.0,status:'keep',desc:'overscroll-behavior eval check'},
        {n:110,lcp:2034,size:971369.0,status:'discard',desc:'JSON metadata block'},
        {n:114,lcp:2033,size:971399.3,status:'keep',desc:'full eval check stable'},
        {n:115,lcp:2109,size:971399.4,status:'discard',desc:'responsive preload'},
        {n:116,lcp:2035,size:971399.3,status:'keep',desc:'first thumbnail eager'},
        {n:117,lcp:2109,size:971399.3,status:'keep',desc:'first thumb eager no fetchpriority'},
        {n:121,lcp:2034,size:971400.9,status:'keep',desc:'full eval stable'},
        {n:123,lcp:2108,size:971400.9,status:'keep',desc:'merged photography LQIP'},
        {n:127,lcp:2109,size:971433.2,status:'keep',desc:'cumulative containment eval'},
        {n:133,lcp:2107,size:971474.4,status:'keep',desc:'containment additions eval'},
        {n:135,lcp:2108,size:971506.9,status:'keep',desc:'rAF batch reveal'},
        {n:136,lcp:2032,size:971514.4,status:'keep',desc:'moderate speculation rules'},
        {n:141,lcp:2034,size:971557.1,status:'keep',desc:'full eval stable perf=100'},
        {n:149,lcp:2109,size:971589.8,status:'keep',desc:'touch-action and compositor hints'},
        {n:154,lcp:2109,size:971634.7,status:'keep',desc:'speculation rules all pages'},
        {n:157,lcp:2036,size:971634.9,status:'keep',desc:'content-visibility in critical CSS'},
        {n:162,lcp:2864,size:971681.2,status:'discard',desc:'photography LCP regression'},
        {n:163,lcp:2108,size:971655.4,status:'keep',desc:'reverted to stable state'},
        {n:164,lcp:2259,size:971655.4,status:'discard',desc:'critical CSS regression'},
        {n:165,lcp:2031,size:705228.1,status:'keep',desc:'clean build'},
        {n:166,lcp:2938,size:705241.6,status:'discard',desc:'CSP upgrade-insecure-requests'},
        {n:167,lcp:2108,size:705228.1,status:'keep',desc:'color-scheme dark in critical CSS'},
        {n:168,lcp:2108,size:705228.2,status:'keep',desc:'content-visibility in critical CSS'},
        {n:173,lcp:2109,size:705260.9,status:'keep',desc:'full eval clean build stable'},
        {n:176,lcp:2107,size:705293.6,status:'keep',desc:'containment on body'},
        {n:181,lcp:2110,size:705326.5,status:'keep',desc:'full eval after re-adding props'},
        {n:188,lcp:2111,size:705359.4,status:'keep',desc:'full eval with recent additions'},
        {n:199,lcp:2110,size:705401.5,status:'keep',desc:'full eval near 200'},
        {n:200,lcp:2109,size:705419.5,status:'keep',desc:'mobile web app meta tags'}
    ];

    /* ── Computed datasets (hardcoded from full results.tsv, not just Lighthouse subset) ── */
    var keptCount = 147, discardCount = 47, crashCount = 4, revertCount = 1;

    /* Best LCP progression (kept experiments only) */
    var bestLcp = 9999;
    var bestProgression = [];
    experiments.forEach(function(e) {
        if (e.status === 'keep' || e.status === 'baseline') {
            if (e.lcp < bestLcp) {
                bestLcp = e.lcp;
                bestProgression.push({n: e.n, lcp: e.lcp, desc: e.desc});
            }
        }
    });

    /* Category analysis */
    var categories = {
        'Resource hints': {tried: 0, kept: 0},
        'Image optimization': {tried: 0, kept: 0},
        'CSS containment': {tried: 0, kept: 0},
        'Hugo config': {tried: 0, kept: 0},
        'Script loading': {tried: 0, kept: 0},
        'HTML minification': {tried: 0, kept: 0},
        'Meta tags': {tried: 0, kept: 0},
        'Other': {tried: 0, kept: 0}
    };

    function categorize(desc) {
        desc = desc.toLowerCase();
        if (desc.match(/preload|prefetch|prerender|preconnect|dns-prefetch|fetchpriority|speculation/)) return 'Resource hints';
        if (desc.match(/thumbnail|q[0-9]|srcset|lqip|image|avatar|photo|gallery sizes|img/)) return 'Image optimization';
        if (desc.match(/contain|content-visibility|isolation|will-change|backface|touch-action|overscroll|pointer-events/)) return 'CSS containment';
        if (desc.match(/hugo|minify|git|build|config|output|taxonomy|cjk|emoji|shortcode|paginate|inline shortcodes|summaryLength/)) return 'Hugo config';
        if (desc.match(/defer|async|script|idle|ric|requestidlecallback|scroll progress/)) return 'Script loading';
        if (desc.match(/keepend|keepdefault|keepdoc|keepwhite/)) return 'HTML minification';
        if (desc.match(/meta|referrer|format-detection|color-scheme|nosniff|csp|permissions|robots/)) return 'Meta tags';
        return 'Other';
    }

    experiments.forEach(function(e) {
        if (e.status === 'baseline') return;
        var cat = categorize(e.desc);
        categories[cat].tried++;
        if (e.status === 'keep') categories[cat].kept++;
    });

    /* Noise demonstration: back-to-back evaluations on same/similar state */
    var noisePairs = [
        {label: 'Exp 39\n(gitInfo)', a: 1960, b: 2033},
        {label: 'Exp 41\n(crit CSS)', a: 1959, b: 2033},
        {label: 'Exp 45\n(fetchpri)', a: 1961, b: 2333},
        {label: 'Exp 68\n(blur)', a: 1960, b: 2033},
        {label: 'Exp 8\n(batch)', a: 2332, b: 2707}
    ];

    /* Preload impact data (delta from best LCP at time of experiment) */
    var preloadData = [
        {label: 'Remove font\npreload', delta: -146},
        {label: 'Preload 1st\nthumbnail', delta: +146},
        {label: 'Remove gallery\npreload', delta: +527},
        {label: 'Preload 3\nthumbnails', delta: +72},
        {label: 'fetchpriority=high\non font', delta: +149},
        {label: 'fetchpriority=high\non gallery', delta: +75},
        {label: 'Font prefetch', delta: +453},
        {label: 'Reorder preloads\nbefore CSS', delta: +751}
    ];

    /* Top wins (biggest LCP improvements from previous best, verified against results.tsv) */
    var topWins = [
        {label: 'content-visibility\non gallery', delta: -222},
        {label: 'Remove font\npreload', delta: -146},
        {label: 'Preload quality\nmatched q60', delta: -76},
        {label: 'fetchpriority=high\non avatar', delta: -75},
        {label: 'Disable\ngitInfo', delta: -73},
        {label: 'Thumbnail\nq80→q70', delta: -72},
        {label: 'contain layout\nstyle paint', delta: -7},
        {label: 'Thumbnail\nq70→q60', delta: -2}
    ].sort(function(a,b) { return a.delta - b.delta; });

    /* ── Render ── */
    function renderCharts() {
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        var textColor = isDark ? '#e0e0e0' : '#090909';
        var gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)';
        var borderColor = isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.12)';
        var barColor = isDark ? '#888' : '#555';
        var accentColor = '#4c81b2';
        var discardColor = isDark ? 'rgba(192,57,43,0.5)' : 'rgba(192,57,43,0.4)';
        var keepColor = isDark ? 'rgba(76,129,178,0.7)' : 'rgba(76,129,178,0.6)';

        var defaultFont = { family: "'Roboto Slab', serif", size: 12, weight: '300' };
        var scaleDefs = {
            x: { grid: { color: gridColor }, ticks: { color: textColor, font: defaultFont } },
            y: { grid: { color: gridColor }, ticks: { color: textColor, font: defaultFont } }
        };
        var pluginDefs = {
            legend: { display: false },
            tooltip: {
                backgroundColor: isDark ? '#1d1e20' : '#fff',
                titleColor: textColor, bodyColor: textColor,
                borderColor: borderColor, borderWidth: 1, padding: 10,
                bodyFont: { family: "'Roboto Slab', serif", size: 13 },
                titleFont: { family: "'Roboto Slab', serif", size: 13, weight: '300' }
            }
        };

        /* ---- 1. LCP Timeline ---- */
        var lcpLabels = experiments.map(function(e) { return e.n; });
        var lcpData = experiments.map(function(e) { return e.lcp; });
        var lcpColors = experiments.map(function(e) {
            if (e.status === 'baseline') return accentColor;
            return e.status === 'discard' ? discardColor : keepColor;
        });
        var lcpBorderColors = experiments.map(function(e) {
            if (e.status === 'baseline') return accentColor;
            return e.status === 'discard' ? 'rgba(192,57,43,0.8)' : accentColor;
        });

        new Chart(document.getElementById('lcp-timeline'), {
            type: 'scatter',
            data: {
                datasets: [{
                    data: experiments.map(function(e) { return {x: e.n, y: e.lcp}; }),
                    backgroundColor: lcpColors,
                    borderColor: lcpBorderColors,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }, {
                    type: 'line',
                    data: (function() {
                        var best = 9999;
                        var pts = [];
                        experiments.forEach(function(e) {
                            if ((e.status === 'keep' || e.status === 'baseline') && e.lcp < best) {
                                best = e.lcp;
                            }
                            if (e.status === 'keep' || e.status === 'baseline') {
                                pts.push({x: e.n, y: best});
                            }
                        });
                        return pts;
                    })(),
                    borderColor: isDark ? '#e0e0e0' : '#333',
                    borderWidth: 1.5,
                    pointRadius: 0,
                    borderDash: [4, 3],
                    fill: false,
                    showLine: true
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: Object.assign({}, scaleDefs.x, {
                        type: 'linear',
                        title: { display: true, text: 'Experiment #', color: textColor, font: defaultFont }
                    }),
                    y: Object.assign({}, scaleDefs.y, {
                        title: { display: true, text: 'Worst LCP (ms)', color: textColor, font: defaultFont },
                        min: 1800
                    })
                },
                plugins: Object.assign({}, pluginDefs, {
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        callbacks: {
                            title: function(items) {
                                var idx = items[0].dataIndex;
                                if (items[0].datasetIndex === 0) {
                                    return 'Experiment ' + experiments[idx].n;
                                }
                                return '';
                            },
                            label: function(ctx) {
                                if (ctx.datasetIndex === 0) {
                                    var e = experiments[ctx.dataIndex];
                                    return e.lcp + 'ms — ' + e.desc + ' (' + e.status + ')';
                                }
                                return 'Best: ' + ctx.parsed.y + 'ms';
                            }
                        }
                    })
                })
            }
        });

        /* ---- 2. Outcomes doughnut ---- */
        new Chart(document.getElementById('outcomes-chart'), {
            type: 'doughnut',
            data: {
                labels: ['Kept', 'Discarded', 'Crashed', 'Reverted'],
                datasets: [{
                    data: [keptCount, discardCount, crashCount, revertCount],
                    backgroundColor: [keepColor, discardColor, isDark ? '#e74c3c' : '#c0392b', isDark ? '#f39c12' : '#d4a017'],
                    borderColor: isDark ? '#1d1e20' : '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: { color: textColor, font: defaultFont, padding: 15 }
                    },
                    title: {
                        display: true, text: 'Experiment Outcomes',
                        color: textColor, font: Object.assign({}, defaultFont, { size: 13 })
                    },
                    tooltip: pluginDefs.tooltip
                }
            }
        });

        /* ---- 3. Category chart ---- */
        var catLabels = Object.keys(categories).filter(function(k) { return categories[k].tried > 0; });
        var catTried = catLabels.map(function(k) { return categories[k].tried; });
        var catKept = catLabels.map(function(k) { return categories[k].kept; });

        new Chart(document.getElementById('category-chart'), {
            type: 'bar',
            data: {
                labels: catLabels,
                datasets: [
                    { label: 'Tried', data: catTried, backgroundColor: isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.1)', borderRadius: 2 },
                    { label: 'Kept', data: catKept, backgroundColor: keepColor, borderRadius: 2 }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                indexAxis: 'y',
                scales: {
                    x: Object.assign({ beginAtZero: true }, scaleDefs.x),
                    y: Object.assign({}, scaleDefs.y, { ticks: Object.assign({}, scaleDefs.y.ticks, { font: Object.assign({}, defaultFont, { size: 11 }) }) })
                },
                plugins: {
                    legend: {
                        display: true, position: 'bottom',
                        labels: { color: textColor, font: defaultFont, padding: 15 }
                    },
                    title: {
                        display: true, text: 'Experiments by Category',
                        color: textColor, font: Object.assign({}, defaultFont, { size: 13 })
                    },
                    tooltip: pluginDefs.tooltip
                }
            }
        });

        /* ---- 4. Top wins horizontal bar ---- */
        new Chart(document.getElementById('top-wins'), {
            type: 'bar',
            data: {
                labels: topWins.map(function(w) { return w.label; }),
                datasets: [{
                    data: topWins.map(function(w) { return Math.abs(w.delta); }),
                    backgroundColor: accentColor,
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                indexAxis: 'y',
                scales: {
                    x: Object.assign({ beginAtZero: true, title: { display: true, text: 'LCP improvement (ms)', color: textColor, font: defaultFont } }, scaleDefs.x),
                    y: scaleDefs.y
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: {
                        display: true, text: 'Biggest LCP Improvements',
                        color: textColor, font: Object.assign({}, defaultFont, { size: 13 })
                    },
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        callbacks: { label: function(ctx) { return '-' + ctx.parsed.x + 'ms'; } }
                    })
                })
            }
        });

        /* ---- 5. Preload impact ---- */
        new Chart(document.getElementById('preload-chart'), {
            type: 'bar',
            data: {
                labels: preloadData.map(function(p) { return p.label; }),
                datasets: [{
                    data: preloadData.map(function(p) { return p.delta; }),
                    backgroundColor: preloadData.map(function(p) {
                        return p.delta < 0 ? accentColor : discardColor;
                    }),
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: Object.assign({}, scaleDefs.x, {
                        ticks: Object.assign({}, scaleDefs.x.ticks, { font: Object.assign({}, defaultFont, { size: 10 }) })
                    }),
                    y: Object.assign({}, scaleDefs.y, {
                        title: { display: true, text: 'LCP change (ms)', color: textColor, font: defaultFont }
                    })
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: {
                        display: true, text: 'Impact of Resource Preloading Experiments',
                        color: textColor, font: Object.assign({}, defaultFont, { size: 13 })
                    },
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        callbacks: {
                            label: function(ctx) {
                                var v = ctx.parsed.y;
                                return (v > 0 ? '+' : '') + v + 'ms (worse = higher)';
                            }
                        }
                    })
                })
            }
        });

        /* ---- 6. Build size timeline ---- */
        var sizeExps = experiments.filter(function(e) { return e.size > 0; });
        new Chart(document.getElementById('size-chart'), {
            type: 'line',
            data: {
                labels: sizeExps.map(function(e) { return e.n; }),
                datasets: [{
                    data: sizeExps.map(function(e) { return Math.round(e.size / 1024); }),
                    borderColor: barColor,
                    backgroundColor: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)',
                    fill: true,
                    borderWidth: 1.5, pointRadius: 0, tension: 0.1
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: Object.assign({}, scaleDefs.x, {
                        title: { display: true, text: 'Experiment #', color: textColor, font: defaultFont }
                    }),
                    y: Object.assign({}, scaleDefs.y, {
                        title: { display: true, text: 'Total build size (MB)', color: textColor, font: defaultFont },
                        ticks: Object.assign({}, scaleDefs.y.ticks, {
                            callback: function(v) { return v + ' MB'; }
                        })
                    })
                },
                plugins: Object.assign({}, pluginDefs, {
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        callbacks: { label: function(ctx) { return ctx.parsed.y + ' MB'; } }
                    })
                })
            }
        });

        /* ---- 7. Noise demonstration ---- */
        new Chart(document.getElementById('noise-chart'), {
            type: 'bar',
            data: {
                labels: noisePairs.map(function(p) { return p.label; }),
                datasets: [
                    { label: 'Run 1', data: noisePairs.map(function(p) { return p.a; }), backgroundColor: accentColor, borderRadius: 2 },
                    { label: 'Run 2', data: noisePairs.map(function(p) { return p.b; }), backgroundColor: barColor, borderRadius: 2 }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: scaleDefs.x,
                    y: Object.assign({}, scaleDefs.y, {
                        min: 1800,
                        title: { display: true, text: 'LCP (ms)', color: textColor, font: defaultFont }
                    })
                },
                plugins: {
                    legend: {
                        display: true, position: 'bottom',
                        labels: { color: textColor, font: defaultFont, padding: 15 }
                    },
                    title: {
                        display: true, text: 'Same Experiment, Different LCP Readings',
                        color: textColor, font: Object.assign({}, defaultFont, { size: 13 })
                    },
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        callbacks: { label: function(ctx) { return ctx.dataset.label + ': ' + ctx.parsed.y + 'ms'; } }
                    })
                }
            }
        });
    }

    renderCharts();
    new MutationObserver(function() { location.reload(); })
        .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
</script>
