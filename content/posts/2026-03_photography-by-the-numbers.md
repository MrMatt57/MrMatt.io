---
date: "2026-03-10"
draft: false
title: "94,000 Photos by the Numbers"
slug: "photography-by-the-numbers"
description: "What 22 years of EXIF data reveals about when I shoot, what I shoot with, and how photography changed from film-era habits to phone-first instinct."
tags:
  - "photography"
  - "software-development"
summary: "What 22 years of EXIF data reveals about when I shoot, what I shoot with, and how photography changed from film-era habits to phone-first instinct."
---

In [Every Camera I've Ever Owned](/posts/camera-gear-timeline/), I traced 22 years of gear. This post is about the photos themselves -- 94,000 of them -- and what their metadata reveals.

I scanned the EXIF headers of every JPEG across 15 Google Takeout zip files. Here's what the data says.

### Volume over time

<div style="position:relative; width:100%; aspect-ratio:5/2; margin:2rem 0;">
<canvas id="yearly-chart"></canvas>
</div>

The yearly photo count forms a bell curve peaking at 2015 with 13,816 photos. The ramp tracks predictable life events -- kids born, vacations, new cameras arriving every year or two. At the peak, I had five cameras active in a single year: phones, compacts, and a DSLR all competing for pocket space. The decline after 2015 is equally clear: one phone replaced everything, and the volume settled to a sustainable rhythm. The 2020 dip is exactly what you'd expect from a year spent mostly indoors.

### When I shoot

<div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin:2rem 0;">
<div style="position:relative; width:100%; aspect-ratio:4/3;">
<canvas id="hourly-chart"></canvas>
</div>
<div style="position:relative; width:100%; aspect-ratio:4/3;">
<canvas id="dow-chart"></canvas>
</div>
</div>

Saturday at 10am is my golden hour. Weekends get twice the shooting volume of midweek. The hourly distribution peaks sharply at 10am with roughly 8,000 photos, then holds a plateau through the afternoon before dropping off after sunset. Weekdays are flat and low -- photography is clearly a leisure activity, not a workday habit.

### The heatmap

<div style="position:relative; width:100%; aspect-ratio:5/2; margin:2rem 0;">
<canvas id="heatmap-chart"></canvas>
</div>

The pattern is clear: weekend mornings and afternoons are when I reach for the camera. The weekday rows are dim and uniform. Saturday and Sunday light up from mid-morning through late afternoon, with the strongest signal clustered around 9am to 3pm.

### People in photos

<div style="position:relative; width:100%; aspect-ratio:5/2; margin:2rem 0;">
<canvas id="people-chart"></canvas>
</div>

The percentage of photos containing people dropped from 70% in 2016 to under 2% after 2020. This could reflect Google's face detection metadata changing over time, or a genuine shift toward landscape and nature photography. Probably both. The early years are noisy because the sample sizes are small -- a few hundred photos per year makes each face detection hit or miss count for a lot.

### Where in the world

<div style="position:relative; width:100%; aspect-ratio:5/2; margin:2rem 0;">
<canvas id="gps-chart"></canvas>
</div>

GPS data went from 0% in the pre-smartphone era to 91% in 2017, then drifted back down. The rise tracks smartphone adoption perfectly -- phones embed GPS coordinates by default, dedicated cameras don't. The decline after 2017 likely reflects tightening privacy settings and location permissions being turned off, plus occasional use of cameras without GPS radios.

### The lens settings

<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1.5rem; margin:2rem 0;">
<div style="position:relative; width:100%; aspect-ratio:4/3;">
<canvas id="aperture-chart"></canvas>
</div>
<div style="position:relative; width:100%; aspect-ratio:4/3;">
<canvas id="focal-chart"></canvas>
</div>
<div style="position:relative; width:100%; aspect-ratio:4/3;">
<canvas id="iso-time-chart"></canvas>
</div>
</div>

f/2.0 at 27mm. That's the phone sweet spot -- a moderately wide angle with a fast-ish aperture. The DSLR's f/1.8 at 50mm barely registers anymore. Average ISO climbs steadily year over year as phones push deeper into low-light computational photography, trading sensor noise for Night Sight algorithms.

### Resolution and exposure

<div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin:2rem 0;">
<div style="position:relative; width:100%; aspect-ratio:4/3;">
<canvas id="resolution-chart"></canvas>
</div>
<div style="position:relative; width:100%; aspect-ratio:4/3;">
<canvas id="exposure-chart"></canvas>
</div>
</div>

Resolution plateaued after the megapixel race ended. The jump from 4MP in 2003 to 12MP in 2012 was dramatic; the crawl from 12MP to 22MP over the next decade was barely noticeable in practice. Most photos are shot between 1/10s and 1/250s -- everyday handheld speeds, the kind of shutter range where image stabilization matters more than raw sensor capability.

### The full heartbeat

<div style="position:relative; width:100%; aspect-ratio:5/2; margin:2rem 0;">
<canvas id="monthly-chart"></canvas>
</div>

Zoom out from yearly averages and the real rhythm appears. Every spike is a trip, a holiday, a new baby, a Saturday morning at the park. The three busiest months -- May 2015, April 2018, April 2015 -- each cracked 1,700 photos. That's 55 to 65 photos a day, every day, for a month straight. The quiet valleys are just as telling: the gaps where life got busy, or the camera stayed in the drawer, or a global pandemic kept everyone indoors.

This is 94,000 shutter presses compressed into a single line. Twenty-two years of reaching for a camera -- first deliberately, then instinctively.

See the full gear timeline in [Every Camera I've Ever Owned](/posts/camera-gear-timeline/).

<script src="/js/chart.umd.min.js"></script>
<script>
(function() {
    fetch('/data/photo-stats.json')
        .then(function(r) { return r.json(); })
        .then(function(data) { renderCharts(data); });

    function renderCharts(data) {
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        var textColor = isDark ? '#e0e0e0' : '#090909';
        var gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)';
        var borderColor = isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.12)';
        var barColor = isDark ? '#888' : '#555';
        var accentColor = '#4c81b2';

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

        /* ---- Yearly totals bar chart ---- */
        var years = Object.keys(data.yearly_totals).sort();
        new Chart(document.getElementById('yearly-chart'), {
            type: 'bar',
            data: {
                labels: years,
                datasets: [{
                    data: years.map(function(y) { return data.yearly_totals[y]; }),
                    backgroundColor: barColor,
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: scaleDefs.x,
                    y: Object.assign({ beginAtZero: true }, scaleDefs.y)
                },
                plugins: pluginDefs
            }
        });

        /* ---- Hour of day bar chart ---- */
        var hours = [];
        var hourlyCounts = [];
        for (var h = 0; h < 24; h++) {
            hours.push(h + ':00');
            hourlyCounts.push(data.hourly[h] || data.hourly[String(h)] || 0);
        }
        new Chart(document.getElementById('hourly-chart'), {
            type: 'bar',
            data: {
                labels: hours,
                datasets: [{
                    data: hourlyCounts,
                    backgroundColor: barColor,
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: Object.assign({}, scaleDefs.x, { ticks: Object.assign({}, scaleDefs.x.ticks, { maxRotation: 45 }) }),
                    y: Object.assign({ beginAtZero: true }, scaleDefs.y)
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: { display: true, text: 'Hour of Day', color: textColor, font: Object.assign({}, defaultFont, { size: 13 }) }
                })
            }
        });

        /* ---- Day of week bar chart ---- */
        var dayOrder = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
        var dayLabels = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
        var dayCounts = dayOrder.map(function(d) { return data.day_of_week[d] || 0; });
        new Chart(document.getElementById('dow-chart'), {
            type: 'bar',
            data: {
                labels: dayLabels,
                datasets: [{
                    data: dayCounts,
                    backgroundColor: barColor,
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: scaleDefs.x,
                    y: Object.assign({ beginAtZero: true }, scaleDefs.y)
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: { display: true, text: 'Day of Week', color: textColor, font: Object.assign({}, defaultFont, { size: 13 }) }
                })
            }
        });

        /* ---- Heatmap (canvas, not Chart.js) ---- */
        var heatCanvas = document.getElementById('heatmap-chart');
        var ctx = heatCanvas.getContext('2d');
        var rect = heatCanvas.parentElement.getBoundingClientRect();
        heatCanvas.width = rect.width;
        heatCanvas.height = rect.height;

        var heatDays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
        var heatDayLabels = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
        var maxHeat = 0;
        heatDays.forEach(function(day) {
            if (!data.heatmap[day]) return;
            for (var hh = 0; hh < 24; hh++) {
                var val = data.heatmap[day][hh] || data.heatmap[day][String(hh)] || 0;
                if (val > maxHeat) maxHeat = val;
            }
        });

        var leftPad = 40;
        var topPad = 20;
        var bottomPad = 30;
        var rightPad = 10;
        var cellW = (heatCanvas.width - leftPad - rightPad) / 24;
        var cellH = (heatCanvas.height - topPad - bottomPad) / 7;

        ctx.font = '11px "Roboto Slab", serif';
        ctx.textAlign = 'right';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = textColor;
        heatDayLabels.forEach(function(label, di) {
            ctx.fillText(label, leftPad - 6, topPad + di * cellH + cellH / 2);
        });

        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        for (var hh = 0; hh < 24; hh++) {
            if (hh % 3 === 0) {
                ctx.fillStyle = textColor;
                ctx.fillText(hh + ':00', leftPad + hh * cellW + cellW / 2, topPad + 7 * cellH + 6);
            }
        }

        heatDays.forEach(function(day, di) {
            for (var hh = 0; hh < 24; hh++) {
                var val = 0;
                if (data.heatmap[day]) {
                    val = data.heatmap[day][hh] || data.heatmap[day][String(hh)] || 0;
                }
                var intensity = maxHeat > 0 ? val / maxHeat : 0;
                var x = leftPad + hh * cellW;
                var y = topPad + di * cellH;

                if (isDark) {
                    var g = Math.round(40 + intensity * 215);
                    ctx.fillStyle = 'rgb(' + g + ',' + g + ',' + g + ')';
                } else {
                    var g = Math.round(255 - intensity * 230);
                    ctx.fillStyle = 'rgb(' + g + ',' + g + ',' + g + ')';
                }
                ctx.fillRect(x + 1, y + 1, cellW - 2, cellH - 2);
            }
        });

        /* ---- People percentage line chart ---- */
        var peopleYears = Object.keys(data.people_by_year).sort();
        var peoplePct = peopleYears.map(function(y) {
            var d = data.people_by_year[y];
            return d.total > 0 ? Math.round(d.with_people / d.total * 1000) / 10 : 0;
        });
        new Chart(document.getElementById('people-chart'), {
            type: 'line',
            data: {
                labels: peopleYears,
                datasets: [{
                    data: peoplePct,
                    borderColor: accentColor,
                    backgroundColor: accentColor + '22',
                    fill: true,
                    borderWidth: 2, pointRadius: 3, tension: 0.3
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: scaleDefs.x,
                    y: Object.assign({ beginAtZero: true, max: 100, ticks: Object.assign({}, scaleDefs.y.ticks, { callback: function(v) { return v + '%'; } }) }, scaleDefs.y)
                },
                plugins: Object.assign({}, pluginDefs, {
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        callbacks: { label: function(ctx) { return ctx.parsed.y + '% with people'; } }
                    })
                })
            }
        });

        /* ---- GPS percentage line chart ---- */
        var gpsYears = Object.keys(data.gps_by_year).sort();
        var gpsPct = gpsYears.map(function(y) {
            var d = data.gps_by_year[y];
            return d.total > 0 ? Math.round(d.with_gps / d.total * 1000) / 10 : 0;
        });
        new Chart(document.getElementById('gps-chart'), {
            type: 'line',
            data: {
                labels: gpsYears,
                datasets: [{
                    data: gpsPct,
                    borderColor: accentColor,
                    backgroundColor: accentColor + '22',
                    fill: true,
                    borderWidth: 2, pointRadius: 3, tension: 0.3
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: scaleDefs.x,
                    y: Object.assign({ beginAtZero: true, max: 100, ticks: Object.assign({}, scaleDefs.y.ticks, { callback: function(v) { return v + '%'; } }) }, scaleDefs.y)
                },
                plugins: Object.assign({}, pluginDefs, {
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        callbacks: { label: function(ctx) { return ctx.parsed.y + '% with GPS'; } }
                    })
                })
            }
        });

        /* ---- Aperture horizontal bar chart (top 10) ---- */
        var apertureEntries = Object.keys(data.aperture_dist).map(function(k) {
            return { label: 'f/' + k, count: data.aperture_dist[k], val: parseFloat(k) };
        }).sort(function(a, b) { return b.count - a.count; }).slice(0, 10)
         .sort(function(a, b) { return a.val - b.val; });
        new Chart(document.getElementById('aperture-chart'), {
            type: 'bar',
            data: {
                labels: apertureEntries.map(function(e) { return e.label; }),
                datasets: [{
                    data: apertureEntries.map(function(e) { return e.count; }),
                    backgroundColor: barColor,
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                indexAxis: 'y',
                scales: {
                    x: Object.assign({ beginAtZero: true }, scaleDefs.x),
                    y: scaleDefs.y
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: { display: true, text: 'Aperture', color: textColor, font: Object.assign({}, defaultFont, { size: 13 }) }
                })
            }
        });

        /* ---- Focal length horizontal bar chart (top 10) ---- */
        var focalEntries = Object.keys(data.focal_dist).map(function(k) {
            return { label: k + 'mm', count: data.focal_dist[k], val: parseInt(k) };
        }).sort(function(a, b) { return b.count - a.count; }).slice(0, 10)
         .sort(function(a, b) { return a.val - b.val; });
        new Chart(document.getElementById('focal-chart'), {
            type: 'bar',
            data: {
                labels: focalEntries.map(function(e) { return e.label; }),
                datasets: [{
                    data: focalEntries.map(function(e) { return e.count; }),
                    backgroundColor: barColor,
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                indexAxis: 'y',
                scales: {
                    x: Object.assign({ beginAtZero: true }, scaleDefs.x),
                    y: scaleDefs.y
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: { display: true, text: 'Focal Length', color: textColor, font: Object.assign({}, defaultFont, { size: 13 }) }
                })
            }
        });

        /* ---- ISO over time line chart ---- */
        var isoYears = Object.keys(data.iso_by_year).sort();
        new Chart(document.getElementById('iso-time-chart'), {
            type: 'line',
            data: {
                labels: isoYears,
                datasets: [{
                    data: isoYears.map(function(y) { return data.iso_by_year[y]; }),
                    borderColor: accentColor,
                    borderWidth: 2, pointRadius: 3, tension: 0.3,
                    fill: false
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: Object.assign({}, scaleDefs.x, { ticks: Object.assign({}, scaleDefs.x.ticks, { maxRotation: 45 }) }),
                    y: Object.assign({ beginAtZero: true }, scaleDefs.y)
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: { display: true, text: 'Avg ISO by Year', color: textColor, font: Object.assign({}, defaultFont, { size: 13 }) }
                })
            }
        });

        /* ---- Resolution line chart ---- */
        var resYears = Object.keys(data.resolution_by_year).sort();
        new Chart(document.getElementById('resolution-chart'), {
            type: 'line',
            data: {
                labels: resYears,
                datasets: [{
                    data: resYears.map(function(y) { return data.resolution_by_year[y]; }),
                    borderColor: accentColor,
                    borderWidth: 2, pointRadius: 3, tension: 0.3,
                    fill: false
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: scaleDefs.x,
                    y: Object.assign({ beginAtZero: true, ticks: Object.assign({}, scaleDefs.y.ticks, { callback: function(v) { return v + ' MP'; } }) }, scaleDefs.y)
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: { display: true, text: 'Avg Resolution', color: textColor, font: Object.assign({}, defaultFont, { size: 13 }) },
                    tooltip: Object.assign({}, pluginDefs.tooltip, {
                        callbacks: { label: function(ctx) { return ctx.parsed.y + ' MP'; } }
                    })
                })
            }
        });

        /* ---- Exposure distribution horizontal bar chart ---- */
        var exposureKeys = Object.keys(data.exposure_dist);
        var exposureCounts = exposureKeys.map(function(k) { return data.exposure_dist[k]; });
        new Chart(document.getElementById('exposure-chart'), {
            type: 'bar',
            data: {
                labels: exposureKeys,
                datasets: [{
                    data: exposureCounts,
                    backgroundColor: barColor,
                    borderRadius: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                indexAxis: 'y',
                scales: {
                    x: Object.assign({ beginAtZero: true }, scaleDefs.x),
                    y: scaleDefs.y
                },
                plugins: Object.assign({}, pluginDefs, {
                    title: { display: true, text: 'Shutter Speed', color: textColor, font: Object.assign({}, defaultFont, { size: 13 }) }
                })
            }
        });

        /* ---- Monthly volume area chart (the heartbeat) ---- */
        var months = Object.keys(data.monthly_volume).sort();
        var monthlyCounts = months.map(function(m) { return data.monthly_volume[m]; });
        /* Show every 12th label (January each year) */
        var monthLabels = months.map(function(m) {
            return m.substring(5) === '01' ? m.substring(0, 4) : '';
        });
        new Chart(document.getElementById('monthly-chart'), {
            type: 'line',
            data: {
                labels: monthLabels,
                datasets: [{
                    data: monthlyCounts,
                    borderColor: isDark ? '#e0e0e0' : '#333',
                    backgroundColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)',
                    fill: true,
                    borderWidth: 1.5, pointRadius: 0, tension: 0.2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                scales: {
                    x: Object.assign({}, scaleDefs.x, {
                        ticks: Object.assign({}, scaleDefs.x.ticks, {
                            maxRotation: 0,
                            autoSkip: false,
                            callback: function(val, i) { return monthLabels[i] || null; }
                        })
                    }),
                    y: Object.assign({ beginAtZero: true }, scaleDefs.y)
                },
                plugins: pluginDefs
            }
        });
    }

    new MutationObserver(function() { location.reload(); })
        .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
</script>
