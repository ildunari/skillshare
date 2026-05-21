# 13. Warm Darkroom — Full Reference

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — line 9
- [Color System](#color-system) — line 28
  - [Palette](#palette) — line 32
  - [Special Tokens](#special-tokens) — line 54
  - [Opacity System (Border on `var(--border-base)`)](#opacity-system-border-on-var--border-base) — line 63
  - [Color Rules](#color-rules) — line 72
- [Typography Matrix](#typography-matrix) — line 83
  - [Font Loading](#font-loading) — line 109
- [Elevation System](#elevation-system) — line 119
  - [Surface Hierarchy](#surface-hierarchy) — line 128
  - [Surface-Shift Tokens](#surface-shift-tokens) — line 138
  - [Vignette Gradient](#vignette-gradient) — line 161
  - [Separation Recipe](#separation-recipe) — line 184
- [Border System](#border-system) — line 190
  - [Widths](#widths) — line 194
  - [Opacity Scale (on `var(--border-base)`)](#opacity-scale-on-var--border-base) — line 202
  - [Patterns](#patterns) — line 211
  - [Focus Ring](#focus-ring) — line 223
- [Component States](#component-states) — line 246
  - [Buttons (Primary)](#buttons-primary) — line 250
  - [Buttons (Ghost / Icon)](#buttons-ghost--icon) — line 261
  - [Text Input](#text-input) — line 272
  - [Chat Input Card](#chat-input-card) — line 283
  - [Cards](#cards) — line 291
  - [Sidebar Items](#sidebar-items) — line 301
  - [Chips](#chips) — line 311
  - [Toggle / Switch](#toggle--switch) — line 321
  - [User Bubble](#user-bubble) — line 337
- [Motion Map](#motion-map) — line 350
  - [Easings](#easings) — line 357
  - [Duration x Easing x Component](#duration-x-easing-x-component) — line 367
  - [Active Press Scale](#active-press-scale) — line 390
- [Layout Tokens](#layout-tokens) — line 402
  - [Spacing Scale](#spacing-scale) — line 412
  - [Density](#density) — line 418
  - [Radius Scale](#radius-scale) — line 430
  - [Responsive Notes](#responsive-notes) — line 446
- [Accessibility Tokens](#accessibility-tokens) — line 454
  - [Reduced Motion](#reduced-motion) — line 480
- [Overlays](#overlays) — line 517
  - [Popover / Dropdown](#popover--dropdown) — line 519
  - [Modal](#modal) — line 535
  - [Tooltip](#tooltip) — line 545
- [Visual Style](#visual-style) — line 558
  - [Film Grain](#film-grain) — line 560
  - [Safe-Light Ambient Wash](#safe-light-ambient-wash) — line 591
  - [Material](#material) — line 618
- [Signature Animations](#signature-animations) — line 628
  - [1. Chemical Reveal (Page Entry)](#1-chemical-reveal-page-entry) — line 630
  - [2. Dodge and Burn Hover](#2-dodge-and-burn-hover) — line 688
  - [3. Film Grain Breathe](#3-film-grain-breathe) — line 721
  - [4. Developing Tray Ripple](#4-developing-tray-ripple) — line 753
  - [5. Contact Sheet Scan](#5-contact-sheet-scan) — line 778
- [Dark Mode Variant (Light Mode)](#dark-mode-variant-light-mode) — line 814
  - [Light Mode: Proof Sheet](#light-mode-proof-sheet) — line 820
- [Mobile Notes](#mobile-notes) — line 849
  - [Effects to Disable on Mobile](#effects-to-disable-on-mobile) — line 851
  - [Effects to Simplify on Mobile](#effects-to-simplify-on-mobile) — line 860
  - [Sizing Adjustments](#sizing-adjustments) — line 866
  - [Performance Budget](#performance-budget) — line 876
- [Data Visualization](#data-visualization) — line 886
- [Implementation Checklist](#implementation-checklist) — line 900

---

## Identity & Philosophy

This theme lives inside a photographer's darkroom. The door is shut. The safe-light casts a dim, warm red wash across the ceiling. Developing trays line the counter -- stop bath, developer, fixer -- and in the silence, an image slowly appears on paper submerged in chemistry. You watch it happen. You cannot rush it.

The core visual tension is between **absolute darkness** and **earned warmth**. The interface is predominantly dark -- not cold-dark like a terminal, but warm-dark like a room lit only by a single red bulb. Color is scarce and meaningful. Sepia tones reference the final print. Safe-light red is the only ambient color, and it is used with extreme restraint -- it marks the boundary between dark and visible, between hidden and revealed. Paper white is reserved for primary text, the way a finished print is the only bright thing in the room.

The signature motion of this theme is the **chemical reveal**: elements do not snap into view. They develop. Opacity builds in layered stages over 2-3 seconds, mimicking the way a photographic image appears in a chemical bath -- first the faintest ghost of form, then midtones filling in, then finally the full image resolving. This is the slowest-reveal theme in the system. Patience is the aesthetic.

**Decision principle:** "When in doubt, ask: would this feel at home in a darkroom? If it demands attention, it does not belong. Light is earned, not given."

**What this theme is NOT:**
- Not high-contrast -- the palette lives in the midtones and shadows, never in harsh black-on-white
- Not retro-nostalgic or kitsch -- no fake film borders, no simulated Polaroid frames, no Instagram filters
- Not red-dominant -- safe-light red is an ambient environmental color, not a brand accent; overusing it breaks the illusion
- Not fast -- if your animations complete in under 300ms, you have missed the darkroom's patience
- Not glossy or digital-feeling -- every surface should feel like it has tooth, like matte photographic paper

---

## Color System

Colors are organized around the physical reality of a darkroom: the warm black of a lightproof room, the dim red-orange wash of the safe-light, the sepia-and-cream tones of developing prints, and the chemical blue of toning solutions. Every color has a reason to exist in this space.

#### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Lightproof Black | `#0E0C0A` | L=0.08 C=0.01 h=60 | Deepest background. The sealed room. Near-black with a warm brown undertone -- not blue-black, not grey-black. This is the darkness of closed curtains and sealed doors. |
| bg | Developer Tray | `#171311` | L=0.11 C=0.012 h=55 | Primary surface background. Sidebar, main content area. The warm-dark surface of everything in the room that is not illuminated. |
| surface | Contact Sheet | `#211C18` | L=0.14 C=0.015 h=50 | Elevated cards, inputs, popovers. A step warmer and lighter, like the grey-brown of a contact sheet holder. |
| recessed | Film Canister | `#0A0908` | L=0.06 C=0.008 h=55 | Code blocks, inset areas. Deeper than page. The interior of a light-tight container. |
| active | Exposed Silver | `#2A2420` | L=0.17 C=0.016 h=50 | Active/pressed items, selected states. The warmest dark surface -- like silver gelatin catching the faintest light. |
| text-primary | Paper White | `#E8E0D4` | L=0.90 C=0.02 h=75 | Headings, body text. Not pure white -- the warm cream of fiber-based photographic paper. The finished print is the brightest element. |
| text-secondary | Fixer Residue | `#A89A8A` | L=0.66 C=0.03 h=65 | Sidebar items, secondary labels. Muted warm grey, like dried fixer marks on a print. |
| text-muted | Underdeveloped | `#7A6E62` | L=0.49 C=0.03 h=60 | Placeholders, timestamps, metadata. The ghost of an image that has not fully developed. |
| text-onAccent | Lightproof Black | `#0E0C0A` | L=0.08 C=0.01 h=60 | Text on accent-colored backgrounds. Same as page -- dark on warm. |
| accent-primary | Sepia Tone | `#C4956A` | L=0.68 C=0.08 h=65 | Brand accent, primary CTA. The warm brown of a sepia-toned print. This is the color of the finished work -- used for links, primary actions, the things that are "done" and resolved. |
| accent-secondary | Chemical Blue | `#5A7A9A` | L=0.53 C=0.06 h=240 | Secondary accent. The cold blue of selenium toner or cyanotype chemistry. Used sparingly for informational states, secondary actions, code syntax. A cool counterpoint to the dominant warmth. |
| border-base | Safe-Light Edge | `#8A6A52` | L=0.48 C=0.06 h=55 | Base border color used at variable opacity. Warm, brownish -- borders in this theme are like the edge of light and shadow. |
| safe-light | Darkroom Red | `#8B3A2A` | L=0.35 C=0.12 h=28 | Environmental color only. The dim red-orange wash of the safe-light. Used for ambient effects, notification badges, and the faintest environmental tint. Never used as a button color or primary UI element. |
| success | Developer Green | `#5A8A5A` | L=0.55 C=0.08 h=140 | Positive states. Muted, organic green -- the color of a well-developed negative held to the light. |
| warning | Amber Fix | `#B8924A` | L=0.64 C=0.10 h=80 | Caution states. Warm amber, like the amber of a nearly-exhausted fixer bath. |
| danger | Stop Bath Red | `#A04030` | L=0.40 C=0.12 h=25 | Error states, destructive actions. The red of stop bath indicator -- urgent but not screaming. |
| info | Chemical Blue | `#5A7A9A` | L=0.53 C=0.06 h=240 | Informational states. Same as accent-secondary. |

#### Special Tokens

| Token | Value | Role |
|---|---|---|
| inlineCode | `#C4956A` at 85% lightness | Code text within prose. Sepia-tinted for warmth. |
| toggleActive | `#C4956A` | Toggle/switch active track. Sepia tone -- the "developed" state. |
| selection | `rgba(196, 149, 106, 0.20)` | `::selection` background. Warm sepia wash. |
| safeLight-ambient | `radial-gradient(ellipse at 50% 20%, rgba(139, 58, 42, 0.04), transparent 70%)` | Environmental safe-light wash applied to page. Extremely subtle red tint from above, as if a safe-light hangs from the ceiling. |

#### Opacity System (Border on `var(--border-base)`)

| Level | Opacity | Usage |
|---|---|---|
| subtle | 10% | Dormant edges, hairline separators at rest. Barely visible in the darkness. |
| card | 18% | Card borders, panel edges. Present but quiet. |
| hover | 28% | Hovered elements. The border warms -- like light grazing an edge. |
| focus | 38% | Focused elements. Clear but not harsh. |

#### Color Rules

- **Safe-light red is environmental, not interactive.** It exists as an ambient page wash and for notification indicators. It is never used as a button background, link color, or accent. The safe-light is part of the room, not part of the UI.
- **Sepia is earned.** The accent-primary sepia tone marks things that are "complete" or "resolved" -- finished prints, confirmed actions, active states. Using it for decorative purposes dilutes its meaning.
- **Chemical blue is the counterpoint.** It appears only where coolness is appropriate: informational labels, code blocks, secondary controls. It prevents the palette from becoming monotonously warm.
- **No pure black, no pure white.** The darkest value is `#0A0908` (recessed), the lightest is `#E8E0D4` (text-primary). The palette lives in the analog range between these -- nothing is absolute.
- **Grain is mandatory.** Every surface carries a faint film grain overlay. This is the texture of the theme. Without it, surfaces feel digital and flat.
- **Warmth gradient for depth:** Darker surfaces are cooler (less chroma). Lighter/elevated surfaces are warmer (more chroma). This mimics how objects closer to the safe-light pick up more of its warm cast.

---

## Typography Matrix

DM Serif Display for headings (high-contrast serif, dramatic, editorial -- the typeface of a photo essay title), Spectral for body text (designed specifically for digital reading, excellent rendering at text sizes, warm seriffed personality), IBM Plex Mono for code and data (corporate-documentary feel, legible, unadorned).

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | serif (DM Serif Display) | 36px | 400 | 1.15 | -0.02em | -- | Hero titles, page names. The typeface of a gallery exhibition title. |
| Heading | serif (DM Serif Display) | 24px | 400 | 1.25 | -0.01em | -- | Section titles, settings headers. DM Serif Display only comes in 400 weight -- its inherent contrast provides visual weight. |
| Subheading | serif (Spectral) | 18px | 500 | 1.35 | normal | -- | Subsection titles, card headers. Spectral at medium weight for authority without the display drama. |
| Body | serif (Spectral) | 16px | 400 | 1.65 | normal | -- | Primary reading text, UI body. Spectral's generous x-height and open counters are optimized for screen reading. The 1.65 line-height gives text room to breathe -- editorial, not dense. |
| Body Small | serif (Spectral) | 14px | 400 | 1.5 | normal | -- | Sidebar items, form labels, secondary text. |
| Button | serif (Spectral) | 14px | 600 | 1.4 | 0.01em | -- | Button labels, emphasized small UI text. Spectral at semi-bold for quiet authority. |
| Input | serif (Spectral) | 14px | 400 | 1.4 | normal | -- | Form input text. Seriffed input text reinforces the editorial/analog character. |
| Code | mono (IBM Plex Mono) | 0.9em | 400 | 1.5 | normal | -- | Inline code, code blocks, data values. IBM Plex Mono's even color and neutral personality keep code readable without competing with the editorial serifs. |
| Label | serif (Spectral) | 12px | 500 | 1.33 | 0.03em | -- | Section labels, metadata, timestamps. Tracked slightly for legibility at small size. The label role uses Spectral to maintain the all-serif identity -- no sans-serif anywhere in the type stack. |
| Caption | serif (Spectral) | 12px | 400 | 1.33 | normal | -- | Disclaimers, footnotes, photo credits. Smallest text. |

**Typographic decisions:**
- **All-serif type stack.** This is a deliberate departure from the standard sans-serif UI convention. The darkroom is an analog space. Sans-serif typefaces feel digital and clinical. The double-serif pairing (DM Serif Display + Spectral) creates a unified editorial voice -- every piece of text feels like it belongs in a photography monograph or gallery catalogue.
- **DM Serif Display at weight 400 only.** This typeface has a single weight. Its high-contrast strokes and dramatic ball terminals provide enough visual presence without needing bold variants. Using it at display and heading sizes only prevents it from becoming fatiguing.
- **Spectral for everything else.** Spectral was designed by Production Type specifically for screen reading. Its x-height, stroke modulation, and hinting are optimized for 14-18px rendering. It carries personality without sacrificing readability.
- **No sans-serif in the system.** If a sans-serif is needed for a specific data-dense context, IBM Plex Mono serves as the "neutral" option. The absence of sans-serif is the typographic signature.
- **Line-height 1.65 for body.** More generous than the standard 1.5. This theme reads slowly. The extra leading gives each line room to settle, reducing the density and creating a meditative reading rhythm.
- `-webkit-font-smoothing: antialiased` is mandatory. Subpixel rendering on dark backgrounds causes color fringing with serif type.
- `text-wrap: pretty` for body text, `text-wrap: balance` for headings.

#### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
```

**Fallback chain:** `"DM Serif Display", "Georgia", serif` | `"Spectral", "Georgia", serif` | `"IBM Plex Mono", "Courier New", ui-monospace, monospace`

---

## Elevation System

**Strategy:** `surface-shifts`

There are no traditional box-shadows in the darkroom. Depth is created through the warmth gradient -- surfaces closer to the viewer (higher elevation) are slightly warmer and lighter, as if they catch more of the safe-light's glow. Surfaces farther away are cooler and darker, receding into the sealed darkness of the room. This mimics real darkroom physics: objects closer to the red bulb pick up more of its color.

Additionally, a subtle vignette gradient darkens the edges of the page, creating the tunnel-vision intimacy of working under a single overhead light source.

#### Surface Hierarchy

| Surface | Background | Warmth | Usage |
|---|---|---|---|
| page | `#0E0C0A` (L=0.08) | Coolest | Main canvas. The sealed room. |
| bg | `#171311` (L=0.11) | Cool-warm | Sidebar, secondary areas. One step into the light. |
| surface | `#211C18` (L=0.14) | Warm | Cards, inputs, panels. The working surface -- the counter, the tray. |
| recessed | `#0A0908` (L=0.06) | Coldest | Code blocks, inset areas. The deep interior of a cabinet. |
| active | `#2A2420` (L=0.17) | Warmest | Active/selected items. Closest to the safe-light. |
| overlay | `#211C18` (L=0.14) | Warm | Popovers, dropdowns. Same as surface but with backdrop blur. |

#### Surface-Shift Tokens

Instead of shadow tokens, this theme defines warmth-shift tokens that control how surfaces communicate elevation:

| Token | Value | Usage |
|---|---|---|
| shift-none | No background change | Flat, dormant. Element sits at its natural surface level. |
| shift-warm | Background lightness +3%, chroma +0.005 | Subtle lift. Cards at rest. The surface catches a fraction more safe-light. |
| shift-warmer | Background lightness +5%, chroma +0.008 | Hovered elements. Noticeably warmer -- like leaning closer to the light. |
| shift-warmest | Background lightness +7%, chroma +0.012 | Focused/active elements. The warmest state before accent color takes over. |
| shift-cool | Background lightness -2%, chroma -0.003 | Recessed areas. Pulling away from the light into deeper shadow. |

**CSS implementation for surface shifts:**

```css
:root {
  --shift-warm: color-mix(in oklch, var(--surface) 92%, var(--safe-light) 8%);
  --shift-warmer: color-mix(in oklch, var(--surface) 85%, var(--safe-light) 15%);
  --shift-warmest: color-mix(in oklch, var(--surface) 78%, var(--safe-light) 22%);
  --shift-cool: color-mix(in oklch, var(--surface) 95%, var(--page) 5%);
}
```

#### Vignette Gradient

A radial vignette darkens the page edges, simulating the single-overhead-light of a darkroom:

```css
.page::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background: radial-gradient(
    ellipse at 50% 30%,
    transparent 40%,
    rgba(10, 9, 8, 0.35) 80%,
    rgba(10, 9, 8, 0.55) 100%
  );
}
```

The vignette center is shifted upward (30% from top) to simulate the overhead position of the safe-light.

#### Separation Recipe

Warmth-step surfaces + faint luminous borders at very low opacity. No visible dividers. Panels separate from the background through the warmth gradient -- a card is warmer than its surroundings, and on hover it warms further. The edge between surface and void is defined by a nearly invisible border (border-base at 10-18% opacity) that catches the eye only when you look for it. The darkness itself is the primary separator.

---

## Border System

Borders in this theme are faint warm edges -- the line where light meets shadow. They are never crisp or prominent. The border color is a muted warm brown that blends with the surfaces, visible only as a subtle delineation.

#### Widths

| Token | Value | Usage |
|---|---|---|
| hairline | 0.5px | Panel edges, sidebar separators. A whisper of structure. |
| default | 1px | Card borders, input borders. Standard working border. |
| medium | 1.5px | Emphasized borders, active states. |
| heavy | 2px | Focus-adjacent, toggle tracks. |

#### Opacity Scale (on `var(--border-base)`)

| Level | Opacity | Usage |
|---|---|---|
| subtle | 10% | Dormant panel edges, rest-state separators. Nearly invisible in the darkness. |
| card | 18% | Card borders at rest. Present but quiet. |
| hover | 28% | Hovered cards, interactive elements. The edge catches more light. |
| focus | 38% | Focused element border before focus ring. Clear but not harsh. |

#### Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| panel-edge | 0.5px | `var(--border-base)` at 10% | Sidebar edges, quiet separators |
| card | 1px | `var(--border-base)` at 18% | Card borders at rest |
| card-hover | 1px | `var(--border-base)` at 28% | Card on hover -- border warms into visibility |
| input | 1px | `var(--border-base)` at 18% | Input rest state |
| input-hover | 1px | `var(--border-base)` at 28% | Input hover |
| input-focus | 1px | `var(--accent-primary)` at 35% | Input focus -- sepia-tinted border |
| separator | 0.5px | `var(--border-base)` at 10% | Internal dividers within cards |

#### Focus Ring

The focus ring uses a warm sepia tone -- consistent with the theme's accent -- with a page-colored gap ring to prevent bleed:

- **Layer 1:** `0 0 0 2px var(--page)` -- gap ring in page color
- **Layer 2:** `0 0 0 4px rgba(196, 149, 106, 0.50)` -- solid sepia ring
- **Offset:** 2px effective (via the gap ring)

**Full CSS:**

```css
:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--page),
    0 0 0 4px rgba(196, 149, 106, 0.50);
}
```

No glow bloom on the focus ring. The darkroom does not glow -- it absorbs. The ring is solid and warm, like the edge of a developing print.

---

## Component States

All component states use the warmth-shift system. Hover warms the surface. Focus adds the sepia focus ring. Active deepens. Transitions are slow and deliberate -- the chemical reveal philosophy extends to micro-interactions.

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `var(--accent-primary)` (`#C4956A`), border none, color `var(--text-onAccent)`, radius 6px, h 34px, padding `0 16px`, font button (Spectral 14px/600), box-shadow none |
| Hover | bg lightens to `#D0A57A` (L+0.04), subtle warmth bloom: `0 0 12px rgba(196, 149, 106, 0.12)` |
| Active | transform `scale(0.97)`, bg darkens to `#B8886A` |
| Focus | focus ring: `0 0 0 2px var(--page), 0 0 0 4px rgba(196, 149, 106, 0.50)` |
| Disabled | opacity 0.4, pointer-events none, box-shadow none, filter `grayscale(0.3)` |
| Transition | background-color 250ms ease-out, transform 120ms ease-out, box-shadow 400ms ease-out |

#### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid var(--border-base)` at 18%, color `var(--text-secondary)`, radius 6px, size 34x34px, box-shadow none |
| Hover | bg `var(--active)`, border at 28%, color `var(--text-primary)` |
| Active | transform `scale(0.97)`, bg `var(--surface)` |
| Focus | focus ring |
| Disabled | opacity 0.4, pointer-events none |
| Transition | all 300ms ease-out |

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, border `1px solid var(--border-base)` at 18%, radius 8px, h 44px, padding `0 14px`, color `var(--text-primary)`, placeholder `var(--text-muted)`, caret-color `var(--accent-primary)`, box-shadow none |
| Hover | border at 28%, bg warms: `var(--shift-warm)` |
| Focus | border `1px solid var(--accent-primary)` at 35%, focus ring, outline none |
| Disabled | opacity 0.4, pointer-events none, bg `var(--bg)`, cursor not-allowed |
| Transition | border-color 200ms ease-out, background-color 400ms ease-out, box-shadow 200ms ease-out |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, radius 20px, border `1px solid var(--border-base)` at 18%, box-shadow none |
| Hover | border at 28%, bg `var(--shift-warm)` |
| Focus-within | border `1px solid var(--accent-primary)` at 30%, bg `var(--shift-warmer)` |
| Transition | all 400ms ease-out |

#### Cards

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, border `1px solid var(--border-base)` at 18%, radius 8px, box-shadow none |
| Hover | border at 28%, bg `var(--shift-warm)` -- the card warms like a print developing |
| Transition | background-color 500ms ease-out, border-color 250ms ease-out |

Note: The card hover transition is intentionally slow (500ms for bg, 250ms for border). The background warmth develops gradually, like an image appearing in a tray. The border responds faster because it is the edge where chemistry meets paper first.

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `var(--text-secondary)`, radius 6px, h 34px, padding `6px 14px`, font bodySmall (Spectral 14px/400) |
| Hover | bg `var(--bg)`, color `var(--text-primary)` |
| Active (current) | bg `var(--active)`, color `var(--accent-primary)`, font-weight 500 |
| Active press | transform `scale(0.985)` |
| Transition | color 120ms ease-out, background 200ms ease-out |

#### Chips

| State | Properties |
|---|---|
| Rest | bg `var(--bg)`, border `1px solid var(--border-base)` at 12%, radius 16px, h 30px, padding `0 12px`, font bodySmall (Spectral 14px/400), color `var(--text-secondary)` |
| Hover | border at 22%, color `var(--text-primary)`, bg `var(--shift-warm)` |
| Active (selected) | bg `rgba(196, 149, 106, 0.12)`, border-color `var(--accent-primary)` at 25%, color `var(--accent-primary)` |
| Active press | transform `scale(0.98)` |
| Transition | all 250ms ease-out |

#### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 38px |
| Track height | 22px |
| Track radius | 9999px (full) |
| Track off bg | `var(--bg)` |
| Track off border | `1px solid var(--border-base)` at 25% |
| Track on bg | `var(--accent-primary)` -- sepia. The toggle is "developed." |
| Track on box-shadow | none (no glow -- darkrooms do not glow) |
| Thumb | 18px circle, `var(--text-primary)` (paper white) |
| Thumb shadow | none |
| Transition | 300ms ease-out -- slow, deliberate switch |
| Focus-visible | focus ring on track |

#### User Bubble

| Property | Value |
|---|---|
| bg | `var(--active)` |
| radius | 16px |
| padding | 10px 16px |
| max-width | 75ch |
| color | `var(--text-primary)` |
| alignment | right |
| border | `1px solid var(--border-base)` at 12% |

---

## Motion Map

The darkroom's motion philosophy is **chemical reveal**. Things do not appear -- they develop. The fastest interaction in this theme (sidebar hover) is 120ms. The slowest (page entry, chemical reveal) is 2500ms. Most transitions sit in the 250-500ms range, which is slow by UI standards but authentic to the theme's analog character.

Three custom easings define the motion vocabulary:

#### Easings

| Name | Value | Character |
|---|---|---|
| developer | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Slow ramp, gentle settle. The pace of chemistry. Used for most transitions. |
| stop-bath | `cubic-bezier(0.0, 0.0, 0.58, 1.0)` | Abrupt start, gradual finish. Like dunking a print in stop bath -- the action is decisive, the settling is gentle. Used for active/press states. |
| fixer | `cubic-bezier(0.22, 1, 0.36, 1)` | Long deceleration tail. The print is almost done developing; the last details resolve slowly. Used for reveals and page transitions. |
| rinse | `cubic-bezier(0.45, 0, 0.55, 1)` | Symmetrical, flowing. Used for ambient grain animation and continuous loops. |
| expose | `cubic-bezier(0.0, 0.5, 0.5, 1.0)` | Front-loaded acceleration, then gradual halt. The moment the enlarger light hits the paper. Used for hover warmth. |

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 120ms / 200ms | developer | Color changes before background. Sequential, not simultaneous. |
| Button hover warmth | 250ms | expose | Background warms gradually, like paper receiving light. |
| Button press scale | 120ms | stop-bath | Decisive, then settles. |
| Toggle slide | 300ms | developer | Slow, deliberate. Toggling is a commitment. |
| Input focus border | 200ms | developer | Border warms into sepia. |
| Input background warmth | 400ms | fixer | Background warmth develops after border -- layered reveal. |
| Card hover warmth | 500ms | expose | The slowest component hover. The card develops like a print. |
| Card border on hover | 250ms | developer | Border responds before background. |
| Chip select | 250ms | developer | Standard pace. |
| Ghost icon hover | 300ms | developer | |
| Panel slide-in | 700ms | fixer | Long deceleration. Panel glides in and settles. |
| Modal enter | 600ms | fixer | Slow fade + scale. The modal develops into view. |
| Modal exit | 400ms | developer | Exits faster than it enters. |
| Hero/page entry | 2500ms | fixer | The chemical reveal. Full 2.5s development. |
| Popover appear | 300ms | developer | |
| Tooltip show | 200ms | developer | |
| Chemical reveal (elements) | 2000-3000ms | fixer | Signature animation. Opacity builds in layered stages. |
| Film grain loop | 8000ms | rinse | Continuous, symmetrical, infinite. |

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Barely perceptible. The darkroom is quiet. |
| Chips | 0.98 | Subtle. |
| Buttons | 0.97 | Standard. |
| Tabs | 0.96 | Pronounced. |
| Cards (clickable) | 0.995 | Nearly imperceptible -- cards are large surfaces. |

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 720px | Main content column. Slightly narrower than standard -- editorial reading width. |
| Narrow max-width | 640px | Landing/focused content. Intimate reading. |
| Sidebar width | 260px | Fixed sidebar. |
| Header height | 48px | Top bar. |
| Spacing unit | 4px | Base multiplier. |

#### Spacing Scale

4, 6, 8, 12, 16, 24, 32, 48, 64px

The scale extends to 64px to support the generous whitespace this theme demands. Editorial layouts need breathing room.

#### Density

**Comfortable.** This theme prioritizes reading comfort and breathing room over information density. Card padding is generous (16-20px). List gaps are 10-12px. The interface does not crowd -- it invites you to look slowly.

| Context | Padding | Gap |
|---|---|---|
| Card internal | 16-20px | -- |
| List items | -- | 10px |
| Section spacing | -- | 32-48px |
| Form field groups | -- | 16px |
| Sidebar item | 6px 14px | 2px |

#### Radius Scale

| Token | Value | Usage |
|---|---|---|
| none | 0px | -- |
| sm | 4px | Small elements, badges |
| md | 6px | Buttons, sidebar items, menu items |
| lg | 8px | Cards, inputs |
| xl | 12px | Popovers |
| 2xl | 16px | Modal containers, user bubbles |
| input | 8px | Form inputs, textareas |
| pill | 20px | Chat input card |
| full | 9999px | Avatars, toggles, chips |

Radii are conservative. Sharp-cornered would feel too digital; over-rounded would feel too soft. The 6-8px range is the sweet spot -- the gentle curve of a photographic print's corners.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (260px) + content column (720px max). Film grain and vignette at full intensity.
- **md (768px):** Sidebar collapses to overlay panel (slides in at 700ms fixer easing). Content fills width at 640px max.
- **sm (640px):** Single column. Card radius reduces from 8px to 6px. Chat input radius reduces from 20px to 12px. Grain effect simplifies (see Mobile Notes). Section spacing reduces from 48px to 32px.

---

## Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring | `0 0 0 2px var(--page), 0 0 0 4px rgba(196, 149, 106, 0.50)` -- warm sepia ring with page-colored gap |
| Disabled opacity | 0.4 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled filter | `grayscale(0.3)` -- desaturate in addition to dimming |
| Selection bg | `rgba(196, 149, 106, 0.20)` |
| Selection color | `var(--text-primary)` (unchanged) |
| Scrollbar width | thin |
| Scrollbar thumb | `var(--border-base)` at 30% |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

**Contrast verification:**
- `#E8E0D4` (text-primary) on `#0E0C0A` (page): 14.2:1 -- passes AAA
- `#E8E0D4` on `#211C18` (surface): 10.1:1 -- passes AAA
- `#A89A8A` (text-secondary) on `#0E0C0A`: 6.8:1 -- passes AA
- `#A89A8A` on `#211C18` (surface): 4.8:1 -- passes AA
- `#7A6E62` (text-muted) on `#0E0C0A`: 4.0:1 -- passes AA for large text (14px+ bold or 18px+). Used only for labels/captions/placeholders at 12px+ weight 500, which qualify. For contexts requiring 4.5:1, lighten to `#8A7E72` (5.0:1).
- `#C4956A` (accent-primary) on `#0E0C0A`: 7.0:1 -- passes AA
- `#C4956A` on `#211C18` (surface): 5.0:1 -- passes AA

#### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.15s !important;
  }

  /* Disable chemical reveal -- elements appear instantly */
  .chemical-reveal {
    opacity: 1 !important;
    animation: none !important;
  }

  /* Disable film grain breathing */
  .film-grain {
    animation: none !important;
  }

  /* Disable vignette pulse if present */
  .page::before {
    animation: none !important;
  }

  /* Disable dodge-and-burn hover effect */
  [data-effect="dodge-burn"] {
    filter: none !important;
  }

  /* Keep surface-shift warmth transitions (they are color changes, not motion) */
  /* background-color transitions are retained at reduced duration */
}
```

---

## Overlays

#### Popover / Dropdown

- **bg:** `var(--surface)` (`#211C18`)
- **border:** `1px solid var(--border-base)` at 25%
- **radius:** 12px
- **box-shadow:** `0 4px 16px rgba(10, 9, 8, 0.40)` -- a warm, dark shadow. Not black, not colored. The shadow of an object in a dimly-lit warm room.
- **backdrop-filter:** `blur(16px)` -- softer than standard. The darkroom is already blurry in the periphery.
- **padding:** 6px
- **z-index:** 50
- **min-width:** 192px, **max-width:** 320px
- **Menu item:** 6px 8px padding, radius 6px, h 34px, font bodySmall (Spectral 14px), color text-secondary
- **Menu item hover:** bg `var(--active)`, color text-primary
- **Transition:** 120ms developer easing
- **Entry animation:** opacity 0 to 1, translateY(4px) to 0, 300ms fixer easing

#### Modal

- **Overlay bg:** `rgba(10, 9, 8, 0.70)` -- warm, heavy dim. The room gets darker, like closing the door further.
- **Overlay backdrop-filter:** `blur(8px)` -- the world outside goes out of focus.
- **Content bg:** `var(--surface)`
- **Content border:** `1px solid var(--border-base)` at 25%
- **Content box-shadow:** `0 8px 32px rgba(10, 9, 8, 0.50)` -- deep warm shadow
- **Content radius:** 16px
- **Entry:** opacity 0 to 1 + scale 0.96 to 1.0, 600ms fixer easing. The modal develops into view.
- **Exit:** opacity 1 to 0 + scale 1.0 to 0.98, 400ms developer easing.

#### Tooltip

- **bg:** `var(--active)` (`#2A2420`)
- **color:** `var(--text-primary)`
- **font:** label size (Spectral 12px), weight 500
- **radius:** 6px
- **padding:** 4px 10px
- **border:** `1px solid var(--border-base)` at 18%
- **box-shadow:** `0 2px 8px rgba(10, 9, 8, 0.30)`
- **No arrow.** Position via offset.

---

## Visual Style

#### Film Grain

Film grain is the material signature of this theme. Every surface carries a subtle noise overlay that breathes slowly -- the grain pattern shifts over an 8-second cycle, creating the impression of a living photographic surface.

**Technique:** SVG feTurbulence filter applied as a `::after` pseudo-element on the page container, composited with `mix-blend-mode: soft-light` at very low opacity.

```css
.page::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 2;
  opacity: 0.035;
  mix-blend-mode: soft-light;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='grain'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23grain)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  animation: grain-breathe 8s rinse infinite;
}

@keyframes grain-breathe {
  0%, 100% { opacity: 0.035; transform: translate(0, 0); }
  25% { opacity: 0.04; transform: translate(-1px, 1px); }
  50% { opacity: 0.03; transform: translate(1px, -1px); }
  75% { opacity: 0.038; transform: translate(-1px, -1px); }
}
```

The grain breathes: opacity oscillates between 3% and 4%, and the position shifts by 1px to prevent the pattern from appearing static. This is barely perceptible but creates a living, organic surface.

#### Safe-Light Ambient Wash

A barely-visible radial gradient tints the upper portion of the page with the safe-light color, simulating the overhead red bulb:

```css
.page::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background: radial-gradient(
    ellipse at 50% 15%,
    rgba(139, 58, 42, 0.035),
    transparent 60%
  ),
  radial-gradient(
    ellipse at 50% 30%,
    transparent 40%,
    rgba(10, 9, 8, 0.35) 80%,
    rgba(10, 9, 8, 0.55) 100%
  );
}
```

This combines the safe-light wash (first gradient, from above) with the vignette (second gradient, darkening edges). The safe-light tint at 3.5% opacity is barely perceptible but gives the room its characteristic warmth.

#### Material

- **Grain:** Moderate (3-4%). `feTurbulence` fractalNoise, stitchTiles, 4 octaves.
- **Grain technique:** SVG feTurbulence inlined as data URI. More predictable than CSS noise functions across browsers.
- **Gloss:** Matte. Every surface has tooth. No reflections, no sheen, no glass effects.
- **Blend mode:** `soft-light` for grain overlay. `normal` for all surface backgrounds.
- **Shader bg:** No. The darkroom is still and physical. No digital noise fields.

---

## Signature Animations

#### 1. Chemical Reveal (Page Entry)

The defining animation. When a page loads, elements do not simply fade in -- they develop like a photographic print in chemistry. The reveal happens in three stages, mimicking the actual chemical development process:

**Stage 1 -- Ghost Image (0-800ms):** Elements appear at 8% opacity with slight blur. The faintest suggestion of form, like the first seconds of a print in developer.

**Stage 2 -- Midtone Fill (800-1800ms):** Opacity builds to 60%. The image's structure becomes clear. Blur reduces. Colors begin to resolve from desaturated to warm.

**Stage 3 -- Full Development (1800-2500ms):** Opacity reaches 100%. All detail resolves. The element is fully "developed."

Elements stagger at 150ms intervals (much longer than typical 30-50ms staggers) -- each element begins its development slightly after the previous one, like multiple prints being processed in sequence.

```css
@keyframes chemical-reveal {
  0% {
    opacity: 0;
    filter: blur(2px) saturate(0.3);
    transform: translateY(4px);
  }
  15% {
    opacity: 0.08;
    filter: blur(1.5px) saturate(0.4);
    transform: translateY(3px);
  }
  40% {
    opacity: 0.35;
    filter: blur(0.8px) saturate(0.6);
    transform: translateY(2px);
  }
  70% {
    opacity: 0.65;
    filter: blur(0.3px) saturate(0.85);
    transform: translateY(0.5px);
  }
  100% {
    opacity: 1;
    filter: blur(0) saturate(1);
    transform: translateY(0);
  }
}

.chemical-reveal {
  animation: chemical-reveal 2.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}

/* Stagger children */
.chemical-reveal-container > *:nth-child(1) { animation-delay: 0ms; }
.chemical-reveal-container > *:nth-child(2) { animation-delay: 150ms; }
.chemical-reveal-container > *:nth-child(3) { animation-delay: 300ms; }
.chemical-reveal-container > *:nth-child(4) { animation-delay: 450ms; }
.chemical-reveal-container > *:nth-child(5) { animation-delay: 600ms; }
.chemical-reveal-container > *:nth-child(6) { animation-delay: 750ms; }
.chemical-reveal-container > *:nth-child(7) { animation-delay: 900ms; }
.chemical-reveal-container > *:nth-child(8) { animation-delay: 1050ms; }
```

**Reduced motion:** Elements appear instantly at full opacity. No blur, no translate.

#### 2. Dodge and Burn Hover

In darkroom printing, "dodging" means blocking light to lighten an area, and "burning" means adding light to darken it. This animation applies the concept to hover states: when you hover over an element, the element subtly brightens (dodged) while the surrounding area dims slightly (burned).

```css
@keyframes dodge {
  0% { filter: brightness(1); }
  100% { filter: brightness(1.08); }
}

.dodge-burn-target {
  transition: filter 400ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.dodge-burn-target:hover {
  filter: brightness(1.08);
}

/* The container dims slightly when a child is hovered */
.dodge-burn-container:has(.dodge-burn-target:hover) {
  filter: brightness(0.95);
  transition: filter 600ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

/* But the hovered element overrides its parent's dimming */
.dodge-burn-container:has(.dodge-burn-target:hover) .dodge-burn-target:hover {
  filter: brightness(1.08);
}
```

The dodge effect (400ms) is faster than the burn effect (600ms) -- the eye goes to the light first, then the surroundings dim. This creates a natural focal-point effect.

**Reduced motion:** Disabled. No brightness changes.

#### 3. Film Grain Breathe

The continuous grain overlay animation described in the Visual Style section. The grain is always alive, always shifting -- the surface is never perfectly still, just as real film grain is never static.

```css
@keyframes grain-breathe {
  0%, 100% {
    opacity: 0.035;
    transform: translate(0, 0) scale(1);
  }
  25% {
    opacity: 0.042;
    transform: translate(-1px, 1px) scale(1.01);
  }
  50% {
    opacity: 0.028;
    transform: translate(1px, -1px) scale(0.99);
  }
  75% {
    opacity: 0.038;
    transform: translate(-1px, -1px) scale(1.005);
  }
}

.film-grain {
  animation: grain-breathe 8s cubic-bezier(0.45, 0, 0.55, 1) infinite;
}
```

**Timing:** 8000ms, infinite loop. `rinse` easing (symmetrical).
**Reduced motion:** Grain freezes at 3.5% opacity, no transform. The texture remains but does not move.

#### 4. Developing Tray Ripple

When a card or container receives new content (e.g., a message appears in a chat), a subtle ripple effect mimics the surface of liquid in a developing tray being disturbed. The ripple is a single concentric ring of warmth that expands outward from the center of the new content.

```css
@keyframes tray-ripple {
  0% {
    box-shadow: inset 0 0 0 0 rgba(196, 149, 106, 0.08);
  }
  40% {
    box-shadow: inset 0 0 30px 10px rgba(196, 149, 106, 0.04);
  }
  100% {
    box-shadow: inset 0 0 60px 30px rgba(196, 149, 106, 0);
  }
}

.tray-ripple {
  animation: tray-ripple 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
```

**Timing:** 1200ms, plays once per content insertion. `fixer` easing.
**Reduced motion:** Disabled. Content appears without ripple.

#### 5. Contact Sheet Scan

For gallery/grid views, elements can enter with a contact-sheet pattern: they appear in a left-to-right, top-to-bottom sequence, as if someone is scanning across a contact sheet of negatives with a loupe. Each element develops independently (chemical reveal) but the stagger follows the reading pattern of a contact sheet.

```css
.contact-sheet-grid {
  display: grid;
  gap: 8px;
}

.contact-sheet-grid > * {
  animation: chemical-reveal 2s cubic-bezier(0.22, 1, 0.36, 1) both;
}

/* Row-major stagger: left-to-right, top-to-bottom */
/* For a 4-column grid: */
.contact-sheet-grid > *:nth-child(1) { animation-delay: 0ms; }
.contact-sheet-grid > *:nth-child(2) { animation-delay: 100ms; }
.contact-sheet-grid > *:nth-child(3) { animation-delay: 200ms; }
.contact-sheet-grid > *:nth-child(4) { animation-delay: 300ms; }
.contact-sheet-grid > *:nth-child(5) { animation-delay: 350ms; }
.contact-sheet-grid > *:nth-child(6) { animation-delay: 450ms; }
.contact-sheet-grid > *:nth-child(7) { animation-delay: 550ms; }
.contact-sheet-grid > *:nth-child(8) { animation-delay: 650ms; }
.contact-sheet-grid > *:nth-child(9) { animation-delay: 700ms; }
.contact-sheet-grid > *:nth-child(10) { animation-delay: 800ms; }
.contact-sheet-grid > *:nth-child(11) { animation-delay: 900ms; }
.contact-sheet-grid > *:nth-child(12) { animation-delay: 1000ms; }
```

Note: The row-start delays (items 1, 5, 9) are closer together (350ms gap between rows vs 100ms within a row). This creates a natural reading rhythm -- quick scan across, slight pause at the row break.

**Reduced motion:** All elements appear simultaneously at full opacity.

---

## Dark Mode Variant (Light Mode)

This is a **dark-native** theme. The darkroom IS dark -- a light mode would be like turning on the fluorescent lights in a darkroom. It would destroy the paper.

However, a "proof sheet" light variant is available for contexts where a dark interface is not appropriate (e.g., printing, daytime reading, accessibility requirements):

#### Light Mode: Proof Sheet

| Token | Dark (Native) | Light (Proof Sheet) | Notes |
|---|---|---|---|
| page | `#0E0C0A` | `#F4F0EA` | Warm cream, like fiber-based paper |
| bg | `#171311` | `#EBE6DE` | Warm off-white |
| surface | `#211C18` | `#FFFFFF` | Pure white -- the white border of a mounted print |
| recessed | `#0A0908` | `#E2DCD4` | Warm grey, like a cardboard mat |
| active | `#2A2420` | `#DDD6CC` | Slightly darker warm |
| text-primary | `#E8E0D4` | `#1A1612` | Near-black, warm |
| text-secondary | `#A89A8A` | `#6A5E52` | Muted warm brown |
| text-muted | `#7A6E62` | `#9A8E82` | Lighter warm grey |
| accent-primary | `#C4956A` | `#9A6A3A` | Darker sepia for contrast on light bg |
| accent-secondary | `#5A7A9A` | `#3A5A7A` | Darker blue for contrast |
| border-base | `#8A6A52` | `#C4B4A2` | Warm sand |
| safe-light | `#8B3A2A` | N/A | Removed. No safe-light in daylight. |

**Light mode rules:**
- Film grain overlay: Disabled. Light mode is the "proof sheet under daylight" -- grain is a dark-mode atmospheric effect.
- Vignette: Disabled. Even lighting on a proof sheet.
- Safe-light ambient wash: Disabled.
- Chemical reveal animation: Replaced with a simpler fade-in (400ms, fixer easing). The metaphor shifts from "developing in chemistry" to "pulling a print from a box."
- Shadows return: Since surface-shifts are harder to perceive on light backgrounds, light mode adds subtle warm shadows: `0 1px 3px rgba(26, 22, 18, 0.06)` on cards, `0 2px 8px rgba(26, 22, 18, 0.10)` on popovers.
- Border opacity increases: subtle goes from 10% to 12%, card from 18% to 22%, hover from 28% to 32%, focus from 38% to 42%. Borders are harder to see on light backgrounds.
- Typography remains unchanged. The all-serif stack works equally well on light paper.
- The decision principle shifts: "When in doubt, ask: would this look right on a gallery wall?" The environment changes from intimate darkroom to public exhibition.

---

## Mobile Notes

#### Effects to Disable on Mobile

- **Film grain overlay** -- Remove entirely. SVG feTurbulence with `mix-blend-mode: soft-light` is expensive on mobile GPUs. The surface becomes smooth.
- **Vignette gradient** -- Remove. Saves a compositing layer.
- **Safe-light ambient wash** -- Remove. Combined with vignette removal, the `::before` pseudo is eliminated.
- **Dodge-and-burn hover** -- There is no hover on touch. Remove.
- **Contact-sheet scan stagger** -- Reduce stagger to 50ms per item (from 100ms). Mobile users expect faster grid population.

#### Effects to Simplify on Mobile

- **Chemical reveal** -- Reduce duration from 2500ms to 1200ms. Remove blur stages (keep only opacity). Mobile browsers struggle with animated filter: blur.
- **Tray ripple** -- Reduce from 1200ms to 600ms.
- **Film grain breathe** -- If grain is retained on high-end mobile, freeze the animation. Static grain texture at 3% opacity, no transform.

#### Sizing Adjustments

- All interactive elements maintain 44px minimum touch target.
- Body text stays 16px (Spectral already comfortable at this size on mobile).
- Card radius: 8px reduces to 6px.
- Chat input radius: 20px reduces to 14px.
- Card padding: 16-20px reduces to 12-16px.
- Section spacing: 48px reduces to 32px.
- Sidebar: Hidden behind hamburger, slides in as overlay panel (700ms fixer easing).

#### Performance Budget

- Maximum box-shadow blur radius across visible elements: 32px.
- No `backdrop-filter` on elements below the overlay z-index (only modals and popovers get blur).
- `will-change` applied during animations only, removed after.
- `@supports not (mix-blend-mode: soft-light)` fallback: disable grain entirely.
- Ambient animation (grain breathe) disabled entirely on mobile.

---

## Data Visualization

| Property | Value |
|---|---|
| Categorical | Sepia `#C4956A`, Chemical Blue `#5A7A9A`, Fixer Amber `#B8924A`, Developer Green `#5A8A5A`, Muted Clay `#9A7060` -- 5 colors at balanced perceptual weight on dark bg |
| Sequential | Single-hue ramp from `#2A2420` (darkest) through `#C4956A` (sepia) to `#E8E0D4` (paper white) |
| Diverging | Sepia `#C4956A` (warm end) to `#5A7A9A` Chemical Blue (cool end) through `#0E0C0A` neutral dark center |
| Grid | Low-ink: `var(--border-base)` at 8% opacity. Grid lines should be nearly invisible. |
| Max hues per chart | 2 (sepia + blue). Additional dimensions use opacity or size, not new hues. |
| Philosophy | Smooth. Data should develop like a print -- continuous tones, no harsh steps. Prefer area charts over bar charts. Prefer gradients over discrete fills. |
| Label font | IBM Plex Mono at 11px, `var(--text-muted)` color. Data labels are quiet metadata. |
| Axis | `var(--border-base)` at 15%. Barely there. Let the data lead. |

---

## Implementation Checklist

- [ ] Google Fonts loaded: DM Serif Display (400), Spectral (400, 500, 600, italic 400), IBM Plex Mono (400)
- [ ] CSS custom properties defined for all palette tokens (page, bg, surface, recessed, active, text-primary/secondary/muted, accent-primary/secondary, border-base, safe-light, semantic colors)
- [ ] Surface-shift tokens implemented via `color-mix(in oklch, ...)` or precalculated hex values
- [ ] Warmth gradient verified: page (coolest) < bg < surface < active (warmest)
- [ ] Film grain SVG feTurbulence applied as `::after` pseudo on page container, `mix-blend-mode: soft-light`, 3.5% opacity
- [ ] Grain breathe animation running at 8s cycle with `rinse` easing
- [ ] Safe-light ambient wash applied as radial-gradient in `::before` pseudo, centered at top, 3.5% opacity
- [ ] Vignette gradient applied in same `::before` pseudo, centered at 50% 30%, darkening edges
- [ ] Border opacity system implemented (10%, 18%, 28%, 38% on `var(--border-base)`)
- [ ] Focus ring on all interactive elements: `0 0 0 2px var(--page), 0 0 0 4px rgba(196, 149, 106, 0.50)`
- [ ] Chemical reveal animation implemented with 3-stage opacity + blur + desaturation
- [ ] Chemical reveal stagger at 150ms intervals per element
- [ ] Dodge-and-burn hover implemented on card grids (brightens target, dims siblings)
- [ ] Component hover transitions using `expose` easing (front-loaded)
- [ ] Card hover warmth transition at 500ms (intentionally slow)
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] `text-wrap: pretty` on body text, `text-wrap: balance` on headings
- [ ] All typography uses serif stack only (no sans-serif in the system)
- [ ] Scrollbar styled: thin, `var(--border-base)` at 30% thumb, transparent track
- [ ] Touch targets >= 44px on all interactive elements
- [ ] Motion map durations verified: slowest at 2500ms (chemical reveal), fastest at 120ms (sidebar hover)
- [ ] `::selection` styled with sepia accent at 20%
- [ ] `::placeholder` color matches `var(--text-muted)` token
- [ ] `prefers-reduced-motion` media query: disables grain animation, chemical reveal, dodge-and-burn, vignette pulse; retains warmth color transitions at 150ms
- [ ] Light mode variant tokens defined and switchable via class or `data-theme` attribute
- [ ] Light mode disables grain, vignette, safe-light wash, and replaces surface-shifts with subtle warm shadows
- [ ] Text contrast verified: text-primary 14.2:1, text-secondary 6.8:1, text-muted 4.0:1 (large text)
- [ ] Mobile: grain overlay removed, vignette removed, chemical reveal simplified to 1200ms opacity-only
- [ ] Mobile: all ambient animations disabled
- [ ] `@supports not (mix-blend-mode: soft-light)` fallback: grain disabled
- [ ] `@supports not (backdrop-filter: blur(1px))` fallback: increased overlay bg opacity to 0.85
- [ ] State transitions tested with correct theme-specific easings (developer, stop-bath, fixer, rinse, expose)
