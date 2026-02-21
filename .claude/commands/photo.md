---
allowed-tools: Bash(cp *), Bash(mkdir *), Bash(ls *), Read, Write, Glob
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

## Step 3: Create the Page Bundle

1. Create the directory: `content/photography/{slug}/`
2. Copy the image into the bundle: `content/photography/{slug}/photo.{ext}` (preserve the original file extension)
3. Create `content/photography/{slug}/index.md` with this front matter:

```yaml
---
title: "{title}"
date: "{YYYY-MM-DD}"
alt: "{alt text}"
draft: false
---
```

Use today's date for the `date` field.

## Step 4: Verify

- Run `ls content/photography/{slug}/` to confirm both files exist.
- Tell the user the photo has been added and will appear automatically on the home page and at `/photography/`.
- Remind them to run `hugo server -D` to preview if the server isn't already running.
