
+++
date = "2008-01-29"
draft = false
title = """Webmasters: Don't forget about DNS..."""
slug = "webmasters-dont-forget-about-dns"
tags = ['Software Development']
banner = "/images/2014/12/dns.png"
aliases = ['/webmasters-dont-forget-about-dns/']
+++


![DNS Error](http://static.mrmatt57.org/img/dns_error.jpg)

*<quote>-A study conducted by IDC determined that only 41% of small companies and 35% of large organizations monitor Internet DNS response times.-</quote>*

-DNS failures account for as much as 29% of system downtime costing companies millions of dollars.-

The Domain Name System (DNS) is arguably the single most important part of the internet. Just think: If websites only had a numerical lookup- our Rolodex-s would be massively confusing. Why don-t webmasters/hosts treat DNS with the same priority? DNS servers carry such a high importance. Without them, no internet. They are often the [target](http://en.wikipedia.org/wiki/DNS_Backbone_DDoS_Attacks) of massive Distributed Denial of Service (DDOS) attacks. Are your DNS records configured properly and secure?

**DNS Performance & Security Enhancements**

Most of the Internet is run on Berkeley Internet Name Domain (BIND) based servers. There have been a lot of failed attempts to create a BIND alternative (GnuDIP, MooDNS, Dents, OakDNS, CustomDNS and dproxy). A couple of active projects are PowerDNS, NSD, djdns and MaraDNS. All boast better security and performance improvements in different environments. If you are hosting your own DNS, you owe it to yourself/network to [review your options](http://en.wikipedia.org/wiki/Comparison_of_DNS_server_software).

<div style="float: right;">![Anycast](http://static.mrmatt57.org/img/ip_anycast.gif)</div>Another performance and security innovation that is becoming increasing popular across many stateless services on the internet is IP [anycast networks](http://en.wikipedia.org/wiki/Anycast). It is a network addressing and routing scheme where data is routed to the nearest or best destination. It helps provide higher availability and load balancing. Many of the TLD servers name servers are already running on anycast networks. In fact these servers survived the massive [DDOS attack last year](http://blog.icann.org/?p=37). UtraDNS, Netriplex and DNS Made Easy are among the few providers to deliver DNS over an anycast network. I imagine many more fill follow suit.

**Minimizing down-time with TTL**

Most of us have been effected by DNS outages. There is not much you can do when a record gets out of whack or a server goes down. You can flush your local cache, maybe even try to resolve against a different server, but the only real cure is time. That is because each DNS record has a setting called Time to Live (TTL). This is how long the record should persist. Once this time expires, a new record is fetched. Also, if the servers aren-t available, you don-t get a record.

A good rule of thumb when setting your TTL is to use your average visitor time. For example, if the average visitor spends five minutes on your site (check your analytics), you should set your TTL to 300 (in seconds). The idea is; in the event of a failover, it has the least impact on visitors and doesn-t require a performance hit for numerous DNS lookups. Some DNS providers won-t allow a TTL setting this low. A lower TTL mean more DNS queries and ultimately more expense.

**Should I outsource my DNS?**

A lot of network architects will actually advise webmasters to host their own DNS records. The route/latency will be the same as HTTP traffic, thus making lookup time approximately the same as a web requests. It also reduces the risk of outages caused solely by DNS. If they are hosted on the same subnet, routing glitches are minimized. If they are on the same server as your website, it will even further reduce the risk of DNS only outages.

However, if you don-t have the time/experience to monitor, review logs and maintain your DNS servers, outsourcing is a great option. But beware, all DNS networks/servers are not created equally. If you are hosting your records with a budget registrar, chances are you are at risk. They are often the target of DDOS attacks, endure lengthy outages/maintenance and have congested networks. Security by obscurity; in the last two years I have had clients with DNS outages lasting greater than 6 hours at two of the major registrars.

The Cadillac of DNS currently is [NeuStar-s UltraDNS](http://www.neustarultraservices.biz/). They have a globally redundant/optimized network with proprietary DNS software powered by Oracle replication. However, they charge by the query, so if you have a busy site, it will get expensive in a hurry. Another high-end service is [Netriplex](http://www.netriplex.com/solutions/critical_dns/). For small to mid size company-s the only way to afford either of these services is to increase unfortunately to your TTL.

<div style="float: right;">[![DNS Made Easy](http://static.mrmatt57.org/img/dns-made-easy-icon.gif)](http://www.dnsmadeeasy.com/u/39743)</div>The best budget priced service with high-end features/support I have found so far is [DNS Made Easy](http://www.dnsmadeeasy.com/u/39743). They have a great feature-set, excellent and knowledgeable staff all at a great price.

**Search Engine Optimization (SEO)**

There have been [reports](http://www.askdavetaylor.com/can_dns_changes_affect_search_engine_results_placement_serp.html) of falling Search Engine Results Placements (SERPs) taking drastic drops soon after a DNS change. Changing just the IP address has not caused any notable problems. It is domain contact and name server changes that have have caused the speculation. Many claim it resets the sites Google -trust points-. There are many influences on SERPs and SEO is always a moving target, so take this warning with a grain for salt. But I thought it was worth mentioning.

**For More Information**

DNS Wiki - [http://en.wikipedia.org/wiki/Domain_name_system](http://en.wikipedia.org/wiki/Domain_name_system)  
 DNS Forum - [http://member.dnsstuff.com/forums/](http://member.dnsstuff.com/forums/)  
 Web-based DNS Tools - [http://www.dnstools.com/](http://www.dnstools.com/)  
 DNS Surveys - [http://www.seoconsultants.com/tools/dns/surveys/](http://www.seoconsultants.com/tools/dns/surveys/)




