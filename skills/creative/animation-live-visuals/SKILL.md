---
name: animation-live-visuals
description: >-
  Make TouchDesigner-style live/generative visuals, audio-reactive stage looks, visualizers, tunnels, feedback, and experimental realtime motion.
metadata:
  hermes:
    command_priority: 88
    tags: ['animation', 'live-visuals', 'touchdesigner', 'audio-reactive']
---

# Animation Live Visuals

Use this for live visuals: audio-reactive orbs, feedback tunnels, particles, stage visuals, generative loops, realtime installations, and TouchDesigner/twozero work.

Prefer `creative__touchdesigner-mcp` and `creative__touchdesigner-hermes-ops` when TouchDesigner is actually live. If the MCP is not available, fall back to a rendered MP4 artifact and say plainly that TouchDesigner was not connected.

## Output standard

For quick explorations, produce a short MP4 or GIF plus a still/contact sheet when useful. For polished work, render a clean MP4 for the requested surface and verify it with `ffprobe` before calling it done.

## Naming note

Telegram shows this command with underscores because Telegram slash commands cannot contain hyphens. Hermes resolves the hyphenated skill name normally elsewhere.
