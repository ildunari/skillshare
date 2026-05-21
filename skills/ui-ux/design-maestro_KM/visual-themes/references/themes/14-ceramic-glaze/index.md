# Ceramic Glaze — Quick Reference

> Soft tactile ceramic -- viscous spring animation, rounded surfaces, cobalt glaze pooling in curves.

**Best for:** Lifestyle apps, wellness platforms, creative tools, note-taking, personal dashboards, portfolio sites, recipe apps, ceramics and craft marketplaces, meditation and journaling apps, cozy SaaS products.

**Decision principle:** "When in doubt, ask: does this feel like it was shaped by hands on a potter's wheel? If it feels machine-cut, round it. If it feels weightless, add spring damping. If it feels cold, warm it."

---

## Color Tokens

| Token | Hex | Role |
|---|---|---|
| page | `#E6DDD0` | Deepest background -- wooden workbench |
| bg | `#F0E6D6` | Primary surface -- bisque clay |
| surface | `#F8F3EC` | Cards, inputs, elevated surfaces -- porcelain slip |
| recessed | `#E8DFD2` | Code blocks, inset areas -- raw clay |
| active | `#DDD3C4` | Active/pressed states, user bubble -- warm stoneware |
| text-primary | `#33291F` | Headings, body text -- fired umber |
| text-secondary | `#706557` | Sidebar items, secondary labels -- kiln ash |
| text-muted | `#9E9487` | Placeholders, timestamps, metadata -- dust |
| text-onAccent | `#F8F3EC` | Text on accent backgrounds -- slip white |
| border-base | `#C4B8A6` | Base border (variable opacity) -- kiln wash |
| accent-primary | `#2B5EA7` | Brand accent, primary CTA -- cobalt glaze |
| accent-secondary | `#7FAD8E` | Secondary accent, tags -- celadon |
| success | `#5D9E6A` | Positive states -- copper green |
| warning | `#C48B2F` | Caution states -- amber flux |
| danger | `#B84E42` | Error states -- iron red |
| info | `#5E8BC4` | Informational states -- light cobalt |
| inlineCode | `#1E4F8A` | Code text in prose -- dark cobalt |
| toggleActive | `#2B5EA7` | Toggle/switch active track |
| selection | `rgba(43, 94, 167, 0.16)` | `::selection` background |

**Border Opacity:** subtle 15%, card 25%, hover 30%, focus 40%

---

## Typography

| Role | Family | Size | Weight | Line-height | Spacing |
|---|---|---|---|---|---|
| Display | DM Sans | 38px | 300 | 1.2 | -0.02em |
| Heading | DM Sans | 24px | 500 | 1.3 | -0.01em |
| Subheading | DM Sans | 18px | 500 | 1.35 | normal |
| Body | Figtree | 16px | 400 | 1.55 | normal |
| Body Small | Figtree | 14px | 400 | 1.4 | normal |
| Button | Figtree | 14px | 500 | 1.4 | 0.01em |
| Input | Figtree | 14px | 430 | 1.4 | normal |
| Label | Figtree | 12px | 400 | 1.33 | 0.02em |
| Code | Geist Mono | 0.9em | 360 | 1.5 | normal |

**Family switch:** DM Sans for Display/Heading/Subheading. Figtree for all else.

---

## Elevation

**Strategy:** Subtle shadows with soft, rounded edges.

**Shadows:**
- `shadow-sm`: `0 1px 3px rgba(51,41,31,0.04), 0 1px 2px rgba(51,41,31,0.03)`
- `shadow-card`: `0 2px 8px rgba(51,41,31,0.05), 0 0 0 0.5px rgba(196,184,166,0.20)`
- `shadow-card-hover`: `0 4px 16px rgba(51,41,31,0.07), 0 0 0 0.5px rgba(196,184,166,0.30)`
- `shadow-input`: `0 2px 12px rgba(51,41,31,0.04), 0 0 0 0.5px rgba(196,184,166,0.20)`
- `shadow-input-hover`: `0 3px 16px rgba(51,41,31,0.05), 0 0 0 0.5px rgba(196,184,166,0.30)`
- `shadow-input-focus`: `0 4px 20px rgba(51,41,31,0.07), 0 0 0 0.5px rgba(196,184,166,0.35)`
- `shadow-popover`: `0 4px 24px rgba(51,41,31,0.12), 0 2px 6px rgba(51,41,31,0.06)`

**Backdrop Blur:** popover 20px, modal 10px, badge 8px

---

## Border System

**Base color:** `#C4B8A6` (Kiln Wash)

**Widths:** hairline 0.5px, default 1px, medium 1.5px, heavy 2px

**Patterns:**
- subtle: `0.5px solid rgba(196,184,166,0.15)` — sidebar edges, hairlines
- card: `0.5px solid rgba(196,184,166,0.25)` — card borders
- hover: `0.5px solid rgba(196,184,166,0.30)` — hover states
- input: `1px solid rgba(196,184,166,0.15)` — form inputs at rest
- input-hover: `1px solid rgba(196,184,166,0.30)` — form inputs on hover

**Focus ring:** `2px solid rgba(43,94,167,0.45)`, offset 2px (cobalt at 45%)

---

## Component Quick-Reference

### Button (Primary/Outlined)
- Rest: `bg transparent`, `border 1px rgba(196,184,166,0.30)`, `radius 12px`, `h 36px`, `padding 0 16px`
- Hover: `bg #E8DFD2`, `border rgba(196,184,166,0.35)`, `shadow-sm`
- Active: `scale(0.97)`
- Transition: `250ms viscous-spring`

### Button (Accent/CTA)
- Rest: `bg #2B5EA7`, `color #F8F3EC`, `radius 12px`, `h 36px`, `padding 0 20px`, `shadow-sm`
- Hover: `bg #244F8E`, cobalt-tinted shadow `0 2px 12px rgba(43,94,167,0.20)`
- Active: `scale(0.97)`
- Transition: `250ms viscous-spring`

### Input (Settings Form)
- Rest: `bg #F8F3EC`, `border 1px rgba(196,184,166,0.15)`, `radius 12px`, `h 44px`, `padding 0 14px`, `caret-color #2B5EA7`
- Hover: `border rgba(196,184,166,0.30)`, `shadow-sm`
- Focus: cobalt focus ring, `border rgba(196,184,166,0.30)`
- Transition: `250ms viscous-spring`

### Chat Input Card
- Rest: `bg #F8F3EC`, `radius 24px`, `border 1px transparent`, `shadow-input`
- Hover: `shadow-input-hover`
- Focus-within: `shadow-input-focus`
- Transition: `300ms viscous-spring`

### Card
- Rest: `bg #F8F3EC`, `border 0.5px rgba(196,184,166,0.20)`, `radius 16px`, `shadow-card`, `padding 24px`
- Hover: `border rgba(196,184,166,0.30)`, `shadow-card-hover`
- Transition: `300ms viscous-spring`

---

## Motion

**Easings:**
- `viscous-spring`: `cubic-bezier(0.23, 1.2, 0.52, 1)` — signature easing, slight overshoot
- `viscous-spring-heavy`: `cubic-bezier(0.18, 1.35, 0.45, 1)` — heavier overshoot
- `default`: `cubic-bezier(0.4, 0, 0.2, 1)` — standard ease-in-out
- `out-quart`: `cubic-bezier(0.165, 0.85, 0.45, 1)` — snappy deceleration
- `out-expo`: `cubic-bezier(0.19, 1, 0.22, 1)` — smooth open/close
- `settle`: `cubic-bezier(0.34, 1.1, 0.64, 1)` — gentle settle

**Durations:**
- Sidebar item: 150ms out-quart
- Button hover: 250ms viscous-spring
- Toggle/chip: 250ms viscous-spring
- Card hover: 300ms viscous-spring
- Input card: 300ms viscous-spring
- Ghost icon: 350ms viscous-spring
- Page entry: 400ms viscous-spring-heavy
- Modal entry: 350ms viscous-spring-heavy
- Panel open/close: 500ms out-expo

**Active Press:** nav 0.985, chip 0.995, button 0.97, tab 0.95, card 0.99

---

## Layout

- Content max-width: 768px
- Narrow max-width: 672px
- Sidebar width: 288px
- Header height: 48px
- Spacing scale: `4, 6, 8, 12, 16, 20, 24, 28, 32, 40px`
- Density: comfortable
- Breakpoints: sm 640px, md 768px, lg 1024px

---

## Accessibility

- Focus ring: `2px solid rgba(43,94,167,0.45)`, offset 2px
- Disabled: opacity 0.5, pointer-events none, shadow none
- Selection: `bg rgba(43,94,167,0.16)`, `color #33291F`
- Scrollbar: `thin`, thumb `rgba(196,184,166,0.35)`, track transparent
- Min touch target: 44px
- Contrast: WCAG AA (4.5:1 text, 3:1 large text)

---

## Section Index

1. [Identity & Philosophy](#identity--philosophy) — Core tension: softness vs weight. Everything is rounded, smooth, approachable, but has mass. Viscous spring physics.
2. [Color System](#color-system) — Warm bisque neutrals (hue 28-36), cobalt blue accent (pooling glaze), celadon secondary, desaturated semantics.
3. [Typography Matrix](#typography-matrix) — DM Sans for display/heading/subheading. Figtree for body and below. Geist Mono for code.
4. [Elevation System](#elevation-system) — Soft diffused shadows with large blur radii. No hard edges. Backdrop blur on popovers.
5. [Border System](#border-system) — Single base color (`#C4B8A6`) at variable opacity (15/25/30/40%). Cobalt focus ring.
6. [Component States](#component-states) — Full state machines for buttons, inputs, cards, sidebar items, chips, toggles, user bubbles.
7. [Motion Map](#motion-map) — Viscous spring easing throughout. 250-400ms durations. Framer Motion: stiffness 150, damping 15.
8. [Overlays](#overlays) — Popover (16px radius, 20px blur), modal (20px radius, 28px padding), tooltip (8px radius, 400ms delay).
9. [Layout Tokens](#layout-tokens) — Comfortable density. 768px content width. Spacing 4-40px scale.
10. [Accessibility Tokens](#accessibility-tokens) — Cobalt focus ring, 44px touch targets, WCAG AA verified.
11. [Visual Style](#visual-style) — 1.5% grain overlay (SVG feTurbulence). Matte surfaces. No gradients on surfaces.
12. [Signature Animations](#signature-animations) — Glaze Pool (cobalt shadow on hover), Viscous Settle (page entry overshoot), Clay Press (button spring-back), Kiln Glow (warm shimmer), Wheel Spin (toggle slide).
13. [Dark Mode Variant](#dark-mode-variant) — Inverted surface hierarchy. Warm undertones preserved. Cobalt lifted to `#3D7AC7`.
14. [Data Visualization](#data-visualization) — Cobalt primary, celadon secondary, 3 hues max. Rounded bar ends. Low-ink grid.
15. [Mobile Notes](#mobile-notes) — Disable grain, reduce blur, compress durations 30%, reduce spacing scale.
16. [Implementation Checklist](#implementation-checklist) — 22-point verification list.
