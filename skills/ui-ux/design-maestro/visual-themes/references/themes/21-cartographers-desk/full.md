# Cartographer's Desk — Complete Theme Reference

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 12
- [Color System](#color-system) — Line 31
  - [Palette](#palette) — Line 33
  - [Special Tokens](#special-tokens) — Line 54
  - [Opacity System](#opacity-system) — Line 62
  - [Color Rules](#color-rules) — Line 73
- [Typography Matrix](#typography-matrix) — Line 82
  - [Font Loading](#font-loading) — Line 108
- [Elevation System](#elevation-system) — Line 114
  - [Surface Hierarchy](#surface-hierarchy) — Line 124
  - [Shadow Tokens](#shadow-tokens) — Line 135
  - [Separation Recipe](#separation-recipe) — Line 153
  - [Backdrop Blur](#backdrop-blur) — Line 158
- [Border System](#border-system) — Line 167
  - [Widths and Patterns](#widths-and-patterns) — Line 172
  - [Focus Ring](#focus-ring) — Line 185
  - [Radius](#radius) — Line 193
- [Component States](#component-states) — Line 210
  - [Buttons (Primary)](#buttons-primary) — Line 214
  - [Buttons (Ghost)](#buttons-ghost) — Line 224
  - [Text Input](#text-input) — Line 236
  - [Chat Input Card](#chat-input-card) — Line 247
  - [Cards](#cards) — Line 256
  - [Sidebar Items](#sidebar-items) — Line 265
  - [Chips](#chips) — Line 276
  - [Toggle / Switch](#toggle--switch) — Line 285
- [Motion Map](#motion-map) — Line 305
  - [Easings](#easings) — Line 311
  - [Duration x Easing x Component](#duration-x-easing-x-component) — Line 321
  - [Active Press Scale](#active-press-scale) — Line 337
  - [Reduced Motion](#reduced-motion) — Line 346
- [Layout Tokens](#layout-tokens) — Line 357
  - [Spacing Scale](#spacing-scale) — Line 368
  - [Density](#density) — Line 372
  - [Responsive Notes](#responsive-notes) — Line 376
- [Accessibility Tokens](#accessibility-tokens) — Line 384
- [Overlays](#overlays) — Line 412
  - [Popover / Dropdown](#popover--dropdown) — Line 414
  - [Modal](#modal) — Line 430
  - [Tooltip](#tooltip) — Line 444
- [Visual Style](#visual-style) — Line 459
  - [Material](#material) — Line 461
  - [Cartographic Rendering Rules](#cartographic-rendering-rules) — Line 487
  - [Data Visualization Philosophy](#data-visualization-philosophy) — Line 505
- [Signature Animations](#signature-animations) — Line 517
  - [1. Paper Layer Slide-In](#1-paper-layer-slide-in) — Line 519
  - [2. Contour Pulse](#2-contour-pulse) — Line 552
  - [3. Viewport Pan](#3-viewport-pan) — Line 583
  - [4. Layer Parallax](#4-layer-parallax) — Line 620
  - [5. Compass Rose Rotation](#5-compass-rose-rotation) — Line 649
- [Dark Mode Variant](#dark-mode-variant) — Line 683
  - [Dark Palette](#dark-palette) — Line 687
  - [Dark Shadow Tokens](#dark-shadow-tokens) — Line 711
  - [Dark Mode Rules](#dark-mode-rules) — Line 722
- [Mobile Notes](#mobile-notes) — Line 736
  - [Effects to Disable](#effects-to-disable) — Line 738
  - [Adjustments](#adjustments) — Line 745
  - [Performance Notes](#performance-notes) — Line 755
- [Implementation Checklist](#implementation-checklist) — Line 764

---

## Identity & Philosophy

This theme lives in a map room. Not a digital map application — a physical cartographer's workspace. Layered sheets of translucent paper pinned to a light table, each carrying a different data layer: the base terrain in ochre wash, water systems in meridian blue, grid references in fine brown ink, elevation contours tracing ridgelines, forest coverage in muted green. The desk itself is warm chart paper — slightly yellowed, slightly rough, the color of a sheet that has been handled by competent hands.

The core visual tension: **precision vs. warmth**. Cartographic data is exacting — coordinates, scales, grid labels, contour intervals — but the medium is organic. Paper has grain. Ink bleeds slightly. Layers stack with tiny misregistrations. The result is information that feels measured and trustworthy, presented on surfaces that feel tangible and real.

Every UI element exists at a position on a conceptual 2D map. Navigation is not clicking links — it is panning a viewport. Panels don't appear — they slide into the visible area from beyond the frame. Depth is not elevation in the material design sense — it is literal layer stacking. A card sits on a surface the way a detail chart sits on a regional map: overlaid, slightly offset, casting a directional shadow onto the layer below.

**Decision principle:** "When in doubt, ask: does this feel like something you'd find on a cartographer's light table? If it feels digital, add paper. If it feels decorative, add data. If it feels static, add spatial movement."

**What this theme is NOT:**
- Not a Google Maps clone — this is analog cartography, not satellite imagery or vector tiles
- Not precious or vintage — working maps are functional documents, not antiques
- Not centered on a single map view — the spatial metaphor extends to all UI: sidebars, cards, inputs, everything
- Not pastel or watercolor — colors come from actual cartographic conventions: Pantone map blues, terrain browns, forest greens
- Not smooth or slick — surfaces have paper-stacking depth with directional offset, not uniform drop shadows

---

## Color System

#### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Chart Paper | `#F5F0E5` | L=0.95 C=0.02 h=85 | Deepest background. Warm off-white, the color of aged cartographic paper under diffuse light. |
| bg | Drafting Vellum | `#EDE8DB` | L=0.93 C=0.02 h=80 | Primary surface. One shade warmer than page, like a second paper layer. |
| surface | Tracing Sheet | `#FFFFFF` | L=1.0 C=0 h=0 | Elevated cards, inputs, popovers. Clean white like fresh tracing paper overlaid on the base. |
| recessed | Field Notebook | `#E5DFD0` | L=0.90 C=0.03 h=78 | Code blocks, inset areas. Slightly darker and warmer, like kraft paper inserts. |
| active | Highlighted Region | `#DCD5C4` | L=0.87 C=0.03 h=75 | Active/pressed items, selected regions. The color of paper where a finger has traced repeatedly. |
| text-primary | India Ink | `#2C2A26` | L=0.22 C=0.01 h=70 | Headings, body text. Near-black with a brown bias — cartographic ink, not printer black. |
| text-secondary | Graphite | `#5C574E` | L=0.42 C=0.02 h=65 | Sidebar items, secondary labels. The color of pencil annotation. |
| text-muted | Faded Notation | `#9A9487` | L=0.64 C=0.02 h=70 | Placeholders, timestamps, metadata. Pencil marks that have been partially erased. |
| text-onAccent | Chart Paper | `#F5F0E5` | L=0.95 C=0.02 h=85 | Text on accent-colored backgrounds. Returns to page color. |
| border-base | Contour Brown | `#8B7D6B` | L=0.57 C=0.04 h=65 | Used at variable opacity. The brown of contour lines and grid references. |
| accent-primary | Meridian Blue | `#2B6CB0` | L=0.50 C=0.12 h=250 | Primary CTA, links, active controls. The blue used for water features on topographic maps. |
| accent-secondary | Terrain Ochre | `#C4883A` | L=0.67 C=0.12 h=70 | Secondary accent for highlights, callouts, elevation data. Land-mass coloring. |
| success | Forest Green | `#3D7C47` | L=0.52 C=0.12 h=145 | Positive states. The green of forest coverage on a topo map. |
| warning | Amber Marker | `#D4930D` | L=0.70 C=0.14 h=75 | Caution states. Cartographic warning symbol color. |
| danger | Boundary Red | `#C0392B` | L=0.50 C=0.16 h=25 | Error states. The red used for political boundaries and restricted zones. |
| info | Meridian Blue | `#2B6CB0` | L=0.50 C=0.12 h=250 | Info states. Matches accent-primary — water and information share the same ink. |

#### Special Tokens

| Token | Value | Role |
|---|---|---|
| inlineCode | `#6B5B3E` | Code text within prose. Deep sepia, like a handwritten coordinate reference. |
| toggleActive | `#3D7C47` | Toggle/switch active track. Forest green — "area covered." |
| selection | `rgba(43,108,176,0.18)` | `::selection` background. Meridian blue at 18%, like a translucent highlight overlay. |

#### Opacity System

Border opacity (on `border-base` Contour Brown):

| Context | Opacity | Usage |
|---|---|---|
| subtle | 12% | Faint grid lines, internal dividers within cards. Like pencil grid on tracing paper. |
| card | 22% | Card-level borders, panel edges. Contour line weight. |
| hover | 32% | Hovered elements, interactive feedback. Traced contour emphasis. |
| focus | 45% | Focus state. Heavy contour, prominent. |

#### Color Rules

- Colors derive from cartographic conventions. Meridian blue is for water, links, and interactive elements (they flow). Terrain ochre is for land, data, and highlights (they are solid). Forest green is for positive/covered/complete. Boundary red is for edges, errors, and limits.
- No gradients on surfaces. Gradients are permitted ONLY for elevation coloring in data visualizations (hypsometric tints).
- The page color (`#F5F0E5`) is not decorative — it IS the work surface. It should feel like paper, not like a tinted website background.
- Text-primary is warm near-black (`#2C2A26`), never pure black. India ink on chart paper has a brown cast.

---

## Typography Matrix

Headline font: Instrument Sans (condensed, modern, dashboard-dense). Body font: Albert Sans (Scandinavian minimalism, small-size legibility). Data/code font: JetBrains Mono (tabular numerals, coordinate readability). This is a three-font stack optimized for dense spatial layouts where labels must be readable at very small sizes — exactly the constraint a map imposes.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Instrument Sans | 28px | 600 | 1.15 | -0.02em | -- | Page titles, region names. Condensed for horizontal space efficiency. |
| Heading | Instrument Sans | 18px | 600 | 1.25 | -0.01em | -- | Section titles, panel headers. Dense heading scale. |
| Body | Albert Sans | 15px | 400 | 1.55 | 0.005em | -- | Primary reading text, descriptions. Optimized for chart-paper background contrast. |
| Body Small | Albert Sans | 13px | 400 | 1.45 | 0.01em | -- | Sidebar items, form labels, secondary text. Map label scale. |
| Button | Instrument Sans | 13px | 550 | 1.35 | 0.02em | -- | Button labels. Slightly tracked for small-size legibility. |
| Input | Albert Sans | 14px | 420 | 1.4 | 0.005em | -- | Form input text. Slightly heavier than body for field legibility. |
| Label | Instrument Sans | 11px | 500 | 1.3 | 0.04em | `text-transform: uppercase` | Metadata, timestamps, axis labels, map grid references. ALL CAPS like map annotations. |
| Code | JetBrains Mono | 13px | 400 | 1.5 | normal | `font-feature-settings: "zero", "tnum"` | Inline code, coordinates, data values. Tabular nums for alignment. |
| Caption | Albert Sans | 11px | 400 | 1.35 | 0.01em | -- | Footnotes, scale bars, legend notes, attribution text. |

**Typographic decisions:**
- Instrument Sans for headings provides condensed energy — it packs more characters per line, essential for dashboard-dense cartographic UIs where labels compete for space.
- Albert Sans for body text provides Scandinavian minimalism — clean, neutral, and critically, excellent legibility at 13-15px. Map interfaces demand small-text readability.
- JetBrains Mono for data ensures coordinate pairs like `48.8566, 2.3522` align in columns with `tnum` (tabular numerals) and `zero` (slashed zero to distinguish from O).
- Labels are ALL CAPS with wide tracking (0.04em) — the convention for map annotations. Grid reference labels, scale text, and metadata all follow this rule.
- `font-smoothing: antialiased` always. Light text on the warm background bleeds without it.
- `text-wrap: pretty` for body text (descriptions can reflow elegantly), `auto` for data text.
- Tight heading scale: 28px display, 18px heading. The gap is intentionally small — cartographic layouts don't have hero sections with massive titles.

#### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;550;600&family=Albert+Sans:wght@400;420;500&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

---

## Elevation System

**Strategy:** `layered-shadows` — paper-stacking

This theme uses a directional shadow system that simulates physical paper sheets stacked on a light table. Each layer casts a shadow in a consistent direction (bottom-right, simulating a desk lamp at top-left). Shadows are warm-toned (brown-tinged, not grey or black) because light passing through chart paper picks up the paper's warmth.

The key difference from generic layered shadows: every shadow has a **directional offset** (x and y are both positive, not centered) and the blur is tight (papers don't float — they sit on each other with minimal air gap).

#### Surface Hierarchy

| Surface | Background | Shadow | Usage |
|---|---|---|---|
| page | `#F5F0E5` (Chart Paper) | none | Main page canvas, the light table surface |
| bg | `#EDE8DB` (Drafting Vellum) | none | Sidebar background, secondary panels. Sits flush on page. |
| card | `#FFFFFF` (Tracing Sheet) | shadow-card | Cards, panels. A sheet of paper placed ON the desk. |
| recessed | `#E5DFD0` (Field Notebook) | none (inset border instead) | Code blocks, inset data wells. Carved into the desk. |
| active | `#DCD5C4` (Highlighted Region) | none | Active items. Paper worn from use. |
| overlay | `#FFFFFF` (Tracing Sheet) | shadow-popover | Popovers, dropdowns. A detail chart placed over the main map. |

#### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `1px 1px 2px rgba(107,91,62,0.08), 0 0 0 0.5px rgba(139,125,107,0.10)` | Small elements, chips. Barely lifted paper edge. |
| shadow-card | `2px 2px 6px rgba(107,91,62,0.10), 1px 1px 2px rgba(107,91,62,0.06)` | Card rest state. Paper on desk — directional, warm, tight blur. |
| shadow-card-hover | `3px 3px 8px rgba(107,91,62,0.14), 1px 1px 3px rgba(107,91,62,0.08)` | Card hover. Paper lifted slightly — shadow grows and shifts. |
| shadow-input | `1px 1px 4px rgba(107,91,62,0.06), 0 0 0 0.5px rgba(139,125,107,0.12)` | Input card rest. Subtle directional lift with hairline ring. |
| shadow-input-hover | `2px 2px 6px rgba(107,91,62,0.10), 0 0 0 0.5px rgba(139,125,107,0.20)` | Input card hover. Shadow deepens, ring brightens. |
| shadow-input-focus | `2px 2px 8px rgba(107,91,62,0.14), 0 0 0 1px rgba(43,108,176,0.30)` | Input card focus. Warm shadow + blue accent ring. |
| shadow-popover | `3px 4px 12px rgba(107,91,62,0.18), 1px 2px 4px rgba(107,91,62,0.10)` | Popovers, dropdowns. Detail chart overlaid — strongest lift. |
| shadow-none | `none` | Recessed/flush surfaces. No lift. |

**Shadow design notes:**
- All shadows use `rgba(107,91,62,...)` — a warm sepia tone derived from the border-base color darkened. Shadows on chart paper are warm, never grey.
- X and Y offsets are always positive and nearly equal (slight bottom-right bias). This creates the consistent "desk lamp at top-left" directionality. Every paper sheet casts its shadow in the same direction.
- Blur radius stays tight: 2-12px range. Papers rest on surfaces — they don't float. The shadow says "this is a separate layer" not "this is hovering."
- The composite format (two shadows per token) adds a sharp close shadow (the paper edge contact line) plus a softer far shadow (the penumbra). This is how real paper shadows work.

#### Separation Recipe

Paper-stacking with directional offset. Surfaces separate through three mechanisms: (1) tint-step — each layer is a slightly different paper tone; (2) directional shadow — every elevated surface casts a warm, bottom-right shadow; (3) contour-weight borders at low opacity for internal structure. No divider lines inside cards — spacing and alignment create grouping. Recessed areas use inset borders (top and left hairlines) to suggest depth carved into the desk surface, not shadows.

#### Backdrop Blur

| Context | Value | Usage |
|---|---|---|
| popover | `12px` | Popovers and dropdowns. Slight blur of underlying map layers. |
| modal | `8px` | Modal backdrop. Map blurs when examining a detail. |
| none | `0px` | Default. Most surfaces are opaque paper. |

---

## Border System

Borders in this theme follow cartographic contour-line conventions. Contour lines vary in weight to communicate hierarchy: index contours (every 5th line) are heavier, intermediate contours are lighter. Similarly, borders use weight variation — not color variation — to communicate hierarchy. The color is always contour brown at varying opacity.

#### Widths and Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| subtle | 0.5px | `border-base` at 12% | Grid lines within cards, faint internal dividers. Intermediate contour. |
| card | 1px | `border-base` at 22% | Card borders, panel edges. Standard contour line. |
| hover | 1px | `border-base` at 32% | Hovered element border. Emphasized contour. |
| heavy | 1.5px | `border-base` at 40% | Section dividers, header underlines. Index contour. |
| input | 1px | `border-base` at 20% | Form input borders at rest. |
| input-hover | 1px | `border-base` at 32% | Input hover. Contour darkens. |
| input-focus | 1.5px | `accent-primary` at 100% | Input focus. Meridian blue — the element becomes a water feature. |
| accent-bottom | 2px | `accent-primary` at 100% | Bottom-border accent on active tabs, selected sections. Map legend indicator. |
| recessed-inset | 0.5px | `border-base` at 15% (top + left only) | Inset border on recessed surfaces, simulating carved depth. |

#### Focus Ring

- **Color:** `rgba(43,108,176,0.50)` (Meridian Blue at 50%)
- **Width:** 2px solid
- **Offset:** 2px (via `outline-offset: 2px`)
- **Implementation:** `outline: 2px solid rgba(43,108,176,0.50); outline-offset: 2px;`
- **Character:** The focus ring is the color of water on a map — it "floods" the focused element's perimeter, creating a moat of attention.

#### Radius

| Token | Value | Usage |
|---|---|---|
| none | 0px | Not used as default |
| sm | 3px | Chips, small badges. Slightly rounded like map pin markers. |
| md | 5px | Buttons, inputs. Functional rounding for click targets. |
| lg | 7px | Cards, panels. Paper-edge rounding — sheets never have perfectly sharp corners. |
| xl | 10px | Major containers. |
| 2xl | 16px | Chat input card, modal. |
| input | 7px | Form inputs. Matches card radius. |
| full | 9999px | Toggles, avatars. Full pill/circle. |

**Radius philosophy:** Real paper sheets have slightly rounded corners from handling. This theme uses modest radii (3-7px) that suggest paper without becoming pill-shaped. Nothing goes below 3px (digital sharpness) or above 16px (over-rounded slop). The radius scale is tighter than most themes because cartographic precision favors structure over softness.

---

## Component States

All transitions use ease-out curves with short durations. The cartographic metaphor demands that interactions feel like sliding paper: quick to initiate, decelerating to rest.

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `accent-primary` (`#2B6CB0`), border none, color `text-onAccent`, radius md (5px), h 34px, padding `0 14px`, font button (Instrument Sans 13px/550) |
| Hover | bg `#245FA0` (darkened 8%), shadow `shadow-sm`, transition 120ms ease-out |
| Active | bg `#1E5290` (darkened 15%), transform `scale(0.97)`, shadow none |
| Focus | outline `2px solid rgba(43,108,176,0.50)`, outline-offset 2px |
| Disabled | opacity 0.45, pointer-events none, cursor not-allowed, shadow none |
| Transition | `background 120ms ease-out, box-shadow 120ms ease-out, transform 80ms ease-out` |

#### Buttons (Ghost)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid border-base at 22%`, color `text-secondary`, radius md (5px), h 34px, padding `0 14px` |
| Hover | bg `recessed` (`#E5DFD0`), border at 32%, color `text-primary`, transition 150ms ease-out |
| Active | bg `active` (`#DCD5C4`), transform `scale(0.97)` |
| Focus | outline focus ring |
| Disabled | opacity 0.45, pointer-events none |
| Transition | `background 150ms ease-out, border-color 150ms ease-out, color 150ms ease-out` |

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `surface` (`#FFFFFF`), border `1px solid border-base at 20%`, radius input (7px), h 40px, padding `0 12px`, font input (Albert Sans 14px/420), color `text-primary`, placeholder `text-muted`, caret-color `accent-primary` |
| Hover | border at 32%, shadow `shadow-input-hover`, transition 150ms ease-out |
| Focus | border `1.5px solid accent-primary`, shadow `shadow-input-focus`, outline none |
| Disabled | opacity 0.45, pointer-events none, bg `recessed`, cursor not-allowed |
| Transition | `border-color 150ms ease-out, box-shadow 200ms ease-out` |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `surface` (`#FFFFFF`), radius 2xl (16px), border `1px solid border-base at 12%`, shadow `shadow-input` |
| Hover | shadow `shadow-input-hover`, border at 22%, transition 200ms ease-out |
| Focus-within | shadow `shadow-input-focus`, border `1px solid accent-primary at 40%` |
| Transition | `box-shadow 200ms ease-out, border-color 150ms ease-out` |

#### Cards

| State | Properties |
|---|---|
| Rest | bg `surface` (`#FFFFFF`), border `1px solid border-base at 22%`, radius lg (7px), shadow `shadow-card` |
| Hover | border at 32%, shadow `shadow-card-hover`, transform `translate(-0.5px, -0.5px)`, transition 180ms ease-out |
| Transition | `border-color 150ms ease-out, box-shadow 180ms ease-out, transform 180ms ease-out` |

**Card hover note:** The `translate(-0.5px, -0.5px)` on hover is the paper-lift metaphor — the card shifts slightly upward and leftward (toward the light source) as if being picked up from the stack. The shadow simultaneously grows in the opposite direction. This coordinated lift-and-shadow-shift is the theme's signature depth interaction.

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `text-secondary`, radius md (5px), h 34px, padding `6px 14px`, font bodySmall (Albert Sans 13px/400) |
| Hover | bg `recessed` (`#E5DFD0`), color `text-primary`, transition 100ms ease-out |
| Active (current) | bg `active` (`#DCD5C4`), color `text-primary`, border-left `2px solid accent-primary`, padding-left 12px (compensate border) |
| Active press | transform `scale(0.985)` |
| Transition | `background 100ms ease-out, color 100ms ease-out` |

#### Chips

| State | Properties |
|---|---|
| Rest | bg `bg` (`#EDE8DB`), border `0.5px solid border-base at 15%`, radius sm (3px), h 28px, padding `0 10px`, font label (Instrument Sans 11px/500), color `text-secondary`, text-transform uppercase, letter-spacing 0.04em |
| Hover | bg `active` (`#DCD5C4`), border at 25%, color `text-primary`, transition 120ms ease-out |
| Active/selected | bg `accent-primary`, color `text-onAccent`, border `accent-primary` |
| Active press | transform `scale(0.995)` |
| Transition | `background 120ms ease-out, border-color 120ms ease-out, color 120ms ease-out` |

#### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 38px |
| Track height | 22px |
| Track radius | full (9999px) |
| Track off bg | `active` token (`#DCD5C4`) |
| Track off border | `1px solid border-base at 22%` |
| Track on bg | `toggleActive` (`#3D7C47`) Forest Green — "terrain covered" |
| Track on border | none |
| Thumb | 18px circle, bg `surface` (`#FFFFFF`), radius full |
| Thumb off position | left 2px |
| Thumb on position | right 2px |
| Thumb shadow | `1px 1px 2px rgba(107,91,62,0.12)` — directional, warm |
| Transition | `background 150ms ease-out, transform 150ms ease-out` |
| Focus-visible | focus ring around entire track |

---

## Motion Map

**Core philosophy:** Spatial continuity. Everything in this UI has a 2D position on the conceptual map. Elements don't "appear" — they are revealed by viewport movement. Transitions feel like panning across a surface, zooming into a region, or sliding one paper layer over another. The key motion verbs: **pan**, **zoom**, **slide**, **parallax**.

Easing follows natural deceleration — things move quickly when pushed and slow down as friction takes hold. Like sliding a sheet of paper across a desk: fast start, gradual stop.

#### Easings

| Name | Value | Character |
|---|---|---|
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. General purpose. |
| pan-out | `cubic-bezier(0.16, 1, 0.3, 1)` | Fast deceleration. Paper sliding to a stop. Primary easing. |
| zoom-in | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Slight overshoot. Zooming into a map region — overshoots then settles. |
| layer-settle | `cubic-bezier(0.22, 0.68, 0, 1.0)` | Gentle landing. Paper settling onto the desk after being placed. |
| out-expo | `cubic-bezier(0.19, 1, 0.22, 1)` | Smooth open/close. Panel reveal. |
| instant | `steps(1)` | Toggle states, mode switches. No spatial metaphor needed. |

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 100ms | pan-out | Quick response — finger sliding across a legend |
| Button hover bg | 120ms | default | Standard interaction speed |
| Toggle/chip state | 150ms | default | General control feedback |
| Card hover shadow + lift | 180ms | pan-out | Paper lift — shadow grows as card shifts |
| Input card shadow | 200ms | default | Shadow transition on focus |
| Ghost icon buttons | 250ms | pan-out | Slightly longer for icon-only targets |
| Panel slide open/close | 400ms | out-expo | Paper panel sliding into view from the edge |
| Page/section entry | 500ms | pan-out | Content panning into the viewport |
| Layer parallax shift | 600ms | layer-settle | Background layers shifting at different rates |
| Zoom transition | 350ms | zoom-in | Zooming into a detail view — slight overshoot |

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Subtle — pressing a map legend entry |
| Chips | 0.995 | Barely perceptible — selecting a filter |
| Buttons | 0.97 | Standard press — stamping a location |
| Tabs | 0.96 | Pronounced — switching map layers |

#### Reduced Motion

- **Strategy:** `reduced-distance` — all transitions still occur but spatial movement is eliminated
- Pan/slide animations collapse to opacity-only fades (200ms linear)
- Zoom transitions become instant cuts
- Card hover lift (`translate`) disabled, shadow-only feedback retained
- Parallax disabled — all layers move at the same rate
- `disableAmbient: true` — compass rose rotation and contour pulse stop
- `disableParallax: true`

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 780px | Main content column. Slightly wider for map-dense data. |
| Narrow max-width | 672px | Focused reading, single-panel views. |
| Sidebar width | 280px | Map legend panel. Fixed. |
| Header height | 48px | Top bar with navigation coordinates. |
| Spacing unit | 4px | Base grid multiplier. |

#### Spacing Scale

4, 6, 8, 12, 16, 20, 28, 36px — includes 6px and 20px for fine-grained control in dense spatial layouts.

#### Density

**Moderate.** Denser than standard consumer UI but not as packed as a Bloomberg terminal. Map interfaces need room for labels and annotations but cannot waste space on padding alone. Internal card padding: 12-16px. Section gaps: 20-28px. List item gaps: 4-6px. This density allows map-like information packing while keeping individual elements scannable.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (280px) + content column. Cards arrange in multi-column grids. Shadow directionality maintained.
- **md (768px):** Sidebar collapses to slide-out overlay (pan-in from left, 400ms out-expo). Content fills width. Card grid reduces to 2 columns.
- **sm (640px):** Single column. Header simplifies — coordinates collapse to compact format. Cards stack vertically with full width. Paper-stacking shadows reduce to `shadow-sm` only (save compositing cost). Parallax disabled.

---

## Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring color | `rgba(43,108,176,0.50)` (Meridian Blue at 50%) |
| Focus ring width | 2px solid |
| Focus ring offset | 2px |
| Disabled opacity | 0.45 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled desaturation | `filter: saturate(0.6)` — muted, not just transparent |
| Selection bg | `rgba(43,108,176,0.18)` (Meridian Blue at 18%) |
| Selection color | `#2C2A26` (text-primary) |
| Scrollbar width | thin |
| Scrollbar thumb | `rgba(139,125,107,0.30)` (Contour Brown at 30%) |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

**Contrast verification:**
- Text-primary `#2C2A26` on page `#F5F0E5` = 11.4:1 (exceeds AAA)
- Text-secondary `#5C574E` on page `#F5F0E5` = 5.1:1 (passes AA)
- Text-muted `#9A9487` on page `#F5F0E5` = 2.7:1 (used for non-essential metadata only, not body text)
- Accent-primary `#2B6CB0` on surface `#FFFFFF` = 5.3:1 (passes AA)
- Text-onAccent `#F5F0E5` on accent-primary `#2B6CB0` = 5.0:1 (passes AA)

---

## Overlays

#### Popover / Dropdown

- **bg:** `surface` token (`#FFFFFF`) at 95% opacity
- **backdrop-filter:** `blur(12px)` — underlying map layers become slightly defocused
- **border:** `1px solid border-base at 25%`
- **radius:** lg (7px)
- **shadow:** `shadow-popover` (3px 4px 12px warm sepia)
- **padding:** 6px
- **z-index:** 50
- **min-width:** 200px, **max-width:** 320px
- **Menu item:** 6px 10px padding, radius md (5px), h 32px, font bodySmall, color text-secondary
- **Menu item hover:** bg `recessed` (`#E5DFD0`), color `text-primary`, transition 100ms pan-out
- **Divider:** `0.5px solid border-base at 12%`, margin `4px 6px`
- **Entry:** opacity 0 to 1 + `translateY(4px)` to `translateY(0)`, 180ms pan-out. Paper detail dropping onto the desk.
- **Exit:** opacity 1 to 0, 120ms default

#### Modal

- **Overlay bg:** `rgba(44,42,38,0.55)` — warm, like looking through smoked glass at the desk beneath
- **Overlay backdrop-filter:** `blur(8px)`
- **Content bg:** `surface` token (`#FFFFFF`)
- **Content border:** `1px solid border-base at 25%`
- **Content radius:** xl (10px)
- **Content shadow:** `shadow-popover`
- **Content padding:** 24px
- **Content max-width:** 520px
- **Entry:** opacity 0 to 1 + `scale(0.96)` to `scale(1)`, 250ms pan-out. A detail chart being placed on the desk and sliding into position.
- **Exit:** opacity 1 to 0 + `scale(1)` to `scale(0.98)`, 180ms default
- **Close button:** Ghost button, top-right, 34x34px

#### Tooltip

- **bg:** `#2C2A26` (India Ink — inverted from the light surface for maximum contrast)
- **color:** `#F5F0E5` (Chart Paper)
- **font:** label size (Instrument Sans 11px, weight 500)
- **border:** none (the inverted color provides sufficient separation)
- **radius:** sm (3px)
- **padding:** 5px 9px
- **shadow:** `1px 1px 4px rgba(107,91,62,0.20)` — directional, warm
- **letter-spacing:** 0.02em
- **No arrow.** Positioned via offset. Appears with opacity fade 120ms default.
- **Character:** Tooltips are map annotations — small, precise, dark ink on the page. Inverted color scheme (dark on light theme) makes them pop like a legend callout.

---

## Visual Style

#### Material

- **Grain:** Subtle paper grain via SVG feTurbulence at 2% opacity. Applied as a full-screen overlay with `pointer-events: none`. This is chart paper — it has texture.

```html
<svg width="0" height="0" style="position:absolute">
  <filter id="chart-paper-grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" stitchTiles="stitch" />
    <feColorMatrix type="saturate" values="0" />
  </filter>
</svg>
```
```css
.paper-grain {
  position: fixed; inset: 0;
  opacity: 0.02;
  filter: url(#chart-paper-grain);
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: multiply;
}
```

- **Gloss:** Matte. Paper surfaces have zero sheen. Buttons and interactive elements have a very slight satin quality from their shadow layer, but no gloss.
- **Blend mode:** multiply for grain layer (adds warmth), normal for all other elements.
- **Shader bg:** false. No WebGL. This is paper, not glass.

#### Cartographic Rendering Rules

- **Contour Line Pattern:** Borders on cards and containers can optionally use `border-style: dashed` with `dash: 6 4` for decorative containers that suggest topographic contour lines. Use sparingly — only on map-related containers, not standard UI cards.

```css
.contour-border {
  border: 1px dashed rgba(139,125,107,0.25);
  border-dasharray: 6 4; /* SVG only; CSS uses border-style: dashed */
}
```

- **Compass Rose:** A decorative SVG element placed in the top-right corner of the main content area. Rotates slowly (60s linear infinite) as an ambient detail. Contour brown at 8% opacity. Disabled at `prefers-reduced-motion`.

- **Grid Reference Labels:** The `Label` typography role (11px, ALL CAPS, 0.04em tracking) is used for grid references, coordinates, and scale annotations. These should appear in `text-muted` color and be positioned absolutely at the edges of containers, like grid labels on a map sheet.

- **Layer Indicator Marks:** Small colored dots (6px circles) in the corner of cards indicate which "map layer" the card belongs to. Use the accent-primary (blue, water/navigation data), accent-secondary (ochre, terrain/metric data), success (green, coverage/status data), or danger (red, alert/boundary data) colors.

#### Data Visualization Philosophy

Cartographic conventions extend to all data visualization:

- **YES:** Choropleth maps (color fill by region), contour/isoline charts, scatter plots with geographic metaphor, heatmaps, treemaps (rectangular territory), layered area charts (stacked terrain).
- **NO:** 3D charts, pie charts, donut charts, radial gauges. Cartographers work in 2D.
- **Color ramps:** Use hypsometric tints — a single-hue ramp from light (low values) to dark (high values). Meridian blue for sequential data. Ochre-to-blue diverging scale for comparison data. Forest green for positive/coverage data.
- **Grid:** Visible but low-ink. `border-base at 8%` gridlines. Labeled axes in `Label` typography.
- **Annotation:** Charts should include annotation markers — small text callouts positioned at key data points, like map annotations. Use `Caption` typography.

---

## Signature Animations

#### 1. Paper Layer Slide-In

New content panels slide in from the edge of the viewport as if being slid across the desk surface. The panel enters with a directional movement (left panels slide from left, right panels from right, bottom panels from below) and its shadow appears progressively as it overlaps the underlying content.

- **Technique:** `transform: translateX()` with progressive shadow reveal
- **Duration:** 400ms
- **Easing:** `pan-out` — `cubic-bezier(0.16, 1, 0.3, 1)`
- **CSS:**
```css
@keyframes slide-from-left {
  from {
    transform: translateX(-100%);
    box-shadow: none;
  }
  to {
    transform: translateX(0);
    box-shadow: 3px 4px 12px rgba(107,91,62,0.18),
                1px 2px 4px rgba(107,91,62,0.10);
  }
}
.panel-enter-left {
  animation: slide-from-left 400ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
@media (prefers-reduced-motion: reduce) {
  .panel-enter-left {
    animation: none;
    opacity: 1;
  }
}
```
- **Reduced motion:** Instant appearance, no slide.

#### 2. Contour Pulse

When a card or section receives updated data, its border briefly pulses through three contour weights — simulating an elevation change on a map. The border goes from standard (1px at 22%) to heavy (1.5px at 40%) and back, as if the terrain shifted and the contour lines redrew.

- **Technique:** `border-width` and `border-opacity` keyframe sequence
- **Duration:** 600ms
- **Easing:** `default` — `cubic-bezier(0.4, 0, 0.2, 1)`
- **CSS:**
```css
@keyframes contour-pulse {
  0% {
    border-color: rgba(139,125,107,0.22);
    box-shadow: 2px 2px 6px rgba(107,91,62,0.10);
  }
  40% {
    border-color: rgba(139,125,107,0.45);
    box-shadow: 3px 3px 10px rgba(107,91,62,0.18);
  }
  100% {
    border-color: rgba(139,125,107,0.22);
    box-shadow: 2px 2px 6px rgba(107,91,62,0.10);
  }
}
.contour-update {
  animation: contour-pulse 600ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
@media (prefers-reduced-motion: reduce) {
  .contour-update { animation: none; }
}
```
- **Reduced motion:** No pulse. Border stays at rest state.

#### 3. Viewport Pan

Page transitions between major sections use a 2D pan — the entire content area shifts horizontally or vertically as if the user is moving a viewport across a larger map surface. The outgoing content slides away and the incoming content slides into frame from the opposite direction.

- **Technique:** `transform: translate()` on both outgoing and incoming content
- **Duration:** 500ms
- **Easing:** `pan-out` — `cubic-bezier(0.16, 1, 0.3, 1)`
- **CSS:**
```css
@keyframes pan-exit-left {
  from { transform: translateX(0); opacity: 1; }
  to { transform: translateX(-40px); opacity: 0; }
}
@keyframes pan-enter-right {
  from { transform: translateX(40px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
.page-exit {
  animation: pan-exit-left 500ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.page-enter {
  animation: pan-enter-right 500ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
@media (prefers-reduced-motion: reduce) {
  .page-exit, .page-enter {
    animation-duration: 200ms;
    animation-name: fade-only;
  }
  @keyframes fade-only {
    from { opacity: 0; transform: none; }
    to { opacity: 1; transform: none; }
  }
}
```
- **Reduced motion:** Crossfade only, no spatial movement.

#### 4. Layer Parallax

When the user scrolls, background elements (compass rose, grid labels, watermark patterns) move at a slower rate than foreground content. This creates depth between the "desk surface" and the "paper layers" on top of it. Three parallax rates: background at 0.3x, mid-layer at 0.6x, foreground at 1.0x.

- **Technique:** `transform: translateY()` driven by scroll position
- **Duration:** Continuous (tied to scroll)
- **Easing:** Linear (direct positional mapping)
- **CSS / JS:**
```css
.parallax-bg { transform: translateY(calc(var(--scroll-y) * 0.3)); }
.parallax-mid { transform: translateY(calc(var(--scroll-y) * 0.6)); }
.parallax-fg { transform: translateY(0); /* default scroll */ }

@media (prefers-reduced-motion: reduce) {
  .parallax-bg, .parallax-mid {
    transform: none !important;
  }
}
```
```js
// Set CSS custom property for scroll position
window.addEventListener('scroll', () => {
  document.documentElement.style.setProperty(
    '--scroll-y', `${window.scrollY * -1}px`
  );
}, { passive: true });
```
- **Reduced motion:** All layers scroll at the same rate. No parallax.

#### 5. Compass Rose Rotation

A slow, continuous rotation of the decorative compass rose SVG in the corner of the content area. 360 degrees over 60 seconds, linear timing. Purely ambient — it reinforces the cartographic identity without demanding attention. The rose is rendered at 8% opacity in contour brown.

- **Technique:** `transform: rotate()` infinite animation
- **Duration:** 60000ms (60 seconds per revolution)
- **Easing:** linear
- **CSS:**
```css
@keyframes compass-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.compass-rose {
  animation: compass-spin 60s linear infinite;
  opacity: 0.08;
  color: var(--border-base);
  pointer-events: none;
  position: absolute;
  top: 16px;
  right: 16px;
  width: 64px;
  height: 64px;
}
@media (prefers-reduced-motion: reduce) {
  .compass-rose {
    animation: none;
    transform: rotate(0deg);
  }
}
```
- **Reduced motion:** Static compass rose. No rotation.

---

## Dark Mode Variant

The dark mode transforms the cartographer's desk from a daytime workspace to a **night survey station**. The light table switches off, surfaces become dark slate, and the meridian blue accent gains luminosity against the dark ground. Paper warmth disappears — this is fieldwork at night, not studio drafting.

#### Dark Palette

| Token | Dark Hex | Role Change |
|---|---|---|
| page | `#1A1C20` | Dark slate. Blue-grey undertone, not warm brown. Nighttime field desk. |
| bg | `#22252A` | Primary surface. Slate one step lighter. |
| surface | `#2C3038` | Cards, inputs. Cold elevated surface like a metal clipboard. |
| recessed | `#14161A` | Code blocks, data wells. Near-black. |
| active | `#363B44` | Active states. Highlighted region under a headlamp. |
| text-primary | `#E0DDD5` | Body text. Warm grey-white, like paper in low light. |
| text-secondary | `rgba(224,221,213,0.64)` | Secondary labels. text-primary at 64%. |
| text-muted | `rgba(224,221,213,0.38)` | Metadata. text-primary at 38%. |
| text-onAccent | `#E0DDD5` | Text on accent backgrounds. |
| border-base | `#5A6270` | Contour lines in moonlight — cooler, bluer than daytime brown. |
| accent-primary | `#4A90D9` | Meridian Blue, lightened for dark contrast. Brighter water on a night map. |
| accent-secondary | `#D4A04A` | Terrain Ochre, lightened. Lantern-lit terrain. |
| success | `#4F9A56` | Forest Green, slightly lifted. |
| warning | `#E0A820` | Amber Marker, brightened. |
| danger | `#D04A3C` | Boundary Red, lifted for dark bg contrast. |
| inlineCode | `#C9A86C` | Warm gold code text. Sepia ink under lamplight. |
| toggleActive | `#4F9A56` | Forest green, lifted. |
| selection | `rgba(74,144,217,0.22)` | Blue at 22%. |

#### Dark Shadow Tokens

Shadows on dark mode are larger and use pure black (not warm sepia). In dark environments, shadows are less visible, so they need more spread to register.

| Token | Dark Value |
|---|---|
| shadow-card | `3px 3px 10px rgba(0,0,0,0.25), 1px 1px 3px rgba(0,0,0,0.15)` |
| shadow-card-hover | `4px 4px 14px rgba(0,0,0,0.30), 2px 2px 4px rgba(0,0,0,0.18)` |
| shadow-input | `2px 2px 6px rgba(0,0,0,0.15), 0 0 0 0.5px rgba(90,98,112,0.18)` |
| shadow-input-focus | `2px 2px 10px rgba(0,0,0,0.20), 0 0 0 1px rgba(74,144,217,0.35)` |
| shadow-popover | `4px 5px 16px rgba(0,0,0,0.35), 2px 3px 6px rgba(0,0,0,0.20)` |

#### Dark Mode Rules

- Surface temperature shifts from warm (brown undertones) to cool (blue-grey undertones). This is not simple inversion — it's a full palette recharacterization from studio to field.
- Paper grain overlay reduces to 1% opacity and shifts blend mode from `multiply` to `soft-light` (grain adds subtle lightness on dark surfaces, not darkness).
- Border-base shifts from warm brown (`#8B7D6B`) to cool slate (`#5A6270`). Borders become cooler.
- Accent-primary (meridian blue) lightens from `#2B6CB0` to `#4A90D9` to maintain contrast on dark surfaces. It should feel luminous, like water reflecting moonlight.
- Shadows shift from warm sepia composite to pure black composite. Warm shadows on dark surfaces look muddy; black shadows are invisible but structurally correct.
- Border opacities shift: subtle 10%, card 18%, hover 28%, focus 40%. Slightly lower than light mode because borders are more visible against dark surfaces.
- The compass rose decorative element shifts to `border-base` at 6% opacity (from 8%). Less visible but still present.
- Focus ring: `rgba(74,144,217,0.55)` — brightened meridian blue for dark contrast.
- Scrollbar thumb: `rgba(90,98,112,0.30)` — cool grey on dark.

---

## Mobile Notes

#### Effects to Disable
- Layer parallax (signature #4) — disabled entirely. All layers scroll at same rate.
- Compass rose rotation (signature #5) — hidden on mobile. Decorative element takes up space.
- Paper grain SVG filter — disabled entirely for GPU performance.
- Card hover lift (`translate(-0.5px, -0.5px)`) — removed. Shadow-only feedback.
- Backdrop-filter blur on popovers — reduced from 12px to 4px.

#### Adjustments
- Header height: 48px (unchanged — already compact)
- Sidebar: hidden by default, slides in as overlay from left edge (400ms out-expo)
- Card radius: maintained (7px — already small)
- Card shadow: reduced to `shadow-sm` only on mobile (one layer of shadow instead of composite)
- Touch targets: all interactive elements maintain 44px minimum tap area
- Font sizes: Body stays 15px (already readable). Labels stay 11px. Display drops from 28px to 24px.
- Spacing scale: 20px section gaps reduce to 16px. Internal padding 12px stays.
- Contour dashed borders: disabled on mobile (rendering cost, visual noise at small scale)

#### Performance Notes
- Paper-stacking shadows are the primary GPU cost. Reducing to `shadow-sm` on mobile eliminates most compositing.
- `backdrop-filter: blur()` is expensive on iOS Safari. Reducing to 4px or removing entirely on low-powered devices.
- SVG feTurbulence grain filter is the single most expensive effect — always disable on mobile.
- Directional shadows (x/y offset) have no additional cost over centered shadows — the offset is just different values, same compositing work.
- `transform: translate()` animations are GPU-composited and cheap. Pan/slide animations can remain on mobile.

---

## Implementation Checklist

- [ ] Google Fonts loaded: Instrument Sans (400, 500, 550, 600) + Albert Sans (400, 420, 500) + JetBrains Mono (400)
- [ ] CSS custom properties defined for ALL color tokens with `data-theme="light"` / `data-theme="dark"` attribute switching
- [ ] Paper grain SVG filter defined in HTML, overlay div styled with `position: fixed; opacity: 0.02; mix-blend-mode: multiply; pointer-events: none; z-index: 9999`
- [ ] Border-radius scale applied: 3px sm, 5px md, 7px lg, 10px xl, 16px 2xl, 7px input, 9999px full
- [ ] Shadow tokens defined with directional offset (positive x and y) using warm sepia rgba values
- [ ] Shadow escalation implemented: card rest -> hover with progressive offset growth
- [ ] Border opacity system: 12% subtle, 22% card, 32% hover, 45% focus
- [ ] Focus ring: `outline: 2px solid rgba(43,108,176,0.50); outline-offset: 2px` on all interactive elements
- [ ] Card hover includes `transform: translate(-0.5px, -0.5px)` coordinated with shadow growth
- [ ] All transitions use ease-out curves — no `ease-in-out` on UI interactions
- [ ] `prefers-reduced-motion` media query: parallax disabled, pan animations collapse to fades, compass rose static, ambient effects paused
- [ ] Typography hierarchy: Instrument Sans for headings/buttons/labels (condensed), Albert Sans for body (clear), JetBrains Mono for code/data (tabular)
- [ ] Label role uses `text-transform: uppercase; letter-spacing: 0.04em` — map annotation convention
- [ ] `font-feature-settings: "zero", "tnum"` on JetBrains Mono for slashed zeros and tabular numerals
- [ ] Scrollbar styled: thin, `rgba(139,125,107,0.30)` thumb, transparent track
- [ ] `::selection` styled: `rgba(43,108,176,0.18)` background
- [ ] `::placeholder` uses text-muted color (`#9A9487`)
- [ ] Touch targets >= 44px on all interactive elements
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] Dark mode: all surface tokens swap to cool slate tones, shadows shift to black composite, borders cool, accent lightens
- [ ] Dark mode: paper grain reduces to 1% opacity with `soft-light` blend mode
- [ ] Compass rose SVG element: positioned top-right, 64x64px, 8% opacity, 60s linear rotation
- [ ] Tooltip uses inverted color scheme (dark bg on light theme, light bg on dark theme)
- [ ] Popover entry animation: `translateY(4px)` fade-in, 180ms pan-out
- [ ] Modal entry: `scale(0.96)` fade-in, 250ms pan-out
- [ ] Layer indicator dots (6px colored circles) available for card categorization
- [ ] Data visualization follows cartographic conventions: 2D only, hypsometric color ramps, low-ink grid lines, annotation markers
