+++
date = "2017-01-14"
draft = false
title = """Static Site Caching with a CDN (Hugo, S3 and KeyCDN)"""
slug = "static-site-content-caching"
description = ""
keywords = "static,site,content,caching"
tags = ['Software Development', 'Website']
+++
I am really enjoying the [switch](/posts/website-update-2016/) to a static Hugo site.  One of the main benefits is not having to run a server to host it.  That also means no `.htacess` or `web.config` files to set headers or caching policies.  With a traditional site "static" assets can be safely cached and dynamic content will be served fresh each request.  Now that the the whole site is static, we need to separate how things are cached.

This sites [toolchain](/stack/) uses s3cmd sync to deploy files to an Amazon S3 bucket that I use as an orgin for KeyCDN.  In most CDNs the only way to vary cache control headers is to take the value from the orgin.  So this means setting the headers in S3.  To do this, you can use s3cmd's to vary headers based on file types.  In my current implemenation I am considering `html`, `xml`, and `json` files that may change and should not be browser cached.  Everything else I am caching for 24 hours.

### Static files to cache
```
s3cmd sync --delete-removed \
    --exclude '.git/*' \
    --rexclude "^(.*\.((html|xml|json)$))*$" \
    --add-header="Cache-Control: max-age=1440" \
    --acl-public \
    --preserve \
    --no-mime-magic \
    --guess-mime-type \
    --recursive \
    public/ \
    s3://BUCKETNAME/     
```
### No-Cache files
```
s3cmd sync --delete-removed \
    --exclude '*' \
    --rinclude "^(.*\.((html|xml|json)$))*$" \
    --add-header="Cache-Control: no-cache, no-store, must-revalidate" \
    --add-header="Pragma: no-cache" \
    --add-header="Expires: 0" \
    --acl-public \
    --preserve \
    --no-mime-magic \
    --guess-mime-type \
    --recursive \
    public/ \
    s3://BUCKETNAME/   
```
The full source can be found in the [travis-ci config](https://github.com/MrMatt57/MrMatt.io/blob/master/.travis.yml) and the [deploy.sh](https://github.com/MrMatt57/MrMatt.io/blob/master/deploy.sh) script on Github.
### CDN settings
In your CDN set your Expire setting to honor your orgin's servers header.

Now static files; `css`, `js`, `fonts` and `images` are browser cached and only the main page is served for each request.
{{< gallery cols="1" >}}
{{% galleryimage file="/img/CacheProfile.jpg" thumb="/img/CacheProfile-thumbnail.jpg" size="1162x159" caption="Personal Best Liberty Bass" %}}
{{< /gallery >}}
### Bonus
Purge you KeyCDN cache with each deployment with an API call
```
curl "https://api.keycdn.com/zones/purge/{ID}.json" -u {KeyCDNToken}:
```
{{% galleryinit %}}    