---
date: "2008-12-03"
draft: false
title: "Amazon Cloudfront - Shopping for a CDN?"
slug: "amazon-cloudfront-c2bb-shopping-for-a-cdn"
tags:
  - "Software Development"
  - "Website"
  - "Performance"
aliases:
  - /amazon-cloudfront-c2bb-shopping-for-a-cdn/
---
![Cloudfront Amazon Data Centers](/img/amazoncloudfront.jpg)

*Location of Amazon Data Centers World-wide. Credit [Werner Vogels](http://www.allthingsdistributed.com/2008/11/amazon_cloudfront.html)*

This past month Amazon sent me an early Christmas present, their very own content deliver network (CDN). Adding to their already robust line of -cloud- offerings, Amazon Cloudfront brings edge server routing to the mix. I have been using Amazon S3 for static content delivery since my most recent [hello world](/posts/hello-world-new-server-theme-content-collaboration/). Cloudfront takes the highly scalable and redundant S3 and puts it closer to the end user, thus distributing throughput and reducing latency.

When it comes to web development, one of my driving forces is performance. I love seeking out and shaving milliseconds off page loads and network requests. One of the best ways to do this is to put the content as close to the source as possible. Content Delivery Networks do just that. If my viewers are in Asia, I don-t want my server in New York and vise versa. With a CDN data is cached at several geographically optimized locations as needed. When a request comes in, it is routed to the nearest location.

### The quickest route to the Jungle

A good tool to analyze network routing, latency and a bunch of other stuff is [pingplotter](http://www.pingplotter.com/). They have a free version and pro version. The free version works great for my purposes. Internet Control Message Protocol (ICMP) Pings are a lightweight and predictable way to provide insight on latency and network conditions. Here is a comparison of my routes between Amazon Cloudfront and my standard web server.

[![Amazon Cloudfront Pingplotter](/img/pingplotter_thumb.jpg "Amazon Cloudfront Pingplotter")](/img/pingplotter.jpg)

As you can see, with Cloudfront I scream right to Amazons Newark, NJ server as apposed to going through McClean, VA, then ATL, and finally to my server in Dallas, TX.

### How Cloudfront performs in the CDN storm

Pingplotter works great to determine *your* route and latency.

[Just-ping.com](http://just-ping.com/) provides a great way to test your host/cdn from many geographic locations at once.

*Disclaimer: The below analysis was put together to illustrate a general concept. Accuracy and real world conditions will vary.*

| Geographic Location | Single Web Server | Amazon Cloudfront | Akamai | LimeLight |
|---|---|---|---|---|
| Florida, U.S.A. | 34.4 | **29.4** | 36.5 | 36.9 |
| Chicago, U.S.A. | 34.5 | 6.6 | 19 | **1.3** |
| San Francisco, U.S.A. | 43.6 | 2.2 | 3.6 | **2** |
| New York, U.S.A. | 43.9 | **5** | 8.9 | 6.6 |
| Santa Clara, U.S.A. | 47.1 | 3.9 | **2.8** | 6.9 |
| Vancouver, Canada | 73 | 52 | **4.5** | 95.6 |
| Austin1, U.S.A. | 102.4 | 38.1 | **5.2** | 76.3 |
| Austin, U.S.A. | 102.7 | 38.1 | **5.3** | 76.4 |
| London, United Kingdom | 108 | 13.2 | 1.8 | **1.6** |
| Amsterdam3, Netherlands | 114.3 | 19.9 | **0.7** | 7.4 |
| Amsterdam2, Netherlands | 115.8 | 20.6 | **1.5** | 8.1 |
| Amsterdam, Netherlands | 118.6 | 0.9 | **0.5** | 0.7 |
| Lille, France | 120.3 | **12.9** | 14.2 | 110.9 |
| Munchen, Germany | 129.1 | **7.6** | 10.2 | 7.7 |
| Zurich, Switzerland | 130.8 | 10.6 | **2.8** | 25.7 |
| Cologne, Germany | 131.8 | 9 | **5** | 20.4 |
| Groningen, Netherlands | 133 | **4.3** | 5.7 | **4.3** |
| Copenhagen, Denmark | 137.9 | 15.6 | **4.1** | 25.3 |
| Antwerp, Belgium | 139.7 | 5.5 | **4.2** | 4.4 |
| Stockholm, Sweden | 142 | 32.7 | **5** | 23.6 |
| Madrid, Spain | 142.4 | 45.2 | **2.5** | 25.1 |
| Paris, France | 149.9 | 8.3 | 17.5 | **1.4** |
| Cagliari, Italy | 165.5 | 30.1 | **29.5** | 30.4 |
| Auckland, New Zealand | 173.7 | 159.8 | **1.1** | 161.4 |
| Krakow, Poland | 174.1 | 31 | **8.8** | 43.6 |
| Haifa, Israel | 177.9 | 78.1 | **0.5** | 64.5 |
| Porto Alegre, Brazil | 179.1 | 149.9 | **30.2** | 169.9 |
| Nagano, Japan | 185.8 | 4.8 | 13.1 | **4.7** |
| Sydney, Australia | 204.8 | 159.2 | **3.3** | 166.2 |
| Hong Kong, China | 206.8 | 2.3 | **2.2** | 65.6 |
| Melbourne, Australia | 207.6 | 177.9 | **1.7** | 166.6 |
| Singapore, Singapore | 238.7 | 137.1 | 13.3 | **3.5** |
| Shanghai, China | 249.1 | 153.5 | 308.3 | **87** |
| Mumbai, India | 280.3 | 259.1 | **1.6** | 263.5 |
| Johannesburg, South Africa | 304.8 | 293.2 | **19.3** | 274.7 |
| **Average (ms)** | **144.1** | **57.65** | **16.98** | **59.15** |

[![Amazon Cloudfront](/img/AmazonCloudfront_thumb.png "Amazon Cloudfront")](/img/AmazonCloudfront.png)

### Setting up and configuring Amazon Cloudfront

Setup was [super easy](http://www.labnol.org/internet/setup-content-delivery-network-with-amazon-s3-cloudfront/5446/) with the latest S3 Organizer Firefox Add-on. You can also complete the setup with a [Curl Script](http://docs.amazonwebservices.com/AmazonCloudFront/latest/GettingStartedGuide/index.html?ToolsYouNeed.html).

