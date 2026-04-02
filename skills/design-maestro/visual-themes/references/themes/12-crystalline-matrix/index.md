# Crystalline Matrix — Quick Reference

> Geometric prismatic precision -- light splitting through faceted crystal, revealing rainbow spectra at structural edges while platinum wireframes hold mathematical order.

**Best for:** Data visualization dashboards, mathematical simulations, scientific tools, developer IDEs, architecture/CAD viewers, engineering documentation, financial modeling, algorithmic art, geometry explorers, physics simulations.

**Decision principle:** "When in doubt, ask: does this look like it was computed? If it looks organic, hand-drawn, or warm, reject it. If it looks like a diagram rendered by a geometry engine, accept it."

---

## Color Palette

### Neutrals & Text

| Token | Hex | OKLCH | Role |
|---|---|---|---|
| page | `#EAEDF0` | L=93.2 C=0.008 h=250 | Crystal mass base |
| bg | `#F0F2F4` | L=95.0 C=0.006 h=250 | Polished outer face |
| surface | `#F7F8FA` | L=97.2 C=0.005 h=250 | Cards, inputs, brightest facet |
| recessed | `#E2E5E9` | L=90.8 C=0.009 h=250 | Code blocks, inset |
| active | `#D5D9DE` | L=87.0 C=0.010 h=250 | Active states, shadow facet |
| text-primary | `#1A1D21` | L=16.0 C=0.008 h=250 | Graphite text |
| text-secondary | `#5C636E` | L=44.0 C=0.015 h=250 | Platinum grey |
| text-muted | `#8E95A0` | L=62.0 C=0.015 h=250 | Wire silver |
| text-onAccent | `#F7F8FA` | L=97.2 C=0.005 h=250 | Crystal white |
| border-base | `#A0A8B4` | L=69.0 C=0.018 h=250 | Wireframe platinum |

### Accents & Semantics

| Token | Hex | OKLCH | Role |
|---|---|---|---|
| accent-primary | `#3B6FD4` | L=50.0 C=0.140 h=260 | Sapphire CTA |
| accent-secondary | `#7B5EA7` | L=46.0 C=0.120 h=300 | Amethyst links |
| success | `#2D8B5E` | L=52.0 C=0.110 h=155 | Emerald facet |
| warning | `#B8902D` | L=62.0 C=0.130 h=80 | Citrine caution |
| danger | `#C44040` | L=48.0 C=0.150 h=25 | Ruby flaw |
| info | `#4A90C4` | L=56.0 C=0.100 h=240 | Ice blue |

### Prismatic Border System

| Token | Value |
|---|---|
| prismatic-gradient | `conic-gradient(from 0deg, #C44040, #B8902D, #2D8B5E, #4A90C4, #3B6FD4, #7B5EA7, #C44040)` |
| prismatic-subtle | Same gradient at 15% opacity |
| prismatic-active | Same gradient at 35% opacity |

### Special Tokens

| Token | Value | Role |
|---|---|---|
| inlineCode | `#4A5568` | Code in prose |
| toggleActive | `#3B6FD4` | Switch track on |
| selection | `rgba(59, 111, 212, 0.14)` | ::selection bg |
| wireframeOverlay | `rgba(160, 168, 180, 0.08)` | Grid lines |
| facetHighlight | `rgba(255, 255, 255, 0.5)` | Top-edge light catch |
| facetShadow | `rgba(26, 29, 33, 0.03)` | Bottom-edge shadow |

### Opacity System

| Level | Opacity | Usage |
|---|---|---|
| subtle | 10% | Sidebar edges, grid lines |
| card | 18% | Card borders |
| hover | 26% | Hover states |
| focus | 36% | Focus borders |

---

## Typography

### Families

- **Display/Heading:** Instrument Sans (condensed geometric authority)
- **Body/UI:** Albert Sans (Scandinavian minimalism)
- **Code:** Geist Mono (modern monospace)

### Role Matrix

| Role | Family | Size | Weight | Line-height | Spacing | Transform | Usage |
|---|---|---|---|---|---|---|---|
| Display | Instrument Sans | 36px | 600 | 1.1 | -0.03em | -- | Hero titles |
| Heading | Instrument Sans | 22px | 600 | 1.2 | -0.015em | -- | Section titles |
| Subheading | Albert Sans | 17px | 600 | 1.3 | -0.005em | -- | Card titles |
| Body | Albert Sans | 15px | 400 | 1.55 | normal | -- | Primary text |
| Body Small | Albert Sans | 13px | 400 | 1.4 | 0.005em | -- | Sidebar, labels |
| Button | Albert Sans | 13px | 500 | 1.4 | 0.02em | uppercase | Button labels |
| Input | Albert Sans | 14px | 400 | 1.4 | normal | -- | Form input |
| Label | Albert Sans | 10px | 600 | 1.3 | 0.08em | uppercase | Metadata, axis markers |
| Code | Geist Mono | 0.9em | 400 | 1.5 | normal | -- | Code, data values |
| Caption | Albert Sans | 11px | 400 | 1.3 | 0.01em | -- | Footnotes |

---

## Elevation

**Strategy:** Faceted surfaces + wireframe overlays + prismatic edge highlights

### Shadow Tokens

| Token | Value |
|---|---|
| shadow-sm | `0 1px 2px rgba(26, 29, 33, 0.05)` |
| shadow-card | `0 1px 3px rgba(26, 29, 33, 0.04), 0 0 0 0.5px rgba(160, 168, 180, 0.18)` |
| shadow-card-hover | `0 2px 6px rgba(26, 29, 33, 0.06), 0 0 0 0.5px rgba(160, 168, 180, 0.26)` |
| shadow-input-focus | `0 2px 8px rgba(26, 29, 33, 0.08), 0 0 0 1px rgba(59, 111, 212, 0.3)` |
| shadow-popover | `0 4px 12px rgba(26, 29, 33, 0.12), 0 1px 3px rgba(26, 29, 33, 0.06)` |

### Facet Gradients

| Token | Value |
|---|---|
| facet-172 | `linear-gradient(172deg, rgba(255,255,255,0.5) 0%, transparent 40%, rgba(26,29,33,0.015) 100%)` |
| facet-168 | `linear-gradient(168deg, rgba(255,255,255,0.45) 0%, transparent 38%, rgba(26,29,33,0.018) 100%)` |
| facet-175 | `linear-gradient(175deg, rgba(255,255,255,0.4) 0%, transparent 42%, rgba(26,29,33,0.012) 100%)` |
| facet-recessed | `linear-gradient(180deg, rgba(26,29,33,0.02) 0%, transparent 30%)` |

---

## Borders

**Base Color:** `#A0A8B4` Wireframe Platinum at variable opacity

| Pattern | Width | Opacity | Usage |
|---|---|---|---|
| subtle | 0.5px | 10% | Sidebar, grid lines |
| card | 0.5px | 18% | Card borders |
| hover | 0.5px | 26% | Hover states |
| input | 1px | 12% | Form inputs |
| wireframe | 1px dashed | 8% | Structural lines |

**Focus Ring:** `2px solid rgba(59, 111, 212, 0.45)`, offset `2px`

---

## Motion

### Easings

| Name | Value | Character |
|---|---|---|
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Mechanical precision |
| out-quart | `cubic-bezier(0.165, 0.85, 0.45, 1)` | Crystal-sharp arrival |
| out-expo | `cubic-bezier(0.19, 1, 0.22, 1)` | Panel open/close |
| geometric-ease | `cubic-bezier(0.25, 0.0, 0.0, 1.0)` | Signature: computed feel |
| symmetric-ease | `cubic-bezier(0.42, 0, 0.58, 1)` | Mirror animations |

### Duration Map

| Component | Duration | Easing |
|---|---|---|
| Sidebar item | 80ms | out-quart |
| Button hover | 120ms | default |
| Toggle/chip | 150ms | default |
| Card hover | 250ms | geometric-ease |
| Ghost button | 250ms | out-quart |
| Prismatic activation | 300ms | geometric-ease |
| Panel open/close | 500ms | out-expo |

### Active Press Scale

- Nav items: `scale(0.985)`
- Chips: `scale(0.995)`
- Buttons: `scale(0.97)`
- Tabs: `scale(0.96)`

---

## Component Quick-Reference

### Button (Primary)

- **Rest:** transparent bg, `1px solid rgba(160,168,180,0.22)`, text-primary, 32px h, 4px radius
- **Hover:** `rgba(160,168,180,0.06)` bg, `0.30` border
- **Focus:** Sapphire ring
- **Transition:** 120ms default

### Input (Text)

- **Rest:** surface bg, `1px solid rgba(160,168,180,0.12)`, facet-172 gradient, sapphire caret
- **Hover:** `0.26` border, shadow-input-hover
- **Focus:** Sapphire ring + sapphire border accent
- **Transition:** 200ms default

### Card

- **Rest:** facet-172 over surface, `0.5px solid rgba(160,168,180,0.18)`, 6px radius, shadow-card
- **Hover:** `0.26` border, prismatic border fades in, shadow-card-hover
- **Transition:** 250ms geometric-ease

---

## Layout

| Token | Value |
|---|---|
| Content max-width | 760px |
| Sidebar width | 260px |
| Header height | 44px |
| Spacing scale | 4, 6, 8, 12, 16, 20, 24, 32, 40px |
| Density | moderate (55:45 content:whitespace) |

---

## Accessibility

| Token | Value |
|---|---|
| Focus ring | `rgba(59, 111, 212, 0.45)`, 2px solid, 2px offset |
| Disabled opacity | 0.4 + pointer-events none |
| Selection bg | `rgba(59, 111, 212, 0.14)` |
| Scrollbar thumb | `rgba(160, 168, 180, 0.28)` |
| Min touch target | 44px |
| Contrast | WCAG AA (4.5:1 text, 3:1 large) |

---

## Section Index

| Section | Line (full.md) |
|---------|------|
| Identity & Philosophy | 55 |
| Color System | 69 |
| Typography Matrix | 193 |
| Elevation System | 239 |
| Border System | 349 |
| Component States | 388 |
| Motion Map | 533 |
| Overlays | 591 |
| Layout Tokens | 644 |
| Accessibility Tokens | 699 |
| Visual Style | 734 |
| Signature Animations | 827 |
| Dark Mode Variant | 1020 |
| Data Visualization | 1055 |
| Mobile Notes | 1070 |
| Implementation Checklist | 1103 |

---

## Key Differentiators

- **Prismatic borders:** Conic-gradient rainbow appears ONLY at edges, never on surfaces
- **Faceted surfaces:** Each card has a different gradient angle (172°, 168°, 175°) simulating crystal faces
- **Wireframe overlays:** Geometric grid patterns at 8% opacity create structural depth
- **Monochrome dominance:** 90% cool grey/white, 10% prismatic accent
- **Geometric precision:** Small border-radius (4-6px), uppercase labels with tracking, cold sans-serif pairing
- **No warmth:** Every surface carries cool blue-grey undertone; warm colors exist only in prismatic gradient
- **Sharp shadows:** Minimal blur, geometric offsets -- crystal refracts, doesn't scatter
- **Signature animations:** Facet rotation, light-catch sparkle, crystal growth, prismatic border sweep
