---
date: "2026-03-20"
draft: false
title: "Give It Access"
slug: "give-it-access"
description: "I asked AI to help me upgrade my PC. The first thing it found was a free performance boost I'd been sitting on for years. The lesson isn't about RAM speeds."
summary: "I asked AI to help me upgrade my PC. The first thing it found was a free performance boost I'd been sitting on for years."
images:
  - "/images/give-it-access-control-board.png"
tags:
  - "reflections"
  - "software-development"
---

{{< figure src="/images/give-it-access-control-board.png" alt="Illustration of a human at a control panel flipping an Access Granted switch while an agent inside the machine holds up a glowing component labeled The Finding" caption="You're the control board. Let the agent do the inspecting." >}}

I asked Claude to help me plan a PC upgrade. Pretty standard stuff... "pull my specs and tell me what to upgrade." It ran a handful of system commands, built a table of my components, and started making recommendations. GPU, motherboard, the usual suspects.

But the first thing it said wasn't "buy this." It was "your RAM is already faster than what your motherboard is running it at."

I have 32GB of G.Skill DDR4-3600. It's been running at 3200MHz this entire time. All I need to do is flip on XMP in my BIOS and I get a free ~10% boost in memory-sensitive workloads. No purchase required. I've been leaving performance on the table for... I don't even know how long. Years, probably!

That one finding floored me. Not because it's complicated (it's a single BIOS toggle), but because of what it took to get there. The AI read my actual system specs, cross-referenced the rated speed of my RAM sticks against the motherboard's reported clock speed, noticed the gap, and flagged it before recommending I spend a single dollar.

### The pattern

This is the thing I keep coming back to. The interesting part isn't that AI can answer questions. It's what happens when you give it access to read something real.

I didn't paste my specs into a chat window. I didn't type "I have DDR4-3600 RAM running at 3200, what should I do?" I wouldn't have known to ask that. The agent pulled the data itself, and the insight fell out of the audit.

That's the pattern. Give it access. Let it read. Let it cross-reference. The value isn't in the answers to questions you already know to ask... it's in the things it notices that you didn't think to look for.

### This works everywhere

I keep running into this. I used to have AI write my code and then I'd commit it, write the commit message, create the PR myself. Standard workflow. Then I gave the agent access to the GitHub CLI. Now it commits, creates the PR, and when review comments come back... it resolves those too. The whole loop that used to bounce between me and the tool just collapsed.

Same thing with application logs. Give an agent direct access to your structured logging and it stops asking you to paste stack traces. It finds the error, does the root cause analysis, applies the fix, and tests it. What used to take a dozen back-and-forth iterations happens in one pass.

### Stop being the middleman

In [The Membrane](/posts/the-membrane/), I wrote that any time you find yourself copying and pasting information into or out of an agent, you're doing work that's inside the cell. The agent can probably access it directly if you let it.

Most people are still doing exactly that. The agent asks for information and they go get it. "What motherboard do you have?" So you open System Information, find the answer, type it back. You're a copy-paste relay. A human API.

Stop doing that. When it asks you for something, push back. Say "go get it yourself." You don't have to give it full admin control... you're still the one approving every command, every permission. You're the control board, not the messenger. And you'll learn more watching it work than you would doing the fetching yourself.

I asked for a PC upgrade plan and got a free one I didn't know I had. Go give something access and see what comes back.

Oh, and if you're running DDR4-3600 at 3200MHz... go enable XMP. It takes 30 seconds.
