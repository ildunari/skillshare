# 19. Monsoon Bazaar — Full Reference

## Table of Contents

| Section | Line |
|---------|------|
| [Identity & Philosophy](#identity--philosophy) | 46 |
| [Color System](#color-system) | 76 |
| [Typography Matrix](#typography-matrix) | 141 |
| [Elevation System](#elevation-system) | 184 |
| [Border System](#border-system) | 227 |
| [Component States](#component-states) | 269 |
| [Motion Map](#motion-map) | 385 |
| [Overlays](#overlays) | 444 |
| [Layout Tokens](#layout-tokens) | 499 |
| [Accessibility Tokens](#accessibility-tokens) | 549 |
| [Visual Style](#visual-style) | 586 |
| [Signature Animations](#signature-animations) | 645 |
| [Data Visualization](#data-visualization) | 867 |
| [Dark Mode Variant](#dark-mode-variant) | 882 |
| [Mobile Notes](#mobile-notes) | 930 |
| [Implementation Checklist](#implementation-checklist) | 960 |

---

## 19. Monsoon Bazaar

> South Asian poster energy — saturated inks, registration offset depth, and controlled chaos at maximum volume.

**Best for:** Event marketing, festival pages, music platforms, food delivery apps, cultural showcases, portfolio sites, editorial magazines, campaign microsites, streetwear storefronts, community bulletin boards, vibrant dashboards, creative agency sites.

---

### Identity & Philosophy

This theme lives at the intersection of a Bollywood movie poster and a spice market stall. The color temperature is searing: hot magenta, deep indigo, saffron yellow, all cranked to maximum saturation and used in defined zones across the layout. The background is raw cotton — the unbleached muslin fabric that drapes across bazaar stalls and serves as the printing substrate for hand-block textile stamps. Everything on top of it is loud, saturated, and deliberate.

The core visual tension is **controlled chaos**. Every color is at maximum saturation, every headline is poster-scale, every animation stamps into place with kinetic energy — but the underlying system is rigidly organized. This is not randomness. It is the organized loudness of a bazaar where every vendor knows their pitch, every banner has its place, every spice jar sits in its designated row. The chaos is performative; the structure is real.

Depth comes from **registration offset** — the look of misaligned print layers where CMYK plates don't perfectly align. Instead of soft shadows or border-based elevation, elements have a 2-3px colored shadow offset to one side (no blur), as if the ink layer beneath them was printed a fraction off. The offset color comes from the secondary accent (indigo or magenta), giving depth a chromatic quality that flat black shadows cannot achieve.

Typography is poster-scale and kinetic. Display text is LARGE, BOLD, and slightly tight-tracked — the energy of hand-painted Bollywood signage translated into Bricolage Grotesque at 800 weight. Body text in DM Sans is clean and modern, creating a deliberate contrast between the explosive headlines and the calm reading experience. This duality is the theme's signature: the poster screams, the body text whispers.

Texture comes from halftone grain — the dot-pattern artifact of cheap offset printing on rough paper. A subtle SVG noise overlay at 3-4% opacity gives every surface the tactile quality of newsprint or hand-block-printed fabric. This is not clean digital rendering; it is ink on cotton.

**Decision principle:** "When in doubt, ask: does this feel like a bazaar poster printed on cotton? If it feels like a SaaS landing page, add more saturation, more weight, more stamp energy. If it feels like visual noise, organize it into zones."

**What this theme is NOT:**
- Not subtle or restrained. This is maximum saturation by design. Muted colors are a failure state.
- Not soft-shadowed. Depth is registration offset only — colored hard offsets, zero blur. No `box-shadow` with blur radius.
- Not random. "Loud" does not mean "unstructured." Every saturated zone has a purpose. Color placement follows strict zone rules.
- Not gradient-based. Fills are flat and solid. The halftone grain is a texture overlay, not a gradient. No `linear-gradient` on surfaces.
- Not Western-festival-generic. This is specifically South Asian poster energy — the density, the saturation, the typographic scale come from a particular visual tradition. It is not Coachella; it is Holi.
- Not slow or floaty. Motion is kinetic — stamp presses, registration jitter, rapid stagger. Nothing drifts. Everything arrives with impact.

---

### Color System

#### Palette

All colors at maximum usable saturation. The palette is organized into zones: the cotton base (neutrals), the ink system (magenta, indigo, saffron), and the semantic overlay.

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Raw Cotton | `#F0E6D4` | L=0.92 C=0.03 h=80 | Deepest background. Unbleached muslin fabric — the bazaar's draped backdrop. Warm, fibrous, slightly yellow. |
| bg | Bleached Cotton | `#F7F0E2` | L=0.95 C=0.025 h=82 | Primary surface. Lighter cotton, the printing substrate. The base sheet everything is stamped onto. |
| surface | White Cotton | `#FFFAF0` | L=0.98 C=0.015 h=85 | Elevated cards, inputs, popovers. Clean cotton stock — the brightest surface. |
| recessed | Dyed Cotton | `#E4D9C6` | L=0.87 C=0.035 h=78 | Code blocks, inset areas. Cotton that has absorbed dye residue — darker, warmer. |
| active | Pressed Cotton | `#D8CCB8` | L=0.83 C=0.04 h=76 | Active/pressed states, selected items. Cotton compressed under a woodblock stamp. |
| text-primary | Block Print Ink | `#1A1210` | L=0.14 C=0.02 h=50 | Headings, body text. Dense vegetable-based ink, near-black with warm undertone. |
| text-secondary | Faded Ink | `#5C4D40` | L=0.38 C=0.04 h=55 | Sidebar items, secondary labels. Ink that has been diluted or aged. |
| text-muted | Worn Print | `#9A8A78` | L=0.60 C=0.04 h=65 | Placeholders, timestamps, metadata. Old block print, faded with handling. |
| text-onAccent | Raw Cotton | `#FFF8EE` | L=0.97 C=0.02 h=85 | Text on accent-colored backgrounds. Cotton showing through ink. |
| border-base | Thread Line | `#BCA890` | L=0.72 C=0.05 h=70 | Base border color at variable opacity. The visible weave line of cotton fabric. |
| accent-primary | Hot Magenta | `#E6166E` | L=0.52 C=0.28 h=358 | Brand accent, primary CTA. Searing pink-red — the fluorescent poster ink that dominates Bollywood hoardings. Maximum saturation. |
| accent-secondary | Deep Indigo | `#2A1B8C` | L=0.28 C=0.22 h=280 | Secondary accent. The indigo dye of traditional textiles — deep blue-violet, rich and dense. Used for registration offset shadows. |
| accent-tertiary | Saffron Yellow | `#F5A623` | L=0.78 C=0.18 h=75 | Tertiary accent. Turmeric/saffron — warm, golden, used for highlights and warning states. The spice market color. |
| success | Henna Green | `#2D8C46` | L=0.52 C=0.16 h=148 | Positive states. The green of henna paste — natural, vegetal, earthy. |
| warning | Saffron Yellow | `#F5A623` | L=0.78 C=0.18 h=75 | Caution states. Shares the saffron accent — context disambiguates. |
| danger | Vermillion Sindoor | `#D42B2B` | L=0.48 C=0.22 h=28 | Error states. The red of sindoor/kumkum — sacred vermillion, unmistakable. |
| info | Monsoon Teal | `#1A8C8C` | L=0.53 C=0.12 h=194 | Informational states. The blue-green of monsoon sky before a downpour. |

#### Special Colors

| Token | Hex | Role |
|---|---|---|
| inlineCode | `#7B2D8E` | Code text within prose. Deep purple — the overprint of magenta and indigo. |
| toggleActive | `#2A1B8C` | Toggle/switch active track. Deep Indigo — the secondary accent. |
| selection | `rgba(230,22,110,0.20)` | `::selection` background. Hot Magenta at 20% — pink highlight on cotton. |

#### Fixed Colors

| Token | Hex | Role |
|---|---|---|
| alwaysBlack | `#000000` | Structural black (mode-independent) |
| alwaysWhite | `#FFFFFF` | Emergency on-dark only (mode-independent) |

#### Opacity System

One border base color (Thread Line `#BCA890`), applied at variable opacity for different levels of separation:

| Level | Opacity | Usage |
|---|---|---|
| subtle | 15% | Lightest separation, hairlines, background structure |
| card | 25% | Card borders, cotton-layer edges |
| hover | 35% | Hover states, emphasized borders |
| focus | 50% | Focus borders, maximum non-ring emphasis |

#### Color Rules

- **Zone discipline.** Magenta, Indigo, and Saffron are never used randomly. Magenta is for primary actions and poster-energy headings. Indigo is for registration offset shadows and secondary emphasis. Saffron is for warmth, highlights, and warning. Each ink has a job.
- **Saturation is structural.** Full saturation on accent colors is the design. Desaturation is only used for disabled states (opacity reduction, not hue shift). A "toned down" Monsoon Bazaar is a broken Monsoon Bazaar.
- **Cotton is the white.** There is no pure white (`#FFFFFF`) in normal use. The lightest surface is `#FFFAF0` (White Cotton). Pure white feels digital; cotton-white feels printed.
- **Black is warm.** Text-primary (`#1A1210`) has a warm brown-black undertone. Pure `#000000` is only for structural purposes (registration offset base).
- **Registration offset shadows use accent colors.** Depth is not black shadow — it is a 2-3px offset in Deep Indigo (`#2A1B8C` at 30-40% opacity) or Hot Magenta (`#E6166E` at 20-30% opacity). This gives elevation a chromatic quality.
- **No gradients on surfaces.** All fills are flat solid color. The halftone grain overlay is a texture, not a gradient.

---

### Typography Matrix

#### Font Families

| Slot | Font | Fallback | Role |
|---|---|---|---|
| display | Bricolage Grotesque | system-ui, -apple-system, sans-serif | Display, Heading. Bold poster grotesque with variable optical sizing. The headline screamer. Its slightly irregular letterforms evoke hand-painted Bollywood signage. |
| body | DM Sans | system-ui, -apple-system, sans-serif | Body, Body Small, Button, Input, Label, Caption. Clean, crisp geometric sans. The calm counterpoint to Bricolage's energy. #1 on Typewolf 2026. |
| mono | Fira Code | ui-monospace, SFMono-Regular, Menlo, monospace | Code, data values. Ligature-enabled monospace with personality. The `=>` and `!=` ligatures add visual craft to code blocks. |

**Why this pairing:** Bricolage Grotesque at 800 weight is the typographic equivalent of a Bollywood poster headline — massive, bold, slightly quirky, impossible to ignore. Its variable `opsz` axis means it maintains clarity from 48px display size down to 20px heading size. DM Sans provides the essential contrast: where Bricolage screams, DM Sans speaks clearly. This duality IS the theme — controlled chaos requires both the loud and the quiet to function. Fira Code was chosen over JetBrains Mono because its ligatures add a craft detail that fits the bazaar's "everything has personality" ethos.

**Family switch boundary:** Bricolage Grotesque handles Display and Heading roles only. DM Sans handles everything from Body down. An implementer seeing Bricolage at body size is fighting the theme's tension — the quiet body text is what makes the loud headlines work.

#### Role Matrix

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Bricolage Grotesque | 48px | 800 | 1.05 (50.4px) | -0.03em | `font-variation-settings: "opsz" 48, "wdth" 100` | Hero titles, page headlines. MASSIVE, BOLD, poster-scale. The bazaar's loudest voice. |
| Heading | Bricolage Grotesque | 28px | 700 | 1.15 (32.2px) | -0.02em | `font-variation-settings: "opsz" 28` | Section titles, card group headers. Still bold, slightly quieter. |
| Subheading | Bricolage Grotesque | 20px | 600 | 1.25 (25px) | -0.01em | -- | Card titles, subsection headers. The transition point from loud to structured. |
| Body | DM Sans | 16px | 400 | 1.55 (24.8px) | normal | -- | Primary reading text, UI body. Clean, calm, readable. |
| Body Small | DM Sans | 14px | 400 | 1.45 (20.3px) | normal | -- | Sidebar items, form labels, secondary UI text. |
| Button | DM Sans | 14px | 600 | 1.4 (19.6px) | 0.04em | `text-transform: uppercase` | Button labels. ALL CAPS with wide tracking — poster-energy on controls. |
| Input | DM Sans | 14px | 450 | 1.4 (19.6px) | normal | -- | Form input text. Slightly heavier than body for field presence. |
| Label | DM Sans | 11px | 700 | 1.33 (14.6px) | 0.1em | `text-transform: uppercase` | Section labels, metadata, timestamps. ALL CAPS, heavily tracked. Maximum poster energy at small scale. |
| Code | Fira Code | 0.9em (14.4px) | 400 | 1.5 (21.6px) | normal | `font-variant-numeric: tabular-nums`, `font-feature-settings: "liga" 1` | Inline code, code blocks, data values. Ligatures enabled. |
| Caption | DM Sans | 12px | 400 | 1.33 (16px) | 0.01em | -- | Disclaimers, footnotes, bottom-of-page text. |

#### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Fira+Code:wght@300..700&display=swap" rel="stylesheet">
```

- **Font smoothing:** `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale` on `<html>`.
- **Font display:** `font-display: swap` on all families.
- **Optical sizing:** `font-optical-sizing: auto` for both Bricolage Grotesque (opsz 12-96) and DM Sans (opsz 9-40).
- **Text wrap:** `text-wrap: balance` for headings, `text-wrap: pretty` for body.

---

### Elevation System

**Strategy:** Registration offset — flat colored shadows with zero blur, offset 2-3px in one direction. Shadows use accent colors (indigo or magenta) instead of black, giving depth a chromatic identity. This simulates misregistered print layers where the ink plate beneath an element is slightly misaligned.

#### Surface Hierarchy

| Surface | Background | Shadow | Usage |
|---|---|---|---|
| page | page token (`#F0E6D4`) | none | Deepest layer. The cotton backdrop. |
| canvas | bg token (`#F7F0E2`) | none | Primary working surface. The base printing substrate. |
| card | surface token (`#FFFAF0`) | shadow-card (indigo offset) | Cards, inputs at rest. Cotton sheet sitting on the base. |
| recessed | recessed token (`#E4D9C6`) | none | Code blocks, inset areas. Dyed cotton, lower layer. |
| active | active token (`#D8CCB8`) | none | Active items, pressed states. Compressed cotton. |
| overlay | surface token (`#FFFAF0`) | shadow-popover (indigo offset, larger) | Popovers, dropdowns. Cotton sheet floating high. |

#### Shadow Tokens (Registration Offset System)

All shadows are hard-edged (blur = 0). The offset direction is bottom-right (light source top-left). Shadow color is Deep Indigo at variable opacity — this is what makes the elevation system chromatic rather than grayscale.

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `2px 2px 0px rgba(42,27,140,0.18)` | Small elements, tags, chips. Slight registration misalignment. |
| shadow-card | `3px 3px 0px rgba(42,27,140,0.22)` | Cards at rest. One print layer above base. |
| shadow-card-hover | `4px 4px 0px rgba(42,27,140,0.28)` | Cards on hover. Registration offset increases — layer lifts. |
| shadow-input | `2px 2px 0px rgba(42,27,140,0.15)` | Input fields at rest. Subtle offset. |
| shadow-input-hover | `3px 3px 0px rgba(42,27,140,0.20)` | Input hover. Offset grows. |
| shadow-input-focus | `3px 3px 0px rgba(42,27,140,0.28)` | Input focus. Maximum offset opacity for active input. |
| shadow-popover | `4px 4px 0px rgba(42,27,140,0.30)` | Menus, popovers, dropdowns. Paper floating high above substrate. |
| shadow-modal | `6px 6px 0px rgba(42,27,140,0.32)` | Modal dialogs. Maximum registration offset. |
| shadow-magenta | `3px 3px 0px rgba(230,22,110,0.20)` | Accent shadow variant. Used on primary buttons and highlighted cards for warm chromatic depth. |
| shadow-none | `none` | Flat surfaces, disabled states, recessed areas. |

**Magenta vs Indigo shadows:** Default registration offset uses indigo (cool). Primary action elements (buttons, highlighted cards) use magenta shadow for warm chromatic pop. The choice signals interactivity — if it has a magenta shadow, you can click it.

#### Backdrop Filter

| Context | Value | Usage |
|---|---|---|
| All contexts | `backdrop-filter: none` | NO backdrop blur. This is printed matter on cotton — physical materials do not frost. |

#### Separation Recipe

Registration offset + tint-step. Layers separate through cotton-color stepping (darker base, lighter overlay) plus a chromatic hard shadow offset that says "this layer was printed slightly off from the one below." No hairline dividers between major sections. Sidebar separation is a 2px solid border at card opacity. Everything is flat fills casting chromatic offset shadows. The indigo offset is the single most important visual signature — it replaces soft shadows entirely.

---

### Border System

#### Base Color

Thread Line `#BCA890` — the visible weave of cotton fabric, applied at variable opacity.

#### Widths and Patterns

| Pattern | Width | Opacity | Usage |
|---|---|---|---|
| subtle | 1px | 15% | Lightest separation, hairlines, background structure lines |
| card | 1.5px | 25% | Card borders, cotton layer edges |
| hover | 2px | 35% | Hover states, emphasized edges |
| input | 2px | 25% | Form input borders at rest |
| input-hover | 2px | 35% | Form input borders on hover |

Borders are thicker than delicate digital themes (1px minimum). This is intentional — block-print edges and textile weave lines are heavier than hairlines. The theme should feel substantial and printed.

#### Width Scale

| Name | Value | Usage |
|---|---|---|
| hairline | 1px | Lightest structural lines |
| default | 1.5px | Standard card and component borders |
| medium | 2px | Input borders, emphasized edges |
| heavy | 3px | Accent zone borders, section dividers, maximum emphasis |

#### Focus Ring

| Property | Value | Notes |
|---|---|---|
| Color | `rgba(42,27,140,0.55)` | Deep Indigo focus ring — consistent with the registration offset color system. |
| Width | 3px solid | Thicker than typical. Poster scale demands bold focus indication. |
| Offset | 2px | Standard offset. |

The focus ring uses indigo (not magenta) because magenta signals "clickable primary action" while indigo signals "system-level indication." Focus is a system behavior, not an action.

---

### Component States

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | `bg: accent-primary (#E6166E)`, `border: 2px solid accent-primary`, `color: text-onAccent (#FFF8EE)`, `border-radius: 6px`, `height: 38px`, `padding: 0 18px`, `font-size: 14px`, `font-weight: 600`, `font-family: DM Sans`, `letter-spacing: 0.04em`, `text-transform: uppercase`, `box-shadow: shadow-magenta (3px 3px 0px rgba(230,22,110,0.20))`, `cursor: pointer` |
| Hover | `box-shadow: 4px 4px 0px rgba(230,22,110,0.28)`, `transform: translate(-1px, -1px)` — button lifts away from its registration offset shadow |
| Active | `box-shadow: none`, `transform: translate(2px, 2px)` — button stamps flat, registration aligns (shadow collapses) |
| Focus | `outline: 3px solid rgba(42,27,140,0.55)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `box-shadow: none`, `cursor: not-allowed` |
| Transition | `transform, box-shadow 100ms cubic-bezier(0.34, 1.56, 0.64, 1)` (stamp easing with overshoot) |

#### Buttons (Ghost/Icon)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: none`, `color: text-secondary (#5C4D40)`, `border-radius: 6px`, `width: 38px`, `height: 38px`, `padding: 0`, `cursor: pointer` |
| Hover | `bg: recessed (#E4D9C6)`, `color: text-primary (#1A1210)` |
| Active | `transform: scale(0.90)` — strong stamp press. Poster energy means pronounced press feedback. |
| Focus | `outline: 3px solid rgba(42,27,140,0.55)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none` |
| Transition | `background-color, color 100ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

#### Buttons (Secondary/Outlined)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: 2px solid accent-primary (#E6166E)`, `color: accent-primary`, `border-radius: 6px`, `height: 38px`, `padding: 0 18px`, `font-size: 14px`, `font-weight: 600`, `letter-spacing: 0.04em`, `text-transform: uppercase`, `box-shadow: shadow-sm (2px 2px 0px rgba(42,27,140,0.18))`, `cursor: pointer` |
| Hover | `bg: rgba(230,22,110,0.08)`, `box-shadow: shadow-card (3px 3px 0px rgba(42,27,140,0.22))`, `transform: translate(-1px, -1px)` |
| Active | `box-shadow: none`, `transform: translate(2px, 2px)` |
| Focus | `outline: 3px solid rgba(42,27,140,0.55)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `box-shadow: none` |
| Transition | `transform, box-shadow, background-color 100ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

#### Text Input

| State | Properties |
|---|---|
| Rest | `bg: surface (#FFFAF0)`, `border: 2px solid border-base at card opacity (25%)`, `border-radius: 6px`, `height: 44px`, `padding: 0 12px`, `font-size: 14px`, `font-weight: 450`, `font-family: DM Sans`, `color: text-primary`, `caret-color: accent-primary (#E6166E)`, `box-shadow: shadow-input (2px 2px 0px rgba(42,27,140,0.15))` |
| Placeholder | `color: text-muted (#9A8A78)` |
| Hover | `border-color: border-base at hover opacity (35%)`, `box-shadow: shadow-input-hover (3px 3px 0px rgba(42,27,140,0.20))` |
| Focus | `outline: 3px solid rgba(42,27,140,0.55)`, `outline-offset: 2px`, `box-shadow: shadow-input-focus (3px 3px 0px rgba(42,27,140,0.28))` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `cursor: not-allowed`, `box-shadow: none` |
| Transition | `border-color, box-shadow 120ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | `bg: surface (#FFFAF0)`, `border-radius: 10px`, `border: 2px solid border-base at card opacity (25%)`, `box-shadow: shadow-card (3px 3px 0px rgba(42,27,140,0.22))` |
| Hover | `box-shadow: shadow-card-hover (4px 4px 0px rgba(42,27,140,0.28))`, `transform: translate(-0.5px, -0.5px)` |
| Focus-within | `box-shadow: shadow-card-hover`, `border-color: border-base at focus opacity (50%)` |
| Inner textarea | `font-size: 16px`, `line-height: 24.8px`, `bg: transparent`, `color: text-primary`, `placeholder-color: text-muted` |
| Transition | `transform, box-shadow, border-color 150ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Cards

| State | Properties |
|---|---|
| Rest | `bg: surface (#FFFAF0)`, `border: 1.5px solid border-base at card opacity (25%)`, `border-radius: 8px`, `box-shadow: shadow-card (3px 3px 0px rgba(42,27,140,0.22))`, `padding: 20px` |
| Hover | `box-shadow: shadow-card-hover (4px 4px 0px rgba(42,27,140,0.28))`, `transform: translate(-1px, -1px)`, `border-color: border-base at hover opacity (35%)` |
| Focus | `outline: 3px solid rgba(42,27,140,0.55)`, `outline-offset: 2px` (clickable cards) |
| Transition | `transform, box-shadow, border-color 120ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

**Accent zone cards:** Cards that serve as section heroes or featured content can use accent-primary as background (`bg: #E6166E`, `color: text-onAccent`, `border: none`). Their registration offset shadow uses magenta variant: `shadow-magenta`. This creates high-energy poster zones within the layout. Use sparingly — maximum one accent zone per viewport.

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `color: text-secondary (#5C4D40)`, `border-radius: 6px`, `height: 36px`, `padding: 6px 16px`, `font-size: 14px`, `font-weight: 400`, `font-family: DM Sans`, `cursor: pointer` |
| Hover | `bg: recessed (#E4D9C6)`, `color: text-primary (#1A1210)` |
| Active (current) | `bg: active (#D8CCB8)`, `color: text-primary`, `box-shadow: shadow-sm (2px 2px 0px rgba(42,27,140,0.18))` |
| Active press | `transform: scale(0.97)` |
| Disabled | `pointer-events: none`, `opacity: 0.4` |
| Transition | `color, background-color 80ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

#### Chips

| State | Properties |
|---|---|
| Rest | `bg: bg (#F7F0E2)`, `border: 1.5px solid border-base at subtle opacity (15%)`, `border-radius: 6px`, `height: 32px`, `padding: 0 10px`, `font-size: 14px`, `font-weight: 400`, `font-family: DM Sans`, `color: text-secondary (#5C4D40)`, `box-shadow: shadow-sm (2px 2px 0px rgba(42,27,140,0.18))` |
| Icon | 16x16px, `display: inline-flex`, `gap: 6px` from label |
| Hover | `bg: active (#D8CCB8)`, `border-color: border-base at card opacity (25%)`, `color: text-primary`, `box-shadow: shadow-card (3px 3px 0px rgba(42,27,140,0.22))` |
| Active press | `transform: scale(0.95)`, `box-shadow: none` |
| Transition | `all 100ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

#### Toggle/Switch

| Property | Value |
|---|---|
| Track | `width: 40px`, `height: 22px`, `border-radius: 6px` (slightly squared — stamp aesthetic, not pill) |
| Track off | `bg: recessed (#E4D9C6)`, `border: 2px solid border-base at card opacity (25%)` |
| Track on | `bg: toggleActive (#2A1B8C)` (Deep Indigo) |
| Thumb | `width: 16px`, `height: 16px`, `bg: surface (#FFFAF0)`, `border-radius: 4px` (squared thumb), `box-shadow: shadow-sm (2px 2px 0px rgba(42,27,140,0.18))` |
| Thumb position off | `translateX(2px)` |
| Thumb position on | `translateX(20px)` |
| Transition | `background-color, transform 120ms cubic-bezier(0.34, 1.56, 0.64, 1)` (stamp easing) |
| Focus-visible | `3px solid rgba(42,27,140,0.55)`, `offset: 2px` |

#### User Message Bubble

| Property | Value |
|---|---|
| bg | `active (#D8CCB8)` |
| border | `1.5px solid border-base at card opacity (25%)` |
| border-radius | 8px |
| padding | `10px 16px` |
| max-width | `85%` (capped at `70ch`) |
| color | `text-primary (#1A1210)` |
| font | DM Sans, 16px, weight 400 |
| alignment | Right-aligned |
| box-shadow | `shadow-sm (2px 2px 0px rgba(42,27,140,0.18))` |

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| stamp | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Overshoot landing. THE signature easing. Elements arrive with kinetic energy, overshoot slightly (~2-3% past target), then snap back. Like a woodblock stamp hitting fabric — impact, then settle. |
| jitter | `cubic-bezier(0.25, 0.1, 0, 1)` | Quick snap with slight instability. For hover state changes. Feels like registration plates settling. |
| press | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. Button presses, basic transitions. The controlled side of controlled chaos. |
| cascade | `cubic-bezier(0.22, 1, 0.36, 1)` | Out-quint. Gentle deceleration for large movements. Panel open/close. Like fabric unfurling. |
| kinetic | `cubic-bezier(0.16, 1.11, 0.3, 1)` | Strong overshoot with fast attack. For display text entries — text slams in and vibrates. The poster-pasting moment. |

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 80ms | stamp | Fast color swap with overshoot. Bazaar energy. |
| Button hover (lift) | 100ms | stamp | Transform + shadow offset grows. Registration layer separates. |
| Button active (press) | 60ms | press | Transform + shadow collapse. Stamp hits the surface. |
| Toggle track color | 120ms | stamp | Background-color and thumb transform. Snappy with click. |
| Chip hover | 100ms | stamp | All properties. Tag lifts off its registration shadow. |
| Card border/shadow hover | 120ms | stamp | Border-color, box-shadow, transform. Layer lifts. |
| Input border hover | 120ms | jitter | Border-color and shadow. Registration settling. |
| Chat input card | 150ms | jitter | Shadow escalation and border change. |
| Ghost icon button | 100ms | stamp | Faster than typical themes — bazaar is direct. |
| Display text entry | 250ms | kinetic | `opacity: 0, translateY(20px), scale(1.05)` to `opacity: 1, translateY(0), scale(1)`. Text SLAMS into place. |
| Card entry | 200ms | stamp | `opacity: 0, scale(0.88), translateY(12px)` to final. Poster element stamped. |
| Modal entry | 200ms | stamp | `scale(0.85)` to `scale(1)` + fade. Poster slapped onto surface. |
| Panel open/close | 300ms | cascade | Sidebar collapse, settings expand. Fabric unfurling. |
| Stagger delay | 35ms | -- | Between staggered children. RAPID — bazaar vendors calling out in quick succession. |
| Menu item hover | 60ms | jitter | Popover item bg/color change. |
| Page hero entry | 300ms | kinetic | Full hero section with text + accent elements. Maximum impact. |

#### Active Press Scale

| Element | Scale/Transform | Notes |
|---|---|---|
| Nav items (sidebar) | `scale(0.97)` | Cotton sheet pressed. |
| Chips | `scale(0.95)` | Stamp tag pressed. More pronounced than soft themes. |
| Buttons (primary) | `translate(2px, 2px)` + `shadow: none` | Registration collapses. Custom press — not scale. |
| Buttons (ghost) | `scale(0.90)` | Strong stamp for icon buttons. Bold, physical. |
| Tabs | `scale(0.93)` | Pronounced tab press. Bazaar energy in every click. |

#### Reduced Motion (`prefers-reduced-motion: reduce`)

| Behavior | Change |
|---|---|
| Strategy | `instant` for spatial transforms. No overshoot, no kinetic text. |
| All translateY entries | Replaced with 100ms opacity-only fade. |
| Press transforms | Disabled. Instant visual state change. |
| Stamp/kinetic overshoot | Disabled. All `cubic-bezier(0.34, 1.56, ...)` and `cubic-bezier(0.16, 1.11, ...)` replaced with `ease`. |
| Stagger delays | Reduced to 0ms. All children appear simultaneously. |
| Registration jitter animation | Disabled. Static offset only. |
| All hover transitions | Remain but capped at 80ms with standard easing. |
| Shadow offset changes | Instant. No transition on box-shadow. |

---

### Overlays

#### Popover/Dropdown

| Property | Value |
|---|---|
| bg | `surface (#FFFAF0)` |
| backdrop-filter | `none` (no blur — printed matter on cotton) |
| border | `2px solid border-base at hover opacity (35%)` |
| border-radius | 8px |
| box-shadow | `shadow-popover (4px 4px 0px rgba(42,27,140,0.30))` |
| padding | 6px |
| min-width | 200px |
| max-width | 320px |
| z-index | 50 |
| overflow-y | `auto` (with `max-height: var(--available-height)`) |
| Menu item | `padding: 6px 10px`, `border-radius: 6px`, `height: 34px`, `font-size: 14px (body-small)`, `font-family: DM Sans`, `color: text-secondary`, `cursor: pointer` |
| Menu item hover | `bg: recessed (#E4D9C6)`, `color: text-primary` |
| Menu item transition | `60ms jitter easing` |
| Separators | `1.5px solid border-base at subtle opacity (15%)`. Visible divider lines — bazaar sections have clear boundaries. |

#### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(26,18,16,0.45)` (warm tinted, not pure black) |
| Overlay backdrop-filter | `none` (no blur) |
| Content bg | `surface (#FFFAF0)` |
| Content border | `2px solid border-base at hover opacity (35%)` |
| Content shadow | `shadow-modal (6px 6px 0px rgba(42,27,140,0.32))` |
| Content border-radius | 8px |
| Content padding | 24px |
| Entry animation | `opacity: 0, scale(0.85)` to `opacity: 1, scale(1)`, 200ms stamp easing. Poster slapped onto surface. |
| Exit animation | `opacity: 0`, 120ms press easing |
| z-index | 60 |

#### Tooltip

| Property | Value |
|---|---|
| bg | `active (#D8CCB8)` |
| color | `text-primary (#1A1210)` |
| font-size | 12px (label role) |
| font-weight | 500 |
| font-family | DM Sans |
| border | `1.5px solid border-base at card opacity (25%)` |
| border-radius | 4px |
| padding | `4px 10px` |
| box-shadow | `shadow-sm (2px 2px 0px rgba(42,27,140,0.18))` |
| Arrow | None. Position-only placement. |
| Delay | 200ms before showing. |
| z-index | 55 |

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 800px | Main content column. Wide enough for poster-energy layouts. |
| Narrow max-width | 680px | Focused content, settings pages. |
| Sidebar width | 280px | Fixed sidebar. |
| Sidebar border | `2px solid border-base at card opacity (25%)` | Right edge. Visible textile-edge separation. |
| Header height | 52px | Top bar. Slightly taller for bold type scale. |
| Spacing unit | 4px | Base multiplier. |

#### Spacing Scale

`4, 6, 8, 12, 16, 20, 24, 32, 40, 48px`

Common applications:
- 4px: icon-text inline gap
- 6px: popover item padding, compact spacing
- 8px: standard element gap, chip padding
- 12px: input padding, button horizontal padding
- 16px: card content inset, sidebar item padding
- 20px: card padding (compact)
- 24px: card padding (standard), modal padding
- 32px: section separation
- 40px: major section gap, hero element spacing
- 48px: hero section padding, poster-scale breathing room

#### Density

**moderate-dense** — The bazaar is packed. Elements are close together but each has clear boundaries through the registration offset shadow system. This is not sparse — it is organized density. The hard offset shadows provide clear separation even at close spacing, so density does not create confusion.

#### Responsive Notes

| Breakpoint | Width | Behavior |
|---|---|---|
| lg | 1024px | Full sidebar + content. Standard desktop. Maximum poster energy. |
| md | 768px | Sidebar collapses to overlay panel. Content fills viewport. |
| sm | 640px | Single column. Cards stack. Registration offsets reduce from 3-4px to 2px. |

On mobile (below md):
- Sidebar becomes an overlay panel with same bg, activated by menu button
- Content max-width becomes 100% with 16px horizontal padding
- Header remains 52px but actions collapse into a popover menu
- Cards stretch to full width, padding reduces from 24px to 16px
- Registration offset shadows reduce by 40% (e.g., `3px 3px` becomes `2px 2px`) to avoid overwhelming small screens
- Display text scales via `clamp(28px, 8vw, 48px)` — maintains poster energy proportionally
- Label tracking reduces from `0.1em` to `0.06em` on small screens

---

### Accessibility Tokens

| Token | Value | Notes |
|---|---|---|
| Focus ring color | `rgba(42,27,140,0.55)` | Deep Indigo — consistent with registration offset system. |
| Focus ring width | `3px solid` | Thicker than typical. Poster scale needs bold focus rings. |
| Focus ring offset | `2px` | Standard offset. |
| Disabled opacity | `0.4` | Lower than typical (0.5) — saturated theme needs stronger disabled signal. |
| Disabled shadow | `none` | Remove all registration offset shadows on disabled. |
| Disabled cursor | `not-allowed` | Standard. |
| Disabled pointer-events | `none` | Standard. |
| Selection bg | `rgba(230,22,110,0.20)` | Hot Magenta at 20%. Pink highlight on cotton. |
| Selection color | `text-primary` | Maintains readability. |
| Scrollbar width | `thin` | Minimal scrollbar presence. |
| Scrollbar thumb | `rgba(188,168,144,0.45)` | Thread Line at 45% — slightly higher for visibility on textured cotton background. |
| Scrollbar track | `transparent` | Clean. |
| Min touch target | 44px | All interactive elements on mobile. |
| Contrast standard | WCAG AA | 4.5:1 text, 3:1 large text. Hot Magenta `#E6166E` on White Cotton `#FFFAF0` = 4.6:1 (passes). Block Print Ink `#1A1210` on Bleached Cotton `#F7F0E2` = 15.2:1 (passes). |

**Scrollbar CSS:**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(188, 168, 144, 0.45) transparent;
}
```

**Contrast verification notes:**
- `#E6166E` (Hot Magenta) on `#FFFAF0` (White Cotton): 4.6:1 — passes AA for normal text
- `#E6166E` (Hot Magenta) on `#F7F0E2` (Bleached Cotton): 4.5:1 — borderline AA, use bold weight (600+) for safety
- `#2A1B8C` (Deep Indigo) on `#FFFAF0` (White Cotton): 10.8:1 — passes AAA
- `#1A1210` (Block Print Ink) on `#F7F0E2` (Bleached Cotton): 15.2:1 — passes AAA
- `#FFF8EE` (text-onAccent) on `#E6166E` (Hot Magenta): 4.6:1 — passes AA

---

### Visual Style

#### Material

| Property | Value |
|---|---|
| Grain | Moderate (3-4%) — halftone dot noise, like offset printing on rough cotton substrate |
| Grain technique | SVG `feTurbulence` overlay (`baseFrequency="1.2"`, 2 octaves, `type="fractalNoise"`) at 3.5% opacity on the page container. Suggests the fibrous texture of hand-block-printed cotton. |
| Gloss | Dead matte. Zero reflections. Block-print ink on cotton dries flat and chalky. |
| Blend mode | `normal` on all surfaces. Inks are opaque. The only exception is the registration offset pseudo-elements which can use `multiply` if overlapping text. |
| Shader bg | `false` |

#### Rendering Philosophy

- **Flat saturated fills:** Every surface is a single solid color at maximum usable saturation. No gradients. No inner glows. No soft anything. The bazaar poster is unapologetic about its colors.
- **Registration offset depth:** ALL depth comes from chromatic hard shadows (indigo or magenta, 2-4px offset, zero blur). This is the ONLY depth mechanism. No soft shadows. No border-only elevation. No surface-color-shift-only elevation.
- **Poster-scale typography:** Display text at 48px/800 weight dominates the viewport. This is not quiet or whispered. The hierarchy between the 48px Bricolage Grotesque headline and the 16px DM Sans body is extreme and intentional — it mirrors the contrast between a painted movie poster headline and its fine print.
- **Zone discipline:** Saturated accent colors appear in defined zones (hero areas, primary CTAs, featured cards), NOT scattered randomly. Between zones, the cotton neutrals provide rest. The pattern is: quiet → LOUD → quiet → LOUD. Without the quiet zones, the loud zones have no impact.
- **Halftone grain:** The SVG noise overlay gives every surface the tactile quality of block-printed fabric. Without it, the flat fills look too digital. With it, they look like ink on cotton.

#### Halftone Grain CSS

```css
.monsoon-grain::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.035;
  mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='1.2' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

#### Registration Offset CSS (for text elements)

Headings and display text can have a subtle registration offset effect — a secondary color layer offset by 1-2px:

```css
.registration-offset {
  position: relative;
}
.registration-offset::before {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 2px;
  color: rgba(42, 27, 140, 0.15); /* Deep Indigo at 15% */
  pointer-events: none;
  z-index: -1;
}
```

Use sparingly — only on Display and Heading roles. Body text should NOT have registration offset; it would impair readability.

---

### Signature Animations

#### 1. Block Stamp Entry

New elements enter by "stamping" onto the cotton surface — arriving with kinetic overshoot, registration offset shadow appearing as the element lands.

```css
@keyframes blockStamp {
  0% {
    opacity: 0;
    transform: scale(0.85) translateY(12px);
    box-shadow: none;
  }
  60% {
    opacity: 1;
    transform: scale(1.03) translateY(-2px);
    box-shadow: 4px 4px 0px rgba(42, 27, 140, 0.28);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
    box-shadow: 3px 3px 0px rgba(42, 27, 140, 0.22);
  }
}

.stamp-enter {
  animation: blockStamp 250ms cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@media (prefers-reduced-motion: reduce) {
  .stamp-enter {
    animation: none;
    opacity: 1;
    transform: none;
    box-shadow: 3px 3px 0px rgba(42, 27, 140, 0.22);
  }
}
```

- **Duration:** 250ms.
- **Easing:** stamp (overshoot). Element briefly exceeds final scale (~1.03), then settles.
- **Shadow:** Animates from none to final offset — registration layer "prints" as element arrives.
- **Reduced motion:** Instant appear with final shadow. No scale, no translate.

#### 2. Kinetic Text Slam

Display-size text slams into the viewport with exaggerated kinetic energy — the poster headline being pasted.

```css
@keyframes textSlam {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(1.08) rotate(-1deg);
    letter-spacing: 0.05em;
  }
  50% {
    opacity: 1;
    transform: translateY(-4px) scale(1.02) rotate(0.5deg);
    letter-spacing: -0.01em;
  }
  75% {
    transform: translateY(1px) scale(0.99) rotate(-0.2deg);
    letter-spacing: -0.025em;
  }
  100% {
    transform: translateY(0) scale(1) rotate(0deg);
    letter-spacing: -0.03em;
  }
}

.text-slam {
  animation: textSlam 300ms cubic-bezier(0.16, 1.11, 0.3, 1) both;
}

@media (prefers-reduced-motion: reduce) {
  .text-slam {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

- **Duration:** 300ms.
- **Easing:** kinetic (strong overshoot). Text overshoots position, scale, AND letter-spacing before settling.
- **Rotation:** Slight rotation oscillation (-1deg to +0.5deg to 0) simulates the imprecision of pasting a poster by hand.
- **Reduced motion:** Instant appear. No movement.

#### 3. Registration Jitter

Subtitle or heading text shows its registration offset layer jittering for 1-2 frames on entry, as if the print plates are settling into alignment.

```css
@keyframes registrationJitter {
  0% {
    text-shadow: 3px 1px 0px rgba(42, 27, 140, 0.20),
                 -1px 2px 0px rgba(230, 22, 110, 0.15);
  }
  25% {
    text-shadow: 1px 3px 0px rgba(42, 27, 140, 0.20),
                 2px -1px 0px rgba(230, 22, 110, 0.15);
  }
  50% {
    text-shadow: 2px 2px 0px rgba(42, 27, 140, 0.18),
                 -1px 1px 0px rgba(230, 22, 110, 0.12);
  }
  75% {
    text-shadow: 2px 1px 0px rgba(42, 27, 140, 0.15),
                 1px 2px 0px rgba(230, 22, 110, 0.08);
  }
  100% {
    text-shadow: 2px 2px 0px rgba(42, 27, 140, 0.12),
                 none;
  }
}

.registration-jitter {
  animation: registrationJitter 200ms steps(4) forwards;
}

@media (prefers-reduced-motion: reduce) {
  .registration-jitter {
    animation: none;
    text-shadow: 2px 2px 0px rgba(42, 27, 140, 0.12);
  }
}
```

- **Duration:** 200ms.
- **Easing:** `steps(4)` — discrete frames, not smooth. Printing plates click into position.
- **Layers:** Two text-shadow colors (indigo + magenta) jitter independently and converge.
- **Final state:** Single subtle indigo offset remains. Magenta layer fully aligns (disappears).
- **Reduced motion:** Static single-layer offset. No jitter.

#### 4. Bazaar Cascade

Cards, list items, and grid elements enter in a rapid stagger cascade — like a row of bazaar stalls opening their shutters in sequence.

```css
@keyframes bazaarCascade {
  0% {
    opacity: 0;
    transform: translateY(16px) scale(0.92);
    box-shadow: none;
  }
  70% {
    opacity: 1;
    transform: translateY(-2px) scale(1.01);
    box-shadow: 4px 4px 0px rgba(42, 27, 140, 0.25);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
    box-shadow: 3px 3px 0px rgba(42, 27, 140, 0.22);
  }
}

.cascade-item {
  animation: bazaarCascade 200ms cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

/* Stagger via custom property */
.cascade-item:nth-child(1) { animation-delay: 0ms; }
.cascade-item:nth-child(2) { animation-delay: 35ms; }
.cascade-item:nth-child(3) { animation-delay: 70ms; }
.cascade-item:nth-child(4) { animation-delay: 105ms; }
.cascade-item:nth-child(5) { animation-delay: 140ms; }
.cascade-item:nth-child(6) { animation-delay: 175ms; }

@media (prefers-reduced-motion: reduce) {
  .cascade-item {
    animation: none;
    opacity: 1;
    transform: none;
    box-shadow: 3px 3px 0px rgba(42, 27, 140, 0.22);
  }
}
```

- **Stagger delay:** 35ms per item. This is RAPID — the bazaar opens fast.
- **Duration:** 200ms per element.
- **Total for 6 items:** 200ms + (5 x 35ms) = 375ms. The entire grid populates in under 400ms.
- **Reduced motion:** All items appear simultaneously. No stagger.

#### 5. Saffron Pulse

A warm saffron pulse that radiates from interactive elements on successful actions (form submit, save, toggle on). The accent-tertiary color briefly floods the element's registration offset shadow.

```css
@keyframes saffronPulse {
  0% {
    box-shadow: 3px 3px 0px rgba(42, 27, 140, 0.22);
  }
  30% {
    box-shadow: 4px 4px 0px rgba(245, 166, 35, 0.40),
                0 0 0 3px rgba(245, 166, 35, 0.15);
  }
  100% {
    box-shadow: 3px 3px 0px rgba(42, 27, 140, 0.22);
  }
}

.saffron-pulse {
  animation: saffronPulse 500ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

@media (prefers-reduced-motion: reduce) {
  .saffron-pulse {
    animation: none;
  }
}
```

- **Duration:** 500ms.
- **Easing:** cascade (out-quint). Saffron flares then gently settles back to indigo offset.
- **Purpose:** Success confirmation. The spice market celebrates a sale.
- **Reduced motion:** No animation. Use a static checkmark or text confirmation instead.

---

### Data Visualization

| Property | Value |
|---|---|
| Categorical palette | Hot Magenta `#E6166E`, Deep Indigo `#2A1B8C`, Saffron `#F5A623`, Henna Green `#2D8C46`, Monsoon Teal `#1A8C8C` |
| Sequential ramp | Magenta single-hue: `#FADCE8` -> `#F0A0C0` -> `#E6166E` -> `#B8104E` -> `#7A0A30` |
| Diverging ramp | Indigo-to-Saffron: `#2A1B8C` -> `#6A5CB0` -> `#F7F0E2` (cotton center) -> `#F0C870` -> `#F5A623` |
| Grid style | low-ink. Axes in text-muted, gridlines in border-base at 10% opacity. Cotton shows through. |
| Max hues per chart | 5 |
| Philosophy | annotated. Labels placed directly on data points with DM Sans 12px. Strong typographic hierarchy. Numbers in Fira Code with `tabular-nums`. |
| Number formatting | Fira Code, `font-variant-numeric: tabular-nums`, right-aligned. |

---

### Dark Mode Variant

This theme is natively light. Dark mode represents "the night bazaar" — stalls lit by tungsten bulbs and neon signage. Surfaces become dark cotton (indigo-tinted), inks and dyes remain vivid.

#### Dark Mode Palette

| Token | Light Hex | Dark Hex | Notes |
|---|---|---|---|
| page | `#F0E6D4` | `#0E0A08` | Deep warm black. Night bazaar backdrop. |
| bg | `#F7F0E2` | `#1A1410` | Dark cotton. Warm charcoal. |
| surface | `#FFFAF0` | `#28201A` | Dark card stock. Warm dark brown — tungsten-lit fabric. |
| recessed | `#E4D9C6` | `#120E0A` | Darker than bg. Shadow under the stall. |
| active | `#D8CCB8` | `#342A22` | Slightly lighter than surface. Pressed under lamplight. |
| text-primary | `#1A1210` | `#F5EEE0` | Warm cream. Cotton-white on dark. |
| text-secondary | `#5C4D40` | `#B8A898` | Warm light gray-brown. |
| text-muted | `#9A8A78` | `#7A6E60` | Warm mid-brown. Faded text under dim light. |
| text-onAccent | `#FFF8EE` | `#FFF8EE` | Same — cotton on accent. |
| border-base | `#BCA890` | `#4A3E32` | Darker thread line for dark surfaces. |
| accent-primary | `#E6166E` | `#FF2880` | Hot Magenta, lifted +12% lightness for dark contrast. Neon sign glow. |
| accent-secondary | `#2A1B8C` | `#5040C0` | Deep Indigo, lifted. Night-bazaar purple under blacklight. |
| accent-tertiary | `#F5A623` | `#FFBA40` | Saffron, lifted. Tungsten warmth. |
| success | `#2D8C46` | `#40A85C` | Henna Green, lifted. |
| danger | `#D42B2B` | `#E84040` | Vermillion, lifted. |
| info | `#1A8C8C` | `#28AAAA` | Monsoon Teal, lifted. |

#### Dark Mode Rules

- Surfaces darken as they recede: `page` (darkest) < `bg` < `surface` (lightest dark surface). Elevation = lightening.
- Accent colors lift +10-15% lightness to maintain contrast on dark backgrounds. Magenta shifts toward neon-pink, indigo toward electric-violet.
- Registration offset shadows shift from indigo-on-light to a lighter indigo variant: `rgba(80,64,192,0.30)` replaces `rgba(42,27,140,0.22)`. Offsets need more lightness to register on dark surfaces.
- Grain overlay switches to `screen` blend mode (was `multiply` in light mode). `opacity: 0.025` (reduced from 0.035 — grain is more visible on dark).
- Border opacity percentages remain the same, but border base shifts to `#4A3E32` (lighter thread on dark fabric).
- `-webkit-font-smoothing: antialiased` is essential for light text on dark.
- Cotton is still the metaphor — it is indigo-dyed cotton, not a digital dark mode.

#### Dark Mode Shadow Tokens

| Token | Dark Value |
|---|---|
| shadow-sm | `2px 2px 0px rgba(80,64,192,0.25)` |
| shadow-card | `3px 3px 0px rgba(80,64,192,0.30)` |
| shadow-card-hover | `4px 4px 0px rgba(80,64,192,0.36)` |
| shadow-popover | `4px 4px 0px rgba(80,64,192,0.38)` |
| shadow-modal | `6px 6px 0px rgba(80,64,192,0.40)` |
| shadow-magenta | `3px 3px 0px rgba(255,40,128,0.25)` |

All shadows remain hard-edged (zero blur) in dark mode. Indigo shifts to lighter violet for visibility.

---

### Mobile Notes

#### Effects to Disable

- **Grain overlay:** Remove SVG `feTurbulence` filter on mobile. Compositing is expensive on mobile Safari.
- **Registration offset on text (::before pseudo):** Disable CSS pseudo-element text offset. Keep box-shadow offsets (they are GPU-composited).
- **Registration Jitter animation:** Disable entirely. Static offset only.
- **Kinetic Text Slam rotation:** Remove `rotate()` keyframes on mobile. Keep scale and translate.

#### Sizing Adjustments

- **Registration offset shadows:** Reduce all offsets by 40% on screens below 640px. `3px 3px` becomes `2px 2px`. `4px 4px` becomes `2px 2px`. `6px 6px` becomes `4px 4px`.
- **Border widths:** Reduce by 0.5px on mobile. `2px` becomes `1.5px`. `1.5px` becomes `1px`.
- **Touch targets:** All interactive elements minimum 44px. Sidebar items at 36px on desktop expand to 44px on mobile.
- **Card padding:** Reduce from 24px to 16px on screens below 640px.
- **Content padding:** 16px horizontal on mobile.
- **Display typography:** Scale via `clamp(28px, 8vw, 48px)`. Poster energy scales proportionally.
- **Label tracking:** Reduce from `0.1em` to `0.06em` below 640px. Heavy tracking needs more horizontal space.
- **Stagger delays:** Halve all stagger delays on mobile (35ms becomes 18ms) for snappier feel.

#### Performance Notes

- This theme is moderately performance-friendly. Hard shadows (zero blur) are cheaper than blurred shadows.
- Registration offset pseudo-elements (::before on text) are the most expensive element on mobile — disable.
- Grain overlay is the second most expensive — disable on all mobile viewports.
- No WebGL or canvas elements required for base theme.
- Saturated colors and flat fills are rendering-cheap. The theme's visual intensity comes from color, not computation.

---

### Implementation Checklist

- [ ] **Fonts loaded:** Bricolage Grotesque (variable, opsz 12-96, wght 200-800), DM Sans (variable, opsz 9-40, wght 100-1000), Fira Code (300-700) via Google Fonts with `font-display: swap`
- [ ] **CSS custom properties defined:** All color tokens, shadow tokens (indigo + magenta variants), border tokens, radius tokens, spacing scale, motion easings, layout values as `:root` variables
- [ ] **Font smoothing applied:** `-webkit-font-smoothing: antialiased` on `<html>`
- [ ] **Typography matrix implemented:** All 10 roles with correct family, size, weight, line-height, letter-spacing, text-transform
- [ ] **Family switch boundary respected:** Bricolage Grotesque for Display/Heading/Subheading only. DM Sans for all other roles.
- [ ] **ZERO gradients enforced:** No `linear-gradient`, `radial-gradient`, or `conic-gradient` on any surface. All fills solid.
- [ ] **Registration offset shadows enforced:** All `box-shadow` values have `0` blur radius. Shadow color is Deep Indigo or Hot Magenta (never pure black except in structural contexts).
- [ ] **Shadow tokens use accent colors:** Indigo `rgba(42,27,140,...)` for standard elements, Magenta `rgba(230,22,110,...)` for primary actions.
- [ ] **Border-radius applied correctly:** sm (4px), md (6px), lg (8px). Toggle uses 6px track, 4px thumb. No pill shapes.
- [ ] **Shadow tokens applied per state:** rest/hover/active on buttons (lift/stamp pattern), rest/hover on cards, rest/hover/focus on inputs
- [ ] **Border opacity system implemented:** All borders use Thread Line `#BCA890` at correct opacity (subtle 15%, card 25%, hover 35%, focus 50%)
- [ ] **Focus ring on all interactive elements:** 3px solid `rgba(42,27,140,0.55)`, offset 2px, on `:focus-visible`
- [ ] **Disabled states complete:** opacity 0.4 + pointer-events none + cursor not-allowed + shadow none
- [ ] **`prefers-reduced-motion` media query present:** All stamp/kinetic easings, registration jitter, stagger delays disabled
- [ ] **Scrollbar styled:** `scrollbar-width: thin`, `scrollbar-color: rgba(188,168,144,0.45) transparent`
- [ ] **`::selection` styled:** Hot Magenta at 20% opacity: `rgba(230,22,110,0.20)`
- [ ] **Touch targets >= 44px on mobile**
- [ ] **State transitions match motion map:** stamp easing for interactive elements, cascade for large movements. No global `transition: all 0.2s`.
- [ ] **Zone discipline validated:** Saturated accent colors appear in defined zones only, not scattered randomly
- [ ] **Halftone grain overlay implemented:** SVG feTurbulence at 3.5% opacity, `mix-blend-mode: multiply`
- [ ] **Registration offset on display text:** CSS `::before` pseudo-element with 2px offset in Deep Indigo at 15%
- [ ] **Dark mode variant tested:** All token swaps applied, shadow color shifted to lighter indigo, accent colors lifted, contrast verified WCAG AA
- [ ] **Stagger delays rapid:** 35ms between children (not the typical 60-80ms). Bazaar energy.
- [ ] **WCAG AA contrast verified:** All text/background combinations checked per contrast verification table
