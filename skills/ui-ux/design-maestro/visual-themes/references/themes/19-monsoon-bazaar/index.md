# Monsoon Bazaar — Quick Reference

> South Asian poster energy — saturated inks, registration offset depth, and controlled chaos at maximum volume.

**Best for:** Event marketing, festival pages, music platforms, food delivery apps, cultural showcases, portfolio sites, editorial magazines, campaign microsites, streetwear storefronts.

**Decision principle:** "When in doubt, ask: does this feel like a bazaar poster printed on cotton? If it feels like a SaaS landing page, add more saturation, more weight, more stamp energy. If it feels like visual noise, organize it into zones."

---

## Color Tokens (Complete)

| Token | Hex | Role |
|---|---|---|
| **Neutrals** | | |
| page | `#F0E6D4` | Raw Cotton — deepest background, unbleached muslin fabric |
| bg | `#F7F0E2` | Bleached Cotton — primary surface, printing substrate |
| surface | `#FFFAF0` | White Cotton — cards, inputs, popovers |
| recessed | `#E4D9C6` | Dyed Cotton — code blocks, inset areas |
| active | `#D8CCB8` | Pressed Cotton — active/pressed states |
| **Text** | | |
| text-primary | `#1A1210` | Block Print Ink — headings, body text |
| text-secondary | `#5C4D40` | Faded Ink — sidebar items, secondary labels |
| text-muted | `#9A8A78` | Worn Print — placeholders, timestamps |
| text-onAccent | `#FFF8EE` | Raw Cotton — text on accent backgrounds |
| **Borders** | | |
| border-base | `#BCA890` | Thread Line — base border (variable opacity) |
| **Accents** | | |
| accent-primary | `#E6166E` | Hot Magenta — brand accent, primary CTA |
| accent-secondary | `#2A1B8C` | Deep Indigo — registration offset shadows |
| accent-tertiary | `#F5A623` | Saffron Yellow — highlights, warnings |
| **Semantics** | | |
| success | `#2D8C46` | Henna Green — positive states |
| warning | `#F5A623` | Saffron Yellow — caution states |
| danger | `#D42B2B` | Vermillion Sindoor — error states |
| info | `#1A8C8C` | Monsoon Teal — informational states |
| **Special** | | |
| inlineCode | `#7B2D8E` | Deep purple (magenta + indigo overprint) |
| toggleActive | `#2A1B8C` | Deep Indigo — toggle active track |
| selection | `rgba(230,22,110,0.20)` | Hot Magenta 20% — `::selection` |
| **Fixed** | | |
| alwaysBlack | `#000000` | Structural black (mode-independent) |
| alwaysWhite | `#FFFFFF` | Emergency on-dark (mode-independent) |

**Opacity System (border-base):**
- subtle: 15% — lightest separation, hairlines
- card: 25% — card borders, cotton layer edges
- hover: 35% — hover states, emphasized borders
- focus: 50% — focus borders, maximum emphasis

---

## Typography (All 9 Roles)

| Role | Family | Size | Weight | Line-height | Tracking | Features | Usage |
|---|---|---|---|---|---|---|---|
| **Display** | Bricolage Grotesque | 48px | 800 | 1.05 | -0.03em | opsz 48 | Hero titles — MASSIVE BOLD poster-scale |
| **Heading** | Bricolage Grotesque | 28px | 700 | 1.15 | -0.02em | opsz 28 | Section titles — bold, quieter |
| **Subheading** | Bricolage Grotesque | 20px | 600 | 1.25 | -0.01em | -- | Card titles, subsection headers |
| **Body** | DM Sans | 16px | 400 | 1.55 | normal | -- | Primary reading text |
| **Body Small** | DM Sans | 14px | 400 | 1.45 | normal | -- | Sidebar items, labels |
| **Button** | DM Sans | 14px | 600 | 1.4 | 0.04em | uppercase | Button labels — ALL CAPS |
| **Input** | DM Sans | 14px | 450 | 1.4 | normal | -- | Form input text |
| **Label** | DM Sans | 11px | 700 | 1.33 | 0.1em | uppercase | Section labels — ALL CAPS |
| **Code** | Fira Code | 0.9em | 400 | 1.5 | normal | liga, tabular-nums | Inline code, code blocks |
| **Caption** | DM Sans | 12px | 400 | 1.33 | 0.01em | -- | Disclaimers, footnotes |

**Font loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Fira+Code:wght@300..700&display=swap" rel="stylesheet">
```

**Family switch boundary:** Bricolage Grotesque for Display/Heading/Subheading ONLY. DM Sans for all other roles.

---

## Elevation System

**Strategy:** Registration offset — flat colored shadows with zero blur, offset 2-3px in one direction. Shadows use Deep Indigo or Hot Magenta (never black).

**Shadow Tokens:**
- shadow-sm: `2px 2px 0px rgba(42,27,140,0.18)` — small elements, tags, chips
- shadow-card: `3px 3px 0px rgba(42,27,140,0.22)` — cards at rest
- shadow-card-hover: `4px 4px 0px rgba(42,27,140,0.28)` — cards on hover
- shadow-input: `2px 2px 0px rgba(42,27,140,0.15)` — input fields rest
- shadow-input-hover: `3px 3px 0px rgba(42,27,140,0.20)` — input hover
- shadow-input-focus: `3px 3px 0px rgba(42,27,140,0.28)` — input focus
- shadow-popover: `4px 4px 0px rgba(42,27,140,0.30)` — menus, dropdowns
- shadow-modal: `6px 6px 0px rgba(42,27,140,0.32)` — modal dialogs
- shadow-magenta: `3px 3px 0px rgba(230,22,110,0.20)` — primary buttons, highlighted cards
- shadow-none: `none` — flat surfaces, disabled

**Depth rule:** Magenta shadow = clickable primary action. Indigo shadow = standard elevation.

---

## Border System

**Base color:** Thread Line `#BCA890` (variable opacity)

**Widths:**
- hairline: 1px
- default: 1.5px
- medium: 2px
- heavy: 3px

**Patterns:**
- subtle: 1px @ 15% — hairlines, background structure
- card: 1.5px @ 25% — card borders
- hover: 2px @ 35% — hover states
- input: 2px @ 25% — form input borders rest
- input-hover: 2px @ 35% — form input borders hover

**Focus ring:** `3px solid rgba(42,27,140,0.55)`, offset 2px — Deep Indigo

---

## Motion System

**Easings:**
- **stamp:** `cubic-bezier(0.34, 1.56, 0.64, 1)` — overshoot landing, THE signature easing
- **jitter:** `cubic-bezier(0.25, 0.1, 0, 1)` — quick snap with instability
- **press:** `cubic-bezier(0.4, 0, 0.2, 1)` — standard ease-in-out
- **cascade:** `cubic-bezier(0.22, 1, 0.36, 1)` — out-quint, panel open/close
- **kinetic:** `cubic-bezier(0.16, 1.11, 0.3, 1)` — strong overshoot, display text slams

**Component Timing:**
- Sidebar item: 80ms stamp
- Button hover: 100ms stamp
- Button active: 60ms press
- Toggle: 120ms stamp
- Chip: 100ms stamp
- Card hover: 120ms stamp
- Input: 120ms jitter
- Ghost button: 100ms stamp
- Display text: 250ms kinetic
- Card entry: 200ms stamp
- Modal: 200ms stamp
- Panel: 300ms cascade
- Stagger delay: 35ms (RAPID)

**Active press scales:**
- Nav items: 0.97
- Chips: 0.95
- Buttons primary: translate(2px, 2px) + shadow: none
- Buttons ghost: 0.90
- Tabs: 0.93

---

## Component Quick-Reference

### Primary Button
- Rest: `bg: #E6166E`, `border: 2px solid #E6166E`, `color: #FFF8EE`, `radius: 6px`, `h: 38px`, `shadow: shadow-magenta`, uppercase
- Hover: shadow grows to `4px 4px`, `transform: translate(-1px, -1px)`
- Active: shadow none, `transform: translate(2px, 2px)` (registration collapses)
- Transition: 100ms stamp

### Text Input
- Rest: `bg: #FFFAF0`, `border: 2px solid border-base @ 25%`, `radius: 6px`, `h: 44px`, `shadow: shadow-input`, `caret: #E6166E`
- Hover: border @ 35%, shadow-input-hover
- Focus: focus ring + shadow-input-focus
- Transition: 120ms jitter

### Card
- Rest: `bg: #FFFAF0`, `border: 1.5px solid border-base @ 25%`, `radius: 8px`, `shadow: shadow-card`, `padding: 20px`
- Hover: shadow-card-hover, `transform: translate(-1px, -1px)`, border @ 35%
- Transition: 120ms stamp

---

## Section Index (from full.md)

1. [Identity & Philosophy](#identity--philosophy) — Line 46
2. [Color System](#color-system) — Line 76
3. [Typography Matrix](#typography-matrix) — Line 141
4. [Elevation System](#elevation-system) — Line 184
5. [Border System](#border-system) — Line 227
6. [Component States](#component-states) — Line 269
7. [Motion Map](#motion-map) — Line 385
8. [Overlays](#overlays) — Line 444
9. [Layout Tokens](#layout-tokens) — Line 499
10. [Accessibility Tokens](#accessibility-tokens) — Line 549
11. [Visual Style](#visual-style) — Line 586
12. [Signature Animations](#signature-animations) — Line 645
13. [Data Visualization](#data-visualization) — Line 867
14. [Dark Mode Variant](#dark-mode-variant) — Line 882
15. [Mobile Notes](#mobile-notes) — Line 930
16. [Implementation Checklist](#implementation-checklist) — Line 960

---

## Critical Rules

- **ZERO gradients** — all fills are flat solid color
- **Registration offset shadows ONLY** — zero blur radius on all box-shadow
- **Saturated accent colors in zones** — magenta/indigo/saffron placed deliberately, not scattered
- **Bricolage Grotesque for Display/Heading/Subheading ONLY** — DM Sans for all other roles
- **Cotton is the white** — lightest surface is `#FFFAF0`, not pure `#FFFFFF`
- **Halftone grain overlay** — SVG feTurbulence at 3.5% opacity, multiply blend
- **Poster-scale typography** — Display 48px/800 weight dominates
- **Kinetic motion** — stamp easing with overshoot is signature, rapid 35ms stagger
- **Indigo focus ring** — `rgba(42,27,140,0.55)` 3px solid
- **Magenta shadow = clickable** — primary actions use shadow-magenta, standard elements use indigo shadows

---

## Mobile Adjustments

- Disable grain overlay (expensive compositing)
- Disable registration offset on text pseudo-elements
- Reduce shadow offsets by 40% (3px → 2px, 4px → 2px, 6px → 4px)
- Reduce border widths by 0.5px
- Display text: `clamp(28px, 8vw, 48px)`
- Label tracking: 0.1em → 0.06em
- Stagger delays: 35ms → 18ms

---

## Layout Quick Values

- Content max-width: 800px
- Narrow max-width: 680px
- Sidebar width: 280px
- Header height: 52px
- Spacing scale: 4, 6, 8, 12, 16, 20, 24, 32, 40, 48px
- Density: moderate-dense
- Breakpoints: sm 640px, md 768px, lg 1024px
