---
name: animation-3d-scene
description: >-
  Make Blender-style 3D scenes, camera moves, materials, object animation, and particle sculptures without making Kosta remember Blender MCP.
metadata:
  hermes:
    command_priority: 88
    tags: ['animation', '3d', 'blender', 'particles']
---

# Animation 3D Scene

Use this for 3D work: product-like renders, particle sculptures, animated cameras, objects/materials, abstract 3D environments, and Blender scene construction.

Prefer `creative__blender-mcp` when Blender and its MCP addon are running. If Blender is not connected, create a fallback storyboard/mock render plan or use available local rendering tools, but do not claim Blender control is live until port 9876 responds.

## Output standard

For quick explorations, produce a short MP4 or GIF plus a still/contact sheet when useful. For polished work, render a clean MP4 for the requested surface and verify it with `ffprobe` before calling it done.

## Naming note

Telegram shows this command with underscores because Telegram slash commands cannot contain hyphens. Hermes resolves the hyphenated skill name normally elsewhere.
