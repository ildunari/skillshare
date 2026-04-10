# Monochrome Terminal — Quick Reference

**Schema:** v2 | **Theme:** 07 | **Density:** very-dense | **Strategy:** borders-only

---

## Color Tokens (Warm Mode: Concrete)

| Token | Hex | Role |
|---|---|---|
| page | `#1A1A18` | Deepest background, warm near-black |
| bg | `#242422` | Primary surface, poured concrete |
| surface | `#2E2E2B` | Cards, inputs, elevated panels |
| recessed | `#111110` | Code blocks, inset areas |
| active | `#3A3A37` | Active/pressed, selected rows |
| text-primary | `#E8E6E1` | Headings, body text, warm off-white |
| text-secondary | `rgba(232,230,225,0.62)` | Secondary labels (text-primary 62%) |
| text-muted | `rgba(232,230,225,0.36)` | Placeholders, metadata (text-primary 36%) |
| text-onAccent | `#FFFFFF` | Text on red accent backgrounds |
| border-base | `#8A8A85` | Variable opacity border color |
| accent-primary | `#E53935` | THE accent: structural red |
| success | `#7CB342` | Positive states, olive-green |
| warning | `#F9A825` | Caution, industrial amber |
| danger | `#E53935` | Error states (same as accent) |
| info | `#78909C` | Info states, blue-grey |
| inlineCode | `#E53935` | Code text within prose |
| toggleActive | `#E53935` | Toggle active track |
| selection | `rgba(229,57,53,0.22)` | Text selection background |

## Color Tokens (Cool Mode: Voltage)

| Token | Hex | Role |
|---|---|---|
| page | `#0D0D0D` | Deepest background, pure black |
| bg | `#161616` | Primary surface, CRT-off dark |
| surface | `#1E1E1E` | Cards, inputs, terminal panels |
| recessed | `#080808` | Code blocks, deep void |
| active | `#2A2A2A` | Active/pressed, cursor highlight |
| text-primary | `#E0E0E0` | Headings, body, phosphor white |
| text-secondary | `rgba(224,224,224,0.62)` | Secondary labels (text-primary 62%) |
| text-muted | `rgba(224,224,224,0.36)` | Placeholders, metadata (text-primary 36%) |
| text-onAccent | `#0D0D0D` | Text on cyan accent backgrounds |
| border-base | `#666666` | Variable opacity border color |
| accent-primary | `#00E5FF` | THE accent: voltage cyan |
| success | `#69F0AE` | Positive states, terminal green |
| warning | `#FFD54F` | Caution, alert amber |
| danger | `#FF5252` | Error states, alarm red |
| info | `#00E5FF` | Info states (same as accent) |
| inlineCode | `#00E5FF` | Code text within prose |
| toggleActive | `#00E5FF` | Toggle active track |
| selection | `rgba(0,229,255,0.20)` | Text selection background |

---

## Typography Roles

### Warm Mode (Concrete)

| Role | Family | Size | Weight | Line-height | Spacing | Features |
|---|---|---|---|---|---|---|
| Display | Barlow Condensed | 20px | 700 | 1.15 | 0.08em | `text-transform: uppercase` |
| Heading | Barlow Condensed | 14px | 600 | 1.25 | 0.06em | `text-transform: uppercase` |
| Body | IBM Plex Mono | 13px | 400 | 1.55 | normal | `"zero"` |
| Body Small | IBM Plex Mono | 11px | 400 | 1.45 | normal | `"zero"` |
| Button | Barlow Condensed | 12px | 600 | 1.4 | 0.05em | `text-transform: uppercase` |
| Input | IBM Plex Mono | 13px | 400 | 1.4 | normal | `"zero"` |
| Label | Barlow Condensed | 10px | 500 | 1.3 | 0.06em | `text-transform: uppercase` |
| Code | IBM Plex Mono | 13px | 400 | 1.55 | normal | `"liga", "zero"` |
| Caption | IBM Plex Mono | 10px | 400 | 1.33 | normal | -- |

### Cool Mode (Voltage)

| Role | Family | Size | Weight | Line-height | Spacing | Features |
|---|---|---|---|---|---|---|
| Display | Barlow Condensed | 20px | 600 | 1.15 | 0.04em | -- |
| Heading | Barlow Condensed | 14px | 500 | 1.25 | 0.03em | -- |
| Body | JetBrains Mono | 13px | 400 | 1.55 | normal | `"zero"` |
| Body Small | JetBrains Mono | 11px | 400 | 1.45 | normal | `"zero"` |
| Button | Barlow Condensed | 12px | 500 | 1.4 | 0.03em | -- |
| Input | JetBrains Mono | 13px | 400 | 1.4 | normal | `"zero"` |
| Label | Barlow Condensed | 10px | 500 | 1.3 | 0.04em | `text-transform: uppercase` |
| Code | JetBrains Mono | 13px | 400 | 1.55 | normal | `"liga", "zero"` |
| Caption | JetBrains Mono | 10px | 400 | 1.33 | normal | -- |

---

## Elevation (borders-only)

**Strategy:** Flat surfaces, no shadows (Warm). One popover shadow (Cool).

**Key Shadow Tokens:**
- `shadow-none` — All surfaces (Warm + Cool)
- `shadow-popover` — Cool: `0 2px 8px rgba(0,0,0,0.6), 0 0 0 1px rgba(102,102,102,0.18)`
- `shadow-input` — `none` (both modes)
- `shadow-input-hover` — `none` (both modes)
- `shadow-input-focus` — Cool: `0 0 0 1px var(--accent-primary)`

**Separation:** Tint-stepping + border weight (1px internal, 1px card, 2px heavy). Exposed grid (6% opacity, 4px spacing) provides alignment structure.

---

## Border System

**Base Color:** `border-base` token (Warm: `#8A8A85`, Cool: `#666666`)

**Opacity Scale:**
- Subtle: 10%
- Card: 18%
- Hover: 28%
- Focus: 100% (accent-primary)
- Grid: 6%

**Focus Ring:**
- Warm: `2px solid #E53935`, offset 1px
- Cool: `2px solid #00E5FF`, offset 1px

**Radius:** ALL values = `0px` (no exceptions)

---

## Motion

**Philosophy:** Mechanical motion. Linear or sharp deceleration only. No springs, no organic easing.

**Easings:**
- `instant` — `steps(1)` (binary state changes)
- `mechanical` — `linear` (constant velocity, theme default)
- `decel` — `cubic-bezier(0.25, 0.46, 0.45, 0.94)` (out-quad, sharp stop)
- `brake` — `cubic-bezier(0.0, 0.0, 0.2, 1.0)` (out-cubic, panel movements)

**Duration Range:** 0-150ms (Warm), 0-120ms (Cool)

**Active Press Scale:** None. No transform scaling on any element.

**Reduced Motion:** All durations → 0ms, all animations paused.

---

## Component Quick-Reference

### Primary Button
- **Rest:** bg `accent-primary`, color `text-onAccent`, h 28px, radius 0px
- **Hover:** bg brightened 12% (Warm: `#EF5350`, Cool: `#33EBFF`), 50ms linear
- **Focus:** `outline: 2px solid accent-primary, offset 1px`

### Text Input
- **Rest:** bg `surface`, border `1px solid border-base@18%`, h 32px, radius 0px
- **Hover:** border@28%, 50ms linear
- **Focus:** border `1px solid accent-primary`, Cool: box-shadow `0 0 0 1px accent-primary`

### Card
- **Rest:** bg `surface`, border `1px solid border-base@18%`, radius 0px, shadow none
- **Hover:** border@28%, bg lifted 1 stop, 50ms linear

### Toggle (Rectangular)
- **Track:** 32x16px, radius 0px
- **Thumb:** 12x12px square, radius 0px
- **Transition:** 80ms linear slide

---

## Section Index (full.md)

1. Identity & Philosophy — Line 24
2. Color System — Line 40
3. Typography Matrix — Line 123
4. Elevation System — Line 181
5. Border System — Line 215
6. Component States — Line 250
7. Motion Map — Line 353
8. Layout Tokens — Line 391
9. Accessibility Tokens — Line 426
10. Overlays — Line 450
11. Visual Style — Line 494
12. Signature Animations — Line 551
13. Mode Variant — Line 678
14. Mobile Notes — Line 730
15. Implementation Checklist — Line 758

---

**Key Constraints:**
- ONE accent color per mode (Red/Cyan)
- 0px border-radius everywhere
- No shadows (Warm), one popover shadow (Cool)
- Monospace is primary body font
- Very dense spacing (4px unit, 28px rows)
- Mechanical motion only (linear/out-quad)
