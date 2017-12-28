
+++
date = "2008-01-24"
draft = false
title = """QOS for SOHO VOIP Solved, Tomato Firmware"""
slug = "qos-for-soho-voip-solved-tomato-firmware"
tags = []
banner = "/images/2014/12/wires-1.jpg"
aliases = ['/qos-for-soho-voip-solved-tomato-firmware/']
+++

Whoa, easy on the Acronyms-.

One of my biggest challenges setting up my Small Office and Home Office (SOHO) Voice Over IP (VOIP) network has been related to Quality of Service (QOS). Have you ever been on a VOIP call and had people complain that you sound like you are in a tin can? Most residential broadband connections have a capped upload speed. If your internet habits are anything like mine, at times you can max your connection in both directions. Creating room for voice traffic can be a challenge. Current voice coding algorithms require 16 - 80 kbps for a single voice connection. If the throughput is not available or the latency is too high (> 250ms one way), voice quality will suffer or with some clients completely drop. A lot of routers/switches claim to come with QOS, most of them are pretty crude and require bandwidth/node fixing. There are also a number of plug and play solutions claiming to clear up the problem. They are generally expensive and do not offer custom traffic shaping.


## The Solution

<div style="float: right;">[![WRT54G](http://static.mrmatt57.org/img/wrtg_thumb.gif "WRT54G")](http://static.mrmatt57.org/img/wrtg.gif)</div>A couple years ago Linksys went open source on one of their most popular broadband routers firmware, the WRT54G. There have been a number of different firmware releases. I tried everything I could get my hands on. The one that stood out from the pack with both features and usability was [Tomato by Jonathan Zarate](http://www.polarcloud.com/tomato) It has a number of enhancements from the default firmware, the most notable being:

- AJAX enabled interface
- Sweet [bandwidth usage monitor](http://www.polarcloud.com/v/scbwm.htm)
- Advanced QOS
- [Access Restrictions](http://www.polarcloud.com/v/screst.htm)
- New wireless features such as WDS and [wireless client modes](http://www.polarcloud.com/v/scclient.htm)
- Raises the limits on maximum connections for P2P
- Allows you to run your custom scripts or telnet/ssh in and do all sorts of things like re-program the SES/AOSS button
- Adds wireless site survey to see your wifi neighbors


## Installing Tomato

Jut a couple of notes here. Make sure you check your device-s hardware version number. Unfortunately you can-t walk into your local computer superstore and pick one up anymore, v5+ hardware is not supported. If your WRT54G is a couple of years old, chances are you have one of the [supported devices](http://www.polarcloud.com/tomatofaq#what_will_this_run_on). Installation is pretty straight forward, just flash it with the [latest firmware](http://www.polarcloud.com/firmware). This will wipe your settings, so make sure you grab screenshots/write them down before you get started. The default GUI username is -admin- or -root- (username is required), ssh and telnet username is always -root-, and the default password is -admin-.


## Configuring Basic Firewall Functions

This step will vary depending on your ISP, network configuration and VOIP provider. WAN/LAN configuration is straight forward and should be configured the same as it was in your default firmware. Port Forwading depends on what VOIP gateway hardware you have. The standard signaling port for SIP is 5060-5063 UDP and RTP voice travels on 16384 - 16482 UDP (some phones may need ranges up to 10000 - 20000 UDP). I have setup a [Trixbox](http://www.trixbox.org/) PBX locally for handling calls (thinking of trying asterisk on linode). Forwarding the above ports allows me to authenticate a trunk with my provider, voip your life. Make a couple of test calls over a quiet internet connection to insure everything is working. Audio in both directions should be without glitch.


## Setting up Quality of Service

With tomato you can classify data by IP or Mac Address, Source/Destination Port and how much data is being transfered. You will want to adjust these setting to match your usage. For example, I am digesting a shoutcast stream 24/7 and have set 8000-8006 to highest priority to avoid interruptions.

### Enabling QOS

- Log-in to your router
- Open the QOS > Basic Settings Menu
- Check -Enable QOS-

<div>![Enabling QOS](http://static.mrmatt57.org/img/QOS_enabled.gif)  
*Note: if you use applications that do a lot of ACKnowledgment requests (BitTorrent), you might want to consider turning this option off*</div>  
### Outbound Rate / Limit

- Max Bandwidth: this is your maximum outbound (upload) bandwidth. You can determine your speed at [DSL Reports](http://www.dslreports.com/stest), [SpeakEasy](http://www.speakeasy.net/speedtest/) or [Speedtest.net](http://www.speedtest.net/). A hack to ensure you have enough overhead is to intentionally low-ball this number. You would only want to do this if absolutely necessary as you would not be fully utilizing your bandwidth.

<div>![QOS Outbound Rate / Limit](http://static.mrmatt57.org/img/QOS_Outbound_Limit.gif)  
*Note: These are the settings that work for me,   
you will most likely have to tweak them*</div>  
### Inbound Limit

- Max Bandwidth: Use the inbound (download) results from your tests above.

<div>![QOS Inbound Limit](http://static.mrmatt57.org/img/QOS_Inbound_limit.gif)  
*Note: These are the settings that work for me,   
you will most likely have to tweak them*</div>  
### Classifications

- Open the QOS > Classifications Menu
- Add Entry for Any Address, TCP/UDP, Src or Dst 5060 (your SIP Signaling port), Highest Priority
- Add Entry for Any Address, TCP/UDP, Src or Dst 16384-16482 (your RTP Voice port range), Highest Priority
- Move them to the top of the list
- *Note: If you have any other traffic (P2P) on ports these ports, you should try the SIP I7-Filter.*
- *Note: Another solution is to setup a QOS classification for the IP/Mac addresss of your standalone VoIP phones or adapters if they are connecting to a trunk over the internet*
- *Note: Some phones require a different RTP range for example, my Linksys SPA942?s call for 10,000 - 20,000 UDP. Check with you phone or ATA documentation to determine the actual RTP port range.*

[![QOS Classifications](http://static.mrmatt57.org/img/QOS_Classifications.gif "QOS Classifications")](http://static.mrmatt57.org/img/QOS_Classifications_full.gif)


## Testing, Testing, Testing

Now that you have established a baseline for your QOS, it-s time to see if it works. First, if possible test on a clean connection to make sure nothing is out of whack. Now for the fun part; max your connection out. Start your P2P, BitTorrent, Large file Uploads, Video Streaming and anything else you can think of. You can check how much you are using in the Bandwidth > Real Time menu. Tomato also comes with two very useful tools to debug your QOS settings.

### Distribution Graphs

- Use these graph to determine where your connections are being classified. If you see something out of balance, you can adjust your classifications accordingly.

<div>[![QOS Distribution Graph](http://static.mrmatt57.org/img/QOS_Graph.gif "QOS Distribution Graph")](http://static.mrmatt57.org/img/QOS_Graph_full.gif)</div>  
### Detailed View

- This shows what traffic is currently flowing and how it is being classified. Take a look at each of the connections and make sure it is classified correctly. This report is also useful for determining the source of rouge traffic.

<div>[![QOS Details](http://static.mrmatt57.org/img/QOS_Details.gif "QOS Details")](http://static.mrmatt57.org/img/QOS_Details_full.gif)</div>  

## The Downside-

Yea, there is usually a con with every pro. To make this setup work correctly, you are essentially capping your throughput. Some networks offer pooled connections and have -boost- speeds. You will not be able to take advantage of these features. Most of the bandwidth related troubles with SOHO VOIP is outbound, so one workaround is to turn off the Inbound Limits. It is not fool-proof, but in some setups will work just fine.


## Summary

As you can see, the Tomato firmware gives you granular traffic shaping control. Implementing these QOS settings has not only eliminated my VOIP problems, it has also made a noticeable difference in the overall speed and consistency of my connection. DNS queries resolve faster, multiple HTTP requests are balanced and I can transfer large files in the background. Even if you are not ready to take the leap to VOIP, I highly recommend Tomato Firmware.

<span id="credits">Banner photo by [-Peter Castleton-](https://flic.kr/p/8yLiUh)</span>



