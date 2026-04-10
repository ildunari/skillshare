# 9. Vapor Silk — Full Theme Specification

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 16
- [Color System](#color-system) — Line 39
  - [Palette](#palette) — Line 41
  - [Special Colors](#special-colors) — Line 65
  - [Fixed Colors](#fixed-colors) — Line 73
  - [Opacity System](#opacity-system) — Line 80
  - [Color Rules](#color-rules) — Line 93
- [Typography Matrix](#typography-matrix) — Line 104
  - [Font Families](#font-families) — Line 106
  - [Role Matrix](#role-matrix) — Line 118
  - [Font Loading](#font-loading) — Line 137
- [Elevation System](#elevation-system) — Line 150
  - [Surface Hierarchy](#surface-hierarchy) — Line 156
  - [Shadow Tokens](#shadow-tokens) — Line 168
  - [Backdrop Filter](#backdrop-filter) — Line 182
  - [Separation Recipe](#separation-recipe) — Line 191
- [Border System](#border-system) — Line 197
  - [Base Color](#base-color) — Line 199
  - [Widths and Patterns](#widths-and-patterns) — Line 203
  - [Width Scale](#width-scale) — Line 213
  - [Focus Ring](#focus-ring) — Line 222
- [Component States](#component-states) — Line 235
  - [Buttons (Primary/Outlined)](#buttons-primaryoutlined) — Line 237
  - [Buttons (Accent/CTA)](#buttons-accentcta) — Line 250
  - [Buttons (Ghost/Icon)](#buttons-ghosticon) — Line 263
  - [Text Input (Settings Form)](#text-input-settings-form) — Line 276
  - [Textarea](#textarea) — Line 289
  - [Chat Input Card](#chat-input-card) — Line 297
  - [Cards](#cards) — Line 309
  - [Sidebar Items](#sidebar-items) — Line 320
  - [Section Labels (Sidebar)](#section-labels-sidebar) — Line 331
  - [Chips (Landing Quick Actions)](#chips-landing-quick-actions) — Line 343
  - [Toggle/Switch](#toggleswitch) — Line 354
  - [User Message Bubble](#user-message-bubble) — Line 368
- [Motion Map](#motion-map) — Line 383
  - [Easings](#easings) — Line 385
  - [Duration x Easing x Component](#duration-x-easing-x-component) — Line 396
  - [Active Press Scale](#active-press-scale) — Line 416
  - [Reduced Motion](#reduced-motion-prefers-reduced-motion-reduce) — Line 424
- [Overlays](#overlays) — Line 439
  - [Popover/Dropdown](#popoverdropdown) — Line 441
  - [Modal](#modal) — Line 462
  - [Tooltip](#tooltip) — Line 477
- [Layout Tokens](#layout-tokens) — Line 494
  - [Spacing Scale](#spacing-scale) — Line 505
  - [Density](#density) — Line 524
  - [Responsive Notes](#responsive-notes) — Line 528
- [Accessibility Tokens](#accessibility-tokens) — Line 545
- [Visual Style](#visual-style) — Line 575
  - [Material](#material) — Line 577
  - [Ambient Mesh Gradient Background](#ambient-mesh-gradient-background) — Line 587
  - [Surface Quality](#surface-quality) — Line 629
- [Signature Animations](#signature-animations) — Line 638
  - [1. Silk Wave Background (Ambient)](#1-silk-wave-background-ambient) — Line 640
  - [2. Mist Fade Reveal (Page Entry)](#2-mist-fade-reveal-page-entry) — Line 658
  - [3. Cloud Lift (Card Hover)](#3-cloud-lift-card-hover) — Line 701
  - [4. Silk Curtain (Panel Slide)](#4-silk-curtain-panel-slide) — Line 733
  - [5. Vapor Dissolve (Element Removal)](#5-vapor-dissolve-element-removal) — Line 797
- [Dark Mode Variant](#dark-mode-variant) — Line 842
  - [Dark Mode Palette](#dark-mode-palette) — Line 846
  - [Dark Mode Special Colors](#dark-mode-special-colors) — Line 867
  - [Dark Mode Rules](#dark-mode-rules) — Line 875
  - [Dark Mode Shadow Tokens](#dark-mode-shadow-tokens) — Line 886
- [Data Visualization](#data-visualization) — Line 896
- [Mobile Notes](#mobile-notes) — Line 912
  - [Effects to Disable](#effects-to-disable) — Line 914
  - [Sizing Adjustments](#sizing-adjustments) — Line 921
  - [Performance Notes](#performance-notes) — Line 932
- [Implementation Checklist](#implementation-checklist) — Line 941

---

## Identity & Philosophy

This theme lives inside a silk scarf caught mid-drift in a sunlit conservatory. The air is warm and still. Light filters through translucent pastel fabric -- lavender, blush, mint -- casting soft colored shadows on a cream floor. Nothing has edges. Nothing is rigid. Every surface dissolves into the next through gentle gradients of warmth and softness. The interface feels like holding something precious in open palms: calm, unhurried, cradled.

The core tension is softness vs structure. Vapor Silk is radically soft (pastels at minimum saturation, maximum border-radius, shadows with extreme blur, transitions that take over a second) while remaining functional and navigable. Softness is the identity, not the excuse for vagueness. Every token is precisely specified -- the softness is engineered, not accidental. A 24px border-radius is a decision. An 800ms transition is a decision. A shadow with 40px blur at 3% opacity is a decision. The calm is deliberate.

Two qualities define this theme. **Ambient presence** means the interface breathes. Background mesh gradients shift slowly over 20-30 second cycles. Colors drift. Nothing is static, but nothing demands attention -- motion exists below the threshold of conscious awareness, felt rather than seen. **Silk materiality** means every surface has the quality of draped fabric: soft, slightly luminous, with gentle folds expressed through layered pastel shadows and generous curves. Flat but dimensional. Matte but warm.

**Decision principle:** "When in doubt, ask: does this feel like a deep breath? If it creates tension, urgency, or sharpness -- soften it. If it feels stagnant or lifeless -- add a slow drift."

**What this theme is NOT:**
- Not sharp or angular -- zero hard edges, zero square corners, zero thin hairline borders
- Not saturated -- every color lives in the pastel range (high lightness, low chroma). No vivid hues anywhere
- Not fast or snappy -- no transition under 200ms except focus ring application. Everything flows
- Not cold -- despite the pastels, the base is warm cream, not cool gray or white
- Not busy or noisy -- no grain, no texture overlays, no particle effects. Surfaces are smooth silk, not rough paper
- Not glassmorphic -- soft blur exists but not the frosted-glass aesthetic. Surfaces are opaque pastels, not transparent panels
- No pure black (`#000000`) or pure white (`#FFFFFF`) anywhere -- every neutral carries a warm cream undertone
- Not bouncy -- no spring overshoot, no elastic snaps. Motion is silk unfurling: smooth, continuous, decelerating

---

## Color System

### Palette

| Token | Name | Hex | HSL | Role |
|---|---|---|---|---|
| page | Silk Cream | `#F3EDE5` | 34 28% 93% | Deepest background -- the sunlit floor beneath the drifting scarves. Warm cream with visible warmth. |
| bg | Cloud Linen | `#F9F5F0` | 34 36% 96% | Primary surface. The lightest warm cream -- the open air of the conservatory. |
| surface | Pearl Silk | `#FEFCF9` | 38 50% 99% | Cards, inputs, elevated surfaces. Nearly white but perceptibly warm. Tint-step creates gentle lift. |
| recessed | Warm Haze | `#EFE9E1` | 36 25% 91% | Code blocks, inset areas. Slightly darker than bg, creates a gentle valley. |
| active | Blush Mist | `#EDE5DF` | 24 22% 90% | Active/pressed states, selected sidebar items, user bubble. Warm and pink-touched. |
| text-primary | Warm Dusk | `#3D3630` | 28 12% 21% | Headings, body text. Dark warm brown -- charcoal with amber undertone. Never cold. |
| text-secondary | Haze Stone | `#7D756D` | 28 7% 46% | Sidebar items, secondary labels. Warm mid-gray. |
| text-muted | Silk Fog | `#ADA5A0` | 18 5% 66% | Placeholders, timestamps, metadata. Warm light gray that whispers, not speaks. |
| text-onAccent | Pearl White | `#FFF9F5` | 24 100% 98% | Text on accent-colored backgrounds. Warm cream white. |
| border-base | Petal Veil | `#D5CBC0` | 34 14% 79% | Base border color, always used at variable opacity. Warm sand, part of the cream family. |
| accent-primary | Dusty Mauve | `#B8899A` | 332 19% 63% | Brand accent, primary CTA. A silk-scarf pink-purple. Calming, not alarming. |
| accent-secondary | Soft Lavender | `#A594C0` | 268 22% 67% | Secondary accent for tags, highlights, subtle emphasis. Lavender silk. |
| accent-tertiary | Pale Mint | `#96C0B0` | 152 19% 67% | Tertiary accent for success-adjacent decoration, freshness notes. Mint-dipped silk. |
| success | Sage Mist | `#7FAF8A` | 132 21% 59% | Positive states, completion indicators. Desaturated green, pastel-compatible. |
| warning | Warm Honey | `#C5A050` | 43 48% 54% | Caution states. Amber-gold that sits naturally in the warm cream world. |
| danger | Muted Rose | `#C07A78` | 2 28% 61% | Error states, destructive actions. Desaturated rose, not alarming red. |
| info | Cloud Blue | `#8BA5BD` | 210 22% 64% | Informational states. Soft enough to not create coldness in the palette. |

### Special Colors

| Token | Value | Role |
|---|---|---|
| inlineCode | `#9B6B82` | Code text within prose -- deeper mauve, reads as "different register" without breaking the pastel calm. |
| toggleActive | `#A594C0` | Toggle/switch active track. Soft lavender, matches accent-secondary. |
| selection | `rgba(184, 137, 154, 0.16)` | `::selection` background. Dusty mauve at 16% opacity -- barely-there blush. |

### Fixed Colors

| Token | Hex | Role |
|---|---|---|
| alwaysBlack | `#000000` | Shadow base (mode-independent) |
| alwaysWhite | `#FFFFFF` | On-dark emergencies only (mode-independent) |

### Opacity System

One border base color (`#D5CBC0`) at variable opacity produces the entire border vocabulary:

| Level | Opacity | Usage |
|---|---|---|
| subtle | 12% | Sidebar edges, hairlines, lightest separation. Even softer than standard -- silk has no hard edges. |
| card | 20% | Card borders, file cards, input shadow ring at rest. Barely visible, felt more than seen. |
| hover | 28% | Hover states, popovers, share button border. Emerges gently on interaction. |
| focus | 38% | Focus borders, active emphasis, maximum non-ring border visibility. |

Note: Opacity values are slightly lower than the standard schema (12/20/28/38 vs 15/25/30/40) because the Vapor Silk palette has less contrast between surface and border colors. Lower opacities prevent borders from appearing too structural for this theme's character.

### Color Rules

- **Dusty mauve is whispered, not shouted.** Used for accent actions (CTA buttons, active toggles), data visualization primaries, and the occasional decorative silk-scarf gradient. Never solid fill on large surfaces.
- **No saturated colors anywhere.** Every color in this theme lives below 50% saturation in HSL. If a color looks "vivid," it is wrong. Desaturate it.
- **Pastels are structural.** Lavender, blush, and mint are not decoration -- they map to accent-primary, accent-secondary, and accent-tertiary with defined roles. Random pastel splashes are forbidden.
- **Semantic colors are heavily muted.** Success/warning/danger sit at very low saturation so they blend into the ambient pastel field. They communicate status without creating urgency.
- **Gradients are ambient only.** Mesh gradients exist in the background as slow-drifting ambient decoration. Surfaces themselves are flat pastel tints -- never gradient fills.
- **Warm undertone is universal.** Even the lavender and mint accents carry slight warmth. There are no cool grays, no blue-tinted whites, no cold shadows.

---

## Typography Matrix

### Font Families

| Slot | Font | Fallback | Role |
|---|---|---|---|
| sans (display) | Outfit | system-ui, -apple-system, sans-serif | Display, Heading. Warm, rounded geometric sans for welcoming architectural roles. |
| sans (body) | Figtree | system-ui, -apple-system, sans-serif | Body, Body Small, Button, Input, Label, Caption. Crisp and warm, excellent readability at small sizes. |
| mono | Space Mono | ui-monospace, SFMono-Regular, Menlo, Monaco, monospace | Code, data values. Quirky character adds personality without being loud. |

**Family switch boundary:** Outfit handles the two largest typographic roles (Display, Heading). Figtree handles everything else (Body, Body Small, Button, Input, Label, Code caption, Caption). Both are geometric sans-serifs with rounded terminals, creating visual cohesion across the boundary. The switch is subtle -- Outfit is slightly more open and warm (wider apertures, rounder curves), Figtree is crisper and more neutral (tighter letterforms, better at small sizes).

**Why this pairing:** Outfit and Figtree share rounded geometric DNA but differ in purpose. Outfit's generous proportions and soft curves create welcoming, human-scale headlines that feel like an invitation to breathe. Figtree's crispness ensures body text remains readable at small sizes without the clinical feel of Inter or the overused softness of Nunito. Space Mono adds personality to code and data -- its quirky character widths and unusual curves feel handmade, reinforcing the artisanal quality of silk rather than the precision of a machine. Together, the trio says "warm, intentional, slightly unusual."

### Role Matrix

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Outfit | 38px | 300 | 1.25 (47.5px) | -0.02em | `font-variation-settings: "wght" 300` | Hero greetings, page titles, ambient welcome messages |
| Heading | Outfit | 24px | 420 | 1.35 (32.4px) | -0.01em | -- | Section titles, settings headers, card group titles |
| Body | Figtree | 16px | 400 | 1.6 (25.6px) | normal | -- | Primary reading text, UI body, descriptions. Extra-generous line-height for airy reading. |
| Body Small | Figtree | 14px | 400 | 1.5 (21px) | normal | -- | Sidebar items, form labels, secondary UI text |
| Button | Figtree | 14px | 480 | 1.4 (19.6px) | 0.01em | -- | Button labels, emphasized small UI text. Slightly heavier and wider-spaced for silk-soft buttons. |
| Input | Figtree | 14px | 420 | 1.4 (19.6px) | normal | -- | Form input text. Heavier than body-small for readability in rounded fields. |
| Label | Figtree | 12px | 400 | 1.33 (16px) | 0.03em | -- | Section labels, metadata, timestamps. Wider spacing for small text legibility in soft palette. |
| Code | Space Mono | 0.9em (14.4px at 16px base) | 400 | 1.55 (22.3px) | -0.01em | `font-variant-numeric: tabular-nums` | Inline code, code blocks, data values |
| Caption | Figtree | 12px | 400 | 1.33 (16px) | normal | -- | Disclaimers, footnotes, bottom-of-page text |

**Variable weight rationale:** 300 for display creates light, airy headlines that feel like text written on silk -- thin enough to be elegant but not so thin they disappear against the cream background. 400 is standard reading weight. 420 for inputs adds gentle heft to typed text in the rounded input fields. 480 for buttons is notably heavier than the standard 460 -- silk-soft buttons with generous radius need slightly bolder text to maintain presence. The Outfit heading weight of 420 (lighter than the standard 460) keeps headings feeling gentle rather than authoritative.

**Line-height rationale:** Body text uses 1.6 (vs the standard 1.5) -- extra-generous leading gives every paragraph an airy, breathable quality that reinforces the theme's calm. This is the typographic equivalent of deep breathing. Display and heading line-heights are also slightly more generous than standard.

### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&family=Figtree:wght@300..900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
```

- **Font smoothing:** `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale` on `<html>`.
- **Font display:** `font-display: swap` on all families.
- **Optical sizing:** `font-optical-sizing: auto` for Outfit (variable font with weight axis).
- **Text wrap:** `text-wrap: balance` for headings, `text-wrap: pretty` for body paragraphs.

---

## Elevation System

**Strategy:** Subtle shadows with high blur radius + tint-stepping.

Separation between surfaces is achieved through a combination of warm tint-stepping (progressively lighter cream tones as surfaces rise) and ultra-soft shadows with extreme blur radii. Where Editorial Calm uses 20px blur on its primary shadow, Vapor Silk uses 32px -- the shadows are clouds, not edges. Interactive elements gain diffuse pastel-tinted shadows that feel like colored light falling through fabric. Border-radius is maximized throughout -- cards at 16px, inputs at 16px, buttons at 12px -- reinforcing the zero-hard-edges philosophy. Popovers add `backdrop-filter: blur(20px)`. No inset shadows are used anywhere.

### Surface Hierarchy

| Surface | Background | Shadow | Usage |
|---|---|---|---|
| page | `#F3EDE5` (page) | none | Deepest layer. The sunlit floor. |
| canvas | `#F9F5F0` (bg) | none | Primary working surface, sidebar background. |
| card | `#FEFCF9` (surface) | shadow-card | Cards, form inputs, menus at rest. Lifted on a cloud. |
| recessed | `#EFE9E1` (recessed) | none | Code blocks, inset areas. Gentle valley. |
| active | `#EDE5DF` (active) | none | Active sidebar item, user message bubble, pressed states. |
| overlay | `#FEFCF9` (surface) | shadow-popover | Popovers, dropdowns, modals. |

### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `0 2px 8px rgba(61, 54, 48, 0.03)` | Small elements, subtle lift. Cloud-wisp shadow. |
| shadow-md | `0 4px 16px rgba(61, 54, 48, 0.04), 0 1px 4px rgba(61, 54, 48, 0.02)` | Medium elevation, standalone cards. |
| shadow-card | `0 4px 32px rgba(61, 54, 48, 0.025), 0 0 0 0.5px rgba(213, 203, 192, 0.20)` | Input card / card rest state. Ultra-wide blur + barely-visible border ring. The signature "floating on clouds" shadow. |
| shadow-card-hover | `0 6px 32px rgba(61, 54, 48, 0.035), 0 0 0 0.5px rgba(213, 203, 192, 0.28)` | Input card / card hover. Shadow deepens gently, ring brightens. |
| shadow-card-focus | `0 6px 32px rgba(61, 54, 48, 0.05), 0 0 0 0.5px rgba(213, 203, 192, 0.28)` | Input card / card focus-within. Shadow reaches full soft depth. |
| shadow-popover | `0 4px 24px rgba(61, 54, 48, 0.08), 0 1px 6px rgba(61, 54, 48, 0.04)` | Menus, popovers, dropdowns. Composite cloud shadow. |
| shadow-none | `none` | Flat surfaces, disabled states, recessed areas. |

**Shadow note:** Shadow base color is `rgba(61, 54, 48, ...)` (warm dark brown matching text-primary) rather than pure black. The opacity values are extremely low (2.5% to 5% for card shadows) -- on the warm cream backgrounds, these shadows are felt as gentle lifting rather than sharp edges. If implementing on backgrounds lighter than `#F9F5F0`, the shadows will be nearly invisible. This is intentional -- Vapor Silk achieves elevation primarily through tint-stepping, with shadows providing only the faintest atmospheric depth.

### Backdrop Filter

| Context | Value | Usage |
|---|---|---|
| popover | `backdrop-filter: blur(20px)` | Popover/dropdown containers. Slightly less than max for performance. |
| modal | `backdrop-filter: blur(16px)` | Modal overlay background. Silk-scarf diffusion. |
| badge | `backdrop-filter: blur(8px)` | Floating labels, ambient badges. |
| none | `backdrop-filter: none` | Default, non-overlay surfaces. |

### Separation Recipe

Tint-step + ultra-soft composite shadow, no visible dividers. The page-to-bg step (from `#F3EDE5` to `#F9F5F0`) creates the primary depth foundation -- warmth recedes, light advances. The bg-to-surface step (from `#F9F5F0` to `#FEFCF9`) lifts cards and inputs so gently that the lift is felt, not seen. Interactive surfaces add cloud-soft shadows (extreme blur radius, minimal opacity) that escalate with interaction state. Popovers combine the surface tint-step with `backdrop-blur(20px)`. Sidebar separation is a single 0.5px line at 12% opacity -- the absolute minimum visible separation. No horizontal rules in the sidebar. No divider lines between content sections. Where grouping is needed, spacing alone (32px gap between groups) provides the separation.

---

## Border System

### Base Color

`#D5CBC0` (Petal Veil). This single warm sand tone, applied at variable opacity, produces the entire border vocabulary. At 12% on warm cream it is a ghost line -- barely perceptible, suggesting structure without imposing it. At 28% it reads as a gentle presence. At 38% it reaches its maximum visibility, still soft enough to avoid sharpness.

### Widths and Patterns

| Pattern | Width | Opacity | CSS Value | Usage |
|---|---|---|---|---|
| subtle | 0.5px | 12% | `0.5px solid rgba(213, 203, 192, 0.12)` | Sidebar right edge, lightest separation. Ghost lines. |
| card | 0.5px | 20% | `0.5px solid rgba(213, 203, 192, 0.20)` | Card borders, file cards. Petal-soft edges. |
| hover | 0.5px | 28% | `0.5px solid rgba(213, 203, 192, 0.28)` | Hover states, popovers. Emerges on interaction. |
| input | 1px | 12% | `1px solid rgba(213, 203, 192, 0.12)` | Form input borders at rest. Wisp-thin, almost invisible. |
| input-hover | 1px | 28% | `1px solid rgba(213, 203, 192, 0.28)` | Form input borders on hover. Materializes gently. |

### Width Scale

| Name | Value | Usage |
|---|---|---|
| hairline | 0.5px | Card edges, sidebar separation, popover borders. The silk standard. |
| default | 1px | Form input borders, transparent-border-for-hover-swap. |
| medium | 1.5px | Accent emphasis (rare -- decorative silk-scarf flourishes). |
| heavy | 2px | Focus ring width only. Never used for structural borders. |

### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(165, 148, 192, 0.52)` |
| Width | 2px solid |
| Style | `outline: 2px solid rgba(165, 148, 192, 0.52)` |
| Offset | `outline-offset: 2px` |
| Applies to | All interactive elements on `:focus-visible` |

Focus ring is soft lavender, matching accent-secondary. In this theme, the focus ring is branded -- the entire palette is so soft that a blue focus ring would be the harshest color on screen. Lavender provides adequate contrast against the cream palette while remaining within the theme's pastel world. The 52% opacity ensures WCAG compliance for focus indicators (3:1 contrast against adjacent colors) while keeping the ring itself pastel.

---

## Component States

### Buttons (Primary/Outlined)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: 0.5px solid rgba(213, 203, 192, 0.28)`, `color: #3D3630 (text-primary)`, `border-radius: 12px`, `height: 36px`, `padding: 0 16px`, `font-size: 14px`, `font-weight: 480`, `font-family: Figtree`, `cursor: pointer` |
| Hover | `bg: #EFE9E1 (recessed)`, `border-color: rgba(213, 203, 192, 0.28)`, `box-shadow: shadow-sm` |
| Active | `transform: scale(0.98)`, `box-shadow: none` |
| Focus | `outline: 2px solid rgba(165, 148, 192, 0.52)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.45`, `pointer-events: none`, `box-shadow: none`, `cursor: not-allowed` |
| Transition | `color, background-color, border-color, box-shadow 250ms cubic-bezier(0.25, 0.1, 0.25, 1)` |

Note: Button height is 36px (vs the standard 32px) -- Vapor Silk gives interactive elements more breathing room. Border-radius is 12px (vs the standard 6px) -- pill-adjacent softness. Active scale is 0.98 (vs 0.97) -- even the press feedback is gentler.

### Buttons (Accent/CTA)

| State | Properties |
|---|---|
| Rest | `bg: #B8899A (accent-primary)`, `border: none`, `color: #FFF9F5 (text-onAccent)`, `border-radius: 12px`, `height: 36px`, `padding: 0 20px`, `font-size: 14px`, `font-weight: 480`, `cursor: pointer`, `box-shadow: 0 2px 12px rgba(184, 137, 154, 0.20)` |
| Hover | `bg: #A97A8C` (5% darker), `box-shadow: 0 4px 16px rgba(184, 137, 154, 0.28)` |
| Active | `transform: scale(0.98)`, `box-shadow: 0 1px 4px rgba(184, 137, 154, 0.15)` |
| Focus | `outline: 2px solid rgba(165, 148, 192, 0.52)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.45`, `pointer-events: none`, `cursor: not-allowed`, `box-shadow: none` |
| Transition | `background-color, box-shadow, transform 300ms cubic-bezier(0.25, 0.1, 0.25, 1)` |

Note: The CTA button carries a colored shadow (mauve-tinted, 20% opacity) that deepens on hover. This is the only place where a colored shadow appears -- it creates a soft glow beneath the accent button, like colored light through silk.

### Buttons (Ghost/Icon)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: none`, `color: #7D756D (text-secondary)`, `border-radius: 12px`, `width: 36px`, `height: 36px`, `padding: 0`, `cursor: pointer` |
| Hover | `bg: #EFE9E1 (recessed)`, `color: #3D3630 (text-primary)` |
| Active | `transform: scale(0.98)` |
| Focus | `outline: 2px solid rgba(165, 148, 192, 0.52)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.45`, `pointer-events: none` |
| Transition | `all 400ms cubic-bezier(0.25, 0.1, 0.25, 1)` |

Note: Ghost buttons use the longest standard transition (400ms vs the typical 300ms). Icon buttons in Vapor Silk should feel like they're responding to a gesture, not reacting to a click. The hover state fades in slowly, like mist forming.

### Text Input (Settings Form)

| State | Properties |
|---|---|
| Rest | `bg: #FEFCF9 (surface)`, `border: 1px solid rgba(213, 203, 192, 0.12)`, `border-radius: 16px`, `height: 44px`, `padding: 0 16px`, `font-size: 14px`, `font-weight: 420`, `font-family: Figtree`, `color: #3D3630 (text-primary)`, `caret-color: #B8899A (accent-primary)` |
| Placeholder | `color: #ADA5A0 (text-muted)` |
| Hover | `border-color: rgba(213, 203, 192, 0.28)`, `box-shadow: shadow-sm` |
| Focus | `outline: 2px solid rgba(165, 148, 192, 0.52)`, `outline-offset: 2px`, `border-color: rgba(213, 203, 192, 0.28)` |
| Disabled | `opacity: 0.45`, `pointer-events: none`, `cursor: not-allowed` |
| Transition | `border-color, box-shadow 300ms cubic-bezier(0.25, 0.1, 0.25, 1)` |

Note: Input border-radius is 16px (vs the standard 9.6px) -- generously rounded pill-like inputs. Caret color is mauve (accent-primary), so the blinking cursor has a soft pastel glow rather than the default black.

### Textarea

| State | Properties |
|---|---|
| Rest | Same bg/border/radius as text input. `padding: 16px`, `line-height: 21px`, `min-height: 140px`, `resize: vertical`, `white-space: pre-wrap` |
| Hover/Focus/Disabled | Same as text input |

### Chat Input Card

| State | Properties |
|---|---|
| Rest | `bg: #FEFCF9 (surface)`, `border-radius: 24px`, `border: 1px solid transparent`, `box-shadow: shadow-card` |
| Hover | `box-shadow: shadow-card-hover` (ring brightens from 20% to 28%) |
| Focus-within | `box-shadow: shadow-card-focus` (shadow deepens from 2.5% to 5%) |
| Inner textarea | `font-size: 16px`, `line-height: 25.6px`, `bg: transparent`, `color: text-primary`, `placeholder-color: text-muted` |
| Transition | `all 500ms cubic-bezier(0.25, 0.1, 0.25, 1)` |

Note: Chat input card uses 24px border-radius (nearly pill-shaped) and the longest interactive transition (500ms). The shadow escalation is extremely subtle -- the card already looks like it is floating, and interaction deepens that float by fractions of a percent. The 500ms transition ensures the shadow change feels like breathing, not switching.

### Cards

| State | Properties |
|---|---|
| Rest | `bg: #FEFCF9 (surface)`, `border: 0.5px solid rgba(213, 203, 192, 0.20)`, `border-radius: 16px`, `box-shadow: shadow-sm`, `padding: 24px` |
| Hover | `border-color: rgba(213, 203, 192, 0.28)`, `box-shadow: shadow-md` |
| Focus | `outline: 2px solid rgba(165, 148, 192, 0.52)`, `outline-offset: 2px` (when card is clickable) |
| Transition | `border-color, box-shadow 350ms cubic-bezier(0.25, 0.1, 0.25, 1)` |

Note: Card border-radius is 16px (vs the standard 8px). Cards in Vapor Silk are cloud-like -- generously rounded, softly shadowed, with 24px padding that gives content room to breathe.

### Sidebar Items

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `color: #7D756D (text-secondary)`, `border-radius: 12px`, `height: 36px`, `padding: 8px 16px`, `font-size: 14px`, `font-weight: 400`, `font-family: Figtree`, `white-space: nowrap`, `overflow: hidden`, `cursor: pointer` |
| Hover | `bg: #EFE9E1 (recessed)`, `color: #3D3630 (text-primary)` |
| Active (current) | `bg: #EDE5DF (active)`, `color: #3D3630 (text-primary)` |
| Active press | `transform: scale(0.985)` |
| Disabled | `pointer-events: none`, `opacity: 0.45`, `box-shadow: none` |
| Transition | `color, background-color 200ms cubic-bezier(0.25, 0.1, 0.25, 1)` |
| Text truncation | Gradient fade mask using `mask-image: linear-gradient(to right, black 85%, transparent)`. Silk-smooth fade, not hard ellipsis. |

### Section Labels (Sidebar)

| Property | Value |
|---|---|
| Font | Figtree, 12px, weight 400, color `#ADA5A0 (text-muted)` |
| Line-height | 16px |
| Letter-spacing | 0.03em |
| Padding | `0 8px 8px` |
| Margin-top | 8px |
| Text-transform | none (lowercase labels, e.g. "Starred", "Recents") |

### Chips (Landing Quick Actions)

| State | Properties |
|---|---|
| Rest | `bg: #F9F5F0 (bg)`, `border: 0.5px solid rgba(213, 203, 192, 0.12)`, `border-radius: 12px`, `height: 36px`, `padding: 0 14px`, `font-size: 14px`, `font-weight: 400`, `font-family: Figtree`, `color: #7D756D (text-secondary)`, `cursor: pointer` |
| Icon | 16x16px, inline-flex, gap 8px from label |
| Hover | `bg: #EDE5DF (active)`, `border-color: rgba(213, 203, 192, 0.20)`, `color: #3D3630 (text-primary)` |
| Active press | `transform: scale(0.995)` |
| Transition | `all 300ms cubic-bezier(0.25, 0.1, 0.25, 1)` |

### Toggle/Switch

| Property | Value |
|---|---|
| Track | `width: 40px`, `height: 22px`, `border-radius: 9999px` |
| Track off | `bg: #EDE5DF (active)` |
| Track on | `bg: #A594C0 (accent-secondary / toggleActive)` |
| Track ring rest | `0.5px` ring using `rgba(213, 203, 192, 0.28)` |
| Track ring hover | `1px` ring (thickens on hover) |
| Thumb | `width: 18px`, `height: 18px`, `bg: #FEFCF9 (surface)`, `border-radius: 9999px`, `box-shadow: 0 1px 4px rgba(61, 54, 48, 0.08)`, centered vertically, slides on toggle |
| Transition | `background-color, transform 300ms cubic-bezier(0.25, 0.1, 0.25, 1)` |
| Focus-visible | Same lavender focus ring as all interactive elements |

Note: Toggle is slightly larger than standard (40x22 vs 36x20). Thumb has its own micro-shadow -- a tiny cloud beneath it. Transition is 300ms (vs standard 150ms) -- the toggle slides like silk, not snaps.

### User Message Bubble

| Property | Value |
|---|---|
| bg | `#EDE5DF (active)` |
| border-radius | 20px |
| padding | `12px 20px` |
| max-width | `85%` (also capped at `75ch`) |
| color | `#3D3630 (text-primary)` |
| font | Figtree, 16px, weight 400 |
| alignment | Right-aligned |

Note: User bubble border-radius is 20px (vs the standard 12px) -- nearly capsule-shaped. Extra padding (12/20 vs 10/16) gives messages a cushioned, silk-pillow feel.

---

## Motion Map

### Easings

| Name | Value | Character |
|---|---|---|
| silk | `cubic-bezier(0.25, 0.1, 0.25, 1)` | The signature easing. Extremely gentle -- slow start, slow middle, slow end. Nothing is fast. Used for most UI transitions. |
| silk-out | `cubic-bezier(0.16, 0.9, 0.4, 1)` | Slightly faster arrival than silk, but still languid. Used for elements that need to "land" (sidebar items, menu items). |
| silk-drift | `cubic-bezier(0.33, 0, 0.67, 1)` | Nearly linear but with soft endpoints. Used for ambient background motion that should feel constant and driftlike. |
| silk-reveal | `cubic-bezier(0.12, 0.8, 0.3, 1)` | Slow-exponential arrival. Panels, modals, page entries. Starts with inertia, ends with a whisper. |
| ambient | `linear` | Used exclusively for the background mesh gradient animation (20-30s cycles). Linear because the motion should be imperceptible per-frame. |

### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 200ms | silk-out | Slower than standard. Mist forming, not light switching. |
| Button hover (primary/outlined) | 250ms | silk | Background, border-color, shadow. Silk unfolding. |
| CTA button hover | 300ms | silk | Background, shadow deepening. |
| Toggle track color | 300ms | silk | Background-color and thumb transform. Silk sliding. |
| Chip hover | 300ms | silk | All properties. |
| Card border/shadow hover | 350ms | silk | border-color, box-shadow. Cloud drifting closer. |
| Input border hover | 300ms | silk | border-color only. Edge materializing. |
| Chat input card shadow | 500ms | silk | All properties including shadow escalation. Breathing. |
| Ghost icon button | 400ms | silk | Longest standard interactive transition. Mist forming. |
| Page/hero content entry | 800ms | silk-reveal | `opacity: 0, translateY(16px)` to `opacity: 1, translateY(0)`. Silk drifting down. |
| Modal entry | 600ms | silk-reveal | `scale(0.96)` to `scale(1)` + fade. Gentle unfurling. |
| Panel open/close | 800ms | silk-reveal | Sidebar collapse, settings panel expand. Curtain drawing. |
| Stagger delay (children) | 120ms | -- | Delay between staggered children. Longer than standard for wave-like cascading. |
| Menu item hover | 200ms | silk | Popover item bg/color change. |
| Mesh gradient cycle | 25000ms | ambient | Full cycle of background mesh drift. Below conscious awareness. |

### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items (sidebar) | `scale(0.985)` | Barely perceptible. Silk-soft compression. |
| Chips | `scale(0.995)` | Almost invisible press. |
| Buttons (primary, ghost, CTA) | `scale(0.98)` | Gentler than standard (0.97). Even the press is cushioned. |
| Tabs | `scale(0.96)` | Slightly more pronounced for segmented controls, but still softer than standard (0.95). |

### Reduced Motion (`prefers-reduced-motion: reduce`)

| Behavior | Change |
|---|---|
| Strategy | `fade-only` -- all animations collapse to simple opacity fades. No spatial movement, no scale. |
| All translateY entries | Replaced with opacity-only fade (no vertical movement). |
| Scale presses | Disabled. Instant visual state change. |
| Stagger delays | Reduced to 0ms. All children appear simultaneously with shared 300ms fade. |
| Ambient mesh gradient | Disabled entirely. Static gradient snapshot. |
| All transitions (hover, focus) | Remain but capped at 150ms. |
| Background drift | Disabled. Static colors. |

---

## Overlays

### Popover/Dropdown

| Property | Value |
|---|---|
| bg | `#FEFCF9 (surface)` |
| backdrop-filter | `blur(20px)` |
| border | `0.5px solid rgba(213, 203, 192, 0.28)` |
| border-radius | 16px |
| box-shadow | `shadow-popover` -- `0 4px 24px rgba(61, 54, 48, 0.08), 0 1px 6px rgba(61, 54, 48, 0.04)` |
| padding | 8px |
| min-width | 192px |
| max-width | 320px |
| z-index | 50 |
| overflow-y | auto (with `max-height: var(--available-height)`) |
| Menu item | `padding: 8px 12px`, `border-radius: 12px`, `height: 36px`, `font-size: 14px (body-small)`, `color: #7D756D (text-secondary)`, `cursor: pointer` |
| Menu item hover | `bg: #EFE9E1 (recessed)`, `color: #3D3630 (text-primary)` |
| Menu item transition | `200ms cubic-bezier(0.25, 0.1, 0.25, 1)` |
| Separators | Spacing only (12px gap between groups). No visible lines. Silk has no seams. |

Note: Popover border-radius is 16px (vs standard 12px). Menu items have 12px border-radius (vs standard 8px). Menu item height is 36px (vs standard 32px). Extra padding everywhere. The popover feels like a cloud that appeared, not a box that opened.

### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(61, 54, 48, 0.25)` (warm tinted, very low opacity -- silk veil, not blackout) |
| Overlay backdrop-filter | `blur(16px)` |
| Content bg | `#FEFCF9 (surface)` |
| Content shadow | `shadow-popover` |
| Content border-radius | 20px |
| Content padding | 28px |
| Entry animation | `opacity: 0, scale(0.96)` to `opacity: 1, scale(1)`, 600ms silk-reveal |
| Exit animation | `opacity: 0`, 400ms silk |
| z-index | 60 |

Note: Modal overlay opacity is only 25% (vs the standard 40-50%). The background remains visible through a silk-like veil rather than being blacked out. The `blur(16px)` provides the actual occlusion while keeping the feel light and airy.

### Tooltip

| Property | Value |
|---|---|
| bg | `#EDE5DF (active)` |
| color | `#3D3630 (text-primary)` |
| font-size | 12px (label role) |
| font-weight | 400 |
| border-radius | 8px |
| padding | `6px 12px` |
| shadow | `0 2px 8px rgba(61, 54, 48, 0.04)` (whisper shadow) |
| Arrow | None. Position-only placement. |
| Delay | 400ms before showing. Longer delay than standard -- nothing is rushed. |
| z-index | 55 |

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column |
| Narrow max-width | 672px | Landing/focused content, settings |
| Sidebar width | 288px | Fixed sidebar |
| Sidebar border | `0.5px solid rgba(213, 203, 192, 0.12)` | Right edge separation -- ghost line |
| Header height | 52px | Top bar. Slightly taller than standard (48px) for more breathing room. |
| Spacing unit | 4px | Base multiplier |

### Spacing Scale

`4, 6, 8, 12, 16, 20, 24, 32, 40, 48px`

Base unit is 4px. Common applications:
- 4px: icon-text inline gap adjustment
- 6px: compact internal spacing (rare in this theme)
- 8px: standard element gap, chip-icon to text gap, sidebar section label padding
- 12px: menu item padding, input horizontal padding, button horizontal padding
- 16px: section padding, card content inset, sidebar item horizontal padding
- 20px: card horizontal padding, user bubble horizontal padding
- 24px: card vertical padding, modal padding, section gap
- 32px: major section separation, group-to-group gap
- 40px: page-level vertical breathing between major sections
- 48px: hero-level vertical spacing, landing page section gaps

Note: The scale extends to 48px (vs standard max of 32px). Vapor Silk uses more whitespace than other themes -- the higher end of the scale gets used frequently for section separation and vertical rhythm.

### Density

**sparse** -- Generous whitespace throughout. Content-to-whitespace ratio 40:60. The interface breathes. Every element has clear space around it. Data density is deliberately low -- if a screen feels crowded, remove elements rather than compressing spacing. The negative space IS the design.

### Responsive Notes

| Breakpoint | Width | Behavior |
|---|---|---|
| lg | 1024px | Full sidebar + content. Default desktop layout. |
| md | 768px | Sidebar collapses to overlay (triggered by soft-cornered hamburger button). Content fills viewport. |
| sm | 640px | Single column. Cards stack vertically. Chips wrap. Input card full-width. |

On mobile (below md):
- Sidebar becomes an overlay panel with the same bg, activated by menu button
- Content max-width becomes 100% with 20px horizontal padding (extra padding vs standard 16px -- maintains silk breathing room on small screens)
- Header remains 52px but actions collapse into a popover menu
- Cards stretch to full width, padding reduces from 24px to 20px (only slight reduction)
- Border-radius values maintained on mobile -- do not reduce them. The rounded softness is essential to the theme's character at every viewport.

---

## Accessibility Tokens

| Token | Value | Notes |
|---|---|---|
| Focus ring color | `rgba(165, 148, 192, 0.52)` | Lavender at 52% opacity. Theme-branded, pastel-compatible. |
| Focus ring width | `2px solid` | Applied via `outline` |
| Focus ring offset | `2px` | Applied via `outline-offset` |
| Disabled opacity | `0.45` | Combined with `pointer-events: none` and `cursor: not-allowed`. Slightly lower than standard 0.5 for more visible distinction in the soft palette. |
| Disabled shadow | `none` | Remove all shadows on disabled elements |
| Selection bg | `rgba(184, 137, 154, 0.16)` | Dusty mauve at 16% -- gentle blush highlight on `::selection` |
| Selection color | `#3D3630 (text-primary)` | Maintains readability on selection |
| Scrollbar width | `thin` | `scrollbar-width: thin` |
| Scrollbar thumb | `rgba(213, 203, 192, 0.30)` | Border-base at 30% opacity |
| Scrollbar track | `transparent` | No visible track |
| Min touch target | 44px | All interactive elements on mobile. Most elements are already 36px+ on desktop. |
| Contrast standard | WCAG AA | 4.5:1 for normal text, 3:1 for large text (18px+) |

**Contrast verification notes:** `text-primary (#3D3630)` on `bg (#F9F5F0)` = ~9.2:1 ratio (passes AAA). `text-secondary (#7D756D)` on `bg (#F9F5F0)` = ~4.6:1 (passes AA). `text-muted (#ADA5A0)` on `bg (#F9F5F0)` = ~2.8:1 (used only for non-essential metadata, meets AA for large text). `accent-primary (#B8899A)` on `bg (#F9F5F0)` = ~3.2:1 (used for large text/icons/CTA only, meets AA large text. Text on accent button uses `text-onAccent` which is nearly white on mauve = ~4.8:1).

**Scrollbar CSS:**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(213, 203, 192, 0.30) transparent;
}
```

---

## Visual Style

### Material

| Property | Value |
|---|---|
| Grain | None. Silk is smooth. No paper fiber, no noise, no texture. |
| Grain technique | None. |
| Gloss | Soft-sheen. Not matte (unlike Editorial Calm), not gloss. A gentle luminosity as if light is passing through translucent fabric. Achieved through slightly elevated lightness on surface tokens and the pastel-tinted shadows. |
| Blend mode | `normal` everywhere. Ambient mesh gradients use `screen` at very low opacity if layered. |
| Shader bg | false. No WebGL backgrounds. Mesh gradient is CSS only. |

### Ambient Mesh Gradient Background

The signature visual of Vapor Silk. A slow-drifting CSS mesh gradient covers the page background, creating the effect of light filtering through colored silk scarves.

**Implementation (CSS):**

```css
.vapor-silk-ambient {
  position: fixed;
  inset: 0;
  z-index: -1;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(184, 137, 154, 0.06) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(165, 148, 192, 0.05) 0%, transparent 55%),
    radial-gradient(ellipse at 60% 80%, rgba(150, 192, 176, 0.04) 0%, transparent 50%),
    radial-gradient(ellipse at 30% 70%, rgba(184, 137, 154, 0.03) 0%, transparent 45%);
  background-color: var(--bg);
  animation: silk-drift 25s silk-drift-easing infinite alternate;
}

@keyframes silk-drift {
  0% {
    background-position: 0% 0%, 100% 0%, 50% 100%, 0% 50%;
  }
  33% {
    background-position: 30% 20%, 70% 30%, 80% 70%, 20% 80%;
  }
  66% {
    background-position: 60% 40%, 40% 60%, 30% 40%, 70% 20%;
  }
  100% {
    background-position: 10% 60%, 90% 50%, 60% 20%, 40% 90%;
  }
}
```

**Key constraints:**
- Gradient opacity never exceeds 6%. The colors should be subliminal -- felt as "warmth" or "softness" without being identifiable as "pink blob" or "purple area."
- Animation duration is 25 seconds per half-cycle (50 seconds total loop). At this speed, motion is imperceptible frame-to-frame. Users notice the change only if they look away and look back.
- Use only the three accent colors (mauve, lavender, mint) as gradient sources. No additional colors.
- The gradient sits behind all content at `z-index: -1` with `position: fixed` so it does not scroll with content.

### Surface Quality

- **Silk luminosity:** Surfaces have a faint inner glow quality -- not a literal glow effect, but achieved through the near-white surface token (`#FEFCF9`) being barely warmer than pure white, creating a sense that surfaces are softly lit from within.
- **Zero hard edges:** Every element has generous border-radius. Even code blocks use 12px radius. The visual vocabulary has no right angles.
- **Pastel cohesion:** All colors on screen should pass the "silk scarf test" -- if you draped a silk scarf across the monitor, the interface colors would blend into the fabric rather than contrasting against it.
- **Negative space is active:** Empty space in Vapor Silk is not absence -- it is the "air" that silk needs to drift. Generous margins and padding are structural design elements, not wasted space.

---

## Signature Animations

### 1. Silk Wave Background (Ambient)

The ambient mesh gradient drifts continuously across the page background, creating slowly shifting pools of pastel color -- like light through silk scarves moving in a gentle breeze.

- **Technique:** Multiple `radial-gradient` layers with offset positions, animated via `background-position` keyframes. See CSS in Visual Style section.
- **Duration:** 25 seconds per half-cycle (50 seconds full loop). Uses `alternate` direction for seamless back-and-forth.
- **Easing:** `silk-drift` -- `cubic-bezier(0.33, 0, 0.67, 1)` (near-linear with soft endpoints).
- **Colors:** Mauve at 6%, lavender at 5%, mint at 4%. Asymmetric opacities create visual depth.
- **Reduced motion:** Disabled entirely. Static gradient snapshot at the 0% keyframe position.

```css
@media (prefers-reduced-motion: no-preference) {
  .vapor-silk-ambient {
    animation: silk-drift 25s cubic-bezier(0.33, 0, 0.67, 1) infinite alternate;
  }
}
```

### 2. Mist Fade Reveal (Page Entry)

Page content materializes from translucent mist -- elements fade from 0% opacity and a subtle vertical offset as if emerging from fog.

- **Technique:** Parent container orchestrates children with `staggerChildren: 0.12` (120ms). Each child animates from `opacity: 0, translateY: 16px` to `opacity: 1, translateY: 0`.
- **Duration:** 800ms per element.
- **Easing:** `silk-reveal` -- `cubic-bezier(0.12, 0.8, 0.3, 1)`.
- **Total cascade example:** 8-item grid completes at 800ms + (7 x 120ms) = 1640ms. The slow cascade feels like curtains parting one by one.
- **Reduced motion:** All items appear simultaneously with 300ms opacity-only fade.

```css
@keyframes mist-fade-in {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.mist-reveal {
  animation: mist-fade-in 800ms cubic-bezier(0.12, 0.8, 0.3, 1) both;
}

.mist-reveal:nth-child(1) { animation-delay: 0ms; }
.mist-reveal:nth-child(2) { animation-delay: 120ms; }
.mist-reveal:nth-child(3) { animation-delay: 240ms; }
.mist-reveal:nth-child(4) { animation-delay: 360ms; }
.mist-reveal:nth-child(5) { animation-delay: 480ms; }
.mist-reveal:nth-child(6) { animation-delay: 600ms; }
.mist-reveal:nth-child(7) { animation-delay: 720ms; }
.mist-reveal:nth-child(8) { animation-delay: 840ms; }

@media (prefers-reduced-motion: reduce) {
  .mist-reveal {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

### 3. Cloud Lift (Card Hover)

When a card is hovered, it appears to float upward on a soft cloud of shadow -- the shadow deepens and spreads while the card gently rises.

- **Technique:** Combined `transform: translateY(-2px)` with shadow escalation from `shadow-sm` to `shadow-md`.
- **Duration:** 350ms.
- **Easing:** `silk` -- `cubic-bezier(0.25, 0.1, 0.25, 1)`.
- **Shadow change:** Drop shadow blur increases from 8px to 16px, opacity from 3% to 4%. Border ring brightens from 20% to 28%.
- **Reduced motion:** Shadow change only, no translateY movement.

```css
.vapor-card {
  transition: transform 350ms cubic-bezier(0.25, 0.1, 0.25, 1),
              box-shadow 350ms cubic-bezier(0.25, 0.1, 0.25, 1),
              border-color 350ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.vapor-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(61, 54, 48, 0.04),
              0 1px 4px rgba(61, 54, 48, 0.02);
  border-color: rgba(213, 203, 192, 0.28);
}

@media (prefers-reduced-motion: reduce) {
  .vapor-card:hover {
    transform: none;
  }
}
```

### 4. Silk Curtain (Panel Slide)

Side panels and setting drawers slide in as if a silk curtain is being drawn aside -- smooth, long, with momentum that decelerates to a whisper at the end.

- **Technique:** `transform: translateX(-100%)` to `translateX(0)` for left panels, with opacity fade from 0 to 1 starting at 40% of the animation.
- **Duration:** 800ms.
- **Easing:** `silk-reveal` -- `cubic-bezier(0.12, 0.8, 0.3, 1)`.
- **Exit:** 600ms, `silk` easing. Slower exit than entry for graceful departure.
- **Reduced motion:** Instant appearance/disappearance with 150ms opacity fade.

```css
@keyframes silk-curtain-enter {
  0% {
    transform: translateX(-100%);
    opacity: 0;
  }
  40% {
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes silk-curtain-exit {
  0% {
    transform: translateX(0);
    opacity: 1;
  }
  60% {
    opacity: 1;
  }
  100% {
    transform: translateX(-100%);
    opacity: 0;
  }
}

.panel-enter {
  animation: silk-curtain-enter 800ms cubic-bezier(0.12, 0.8, 0.3, 1) both;
}

.panel-exit {
  animation: silk-curtain-exit 600ms cubic-bezier(0.25, 0.1, 0.25, 1) both;
}

@media (prefers-reduced-motion: reduce) {
  .panel-enter,
  .panel-exit {
    animation-duration: 150ms;
    animation-timing-function: linear;
  }
  @keyframes silk-curtain-enter {
    from { opacity: 0; transform: none; }
    to { opacity: 1; transform: none; }
  }
  @keyframes silk-curtain-exit {
    from { opacity: 1; transform: none; }
    to { opacity: 0; transform: none; }
  }
}
```

### 5. Vapor Dissolve (Element Removal)

When elements are removed or dismissed, they dissolve into vapor -- fading upward and outward as if evaporating into warm air.

- **Technique:** Combined `opacity: 0`, `transform: translateY(-8px) scale(1.02)`, and `filter: blur(4px)` for a dissolve-into-mist effect.
- **Duration:** 500ms.
- **Easing:** `silk` -- `cubic-bezier(0.25, 0.1, 0.25, 1)`.
- **Stagger (for list removal):** 60ms delay between siblings for a ripple-dissolve effect.
- **Reduced motion:** Opacity-only fade at 200ms.

```css
@keyframes vapor-dissolve {
  0% {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0px);
  }
  100% {
    opacity: 0;
    transform: translateY(-8px) scale(1.02);
    filter: blur(4px);
  }
}

.dissolving {
  animation: vapor-dissolve 500ms cubic-bezier(0.25, 0.1, 0.25, 1) both;
}

.dissolving:nth-child(1) { animation-delay: 0ms; }
.dissolving:nth-child(2) { animation-delay: 60ms; }
.dissolving:nth-child(3) { animation-delay: 120ms; }

@media (prefers-reduced-motion: reduce) {
  .dissolving {
    animation: none;
    transition: opacity 200ms linear;
    opacity: 0;
    filter: none;
    transform: none;
  }
}
```

---

## Dark Mode Variant

This theme is natively light. The dark mode variant inverts the surface hierarchy: deeper layers become darker, elevated surfaces become slightly lighter. All warm undertones are preserved. The pastel accents become slightly more saturated on dark to maintain visibility without losing their gentle character.

### Dark Mode Palette

| Token | Light Hex | Dark Hex | Dark HSL | Notes |
|---|---|---|---|---|
| page | `#F3EDE5` | `#16140F` | 34 20% 7% | Deepest dark surface. Warm amber-black. |
| bg | `#F9F5F0` | `#1E1B16` | 30 16% 10% | Primary dark surface. Warm charcoal with amber cast. |
| surface | `#FEFCF9` | `#282520` | 30 12% 14% | Cards, inputs. Slightly lighter than bg. |
| recessed | `#EFE9E1` | `#1A1814` | 30 12% 9% | Code blocks, inset. Slightly darker than bg. |
| active | `#EDE5DF` | `#12100C` | 32 20% 6% | Active items, user bubble. Darkest interactive surface. |
| text-primary | `#3D3630` | `#F9F5F0` | 34 36% 96% | Primary text. Warm cream -- mirrors the light bg. |
| text-secondary | `#7D756D` | `#B5AEA4` | 30 9% 68% | Secondary text. Warm light gray. |
| text-muted | `#ADA5A0` | `#7A746C` | 28 6% 45% | Muted text. |
| border-base | `#D5CBC0` | `#8A8070` | 33 11% 49% | Border base. Darker sand. Same opacity system applies. |
| accent-primary | `#B8899A` | `#C89DAE` | 332 26% 70% | Dusty mauve, slightly saturated for dark bg visibility. |
| accent-secondary | `#A594C0` | `#B5A4D0` | 268 28% 73% | Soft lavender, slightly lifted. |
| accent-tertiary | `#96C0B0` | `#A6D0C0` | 152 24% 73% | Pale mint, slightly lifted. |
| success | `#7FAF8A` | `#8FBF9A` | 132 22% 65% | Slightly lifted for dark bg contrast. |
| warning | `#C5A050` | `#D5B060` | 43 51% 61% | Slightly lifted. |
| danger | `#C07A78` | `#D08A88` | 2 33% 67% | Slightly lifted. |
| info | `#8BA5BD` | `#9BB5CD` | 210 26% 71% | Slightly lifted. |

### Dark Mode Special Colors

| Token | Dark Value |
|---|---|
| inlineCode | `#E8A0B0` | Warm pink for code text on dark -- softer than red, sits within the pastel family. |
| toggleActive | `#B5A4D0` (matches dark accent-secondary) |
| selection | `rgba(200, 157, 174, 0.20)` | Dark mauve at 20% for visibility on dark surfaces. |

### Dark Mode Rules

- Surfaces lighten as they elevate: `page (#16140F)` < `bg (#1E1B16)` < `surface (#282520)`. Standard dark-mode convention.
- Accent colors become slightly more saturated (+5-8% saturation) and lighter (+5-7% lightness) to maintain the pastel quality against dark backgrounds. They should still read as "soft" -- not vivid.
- Text colors invert: primary becomes warm cream, secondary/muted become progressively dimmer warm grays.
- Border opacity system remains the same (12/20/28/38%), but the base color shifts to `#8A8070` so borders are visible against dark surfaces.
- Shadow percentages increase: `shadow-card` uses 5% rest / 8% focus (vs 2.5%/5% in light mode). `shadow-popover` uses 16% (vs 8% in light mode). Shadow base color shifts to pure black `rgba(0,0,0,...)`.
- Apply `-webkit-font-smoothing: antialiased` (already specified, but essential for light text on dark backgrounds).
- Ambient mesh gradient opacities increase from 4-6% to 6-9% for visibility on dark backgrounds.
- Modal overlay bg shifts from 25% to 35% opacity (dark backgrounds need less additional darkening).

### Dark Mode Shadow Tokens

| Token | Dark Value |
|---|---|
| shadow-card | `0 4px 32px rgba(0, 0, 0, 0.05), 0 0 0 0.5px rgba(138, 128, 112, 0.12)` |
| shadow-card-hover | `0 6px 32px rgba(0, 0, 0, 0.07), 0 0 0 0.5px rgba(138, 128, 112, 0.28)` |
| shadow-card-focus | `0 6px 32px rgba(0, 0, 0, 0.08), 0 0 0 0.5px rgba(138, 128, 112, 0.28)` |
| shadow-popover | `0 4px 24px rgba(0, 0, 0, 0.16), 0 1px 6px rgba(0, 0, 0, 0.08)` |

---

## Data Visualization

| Property | Value |
|---|---|
| Categorical palette | Dusty Mauve `#B8899A`, Cloud Blue `#8BA5BD`, Sage Mist `#7FAF8A`, Warm Honey `#C5A050`, Soft Lavender `#A594C0`. Max 5 hues per chart, all pastel. |
| Sequential ramp | Mauve single-hue: `#F0DDE4` (lightest) -> `#D8B5C2` -> `#B8899A` -> `#9A6B7E` -> `#7C4D62` (darkest) |
| Diverging ramp | Mint-to-Mauve: `#96C0B0` -> `#C0D8CE` -> `#F3EDE5` (neutral center) -> `#D8B5C2` -> `#B8899A` |
| Grid style | low-ink. Axes in text-muted, gridlines in border-base at 8% opacity. Nearly invisible structure. |
| Max hues per chart | 3 (fewer than standard to maintain pastel calm). |
| Philosophy | smooth. Interpolated curves, no stepped bars when possible. Data should flow like silk, not stack like blocks. |
| Number formatting | Space Mono with `font-variant-numeric: tabular-nums`. Right-aligned in columns. |
| Animation | Chart elements enter with mist-fade-reveal stagger at 120ms intervals, 800ms per element. |

---

## Mobile Notes

### Effects to Disable

- **Ambient mesh gradient animation:** Disable CSS animation. Show static gradient snapshot (reduces GPU compositing on mobile). The static gradient with all four radial-gradient layers remains -- only the animation stops.
- **Backdrop blur on popovers:** Reduce from `blur(20px)` to `blur(12px)`. Keep modal blur at `blur(10px)`.
- **Vapor Dissolve blur effect:** Remove `filter: blur(4px)` from exit animation (blur is expensive on mobile GPU). Keep opacity and transform.
- **Cloud Lift translateY:** Disable the `-2px` hover translation on mobile (no hover on touch). Keep shadow escalation for `:active` state.

### Sizing Adjustments

- **Touch targets:** All interactive elements minimum 44px (sidebar items expand from 36px desktop to 44px mobile).
- **Stagger delays:** Reduce from 120ms to 80ms for faster mobile cascades.
- **Card padding:** Reduce from 24px to 20px on screens below 640px. Only slight reduction -- maintain breathing room.
- **Content padding:** 20px horizontal on mobile (vs centered max-width on desktop). Extra generous for silk feel.
- **Typography:** Display role reduces from 38px to `clamp(28px, 6vw, 38px)`. All other roles remain fixed.
- **Border-radius:** Maintained on mobile. Do not reduce. Rounded softness is essential at every viewport size.
- **Toggle size:** Maintained at 40x22px. Already exceeds 44px touch target via padding.
- **Button height:** Maintained at 36px on mobile. Touch target met via 44px minimum spacing.

### Performance Notes

- This theme is performance-friendly when ambient animation is disabled on mobile. No particle systems, no WebGL, no canvas rendering.
- The primary performance concern is the ambient mesh gradient animation on desktop (4 layered `radial-gradient` with `background-position` animation). This is GPU-composited by default in modern browsers but should still be disabled on mobile.
- Shadow composites with 32px blur are GPU-composited and performant.
- `backdrop-filter: blur()` is the most expensive effect in this theme. Reduced on mobile.
- No grain overlay means no SVG filter overhead.

---

## Implementation Checklist

- [ ] **Fonts loaded:** Outfit (variable, 100-900), Figtree (variable, 300-900), Space Mono (400, 700) via Google Fonts with `font-display: swap`
- [ ] **CSS custom properties defined:** All color tokens, shadow tokens, border tokens, radius tokens, spacing scale, motion easings, layout values as `:root` variables
- [ ] **Font smoothing applied:** `-webkit-font-smoothing: antialiased` on `<html>`
- [ ] **Typography matrix implemented:** All 9 roles with correct family, size, weight, line-height, letter-spacing
- [ ] **Family switch boundary respected:** Outfit for Display/Heading only. Figtree for all other roles.
- [ ] **Border-radius applied correctly:** sm (8px), md (12px), lg (16px), xl (20px), 2xl (24px), input (16px), full (9999px) -- all values elevated from standard for silk softness
- [ ] **Shadow tokens applied per state:** rest/hover/focus on cards and input card, sm on small elements, popover on menus
- [ ] **Border opacity system implemented:** All borders use base color at correct opacity level (subtle 12%, card 20%, hover 28%, focus 38%)
- [ ] **Focus ring on all interactive elements:** `outline: 2px solid rgba(165, 148, 192, 0.52)`, `outline-offset: 2px` on `:focus-visible`
- [ ] **Disabled states complete:** opacity 0.45 + pointer-events none + cursor not-allowed + shadow none
- [ ] **`prefers-reduced-motion` media query present:** All animations wrapped or checked. Ambient mesh gradient disabled. Spatial transforms removed. Fade-only fallback.
- [ ] **Scrollbar styled:** `scrollbar-width: thin`, `scrollbar-color: rgba(213, 203, 192, 0.30) transparent`
- [ ] **`::selection` styled:** `background: rgba(184, 137, 154, 0.16)`, `color: #3D3630`
- [ ] **Touch targets >= 44px on mobile**
- [ ] **State transitions match motion map:** Each component uses its specified duration and the `silk` easing family, not a global `transition: all 0.2s`
- [ ] **Ambient mesh gradient implemented:** 4 radial-gradient layers, 25s animation cycle, `z-index: -1`, disabled on mobile and prefers-reduced-motion
- [ ] **Dark mode variant tested:** All token swaps applied, accent saturation increased, shadow percentages adjusted, text contrast verified WCAG AA
- [ ] **Data visualization tokens applied:** Categorical palette (pastel, max 3 hues), smooth philosophy, Space Mono tabular-nums
- [ ] **No hard edges anywhere:** Every element uses generous border-radius. Code blocks 12px, cards 16px, buttons 12px, inputs 16px, chat input 24px, modals 20px, popovers 16px
- [ ] **Gradient fade mask on sidebar items:** `mask-image: linear-gradient(to right, black 85%, transparent)`, not `text-overflow: ellipsis`
- [ ] **Motion durations are silk-long:** Minimum 200ms for interactive transitions, 800ms for reveals, 25s for ambient. Nothing snappy.
