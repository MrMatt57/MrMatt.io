#!/usr/bin/env python3
"""
Fixed evaluation harness for autoresearch-webperf.
Analogous to prepare.py in Karpathy's autoresearch.

DO NOT MODIFY THIS FILE during experiments.

Usage:
    python autoresearch/evaluate.py          # Full eval (build + Lighthouse)
    python autoresearch/evaluate.py --quick  # Quick eval (build metrics only)
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from html.parser import HTMLParser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# ── Fixed constants ──────────────────────────────────────────────────────────

SITE_DIR = Path(__file__).resolve().parent.parent  # MrMatt.io root
PUBLIC_DIR = SITE_DIR / "public"
PORT = 8765

# Pages to evaluate — representative cross-section of the site
EVAL_PAGES = [
    "/",                 # Homepage (LCP: avatar image)
    "/about/",           # Simple content page
    "/photography/",     # Heaviest page (gallery JS, many images)
]

# HTML attributes that may change for perf without affecting visuals
PERF_ATTRS = frozenset({
    "loading", "fetchpriority", "decoding", "sizes", "srcset",
    "media", "as", "crossorigin", "importance", "rel",
    "async", "defer", "type", "integrity", "nonce",
})


# ── Structural integrity ────────────────────────────────────────────────────

class BodyStructureParser(HTMLParser):
    """
    Extract the body's tag tree for visual regression detection.

    Captures tag names and structural attributes (class, id, role) while
    ignoring performance-only attributes. If the resulting tree changes
    between experiments, the agent made a structural/visual change.
    """

    def __init__(self):
        super().__init__()
        self.in_body = False
        self.depth = 0
        self.tokens = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
            self.depth = 0
            return
        if not self.in_body:
            return
        # Keep only structural attributes
        structural = []
        for name, value in sorted(attrs):
            if name in ("class", "id", "role", "aria-label"):
                structural.append(f"{name}={value}")
        attr_str = " ".join(structural)
        self.tokens.append(f"{'  ' * self.depth}<{tag} {attr_str}>")
        self.depth += 1

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
            return
        if not self.in_body:
            return
        self.depth = max(0, self.depth - 1)
        self.tokens.append(f"{'  ' * self.depth}</{tag}>")


def compute_structure_hash(pages):
    """
    Compute a combined structural hash of key pages' <body> content.
    Returns (combined_hash, {page: hash}).
    """
    page_hashes = {}

    for page in pages:
        if page.endswith("/"):
            filepath = PUBLIC_DIR / page.lstrip("/") / "index.html"
        else:
            filepath = PUBLIC_DIR / page.lstrip("/")

        if not filepath.exists():
            page_hashes[page] = "MISSING"
            continue

        html = filepath.read_text(encoding="utf-8", errors="replace")
        parser = BodyStructureParser()
        parser.feed(html)
        tree = "\n".join(parser.tokens)
        page_hashes[page] = hashlib.sha256(tree.encode()).hexdigest()[:16]

    combined = "|".join(f"{p}={h}" for p, h in sorted(page_hashes.items()))
    combined_hash = hashlib.sha256(combined.encode()).hexdigest()[:16]
    return combined_hash, page_hashes


# ── Build ────────────────────────────────────────────────────────────────────

def build_site():
    """Build the Hugo site. Returns (success, build_time_ms, stderr)."""
    start = time.time()
    try:
        result = subprocess.run(
            ["hugo", "--minify", "--gc"],
            cwd=str(SITE_DIR),
            capture_output=True,
            text=True,
            timeout=120,
        )
        elapsed = (time.time() - start) * 1000
        return result.returncode == 0, elapsed, result.stderr.strip()
    except subprocess.TimeoutExpired:
        elapsed = (time.time() - start) * 1000
        return False, elapsed, "BUILD TIMEOUT (>120s)"
    except FileNotFoundError:
        return False, 0, "hugo not found in PATH"


# ── Output metrics ───────────────────────────────────────────────────────────

def measure_output():
    """Measure build output file sizes by category."""
    totals = {"total": 0, "html": 0, "css": 0, "js": 0, "img": 0, "font": 0}
    file_count = 0

    ext_map = {
        ".html": "html", ".htm": "html",
        ".css": "css",
        ".js": "js",
        ".jpg": "img", ".jpeg": "img", ".png": "img", ".gif": "img",
        ".webp": "img", ".svg": "img", ".avif": "img", ".ico": "img",
        ".woff2": "font", ".woff": "font", ".ttf": "font", ".otf": "font",
    }

    for f in PUBLIC_DIR.rglob("*"):
        if not f.is_file():
            continue
        size = f.stat().st_size
        totals["total"] += size
        file_count += 1
        category = ext_map.get(f.suffix.lower())
        if category:
            totals[category] += size

    return {
        "total_size_kb": round(totals["total"] / 1024, 1),
        "html_size_kb": round(totals["html"] / 1024, 1),
        "css_size_kb": round(totals["css"] / 1024, 1),
        "js_size_kb": round(totals["js"] / 1024, 1),
        "img_size_kb": round(totals["img"] / 1024, 1),
        "font_size_kb": round(totals["font"] / 1024, 1),
        "file_count": file_count,
    }


# ── Lighthouse ───────────────────────────────────────────────────────────────

def _find_lighthouse():
    """Find lighthouse CLI. Returns command list or None."""
    if shutil.which("lighthouse"):
        return ["lighthouse"]
    if shutil.which("npx"):
        return ["npx", "lighthouse"]
    return None


def serve_site():
    """Start a quiet local HTTP server. Returns the server instance."""
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)
        def handle(self):
            try:
                super().handle()
            except ConnectionResetError:
                pass  # Normal during Lighthouse probing

    server = HTTPServer(("127.0.0.1", PORT), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.5)
    return server


def run_lighthouse_page(cmd_base, page):
    """Run Lighthouse on one page with mobile throttling. Returns scores dict or None."""
    url = f"http://127.0.0.1:{PORT}{page}"
    cmd = cmd_base + [
        url,
        "--output=json",
        "--chrome-flags=--headless --no-sandbox --disable-gpu",
        "--only-categories=performance",
        "--quiet",
        # Mobile throttling (Lighthouse defaults, made explicit)
        "--screenEmulation.mobile=true",
        "--screenEmulation.width=412",
        "--screenEmulation.height=823",
        "--throttling-method=simulate",
        "--throttling.cpuSlowdownMultiplier=4",
        "--throttling.downloadThroughputKbps=1638.4",
        "--throttling.uploadThroughputKbps=675",
        "--throttling.rttMs=150",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
            shell=(os.name == "nt"),  # Windows needs shell for .CMD scripts
        )
        # Note: Lighthouse may return exit code 1 on Windows due to Chrome
        # launcher cleanup — so we ignore returncode and try to parse JSON.
        if not result.stdout.strip():
            return None

        data = json.loads(result.stdout)
        cats = data.get("categories", {})
        audits = data.get("audits", {})

        perf_raw = cats.get("performance", {}).get("score")
        if perf_raw is None:
            return None

        return {
            "perf_score": round(perf_raw * 100),
            "fcp_ms": round(audits.get("first-contentful-paint", {}).get("numericValue", 0)),
            "lcp_ms": round(audits.get("largest-contentful-paint", {}).get("numericValue", 0)),
            "cls": round(audits.get("cumulative-layout-shift", {}).get("numericValue", 0), 4),
            "tbt_ms": round(audits.get("total-blocking-time", {}).get("numericValue", 0)),
            "si_ms": round(audits.get("speed-index", {}).get("numericValue", 0)),
        }
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def run_lighthouse_all(pages):
    """Run Lighthouse on all eval pages. Returns (avg_scores, per_page)."""
    cmd = _find_lighthouse()
    if not cmd:
        return None, {}

    server = None
    try:
        server = serve_site()
        per_page = {}
        for page in pages:
            scores = run_lighthouse_page(cmd, page)
            if scores:
                per_page[page] = scores

        if not per_page:
            return None, {}

        n = len(per_page)
        worst_lcp = max(s["lcp_ms"] for s in per_page.values())
        avg = {
            "worst_lcp_ms": worst_lcp,
            "perf_score": round(sum(s["perf_score"] for s in per_page.values()) / n),
            "avg_fcp_ms": round(sum(s["fcp_ms"] for s in per_page.values()) / n),
            "avg_lcp_ms": round(sum(s["lcp_ms"] for s in per_page.values()) / n),
            "avg_cls": round(sum(s["cls"] for s in per_page.values()) / n, 4),
            "avg_tbt_ms": round(sum(s["tbt_ms"] for s in per_page.values()) / n),
            "avg_si_ms": round(sum(s["si_ms"] for s in per_page.values()) / n),
        }
        return avg, per_page
    finally:
        if server:
            server.shutdown()


# ── Main evaluation ─────────────────────────────────────────────────────────

def evaluate(quick=False):
    """Run the full evaluation pipeline and print results."""
    print("=" * 60)
    print("AUTORESEARCH-WEBPERF EVALUATION" + (" (quick)" if quick else ""))
    print("=" * 60)

    # 1. Build
    success, build_ms, stderr = build_site()
    if not success:
        print("---")
        print("build_status:     FAILED")
        print(f"build_error:      {stderr[:300]}")
        return

    # 2. Output metrics
    metrics = measure_output()

    # 3. Structural integrity
    combined_hash, page_hashes = compute_structure_hash(EVAL_PAGES)

    # 4. Lighthouse (skip in quick mode)
    avg_scores = None
    per_page = {}
    if not quick:
        avg_scores, per_page = run_lighthouse_all(EVAL_PAGES)

    # 5. Print results (grep-friendly key: value format)
    print("---")
    print(f"build_time_ms:    {build_ms:.0f}")
    print(f"total_size_kb:    {metrics['total_size_kb']}")
    print(f"html_size_kb:     {metrics['html_size_kb']}")
    print(f"css_size_kb:      {metrics['css_size_kb']}")
    print(f"js_size_kb:       {metrics['js_size_kb']}")
    print(f"img_size_kb:      {metrics['img_size_kb']}")
    print(f"font_size_kb:     {metrics['font_size_kb']}")
    print(f"file_count:       {metrics['file_count']}")
    print(f"structure_hash:   {combined_hash}")

    for page, h in sorted(page_hashes.items()):
        print(f"  hash[{page}]: {h}")

    if avg_scores:
        print(f"worst_lcp_ms:     {avg_scores['worst_lcp_ms']}  << PRIMARY METRIC (lower is better)")
        print(f"perf_score:       {avg_scores['perf_score']}")
        print(f"avg_fcp_ms:       {avg_scores['avg_fcp_ms']}")
        print(f"avg_lcp_ms:       {avg_scores['avg_lcp_ms']}")
        print(f"avg_cls:          {avg_scores['avg_cls']}")
        print(f"avg_tbt_ms:       {avg_scores['avg_tbt_ms']}")
        print(f"avg_si_ms:        {avg_scores['avg_si_ms']}")
        for page, scores in sorted(per_page.items()):
            print(f"  lighthouse[{page}]: perf={scores['perf_score']}"
                  f" fcp={scores['fcp_ms']}ms lcp={scores['lcp_ms']}ms"
                  f" cls={scores['cls']} tbt={scores['tbt_ms']}ms")
    elif not quick:
        print("worst_lcp_ms:     N/A")
        print("# Lighthouse not found. Install: npm install -g lighthouse")
        print("# Falling back to total_size_kb as metric (lower is better)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autoresearch web perf evaluator")
    parser.add_argument(
        "--quick", action="store_true",
        help="Skip Lighthouse, only measure build output metrics",
    )
    args = parser.parse_args()
    evaluate(quick=args.quick)
