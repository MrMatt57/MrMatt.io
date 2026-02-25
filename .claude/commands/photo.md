---
allowed-tools: Bash(cp *), Bash(mkdir *), Bash(ls *), Bash(python3 *), Bash(python *), Read, Write, Glob
---

# /photo — Add a photo to the photography gallery

You are adding a new photo to the site's photography section. The user will provide a path to an image file as `$ARGUMENTS`.

## Step 1: Validate the Image

The argument `$ARGUMENTS` should be a path to an image file (`.jpg`, `.jpeg`, `.png`, `.webp`).

- Use the `Read` tool to view the image file. You are a multimodal LLM and can see image contents.
- If the file doesn't exist or isn't an image, tell the user and stop.

## Step 2: Analyze the Image

Look at the image carefully and determine:

1. **Title**: A short, descriptive title (2-5 words, title case). Example: "Harbor Sunset", "Morning Coffee"
2. **Alt text**: A one-sentence description of what's in the image for accessibility. Be specific and descriptive.
3. **Slug**: A kebab-case slug derived from the title. Example: `harbor-sunset`, `morning-coffee`

Tell the user what you see and confirm the title, alt text, and slug before proceeding. Use `AskUserQuestion` if needed.

## Step 3: Extract the Photo Date

Before creating the page bundle, try to extract the original capture date from the image's EXIF metadata.

Run this command to extract the EXIF date (try `python3` first, fall back to `python`):

```bash
python3 -c "
from PIL import Image
from PIL.ExifTags import Base
img = Image.open('$ARGUMENTS')
exif = img.getexif()
dto = exif.get(Base.DateTimeOriginal) or exif.get(Base.DateTime)
if dto: print(dto[:10].replace(':', '-'))
" 2>/dev/null || python -c "
from PIL import Image
from PIL.ExifTags import Base
img = Image.open('$ARGUMENTS')
exif = img.getexif()
dto = exif.get(Base.DateTimeOriginal) or exif.get(Base.DateTime)
if dto: print(dto[:10].replace(':', '-'))
" 2>/dev/null
```

- If the command outputs a date (e.g., `2025-08-10`), use that as the photo date.
- If the command fails or outputs nothing (no EXIF data, no Python/Pillow available), fall back to today's date.

## Step 4: Create the Page Bundle

1. Create the directory: `content/photography/{date}-{slug}/` (using the date from Step 3)
2. Copy the image into the bundle: `content/photography/{date}-{slug}/photo.{ext}` (preserve the original file extension)
3. Create `content/photography/{date}-{slug}/index.md` with this front matter:

```yaml
---
title: "{title}"
date: "{YYYY-MM-DD}"
alt: "{alt text}"
draft: false
---
```

Use the date extracted in Step 3 for both the directory name and the `date` field.

## Step 5: Verify

- Run `ls content/photography/{date}-{slug}/` to confirm both files exist.
- Tell the user the photo has been added and will appear automatically on the home page and at `/photography/`.
- Remind them to run `hugo server -D` to preview if the server isn't already running.
