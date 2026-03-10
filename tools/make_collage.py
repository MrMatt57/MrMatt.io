"""Generate a gallery preview collage from selected photos."""
import os
from PIL import Image

GALLERY = "C:/dev/MrMatt.io/content/photography"
OUTPUT = "C:/dev/MrMatt.io/static/images/gallery-preview.jpg"

# Hand-picked diverse selection for the collage
PICKS = [
    "2023-08-31-rocky-shore-overlook",      # turquoise Caribbean
    "2024-06-18-smoky-mountain-ridges",      # blue mountain ridges
    "2009-08-03-maine-lake-horizon",         # Maine lake
    "2025-03-29-sphere-at-dusk",             # The Sphere
    "2010-08-07-fresh-hop-harvest",          # hops close-up
    "2021-10-15-autumn-lake-reflections",    # autumn lake
    "2020-09-04-rolling-green-fields",       # aerial green
    "2025-07-11-harpers-ferry-confluence",   # river confluence
]

COLS = 4
ROWS = 2
CELL = 400
GAP = 4

width = COLS * CELL + (COLS - 1) * GAP
height = ROWS * CELL + (ROWS - 1) * GAP
collage = Image.new('RGB', (width, height), (20, 20, 20))

for idx, slug in enumerate(PICKS):
    row = idx // COLS
    col = idx % COLS
    x = col * (CELL + GAP)
    y = row * (CELL + GAP)

    photo_path = os.path.join(GALLERY, slug, "photo.jpg")
    if not os.path.exists(photo_path):
        photo_path = os.path.join(GALLERY, slug, "photo.JPG")

    try:
        img = Image.open(photo_path).convert('RGB')
        # Center crop to square
        w, h = img.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        img = img.crop((left, top, left + side, top + side))
        img = img.resize((CELL, CELL), Image.LANCZOS)
        collage.paste(img, (x, y))
    except Exception as e:
        print(f"Error with {slug}: {e}")

collage.save(OUTPUT, 'JPEG', quality=85)
size = os.path.getsize(OUTPUT)
print(f"Saved {OUTPUT} ({size // 1024}KB, {width}x{height})")
