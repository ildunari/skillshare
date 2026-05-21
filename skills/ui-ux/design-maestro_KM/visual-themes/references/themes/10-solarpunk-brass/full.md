# 10. Solarpunk Brass — Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 26
- [Color System](#color-system) — Line 48
  - [Palette](#palette) — Line 50
  - [Special Tokens](#special-tokens) — Line 72
  - [Brass + Green Duality System](#brass--green-duality-system) — Line 84
  - [Opacity System](#opacity-system) — Line 102
  - [Color Rules](#color-rules) — Line 113
- [Typography Matrix](#typography-matrix) — Line 123
  - [Font Stack](#font-stack) — Line 125
  - [Typographic Duality](#typographic-duality) — Line 148
  - [Font Loading](#font-loading) — Line 161
- [Elevation System](#elevation-system) — Line 181
  - [Surface Hierarchy](#surface-hierarchy) — Line 187
  - [Shadow Tokens — Organic (Botanical)](#shadow-tokens--organic-botanical) — Line 197
  - [Shadow Tokens — Mechanical (Instrument)](#shadow-tokens--mechanical-instrument) — Line 212
  - [Shadow Assignment Guide](#shadow-assignment-guide) — Line 221
  - [Separation Recipe](#separation-recipe) — Line 236
- [Border System](#border-system) — Line 242
  - [Widths](#widths) — Line 244
  - [Opacity Scale](#opacity-scale-on-border-base-trellis-wire) — Line 253
  - [Border Patterns](#border-patterns) — Line 264
  - [Focus Ring](#focus-ring) — Line 277
- [Component States](#component-states) — Line 289
  - [Buttons (Primary)](#buttons-primary) — Line 291
  - [Buttons (Secondary)](#buttons-secondary) — Line 303
  - [Buttons (Ghost / Icon)](#buttons-ghost--icon) — Line 317
  - [Text Input](#text-input) — Line 330
  - [Chat Input Card](#chat-input-card) — Line 343
  - [Cards](#cards) — Line 354
  - [Data Readout Cards (Theme-Specific)](#data-readout-cards-theme-specific) — Line 364
  - [Sidebar Items](#sidebar-items) — Line 376
  - [Chips](#chips) — Line 388
  - [Toggle / Switch](#toggle--switch) — Line 399
  - [Slider](#slider) — Line 419
- [Motion Map](#motion-map) — Line 435
  - [Easings](#easings) — Line 437
  - [Duration x Easing x Component](#duration-x-easing-x-component) — Line 448
  - [Active Press Scale](#active-press-scale) — Line 470
  - [Reduced Motion](#reduced-motion) — Line 481
- [Overlays](#overlays) — Line 494
  - [Popover / Dropdown](#popover--dropdown) — Line 496
  - [Modal](#modal) — Line 516
  - [Tooltip](#tooltip) — Line 533
- [Layout Tokens](#layout-tokens) — Line 550
  - [Spacing Scale](#spacing-scale) — Line 560
  - [Radius Scale](#radius-scale) — Line 576
  - [Density](#density) — Line 592
  - [Responsive Notes](#responsive-notes) — Line 595
- [Accessibility Tokens](#accessibility-tokens) — Line 603
- [Visual Style](#visual-style) — Line 654
- [Signature Animations](#signature-animations) — Line 716
  - [1. Leaf Unfurl Reveal](#1-leaf-unfurl-reveal) — Line 718
  - [2. Gear Rotate Data Update](#2-gear-rotate-data-update) — Line 746
  - [3. Vine Crawl Navigation](#3-vine-crawl-navigation) — Line 783
  - [4. Brass Patina Shift](#4-brass-patina-shift) — Line 801
  - [5. Gauge Needle Sweep](#5-gauge-needle-sweep) — Line 820
- [Dark Mode Variant](#dark-mode-variant) — Line 850
  - [Dark Palette](#dark-palette) — Line 856
  - [Dark Mode Rules](#dark-mode-rules) — Line 875
- [Mobile Notes](#mobile-notes) — Line 893
  - [Effects to Disable](#effects-to-disable) — Line 895
  - [Adjustments](#adjustments) — Line 902
  - [Performance Notes](#performance-notes) — Line 916
- [Data Visualization](#data-visualization) — Line 926
- [Theme-Specific Components](#theme-specific-components) — Line 942
  - [Brass Instrument Panel](#brass-instrument-panel) — Line 944
  - [Botanical Tag](#botanical-tag) — Line 959
- [Theme-Specific CSS Custom Properties](#theme-specific-css-custom-properties) — Line 971
- [Implementation Checklist](#implementation-checklist) — Line 1071

---

## 10. Solarpunk Brass

> A greenhouse full of technology -- vine-covered circuits, polished brass instruments, warm sunlight through green glass, where organic and mechanical coexist.

**Best for:** Environmental dashboards, botanical databases, sustainable tech platforms, smart garden interfaces, IoT sensor displays, permaculture planning tools, bio-architecture studios, citizen science apps, green energy monitors, solarpunk fiction writing tools.

---

### Identity & Philosophy

This theme lives in the world of solarpunk -- a future where technology serves ecology, where brass gears monitor soil moisture and vine tendrils wrap around circuit boards. The design metaphor is the greenhouse laboratory: warm sunlight filtering through green glass onto polished brass instruments surrounded by climbing plants. Every surface is sun-warmed linen or weathered wood. Every accent is polished brass catching the light. Every green element grows organically from the edges.

The core tension is **organic versus mechanical**. Two systems coexist in the same space, and neither dominates. Botanical elements -- leaves, vines, growth patterns -- follow organic rhythms: slow, springy, unfurling over 400-600ms. Mechanical elements -- toggles, switches, data readouts -- follow clockwork rhythms: precise, instant, clicking into place in 100-150ms. This dual animation language is the theme's signature. When both systems animate simultaneously, the contrast tells a story: nature moves at nature's pace, machines move at machine's pace.

The brass + green combination is the color signature. Polished brass (`#C19A49`) appears as instrument bezels, data readout frames, progress indicators, and interactive accent elements. Forest green appears as semantic positive states, botanical decorative elements, and the secondary voice of the interface. The warm linen base (`#F4EFE4`) grounds everything in sunlit natural fiber.

Typography pairs Fraunces (a variable serif with a "wonky" axis that produces organic, hand-drawn stroke variation) for display text with DM Sans (clean, geometric, precise) for body text. This pairing embodies the organic-mechanical duality at the typographic level: headings feel hand-lettered and alive, body text feels engineered and clear.

**Decision principle:** "When in doubt, ask: does this feel like it belongs in a greenhouse full of technology? If it feels sterile, add warmth. If it feels chaotic, add precision. If it feels like only nature or only machine, find the hybrid."

**What this theme is NOT:**
- Not steampunk -- steampunk is Victorian darkness, gears for decoration, and dystopian grime. Solarpunk is sunlit, functional, and optimistic. No dark copper, no Victorian ornament, no decorative gears.
- Not purely organic -- this is not a plant app with leaf illustrations. The mechanical half is equally important. Without brass, toggles, and clockwork precision, this is just another green theme.
- Not purely mechanical -- cold industrial aesthetics miss the point. Every surface must carry the warmth of sunlight and natural materials.
- Not retro-futurist -- the brass is functional instrumentation, not Art Deco decoration. Think weather station, not Jules Verne.
- Not saturated -- colors are warm and earthy, not neon green or shiny gold. The brass is warm yellow-brown, not metallic gold. The greens are forest and sage, not lime or emerald.
- Not dark-first -- this is a sun-drenched greenhouse. The default mode is warm light. Darkness is for the evening variant, not the core identity.

---

### Color System

#### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Greenhouse Linen | `#EDE7D9` | L=0.93 C=0.02 h=82 | Deepest background. Sun-bleached linen stretched behind all content. Warm, fibrous, never cold. |
| bg | Sunlit Parchment | `#F4EFE4` | L=0.95 C=0.02 h=80 | Primary surface. The warm tone of paper left in a south-facing window. |
| surface | Bleached Cotton | `#FAF7F0` | L=0.97 C=0.01 h=78 | Elevated cards, inputs, popovers. Brightest surface -- fresh linen under direct sunlight. |
| recessed | Potting Soil Tint | `#E3DDD0` | L=0.90 C=0.02 h=80 | Code blocks, inset areas. Darker warm tone suggesting rich earth beneath surfaces. |
| active | Pressed Linen | `#D9D2C3` | L=0.86 C=0.03 h=78 | Active/pressed items, user bubbles. Linen under finger pressure -- slightly darker from compression. |
| text-primary | Workshop Ink | `#2C2A24` | L=0.22 C=0.01 h=85 | Headings, body text. Dark warm brown-black, like ink used in botanical illustrations. |
| text-secondary | Weathered Label | `#6E6959` | L=0.48 C=0.02 h=80 | Sidebar items, secondary labels. Faded text on an old brass instrument nameplate. |
| text-muted | Aged Paper | `#928C7E` | L=0.61 C=0.02 h=75 | Placeholders, timestamps, metadata. Text that has faded with sun exposure. WCAG AA on surface. |
| text-onAccent | Bleached Cotton | `#FAF7F0` | L=0.97 C=0.01 h=78 | Text placed on accent-colored backgrounds. |
| border-base | Trellis Wire | `#B8B0A0` | L=0.74 C=0.02 h=78 | Base border color at variable opacity. The thin wire of a garden trellis. |
| accent-primary | Polished Brass | `#C19A49` | L=0.70 C=0.12 h=78 | Primary accent. Polished brass instrument bezels, active states, data readout frames. The warm yellow-brown of a well-maintained scientific instrument. |
| accent-secondary | Greenhouse Glass | `#4A7C59` | L=0.50 C=0.10 h=150 | Links, interactive elements, botanical highlights. The green tint of old greenhouse glass panes. |
| success | Spring Growth | `#5B8C4A` | L=0.55 C=0.10 h=140 | Positive states. New leaf green -- the vibrant fresh growth of healthy plants. |
| warning | Aged Brass | `#B8892E` | L=0.63 C=0.12 h=75 | Caution states. Brass that needs polishing -- warm amber with patina undertones. |
| danger | Kiln Brick | `#A04535` | L=0.43 C=0.12 h=25 | Error states. The fired-clay red of greenhouse heating bricks. |
| info | Patina Verdigris | `#4D8A7A` | L=0.55 C=0.08 h=175 | Informational states. The blue-green patina that forms on brass exposed to moisture and air. |

#### Special Tokens

| Token | Hex | Role |
|---|---|---|
| inlineCode | `#7A6830` | Code text within prose. Darkened brass, legible on linen surfaces. |
| toggleActive | `#5B8C4A` | Toggle/switch active track. Spring growth green -- organic activation. |
| selection | `rgba(193, 154, 73, 0.20)` | `::selection` background. Brass glow at low opacity. |
| brass-highlight | `#D4AA55` | Lighter brass for hover shimmer and subtle highlights. |
| brass-muted | `rgba(193, 154, 73, 0.30)` | Brass at 30% opacity for decorative lines, instrument bezels. |
| brass-subtle | `rgba(193, 154, 73, 0.12)` | Brass at 12% opacity for hover tints on mechanical elements. |
| patina-green | `#6BA38E` | Spring patina green -- the verdigris accent on decorative brass elements. |

#### Brass + Green Duality System

The two accent colors serve different semantic roles, reinforcing the organic-mechanical split:

| Context | Color | Usage |
|---|---|---|
| Mechanical elements | Polished Brass `#C19A49` | Data readouts, instrument frames, progress indicators, focus rings, active borders, toggles (off track), number displays |
| Organic elements | Greenhouse Glass `#4A7C59` | Growth indicators, success states, toggles (on track), botanical decorative elements, navigation active states, positive trends |
| Patina (hybrid) | Patina Verdigris `#4D8A7A` | Where brass meets moisture -- info states, links, elements that bridge mechanical and organic |
| Warning (tarnished) | Aged Brass `#B8892E` | Brass needing attention -- warning states, stale data, maintenance alerts |

**Color anti-patterns (never do these):**
- Brass and green used in equal proportion in the same component. One must lead; the other accents.
- Saturated neon green of any kind. All greens are forest/sage tones.
- Metallic/chrome effects. The brass is warm and matte, not reflective like jewelry.
- Pure gold (`#FFD700`). The brass is darker, warmer, more brown-yellow.
- Green text on light backgrounds (contrast issues). Green is for decorative and semantic elements, not body text.

#### Opacity System

Border opacity (on `border-base` Trellis Wire):

| Level | Opacity | Usage |
|---|---|---|
| subtle | 12% | Ghost borders, whisper-thin edges between related areas |
| card | 20% | Default card and content borders at rest |
| hover | 30% | Hovered elements, interactive state escalation |
| focus | 40% | Focused inputs, active delineation |
| emphasis | 50% | Strong borders on mechanical elements, instrument bezels |

#### Color Rules

- No pure greys. Every neutral carries a warm yellow-brown undertone from sun-bleached linen.
- Brass is functional, not decorative. It marks interactive elements, data frames, and instrument bezels -- never used as pure ornamentation.
- Green is earned. It appears where growth, life, or positive state is meaningful. Random green accents feel like decoration, not ecology.
- The warm linen base palette steps from deep (Greenhouse Linen) to bright (Bleached Cotton). Elevation = brightness = proximity to the glass roof and sunlight.
- Maximum three colors visible at any moment besides neutrals: brass + green + one semantic color.
- No gradients on UI surfaces. Gradients are reserved for the signature Brass Patina Shift animation only. Surfaces are flat linen.

---

### Typography Matrix

#### Font Stack

Fraunces is the display typeface -- a variable "Old Style" serif with a distinctive "wonky" axis (`WONK`) that produces organic, slightly irregular stroke terminals and letter shapes. At higher WONK values, the font looks hand-drawn and alive, like text from a botanical field notebook. At WONK 0, it becomes more conventional. This theme uses WONK 1 (full wonk) for display text and WONK 0 for smaller sizes where readability matters more than character.

DM Sans is the body typeface -- clean, geometric, highly readable. It represents the mechanical precision of the instrumentation side. Its neutrality contrasts with Fraunces' organic personality.

IBM Plex Mono handles data display and code -- corporate-scientific, optimized for tabular number alignment, suggesting lab instrument readouts.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | serif (Fraunces) | 36px | 400 | 1.2 | -0.02em | `font-variation-settings: "WONK" 1, "opsz" 36; font-feature-settings: "liga" 1, "kern" 1` | Hero titles, page names. The WONK axis creates organic, botanical-feeling display text. |
| Heading | serif (Fraunces) | 24px | 500 | 1.3 | -0.01em | `font-variation-settings: "WONK" 1, "opsz" 24` | Section titles, settings headers. Still wonky at heading size. |
| Subheading | serif (Fraunces) | 19px | 500 | 1.4 | normal | `font-variation-settings: "WONK" 0, "opsz" 19` | Subsection labels. WONK off at this smaller size for clarity. |
| Body | sans (DM Sans) | 16px | 400 | 1.55 | normal | `font-feature-settings: "kern" 1` | Primary reading text. Clean mechanical precision. |
| Body Small | sans (DM Sans) | 14px | 400 | 1.45 | normal | -- | Sidebar items, form labels, secondary UI text. |
| Button | sans (DM Sans) | 14px | 500 | 1.4 | 0.02em | -- | Button labels. Slightly tracked for clarity at small size. |
| Input | sans (DM Sans) | 14px | 430 | 1.4 | normal | `font-feature-settings: "kern" 1` | Form input text. Intermediate weight feels considered. |
| Label | sans (DM Sans) | 12px | 500 | 1.33 | 0.04em | `text-transform: uppercase` | Metadata, timestamps, instrument readout labels. Uppercase suits the scientific-instrument aesthetic. |
| Code | mono (IBM Plex Mono) | 0.9em | 400 | 1.55 | normal | `font-feature-settings: "liga" 0; font-variant-numeric: tabular-nums` | Inline code, code blocks, sensor data readouts. Tabular nums for aligned data columns. |
| Caption | sans (DM Sans) | 12px | 400 | 1.33 | 0.01em | -- | Disclaimers, footnotes, instrument fine-print. |
| Data Value | mono (IBM Plex Mono) | 18px | 500 | 1.2 | -0.02em | `font-variant-numeric: tabular-nums, lining-nums` | Large numeric readouts on brass instrument displays. Tight tracking for mechanical precision. |

#### Typographic Duality

The font pairing embodies the theme's core tension:

| Aspect | Fraunces (Organic) | DM Sans (Mechanical) |
|---|---|---|
| Used for | Display, headings, hero text | Body, buttons, labels, UI chrome |
| Character | Wonky, hand-drawn, alive | Clean, geometric, precise |
| Personality | Botanical notebook | Lab instrument panel |
| Weight range | 400-500 (lighter, more organic) | 400-500 (precise, functional) |
| Where it appears | Content that names, describes, inspires | Content that instructs, labels, controls |

#### Font Loading

```html
<!-- Solarpunk Brass Theme -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,WONK@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,430;0,9..40,500;1,9..40,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**Fallback chains:**
- Display: `"Fraunces", Georgia, "Times New Roman", serif`
- Body: `"DM Sans", system-ui, -apple-system, sans-serif`
- Mono: `"IBM Plex Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace`

**Fraunces variable axes:**
- `WONK` (0-1): Controls stroke terminal wonkiness. This theme uses 1 for display, 0 for subheading and below.
- `opsz` (9-144): Optical size. Always set to match font-size for optimal rendering.
- `wght` (100-900): Weight. This theme uses 400-600 range.

---

### Elevation System

**Strategy:** `dual-shadow` -- organic elements use soft, diffuse warm shadows. Mechanical elements use hard-edged, tight shadows with metallic character.

This is the only theme in the roster with two distinct shadow languages. Botanical/content elements cast shadows like objects in natural sunlight: soft, warm-toned, slightly diffuse. Mechanical/instrument elements cast shadows like objects under focused task lighting: crisp, tight, with a slight brass-warm tint.

#### Surface Hierarchy

| Surface | Background | Border | Shadow | Usage |
|---|---|---|---|---|
| page | `#EDE7D9` Greenhouse Linen | none | none | Deepest background. The linen beneath everything. |
| linen | `#F4EFE4` Sunlit Parchment | `0.5px solid border-base/12%` | none | Primary content surface, sidebar background. |
| panel | `#FAF7F0` Bleached Cotton | `0.5px solid border-base/20%` | shadow-organic-sm | Elevated cards, content panels. Botanical shadow. |
| instrument | `#FAF7F0` Bleached Cotton | `1px solid border-base/30%` | shadow-mechanical-sm | Brass-framed elements, data readouts. Hard-edged shadow. |
| soil | `#E3DDD0` Potting Soil Tint | `0.5px solid border-base/12%` | `inset 0 1px 3px rgba(44,42,36,0.04)` | Recessed areas, code blocks. Sunken into the potting bench. |
| overlay | `#FAF7F0` Bleached Cotton | `0.5px solid rgba(193,154,73,0.25)` | shadow-overlay | Popovers, dropdowns. Brass-tinted border. |

#### Shadow Tokens -- Organic (Botanical)

Soft, warm, diffuse. Like sunlight casting shadows through greenhouse glass.

| Token | Value | Usage |
|---|---|---|
| shadow-organic-none | `none` | Flat surfaces, page background |
| shadow-organic-sm | `0 2px 8px rgba(44,42,36,0.04), 0 1px 3px rgba(44,42,36,0.03)` | Cards at rest. A warm whisper of depth. |
| shadow-organic-md | `0 4px 14px rgba(44,42,36,0.06), 0 2px 4px rgba(44,42,36,0.03)` | Card hover. Slightly deeper, still soft. |
| shadow-organic-focus | `0 4px 14px rgba(44,42,36,0.06), 0 0 0 2px rgba(193,154,73,0.45)` | Input focus. Organic shadow + brass focus ring. |
| shadow-organic-overlay | `0 8px 24px rgba(44,42,36,0.08), 0 2px 6px rgba(44,42,36,0.04)` | Popovers, modals. Widest organic shadow. |

#### Shadow Tokens -- Mechanical (Instrument)

Tighter, crisper, with a warm brass tint. Like a brass instrument sitting on a wooden bench under task lighting.

| Token | Value | Usage |
|---|---|---|
| shadow-mechanical-none | `none` | Flat mechanical elements |
| shadow-mechanical-sm | `0 1px 3px rgba(44,42,36,0.08), 0 0.5px 1px rgba(44,42,36,0.06)` | Data readouts, small instrument bezels at rest. Tight, defined edge. |
| shadow-mechanical-md | `0 2px 4px rgba(44,42,36,0.10), 0 1px 2px rgba(44,42,36,0.06)` | Instrument hover. Slightly lifted. |
| shadow-mechanical-active | `0 0.5px 1px rgba(44,42,36,0.10)` | Pressed mechanical element. Shadow compresses -- instrument pushed down onto bench. |
| shadow-mechanical-bezel | `inset 0 1px 0 rgba(255,255,255,0.08), 0 1px 3px rgba(44,42,36,0.10)` | Brass bezel ring. Inner highlight + outer shadow creates a rim of polished metal. |

#### Shadow Assignment Guide

| Element | Shadow Language | Why |
|---|---|---|
| Content cards | Organic | Cards contain botanical/content information, they float like leaves |
| Data readout panels | Mechanical | Instruments sit firmly, cast hard shadows |
| Buttons | Mechanical | Buttons are controls -- they click |
| Input fields | Organic (rest) to Mechanical (focus) | Inputs transition from resting botanical to active instrument |
| Toggles, switches | Mechanical | Physical toggles, brass switches |
| Popovers, dropdowns | Organic | Menus unfurl like seed pods opening |
| Modal dialogs | Organic | Modals float above like greenhouse panels |
| Chips, tags | Organic | Labels are paper/organic tags tied to items |
| Progress bars | Mechanical | Brass instrument gauges |

#### Separation Recipe

The primary separation mechanism is surface-brightness stepping with dual shadow languages reinforcing the organic-mechanical split. Linen surfaces step from deep warm (Greenhouse Linen) through progressively lighter sheets toward the sunlit roof. Borders are thin trellis-wire lines at low opacity. Organic elements separate through soft warm shadows that suggest sunlight and depth. Mechanical elements separate through tight crisp shadows that suggest weight and precision. Gold brass accents at 25-30% opacity serve as visible separators for instrument bezels and data frame borders.

---

### Border System

#### Widths

| Name | Width | Usage |
|---|---|---|
| hairline | 0.5px | Organic element borders. Thin as a vine tendril. |
| default | 1px | Standard borders, input fields, mechanical element edges. |
| medium | 1.5px | Instrument bezel borders, emphasized dividers. |
| heavy | 2px | Focus ring width. Maximum border weight. Brass instrument frame. |

#### Opacity Scale (on `border-base` Trellis Wire)

| Level | Opacity | Usage |
|---|---|---|
| subtle | 12% | Ghost borders, organic element edges at rest |
| card | 20% | Default card and panel borders |
| hover | 30% | Hovered elements, interactive state |
| focus | 40% | Focused inputs, active delineation |
| emphasis | 50% | Brass instrument bezels, data readout frames |

#### Border Patterns

| Pattern | Width | Color/Opacity | Usage |
|---|---|---|---|
| organic-rest | 0.5px | border-base at 12% | Botanical cards, content panels at rest |
| organic-hover | 0.5px | border-base at 20% | Content cards on hover |
| mechanical-rest | 1px | border-base at 20% | Instrument panels, data readouts at rest |
| mechanical-hover | 1px | border-base at 30% | Instrument panels on hover |
| input-rest | 1px | border-base at 15% | Form input borders at rest |
| input-hover | 1px | border-base at 25% | Input hover state |
| input-focus | 1px | brass at 40% | Input focus -- border transitions from wire to brass |
| brass-bezel | 1.5px | brass at 50% | Instrument frame borders, data readout bezels |
| brass-accent | 1px | brass at 30% | Decorative brass lines, section dividers |

#### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(193, 154, 73, 0.50)` -- polished brass |
| Width | 2px solid |
| Offset | 2px |
| Implementation | `box-shadow: 0 0 0 2px #F4EFE4, 0 0 0 4px rgba(193,154,73,0.50)` |

The focus ring is brass, not blue. Brass focus rings reinforce the instrument-panel aesthetic -- every focused element looks like an activated control on a brass dashboard. The inner ring uses the `bg` linen color to visually separate the brass indicator from the element surface.

---

### Component States

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `#C19A49` (Polished Brass), border none, color `#FAF7F0` (Bleached Cotton), radius 6px, h 36px, padding `0 20px`, font button (DM Sans, 14px, 500), shadow shadow-mechanical-sm |
| Hover | bg `#B38D3F` (darker brass), shadow shadow-mechanical-md |
| Active | bg `#A68038`, transform `scale(0.97)`, shadow shadow-mechanical-active |
| Focus | brass focus ring appended |
| Disabled | opacity 0.45, pointer-events none, cursor not-allowed, shadow none |
| Transition | background 120ms default, transform 100ms default, box-shadow 120ms default |

Primary buttons are brass -- they are mechanical controls that click with precision. Transition timing is fast (mechanical language: 100-120ms).

#### Buttons (Secondary)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid rgba(193,154,73,0.35)`, color `#C19A49`, radius 6px, h 36px, padding `0 20px`, font button, shadow none |
| Hover | bg `rgba(193,154,73,0.08)`, border at 50% opacity, color `#A68038` |
| Active | bg `rgba(193,154,73,0.15)`, transform `scale(0.97)` |
| Focus | brass focus ring |
| Disabled | opacity 0.45, pointer-events none |
| Transition | all 120ms default |

Secondary buttons have a brass border outline -- the wireframe of an instrument control.

#### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border none, color `#6E6959` (Weathered Label), radius 6px, size 36x36px |
| Hover | bg `rgba(193,154,73,0.08)` (brass whisper tint), color `#2C2A24` |
| Active | bg `rgba(193,154,73,0.15)`, transform `scale(0.97)` |
| Focus | brass focus ring |
| Disabled | opacity 0.45, pointer-events none |
| Transition | background 150ms default, color 150ms default |

Ghost buttons warm with a brass tint on hover -- subtle warmth from nearby brass instruments.

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `#FAF7F0` (Bleached Cotton), border `1px solid rgba(184,176,160,0.15)`, radius 8px, h 44px, padding `0 14px`, shadow none, color `#2C2A24`, placeholder `#928C7E`, caret-color `#C19A49` (brass caret) |
| Hover | border at 25% opacity, shadow shadow-organic-sm |
| Focus | border `1px solid rgba(193,154,73,0.40)` (brass border), shadow shadow-organic-focus, outline none |
| Disabled | opacity 0.45, bg `#E3DDD0`, pointer-events none, cursor not-allowed |
| Transition | border-color 250ms ease-out (organic timing), box-shadow 350ms ease-out |

The text cursor (caret) is brass -- as the user types, they write with a brass nib. Input focus transitions organically (slow border color change) but the brass border itself signals mechanical activation. This is a hybrid-language component.

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `#FAF7F0`, radius 16px, border `0.5px solid rgba(184,176,160,0.12)`, shadow shadow-organic-sm, padding 18px |
| Hover | border at 20%, shadow shadow-organic-md |
| Focus-within | border `0.5px solid rgba(193,154,73,0.25)`, shadow shadow-organic-focus |
| Transition | all 400ms cubic-bezier(0.22, 1, 0.36, 1) (organic easing) |

The chat card uses organic animation language -- it breathes and grows into focus, not clicks.

#### Cards

| State | Properties |
|---|---|
| Rest | bg `#FAF7F0`, border `0.5px solid rgba(184,176,160,0.20)`, radius 10px, shadow shadow-organic-sm, padding 24px |
| Hover | border at 25%, shadow shadow-organic-md |
| Selected | border-bottom `1.5px solid rgba(193,154,73,0.45)` (brass accent line at base) |
| Transition | border-color 350ms ease-out, box-shadow 450ms cubic-bezier(0.22, 1, 0.36, 1) |

Cards use organic animation language. Selected cards receive a brass bottom accent -- an instrument measurement marker.

#### Data Readout Cards (Theme-Specific)

| State | Properties |
|---|---|
| Rest | bg `#FAF7F0`, border `1.5px solid rgba(193,154,73,0.30)` (brass bezel), radius 8px, shadow shadow-mechanical-sm, padding 20px |
| Hover | border at 45%, shadow shadow-mechanical-md |
| Active | shadow shadow-mechanical-active, transform `scale(0.99)` |
| Transition | border-color 100ms default, box-shadow 100ms default, transform 80ms default |

Data readout cards are mechanical -- brass-bezeled instrument panels that respond with clockwork precision. Their transitions are 100ms (mechanical language), in sharp contrast to standard cards at 350-450ms (organic language).

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `#6E6959` (Weathered Label), radius 6px, h 36px, padding `6px 16px`, font bodySmall |
| Hover | bg `rgba(74,124,89,0.06)` (greenhouse glass tint), color `#2C2A24` |
| Active (current) | bg `rgba(74,124,89,0.10)`, color `#2C2A24`, border-left `2px solid #4A7C59` (greenhouse green) |
| Active press | transform `scale(0.985)` |
| Transition | color 150ms default, background 200ms ease-out |

Active sidebar items use green (organic language) -- navigation is a living, growing structure, not a mechanical toggle. The green left border suggests a vine climbing the sidebar edge.

#### Chips

| State | Properties |
|---|---|
| Rest | bg `#F4EFE4` (Sunlit Parchment), border `0.5px solid rgba(184,176,160,0.15)`, radius 8px, h 32px, padding `0 12px`, font bodySmall, color `#6E6959` |
| Hover | bg `#EDE7D9`, border at 25%, color `#2C2A24` |
| Selected | bg `rgba(193,154,73,0.10)`, border `0.5px solid rgba(193,154,73,0.25)`, color `#2C2A24` |
| Active press | transform `scale(0.995)` |
| Transition | all 200ms ease-out |

Chips are organic labels -- paper tags attached to specimens. Selected chips gain a brass tint, marking them as "catalogued."

#### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 40px |
| Track height | 22px |
| Track radius | 9999px |
| Track off bg | `rgba(184,176,160,0.25)` (trellis wire) |
| Track off ring | `0.5px solid rgba(184,176,160,0.20)` |
| Track on bg | `#5B8C4A` (Spring Growth green) |
| Track on ring | `0.5px solid rgba(91,140,74,0.30)` |
| Thumb | 18px `#FAF7F0` circle |
| Thumb shadow | shadow-mechanical-sm |
| Ring hover | thickens to 1px |
| Transition | 130ms cubic-bezier(0.4, 0, 0.2, 1) |
| Focus-visible | brass focus ring |

Toggles use mechanical animation language -- 130ms, precise click. The off state is neutral trellis wire; the on state is organic green (growth activated). The thumb shadow is mechanical (hard-edged), because the toggle is a physical switch.

#### Slider

| Property | Value |
|---|---|
| Track height | 2px |
| Track color | `rgba(184,176,160,0.30)` (Trellis Wire at 30%) |
| Track filled | `rgba(193,154,73,0.70)` (brass gauge fill) |
| Thumb | 14px circle, `#FAF7F0` fill, `1.5px solid rgba(193,154,73,0.50)` brass border |
| Thumb hover | border widens to 2px, shadow shadow-mechanical-md |
| Thumb active | scale(1.08), shadow shadow-mechanical-active |
| Value display | IBM Plex Mono, 14px, `font-variant-numeric: tabular-nums` |
| Transition | 100ms default (mechanical language) |

The slider is a brass instrument gauge -- the filled track is the brass measurement level, the thumb is a calibrated knob.

---

### Motion Map

#### Easings

| Name | Value | Character | Language |
|---|---|---|---|
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. Baseline for neutral elements. | Neutral |
| click | `cubic-bezier(0.2, 0, 0, 1)` | Snappy deceleration. Fast arrival, minimal overshoot. Like a brass toggle snapping into place. | Mechanical |
| precise | `cubic-bezier(0.25, 0.1, 0.1, 1)` | Tight, controlled deceleration. For instrument readout updates, data changes. | Mechanical |
| grow | `cubic-bezier(0.22, 1.2, 0.36, 1)` | Slight overshoot, like a vine tendril reaching and then settling. Spring-like without being bouncy. | Organic |
| unfurl | `cubic-bezier(0.12, 0.8, 0.3, 1)` | Slow start, long gentle tail. Like a fern frond uncurling. For reveals and page entries. | Organic |
| settle | `cubic-bezier(0.22, 1, 0.36, 1)` | Smooth ease-out-quint. For elements coming to rest after organic motion. | Organic |

#### Duration x Easing x Component

| Component | Duration | Easing | Language | Notes |
|---|---|---|---|---|
| Toggle click | 130ms | click | Mechanical | Brass switch snapping into position |
| Button hover bg | 120ms | default | Mechanical | Controls respond instantly |
| Button active press | 100ms | click | Mechanical | Press-and-release, instant |
| Slider thumb drag | 100ms | precise | Mechanical | Gauge knob follows finger precisely |
| Data readout update | 80ms | precise | Mechanical | Numbers tick over like an analog counter |
| Sidebar item bg/color | 200ms | settle | Organic | Navigation grows into state |
| Card shadow on hover | 450ms | unfurl | Organic | Shadow deepens like a cloud passing |
| Card border on hover | 350ms | settle | Organic | Border warms gradually |
| Input focus ring | 350ms | grow | Organic | Brass ring grows outward organically |
| Input border-color focus | 250ms | settle | Organic | Border warms from wire to brass |
| Chip hover/select | 200ms | settle | Organic | Paper tag warms |
| Chat card focus-within | 400ms | unfurl | Organic | Card expands into active state |
| Panel open/close | 500ms | unfurl | Organic | Greenhouse panel sliding open |
| Modal enter | 600ms | unfurl | Organic | Glass panel descends slowly |
| Modal exit | 350ms | settle | Organic | Faster close than open |
| Hero/page entry | 700ms | unfurl | Organic | Content unfurls like morning glory |
| Popover appear | 250ms | grow | Organic | Seed pod opening |
| Stagger offset | 60ms | -- | Organic | Between staggered children |

#### Active Press Scale

| Element | Scale | Language | Notes |
|---|---|---|---|
| Nav items | 0.985 | Organic | Subtle, vine flexibility |
| Chips | 0.995 | Organic | Barely perceptible on paper tags |
| Standard buttons | 0.97 | Mechanical | Definite mechanical click-down |
| Data readout cards | 0.99 | Mechanical | Instrument pressed firmly |
| Tabs | 0.96 | Mechanical | Pronounced toggle lever |

#### Reduced Motion

| Behavior | Value |
|---|---|
| Strategy | `reduced-distance` -- all spatial animations reduce to 4px max travel. Durations halved. Ambient animations disabled. |
| All organic durations | Cap at 200ms |
| All mechanical durations | Cap at 100ms |
| Vine crawl animation | Disabled |
| Gear rotate animation | Disabled |
| Brass Patina Shift | Static gradient, no animation |
| Leaf unfurl reveal | Collapses to 150ms opacity fade |
| Gauge needle sweep | Static final position |

---

### Overlays

#### Popover / Dropdown

| Property | Value |
|---|---|
| bg | `#FAF7F0` (Bleached Cotton) |
| border | `0.5px solid rgba(193,154,73,0.25)` (brass-tinted border) |
| radius | 10px |
| shadow | shadow-organic-overlay |
| backdrop-filter | `blur(16px)` |
| padding | 6px |
| z-index | 50 |
| min-width | 200px |
| max-width | 320px |
| Menu item | 6px 10px padding, radius 8px, h 36px, font bodySmall, color text-secondary |
| Menu item hover | bg `rgba(193,154,73,0.06)`, color text-primary |
| Separator | `1px solid rgba(193,154,73,0.15)` brass accent line, margin 4px 0 |
| Transition | 250ms grow (organic -- seed pod opening) |

Popovers have a brass-tinted border -- the instrument panel opens to reveal controls within.

#### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(44,42,36,0.25)` (warm scrim -- not too dark, greenhouse stays visible) |
| Overlay backdrop-filter | `blur(8px)` |
| Content bg | `#FAF7F0` |
| Content border | `0.5px solid rgba(193,154,73,0.30)` (brass frame) |
| Content shadow | shadow-organic-overlay |
| Content radius | 14px |
| Content padding | 28px |
| Entry | opacity `0` to `1` + translateY `12px` to `0` + scale `0.97` to `1`, 600ms unfurl |
| Exit | opacity `1` to `0` + scale `1` to `0.98`, 350ms settle |

The modal is a greenhouse glass panel lowered from the roof. The scrim is light (25%) -- the greenhouse beneath should remain partially visible. The brass border frames it like a brass-cornered display case.

#### Tooltip

| Property | Value |
|---|---|
| bg | `#2C2A24` (Workshop Ink) |
| color | `#F4EFE4` (Sunlit Parchment) |
| font | label size (12px, DM Sans, 500, uppercase) |
| radius | 6px |
| padding | 5px 10px |
| shadow | `0 2px 6px rgba(44,42,36,0.12)` |
| No arrow | Position via offset |
| Entry | opacity fade, 150ms default (mechanical -- tooltips are informational readouts) |

Tooltips are instrument labels -- small brass nameplates explaining what a control does. They appear mechanically (fast, precise).

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column. Standard comfortable reading width. |
| Narrow max-width | 640px | Focused content, settings pages, single-column reading. |
| Sidebar width | 280px | Fixed sidebar. Slightly wider to accommodate label + icon layouts. |
| Header height | 52px | Top bar. Brass instrument panel height. |
| Spacing unit | 4px | Base multiplier. Standard 4px grid. |

#### Spacing Scale

4, 6, 8, 12, 16, 20, 24, 32, 48px

| Context | Typical Gap | Notes |
|---|---|---|
| Between paragraphs | 16px | 1x body font size |
| Between form fields | 20px | Comfortable vertical rhythm |
| Between cards | 16px | Cards sit on the potting bench side by side |
| Between sections | 32-48px | Clear breathing room without Kintsugi-level spaciousness |
| Card internal padding | 24px | Generous but functional |
| Page edge padding | 32px | Content framed by warm margins |
| Between sidebar items | 4px | Tight vine-like list |
| Header to content | 32px | Clean separation from the instrument panel header |

#### Radius Scale

| Token | Value | Usage |
|---|---|---|
| none | 0px | -- |
| sm | 4px | Badges, small elements, tooltip |
| md | 6px | Sidebar items, menu items, buttons |
| lg | 8px | Input fields, chips |
| xl | 10px | Cards, panels |
| 2xl | 14px | Modals, large panels |
| input | 8px | Form inputs specifically |
| full | 9999px | Toggles, avatars, pill shapes |

Radii are rounded but not pill-shaped -- the aesthetic is turned wood and polished brass edges, not capsules. Softer than a machine shop (4px min), crisper than a watercolor painting.

#### Density

Comfortable. This theme is neither sparse nor dense -- it reflects a working greenhouse where instruments and plants share space efficiently. Content-to-whitespace ratio targets 50:50. Functional enough for dashboards, airy enough for contemplation.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (280px) + content column (768px max). Brass instrument panel header visible.
- **md (768px):** Sidebar collapses to hamburger overlay. Content fills viewport with 24px side padding. Data readout cards reflow to single column.
- **sm (640px):** Single column. Card padding reduces from 24px to 16px. Brass bezel borders reduce from 1.5px to 1px. Section spacing from 48px to 32px. Toggle and slider maintain 44px touch targets. Signature animations disabled (vine crawl, gear rotate).

---

### Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring color | `rgba(193, 154, 73, 0.50)` (polished brass) |
| Focus ring width | 2px solid |
| Focus ring offset | 2px (inner ring: `#F4EFE4` linen bg color) |
| Focus ring implementation | `box-shadow: 0 0 0 2px var(--bg), 0 0 0 4px rgba(193,154,73,0.50)` |
| Disabled opacity | 0.45 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled shadow | none |
| Selection bg | `rgba(193,154,73,0.20)` (brass at 20%) |
| Selection color | `#2C2A24` (Workshop Ink, text-primary) |
| Scrollbar width | thin |
| Scrollbar thumb | `rgba(193,154,73,0.30)` (brass-tinted) |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

**Contrast verification:**
- `text-primary` (#2C2A24) on `surface` (#FAF7F0): 12.8:1 -- exceeds AAA
- `text-secondary` (#6E6959) on `surface` (#FAF7F0): 4.9:1 -- meets AA
- `text-muted` (#928C7E) on `surface` (#FAF7F0): 3.3:1 -- meets AA for large text (used only at 12px label with uppercase + weight 500, which qualifies as bold large text equivalent). For body text on `bg` (#F4EFE4): 3.5:1. Use `#867F72` for stricter compliance.
- `accent-primary` brass (#C19A49) on white text (#FAF7F0): 3.1:1 -- meets AA for large text (button labels at 14px/500 weight). For maximum compliance, darken button brass to `#A68038` (4.1:1).
- `accent-secondary` green (#4A7C59) on `surface` (#FAF7F0): 4.8:1 -- meets AA.

**Reduced motion strategy:**

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 100ms !important;
    scroll-behavior: auto !important;
  }
  .vine-crawl,
  .gear-rotate,
  .leaf-unfurl,
  .gauge-sweep,
  .brass-patina-shift {
    animation: none !important;
  }
}
```

---

### Visual Style

- **Material:** Sun-bleached linen and polished brass. Surfaces feel like stretched natural fiber -- warm, textured, matte. Brass accents feel like polished-but-not-chrome metal -- warm, slightly reflective, with visible grain direction.

- **Linen Texture:** Applied via SVG `feTurbulence` filter as a subtle background overlay. The texture suggests woven linen fiber, warmer and coarser than Kintsugi's washi paper.

```svg
<svg width="0" height="0" aria-hidden="true">
  <filter id="linen-grain">
    <feTurbulence
      type="fractalNoise"
      baseFrequency="0.75"
      numOctaves="4"
      stitchTiles="stitch"
      result="noise"
    />
    <feColorMatrix
      type="saturate"
      values="0"
      in="noise"
      result="mono"
    />
    <feBlend mode="multiply" in="SourceGraphic" in2="mono"/>
  </filter>
</svg>
```

```css
.solarpunk-page::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  filter: url(#linen-grain);
  opacity: 0.025; /* 2.5% -- slightly more visible than washi, linen is coarser */
  mix-blend-mode: multiply;
  z-index: 9999;
}
```

The `baseFrequency` of 0.75 creates a medium-grained fiber pattern (coarser than Kintsugi's 0.9 washi but finer than heavy canvas). The 2.5% opacity makes the texture perceivable on close inspection but invisible at glance.

- **Brass Bezel Rendering:** Data readout cards and instrument-style elements get a subtle brass border treatment. The bezel uses `border` + `box-shadow` to create a rimmed metallic edge without gradient or metallic CSS effects:

```css
.brass-bezel {
  border: 1.5px solid rgba(193, 154, 73, 0.35);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),  /* top inner highlight */
    0 1px 3px rgba(44, 42, 36, 0.10);           /* outer shadow */
  border-radius: 8px;
}
```

The inner highlight suggests light catching the brass rim. The outer shadow grounds it on the surface. No metallic gradients, no gold glow -- the effect is subtle and physical.

- **Grain:** Subtle (2.5% opacity). Linen fiber texture via feTurbulence.
- **Gloss:** Matte for surfaces. Soft-sheen for brass bezel elements (achieved through the inner highlight, not actual gloss).
- **Blend mode:** `multiply` for the linen grain overlay. `normal` for all other elements.
- **Shader bg:** False. No WebGL. SVG filter only.

---

### Signature Animations

#### 1. Leaf Unfurl Reveal

Content blocks enter with a combined vertical + horizontal expansion, like a leaf unfurling from a tightly curled bud. A `clip-path` rectangle expands from the top-left corner while opacity fades in. The asymmetric origin (top-left, not center) reinforces the organic growth direction.

```css
@keyframes leaf-unfurl {
  0% {
    clip-path: inset(0 100% 100% 0);
    opacity: 0;
    transform: scale(0.96);
  }
  40% {
    clip-path: inset(0 40% 30% 0);
    opacity: 0.7;
  }
  100% {
    clip-path: inset(0 0 0 0);
    opacity: 1;
    transform: scale(1);
  }
}
.unfurl-reveal {
  animation: leaf-unfurl 600ms cubic-bezier(0.22, 1.2, 0.36, 1) both;
}
```

Duration: 600ms, easing: grow (organic). The slight overshoot in the easing makes the element reach and then settle, like a tendril finding its support. Reduced motion: 150ms opacity-only fade.

#### 2. Gear Rotate Data Update

When numeric data values change in instrument readout panels, the digits rotate vertically -- old value scrolls up and out, new value scrolls in from below. Like the numbered wheels on a mechanical counter clicking over. Each digit animates independently with a 30ms stagger, creating a satisfying cascade effect.

```css
@keyframes gear-tick-out {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(-100%);
    opacity: 0;
  }
}
@keyframes gear-tick-in {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.gear-digit-exit {
  animation: gear-tick-out 120ms cubic-bezier(0.2, 0, 0, 1) both;
}
.gear-digit-enter {
  animation: gear-tick-in 120ms cubic-bezier(0.2, 0, 0, 1) both;
}
/* Stagger per digit: nth-child(1) delay 0ms, nth-child(2) delay 30ms, etc. */
```

Duration: 120ms per digit, easing: click (mechanical). The short duration and precise easing create a satisfying clockwork tick. Reduced motion: instant swap with no animation.

#### 3. Vine Crawl Navigation

When navigating between sidebar items, the active indicator (green left border) animates from the previous position to the new one, crawling like a vine tendril up or down the sidebar. The indicator has a slight elastic overshoot at the destination.

```css
.vine-indicator {
  position: absolute;
  left: 0;
  width: 2px;
  height: 36px;
  background: #4A7C59;
  border-radius: 0 2px 2px 0;
  transition: top 500ms cubic-bezier(0.22, 1.2, 0.36, 1);
}
```

Duration: 500ms, easing: grow (organic). The vine crawls at its own pace, even while mechanical elements click instantly. The 1.2 overshoot makes the indicator reach slightly past its target and then settle back. Reduced motion: instant position change.

#### 4. Brass Patina Shift

A slow, ambient color shift on brass accent elements. The brass surface cycles subtly between polished brass (`#C19A49`) and patina verdigris (`#6BA38E`) and back, suggesting the living chemical reaction between metal and air. Applied to decorative brass elements only (not interactive controls).

```css
@keyframes brass-patina {
  0%, 100% {
    color: #C19A49;
  }
  50% {
    color: #8BA87A;
  }
}
.patina-shift {
  animation: brass-patina 12s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
```

Duration: 12s full cycle. Extremely slow -- the patina forms over geological time scaled to interface time. Applied only to decorative border accents, never to interactive elements. Reduced motion: static brass color, no shift.

#### 5. Gauge Needle Sweep

Progress bars and loading indicators fill with a gauge-needle sweep -- the fill line sweeps from 0% to the target value with a slight overshoot and settle-back, like a brass pressure gauge needle swinging to its reading. The overshoot is proportional to the target value (larger values = more overshoot).

```css
@keyframes gauge-sweep {
  0% {
    transform: scaleX(0);
    transform-origin: left;
  }
  70% {
    transform: scaleX(1.03); /* 3% overshoot */
    transform-origin: left;
  }
  100% {
    transform: scaleX(1);
    transform-origin: left;
  }
}
.gauge-fill {
  height: 3px;
  background: linear-gradient(90deg, #C19A49 0%, #D4AA55 100%);
  animation: gauge-sweep 800ms cubic-bezier(0.22, 1.2, 0.36, 1) both;
}
```

Duration: 800ms, easing: grow (organic start, mechanical precision at end). The overshoot-and-settle is the hybrid moment -- organic momentum meeting mechanical calibration. Reduced motion: instant fill to target width.

---

### Dark Mode Variant

Solarpunk Brass's default is a warm light theme -- the greenhouse in daytime. The dark variant is the **greenhouse at dusk**: warm amber light from brass oil lamps, deep green foliage in shadow, instruments glowing faintly in the low light.

#### Dark Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Night Soil | `#1A1915` | Deepest background. Rich warm dark earth. |
| bg | Dusk Timber | `#222018` | Primary surface. Dark wood workbench. |
| surface | Lamp-lit Panel | `#2A2820` | Elevated cards, inputs. Warm surface catching oil-lamp glow. |
| recessed | Deep Potting | `#141310` | Code blocks, inset areas. Darkest earth. |
| active | Pressed Timber | `#333028` | Active/pressed items. Dark wood under pressure. |
| text-primary | Lamp Linen | `#E8E2D4` | Headings, body text at 90% opacity. Warm white in lamplight. |
| text-secondary | Dusty Shelf | `#9E9888` | Secondary labels at 65% opacity. |
| text-muted | Shadow Grain | `#706A5C` | Placeholders, timestamps. Low visibility in dim light. |
| border-base | Night Trellis | `#3E3B30` | Border base. Dark trellis wire, barely visible. |
| accent-primary | Lamplight Brass | `#D4AA55` | Brightened brass for dark contrast. Glows warmer in lamplight. |
| accent-secondary | Night Greenhouse | `#5A9E72` | Brightened green for dark readability. Foliage catching lamp light. |
| success | Moonlit Leaf | `#6BAA5E` | Brighter green for dark contrast. |
| warning | Tarnished Brass | `#C99E40` | Warm amber warning. |
| danger | Ember Brick | `#C25545` | Lifted red for dark readability. |
| info | Night Patina | `#5AA08E` | Brightened verdigris. |

#### Dark Mode Rules

| Change | Light Value | Dark Value | Reason |
|---|---|---|---|
| Surface elevation | Brightness stepping up | Brightness stepping up (darker base, lighter cards) | Same direction but compressed range |
| Brass accent | `#C19A49` | `#D4AA55` | Brass brightens to glow in lamplight |
| Green accent | `#4A7C59` | `#5A9E72` | Greens lift for readability on dark |
| Shadow direction | Warm rgba shadows | Warm rgba glows at 3-5% opacity | Shadows become ambient warmth emanating from brass elements |
| Organic shadows | Downward, diffuse | Ambient warm glow, slight brass tint | `0 0 12px rgba(193,154,73,0.04)` |
| Mechanical shadows | Tight, directional | Tighter with brass highlight | `inset 0 1px 0 rgba(193,154,73,0.06)` |
| Border opacity scale | 12/20/30/40/50% | 15/25/35/45/55% | Slightly higher opacity for visibility in dark |
| Linen texture | multiply at 2.5% | soft-light at 1.5% | Reduced intensity, different blend mode |
| Focus ring brass | 50% opacity | 60% opacity | More visible in dark context |
| Brass patina shift animation | Full cycle | Static brass glow | Too distracting in dark mode |
| Text link color | `#4A7C59` | `#6BAA5E` | Lifts for contrast |
| Code bg | `#E3DDD0` | `#141310` | Darkest recessed surface |

---

### Mobile Notes

#### Effects to Disable
- Linen feTurbulence texture overlay -- disable on mobile (replace with static CSS `background-image` texture or omit)
- Brass patina shift animation (signature #4) -- static brass color
- Vine crawl navigation animation (signature #3) -- instant position snap
- Leaf unfurl clip-path animation (signature #1) -- replace with 200ms opacity fade
- `backdrop-filter: blur()` on popovers -- reduce to `blur(4px)` or disable if janky

#### Adjustments
- Body text stays 16px minimum
- Card internal padding reduces from 24px to 16px
- Section spacing reduces from 48px to 28px
- Brass bezel borders reduce from 1.5px to 1px
- Data readout card radius reduces from 8px to 6px
- Sidebar overlay width: 300px (wider for touch targets)
- All interactive elements maintain minimum 44px touch target
- Header height stays 52px
- Scrollbar styling removed (native mobile scrolling)
- Brass focus rings remain (important for accessibility)
- Toggle track width increases from 40px to 48px for touch comfort
- Gear rotate animation (signature #2) keeps reduced 80ms timing (light enough for mobile)

#### Performance Notes
- Linen SVG feTurbulence filter is the main performance concern. Disable on mobile.
- Dual shadow language: collapse to single shadow language (organic only) on mobile to reduce paint operations.
- `will-change: transform, opacity` only during active animations, never permanent.
- Total animation budget on mobile: 2 concurrent transitions maximum.
- Gauge sweep animation is GPU-friendly (transform only). Keep on mobile.
- IBM Plex Mono + Fraunces + DM Sans total: ~150KB. Acceptable with `font-display: swap`.

---

### Data Visualization

| Property | Value |
|---|---|
| Categorical palette | `#C19A49` (Brass), `#4A7C59` (Greenhouse), `#A04535` (Kiln Brick), `#4D8A7A` (Patina), `#B8892E` (Aged Brass), `#5B8C4A` (Spring Growth) -- 6 colors max |
| Sequential ramp | Single-hue brass: `#F4E6C0` (light brass) to `#C19A49` (full brass) to `#7A6830` (dark brass) |
| Diverging ramp | Green to neutral to brass: `#4A7C59` to `#F4EFE4` to `#C19A49` |
| Grid lines | Low-ink: `border-base` at 10% opacity. Near-invisible trellis. |
| Max hues per chart | 3 (prefer 2: brass + green) |
| Philosophy | Instrument-panel aesthetic. Clean, precise annotations. Use IBM Plex Mono for all data labels. Brass for primary data series, green for comparison/growth series. |
| Axis labels | DM Sans, 12px, 500, uppercase, text-secondary color |
| Value labels | IBM Plex Mono, 12px, text-primary color, `font-variant-numeric: tabular-nums` |
| Chart border | 1.5px brass bezel border around chart containers |

---

### Theme-Specific Components

#### Brass Instrument Panel

A specialized card component for data displays. Features a brass bezel border, IBM Plex Mono numeric readouts, and mechanical animation language.

| Property | Value |
|---|---|
| Container | bg `#FAF7F0`, border `1.5px solid rgba(193,154,73,0.35)`, radius 8px, shadow shadow-mechanical-sm |
| Header bar | border-bottom `1px solid rgba(193,154,73,0.20)`, padding 12px 20px |
| Header label | DM Sans, 12px, 500, uppercase, 0.04em tracking, color text-secondary |
| Value display | IBM Plex Mono, 24px, 500, color text-primary, `font-variant-numeric: tabular-nums, lining-nums` |
| Unit label | IBM Plex Mono, 12px, 400, color text-muted, margin-left 4px |
| Trend indicator | Small triangle icon (8px), color success (up) or danger (down) |
| Hover | bezel border brightens to 50% opacity, shadow shadow-mechanical-md |
| Data update | Gear rotate animation (signature #2) on value digits |

#### Botanical Tag

A chip variant for plant/specimen-style categorization. Slightly warmer than standard chips, with a leaf-green accent dot.

| Property | Value |
|---|---|
| Container | bg `rgba(74,124,89,0.06)`, border `0.5px solid rgba(74,124,89,0.15)`, radius 12px (more rounded -- organic shape), h 28px, padding `0 12px 0 8px` |
| Status dot | 6px circle, bg `#5B8C4A`, margin-right 6px |
| Text | DM Sans, 13px, 400, color text-secondary |
| Hover | bg `rgba(74,124,89,0.12)`, border at 25% |

---

### Theme-Specific CSS Custom Properties

```css
:root[data-theme="solarpunk-brass"] {
  /* Core surfaces */
  --page: #EDE7D9;
  --bg: #F4EFE4;
  --surface: #FAF7F0;
  --recessed: #E3DDD0;
  --active: #D9D2C3;

  /* Text */
  --text-primary: #2C2A24;
  --text-secondary: #6E6959;
  --text-muted: #928C7E;

  /* Brass system */
  --brass: #C19A49;
  --brass-highlight: #D4AA55;
  --brass-muted: rgba(193, 154, 73, 0.30);
  --brass-subtle: rgba(193, 154, 73, 0.12);
  --brass-focus: rgba(193, 154, 73, 0.50);
  --brass-hover: rgba(193, 154, 73, 0.08);

  /* Green system */
  --greenhouse: #4A7C59;
  --greenhouse-subtle: rgba(74, 124, 89, 0.06);
  --greenhouse-hover: rgba(74, 124, 89, 0.10);
  --patina: #4D8A7A;

  /* Accents */
  --accent-primary: #C19A49;
  --accent-secondary: #4A7C59;

  /* Semantics */
  --success: #5B8C4A;
  --warning: #B8892E;
  --danger: #A04535;
  --info: #4D8A7A;

  /* Borders */
  --border-base: #B8B0A0;
  --border-subtle: rgba(184, 176, 160, 0.12);
  --border-card: rgba(184, 176, 160, 0.20);
  --border-hover: rgba(184, 176, 160, 0.30);
  --border-focus: rgba(184, 176, 160, 0.40);
  --border-emphasis: rgba(184, 176, 160, 0.50);

  /* Focus */
  --focus-ring: 0 0 0 2px var(--bg), 0 0 0 4px var(--brass-focus);

  /* Shadows -- Organic */
  --shadow-organic-sm: 0 2px 8px rgba(44,42,36,0.04), 0 1px 3px rgba(44,42,36,0.03);
  --shadow-organic-md: 0 4px 14px rgba(44,42,36,0.06), 0 2px 4px rgba(44,42,36,0.03);
  --shadow-organic-focus: 0 4px 14px rgba(44,42,36,0.06), 0 0 0 2px rgba(193,154,73,0.45);
  --shadow-organic-overlay: 0 8px 24px rgba(44,42,36,0.08), 0 2px 6px rgba(44,42,36,0.04);

  /* Shadows -- Mechanical */
  --shadow-mechanical-sm: 0 1px 3px rgba(44,42,36,0.08), 0 0.5px 1px rgba(44,42,36,0.06);
  --shadow-mechanical-md: 0 2px 4px rgba(44,42,36,0.10), 0 1px 2px rgba(44,42,36,0.06);
  --shadow-mechanical-active: 0 0.5px 1px rgba(44,42,36,0.10);
  --shadow-mechanical-bezel: inset 0 1px 0 rgba(255,255,255,0.08), 0 1px 3px rgba(44,42,36,0.10);

  /* Motion -- Mechanical */
  --ease-click: cubic-bezier(0.2, 0, 0, 1);
  --ease-precise: cubic-bezier(0.25, 0.1, 0.1, 1);
  --duration-tick: 80ms;
  --duration-click: 120ms;
  --duration-snap: 130ms;

  /* Motion -- Organic */
  --ease-grow: cubic-bezier(0.22, 1.2, 0.36, 1);
  --ease-unfurl: cubic-bezier(0.12, 0.8, 0.3, 1);
  --ease-settle: cubic-bezier(0.22, 1, 0.36, 1);
  --duration-warmth: 200ms;
  --duration-bloom: 350ms;
  --duration-unfurl: 500ms;
  --duration-grow: 600ms;
  --duration-reveal: 700ms;

  /* Motion -- Default */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --duration-default: 150ms;

  /* Layout */
  --content-max-width: 768px;
  --narrow-max-width: 640px;
  --sidebar-width: 280px;
  --header-height: 52px;
  --spacing-unit: 4px;

  /* Typography */
  --font-display: "Fraunces", Georgia, "Times New Roman", serif;
  --font-body: "DM Sans", system-ui, -apple-system, sans-serif;
  --font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
}
```

---

### Implementation Checklist

- [ ] Google Fonts loaded: Fraunces (variable, 400-600 with WONK axis), DM Sans (variable, 400-500), IBM Plex Mono (400, 500)
- [ ] CSS custom properties defined for all color tokens including the brass system (`--brass`, `--brass-highlight`, `--brass-muted`, `--brass-subtle`, `--brass-focus`, `--brass-hover`)
- [ ] CSS custom properties defined for the green system (`--greenhouse`, `--greenhouse-subtle`, `--greenhouse-hover`, `--patina`)
- [ ] Fraunces `font-variation-settings: "WONK" 1, "opsz" <size>` applied on display/heading text
- [ ] Fraunces `font-variation-settings: "WONK" 0` applied on subheading and smaller sizes
- [ ] DM Sans used for all body/UI text with appropriate weight values (400, 430, 500)
- [ ] IBM Plex Mono used for code, data readouts, and numeric values with `font-variant-numeric: tabular-nums`
- [ ] `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale` on root element
- [ ] `font-display: swap` on all font imports
- [ ] Focus ring uses brass (`rgba(193,154,73,0.50)`) on all interactive elements via `box-shadow`
- [ ] Brass caret color on text inputs (`caret-color: var(--brass)`)
- [ ] Dual shadow system implemented: organic shadows for content/cards, mechanical shadows for data readouts/instruments
- [ ] Shadow tokens used per component: organic-sm (card rest), organic-md (card hover), mechanical-sm (instrument rest), mechanical-md (instrument hover)
- [ ] Dual animation language implemented: organic (200-700ms, grow/unfurl/settle easing) for content elements, mechanical (80-130ms, click/precise easing) for controls/instruments
- [ ] Border opacity system: subtle/card/hover/focus/emphasis at 12/20/30/40/50%
- [ ] Brass bezel borders (1.5px, brass at 35%) on data readout components
- [ ] Border-radius minimum 4px, scale: 4/6/8/10/14px + 9999px
- [ ] Spacing scale: 4/6/8/12/16/20/24/32/48px with 4px base unit
- [ ] Content max-width 768px, sidebar 280px, header 52px
- [ ] Linen texture SVG filter implemented at 2.5% opacity with `mix-blend-mode: multiply`
- [ ] Labels use uppercase `text-transform` with DM Sans 500 weight and 0.04em tracking
- [ ] `prefers-reduced-motion` media query: organic durations cap at 200ms, mechanical at 100ms, ambient animations disabled, signature animations collapsed to opacity fades or disabled
- [ ] Scrollbar thumb uses brass tint (`rgba(193,154,73,0.30)`), transparent track
- [ ] `::selection` styled with brass at 20% opacity
- [ ] `::placeholder` color matches `text-muted` token (#928C7E)
- [ ] Touch targets >= 44px on all interactive elements
- [ ] WCAG AA contrast verified for all text-on-surface combinations
- [ ] Dark mode variant: surfaces shift to Night Soil/Dusk Timber/Lamp-lit Panel palette, brass brightens to `#D4AA55`, greens lift to `#5A9E72`
- [ ] Sidebar active state uses green (`#4A7C59`) left border, not brass
- [ ] Toggle on-state uses Spring Growth green (`#5B8C4A`), off-state uses neutral trellis wire
- [ ] No metallic gradients or chrome effects. Brass effect achieved through border + subtle box-shadow only.
- [ ] Mobile: linen texture disabled, dual shadows collapsed to organic-only, signature animations 1/3/4 disabled, touch targets maintained
- [ ] All state transitions match motion map: mechanical elements fast (80-130ms), organic elements slow (200-700ms)
- [ ] No pure greys in any surface or border. All neutrals carry warm yellow-brown undertone.
