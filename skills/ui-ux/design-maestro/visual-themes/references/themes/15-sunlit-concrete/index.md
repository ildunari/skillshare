# Sunlit Concrete — Quick Reference

> Industrial daylight rendered as interface — where safety colors carry meaning, condensed type carries density, and every readout is visible from across the room.

**Best for:** Manufacturing dashboards, factory control rooms, SCADA/HMI interfaces, industrial IoT monitoring, safety compliance panels, warehouse management, fleet operations, equipment health dashboards.

**Mood:** Dense, functional, industrial, safety-aware, readable-from-distance
**Decision principle:** "Can the operator read this from across the room?"

---

## Color Tokens (Complete)

### Neutrals
- `page` — Raw Concrete `#E8E3DB` (L=0.91 C=0.012 h=80)
- `bg` — Sealed Concrete `#F0ECE5` (L=0.94 C=0.011 h=80)
- `surface` — Daylit Panel `#F8F5F0` (L=0.97 C=0.008 h=80)
- `recessed` — Shadow Concrete `#D9D3C9` (L=0.85 C=0.015 h=80)
- `active` — Pressed Slab `#CFC8BC` (L=0.82 C=0.018 h=80)

### Text
- `text-primary` — Shop Floor Black `#2C2A26` (L=0.22)
- `text-secondary` — Worn Stencil `#5C5850` (L=0.41)
- `text-muted` — Dust Grey `#8A857C` (L=0.58)
- `text-onAccent` — Safety White `#FFFFFF`

### Borders
- `border-base` — Rebar Seam `#9E9890` (L=0.64, used at variable opacity)
  - Subtle: 12% | Card: 22% | Hover: 35% | Focus: 50% | Heavy: 60%

### Accents & Semantics
- `accent-primary` — Steel Blue `#4A7FA5` (L=0.56 C=0.08 h=240)
- `accent-secondary` — OSHA Orange `#E8651A` (L=0.60 C=0.18 h=55)
- `success` — Operational Green `#3D8B37` (L=0.52 C=0.12 h=142)
- `warning` — Threshold Amber `#D4940A` (L=0.67 C=0.15 h=85)
- `danger` — Stop Red `#CC2936` (L=0.45 C=0.17 h=25)
- `info` — Steel Blue `#4A7FA5` (same as accent-primary)

### Special
- `inlineCode` — `#B85A18` (darkened orange)
- `toggleActive` — `#3D8B37` (operational green)
- `selection` — `rgba(74,127,165,0.22)` (steel blue 22%)
- `kpiHighlight` — `#E8651A` (OSHA orange)
- `kpiCritical` — `#CC2936` (stop red)

---

## Typography (All 9 Roles)

| Role | Family | Size | Weight | Line | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| **KPI Display** | Barlow Condensed | 56px | 700 | 1.0 | -0.02em | `tabular-nums` | Large metric readouts, hero numbers |
| **Display** | Barlow Condensed | 28px | 600 | 1.15 | -0.01em | — | Page titles, section heroes |
| **Heading** | Barlow Condensed | 18px | 600 | 1.25 | 0.01em | `uppercase` | Section titles, card headers |
| **Body** | Barlow | 15px | 400 | 1.55 | normal | — | Primary reading text |
| **Body Small** | Barlow | 13px | 400 | 1.45 | normal | — | Sidebar, labels, secondary UI |
| **Button** | Barlow | 14px | 600 | 1.4 | 0.03em | `uppercase` | Button labels |
| **Input** | Barlow | 14px | 400 | 1.4 | normal | — | Form input text |
| **Label** | Barlow Condensed | 11px | 500 | 1.3 | 0.06em | `uppercase` | Metadata, timestamps, axis labels |
| **Code** | IBM Plex Mono | 13px | 400 | 1.55 | normal | `"zero", "tnum"` | Inline code, serial numbers |
| **Caption** | Barlow | 11px | 400 | 1.33 | normal | — | Disclaimers, footnotes |
| **KPI Unit** | Barlow Condensed | 18px | 500 | 1.0 | 0.02em | `uppercase` | Unit labels (PSI, RPM, °C) |

**Font Load:**
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
```

---

## Elevation

**Strategy:** Hard-shadows (directional overhead lighting)

**Shadow Tokens:**
- `shadow-sm` — `0 2px 0 rgba(44,42,38,0.08)` (hard 2px drop, zero blur)
- `shadow-card` — `0 3px 0 rgba(44,42,38,0.10), 0 1px 0 rgba(44,42,38,0.05)`
- `shadow-card-hover` — `0 4px 1px rgba(44,42,38,0.12), 0 1px 0 rgba(44,42,38,0.06)`
- `shadow-input` — `0 2px 0 rgba(44,42,38,0.06), 0 0 0 1px rgba(158,152,144,0.22)`
- `shadow-input-hover` — `0 2px 0 rgba(44,42,38,0.08), 0 0 0 1px rgba(158,152,144,0.35)`
- `shadow-input-focus` — `0 2px 0 rgba(44,42,38,0.08), 0 0 0 2px rgba(74,127,165,0.50)`
- `shadow-popover` — `0 6px 1px rgba(44,42,38,0.15), 0 2px 0 rgba(44,42,38,0.08)`
- `shadow-kpi` — `0 4px 0 rgba(44,42,38,0.12)` (extra-hard, zero blur)

**Recipe:** Hard directional shadows from overhead + concrete tint-stepping. Shadows drop straight down (Y+ only), minimal blur (0-1px). Each surface level gets progressively lighter.

---

## Border System

**Radius:**
- `none` 0px | `sm` 3px | `md` 4px | `lg` 6px | `xl` 8px | `input` 4px | `full` 9999px (LEDs only)

**Patterns:**
- Subtle: 1px @ 12% (dividers, internal rules)
- Card: 1px @ 22% (card edges, input rest)
- Hover: 1px @ 35% (hovered elements)
- Heavy: 2px @ 60% (major dividers)
- Safety-left: 3px @ 100% (alarm accent borders)

**Focus Ring:**
- Color: `rgba(74,127,165,0.56)` (steel blue)
- Width: 2px solid, offset 2px
- On safety backgrounds: `rgba(255,255,255,0.70)` (white)

---

## Motion

**Core Philosophy:** Pneumatic motion — sharp starts, hard stops. Industrial actuators, not springs.

**Easings:**
- `pneumatic` — `cubic-bezier(0.7, 0, 0.3, 1)` (primary, sharp attack/stop)
- `mechanical` — `linear` (gauges, progress bars — constant velocity)
- `brake` — `cubic-bezier(0.0, 0.0, 0.2, 1.0)` (panels, larger movements)
- `instant` — `steps(1)` (alarm state changes)

**Durations:**
- Button hover: 120ms pneumatic
- Button press: 80ms pneumatic
- Sidebar item: 100ms pneumatic
- Toggle: 150ms pneumatic
- Input focus: 100ms pneumatic
- Card hover: 150ms pneumatic
- Panel open/close: 200ms brake
- Modal entry: 250ms brake
- Gauge fill: 300ms mechanical
- Alarm state: 0ms instant

**Active Press:** `translateY(1px)` for buttons/nav (downward press, not scale)

---

## Component Quick-Reference

### Button (Primary)
- Rest: bg `accent-primary`, color white, h 36px, radius md, shadow-sm
- Hover: bg darkened 12%, shadow-card, 120ms pneumatic
- Active: bg darkened 22%, shadow-sm, `translateY(1px)`, 80ms
- Focus: focus ring (steel blue)

### Input
- Rest: bg `surface`, border 1px @ 22%, h 40px, radius md, shadow-input
- Hover: border @ 35%, shadow-input-hover, 100ms pneumatic
- Focus: border 2px `accent-primary`, shadow-input-focus, outline none
- Error: border 2px `danger`, red focus ring

### Card (Standard)
- Rest: bg `surface`, border 1px @ 22%, radius lg, shadow-card, padding 16px
- Hover: border @ 35%, shadow-card-hover, 150ms pneumatic
- Active: border `accent-primary` @ 60%

### KPI Readout Card (Signature Component)
- Rest: bg `surface`, border 1px @ 22%, radius lg, shadow-kpi, padding 16px-20px
- Normal: number `text-primary`, label `text-muted`
- Warning: number `warning`, left border 3px amber
- Caution: number `text-primary`, bg tint orange 6%, bottom border 3px OSHA orange
- Critical: number `danger`, bg tint red 6%, full border 2px red, shadow gains red tint

**KPI Card Anatomy:**
```
LABEL (11px uppercase condensed, muted)

1,247.3  PSI  ← KPI Display (56px) + Unit (18px)
▲ +12.4% from last hour  ← Delta (13px, green if positive)
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬░░░░░  ← Threshold bar (optional)
```

---

## Section Index (from full.md)

- **Identity & Philosophy** — Line 50
- **Color System** — Line 87 (Palette, Special Tokens, Opacity, Rules)
- **Typography Matrix** — Line 143
- **Elevation System** — Line 180 (Strategy: hard-shadows, Surface Hierarchy, Shadow Tokens, Separation Recipe)
- **Border System** — Line 218 (Radius, Widths/Patterns, Focus Ring)
- **Component States** — Line 257 (Buttons Primary/Safety/Ghost, Input, KPI Card, Cards, Sidebar, Chips, Toggle, Tabs, Status Indicators)
- **Motion Map** — Line 400 (Easings, Duration×Easing×Component, Active Press Scale)
- **Layout Tokens** — Line 449 (Content max-width 1200px, spacing scale, density: dense, responsive notes)
- **Accessibility Tokens** — Line 484 (Focus ring, disabled, selection, scrollbar, touch targets 44px, WCAG AA)
- **Overlays** — Line 518 (Popover, Modal, Tooltip, Command Palette)
- **Visual Style** — Line 576 (Material: concrete grain 3% SVG noise, hard directional lighting, data viz philosophy)
- **Signature Animations** — Line 630
  1. Pneumatic Actuator Press (translateY press)
  2. Gauge Fill (linear constant-velocity fill)
  3. Alarm Pulse (hard blink, steps(2))
  4. Panel Slide (brake easing, 200ms)
  5. KPI Number Snap (exit up, enter down, 180ms)
  6. Stagger Load (40ms delay, power-on effect)
- **Dark Mode Variant** — Line 806 (Night shift control room, safety colors brighten, shadows→near-black, grain→soft-light 4%)
- **Mobile Notes** — Line 855 (Disable: grain, stagger, KPI snap. Adjustments: KPI 56px→36px, sidebar overlay, touch 44px)
- **Implementation Checklist** — Line 889 (42 items)

---

## Key Distinctions

**Safety Color Semantics (OSHA/ANSI):**
- Orange = caution, attention required (NEVER decorative)
- Red = danger, stop, critical alarm
- Green = operational, safe, within tolerance
- Amber = warning, approaching threshold
- Steel blue = informational, interactive (the ONLY non-safety color)

**KPI Display Role (Unique to this theme):**
- Barlow Condensed 56px/700, `tabular-nums`
- Largest text in the entire roster
- Can scale 40-72px depending on context
- Paired with KPI Unit role (18px condensed uppercase)

**Material Identity:**
- Warm concrete grey (hue ~80, yellow-ochre undertone)
- Concrete grain: SVG feTurbulence @ 3% opacity, multiply blend
- Hard directional lighting: shadows drop straight down (Y+ only), 0-1px blur
- Matte finish everywhere (no gloss except toggle thumb)

**What This Theme Is NOT:**
- Not dark (sunlit factory floor, not night terminal)
- Not delicate (no hairline borders, no subtle shadows)
- Not decorative (safety colors carry meaning, not aesthetics)
- Not minimal (dense, information-rich dashboards)
- Not cool-toned (concrete is warm, not blue-grey)

---

## Dark Mode Key Changes

- Surfaces darken: page `#1C1B18`, bg `#252420`, surface `#2F2E29`
- Safety colors BRIGHTEN 15-20% for contrast
- Shadows: warm-grey → near-black `rgba(0,0,0,0.25)`, blur 1-2px
- Grain: multiply → soft-light @ 4% opacity
- Border opacity: 8% / 15% / 25% / 40%
- Focus ring: steel blue `rgba(107,163,204,0.65)`

---

## Critical Implementation Notes

- [ ] All numeric displays use `tabular-nums`
- [ ] Heading/Button/Label use `text-transform: uppercase`
- [ ] IBM Plex Mono with `font-feature-settings: "zero", "tnum"`
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] Shadows: Y-offset only, 0-1px blur, warm-grey tone
- [ ] Button press: `translateY(1px)` (down), not `scale()`
- [ ] Toggle ON state: green (`success`), not accent-primary
- [ ] Alarm state changes: 0ms instant (safety first)
- [ ] Concrete grain: desktop only (disable on mobile for GPU performance)
- [ ] KPI grid: `auto-fit, minmax(280px, 1fr)` responsive columns
- [ ] Content max-width: 1200px (wider for dashboard layouts)
- [ ] Touch targets: 44px minimum on mobile
- [ ] Reduced motion: all transitions → 0ms, pulse → static

---

**Identity in one sentence:** Industrial control room flooded with daylight, where massive condensed numbers dominate the screen, safety colors follow OSHA standards, and every element is designed to be read from across the factory floor.
