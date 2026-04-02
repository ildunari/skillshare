# Sunlit Concrete — Full Reference

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 50
- [Color System](#color-system) — Line 87
  - [Palette](#palette) — Line 89
  - [Special Tokens](#special-tokens) — Line 110
  - [Opacity System](#opacity-system) — Line 120
  - [Color Rules](#color-rules) — Line 133
- [Typography Matrix](#typography-matrix) — Line 143
  - [Font Loading](#font-loading) — Line 173
- [Elevation System](#elevation-system) — Line 180
  - [Surface Hierarchy](#surface-hierarchy) — Line 186
  - [Shadow Tokens](#shadow-tokens) — Line 198
  - [Separation Recipe](#separation-recipe) — Line 212
- [Border System](#border-system) — Line 218
  - [Radius Tokens](#radius-tokens) — Line 222
  - [Widths and Patterns](#widths-and-patterns) — Line 233
  - [Focus Ring](#focus-ring) — Line 248
- [Component States](#component-states) — Line 257
  - [Buttons (Primary)](#buttons-primary) — Line 265
  - [Buttons (Safety/Danger)](#buttons-safetydanger) — Line 276
  - [Buttons (Ghost)](#buttons-ghost) — Line 287
  - [Text Input](#text-input) — Line 298
  - [KPI Readout Card](#kpi-readout-card) — Line 309
  - [Cards (Standard)](#cards-standard) — Line 335
  - [Sidebar Items](#sidebar-items) — Line 343
  - [Chips / Tags](#chips--tags) — Line 353
  - [Toggle / Switch](#toggle--switch) — Line 363
  - [Tabs](#tabs) — Line 382
  - [Status Indicators](#status-indicators) — Line 391
- [Motion Map](#motion-map) — Line 400
  - [Easings](#easings) — Line 407
  - [Duration × Easing × Component](#duration--easing--component) — Line 416
  - [Active Press Scale](#active-press-scale) — Line 437
- [Layout Tokens](#layout-tokens) — Line 449
  - [Spacing Scale](#spacing-scale) — Line 461
  - [Density](#density) — Line 465
  - [Responsive Notes](#responsive-notes) — Line 477
- [Accessibility Tokens](#accessibility-tokens) — Line 484
- [Overlays](#overlays) — Line 518
  - [Popover / Dropdown](#popover--dropdown) — Line 522
  - [Modal](#modal) — Line 539
  - [Tooltip](#tooltip) — Line 553
  - [Command Palette / Search Overlay](#command-palette--search-overlay) — Line 564
- [Visual Style](#visual-style) — Line 576
  - [Material](#material) — Line 580
  - [Hard Directional Lighting](#hard-directional-lighting) — Line 608
  - [Data Visualization Philosophy](#data-visualization-philosophy) — Line 619
- [Signature Animations](#signature-animations) — Line 630
  - [1. Pneumatic Actuator Press](#1-pneumatic-actuator-press) — Line 632
  - [2. Gauge Fill](#2-gauge-fill) — Line 654
  - [3. Alarm Pulse](#3-alarm-pulse) — Line 680
  - [4. Panel Slide (Pneumatic Door)](#4-panel-slide-pneumatic-door) — Line 707
  - [5. KPI Number Snap](#5-kpi-number-snap) — Line 742
  - [6. Stagger Load (Equipment Grid)](#6-stagger-load-equipment-grid) — Line 769
- [Dark Mode Variant](#dark-mode-variant) — Line 806
  - [Dark Mode Palette](#dark-mode-palette) — Line 811
  - [Dark Mode Special Tokens](#dark-mode-special-tokens) — Line 830
  - [Dark Mode Rules](#dark-mode-rules) — Line 840
- [Mobile Notes](#mobile-notes) — Line 855
  - [Effects to Disable](#effects-to-disable) — Line 857
  - [Adjustments](#adjustments) — Line 863
  - [Performance Notes](#performance-notes) — Line 878
- [Implementation Checklist](#implementation-checklist) — Line 889

---

## 15. Sunlit Concrete

> Industrial daylight rendered as interface — where safety colors carry meaning, condensed type carries density, and every readout is visible from across the room.

**Best for:** Manufacturing dashboards, factory control rooms, SCADA/HMI interfaces, industrial IoT monitoring, safety compliance panels, warehouse management, fleet operations, equipment health dashboards, supply chain logistics, energy grid monitoring, building management systems, construction project trackers.

---

### Identity & Philosophy

This theme lives in the world of a factory control room flooded with natural light. Skylights cut rectangles of sun across poured concrete floors. Steel catwalks run overhead. OSHA-orange safety labels are bolted to every panel. Large metric readouts — the kind you can read from thirty feet away — display throughput, temperature, pressure, uptime. The light is hard and directional: overhead fluorescents supplemented by skylights that throw sharp shadows downward. Everything here is functional. Nothing is decorative. If something has color, it is because color saves lives.

The core visual tension: **industrial weight vs. daylight clarity**. The palette is concrete grey — warm, sunlit, with visible aggregate texture — but the interface is flooded with light, not buried in darkness. This is not a dark terminal. This is a bright, physical workspace where you stand, not sit. Where readouts are BIG because the operator is twenty feet away. Where orange means "pay attention" and red means "stop the line."

The signature element is the **large-format KPI readout**. Numbers are enormous — Barlow Condensed at 48-72px, condensed and heavy, like the seven-segment displays bolted to factory walls. These numbers dominate the screen. They are the reason the interface exists. Everything else — labels, navigation, controls — serves the numbers.

Safety color semantics are not decorative. They follow OSHA/ANSI standards:
- **Orange** = caution, potential hazard, attention required
- **Red** = danger, stop, critical alarm, immediate action
- **Green** = operational, safe, within tolerance, go
- **Yellow/Amber** = warning, approaching threshold
- **Steel blue** = informational, interactive, navigational (the non-safety color)

**Decision principle:** "When in doubt, ask: can the operator read this from across the room? If it's too small, too subtle, or too decorative, it doesn't belong on the factory floor."

**What this theme is NOT:**
- Not dark — this is a daylight theme; the base surface is light concrete grey, not charcoal or black
- Not delicate — no hairline borders, no whisper-thin type, no subtle shadows; everything is built to be read at distance
- Not decorative — no gradients, no ornamental elements, no rounded pill shapes; corners are functional (small radius, not zero, not pill)
- Not minimal — this is a dense, information-rich theme; whitespace exists for readability, not aesthetics
- Not cool-toned — concrete is warm; the grey has yellow-ochre undertone, not blue
- Not a consumer product — this is industrial software; it looks like it controls real equipment because it does
- Not small — KPI readouts are the largest text in any theme in the roster; condensed type at massive scale is the identity

---

### Color System

#### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Raw Concrete | `#E8E3DB` | L=0.91 C=0.012 h=80 | Deepest background. Warm concrete grey with visible yellow undertone. The factory floor. |
| bg | Sealed Concrete | `#F0ECE5` | L=0.94 C=0.011 h=80 | Primary surface. One step lighter — sealed concrete with a matte finish. |
| surface | Daylit Panel | `#F8F5F0` | L=0.97 C=0.008 h=80 | Elevated cards, inputs, control panels. Near-white with warm tint. The painted steel panel. |
| recessed | Shadow Concrete | `#D9D3C9` | L=0.85 C=0.015 h=80 | Code blocks, inset gauges, recessed meter wells. Concrete in shadow. |
| active | Pressed Slab | `#CFC8BC` | L=0.82 C=0.018 h=80 | Active/pressed items, selected rows. Concrete under the weight of a boot print. |
| text-primary | Shop Floor Black | `#2C2A26` | L=0.22 C=0.010 h=80 | Headings, body text, KPI readouts. Near-black with warm undertone. Stencil ink. |
| text-secondary | Worn Stencil | `#5C5850` | L=0.41 C=0.012 h=80 | Sidebar items, secondary labels, supporting text. Faded stencil marking. |
| text-muted | Dust Grey | `#8A857C` | L=0.58 C=0.014 h=80 | Placeholders, timestamps, metadata. Concrete dust color. |
| text-onAccent | Safety White | `#FFFFFF` | L=1.0 C=0 h=0 | Text on orange/red/green accent backgrounds. Pure white for maximum contrast on safety colors. |
| border-base | Rebar Seam | `#9E9890` | L=0.64 C=0.012 h=80 | Used at variable opacity. The color of exposed rebar and concrete form seams. |
| accent-primary | Steel Blue | `#4A7FA5` | L=0.56 C=0.08 h=240 | Interactive elements, links, navigation highlights, informational states. The blue of control panel buttons. |
| accent-secondary | OSHA Orange | `#E8651A` | L=0.60 C=0.18 h=55 | Caution states, attention badges, highlighted KPIs, the signature safety color. |
| success | Operational Green | `#3D8B37` | L=0.52 C=0.12 h=142 | System operational, within tolerance, go status. ANSI safety green. |
| warning | Threshold Amber | `#D4940A` | L=0.67 C=0.15 h=85 | Approaching threshold, warning state. Industrial amber. |
| danger | Stop Red | `#CC2936` | L=0.45 C=0.17 h=25 | Critical alarm, stop the line, immediate action. ANSI safety red. |
| info | Steel Blue | `#4A7FA5` | L=0.56 C=0.08 h=240 | Informational states. Same as accent-primary — blue is the informational color. |

#### Special Tokens

| Token | Value | Role |
|---|---|---|
| inlineCode | `#B85A18` | Code text within prose. Darkened orange — reads as "data" in the safety color family. |
| toggleActive | `#3D8B37` | Toggle/switch active track. Operational green — toggle ON means "operational." |
| selection | `rgba(74,127,165,0.22)` | `::selection` background. Steel blue at 22%. |
| kpiHighlight | `#E8651A` | Background tint for highlighted KPI readouts. OSHA orange. |
| kpiCritical | `#CC2936` | Background tint for critical KPI readouts. Stop red. |

#### Opacity System

Border opacity (on `border-base`):

| Context | Opacity | Usage |
|---|---|---|
| subtle | 12% | Internal dividers, grid rules, hairline separators within panels. |
| card | 22% | Card-level borders, panel edges, input borders at rest. Visible from distance. |
| hover | 35% | Hovered elements, interactive feedback borders. Clear state change. |
| focus | 50% | Focused elements. High-contrast border for keyboard navigation. |
| heavy | 60% | Major section dividers, header underlines, emphasis borders. |

#### Color Rules

- Safety colors are NEVER decorative. Orange means caution. Red means danger. Green means operational. Using these colors for branding, decoration, or aesthetics violates the theme's identity.
- Steel blue is the ONLY non-safety color. It marks interactive elements and informational states. Everything else is concrete grey or a safety color.
- KPI readouts are the color priority. If a number is normal, it is `text-primary` (black on concrete). If it approaches a threshold, it gains an amber indicator. If it exceeds threshold, it gains orange background. If it is critical, it gains red background. Color escalation follows the real-world alarm ladder.
- No gradients. Flat fills only. Factory signage doesn't gradient.
- The concrete grey palette has a consistent warm yellow undertone (hue ~80 in OKLCH). Cool greys are prohibited — they break the sunlit-concrete materiality.
- White (`#FFFFFF`) is reserved for text-on-safety-color and for the `surface` token. It is not used as a decorative background color.

---

### Typography Matrix

The typography system uses three families with distinct roles. Barlow Condensed is the industrial display face — condensed, dense, designed for large-format readouts where horizontal space is at a premium. Barlow (regular width) is the body workhorse — readable, neutral, industrial without being harsh. IBM Plex Mono handles data, code, and tabular values.

The defining typographic choice: **KPI readouts use Barlow Condensed at 48-72px**. These are the seven-segment-display equivalent in web type. Condensed letterforms allow enormous point sizes in tight horizontal spaces. The numbers are the interface.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| KPI Display | Barlow Condensed | 56px | 700 | 1.0 | -0.02em | `font-variant-numeric: tabular-nums` | Large metric readouts, primary KPIs, the hero numbers. Visible from across the room. |
| Display | Barlow Condensed | 28px | 600 | 1.15 | -0.01em | — | Page titles, section heroes, panel headers. Condensed for density. |
| Heading | Barlow Condensed | 18px | 600 | 1.25 | 0.01em | `text-transform: uppercase` | Section titles, card headers, group labels. ALL CAPS stencil treatment. |
| Body | Barlow | 15px | 400 | 1.55 | normal | — | Primary reading text, descriptions, instructions. Regular-width Barlow for readability. |
| Body Small | Barlow | 13px | 400 | 1.45 | normal | — | Sidebar items, form labels, secondary UI text, dense lists. |
| Button | Barlow | 14px | 600 | 1.4 | 0.03em | `text-transform: uppercase` | Button labels. Uppercase, semi-bold, clear action text. |
| Input | Barlow | 14px | 400 | 1.4 | normal | — | Form input text, search fields, command entry. |
| Label | Barlow Condensed | 11px | 500 | 1.3 | 0.06em | `text-transform: uppercase` | Metadata, timestamps, axis labels, gauge labels, unit indicators. ALL CAPS condensed. |
| Code | IBM Plex Mono | 13px | 400 | 1.55 | normal | `font-feature-settings: "zero", "tnum"` | Inline code, serial numbers, equipment IDs, log output. |
| Caption | Barlow | 11px | 400 | 1.33 | normal | — | Disclaimers, footnotes, compliance text, fine print. |
| KPI Unit | Barlow Condensed | 18px | 500 | 1.0 | 0.02em | `text-transform: uppercase` | Unit labels paired with KPI display (e.g., "PSI", "RPM", "°C"). Smaller than the number, same condensed family. |

**Typographic decisions:**
- Barlow Condensed is the **display and label** font. It appears at two extremes: very large (KPI readouts, 48-72px) and very small (labels, 11px). In both cases, the condensed width allows high information density.
- Barlow (regular) is the **body and interaction** font. It is the readable, everyday workhorse. Not condensed — comfortable for paragraph reading and form interaction.
- IBM Plex Mono is the **data** font. Equipment serial numbers, log entries, code snippets, anything that is machine-generated data.
- The KPI Display role is unique to this theme. No other theme has a role this large. The 56px default can scale to 72px for hero metrics or down to 40px for secondary KPIs.
- `tabular-nums` is mandatory on all numeric displays for column alignment in data tables and metric grids.
- `font-smoothing: antialiased` always — especially important for condensed type at large sizes on light backgrounds.
- `text-wrap: balance` for headings, `auto` for body text.

#### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
```

---

### Elevation System

**Strategy:** `hard-shadows` (directional overhead lighting)

This theme simulates hard overhead factory lighting — skylights and fluorescent panels casting sharp, directional shadows straight down. Shadows have minimal blur, sharp edges, and a warm-grey tone. They simulate physical objects sitting on a concrete surface under bright, flat overhead light. The shadow direction is always top-to-bottom (positive Y offset only). No ambient glow. No diffuse haze. Hard light, hard shadows.

#### Surface Hierarchy

| Surface | Background | Shadow | Usage |
|---|---|---|---|
| page | `#E8E3DB` (raw concrete) | none | Main page canvas, sidebar background, the floor |
| bg | `#F0ECE5` (sealed concrete) | none | Primary content area, main panels |
| surface | `#F8F5F0` (daylit panel) | shadow-card | Cards, inputs, control panels, elevated elements |
| recessed | `#D9D3C9` (shadow concrete) | none (inset appearance via darker bg) | Code blocks, gauge wells, inset meter displays |
| active | `#CFC8BC` (pressed slab) | none | Active/pressed items, selected states |
| overlay | `#F8F5F0` (daylit panel) | shadow-popover | Popovers, dropdowns, context menus |

#### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `0 2px 0 rgba(44,42,38,0.08)` | Small elements. Hard 2px drop, zero blur. Like a label plate bolted to a panel. |
| shadow-card | `0 3px 0 rgba(44,42,38,0.10), 0 1px 0 rgba(44,42,38,0.05)` | Cards, control panels at rest. Hard directional shadow, 3px drop. |
| shadow-card-hover | `0 4px 1px rgba(44,42,38,0.12), 0 1px 0 rgba(44,42,38,0.06)` | Card hover — shadow extends 1px deeper, minimal blur introduced. Panel lifting slightly. |
| shadow-input | `0 2px 0 rgba(44,42,38,0.06), 0 0 0 1px rgba(158,152,144,0.22)` | Input rest. Hard 2px drop + 1px ring at card border opacity. |
| shadow-input-hover | `0 2px 0 rgba(44,42,38,0.08), 0 0 0 1px rgba(158,152,144,0.35)` | Input hover. Ring brightens to hover opacity. |
| shadow-input-focus | `0 2px 0 rgba(44,42,38,0.08), 0 0 0 2px rgba(74,127,165,0.50)` | Input focus. Steel blue focus ring replaces border. |
| shadow-popover | `0 6px 1px rgba(44,42,38,0.15), 0 2px 0 rgba(44,42,38,0.08)` | Popovers, dropdowns. Heaviest shadow — highest elevation. Still mostly hard (1px blur). |
| shadow-kpi | `0 4px 0 rgba(44,42,38,0.12)` | KPI readout cards. Extra-hard shadow, zero blur. These panels jut out from the wall. |
| shadow-none | `none` | Recessed surfaces, page-level elements. |

#### Separation Recipe

Hard directional shadows from overhead lighting + concrete tint-stepping. Each surface level gets progressively lighter (raw concrete → sealed concrete → daylit panel). Shadows drop straight down with near-zero blur, simulating objects bolted to a concrete wall under fluorescent/skylight illumination. Cards and panels cast sharp downward shadows onto the concrete page surface. Borders reinforce separation at card and hover levels. No backdrop blur on any surface — everything is opaque and physical. The recessed surface (gauge wells, code blocks) uses a darker concrete tone to simulate shadow/recess without needing inset shadows.

---

### Border System

Border radius uses small, functional values — not zero (too brutalist), not pill-shaped (too soft). The radii suggest machined metal edges: precise, slightly eased, industrial.

#### Radius Tokens

| Token | Value | Usage |
|---|---|---|
| none | 0px | Never used as default. Explicit zero only for specific elements (progress bars, linear gauges). |
| sm | 3px | Chips, tags, small badges, inline indicators. Machined edge. |
| md | 4px | Buttons, inputs, sidebar items. Standard control radius. |
| lg | 6px | Cards, panels, KPI readout containers. Panel edge. |
| xl | 8px | Popovers, dropdowns, modals. Largest standard radius. |
| input | 4px | Form inputs. Matches button radius for visual consistency. |
| full | 9999px | Status LEDs only. The one element that is truly round. |

#### Widths and Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| subtle | 1px | `border-base` at 12% | Internal dividers within cards, table row separators. |
| card | 1px | `border-base` at 22% | Card borders, panel edges, input borders at rest. |
| hover | 1px | `border-base` at 35% | Hovered elements. Clear visual feedback. |
| heavy | 2px | `border-base` at 60% | Major section dividers, header underlines, emphasis borders. |
| input | 1px | `border-base` at 22% | Form input borders at rest. Same weight as card. |
| input-hover | 1px | `border-base` at 35% | Input hover. Border brightens to hover opacity. |
| input-focus | 2px | `accent-primary` at 100% | Input focus. Full steel blue, heavier weight. |
| safety-left | 3px | safety color at 100% | Left-border accent on alarm items, safety callouts. 3px for visibility. |
| kpi-accent | 3px | `accent-secondary` (OSHA orange) at 100% | Bottom border on highlighted KPI cards. Orange stripe. |

#### Focus Ring

- **Color:** `rgba(74, 127, 165, 0.56)` (steel blue at 56%)
- **Width:** 2px solid
- **Offset:** 2px
- **Implementation:** `outline: 2px solid rgba(74,127,165,0.56); outline-offset: 2px;`
- **On safety-colored backgrounds:** Focus ring uses `rgba(255,255,255,0.70)` (white) to maintain visibility against orange/red/green.
- **Keyboard-only:** Use `:focus-visible` to show ring only on keyboard navigation, not mouse click.

---

### Component States

All transitions use the **pneumatic** easing curve: `cubic-bezier(0.7, 0, 0.3, 1)`. This produces sharp starts and hard stops — like a pneumatic actuator or hydraulic piston. Things move with industrial force: no gentle ramp-up, no soft landing. The motion arrives and stops.

For micro-interactions (hover, border changes), durations are 100-150ms. For larger movements (panel reveals, modal entry), 200-250ms. Everything is fast and decisive — this is a control room, not a meditation app.

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `accent-primary` (`#4A7FA5`), border none, color `text-onAccent` (white), radius md (4px), h 36px, padding `0 16px`, font button (Barlow 14px/600 uppercase), shadow shadow-sm |
| Hover | bg `#3D6E91` (steel blue darkened 12%), shadow shadow-card, transition 120ms pneumatic |
| Active | bg `#335E7D` (steel blue darkened 22%), shadow shadow-sm (shadow retracts), transform `translateY(1px)` (button presses down) |
| Focus | outline focus ring (`2px solid rgba(74,127,165,0.56)`, offset 2px) |
| Disabled | opacity 0.4, pointer-events none, cursor not-allowed, shadow none, bg desaturated to `#7A9AAF` |
| Transition | `background-color 120ms cubic-bezier(0.7, 0, 0.3, 1), box-shadow 120ms cubic-bezier(0.7, 0, 0.3, 1), transform 80ms cubic-bezier(0.7, 0, 0.3, 1)` |

#### Buttons (Safety/Danger)

| State | Properties |
|---|---|
| Rest | bg `danger` (`#CC2936`), border none, color white, radius md, h 36px, padding `0 16px`, font button, shadow shadow-sm |
| Hover | bg `#B8232F` (red darkened), shadow shadow-card |
| Active | bg `#A01E28`, shadow shadow-sm, transform `translateY(1px)` |
| Focus | outline `2px solid rgba(255,255,255,0.70)`, offset 2px (white ring on red bg) |
| Disabled | opacity 0.4, pointer-events none |
| Transition | Same as primary button |

#### Buttons (Ghost)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid border-base at 22%`, color `text-secondary`, radius md (4px), h 36px, padding `0 14px`, font button |
| Hover | bg `recessed` (`#D9D3C9`), border at 35%, color `text-primary`, transition 120ms pneumatic |
| Active | bg `active` (`#CFC8BC`), transform `translateY(1px)` |
| Focus | outline focus ring |
| Disabled | opacity 0.4, pointer-events none |
| Transition | `all 120ms cubic-bezier(0.7, 0, 0.3, 1)` |

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `surface` (`#F8F5F0`), border `1px solid border-base at 22%`, radius md (4px), h 40px, padding `0 12px`, font input (Barlow 14px/400), color `text-primary`, placeholder `text-muted` (`#8A857C`), caret-color `accent-primary`, shadow shadow-input |
| Hover | border at 35% opacity, shadow shadow-input-hover, transition 100ms pneumatic |
| Focus | border `2px solid accent-primary`, shadow shadow-input-focus, outline none |
| Error | border `2px solid danger` (`#CC2936`), shadow `0 2px 0 rgba(204,41,54,0.08), 0 0 0 2px rgba(204,41,54,0.20)` |
| Disabled | opacity 0.4, pointer-events none, bg `bg` (`#F0ECE5`), cursor not-allowed |
| Transition | `border-color 100ms cubic-bezier(0.7, 0, 0.3, 1), box-shadow 100ms cubic-bezier(0.7, 0, 0.3, 1)` |

#### KPI Readout Card

The signature component. A large metric display card with the number as hero element.

| State | Properties |
|---|---|
| Rest | bg `surface`, border `1px solid border-base at 22%`, radius lg (6px), shadow shadow-kpi, padding `16px 20px` |
| Normal value | Number in `text-primary`, label in `text-muted`, no accent color |
| Warning threshold | Number in `warning` (`#D4940A`), left border `3px solid warning`, label gains amber dot indicator |
| Caution state | Number in `text-primary`, bg tinted with `rgba(232,101,26,0.06)` (faint orange wash), bottom border `3px solid accent-secondary` (OSHA orange) |
| Critical alarm | Number in `danger` (`#CC2936`), bg tinted with `rgba(204,41,54,0.06)` (faint red wash), full border `2px solid danger`, shadow gains red tint: `0 4px 0 rgba(204,41,54,0.15)` |
| Hover | shadow shadow-card-hover, transition 150ms pneumatic |
| Transition | `box-shadow 150ms cubic-bezier(0.7, 0, 0.3, 1), border-color 100ms cubic-bezier(0.7, 0, 0.3, 1), background-color 200ms cubic-bezier(0.7, 0, 0.3, 1)` |

**KPI Card anatomy:**
```
┌─────────────────────────────┐
│  LABEL (Barlow Condensed 11px uppercase, text-muted)
│
│  1,247.3  PSI               │  ← KPI Display (56px) + Unit (18px)
│  ▲ +12.4% from last hour    │  ← Delta (Body Small 13px, success green if positive)
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬░░░░░      │  ← Optional: threshold bar (progress toward limit)
└─────────────────────────────┘
```

#### Cards (Standard)

| State | Properties |
|---|---|
| Rest | bg `surface` (`#F8F5F0`), border `1px solid border-base at 22%`, radius lg (6px), shadow shadow-card, padding `16px` |
| Hover | border at 35%, shadow shadow-card-hover, transition 150ms pneumatic |
| Active/Selected | border `1px solid accent-primary at 60%`, bg `surface` (unchanged), shadow shadow-card |
| Transition | `border-color 150ms cubic-bezier(0.7, 0, 0.3, 1), box-shadow 150ms cubic-bezier(0.7, 0, 0.3, 1)` |

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `text-secondary` (`#5C5850`), radius md (4px), h 34px, padding `6px 12px`, font bodySmall (Barlow 13px/400) |
| Hover | bg `recessed` (`#D9D3C9`), color `text-primary`, transition 100ms pneumatic |
| Active (current) | bg `active` (`#CFC8BC`), color `text-primary`, font-weight 600, border-left `3px solid accent-primary`, padding-left 9px (compensate border) |
| Active hover | bg `active` darkened 3% (`#C7C0B4`), color `text-primary` |
| Transition | `all 100ms cubic-bezier(0.7, 0, 0.3, 1)` |

#### Chips / Tags

| State | Properties |
|---|---|
| Rest | bg `bg` (`#F0ECE5`), border `1px solid border-base at 12%`, radius sm (3px), h 26px, padding `0 8px`, font label (Barlow Condensed 11px/500 uppercase), color `text-secondary` |
| Hover | bg `recessed`, border at 22%, color `text-primary`, transition 100ms pneumatic |
| Active/selected | bg `accent-primary` (`#4A7FA5`), color white, border `accent-primary` |
| Safety chip (warning) | bg `rgba(212,148,10,0.12)`, color `#9A7008`, border `1px solid rgba(212,148,10,0.30)` |
| Safety chip (danger) | bg `rgba(204,41,54,0.10)`, color `#CC2936`, border `1px solid rgba(204,41,54,0.25)` |
| Safety chip (success) | bg `rgba(61,139,55,0.10)`, color `#3D8B37`, border `1px solid rgba(61,139,55,0.25)` |
| Transition | `all 100ms cubic-bezier(0.7, 0, 0.3, 1)` |

#### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 40px |
| Track height | 22px |
| Track radius | full (9999px) — the only round element in the theme, representing a physical toggle switch |
| Track off bg | `recessed` (`#D9D3C9`) |
| Track off border | `1px solid border-base at 22%` |
| Track on bg | `success` (`#3D8B37`) — toggle ON = operational/active = green |
| Track on border | none |
| Thumb | 16px circle, bg `#FFFFFF`, radius full |
| Thumb off position | left 3px |
| Thumb on position | right 3px |
| Thumb shadow | `0 1px 2px rgba(44,42,38,0.15)` — small hard shadow on the toggle knob |
| Transition | `all 150ms cubic-bezier(0.7, 0, 0.3, 1)` — pneumatic snap |
| Focus-visible | focus ring around entire track |

#### Tabs

| State | Properties |
|---|---|
| Rest | bg transparent, color `text-muted`, radius none, h 36px, padding `0 14px`, font bodySmall (Barlow 13px/400), border-bottom `2px solid transparent` |
| Hover | color `text-secondary`, border-bottom `2px solid border-base at 22%`, transition 100ms pneumatic |
| Active | color `text-primary`, font-weight 600, border-bottom `3px solid accent-primary` |
| Transition | `all 100ms cubic-bezier(0.7, 0, 0.3, 1)` |

#### Status Indicators

| Variant | Properties |
|---|---|
| Operational | 8px circle, bg `success` (`#3D8B37`), radius full, shadow `0 0 0 2px rgba(61,139,55,0.20)` |
| Warning | 8px circle, bg `warning` (`#D4940A`), radius full, pulsing (led-pulse animation) |
| Critical | 8px circle, bg `danger` (`#CC2936`), radius full, fast pulse (alarm-pulse animation, 800ms) |
| Offline | 8px circle, bg `text-muted` (`#8A857C`), radius full, no animation |
| Info | 8px circle, bg `accent-primary` (`#4A7FA5`), radius full, no animation |

---

### Motion Map

**Core philosophy:** Pneumatic motion. Every transition uses a sharp, industrial easing curve — `cubic-bezier(0.7, 0, 0.3, 1)` — that simulates pneumatic actuators. Things start moving immediately (no gentle ramp-up) and stop hard (no soft landing). The feel is hydraulic: pistons, not springs. Levers, not rubber bands. Durations are short (100-250ms) because operators need instant feedback. Nothing lingers. Nothing bounces.

#### Easings

| Name | Value | Character |
|---|---|---|
| pneumatic | `cubic-bezier(0.7, 0, 0.3, 1)` | The primary easing. Sharp attack, hard stop. Like a pneumatic piston reaching end of stroke. |
| mechanical | `linear` | Constant velocity. For progress bars, gauge fills, loading indicators. Machines move at constant speed. |
| brake | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | Out-cubic. For larger panel movements where pure pneumatic feels too abrupt. Still hard stop, gentler start. |
| instant | `steps(1)` | Single-frame snap. For alarm state changes — critical status appears immediately, no transition. |

#### Duration × Easing × Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Button hover bg | 120ms | pneumatic | Fast, decisive color shift. Operator knows they're on a control. |
| Button active press | 80ms | pneumatic | Faster than hover. The press is quicker than the approach. |
| Sidebar item hover | 100ms | pneumatic | Background and color change together. Quick identification. |
| Chip hover/select | 100ms | pneumatic | State change with authority. |
| Toggle thumb slide | 150ms | pneumatic | Thumb snaps to position. No spring, no overshoot. Piston. |
| Input focus border | 100ms | pneumatic | Border snaps to steel blue. Clear focus indication. |
| Card hover shadow | 150ms | pneumatic | Shadow deepens as card "lifts" under cursor. |
| Tab indicator | 120ms | pneumatic | Active indicator snaps to new tab. |
| Panel open/close | 200ms | brake | Larger movement gets brake easing. Panel slides like a heavy door. |
| Popover entry | 150ms | pneumatic | Quick appearance with authority. |
| Modal entry | 250ms | brake | Largest element gets longest duration. Still fast. |
| Tooltip entry | 80ms | pneumatic | Near-instant. Data tooltip for metric readout. |
| KPI value update | 200ms | pneumatic | Number changes snap in. No counting animation by default. |
| Progress/gauge fill | 300ms | mechanical | Linear fill — like fluid in a gauge. Constant velocity. |
| Alarm state change | 0ms | instant | Critical alerts appear immediately. No transition. Safety first. |

#### Active Press Scale

| Element | Transform | Notes |
|---|---|---|
| Buttons (primary & ghost) | `translateY(1px)` | Buttons press DOWN, not inward. Like pressing a physical button on a panel. |
| Nav items | `translateY(1px)` | Same downward press. |
| Chips | `scale(0.98)` | Slight compression — chip is smaller, press is tighter. |
| Cards (clickable) | `translateY(1px)` | Subtle downward press. |
| Tabs | none | Tabs don't press — they switch. Active state is the indicator border. |

**Note on `translateY` vs `scale`:** This theme uses `translateY(1px)` for most press states instead of `scale()`. Physical buttons on a control panel press DOWN into the surface — they don't shrink. The 1px translation simulates this downward travel.

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 1200px | Main content column. Wider than typical — industrial dashboards need horizontal space for KPI grids. |
| Narrow max-width | 768px | Focused content, forms, single-panel views. |
| Sidebar width | 260px | Fixed sidebar. Equipment navigation, zone selection. |
| Header height | 52px | Top bar. Slightly taller for zone/line indicators and status LEDs. |
| KPI grid gap | 16px | Gap between KPI readout cards. Consistent, visible separation. |
| Spacing unit | 4px | Base grid multiplier. ALL spacing is 4px multiples. |

#### Spacing Scale

4, 8, 12, 16, 20, 24, 32, 48px — 4px-aligned.

#### Density

**Dense.** This is an information-rich industrial dashboard theme.
- 12px internal padding on cards and panels
- 8px gaps between list items
- 16px section spacing
- 34-36px row heights for lists and tables
- 26px chip/tag heights
- 40px input heights (balancing density with touch accessibility)
- KPI cards have more generous padding (16-20px) because the numbers need breathing room at large sizes
- Content is packed but readable — every metric visible at a glance

#### Responsive Notes

- **lg (1024px+):** Full sidebar (260px) + content area. KPI grid at 3-4 columns with `auto-fit, minmax(280px, 1fr)`. Data tables at full width with horizontal scroll for overflow.
- **md (768px):** Sidebar collapses to icon rail (48px) or hides behind hamburger. KPI grid drops to 2 columns. KPI Display font size reduces from 56px to 40px.
- **sm (640px):** Single column. Sidebar becomes overlay (200ms brake easing slide-in). KPI grid at 1 column, full width. KPI Display font size reduces to 36px. Tables switch to stacked card layout. Touch targets expand to 44px minimum. Header compresses: zone name truncates, non-critical status indicators hide.

---

### Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring color | `rgba(74, 127, 165, 0.56)` (steel blue) |
| Focus ring on safety bg | `rgba(255, 255, 255, 0.70)` (white — for elements on orange/red/green backgrounds) |
| Focus ring width | 2px solid |
| Focus ring offset | 2px |
| Disabled opacity | 0.4 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled shadow | none |
| Selection bg | `rgba(74,127,165,0.22)` (steel blue at 22%) |
| Selection color | `#2C2A26` (text-primary) |
| Scrollbar width | thin |
| Scrollbar thumb | `rgba(158,152,144,0.30)` (border-base at 30%) |
| Scrollbar track | `rgba(158,152,144,0.06)` (barely visible track on concrete bg) |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text/UI components) |

**Contrast notes:** `text-primary` (`#2C2A26`) on `page` (`#E8E3DB`) = 9.8:1 (exceeds AAA). `text-secondary` (`#5C5850`) on `page` = 4.7:1 (passes AA). `text-muted` (`#8A857C`) on `page` = 3.1:1 (passes AA for large text, use at 15px+ or as supplementary label only). `accent-primary` (`#4A7FA5`) on `surface` (`#F8F5F0`) = 4.1:1 (passes AA for large text; use as clickable text at 14px+ with underline). White on `accent-secondary` (`#E8651A`) = 3.8:1 (passes AA for large text — KPI labels on orange use bold 14px+). White on `danger` (`#CC2936`) = 5.5:1 (passes AA).

**Reduced motion:** All transitions collapse to `0ms`. Pneumatic actuator animation stops. Gauge fill becomes instant. Alarm pulse becomes static indicator. Progress bars snap to final value. `prefers-reduced-motion: reduce` triggers:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0ms !important;
    animation-duration: 0ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

---

### Overlays

#### Popover / Dropdown

- **bg:** `surface` token (`#F8F5F0`)
- **backdrop-filter:** none (opaque panels — factory control menus are solid, not frosted glass)
- **border:** `1px solid border-base at 35%` (hover-weight border — popovers are elevated, need clear edge)
- **radius:** xl (8px)
- **shadow:** shadow-popover (`0 6px 1px rgba(44,42,38,0.15), 0 2px 0 rgba(44,42,38,0.08)`)
- **padding:** 4px
- **z-index:** 50
- **min-width:** 200px, **max-width:** 320px
- **Menu item:** 6px 10px padding, radius md (4px), h 34px, font bodySmall (Barlow 13px/400), color `text-secondary`
- **Menu item hover:** bg `recessed` (`#D9D3C9`), color `text-primary`, transition 100ms pneumatic
- **Menu item danger:** color `danger` (`#CC2936`), hover bg `rgba(204,41,54,0.08)`
- **Divider:** `1px solid border-base at 12%`, margin `4px 0`
- **Entry:** opacity 0→1 + translateY(-4px)→translateY(0), 150ms pneumatic
- **Exit:** opacity 1→0, 100ms pneumatic

#### Modal

- **Overlay bg:** `rgba(44, 42, 38, 0.55)` (warm concrete overlay, not pure black)
- **Overlay backdrop-filter:** `blur(4px)` — slight blur, like looking through a safety glass panel
- **Content bg:** `surface` token (`#F8F5F0`)
- **Content border:** `1px solid border-base at 35%`
- **Content radius:** xl (8px)
- **Content shadow:** shadow-popover
- **Content padding:** 24px
- **Content max-width:** 560px
- **Entry:** opacity 0→1 + scale(0.97)→scale(1), 250ms brake easing
- **Exit:** opacity 1→0, 150ms pneumatic
- **Close button:** Ghost button, top-right, 32x32px, contains X icon

#### Tooltip

- **bg:** `active` token (`#CFC8BC`)
- **color:** `text-primary` (`#2C2A26`)
- **font:** label (Barlow Condensed 11px/500 uppercase)
- **border:** `1px solid border-base at 22%`
- **radius:** sm (3px)
- **padding:** 4px 8px
- **shadow:** shadow-sm (`0 2px 0 rgba(44,42,38,0.08)`)
- **No arrow.** Position via offset. Appears with 80ms pneumatic fade.
- **Max-width:** 260px. Text wraps if needed.

#### Command Palette / Search Overlay

- **bg:** `surface` (`#F8F5F0`)
- **border:** `2px solid border-base at 35%`
- **radius:** xl (8px)
- **shadow:** shadow-popover
- **Input:** full-width text input at top, 48px height, Barlow 16px/400, no border (integrated into palette)
- **Results list:** below input, separated by `1px solid border-base at 12%`
- **Result item:** 36px height, bodySmall font, icon + text layout
- **Result hover:** bg `recessed`, transition 100ms pneumatic

---

### Visual Style

#### Material

- **Concrete grain:** Subtle noise texture via SVG feTurbulence at 3% opacity on light backgrounds. Coarser frequency than paper grain — this is poured concrete with visible aggregate. Applied to `page` surface only.

```html
<svg width="0" height="0" style="position:absolute">
  <filter id="concrete-noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="4" stitchTiles="stitch" />
    <feColorMatrix type="saturate" values="0" />
  </filter>
</svg>
```
```css
.concrete-grain {
  position: fixed;
  inset: 0;
  opacity: 0.03;
  filter: url(#concrete-noise);
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: multiply;
}
```

- **Gloss:** Matte. Zero sheen. Concrete is matte. Steel panels are matte powder-coated. The only reflective element is the toggle switch thumb (white with a small shadow).
- **Blend mode:** Normal everywhere except grain overlay (multiply).
- **Shader bg:** False. No WebGL, no canvas backgrounds. This is a functional interface, not a demo.

#### Hard Directional Lighting

The defining visual characteristic: all shadows cast straight down, simulating overhead factory lighting (skylights + fluorescents). This creates a consistent "lit from above" appearance across every element:
- Shadow Y-offset is always positive (downward)
- Shadow X-offset is always 0 (light is directly overhead)
- Shadow blur is minimal (0-1px) — hard light = hard edges
- Shadow color uses the warm concrete dark tone (`rgba(44,42,38,...)`) at low opacity

This lighting model means the **top edges of elements are brighter** (catching light) and **bottom edges are in shadow**. Cards and panels should have a slight top highlight (via lighter top border or inset box-shadow `inset 0 1px 0 rgba(255,255,255,0.15)`) to reinforce the overhead lighting.

#### Data Visualization Philosophy

Safety-color-aware with concrete-neutral defaults:

- **YES:** Large KPI readouts (the hero element), gauge meters (linear or radial), bar charts (concrete grey bars, safety-colored thresholds), line charts (steel blue lines, red/orange threshold lines), heatmaps (grey→orange→red gradient for temperature/severity), sparklines (inline with KPI readouts).
- **NO:** Pie charts, donut charts, multi-color scatter plots, 3D charts, decorative area fills, rainbow gradients.
- **Color rule:** Charts default to `text-secondary` grey for data. Threshold lines use safety colors (green for normal range, amber for warning zone, red for danger zone). Interactive elements use steel blue. Never more than 3 colors in a single chart.
- **Grid:** Low-ink. Chart grid lines at `border-base at 8%`. Axis labels in Label font (Barlow Condensed 11px uppercase).
- **Number format:** Tabular numerals everywhere. Barlow Condensed for large numbers, IBM Plex Mono for small/tabular numbers. Thousands separators (commas). Fixed decimal places per metric.

---

### Signature Animations

#### 1. Pneumatic Actuator Press

The universal interaction feedback. When a button or control is pressed, it translates downward 1px and its shadow retracts — simulating a physical button being pushed into a control panel. On release, the button returns to rest position and the shadow extends again. The motion is sharp: no bounce, no overshoot, pure mechanical travel.

- **Technique:** `transform: translateY()` + `box-shadow` change on `:active`
- **Duration:** 80ms press, 120ms release
- **Easing:** `cubic-bezier(0.7, 0, 0.3, 1)` (pneumatic)
- **CSS:**
```css
.btn-pneumatic {
  transition: transform 80ms cubic-bezier(0.7, 0, 0.3, 1),
              box-shadow 80ms cubic-bezier(0.7, 0, 0.3, 1);
  box-shadow: 0 3px 0 rgba(44,42,38,0.10), 0 1px 0 rgba(44,42,38,0.05);
}
.btn-pneumatic:active {
  transform: translateY(2px);
  box-shadow: 0 1px 0 rgba(44,42,38,0.08);
  transition-duration: 60ms;
}
```
- **Reduced motion:** Instant state change, no translation. Background color change only.
- **Usage:** All primary and ghost buttons, clickable cards, control panel buttons.

#### 2. Gauge Fill

When a metric value changes or a progress bar loads, it fills with a constant-velocity linear motion — like fluid rising in a sight glass or mercury in a thermometer. No easing. Constant speed from start to finish. The fill color shifts through safety colors as it approaches thresholds (green → amber → red).

- **Technique:** `width` or `height` animation with `linear` easing + color transitions at threshold breakpoints
- **Duration:** 300ms for small changes, 600ms for full-range fills
- **Easing:** `linear` (constant velocity — machines fill at constant rate)
- **CSS:**
```css
@keyframes gauge-fill {
  from { width: var(--gauge-start, 0%); }
  to { width: var(--gauge-end, 100%); }
}
.gauge-bar {
  height: 8px;
  background: var(--gauge-color, var(--success));
  border-radius: 0;
  animation: gauge-fill 300ms linear forwards;
}
.gauge-bar[data-level="warning"] { --gauge-color: var(--warning); }
.gauge-bar[data-level="danger"] { --gauge-color: var(--danger); }
```
- **Reduced motion:** Instant fill to target value, no animation.
- **Usage:** Progress bars, threshold gauges, loading indicators, capacity meters.

#### 3. Alarm Pulse

Critical status indicators pulse with a hard, mechanical blink — not a smooth fade. The indicator snaps between full opacity and reduced opacity, like a warning light on a factory floor. Two variants: slow pulse (warning) and fast pulse (critical alarm).

- **Technique:** `opacity` animation with `steps(2)` — binary states, no interpolation
- **Duration:** 1600ms (warning/slow), 800ms (critical/fast)
- **Easing:** `steps(2)` — hard snap between states, like a relay switching a light
- **CSS:**
```css
@keyframes alarm-pulse-slow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.25; }
}
@keyframes alarm-pulse-fast {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.15; }
}
.status-warning {
  animation: alarm-pulse-slow 1600ms steps(2) infinite;
}
.status-critical {
  animation: alarm-pulse-fast 800ms steps(2) infinite;
}
```
- **Reduced motion:** Static indicator at full opacity. No blink. Rely on color alone for state communication.
- **Usage:** Status LEDs, alarm indicators, system health badges, equipment fault icons.

#### 4. Panel Slide (Pneumatic Door)

Panels, drawers, and sidebars open with pneumatic authority — they move at constant velocity with a sharp deceleration at the end, like a hydraulic door reaching its stop. No bounce, no overshoot. The panel simply arrives. A subtle shadow appears as the panel reaches full extension.

- **Technique:** `transform: translateX()` with brake easing
- **Duration:** 200ms open, 150ms close
- **Easing:** `cubic-bezier(0.0, 0.0, 0.2, 1.0)` (brake — out-cubic)
- **CSS:**
```css
@keyframes panel-open {
  from {
    transform: translateX(-100%);
    box-shadow: none;
  }
  to {
    transform: translateX(0);
    box-shadow: 6px 0 1px rgba(44,42,38,0.10);
  }
}
@keyframes panel-close {
  from {
    transform: translateX(0);
    box-shadow: 6px 0 1px rgba(44,42,38,0.10);
  }
  to {
    transform: translateX(-100%);
    box-shadow: none;
  }
}
.panel-enter { animation: panel-open 200ms cubic-bezier(0.0, 0.0, 0.2, 1.0) forwards; }
.panel-exit { animation: panel-close 150ms cubic-bezier(0.7, 0, 0.3, 1) forwards; }
```
- **Reduced motion:** Instant open/close, no slide.
- **Usage:** Sidebar toggle, detail panels, filter drawers, equipment inspection overlays.

#### 5. KPI Number Snap

When a KPI readout value changes, the old number snaps out (opacity 1→0, translateY 0→-8px) and the new number snaps in (opacity 0→1, translateY 8px→0). The transition is fast and mechanical — like a split-flap display or a mechanical counter rolling over. Old value exits upward, new value enters from below.

- **Technique:** Sequential opacity + translateY with pneumatic easing
- **Duration:** 180ms total (90ms exit + 90ms enter)
- **Easing:** `cubic-bezier(0.7, 0, 0.3, 1)` (pneumatic)
- **CSS:**
```css
@keyframes kpi-exit {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-8px); }
}
@keyframes kpi-enter {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
.kpi-value-exit {
  animation: kpi-exit 90ms cubic-bezier(0.7, 0, 0.3, 1) forwards;
}
.kpi-value-enter {
  animation: kpi-enter 90ms cubic-bezier(0.7, 0, 0.3, 1) forwards;
  animation-delay: 90ms;
}
```
- **Reduced motion:** Instant number swap. No animation.
- **Usage:** KPI readout cards, live metric displays, counter components, real-time data updates.

#### 6. Stagger Load (Equipment Grid)

When a grid of KPI cards or equipment status panels loads, they stagger in from top-left to bottom-right with a pneumatic fade+lift. Each card appears 40ms after the previous one. The stagger simulates a control room powering up — systems coming online one by one.

- **Technique:** Staggered `opacity` + `translateY` with pneumatic easing
- **Duration:** 200ms per card, 40ms stagger delay
- **Easing:** `cubic-bezier(0.7, 0, 0.3, 1)` (pneumatic)
- **CSS:**
```css
@keyframes card-power-on {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.kpi-grid > * {
  opacity: 0;
  animation: card-power-on 200ms cubic-bezier(0.7, 0, 0.3, 1) forwards;
}
.kpi-grid > *:nth-child(1) { animation-delay: 0ms; }
.kpi-grid > *:nth-child(2) { animation-delay: 40ms; }
.kpi-grid > *:nth-child(3) { animation-delay: 80ms; }
.kpi-grid > *:nth-child(4) { animation-delay: 120ms; }
.kpi-grid > *:nth-child(5) { animation-delay: 160ms; }
.kpi-grid > *:nth-child(6) { animation-delay: 200ms; }
/* ... etc */
```
- **Reduced motion:** All cards appear simultaneously, no stagger.
- **Usage:** Dashboard initial load, zone view switch, KPI grid refresh, equipment list population.

---

### Dark Mode Variant

The dark variant transforms the sunlit factory floor into a **night shift control room**. The skylights are dark. Overhead fluorescents are the sole light source. Concrete surfaces darken to charcoal. Safety colors intensify against the dark background — they are now the primary light sources in the room. The KPI readouts glow against the darkness like backlit instrument panels.

#### Dark Mode Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Night Concrete | `#1C1B18` | Deepest background. Warm near-black — concrete at night. |
| bg | Dark Slab | `#252420` | Primary surface. One step above page. Sealed concrete under fluorescent light. |
| surface | Control Panel | `#2F2E29` | Elevated cards, inputs, panels. The brushed-steel control panel surface. |
| recessed | Deep Shadow | `#13120F` | Code blocks, inset gauges. The shadow under a catwalk. |
| active | Pressed Dark | `#3A3935` | Active/pressed items. Concrete under load in dim light. |
| text-primary | Fluorescent White | `#E8E4DC` | Headings, body, KPI readouts. Warm off-white, like text under warm fluorescents. |
| text-secondary | Dim Stencil | `rgba(232,228,220,0.65)` | Secondary labels. text-primary at 65%. |
| text-muted | Night Dust | `rgba(232,228,220,0.38)` | Placeholders, metadata. text-primary at 38%. |
| text-onAccent | Safety White | `#FFFFFF` | Text on safety color backgrounds. Pure white. |
| border-base | Night Rebar | `#6E6A62` | Used at variable opacity. Darker rebar tone for dark surfaces. |
| accent-primary | Bright Steel | `#6BA3CC` | Interactive elements. Steel blue lightened for dark background contrast. |
| accent-secondary | Safety Orange | `#F07A2E` | OSHA orange lightened slightly for dark background readability. |
| success | Signal Green | `#5CAF54` | Operational states. Brightened for dark background. |
| warning | Lamp Amber | `#E8A820` | Warning states. Brightened for dark background. |
| danger | Alarm Red | `#E03B47` | Critical states. Brightened for dark background. |
| info | Bright Steel | `#6BA3CC` | Same as accent-primary. |

#### Dark Mode Special Tokens

| Token | Value | Role |
|---|---|---|
| inlineCode | `#F07A2E` | Inline code text. Safety orange on dark. |
| toggleActive | `#5CAF54` | Toggle on = green. Brighter for dark bg. |
| selection | `rgba(107,163,204,0.25)` | Steel blue at 25% on dark. |
| kpiHighlight | `rgba(240,122,46,0.15)` | Faint orange wash on dark KPI cards. |
| kpiCritical | `rgba(224,59,71,0.15)` | Faint red wash on dark KPI cards. |

#### Dark Mode Rules

- All surface tokens darken. Surface hierarchy inverts: higher elevation = slightly lighter (as per standard dark mode).
- Safety colors BRIGHTEN by ~15-20% to maintain contrast on dark backgrounds. They become the primary light sources.
- Shadows shift from warm-grey to near-black: `rgba(0,0,0,0.25)` replaces `rgba(44,42,38,0.10)`. Shadow blur increases slightly (0-1px → 1-2px) because hard shadows are less visible on dark backgrounds.
- Concrete grain overlay changes from `multiply` to `soft-light` blend mode and increases to 4% opacity — grain is less visible on dark surfaces and needs compensation.
- Border opacity values shift down: subtle 8%, card 15%, hover 25%, focus 40% — darker backgrounds need less border weight to achieve the same perceived separation.
- Focus ring maintains same color but shifts to steel blue: `rgba(107,163,204,0.65)`.
- KPI readout cards gain a subtle `inset 0 1px 0 rgba(255,255,255,0.04)` top highlight to reinforce the overhead lighting model on dark surfaces.
- Top highlight on cards/panels: `inset 0 1px 0 rgba(255,255,255,0.03)` — catching the fluorescent light overhead.
- All motion durations remain identical. Dark mode does not change the animation system.
- Typography sizes, weights, and families remain identical. Only colors change.

---

### Mobile Notes

#### Effects to Disable
- Concrete grain SVG filter — disabled on mobile for GPU performance
- Stagger load animation — all cards appear simultaneously (no 40ms delays)
- KPI Number Snap — values appear instantly, no exit/enter animation
- Alarm pulse on non-critical indicators (warning level) — static color only. Critical alarm pulse retained for safety.

#### Adjustments
- Header height: 52px → 48px (slight compression)
- Sidebar: hidden by default, slides in as overlay (200ms brake easing) triggered by hamburger
- KPI Display font size: 56px → 36px (fits single-column mobile layout)
- KPI Unit font size: 18px → 14px
- KPI grid: single column, full width, 12px gap
- Touch targets: all interactive elements maintain 44px minimum tap area. Buttons are already 36px visual height — extend hit area with invisible padding.
- Input heights: 40px (already meets 44px minimum with padding)
- Card padding: 16px → 12px (tighter on mobile)
- Button padding: `0 16px` → `0 12px`
- Toggle size: 40x22px → 44x24px (larger for touch accuracy)
- Data tables: horizontal scroll with sticky first column, or collapse to stacked card layout below 640px
- Status indicators: 8px → 10px circles (slightly larger for mobile visibility)
- Spacing between list items: minimum 8px gap for touch accuracy

#### Performance Notes
- SVG feTurbulence filter is the single most expensive effect — disable first on mobile
- Hard shadows (minimal blur) are cheaper to render than blurred shadows — this theme is inherently GPU-friendly
- Barlow Condensed + Barlow + IBM Plex Mono = 3 font families — preload critical weights (Barlow Condensed 600/700, Barlow 400) to avoid layout shift
- Linear and pneumatic easing curves are computationally cheaper than spring physics — fewer interpolation calculations
- `translateY(1px)` press animations are compositable (GPU layer) — no layout thrashing
- KPI number snap uses `opacity` + `transform` only — compositable, no reflow
- No `backdrop-filter` usage (except slight modal blur) — avoid on mobile entirely if performance is constrained

---

### Implementation Checklist

- [ ] Google Fonts loaded: Barlow Condensed (500, 600, 700) + Barlow (400, 600) + IBM Plex Mono (400)
- [ ] CSS custom properties defined for ALL color tokens (light mode default, dark mode via `data-theme="dark"` or `prefers-color-scheme`)
- [ ] Border-radius tokens applied: 0px none, 3px sm, 4px md, 6px lg, 8px xl, 9999px full (status LEDs only)
- [ ] Shadow tokens defined with hard directional values (minimal blur, positive Y-offset only)
- [ ] Shadow escalation per state: shadow-sm → shadow-card → shadow-card-hover → shadow-popover
- [ ] Border opacity system implemented: 12% subtle, 22% card, 35% hover, 50% focus, 60% heavy
- [ ] Focus ring uses `outline: 2px solid rgba(74,127,165,0.56); outline-offset: 2px` via `:focus-visible`
- [ ] Focus ring on safety-colored backgrounds uses white variant (`rgba(255,255,255,0.70)`)
- [ ] All transitions use pneumatic easing `cubic-bezier(0.7, 0, 0.3, 1)` unless otherwise specified
- [ ] `prefers-reduced-motion` media query: all durations 0ms, all animations paused, alarm pulse becomes static
- [ ] KPI Display role implemented: Barlow Condensed 56px/700, `tabular-nums`, visible from distance
- [ ] KPI Unit role implemented: Barlow Condensed 18px/500 uppercase, paired with KPI Display
- [ ] Heading role uses ALL CAPS via `text-transform: uppercase`
- [ ] Button role uses ALL CAPS via `text-transform: uppercase`
- [ ] Label role uses ALL CAPS via `text-transform: uppercase`
- [ ] IBM Plex Mono used for all code, serial numbers, and tabular data with `font-feature-settings: "zero", "tnum"`
- [ ] `tabular-nums` applied to all numeric displays
- [ ] Safety color semantics enforced: orange=caution, red=danger, green=operational, amber=warning
- [ ] Scrollbar styled: thin, border-base at 30% thumb, 6% track
- [ ] `::selection` styled with steel blue at 22%
- [ ] `::placeholder` color matches `text-muted` token
- [ ] Touch targets >= 44px on all interactive elements (mobile)
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] Concrete grain SVG filter applied on desktop, disabled on mobile
- [ ] Hard directional shadows: Y-offset only, 0-1px blur, warm-grey tone
- [ ] Top highlight on cards: `inset 0 1px 0 rgba(255,255,255,0.08)` to simulate overhead light catch
- [ ] KPI card alarm states: background tint + border color + number color escalation
- [ ] Toggle uses green (`success`) for ON state, not accent-primary
- [ ] Button press uses `translateY(1px)` (downward press), not `scale()`
- [ ] Data viz follows safety-color-aware philosophy: grey data, safety thresholds, max 3 colors per chart
- [ ] Dark mode: all safety colors brighten, surface tokens darken, shadow color shifts to near-black
- [ ] Dark mode: grain overlay switches to `soft-light` blend mode at 4% opacity
- [ ] Dark mode: border opacity values decrease (8%/15%/25%/40%)
- [ ] All 6 signature animations implemented with correct timing and easing
- [ ] Content max-width at 1200px (wider than standard for dashboard layouts)
- [ ] KPI grid uses `auto-fit, minmax(280px, 1fr)` for responsive columns
- [ ] Alarm state changes are instant (0ms) — safety alerts never transition
