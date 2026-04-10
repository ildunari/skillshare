# Monochrome Terminal — Full Specification

**Schema:** v2
**Theme Number:** 07
**Tagline:** Single-accent monochrome density -- raw infrastructure rendered as interface
**Temperature:** Warm (Concrete) / Cool (Voltage)
**Density:** very-dense
**Strategy:** borders-only

---

## Table of Contents

1. [Identity & Philosophy](#identity--philosophy) — Line 24
2. [Color System](#color-system) — Line 40
   - Warm Mode Palette — Line 42
   - Special Tokens (Warm) — Line 64
   - Cool Mode Palette — Line 72
   - Special Tokens (Cool) — Line 92
   - Opacity System — Line 100
   - Color Rules — Line 112
3. [Typography Matrix](#typography-matrix) — Line 123
   - Warm Mode — Line 125
   - Cool Mode — Line 141
   - Font Loading — Line 169
4. [Elevation System](#elevation-system) — Line 181
   - Surface Hierarchy — Line 187
   - Shadow Tokens — Line 199
   - Separation Recipe — Line 209
5. [Border System](#border-system) — Line 215
   - Widths and Patterns — Line 219
   - Focus Ring — Line 231
   - Radius (Global Override) — Line 240
6. [Component States](#component-states) — Line 250
   - Buttons (Primary) — Line 256
   - Buttons (Ghost) — Line 266
   - Text Input — Line 277
   - Chat Input Card — Line 287
   - Cards — Line 296
   - Sidebar Items — Line 305
   - Chips / Tags — Line 314
   - Toggle / Switch — Line 323
   - Tabs — Line 343
7. [Motion Map](#motion-map) — Line 353
   - Easings — Line 357
   - Duration × Easing × Component — Line 367
   - Active Press Scale — Line 386
8. [Layout Tokens](#layout-tokens) — Line 391
   - Spacing Scale — Line 403
   - Density — Line 407
   - Responsive Notes — Line 417
9. [Accessibility Tokens](#accessibility-tokens) — Line 426
10. [Overlays](#overlays) — Line 450
    - Popover / Dropdown — Line 452
    - Modal — Line 468
    - Tooltip — Line 481
11. [Visual Style](#visual-style) — Line 494
    - Material — Line 496
    - Exposed Grid — Line 524
    - Data Visualization Philosophy — Line 540
12. [Signature Animations](#signature-animations) — Line 551
    - Terminal Cursor Blink — Line 553
    - Relay Switch — Line 580
    - Scan Line Load — Line 601
    - Status LED Pulse — Line 627
    - Mechanical Panel Reveal — Line 654
13. [Mode Variant](#mode-variant) — Line 678
    - Warm vs Cool Comparison — Line 682
    - Light Mode Variant — Line 698
14. [Mobile Notes](#mobile-notes) — Line 730
    - Effects to Disable — Line 732
    - Adjustments — Line 741
    - Performance Notes — Line 748
15. [Implementation Checklist](#implementation-checklist) — Line 758

---

## Identity & Philosophy

This theme lives in the world of a well-organized server room at 2 AM. Rows of machines humming behind steel mesh, status LEDs blinking in the dark, monochrome monitors displaying scrolling logs. The beauty here is structural -- the elegance of raw infrastructure exposed without apology. Every element is a functional component in a machine, not a decorative flourish on a page.

The core visual tension: **austerity vs. clarity**. The palette is almost entirely greyscale. One single accent color carries ALL communicative weight -- it is the only non-grey hue in the entire interface. This constraint forces ruthless prioritization. If something is colored, it matters. If it is grey, it is infrastructure. The accent is earned, never decorative.

The theme ships with two modes -- **Warm ("Concrete")** and **Cool ("Voltage")** -- that share identical spatial systems, component architecture, and motion philosophy but diverge in temperature, accent hue, and material feel. Warm mode is poured concrete: warm charcoals, hairline cracks of light, a single structural red accent like a fire alarm on a grey wall. Cool mode is high-voltage terminal: pure neutrals, clinical precision, a single cyan accent like a cursor blinking on a black screen.

The single unifying signature across both modes: **mechanical motion**. Every transition is instant or near-instant. State changes snap. There are no springs, no bounces, no organic easing curves. Hover states switch like relays. Panels open like blast doors -- linear, constant-velocity, zero overshoot. The only permitted easing is linear and a sharp deceleration (`out-quad`). Nothing in this theme moves like a living thing. Everything moves like a machine.

**Decision principle:** "When in doubt, ask: would this feel at home on a server rack? If it feels soft, harden it. If it feels round, square it. If it feels colorful, grey it. If it moves organically, mechanize it."

**What this theme is NOT:**
- Not rounded -- every radius is 0px, no exceptions, no pill shapes, no circles, no soft corners
- Not colorful -- ONE accent color per mode, everything else is greyscale, no secondary accent, no gradients
- Not sparse -- this is the densest theme in the roster; if there is whitespace, it is wasted space
- Not organic -- no spring physics, no bounce, no elastic motion, no biomorphic shapes
- Not decorative -- no ornamental borders, no gratuitous shadows, no visual sugar of any kind
- Not a dark-mode-of-a-light-theme -- both modes are dark-native; the light variant is an accommodation, not the default

---

## Color System

#### Warm Mode ("Concrete") Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Deep Concrete | `#1A1A18` | Deepest background. Warm near-black with slight olive undertone. The raw slab. |
| bg | Warm Charcoal | `#242422` | Primary surface. One step above page. Poured concrete surface. |
| surface | Ash Grey | `#2E2E2B` | Elevated cards, inputs, popovers. Warm mid-tone concrete. |
| recessed | Void Concrete | `#111110` | Code blocks, inset areas. Darkest recess, shadow of the slab. |
| active | Pressed Concrete | `#3A3A37` | Active/pressed items, selected rows. Concrete under load. |
| text-primary | Raw White | `#E8E6E1` | Headings, body text. Warm off-white, like chalk on concrete. |
| text-secondary | Worn Stencil | `rgba(232,230,225,0.62)` | Sidebar items, secondary labels. text-primary at 62%. |
| text-muted | Faded Marking | `rgba(232,230,225,0.36)` | Placeholders, timestamps, metadata. text-primary at 36%. |
| text-onAccent | Slab Black | `#FFFFFF` | Text on red accent backgrounds. Pure white for maximum contrast. |
| border-base | Rebar Grey | `#8A8A85` | Used at variable opacity. The exposed steel inside concrete. |
| accent-primary | Structural Red | `#E53935` | THE accent. Fire alarm red. Primary CTA, active states, alerts, the ONE color. |
| success | Signal Green | `#7CB342` | Positive states. Desaturated olive-green, harmonizes with warm greys. |
| warning | Caution Amber | `#F9A825` | Caution states. Industrial warning yellow-amber. |
| danger | Structural Red | `#E53935` | Error states. Same as accent -- in this theme, danger IS the accent. |
| info | Concrete Blue | `#78909C` | Info states. Blue-grey, barely chromatic. Stays monochrome-adjacent. |

**Note on danger = accent:** In Warm mode, the accent IS red. Danger states use the same hue. This is intentional -- the theme has ONE color, and that color serves double duty. Contextual meaning comes from placement and iconography, not hue differentiation.

#### Special Tokens (Warm)

| Token | Value | Role |
|---|---|---|
| inlineCode | `#E53935` | Code text within prose. The accent red, monochrome exception. |
| toggleActive | `#E53935` | Toggle/switch active track. The accent red. |
| selection | `rgba(229,57,53,0.22)` | `::selection` background. Accent red at 22%. |

#### Cool Mode ("Voltage") Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Terminal Black | `#0D0D0D` | Deepest background. Near-black, pure neutral, zero warmth. |
| bg | Screen Dark | `#161616` | Primary surface. CRT-off darkness. |
| surface | Panel Grey | `#1E1E1E` | Elevated cards, inputs, popovers. Terminal panel surface. |
| recessed | Deep Void | `#080808` | Code blocks, inset areas. The space between components. |
| active | Highlight Bar | `#2A2A2A` | Active/pressed items, selected rows. Cursor-line highlight. |
| text-primary | Phosphor White | `#E0E0E0` | Headings, body text. Cool neutral white, CRT phosphor tone. |
| text-secondary | Dim Phosphor | `rgba(224,224,224,0.62)` | Sidebar items, secondary labels. text-primary at 62%. |
| text-muted | Ghost Phosphor | `rgba(224,224,224,0.36)` | Placeholders, timestamps, metadata. text-primary at 36%. |
| text-onAccent | Terminal Black | `#0D0D0D` | Text on cyan accent backgrounds. Dark on bright cyan. |
| border-base | Wire Grey | `#666666` | Used at variable opacity. Neutral mid-grey, like exposed wiring. |
| accent-primary | Voltage Cyan | `#00E5FF` | THE accent. High-voltage cyan. Cursor, active states, the ONE color. |
| success | Terminal Green | `#69F0AE` | Positive states. Bright terminal green, high contrast on dark. |
| warning | Alert Amber | `#FFD54F` | Caution states. Amber warning signal. |
| danger | Alarm Red | `#FF5252` | Error states. Distinct from accent (cyan) in cool mode. |
| info | Voltage Cyan | `#00E5FF` | Info states. Same as accent -- cyan is informational by nature. |

#### Special Tokens (Cool)

| Token | Value | Role |
|---|---|---|
| inlineCode | `#00E5FF` | Code text within prose. The accent cyan. |
| toggleActive | `#00E5FF` | Toggle/switch active track. The accent cyan. |
| selection | `rgba(0,229,255,0.20)` | `::selection` background. Accent cyan at 20%. |

#### Opacity System

Border opacity (on `border-base` per mode):

| Context | Opacity | Usage |
|---|---|---|
| subtle | 10% | Internal dividers, grid rules, hairline separators. Maximum subtlety. |
| card | 18% | Card-level borders, panel edges, input borders at rest. |
| hover | 28% | Hovered elements, interactive feedback borders. |
| focus | 100% (accent) | Focus state. Full accent color replaces border-base entirely. |
| grid | 6% | Exposed background grid lines. Visible but non-competing. |

#### Color Rules

- ONE accent color per mode. Red (Warm) or Cyan (Cool). No secondary accent. No tertiary. ONE.
- Every non-grey color must encode information. The accent marks interactive or active states. Semantic colors mark system states. Nothing else gets hue.
- Greyscale is the primary visual language. 90%+ of all pixels on screen should be grey, black, or white.
- Warm and Cool modes must NEVER be mixed. They share geometry, not palette.
- The info semantic color intentionally overlaps with accent in Cool mode (both cyan) and is intentionally desaturated in Warm mode (blue-grey). This preserves the single-accent constraint.
- No gradients anywhere. Flat fills only. The only visual texture is the concrete grain overlay in Warm mode.

---

## Typography Matrix

#### Warm Mode ("Concrete")

Headline font: Barlow Condensed. Body/data font: IBM Plex Mono. The condensed sans headlines feel like stenciled labels on concrete infrastructure -- utilitarian, compressed, industrial.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Barlow Condensed | 20px | 700 | 1.15 | 0.08em | `text-transform: uppercase` | Hero titles, page names. ALL CAPS stencil. |
| Heading | Barlow Condensed | 14px | 600 | 1.25 | 0.06em | `text-transform: uppercase` | Section titles, panel headers. ALL CAPS. |
| Body | IBM Plex Mono | 13px | 400 | 1.55 | normal | `font-feature-settings: "zero"` | Primary reading text, log output, data. |
| Body Small | IBM Plex Mono | 11px | 400 | 1.45 | normal | `font-feature-settings: "zero"` | Sidebar items, form labels, dense lists. |
| Button | Barlow Condensed | 12px | 600 | 1.4 | 0.05em | `text-transform: uppercase` | Button labels. ALL CAPS stencil. |
| Input | IBM Plex Mono | 13px | 400 | 1.4 | normal | `font-feature-settings: "zero"` | Form input text, command entry. |
| Label | Barlow Condensed | 10px | 500 | 1.3 | 0.06em | `text-transform: uppercase` | Metadata, timestamps, axis labels. ALL CAPS. |
| Code | IBM Plex Mono | 13px | 400 | 1.55 | normal | `font-feature-settings: "liga", "zero"` | Inline code, code blocks, terminal output. |
| Caption | IBM Plex Mono | 10px | 400 | 1.33 | normal | -- | Footnotes, disclaimers, status bar text. |

#### Cool Mode ("Voltage")

Headline font: Barlow Condensed. Body/data font: JetBrains Mono. Cool mode uses the same condensed headline treatment but pairs with JetBrains Mono for a sharper, more technical body feel. Sentence case for headlines (no ALL CAPS) -- the voltage mode is clinical, not industrial.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Barlow Condensed | 20px | 600 | 1.15 | 0.04em | -- | Hero titles, page names. Sentence case. |
| Heading | Barlow Condensed | 14px | 500 | 1.25 | 0.03em | -- | Section titles, panel headers. Sentence case. |
| Body | JetBrains Mono | 13px | 400 | 1.55 | normal | `font-feature-settings: "zero"` | Primary reading text, log output, data. |
| Body Small | JetBrains Mono | 11px | 400 | 1.45 | normal | `font-feature-settings: "zero"` | Sidebar items, form labels, dense lists. |
| Button | Barlow Condensed | 12px | 500 | 1.4 | 0.03em | -- | Button labels. Sentence case. |
| Input | JetBrains Mono | 13px | 400 | 1.4 | normal | `font-feature-settings: "zero"` | Form input text, command entry. |
| Label | Barlow Condensed | 10px | 500 | 1.3 | 0.04em | `text-transform: uppercase` | Metadata, timestamps, axis labels. Uppercase labels only. |
| Code | JetBrains Mono | 13px | 400 | 1.55 | normal | `font-feature-settings: "liga", "zero"` | Inline code, code blocks, terminal output. |
| Caption | JetBrains Mono | 10px | 400 | 1.33 | normal | -- | Footnotes, disclaimers, status bar text. |

**Typographic decisions:**
- Monospace is the PRIMARY reading experience. Body text, data, inputs, code -- all mono. This is the defining typographic choice of the theme.
- Barlow Condensed is used ONLY for structural labels: display, heading, button, label. It is a stencil, not a reading font.
- Warm mode uses ALL CAPS for all Barlow Condensed usage -- the stenciled-on-concrete feel.
- Cool mode uses ALL CAPS only for labels (metadata/timestamps). Headlines and buttons are sentence case -- cleaner, more terminal-like.
- Strict size hierarchy: Small (10-11px), Medium (12-13px), Large (14-20px). Dense and compressed.
- `font-smoothing: antialiased` always.
- `text-wrap: auto` (no `pretty` -- terminal text does not reflow poetically).
- Slashed zero (`"zero"` feature) is mandatory for all monospace to distinguish `0` from `O`.
- IBM Plex Mono (Warm) has a slightly wider character width than JetBrains Mono (Cool), contributing to the "concrete slab" heaviness of Warm mode vs. the "precision instrument" feel of Cool mode.

#### Font Loading

**Warm mode:**
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
```

**Cool mode:**
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

---

## Elevation System

**Strategy:** `borders-only`

This is a flat theme. Depth is communicated through border weight, surface tint-stepping, and the exposed grid -- never through shadows. Warm mode has ZERO shadows. Cool mode has exactly one: a tight popover shadow for menus/dropdowns.

#### Surface Hierarchy

| Surface | Background (Warm) | Background (Cool) | Shadow | Usage |
|---|---|---|---|---|
| page | `#1A1A18` | `#0D0D0D` | none | Main page canvas, deepest layer |
| bg | `#242422` | `#161616` | none | Primary surface, sidebar background |
| surface | `#2E2E2B` | `#1E1E1E` | none | Cards, inputs, elevated panels |
| recessed | `#111110` | `#080808` | none | Code blocks, data wells, inset areas |
| active | `#3A3A37` | `#2A2A2A` | none | Active/pressed, selected rows, highlights |
| overlay | `#2E2E2B` | `#1E1E1E` | shadow-popover (Cool only) | Popovers, dropdowns, context menus |

#### Shadow Tokens

| Token | Warm Value | Cool Value | Usage |
|---|---|---|---|
| shadow-none | `none` | `none` | All standard surfaces. The default. |
| shadow-popover | `none` | `0 2px 8px rgba(0,0,0,0.6), 0 0 0 1px rgba(102,102,102,0.18)` | Popovers/dropdowns. Cool mode only. |
| shadow-input | `none` | `none` | Input card rest. Flat everywhere. |
| shadow-input-hover | `none` | `none` | Input card hover. Flat everywhere. |
| shadow-input-focus | `none` | `0 0 0 1px var(--accent-primary)` | Input focus ring. Cool mode only. |

#### Separation Recipe

Borders-only with tint-stepping. Each surface level is 1-2 stops lighter on a greyscale ramp. Borders increase in weight (1px internal, 1.5px card, 2px heavy) to communicate hierarchy. An optional exposed background grid (6% opacity, 4px spacing) provides alignment structure visible through transparent surfaces. No shadows in Warm mode. One tight popover shadow in Cool mode for dropdown/menu disambiguation. No dividers inside cards -- grid alignment and tint-step alone create visual grouping. Dense spacing + rigid grid = implicit separation without ornament.

---

## Border System

ALL border-radius values are `0px`. No exceptions. Everything is rectangular. This is a defining constraint of the theme and MUST be enforced globally.

#### Widths and Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| grid | 1px | `border-base` at 6% | Background grid lines, exposed alignment structure. |
| internal | 1px | `border-base` at 10% | Dividers within cards, table rules, separators. |
| card | 1px | `border-base` at 18% | Card edges, panel boundaries, section dividers. |
| heavy | 2px | `border-base` at 28% | Major section dividers, header underlines, emphasis borders. |
| input | 1px | `border-base` at 18% | Form input borders at rest. Same as card weight. |
| input-hover | 1px | `border-base` at 28% | Input hover state. |
| input-focus | 1px | accent-primary at 100% | Input focus. Full accent color. |
| accent-left | 2px | accent-primary at 100% | Left-border accent on active sidebar items, callouts, alerts. |

#### Focus Ring

- **Warm mode:** `2px solid #E53935` (structural red accent)
- **Cool mode:** `2px solid #00E5FF` (voltage cyan accent)
- **Width:** 2px solid
- **Offset:** 1px (via `outline-offset: 1px`) -- tighter offset than most themes for density
- **Implementation:** `outline: 2px solid var(--accent-primary); outline-offset: 1px;`
- **No inner ring, no glow, no shadow.** The sharp rectangular outline on a dark background is sufficient.

#### Radius (Global Override)

| Token | Value |
|---|---|
| none / sm / md / lg / xl / 2xl / input / full | ALL `0px` |

**CSS safety net:** Apply `* { border-radius: 0 !important; }` as a global override to catch any component library defaults that might leak through.

---

## Component States

All transitions use `linear` or `ease-out` (mechanical) timing. No springs, no elastic easing. State changes are fast (0-100ms). The feel is relay-switch, not rubber-band.

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `accent-primary`, border none, color `text-onAccent`, radius 0px, h 28px, padding `0 10px`, font button |
| Hover | bg `accent-primary` brightened 12% (Warm: `#EF5350`, Cool: `#33EBFF`), transition 50ms linear |
| Active | bg `accent-primary` darkened 15% (Warm: `#C62828`, Cool: `#00B8D4`), no scale transform |
| Focus | outline `2px solid var(--accent-primary)`, outline-offset 1px |
| Disabled | opacity 0.3, pointer-events none, cursor not-allowed |
| Transition | `background-color 50ms linear` -- mechanical snap with minimal interpolation |

#### Buttons (Ghost)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid border-base at 18%`, color `text-secondary`, radius 0px, h 28px, padding `0 10px` |
| Hover | bg `active`, border at 28%, color `text-primary`, transition 50ms linear |
| Active | bg `surface`, border at 28% |
| Focus | outline focus ring |
| Disabled | opacity 0.3, pointer-events none |
| Transition | `all 50ms linear` |

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `surface`, border `1px solid border-base at 18%`, radius 0px, h 32px, padding `0 8px`, font input, color `text-primary`, placeholder `text-muted`, caret-color `accent-primary` |
| Hover | border at 28% opacity, transition 50ms linear |
| Focus | border `1px solid accent-primary`, outline none, box-shadow `0 0 0 1px var(--accent-primary)` (Cool only) |
| Disabled | opacity 0.3, pointer-events none, bg `bg` |
| Transition | `border-color 50ms linear` |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `surface`, radius 0px, border `1px solid border-base at 18%`, shadow none |
| Hover | border at 28%, transition 50ms linear |
| Focus-within | border `1px solid accent-primary` |
| Transition | `border-color 50ms linear` |

#### Cards

| State | Properties |
|---|---|
| Rest | bg `surface`, border `1px solid border-base at 18%`, radius 0px, shadow none |
| Hover | border at 28%, bg lifted 1 stop (Warm: `#333330`, Cool: `#232323`), transition 50ms linear |
| Transition | `all 50ms linear` |

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `text-secondary`, radius 0px, h 28px, padding `2px 10px`, font bodySmall |
| Hover | bg `active`, color `text-primary`, transition 50ms linear |
| Active (current) | bg `active`, color `accent-primary`, border-left `2px solid accent-primary`, padding-left 8px (compensate border) |
| Transition | `all 50ms linear` |

#### Chips / Tags

| State | Properties |
|---|---|
| Rest | bg `bg`, border `1px solid border-base at 10%`, radius 0px, h 22px, padding `0 6px`, font label (10px), color `text-secondary` |
| Hover | bg `active`, border at 18%, color `text-primary`, transition 50ms linear |
| Active/selected | bg `accent-primary`, color `text-onAccent`, border accent-primary |
| Transition | `all 50ms linear` |

#### Toggle / Switch

**Theme override:** Rectangular toggle. NOT pill-shaped. 32x16px sharp rectangle.

| Property | Value |
|---|---|
| Track width | 32px |
| Track height | 16px |
| Track radius | 0px |
| Track off bg | `active` token (Warm: `#3A3A37`, Cool: `#2A2A2A`) |
| Track off border | `1px solid border-base at 18%` |
| Track on bg | `accent-primary` (Warm: `#E53935`, Cool: `#00E5FF`) |
| Track on border | none |
| Thumb | 12x12px square, bg `text-primary`, 0px radius |
| Thumb off position | left 2px |
| Thumb on position | right 2px |
| Thumb shadow | none |
| Transition | `all 50ms linear` -- thumb slides linearly, no spring, no bounce |
| Focus-visible | focus ring around entire track |

#### Tabs

| State | Properties |
|---|---|
| Rest | bg transparent, color `text-muted`, radius 0px, h 28px, padding `0 10px`, font bodySmall, border-bottom `2px solid transparent` |
| Hover | color `text-secondary`, border-bottom `2px solid border-base at 18%`, transition 50ms linear |
| Active | color `text-primary`, border-bottom `2px solid accent-primary` |
| Transition | `all 50ms linear` |

---

## Motion Map

**Core philosophy:** Mechanical motion. Every transition is linear or uses a sharp deceleration curve (`out-quad`). No springs, no elastic easing, no organic curves. State changes are fast -- most interactions complete in 0-100ms. Panel reveals use linear motion at constant velocity. The feel is electromechanical: relays switching, shutters opening, indicators snapping on.

#### Easings

| Name | Value | Character |
|---|---|---|
| instant | `steps(1)` | Single-frame snap. For binary state changes (on/off). |
| mechanical | `linear` | Constant velocity. The default for this theme. No acceleration, no deceleration. |
| decel | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` | Out-quad. Sharp stop, like a machine hitting its end-stop. |
| brake | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | Out-cubic. Slightly smoother deceleration for larger panel movements. |

#### Duration × Easing × Component

| Component | Duration (Warm) | Duration (Cool) | Easing | Notes |
|---|---|---|---|---|
| Button hover bg | 50ms | 50ms | mechanical | Fast linear color shift |
| Sidebar item hover | 50ms | 50ms | mechanical | Linear bg/color change |
| Chip hover/select | 50ms | 50ms | mechanical | Linear state change |
| Toggle thumb slide | 80ms | 80ms | mechanical | Linear slide, no spring |
| Input focus border | 0ms | 0ms | instant | Instant border color snap |
| Card hover border | 50ms | 50ms | mechanical | Linear border opacity shift |
| Tab indicator slide | 100ms | 100ms | decel | Indicator slides to new position with sharp stop |
| Panel open/close | 150ms | 120ms | mechanical | Linear height/width reveal. Warm slightly slower (heavier). |
| Popover entry | 80ms | 60ms | decel | Quick decel entry. Warm slightly heavier. |
| Modal entry | 120ms | 100ms | mechanical | Linear opacity 0-to-1 fade |
| Tooltip entry | 0ms | 0ms | instant | Instant appearance |
| Cursor blink | 800ms | 800ms | `steps(2)` | Terminal cursor blink at 400ms intervals |
| Status LED pulse | 1600ms | 1600ms | `steps(2)` | Slow blink for status indicators |
| Scrollbar fade | 300ms | 300ms | mechanical | Linear fade to transparent on idle |

#### Active Press Scale

**None.** No `transform: scale()` on any element. Active states are communicated through color darkening only. Scale transforms introduce organic feel -- this theme communicates state through color, border, and background changes exclusively.

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column |
| Narrow max-width | 640px | Focused content, single-panel views |
| Sidebar width | 240px | Fixed sidebar. Narrower than typical for density. |
| Header height | 36px | Compact top bar. Dense. |
| Status bar height | 20px | Bottom status bar. Terminal-style. |
| Spacing unit | 4px | Base grid multiplier. ALL spacing is 4px multiples. |

#### Spacing Scale

4, 8, 12, 16, 20, 24, 32px -- strictly 4px-aligned. No 6px, no 10px.

#### Density

**Very Dense.** This is the densest theme in the roster.
- 4px internal padding on cards and panels
- 2-4px gaps between list items
- 8-12px section spacing
- 28px row heights for lists and tables (not 32px)
- 22px chip/tag heights
- 32px input heights (not 44px -- density over comfort)
- Content is packed tight. Every pixel of whitespace must justify its existence.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (240px) + content column + optional secondary panel. Triple-column layouts for monitoring dashboards.
- **md (768px):** Sidebar collapses to icon-only rail (36px). Content fills available width. Data tables maintain horizontal scroll.
- **sm (640px):** Single column. Header collapses to minimal bar with hamburger. Sidebar becomes overlay (linear slide-in, 120ms). Tables switch to stacked rows. Touch targets expand to 44px minimum (override visual density on mobile).
- Grid lines hidden below `md` breakpoint for cleanliness on smaller screens.

---

## Accessibility Tokens

| Token | Warm Value | Cool Value |
|---|---|---|
| Focus ring color | `#E53935` (structural red) | `#00E5FF` (voltage cyan) |
| Focus ring width | 2px solid | 2px solid |
| Focus ring offset | 1px | 1px |
| Disabled opacity | 0.3 | 0.3 |
| Disabled pointer-events | none | none |
| Disabled cursor | not-allowed | not-allowed |
| Selection bg | `rgba(229,57,53,0.22)` | `rgba(0,229,255,0.20)` |
| Selection color | `#E8E6E1` (text-primary) | `#E0E0E0` (text-primary) |
| Scrollbar width | thin | thin |
| Scrollbar thumb | `rgba(138,138,133,0.22)` | `rgba(102,102,102,0.28)` |
| Scrollbar track | transparent | transparent |
| Min touch target | 44px | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large) | WCAG AA (4.5:1 text, 3:1 large) |

**Contrast notes:** Warm mode `#E8E6E1` on `#1A1A18` = 13.8:1. Cool mode `#E0E0E0` on `#0D0D0D` = 15.3:1. Both exceed AAA. Accent text: Warm `#E53935` on `#1A1A18` = 5.2:1 (passes AA). Cool `#00E5FF` on `#0D0D0D` = 12.4:1 (passes AAA).

**Reduced motion:** All transitions collapse to `0ms` (instant). Cursor blink stops. Status LED blink stops. Panel reveals become instant. Scrollbar fade becomes instant. `prefers-reduced-motion: reduce` triggers `* { transition-duration: 0ms !important; animation-duration: 0ms !important; }`.

---

## Overlays

#### Popover / Dropdown

- **bg:** `surface` token (Warm: `#2E2E2B`, Cool: `#1E1E1E`)
- **backdrop-filter:** none (both modes -- no blur, no frosted glass, pure opaque panels)
- **border:** `1px solid border-base at 28%`
- **radius:** 0px
- **shadow:** none (Warm), shadow-popover (Cool: `0 2px 8px rgba(0,0,0,0.6), 0 0 0 1px rgba(102,102,102,0.18)`)
- **padding:** 2px
- **z-index:** 50
- **min-width:** 160px, **max-width:** 280px
- **Menu item:** 2px 8px padding, radius 0px, h 26px, font bodySmall, color text-secondary
- **Menu item hover:** bg `active`, color `text-primary`, transition 50ms linear
- **Entry:** opacity 0 to 1, 80ms decel (Warm) / 60ms decel (Cool)
- **Exit:** opacity 1 to 0, 60ms linear

#### Modal

- **Overlay bg:** Warm: `rgba(26,26,24,0.88)`, Cool: `rgba(13,13,13,0.88)`
- **Overlay backdrop-filter:** none (no blur -- opaque overlay is sufficient for this aesthetic)
- **Content bg:** `surface` token
- **Content border:** `2px solid border-base at 28%`
- **Content radius:** 0px
- **Content shadow:** none
- **Content padding:** 12px
- **Entry:** opacity 0 to 1, 120ms linear (Warm) / 100ms linear (Cool) -- mechanical fade
- **Exit:** opacity 1 to 0, 80ms linear
- **Close button:** Ghost button, top-right, 28x28px, contains `x` character in monospace

#### Tooltip

- **bg:** `active` token (Warm: `#3A3A37`, Cool: `#2A2A2A`)
- **color:** `text-primary`
- **font:** label size (10px), monospace family, weight 400
- **border:** `1px solid border-base at 18%`
- **radius:** 0px
- **padding:** 2px 6px
- **shadow:** none
- **No arrow.** Position via offset. Appears instantly (0ms, `steps(1)`).
- **Max-width:** 240px. Text wraps if needed.

---

## Visual Style

#### Material

- **Grain (Warm mode only):** Subtle concrete noise via SVG feTurbulence filter at 2% opacity. Coarser frequency than Pixel Grid's paper grain -- this is poured concrete, not newsprint.

```html
<svg width="0" height="0" style="position:absolute">
  <filter id="concrete-grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" />
    <feColorMatrix type="saturate" values="0" />
  </filter>
</svg>
```
```css
.grain-overlay {
  position: fixed; inset: 0;
  opacity: 0.02;
  filter: url(#concrete-grain);
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: multiply;
}
```

- **Grain (Cool mode):** None. Pure digital surfaces. Zero texture. The screen is pristine.
- **Gloss:** Matte. Zero sheen, zero reflections. Surfaces are flat and opaque.
- **Blend mode:** Normal (Cool), multiply for grain layer only (Warm).
- **Shader bg:** False. No WebGL, no canvas backgrounds.

#### Exposed Grid

The defining visual element of this theme. An optional background grid rendered at 6% opacity of `border-base`, with lines at every `spacing-unit` (4px) interval. The grid is visible through all transparent or semi-transparent surfaces, providing a constant structural reference -- like graph paper behind the interface.

```css
.exposed-grid {
  background-image:
    linear-gradient(var(--border-base-6) 1px, transparent 1px),
    linear-gradient(90deg, var(--border-base-6) 1px, transparent 1px);
  background-size: 4px 4px;
  background-position: -0.5px -0.5px;
}
```

The grid is applied to the `page` surface and shows through wherever `bg` or `surface` elements have gaps between them. It is NOT applied inside cards or panels -- only on the background canvas.

#### Data Visualization Philosophy

Monochrome-first with accent highlights:

- **YES:** Line charts (single color, no fill), bar charts (greyscale bars, accent for highlighted), tables (the native format), heatmaps (greyscale gradient with accent for peaks), sparklines (single-pixel-width lines).
- **NO:** Pie charts, donut charts, multi-color area fills, 3D charts, decorative gradients.
- **Color rule:** Charts use greyscale for data and accent-primary for the single most important data point or threshold line. If you need to distinguish multiple series, use line-weight and dash-pattern variation, not color.
- **Grid:** Exposed. Chart grid lines are visible at the same `border-base at 6%` opacity as the background grid.

---

## Signature Animations

#### 1. Terminal Cursor Blink

The universal heartbeat of this theme. A blinking cursor indicator (the accent color) that appears on active elements -- text inputs, active sidebar items, the command palette. On/off at 800ms interval using `steps(2)`.

- **Technique:** `opacity` animation with `steps(2)`
- **Duration:** 800ms (400ms on, 400ms off)
- **Easing:** `steps(2)`
- **CSS:**
```css
@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
.cursor-active::after {
  content: "";
  display: inline-block;
  width: 2px;
  height: 1em;
  background: var(--accent-primary);
  animation: cursor-blink 800ms steps(2) infinite;
  vertical-align: text-bottom;
  margin-left: 1px;
}
```
- **Reduced motion:** Static cursor, no blink. Stays at full opacity.

#### 2. Relay Switch

When a component changes state (hover, active, toggle), it snaps to the new state with a brief intermediate flash -- like an electrical relay closing. The element flashes to `accent-primary` at 15% opacity for one frame (16ms) before settling into the target state.

- **Technique:** Keyframe animation triggered on state change via class toggle
- **Duration:** 100ms total (16ms flash, 84ms settle)
- **Easing:** `steps(2)` for the flash frame, then linear settle
- **CSS:**
```css
@keyframes relay-switch {
  0% { background-color: var(--current-bg); }
  16% { background-color: color-mix(in srgb, var(--accent-primary) 15%, var(--target-bg)); }
  100% { background-color: var(--target-bg); }
}
.relay-transition {
  animation: relay-switch 100ms steps(2) forwards;
}
```
- **Reduced motion:** Instant state change, no flash frame.
- **Usage:** Toggle switches, sidebar item selection, tab switching. NOT used on button hover (too frequent).

#### 3. Scan Line Load

When a panel or section loads data, a single horizontal line sweeps from top to bottom of the container -- like a CRT scan line or a barcode scanner. The line is 1px tall, full-width, colored `accent-primary` at 40% opacity.

- **Technique:** `transform: translateY()` animation with `linear` easing
- **Duration:** 600ms
- **Easing:** `linear` (constant velocity, mechanical sweep)
- **CSS:**
```css
@keyframes scan-line {
  from { transform: translateY(0); opacity: 0.4; }
  to { transform: translateY(var(--container-height)); opacity: 0; }
}
.scan-loading::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: var(--accent-primary);
  animation: scan-line 600ms linear forwards;
  pointer-events: none;
}
```
- **Reduced motion:** No scan line. Content appears instantly.
- **Usage:** Data table initial load, panel content refresh, log buffer fill.

#### 4. Status LED Pulse

Status indicators (system health, connection status, build status) use a slow blink that differs from the cursor blink. Instead of on/off, the LED dims to 30% and brightens to 100% -- like an LED power indicator on hardware.

- **Technique:** `opacity` animation with `steps(2)`
- **Duration:** 1600ms (800ms bright, 800ms dim)
- **Easing:** `steps(2)` -- snaps between bright and dim, no smooth fade
- **CSS:**
```css
@keyframes led-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
.status-led {
  display: inline-block;
  width: 6px;
  height: 6px;
  background: var(--accent-primary);
  animation: led-pulse 1600ms steps(2) infinite;
}
.status-led--success { background: var(--success); }
.status-led--warning { background: var(--warning); }
.status-led--danger { background: var(--danger); }
```
- **Reduced motion:** Static at full opacity.
- **Usage:** Server status, WebSocket connection indicator, CI build running, system health dashboard.

#### 5. Mechanical Panel Reveal

Panels and side-drawers open with pure linear motion -- constant velocity from start to finish, like a blast door or an industrial shutter. No acceleration, no deceleration, no overshoot. The panel simply moves from closed to open at a fixed speed.

- **Technique:** `transform: translateX()` or `height` animation with `linear` easing
- **Duration:** 150ms (Warm), 120ms (Cool)
- **Easing:** `linear`
- **CSS:**
```css
@keyframes panel-open {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}
@keyframes panel-close {
  from { transform: translateX(0); }
  to { transform: translateX(-100%); }
}
.panel-enter { animation: panel-open 150ms linear forwards; }
.panel-exit { animation: panel-close 120ms linear forwards; }
```
- **Reduced motion:** Instant open/close, no slide.
- **Usage:** Sidebar toggle, inspector panels, command palette, settings drawer.

---

## Mode Variant

Both Warm and Cool modes are dark themes. Neither is "the dark mode of the other" -- they are parallel interpretations of the same monochrome-dense philosophy at different color temperatures.

#### Warm vs Cool Comparison

| Dimension | Warm ("Concrete") | Cool ("Voltage") |
|---|---|---|
| Page bg | `#1A1A18` (warm charcoal) | `#0D0D0D` (near-black neutral) |
| Temperature | Warm, olive-tinged greys | Cool, pure neutral greys |
| Headline font | Barlow Condensed, ALL CAPS, wide tracking | Barlow Condensed, sentence case, tighter tracking |
| Body font | IBM Plex Mono | JetBrains Mono |
| Accent | Structural Red `#E53935` | Voltage Cyan `#00E5FF` |
| Grain | Yes (2% feTurbulence concrete noise, `multiply`) | No grain |
| Shadows | Zero -- borders only | One popover shadow |
| Text color | Warm off-white `#E8E6E1` | Cool neutral `#E0E0E0` |
| Danger color | Same as accent (red) | Distinct from accent (red vs cyan) |
| Motion speed | Slightly slower (heavier, concrete) | Slightly faster (lighter, electronic) |
| Vibe | Poured concrete, server room, bunker | High-voltage terminal, clean room, control center |

#### Light Mode Variant

For both Warm and Cool, the light variant inverts the surface ramp while preserving the same accent system, motion philosophy, and zero-radius constraint.

| Token | Warm Light | Cool Light |
|---|---|---|
| page | `#EDEBE8` (warm off-white) | `#F5F5F5` (cool near-white) |
| bg | `#E3E1DE` (warm cream) | `#EBEBEB` (light grey) |
| surface | `#FFFFFF` (white) | `#FFFFFF` (white) |
| recessed | `#D9D7D3` (warm tan) | `#E0E0E0` (grey) |
| active | `#CFCDC8` (warm highlighted) | `#D5D5D5` (mid grey) |
| text-primary | `#1A1A18` (warm charcoal) | `#0D0D0D` (near-black) |
| text-secondary | `rgba(26,26,24,0.62)` | `rgba(13,13,13,0.62)` |
| text-muted | `rgba(26,26,24,0.36)` | `rgba(13,13,13,0.36)` |
| border-base | `#78756F` (warm mid-grey) | `#999999` (neutral mid-grey) |
| accent-primary | `#C62828` (darker red for contrast on light) | `#00ACC1` (darker cyan for contrast on light) |
| success | `#558B2F` (darker olive) | `#2E7D32` (darker green) |
| warning | `#F57F17` (darker amber) | `#F57F17` (darker amber) |
| danger | `#C62828` (darker red) | `#D32F2F` (darker red) |
| inlineCode | `#C62828` (dark red) | `#00838F` (dark cyan) |
| scrollbar thumb | `rgba(120,117,111,0.22)` | `rgba(153,153,153,0.28)` |
| selection bg | `rgba(198,40,40,0.18)` | `rgba(0,172,193,0.18)` |

**Light mode rules:**
- Concrete grain (Warm) increases to 3% opacity on light backgrounds
- Shadows remain zero (Warm) / one popover (Cool) -- light mode does not add shadows
- Border opacity values shift down: subtle 6%, card 12%, hover 20% (lighter background needs less border weight)
- Focus ring uses darkened accent color, 2px solid, 1px offset
- All motion durations remain identical -- light mode does not change the animation system
- Grid lines (exposed grid) reduce to 4% opacity on light backgrounds
- 0px border-radius is maintained absolutely -- light mode does not soften anything

---

## Mobile Notes

#### Effects to Disable
- Exposed background grid -- hidden on screens below `md` (768px) for performance and visual cleanliness
- Concrete grain overlay (Warm mode) -- disabled entirely on mobile for performance
- Scan line load animation (signature #3) -- replaced with instant content appearance
- Status LED pulse animation reduced to static indicator (no blink) on mobile to reduce visual noise

#### Adjustments
- Header height: 36px (unchanged -- already compact)
- Sidebar: hidden by default, slides in as overlay (linear, 120ms) triggered by hamburger
- Touch targets: all interactive elements maintain 44px minimum tap area even if visual size is smaller (extend hit area with invisible padding). This overrides the 28px visual heights used in desktop density mode.
- Font sizes: Body stays 13px mono (dense enough to be information-rich, large enough to be readable on mobile)
- Button heights increase from 28px visual to 44px tap target (padding extends the hit area, not the visual footprint)
- Data tables: horizontal scroll with sticky first column, or collapse to stacked card layout below 640px
- Spacing relaxes slightly on mobile: minimum gap between list items increases from 2px to 4px for touch accuracy

#### Performance Notes
- No `backdrop-filter` in either mode (already none in Warm, none needed in Cool popover context on mobile)
- No `box-shadow` compositing -- borders-only strategy is GPU-friendly
- Linear and `steps(n)` animations are cheaper than spring/bezier curves -- fewer interpolation frames needed
- Concrete grain SVG filter (Warm mode) is the single most expensive effect -- disable on mobile first
- Exposed grid CSS background-image is a repeating gradient -- minimal GPU cost on desktop, but disable on mobile for battery savings
- Monospace fonts may render slightly slower than proportional fonts on some mobile renderers -- preload critical weights

---

## Implementation Checklist

- [ ] Google Fonts loaded: Barlow Condensed (500, 600, 700) + IBM Plex Mono (400) for Warm; Barlow Condensed (500, 600) + JetBrains Mono (400) for Cool
- [ ] CSS custom properties defined for ALL color tokens per mode (use `data-theme="warm"` / `data-theme="cool"` attribute)
- [ ] ALL border-radius values set to 0px globally (`* { border-radius: 0 !important; }` as safety net)
- [ ] Border weight hierarchy applied: 1px internal, 1px card, 2px heavy
- [ ] Border opacity system implemented: 6% grid, 10% subtle, 18% card, 28% hover
- [ ] Focus ring uses `outline: 2px solid var(--accent-primary); outline-offset: 1px` on all interactive elements
- [ ] All transitions use `linear`, `steps(n)`, or `out-quad` easing -- zero spring/elastic physics
- [ ] `prefers-reduced-motion` media query: all durations set to 0ms, all animations paused/removed
- [ ] Toggle is rectangular (32x16px, 0px radius, square 12x12px thumb)
- [ ] Exposed grid background applied to page surface at 6% opacity, 4px spacing
- [ ] Concrete grain SVG filter applied in Warm mode (disabled on mobile)
- [ ] Typography: monospace is primary body font in both modes
- [ ] Barlow Condensed used only for display/heading/button/label roles
- [ ] Warm mode `text-transform: uppercase` applied to all Barlow Condensed usage
- [ ] Cool mode `text-transform: uppercase` applied only to label role
- [ ] Slashed zero (`font-feature-settings: "zero"`) on all monospace text
- [ ] ONE accent color per mode enforced: Red (Warm), Cyan (Cool). No secondary accent anywhere.
- [ ] Scrollbar styled: thin, border-base thumb at 22-28%, transparent track
- [ ] `::selection` styled with accent-primary at 20-22%
- [ ] `::placeholder` opacity matches text-muted token (36%)
- [ ] Touch targets >= 44px on all interactive elements (mobile override on 28px visual heights)
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] Data visualization follows monochrome-first philosophy: greyscale data, accent for highlights only
- [ ] Light mode variant: all surface tokens swap, border opacity decreases, accent colors darken for contrast
- [ ] Status bar (20px height) implemented at bottom of viewport with monospace text
- [ ] Row heights at 28px for dense lists and tables (not 32px)
- [ ] No gradients anywhere in the theme
- [ ] All 5 signature animations implemented with correct timing and easing
- [ ] Modal/popover overlays are opaque (no backdrop blur)
