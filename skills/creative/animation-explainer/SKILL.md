---
name: animation-explainer
description: >-
  Make clear math, science, algorithm, and technical explainer animations without making Kosta remember Manim or other tool names.
metadata:
  hermes:
    command_priority: 88
    tags: ['animation', 'explainer', 'science', 'math', 'technical']
---

# Animation Explainer

Use this for moving explanations: equations, diagrams that build step-by-step, algorithm visualizations, research concepts, mechanisms, plots, and educational motion.

Prefer `creative__manim-video` when the piece is math/science/technical and benefits from precise geometry. Use `creative__animation-lab` when the brief needs more cinematic polish than whiteboard/math style.

## Output standard

For quick explorations, produce a short MP4 or GIF plus a still/contact sheet when useful. For polished work, render a clean MP4 for the requested surface and verify it with `ffprobe` before calling it done.

## Naming note

Telegram shows this command with underscores because Telegram slash commands cannot contain hyphens. Hermes resolves the hyphenated skill name normally elsewhere.
