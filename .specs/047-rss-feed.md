# 047: Styled RSS Feed with Image Thumbnails

**Branch**: `feature/rss-feed`
**Created**: 2026-03-09

## Summary

Add a polished RSS feed experience: a styled RSS page (XSLT) that renders beautifully in browsers instead of raw XML, image thumbnails for each post via `<media:content>` tags using cover/OG images, and a subtle "Feed" link in the site footer matching the existing link style.

## Requirements

- Add RSS text link ("Feed") to the footer, matching existing inline link style (no icons, no orange badges)
- Override PaperMod's RSS template to include `<media:content>` tags with post cover images
- Fall back to site default image (`/images/MattWalker-avatar.png`) for posts without cover images
- Create an XSL stylesheet that transforms the RSS XML into a styled HTML page when viewed in a browser
- XSL page must match site typography (Roboto Slab), color scheme, and minimal aesthetic
- XSL page should include a brief explanation of what RSS is and how to subscribe
- Support dark mode in the XSL stylesheet via `prefers-color-scheme`
- Show post thumbnails in the styled feed page when available

## Design

### RSS Template (`layouts/_default/rss.xml`)
- Copy PaperMod's template, add `xmlns:media` namespace
- Add `<?xml-stylesheet?>` processing instruction pointing to `/rss.xsl`
- For each item, add `<media:content>` with the post's `cover.image` (or site default)
- Use `absURL` to ensure full URLs for images

### XSL Stylesheet (`static/rss.xsl`)
- Transforms RSS 2.0 XML into clean HTML
- Self-contained: all CSS is inlined (since it renders as a standalone page)
- Typography: Roboto Slab from Google Fonts (self-hosted fonts won't work here since XSL generates its own document)
- Colors: match site (#090909 text, #fff background, #b9cadb accent, #4c81b2 hover)
- Dark mode: `prefers-color-scheme: dark` media query with site's dark palette
- Layout: centered content, max-width ~40em, generous whitespace
- Header: site title + subtitle explaining "This is an RSS feed"
- Each post: title (linked), date, description, thumbnail if available
- Footer: link back to site

### Footer Link
- Add "Feed" as a text link to `/index.xml` in the footer's `<ul class="footer-links">`
- Placed after "Creative Commons" as the last item

## Files to Modify

| File | Change |
|------|--------|
| `layouts/_default/rss.xml` | Updated — added XSL stylesheet reference, media namespace, and media:content tags |
| `static/rss.xsl` | New file — XSL stylesheet for browser-rendered feed page |
| `layouts/partials/footer.html` | Add "Feed" link to footer-links list |

## Test Plan

- [x] Hugo builds with no errors (`hugo --minify`)
- [ ] Site renders correctly on localhost (`hugo server -D`)
- [x] RSS feed at `/index.xml` is valid XML with media:content tags
- [x] RSS feed includes XSL stylesheet reference
- [ ] Viewing `/index.xml` in a browser shows styled HTML page (not raw XML)
- [ ] Footer shows "Feed" link styled consistently with other links
- [x] Posts with cover images show thumbnails in feed
- [x] Posts without cover images fall back to default site image
- [ ] Dark mode works on the styled feed page
