"""
Batch import photos into Hugo gallery page bundles.
Extracts EXIF dates, creates directories, copies photos.
Outputs manifest.json for AI description step.
"""
import os
import sys
import json
import shutil
import re
from PIL import Image
from PIL.ExifTags import Base

SRC_DIR = "F:/Photos/pipeline/gallery_picks_website"
GALLERY_DIR = "C:/dev/MrMatt.io/content/photography"

def extract_exif_date(path):
    """Extract capture date from EXIF data."""
    try:
        img = Image.open(path)
        exif = img.getexif()
        dto = exif.get(Base.DateTimeOriginal) or exif.get(Base.DateTime)
        if dto:
            return dto[:10].replace(':', '-')
    except:
        pass
    return None

def date_from_filename(filename):
    """Extract date from Google Takeout filename patterns."""
    # PXL_20250418_125218047 -> 2025-04-18
    m = re.search(r'PXL_(\d{4})(\d{2})(\d{2})_', filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    # IMG_20190511_140547 -> 2019-05-11
    m = re.search(r'IMG_(\d{4})(\d{2})(\d{2})_', filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    # 20090803-IMG_0374 -> 2009-08-03
    m = re.search(r'(\d{4})(\d{2})(\d{2})-IMG_', filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    # DJI_0013 -> no date, use album
    # 4747954836 (Flickr IDs) -> no date
    # IMG_0302 -> no date from filename

    # Photos_from_YYYY -> use year
    m = re.search(r'Photos_from_(\d{4})__', filename)
    if m:
        return f"{m.group(1)}-06-15"  # mid-year fallback

    # Maine_2009__ -> 2009
    m = re.search(r'Maine_(\d{4})__', filename)
    if m:
        return f"{m.group(1)}-08-03"  # August for Maine trips

    # Cruise_2023__ -> 2023
    m = re.search(r'Cruise_(\d{4})__', filename)
    if m:
        return f"{m.group(1)}-08-31"

    # Cruise_2019__ -> 2019
    m = re.search(r'Cruise_(\d{4})__', filename)
    if m:
        return f"{m.group(1)}-05-11"

    # Luray_2022__
    m = re.search(r'Luray_(\d{4})_', filename)
    if m:
        return f"{m.group(1)}-04-16"

    # Smoky_s_2024__
    m = re.search(r'Smoky_s_(\d{4})__', filename)
    if m:
        return f"{m.group(1)}-06-18"

    # Dead_and_Co_Sphere_2025__
    m = re.search(r'Sphere_(\d{4})', filename)
    if m:
        return f"{m.group(1)}-03-30"

    # Gartner_2022__
    m = re.search(r'Gartner_(\d{4})__', filename)
    if m:
        return f"{m.group(1)}-08-23"

    # DoigReunion -> 2017
    if 'DoigReunion' in filename:
        return "2017-08-12"

    return None

def generate_slug_placeholder(filename):
    """Generate a basic slug from filename. Will be replaced by AI."""
    # Remove album prefix and extension
    name = filename.split('__', 1)[-1] if '__' in filename else filename
    name = os.path.splitext(name)[0]
    # Clean up
    name = re.sub(r'[^a-zA-Z0-9]', '-', name.lower())
    name = re.sub(r'-+', '-', name).strip('-')
    return name[:40]

def main():
    files = sorted([f for f in os.listdir(SRC_DIR)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])

    print(f"Found {len(files)} photos to import")

    manifest = []

    for i, filename in enumerate(files):
        src_path = os.path.join(SRC_DIR, filename)

        # Get date
        date = extract_exif_date(src_path) or date_from_filename(filename)
        if not date:
            date = "2020-01-01"  # absolute fallback
            print(f"  WARNING: no date for {filename}, using fallback")

        # Generate temp slug (will be replaced)
        slug = generate_slug_placeholder(filename)

        # Bundle dir
        bundle_name = f"{date}-{slug}"
        bundle_dir = os.path.join(GALLERY_DIR, bundle_name)

        # Handle duplicate dates/slugs
        if os.path.exists(bundle_dir):
            bundle_name = f"{date}-{slug}-{i}"
            bundle_dir = os.path.join(GALLERY_DIR, bundle_name)

        os.makedirs(bundle_dir, exist_ok=True)

        # Copy photo
        ext = os.path.splitext(filename)[1].lower()
        dst_photo = os.path.join(bundle_dir, f"photo{ext}")
        shutil.copy2(src_path, dst_photo)

        # Create placeholder index.md (to be filled by AI)
        index_path = os.path.join(bundle_dir, "index.md")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f'---\ntitle: "PENDING"\ndate: "{date}"\nalt: "PENDING"\ndescription: "PENDING"\ndraft: false\n---\n')

        manifest.append({
            'index': i,
            'filename': filename,
            'date': date,
            'bundle_name': bundle_name,
            'bundle_dir': bundle_dir.replace('\\', '/'),
            'photo_path': dst_photo.replace('\\', '/'),
            'index_path': index_path.replace('\\', '/'),
        })

        print(f"  [{i+1:2d}/{len(files)}] {date} {filename[:60]}")

    # Write manifest
    manifest_path = os.path.join(GALLERY_DIR, '_batch_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\nCreated {len(manifest)} page bundles")
    print(f"Manifest: {manifest_path}")
    print(f"\nNext: AI agents will read photos and fill in title/alt/description")

if __name__ == '__main__':
    main()
