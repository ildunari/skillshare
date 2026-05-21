# Merge notes

This skill combines the strongest parts of two source skills.

## What came from `liquid-glass`

- richer low-level reference material on SVG filters, CodePen demos, Framer Motion patterns, and library options
- a zero-dependency React + SVG filter component
- a library-backed `liquid-glass-react` wrapper for quick prototyping
- a parametric SVG filter generator script
- a standalone HTML demo

## What came from `liquid-glass-mcp-ui`

- stronger trigger boundary for real app work instead of generic inspiration scraping
- clearer production tiers: CSS/Motion default, SVG hero surfaces, libraries/shaders only when justified
- MCP-specific UI judgment for chat shells, command docks, inspectors, tool panels, and dense result views
- templates tuned for tool-heavy interfaces instead of generic showcase cards
- a Python scaffolder for quickly dropping starter files into a project

## What changed in the merged version

- combined both template sets under one `assets/templates/` directory
- expanded the scaffolder to emit either the lightweight Motion stack or the heavier filter/library variants
- kept the stronger MCP and production guidance as the main skill spine
- preserved the richer reference corpus as on-demand material instead of bloating `SKILL.md`
