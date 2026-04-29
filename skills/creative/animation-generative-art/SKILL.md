---
name: animation-generative-art
targets: [hermes-default, hermes-gpt, claude]
description: >-
  Make coded visual loops: particles, flow fields, shaders, canvas sketches, procedural art, and interactive animation studies.
metadata:
  hermes:
    command_priority: 88
    tags: ['animation', 'generative-art', 'creative-coding', 'particles']
---

# Animation Generative Art

Use this for coded visual art: particles, flow fields, reaction-diffusion looks, shader-ish canvas animation, interactive sketches, creative coding, loops, and procedural systems.

Prefer `creative__p5js` and, when richer browser/game rendering is needed, `media-creative__game-dev` or `media-creative__algorithmic-art-enhanced`. Export a video/GIF when the user wants a deliverable, not just source code.

## Output standard

For quick explorations, produce a short MP4 or GIF plus a still/contact sheet when useful. For polished work, render a clean MP4 for the requested surface and verify it with `ffprobe` before calling it done.

## Naming note

Telegram shows this command with underscores because Telegram slash commands cannot contain hyphens. Hermes resolves the hyphenated skill name normally elsewhere.
