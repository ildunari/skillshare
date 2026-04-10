# Editorial Calm — Full Specification

> Schema v2 | 760 lines | Last updated: 2026-02-16

## Table of Contents

| Section | Line |
|---|---|
| Identity & Philosophy | 36 |
| Color System | 56 |
| Typography Matrix | 118 |
| Elevation System | 166 |
| Border System | 212 |
| Component States | 251 |
| Motion Map | 382 |
| Overlays | 434 |
| Layout Tokens | 487 |
| Accessibility Tokens | 537 |
| Visual Style | 565 |
| Signature Animations | 617 |
| Dark Mode Variant | 670 |
| Data Visualization | 724 |
| Mobile Notes | 738 |
| Implementation Checklist | 765 |

---

## 1. Editorial Calm

> Warm editorial matte -- the Anthropic aesthetic. A beautifully typeset magazine spread in a sunlit room.

**Best for:** Generative art, particle systems, SaaS dashboards, analytics, data visualization, long-form editorial, content platforms, design tools, thoughtful productivity apps.

---

### Identity & Philosophy

This theme lives in a sunlit room with a cup of coffee. The table is natural wood. The paper is warm beige with visible tooth. The ink is terracotta and charcoal. Outside the window, morning light casts long warm shadows. Nothing is glossy. Nothing blinks. The interface reads like a considered publication -- every element placed with typographic intention, every whitespace earned.

The core tension is warmth vs precision. Editorial Calm is both cozy (warm beige, terracotta, matte textures) and exacting (variable font weights to the unit, pixel-precise shadow composites, opacity systems with four named levels). It feels approachable but never casual. Friendly but never sloppy.

Two modes share one soul. **Canvas mode** (warm beige background, generative art and visualizations) and **Dashboard mode** (warm white background, SaaS and analytics) are not separate themes -- they are the same editorial voice applied to different tasks. The same fonts, the same warm undertones, the same terracotta accent, the same motion personality. What changes is density, background temperature, and data display philosophy.

**Decision principle:** "When in doubt, ask: would a thoughtful print designer do this? If it feels like a web template, remove it. If it feels like a magazine layout, keep it."

**What this theme is NOT:**
- Not glossy, shiny, or glassmorphic
- Not cold or clinical -- warmth is in every token
- Not sparse to emptiness -- editorial density means content is present and well-organized, not hidden
- Not playful -- no bouncy springs, no overshoots, no wiggles
- Not gradient-heavy -- flat matte surfaces with tint-stepping, never gradient fills
- No pure black (`#000000`) or pure white (`#FFFFFF`) anywhere -- every neutral carries warm undertone

---

### Color System

#### Palette

All neutrals carry a warm yellow-brown undertone (hue 34-60 in HSL). The accent is terracotta-orange, which reads as warm editorial ink -- not alerting like red, not cold like blue, distinctly Anthropic. Semantic colors are desaturated to coexist with the warm neutral palette.

| Token | Name | Hex | HSL | Role |
|---|---|---|---|---|
| page | Warm Stone | `#E8E3DA` | 38 18% 88% | Deepest background -- the "table beneath the paper." Slightly darker than bg, grounds the page. |
| bg (Canvas) | Warm Beige | `#F0EBE3` | 37 26% 91% | Primary surface in Canvas mode. The classic Anthropic warm paper tone. |
| bg (Dashboard) | Warm White | `#F7F7F5` | 60 8% 96% | Primary surface in Dashboard mode. Cleaner, less saturated -- lets data breathe. |
| surface | Cream | `#FAF8F4` | 45 33% 97% | Cards, inputs, elevated surfaces. Lighter than bg -- tint-step creates lift without shadow. |
| recessed | Warm Sand | `#EDE8DF` | 38 23% 89% | Code blocks, inset areas, recessed panels. Darker than bg, signals "secondary." |
| active | Light Sand | `#E5DFD5` | 36 21% 86% | Active/pressed states, selected sidebar items, user bubble. |
| text-primary | Warm Charcoal | `#2C2925` | 34 9% 16% | Headings, body text. Near-black with warm cast -- never pure black. |
| text-secondary | Stone | `#6B6560` | 25 5% 40% | Sidebar items, secondary labels, icon default color. |
| text-muted | Haze | `#9C9690` | 30 4% 59% | Placeholders, timestamps, metadata, section labels. |
| text-onAccent | Cream White | `#FFF8F2` | 30 100% 97% | Text on accent-colored backgrounds. Warm white, not pure white. |
| border-base | Sand Veil | `#C4BAA8` | 39 16% 71% | Base border color, always used at variable opacity. Never applied as solid. |
| accent-primary | Terracotta | `#D97757` | 15 63% 60% | Brand accent, primary CTA, Claude icon. The Anthropic signature. |
| accent-secondary | Burnt Sienna | `#C15F3C` | 15 53% 50% | Hover state for CTA, Canvas mode density map high-energy. |
| success | Forest Sage | `#5A8A50` | 110 28% 43% | Positive states, completion indicators. Desaturated green with warm undertone. |
| warning | Warm Amber | `#B17506` | 39 93% 36% | Caution states. Amber that sits naturally in the warm palette. |
| danger | Muted Coral | `#C4534A` | 3 46% 53% | Error states, destructive actions. Desaturated, not alarming, still clearly danger. |
| info | Warm Blue | `#5B7FA5` | 212 30% 50% | Informational states. Cool enough to read as "info" but desaturated. |

#### Special Colors

| Token | Value | Role |
|---|---|---|
| inlineCode | `#B85C3A` | Code text within prose -- darker terracotta, reads as "different register." |
| toggleActive | `#2C84DB` | Toggle/switch active track. Blue, distinct from terracotta accent. |
| selection | `rgba(217, 119, 87, 0.18)` | `::selection` background. Terracotta at 18% opacity. |

#### Fixed Colors

| Token | Hex | Role |
|---|---|---|
| alwaysBlack | `#000000` | Shadow base (mode-independent) |
| alwaysWhite | `#FFFFFF` | On-dark emergencies only (mode-independent) |

#### Opacity System

One border base color (`#C4BAA8`) at variable opacity produces the entire border vocabulary:

| Level | Opacity | Usage |
|---|---|---|
| subtle | 15% | Sidebar edges, hairlines, lightest separation, input border at rest |
| card | 25% | Card borders, file cards, input shadow ring at rest |
| hover | 30% | Hover states, popovers, share button border |
| focus | 40% | Focus borders, active emphasis, maximum non-ring border visibility |

#### Color Rules

- **Terracotta is earned.** Used only for accent actions (CTA buttons, active toggles in accent style), the Claude icon, and data visualization primaries. Never decorative fill.
- **No gradients on surfaces.** Flat matte tints only. Surface hierarchy comes from tint-stepping, not gradients.
- **Semantic colors are desaturated.** Success/warning/danger sit at reduced saturation so they coexist with warm neutrals without creating jarring contrast.
- **Border-base is warm sand.** Borders are part of the surface system, not layered on top. They share the warm undertone family.
- **Red is reserved for danger.** No decorative reds. Coral and sienna tones in Canvas mode particle mapping are distinct from the danger red.

---

### Typography Matrix

#### Font Families

| Slot | Font | Fallback | Role |
|---|---|---|---|
| sans (display) | Plus Jakarta Sans | system-ui, -apple-system, sans-serif | Display, Heading, Subheading. Refined geometric sans for architectural roles. |
| sans (body) | DM Sans | system-ui, -apple-system, sans-serif | Body, Body Small, Button, Input, Label, Caption. Clean, readable workhorse. |
| mono | Geist Mono | ui-monospace, SFMono-Regular, Menlo, Monaco, monospace | Code, data values. Modern monospace, clean numerals. |

**Family switch boundary:** Plus Jakarta Sans handles the three largest typographic roles (Display, Heading, Subheading). DM Sans handles everything else (Body, Body Small, Button, Input, Label, Code caption, Caption). An implementer should never mix them beyond this boundary. Both are geometric sans-serifs from the same design universe; the switch is subtle and intentional. Jakarta is more architectural (sharper joints, tighter apertures), DM Sans is rounder and more neutral (better for sustained reading).

**Why this pairing:** Plus Jakarta Sans and DM Sans share geometric DNA but differ in personality. Jakarta adds refinement to headlines without being flashy. DM Sans (#1 on Typewolf 2026) adds warmth to body text without being soft. Geist Mono completes the trio with a modern monospace that feels contemporary rather than retro -- important because this theme is warm and editorial, not nostalgic.

#### Role Matrix

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Plus Jakarta Sans | 38px | 290 | 1.2 (45.6px) | -0.02em | `font-variation-settings: "opsz" 48` | Hero greetings, page titles, marketing headlines |
| Heading | Plus Jakarta Sans | 24px | 460 | 1.3 (31.2px) | -0.01em | -- | Section titles, settings headers, card group titles |
| Subheading | Plus Jakarta Sans | 18px | 500 | 1.35 (24.3px) | normal | -- | Card titles, subsection headers (theme-specific addition beyond 9 standard roles) |
| Body | DM Sans | 16px | 400 | 1.5 (24px) | normal | -- | Primary reading text, UI body, descriptions |
| Body Small | DM Sans | 14px | 400 | 1.4 (19.6px) | normal | -- | Sidebar items, form labels, secondary UI text |
| Button | DM Sans | 14px | 460 | 1.4 (19.6px) | normal | -- | Button labels, emphasized small UI text |
| Input | DM Sans | 14px | 430 | 1.4 (19.6px) | normal | -- | Form input text. Heavier than body-small for readability in fields. |
| Label | DM Sans | 12px | 400 | 1.33 (16px) | 0.02em | -- | Section labels ("Starred", "Recents"), metadata, timestamps |
| Code | Geist Mono | 0.9em (14.4px at 16px base) | 360 | 1.5 (21.6px) | normal | `font-variant-numeric: tabular-nums` | Inline code, code blocks, data values |
| Caption | DM Sans | 12px | 400 | 1.33 (16px) | normal | -- | Disclaimers, footnotes, bottom-of-page text |

**Variable weight rationale:** 290 for display creates ultra-light editorial headlines (magazine thinness). 400 is standard reading weight. 430 for inputs adds just enough heft to make typed text feel "present" in a field. 460 for buttons and headings signals "interactive" or "structural" without the bluntness of 500+. 500 for subheadings sits between heading (460) and bold emphasis (530+). These precise values are only possible with variable fonts.

#### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@200..800&family=DM+Sans:wght@100..1000&display=swap" rel="stylesheet">
```

Note: Geist Mono is available via `https://cdn.jsdelivr.net/npm/geist@1/dist/fonts/geist-mono/style.css` or can be self-hosted from the Vercel Geist package.

- **Font smoothing:** `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale` on `<html>`.
- **Font display:** `font-display: swap` on all families.
- **Optical sizing:** `font-optical-sizing: auto` for variable fonts with `opsz` axis.
- **Text wrap:** `text-wrap: balance` for headings, `text-wrap: pretty` for body paragraphs.

---

### Elevation System

**Strategy:** Surface-shifts + subtle composite shadows.

Separation between surfaces is achieved primarily through tint-stepping (the bg token is lighter than the page token; the surface token is lighter than the bg token). Interactive elements gain subtle composite shadows: a wide soft drop shadow for depth plus a tight 0.5px spread ring for edge definition. No visible dividers between major page sections. A single 0.5px hairline border separates sidebar from content. Popovers add `backdrop-filter: blur(24px)`. No inset shadows are used anywhere.

#### Surface Hierarchy

| Surface | Background | Shadow | Usage |
|---|---|---|---|
| page | `#E8E3DA` (page) | none | Deepest layer. The "table" the paper sits on. |
| canvas | `#F0EBE3` Canvas / `#F7F7F5` Dashboard | none | Primary working surface, sidebar background. |
| card | `#FAF8F4` (surface) | shadow-input | Input card, form inputs, menus at rest. |
| recessed | `#EDE8DF` (recessed) | none | Code blocks, inset areas. |
| active | `#E5DFD5` (active) | none | Active sidebar item, user message bubble, pressed states. |
| overlay | `#FAF8F4` (surface) | shadow-popover | Popovers, dropdowns, modals. |

#### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `0 1px 2px rgba(44, 41, 37, 0.04)` | Small elements, file cards. |
| shadow-md | `0 4px 6px -1px rgba(44, 41, 37, 0.06), 0 2px 4px -2px rgba(44, 41, 37, 0.04)` | Scroll-to-bottom button, medium elevation. |
| shadow-input | `0 4px 20px rgba(44, 41, 37, 0.03), 0 0 0 0.5px rgba(196, 186, 168, 0.25)` | Input card rest state. Warm-tinted drop shadow + border ring. |
| shadow-input-hover | `0 4px 20px rgba(44, 41, 37, 0.03), 0 0 0 0.5px rgba(196, 186, 168, 0.30)` | Input card hover. Ring brightens from 25% to 30%. |
| shadow-input-focus | `0 4px 20px rgba(44, 41, 37, 0.06), 0 0 0 0.5px rgba(196, 186, 168, 0.30)` | Input card focus-within. Drop shadow deepens from 3% to 6%. |
| shadow-popover | `0 2px 8px rgba(44, 41, 37, 0.12)` | Menus, popovers, dropdowns. |
| shadow-none | `none` | Flat surfaces, disabled states, recessed areas. |

**Light mode shadow note:** Shadow base color is `rgba(44, 41, 37, ...)` (warm near-black matching text-primary) rather than pure black. On very warm or very light backgrounds, the rest-state shadow at 3% may appear nearly invisible. If implementing on backgrounds lighter than `#F0EBE3`, increase shadow percentages by +2% (e.g., 3% becomes 5%, 6% becomes 8%). The shadow system should always be perceptible on hover -- if it is not, the percentages need adjustment.

#### Backdrop Filter

| Context | Value | Usage |
|---|---|---|
| popover | `backdrop-filter: blur(24px)` | Popover/dropdown containers |
| modal | `backdrop-filter: blur(12px)` | Modal overlay background |
| badge | `backdrop-filter: blur(8px)` | File type badges, floating labels |
| none | `backdrop-filter: none` | Default, non-overlay surfaces |

#### Separation Recipe

Tint-step + subtle composite shadow, no visible dividers. The page-to-bg step (from `#E8E3DA` to `#F0EBE3`) creates the primary depth foundation. The bg-to-surface step (from `#F0EBE3` to `#FAF8F4`) lifts cards and inputs. Interactive surfaces add composite shadows (soft drop + tight ring) that escalate with interaction state. Popovers combine the surface tint-step with `backdrop-blur-xl`. Sidebar separation is a single 0.5px hairline at 15% opacity -- the thinnest possible visible line. No horizontal rules in the sidebar. No divider lines between content sections.

---

### Border System

#### Base Color

`#C4BAA8` (Sand Veil). This single warm sand tone, applied at variable opacity, produces the entire border vocabulary. At 15% on warm beige it is barely visible. At 30% it reads as a deliberate edge. At 40% it commands attention for focus states.

#### Widths and Patterns

| Pattern | Width | Opacity | CSS Value | Usage |
|---|---|---|---|---|
| subtle | 0.5px | 15% | `0.5px solid rgba(196, 186, 168, 0.15)` | Sidebar right edge, hairlines, lightest separation |
| card | 0.5px | 25% | `0.5px solid rgba(196, 186, 168, 0.25)` | File cards, card borders |
| hover | 0.5px | 30% | `0.5px solid rgba(196, 186, 168, 0.30)` | Hover states, popovers, share button |
| input | 1px | 15% | `1px solid rgba(196, 186, 168, 0.15)` | Form input borders at rest |
| input-hover | 1px | 30% | `1px solid rgba(196, 186, 168, 0.30)` | Form input borders on hover |

#### Width Scale

| Name | Value | Usage |
|---|---|---|
| hairline | 0.5px | Card edges, sidebar separation, popover borders |
| default | 1px | Form input borders, transparent-border-for-hover-swap |
| medium | 1.5px | Heavy emphasis (rare -- only for custom component accents) |
| heavy | 2px | Focus ring width |

#### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(116, 171, 226, 0.56)` |
| Width | 2px solid |
| Style | `outline: 2px solid rgba(116, 171, 226, 0.56)` |
| Offset | `outline-offset: 2px` |
| Applies to | All interactive elements on `:focus-visible` |

Focus ring is blue, not terracotta. Focus rings are functional accessibility signals, not brand elements. Blue provides maximum contrast against the warm palette without reading as semantic color (not success-green or danger-red). This matches the claude.ai production pattern.

---

### Component States

#### Buttons (Primary/Outlined)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: 0.5px solid rgba(196, 186, 168, 0.30)`, `color: #2C2925 (text-primary)`, `border-radius: 6px`, `height: 32px`, `padding: 0 12px`, `font-size: 14px`, `font-weight: 460`, `font-family: DM Sans`, `cursor: pointer` |
| Hover | `bg: #EDE8DF (recessed)`, `border-color: rgba(196, 186, 168, 0.30)` |
| Active | `transform: scale(0.97)`, `shadow: none` |
| Focus | `outline: 2px solid rgba(116, 171, 226, 0.56)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `shadow: none`, `cursor: not-allowed` |
| Transition | `color, background-color, border-color 100ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Buttons (Accent/CTA)

| State | Properties |
|---|---|
| Rest | `bg: #D97757 (accent-primary)`, `border: none`, `color: #FFF8F2 (text-onAccent)`, `border-radius: 6px`, `height: 32px`, `padding: 0 16px`, `font-size: 14px`, `font-weight: 460`, `cursor: pointer` |
| Hover | `bg: #C15F3C (accent-secondary)` |
| Active | `transform: scale(0.97)` |
| Focus | `outline: 2px solid rgba(116, 171, 226, 0.56)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `cursor: not-allowed` |
| Transition | `background-color 100ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Buttons (Ghost/Icon)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: none`, `color: #6B6560 (text-secondary)`, `border-radius: 6px`, `width: 32px`, `height: 32px`, `padding: 0`, `cursor: pointer` |
| Hover | `bg: #EDE8DF (recessed)`, `color: #2C2925 (text-primary)` |
| Active | `transform: scale(0.97)` |
| Focus | `outline: 2px solid rgba(116, 171, 226, 0.56)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none` |
| Transition | `all 300ms cubic-bezier(0.165, 0.85, 0.45, 1)` |

#### Text Input (Settings Form)

| State | Properties |
|---|---|
| Rest | `bg: #FAF8F4 (surface)`, `border: 1px solid rgba(196, 186, 168, 0.15)`, `border-radius: 9.6px`, `height: 44px`, `padding: 0 12px`, `font-size: 14px`, `font-weight: 430`, `font-family: DM Sans`, `color: #2C2925 (text-primary)`, `caret-color: #2C2925` |
| Placeholder | `color: #9C9690 (text-muted)` |
| Hover | `border-color: rgba(196, 186, 168, 0.30)` |
| Focus | `outline: 2px solid rgba(116, 171, 226, 0.56)`, `outline-offset: 2px`, `border-color: rgba(196, 186, 168, 0.30)` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `cursor: not-allowed` |
| Transition | `border-color 150ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Textarea

| State | Properties |
|---|---|
| Rest | Same bg/border/radius as text input. `padding: 12px`, `line-height: 19.6px`, `min-height: 120px`, `resize: vertical`, `white-space: pre-wrap` |
| Hover/Focus/Disabled | Same as text input |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | `bg: #FAF8F4 (surface)`, `border-radius: 20px`, `border: 1px solid transparent`, `box-shadow: shadow-input` |
| Hover | `box-shadow: shadow-input-hover` (ring brightens from 25% to 30%) |
| Focus-within | `box-shadow: shadow-input-focus` (drop shadow deepens from 3% to 6%) |
| Inner textarea | `font-size: 16px`, `line-height: 22.4px`, `bg: transparent`, `color: text-primary`, `placeholder-color: text-muted` |
| Transition | `all 200ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Cards

| State | Properties |
|---|---|
| Rest | `bg: #FAF8F4 (surface)`, `border: 0.5px solid rgba(196, 186, 168, 0.25)`, `border-radius: 8px`, `box-shadow: shadow-sm`, `padding: 20px` |
| Hover | `border-color: rgba(196, 186, 168, 0.30)`, `box-shadow: shadow-md` |
| Focus | `outline: 2px solid rgba(116, 171, 226, 0.56)`, `outline-offset: 2px` (when card is clickable) |
| Transition | `border-color, box-shadow 150ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `color: #6B6560 (text-secondary)`, `border-radius: 6px`, `height: 32px`, `padding: 6px 16px`, `font-size: 12px`, `font-weight: 400`, `font-family: DM Sans`, `white-space: nowrap`, `overflow: hidden`, `cursor: pointer` |
| Hover | `bg: #EDE8DF (recessed)`, `color: #2C2925 (text-primary)` |
| Active (current) | `bg: #E5DFD5 (active)`, `color: #2C2925 (text-primary)` |
| Active press | `transform: scale(0.985)` |
| Disabled | `pointer-events: none`, `opacity: 0.5`, `shadow: none` |
| Transition | `color, background-color, border-color 75ms cubic-bezier(0.165, 0.85, 0.45, 1)` |
| Text truncation | Gradient fade mask using `mask-image: linear-gradient(to right, black 85%, transparent)`. Not `text-overflow: ellipsis`. |

#### Section Labels (Sidebar)

| Property | Value |
|---|---|
| Font | DM Sans, 12px, weight 400, color `#9C9690 (text-muted)` |
| Line-height | 16px |
| Padding | `0 8px 8px` |
| Margin-top | 4px |
| Text-transform | none (lowercase labels, e.g. "Starred", "Recents") |

#### Chips (Landing Quick Actions)

| State | Properties |
|---|---|
| Rest | `bg: bg token (#F0EBE3 or #F7F7F5)`, `border: 0.5px solid rgba(196, 186, 168, 0.15)`, `border-radius: 8px`, `height: 32px`, `padding: 0 10px`, `font-size: 14px`, `font-weight: 400`, `font-family: DM Sans`, `color: #6B6560 (text-secondary)`, `cursor: pointer` |
| Icon | 16x16px, inline-flex, gap 8px from label |
| Hover | `bg: #E5DFD5 (active)`, `border-color: #E5DFD5`, `color: #2C2925 (text-primary)` |
| Active press | `transform: scale(0.995)` |
| Transition | `all 150ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Toggle/Switch

| Property | Value |
|---|---|
| Track | `width: 36px`, `height: 20px`, `border-radius: 9999px` |
| Track off | `bg: #E5DFD5 (active)` |
| Track on | `bg: #2C84DB (toggleActive)` |
| Track ring rest | `0.5px` ring using `rgba(196, 186, 168, 0.30)` |
| Track ring hover | `1px` ring (thickens on hover) |
| Thumb | `width: 16px`, `height: 16px`, `bg: #FAF8F4 (surface)`, `border-radius: 9999px`, centered vertically, slides on toggle |
| Transition | `background-color, transform 150ms cubic-bezier(0.4, 0, 0.2, 1)` |
| Focus-visible | Same blue focus ring as all interactive elements |

#### User Message Bubble

| Property | Value |
|---|---|
| bg | `#E5DFD5 (active)` |
| border-radius | 12px |
| padding | `10px 16px` |
| max-width | `85%` (also capped at `75ch`) |
| color | `#2C2925 (text-primary)` |
| font | DM Sans, 16px, weight 400 |
| alignment | Right-aligned |

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. Most UI transitions. |
| out-quart | `cubic-bezier(0.165, 0.85, 0.45, 1)` | Snappy deceleration. Sidebar items, ghost buttons. |
| out-quint | `cubic-bezier(0.22, 1, 0.36, 1)` | The editorial signature easing. Gentle, considered arrival. Page entries. |
| out-expo | `cubic-bezier(0.19, 1, 0.22, 1)` | Near-instant arrival, long settle. Panel open/close. |
| gentle-spring | `stiffness: 120, damping: 20` | Soft spring for particle physics. No ring, critically damped. |

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 75ms | out-quart | Color and bg only. Fast, snappy. |
| Button hover (primary/outlined) | 100ms | default | Background, border-color, color. |
| Toggle track color | 150ms | default | Background-color and thumb transform. |
| Chip hover | 150ms | default | All properties. |
| Card border/shadow hover | 150ms | default | border-color, box-shadow. |
| Input border hover | 150ms | default | border-color only. |
| Chat input card shadow | 200ms | default | All properties including shadow escalation. |
| Ghost icon button | 300ms | out-quart | Slower, more considered for icon-only actions. |
| Page/hero content entry | 300ms | out-quint | `opacity: 0, translateY(12px)` to `opacity: 1, translateY(0)`. |
| Modal entry | 200ms | out-expo | `scale(0.95)` to `scale(1)` + fade. |
| Panel open/close | 500ms | out-expo | Sidebar collapse, settings panel expand. |
| Editorial stagger delay | 80ms | -- | Delay between staggered children (Canvas). 60ms in Dashboard. |
| Menu item hover | 75ms | default | Popover item bg/color change. |

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items (sidebar) | `scale(0.985)` | Barely perceptible. Editorial restraint. |
| Chips | `scale(0.995)` | Almost invisible press. |
| Buttons (primary, ghost) | `scale(0.97)` | Standard press feedback. |
| Tabs (settings) | `scale(0.95)` | More pronounced for segmented controls. |

#### Reduced Motion (`prefers-reduced-motion: reduce`)

| Behavior | Change |
|---|---|
| Strategy | `reduced-distance` -- animations still occur but with no spatial movement. |
| All translateY entries | Replaced with opacity-only fade (no vertical movement). |
| Scale presses | Disabled. Instant visual state change. |
| Stagger delays | Reduced to 0ms. All children appear simultaneously with shared fade. |
| Ambient motion (breath cycle, drift) | Disabled entirely. |
| Particle physics | Disabled. Static render. |
| All transitions (hover, focus) | Remain but capped at 75ms. |

---

### Overlays

#### Popover/Dropdown

| Property | Value |
|---|---|
| bg | `#FAF8F4 (surface)` |
| backdrop-filter | `blur(24px)` |
| border | `0.5px solid rgba(196, 186, 168, 0.30)` |
| border-radius | 12px |
| box-shadow | `shadow-popover` -- `0 2px 8px rgba(44, 41, 37, 0.12)` |
| padding | 6px |
| min-width | 192px |
| max-width | 320px |
| z-index | 50 |
| overflow-y | auto (with `max-height: var(--available-height)`) |
| Menu item | `padding: 6px 8px`, `border-radius: 8px`, `height: 32px`, `font-size: 14px (body-small)`, `color: #6B6560 (text-secondary)`, `cursor: pointer` |
| Menu item hover | `bg: #EDE8DF (recessed)`, `color: #2C2925 (text-primary)` |
| Menu item transition | `75ms cubic-bezier(0.4, 0, 0.2, 1)` |
| Separators | Spacing only (8px gap between groups). No visible lines. |

#### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(44, 41, 37, 0.40)` (warm tinted, not pure black) |
| Overlay backdrop-filter | `blur(12px)` |
| Content bg | `#FAF8F4 (surface)` |
| Content shadow | `shadow-popover` |
| Content border-radius | 12px |
| Content padding | 24px |
| Entry animation | `opacity: 0, scale(0.95)` to `opacity: 1, scale(1)`, 200ms out-expo |
| Exit animation | `opacity: 0`, 150ms default |
| z-index | 60 |

#### Tooltip

| Property | Value |
|---|---|
| bg | `#E5DFD5 (active)` |
| color | `#2C2925 (text-primary)` |
| font-size | 12px (label role) |
| font-weight | 400 |
| border-radius | 4px |
| padding | `4px 8px` |
| shadow | none (tooltips are flat in this theme) |
| Arrow | None. Position-only placement. |
| Delay | 300ms before showing. |
| z-index | 55 |

---

### Layout Tokens

| Token | Canvas Mode | Dashboard Mode | Usage |
|---|---|---|---|
| Content max-width | 768px | 1024px | Main content column |
| Narrow max-width | 672px | 768px | Landing/focused content, settings |
| Sidebar width | 288px | 288px | Fixed sidebar, both modes |
| Sidebar border | `0.5px solid rgba(196, 186, 168, 0.15)` | Same | Right edge separation |
| Header height | 48px | 48px | Top bar |
| Spacing unit | 4px | 4px | Base multiplier |

Dashboard mode retains the 288px sidebar. It does not switch to top-nav. The wider content max-width (1024px vs 768px) is the primary layout difference, allowing dashboard content (charts, tables, metrics) more horizontal room while keeping navigation consistent.

#### Spacing Scale

`4, 6, 8, 10, 12, 16, 20, 24, 28, 32px`

Base unit is 4px (Tailwind default). Common applications:
- 4px: icon-text inline gap adjustment
- 6px: menu item padding, compact element spacing
- 8px: standard element gap, chip padding, icon-text gap
- 12px: input padding, button horizontal padding
- 16px: section padding, card content inset, sidebar item horizontal padding
- 24px: card padding, modal padding, section gap
- 32px: major section separation

#### Density

| Mode | Density | Notes |
|---|---|---|
| Canvas | sparse | Generous whitespace. Content-to-whitespace ratio 45:55. Let the beige canvas breathe. |
| Dashboard | comfortable | Tighter spacing. Data-oriented. Content-to-whitespace ratio 60:40. Still editorial, never cramped. |

#### Responsive Notes

| Breakpoint | Width | Behavior |
|---|---|---|
| lg | 1024px | Full sidebar + content. Default desktop layout. |
| md | 768px | Sidebar collapses to overlay (triggered by hamburger). Content fills viewport. |
| sm | 640px | Single column. Cards stack vertically. Chips wrap. Input card full-width. |

On mobile (below md):
- Sidebar becomes an overlay panel with the same bg, activated by menu button
- Content max-width becomes 100% with 16px horizontal padding
- Header remains 48px but actions collapse into a popover menu
- Cards stretch to full width, padding reduces from 24px to 16px
- Dashboard mode grid switches from multi-column to single-column stack

---

### Accessibility Tokens

| Token | Value | Notes |
|---|---|---|
| Focus ring color | `rgba(116, 171, 226, 0.56)` | Blue at 56% opacity. Functional, not branded. |
| Focus ring width | `2px solid` | Applied via `outline` |
| Focus ring offset | `2px` | Applied via `outline-offset` |
| Disabled opacity | `0.5` | Combined with `pointer-events: none` and `cursor: not-allowed` |
| Disabled shadow | `none` | Remove all shadows on disabled elements |
| Selection bg | `rgba(217, 119, 87, 0.18)` | Terracotta at 18% -- `::selection` |
| Selection color | `#2C2925 (text-primary)` | Maintains readability on selection |
| Scrollbar width | `thin` | `scrollbar-width: thin` |
| Scrollbar thumb | `rgba(196, 186, 168, 0.35)` | Border-base at 35% opacity |
| Scrollbar track | `transparent` | No visible track |
| Min touch target | 44px | All interactive elements on mobile |
| Contrast standard | WCAG AA | 4.5:1 for normal text, 3:1 for large text (18px+) |

**Scrollbar CSS:**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(196, 186, 168, 0.35) transparent;
}
```

---

### Visual Style

#### Material

| Property | Value |
|---|---|
| Grain | Subtle (1-2%) in Canvas mode. None in Dashboard mode. |
| Grain technique | SVG `feTurbulence` overlay (`baseFrequency="1.2"`, 1 octave, `type="fractalNoise"`) at 1.5% opacity. Suggests handmade paper fiber. |
| Gloss | Matte. No reflections, no sheens, no glass effects. |
| Blend mode | `multiply` for particle overlap in Canvas mode. `normal` everywhere else. |
| Shader bg | false. No WebGL backgrounds. |

#### Canvas Mode Rendering

- **Matte particles:** Soft matte circles with alpha blending. No glow, no bloom, no glitter.
- **Watercolor overlap:** Where particles overlap, colors blend like watercolor wash. Use `mix-blend-mode: multiply` or reduced-opacity layering on a canvas element.
- **Physics:** 0.5x speed. Low gravity, high air resistance. Particles float and settle, they do not bounce.
- **Density mapping:** Color shifts from `#E8B49C` coral (sparse) to `#C15F3C` sienna (medium) to `#3F4E4F` forest (dense). This creates natural depth from particle accumulation.
- **Negative space:** Let the beige canvas breathe. Not every pixel needs a particle. Empty space is a feature.

#### Dashboard Mode Rendering

- **Micro-grid:** A 32x32px grid of 1px lines using border-base at 8% opacity, visible behind content areas on the background surface. Creates a subtle ledger-paper quality.

```css
.dashboard-bg {
  background-image:
    repeating-linear-gradient(
      to right,
      rgba(196, 186, 168, 0.08) 0px,
      rgba(196, 186, 168, 0.08) 1px,
      transparent 1px,
      transparent 32px
    ),
    repeating-linear-gradient(
      to bottom,
      rgba(196, 186, 168, 0.08) 0px,
      rgba(196, 186, 168, 0.08) 1px,
      transparent 1px,
      transparent 32px
    );
}
```

Alternative implementation: SVG `<pattern>` with a 32x32 `viewBox` containing two 1px lines, applied as `background-image: url("data:image/svg+xml,...")`.

- **Strict 3-level hierarchy:** Primary metric (large, Plus Jakarta Sans 24px/460 or 38px/290 for hero KPIs, terracotta if emphasized). Secondary metric (medium, DM Sans 16px/400, text-primary). Tertiary (small, DM Sans 14px/400, text-secondary).
- **Semantic-only color:** In Dashboard mode, color is never decorative. Success/warning/danger for status. Terracotta for primary data series only. All other data uses text-primary/secondary/muted hierarchy.
- **Data typography:** All numeric data uses Geist Mono with `font-variant-numeric: tabular-nums` for column alignment.

---

### Signature Animations

#### 1. Watercolor Bleed (Canvas mode)

New particle groups spread outward from their origin point with decreasing opacity, simulating watercolor pigment bleeding into wet paper.

- **Technique:** Each new particle spawns 3-4 "echo" particles at 60%, 30%, 15% opacity, expanding outward at 0.3x the main particle's velocity. Echoes use the particle's color interpolated toward the background (`#F0EBE3`) using OKLCH color mixing.
- **Duration:** 800ms for the full bleed.
- **Easing:** gentle-spring (`stiffness: 120, damping: 20`).
- **Blend mode:** `multiply` on the echo particles.
- **Reduced motion:** Static spawn at full opacity, no echoes.

#### 2. Editorial Stagger (Both modes)

UI elements and data points enter in a staggered cascade, top-left to bottom-right, with 80ms delay between each element.

- **Technique:** Parent container orchestrates children with `staggerChildren: 0.08`. Each child animates from `opacity: 0, translateY: 12px` to `opacity: 1, translateY: 0`.
- **Duration:** 300ms per element.
- **Easing:** out-quint (`cubic-bezier(0.22, 1, 0.36, 1)`).
- **Dashboard variant:** 60ms stagger delay for faster data density.
- **Total cascade example:** 12-item grid completes at 300ms + (11 x 80ms) = 1180ms.
- **Reduced motion:** All items appear simultaneously with 150ms opacity-only fade.

#### 3. Thermal Shift (Canvas mode)

Particles continuously shift color based on their current velocity, creating a living heat-map effect.

- **Mapping:** velocity 0 = faint sand (`#E8E3DA` at 40% opacity), velocity 0.3 = coral (`#E8B49C`), velocity 0.7 = sienna (`#C15F3C`), velocity 1.0 = forest (`#3F4E4F`).
- **Interpolation:** Smooth OKLCH interpolation between stops, not stepped.
- **Update rate:** Every `requestAnimationFrame` tick.
- **Reduced motion:** Static colors based on initial velocity, no runtime updates.

#### 4. Breath Cycle (Canvas mode)

The entire particle field subtly expands and contracts, like the canvas is breathing.

- **Technique:** `transform: scale()` oscillating between `0.98` and `1.02` on the particle container element.
- **Duration:** 8 seconds per full cycle (4s expand, 4s contract).
- **Easing:** `cubic-bezier(0.37, 0, 0.63, 1)` (sine-like ease-in-out for smooth ambient oscillation).
- **Reduced motion:** Disabled entirely.

#### 5. Settle Drift (Canvas mode)

New particles overshoot their target position by 3-5px, then drift back with spring physics. The landing undersells rather than oversells.

- **Technique:** Spring animation targeting final position, with initial velocity causing slight overshoot. One overshoot, no oscillation.
- **Spring params:** `stiffness: 180, damping: 24` (critically damped).
- **Duration:** ~400ms to fully settle.
- **Overshoot distance:** 3-5px, proportional to spawn velocity.
- **Reduced motion:** Direct placement at target position, no overshoot.

---

### Dark Mode Variant

This theme is natively light. The dark mode variant inverts the surface hierarchy: deeper layers become darker, elevated surfaces become slightly lighter. All warm undertones are preserved.

#### Dark Mode Palette

| Token | Light Hex | Dark Hex | Dark HSL | Notes |
|---|---|---|---|---|
| page | `#E8E3DA` | `#141210` | 30 14% 7% | Deepest dark surface. Warm lacquer black. |
| bg | `#F0EBE3` | `#1C1917` | 24 10% 10% | Primary dark surface. Warm charcoal. |
| surface | `#FAF8F4` | `#262420` | 34 8% 14% | Cards, inputs. Slightly lighter than bg. |
| recessed | `#EDE8DF` | `#1A1816` | 24 8% 9% | Code blocks, inset. Slightly darker than bg. |
| active | `#E5DFD5` | `#0E0D0B` | 40 12% 5% | Active items, user bubble. Darkest interactive. |
| text-primary | `#2C2925` | `#FAF8F4` | 45 33% 97% | Primary text. Warm cream. |
| text-secondary | `#6B6560` | `#B8B2A8` | 33 9% 69% | Secondary text. Warm light gray. |
| text-muted | `#9C9690` | `#7A756E` | 28 5% 45% | Muted text. |
| border-base | `#C4BAA8` | `#8A8070` | 33 11% 49% | Border base. Darker sand. Same opacity system applies. |
| accent-primary | `#D97757` | `#D97757` | 15 63% 60% | Terracotta unchanged. Works on dark. |
| accent-secondary | `#C15F3C` | `#E08A6A` | 15 67% 65% | Slightly lifted for dark bg contrast. |
| success | `#5A8A50` | `#6A9A60` | 110 25% 49% | Slightly lifted. |
| warning | `#B17506` | `#C48510` | 39 85% 41% | Slightly lifted. |
| danger | `#C4534A` | `#D06358` | 4 52% 58% | Slightly lifted. |
| info | `#5B7FA5` | `#6B8FB5` | 212 29% 56% | Slightly lifted. |

#### Dark Mode Special Colors

| Token | Dark Value |
|---|---|
| inlineCode | `#FE8181` (salmon/red for code text, per claude.ai pattern) |
| toggleActive | `#2C84DB` (unchanged) |
| selection | `rgba(217, 119, 87, 0.20)` (slightly higher opacity for visibility on dark) |

#### Dark Mode Rules

- Surfaces lighten as they elevate: `page (#141210)` < `bg (#1C1917)` < `surface (#262420)`. This is the standard dark-mode convention.
- Accent (terracotta) remains unchanged -- it reads well on both light and dark backgrounds.
- Text colors invert: primary becomes warm cream, secondary/muted become progressively dimmer warm grays.
- Border opacity system remains the same (15/25/30/40%), but the base color shifts to `#8A8070` (darker sand) so borders are visible against dark surfaces.
- Shadow percentages increase: `shadow-input` uses 5% rest / 8% focus (vs 3%/6% in light mode). `shadow-popover` uses 24% (vs 12% in light mode).
- Apply `-webkit-font-smoothing: antialiased` (already specified, but essential for light text on dark backgrounds).
- Grain overlay (Canvas mode) inverts to `screen` blend mode at 2% opacity.
- Micro-grid (Dashboard mode) uses border-base at 6% opacity (reduced from 8% because grid lines are more visible on dark).

#### Dark Mode Shadow Tokens

| Token | Dark Value |
|---|---|
| shadow-input | `0 4px 20px rgba(0, 0, 0, 0.05), 0 0 0 0.5px rgba(138, 128, 112, 0.15)` |
| shadow-input-hover | `0 4px 20px rgba(0, 0, 0, 0.05), 0 0 0 0.5px rgba(138, 128, 112, 0.30)` |
| shadow-input-focus | `0 4px 20px rgba(0, 0, 0, 0.08), 0 0 0 0.5px rgba(138, 128, 112, 0.30)` |
| shadow-popover | `0 2px 8px rgba(0, 0, 0, 0.24)` |

---

### Data Visualization

| Property | Value |
|---|---|
| Categorical palette | Terracotta `#D97757`, Forest `#3F4E4F`, Warm Amber `#B17506`, Info Blue `#5B7FA5`, Muted Coral `#C4534A`. Max 5 hues per chart. |
| Sequential ramp | Terracotta single-hue: `#F5DDD0` (lightest) -> `#E8B49C` -> `#D97757` -> `#C15F3C` -> `#8A3A20` (darkest) |
| Diverging ramp | Forest-to-Terracotta: `#3F4E4F` -> `#8A9A8F` -> `#EDE8DF` (neutral center) -> `#E8B49C` -> `#D97757` |
| Grid style | low-ink. Axes in text-muted, gridlines in border-base at 10% opacity. |
| Max hues per chart | 2 in Dashboard mode (semantic only). 5 in Canvas mode. |
| Philosophy | annotated. Labels on data, not legends. Sparklines preferred over complex charts in Dashboard mode. |
| Number formatting | Geist Mono with `font-variant-numeric: tabular-nums`. Right-aligned in columns. |

---

### Mobile Notes

#### Effects to Disable

- **Canvas mode grain overlay:** Remove SVG `feTurbulence` filter (causes GPU memory pressure on mobile Safari).
- **Breath Cycle animation:** Disable (continuous scale transforms cause layout recalculations on some mobile browsers).
- **Backdrop blur on popovers:** Reduce from `blur(24px)` to `blur(12px)` (performance on older devices). Keep modal blur at `blur(8px)`.
- **Watercolor Bleed echoes:** Reduce from 3-4 echoes to 1-2 (fewer particle spawns).

#### Sizing Adjustments

- **Particle count (Canvas):** Reduce to 60% of desktop count.
- **Stagger delays:** Halve all stagger delays (80ms becomes 40ms, 60ms becomes 30ms) for snappier mobile feel.
- **Touch targets:** All interactive elements minimum 44px (some sidebar items at 32px on desktop expand to 44px on mobile).
- **Card padding:** Reduce from 24px to 16px on screens below 640px.
- **Content padding:** 16px horizontal on mobile (vs centered max-width on desktop).
- **Typography:** Display role reduces from 38px to `clamp(28px, 6vw, 38px)`. All other roles remain fixed.

#### Performance Notes

- This theme is performance-friendly. Matte particles (no glow, no blur) are cheaper than glowing particles.
- The primary performance concern is Canvas mode particle count on mobile. Cap at 200 particles.
- Dashboard mode has no performance concerns beyond standard responsive behavior.
- Shadow composites (drop + ring) are well-supported and GPU-composited.

---

### Implementation Checklist

- [ ] **Fonts loaded:** Plus Jakarta Sans (variable, 200-800), DM Sans (variable, 100-1000), Geist Mono (variable, 100-900) via Google Fonts / CDN with `font-display: swap`
- [ ] **CSS custom properties defined:** All color tokens, shadow tokens, border tokens, radius tokens, spacing scale, motion easings, layout values as `:root` variables
- [ ] **Font smoothing applied:** `-webkit-font-smoothing: antialiased` on `<html>`
- [ ] **Typography matrix implemented:** All 10 roles with correct family, size, weight, line-height, letter-spacing
- [ ] **Family switch boundary respected:** Plus Jakarta Sans for Display/Heading/Subheading only. DM Sans for all other roles.
- [ ] **Border-radius applied correctly:** sm (4px), md (6px), lg (8px), xl (12px), 2xl (20px), input (9.6px), full (9999px)
- [ ] **Shadow tokens applied per state:** rest/hover/focus on input card, sm on file cards, popover on menus
- [ ] **Border opacity system implemented:** All borders use base color at correct opacity level (subtle 15%, card 25%, hover 30%, focus 40%)
- [ ] **Focus ring on all interactive elements:** `outline: 2px solid rgba(116, 171, 226, 0.56)`, `outline-offset: 2px` on `:focus-visible`
- [ ] **Disabled states complete:** opacity 0.5 + pointer-events none + cursor not-allowed + shadow none
- [ ] **`prefers-reduced-motion` media query present:** All animations wrapped or checked
- [ ] **Scrollbar styled:** `scrollbar-width: thin`, `scrollbar-color: rgba(196, 186, 168, 0.35) transparent`
- [ ] **`::selection` styled:** `background: rgba(217, 119, 87, 0.18)`, `color: #2C2925`
- [ ] **Touch targets >= 44px on mobile**
- [ ] **State transitions match motion map:** Each component uses its specified duration and easing, not a global `transition: all 0.2s`
- [ ] **Canvas/Dashboard mode switch implemented:** Background color, content max-width, density, micro-grid, and stagger delay all switch correctly
- [ ] **Dark mode variant tested:** All token swaps applied, shadow percentages adjusted, text contrast verified WCAG AA
- [ ] **Data visualization tokens applied:** Categorical palette, sequential ramp, grid style, number formatting with Geist Mono tabular-nums
- [ ] **Micro-grid (Dashboard):** `repeating-linear-gradient` at 8% opacity, 32x32px cells
- [ ] **Gradient fade mask on sidebar items:** Not `text-overflow: ellipsis`
