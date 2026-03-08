#!/usr/bin/env python3
"""
Photo Scorer — Find your best photos using AI.

Pipeline:
  1. SCAN   — Extract EXIF metadata, detect duplicates, catalog all photos
  2. FILTER — Pre-filter by technical quality signals (resolution, camera, etc.)
  3. SCORE  — Quick AI scoring with Claude Haiku (1-10 rating per photo)
  4. RANK   — Detailed AI analysis of top candidates with Claude Sonnet

Usage:
  python score_photos.py scan   <photo_dir>                    # Stage 1
  python score_photos.py filter [--min-mp 4] [--cameras ...]   # Stage 2
  python score_photos.py score  [--batch-size 5] [--workers 4] # Stage 3
  python score_photos.py rank   [--top 500]                    # Stage 4
  python score_photos.py pipeline <photo_dir> [all options]    # All stages
  python score_photos.py costs                                 # Estimate costs

All outputs are saved to <photo_dir>/.photo-scorer/ and are resumable.
"""

import argparse
import base64
import hashlib
import io
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image, ExifTags
from tqdm import tqdm

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIF_SUPPORTED = True
except ImportError:
    HEIF_SUPPORTED = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp", ".bmp",
    ".heic", ".heif",
}

# Common screenshot resolutions to flag
SCREENSHOT_RESOLUTIONS = {
    (1920, 1080), (2560, 1440), (3840, 2160), (1080, 1920),
    (1440, 2560), (2160, 3840), (1366, 768), (768, 1366),
    (2560, 1600), (1600, 2560), (2880, 1800), (1800, 2880),
    (1280, 720), (720, 1280), (3024, 1964), (1964, 3024),
}

QUICK_SCORE_PROMPT = """You are an expert photography curator selecting images for a personal website portfolio.

For each photo, provide a JSON object with:
- "score": integer 1-10 (10 = stunning portfolio piece, 7+ = website worthy, 4-6 = decent but not special, 1-3 = not suitable)
- "category": one of "landscape", "portrait", "architecture", "street", "nature", "wildlife", "food", "travel", "macro", "aerial", "abstract", "event", "other"
- "brief": 5-10 word description

Scoring guide:
- 9-10: Exceptional composition, lighting, subject. Would anchor a portfolio.
- 7-8: Strong photo, good technique, interesting subject. Solid portfolio addition.
- 5-6: Technically OK but not compelling. Ordinary subject or composition.
- 3-4: Snapshot quality. Poor composition, boring subject, or technical issues.
- 1-2: Not a photograph worth keeping (blurry, dark, accidental, screenshot).

Be selective. Only 5-10% of photos should score 7+. This is a curated portfolio, not a photo dump.

Respond with ONLY a JSON array of objects, one per image, in the order they were provided.
Example: [{"score": 8, "category": "landscape", "brief": "Golden hour mountain lake reflection"}]"""

DETAILED_RANK_PROMPT = """You are a professional photography curator doing final portfolio selection.

Analyze this photograph in detail for inclusion in a personal website photography portfolio.

Score each dimension 1-10:
- "composition": Balance, rule of thirds, leading lines, framing, depth
- "technical": Sharpness, exposure, dynamic range, color accuracy, noise
- "visual_interest": How compelling, striking, or emotionally engaging
- "uniqueness": How distinctive — would this stand out in a portfolio?
- "web_suitability": Overall fit for a personal photography portfolio

Also provide:
- "overall": weighted average (composition 25%, technical 20%, visual_interest 30%, uniqueness 15%, web_suitability 10%)
- "category": landscape|portrait|architecture|street|nature|wildlife|food|travel|macro|aerial|abstract|event|other
- "tags": list of 3-5 descriptive tags
- "description": One compelling sentence describing the photo
- "standout": What makes this photo special (or what holds it back)

Respond with ONLY a JSON object."""

# Resize target for API calls (pixels on long edge)
QUICK_SCORE_SIZE = 512
DETAILED_RANK_SIZE = 1024

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("photo-scorer")


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class PhotoMeta:
    path: str
    filename: str
    size_bytes: int
    width: int = 0
    height: int = 0
    megapixels: float = 0.0
    camera_make: str = ""
    camera_model: str = ""
    lens: str = ""
    focal_length: str = ""
    aperture: str = ""
    shutter_speed: str = ""
    iso: str = ""
    date_taken: str = ""
    has_gps: bool = False
    file_hash: str = ""
    is_screenshot: bool = False
    google_origin: str = ""  # from Takeout JSON sidecar
    google_description: str = ""

    # Scores (filled in later stages)
    quick_score: int = 0
    quick_category: str = ""
    quick_brief: str = ""
    detailed_scores: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Stage 1: SCAN — Extract EXIF + catalog
# ---------------------------------------------------------------------------

def file_hash_quick(path: Path, chunk_size: int = 65536) -> str:
    """Fast hash using first 64KB + file size for dedup."""
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            h.update(f.read(chunk_size))
        h.update(str(path.stat().st_size).encode())
    except OSError:
        return ""
    return h.hexdigest()


def extract_exif(path: Path) -> dict:
    """Extract EXIF data from an image file."""
    result = {}
    try:
        with Image.open(path) as img:
            result["width"] = img.width
            result["height"] = img.height

            exif_data = img.getexif()
            if not exif_data:
                return result

            # Map tag IDs to names
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                if isinstance(value, bytes):
                    continue
                result[tag_name] = str(value)

            # Try to get IFD EXIF data (contains more detail)
            try:
                ifd = exif_data.get_ifd(ExifTags.IFD.Exif)
                for tag_id, value in ifd.items():
                    tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                    if isinstance(value, bytes):
                        continue
                    result[tag_name] = str(value)
            except Exception:
                pass

            # Check for GPS
            try:
                gps_ifd = exif_data.get_ifd(ExifTags.IFD.GPSInfo)
                result["has_gps"] = bool(gps_ifd)
            except Exception:
                result["has_gps"] = False

    except Exception as e:
        log.debug(f"EXIF extraction failed for {path}: {e}")
    return result


def parse_google_sidecar(image_path: Path) -> dict:
    """Parse Google Takeout JSON sidecar file if it exists."""
    sidecar = image_path.parent / f"{image_path.name}.json"
    if not sidecar.exists():
        # Sometimes the JSON has a slightly different name
        for candidate in image_path.parent.glob(f"{image_path.stem}*.json"):
            sidecar = candidate
            break
        else:
            return {}
    try:
        with open(sidecar, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = {}
        origin = data.get("googlePhotosOrigin", {})
        if "mobileUpload" in origin:
            result["google_origin"] = origin["mobileUpload"].get("deviceType", "mobile")
        elif "fromPartnerSharing" in origin:
            result["google_origin"] = "partner_sharing"
        result["google_description"] = data.get("description", "")
        if "photoTakenTime" in data:
            ts = int(data["photoTakenTime"].get("timestamp", 0))
            if ts:
                result["date_taken_ts"] = ts
        return result
    except Exception:
        return {}


def scan_single_photo(path: Path) -> Optional[PhotoMeta]:
    """Scan a single photo and return its metadata."""
    try:
        stat = path.stat()
        exif = extract_exif(path)
        sidecar = parse_google_sidecar(path)

        w = exif.get("width", 0)
        h = exif.get("height", 0)
        mp = (w * h) / 1_000_000 if w and h else 0

        is_screenshot = (
            (w, h) in SCREENSHOT_RESOLUTIONS
            and not exif.get("Make", "")
            and not exif.get("Model", "")
        )

        date_taken = exif.get("DateTimeOriginal", exif.get("DateTime", ""))

        return PhotoMeta(
            path=str(path),
            filename=path.name,
            size_bytes=stat.st_size,
            width=w,
            height=h,
            megapixels=round(mp, 1),
            camera_make=exif.get("Make", ""),
            camera_model=exif.get("Model", ""),
            lens=exif.get("LensModel", exif.get("LensSpecification", "")),
            focal_length=exif.get("FocalLength", ""),
            aperture=exif.get("FNumber", exif.get("ApertureValue", "")),
            shutter_speed=exif.get("ExposureTime", exif.get("ShutterSpeedValue", "")),
            iso=exif.get("ISOSpeedRatings", ""),
            date_taken=date_taken,
            has_gps=exif.get("has_gps", False),
            file_hash=file_hash_quick(path),
            is_screenshot=is_screenshot,
            google_origin=sidecar.get("google_origin", ""),
            google_description=sidecar.get("google_description", ""),
        )
    except Exception as e:
        log.debug(f"Failed to scan {path}: {e}")
        return None


def find_all_images(photo_dir: Path) -> list[Path]:
    """Recursively find all image files."""
    images = []
    for root, _, files in os.walk(photo_dir):
        for f in files:
            if Path(f).suffix.lower() in IMAGE_EXTENSIONS:
                images.append(Path(root) / f)
    return images


def stage_scan(photo_dir: Path, output_dir: Path, workers: int = 8) -> list[PhotoMeta]:
    """Stage 1: Scan all photos and extract metadata."""
    scan_file = output_dir / "1_scan.json"

    # Resume support
    existing = {}
    if scan_file.exists():
        log.info("Found existing scan data, loading for resume...")
        with open(scan_file, "r") as f:
            for item in json.load(f):
                existing[item["path"]] = item

    log.info("Finding all images...")
    all_images = find_all_images(photo_dir)
    log.info(f"Found {len(all_images):,} image files")

    # Skip already-scanned files
    to_scan = [p for p in all_images if str(p) not in existing]
    log.info(f"Need to scan {len(to_scan):,} new files ({len(existing):,} already scanned)")

    results = list(existing.values())
    scanned_count = 0

    if to_scan:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(scan_single_photo, p): p for p in to_scan}
            with tqdm(total=len(to_scan), desc="Scanning", unit="photo") as pbar:
                for future in as_completed(futures):
                    meta = future.result()
                    if meta:
                        results.append(asdict(meta))
                    pbar.update(1)
                    scanned_count += 1

                    # Periodic save every 5000 photos
                    if scanned_count % 5000 == 0:
                        with open(scan_file, "w") as f:
                            json.dump(results, f)

    # Final save
    with open(scan_file, "w") as f:
        json.dump(results, f, indent=2)

    log.info(f"Scan complete: {len(results):,} photos cataloged → {scan_file}")

    # Print summary stats
    cameras = {}
    for r in results:
        cam = r.get("camera_model", "") or "Unknown"
        cameras[cam] = cameras.get(cam, 0) + 1
    log.info("Top cameras:")
    for cam, count in sorted(cameras.items(), key=lambda x: -x[1])[:10]:
        log.info(f"  {cam}: {count:,}")

    screenshots = sum(1 for r in results if r.get("is_screenshot"))
    log.info(f"Detected screenshots: {screenshots:,}")

    return results


# ---------------------------------------------------------------------------
# Stage 2: FILTER — Pre-filter by quality signals
# ---------------------------------------------------------------------------

def stage_filter(
    output_dir: Path,
    min_mp: float = 4.0,
    min_file_size: int = 500_000,
    exclude_screenshots: bool = True,
    camera_allowlist: Optional[list[str]] = None,
    camera_blocklist: Optional[list[str]] = None,
    dedup: bool = True,
) -> list[dict]:
    """Stage 2: Pre-filter photos based on technical quality signals."""
    scan_file = output_dir / "1_scan.json"
    filter_file = output_dir / "2_filtered.json"

    if not scan_file.exists():
        log.error("No scan data found. Run 'scan' first.")
        sys.exit(1)

    with open(scan_file, "r") as f:
        photos = json.load(f)

    log.info(f"Starting filter on {len(photos):,} photos")
    initial = len(photos)

    # Filter: minimum resolution
    photos = [p for p in photos if p.get("megapixels", 0) >= min_mp]
    log.info(f"  After min {min_mp}MP filter: {len(photos):,} ({initial - len(photos):,} removed)")

    # Filter: minimum file size (eliminates thumbnails, icons)
    before = len(photos)
    photos = [p for p in photos if p.get("size_bytes", 0) >= min_file_size]
    log.info(f"  After min file size ({min_file_size // 1000}KB): {len(photos):,} ({before - len(photos):,} removed)")

    # Filter: screenshots
    if exclude_screenshots:
        before = len(photos)
        photos = [p for p in photos if not p.get("is_screenshot")]
        log.info(f"  After screenshot removal: {len(photos):,} ({before - len(photos):,} removed)")

    # Filter: camera allowlist
    if camera_allowlist:
        before = len(photos)
        allow_lower = [c.lower() for c in camera_allowlist]
        photos = [
            p for p in photos
            if any(a in (p.get("camera_model", "") or "").lower() for a in allow_lower)
        ]
        log.info(f"  After camera allowlist: {len(photos):,} ({before - len(photos):,} removed)")

    # Filter: camera blocklist
    if camera_blocklist:
        before = len(photos)
        block_lower = [c.lower() for c in camera_blocklist]
        photos = [
            p for p in photos
            if not any(b in (p.get("camera_model", "") or "").lower() for b in block_lower)
        ]
        log.info(f"  After camera blocklist: {len(photos):,} ({before - len(photos):,} removed)")

    # Dedup by file hash
    if dedup:
        before = len(photos)
        seen_hashes = set()
        deduped = []
        for p in photos:
            h = p.get("file_hash", "")
            if h and h in seen_hashes:
                continue
            if h:
                seen_hashes.add(h)
            deduped.append(p)
        photos = deduped
        log.info(f"  After dedup: {len(photos):,} ({before - len(photos):,} duplicates removed)")

    with open(filter_file, "w") as f:
        json.dump(photos, f, indent=2)

    log.info(f"Filter complete: {len(photos):,} candidates → {filter_file}")
    return photos


# ---------------------------------------------------------------------------
# Stage 3: SCORE — Quick AI scoring with Claude Haiku
# ---------------------------------------------------------------------------

def resize_for_api(image_path: str, max_size: int) -> Optional[str]:
    """Resize image and return base64-encoded JPEG."""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Resize maintaining aspect ratio
            w, h = img.size
            if max(w, h) > max_size:
                ratio = max_size / max(w, h)
                new_size = (int(w * ratio), int(h * ratio))
                img = img.resize(new_size, Image.LANCZOS)

            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=80)
            return base64.standard_b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        log.debug(f"Failed to resize {image_path}: {e}")
        return None


def score_batch(client, batch: list[dict], model: str) -> list[dict]:
    """Score a batch of photos using Claude Vision API."""
    content = []

    for i, photo in enumerate(batch):
        img_b64 = resize_for_api(photo["path"], QUICK_SCORE_SIZE)
        if not img_b64:
            continue
        content.append({
            "type": "text",
            "text": f"Photo {i + 1} ({photo['filename']}):"
        })
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": img_b64,
            }
        })

    if not content:
        return []

    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=QUICK_SCORE_PROMPT,
            messages=[{"role": "user", "content": content}],
        )
        text = response.content[0].text.strip()
        # Extract JSON from response
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        scores = json.loads(text)
        if isinstance(scores, dict):
            scores = [scores]
        return scores
    except json.JSONDecodeError as e:
        log.warning(f"Failed to parse AI response: {e}")
        log.debug(f"Response text: {text}")
        return []
    except Exception as e:
        log.warning(f"API call failed: {e}")
        return []


def stage_score(
    output_dir: Path,
    batch_size: int = 5,
    workers: int = 4,
    model: str = "claude-haiku-4-5-20251001",
    rate_limit_delay: float = 0.1,
) -> list[dict]:
    """Stage 3: Quick AI scoring of filtered photos."""
    if not ANTHROPIC_AVAILABLE:
        log.error("anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)

    filter_file = output_dir / "2_filtered.json"
    score_file = output_dir / "3_scored.json"

    if not filter_file.exists():
        log.error("No filtered data found. Run 'filter' first.")
        sys.exit(1)

    with open(filter_file, "r") as f:
        photos = json.load(f)

    # Resume support: load existing scores
    scored = {}
    if score_file.exists():
        with open(score_file, "r") as f:
            for item in json.load(f):
                scored[item["path"]] = item

    to_score = [p for p in photos if p["path"] not in scored]
    log.info(f"Scoring {len(to_score):,} photos ({len(scored):,} already scored)")

    if not to_score:
        log.info("All photos already scored!")
        return list(scored.values())

    # Cost estimate
    est_batches = (len(to_score) + batch_size - 1) // batch_size
    est_input_tokens = est_batches * (500 + batch_size * 800)  # prompt + images
    est_output_tokens = est_batches * batch_size * 40
    est_cost = (est_input_tokens * 0.80 + est_output_tokens * 4.0) / 1_000_000
    log.info(f"Estimated cost: ~${est_cost:.2f} ({est_batches:,} API calls)")
    log.info(f"Estimated tokens: ~{est_input_tokens:,} input, ~{est_output_tokens:,} output")

    client = anthropic.Anthropic()

    # Process in batches
    batches = [to_score[i:i + batch_size] for i in range(0, len(to_score), batch_size)]
    results = list(scored.values())
    save_interval = max(1, len(batches) // 20)  # Save ~20 times during the run

    with tqdm(total=len(to_score), desc="AI Scoring", unit="photo") as pbar:
        for batch_idx, batch in enumerate(batches):
            scores = score_batch(client, batch, model)

            # Match scores back to photos
            for i, photo in enumerate(batch):
                if i < len(scores):
                    s = scores[i]
                    photo["quick_score"] = s.get("score", 0)
                    photo["quick_category"] = s.get("category", "")
                    photo["quick_brief"] = s.get("brief", "")
                else:
                    photo["quick_score"] = 0
                    photo["quick_category"] = ""
                    photo["quick_brief"] = "scoring_failed"
                results.append(photo)
                scored[photo["path"]] = photo

            pbar.update(len(batch))

            # Periodic save
            if (batch_idx + 1) % save_interval == 0:
                with open(score_file, "w") as f:
                    json.dump(results, f)

            time.sleep(rate_limit_delay)

    # Sort by score descending
    results.sort(key=lambda x: x.get("quick_score", 0), reverse=True)

    with open(score_file, "w") as f:
        json.dump(results, f, indent=2)

    # Print score distribution
    dist = {}
    for r in results:
        s = r.get("quick_score", 0)
        dist[s] = dist.get(s, 0) + 1
    log.info("Score distribution:")
    for score in sorted(dist.keys(), reverse=True):
        bar = "#" * (dist[score] // max(1, max(dist.values()) // 40))
        log.info(f"  {score:2d}: {dist[score]:6,} {bar}")

    high = sum(1 for r in results if r.get("quick_score", 0) >= 7)
    log.info(f"Photos scoring 7+: {high:,} ({100 * high / max(1, len(results)):.1f}%)")
    log.info(f"Scoring complete → {score_file}")
    return results


# ---------------------------------------------------------------------------
# Stage 4: RANK — Detailed AI analysis of top candidates
# ---------------------------------------------------------------------------

def rank_single(client, photo: dict, model: str) -> dict:
    """Detailed scoring of a single photo."""
    img_b64 = resize_for_api(photo["path"], DETAILED_RANK_SIZE)
    if not img_b64:
        return photo

    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=DETAILED_RANK_PROMPT,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": img_b64,
                        }
                    },
                    {
                        "type": "text",
                        "text": f"Filename: {photo['filename']}\nCamera: {photo.get('camera_model', 'Unknown')}\nQuick score: {photo.get('quick_score', 'N/A')}"
                    }
                ]
            }],
        )
        text = response.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        detailed = json.loads(text)
        photo["detailed_scores"] = detailed
        photo["detailed_overall"] = detailed.get("overall", 0)
    except Exception as e:
        log.warning(f"Detailed scoring failed for {photo['filename']}: {e}")
        photo["detailed_scores"] = {}
        photo["detailed_overall"] = 0

    return photo


def stage_rank(
    output_dir: Path,
    top_n: int = 500,
    model: str = "claude-sonnet-4-20250514",
    workers: int = 3,
    rate_limit_delay: float = 0.2,
) -> list[dict]:
    """Stage 4: Detailed ranking of top candidates."""
    if not ANTHROPIC_AVAILABLE:
        log.error("anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)

    score_file = output_dir / "3_scored.json"
    rank_file = output_dir / "4_ranked.json"
    csv_file = output_dir / "4_ranked.csv"

    if not score_file.exists():
        log.error("No score data found. Run 'score' first.")
        sys.exit(1)

    with open(score_file, "r") as f:
        all_scored = json.load(f)

    # Take top N by quick score
    all_scored.sort(key=lambda x: x.get("quick_score", 0), reverse=True)
    candidates = all_scored[:top_n]
    log.info(f"Detailed ranking of top {len(candidates):,} photos")

    # Resume support
    ranked = {}
    if rank_file.exists():
        with open(rank_file, "r") as f:
            for item in json.load(f):
                if item.get("detailed_scores"):
                    ranked[item["path"]] = item

    to_rank = [p for p in candidates if p["path"] not in ranked]
    log.info(f"Need to rank {len(to_rank):,} photos ({len(ranked):,} already ranked)")

    if not to_rank:
        log.info("All candidates already ranked!")
        results = list(ranked.values())
    else:
        # Cost estimate
        est_input = len(to_rank) * 2200
        est_output = len(to_rank) * 300
        est_cost = (est_input * 3.0 + est_output * 15.0) / 1_000_000
        log.info(f"Estimated cost: ~${est_cost:.2f}")

        client = anthropic.Anthropic()
        results = list(ranked.values())
        save_interval = max(1, len(to_rank) // 20)

        with tqdm(total=len(to_rank), desc="Detailed Ranking", unit="photo") as pbar:
            for idx, photo in enumerate(to_rank):
                result = rank_single(client, photo, model)
                results.append(result)
                ranked[result["path"]] = result
                pbar.update(1)

                if (idx + 1) % save_interval == 0:
                    with open(rank_file, "w") as f:
                        json.dump(results, f)

                time.sleep(rate_limit_delay)

    # Sort by detailed overall score
    results.sort(key=lambda x: x.get("detailed_overall", 0), reverse=True)

    with open(rank_file, "w") as f:
        json.dump(results, f, indent=2)

    # Write CSV for easy review
    import csv
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Rank", "Overall", "Composition", "Technical", "Visual Interest",
            "Uniqueness", "Web Suitability", "Category", "Description",
            "Tags", "Filename", "Path", "Camera", "Quick Score"
        ])
        for i, r in enumerate(results, 1):
            d = r.get("detailed_scores", {})
            writer.writerow([
                i,
                d.get("overall", ""),
                d.get("composition", ""),
                d.get("technical", ""),
                d.get("visual_interest", ""),
                d.get("uniqueness", ""),
                d.get("web_suitability", ""),
                d.get("category", r.get("quick_category", "")),
                d.get("description", r.get("quick_brief", "")),
                "|".join(d.get("tags", [])),
                r.get("filename", ""),
                r.get("path", ""),
                r.get("camera_model", ""),
                r.get("quick_score", ""),
            ])

    log.info(f"Ranking complete → {rank_file}")
    log.info(f"CSV export → {csv_file}")
    log.info(f"\nTop 20 photos:")
    for i, r in enumerate(results[:20], 1):
        d = r.get("detailed_scores", {})
        log.info(
            f"  {i:3d}. [{d.get('overall', '?')}/10] {r['filename']}"
            f" — {d.get('description', r.get('quick_brief', ''))}"
        )

    return results


# ---------------------------------------------------------------------------
# Cost estimator
# ---------------------------------------------------------------------------

def estimate_costs(output_dir: Path, batch_size: int = 5, top_n: int = 500):
    """Print cost estimates based on current pipeline state."""
    print("\n=== Photo Scorer Cost Estimate ===\n")

    scan_file = output_dir / "1_scan.json"
    filter_file = output_dir / "2_filtered.json"

    if scan_file.exists():
        with open(scan_file, "r") as f:
            scan_count = len(json.load(f))
        print(f"Scanned photos: {scan_count:,}")
    else:
        scan_count = 0
        print("Scanned photos: (run 'scan' first)")

    if filter_file.exists():
        with open(filter_file, "r") as f:
            filter_count = len(json.load(f))
        print(f"Filtered candidates: {filter_count:,}")
    else:
        filter_count = int(scan_count * 0.15) if scan_count else 30000
        print(f"Filtered candidates: ~{filter_count:,} (estimated)")

    # Stage 3: Haiku quick scoring
    batches = (filter_count + batch_size - 1) // batch_size
    haiku_input = batches * (500 + batch_size * 800)
    haiku_output = batches * batch_size * 40
    haiku_cost = (haiku_input * 0.80 + haiku_output * 4.0) / 1_000_000

    print(f"\nStage 3 — Haiku Quick Score ({filter_count:,} photos):")
    print(f"  API calls: ~{batches:,}")
    print(f"  Tokens: ~{haiku_input:,} in, ~{haiku_output:,} out")
    print(f"  Cost: ~${haiku_cost:.2f}")

    # Stage 4: Sonnet detailed ranking
    rank_count = min(top_n, filter_count)
    sonnet_input = rank_count * 2200
    sonnet_output = rank_count * 300
    sonnet_cost = (sonnet_input * 3.0 + sonnet_output * 15.0) / 1_000_000

    print(f"\nStage 4 — Sonnet Detailed Rank (top {rank_count:,} photos):")
    print(f"  API calls: ~{rank_count:,}")
    print(f"  Tokens: ~{sonnet_input:,} in, ~{sonnet_output:,} out")
    print(f"  Cost: ~${sonnet_cost:.2f}")

    print(f"\n  Total estimated cost: ~${haiku_cost + sonnet_cost:.2f}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Photo Scorer — Find your best photos using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full pipeline on a Google Takeout export
  python score_photos.py pipeline ~/Photos/Takeout/Google\\ Photos

  # Just scan and filter to see what you're working with
  python score_photos.py scan ~/Photos
  python score_photos.py filter --min-mp 6

  # Score with a specific model
  python score_photos.py score --model claude-haiku-4-5-20251001

  # Rank top 1000 instead of default 500
  python score_photos.py rank --top 1000

  # See estimated costs before committing
  python score_photos.py costs
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Pipeline stage to run")

    # scan
    p_scan = subparsers.add_parser("scan", help="Stage 1: Scan photos and extract EXIF")
    p_scan.add_argument("photo_dir", type=Path, help="Directory containing photos")
    p_scan.add_argument("--workers", type=int, default=8, help="Parallel scan workers")
    p_scan.add_argument("--output", type=Path, help="Output directory (default: <photo_dir>/.photo-scorer)")

    # filter
    p_filter = subparsers.add_parser("filter", help="Stage 2: Pre-filter by quality signals")
    p_filter.add_argument("--min-mp", type=float, default=4.0, help="Minimum megapixels (default: 4)")
    p_filter.add_argument("--min-file-size", type=int, default=500000, help="Minimum file size in bytes")
    p_filter.add_argument("--keep-screenshots", action="store_true", help="Don't exclude screenshots")
    p_filter.add_argument("--cameras", nargs="+", help="Only include these camera models")
    p_filter.add_argument("--exclude-cameras", nargs="+", help="Exclude these camera models")
    p_filter.add_argument("--no-dedup", action="store_true", help="Skip deduplication")
    p_filter.add_argument("--output", type=Path, help="Output directory")

    # score
    p_score = subparsers.add_parser("score", help="Stage 3: Quick AI scoring")
    p_score.add_argument("--batch-size", type=int, default=5, help="Photos per API call")
    p_score.add_argument("--workers", type=int, default=4, help="Parallel API workers")
    p_score.add_argument("--model", default="claude-haiku-4-5-20251001", help="Model for scoring")
    p_score.add_argument("--rate-limit", type=float, default=0.1, help="Delay between API calls (seconds)")
    p_score.add_argument("--output", type=Path, help="Output directory")

    # rank
    p_rank = subparsers.add_parser("rank", help="Stage 4: Detailed ranking of top photos")
    p_rank.add_argument("--top", type=int, default=500, help="Number of top photos to rank in detail")
    p_rank.add_argument("--model", default="claude-sonnet-4-20250514", help="Model for ranking")
    p_rank.add_argument("--workers", type=int, default=3, help="Parallel API workers")
    p_rank.add_argument("--rate-limit", type=float, default=0.2, help="Delay between API calls")
    p_rank.add_argument("--output", type=Path, help="Output directory")

    # costs
    p_costs = subparsers.add_parser("costs", help="Estimate API costs")
    p_costs.add_argument("--batch-size", type=int, default=5)
    p_costs.add_argument("--top", type=int, default=500)
    p_costs.add_argument("--output", type=Path, help="Output directory")

    # pipeline (all stages)
    p_pipe = subparsers.add_parser("pipeline", help="Run full pipeline")
    p_pipe.add_argument("photo_dir", type=Path, help="Directory containing photos")
    p_pipe.add_argument("--min-mp", type=float, default=4.0)
    p_pipe.add_argument("--min-file-size", type=int, default=500000)
    p_pipe.add_argument("--cameras", nargs="+")
    p_pipe.add_argument("--exclude-cameras", nargs="+")
    p_pipe.add_argument("--batch-size", type=int, default=5)
    p_pipe.add_argument("--top", type=int, default=500)
    p_pipe.add_argument("--score-model", default="claude-haiku-4-5-20251001")
    p_pipe.add_argument("--rank-model", default="claude-sonnet-4-20250514")
    p_pipe.add_argument("--workers", type=int, default=4)
    p_pipe.add_argument("--output", type=Path)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Determine output directory
    output_dir = getattr(args, "output", None)
    if not output_dir:
        # Try to find photo_dir from args or from existing output
        photo_dir = getattr(args, "photo_dir", None)
        if photo_dir:
            output_dir = photo_dir / ".photo-scorer"
        else:
            # Look for existing output in current directory
            candidates = list(Path(".").glob("**/.photo-scorer"))
            if candidates:
                output_dir = candidates[0]
            else:
                log.error("No output directory found. Specify --output or provide photo_dir.")
                sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Save photo_dir reference for later stages
    config_file = output_dir / "config.json"
    if hasattr(args, "photo_dir") and args.photo_dir:
        config = {"photo_dir": str(args.photo_dir.resolve())}
        with open(config_file, "w") as f:
            json.dump(config, f)

    if args.command == "scan":
        stage_scan(args.photo_dir, output_dir, workers=args.workers)

    elif args.command == "filter":
        stage_filter(
            output_dir,
            min_mp=args.min_mp,
            min_file_size=args.min_file_size,
            exclude_screenshots=not args.keep_screenshots,
            camera_allowlist=args.cameras,
            camera_blocklist=args.exclude_cameras,
            dedup=not args.no_dedup,
        )

    elif args.command == "score":
        stage_score(
            output_dir,
            batch_size=args.batch_size,
            workers=args.workers,
            model=args.model,
            rate_limit_delay=args.rate_limit,
        )

    elif args.command == "rank":
        stage_rank(
            output_dir,
            top_n=args.top,
            model=args.model,
            workers=args.workers,
            rate_limit_delay=args.rate_limit,
        )

    elif args.command == "costs":
        estimate_costs(output_dir, batch_size=args.batch_size, top_n=args.top)

    elif args.command == "pipeline":
        log.info("=" * 60)
        log.info("STAGE 1: SCAN")
        log.info("=" * 60)
        stage_scan(args.photo_dir, output_dir, workers=args.workers)

        log.info("\n" + "=" * 60)
        log.info("STAGE 2: FILTER")
        log.info("=" * 60)
        stage_filter(
            output_dir,
            min_mp=args.min_mp,
            min_file_size=args.min_file_size,
            camera_allowlist=args.cameras,
            camera_blocklist=args.exclude_cameras,
        )

        log.info("\n" + "=" * 60)
        log.info("COST ESTIMATE")
        log.info("=" * 60)
        estimate_costs(output_dir, batch_size=args.batch_size, top_n=args.top)

        response = input("\nProceed with AI scoring? (y/n): ").strip().lower()
        if response != "y":
            log.info("Stopped before scoring. Run 'score' and 'rank' when ready.")
            sys.exit(0)

        log.info("\n" + "=" * 60)
        log.info("STAGE 3: QUICK AI SCORE")
        log.info("=" * 60)
        stage_score(
            output_dir,
            batch_size=args.batch_size,
            model=args.score_model,
            rate_limit_delay=0.1,
        )

        log.info("\n" + "=" * 60)
        log.info("STAGE 4: DETAILED RANKING")
        log.info("=" * 60)
        stage_rank(
            output_dir,
            top_n=args.top,
            model=args.rank_model,
        )

        log.info("\n" + "=" * 60)
        log.info("PIPELINE COMPLETE")
        log.info("=" * 60)
        log.info(f"Results in: {output_dir}")
        log.info(f"Open {output_dir / '4_ranked.csv'} to review your top photos!")


if __name__ == "__main__":
    main()
