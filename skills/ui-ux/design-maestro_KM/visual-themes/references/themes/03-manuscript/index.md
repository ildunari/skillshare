# Manuscript — Quick Reference
> Living manuscripts -- serif typography as identity, paper as material metaphor.

**Schema:** v2 | **Mode:** Alchemical / Editorial | **Full spec:** `full.md` (746 lines)

---

## Color Tokens

### Alchemical Mode

| Token | Hex | Role |
|---|---|---|
| page | `#F8F4EC` | Deepest background (parchment) |
| bg | `#FDF6E3` | Primary surface (vellum) |
| surface | `#FFFBF3` | Elevated cards, inputs (laid paper) |
| recessed | `#EDE6D6` | Code blocks, inset (foxed paper) |
| active | `#E8DFD0` | Active/pressed states (blotting sand) |
| text-primary | `#1B2438` | Headings, body (iron gall ink) |
| text-secondary | `#5C5647` | Sidebar items (faded ink) |
| text-muted | `#7A7A70` | Placeholders (pencil lead) — WCAG AA |
| text-onAccent | `#FDF6E3` | Text on accents |
| border-base | `#8B7E6A` | Variable opacity (ruled line) |
| accent-primary | `#7B6840` | Primary CTA (oxidized copper) |
| accent-secondary | `#8B4513` | Links, annotations (sealing wax) |
| success | `#4A7C59` | Positive states (verdigris green) |
| warning | `#B8860B` | Caution (goldenrod) |
| danger | `#9B3A2E` | Errors (sienna red) |
| info | `#3B5998` | Informational (indigo ink) |
| inlineCode | `#7B6840` | Code in prose |
| toggleActive | `#4A7C59` | Toggle track active |
| selection | `rgba(123,104,64,0.18)` | `::selection` background |

### Editorial Mode

| Token | Hex | Role |
|---|---|---|
| page | `#FAF6EE` | Deepest background (ivory stock) |
| bg | `#FEFCF7` | Primary surface (warm white) |
| surface | `#FFFFFF` | Elevated cards, inputs (cotton) |
| recessed | `#EDEBE5` | Code blocks, inset (French grey) |
| active | `#E5E0D6` | Active/pressed states (pressed linen) |
| text-primary | `#1C1E23` | Headings, body (letterpress black) |
| text-secondary | `#555961` | Sidebar items (body grey) |
| text-muted | `#7A7A70` | Placeholders (caption grey) — WCAG AA |
| text-onAccent | `#FEFCF7` | Text on accents |
| border-base | `#9B9489` | Variable opacity (rule line) |
| accent-primary | `#7A5C3A` | Primary CTA (burnt umber) |
| accent-secondary | `#3A5A7C` | Links (printer's blue) |
| success | `#4A7C59` | Positive states (forest ink) |
| warning | `#B8860B` | Caution (ochre) |
| danger | `#9B3A2E` | Errors (crimson lake) |
| info | `#3B5998` | Informational (composing blue) |
| inlineCode | `#7A5C3A` | Code in prose |
| toggleActive | `#4A7C59` | Toggle track active |
| selection | `rgba(122,92,58,0.15)` | `::selection` background |

### Border Opacity System

| Level | Opacity | Usage |
|---|---|---|
| subtle | 15% | Panel edges, hairlines |
| card | 25% | Card borders, boundaries |
| hover | 35% | Hovered elements |
| heavy | 50% | Active/focused borders |

---

## Typography Roles

### Alchemical Mode
**Fonts:** EB Garamond (primary), Libre Caslon Text (blockquotes), IBM Plex Mono (code)

| Role | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|
| Display | 36px | 500 | 1.15 | -0.01em | `"opsz" 36, "liga" 1, "kern" 1` | Hero titles |
| Heading | 24px | 500 | 1.3 | normal | `"opsz" 24, "liga" 1` | Section titles |
| Body | 17px | 400 | 1.65 | normal | `"opsz" 17, "liga" 1, "onum" 1` | Primary reading text |
| Body Small | 15px | 400 | 1.55 | normal | `"opsz" 15` | Sidebar items |
| Button | 14px | 600 | 1.4 | 0.06em | **`"smcp" 1, "opsz" 14`** | Button labels (small caps) |
| Input | 16px | 400 | 1.5 | normal | `"opsz" 16, "liga" 1` | Form input text |
| Label | 12px | 400 | 1.33 | 0.04em | `"smcp" 1, "opsz" 12` | Metadata (small caps) |
| Code | 0.88em | 400 | 1.55 | normal | `"liga" 0` | Code blocks |
| Caption | 12px | 400 | 1.4 | normal | `"opsz" 12` | Footnotes |

### Editorial Mode
**Fonts:** Newsreader (display/heading), Source Serif 4 (body), JetBrains Mono (code)

| Role | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|
| Display | 36px | 500 | 1.15 | -0.01em | `"opsz" 36, "liga" 1` | Hero titles |
| Heading | 24px | 500 | 1.3 | normal | `"opsz" 24` | Section titles |
| Body | 17px | 400 | 1.65 | normal | `"opsz" 17, "liga" 1` | Primary reading text |
| Body Small | 15px | 400 | 1.5 | normal | `"opsz" 15` | Sidebar items |
| Button | 14px | 600 | 1.4 | 0.02em | `"opsz" 14` | Button labels (normal case) |
| Input | 16px | 400 | 1.5 | normal | `"opsz" 16` | Form input text |
| Label | 12px | 400 | 1.33 | 0.02em | -- | Metadata |
| Code | 0.88em | 400 | 1.55 | normal | `"liga" 1` | Code blocks (ligatures on) |
| Caption | 12px | 400 | 1.4 | normal | -- | Footnotes |

**Key difference:** Alchemical uses small caps for buttons/labels; Editorial uses normal case.

---

## Elevation Strategy

**Alchemical:** `borders-only` — Hard directional shadows (desk lamp upper-left), zero blur
**Editorial:** `subtle-shadows` — Whisper-thin composite shadows (drop + hairline ring)

### Shadow Tokens

| Token | Alchemical | Editorial |
|---|---|---|
| shadow-sm | `2px 3px 0 rgba(27,36,56,0.06)` | `0 1px 3px rgba(28,30,35,0.04)` |
| shadow-md | `3px 4px 0 rgba(27,36,56,0.08)` | `0 1px 2px rgba(28,30,35,0.05), 0 0 0 0.5px rgba(155,148,137,0.12)` |
| shadow-lg | `4px 5px 0 rgba(27,36,56,0.12)` | `0 2px 8px rgba(28,30,35,0.08), 0 0 0 0.5px rgba(155,148,137,0.15)` |
| shadow-hover | `4px 5px 0 rgba(27,36,56,0.10)` | `0 2px 6px rgba(28,30,35,0.07), 0 0 0 0.5px rgba(155,148,137,0.18)` |
| shadow-input-focus | `3px 4px 0 rgba(27,36,56,0.08), 0 0 0 2px rgba(123,104,64,0.35)` | `0 1px 2px rgba(28,30,35,0.05), 0 0 0 2px rgba(58,90,124,0.3)` |

**Separation recipe:**
- Alchemical: Warm surface stepping + ruled borders (15-50% opacity) + hard shadow on elevated elements
- Editorial: Subtle surface stepping + whisper composites + hairline borders (10-25% opacity)

---

## Border System

### Widths
- **hairline:** 0.5px (panel edges)
- **default:** 1px (cards, inputs, rules)
- **medium:** 1.5px (section dividers)
- **heavy:** 2px (focus indicators)

### Focus Ring
- **Alchemical:** `rgba(123, 104, 64, 0.35)` warm amber, 2px solid, 2px offset (with inner bg ring)
- **Editorial:** `rgba(58, 90, 124, 0.3)` blue-grey, 2px solid, 2px offset (with inner bg ring)

---

## Motion Personality

### Easings
- **Alchemical:** `ink-spread` (viscous, organic) — `cubic-bezier(0.25, 0.05, 0.15, 1)`
- **Alchemical:** `ink-ease` (sticky) — `cubic-bezier(0.3, 0.1, 0.2, 1)`
- **Editorial:** `ease-out` (invisible) — `cubic-bezier(0.25, 0.1, 0.25, 1)`
- **Editorial:** `ease-snap` (snappy) — `cubic-bezier(0.2, 0.8, 0.3, 1)`

### Duration Range
- **Alchemical:** 150-800ms (slow, viscous)
- **Editorial:** 75-350ms (fast, invisible)

### Press Scale
- **Nav items:** 0.985 (Alch), 0.99 (Edit)
- **Buttons:** 0.97 (Alch), 0.98 (Edit)
- **Chips:** 0.98 (Alch), 0.99 (Edit)

### Reduced Motion
- **Alchemical:** `fade-only` (200ms cap, all spatial animations collapse to opacity)
- **Editorial:** `instant` (100ms cap, all transitions near-zero duration)

---

## Key Component Quick-Reference

### Primary Button

**Alchemical:**
Rest: `bg #7B6840`, no border, `color #FDF6E3`, radius 4px, h 34px, **small caps**, shadow-desk-sm
Hover: `bg #6A5A36`
Active: `scale(0.97)`, `bg #5C4E2E`
Transition: bg 150ms ink-spread, transform 100ms ink-spread

**Editorial:**
Rest: `bg #7A5C3A`, no border, `color #FEFCF7`, radius 6px, h 34px, normal case, no shadow
Hover: `bg #6B4F30`, shadow-whisper-sm
Active: `scale(0.98)`, `bg #5E4428`
Transition: bg 100ms ease-out, transform 80ms ease-out

---

### Text Input

**Alchemical:**
Rest: `bg #FFFBF3`, border `1px solid rgba(139,126,106,0.25)`, radius 4px, h 44px, shadow-desk-sm, caret `#7B6840`
Hover: border 35%, shadow-desk-md
Focus: border `rgba(123,104,64,0.5)`, shadow-input-focus-alch
Transition: border 150ms ink-ease, box-shadow 200ms ink-ease

**Editorial:**
Rest: `bg #FFFFFF`, border `1px solid rgba(155,148,137,0.2)`, radius 6px, h 44px, shadow-whisper-md, caret `#7A5C3A`
Hover: border 30%, shadow-whisper-hover
Focus: border `rgba(58,90,124,0.4)`, shadow-input-focus-edit
Transition: border 100ms ease-out, box-shadow 120ms ease-out

---

### Card

**Alchemical:**
Rest: `bg #FFFBF3`, border `1px solid rgba(139,126,106,0.25)`, radius 4px, shadow-desk-md
Hover: border 35%, shadow-desk-hover
Transition: border 200ms ink-ease, box-shadow 250ms ink-ease

**Editorial:**
Rest: `bg #FFFFFF`, border `0.5px solid rgba(155,148,137,0.2)`, radius 8px, shadow-whisper-md
Hover: border 25%, shadow-whisper-hover
Transition: border 100ms ease-out, box-shadow 120ms ease-out

---

## Section Index (Full Spec)

- **Identity & Philosophy** → Line 16
- **Color System** → Line 38
  - Alchemical Mode Palette → Line 40
  - Editorial Mode Palette → Line 61
  - Special Tokens → Line 82
  - Opacity System → Line 90
  - Color Rules → Line 101
- **Typography Matrix** → Line 110
  - Alchemical Mode → Line 112
  - Editorial Mode → Line 131
  - Typographic Decisions → Line 148
  - Font Loading → Line 158
- **Elevation System** → Line 174
  - Alchemical Mode (Desk Lamp) → Line 180
  - Editorial Mode (Whisper Shadows) → Line 192
  - Shadow Tokens → Line 204
  - Separation Recipe → Line 222
- **Border System** → Line 229
  - Widths → Line 231
  - Opacity Scale → Line 240
  - Border Patterns → Line 249
  - Focus Ring → Line 262
- **Component States** → Line 274
  - Buttons (Primary) → Line 276
  - Buttons (Ghost/Icon) → Line 287
  - Text Input → Line 298
  - Chat Input Card → Line 308
  - Cards → Line 317
  - Sidebar Items → Line 325
  - Chips → Line 334
  - Toggle/Switch → Line 346
- **Motion Map** → Line 363
  - Easings → Line 365
  - Duration × Easing × Component → Line 376
  - Active Press Scale → Line 394
- **Layout Tokens** → Line 405
  - Spacing Scale → Line 416
  - Density → Line 420
  - Radius Scale → Line 424
  - Responsive Notes → Line 439
- **Accessibility Tokens** → Line 447
- **Overlays** → Line 480
  - Popover/Dropdown → Line 482
  - Modal → Line 498
  - Tooltip → Line 511
- **Visual Style** → Line 524
  - Paper Grain SVG (Alchemical) → Line 534
- **Signature Animations** → Line 548
  - Alchemical Mode (5 Animations) → Line 550
  - Editorial Mode (3 Animations) → Line 608
- **Mode Variant: Alchemical vs Editorial** → Line 658
  - Dark Mode Direction → Line 680
- **Mobile Notes** → Line 697
  - Effects to Disable → Line 699
  - Adjustments → Line 705
  - Performance Notes → Line 715
- **Implementation Checklist** → Line 723
