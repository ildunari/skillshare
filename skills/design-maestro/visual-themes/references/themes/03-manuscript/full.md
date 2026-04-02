# Manuscript — Full Specification

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 16
- [Color System](#color-system) — Line 38
  - [Alchemical Mode Palette](#alchemical-mode-palette) — Line 40
  - [Editorial Mode Palette](#editorial-mode-palette) — Line 61
  - [Special Tokens (Both Modes)](#special-tokens-both-modes) — Line 82
  - [Opacity System](#opacity-system) — Line 90
  - [Color Rules](#color-rules) — Line 101
- [Typography Matrix](#typography-matrix) — Line 110
  - [Alchemical Mode](#alchemical-mode) — Line 112
  - [Editorial Mode](#editorial-mode) — Line 131
  - [Typographic Decisions (Both Modes)](#typographic-decisions-both-modes) — Line 148
  - [Font Loading](#font-loading) — Line 158
- [Elevation System](#elevation-system) — Line 174
  - [Alchemical Mode — Desk Lamp Shadow](#alchemical-mode--desk-lamp-shadow) — Line 180
  - [Editorial Mode — Whisper Composite Shadows](#editorial-mode--whisper-composite-shadows) — Line 192
  - [Shadow Tokens (Combined)](#shadow-tokens-combined) — Line 204
  - [Separation Recipe](#separation-recipe) — Line 222
- [Border System](#border-system) — Line 229
  - [Widths](#widths) — Line 231
  - [Opacity Scale (on mode-specific border-base)](#opacity-scale-on-mode-specific-border-base) — Line 240
  - [Border Patterns](#border-patterns) — Line 249
  - [Focus Ring](#focus-ring) — Line 262
- [Component States](#component-states) — Line 274
  - [Buttons (Primary)](#buttons-primary) — Line 276
  - [Buttons (Ghost / Icon)](#buttons-ghost--icon) — Line 287
  - [Text Input](#text-input) — Line 298
  - [Chat Input Card](#chat-input-card) — Line 308
  - [Cards](#cards) — Line 317
  - [Sidebar Items](#sidebar-items) — Line 325
  - [Chips](#chips) — Line 334
  - [Toggle / Switch](#toggle--switch) — Line 346
- [Motion Map](#motion-map) — Line 363
  - [Easings](#easings) — Line 365
  - [Duration x Easing x Component](#duration-x-easing-x-component) — Line 376
  - [Active Press Scale](#active-press-scale) — Line 394
- [Layout Tokens](#layout-tokens) — Line 405
  - [Spacing Scale](#spacing-scale) — Line 416
  - [Density](#density) — Line 420
  - [Radius Scale](#radius-scale) — Line 424
  - [Responsive Notes](#responsive-notes) — Line 439
- [Accessibility Tokens](#accessibility-tokens) — Line 447
- [Overlays](#overlays) — Line 480
  - [Popover / Dropdown](#popover--dropdown) — Line 482
  - [Modal](#modal) — Line 498
  - [Tooltip](#tooltip) — Line 511
- [Visual Style](#visual-style) — Line 524
  - [Paper Grain SVG (Alchemical)](#paper-grain-svg-alchemical) — Line 534
- [Signature Animations](#signature-animations) — Line 548
  - [Alchemical Mode (5 Animations)](#alchemical-mode-5-animations) — Line 550
  - [Editorial Mode (3 Animations)](#editorial-mode-3-animations) — Line 608
- [Mode Variant: Alchemical vs Editorial](#mode-variant-alchemical-vs-editorial) — Line 658
  - [Dark Mode Direction](#dark-mode-direction) — Line 680
- [Mobile Notes](#mobile-notes) — Line 697
  - [Effects to Disable](#effects-to-disable) — Line 699
  - [Adjustments](#adjustments) — Line 705
  - [Performance Notes](#performance-notes) — Line 715
- [Implementation Checklist](#implementation-checklist) — Line 723

---

## 3. Manuscript

> Living manuscripts -- serif typography as identity, paper as material metaphor.

**Best for:** Writing tools, note-taking apps, knowledge bases, digital publishing, editorial platforms, literary apps, journaling, research tools, long-form reading interfaces.

---

### Identity & Philosophy

This theme lives in the world of handwritten manuscripts and finely typeset books. Paper is the primary material. Serif typography is not decoration -- it IS the design language. Every surface reads as a sheet, a leaf, a folio. Elevation is expressed through paper layering, not digital shadow gradients. The ink is alive: text has weight, presence, and craft.

The theme operates in two distinct modes that share a common material vocabulary but diverge in personality:

**Alchemical mode** is the hand-annotated working manuscript. Parchment tones, iron gall ink, copper-plate annotations in the margins. Motion is viscous -- ink spreading across fibrous paper, slow and organic. Buttons use small caps. Shadows are hard and directional, cast by a single desk lamp. The grain of laid paper is visible. This is a scholar's working desk, not a display case.

**Editorial mode** is the well-set letterpress book. Ivory cotton stock, perfectly justified columns, invisible typesetter precision. Motion is fast and nearly invisible -- the reader should never notice the interface moving. Shadows are whisper-thin composite layers. Surfaces are clean, smooth, matte. This is the finished volume, not the workshop.

**Decision principle:** "When in doubt, ask: does this feel like it was set in type or drawn by hand? Alchemical = drawn. Editorial = set. If it feels digital, add paper. If it feels decorative, remove it."

**What this theme is NOT:**
- Not skeuomorphic -- paper is the material metaphor, but we are not simulating a physical book with page curls and leather bindings
- Not monochrome -- warm neutrals have subtle color; the palette is restrained but not grey
- Not cold -- every surface carries warmth; zero blue-white undertones
- Not sans-serif -- if your output uses a sans-serif for body text, you have missed the entire point
- Not fast (Alchemical) / Not slow (Editorial) -- each mode has its own temporal identity

---

### Color System

#### Alchemical Mode Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Parchment | `#F8F4EC` | Deepest background. Aged paper with visible warmth. |
| bg | Vellum | `#FDF6E3` | Primary surface. Calfskin parchment, slightly lighter than page. |
| surface | Laid Paper | `#FFFBF3` | Elevated cards, inputs, popovers. Bright writing surface. |
| recessed | Foxed Paper | `#EDE6D6` | Code blocks, inset areas. Slightly darkened, aged paper. |
| active | Blotting Sand | `#E8DFD0` | Active/pressed items, user bubbles. Sand-dusted paper. |
| text-primary | Iron Gall Ink | `#1B2438` | Headings, body text. Dark blue-black of iron gall ink. |
| text-secondary | Faded Ink | `#5C5647` | Sidebar items, secondary labels. Ink that has oxidized lighter. |
| text-muted | Pencil Lead | `#7A7A70` | Placeholders, timestamps, metadata. Graphite annotation tone. WCAG AA compliant on all surfaces. |
| text-onAccent | Parchment White | `#FDF6E3` | Text on accent-colored backgrounds. |
| border-base | Ruled Line | `#8B7E6A` | Base border color used at variable opacity. Warm umber rule line. |
| accent-primary | Oxidized Copper | `#7B6840` | Primary CTA, active elements. Verdigris-touched copper. |
| accent-secondary | Sealing Wax | `#8B4513` | Secondary accent for links, annotations. Saddle-brown wax. |
| success | Verdigris Green | `#4A7C59` | Positive states, confirmations. Patinated copper-green. |
| warning | Goldenrod | `#B8860B` | Caution states. Illuminated manuscript gold. |
| danger | Sienna Red | `#9B3A2E` | Error states, destructive actions. Red ochre pigment. |
| info | Indigo Ink | `#3B5998` | Informational states. Deep indigo writing ink. |

#### Editorial Mode Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Ivory Stock | `#FAF6EE` | Deepest background. Fine book paper, warm ivory. |
| bg | Warm White | `#FEFCF7` | Primary surface. Premium cotton rag paper. |
| surface | Cotton | `#FFFFFF` | Elevated cards, inputs. Bright white cotton stock. |
| recessed | French Grey | `#EDEBE5` | Code blocks, inset areas. Cool-warm grey tint. |
| active | Pressed Linen | `#E5E0D6` | Active/pressed states. Linen texture impression. |
| text-primary | Letterpress Black | `#1C1E23` | Headings, body text. Dense black impression ink. |
| text-secondary | Body Grey | `#555961` | Sidebar items, secondary labels. Professional grey. |
| text-muted | Caption Grey | `#7A7A70` | Placeholders, timestamps. Restrained grey, WCAG AA compliant. |
| text-onAccent | Stock White | `#FEFCF7` | Text on accent-colored backgrounds. |
| border-base | Rule Line | `#9B9489` | Base border color at variable opacity. Typographic rule. |
| accent-primary | Burnt Umber | `#7A5C3A` | Primary CTA. Warm brown-amber, bookbinder's leather. |
| accent-secondary | Printer's Blue | `#3A5A7C` | Secondary accent for links. Composing-room blue. |
| success | Forest Ink | `#4A7C59` | Positive states. Same verdigris as Alchemical for consistency. |
| warning | Ochre | `#B8860B` | Caution states. Same goldenrod for consistency. |
| danger | Crimson Lake | `#9B3A2E` | Error states. Same sienna red for consistency. |
| info | Composing Blue | `#3B5998` | Informational states. Same indigo for consistency. |

#### Special Tokens (Both Modes)

| Token | Alchemical | Editorial | Role |
|---|---|---|---|
| inlineCode | `#7B6840` | `#7A5C3A` | Code text within prose. Matches accent-primary per mode. |
| toggleActive | `#4A7C59` | `#4A7C59` | Toggle/switch active track. Verdigris green. |
| selection | `rgba(123,104,64,0.18)` | `rgba(122,92,58,0.15)` | `::selection` background. Accent at low opacity. |

#### Opacity System

Border opacity (on mode-specific `border-base`):

| Level | Opacity | Usage |
|---|---|---|
| subtle | 15% | Panel edges, hairlines between sections |
| card | 25% | Card borders, content area boundaries |
| hover | 35% | Hovered elements, interactive state |
| heavy | 50% | Active/focused borders, strong delineation |

#### Color Rules

- No pure greys. Every neutral carries a warm undertone (yellow-brown bias).
- Accent colors are earth pigments, not synthetic hues. Nothing neon, nothing saturated beyond what pigment allows.
- Semantic colors (success, warning, danger, info) are shared between modes. They are historical pigment approximations.
- The page/bg/surface gradient moves from warm-dark to warm-light. Higher surfaces are brighter paper.
- Red is destructive only. Green is confirmatory only. Gold/goldenrod is cautionary.

---

### Typography Matrix

#### Alchemical Mode

 EB Garamond is the primary typeface -- a true Garamond revival with optical sizes and OpenType features including small caps. Libre Caslon Text serves blockquotes, epigraphs, and figure captions (any "quoted voice" distinct from the author's). IBM Plex Mono handles code.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | serif (EB Garamond) | 36px | 500 | 1.15 | -0.01em | `font-feature-settings: "opsz" 36, "liga" 1, "kern" 1` | Hero titles, page names |
| Heading | serif (EB Garamond) | 24px | 500 | 1.3 | normal | `font-feature-settings: "opsz" 24, "liga" 1` | Section titles, settings headers |
| Subheading | serif (EB Garamond) | 19px | 600 | 1.4 | 0.01em | `font-feature-settings: "smcp" 1, "opsz" 19` | Subsection labels. Small caps form. |
| Body | serif (EB Garamond) | 17px | 400 | 1.65 | normal | `font-feature-settings: "opsz" 17, "liga" 1, "onum" 1` | Primary reading text, UI body. Old-style numerals. |
| Body Small | serif (EB Garamond) | 15px | 400 | 1.55 | normal | `font-feature-settings: "opsz" 15` | Sidebar items, secondary UI text |
| Button | serif (EB Garamond) | 14px | 600 | 1.4 | 0.06em | `font-feature-settings: "smcp" 1, "opsz" 14` | Button labels. ALWAYS small caps in Alchemical mode. |
| Input | serif (EB Garamond) | 16px | 400 | 1.5 | normal | `font-feature-settings: "opsz" 16, "liga" 1` | Form input text |
| Blockquote | serif (Libre Caslon Text) | 17px | 400 italic | 1.65 | normal | `font-style: italic` | Blockquotes, epigraphs, figure captions, pull quotes |
| Label | serif (EB Garamond) | 12px | 400 | 1.33 | 0.04em | `font-feature-settings: "smcp" 1, "opsz" 12` | Metadata, timestamps. Small caps. |
| Code | mono (IBM Plex Mono) | 0.88em | 400 | 1.55 | normal | `font-feature-settings: "liga" 0` | Inline code, code blocks |
| Caption | serif (EB Garamond) | 12px | 400 | 1.4 | normal | `font-feature-settings: "opsz" 12` | Disclaimers, footnotes |

#### Editorial Mode

Newsreader provides display and heading weight with its designed-for-screen serif construction. Source Serif 4 handles body text with its optimized reading experience and optical sizing. JetBrains Mono for code.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | serif (Newsreader) | 36px | 500 | 1.15 | -0.01em | `font-feature-settings: "opsz" 36, "liga" 1` | Hero titles, page names |
| Heading | serif (Newsreader) | 24px | 500 | 1.3 | normal | `font-feature-settings: "opsz" 24` | Section titles, settings headers |
| Subheading | serif (Newsreader) | 19px | 600 | 1.35 | 0.005em | `font-feature-settings: "opsz" 19` | Subsection labels |
| Body | serif (Source Serif 4) | 17px | 400 | 1.65 | normal | `font-feature-settings: "opsz" 17, "liga" 1` | Primary reading text, UI body |
| Body Small | serif (Source Serif 4) | 15px | 400 | 1.5 | normal | `font-feature-settings: "opsz" 15` | Sidebar items, secondary UI text |
| Button | serif (Newsreader) | 14px | 600 | 1.4 | 0.02em | `font-feature-settings: "opsz" 14` | Button labels. Normal case in Editorial (no small caps). |
| Input | serif (Source Serif 4) | 16px | 400 | 1.5 | normal | `font-feature-settings: "opsz" 16` | Form input text |
| Blockquote | serif (Source Serif 4) | 17px | 400 italic | 1.65 | normal | `font-style: italic` | Blockquotes, epigraphs, figure captions |
| Label | serif (Source Serif 4) | 12px | 400 | 1.33 | 0.02em | `text-transform: none` | Metadata, timestamps |
| Code | mono (JetBrains Mono) | 0.88em | 400 | 1.55 | normal | `font-feature-settings: "liga" 1` | Inline code, code blocks. Ligatures enabled. |
| Caption | serif (Source Serif 4) | 12px | 400 | 1.4 | normal | -- | Disclaimers, footnotes |

#### Typographic Decisions (Both Modes)

- 17px body is deliberate: serif text requires slightly larger sizing than sans-serif for equivalent readability on screen.
- 1.65 line-height for body text: serifs need more vertical breathing room than sans-serifs.
- `-webkit-font-smoothing: antialiased` always. Critical for serif rendering on light backgrounds.
- `text-wrap: pretty` for body text to avoid orphans and improve rag quality.
- Libre Caslon Text (Alchemical) is scoped to: blockquotes, epigraphs, figure captions, pull quotes, and any "attributed voice" content. It is NOT used for general body or UI text.
- Small caps fallback: `@supports not (font-feature-settings: "smcp" 1) { .small-caps { text-transform: uppercase; font-size: 0.85em; letter-spacing: 0.08em; } }` -- synthesized small caps via uppercase at reduced size when OpenType is unavailable.

#### Font Loading

```html
<!-- Alchemical Mode -->
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Libre+Caslon+Text:ital@0;1&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">

<!-- Editorial Mode -->
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

**Fallback chains:**
- Alchemical: `"EB Garamond", "Garamond", "Times New Roman", Georgia, serif`
- Editorial display: `"Newsreader", "Georgia", "Times New Roman", serif`
- Editorial body: `"Source Serif 4", "Source Serif Pro", Georgia, serif`

---

### Elevation System

**Strategy:** `borders-only` (Alchemical) / `subtle-shadows` (Editorial)

Paper does not float. Paper layers. The elevation metaphor is a stack of sheets on a desk, not cards hovering in space.

#### Alchemical Mode -- Desk Lamp Shadow

Elevation is expressed through borders and a single hard directional shadow cast by an implied desk lamp at the upper-left. No blur. No ambient glow. The shadow is an opaque rectangle offset, like a physical object on a lit surface.

| Surface | Background | Border | Shadow | Usage |
|---|---|---|---|---|
| page | `#F8F4EC` | none | none | Desk surface, behind all paper |
| manuscript | `#FDF6E3` | `0.5px solid border-base/25%` | none | Primary writing surface |
| folio | `#FFFBF3` | `1px solid border-base/35%` | `3px 4px 0 rgba(27,36,56,0.08)` | Elevated cards, inputs. Hard directional shadow. |
| palimpsest | `#EDE6D6` | `0.5px solid border-base/15%` | none | Recessed areas, code blocks. Written-over paper. |
| overlay | `#FFFBF3` | `1px solid border-base/50%` | `4px 5px 0 rgba(27,36,56,0.12)` | Popovers, dropdowns. Strongest shadow. |

#### Editorial Mode -- Whisper Composite Shadows

Elevation uses whisper-thin composite shadows: a hair-fine drop shadow paired with a 0.5px ring. The shadows are barely visible -- the typesetter's hand should be invisible.

| Surface | Background | Border | Shadow | Usage |
|---|---|---|---|---|
| page | `#FAF6EE` | none | none | Book page, behind all content |
| leaf | `#FEFCF7` | `0.5px solid border-base/15%` | `0 1px 3px rgba(28,30,35,0.04)` | Primary content surface |
| folio | `#FFFFFF` | `0.5px solid border-base/20%` | `0 1px 2px rgba(28,30,35,0.05), 0 0 0 0.5px rgba(155,148,137,0.12)` | Elevated cards, inputs. Drop + ring composite. |
| signature | `#EDEBE5` | `0.5px solid border-base/15%` | `inset 0 1px 2px rgba(28,30,35,0.04)` | Recessed areas. Subtle inner shadow. |
| overlay | `#FFFFFF` | `0.5px solid border-base/25%` | `0 2px 8px rgba(28,30,35,0.08), 0 0 0 0.5px rgba(155,148,137,0.15)` | Popovers, modals. Wider spread composite. |

#### Shadow Tokens (Combined)

| Token | Mode | Value | Usage |
|---|---|---|---|
| shadow-none | Both | `none` | Page background, flat surfaces |
| shadow-desk-sm | Alchemical | `2px 3px 0 rgba(27,36,56,0.06)` | Small elements, badges |
| shadow-desk-md | Alchemical | `3px 4px 0 rgba(27,36,56,0.08)` | Cards, input card. Primary desk lamp shadow. |
| shadow-desk-lg | Alchemical | `4px 5px 0 rgba(27,36,56,0.12)` | Popovers, overlays. Maximum desk lamp shadow. |
| shadow-desk-hover | Alchemical | `4px 5px 0 rgba(27,36,56,0.10)` | Card hover. Shadow slightly deepens. |
| shadow-whisper-sm | Editorial | `0 1px 3px rgba(28,30,35,0.04)` | Small elements, leaf-level surfaces |
| shadow-whisper-md | Editorial | `0 1px 2px rgba(28,30,35,0.05), 0 0 0 0.5px rgba(155,148,137,0.12)` | Cards, input card. Drop + ring. |
| shadow-whisper-lg | Editorial | `0 2px 8px rgba(28,30,35,0.08), 0 0 0 0.5px rgba(155,148,137,0.15)` | Popovers, modals. Wider composite. |
| shadow-whisper-hover | Editorial | `0 2px 6px rgba(28,30,35,0.07), 0 0 0 0.5px rgba(155,148,137,0.18)` | Card hover. Ring darkens slightly. |
| shadow-input-focus-alch | Alchemical | `3px 4px 0 rgba(27,36,56,0.08), 0 0 0 2px rgba(123,104,64,0.35)` | Input focus. Desk shadow + warm amber ring. |
| shadow-input-focus-edit | Editorial | `0 1px 2px rgba(28,30,35,0.05), 0 0 0 2px rgba(58,90,124,0.3)` | Input focus. Whisper shadow + blue-grey ring. |
| shadow-inset | Both | `inset 0 1px 2px rgba(0,0,0,0.04)` | Recessed surfaces, code blocks |

#### Separation Recipe

Alchemical: Warm-tinted surface stepping (page darker than bg lighter than surface) + ruled-line borders at variable opacity + hard directional shadow on elevated sheets. No dividers inside cards. Hierarchy = paper brightness + border weight.

Editorial: Subtle surface stepping + whisper composite shadows (drop + hairline ring) + minimal borders. Dividers are thin horizontal rules (`border-base` at 10%) when needed. Hierarchy = shadow complexity + border opacity.

---

### Border System

#### Widths

| Name | Width | Usage |
|---|---|---|
| hairline | 0.5px | Panel edges, subtle separators |
| default | 1px | Card borders, input borders, standard rules |
| medium | 1.5px | Section dividers, emphasized rules |
| heavy | 2px | Active states, focus indicators |

#### Opacity Scale (on mode-specific `border-base`)

| Level | Opacity | Usage |
|---|---|---|
| subtle | 15% | Hairline edges, ghost borders |
| card | 25% | Standard card and panel borders |
| hover | 35% | Hovered elements, interactive borders |
| heavy | 50% | Active/focused elements, strong delineation |

#### Border Patterns

| Pattern | Width | Opacity | Usage |
|---|---|---|---|
| subtle | hairline (0.5px) | 15% | Panel edges, section separators |
| card | default (1px) | 25% | Card borders (Alchemical) or hairline (0.5px) at 20% (Editorial) |
| hover | default (1px) | 35% | Hovered cards, interactive elements |
| input | default (1px) | 25% | Form input borders |
| input-hover | default (1px) | 35% | Input hover state |
| rule | medium (1.5px) | 15% | Horizontal typographic rules, section breaks |
| heavy | heavy (2px) | 50% | Active elements, strong emphasis |

#### Focus Ring

| Property | Alchemical | Editorial |
|---|---|---|
| Color | `rgba(123, 104, 64, 0.35)` -- warm amber | `rgba(58, 90, 124, 0.3)` -- blue-grey |
| Width | 2px solid | 2px solid |
| Offset | 2px | 2px |
| Implementation | `box-shadow: 0 0 0 2px #FDF6E3, 0 0 0 4px rgba(123,104,64,0.35)` | `box-shadow: 0 0 0 2px #FEFCF7, 0 0 0 4px rgba(58,90,124,0.3)` |

The inner ring uses the mode's `bg` color to separate the focus indicator from the element surface.

---

### Component States

#### Buttons (Primary)

| State | Alchemical | Editorial |
|---|---|---|
| Rest | bg `#7B6840`, border none, color `#FDF6E3`, radius 4px, h 34px, padding `0 16px`, font button (small caps, 14px, 600, `smcp`), shadow shadow-desk-sm | bg `#7A5C3A`, border none, color `#FEFCF7`, radius 6px, h 34px, padding `0 16px`, font button (14px, 600, normal case), shadow none |
| Hover | bg `#6A5A36` (darker copper) | bg `#6B4F30` (darker umber), shadow shadow-whisper-sm |
| Active | bg `#5C4E2E`, transform `scale(0.97)` | bg `#5E4428`, transform `scale(0.98)` |
| Focus | focus ring (warm amber) appended | focus ring (blue-grey) appended |
| Disabled | opacity 0.45, pointer-events none, cursor not-allowed | opacity 0.45, pointer-events none, cursor not-allowed |
| Transition | background 150ms ink-spread, transform 100ms ink-spread | background 100ms ease-out, transform 80ms ease-out |

#### Buttons (Ghost / Icon)

| State | Alchemical | Editorial |
|---|---|---|
| Rest | bg transparent, border none, color `#5C5647`, radius 4px, size 32x32px | bg transparent, border none, color `#555961`, radius 6px, size 32x32px |
| Hover | bg `rgba(139,126,106,0.1)`, color `#1B2438` | bg `rgba(155,148,137,0.08)`, color `#1C1E23` |
| Active | bg `rgba(139,126,106,0.18)`, transform `scale(0.97)` | bg `rgba(155,148,137,0.12)`, transform `scale(0.98)` |
| Focus | focus ring | focus ring |
| Disabled | opacity 0.45, pointer-events none | opacity 0.45, pointer-events none |
| Transition | background 200ms ink-ease, color 200ms ink-ease | background 100ms ease-out, color 100ms ease-out |

#### Text Input

| State | Alchemical | Editorial |
|---|---|---|
| Rest | bg `#FFFBF3`, border `1px solid rgba(139,126,106,0.25)`, radius 4px, h 44px, padding `0 12px`, shadow shadow-desk-sm, color `#1B2438`, placeholder `#7A7A70`, caret-color `#7B6840` | bg `#FFFFFF`, border `1px solid rgba(155,148,137,0.2)`, radius 6px, h 44px, padding `0 12px`, shadow shadow-whisper-md, color `#1C1E23`, placeholder `#7A7A70`, caret-color `#7A5C3A` |
| Hover | border at 35% opacity, shadow shadow-desk-md | border at 30% opacity, shadow shadow-whisper-hover |
| Focus | border `1px solid rgba(123,104,64,0.5)`, shadow shadow-input-focus-alch, outline none | border `1px solid rgba(58,90,124,0.4)`, shadow shadow-input-focus-edit, outline none |
| Disabled | opacity 0.45, bg `#EDE6D6`, pointer-events none | opacity 0.45, bg `#EDEBE5`, pointer-events none |
| Transition | border-color 150ms ink-ease, box-shadow 200ms ink-ease | border-color 100ms ease-out, box-shadow 120ms ease-out |

#### Chat Input Card

| State | Alchemical | Editorial |
|---|---|---|
| Rest | bg `#FFFBF3`, radius 12px, border `1px solid rgba(139,126,106,0.25)`, shadow shadow-desk-md | bg `#FFFFFF`, radius 16px, border `0.5px solid rgba(155,148,137,0.15)`, shadow shadow-whisper-md |
| Hover | border at 35%, shadow shadow-desk-hover | border at 20%, shadow shadow-whisper-hover |
| Focus-within | border `1px solid rgba(123,104,64,0.4)`, shadow shadow-input-focus-alch | border `0.5px solid rgba(58,90,124,0.3)`, shadow shadow-input-focus-edit |
| Transition | all 200ms ink-ease | all 150ms ease-out |

#### Cards

| State | Alchemical | Editorial |
|---|---|---|
| Rest | bg `#FFFBF3`, border `1px solid rgba(139,126,106,0.25)`, radius 4px, shadow shadow-desk-md | bg `#FFFFFF`, border `0.5px solid rgba(155,148,137,0.2)`, radius 8px, shadow shadow-whisper-md |
| Hover | border at 35%, shadow shadow-desk-hover | border at 25%, shadow shadow-whisper-hover |
| Transition | border-color 200ms ink-ease, box-shadow 250ms ink-ease | border-color 100ms ease-out, box-shadow 120ms ease-out |

#### Sidebar Items

| State | Alchemical | Editorial |
|---|---|---|
| Rest | bg transparent, color `#5C5647`, radius 2px, h 34px, padding `6px 12px`, font bodySmall | bg transparent, color `#555961`, radius 6px, h 34px, padding `6px 12px`, font bodySmall |
| Hover | bg `rgba(139,126,106,0.1)`, color `#1B2438` | bg `rgba(155,148,137,0.06)`, color `#1C1E23` |
| Active (current) | bg `rgba(139,126,106,0.15)`, color `#1B2438`, font-weight 500 | bg `rgba(155,148,137,0.1)`, color `#1C1E23`, font-weight 500 |
| Active press | transform `scale(0.985)` | transform `scale(0.99)` |
| Transition | color 150ms ink-ease, background 150ms ink-ease | color 75ms ease-out, background 75ms ease-out |

#### Chips

| State | Alchemical | Editorial |
|---|---|---|
| Rest | bg `#F8F4EC`, border `0.5px solid rgba(139,126,106,0.2)`, radius 2px, h 30px, padding `0 10px`, font label (small caps), color `#5C5647` | bg `#FAF6EE`, border `0.5px solid rgba(155,148,137,0.15)`, radius 14px (pill), h 30px, padding `0 10px`, font bodySmall, color `#555961` |
| Hover | bg `#EDE6D6`, border at 30%, color `#1B2438` | bg `#EDEBE5`, border at 20%, color `#1C1E23` |
| Active press | transform `scale(0.98)` | transform `scale(0.99)` |
| Transition | all 200ms ink-ease | all 100ms ease-out |

Alchemical chips are rectangular (radius 2px) with small-caps labels. Editorial chips are pills (radius 14px) with normal-case labels.

#### Toggle / Switch

| Property | Alchemical | Editorial |
|---|---|---|
| Track width | 40px | 40px |
| Track height | 22px | 22px |
| Track radius | 9999px | 9999px |
| Track off bg | `rgba(139,126,106,0.2)` | `rgba(155,148,137,0.15)` |
| Track off ring | `0.5px solid rgba(139,126,106,0.25)` | `0.5px solid rgba(155,148,137,0.2)` |
| Track on bg | `#4A7C59` (verdigris) | `#4A7C59` (verdigris) |
| Thumb | 18px `#FFFBF3` circle | 18px `#FFFFFF` circle |
| Thumb shadow | `1px 2px 0 rgba(27,36,56,0.08)` (hard directional) | `0 1px 2px rgba(28,30,35,0.1)` (soft) |
| Ring hover | thickens to 1px | thickens to 1px |
| Transition | 200ms ink-ease | 150ms ease-out |
| Focus-visible | warm amber focus ring | blue-grey focus ring |

---

### Motion Map

#### Easings

| Name | Value | Mode | Character |
|---|---|---|---|
| ink-spread | `cubic-bezier(0.25, 0.05, 0.15, 1)` | Alchemical | Viscous ink spreading on paper. Slow start, long deceleration tail. |
| ink-ease | `cubic-bezier(0.3, 0.1, 0.2, 1)` | Alchemical | General ink-flavored ease-out. Slightly sticky. |
| page-turn | `cubic-bezier(0.4, 0, 0.1, 1)` | Alchemical | Page turning. Acceleration then gentle settle. |
| ease-out | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Editorial | Standard smooth ease-out. Nearly invisible. |
| ease-snap | `cubic-bezier(0.2, 0.8, 0.3, 1)` | Editorial | Snappy deceleration for micro-interactions. |
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Both | Standard ease-in-out fallback. |

#### Duration x Easing x Component

| Component | Alchemical Duration | Alchemical Easing | Editorial Duration | Editorial Easing | Notes |
|---|---|---|---|---|---|
| Sidebar item bg/color | 150ms | ink-ease | 75ms | ease-snap | Alchemical is noticeably slower |
| Button hover bg | 200ms | ink-spread | 100ms | ease-out | Ink spreading vs instant tint |
| Button active scale | 150ms | ink-ease | 80ms | ease-snap | Press feedback |
| Toggle slide | 250ms | ink-spread | 150ms | ease-out | Thumb slides |
| Chip hover | 200ms | ink-ease | 100ms | ease-out | Background transition |
| Card shadow on hover | 300ms | ink-spread | 120ms | ease-out | Shadow deepens slowly vs quickly |
| Input focus ring | 250ms | ink-spread | 100ms | ease-out | Ring appearance |
| Panel open/close | 500ms | page-turn | 250ms | ease-out | Sidebar, overlay panels |
| Modal enter | 600ms | ink-spread | 250ms | ease-out | Modal fade + position |
| Hero/page entry | 800ms | ink-spread | 350ms | ease-out | Fade + drift upward |
| Ink-bleed reveal | 600ms | ink-spread | -- | -- | Alchemical signature only |
| Popover appear | 300ms | ink-ease | 150ms | ease-snap | Menu/dropdown entry |

#### Active Press Scale

| Element | Alchemical | Editorial | Notes |
|---|---|---|---|
| Nav items | 0.985 | 0.99 | Barely perceptible |
| Chips | 0.98 | 0.99 | Subtle |
| Buttons | 0.97 | 0.98 | Standard |
| Tabs | 0.96 | 0.98 | More pronounced |
| Cards (clickable) | 0.99 | 0.995 | Very subtle on large surfaces |

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 680px | Main content column. Narrower than most themes -- optimized for serif line length (~65 characters at 17px). |
| Narrow max-width | 580px | Focused reading, long-form content |
| Sidebar width | 260px | Fixed sidebar |
| Header height | 48px | Top bar |
| Spacing unit | 4px | Base multiplier |

#### Spacing Scale

4, 8, 12, 16, 20, 24, 32, 48px

#### Density

Comfortable. Generous vertical rhythm. 16px internal card padding, 12px gaps between list items, 32-48px section spacing. Serif text at 1.65 line-height creates natural openness.

#### Radius Scale

| Token | Alchemical | Editorial | Usage |
|---|---|---|---|
| none | 0px | 0px | -- |
| sm | 2px | 4px | Badges, small elements. Alchemical is sharper. |
| md | 4px | 6px | Sidebar items, menu items |
| lg | 4px | 8px | Cards. Alchemical stays rectilinear. |
| xl | 8px | 12px | Modals, large panels |
| 2xl | 12px | 16px | Chat input card |
| input | 4px | 6px | Form inputs, textareas |
| full | 9999px | 9999px | Toggles, pills, avatars |

Alchemical mode uses tighter radii throughout (2-8px range) for a more angular, hand-crafted feel. Editorial mode uses standard web radii (4-16px range) for a polished, professional feel.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (260px) + content column (680px max). Standard layout.
- **md (768px):** Sidebar collapses to overlay panel. Content column expands to fill. Chat input card radius reduces by 4px per mode.
- **sm (640px):** Single column. Body text stays 17px. Card radii reduce by 2px. Section spacing reduces from 48px to 32px. Line-height can reduce to 1.55 for space efficiency.

---

### Accessibility Tokens

| Token | Alchemical | Editorial |
|---|---|---|
| Focus ring color | `rgba(123, 104, 64, 0.35)` | `rgba(58, 90, 124, 0.3)` |
| Focus ring width | 2px solid | 2px solid |
| Focus ring offset | 2px (inner ring: mode `bg` color) | 2px (inner ring: mode `bg` color) |
| Disabled opacity | 0.45 | 0.45 |
| Disabled pointer-events | none | none |
| Disabled cursor | not-allowed | not-allowed |
| Selection bg | `rgba(123,104,64,0.18)` | `rgba(122,92,58,0.15)` |
| Selection color | `#1B2438` (text-primary) | `#1C1E23` (text-primary) |
| Scrollbar width | thin | thin |
| Scrollbar thumb | `rgba(139,126,106,0.3)` | `rgba(155,148,137,0.25)` |
| Scrollbar track | transparent | transparent |
| Min touch target | 44px | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) | WCAG AA (4.5:1 text, 3:1 large text) |

**Reduced motion per mode:**

| Behavior | Alchemical | Editorial |
|---|---|---|
| Strategy | `fade-only` -- all spatial/ink animations collapse to simple opacity fades | `instant` -- transitions reduce to near-zero duration |
| Ink-bleed reveal | Collapses to 200ms opacity fade | N/A |
| Paper grain | Static texture (no animation) | N/A |
| Desk lamp shadow | Static, no transition on hover | Static |
| Signature animations | All disabled | All disabled |
| Duration override | All durations cap at 200ms | All durations cap at 100ms |

**Contrast notes:** `text-muted` at `#7A7A70` achieves 4.6:1 against `#FFFBF3` (Alchemical surface) and 4.5:1 against `#FFFFFF` (Editorial surface), meeting WCAG AA for normal text. Against darker `page` backgrounds the ratio improves to 5.0:1+.

---

### Overlays

#### Popover / Dropdown

| Property | Alchemical | Editorial |
|---|---|---|
| bg | `#FFFBF3` | `#FFFFFF` |
| border | `1px solid rgba(139,126,106,0.35)` | `0.5px solid rgba(155,148,137,0.2)` |
| radius | 4px | 10px |
| shadow | shadow-desk-lg | shadow-whisper-lg |
| padding | 6px | 6px |
| z-index | 50 | 50 |
| min-width | 192px | 192px |
| max-width | 320px | 320px |
| Menu item | 6px 8px padding, radius 2px, h 32px, font bodySmall, color text-secondary | 6px 8px padding, radius 6px, h 32px, font bodySmall, color text-secondary |
| Menu item hover | bg `rgba(139,126,106,0.1)`, color text-primary | bg `rgba(155,148,137,0.06)`, color text-primary |
| Transition | 150ms ink-ease | 75ms ease-snap |

#### Modal

| Property | Alchemical | Editorial |
|---|---|---|
| Overlay bg | `rgba(27,36,56,0.25)` | `rgba(28,30,35,0.2)` |
| Overlay backdrop-filter | none (paper does not blur) | `blur(4px)` (very subtle) |
| Content bg | `#FFFBF3` | `#FFFFFF` |
| Content border | `1px solid rgba(139,126,106,0.35)` | `0.5px solid rgba(155,148,137,0.2)` |
| Content shadow | shadow-desk-lg | shadow-whisper-lg |
| Content radius | 8px | 14px |
| Entry | opacity `0` to `1` + translateY `12px` to `0`, 600ms ink-spread | opacity `0` to `1` + scale `0.97` to `1.0`, 250ms ease-out |
| Exit | opacity `1` to `0`, 300ms ink-ease | opacity `1` to `0` + scale `1.0` to `0.98`, 150ms ease-out |

#### Tooltip

| Property | Alchemical | Editorial |
|---|---|---|
| bg | `#1B2438` (iron gall ink) | `#1C1E23` (letterpress black) |
| color | `#FDF6E3` (vellum) | `#FEFCF7` (warm white) |
| font | label size (12px), EB Garamond small caps | label size (12px), Source Serif 4 |
| radius | 2px | 6px |
| padding | 4px 8px | 4px 10px |
| shadow | shadow-desk-sm | shadow-whisper-sm |
| No arrow | Position via offset | Position via offset |

---

### Visual Style

- **Grain (Alchemical only):** Subtle paper grain via SVG `feTurbulence`. Base frequency `0.65`, numOctaves `4`, type `fractalNoise`. Applied as a full-viewport overlay at 3-4% opacity with `mix-blend-mode: multiply`. The grain gives every surface the texture of laid paper. Apply via CSS `filter: url(#paper-grain)` or as a pseudo-element background.
- **Grain (Editorial):** None. Cotton stock is smooth, pristine. Zero texture.
- **Gloss:** Matte on both modes. No sheen, no reflections, no specular highlights. Paper absorbs light.
- **Blend mode:** `multiply` for the paper grain overlay (Alchemical). `normal` for everything else.
- **Directional shadow (Alchemical):** The desk lamp sits upper-left. All hard shadows offset to the right and down (positive x, positive y). No blur radius. This creates a consistent physical metaphor across every elevated element.
- **Material quality:** Paper. Not card stock (too rigid), not tissue (too thin), not canvas (too rough). Medium-weight writing paper with natural warmth and slight translucency where sheets overlap. Edges are cut, not rounded.
- **Shader bg:** False. No WebGL. The paper grain is SVG-based for performance and accessibility.

#### Paper Grain SVG (Alchemical)

```svg
<svg width="0" height="0">
  <filter id="paper-grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" stitchTiles="stitch" result="noise"/>
    <feColorMatrix type="saturate" values="0" in="noise" result="mono"/>
    <feBlend mode="multiply" in="SourceGraphic" in2="mono"/>
  </filter>
</svg>
```

---

### Signature Animations

#### Alchemical Mode (5 Animations)

**1. Ink-Bleed Reveal**

Text and UI elements reveal with an ink-bleed effect: a `clip-path` circle expands from the center while a subtle blur (`filter: blur()`) transitions from 4px to 0px. The effect simulates ink soaking into paper fibers, spreading outward. Duration: 600ms, easing: ink-spread. `clip-path: circle()` grows from 0% to 100%.

```css
@keyframes ink-bleed {
  from {
    clip-path: circle(0% at 50% 50%);
    filter: blur(4px);
    opacity: 0.3;
  }
  to {
    clip-path: circle(100% at 50% 50%);
    filter: blur(0px);
    opacity: 1;
  }
}
.ink-reveal { animation: ink-bleed 600ms cubic-bezier(0.25, 0.05, 0.15, 1) both; }
```

Reduced motion: collapses to 200ms opacity-only fade.

**2. Paper Grain Drift**

The feTurbulence grain overlay shifts its `seed` attribute at a very slow rate (every 3 seconds) via JavaScript, creating a subtle living-paper effect. The grain never changes dramatically -- it breathes. Alternatively, use CSS `transform: translate()` to shift the grain overlay by 1-2px periodically.

Reduced motion: grain becomes static (no drift).

**3. Desk Lamp Shadow Shift**

On card hover, the hard directional shadow shifts slightly -- from `3px 4px 0` to `4px 5px 0` -- as if the card lifted fractionally closer to the lamp. Duration: 300ms, easing: ink-spread. The effect is purely shadow-based; the card itself does not move or scale.

```css
.manuscript-card {
  box-shadow: 3px 4px 0 rgba(27,36,56,0.08);
  transition: box-shadow 300ms cubic-bezier(0.25, 0.05, 0.15, 1);
}
.manuscript-card:hover {
  box-shadow: 4px 5px 0 rgba(27,36,56,0.10);
}
```

Reduced motion: shadow is static, no transition.

**4. Copper Patina Accent Shift**

The accent-primary color (`#7B6840`) shifts very subtly toward green (`#6B7840`) on prolonged hover (>500ms) via a CSS transition on `color` or `background-color`. This simulates the verdigris patination of copper over time. Duration: 800ms, easing: ink-spread. The shift is barely perceptible -- 10-15 degrees on the hue wheel.

Reduced motion: disabled entirely.

**5. Margin Note Entry**

Secondary annotations (tooltips, helper text, validation messages) enter from the right margin with a horizontal slide: `translateX(20px)` to `0` with opacity `0` to `1`. Duration: 400ms, easing: ink-ease. This mimics a scholar's marginal annotation being inscribed.

Reduced motion: collapses to opacity-only fade, 150ms.

#### Editorial Mode (3 Animations)

**1. Letterpress Impression**

On button press or card click, the element's shadow briefly intensifies then settles -- simulating the moment a letterpress plate stamps into paper. The `box-shadow` transitions from the rest state to a slightly deeper composite (additional 1px y-offset, 2% more opacity), then settles back. Duration: 200ms total (100ms deepen + 100ms settle), easing: ease-snap.

```css
@keyframes letterpress {
  0% { box-shadow: 0 1px 2px rgba(28,30,35,0.05), 0 0 0 0.5px rgba(155,148,137,0.12); }
  50% { box-shadow: 0 2px 3px rgba(28,30,35,0.08), 0 0 0 0.5px rgba(155,148,137,0.18); }
  100% { box-shadow: 0 1px 2px rgba(28,30,35,0.05), 0 0 0 0.5px rgba(155,148,137,0.12); }
}
```

Reduced motion: no animation, standard state change.

**2. Section Rule Draw**

Horizontal typographic rules (`<hr>` or section dividers) animate into view with `transform: scaleX(0)` to `scaleX(1)`, origin left. Duration: 350ms, easing: ease-out. The rule draws itself across the page like a composing stick setting a line.

```css
@keyframes rule-draw {
  from { transform: scaleX(0); transform-origin: left; }
  to { transform: scaleX(1); transform-origin: left; }
}
.section-rule { animation: rule-draw 350ms cubic-bezier(0.25, 0.1, 0.25, 1) both; }
```

Reduced motion: rule appears instantly (no animation).

**3. Quiet Stagger**

Content blocks (paragraphs, cards, list items) entering the viewport stagger with opacity-only animations. Each successive element delays by 35ms. Opacity transitions from 0 to 1 over 250ms with ease-out. No spatial movement at all -- the content simply materializes like type being revealed on a printed page.

```css
.stagger-item {
  opacity: 0;
  animation: quiet-fade 250ms cubic-bezier(0.25, 0.1, 0.25, 1) both;
}
@keyframes quiet-fade { to { opacity: 1; } }
.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 35ms; }
.stagger-item:nth-child(3) { animation-delay: 70ms; }
/* ... continue pattern ... */
```

Reduced motion: all items appear simultaneously (no stagger delay).

---

### Mode Variant: Alchemical vs Editorial

| Dimension | Alchemical | Editorial |
|---|---|---|
| Paper tone | Parchment warm (#F8F4EC) | Ivory cool-warm (#FAF6EE) |
| Display font | EB Garamond | Newsreader |
| Body font | EB Garamond | Source Serif 4 |
| Code font | IBM Plex Mono | JetBrains Mono |
| Button text | Small caps (`smcp`) | Normal case |
| Chip shape | Rectangular (2px radius) | Pill (14px radius) |
| Card radius | 4px | 8px |
| Shadow type | Hard directional (desk lamp) | Soft composite (whisper) |
| Shadow blur | 0px (zero blur) | 2-8px (soft blur) |
| Focus ring color | Warm amber | Blue-grey |
| Motion speed | Slow (150-800ms) | Fast (75-350ms) |
| Motion character | Viscous, organic, sticky | Invisible, mechanical, instant |
| Grain texture | feTurbulence paper grain at 3-4% | None |
| Modal entry | translateY slide, 600ms | scale + opacity, 250ms |
| Border weight | Heavier (1px standard) | Lighter (0.5px standard) |
| Accent hue | Oxidized copper (#7B6840) | Burnt umber (#7A5C3A) |
| Overall feel | Scholar's workshop | Publisher's proof |

#### Dark Mode Direction

Neither mode is designed dark-first. A dark manuscript variant would reverse the paper metaphor:

- **Page/bg:** Deep warm brown (`#1A1610`) simulating dark leather or aged wood desk
- **Surface:** Warm dark (`#2A2520`) for cards -- illuminated parchment fragment against dark desk
- **Text:** Aged ivory (`#E8E0D0`) for primary text -- ink becomes light on dark
- **Accent:** Both accent colors lighten by 15-20% for contrast
- **Shadows:** Alchemical hard shadows become warm glows (`rgba(248,244,236,0.06)`); Editorial whisper shadows become warm-tinted (`rgba(200,190,170,0.08)`)
- **Paper grain:** Inverts to a very subtle light noise on dark surfaces
- **Borders:** `border-base` lightens to `#6B6050`, used at same opacity scale

Full dark mode implementation is deferred -- the theme's identity is fundamentally light-paper-forward.

---

### Mobile Notes

#### Effects to Disable
- Paper grain drift animation (Alchemical signature #2) -- use static grain only
- Copper patina accent shift (Alchemical signature #4) -- disabled entirely
- Desk lamp shadow transitions (Alchemical signature #3) -- static shadow, no transition on hover
- Quiet stagger delays beyond 3rd item (Editorial signature #3) -- cap stagger at 3 items

#### Adjustments
- Body text stays 17px (already comfortable for mobile serif reading)
- Card radii reduce by 2px per mode (Alchemical 4px stays 4px minimum; Editorial 8px becomes 6px)
- Chat input card radius: Alchemical 12px to 8px; Editorial 16px to 12px
- Section spacing reduces from 48px to 32px
- Paper grain opacity reduces from 3-4% to 2% for rendering performance
- Hard shadow (Alchemical) offset reduces from `3px 4px` to `2px 3px` on smaller screens
- All interactive elements maintain minimum 44px touch target
- Sidebar overlay uses mode surface color (not lower-elevation page color)

#### Performance Notes
- Paper grain SVG filter is GPU-composited but lightweight. Single-layer filter is within mobile budget.
- No `backdrop-filter` in either mode (unlike glass themes), so compositing cost is minimal.
- Hard shadows (zero blur) are cheaper to render than blurred shadows.
- `will-change: transform` only during active animations, never permanent.
- Total animation budget on mobile: 2 concurrent transitions maximum.

---

### Implementation Checklist

- [ ] Google Fonts loaded per mode: EB Garamond (400, 500, 600 + italics), Libre Caslon Text (400 + italic), IBM Plex Mono (400) for Alchemical; Newsreader (400, 500, 600 + italics), Source Serif 4 (400, 600 + italic), JetBrains Mono (400) for Editorial
- [ ] CSS custom properties defined for all color tokens per mode (use `data-mode="alchemical"` / `data-mode="editorial"` attribute switching)
- [ ] `font-feature-settings` applied per typography role: `"smcp"` on Alchemical buttons/labels/subheadings, `"opsz"` on all variable-axis fonts, `"onum"` on body text, `"liga"` where specified
- [ ] `@supports not (font-feature-settings: "smcp" 1)` fallback defined: `text-transform: uppercase; font-size: 0.85em; letter-spacing: 0.08em`
- [ ] `text-wrap: pretty` applied to body text elements
- [ ] `-webkit-font-smoothing: antialiased` on root element
- [ ] Border-radius scale applied per mode per component (Alchemical tighter, Editorial standard)
- [ ] Shadow tokens applied per mode: hard directional (Alchemical) vs whisper composite (Editorial)
- [ ] Shadow escalation on hover for cards and inputs (shadow-desk-md to shadow-desk-hover; shadow-whisper-md to shadow-whisper-hover)
- [ ] Border opacity system implemented: `border-base` at 15/25/35/50% per mode
- [ ] Focus ring per mode: warm amber (Alchemical) vs blue-grey (Editorial) with mode-bg inner ring
- [ ] Paper grain SVG filter implemented (Alchemical only) with `mix-blend-mode: multiply` at 3-4% opacity
- [ ] `prefers-reduced-motion` media query: Alchemical collapses to fade-only (200ms cap), Editorial collapses to instant (100ms cap), all signature animations disabled, grain becomes static
- [ ] Scrollbar styled per mode: warm thumb (Alchemical) vs neutral thumb (Editorial), transparent track
- [ ] Touch targets >= 44px on all interactive elements
- [ ] State transitions match motion map per mode: slow ink-spread easings (Alchemical) vs fast ease-out (Editorial)
- [ ] `::selection` styled per mode with accent-primary at 18% (Alchemical) / 15% (Editorial)
- [ ] `::placeholder` color matches `text-muted` token (`#7A7A70`) in both modes
- [ ] Mode switching mechanism implemented (CSS custom properties swap on `data-mode` attribute change)
- [ ] Libre Caslon Text scoped only to blockquotes, epigraphs, figure captions, and pull quotes (not general body text)
- [ ] Small caps buttons verified: Alchemical buttons render in true OpenType small caps, not fake CSS small-caps
