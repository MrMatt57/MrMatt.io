---
date: "2026-03-10"
draft: false
title: "Every Camera I've Ever Owned"
slug: "camera-gear-timeline"
description: "35 cameras, 22 phones, and a Canon Rebel — 22 years of photography gear traced through 94,000 photos of EXIF data."
tags:
  - "photography"
  - "software-development"
summary: "35 cameras, 22 phones, and a Canon Rebel — 22 years of photography gear traced through 94,000 photos of EXIF data."
---

These are all the cameras I've ever owned -- starting with a Canon Rebel 35mm SLR in high school and ending with the latest Pixel. The film rolls live in shoeboxes, not in metadata, but every digital photo carries its camera's name quietly in the EXIF header. I scanned the EXIF headers of 94,000 Google Photos and found 75 different cameras spanning 22 years. Some were mine. Some were friends' phones showing up in shared albums. After filtering down to just the cameras I actually owned, the timeline tells a clear story.

One caveat: this is JPEG only. The pipeline skips raw files -- CR2s from the Canons, NEFs from the Nikons -- because Google Takeout bundles the JPEGs but not always the raws. So the real photo counts for the DSLR era are higher than what's shown here. The raws live on hard drives, not in the cloud.

After [scanning 723GB of Google Takeout data](/posts/google-takeout-gallery-curation/) to build this site's photography gallery, I had the pipeline and the raw material. So I pointed a Python script at all 15 zip files, read the first 64KB of every JPEG to extract the EXIF header, normalized the camera names, and loaded it all into a SQLite database.

### The timeline

<div style="position:relative;width:100%;aspect-ratio:2/1;margin:2rem 0;">
<canvas id="timeline-chart"></canvas>
</div>

The pattern is clear: dedicated cameras dominated until around 2013, then phones took over completely. The transition wasn't gradual -- it was a cliff. Once the Samsung Galaxy Note II arrived, the Canon PowerShots and Nikon DSLRs collected dust.

### The eras

The earliest camera in the data is the Sony Cyber-shot DSC-V1, which became the real workhorse of the compact era: 3,845 photos over seven years. Canon PowerShots, Pentax compacts, more Kodak EasyShares -- a new camera every year or two, each one a modest upgrade. This was the age of carrying a dedicated device in a belt pouch and hoping the batteries held.

The DSLR era was really just one camera: the Nikon D3100. It was the real commitment -- 5,729 photos over six years. It lived in the camera bag for every family trip and holiday. But carrying a body, two lenses, and a charger loses its appeal when the thing in your pocket takes a photo that's good enough.

The phone revolution hit around 2012. The Samsung Galaxy Note II changed everything -- 11,039 photos on a single device. Then the Note 4 pushed even further: 12,704 photos, making it the single most-used camera I've ever owned. The compact cameras and DSLRs were done.

The Pixel years run from 2016 to present. Google Pixel XL, 2 XL, 3 XL, 4 XL, 5, 6 Pro, 8 Pro, 9 Pro XL, 10 Pro XL. Nine Pixels in ten years. The best camera is the one you have with you, and the phone won that argument decisively.

### Phone vs. dedicated camera

<div style="position:relative;width:100%;aspect-ratio:5/4;margin:2rem 0;">
<canvas id="category-chart"></canvas>
</div>

The crossover happened around 2013. By 2018, dedicated cameras were effectively zero. Computational photography didn't just match optical quality -- it made the camera you always have with you the best camera.

### The cameras

<div id="canon-rebel-card" style="padding:1.25rem 0;border-bottom:1px solid rgba(128,128,128,0.2);">
<div style="display:flex;gap:1.25rem;align-items:flex-start;">
<img src="/images/camera-timeline/canon-eos-rebel.webp" alt="Canon EOS Rebel" loading="lazy" class="camera-card-img" onerror="this.style.display='none'">
<div style="min-width:0;flex:1;">
<strong style="font-size:1.05rem;">Canon EOS Rebel</strong><br>
<span style="color:var(--secondary);font-size:0.85rem;">~1998 &middot; 35mm film SLR &middot; No EXIF data</span><br>
<span style="font-size:0.85rem;color:var(--secondary);">The one that started it all. A run-of-the-mill Canon Rebel that I used in high school photography class. The rolls of Kodak Gold and Tri-X are in a shoebox somewhere, but this is where it began.</span>
</div></div>
</div>

<div id="camera-cards"></div>

### How I built this

Nearly a terabyte of Google Takeout data. Twenty-two years of photos. The pipeline is four Python scripts: [`scan_camera_exif.py`](https://github.com/shortnd/MrMatt.io/blob/master/tools/scan_camera_exif.py) rips through every JPEG across 15 zip files, reads the first 64KB to extract the EXIF header, and loads it into SQLite -- three parallel workers, 30 minutes. [`normalize_cameras.py`](https://github.com/shortnd/MrMatt.io/blob/master/tools/normalize_cameras.py) maps raw EXIF strings to clean names (Samsung's EXIF says "SM-G920V" not "Galaxy S6"). [`export_camera_timeline.py`](https://github.com/shortnd/MrMatt.io/blob/master/tools/export_camera_timeline.py) and [`export_photo_stats.py`](https://github.com/shortnd/MrMatt.io/blob/master/tools/export_photo_stats.py) query the database and output the JSON that powers these charts. The result: 94,000 photos with every camera, aperture, ISO, focal length, and GPS coordinate preserved in a queryable database. Charts are self-hosted [Chart.js](https://www.chartjs.org/) -- no CDN, no npm, just a single JS file.

For the deep dive into what all that EXIF data reveals about shooting patterns, see [94,000 Photos by the Numbers](/posts/photography-by-the-numbers/).

<script src="/js/chart.umd.min.js"></script>
<script>
(function() {
    fetch('/data/camera-timeline.json')
        .then(function(r) { return r.json(); })
        .then(function(data) { renderCharts(data); });

    /* Cameras I actually owned (exclude friends' shared photos) */
    var NOT_OWNED = [
        'Apple iPhone 5s', 'Apple iPhone 5c', 'Apple iPhone 6',
        'Apple iPhone 6s', 'Apple iPhone 6s Plus', 'Apple iPhone 7',
        'Apple iPhone 8', 'Apple iPhone X', 'Apple iPhone XR',
        'Apple iPhone 11', 'Apple iPhone 12 Mini',
        'Apple iPhone 16', 'Apple iPhone 16 Pro',
        'Canon EOS Rebel XTi', 'Canon EOS 5D Mark II',
        'Canon EOS 5D Mark III', 'Canon EOS 5D Mark IV',
        'Sony A6000', 'DJI Phantom 4',
        'Samsung Galaxy S24', 'Samsung Galaxy Tab S2',
        'Pentax Optio S5z', 'Pentax Optio 30',
        'Canon PowerShot SD400', 'Canon PowerShot SD450', 'Canon PowerShot SD1000',
        'Nikon D3000',
        'Google Pixel 6a', 'Google Pixel 8a',
        'Sony Cyber-shot DSC-P100',
        'Kodak EasyShare DX4900', 'Kodak EasyShare C533', 'Kodak EasyShare M893'
    ];

    function isOwned(name) {
        return NOT_OWNED.indexOf(name) === -1;
    }

    function renderCharts(data) {
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        var textColor = isDark ? '#e0e0e0' : '#090909';
        var gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)';
        var borderColor = isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.12)';
        var barColor = isDark ? '#888' : '#555';
        var accentColor = '#4c81b2';

        var PALETTE = isDark
            ? ['#e8e8e8','#d0d0d0','#b8b8b8','#a0a0a0','#888','#707070','#585858',
               '#4c81b2','#5a8fbd','#6b9dc7','#7cabd1','#8db9db',
               '#f0f0f0','#c8c8c8','#a8a8a8','#888','#686868','#484848','#383838']
            : ['#1a1a1a','#2d2d2d','#404040','#535353','#666','#797979','#8c8c8c',
               '#4c81b2','#5a8fbd','#6b9dc7','#7cabd1','#8db9db',
               '#9f9f9f','#b2b2b2','#c5c5c5','#d8d8d8','#ebebeb','#f0f0f0','#333'];

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

        /* ---- Chart 1: Timeline stacked area (owned cameras with 50+ photos) ---- */
        var years = Object.keys(data.timeline).sort();
        var cameraNames = data.cameras
            .filter(function(c) { return c.photo_count >= 50 && isOwned(c.display_name); })
            .sort(function(a, b) { return (a.first_seen || '').localeCompare(b.first_seen || ''); })
            .map(function(c) { return c.display_name; });
        var timelineDS = cameraNames.map(function(name, i) {
            return {
                label: name,
                data: years.map(function(y) { return (data.timeline[y] && data.timeline[y][name]) || 0; }),
                fill: true,
                backgroundColor: PALETTE[i % PALETTE.length] + '88',
                borderColor: PALETTE[i % PALETTE.length],
                borderWidth: 1, pointRadius: 0, tension: 0.3
            };
        });
        new Chart(document.getElementById('timeline-chart'), {
            type: 'line',
            data: { labels: years, datasets: timelineDS },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: { x: scaleDefs.x, y: Object.assign({ stacked: true, beginAtZero: true }, scaleDefs.y) },
                plugins: Object.assign({}, pluginDefs, {
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        mode: 'index', intersect: false,
                        filter: function(item) { return item.raw > 0; }
                    })
                })
            }
        });

        /* ---- Chart 2: Category breakdown (stacked bar) ---- */
        var catYears = Object.keys(data.category_by_year).sort();
        var categories = ['phone','compact','dslr','drone','action','tablet'];
        var catColors = isDark
            ? { phone:'#e0e0e0', compact:'#888', dslr:'#bbb', drone:'#4c81b2', action:'#5a8fbd', tablet:'#555' }
            : { phone:'#333', compact:'#999', dslr:'#666', drone:'#4c81b2', action:'#5a8fbd', tablet:'#bbb' };
        var catLabels = { phone:'Phone', compact:'Compact', dslr:'DSLR', drone:'Drone', action:'Action Cam', tablet:'Tablet' };
        var catDS = categories.map(function(cat) {
            return {
                label: catLabels[cat] || cat,
                data: catYears.map(function(y) { return (data.category_by_year[y] && data.category_by_year[y][cat]) || 0; }),
                backgroundColor: catColors[cat] || '#999', borderRadius: 2
            };
        }).filter(function(ds) { return ds.data.some(function(v) { return v > 0; }); });
        new Chart(document.getElementById('category-chart'), {
            type: 'bar',
            data: { labels: catYears, datasets: catDS },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: { x: Object.assign({ stacked: true }, scaleDefs.x), y: Object.assign({ stacked: true, beginAtZero: true }, scaleDefs.y) },
                plugins: Object.assign({}, pluginDefs, {
                    legend: { display: true, labels: { color: textColor, font: defaultFont, boxWidth: 12, padding: 16 } }
                })
            }
        });

        /* ---- Camera cards with sparkline histograms ---- */
        var container = document.getElementById('camera-cards');
        if (!container) return;

        /* Build yearly counts per camera for sparklines */
        var allYears = Object.keys(data.timeline).sort();
        var firstYear = parseInt(allYears[0]);
        var lastYear = parseInt(allYears[allYears.length - 1]);
        var yearSpan = lastYear - firstYear + 1;

        /* Find global max yearly count (across owned cameras) for consistent scaling */
        var globalMax = 0;
        data.cameras.forEach(function(cam) {
            if (!isOwned(cam.display_name) || cam.photo_count < 10) return;
            allYears.forEach(function(y) {
                var cnt = (data.timeline[y] && data.timeline[y][cam.display_name]) || 0;
                if (cnt > globalMax) globalMax = cnt;
            });
        });

        var html = '';
        var cardIndex = 0;
        var cams = data.cameras
            .filter(function(c) { return c.photo_count >= 10 && isOwned(c.display_name); })
            .sort(function(a, b) { return (a.first_seen || '').localeCompare(b.first_seen || ''); });

        cams.forEach(function(cam) {
            var fy = cam.first_seen ? cam.first_seen.substring(0, 4) : '?';
            var ly = cam.last_seen ? cam.last_seen.substring(0, 4) : '?';
            var range = fy === ly ? fy : fy + ' \u2013 ' + ly;
            var pct = (cam.photo_count / data.summary.total_photos * 100).toFixed(1);
            var cat = cam.category ? cam.category.charAt(0).toUpperCase() + cam.category.slice(1) : '';
            var stats = [];
            if (cam.median_aperture) stats.push('f/' + cam.median_aperture.toFixed(1));
            if (cam.median_iso) stats.push('ISO ' + cam.median_iso);
            if (cam.median_focal_length_35mm) stats.push(cam.median_focal_length_35mm + 'mm');
            var slug = cam.display_name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
            var canvasId = 'spark-' + cardIndex;

            html += '<div style="padding:1.25rem 0;border-bottom:1px solid ' + borderColor + ';">';
            html += '<div style="display:flex;gap:1.25rem;align-items:flex-start;">';
            html += '<img src="/images/camera-timeline/' + slug + '.webp" alt="' + cam.display_name + '" loading="lazy" ';
            html += 'class="camera-card-img" ';
            html += 'onerror="this.style.display=\'none\'">';
            html += '<div style="min-width:0;flex:1;">';
            html += '<strong style="font-size:1.05rem;">' + cam.display_name + '</strong><br>';
            html += '<span style="color:var(--secondary);font-size:0.85rem;">' + range + ' &middot; ' + cam.photo_count.toLocaleString() + ' photos (' + pct + '%) &middot; ' + cat + '</span>';
            if (stats.length) html += '<br><span style="font-size:0.85rem;color:var(--secondary);">' + stats.join(' &middot; ') + '</span>';
            html += '</div></div>';
            /* Sparkline histogram spanning full timeline */
            html += '<div class="camera-sparkline">';
            html += '<canvas id="' + canvasId + '"></canvas>';
            html += '</div>';
            html += '</div>';

            cardIndex++;
        });
        container.innerHTML = html;

        /* Shared tooltip element for sparkline hover */
        var tip = document.createElement('div');
        tip.style.cssText = 'position:fixed;padding:3px 7px;font-size:0.75rem;font-family:"Roboto Slab",serif;'
            + 'border-radius:3px;pointer-events:none;z-index:9999;opacity:0;transition:opacity 0.1s;white-space:nowrap;'
            + 'background:' + (isDark ? '#1d1e20' : '#fff') + ';color:' + textColor + ';'
            + 'border:1px solid ' + borderColor + ';';
        document.body.appendChild(tip);

        /* Draw sparkline histograms */
        cardIndex = 0;
        cams.forEach(function(cam) {
            var canvas = document.getElementById('spark-' + cardIndex);
            if (!canvas) { cardIndex++; return; }
            var ctx = canvas.getContext('2d');
            var rect = canvas.getBoundingClientRect();
            var dpr = window.devicePixelRatio || 1;
            canvas.width = rect.width * dpr;
            canvas.height = rect.height * dpr;
            ctx.scale(dpr, dpr);
            var w = rect.width;
            var h = rect.height;

            var barW = Math.max(1, (w - yearSpan + 1) / yearSpan);
            var gap = 1;
            var totalBarW = barW + gap;

            /* Get this camera's yearly counts */
            var counts = allYears.map(function(y) {
                return (data.timeline[y] && data.timeline[y][cam.display_name]) || 0;
            });
            var localMax = Math.max.apply(null, counts);

            /* Draw year bars */
            for (var i = 0; i < yearSpan; i++) {
                var count = counts[i] || 0;
                var x = i * totalBarW;

                if (count === 0) {
                    /* Empty year: faint tick mark */
                    ctx.fillStyle = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)';
                    ctx.fillRect(x, h - 2, barW, 2);
                } else {
                    /* Active year: height proportional to count, scaled to local max */
                    var barH = Math.max(3, (count / localMax) * (h - 2));
                    var intensity = count / localMax;
                    if (intensity > 0.8) {
                        ctx.fillStyle = accentColor;
                    } else {
                        ctx.fillStyle = isDark
                            ? 'rgba(255,255,255,' + (0.2 + intensity * 0.6) + ')'
                            : 'rgba(0,0,0,' + (0.15 + intensity * 0.55) + ')';
                    }
                    ctx.fillRect(x, h - barH, barW, barH);
                }
            }

            /* Hover: show year + count tooltip */
            (function(cvs, cts, tw) {
                cvs.addEventListener('mousemove', function(e) {
                    var cr = cvs.getBoundingClientRect();
                    var mx = e.clientX - cr.left;
                    var idx = Math.floor(mx / tw);
                    if (idx < 0 || idx >= yearSpan) { tip.style.opacity = '0'; return; }
                    var yr = allYears[idx];
                    var cnt = cts[idx] || 0;
                    tip.textContent = yr + (cnt > 0 ? ' \u2014 ' + cnt.toLocaleString() + ' photos' : '');
                    tip.style.left = (e.clientX + 10) + 'px';
                    tip.style.top = (e.clientY - 28) + 'px';
                    tip.style.opacity = '1';
                });
                cvs.addEventListener('mouseleave', function() {
                    tip.style.opacity = '0';
                });
            })(canvas, counts, totalBarW);

            cardIndex++;
        });
    }

    /* Re-render on theme toggle */
    new MutationObserver(function() { location.reload(); })
        .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
</script>
