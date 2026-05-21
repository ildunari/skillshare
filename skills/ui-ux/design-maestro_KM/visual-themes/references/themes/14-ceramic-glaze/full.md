# Ceramic Glaze

**Table of Contents**
- [Identity & Philosophy](#identity--philosophy) — line 16
- [Color System](#color-system) — line 29
  - [Palette](#palette) — line 31
  - [Special Colors](#special-colors) — line 55
  - [Fixed Colors](#fixed-colors) — line 63
  - [Opacity System](#opacity-system) — line 69
  - [Color Rules](#color-rules) — line 80
- [Typography Matrix](#typography-matrix) — line 90
  - [Font Families](#font-families) — line 92
  - [Role Matrix](#role-matrix) — line 104
  - [Font Loading](#font-loading) — line 122
- [Elevation System](#elevation-system) — line 138
  - [Surface Hierarchy](#surface-hierarchy) — line 144
  - [Shadow Tokens](#shadow-tokens) — line 156
  - [Backdrop Filter](#backdrop-filter) — line 169
  - [Separation Recipe](#separation-recipe) — line 178
- [Border System](#border-system) — line 183
  - [Base Color](#base-color) — line 185
  - [Widths and Patterns](#widths-and-patterns) — line 187
  - [Width Scale](#width-scale) — line 198
  - [Focus Ring](#focus-ring) — line 206
- [Component States](#component-states) — line 219
  - [Buttons (Primary/Outlined)](#buttons-primaryoutlined) — line 221
  - [Buttons (Accent/CTA)](#buttons-accentcta) — line 232
  - [Buttons (Ghost/Icon)](#buttons-ghosticon) — line 245
  - [Text Input (Settings Form)](#text-input-settings-form) — line 256
  - [Chat Input Card](#chat-input-card) — line 270
  - [Cards](#cards) — line 282
  - [Sidebar Items](#sidebar-items) — line 293
  - [Section Labels (Sidebar)](#section-labels-sidebar) — line 307
  - [Chips (Quick Actions)](#chips-quick-actions) — line 318
  - [Toggle/Switch](#toggleswitch) — line 330
  - [User Message Bubble](#user-message-bubble) — line 345
- [Motion Map](#motion-map) — line 357
  - [Easings](#easings) — line 359
  - [Duration x Easing x Component](#duration-x-easing-x-component) — line 370
  - [Active Press Scale](#active-press-scale) — line 389
  - [Reduced Motion](#reduced-motion-prefers-reduced-motion-reduce) — line 398
- [Overlays](#overlays) — line 412
  - [Popover/Dropdown](#popoverdropdown) — line 414
  - [Modal](#modal) — line 436
  - [Tooltip](#tooltip) — line 452
- [Layout Tokens](#layout-tokens) — line 471
  - [Spacing Scale](#spacing-scale) — line 481
  - [Density](#density) — line 498
  - [Responsive Notes](#responsive-notes) — line 503
- [Accessibility Tokens](#accessibility-tokens) — line 520
- [Visual Style](#visual-style) — line 552
  - [Material](#material) — line 554
  - [Rendering Philosophy](#rendering-philosophy) — line 564
- [Signature Animations](#signature-animations) — line 576
  - [1. Glaze Pool (Cobalt CTA hover)](#1-glaze-pool-cobalt-cta-hover) — line 578
  - [2. Viscous Settle (Page entry)](#2-viscous-settle-page-entry) — line 608
  - [3. Clay Press (Active press feedback)](#3-clay-press-active-press-feedback) — line 655
  - [4. Kiln Glow (Loading/processing state)](#4-kiln-glow-loadingprocessing-state) — line 680
  - [5. Wheel Spin (Toggle transition)](#5-wheel-spin-toggle-transition) — line 713
- [Dark Mode Variant](#dark-mode-variant) — line 756
  - [Dark Mode Palette](#dark-mode-palette) — line 758
  - [Dark Mode Special Colors](#dark-mode-special-colors) — line 779
  - [Dark Mode Rules](#dark-mode-rules) — line 786
  - [Dark Mode Shadow Tokens](#dark-mode-shadow-tokens) — line 799
- [Data Visualization](#data-visualization) — line 809
- [Mobile Notes](#mobile-notes) — line 826
  - [Effects to Disable](#effects-to-disable) — line 828
  - [Sizing Adjustments](#sizing-adjustments) — line 835
  - [Performance Notes](#performance-notes) — line 845
- [Implementation Checklist](#implementation-checklist) — line 853

---

## Identity & Philosophy

This theme lives in a potter's studio at golden hour. The kiln has cooled. On the shelf, bisque-fired bowls wait for their final glaze. The air smells of wet clay and warm minerals. Every surface in this space is rounded -- thrown on a wheel, smoothed by hands, fired until permanent. The cobalt blue glaze pools thicker in the curves of each piece, catching light in dense saturated puddles while thinning to a whisper on the high points. A celadon green vase sits drying nearby. The wood workbench is warm, dusted with fine white porcelain dust.

The core tension is softness vs weight. Everything in this theme is rounded, smooth, and approachable, but nothing floats. Elements have mass. They settle into position with viscous spring physics -- overshooting slightly, resolving slowly, like a lump of clay centering itself on the wheel. The border-radius is generous everywhere (12px minimum for containers, 9999px for pills). Shadows are soft and diffused, like a rounded ceramic piece casting a gentle shadow on a warm wooden table. There is no sharpness -- no sharp corners, no crisp linear animations, no hard grid edges.

Two qualities define this theme. **Tactile weight** -- motion feels heavy, deliberate, viscous. Springs have low stiffness and moderate damping, producing noticeable overshoot that resolves into stillness. Elements feel like they have mass proportional to their size. **Rounded softness** -- every edge, every corner, every transition curve is rounded. The `border-radius` is the primary elevation language. A card with 16px radius and a subtle shadow reads as "above" because it looks like a ceramic tile sitting on the surface.

**Decision principle:** "When in doubt, ask: does this feel like it was shaped by hands on a potter's wheel? If it feels machine-cut, round it. If it feels weightless, add spring damping. If it feels cold, warm it."

**What this theme is NOT:**
- Not sharp or geometric -- no 0px radius, no angular layouts, no triangular decorations
- Not bouncy or playful -- the spring physics are viscous and weighted, not rubbery or cartoon-like
- Not cold or clinical -- every neutral carries a warm bisque undertone
- Not glossy or glassy -- this is fired matte ceramic, not polished glass or chrome
- Not flat/borderless -- subtle shadows with soft spread create the dimensional quality of rounded ceramic objects
- Not fast -- animations settle in 250-400ms, not 75-150ms. Things that move quickly feel weightless, and weight is this theme's signature
- No pure black (`#000000`) or pure white (`#FFFFFF`) anywhere -- every value carries warmth

---

## Color System

### Palette

All neutrals carry a warm yellow-red undertone (hue 28-45 in HSL), evoking bisque-fired clay before glazing. The primary accent is cobalt blue -- the deep, saturated blue of traditional cobalt oxide glaze that pools thick in concave surfaces and thins on convex ones. The secondary accent is celadon green, the classic jade-like glaze of East Asian ceramics. Semantic colors are desaturated to coexist with the warm neutral palette without creating jarring temperature collisions.

| Token | Name | Hex | HSL | Role |
|---|---|---|---|---|
| page | Kiln Stone | `#E6DDD0` | 33 24% 86% | Deepest background -- the wooden workbench beneath the ceramic. Slightly darker than bg, grounding warm tone. |
| bg | Bisque Clay | `#F0E6D6` | 36 45% 89% | Primary surface. The warm bisque tone of unfired clay. The foundation everything sits on. |
| surface | Porcelain Slip | `#F8F3EC` | 35 40% 95% | Cards, inputs, elevated surfaces. The pale cream of liquid porcelain slip. Lighter than bg -- tint-step creates lift. |
| recessed | Raw Clay | `#E8DFD2` | 34 30% 87% | Code blocks, inset areas, recessed panels. Slightly darker than bg, like an unglazed interior. |
| active | Warm Stoneware | `#DDD3C4` | 33 25% 82% | Active/pressed states, selected sidebar items, user bubble. The warm tan of stoneware. |
| text-primary | Fired Umber | `#33291F` | 30 25% 16% | Headings, body text. Deep warm brown-black, like dark clay body after high-fire reduction. |
| text-secondary | Kiln Ash | `#706557` | 30 12% 39% | Sidebar items, secondary labels, icon default color. Warm ash tone. |
| text-muted | Dust | `#9E9487` | 30 10% 57% | Placeholders, timestamps, metadata, section labels. Fine ceramic dust. |
| text-onAccent | Slip White | `#F8F3EC` | 35 40% 95% | Text on accent-colored backgrounds. Warm porcelain white, not pure white. |
| border-base | Kiln Wash | `#C4B8A6` | 34 19% 71% | Base border color, always used at variable opacity. Warm sand, like the kiln wash coating on shelves. |
| accent-primary | Cobalt Glaze | `#2B5EA7` | 215 59% 41% | Brand accent, primary CTA. The signature cobalt oxide glaze -- deep, saturated blue pooling in curves. |
| accent-secondary | Celadon | `#7FAD8E` | 139 22% 59% | Secondary accent, status tags, category badges. The soft jade-green of celadon glaze. |
| success | Copper Green | `#5D9E6A` | 133 26% 49% | Positive states, completion indicators. Like copper oxide glaze turning green in reduction firing. |
| warning | Amber Flux | `#C48B2F` | 39 62% 48% | Caution states. The warm amber of flux-rich glaze pooling at the foot of a pot. |
| danger | Iron Red | `#B84E42` | 6 47% 49% | Error states, destructive actions. The muted red of iron-rich clay, not alarming, clearly different. |
| info | Light Cobalt | `#5E8BC4` | 214 44% 57% | Informational states. A lighter wash of the cobalt accent, clearly related but subordinate. |

### Special Colors

| Token | Value | Role |
|---|---|---|
| inlineCode | `#1E4F8A` | Code text within prose -- dark cobalt, reads as "different register" while staying in the glaze family. |
| toggleActive | `#2B5EA7` | Toggle/switch active track. Cobalt glaze -- same as primary accent for consistency. |
| selection | `rgba(43, 94, 167, 0.16)` | `::selection` background. Cobalt at 16% opacity -- a thin wash of glaze over selected text. |

### Fixed Colors

| Token | Hex | Role |
|---|---|---|
| alwaysBlack | `#000000` | Shadow base (mode-independent) |
| alwaysWhite | `#FFFFFF` | On-dark emergencies only (mode-independent) |

### Opacity System

One border base color (`#C4B8A6`, Kiln Wash) at variable opacity produces the entire border vocabulary:

| Level | Opacity | Usage |
|---|---|---|
| subtle | 15% | Sidebar edges, hairlines, lightest separation, input border at rest |
| card | 25% | Card borders, elevated container edges |
| hover | 30% | Hover states, popovers, interactive border emphasis |
| focus | 40% | Focus borders, active emphasis, maximum non-ring border visibility |

### Color Rules

- **Cobalt is earned.** Used only for primary CTA buttons, active toggles, links, and the primary data visualization series. Never used as decorative fill or large surface color. The cobalt glaze is precious -- applied with intention, not splashed.
- **Celadon is supporting.** Secondary accent for badges, tags, and data viz secondary series. Never competes with cobalt for attention.
- **No gradients on surfaces.** Flat matte ceramic surfaces only. Hierarchy comes from tint-stepping (bg < surface < overlay), not gradient fills. The only acceptable gradient is in data visualization sequential ramps.
- **Semantic colors are desaturated.** Success, warning, danger use ceramic glaze pigment metaphors (copper green, amber flux, iron red) at reduced saturation so they coexist with the warm palette.
- **Warm undertone is universal.** Every neutral, from page to text-primary, carries hue 28-36. There are no cool grays in this palette.
- **The bisque-to-cobalt contrast is the signature.** Warm bisque surfaces with cobalt blue accents create the distinctive tension of this theme -- earthen warmth meeting the cool depth of glaze.

---

## Typography Matrix

### Font Families

| Slot | Font | Fallback | Role |
|---|---|---|---|
| sans (display + heading) | DM Sans | system-ui, -apple-system, sans-serif | Display, Heading, Subheading. Rounded geometric sans -- no sharp corners in the letterforms. Soft, friendly, tactile. |
| sans (body) | Figtree | system-ui, -apple-system, sans-serif | Body, Body Small, Button, Input, Label, Caption. Warm, crisp workhorse. Slightly more personality than a neutral sans. |
| mono | Geist Mono | ui-monospace, SFMono-Regular, Menlo, Monaco, monospace | Code, data values. Modern monospace, clean numerals. |

**Family switch boundary:** DM Sans handles the three largest typographic roles (Display, Heading, Subheading). Figtree handles everything at body level and below (Body, Body Small, Button, Input, Label, Caption). Both are geometric sans-serifs with rounded character -- DM Sans is rounder and softer at display sizes, while Figtree is warmer and more readable at text sizes. The switch is subtle and intentional: DM Sans's rounded terminals and open counters give headlines a soft, sculpted quality that mirrors the rounded ceramic forms. Figtree's slightly crisper letterforms provide the clarity needed for sustained reading.

**Why this pairing:** DM Sans + Figtree share rounded DNA without sharp edges. DM Sans at large sizes feels like letters shaped by hand -- smoothed at every joint, generous bowls, open counters. Figtree at small sizes adds just enough warmth and crispness to be readable without becoming clinical. Neither font has sharp terminals or aggressive geometry. Together they feel like type that was smoothed on a wheel, not cut with a blade. Geist Mono adds a modern counterpoint for code and data -- contemporary but not cold.

### Role Matrix

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | DM Sans | 38px | 300 | 1.2 (45.6px) | -0.02em | `font-optical-sizing: auto` | Hero greetings, page titles. Thin, smooth, sculptural -- like engraved text in fired clay. |
| Heading | DM Sans | 24px | 500 | 1.3 (31.2px) | -0.01em | -- | Section titles, settings headers. Medium weight, round, authoritative but warm. |
| Subheading | DM Sans | 18px | 500 | 1.35 (24.3px) | normal | -- | Card titles, subsection headers. Bridges heading and body. |
| Body | Figtree | 16px | 400 | 1.55 (24.8px) | normal | -- | Primary reading text, UI body, descriptions. Slightly taller line-height than default for warmth and readability. |
| Body Small | Figtree | 14px | 400 | 1.4 (19.6px) | normal | -- | Sidebar items, form labels, secondary UI text. |
| Button | Figtree | 14px | 500 | 1.4 (19.6px) | 0.01em | -- | Button labels, emphasized small UI text. Slightly heavier than body-small for tactile presence. |
| Input | Figtree | 14px | 430 | 1.4 (19.6px) | normal | -- | Form input text. Heavier than body-small for readability in fields. |
| Label | Figtree | 12px | 400 | 1.33 (16px) | 0.02em | -- | Section labels, metadata, timestamps. Slightly tracked for clarity at small sizes. |
| Code | Geist Mono | 0.9em (14.4px at 16px base) | 360 | 1.5 (21.6px) | normal | `font-variant-numeric: tabular-nums` | Inline code, code blocks, data values. |
| Caption | Figtree | 12px | 400 | 1.33 (16px) | normal | -- | Disclaimers, footnotes, bottom-of-page text. |

**Variable weight rationale:** 300 for display creates light, airy headlines that echo the thinness of glaze on a convex surface. 400 is the standard reading weight. 430 for inputs adds enough presence for typed text to feel grounded in the field. 500 for headings, subheadings, and buttons provides weight without the heaviness of 600+ -- everything stays smooth and rounded. These values require variable font loading.

### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Figtree:ital,wght@0,300..900;1,300..900&display=swap" rel="stylesheet">
```

Note: Geist Mono is available via `https://cdn.jsdelivr.net/npm/geist@1/dist/fonts/geist-mono/style.css` or can be self-hosted from the Vercel Geist package.

- **Font smoothing:** `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale` on `<html>`.
- **Font display:** `font-display: swap` on all families.
- **Optical sizing:** `font-optical-sizing: auto` for DM Sans (variable with `opsz` axis).
- **Text wrap:** `text-wrap: balance` for headings, `text-wrap: pretty` for body paragraphs.

---

## Elevation System

**Strategy:** Subtle shadows with soft, rounded edges.

Ceramic Glaze uses rounded shadows as its primary depth language. Every shadow is soft-edged with large spread, mimicking the gentle shadow a rounded ceramic bowl casts on a wooden surface. There are no hard drop shadows, no tight edge shadows, no inset shadows. The roundness of the border-radius works in concert with the diffused shadows to create a sense of physical ceramic objects resting on a warm surface. Popovers add `backdrop-filter: blur(20px)` for a frosted porcelain effect. Sidebar separation uses a single 0.5px hairline at 15% opacity.

### Surface Hierarchy

| Surface | Background | Shadow | Usage |
|---|---|---|---|
| page | `#E6DDD0` (page) | none | Deepest layer. The workbench everything rests on. |
| canvas | `#F0E6D6` (bg) | none | Primary working surface, sidebar background. Bisque clay. |
| card | `#F8F3EC` (surface) | shadow-card | Cards, input areas, menus at rest. Porcelain slip -- slightly lifted. |
| recessed | `#E8DFD2` (recessed) | none | Code blocks, inset areas. Raw, unglazed interior. |
| active | `#DDD3C4` (active) | none | Active sidebar item, user message bubble, pressed states. Warm stoneware. |
| overlay | `#F8F3EC` (surface) | shadow-popover | Popovers, dropdowns, modals. Floating ceramic. |

### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `0 1px 3px rgba(51, 41, 31, 0.04), 0 1px 2px rgba(51, 41, 31, 0.03)` | Small elements, chips, tags. Barely-there lift. |
| shadow-card | `0 2px 8px rgba(51, 41, 31, 0.05), 0 0 0 0.5px rgba(196, 184, 166, 0.20)` | Cards, input containers at rest. Soft diffused shadow + faint border ring. |
| shadow-card-hover | `0 4px 16px rgba(51, 41, 31, 0.07), 0 0 0 0.5px rgba(196, 184, 166, 0.30)` | Card hover. Shadow grows softer and wider, ring brightens. |
| shadow-input | `0 2px 12px rgba(51, 41, 31, 0.04), 0 0 0 0.5px rgba(196, 184, 166, 0.20)` | Input card rest state. Gentle diffused shadow + border ring. |
| shadow-input-hover | `0 3px 16px rgba(51, 41, 31, 0.05), 0 0 0 0.5px rgba(196, 184, 166, 0.30)` | Input card hover. Shadow expands, ring brightens from 20% to 30%. |
| shadow-input-focus | `0 4px 20px rgba(51, 41, 31, 0.07), 0 0 0 0.5px rgba(196, 184, 166, 0.35)` | Input card focus-within. Shadow deepens and widens, ring brightens to 35%. |
| shadow-popover | `0 4px 24px rgba(51, 41, 31, 0.12), 0 2px 6px rgba(51, 41, 31, 0.06)` | Menus, popovers, dropdowns. Dual-layer soft shadow for floating ceramic feel. |
| shadow-none | `none` | Flat surfaces, disabled states, recessed areas. |

**Shadow note:** Shadow base color is `rgba(51, 41, 31, ...)` -- warm umber matching text-primary -- rather than pure black. All shadows use large blur radii to maintain the soft, diffused quality. The shadows should feel like a rounded ceramic piece on a wooden surface, not like a flat card lifting off a page. If implementing on very light backgrounds (lighter than `#F0E6D6`), increase shadow percentages by +2%.

### Backdrop Filter

| Context | Value | Usage |
|---|---|---|
| popover | `backdrop-filter: blur(20px)` | Popover/dropdown containers. Frosted porcelain. |
| modal | `backdrop-filter: blur(10px)` | Modal overlay background. |
| badge | `backdrop-filter: blur(8px)` | Floating labels, status badges. |
| none | `backdrop-filter: none` | Default, non-overlay surfaces. |

### Separation Recipe

Tint-step + soft diffused shadow, no visible dividers. The page-to-bg step (from `#E6DDD0` to `#F0E6D6`) creates the primary depth foundation -- the workbench to the clay. The bg-to-surface step (from `#F0E6D6` to `#F8F3EC`) lifts cards and inputs like ceramic pieces sitting on the table. Interactive surfaces add soft composite shadows (wide diffused drop + tight 0.5px ring) that escalate with interaction state. Popovers combine the surface tint-step with `backdrop-filter: blur(20px)` for a frosted porcelain quality. Sidebar separation is a single 0.5px hairline at 15% opacity. No horizontal rules. No divider lines between content sections. Separation is achieved through surface color and shadow alone.

---

## Border System

### Base Color

`#C4B8A6` (Kiln Wash). This single warm sand tone, applied at variable opacity, produces the entire border vocabulary. At 15% on bisque clay it is barely visible -- like a faint line scored in unfired clay. At 30% it reads as a deliberate edge. At 40% it draws attention for focus states.

### Widths and Patterns

| Pattern | Width | Opacity | CSS Value | Usage |
|---|---|---|---|---|
| subtle | 0.5px | 15% | `0.5px solid rgba(196, 184, 166, 0.15)` | Sidebar right edge, hairlines, lightest separation |
| card | 0.5px | 25% | `0.5px solid rgba(196, 184, 166, 0.25)` | Card borders, container edges (works with shadow-card) |
| hover | 0.5px | 30% | `0.5px solid rgba(196, 184, 166, 0.30)` | Hover states, popovers |
| input | 1px | 15% | `1px solid rgba(196, 184, 166, 0.15)` | Form input borders at rest |
| input-hover | 1px | 30% | `1px solid rgba(196, 184, 166, 0.30)` | Form input borders on hover |

### Width Scale

| Name | Value | Usage |
|---|---|---|
| hairline | 0.5px | Card edges, sidebar separation, popover borders |
| default | 1px | Form input borders, transparent-border-for-hover-swap |
| medium | 1.5px | Heavy emphasis (rare -- only for custom component accents) |
| heavy | 2px | Focus ring width |

### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(43, 94, 167, 0.45)` |
| Width | 2px solid |
| Style | `outline: 2px solid rgba(43, 94, 167, 0.45)` |
| Offset | `outline-offset: 2px` |
| Applies to | All interactive elements on `:focus-visible` |

Focus ring uses cobalt glaze blue at 45% opacity. Unlike many themes that use a generic blue, this focus ring is thematically integrated -- the cobalt glaze IS the accent, so a cobalt focus ring feels native rather than bolted-on. The 45% opacity keeps it visible against bisque backgrounds without being harsh. The ring is rounded by the element's `border-radius`, which reinforces the rounded ceramic language.

---

## Component States

### Buttons (Primary/Outlined)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: 1px solid rgba(196, 184, 166, 0.30)`, `color: #33291F (text-primary)`, `border-radius: 12px`, `height: 36px`, `padding: 0 16px`, `font-size: 14px`, `font-weight: 500`, `font-family: Figtree`, `cursor: pointer` |
| Hover | `bg: #E8DFD2 (recessed)`, `border-color: rgba(196, 184, 166, 0.35)`, `box-shadow: shadow-sm` |
| Active | `transform: scale(0.97)`, `box-shadow: none` |
| Focus | `outline: 2px solid rgba(43, 94, 167, 0.45)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `box-shadow: none`, `cursor: not-allowed` |
| Transition | `color, background-color, border-color, box-shadow, transform 250ms cubic-bezier(0.23, 1.2, 0.52, 1)` |

Note the 12px border-radius on buttons -- larger than most themes, reinforcing the rounded ceramic language. The transition uses the viscous spring easing, producing a slight overshoot on hover that settles.

### Buttons (Accent/CTA)

| State | Properties |
|---|---|
| Rest | `bg: #2B5EA7 (accent-primary)`, `border: none`, `color: #F8F3EC (text-onAccent)`, `border-radius: 12px`, `height: 36px`, `padding: 0 20px`, `font-size: 14px`, `font-weight: 500`, `font-family: Figtree`, `cursor: pointer`, `box-shadow: shadow-sm` |
| Hover | `bg: #244F8E` (darkened cobalt), `box-shadow: 0 2px 12px rgba(43, 94, 167, 0.20)` (cobalt-tinted shadow) |
| Active | `transform: scale(0.97)`, `box-shadow: 0 1px 4px rgba(43, 94, 167, 0.15)` |
| Focus | `outline: 2px solid rgba(43, 94, 167, 0.45)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `cursor: not-allowed`, `box-shadow: none` |
| Transition | `background-color, box-shadow, transform 250ms cubic-bezier(0.23, 1.2, 0.52, 1)` |

The cobalt CTA button gets a cobalt-tinted hover shadow -- the glaze "pools" around the button on hover. This is the signature detail: the accent color bleeds into the shadow space, like glaze running down a vertical surface.

### Buttons (Ghost/Icon)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: none`, `color: #706557 (text-secondary)`, `border-radius: 12px`, `width: 36px`, `height: 36px`, `padding: 0`, `cursor: pointer` |
| Hover | `bg: #E8DFD2 (recessed)`, `color: #33291F (text-primary)` |
| Active | `transform: scale(0.97)` |
| Focus | `outline: 2px solid rgba(43, 94, 167, 0.45)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none` |
| Transition | `all 350ms cubic-bezier(0.23, 1.2, 0.52, 1)` |

Ghost buttons use the slowest button transition (350ms) with viscous spring easing. The color change from secondary to primary feels weighted and considered.

### Text Input (Settings Form)

| State | Properties |
|---|---|
| Rest | `bg: #F8F3EC (surface)`, `border: 1px solid rgba(196, 184, 166, 0.15)`, `border-radius: 12px`, `height: 44px`, `padding: 0 14px`, `font-size: 14px`, `font-weight: 430`, `font-family: Figtree`, `color: #33291F (text-primary)`, `caret-color: #2B5EA7 (accent-primary)` |
| Placeholder | `color: #9E9487 (text-muted)` |
| Hover | `border-color: rgba(196, 184, 166, 0.30)`, `box-shadow: shadow-sm` |
| Focus | `outline: 2px solid rgba(43, 94, 167, 0.45)`, `outline-offset: 2px`, `border-color: rgba(196, 184, 166, 0.30)` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `cursor: not-allowed` |
| Transition | `border-color, box-shadow 250ms cubic-bezier(0.23, 1.2, 0.52, 1)` |

Note the 12px border-radius on inputs (larger than the schema default of 9.6px) and the cobalt caret color -- when typing, the cursor is a thin cobalt line, a thread of glaze inside the clay form. Input height is 44px to meet accessibility touch target requirements.

### Chat Input Card

| State | Properties |
|---|---|
| Rest | `bg: #F8F3EC (surface)`, `border-radius: 24px`, `border: 1px solid transparent`, `box-shadow: shadow-input` |
| Hover | `box-shadow: shadow-input-hover` (shadow expands, ring brightens from 20% to 30%) |
| Focus-within | `box-shadow: shadow-input-focus` (shadow widens and deepens, ring brightens to 35%) |
| Inner textarea | `font-size: 16px`, `line-height: 24.8px`, `bg: transparent`, `color: text-primary`, `placeholder-color: text-muted`, `caret-color: #2B5EA7` |
| Transition | `all 300ms cubic-bezier(0.23, 1.2, 0.52, 1)` |

The chat input card has the largest border-radius (24px) -- it looks like a ceramic bowl from above, a rounded vessel for user input. The transition is 300ms with viscous spring, producing a gentle expansion of the shadow on focus that feels like the card is settling deeper into the surface.

### Cards

| State | Properties |
|---|---|
| Rest | `bg: #F8F3EC (surface)`, `border: 0.5px solid rgba(196, 184, 166, 0.20)`, `border-radius: 16px`, `box-shadow: shadow-card`, `padding: 24px` |
| Hover | `border-color: rgba(196, 184, 166, 0.30)`, `box-shadow: shadow-card-hover` |
| Focus | `outline: 2px solid rgba(43, 94, 167, 0.45)`, `outline-offset: 2px` (when card is clickable) |
| Transition | `border-color, box-shadow 300ms cubic-bezier(0.23, 1.2, 0.52, 1)` |

Cards have 16px border-radius -- the largest of any non-pill element. They look like ceramic tiles or coasters. The shadow escalation on hover (from `shadow-card` to `shadow-card-hover`) feels like gently lifting a ceramic piece off the table -- the shadow grows wider and softer underneath.

### Sidebar Items

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `color: #706557 (text-secondary)`, `border-radius: 12px`, `height: 36px`, `padding: 6px 16px`, `font-size: 14px`, `font-weight: 400`, `font-family: Figtree`, `white-space: nowrap`, `overflow: hidden`, `cursor: pointer` |
| Hover | `bg: #E8DFD2 (recessed)`, `color: #33291F (text-primary)` |
| Active (current) | `bg: #DDD3C4 (active)`, `color: #33291F (text-primary)` |
| Active press | `transform: scale(0.985)` |
| Disabled | `pointer-events: none`, `opacity: 0.5` |
| Transition | `color, background-color 150ms cubic-bezier(0.23, 1.2, 0.52, 1)` |
| Text truncation | Gradient fade mask using `mask-image: linear-gradient(to right, black 85%, transparent)`. Not `text-overflow: ellipsis`. |

Sidebar items at 12px radius match buttons, creating visual consistency across interactive elements. The 36px height (vs 32px standard) gives more vertical breathing room, contributing to the comfortable density.

### Section Labels (Sidebar)

| Property | Value |
|---|---|
| Font | Figtree, 12px, weight 400, color `#9E9487 (text-muted)` |
| Line-height | 16px |
| Padding | `0 8px 8px` |
| Margin-top | 4px |
| Text-transform | none (lowercase labels, e.g. "Starred", "Recents") |
| Letter-spacing | 0.02em |

### Chips (Quick Actions)

| State | Properties |
|---|---|
| Rest | `bg: #F0E6D6 (bg)`, `border: 0.5px solid rgba(196, 184, 166, 0.15)`, `border-radius: 9999px`, `height: 36px`, `padding: 0 14px`, `font-size: 14px`, `font-weight: 400`, `font-family: Figtree`, `color: #706557 (text-secondary)`, `cursor: pointer` |
| Icon | 16x16px, inline-flex, gap 8px from label |
| Hover | `bg: #DDD3C4 (active)`, `border-color: rgba(196, 184, 166, 0.25)`, `color: #33291F (text-primary)` |
| Active press | `transform: scale(0.995)` |
| Transition | `all 250ms cubic-bezier(0.23, 1.2, 0.52, 1)` |

Chips are full-round pills (`border-radius: 9999px`) -- the most extreme expression of the rounded ceramic language. They look like small polished pebbles or kiln pegs.

### Toggle/Switch

| Property | Value |
|---|---|
| Track | `width: 40px`, `height: 22px`, `border-radius: 9999px` |
| Track off | `bg: #DDD3C4 (active)` |
| Track on | `bg: #2B5EA7 (cobalt glaze)` |
| Track ring rest | `0.5px` ring using `rgba(196, 184, 166, 0.25)` |
| Track ring hover | `1px` ring (thickens on hover) |
| Thumb | `width: 18px`, `height: 18px`, `bg: #F8F3EC (surface)`, `border-radius: 9999px`, `box-shadow: 0 1px 3px rgba(51, 41, 31, 0.08)`, centered vertically, slides on toggle |
| Transition | `background-color, transform 300ms cubic-bezier(0.23, 1.2, 0.52, 1)` |
| Focus-visible | Cobalt focus ring as all interactive elements |

The toggle is slightly larger than standard (40x22 vs 36x20) to maintain the generous, rounded quality. The thumb has a subtle shadow, like a small ceramic knob. The 300ms viscous spring transition means the thumb slides with mass -- it overshoots slightly and settles. Toggle track is slightly bigger and rounder for the ceramic feel.

### User Message Bubble

| Property | Value |
|---|---|
| bg | `#DDD3C4 (active)` |
| border-radius | 20px |
| padding | `12px 18px` |
| max-width | `85%` (also capped at `75ch`) |
| color | `#33291F (text-primary)` |
| font | Figtree, 16px, weight 400 |
| alignment | Right-aligned |

The user bubble has 20px radius -- extremely rounded, like a speech bubble formed from clay. The generous padding (12px 18px vs standard 10px 16px) reinforces the comfortable, weighted feel.

---

## Motion Map

### Easings

| Name | Value | Character |
|---|---|---|
| viscous-spring | `cubic-bezier(0.23, 1.2, 0.52, 1)` | The signature easing. Viscous spring approximation -- slight overshoot (1.2 control point) that resolves smoothly. Elements feel like clay settling on a wheel. |
| viscous-spring-heavy | `cubic-bezier(0.18, 1.35, 0.45, 1)` | Heavier overshoot for larger elements (panels, modals). More mass, more settle time. |
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. For micro-interactions that don't need spring character. |
| out-quart | `cubic-bezier(0.165, 0.85, 0.45, 1)` | Snappy deceleration for sidebar items. |
| out-expo | `cubic-bezier(0.19, 1, 0.22, 1)` | Near-instant arrival, long settle. Panel open/close. |
| settle | `cubic-bezier(0.34, 1.1, 0.64, 1)` | Gentle settle with minimal overshoot. Tooltip and badge appearance. |

**Spring physics note:** For Framer Motion / Motion implementations, the viscous spring translates to `type: "spring", stiffness: 150, damping: 15`. This produces approximately 250-400ms settle times with visible overshoot that resolves slowly. The `damping: 15` (lower than the typical 20-30) creates the distinctive "settling like clay" quality -- elements don't snap into place, they ease in with a slight wobble.

### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 150ms | out-quart | Faster than other elements -- sidebar navigation should feel responsive even in a weighted theme. |
| Button hover (primary/outlined) | 250ms | viscous-spring | Background, border-color, shadow. Visible overshoot on bg opacity. |
| Toggle thumb slide | 300ms | viscous-spring | Background-color and thumb transform. Thumb overshoots target position slightly. |
| Chip hover | 250ms | viscous-spring | All properties. |
| Card border/shadow hover | 300ms | viscous-spring | border-color, box-shadow. Shadow "pools" wider with spring ease. |
| Input border hover | 250ms | viscous-spring | border-color, box-shadow. |
| Chat input card shadow | 300ms | viscous-spring | All properties including shadow escalation. |
| Ghost icon button | 350ms | viscous-spring | Slowest button transition. Ghost icons feel heaviest. |
| Page/hero content entry | 400ms | viscous-spring-heavy | `opacity: 0, translateY(16px)` to `opacity: 1, translateY(0)`. Notable overshoot. |
| Modal entry | 350ms | viscous-spring-heavy | `scale(0.92)` to `scale(1)` + fade. Larger scale range than typical (0.92 vs 0.95) for more visible spring settle. |
| Panel open/close | 500ms | out-expo | Sidebar collapse, settings panel expand. |
| Menu item hover | 100ms | default | Popover item bg/color change. Fast within menus. |
| Stagger delay | 100ms | -- | Delay between staggered children. Slightly longer than standard for the weighted feel. |

### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items (sidebar) | `scale(0.985)` | Subtle press. |
| Chips | `scale(0.995)` | Almost invisible press -- pills are already small. |
| Buttons (primary, ghost) | `scale(0.97)` | Standard press feedback. Spring-back with viscous easing. |
| Tabs | `scale(0.95)` | More pronounced for segmented controls. |
| Cards (clickable) | `scale(0.99)` | Very subtle -- large elements should not jump dramatically. |

### Reduced Motion (`prefers-reduced-motion: reduce`)

| Behavior | Change |
|---|---|
| Strategy | `reduced-distance` -- animations still occur but with no spatial movement and no spring overshoot. |
| All translateY entries | Replaced with opacity-only fade (no vertical movement). |
| Scale presses | Disabled. Instant visual state change. |
| Spring overshoot | Eliminated. All easings revert to `cubic-bezier(0.4, 0, 0.2, 1)`. |
| Stagger delays | Reduced to 0ms. All children appear simultaneously with shared fade. |
| Viscous spring transitions | Replaced with 150ms default easing. No overshoot. |
| All transitions (hover, focus) | Remain but capped at 100ms with default easing. |
| Glaze pool animation | Disabled entirely. |
| Kiln shimmer | Disabled entirely. |

---

## Overlays

### Popover/Dropdown

| Property | Value |
|---|---|
| bg | `#F8F3EC (surface)` |
| backdrop-filter | `blur(20px)` |
| border | `0.5px solid rgba(196, 184, 166, 0.30)` |
| border-radius | 16px |
| box-shadow | `shadow-popover` -- `0 4px 24px rgba(51, 41, 31, 0.12), 0 2px 6px rgba(51, 41, 31, 0.06)` |
| padding | 8px |
| min-width | 200px |
| max-width | 320px |
| z-index | 50 |
| overflow-y | auto (with `max-height: var(--available-height)`) |
| Menu item | `padding: 8px 10px`, `border-radius: 12px`, `height: 36px`, `font-size: 14px (body-small)`, `color: #706557 (text-secondary)`, `cursor: pointer` |
| Menu item hover | `bg: #E8DFD2 (recessed)`, `color: #33291F (text-primary)` |
| Menu item transition | `100ms cubic-bezier(0.4, 0, 0.2, 1)` |
| Separators | Spacing only (8px gap between groups). No visible lines. |
| Entry animation | `opacity: 0, scale(0.95), translateY(-4px)` to `opacity: 1, scale(1), translateY(0)`, 300ms viscous-spring |

The popover has 16px border-radius and 8px internal padding, with menu items at 12px radius. This creates a nested rounded container -- like opening a ceramic lidded jar. The entry animation uses viscous spring, so the popover slightly overshoots its final position before settling.

### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(51, 41, 31, 0.35)` (warm umber tinted, not pure black) |
| Overlay backdrop-filter | `blur(10px)` |
| Content bg | `#F8F3EC (surface)` |
| Content shadow | `shadow-popover` |
| Content border-radius | 20px |
| Content padding | 28px |
| Entry animation | `opacity: 0, scale(0.92)` to `opacity: 1, scale(1)`, 350ms viscous-spring-heavy |
| Exit animation | `opacity: 0, scale(0.96)`, 200ms default |
| z-index | 60 |

The modal uses 20px border-radius (the second-largest after the chat input card) and 28px padding. The overlay tint is warm umber rather than pure black. The entry animation starts at `scale(0.92)` -- further from 1.0 than typical -- creating more visible spring settle as the modal "drops" into view with weight.

### Tooltip

| Property | Value |
|---|---|
| bg | `#DDD3C4 (active)` |
| color | `#33291F (text-primary)` |
| font-size | 12px (label role) |
| font-weight | 400 |
| border-radius | 8px |
| padding | `6px 10px` |
| shadow | `shadow-sm` |
| Arrow | None. Position-only placement. |
| Delay | 400ms before showing (longer than standard -- nothing rushes in this theme). |
| Entry animation | `opacity: 0, translateY(2px)` to `opacity: 1, translateY(0)`, 200ms settle easing |
| z-index | 55 |

Tooltips have a small shadow (unlike many flat tooltip implementations) because in this theme, everything that floats casts a soft shadow. The 8px radius is the smallest radius in the theme -- even tooltips are rounded.

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column |
| Narrow max-width | 672px | Landing/focused content, settings |
| Sidebar width | 288px | Fixed sidebar |
| Sidebar border | `0.5px solid rgba(196, 184, 166, 0.15)` | Right edge separation |
| Header height | 48px | Top bar |
| Spacing unit | 4px | Base multiplier |

### Spacing Scale

`4, 6, 8, 12, 16, 20, 24, 28, 32, 40px`

Base unit is 4px. Common applications in this theme:
- 4px: icon-text inline gap adjustment
- 6px: tight internal spacing
- 8px: standard element gap, chip padding, popover internal padding, icon-text gap
- 12px: input horizontal padding, button side padding
- 16px: card group gap, sidebar item horizontal padding, section padding
- 20px: medium section gap
- 24px: card internal padding
- 28px: modal internal padding (generous, like the walls of a thick ceramic bowl)
- 32px: major section separation
- 40px: page-level vertical separation (generous, unhurried)

### Density

**Density:** comfortable

This theme is `comfortable` density -- never cramped, never sparse. The generous border-radii and larger component heights (36px buttons vs 32px standard, 44px inputs) naturally consume more vertical space, and the spacing should support this. Content-to-whitespace ratio: 55:45. Things breathe, but there is always something to look at. The comfortable density mirrors the physical studio: tools are organized but not jammed together, with room to reach for each piece.

### Responsive Notes

| Breakpoint | Width | Behavior |
|---|---|---|
| lg | 1024px | Full sidebar + content. Default desktop layout. |
| md | 768px | Sidebar collapses to overlay (triggered by menu button). Content fills viewport. |
| sm | 640px | Single column. Cards stack vertically. Chips wrap. Input card full-width. |

On mobile (below md):
- Sidebar becomes an overlay panel with the same bg, activated by menu button
- Content max-width becomes 100% with 16px horizontal padding
- Header remains 48px but actions collapse into a popover menu
- Cards stretch to full width, padding reduces from 24px to 20px (still generous)
- Border-radius values remain unchanged -- roundness is non-negotiable on any viewport
- Component heights (36px buttons, 44px inputs) remain unchanged for touch accessibility
- Spacing scale compresses: 40px section gaps reduce to 28px, 32px gaps reduce to 24px

---

## Accessibility Tokens

| Token | Value | Notes |
|---|---|---|
| Focus ring color | `rgba(43, 94, 167, 0.45)` | Cobalt at 45% opacity. Thematic, visible against warm bisque. |
| Focus ring width | `2px solid` | Applied via `outline` |
| Focus ring offset | `2px` | Applied via `outline-offset` |
| Disabled opacity | `0.5` | Combined with `pointer-events: none` and `cursor: not-allowed` |
| Disabled shadow | `none` | Remove all shadows on disabled elements |
| Selection bg | `rgba(43, 94, 167, 0.16)` | Cobalt at 16% -- `::selection` |
| Selection color | `#33291F (text-primary)` | Maintains readability on selection |
| Scrollbar width | `thin` | `scrollbar-width: thin` |
| Scrollbar thumb | `rgba(196, 184, 166, 0.35)` | Kiln-wash at 35% opacity |
| Scrollbar track | `transparent` | No visible track |
| Min touch target | 44px | All interactive elements -- met by default (36px buttons have 44px click area with padding) |
| Contrast standard | WCAG AA | 4.5:1 for normal text, 3:1 for large text (18px+) |

**Contrast verification:**
- `#33291F` (text-primary) on `#F0E6D6` (bg): contrast ratio ~12:1 (passes AAA)
- `#706557` (text-secondary) on `#F0E6D6` (bg): contrast ratio ~4.7:1 (passes AA)
- `#9E9487` (text-muted) on `#F0E6D6` (bg): contrast ratio ~3.2:1 (passes AA for large text only -- muted text is used only for metadata and labels, which are supplementary)
- `#F8F3EC` (text-onAccent) on `#2B5EA7` (cobalt): contrast ratio ~7.5:1 (passes AAA)

**Scrollbar CSS:**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(196, 184, 166, 0.35) transparent;
}
```

---

## Visual Style

### Material

| Property | Value |
|---|---|
| Grain | Subtle (1-2%). Suggests the fine tooth of bisque-fired clay. |
| Grain technique | SVG `feTurbulence` overlay (`baseFrequency="0.9"`, 1 octave, `type="fractalNoise"`) at 1.5% opacity. Slightly coarser than paper grain -- this is clay, not paper. |
| Gloss | Matte. No reflections, no sheens. The surfaces are bisque (unfired) -- only the cobalt accent has the implied sheen of glaze. |
| Blend mode | `normal` everywhere. No multiply blending. |
| Shader bg | false. No WebGL backgrounds. |

### Rendering Philosophy

This theme does not simulate ceramic literally. It borrows the *qualities* of ceramic: warmth, roundness, weight, soft shadows, the contrast between matte clay and glossy glaze (bisque surfaces vs cobalt accent). The grain overlay suggests material texture. The generous radii suggest wheel-thrown forms. The viscous spring motion suggests the inertia of dense material. Together these create an interface that *feels* ceramic without being skeuomorphic.

- **Rounded everything:** The minimum border-radius for any container is 12px. Pills use 9999px. No square corners exist in this theme.
- **Soft shadows everywhere:** Every floating element casts a shadow. The shadows are always diffused (large blur radius, low opacity). No hard-edged shadows.
- **Cobalt pooling effect:** On hover, the cobalt accent CTA button gains a cobalt-tinted shadow (`rgba(43, 94, 167, 0.20)`) that mimics glaze pooling around the base of a ceramic form.
- **Weight in motion:** Every animation takes 250-400ms. Nothing is instant. The viscous spring easing creates a sense of mass -- elements don't snap, they settle.
- **Surface warmth:** All surface colors exist on a warm HSL hue (28-36). There are no cool grays. Even code blocks and recessed areas carry warmth.

---

## Signature Animations

### 1. Glaze Pool (Cobalt CTA hover)

On hover, the cobalt accent button's shadow transitions from a neutral warm shadow to a cobalt-tinted glow that spreads wider, simulating glaze flowing and pooling around the base of a ceramic piece.

- **Technique:** `box-shadow` transition from `0 1px 3px rgba(51, 41, 31, 0.04)` to `0 4px 20px rgba(43, 94, 167, 0.18), 0 2px 8px rgba(43, 94, 167, 0.12)`. The shadow color shifts from neutral umber to saturated cobalt.
- **Duration:** 300ms.
- **Easing:** viscous-spring (`cubic-bezier(0.23, 1.2, 0.52, 1)`).
- **Reduced motion:** Shadow color change only, no size expansion.

```css
.btn-cobalt {
  box-shadow: 0 1px 3px rgba(51, 41, 31, 0.04), 0 1px 2px rgba(51, 41, 31, 0.03);
  transition: box-shadow 300ms cubic-bezier(0.23, 1.2, 0.52, 1),
              background-color 300ms cubic-bezier(0.23, 1.2, 0.52, 1),
              transform 250ms cubic-bezier(0.23, 1.2, 0.52, 1);
}
.btn-cobalt:hover {
  box-shadow: 0 4px 20px rgba(43, 94, 167, 0.18), 0 2px 8px rgba(43, 94, 167, 0.12);
  background-color: #244F8E;
}
.btn-cobalt:active {
  transform: scale(0.97);
  box-shadow: 0 1px 4px rgba(43, 94, 167, 0.15);
}
@media (prefers-reduced-motion: reduce) {
  .btn-cobalt {
    transition: background-color 100ms ease, box-shadow 100ms ease;
  }
}
```

### 2. Viscous Settle (Page entry)

UI elements enter the page with spring physics that produce visible overshoot. Elements slide up from 16px below their final position, overshoot by 2-3px, then settle back. Like placing a clay form on a shelf -- it shifts slightly before finding its rest.

- **Technique:** Staggered children with `opacity: 0, translateY(16px)` to `opacity: 1, translateY(0)`, using viscous spring easing that overshoots.
- **Duration:** 400ms per element.
- **Stagger:** 100ms between siblings.
- **Easing:** viscous-spring-heavy (`cubic-bezier(0.18, 1.35, 0.45, 1)`) -- the 1.35 control point produces ~3px overshoot on a 16px translation.
- **Cascade:** Top-left to bottom-right.

```css
@keyframes viscous-settle {
  0% {
    opacity: 0;
    transform: translateY(16px);
  }
  60% {
    opacity: 1;
    transform: translateY(-3px); /* overshoot */
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
.stagger-item {
  animation: viscous-settle 400ms cubic-bezier(0.18, 1.35, 0.45, 1) both;
}
.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 100ms; }
.stagger-item:nth-child(3) { animation-delay: 200ms; }
.stagger-item:nth-child(4) { animation-delay: 300ms; }
.stagger-item:nth-child(5) { animation-delay: 400ms; }

@media (prefers-reduced-motion: reduce) {
  .stagger-item {
    animation: fade-in 150ms ease both;
    animation-delay: 0ms !important;
  }
  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }
}
```

### 3. Clay Press (Active press feedback)

When a button is pressed, it scales down with viscous spring physics and bounces back with a subtle overshoot -- like pressing a finger into soft clay and watching it spring back.

- **Technique:** On `:active`, `transform: scale(0.97)`. On release, the spring-back uses viscous-spring easing, producing a brief `scale(1.005)` overshoot before settling at `scale(1)`.
- **Duration:** 250ms for press, 350ms for release.
- **Easing:** viscous-spring for release.

```css
.btn-ceramic {
  transition: transform 250ms cubic-bezier(0.23, 1.2, 0.52, 1);
}
.btn-ceramic:active {
  transform: scale(0.97);
  transition-duration: 80ms;
  transition-timing-function: ease-out;
}
/* Spring-back on release is handled by the default transition
   (250ms viscous-spring) which naturally overshoots */
@media (prefers-reduced-motion: reduce) {
  .btn-ceramic {
    transition: none;
  }
}
```

### 4. Kiln Glow (Loading/processing state)

A warm amber shimmer travels across loading skeleton elements, like the glow of heat inside a kiln viewed through the peephole. Instead of the standard cool-gray shimmer, this uses the warm palette.

- **Technique:** CSS gradient animation using warm bisque tones: from `#E8DFD2` (recessed) through `#F0E6D6` (bg) to `#E8DFD2` (recessed). The highlight is `#F8F3EC` (surface) -- brighter, suggesting heat.
- **Duration:** 2s per cycle (slower than standard 1.5s shimmer -- unhurried, like kiln firing).
- **Direction:** Left to right, repeating.

```css
.kiln-shimmer {
  background: linear-gradient(
    90deg,
    #E8DFD2 0%,
    #E8DFD2 30%,
    #F8F3EC 50%,
    #E8DFD2 70%,
    #E8DFD2 100%
  );
  background-size: 200% 100%;
  animation: kiln-glow 2s ease-in-out infinite;
  border-radius: 12px;
}
@keyframes kiln-glow {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
@media (prefers-reduced-motion: reduce) {
  .kiln-shimmer {
    animation: none;
    background: #E8DFD2;
  }
}
```

### 5. Wheel Spin (Toggle transition)

When a toggle switches state, the thumb slides with viscous spring physics -- overshooting its target position and settling back, like a potter's wheel decelerating. The track color transitions through an intermediate warm tone before arriving at cobalt (on) or stoneware (off).

- **Technique:** The toggle thumb uses `transform: translateX()` with viscous-spring easing. The track `background-color` transitions through `#6B8DBF` (a mid-tone between stoneware and cobalt) before arriving at the final color.
- **Duration:** 300ms.
- **Easing:** viscous-spring (`cubic-bezier(0.23, 1.2, 0.52, 1)`).

```css
.toggle-track {
  width: 40px;
  height: 22px;
  border-radius: 9999px;
  background-color: #DDD3C4; /* off state - warm stoneware */
  transition: background-color 300ms cubic-bezier(0.23, 1.2, 0.52, 1);
  position: relative;
  cursor: pointer;
}
.toggle-track[data-state="on"] {
  background-color: #2B5EA7; /* cobalt glaze */
}
.toggle-thumb {
  width: 18px;
  height: 18px;
  border-radius: 9999px;
  background: #F8F3EC;
  box-shadow: 0 1px 3px rgba(51, 41, 31, 0.08);
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 300ms cubic-bezier(0.23, 1.2, 0.52, 1);
}
.toggle-track[data-state="on"] .toggle-thumb {
  transform: translateX(18px);
}
@media (prefers-reduced-motion: reduce) {
  .toggle-track, .toggle-thumb {
    transition-duration: 100ms;
    transition-timing-function: ease;
  }
}
```

---

## Dark Mode Variant

This theme is natively light. The dark mode variant inverts the surface hierarchy: deeper layers become darker, elevated surfaces become slightly lighter. All warm undertones are preserved -- the dark mode should feel like the potter's studio at night, lit by a single warm lamp and the residual heat of the kiln.

### Dark Mode Palette

| Token | Light Hex | Dark Hex | Dark HSL | Notes |
|---|---|---|---|---|
| page | `#E6DDD0` | `#161210` | 24 19% 7% | Deepest dark surface. Warm charcoal, like cooled kiln walls. |
| bg | `#F0E6D6` | `#1E1A16` | 28 15% 10% | Primary dark surface. Dark warm clay. |
| surface | `#F8F3EC` | `#2A2520` | 30 13% 15% | Cards, inputs. Slightly lighter than bg. |
| recessed | `#E8DFD2` | `#1A1714` | 26 12% 9% | Code blocks, inset. Slightly darker than bg. |
| active | `#DDD3C4` | `#12100D` | 30 17% 6% | Active items, user bubble. Darkest interactive. |
| text-primary | `#33291F` | `#F5EFEA` | 30 35% 94% | Primary text. Warm cream. |
| text-secondary | `#706557` | `#B8AFA3` | 30 10% 68% | Secondary text. Warm light gray. |
| text-muted | `#9E9487` | `#7D756B` | 30 8% 45% | Muted text. |
| border-base | `#C4B8A6` | `#8A7F70` | 33 12% 49% | Border base. Darker kiln wash. Same opacity system applies. |
| accent-primary | `#2B5EA7` | `#3D7AC7` | 215 53% 51% | Cobalt glaze -- slightly lifted for dark bg contrast. |
| accent-secondary | `#7FAD8E` | `#8EBDA0` | 139 22% 65% | Celadon -- slightly lifted. |
| success | `#5D9E6A` | `#6DAE7A` | 133 25% 55% | Copper green -- slightly lifted. |
| warning | `#C48B2F` | `#D49B3F` | 39 60% 54% | Amber flux -- slightly lifted. |
| danger | `#B84E42` | `#C85E52` | 6 47% 55% | Iron red -- slightly lifted. |
| info | `#5E8BC4` | `#6E9BD4` | 214 44% 63% | Light cobalt -- slightly lifted. |

### Dark Mode Special Colors

| Token | Dark Value |
|---|---|
| inlineCode | `#7EB8E5` | Lighter cobalt for code text on dark backgrounds. |
| toggleActive | `#3D7AC7` | Lifted cobalt to match dark mode accent-primary. |
| selection | `rgba(61, 122, 199, 0.22)` | Dark mode cobalt at 22% -- slightly higher opacity for visibility. |

### Dark Mode Rules

- Surfaces lighten as they elevate: `page (#161210)` < `bg (#1E1A16)` < `surface (#2A2520)`. Standard dark-mode elevation convention.
- Accent colors (cobalt and celadon) are lifted +10% lightness for visibility against dark surfaces. The cobalt shifts from `#2B5EA7` to `#3D7AC7`.
- Text colors invert: primary becomes warm cream, secondary/muted become progressively dimmer warm grays.
- Border opacity system remains the same (15/25/30/40%), but the base color shifts to `#8A7F70` (darker kiln wash) for visibility against dark surfaces.
- Shadow percentages increase: `shadow-card` uses 8% rest / 12% hover (vs 5%/7% in light). `shadow-popover` uses 20% / 10% dual layer (vs 12%/6% in light). Shadow base color shifts to pure `rgba(0, 0, 0, ...)` since dark-on-dark needs more intensity.
- Apply `-webkit-font-smoothing: antialiased` (already specified, essential for light text on dark backgrounds).
- Grain overlay changes to `screen` blend mode at 2% opacity (inverted from `normal` in light mode).
- Focus ring cobalt updates to `rgba(61, 122, 199, 0.50)` -- slightly lifted for dark bg visibility.
- All border-radius values remain identical. Roundness does not change with color mode.

### Dark Mode Shadow Tokens

| Token | Dark Value |
|---|---|
| shadow-card | `0 2px 8px rgba(0, 0, 0, 0.08), 0 0 0 0.5px rgba(138, 127, 112, 0.15)` |
| shadow-card-hover | `0 4px 16px rgba(0, 0, 0, 0.12), 0 0 0 0.5px rgba(138, 127, 112, 0.25)` |
| shadow-input | `0 2px 12px rgba(0, 0, 0, 0.06), 0 0 0 0.5px rgba(138, 127, 112, 0.15)` |
| shadow-input-hover | `0 3px 16px rgba(0, 0, 0, 0.08), 0 0 0 0.5px rgba(138, 127, 112, 0.25)` |
| shadow-input-focus | `0 4px 20px rgba(0, 0, 0, 0.12), 0 0 0 0.5px rgba(138, 127, 112, 0.30)` |
| shadow-popover | `0 4px 24px rgba(0, 0, 0, 0.20), 0 2px 6px rgba(0, 0, 0, 0.10)` |

---

## Data Visualization

| Property | Value |
|---|---|
| Categorical palette | Cobalt `#2B5EA7`, Celadon `#7FAD8E`, Amber `#C48B2F`, Iron Red `#B84E42`, Light Cobalt `#5E8BC4`. Max 5 hues per chart. |
| Sequential ramp | Cobalt single-hue: `#C8DAF0` (lightest) -> `#8AADE0` -> `#5E8BC4` -> `#2B5EA7` -> `#1A3D6E` (darkest) |
| Diverging ramp | Celadon-to-Cobalt: `#7FAD8E` -> `#B5D4BD` -> `#F0E6D6` (neutral bisque center) -> `#8AADE0` -> `#2B5EA7` |
| Grid style | low-ink. Axes in text-muted, gridlines in border-base at 8% opacity. |
| Max hues per chart | 3 (cobalt primary, celadon secondary, one semantic color for emphasis). |
| Philosophy | annotated. Labels on data, not legends. Rounded bar ends (`border-radius` on bar chart tops). |
| Number formatting | Geist Mono with `font-variant-numeric: tabular-nums`. Right-aligned in columns. |
| Chart containers | 16px border-radius. Same card treatment as all other cards. |
| Rounded bars | Bar chart bars use `border-radius: 6px 6px 0 0` on top -- even data visualization gets the ceramic rounded treatment. |

---

## Mobile Notes

### Effects to Disable

- **Grain overlay:** Remove SVG `feTurbulence` filter (GPU memory pressure on mobile Safari).
- **Backdrop blur on popovers:** Reduce from `blur(20px)` to `blur(10px)` (performance on older devices). Keep modal blur at `blur(8px)`.
- **Glaze Pool shadow expansion:** Simplify to single-layer shadow on hover (remove dual-layer composite).

### Sizing Adjustments

- **Stagger delays:** Reduce from 100ms to 60ms for snappier mobile feel.
- **Viscous spring durations:** Reduce by 30% on mobile (e.g., 300ms becomes 210ms). Mobile users expect faster responses, and the viscous feel can register as laggy on touch.
- **Touch targets:** All interactive elements minimum 44px -- already met by default with this theme's generous component heights (36px buttons, 44px inputs).
- **Card padding:** Reduce from 24px to 20px on screens below 640px. Still generous.
- **Content padding:** 16px horizontal on mobile (vs centered max-width on desktop).
- **Typography:** Display role reduces from 38px to `clamp(28px, 6vw, 38px)`. All other roles remain fixed.
- **Modal padding:** Reduce from 28px to 20px on mobile.

### Performance Notes

- This theme is moderately performance-friendly. The generous border-radius values are GPU-composited. The soft shadows use standard `box-shadow`, which is well-optimized.
- The primary performance concern is the viscous spring easing -- cubic-bezier with overshooting control points is handled by the compositor but can compound if many elements transition simultaneously. Limit concurrent spring transitions to 8-10 elements.
- The grain overlay and backdrop blur are the heaviest effects. Both should be reduced or removed on low-powered devices.
- Shadow composites (drop + ring) are well-supported and GPU-composited on modern hardware.

---

## Implementation Checklist

- [ ] **Fonts loaded:** DM Sans (variable opsz, 100-1000 weight), Figtree (variable, 300-900 weight), Geist Mono (variable, 100-900) via Google Fonts / CDN with `font-display: swap`
- [ ] **CSS custom properties defined:** All color tokens, shadow tokens, border tokens, radius tokens, spacing scale, motion easings, layout values as `:root` variables
- [ ] **Font smoothing applied:** `-webkit-font-smoothing: antialiased` on `<html>`
- [ ] **Typography matrix implemented:** All 10 roles with correct family, size, weight, line-height, letter-spacing
- [ ] **Family switch boundary respected:** DM Sans for Display/Heading/Subheading only. Figtree for all other roles.
- [ ] **Border-radius system applied:** Minimum 12px on containers, 16px on cards, 20px on modals/chat input, 9999px on pills/toggles, 8px on tooltips (smallest). No 0px or 4px radius anywhere.
- [ ] **Shadow tokens applied per state:** rest/hover/focus on input card and cards, sm on chips, popover on menus. All shadows are soft-diffused (large blur, low opacity).
- [ ] **Border opacity system implemented:** All borders use base color (`#C4B8A6`) at correct opacity level (subtle 15%, card 25%, hover 30%, focus 40%)
- [ ] **Focus ring on all interactive elements:** `outline: 2px solid rgba(43, 94, 167, 0.45)`, `outline-offset: 2px` on `:focus-visible`. Cobalt-themed, not generic blue.
- [ ] **Disabled states complete:** opacity 0.5 + pointer-events none + cursor not-allowed + shadow none
- [ ] **Viscous spring easing used throughout:** `cubic-bezier(0.23, 1.2, 0.52, 1)` as the default transition easing. NOT `ease` or `ease-in-out`.
- [ ] **Motion durations match motion map:** 250-400ms range. Nothing faster than 100ms except menu items. No `transition: all 0.2s`.
- [ ] **`prefers-reduced-motion` media query present:** All spring animations replaced with 100ms default easing. All translateY removed. All stagger delays zeroed.
- [ ] **Scrollbar styled:** `scrollbar-width: thin`, `scrollbar-color: rgba(196, 184, 166, 0.35) transparent`
- [ ] **`::selection` styled:** `background: rgba(43, 94, 167, 0.16)`, `color: #33291F`
- [ ] **Touch targets >= 44px on mobile:** Met by default with 36px buttons + padding, 44px inputs.
- [ ] **State transitions match motion map:** Each component uses its specified duration and viscous spring easing.
- [ ] **Cobalt accent used intentionally:** Only for CTA, toggles, links, primary data series. Never decorative.
- [ ] **Dark mode variant tested:** All token swaps applied, accent colors lifted, shadow percentages adjusted, text contrast verified WCAG AA.
- [ ] **Signature animations implemented:** Glaze Pool (hover shadow), Viscous Settle (page entry), Clay Press (active feedback), Kiln Glow (loading shimmer), Wheel Spin (toggle).
- [ ] **Grain overlay present:** SVG `feTurbulence` at 1.5% opacity. Disabled on mobile.
- [ ] **Gradient fade mask on sidebar items:** Not `text-overflow: ellipsis`.
- [ ] **Caret color set to cobalt:** `caret-color: #2B5EA7` on all text inputs.
- [ ] **Data visualization uses rounded bar ends:** `border-radius: 6px 6px 0 0` on chart bars.
