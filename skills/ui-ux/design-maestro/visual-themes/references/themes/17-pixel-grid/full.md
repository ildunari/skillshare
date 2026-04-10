# Pixel Grid — Full Reference

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — line 69
- [Color System](#color-system) — line 88
  - [Warm Mode ("Gazette") Palette](#warm-mode-gazette-palette) — line 90
  - [Special Tokens (Warm)](#special-tokens-warm) — line 122
  - [Cool Mode ("Terminal") Palette](#cool-mode-terminal-palette) — line 130
  - [Special Tokens (Cool)](#special-tokens-cool) — line 162
  - [Opacity System](#opacity-system) — line 170
  - [Color Rules](#color-rules) — line 181
- [Typography Matrix](#typography-matrix) — line 190
  - [Warm Mode ("Gazette")](#warm-mode-gazette) — line 192
  - [Cool Mode ("Terminal")](#cool-mode-terminal) — line 208
  - [Font Loading](#font-loading) — line 224
- [Elevation System](#elevation-system) — line 238
  - [Surface Hierarchy](#surface-hierarchy) — line 244
  - [Shadow Tokens](#shadow-tokens) — line 255
  - [Separation Recipe](#separation-recipe) — line 265
- [Border System](#border-system) — line 271
  - [Widths and Patterns](#widths-and-patterns) — line 275
  - [Focus Ring](#focus-ring) — line 287
  - [Radius (Global Override)](#radius-global-override) — line 296
- [Component States](#component-states) — line 304
  - [Buttons (Primary)](#buttons-primary) — line 308
  - [Buttons (Ghost)](#buttons-ghost) — line 319
  - [Text Input](#text-input) — line 330
  - [Chat Input Card](#chat-input-card) — line 340
  - [Cards](#cards) — line 349
  - [Sidebar Items](#sidebar-items) — line 357
  - [Chips](#chips) — line 366
  - [Toggle / Switch](#toggle--switch) — line 375
- [Motion Map](#motion-map) — line 397
  - [Easings](#easings) — line 401
  - [Tick Interval](#tick-interval) — line 412
  - [Duration x Easing x Component](#duration-x-easing-x-component) — line 416
  - [Active Press Scale](#active-press-scale) — line 433
- [Layout Tokens](#layout-tokens) — line 439
  - [Spacing Scale](#spacing-scale) — line 449
  - [Density](#density) — line 453
  - [Responsive Notes](#responsive-notes) — line 457
- [Accessibility Tokens](#accessibility-tokens) — line 465
- [Overlays](#overlays) — line 489
  - [Popover / Dropdown](#popover--dropdown) — line 491
  - [Modal](#modal) — line 506
  - [Tooltip](#tooltip) — line 519
- [Visual Style](#visual-style) — line 532
  - [Pixel Components](#pixel-components) — line 534
  - [Material](#material) — line 687
  - [Data Visualization Philosophy](#data-visualization-philosophy) — line 715
- [Signature Animations](#signature-animations) — line 725
  - [1. Pixel Ticker Tape](#1-pixel-ticker-tape) — line 727
  - [2. Grid Cell Update Flash](#2-grid-cell-update-flash) — line 744
  - [3. Status Blink](#3-status-blink) — line 763
  - [4. Step Block Fill](#4-step-block-fill) — line 780
  - [5. Card Entrance (The Exception)](#5-card-entrance-the-exception) — line 800
- [Mode Variant](#mode-variant) — line 819
  - [Warm vs Cool Comparison](#warm-vs-cool-comparison) — line 823
  - [Light Mode Variant](#light-mode-variant) — line 837
- [Mobile Notes](#mobile-notes) — line 869
  - [Effects to Disable](#effects-to-disable) — line 871
  - [Adjustments](#adjustments) — line 877
  - [Performance Notes](#performance-notes) — line 886
- [Implementation Checklist](#implementation-checklist) — line 894

---

## Identity & Philosophy

This theme lives in the world of a Bloomberg terminal reimagined by a design studio. Dense, information-rich surfaces where every pixel earns its place. Data is not decorated — it is presented on a grid, quantized into discrete steps, and read like a broadsheet or a system log. The aesthetic tension: extreme density vs. extreme legibility. Surfaces are packed with information but never cluttered because the grid imposes absolute order.

The theme ships with two thermal modes — **Warm ("Gazette")** and **Cool ("Terminal")** — that share the same spatial system, component architecture, and motion philosophy but diverge completely in palette, typography, and material feel. Warm mode is a newspaper broadsheet: earth tones, cream paper grain, Space Grotesk headlines in ALL CAPS with wide tracking, JetBrains Mono for body text. Cool mode is a Vercel-grade terminal: true black page, vivid blue accents, Inter headlines in sentence case, Geist Mono for body text.

The single unifying signature across both modes: **quantized motion**. Every transition uses CSS `steps(n)` timing. Nothing slides smoothly. Hover states snap on in a single frame via `steps(1)`. Progress bars advance in discrete ticks. Loading animations march in 8-frame loops. This is the visual equivalent of a clock ticking — precise, mechanical, deliberate. The only exception is one card-entrance animation (200ms linear) for initial page load.

**Decision principle:** "When in doubt, ask: does this feel like data on a grid? If it feels smooth, step it. If it feels round, square it. If it feels decorative, remove it."

**What this theme is NOT:**
- Not smooth — if any transition uses `cubic-bezier`, you have missed the point (one exception: card entrance)
- Not rounded — every radius is 0px, no exceptions, no pill shapes, no circles
- Not sparse — density is the default; if there is whitespace, fill it with data
- Not colorful for decoration — color is a data channel, not ornament
- Not a single mode — Warm and Cool are equally valid; neither is "the dark mode of the other"

---

## Color System

#### Warm Mode ("Gazette") Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Warm Charcoal | `#1C1917` | Deepest background. Newsprint dark, warm undertone. |
| bg | Dark Stone | `#292524` | Primary surface. Slightly lifted from page. |
| surface | Antique Cream | `#353130` | Elevated cards, inputs, popovers. Warm mid-tone. |
| recessed | Deep Char | `#0C0A09` | Code blocks, inset data wells. Darkest recessed. |
| active | Warm Highlight | `#44403C` | Active/pressed items, selected rows. |
| text-primary | Parchment | `#FAEBD7` | Headings, body text. Antique white, warm cast. |
| text-secondary | Faded Ink | `rgba(250,235,215,0.64)` | Sidebar items, secondary labels. text-primary at 64%. |
| text-muted | Ghost Ink | `rgba(250,235,215,0.38)` | Placeholders, timestamps, metadata. text-primary at 38%. |
| text-onAccent | Dark Print | `#1C1917` | Text on sienna accent backgrounds. |
| border-base | Warm Edge | `#A8A29E` | Used at variable opacity. Stone 400. |
| accent-primary | Sienna | `#D97757` | Primary CTA, active controls, chart highlight. |
| accent-secondary | Burnt Gold | `#CA8A04` | Secondary accent for links, info callouts. |
| success | Olive Green | `#84CC16` | Positive states. Lime-shifted for warm harmony. |
| warning | Amber | `#F59E0B` | Caution states. |
| danger | Rust Red | `#DC2626` | Error states, destructive actions. |
| info | Warm Blue | `#60A5FA` | Info states, informational chips. |

**Per-Agent Accent System (Warm):** Six agent colors at equal OKLCH lightness (L=0.72, C=0.14):

| Agent | Hex | Hue | Usage |
|---|---|---|---|
| Agent 1 | `#D97757` | 30 (sienna) | Primary agent, default accent |
| Agent 2 | `#CA8A04` | 85 (gold) | Secondary agent |
| Agent 3 | `#84CC16` | 125 (olive) | Tertiary agent |
| Agent 4 | `#06B6D4` | 195 (cyan) | Fourth agent |
| Agent 5 | `#818CF8` | 260 (indigo) | Fifth agent |
| Agent 6 | `#E879A8` | 340 (rose) | Sixth agent |

#### Special Tokens (Warm)

| Token | Value | Role |
|---|---|---|
| inlineCode | `#F97316` | Code text within prose. Orange, high contrast on dark warm. |
| toggleActive | `#84CC16` | Toggle/switch active track. Matches success. |
| selection | `rgba(217,119,87,0.25)` | `::selection` background. Sienna at 25%. |

#### Cool Mode ("Terminal") Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | True Black | `#000000` | Deepest background. Pure black, zero warmth. |
| bg | Dark Grey | `#0A0A0A` | Primary surface. Barely lifted from black. |
| surface | Carbon | `#161616` | Elevated cards, inputs, popovers. Vercel surface. |
| recessed | Void | `#050505` | Code blocks, inset data wells. Near-black. |
| active | Charcoal | `#262626` | Active/pressed items, selected rows. |
| text-primary | Pure White | `#EDEDED` | Headings, body text. Vercel white. |
| text-secondary | Mid Grey | `rgba(237,237,237,0.64)` | Sidebar items, secondary labels. text-primary at 64%. |
| text-muted | Dim Grey | `rgba(237,237,237,0.38)` | Placeholders, timestamps, metadata. text-primary at 38%. |
| text-onAccent | White | `#FFFFFF` | Text on vivid blue accent backgrounds. |
| border-base | Neutral Edge | `#525252` | Used at variable opacity. Neutral 600. |
| accent-primary | Vivid Blue | `#0070F3` | Primary CTA, active controls. Vercel blue. |
| accent-secondary | Cyan | `#00D4FF` | Secondary accent for links, data highlights. |
| success | Neon Green | `#22C55E` | Positive states. |
| warning | Orange | `#F59E0B` | Caution states. |
| danger | Red | `#EF4444` | Error states, destructive actions. |
| info | Light Blue | `#3B82F6` | Info states. |

**Per-Agent Accent System (Cool):** Six agent colors at equal OKLCH lightness (L=0.72, C=0.16):

| Agent | Hex | Hue | Usage |
|---|---|---|---|
| Agent 1 | `#0070F3` | 220 (blue) | Primary agent, default accent |
| Agent 2 | `#00D4FF` | 190 (cyan) | Secondary agent |
| Agent 3 | `#22C55E` | 145 (green) | Tertiary agent |
| Agent 4 | `#F59E0B` | 45 (amber) | Fourth agent |
| Agent 5 | `#A855F7` | 275 (purple) | Fifth agent |
| Agent 6 | `#EC4899` | 330 (pink) | Sixth agent |

#### Special Tokens (Cool)

| Token | Value | Role |
|---|---|---|
| inlineCode | `#00D4FF` | Code text within prose. Cyan, terminal-native. |
| toggleActive | `#22C55E` | Toggle/switch active track. Matches success. |
| selection | `rgba(0,112,243,0.25)` | `::selection` background. Vivid blue at 25%. |

#### Opacity System

Border opacity (on `border-base` per mode):

| Context | Opacity | Usage |
|---|---|---|
| subtle | 12% | Internal dividers, grid lines within cards. |
| card | 20% | Card-level borders, panel edges. |
| hover | 30% | Hovered elements, interactive feedback. |
| focus | 100% (accent) | Focus ring. Full accent color, not border-base. |

#### Color Rules

- Color is a data channel. Every color must encode information — no decorative gradients, no color-for-beauty.
- The per-agent accent system is mandatory for multi-agent UIs. All six hues are perceptually equal — no agent "stands out" by color alone.
- Warm and Cool modes must NEVER be mixed. Pick one per deployment. They share geometry, not palette.
- Semantic colors (success/warning/danger) are slightly shifted per mode for harmony but remain functionally identical.

---

## Typography Matrix

#### Warm Mode ("Gazette")

Headline font: Space Grotesk. Body/data font: JetBrains Mono. Headlines are ALL CAPS with wide tracking — the newspaper broadsheet convention.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Space Grotesk | 18px | 700 | 1.2 | 0.14em | `text-transform: uppercase` | Hero titles, page names. ALL CAPS. |
| Heading | Space Grotesk | 13px | 700 | 1.3 | 0.10em | `text-transform: uppercase` | Section titles, panel headers. ALL CAPS. |
| Body | JetBrains Mono | 13px | 400 | 1.5 | normal | `font-feature-settings: "zero"` | Primary reading text, data tables. |
| Body Small | JetBrains Mono | 11px | 400 | 1.45 | normal | `font-feature-settings: "zero"` | Sidebar items, form labels. |
| Button | Space Grotesk | 11px | 600 | 1.4 | 0.06em | `text-transform: uppercase` | Button labels. ALL CAPS. |
| Input | JetBrains Mono | 13px | 400 | 1.4 | normal | `font-feature-settings: "zero"` | Form input text. |
| Label | Space Grotesk | 9px | 500 | 1.3 | 0.08em | `text-transform: uppercase` | Metadata, timestamps, axis labels. ALL CAPS. |
| Code | JetBrains Mono | 12px | 400 | 1.5 | normal | `font-feature-settings: "liga", "zero"` | Inline code, code blocks. |
| Caption | JetBrains Mono | 9px | 400 | 1.33 | normal | -- | Footnotes, disclaimers, tiny data annotations. |

#### Cool Mode ("Terminal")

Headline font: Inter. Body/data font: Geist Mono. Headlines are sentence case — the Vercel convention.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Inter | 17px | 600 | 1.2 | -0.02em | -- | Hero titles, page names. Sentence case. |
| Heading | Inter | 13px | 600 | 1.3 | -0.01em | -- | Section titles, panel headers. |
| Body | Geist Mono | 13px | 400 | 1.5 | normal | -- | Primary reading text, data tables. |
| Body Small | Geist Mono | 11px | 400 | 1.45 | normal | -- | Sidebar items, form labels. |
| Button | Inter | 11px | 500 | 1.4 | 0.01em | -- | Button labels. |
| Input | Geist Mono | 13px | 400 | 1.4 | normal | -- | Form input text. |
| Label | Inter | 9px | 500 | 1.3 | 0.04em | `text-transform: uppercase` | Metadata, timestamps, axis labels. |
| Code | Geist Mono | 12px | 400 | 1.5 | normal | -- | Inline code, code blocks. |
| Caption | Geist Mono | 9px | 400 | 1.33 | normal | -- | Footnotes, disclaimers, tiny data annotations. |

#### Font Loading

**Warm mode:**
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

**Cool mode:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600&family=Geist+Mono:wght@400&display=swap" rel="stylesheet">
```

---

## Elevation System

**Strategy:** `borders-only`

This is a flat theme. Depth is communicated through border weight and surface tint, not shadows. Warm mode has ZERO shadows. Cool mode has exactly one shadow: a subtle popover drop.

#### Surface Hierarchy

| Surface | Background (Warm) | Background (Cool) | Shadow | Usage |
|---|---|---|---|---|
| page | `#1C1917` | `#000000` | none | Main page canvas |
| bg | `#292524` | `#0A0A0A` | none | Primary surface, sidebar bg |
| surface | `#353130` | `#161616` | none | Cards, inputs, elevated panels |
| recessed | `#0C0A09` | `#050505` | none | Code blocks, data wells |
| active | `#44403C` | `#262626` | none | Active/pressed, selected rows |
| overlay | `#353130` | `#161616` | shadow-popover (Cool only) | Popovers, dropdowns |

#### Shadow Tokens

| Token | Warm Value | Cool Value | Usage |
|---|---|---|---|
| shadow-none | `none` | `none` | All standard surfaces. Default. |
| shadow-popover | `none` | `0 4px 12px rgba(0,0,0,0.5), 0 0 0 1px rgba(82,82,82,0.20)` | Popovers/dropdowns. Cool mode only. |
| shadow-input | `none` | `none` | Input card rest. Flat. |
| shadow-input-hover | `none` | `none` | Input card hover. Flat. |
| shadow-input-focus | `none` | `0 0 0 2px var(--accent-primary)` | Input card focus. Ring only. |

#### Separation Recipe

Borders-only. Surfaces separate through tint-step (each level is 1-2 stops lighter on a grey ramp) and border weight (1px internal, 1.5px card, 2px heavy). No shadows in Warm mode. One popover shadow in Cool mode for dropdowns/menus only. No dividers inside cards — grid alignment itself creates visual grouping. Dense spacing + consistent grid = implicit separation.

---

## Border System

ALL border-radius values are `0px`. No exceptions. Rectangles only.

#### Widths and Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| internal | 1px | `border-base` at 12% | Dividers within cards, grid lines, separators. |
| card | 1.5px | `border-base` at 20% | Card edges, panel boundaries, input borders. |
| heavy | 2px | `border-base` at 30% | Section dividers, header underlines, emphasis borders. |
| input | 1.5px | `border-base` at 20% | Form input borders at rest. Same as card. |
| input-hover | 1.5px | `border-base` at 30% | Input hover. |
| input-focus | 1.5px | accent-primary at 100% | Input focus. Full accent color. |
| accent-left | 2px | accent-primary at 100% | Left-border accent on active sidebar items, callouts. |

#### Focus Ring

- **Warm mode:** `2px solid #D97757` (sienna accent)
- **Cool mode:** `2px solid #0070F3` (vivid blue accent)
- **Width:** 2px solid
- **Offset:** 2px (via `outline-offset: 2px`)
- **Implementation:** `outline: 2px solid var(--accent-primary); outline-offset: 2px;`
- **No inner white ring.** The sharp rectangular outline on a dark background provides sufficient contrast.

#### Radius (Global Override)

| Token | Value |
|---|---|
| none / sm / md / lg / xl / 2xl / input / full | ALL `0px` |

---

## Component States

All transitions are `steps(1)` (instant snap) unless explicitly noted otherwise.

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `accent-primary`, border none, color `text-onAccent`, radius 0px, h 32px, padding `0 12px`, font button |
| Hover | bg `accent-primary` lightened 8% (Warm: `#E0916F`, Cool: `#1A80F5`), transition `steps(1)` |
| Active | bg `accent-primary` darkened 10% (Warm: `#C46845`, Cool: `#005BC2`), no transform (no scale on pixel grid) |
| Focus | outline `2px solid var(--accent-primary)`, outline-offset 2px |
| Disabled | opacity 0.35, pointer-events none, cursor not-allowed |
| Transition | `background 0ms steps(1)` — instant color snap |

#### Buttons (Ghost)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid border-base at 12%`, color `text-secondary`, radius 0px, h 32px, padding `0 12px` |
| Hover | bg `active`, border at 20%, color `text-primary`, transition `steps(1)` |
| Active | bg `surface`, border at 30% |
| Focus | outline focus ring |
| Disabled | opacity 0.35, pointer-events none |
| Transition | `all 0ms steps(1)` — instant snap |

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `surface`, border `1.5px solid border-base at 20%`, radius 0px, h 36px, padding `0 8px`, font input, color `text-primary`, placeholder `text-muted`, caret-color `accent-primary` |
| Hover | border at 30% opacity, transition `steps(1)` |
| Focus | border `1.5px solid accent-primary`, outline none, box-shadow `0 0 0 1px var(--accent-primary)` (Cool only) |
| Disabled | opacity 0.35, pointer-events none, bg `bg` |
| Transition | `border-color 0ms steps(1)` |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `surface`, radius 0px, border `1.5px solid border-base at 20%`, shadow none |
| Hover | border at 30%, transition `steps(1)` |
| Focus-within | border `1.5px solid accent-primary` |
| Transition | `all 0ms steps(1)` |

#### Cards

| State | Properties |
|---|---|
| Rest | bg `surface`, border `1.5px solid border-base at 20%`, radius 0px, shadow none |
| Hover | border at 30%, bg lightened 1 stop (Warm: `#3D3937`, Cool: `#1A1A1A`), transition `steps(1)` |
| Transition | `all 0ms steps(1)` |

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `text-secondary`, radius 0px, h 32px, padding `4px 12px`, font bodySmall |
| Hover | bg `active`, color `text-primary`, transition `steps(1)` |
| Active (current) | bg `active`, color `text-primary`, border-left `2px solid accent-primary`, padding-left 10px (compensate border) |
| Transition | `all 0ms steps(1)` |

#### Chips

| State | Properties |
|---|---|
| Rest | bg `bg`, border `1px solid border-base at 12%`, radius 0px, h 24px, padding `0 8px`, font label (9px), color `text-secondary` |
| Hover | bg `active`, border at 20%, color `text-primary`, transition `steps(1)` |
| Active/selected | bg `accent-primary`, color `text-onAccent`, border accent-primary |
| Transition | `all 0ms steps(1)` |

#### Toggle / Switch

**Theme override:** Rectangular toggle. NOT pill-shaped. 36x18px sharp rectangle.

| Property | Value |
|---|---|
| Track width | 36px |
| Track height | 18px |
| Track radius | 0px |
| Track off bg | `active` token (Warm: `#44403C`, Cool: `#262626`) |
| Track off border | `1.5px solid border-base at 20%` |
| Track on bg | `toggleActive` (Warm: `#84CC16`, Cool: `#22C55E`) |
| Track on border | none |
| Thumb | 14x14px square, bg `text-primary`, 0px radius |
| Thumb off position | left 2px |
| Thumb on position | right 2px |
| Thumb shadow | none |
| Transition | `all 0ms steps(1)` — thumb snaps between positions, no slide |
| Focus-visible | focus ring around entire track |

---

## Motion Map

**Core philosophy:** All motion is quantized. The `steps(n)` CSS timing function is the only permitted easing. `cubic-bezier` is banned except for the single card-entrance exception.

#### Easings

| Name | Value | Character |
|---|---|---|
| instant | `steps(1)` | Single-frame snap. The default for all interactions. |
| tick-2 | `steps(2)` | Two-frame blink. Loading indicators. |
| tick-4 | `steps(4)` | Four-frame stutter. Progress bars. |
| tick-8 | `steps(8)` | Eight-frame march. Signature step animation. |
| tick-16 | `steps(16)` | Sixteen-frame sequence. Smooth-ish for large movements. |
| card-entrance | `linear` | ONLY exception. 200ms linear for initial card entrance. |

#### Tick Interval

The base tick interval is **800ms**. All `steps(n)` animations have their total duration derived from `800ms / n` per step or multiples thereof. An 8-step animation over 800ms = 100ms per frame.

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Button hover bg | 0ms | `steps(1)` | Instant color snap |
| Sidebar item hover | 0ms | `steps(1)` | Instant bg/color snap |
| Toggle thumb position | 0ms | `steps(1)` | Thumb teleports, no slide |
| Chip hover/select | 0ms | `steps(1)` | Instant state change |
| Input focus border | 0ms | `steps(1)` | Instant border color |
| Card hover border | 0ms | `steps(1)` | Instant border opacity |
| Card entrance | 200ms | `linear` | Opacity 0-to-1 fade-in on mount. THE exception. |
| Progress bar advance | 800ms | `steps(8)` | 8-step march per segment |
| Status indicator blink | 800ms | `steps(2)` | On/off blink at 400ms intervals |
| Data cell update flash | 400ms | `steps(4)` | Brief highlight on value change |
| Step block fill | 1600ms | `steps(16)` | Loading/progress across 16 steps |
| Pixel icon animation | 800ms | `steps(8)` | Sprite-like frame sequence |

#### Active Press Scale

**None.** No scale transforms on any element. Pixel Grid does not use `transform: scale()`. Active states are communicated through color/background change only, snapped via `steps(1)`.

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column |
| Narrow max-width | 640px | Focused data views |
| Sidebar width | 260px | Fixed sidebar, dense |
| Header height | 40px | Compact top bar |
| Spacing unit | 4px | Base grid multiplier. ALL spacing is 4px multiples. |

#### Spacing Scale

4, 8, 12, 16, 24, 32, 48px — strictly 4px-aligned. No 6px, no 10px.

#### Density

**Dense.** 4-8px internal padding on cards. 4px gaps between list items. 12-16px section spacing. This theme prioritizes information density over breathing room.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (260px) + content column. Data tables at full width with horizontal scroll.
- **md (768px):** Sidebar collapses to icon-only rail (48px) or hidden. Content fills available width.
- **sm (640px):** Single column. Header simplifies to hamburger. Data tables switch to stacked card view. Pixel components scale down but maintain grid alignment.

---

## Accessibility Tokens

| Token | Warm Value | Cool Value |
|---|---|---|
| Focus ring color | `#D97757` (sienna) | `#0070F3` (vivid blue) |
| Focus ring width | 2px solid | 2px solid |
| Focus ring offset | 2px | 2px |
| Disabled opacity | 0.35 | 0.35 |
| Disabled pointer-events | none | none |
| Disabled cursor | not-allowed | not-allowed |
| Selection bg | `rgba(217,119,87,0.25)` | `rgba(0,112,243,0.25)` |
| Selection color | `#FAEBD7` (text-primary) | `#EDEDED` (text-primary) |
| Scrollbar width | thin | thin |
| Scrollbar thumb | `rgba(168,162,158,0.25)` | `rgba(82,82,82,0.30)` |
| Scrollbar track | transparent | transparent |
| Min touch target | 44px | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large) | WCAG AA (4.5:1 text, 3:1 large) |

**Contrast notes:** Warm mode `#FAEBD7` on `#1C1917` = 13.2:1. Cool mode `#EDEDED` on `#000000` = 18.1:1. Both exceed AAA. Accent text: Warm `#D97757` on `#1C1917` = 4.8:1 (passes AA). Cool `#0070F3` on `#000000` = 4.6:1 (passes AA).

**Reduced motion:** All `steps(n)` animations collapse to `steps(1)` (instant). Card entrance animation disabled entirely. Status blink animations pause. Pixel component animations freeze to static state.

---

## Overlays

#### Popover / Dropdown

- **bg:** `surface` token (Warm: `#353130`, Cool: `#161616`)
- **backdrop-filter:** none (Warm), `blur(4px)` (Cool — subtle only)
- **border:** `1.5px solid border-base at 25%`
- **radius:** 0px
- **shadow:** none (Warm), shadow-popover (Cool)
- **padding:** 4px
- **z-index:** 50
- **min-width:** 180px, **max-width:** 280px
- **Menu item:** 4px 8px padding, radius 0px, h 28px, font bodySmall, color text-secondary
- **Menu item hover:** bg `active`, color `text-primary`, transition `steps(1)`
- **Entry:** opacity 0 to 1, 0ms `steps(1)` — pops in instantly
- **Exit:** opacity 1 to 0, 0ms `steps(1)` — pops out instantly

#### Modal

- **Overlay bg:** Warm: `rgba(28,25,23,0.85)`, Cool: `rgba(0,0,0,0.85)`
- **Overlay backdrop-filter:** none (Warm), `blur(4px)` (Cool)
- **Content bg:** `surface` token
- **Content border:** `2px solid border-base at 30%`
- **Content radius:** 0px
- **Content shadow:** none (Warm), shadow-popover (Cool)
- **Content padding:** 16px
- **Entry:** opacity 0 to 1, 0ms `steps(1)` — instant appearance
- **Exit:** opacity 1 to 0, 0ms `steps(1)` — instant disappearance
- **Close button:** Ghost button, top-right, 32x32px

#### Tooltip

- **bg:** `active` token (Warm: `#44403C`, Cool: `#262626`)
- **color:** `text-primary`
- **font:** label size (9px), weight 400
- **border:** `1px solid border-base at 20%`
- **radius:** 0px
- **padding:** 4px 8px
- **shadow:** none
- **No arrow.** Position via offset. Appears instantly via `steps(1)`.

---

## Visual Style

#### Pixel Components

Five bespoke pixel-art components unique to this theme. These are NOT icons — they are functional UI elements built from discrete pixel blocks on a grid.

##### 1. Mosaic Status Bar

A horizontal bar composed of 4x4px squares. Each square represents a data point or time slice, colored by status. The bar reads left-to-right as a timeline.

- **Dimensions:** Full content width, 4px tall (single row) or 8px tall (double row)
- **Cell size:** 4x4px, no gap between cells
- **Colors:** success (green), warning (amber), danger (red), `bg` (no data/neutral)
- **Border:** none — cells are contiguous
- **CSS:** `display: grid; grid-template-columns: repeat(auto-fill, 4px); grid-auto-rows: 4px;`
- **Usage:** Uptime bars, build status history, activity timelines

##### 2. 3x3 Status Grid

A 3x3 matrix of squares that encodes system health across 9 dimensions. Think of it as a tiny heatmap.

- **Dimensions:** 24x24px total (3 columns x 3 rows, 8x8px per cell, no gap)
- **Cell size:** 8x8px, 0px gap
- **Colors:** Gradient from `bg` (idle) through `accent-primary` (active) to `danger` (critical)
- **Border:** `1px solid border-base at 12%` around the entire grid
- **CSS:** `display: grid; grid-template-columns: repeat(3, 8px); grid-template-rows: repeat(3, 8px);`
- **Usage:** Service health matrix, multi-metric status at a glance

##### 3. Pixel Bar Chart

Vertical bars built from stacked 4x4px blocks instead of smooth rectangles. Values are quantized to the nearest 4px increment.

- **Bar width:** 4px per bar (or 8px for wider variant)
- **Bar gap:** 2px between bars (or 4px for wider)
- **Block size:** 4x4px per unit
- **Max height:** 40px (10 blocks) or 80px (20 blocks)
- **Fill color:** `accent-primary`, with top block optionally highlighted at 80% opacity for "partial" final unit
- **Empty color:** `bg` token
- **Axis:** Optional bottom label in `caption` font, left axis in `label` font
- **CSS:** Each bar is `display: flex; flex-direction: column-reverse;` with `div` blocks
- **Usage:** Sparklines, inline metrics, histogram bins

##### 4. Step Blocks

A horizontal progress indicator made of discrete blocks. Similar to a segmented progress bar but with hard edges and no fill animation.

- **Block count:** Variable (typically 5, 8, 10, or 16)
- **Block size:** 8x8px per block, 2px gap
- **Filled color:** `accent-primary`
- **Empty color:** `border-base at 12%`
- **Active (current) block:** `accent-primary` at 60% opacity (blinks at `steps(2)` 800ms if animated)
- **Border:** none per block — color alone differentiates
- **CSS:** `display: flex; gap: 2px;` with square `div` children
- **Usage:** Progress indicators, step completion, capacity meters

##### 5. 7x7 Pixel Icons

A set of icons rendered on a 7x7 pixel grid. Each icon is defined as a bitmap pattern where filled cells use `text-primary` and empty cells are transparent. The 7x7 grid at 3px per cell = 21x21px rendered size.

- **Grid:** 7 columns x 7 rows
- **Cell size:** 3x3px, 0px gap
- **Filled color:** `text-primary` (or `accent-primary` for active state)
- **Rendered size:** 21x21px
- **CSS:** `display: grid; grid-template-columns: repeat(7, 3px); grid-template-rows: repeat(7, 3px);`

**Icon bitmap patterns** (1 = filled, 0 = empty):

**Arrow right:**
```
0 0 0 1 0 0 0
0 0 0 0 1 0 0
0 0 0 0 0 1 0
1 1 1 1 1 1 1
0 0 0 0 0 1 0
0 0 0 0 1 0 0
0 0 0 1 0 0 0
```

**Checkmark:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 1
0 0 0 0 0 1 0
0 0 0 0 1 0 0
1 0 0 1 0 0 0
0 1 1 0 0 0 0
0 0 0 0 0 0 0
```

**Warning (exclamation):**
```
0 0 0 1 0 0 0
0 0 0 1 0 0 0
0 0 0 1 0 0 0
0 0 0 1 0 0 0
0 0 0 1 0 0 0
0 0 0 0 0 0 0
0 0 0 1 0 0 0
```

**Close (X):**
```
1 0 0 0 0 0 1
0 1 0 0 0 1 0
0 0 1 0 1 0 0
0 0 0 1 0 0 0
0 0 1 0 1 0 0
0 1 0 0 0 1 0
1 0 0 0 0 0 1
```

**Settings (gear):**
```
0 1 0 1 0 1 0
1 1 1 1 1 1 1
0 1 0 0 0 1 0
1 1 0 0 0 1 1
0 1 0 0 0 1 0
1 1 1 1 1 1 1
0 1 0 1 0 1 0
```

**Chart (bar):**
```
0 0 0 0 0 1 0
0 0 0 0 0 1 0
0 0 0 1 0 1 0
0 0 0 1 0 1 0
0 1 0 1 0 1 0
0 1 0 1 0 1 0
1 1 1 1 1 1 1
```

**Search (magnifier):**
```
0 1 1 1 0 0 0
1 0 0 0 1 0 0
1 0 0 0 1 0 0
1 0 0 0 1 0 0
0 1 1 1 0 0 0
0 0 0 0 1 0 0
0 0 0 0 0 1 0
```

**Menu (hamburger):**
```
0 0 0 0 0 0 0
1 1 1 1 1 1 1
0 0 0 0 0 0 0
1 1 1 1 1 1 1
0 0 0 0 0 0 0
1 1 1 1 1 1 1
0 0 0 0 0 0 0
```

#### Material

- **Grain (Warm mode only):** Subtle paper grain via SVG feTurbulence filter at 1-2% opacity. Apply as a full-screen overlay with `pointer-events: none`.

```html
<svg width="0" height="0" style="position:absolute">
  <filter id="paper-grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch" />
    <feColorMatrix type="saturate" values="0" />
  </filter>
</svg>
```
```css
.grain-overlay {
  position: fixed; inset: 0;
  opacity: 0.018;
  filter: url(#paper-grain);
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: overlay;
}
```

- **Grain (Cool mode):** None. Pure digital surfaces. No noise, no texture.
- **Gloss:** Matte. Zero sheen, zero reflections. Surfaces are flat and opaque.
- **Blend mode:** Normal (Cool), overlay for grain layer only (Warm).
- **Shader bg:** False. No WebGL, no canvas backgrounds.

#### Data Visualization Philosophy

The quantized aesthetic extends to all charts and data visualization:

- **YES:** Stepped line charts (values jump between discrete levels), bar charts (pixel blocks), heatmaps (grid cells), treemaps (rectangular), tables (the native format).
- **NO:** Smooth line charts, Bezier curves, radial/circular charts, pie charts, donut charts, gauges with sweep arcs.
- **Partially:** Area charts (allowed if filled with stacked pixel rows, not smooth gradients), scatter plots (each dot is a square pixel, not a circle).

---

## Signature Animations

#### 1. Pixel Ticker Tape

A horizontal data feed that advances in discrete `steps(8)` increments rather than smooth scrolling. Text and values appear to be typed by a mechanical printer — each character appears in a stepped sequence.

- **Technique:** `transform: translateX()` animation with `steps(8)` timing
- **Duration:** 800ms per 8-character advance
- **Easing:** `steps(8)`
- **CSS:**
```css
@keyframes ticker-advance {
  from { transform: translateX(0); }
  to { transform: translateX(-100%); }
}
.ticker { animation: ticker-advance 6400ms steps(64) infinite; }
```
- **Reduced motion:** Paused. Shows static text.

#### 2. Grid Cell Update Flash

When a data value changes, the cell background flashes through a 4-step color sequence: `accent-primary` (100%) -> `accent-primary` (60%) -> `accent-primary` (30%) -> `surface` (rest). Each step holds for 100ms.

- **Technique:** `background-color` keyframe animation with `steps(4)`
- **Duration:** 400ms total (100ms per frame)
- **Easing:** `steps(4)`
- **CSS:**
```css
@keyframes cell-flash {
  0%   { background: var(--accent-primary); }
  25%  { background: color-mix(in oklch, var(--accent-primary) 60%, var(--surface)); }
  50%  { background: color-mix(in oklch, var(--accent-primary) 30%, var(--surface)); }
  100% { background: var(--surface); }
}
.cell-updated { animation: cell-flash 400ms steps(4) forwards; }
```
- **Reduced motion:** Instant background change, no flash sequence.

#### 3. Status Blink

Active status indicators blink on/off at a steady 800ms interval using `steps(2)`. The indicator alternates between `accent-primary` and `transparent` — a mechanical heartbeat.

- **Technique:** `opacity` animation with `steps(2)`
- **Duration:** 800ms (400ms on, 400ms off)
- **Easing:** `steps(2)`
- **CSS:**
```css
@keyframes status-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
.status-active { animation: status-blink 800ms steps(2) infinite; }
```
- **Reduced motion:** Static at full opacity, no blink.

#### 4. Step Block Fill

Progress fills across step blocks one at a time in sequence. Each block snaps from empty to filled — no gradual fill within a single block.

- **Technique:** Sequential `background-color` changes via CSS animation delay
- **Duration:** 100ms per block transition, total = blocks x 100ms
- **Easing:** `steps(1)` per block
- **CSS:**
```css
.step-block {
  background: var(--border-base-12);
  transition: background 0ms steps(1);
}
.step-block.filled {
  background: var(--accent-primary);
}
/* Stagger via animation-delay: nth-child(1) 0ms, nth-child(2) 100ms, etc. */
```
- **Reduced motion:** All blocks fill simultaneously.

#### 5. Card Entrance (The Exception)

The ONLY non-stepped animation. Cards fade in with `opacity: 0` to `opacity: 1` over 200ms linear on initial page mount. This provides a gentle entry without violating the grid aesthetic — linear timing has no curves.

- **Technique:** `opacity` animation with `linear` timing
- **Duration:** 200ms
- **Easing:** `linear` (NOT cubic-bezier — linear is permitted because it has no curve)
- **CSS:**
```css
@keyframes card-enter {
  from { opacity: 0; }
  to { opacity: 1; }
}
.card { animation: card-enter 200ms linear both; }
```
- **Reduced motion:** Instant appearance, no fade.

---

## Mode Variant

Both Warm and Cool modes are dark themes. The light mode variant is provided below for applications that require it.

#### Warm vs Cool Comparison

| Dimension | Warm ("Gazette") | Cool ("Terminal") |
|---|---|---|
| Page bg | `#1C1917` (warm charcoal) | `#000000` (true black) |
| Temperature | Warm, earthy | Cold, clinical |
| Headline font | Space Grotesk, ALL CAPS, wide tracking | Inter, sentence case, tight tracking |
| Body font | JetBrains Mono | Geist Mono |
| Accent | Sienna `#D97757` | Vivid Blue `#0070F3` |
| Grain | Yes (1-2% feTurbulence paper noise) | No grain |
| Shadows | Zero — borders only | One popover shadow |
| Text color | Antique white `#FAEBD7` | Pure grey-white `#EDEDED` |
| Vibe | Newspaper broadsheet, financial terminal | Vercel dashboard, developer IDE |

#### Light Mode Variant

For both Warm and Cool, the light variant inverts the surface ramp while preserving the same accent system and motion philosophy.

| Token | Warm Light | Cool Light |
|---|---|---|
| page | `#F5F0EB` (warm off-white) | `#FAFAFA` (near-white) |
| bg | `#EDE8E3` (warm cream) | `#F0F0F0` (light grey) |
| surface | `#FFFFFF` (white) | `#FFFFFF` (white) |
| recessed | `#E5DFD9` (warm tan) | `#E5E5E5` (grey) |
| active | `#DDD7D0` (warm highlighted) | `#D4D4D4` (dark grey highlight) |
| text-primary | `#1C1917` (warm charcoal) | `#0A0A0A` (near-black) |
| text-secondary | `rgba(28,25,23,0.64)` | `rgba(10,10,10,0.64)` |
| text-muted | `rgba(28,25,23,0.38)` | `rgba(10,10,10,0.38)` |
| border-base | `#78716C` (stone 500) | `#A3A3A3` (neutral 400) |
| accent-primary | `#C45C3E` (darker sienna for contrast) | `#0060D0` (darker blue for contrast) |
| success | `#65A30D` (darker olive) | `#16A34A` (darker green) |
| warning | `#D97706` (darker amber) | `#D97706` (darker amber) |
| danger | `#B91C1C` (darker red) | `#DC2626` (darker red) |
| inlineCode | `#C2410C` (dark orange) | `#0369A1` (dark cyan) |
| scrollbar thumb | `rgba(120,113,108,0.25)` | `rgba(163,163,163,0.30)` |
| selection bg | `rgba(196,92,62,0.20)` | `rgba(0,96,208,0.20)` |

**Light mode rules:**
- Paper grain (Warm) increases to 2.5% opacity on light backgrounds
- Shadows remain zero (Warm) / one popover (Cool) — light mode does not add shadows
- Border opacity values shift: subtle 8%, card 15%, hover 22% (lighter background needs less border)
- Focus ring remains same accent color, 2px solid, 2px offset
- All motion remains `steps(n)` — light mode does not change the animation system

---

## Mobile Notes

#### Effects to Disable
- Ticker tape animation (signature #1) — pauses, shows static value
- Grid cell update flash animation (signature #2) — instant color change only
- Status blink animation reduced to 1600ms interval (half-speed) to reduce visual noise
- Paper grain overlay (Warm mode) — disabled entirely on mobile for performance

#### Adjustments
- Header height: 40px (unchanged — already compact)
- Sidebar: hidden by default, slides in as overlay (instant via `steps(1)`)
- Pixel component minimum cell size: 4px (unchanged — already at minimum)
- Touch targets: all interactive elements maintain 44px minimum tap area even if visual size is smaller (extend hit area with padding)
- Font sizes: Body stays 13px mono (already small enough to be dense, large enough to be readable on mobile)
- 7x7 pixel icons scale to 4px per cell = 28x28px rendered (from 21x21px desktop) for touch-friendliness
- Data tables: horizontal scroll with sticky first column, or collapse to card layout below 640px

#### Performance Notes
- No `backdrop-filter` in Warm mode (already none). Cool mode popover blur is only 4px — negligible cost.
- No box-shadow compositing — borders-only strategy is GPU-friendly.
- `steps(n)` animations are cheaper than `cubic-bezier` — the browser skips interpolation frames.
- Paper grain SVG filter (Warm mode) is the single most expensive effect — disable on mobile first.

---

## Implementation Checklist

- [ ] Google Fonts loaded: Space Grotesk (500, 600, 700) + JetBrains Mono (400) for Warm; Inter (500, 600) + Geist Mono (400) for Cool
- [ ] CSS custom properties defined for ALL color tokens per mode (use `data-theme="warm"` / `data-theme="cool"` attribute)
- [ ] ALL border-radius values set to 0px globally (`* { border-radius: 0 !important; }` as safety net)
- [ ] Border weight hierarchy applied: 1px internal, 1.5px card, 2px heavy
- [ ] Border opacity system implemented: 12% subtle, 20% card, 30% hover
- [ ] Focus ring uses `outline: 2px solid var(--accent-primary); outline-offset: 2px` on all interactive elements
- [ ] All transitions use `steps(1)` or `steps(n)` — zero `cubic-bezier` (except card entrance `linear`)
- [ ] `prefers-reduced-motion` media query: all `steps(n>1)` collapse to `steps(1)`, card entrance disabled, blink animations paused
- [ ] Toggle is rectangular (36x18px, 0px radius, square 14x14px thumb)
- [ ] 5 pixel components implemented with correct grid dimensions and colors
- [ ] 7x7 pixel icon set rendered with bitmap patterns
- [ ] Paper grain SVG filter applied in Warm mode (disabled on mobile)
- [ ] Typography strict 3-size hierarchy enforced (9-11px / 12-13px / 17-18px)
- [ ] Per-agent accent system implemented with 6 colors at equal OKLCH lightness
- [ ] Scrollbar styled: thin, border-base thumb at 25-30%, transparent track
- [ ] `::selection` styled with accent-primary at 25%
- [ ] `::placeholder` opacity matches text-muted token
- [ ] Touch targets >= 44px on all interactive elements
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] Data visualization follows quantized philosophy: stepped lines, pixel bars, no smooth curves
- [ ] Light mode variant: all surface tokens swap, border opacity decreases, accent colors darken for contrast
- [ ] `font-feature-settings: "zero"` applied to JetBrains Mono (Warm mode) for slashed zeros
- [ ] Warm mode `text-transform: uppercase` applied to all Space Grotesk usage (display, heading, button, label)
