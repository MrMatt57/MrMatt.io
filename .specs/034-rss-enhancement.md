# Spec 034: RSS Feed Enhancement

## Goal

Improve the site's RSS feed with better metadata — author info, a meaningful site description, full post content for feed readers, and proper channel-level metadata.

## Background

Hugo's embedded RSS template has limitations:
- Channel `<description>` is auto-generated as "Recent content on {title}" — not customizable via config
- No `<content:encoded>` element — items only include `.Summary` in `<description>`
- Author info requires `params.author.email` to render `<managingEditor>` and per-item `<author>`

A custom RSS template is needed to address these issues.

## Changes

### 1. Custom RSS template (`layouts/_default/rss.xml`)

Based on Hugo's embedded template with the following enhancements:
- Channel `<description>` uses `site.Params.description` when available
- Adds `<content:encoded>` with full `.Content` for each item
- Includes `<managingEditor>` with author name even without email
- Adds `xmlns:content` namespace declaration for `content:encoded`

### 2. Config updates (`hugo.toml`)

- Add `description` to `[params]` for the site description used in RSS channel

## Test Plan

- [x] `hugo --minify` builds without errors
- [x] `public/index.xml` channel `<description>` contains the custom site description
- [x] `public/index.xml` channel has `<managingEditor>` with author name
- [x] `public/index.xml` items include `<content:encoded>` with full post content
- [x] `public/index.xml` channel has `<language>en-us</language>`
- [x] RSS feed is valid XML
