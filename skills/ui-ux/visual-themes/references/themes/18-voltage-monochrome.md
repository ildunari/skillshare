## 18. Voltage Monochrome

> A high-structure monochrome system with one "voltage" accent that behaves like a spotlight. Everything is about hierarchy and focus.

**Best for:** Developer tools, ops dashboards, dense tables, IDE-like interfaces, terminal UIs, system monitors.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Near White | `#FAFAFA` | Primary canvas. Clean, clinical. |
| Alt Background | Light Grey | `#F0F0F0` | Cards, sidebars, table rows (alternating). |
| Primary Text | Near Black | `#141414` | Body text, headings. Maximum readability. |
| Secondary Text | Mid Grey | `#6B6B6B` | Captions, metadata, timestamps. |
| Voltage Accent | Electric Cyan | `#00C2D1` | Focus rings, selection, active states, primary CTAs. Used SPARINGLY. |
| Border | Silver | `#D4D4D4` | Dividers, table gridlines, input borders. |
| Surface Elevated | Pure White | `#FFFFFF` | Modals, dropdowns, floating panels. |
| Error | Signal Red | `#DC2626` | Error states only. The one non-monochrome semantic. |

### Typography
- **Display:** Inter (variable, 600–700 weight) — tight metrics, neutral precision
- **Body:** Inter (400 weight) — consistent family, no pairing friction
- **Mono:** JetBrains Mono (ligatures enabled) — the workhorse for code and data

### Visual Style
- **Zero Decoration:** No texture, no grain, no gradients. Pure flat vector surfaces. Color does the work.
- **Grid Religion:** Visible 1px gridlines in tables. Alignment is the aesthetic. Every element snaps to a 4px grid.
- **One Accent Rule:** Electric cyan appears ONLY on: focused elements, selected items, active states, and primary actions. Never decorative. Never ambient.
- **Density First:** Tight spacing (4px gaps), compact rows (32px height), dense information. This theme respects screen real estate.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.2, 0, 0, 1)` — sharp ease-out. Instant-feeling, precise.
- **Timing:** Fast. Micro-interactions 80–120ms. View changes 150–200ms. Nothing lingers.
- **Motion Character:** Mechanical and precise. No overshoot, no bounce, no spring. Clean cuts.
- **Physics:** None. This is a machine, not an organism.

### Signature Animations
1. **Snap Focus** — Focus rings appear instantly (0ms) with a 1px cyan outline. No fade, no bloom. Binary on/off.
2. **Row Highlight** — Table rows get a 2px left-border in cyan on hover, appearing at 80ms. Clean slide-in from left edge.
3. **Panel Slide** — Sidepanels and drawers slide in from their edge at 180ms, sharp ease-out. No overlay dim.
4. **Data Pulse** — Live-updating values briefly flash cyan background (`rgba(0,194,209,0.1)`) for 500ms on change, then fade.
5. **Collapse/Expand** — Sections collapse with `max-height` animation at 150ms. No accordion bounce. Clean.

### UI Components
- **Buttons:** Primary: cyan fill, white text, `border-radius: 4px`. Secondary: 1px silver border, near-black text. Hover: darken 10%. Active: `scale(0.98)`. No shadow.
- **Sliders:** Track is 2px silver line. Thumb is 10px cyan circle, no border. Value in JetBrains Mono, monospaced alignment.
- **Cards:** White background, 1px silver border. `border-radius: 4px`. Padding 16px. No shadow.
- **Tooltips:** Near-black background, white text. Inter 12px. `border-radius: 3px`. Arrow pointer.
- **Dividers:** Silver at 100% opacity. 1px. Hard lines, not fuzzy.

### Dark Mode Variant

Voltage Monochrome has a full dark mode — not an afterthought, a first-class variant. This theme was BORN to be dark. The dark variant IS the real one.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#FAFAFA` Near White | `#0A0A0A` True Near-Black | oklch(0.06 0.00 0) — pure neutral, zero color cast |
| Card / surface | `#F0F0F0` Light Grey | `#111111` Dark Panel | oklch(0.09 0.00 0) — elevated cards |
| Alt surface | `#FFFFFF` Pure White | `#1A1A1A` Deep Panel | oklch(0.13 0.00 0) — modals, dropdowns |
| Border | `#D4D4D4` Silver | `#2A2A2A` Wire Frame | oklch(0.19 0.00 0) — dividers, gridlines |
| Border heavy | — | `#444444` Bright Wire | oklch(0.30 0.00 0) — hover, emphasis |
| Primary text | `#141414` Near Black | `#E5E5E5` Near White | oklch(0.92 0.00 0) at 90% — higher opacity for monochrome clarity |
| Secondary text | `#6B6B6B` Mid Grey | `#A0A0A0` Lifted Grey | oklch(0.67 0.00 0) — captions, metadata |
| Dim text | — | `#6B6B6B` Mid Grey | oklch(0.46 0.00 0) — timestamps, tertiary |
| Grey ladder | `#FAFAFA`→`#F0F0F0`→`#D4D4D4`→`#6B6B6B`→`#141414` | `#1A1A1A`→`#2A2A2A`→`#444444`→`#6B6B6B`→`#A0A0A0`→`#E5E5E5` | Full grey ramp inverts cleanly |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Electric Cyan | `#00C2D1` | `#00C2D1` (unchanged) | Already vivid. Designed for this — cyan pops equally on white and black |
| Error Red | `#DC2626` | `#EF4444` (lighter) | Slight brightening for visibility on dark backgrounds |
| Focus ring | 1px cyan outline | 1px cyan outline (unchanged) | Binary on/off — works identically in both modes |

#### Shadow & Depth Adaptation
- Light: No shadows — flat, clinical, zero decoration
- Dark: STILL no shadows. Zero decoration rule preserved absolutely. Depth from border color steps only: `#111111` (card) sits on `#0A0A0A` (page), bordered by `#2A2A2A`. The monochrome grey ladder provides all the visual separation needed

#### Texture & Grain Adaptation
- Light: No texture — pure flat vector surfaces
- Dark: No texture. Still pure flat vector. The zero-decoration principle is mode-independent. Grid lines shift from 8% black on light to 8% white on dark — same structural visibility, inverted

#### Dark Mode Rules
- One-accent rule preserved absolutely — cyan is STILL the only color. No warm tones, no additional accents in dark mode
- Grey ladder inverts cleanly: 6 stops from `#1A1A1A` through `#E5E5E5`, providing the same hierarchical range as light mode
- Grid visibility: `1px solid rgba(255,255,255,0.08)` replaces `1px solid rgba(0,0,0,0.08)` — same 8% opacity, inverted base
- Text at 90% opacity (not 87%) — monochrome themes need slightly higher text contrast because there's no color to create emphasis
- "This theme was BORN to be dark. The dark variant IS the real one"

### Mobile Notes
- Maintain tight spacing — this theme is about density even on mobile.
- Touch targets: 44px minimum height, but reduce horizontal padding to keep density.
- Disable row-highlight left-border animation (not useful for touch interfaces).
