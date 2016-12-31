
+++
date = "2008-12-03"
draft = false
title = """Amazon Cloudfront - Shopping for a CDN?"""
slug = "amazon-cloudfront-c2bb-shopping-for-a-cdn"
tags = ['Software Development', 'Website', 'Performance']
banner = "/images/2014/12/AWS-Logo-Orange3.jpg"
aliases = ['/amazon-cloudfront-c2bb-shopping-for-a-cdn/']
+++

![Cloudfront Amazon Data Centers](http://static.mrmatt57.org/img/amazoncloudfront.jpg)<span id="credits">  
 Location of Amazon Data Centers World-wide. Credit [Werner Vogels](http://www.allthingsdistributed.com/2008/11/amazon_cloudfront.html)</span>

This past month Amazon sent me an early Christmas present, their very own content deliver network (CDN). Adding to their already robust line of -cloud- offerings, Amazon Cloudfront brings edge server routing to the mix. I have been using Amazon S3 for static content delivery since my most recent [hello world](http://mrmatt57.org/2008/01/16/hello-world-new-server-theme-content-collaboration/). Cloudfront takes the highly scalable and redundant S3 and puts it closer to the end user, thus distributing throughput and reducing latency.

When it comes to web development, one of my driving forces is performance. I love seeking out and shaving milliseconds off page loads and network requests. One of the best ways to do this is to put the content as close to the source as possible. Content Delivery Networks do just that. If my viewers are in Asia, I don-t want my server in New York and vise versa. With a CDN data is cached at several geographically optimized locations as needed. When a request comes in, it is routed to the nearest location.

### The quickest route to the Jungle

A good tool to analyze network routing, latency and a bunch of other stuff is [pingplotter](http://www.pingplotter.com/). They have a free version and pro version. The free version works great for my purposes. Internet Control Message Protocol (ICMP) Pings are a lightweight and predictable way to provide insight on latency and network conditions. Here is a comparison of my routes between Amazon Cloudfront and my standard web server.

[![Amazon Cloudfront Pingplotter](http://static.mrmatt57.org/img/pingplotter_thumb.jpg "Amazon Cloudfront Pingplotter")](http://static.mrmatt57.org/img/pingplotter.jpg)

As you can see, with Cloudfront I scream right to Amazons Newark, NJ server as apposed to going through McClean, VA, then ATL, and finally to my server in Dallas, TX.

### How Cloudfront performs in the CDN storm

Pingplotter works great to determine *your* route and latency.

[Just-ping.com](http://just-ping.com/) provides a great way to test your host/cdn from many geographic locations at once.

*Disclaimer: The below analysis was put together to illustrate a general concept. Accuracy and real world conditions will vary.*<link href="//spreadsheets.google.com/client/css/1899949536-trix_main.css" rel="stylesheet" type="text/css"></link><style>.tblGenFixed td {padding:0 3px;overflow:hidden;white-space:normal;letter-spacing:0;word-spacing:0;background-color:#fff;z-index:1;border-top:0px none;border-left:0px none;border-bottom:1px solid #CCC;border-right:1px solid #CCC;} .dn {display:none} .tblGenFixed td.s0 {background-color:white;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;color:#000000;text-decoration:none;text-align:left;vertical-align:bottom;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-right:1px solid black;border-bottom:1px solid black;border-left:1px solid black;} .tblGenFixed td.s2 {background-color:#99cc00;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;color:#4b4b4b;text-decoration:none;text-align:center;vertical-align:bottom;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-right:1px solid black;border-bottom:1px solid black;} .tblGenFixed td.s1 {background-color:white;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;color:#767676;text-decoration:none;text-align:center;vertical-align:bottom;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-right:1px solid black;border-bottom:1px solid black;} .tblGenFixed td.s5 {background-color:white;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:bold;font-style:normal;color:#000000;text-decoration:none;text-align:center;vertical-align:bottom;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-right:1px solid #CCC;border-bottom:1px solid #CCC;} .tblGenFixed td.s3 {background-color:white;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;text-decoration:none;vertical-align:bottom;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-right:1px solid #CCC;border-bottom:1px solid #CCC;} .tblGenFixed td.s4 {background-color:white;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:bold;font-style:normal;color:#000000;text-decoration:none;text-align:left;vertical-align:bottom;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-right:1px solid #CCC;border-bottom:1px solid #CCC;border-left:1px solid #CCC;} </style>

  
<table cellpadding="0" class="tblGenFixed colHead_0"><tr><td class="rShim" style="width:0;"></td><td class="rShim" style="width:184px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim hdn" style="display:none;width:120px;"></td></tr><tr isfrozenrow="true"><td class="hd">.

</td><td style="background-color:#000000;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;color:#ffffff;text-decoration:none;text-align:left;vertical-align:middle;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-top:1px solid black;border-right:1px solid black;border-bottom:1px solid black;border-left:1px solid black;;">Geographic Location</td><td style="background-color:#000000;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;color:#ffffff;text-decoration:none;text-align:center;vertical-align:middle;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-top:1px solid black;border-right:1px solid black;border-bottom:1px solid black;;">Single Web Server</td><td style="background-color:#000000;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;color:#ffffff;text-decoration:none;text-align:center;vertical-align:middle;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-top:1px solid black;border-right:1px solid black;border-bottom:1px solid black;;">Amazon Cloudfront</td><td style="background-color:#000000;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;color:#ffffff;text-decoration:none;text-align:center;vertical-align:middle;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-top:1px solid black;border-right:1px solid black;border-bottom:1px solid black;;">Akamai</td><td style="background-color:#000000;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;color:#ffffff;text-decoration:none;text-align:center;vertical-align:middle;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-top:1px solid black;border-right:1px solid black;border-bottom:1px solid black;;">LimeLight</td><td class="dn" style="background-color:white;font-family:arial,sans,sans-serif;font-size:100.0%;font-weight:normal;font-style:normal;text-decoration:none;vertical-align:middle;white-space:normal;overflow:hidden;text-indent:0px;padding-left:3px;border-top:1px solid #CCC;border-right:1px solid #CCC;border-bottom:1px solid #CCC;;"></td><td class="headerEnd"></td></tr><tr id="sortBar_0"><td class="sortBar"></td><td class="sortBar"></td><td class="sortBar"></td><td class="sortBar"></td><td class="sortBar"></td><td class="sortBar"></td><td class="sortBar" style="display:none;"></td><td class="headerEnd"></td></tr></table><table border="0" cellpadding="0" cellspacing="0" id="tblMain"><tr><td><table border="0" cellpadding="0" cellspacing="0" class="tblGenFixed" id="tblMain_0"><tr><td class="rShim" style="width:0;"></td><td class="rShim" style="width:184px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim hdn" style="display:none;width:120px;"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Florida, U.S.A.</td><td class="s1 ">34.4</td><td class="s2 ">29.4</td><td class="s1 ">36.5</td><td class="s1 ">36.9</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Chicago, U.S.A.</td><td class="s1 ">34.5</td><td class="s1 ">6.6</td><td class="s1 ">19</td><td class="s2 ">1.3</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> San Francisco, U.S.A.</td><td class="s1 ">43.6</td><td class="s1 ">2.2</td><td class="s1 ">3.6</td><td class="s2 ">2</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> New York, U.S.A.</td><td class="s1 ">43.9</td><td class="s2 ">5</td><td class="s1 ">8.9</td><td class="s1 ">6.6</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Santa Clara, U.S.A.</td><td class="s1 ">47.1</td><td class="s1 ">3.9</td><td class="s2 ">2.8</td><td class="s1 ">6.9</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Vancouver, Canada</td><td class="s1 ">73</td><td class="s1 ">52</td><td class="s2 ">4.5</td><td class="s1 ">95.6</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Austin1, U.S.A.</td><td class="s1 ">102.4</td><td class="s1 ">38.1</td><td class="s2 ">5.2</td><td class="s1 ">76.3</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Austin, U.S.A.</td><td class="s1 ">102.7</td><td class="s1 ">38.1</td><td class="s2 ">5.3</td><td class="s1 ">76.4</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> London, United Kingdom</td><td class="s1 ">108</td><td class="s1 ">13.2</td><td class="s1 ">1.8</td><td class="s2 ">1.6</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Amsterdam3, Netherlands</td><td class="s1 ">114.3</td><td class="s1 ">19.9</td><td class="s2 ">0.7</td><td class="s1 ">7.4</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Amsterdam2, Netherlands</td><td class="s1 ">115.8</td><td class="s1 ">20.6</td><td class="s2 ">1.5</td><td class="s1 ">8.1</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Amsterdam, Netherlands</td><td class="s1 ">118.6</td><td class="s1 ">0.9</td><td class="s2 ">0.5</td><td class="s1 ">0.7</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Lille, France</td><td class="s1 ">120.3</td><td class="s2 ">12.9</td><td class="s1 ">14.2</td><td class="s1 ">110.9</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Munchen, Germany</td><td class="s1 ">129.1</td><td class="s2 ">7.6</td><td class="s1 ">10.2</td><td class="s1 ">7.7</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Zurich, Switzerland</td><td class="s1 ">130.8</td><td class="s1 ">10.6</td><td class="s2 ">2.8</td><td class="s1 ">25.7</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Cologne, Germany</td><td class="s1 ">131.8</td><td class="s1 ">9</td><td class="s2 ">5</td><td class="s1 ">20.4</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Groningen, Netherlands</td><td class="s1 ">133</td><td class="s2 ">4.3</td><td class="s1 ">5.7</td><td class="s2 ">4.3</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Copenhagen, Denmark</td><td class="s1 ">137.9</td><td class="s1 ">15.6</td><td class="s2 ">4.1</td><td class="s1 ">25.3</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Antwerp, Belgium</td><td class="s1 ">139.7</td><td class="s1 ">5.5</td><td class="s2 ">4.2</td><td class="s1 ">4.4</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Stockholm, Sweden</td><td class="s1 ">142</td><td class="s1 ">32.7</td><td class="s2 ">5</td><td class="s1 ">23.6</td><td class="s3 dn"></td></tr></table></td></tr><tr><td><table border="0" cellpadding="0" cellspacing="0" class="tblGenFixed" id="tblMain_1"><tr><td class="rShim" style="width:0;"></td><td class="rShim" style="width:184px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim" style="width:81px;"></td><td class="rShim hdn" style="display:none;width:120px;"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Madrid, Spain</td><td class="s1 ">142.4</td><td class="s1 ">45.2</td><td class="s2 ">2.5</td><td class="s1 ">25.1</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Paris, France</td><td class="s1 ">149.9</td><td class="s1 ">8.3</td><td class="s1 ">17.5</td><td class="s2 ">1.4</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Cagliari, Italy</td><td class="s1 ">165.5</td><td class="s1 ">30.1</td><td class="s2 ">29.5</td><td class="s1 ">30.4</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Auckland, New Zealand</td><td class="s1 ">173.7</td><td class="s1 ">159.8</td><td class="s2 ">1.1</td><td class="s1 ">161.4</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Krakow, Poland</td><td class="s1 ">174.1</td><td class="s1 ">31</td><td class="s2 ">8.8</td><td class="s1 ">43.6</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Haifa, Israel</td><td class="s1 ">177.9</td><td class="s1 ">78.1</td><td class="s2 ">0.5</td><td class="s1 ">64.5</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Porto Alegre, Brazil</td><td class="s1 ">179.1</td><td class="s1 ">149.9</td><td class="s2 ">30.2</td><td class="s1 ">169.9</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Nagano, Japan</td><td class="s1 ">185.8</td><td class="s1 ">4.8</td><td class="s1 ">13.1</td><td class="s2 ">4.7</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Sydney, Australia</td><td class="s1 ">204.8</td><td class="s1 ">159.2</td><td class="s2 ">3.3</td><td class="s1 ">166.2</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Hong Kong, China</td><td class="s1 ">206.8</td><td class="s1 ">2.3</td><td class="s2 ">2.2</td><td class="s1 ">65.6</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Melbourne, Australia</td><td class="s1 ">207.6</td><td class="s1 ">177.9</td><td class="s2 ">1.7</td><td class="s1 ">166.6</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Singapore, Singapore</td><td class="s1 ">238.7</td><td class="s1 ">137.1</td><td class="s1 ">13.3</td><td class="s2 ">3.5</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Shanghai, China</td><td class="s1 ">249.1</td><td class="s1 ">153.5</td><td class="s1 ">308.3</td><td class="s2 ">87</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Mumbai, India</td><td class="s1 ">280.3</td><td class="s1 ">259.1</td><td class="s2 ">1.6</td><td class="s1 ">263.5</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s0 "> Johannesburg, South Africa</td><td class="s1 ">304.8</td><td class="s1 ">293.2</td><td class="s2 ">19.3</td><td class="s1 ">274.7</td><td class="s3 dn"></td></tr><tr><td class="hd">.

</td><td class="s4 ">Average (miliseconds)</td><td class="s5 ">144.1</td><td class="s5 ">57.65</td><td class="s5 ">16.98</td><td class="s5 ">59.15</td><td class="dn"></td></tr></table></td></tr></table>[![Amazon Cloudfront](http://static.mrmatt57.org/img/AmazonCloudfront_thumb.png "Amazon Cloudfront")](http://static.mrmatt57.org/img/AmazonCloudfront.png)

### Setting up and configuring Amazon Cloudfront

Setup was [super easy](http://www.labnol.org/internet/setup-content-delivery-network-with-amazon-s3-cloudfront/5446/) with the latest S3 Organizer Firefox Add-on. You can also complete the setup with a [Curl Script](http://docs.amazonwebservices.com/AmazonCloudFront/latest/GettingStartedGuide/index.html?ToolsYouNeed.html).




