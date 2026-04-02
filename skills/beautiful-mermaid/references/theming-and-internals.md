# Beautiful Mermaid — Theming & Internals Reference

Read this file when you need to understand WHY certain styling choices matter or when
debugging visual issues.

## The Two-Color Theme System

Beautiful-mermaid's theming is built on a **mono mode** principle: every color in the
diagram is derived from just two values — `bg` (background) and `fg` (foreground).

The renderer uses CSS `color-mix()` to derive all intermediate colors:

| Derived Color | Source | Mix Ratio |
|--------------|--------|-----------|
| Primary text | `fg` | 100% |
| Secondary text | `fg` into `bg` | 60% |
| Muted text | `fg` into `bg` | 40% |
| Faint text | `fg` into `bg` | 25% |
| Edge/connector lines | `fg` into `bg` | 50% |
| Arrow heads | `fg` into `bg` | 85% |
| Node fill (tint) | `fg` into `bg` | 3% |
| Node stroke | `fg` into `bg` | 20% |
| Group header bg | `fg` into `bg` | 5% |
| Inner borders | `fg` into `bg` | 12% |

This is why custom `fill` and `stroke` look wrong — they bypass this carefully
calibrated cascade and create jarring contrast against the derived colors.

## Why Custom Colors Break Things

When you write `classDef myClass fill:#2ecc71,stroke:#27ae60,color:#fff`:
1. The node gets a bright green fill while every other node has a subtle 3% tint
2. The white text clashes with the theme's text color
3. The custom stroke width/color doesn't match the 20% derived stroke
4. It looks like a foreign object pasted onto an otherwise cohesive diagram

The renderer is designed to make diagrams look good WITHOUT any custom styling.
Trust it.

## Available Themes (15 Built-In)

| Theme | Type | Background | Foreground |
|-------|------|-----------|------------|
| zinc-light | Light | #FFFFFF | #27272A |
| zinc-dark | Dark | #18181B | #FAFAFA |
| tokyo-night | Dark | #1a1b26 | #a9b1d6 |
| tokyo-night-storm | Dark | #24283b | #a9b1d6 |
| tokyo-night-light | Light | #d5d6db | #343b58 |
| catppuccin-mocha | Dark | #1e1e2e | #cdd6f4 |
| catppuccin-latte | Light | #eff1f5 | #4c4f69 |
| nord | Dark | #2e3440 | #d8dee9 |
| nord-light | Light | #eceff4 | #2e3440 |
| dracula | Dark | #282a36 | #f8f8f2 |
| github-light | Light | #ffffff | #1f2328 |
| github-dark | Dark | #0d1117 | #e6edf3 |
| solarized-light | Light | #fdf6e3 | #657b83 |
| solarized-dark | Dark | #002b36 | #839496 |
| one-dark | Dark | #282c34 | #abb2bf |

The theme is selected by Craft Agent based on the user's app theme — you don't
control which theme is active. This means your diagram must look good in ANY theme,
which is another reason to avoid hardcoded colors.

## Fixed Style Constants

These are baked into the renderer and cannot be changed:
- Rectangle corners: `rx=0 ry=0` (sharp) — unlike standard Mermaid's rounded defaults
- Rounded node corners: `rx=6`
- Stadium shape: `rx=height/2` (full pill)
- Stroke widths: outer box 1px, inner box 0.75px, connectors 1px
- Arrow heads: filled triangles, 8×5 px
- Dashed edges: `stroke-dasharray="4 4"`
- Font: Inter (13px/500 for labels, 11px/400 for edge labels, 12px/600 for group headers)
- Class/ER member text: JetBrains Mono
- Node padding: 20px horizontal, 10px vertical

## Layout Engine

Beautiful-mermaid uses **ELK.js** (Eclipse Layout Kernel) instead of Mermaid's dagre.
ELK generally produces cleaner layouts with better edge routing, but:
- It may position nodes differently than you'd expect from standard Mermaid
- Very large graphs can have suboptimal crossing minimization
- Direction (LR vs TD) significantly affects quality — LR is usually better

## XY Chart Specifics

XY charts get significantly enhanced visual treatment:
- Dot grid background (not solid lines) at 0.65 opacity
- Bars have 8px rounded corners on ALL corners (not just top)
- Lines use natural cubic spline interpolation (smooth curves, not straight segments)
- Line shadows: 5px wide at 0.12 opacity
- Lines with ≤12 points show data point dots automatically
- Monochromatic color palette derived from the accent color
- Horizontal orientation available: `xychart-beta horizontal`
