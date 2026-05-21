# 10. Solarpunk Brass — Quick Reference

> A greenhouse full of technology -- vine-covered circuits, polished brass instruments, warm sunlight through green glass, where organic and mechanical coexist.

**Best for:** Environmental dashboards, botanical databases, sustainable tech platforms, smart garden interfaces, IoT sensor displays, permaculture planning tools

---

## Color Tokens

| Token | Hex | Role |
|---|---|---|
| **Neutrals** | | |
| page | `#EDE7D9` | Greenhouse Linen — deepest background |
| bg | `#F4EFE4` | Sunlit Parchment — primary surface |
| surface | `#FAF7F0` | Bleached Cotton — cards, inputs, elevated |
| recessed | `#E3DDD0` | Potting Soil Tint — code blocks, inset |
| active | `#D9D2C3` | Pressed Linen — active/pressed items |
| **Text** | | |
| text-primary | `#2C2A24` | Workshop Ink — headings, body |
| text-secondary | `#6E6959` | Weathered Label — secondary labels |
| text-muted | `#928C7E` | Aged Paper — placeholders, timestamps |
| text-onAccent | `#FAF7F0` | Bleached Cotton — text on accent backgrounds |
| **Borders** | | |
| border-base | `#B8B0A0` | Trellis Wire — at variable opacity |
| **Accents** | | |
| accent-primary | `#C19A49` | Polished Brass — primary accent |
| accent-secondary | `#4A7C59` | Greenhouse Glass — secondary accent |
| **Semantics** | | |
| success | `#5B8C4A` | Spring Growth — positive states |
| warning | `#B8892E` | Aged Brass — caution states |
| danger | `#A04535` | Kiln Brick — error states |
| info | `#4D8A7A` | Patina Verdigris — informational |
| **Special** | | |
| inlineCode | `#7A6830` | Darkened brass for code text |
| toggleActive | `#5B8C4A` | Spring Growth — toggle on state |
| selection | `rgba(193,154,73,0.20)` | Brass at 20% — text selection |
| brass-highlight | `#D4AA55` | Lighter brass for hover shimmer |
| brass-muted | `rgba(193,154,73,0.30)` | Brass at 30% — decorative lines |
| brass-subtle | `rgba(193,154,73,0.12)` | Brass at 12% — hover tints |
| patina-green | `#6BA38E` | Verdigris — decorative brass accents |

**Opacity Scale (border-base):** subtle 12%, card 20%, hover 30%, focus 40%, emphasis 50%

---

## Typography

| Role | Family | Size | Weight | Line-height | Spacing | Features |
|---|---|---|---|---|---|---|
| Display | Fraunces | 36px | 400 | 1.2 | -0.02em | WONK 1, opsz 36, liga, kern |
| Heading | Fraunces | 24px | 500 | 1.3 | -0.01em | WONK 1, opsz 24 |
| Subheading | Fraunces | 19px | 500 | 1.4 | normal | WONK 0, opsz 19 |
| Body | DM Sans | 16px | 400 | 1.55 | normal | kern |
| Body Small | DM Sans | 14px | 400 | 1.45 | normal | -- |
| Button | DM Sans | 14px | 500 | 1.4 | 0.02em | -- |
| Input | DM Sans | 14px | 430 | 1.4 | normal | kern |
| Label | DM Sans | 12px | 500 | 1.33 | 0.04em | uppercase |
| Code | IBM Plex Mono | 0.9em | 400 | 1.55 | normal | tabular-nums |
| Caption | DM Sans | 12px | 400 | 1.33 | 0.01em | -- |
| Data Value | IBM Plex Mono | 18px | 500 | 1.2 | -0.02em | tabular-nums, lining-nums |

**Duality:** Fraunces (organic, wonky) for display/headings. DM Sans (mechanical, precise) for body/UI. IBM Plex Mono for data.

---

## Elevation

**Strategy:** Dual-shadow — organic (soft, warm, botanical) vs. mechanical (tight, crisp, instrument-like)

**Organic Shadows:**
- sm: `0 2px 8px rgba(44,42,36,0.04), 0 1px 3px rgba(44,42,36,0.03)` — cards at rest
- md: `0 4px 14px rgba(44,42,36,0.06), 0 2px 4px rgba(44,42,36,0.03)` — card hover
- focus: `0 4px 14px rgba(44,42,36,0.06), 0 0 0 2px rgba(193,154,73,0.45)` — input focus
- overlay: `0 8px 24px rgba(44,42,36,0.08), 0 2px 6px rgba(44,42,36,0.04)` — popovers, modals

**Mechanical Shadows:**
- sm: `0 1px 3px rgba(44,42,36,0.08), 0 0.5px 1px rgba(44,42,36,0.06)` — instrument rest
- md: `0 2px 4px rgba(44,42,36,0.10), 0 1px 2px rgba(44,42,36,0.06)` — instrument hover
- active: `0 0.5px 1px rgba(44,42,36,0.10)` — pressed mechanical
- bezel: `inset 0 1px 0 rgba(255,255,255,0.08), 0 1px 3px rgba(44,42,36,0.10)` — brass bezel

**Assignment:** Content cards → organic. Data panels → mechanical. Inputs → organic (rest) to mechanical (focus).

---

## Borders

**Widths:** hairline 0.5px, default 1px, medium 1.5px, heavy 2px

**Focus Ring:** `rgba(193,154,73,0.50)` brass, 2px solid, 2px offset
Implementation: `box-shadow: 0 0 0 2px #F4EFE4, 0 0 0 4px rgba(193,154,73,0.50)`

---

## Motion

**Dual Language:** Organic (200-700ms, grow/unfurl/settle) for content. Mechanical (80-130ms, click/precise) for controls.

**Easings:**
- default: `cubic-bezier(0.4, 0, 0.2, 1)`
- click: `cubic-bezier(0.2, 0, 0, 1)` — mechanical snap
- precise: `cubic-bezier(0.25, 0.1, 0.1, 1)` — data updates
- grow: `cubic-bezier(0.22, 1.2, 0.36, 1)` — organic overshoot
- unfurl: `cubic-bezier(0.12, 0.8, 0.3, 1)` — slow organic reveal
- settle: `cubic-bezier(0.22, 1, 0.36, 1)` — organic ease-out

**Durations:**
- Mechanical: 80ms (data tick), 100ms (button press), 120ms (button hover), 130ms (toggle)
- Organic: 200ms (sidebar), 250ms (input border), 350ms (card border), 400ms (chat card), 450ms (card shadow), 500ms (panel), 600ms (modal/reveal), 700ms (page entry)

**Active Press:** nav 0.985, chips 0.995, buttons 0.97, data cards 0.99, tabs 0.96

**Reduced Motion:** Organic cap 200ms, mechanical cap 100ms, ambient animations disabled

---

## Component Quick-Reference

**Primary Button:**
Rest: bg `#C19A49`, color `#FAF7F0`, radius 6px, h 36px, shadow mechanical-sm
Hover: darker brass, shadow mechanical-md
Active: scale(0.97), shadow mechanical-active
Transition: 120ms default (mechanical)

**Text Input:**
Rest: bg `#FAF7F0`, border `1px solid rgba(184,176,160,0.15)`, radius 8px, h 44px, caret-color `#C19A49`
Hover: border 25% opacity, shadow organic-sm
Focus: border `1px solid rgba(193,154,73,0.40)`, shadow organic-focus
Transition: border-color 250ms ease-out, box-shadow 350ms ease-out (organic)

**Card:**
Rest: bg `#FAF7F0`, border `0.5px solid rgba(184,176,160,0.20)`, radius 10px, shadow organic-sm
Hover: border 25%, shadow organic-md
Transition: border-color 350ms ease-out, box-shadow 450ms grow (organic)

**Toggle:**
Track: 40x22px, off `rgba(184,176,160,0.25)`, on `#5B8C4A` (Spring Growth)
Thumb: 18px, shadow mechanical-sm
Transition: 130ms default (mechanical)

---

## Section Index (full.md)

- [Identity & Philosophy](#identity--philosophy) — Line 26
- [Color System](#color-system) — Line 48
- [Typography Matrix](#typography-matrix) — Line 123
- [Elevation System](#elevation-system) — Line 181
- [Border System](#border-system) — Line 242
- [Component States](#component-states) — Line 289
- [Motion Map](#motion-map) — Line 435
- [Overlays](#overlays) — Line 494
- [Layout Tokens](#layout-tokens) — Line 550
- [Accessibility Tokens](#accessibility-tokens) — Line 603
- [Visual Style](#visual-style) — Line 654
- [Signature Animations](#signature-animations) — Line 716
- [Dark Mode Variant](#dark-mode-variant) — Line 850
- [Mobile Notes](#mobile-notes) — Line 893
- [Data Visualization](#data-visualization) — Line 926
- [Theme-Specific Components](#theme-specific-components) — Line 942
- [CSS Custom Properties](#theme-specific-css-custom-properties) — Line 971
- [Implementation Checklist](#implementation-checklist) — Line 1071
