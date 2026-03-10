<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:media="http://search.yahoo.com/mrss/">

  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes" />

  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title><xsl:value-of select="/rss/channel/title" /> — Feed</title>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="" />
        <link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300;400;600&amp;display=swap" rel="stylesheet" />
        <style>
          *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

          body {
            font-family: "Roboto Slab", serif;
            font-weight: 300;
            color: #090909;
            background: #fff;
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
          }

          .wrapper {
            max-width: 40em;
            width: 90%;
            margin: 0 auto;
            padding: 3rem 0 4rem;
          }

          .feed-header {
            margin-bottom: 3rem;
          }

          .feed-header h1 {
            font-size: 1.75rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
          }

          .feed-header h1 a {
            color: #090909;
            text-decoration: none;
            border-bottom: 2px solid #b9cadb;
            transition: border-color 0.15s linear;
          }

          .feed-header h1 a:hover {
            border-bottom-color: #4c81b2;
          }

          .feed-notice {
            font-size: 0.95rem;
            color: #555;
            line-height: 1.6;
            margin-bottom: 1rem;
          }

          .feed-notice strong {
            font-weight: 600;
            color: #090909;
          }

          .feed-notice code {
            font-size: 0.85em;
            background: #f4f4f4;
            padding: 0.15em 0.4em;
            border-radius: 3px;
          }

          .feed-url {
            display: inline-block;
            font-size: 0.85rem;
            color: #555;
            background: #f4f4f4;
            padding: 0.4em 0.75em;
            border-radius: 4px;
            font-family: monospace;
            word-break: break-all;
            margin-top: 0.5rem;
          }

          hr {
            border: 0;
            border-top: 1px solid #e1e1e1;
            margin: 2rem 0;
          }

          .feed-item {
            display: flex;
            gap: 1.25rem;
            align-items: flex-start;
            padding: 1.5rem 0;
            border-bottom: 1px solid #f0f0f0;
          }

          .feed-item:last-child {
            border-bottom: none;
          }

          .feed-item-thumb {
            flex-shrink: 0;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
          }

          .feed-item-content {
            flex: 1;
            min-width: 0;
          }

          .feed-item-title {
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: -0.01em;
            margin-bottom: 0.25rem;
          }

          .feed-item-title a {
            color: #090909;
            text-decoration: none;
            border-bottom: 2px solid transparent;
            transition: border-color 0.15s linear;
          }

          .feed-item-title a:hover {
            border-bottom-color: #4c81b2;
          }

          .feed-item-date {
            font-size: 0.8rem;
            color: #888;
            margin-bottom: 0.4rem;
          }

          .feed-item-desc {
            font-size: 0.9rem;
            color: #444;
            line-height: 1.55;
          }

          .feed-footer {
            text-align: center;
            padding-top: 2rem;
            font-size: 0.85rem;
            color: #888;
          }

          .feed-footer a {
            color: #090909;
            text-decoration: none;
            border-bottom: 2px solid #b9cadb;
            transition: border-color 0.15s linear;
          }

          .feed-footer a:hover {
            border-bottom-color: #4c81b2;
          }

          @media (prefers-color-scheme: dark) {
            body { background: #1d1e20; color: #d1d1d1; }

            .feed-header h1 a { color: #d1d1d1; border-bottom-color: rgba(185, 202, 219, 0.3); }
            .feed-header h1 a:hover { border-bottom-color: rgba(76, 129, 178, 0.7); }

            .feed-notice { color: #999; }
            .feed-notice strong { color: #d1d1d1; }
            .feed-notice code { background: #2a2b2d; color: #d1d1d1; }

            .feed-url { background: #2a2b2d; color: #999; }

            hr { border-top-color: #333; }

            .feed-item { border-bottom-color: #2a2b2d; }
            .feed-item-thumb { }
            .feed-item-title a { color: #d1d1d1; }
            .feed-item-title a:hover { border-bottom-color: rgba(76, 129, 178, 0.7); }
            .feed-item-date { color: #777; }
            .feed-item-desc { color: #999; }

            .feed-footer { color: #666; }
            .feed-footer a { color: #d1d1d1; border-bottom-color: rgba(185, 202, 219, 0.3); }
            .feed-footer a:hover { border-bottom-color: rgba(76, 129, 178, 0.7); }
          }

          @media (max-width: 480px) {
            .feed-item-thumb { width: 60px; height: 60px; }
            .feed-item { gap: 1rem; }
          }
        </style>
      </head>
      <body>
        <div class="wrapper">
          <header class="feed-header">
            <h1>
              <a>
                <xsl:attribute name="href">
                  <xsl:value-of select="/rss/channel/link" />
                </xsl:attribute>
                <xsl:value-of select="/rss/channel/title" />
              </a>
            </h1>
            <p class="feed-notice">
              <strong>You're looking at an RSS feed.</strong>
              Subscribe by copying the URL into your reader of choice.
            </p>
            <span class="feed-url">
              <xsl:value-of select="/rss/channel/atom:link[@rel='self']/@href" />
            </span>
          </header>

          <hr />

          <xsl:for-each select="/rss/channel/item">
            <article class="feed-item">
              <xsl:if test="media:content/@url">
                <img class="feed-item-thumb" loading="lazy">
                  <xsl:attribute name="src">
                    <xsl:value-of select="media:content/@url" />
                  </xsl:attribute>
                  <xsl:attribute name="alt">
                    <xsl:value-of select="title" />
                  </xsl:attribute>
                </img>
              </xsl:if>
              <div class="feed-item-content">
                <h2 class="feed-item-title">
                  <a>
                    <xsl:attribute name="href">
                      <xsl:value-of select="link" />
                    </xsl:attribute>
                    <xsl:value-of select="title" />
                  </a>
                </h2>
                <time class="feed-item-date">
                  <xsl:value-of select="pubDate" />
                </time>
                <xsl:if test="string-length(description) &gt; 0">
                  <p class="feed-item-desc">
                    <xsl:value-of select="description" />
                  </p>
                </xsl:if>
              </div>
            </article>
          </xsl:for-each>

          <footer class="feed-footer">
            <a>
              <xsl:attribute name="href">
                <xsl:value-of select="/rss/channel/link" />
              </xsl:attribute>
              <xsl:value-of select="/rss/channel/title" />
            </a>
          </footer>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
