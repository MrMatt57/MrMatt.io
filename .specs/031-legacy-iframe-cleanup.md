# Spec 031: Legacy Iframe and HTTP Link Cleanup

## Problem

Old posts from 2007-2010 embed content over plain HTTP using iframes, Flash embeds, and
Amazon affiliate widgets. These are a mix of dead services (Amazon affiliate iframes,
Flash embeds) and upgradeable URLs (Google Maps, Flickr, YouTube, Wikipedia, archive.org).

Mixed content (HTTP resources on an HTTPS page) is blocked by modern browsers, so these
embeds either fail silently or trigger security warnings.

## Solution

1. **Remove dead Amazon affiliate iframes** (`http://rcm.amazon.com/e/cm?...`) -- service
   is long dead.
2. **Remove dead Amazon tracking pixels** (`http://www.assoc-amazon.com/e/ir?...`) --
   1x1 invisible images for affiliate tracking, no longer functional.
3. **Remove dead Flash embeds** (`<embed ... src="http://static.mrmatt57.org/..."`) --
   Flash is dead and the media server is gone.
4. **Upgrade Google Maps iframe** from `http://maps.google.com` to
   `https://maps.google.com`.
5. **Upgrade plain HTTP links** to HTTPS for sites that support it: Flickr, YouTube,
   Wikipedia, archive.org, Amazon product pages, moo.com, GitHub Pages sites, etc.
6. **Leave alone**: URLs inside code blocks, URLs that are part of technical discussion
   about HTTP/DNS, and URLs to sites that are truly dead and cannot be verified.

## Files Changed

- `content/posts/2008-07_remote-control-extender-convert-your-ir-remote-to-rf.md`
- `content/posts/2008-02_movie-into-the-wild.md`
- `content/posts/2008-01_voicemail-funny-it-momment.md`
- `content/posts/2009-08_canoe-camping-penobscot-river-maine.md`
- `content/posts/2010-05_time-lapse-chdk.md`
- `content/posts/2007-08_building-a-lipo-charging-station.md`
- `content/posts/2007-12_december-is-for-cynics.md`
- `content/posts/2007-12_live-music.md`
- `content/posts/2007-12_how-projects-really-work.md`
- `content/posts/2007-12_my-rig.md`
- `content/posts/2007-12_1994-honda-accord.md`
- `content/posts/2007-10_james-bond-style-usb-key-ironkey.md`
- `content/posts/2008-01_hello-world-new-server-theme-content-collaboration.md`
- `content/posts/2008-01_webmasters-dont-forget-about-dns.md`
- `content/posts/2008-01_voicemail-funny-it-momment.md`
- `content/posts/2008-01_qos-for-soho-voip-solved-tomato-firmware.md`
- `content/posts/2008-02_old-technology-meets-new-xbox-hd-dvd-asus-eee.md`
- `content/posts/2008-02_rc-airplane-flight-boxfield-bag.md`
- `content/posts/2008-02_thank-you-microsoft-vista-sp1-is-nice.md`
- `content/posts/2008-03_printing-on-paper-is-a-bad-habit.md`
- `content/posts/2008-04_business-cards-moo-cards.md`
- `content/posts/2008-04_css-naked-day.md`
- `content/posts/2008-12_amazon-cloudfront-c2bb-shopping-for-a-cdn.md`
- `content/posts/2009-01_honda-slow-window-syndrome.md`
- `content/posts/2009-04_hike-loch-raven-reservoir-w-iphone-3g-gps.md`
- `content/posts/2017-01_Accessibility-Testing.md`

## Test Plan

- [x] No `<iframe` tags with `http://` src attributes remain in content
- [x] No `<embed` tags with `http://` src attributes remain in content
- [x] No Amazon affiliate iframes remain (`rcm.amazon.com`)
- [x] No Amazon tracking pixels remain (`assoc-amazon.com`)
- [x] Google Maps iframe upgraded to HTTPS
- [x] Flickr links upgraded to HTTPS
- [x] YouTube links upgraded to HTTPS
- [x] Wikipedia links upgraded to HTTPS
- [x] archive.org links upgraded to HTTPS
- [x] Code blocks left untouched
- [x] Hugo builds successfully with `hugo --minify`
