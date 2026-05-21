# Liquid Glass — Full Specification

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 31
- [Color System](#color-system) — Line 48
  - [Palette](#palette) — Line 50
  - [Special Tokens](#special-tokens) — Line 73
  - [Opacity System](#opacity-system) — Line 81
  - [Glass Tint System](#glass-tint-system) — Line 101
  - [Color Rules](#color-rules) — Line 114
- [Typography Matrix](#typography-matrix) — Line 123
  - [Font Loading](#font-loading) — Line 147
- [Elevation System](#elevation-system) — Line 156
  - [Surface Hierarchy](#surface-hierarchy) — Line 164
  - [Shadow Tokens](#shadow-tokens) — Line 177
  - [Backdrop-Filter Tokens](#backdrop-filter-tokens) — Line 196
  - [Glass Edge Highlight (Refraction)](#glass-edge-highlight-refraction) — Line 209
  - [Separation Recipe](#separation-recipe) — Line 220
- [Border System](#border-system) — Line 225
  - [Widths and Patterns](#widths-and-patterns) — Line 230
  - [Focus Ring](#focus-ring) — Line 243
- [Component States](#component-states) — Line 251
  - [Buttons (Primary)](#buttons-primary) — Line 253
  - [Buttons (Ghost / Icon)](#buttons-ghost--icon) — Line 265
  - [Buttons (Secondary / Glass)](#buttons-secondary--glass) — Line 277
  - [Text Input](#text-input) — Line 289
  - [Chat Input Card (Glass)](#chat-input-card-glass) — Line 300
  - [Cards](#cards) — Line 308
  - [Sidebar Items](#sidebar-items) — Line 316
  - [Chips](#chips) — Line 326
  - [Toggle / Switch](#toggle--switch) — Line 335
- [Motion Map](#motion-map) — Line 352
  - [Easings](#easings) — Line 354
  - [Duration x Easing x Component](#duration-x-easing-x-component) — Line 369
  - [Active Press Scale](#active-press-scale) — Line 382
- [Overlays](#overlays) — Line 393
  - [Popover / Dropdown](#popover--dropdown) — Line 395
  - [Modal](#modal) — Line 411
  - [Tooltip](#tooltip) — Line 424
- [Layout Tokens](#layout-tokens) — Line 436
  - [Spacing Scale](#spacing-scale) — Line 447
  - [Density](#density) — Line 451
  - [Radius Scale (Theme Override)](#radius-scale-theme-override) — Line 455
  - [Responsive Notes](#responsive-notes) — Line 470
- [Accessibility Tokens](#accessibility-tokens) — Line 478
  - [Reduced Motion](#reduced-motion-prefers-reduced-motion-reduce) — Line 497
- [Visual Style](#visual-style) — Line 517
- [Signature Animations](#signature-animations) — Line 527
  - [1. Glass Panel Slide](#1-glass-panel-slide) — Line 529
  - [2. Blur-Focus Modal](#2-blur-focus-modal) — Line 549
  - [3. Shadow Elevation Shift](#3-shadow-elevation-shift) — Line 564
  - [4. Depth Parallax](#4-depth-parallax) — Line 577
  - [5. Glass Ripple Focus](#5-glass-ripple-focus) — Line 581
- [Dark Mode Variant](#dark-mode-variant) — Line 594
  - [Dark Palette](#dark-palette) — Line 598
  - [Dark Mode Rules](#dark-mode-rules) — Line 616
- [Mobile Notes](#mobile-notes) — Line 629
  - [Effects to Disable](#effects-to-disable) — Line 631
  - [Adjustments](#adjustments) — Line 636
  - [Performance Notes](#performance-notes) — Line 646
- [Implementation Checklist](#implementation-checklist) — Line 653

---

## 5. Liquid Glass

> Frosted surfaces floating in light — precision depth through translucency.

**Best for:** Productivity apps, settings panels, system tools, dashboards, portfolio showcases, modern SaaS, any interface that wants to feel like native macOS/iOS.

---

### Identity & Philosophy

This theme lives in the world of an Apple product reveal. Pristine white surfaces, frosted glass panels hovering at precise depths, system blue accents appearing only for active controls. The glass IS the design language. There are no textures, no grain, no decorative flourishes — personality comes entirely from the interplay of translucent layers, blurred backgrounds, and layered composite shadows that give each surface a measurable z-depth. This is macOS Sonoma's control center, iOS notification panels, visionOS floating windows.

The core tension is extreme cleanliness vs. extreme depth complexity. The surfaces look simple, nearly empty. But underneath, the engineering is the most demanding of any theme: multiple `backdrop-filter` layers, composite shadows with 3-4 values each, refraction-edge highlights, saturation-boosted blurs. The simplicity is expensive.

**Decision principle:** "When in doubt, ask: would this look like a system control on visionOS? If it feels decorated, remove it. If it feels flat, add another glass layer."

**What this theme is NOT:**
- Not frosted glass as decoration — the blur IS the structure, not ornament
- Not dark-first — this is light-mode-native; glass requires content behind it to show translucency
- Not colorful — system blue only; everything else is greyscale with alpha
- Not warm — clinical, precisely cool; cold whites, neutral greys, zero yellow or beige undertone
- Not flat — if your output has no `backdrop-filter` or layered shadows, you have missed the entire point

---

### Color System

#### Palette

The palette is deliberately restrained. Glass panels derive their visual richness from what shows through them, not from their own color. Surface colors carry alpha channels because true glass is never fully opaque.

| Token | Name | Hex / Value | Role |
|---|---|---|---|
| page | Cloud Grey | `#F2F2F7` | Deepest background. Apple system grey 6 light. Solid, provides the canvas glass sits on. |
| bg | Glass White | `rgba(255,255,255,0.72)` | Primary glass surface. Semi-transparent white with backdrop-filter. |
| surface | Frosted Panel | `rgba(255,255,255,0.82)` | Elevated cards, inputs, popovers. Higher opacity = higher elevation. |
| recessed | Inset Grey | `#E5E5EA` | Code blocks, inset areas. Solid, slightly darker than page. |
| active | Pressed Glass | `rgba(0,0,0,0.06)` | Active/pressed items, selection highlight. Darkened tint over glass. |
| text-primary | System Black | `#1D1D1F` | Headings, body text. Apple system label color. |
| text-secondary | Secondary Label | `rgba(60,60,67,0.6)` | Sidebar items, secondary labels. Single base at 60% opacity. |
| text-muted | Tertiary Label | `rgba(60,60,67,0.3)` | Placeholders, timestamps, metadata. Same base at 30% opacity. |
| text-onAccent | On Blue | `#FFFFFF` | Text on accent-blue backgrounds. |
| border-base | Separator | `#3C3C43` | Used at very low opacity (8-20%). Apple opaque separator mapped to alpha system. |
| accent-primary | System Blue | `#007AFF` | Primary CTA, active toggles, focus rings. |
| accent-secondary | System Blue Light | `#5AC8FA` | Informational accents, secondary blue for links in context. |
| success | System Green | `#34C759` | Positive states, toggle on-state. |
| warning | System Orange | `#FF9500` | Caution states. |
| danger | System Red | `#FF3B30` | Error states, destructive actions. |
| info | System Blue | `#007AFF` | Info states (same as accent). |

#### Special Tokens

| Token | Value | Role |
|---|---|---|
| inlineCode | `#AD3DA4` | Code text within prose. Apple purple, like Xcode syntax. |
| toggleActive | `#34C759` | Toggle/switch active track. System Green, matching iOS. |
| selection | `rgba(0,122,255,0.2)` | `::selection` background. System Blue at 20%. |

#### Opacity System

Glass opacity is the primary design tool. The same white at different opacities creates the entire surface hierarchy:

| Level | Opacity | Usage |
|---|---|---|
| Glass level 1 | 50% white | Chips, secondary glass elements, sidebar (subtle glass) |
| Glass level 2 | 72% white | Primary cards, input areas, standard glass panels |
| Glass level 3 | 82% white | Popovers, dropdowns, elevated glass |
| Glass level 4 | 92% white | Modals, dialog panels — nearly opaque |

Border opacity (on `border-base` `#3C3C43`):

| Context | Opacity | Usage |
|---|---|---|
| subtle | 8% | Glass panel edge. Almost invisible. |
| card | 12% | Card-style glass panels. Slightly more definition. |
| hover | 18% | Hovered glass panels. Border becomes present. |
| focus | 100% (System Blue) | Focus ring. Full accent color, not border-base. |

#### Glass Tint System

For semantic states, glass panels accept a color tint at very low opacity, maintaining the glass vocabulary while communicating status:

| State | Tint Value | Usage |
|---|---|---|
| Success glass | `rgba(52,199,89,0.06)` | Success notifications, confirmation panels |
| Warning glass | `rgba(255,149,0,0.06)` | Warning banners, caution panels |
| Danger glass | `rgba(255,59,48,0.06)` | Error notifications, destructive confirmation |
| Info glass | `rgba(0,122,255,0.05)` | Informational callouts, tip panels |

Apply tint as the `background-color` on top of the standard glass `backdrop-filter`. The blur still shows through; the tint just shifts the hue.

#### Color Rules

- No gradients on surfaces. Glass is flat-colored with translucency — the "gradient" comes from the blurred content behind it.
- Color is earned. Only System Blue and semantic colors. Everything else is greyscale.
- Alpha channels are load-bearing. The same base white at different opacities creates the entire surface hierarchy.
- The page background should ideally have content or subtle pattern behind it so glass translucency has something to reveal. Without background variation, glass reads as solid white.

---

### Typography Matrix

System-font-first approach. SF Pro is Apple's system font; Plus Jakarta Sans is the closest Google Fonts equivalent for headings, DM Sans for body, Geist Mono for code. Type is deliberately invisible — clean, neutral, no personality. The glass does the talking.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | sans (Plus Jakarta Sans) | 34px | 700 | 1.1 | -0.03em | -- | Hero titles, page names |
| Heading | sans (Plus Jakarta Sans) | 22px | 600 | 1.27 | -0.015em | -- | Section titles, settings headers |
| Subheading | sans (Plus Jakarta Sans) | 18px | 600 | 1.3 | -0.01em | -- | Card titles, subsection headers, panel labels |
| Body | sans (DM Sans) | 17px | 400 | 1.47 | -0.01em | -- | Primary reading text, UI body |
| Body Small | sans (DM Sans) | 15px | 400 | 1.4 | -0.005em | -- | Sidebar items, form labels, secondary UI text |
| Button | sans (Plus Jakarta Sans) | 15px | 600 | 1.4 | -0.005em | -- | Button labels, emphasized small UI text |
| Input | sans (DM Sans) | 15px | 400 | 1.4 | normal | -- | Form input text |
| Label | sans (DM Sans) | 13px | 400 | 1.3 | 0.01em | none | Section labels, metadata, timestamps |
| Code | mono (Geist Mono) | 0.9em | 400 | 1.5 | normal | -- | Inline code, code blocks, data values |
| Caption | sans (DM Sans) | 12px | 400 | 1.33 | normal | -- | Disclaimers, footnotes, bottom-of-page text |

**Typographic decisions:**
- Sizes follow Apple HIG (17px body, 15px secondary, 13px caption, 22px title, 34px large title) rather than web defaults (16/14/12). The 17px body is deliberate — it creates the "this feels like a native app" quality.
- Weight 600 (semibold) for headings and buttons, not 700. Apple uses SF Pro Semibold for most UI elements.
- Negative letter-spacing on display and heading text (tighter tracking, as Apple does).
- `font-smoothing: antialiased` always — critical on light backgrounds for Apple-quality rendering.
- `text-wrap: pretty` for body text.

#### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400&display=swap" rel="stylesheet">
```

**Fallback chain:** `"Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", system-ui, sans-serif`

---

### Elevation System

**Strategy:** `layered-shadows`

This is the defining section. Every glass panel exists at a specific z-depth, expressed through the combination of shadow complexity, `backdrop-filter` blur radius, and surface opacity. Higher surfaces get more shadow layers, more blur, and more opacity.

#### Surface Hierarchy

| Surface | Background | Shadow | Backdrop-Filter | Usage |
|---|---|---|---|---|
| page | `#F2F2F7` solid | none | none | Main page canvas, behind all glass |
| glass-subtle | `rgba(255,255,255,0.5)` | shadow-glass-1 | `blur(12px) saturate(1.5)` | Sidebar, secondary panels |
| glass-card | `rgba(255,255,255,0.72)` | shadow-glass-2 | `blur(20px) saturate(1.8)` | Primary cards, input areas |
| glass-elevated | `rgba(255,255,255,0.82)` | shadow-glass-3 | `blur(24px) saturate(1.8)` | Popovers, dropdowns |
| glass-modal | `rgba(255,255,255,0.92)` | shadow-glass-4 | `blur(40px) saturate(2.0)` | Modals, dialog panels |
| recessed | `#E5E5EA` solid | shadow-inset | none | Code blocks, inset areas |
| active | `rgba(0,0,0,0.06)` | none | none | Active/pressed states |

**Opacity escalation rule:** When glass nests inside glass (e.g., a popover appearing over a glass card), each nested layer is 10% more opaque than its standalone value. A popover (standalone 82%) on a glass-card becomes 92%. This prevents the muddy translucency that occurs when multiple blurs compound.

#### Shadow Tokens

Each shadow is a composite of multiple layers. The glass aesthetic demands this: a soft ambient shadow for general lift, a crisp contact shadow for grounding, and optionally a highlight edge for refraction.

| Token | Value | Usage |
|---|---|---|
| shadow-glass-1 | `0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03)` | Level 1: sidebar, secondary panels. Barely-there lift. |
| shadow-glass-2 | `0 0.5px 1px rgba(0,0,0,0.06), 0 2px 6px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06)` | Level 2: primary cards, input card. Contact + mid-spread + ambient. |
| shadow-glass-3 | `0 0.5px 1px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.04), 0 12px 32px rgba(0,0,0,0.08), 0 24px 48px rgba(0,0,0,0.04)` | Level 3: popovers, dropdowns. Four layers: contact + tight + medium + wide ambient. |
| shadow-glass-4 | `0 1px 2px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.06), 0 24px 48px rgba(0,0,0,0.08), 0 48px 96px rgba(0,0,0,0.06)` | Level 4: modals. Maximum depth, soft ambient light. |
| shadow-input | `0 0.5px 1px rgba(0,0,0,0.04), 0 2px 6px rgba(0,0,0,0.03), 0 0 0 0.5px rgba(60,60,67,0.08)` | Input card rest. Glass-2 shadow + hairline ring. |
| shadow-input-hover | `0 0.5px 1px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.05), 0 0 0 0.5px rgba(60,60,67,0.12)` | Input card hover. Shadow spreads wider, ring more visible. |
| shadow-input-focus | `0 0.5px 1px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.06), 0 0 0 2px rgba(0,122,255,0.4)` | Input card focus. Blue focus ring replaces hairline ring. |
| shadow-popover | `0 1px 4px rgba(0,0,0,0.08), 0 8px 24px rgba(0,0,0,0.08), 0 24px 48px rgba(0,0,0,0.06)` | Menus, dropdowns. Three-layer composite. |
| shadow-inset | `inset 0 1px 2px rgba(0,0,0,0.04)` | Recessed surfaces, code blocks. Subtle inner shadow. |
| shadow-sm | `0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.03)` | Small elements, badges. |
| shadow-md | `0 2px 4px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.06)` | Mid-elevation elements. |
| shadow-none | `none` | Flat surfaces, page background. |

#### Backdrop-Filter Tokens

| Token | Value | Usage |
|---|---|---|
| glass-subtle | `blur(12px) saturate(1.5)` | Sidebar, low-priority glass |
| glass-standard | `blur(20px) saturate(1.8)` | Primary cards, standard glass panels |
| glass-elevated | `blur(24px) saturate(1.8)` | Popovers, menus |
| glass-heavy | `blur(40px) saturate(2.0)` | Modals, overlays |
| glass-none | `none` | Solid surfaces, page background |

The `saturate()` boost is essential. Without it, blurred content behind glass looks washed out and dead. `saturate(1.8)` makes the background slightly more vivid through the glass, which is how Apple achieves the "glass looks alive" effect.

#### Glass Edge Highlight (Refraction)

A `border-top` of white at varying opacity creates a refraction highlight — the appearance of light catching the top edge of a glass sheet:

| Level | Value | Usage |
|---|---|---|
| Glass-1 | `border-top: 0.5px solid rgba(255,255,255,0.3)` | Sidebar panels |
| Glass-2 | `border-top: 0.5px solid rgba(255,255,255,0.5)` | Cards, input card |
| Glass-3 | `border-top: 0.5px solid rgba(255,255,255,0.6)` | Popovers |
| Glass-4 | `border-top: 0.5px solid rgba(255,255,255,0.7)` | Modals |

#### Separation Recipe

Translucency + layered composite shadows + saturation-boosted blur. No visible borders between content areas. Panels separate from the background through their frosted-glass treatment — blur radius and shadow depth communicate z-position. No dividers inside glass panels. Hierarchy is expressed through opacity (more opaque = higher) and shadow complexity (more layers = higher). The top-edge refraction highlight provides a final depth cue.

---

### Border System

Borders on glass panels serve as edge definitions — barely-visible hairlines marking where one translucent surface meets the background. Too thick breaks the glass illusion. Too visible and it reads as a card, not a panel.

#### Widths and Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| glass-edge | 0.5px | `border-base` at 8% | Default glass panel edge. Almost invisible. |
| glass-card | 0.5px | `border-base` at 12% | Card-style glass. Slightly more definition. |
| glass-hover | 0.5px | `border-base` at 18% | Hovered glass panels. |
| glass-refraction | 0.5px | `rgba(255,255,255,0.5)` | Top-edge highlight on glass (white, not grey). |
| input | 1px | `border-base` at 12% | Form input borders. Heavier for usability. |
| input-hover | 1px | `border-base` at 20% | Input hover state. |
| input-focus | 1px | `rgba(0,122,255,0.5)` | Input focus state. Blue border. |
| separator | 0.5px | `border-base` at 10% | Horizontal/vertical dividers within panels. |

#### Focus Ring

- **Color:** `rgba(0, 122, 255, 0.4)` — System Blue at 40%
- **Width:** 2px solid (via `box-shadow`)
- **Offset:** 2px white inner ring
- **Implementation:** `box-shadow: 0 0 0 2px #FFFFFF, 0 0 0 4px rgba(0,122,255,0.4)` — the white offset ring separates the blue from the glass surface, preventing visual bleed

---

### Component States

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `#007AFF`, border none, color `#FFFFFF`, radius 8px, h 34px, padding `0 16px`, font button, shadow none |
| Hover | bg `#0070EB` (slightly darker blue) |
| Active | transform `scale(0.97)`, bg `#0064D2` (darker still) |
| Focus | box-shadow `0 0 0 2px #FFF, 0 0 0 4px rgba(0,122,255,0.4)` |
| Disabled | opacity 0.4, pointer-events none, cursor not-allowed |
| Transition | background 100ms apple-ease, transform 100ms apple-ease |

#### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border none, color `rgba(60,60,67,0.6)`, radius 6px, size 32x32px |
| Hover | bg `rgba(0,0,0,0.04)`, color `#1D1D1F` |
| Active | bg `rgba(0,0,0,0.08)`, transform `scale(0.97)` |
| Focus | focus ring |
| Disabled | opacity 0.4, pointer-events none |
| Transition | background 250ms out-quart, color 250ms out-quart |

#### Buttons (Secondary / Glass)

| State | Properties |
|---|---|
| Rest | bg `rgba(255,255,255,0.72)`, border 0.5px at `border-base` 12%, color `#1D1D1F`, radius 8px, h 34px, backdrop-filter `blur(12px) saturate(1.5)`, shadow shadow-glass-1 |
| Hover | bg `rgba(255,255,255,0.82)`, border at 18%, shadow shadow-glass-2 |
| Active | transform `scale(0.97)`, shadow shadow-glass-1 (shadow reduces on press) |
| Focus | focus ring appended to existing shadow |
| Disabled | opacity 0.4, pointer-events none, backdrop-filter none |
| Transition | all 150ms apple-ease |

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `rgba(255,255,255,0.72)`, border `1px solid rgba(60,60,67,0.12)`, radius 10px, h 44px, padding `0 12px`, backdrop-filter `blur(20px) saturate(1.8)`, shadow shadow-input, color `#1D1D1F`, placeholder `rgba(60,60,67,0.3)`, caret-color `#007AFF` |
| Hover | border `1px solid rgba(60,60,67,0.2)`, shadow shadow-input-hover |
| Focus | border `1px solid rgba(0,122,255,0.5)`, shadow shadow-input-focus, outline none |
| Disabled | opacity 0.4, pointer-events none, bg `rgba(255,255,255,0.5)`, backdrop-filter none |
| Transition | border-color 150ms apple-ease, box-shadow 200ms apple-ease |

#### Chat Input Card (Glass)

| State | Properties |
|---|---|
| Rest | bg `rgba(255,255,255,0.72)`, radius 20px, border `1px solid transparent`, backdrop-filter `blur(20px) saturate(1.8)`, shadow shadow-glass-2, border-top `0.5px solid rgba(255,255,255,0.5)` |
| Hover | shadow shadow-input-hover, border `1px solid rgba(60,60,67,0.12)` |
| Focus-within | shadow shadow-input-focus, border `1px solid rgba(0,122,255,0.3)` |
| Transition | all 200ms apple-ease |

#### Cards

| State | Properties |
|---|---|
| Rest | bg `rgba(255,255,255,0.72)`, border `0.5px solid rgba(60,60,67,0.12)`, radius 12px, backdrop-filter `blur(20px) saturate(1.8)`, shadow shadow-glass-2, border-top `0.5px solid rgba(255,255,255,0.5)` |
| Hover | shadow shadow-glass-3, border `0.5px solid rgba(60,60,67,0.18)` — card lifts on hover |
| Transition | box-shadow 200ms apple-ease, border-color 150ms apple-ease |

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `rgba(60,60,67,0.6)`, radius 8px, h 34px, padding `6px 12px`, font bodySmall |
| Hover | bg `rgba(0,0,0,0.04)`, color `#1D1D1F` |
| Active (current) | bg `rgba(0,0,0,0.06)`, color `#1D1D1F`, font-weight 500 |
| Active press | transform `scale(0.985)` |
| Transition | color 75ms out-quart, background 75ms out-quart |

#### Chips

| State | Properties |
|---|---|
| Rest | bg `rgba(255,255,255,0.5)`, border `0.5px solid rgba(60,60,67,0.08)`, radius 20px (pill), h 32px, padding `0 12px`, font bodySmall, color `rgba(60,60,67,0.6)`, backdrop-filter `blur(8px) saturate(1.3)` |
| Hover | bg `rgba(255,255,255,0.72)`, border at 12% opacity, color `#1D1D1F` |
| Active press | transform `scale(0.98)` |
| Transition | all 150ms default |

#### Toggle / Switch

**Theme override:** Apple-faithful dimensions at 51x31px (overrides schema default 36x20px).

| Property | Value |
|---|---|
| Track width | 51px |
| Track height | 31px |
| Track radius | 9999px (full) |
| Track off bg | `rgba(0,0,0,0.06)` |
| Track off ring | `0.5px solid rgba(60,60,67,0.08)` |
| Track on bg | `#34C759` (System Green) |
| Thumb | 27px white circle |
| Thumb shadow | `0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08)` |
| Ring hover | thickens to 1px |
| Transition | 200ms apple-ease |
| Focus-visible | same blue focus ring as all interactive elements |

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard system ease-in-out |
| apple-ease | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Apple's default ease-out. Sharper deceleration. |
| spring-gentle | `cubic-bezier(0.2, 0.8, 0.2, 1.02)` | Gentle spring with tiny overshoot. Glass panel slides. |
| out-quart | `cubic-bezier(0.165, 0.85, 0.45, 1)` | Snappy deceleration for small interactions. |
| out-expo | `cubic-bezier(0.19, 1, 0.22, 1)` | Smooth open/close for panels and modals. |

For Framer Motion / Motion spring-based animations:
- **Standard:** `type: "spring", stiffness: 300, damping: 30` — panel opens, card appearances
- **Gentle:** `type: "spring", stiffness: 200, damping: 25` — glass slides, parallax layers
- **Snappy:** `type: "spring", stiffness: 500, damping: 35` — button presses, toggles

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 75ms | out-quart | Instant feel, color shift only |
| Button hover | 100ms | apple-ease | Background tint appears quickly |
| Toggle/chip/general | 150ms | default | Standard micro-interaction |
| Glass card shadow | 200ms | apple-ease | Shadow deepens and spreads on hover |
| Ghost icon buttons | 250ms | out-quart | Slightly slower for the bg tint reveal |
| Glass panel slide-in | 350ms | spring-gentle | Panels enter from side with spring curve |
| Blur-focus modal | 300ms | out-expo | Background blur + modal scale-up |
| Hero/page entry | 400ms | out-expo | Fade + slight upward drift |

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Barely perceptible |
| Chips | 0.98 | Slightly more visible |
| Buttons | 0.97 | Standard Apple button press |
| Tabs | 0.96 | More pronounced |
| Cards (clickable) | 0.99 | Very subtle — cards are large, less scale needed |

---

### Overlays

#### Popover / Dropdown

- **bg:** `rgba(255,255,255,0.82)` (glass-elevated opacity)
- **backdrop-filter:** `blur(24px) saturate(1.8)`
- **border:** `0.5px solid rgba(60,60,67,0.18)`
- **border-top:** `0.5px solid rgba(255,255,255,0.6)` (refraction highlight)
- **radius:** 12px
- **shadow:** shadow-glass-3
- **padding:** 6px
- **z-index:** 50
- **min-width:** 192px, **max-width:** 320px
- **overflow-y:** auto, max-height dynamic
- **Menu item:** 6px 8px padding, radius 8px, h 32px, font bodySmall, color text-secondary
- **Menu item hover:** bg `rgba(0,0,0,0.04)`, color text-primary
- **Transition:** 75ms default

#### Modal

- **Overlay bg:** `rgba(0,0,0,0.2)`
- **Overlay backdrop-filter:** `blur(12px)` — the background goes out of focus
- **Content bg:** `rgba(255,255,255,0.92)` (glass-modal opacity)
- **Content backdrop-filter:** `blur(40px) saturate(2.0)`
- **Content shadow:** shadow-glass-4
- **Content radius:** 16px
- **Content border-top:** `0.5px solid rgba(255,255,255,0.7)`
- **Entry:** scale `0.95` to `1.0` + opacity `0` to `1` + y `10px` to `0`, 300ms out-expo
- **Exit:** opacity `1` to `0` + scale `1.0` to `0.97`, 200ms apple-ease

#### Tooltip

Tooltips are NOT glass. They are solid, high-contrast surfaces for instant readability.

- **bg:** `#1D1D1F` (text-primary color, inverted)
- **color:** `#FFFFFF`
- **font:** label size (13px), weight 400
- **radius:** 6px
- **padding:** 4px 8px
- **shadow:** shadow-sm
- **No arrow.** Position via offset.

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column |
| Narrow max-width | 672px | Landing/focused content |
| Sidebar width | 280px | Fixed sidebar (glass-subtle) |
| Header height | 52px | Top bar, transparent bg |
| Spacing unit | 4px | Base multiplier |

#### Spacing Scale

4, 6, 8, 10, 12, 16, 24, 32px

#### Density

Comfortable. Apple HIG spacing: generous but not wasteful. 12-16px internal padding on cards, 8px gaps between list items, 24-32px section spacing.

#### Radius Scale (Theme Override)

Apple uses larger radii than typical web. This theme's scale:

| Token | Value | Usage |
|---|---|---|
| none | 0px | -- |
| sm | 6px | Badges, small elements |
| md | 8px | Sidebar items, chips, menu items |
| lg | 12px | Cards, popovers |
| xl | 16px | Modal containers |
| 2xl | 20px | Input card, large panels |
| input | 10px | Form inputs, textareas |
| full | 9999px | Avatars, toggles, pills |

#### Responsive Notes

- **lg (1024px+):** Full sidebar (280px, glass-subtle) + content column. Two concurrent glass layers.
- **md (768px):** Sidebar collapses to overlay panel (slides in as glass-elevated over content). One glass layer baseline.
- **sm (640px):** Single column. Header simplifies. Glass card radii reduce from 12px to 8px. Input card radius reduces from 20px to 12px. Blur values reduce by 40% for mobile performance.

---

### Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring color | `rgba(0, 122, 255, 0.4)` — System Blue at 40% |
| Focus ring width | 2px solid |
| Focus ring offset | 2px (white inner ring: `0 0 0 2px #FFF, 0 0 0 4px rgba(0,122,255,0.4)`) |
| Disabled opacity | 0.4 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled backdrop-filter | none (remove blur on disabled glass elements to signal inactivity) |
| Selection bg | `rgba(0, 122, 255, 0.2)` — System Blue at 20% |
| Selection color | `#1D1D1F` (text-primary, unchanged) |
| Scrollbar width | thin |
| Scrollbar thumb | `rgba(60, 60, 67, 0.2)` |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

#### Reduced Motion (`prefers-reduced-motion: reduce`)

| Behavior | Change |
|---|---|
| Strategy | `crossfade` — all spatial animations collapse to opacity-only crossfades. Glass panels fade in rather than sliding. |
| Glass Panel Slide (sig. #1) | `translateX` and blur ramp-up removed. Panel crossfades in at full blur over 150ms. `backdrop-filter` remains at target value instantly. |
| Blur-Focus Modal (sig. #2) | Background blur applies instantly (no progressive blur animation). Modal fades in at `scale(1)` — no scale or translateY movement. Duration capped at 150ms. |
| Shadow Elevation Shift (sig. #3) | Shadow transitions capped at 0.01s (effectively instant). Hover still changes shadow value but without visible animation. |
| Depth Parallax (sig. #4) | Disabled entirely. All layers scroll at 1.0x speed. `will-change: transform` never applied. |
| Glass Ripple Focus (sig. #5) | Focus ring appears instantly — no ripple expansion animation. `box-shadow` snaps to final value. |
| Scale presses | Disabled. No `transform: scale()` on active press. Instant visual state change via background/shadow only. |
| All hover/focus transitions | Remain functional but duration capped at 75ms. |
| `backdrop-filter` treatment | **Retained.** Blur and saturate values remain unchanged — they are static visual effects, not motion. Removing blur would break the glass visual language. Only the *animation* of blur values is removed. |
| Duration override cap | All animation durations capped at 0.01s. Transition durations capped at 75ms. |

**Glass contrast note:** All glass surfaces use minimum 72% white opacity. At this opacity, `#1D1D1F` text achieves 8.2:1 contrast ratio even when glass sits over a `#F2F2F7` background — well above AA. Against the worst case (glass over dark content), 72% white opacity resolves to approximately `rgb(194,194,199)`, and `#1D1D1F` against that is ~6.8:1, still AA-compliant. If glass appears over mixed dark-and-light backgrounds, increase opacity to 85% minimum.

---

### Visual Style

- **Grain:** None. Glass is pristine — not a single speck of noise. Any grain would undermine the clinical purity.
- **Gloss:** Soft sheen. The glass edge refraction highlights (white `border-top` at 30-70% opacity per level) provide the only gloss effect. No specular highlights, no reflections.
- **Blend mode:** Normal. No multiply, no screen. Translucency comes from alpha compositing and `backdrop-filter`, not blend modes.
- **Shader bg:** False. No WebGL, no canvas backgrounds. The page canvas is a simple solid color. If a background pattern is desired, use a CSS `radial-gradient` of extremely subtle concentric circles (`rgba(0,0,0,0.015)`) to give the glass something to show through — but this is optional.
- **Material quality:** The material is glass. Not plastic, not acrylic, not ice. Glass is perfectly smooth, perfectly flat, with depth communicated only through shadow and blur. Edges are precise, not rounded blobs. Corners are exact arcs.

---

### Signature Animations

#### 1. Glass Panel Slide

Glass panels enter from the side (bottom on mobile) with a spring animation. The panel starts 30px off-screen at 0% opacity with `backdrop-filter: blur(0px)`. It slides in with `spring(300, 30)`, fading in while the blur progressively frosts to its target value. The background appears to freeze as the panel arrives. Duration: 350ms.

```css
@keyframes glass-slide-in {
  from {
    transform: translateX(30px);
    opacity: 0;
    backdrop-filter: blur(0px) saturate(1);
  }
  to {
    transform: translateX(0);
    opacity: 1;
    backdrop-filter: blur(20px) saturate(1.8);
  }
}
.glass-slide { animation: glass-slide-in 350ms cubic-bezier(0.2, 0.8, 0.2, 1.02) both; }
```

#### 2. Blur-Focus Modal

Two simultaneous actions: (a) the background receives a progressive blur (`0` to `blur(12px)`) and dims to `rgba(0,0,0,0.2)`, and (b) the modal scales from `0.95` to `1.0` with fade-in, entering from 10px below with an out-expo curve. The background blur is the glass-native way to create a modal overlay — it looks like adjusting a camera's focal plane. Duration: 300ms.

```css
@keyframes blur-focus-overlay {
  from { backdrop-filter: blur(0px); background: rgba(0,0,0,0); }
  to { backdrop-filter: blur(12px); background: rgba(0,0,0,0.2); }
}
@keyframes modal-enter {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
```

#### 3. Shadow Elevation Shift

On glass card hover, the shadow animates from shadow-glass-2 to shadow-glass-3 over 200ms. Each shadow layer independently transitions — the contact shadow tightens slightly while the ambient shadow widens, simulating the card physically lifting. This is the glass theme's hover signature: depth change, not color change.

```css
.glass-card {
  box-shadow: 0 0.5px 1px rgba(0,0,0,0.06), 0 2px 6px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06);
  transition: box-shadow 200ms cubic-bezier(0.25, 0.1, 0.25, 1);
}
.glass-card:hover {
  box-shadow: 0 0.5px 1px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.04), 0 12px 32px rgba(0,0,0,0.08), 0 24px 48px rgba(0,0,0,0.04);
}
```

#### 4. Depth Parallax

Glass panels at different elevation levels scroll at slightly different rates. Level 1 panels move at 1.0x scroll speed (normal), level 2 at 0.98x, level 3 at 0.96x. The 2-4% difference is nearly invisible but creates a subconscious sense of layered depth. Use `transform: translateY()` on scroll via `requestAnimationFrame`. Apply `will-change: transform` during scroll, remove after. Disable entirely with `prefers-reduced-motion`.

#### 5. Glass Ripple Focus

When a glass element receives keyboard focus, the focus ring expands outward from the element as a brief ripple rather than appearing instantly. The `box-shadow` animates from `0 0 0 0px` to `0 0 0 2px #FFF, 0 0 0 4px rgba(0,122,255,0.4)` over 150ms with apple-ease. This makes keyboard navigation feel intentional, not mechanical.

```css
@keyframes focus-ripple {
  from { box-shadow: 0 0 0 0px rgba(0,122,255,0); }
  to { box-shadow: 0 0 0 2px #FFFFFF, 0 0 0 4px rgba(0,122,255,0.4); }
}
```

---

### Dark Mode Variant

**Not natively dark.** This is a light-mode-first theme. The dark variant reverses the glass treatment: panels become dark-frosted translucent surfaces over a dark canvas.

#### Dark Palette

| Token | Light Value | Dark Value | Notes |
|---|---|---|---|
| page | `#F2F2F7` | `#1C1C1E` | Apple dark background |
| bg (glass) | `rgba(255,255,255,0.72)` | `rgba(44,44,46,0.72)` | Dark frosted glass |
| surface (glass) | `rgba(255,255,255,0.82)` | `rgba(58,58,60,0.80)` | Elevated dark glass |
| recessed | `#E5E5EA` | `#0A0A0A` | Deep recessed |
| active | `rgba(0,0,0,0.06)` | `rgba(255,255,255,0.08)` | Inverted active tint |
| text-primary | `#1D1D1F` | `#F5F5F7` | Near-white |
| text-secondary | `rgba(60,60,67,0.6)` | `rgba(235,235,245,0.6)` | Inverted base at 60% |
| text-muted | `rgba(60,60,67,0.3)` | `rgba(235,235,245,0.3)` | Inverted base at 30% |
| border-base | `#3C3C43` | `#545458` | Lighter separator for dark |
| accent-primary | `#007AFF` | `#0A84FF` | Dark mode blue (brighter) |
| success | `#34C759` | `#30D158` | Dark mode green (brighter) |
| warning | `#FF9500` | `#FF9F0A` | Dark mode orange |
| danger | `#FF3B30` | `#FF453A` | Dark mode red |

#### Dark Mode Rules

- Surfaces use the same alpha-opacity system — just over dark base colors instead of white
- `backdrop-filter` `saturate()` increases to `2.0` for standard glass (dark glass needs more vibrancy to avoid looking dead)
- Glass edge refraction highlights become MORE important in dark mode (shadows are less visible against dark backgrounds). Increase white `border-top` opacity by 10% per level.
- Shadows shift to darker values: `rgba(0,0,0,0.15)` replaces `rgba(0,0,0,0.06)` for contact shadows
- Scrollbar thumb: `rgba(235,235,245,0.2)`
- Selection bg: `rgba(10,132,255,0.3)` (dark mode blue at 30%)
- `inlineCode`: `#FC6C6C` (lighter salmon for dark backgrounds)
- Focus ring remains the same blue — it works on both modes

---

### Mobile Notes

#### Effects to Disable
- Depth parallax animation (signature #4) — disabled entirely
- Glass Ripple Focus animation (signature #5) — collapses to instant focus ring
- Reduce max concurrent glass layers from 3 to 2

#### Adjustments
- `backdrop-filter: blur()` values reduce by 40%: `blur(20px)` becomes `blur(12px)`, `blur(12px)` becomes `blur(8px)`, `blur(40px)` becomes `blur(24px)`
- `saturate()` reduces by 15%: `saturate(1.8)` becomes `saturate(1.5)`
- Glass opacity increases by 10%: 72% becomes 82%, 82% becomes 90% — ensures readability on smaller screens
- Card border-radius: 12px reduces to 8px
- Input card border-radius: 20px reduces to 12px
- Toggle stays 51x31px (already 44px+ touch target)
- All interactive elements maintain minimum 44px touch target
- Body text stays 17px (already comfortable for mobile)

#### Performance Notes
- `backdrop-filter` is GPU-composited but expensive when stacked. Two concurrent blurred layers is the mobile budget.
- Apply `will-change: transform` only during animations, never permanently.
- Sidebar overlay on mobile uses glass-elevated (not glass-subtle) to reduce visual noise from the content underneath.
- Total visible blur radius across all layers should not exceed 50px on mobile (vs 80px desktop budget).

---

### Implementation Checklist

- [ ] Google Fonts loaded: Plus Jakarta Sans (400, 500, 600, 700), DM Sans (400, 500), Geist Mono (400)
- [ ] CSS custom properties defined for all color tokens including rgba glass surfaces
- [ ] `backdrop-filter` applied to all glass surfaces with correct blur and saturate values
- [ ] `@supports not (backdrop-filter: blur(1px))` fallback defined (near-opaque bg, standard shadows)
- [ ] Border-radius scale applied per component (8, 10, 12, 16, 20px)
- [ ] Shadow composite tokens applied per elevation level (glass-1 through glass-4)
- [ ] Shadow escalation on hover/focus for cards and inputs (glass-2 to glass-3, input to input-hover to input-focus)
- [ ] Glass edge refraction highlights (`border-top` white at varying opacity) on all glass panels
- [ ] Opacity escalation rule applied to nested glass (each nested layer +10% opacity)
- [ ] Border opacity system implemented (8%, 12%, 18% on `border-base`)
- [ ] Focus ring (`0 0 0 2px #FFF, 0 0 0 4px rgba(0,122,255,0.4)`) on all interactive elements
- [ ] `prefers-reduced-motion` media query: spatial animations collapse to fades, parallax disabled, backdrop-filter retained
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] Scrollbar styled: thin, `rgba(60,60,67,0.2)` thumb, transparent track
- [ ] Touch targets >= 44px on all interactive elements
- [ ] State transitions match motion map (75ms sidebar, 100ms buttons, 150ms toggles, 200ms cards, 350ms panels)
- [ ] Glass tint system implemented for semantic notification panels
- [ ] `::selection` styled with System Blue at 20%
- [ ] `::placeholder` opacity matches text-muted token
- [ ] Dark mode variant: all tokens swap, saturate values increase, refraction highlights intensify
