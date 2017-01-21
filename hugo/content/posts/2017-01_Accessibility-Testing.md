+++
date = "2017-01-21"
draft = false
title = """Broadening horizons with web accessibility, testing and automation (Hugo, Sitemap.xml and Pa11y)"""
slug = "broadening-horizons-in-web-accessibility"
description = ""
keywords = "static,site,content,accessibility,pa11y,travis,ci"
tags = ['Software Development', 'Website']
+++

{{% toc %}} 

When rebuilding my site I wanted to start as simple as possible, put the sledge hammers away and carefully evaluate each decision as things get built up. Not just with the technology stack, but the content too.

In the past, reading through accessability standards like [508](https://www.section508.gov/) and [WCAG](https://www.w3.org/WAI/intro/wcag.php) were daunting and felt like red tape. I have always aspired to having semantic markup, mostly from an clean code and Search Engine Optimization standpoint. True web accessability was always on the back-burner. 

In a recent project at work, I was turned onto [HTML Sniffer](http://squizlabs.github.io/HTML_CodeSniffer/) and the tools that suround it, namely [Pa11y](http://pa11y.org/).  They have not only helped me begin to charter the world of web accessability but have given me a greater appreciation for why it is needed.  They had to be fundamental part of my development toolchain.

### HTML Sniffer bookmarklet

The [bookmarklet](http://squizlabs.github.io/HTML_CodeSniffer/) alone is a great tool for manually testing and learning more about accessiblity standards.  It shows you an interactive view of what needs to be fixed (errors), things to review and possibly resolve (warnings) and helpful guides to get you in the right mindset (notices).

![HTML Sniffer Bookmarklet](/img/html-sniffer-bookmarklet.png)

### Automating testing with Pa11y-ci

For every post or change to the website it isn't feasible to regression test every page.  This is where Pa11y comes in.  It provides a command-line interface and some reporting tools on top of html sniffer.

I evaluated Pa11y dashboard, but in the theme of a static site I didn't want to host it somewhere (runs on Node.js/MongoDb).  I also interested to see what the [Pa11y Sidekick](https://github.com/pa11y/sidekick) project does.  In the meantime, I decided to integrate it into my own build process.

Here is how it works.

1. Continuous integration build kicks off
2. Hugo generates static content along with sitemap.xml of all the pages in the site.
3. Starts up lightweight server with http-server
4. Runs pa11y-ci command pointed at locally hosted sitemap.xml, replacing normal host with localhost.
5. Pa11y executes a headless PhantomJS browswer against all pages in the sitemap and reports any errors.
6. If the command exits with an error, the build fails and no harm, no foul is done to the site.

#### Commands
```bash
# Build site and site map to /public directory

# Install node modules
npm install -g http-server pa11y pa11y-ci

# Start local server against static site files
http-server ./public --silent &

# Run pa11y against sitemap
pa11y-ci --sitemap http://localhost:8080/sitemap.xml \
         --sitemap-find "https://mrmatt.io/" \
         --sitemap-replace "http://localhost:8080/"
```
*The full configuration can be found in the sites [travis-ci config](https://github.com/MrMatt57/MrMatt.io/blob/master/.travis.yml).*

#### Output
Here is an example of what it looks like when an error is thrown.
{{< gallery cols="1" >}}
{{% galleryimage file="/img/pa11y-ci.jpg" thumb="/img/pa11y-ci-thumbnail.jpg" size="1310x418" caption="Pa11y-ci error output" %}}
{{< /gallery >}}

#### Configuration
There are many configuration options outsite of what is available through the pa11y-ci command line.  A
`.pa11yci` can serve as a proxy to the underlying pa11y configuration.  Mine is pretty basic, setting a page timeout limit of 10 seconds and the target standard. I chose WCAG2AA as a strict but good balance for testing rules.  
```json
{
    "defaults": {
        "timeout": 10000,
        "standard": "WCAG2AA"
    }
}
```
*At [one point](https://github.com/MrMatt57/MrMatt.io/commit/597d47e6746dc196aaf5f51b3f648f6d62bbbdb0) I had to disable a rule becuase Disqus comments were injecting a poorly formatted iframe.  I have since remove Discus in favor for static comments.*

### Development Testing
To test locally, I created a Node.js "test" script command to go agains the Hugo hosted site.

```json
{
  "scripts": {
    "test": "pa11y-ci --sitemap http://localhost:3000/sitemap.xml"
  }
}
```

### Conclusion
I know this barely scratchs the surface of accessability testing, but if anything I hope sparks an interest in learning more about it as it has for me.  It also helps serve as a gatekeeper for any not-so-good markup making it into the site.  I think the [Sidekick](https://github.com/pa11y/sidekick) project will bring better reporting and analysis, but for now the bookmarklet and build integration keep me at least a little better tuned in.

{{% galleryinit %}}    