---
name: animation-from-website
description: >-
  Turn a URL or existing website into a short video walkthrough, promo, or animated capture.
metadata:
  hermes:
    command_priority: 88
    tags: ['animation', 'website-video', 'capture', 'promo']
---

# Animation From Website

Use this when the user gives a website/URL and asks for a video, walkthrough, demo, teaser, launch clip, or animated capture.

Prefer `media-creative__website-to-hyperframes` plus `media-creative__hyperframes`. Capture the real page, build a short narrative, then render an MP4. If the website is private or logged-in, use browser tooling first and call out what could not be captured.

## Output standard

For quick explorations, produce a short MP4 or GIF plus a still/contact sheet when useful. For polished work, render a clean MP4 for the requested surface and verify it with `ffprobe` before calling it done.

## Naming note

Telegram shows this command with underscores because Telegram slash commands cannot contain hyphens. Hermes resolves the hyphenated skill name normally elsewhere.
