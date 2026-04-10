# Cartographer's Desk — Quick Reference

> Layered topographic surfaces — spatial UI where every element has map coordinates and elevation is literal.

**Best for:** Spatial data apps, geographic dashboards, project management with hierarchy, multi-layer document editors, infrastructure topology views, network maps, knowledge graphs, API documentation with nested structures.

---

## Color Tokens (Complete)

| Token | Hex | Role |
|---|---|---|
| **Neutrals** |
| page | `#F5F0E5` | Chart Paper — deepest background |
| bg | `#EDE8DB` | Drafting Vellum — primary surface |
| surface | `#FFFFFF` | Tracing Sheet — elevated cards/inputs |
| recessed | `#E5DFD0` | Field Notebook — code blocks/insets |
| active | `#DCD5C4` | Highlighted Region — active/pressed states |
| **Text** |
| text-primary | `#2C2A26` | India Ink — headings, body text |
| text-secondary | `#5C574E` | Graphite — sidebar items, labels |
| text-muted | `#9A9487` | Faded Notation — placeholders, metadata |
| text-onAccent | `#F5F0E5` | Chart Paper — text on accent backgrounds |
| **Accents** |
| accent-primary | `#2B6CB0` | Meridian Blue — primary CTA, links |
| accent-secondary | `#C4883A` | Terrain Ochre — secondary accent |
| **Semantics** |
| success | `#3D7C47` | Forest Green — positive states |
| warning | `#D4930D` | Amber Marker — caution states |
| danger | `#C0392B` | Boundary Red — error states |
| info | `#2B6CB0` | Meridian Blue — info states |
| **Border & Special** |
| border-base | `#8B7D6B` | Contour Brown — used at variable opacity |
| inlineCode | `#6B5B3E` | Deep sepia — code text in prose |
| toggleActive | `#3D7C47` | Forest Green — toggle active track |
| selection | `rgba(43,108,176,0.18)` | Meridian Blue 18% — text selection |

**Border Opacity System:** 12% subtle / 22% card / 32% hover / 45% focus

---

## Typography (9 Roles)

| Role | Family | Size | Weight | Line | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Instrument Sans | 28px | 600 | 1.15 | -0.02em | -- | Page titles, region names |
| Heading | Instrument Sans | 18px | 600 | 1.25 | -0.01em | -- | Section titles, panel headers |
| Body | Albert Sans | 15px | 400 | 1.55 | 0.005em | -- | Primary reading text |
| Body Small | Albert Sans | 13px | 400 | 1.45 | 0.01em | -- | Sidebar items, form labels |
| Button | Instrument Sans | 13px | 550 | 1.35 | 0.02em | -- | Button labels |
| Input | Albert Sans | 14px | 420 | 1.4 | 0.005em | -- | Form input text |
| Label | Instrument Sans | 11px | 500 | 1.3 | 0.04em | `text-transform: uppercase` | Metadata, grid references (ALL CAPS) |
| Code | JetBrains Mono | 13px | 400 | 1.5 | normal | `"zero", "tnum"` | Inline code, coordinates, data values |
| Caption | Albert Sans | 11px | 400 | 1.35 | 0.01em | -- | Footnotes, legend notes, attribution |

**Font Loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;550;600&family=Albert+Sans:wght@400;420;500&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

---

## Elevation

**Strategy:** `layered-shadows` — paper-stacking with directional offset

**Shadow Tokens:**
- `shadow-sm` — `1px 1px 2px rgba(107,91,62,0.08), 0 0 0 0.5px rgba(139,125,107,0.10)`
- `shadow-card` — `2px 2px 6px rgba(107,91,62,0.10), 1px 1px 2px rgba(107,91,62,0.06)`
- `shadow-card-hover` — `3px 3px 8px rgba(107,91,62,0.14), 1px 1px 3px rgba(107,91,62,0.08)`
- `shadow-input` — `1px 1px 4px rgba(107,91,62,0.06), 0 0 0 0.5px rgba(139,125,107,0.12)`
- `shadow-input-focus` — `2px 2px 8px rgba(107,91,62,0.14), 0 0 0 1px rgba(43,108,176,0.30)`
- `shadow-popover` — `3px 4px 12px rgba(107,91,62,0.18), 1px 2px 4px rgba(107,91,62,0.10)`

All shadows use warm sepia tone (`rgba(107,91,62,...)`) with positive X/Y offsets (bottom-right directionality).

**Backdrop Blur:** popover 12px / modal 8px / none 0px

---

## Borders

**Base Color:** `#8B7D6B` (Contour Brown) at variable opacity

**Widths:** 0.5px subtle / 1px card/input / 1.5px heavy/focus / 2px accent-bottom

**Focus Ring:** `rgba(43,108,176,0.50)` 2px solid, 2px offset

**Radius:** sm 3px / md 5px / lg 7px / xl 10px / 2xl 16px / input 7px / full 9999px

---

## Motion

**Easings:**
- `default` — `cubic-bezier(0.4, 0, 0.2, 1)` — standard ease-in-out
- `pan-out` — `cubic-bezier(0.16, 1, 0.3, 1)` — fast deceleration (primary)
- `zoom-in` — `cubic-bezier(0.34, 1.56, 0.64, 1)` — slight overshoot
- `layer-settle` — `cubic-bezier(0.22, 0.68, 0, 1.0)` — gentle landing
- `out-expo` — `cubic-bezier(0.19, 1, 0.22, 1)` — smooth open/close

**Durations:**
- Sidebar items: 100ms pan-out
- Button hover: 120ms default
- Toggle/chip: 150ms default
- Card lift: 180ms pan-out
- Input shadow: 200ms default
- Ghost icon: 250ms pan-out
- Panel slide: 400ms out-expo
- Page entry: 500ms pan-out

**Active Press:** nav 0.985 / chip 0.995 / button 0.97 / tab 0.96

**Reduced Motion:** `reduced-distance` — spatial movement disabled, opacity-only fades, parallax off

---

## Component Quick-Reference

### Primary Button
- Rest: bg `#2B6CB0`, color `#F5F0E5`, radius md (5px), h 34px, padding `0 14px`
- Hover: bg `#245FA0` (darkened 8%), shadow-sm, 120ms ease-out
- Active: bg `#1E5290`, scale(0.97)
- Focus: 2px Meridian Blue ring, 2px offset

### Text Input
- Rest: bg `#FFFFFF`, border `1px #8B7D6B at 20%`, radius 7px, h 40px, padding `0 12px`
- Hover: border at 32%, shadow-input-hover, 150ms ease-out
- Focus: border `1.5px #2B6CB0`, shadow-input-focus

### Card
- Rest: bg `#FFFFFF`, border `1px #8B7D6B at 22%`, radius lg (7px), shadow-card
- Hover: border at 32%, shadow-card-hover, `translate(-0.5px, -0.5px)`, 180ms ease-out
- **Signature:** Card lifts toward light source (top-left) while shadow grows opposite direction

---

## Layout

- Content max-width: 780px
- Narrow max-width: 672px
- Sidebar width: 280px (fixed)
- Header height: 48px
- Spacing scale: 4, 6, 8, 12, 16, 20, 28, 36px
- Density: **Moderate** — denser than consumer UI, less than Bloomberg

---

## Section Index

1. [Identity & Philosophy](#identity--philosophy) — Line 12 in full.md
2. [Color System](#color-system) — Line 31
3. [Typography Matrix](#typography-matrix) — Line 82
4. [Elevation System](#elevation-system) — Line 114
5. [Border System](#border-system) — Line 167
6. [Component States](#component-states) — Line 210
7. [Motion Map](#motion-map) — Line 305
8. [Layout Tokens](#layout-tokens) — Line 357
9. [Accessibility Tokens](#accessibility-tokens) — Line 384
10. [Overlays](#overlays) — Line 412
11. [Visual Style](#visual-style) — Line 459
12. [Signature Animations](#signature-animations) — Line 517
13. [Dark Mode Variant](#dark-mode-variant) — Line 683
14. [Mobile Notes](#mobile-notes) — Line 736
15. [Implementation Checklist](#implementation-checklist) — Line 764

---

## Core Identity

**Decision principle:** "When in doubt, ask: does this feel like something you'd find on a cartographer's light table? If it feels digital, add paper. If it feels decorative, add data. If it feels static, add spatial movement."

**Visual tension:** Precision vs. warmth — cartographic data is exacting, but the medium is organic paper.

**Spatial metaphor:** Every UI element has 2D map coordinates. Navigation = viewport panning. Panels slide from beyond the frame. Depth = literal layer stacking.

**Colors from cartography:** Meridian Blue (water/links), Terrain Ochre (land/data), Forest Green (coverage/status), Boundary Red (edges/errors), Contour Brown (grid lines).

**Typography:** Instrument Sans (condensed headings), Albert Sans (body legibility), JetBrains Mono (tabular data). Labels ALL CAPS with 0.04em tracking.

**Material:** Paper grain at 2% opacity (feTurbulence SVG filter), warm directional shadows, matte surfaces, no WebGL.

**Signature animations:** Paper layer slide-in, contour pulse, viewport pan, layer parallax, compass rose rotation (60s).
