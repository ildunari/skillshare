# Pixel Grid — Quick Reference

**Best for:** Data dashboards, analytics platforms, developer monitoring tools, terminal-adjacent apps, real-time telemetry, infrastructure status pages, quantitative research tools.

**Decision principle:** "When in doubt, ask: does this feel like data on a grid? If it feels smooth, step it. If it feels round, square it. If it feels decorative, remove it."

---

## Dual Thermal Modes

**Warm ("Gazette"):** Newspaper broadsheet — warm earthy tones, cream paper grain, Space Grotesk ALL CAPS headlines, JetBrains Mono body.

**Cool ("Terminal"):** Vercel-grade terminal — true black, vivid blue accents, Inter sentence-case headlines, Geist Mono body.

**Shared philosophy:** Quantized motion (`steps(n)`), 0px radius everywhere, borders-only elevation, dense information display.

---

## Color Tokens

### Warm Mode ("Gazette")

| Token | Hex | Role |
|---|---|---|
| page | `#1C1917` | Deepest background. Newsprint dark, warm undertone. |
| bg | `#292524` | Primary surface. Slightly lifted from page. |
| surface | `#353130` | Elevated cards, inputs, popovers. Warm mid-tone. |
| recessed | `#0C0A09` | Code blocks, inset data wells. Darkest recessed. |
| active | `#44403C` | Active/pressed items, selected rows. |
| text-primary | `#FAEBD7` | Headings, body text. Antique white, warm cast. |
| text-secondary | `rgba(250,235,215,0.64)` | Sidebar items, secondary labels. text-primary at 64%. |
| text-muted | `rgba(250,235,215,0.38)` | Placeholders, timestamps, metadata. text-primary at 38%. |
| text-onAccent | `#1C1917` | Text on sienna accent backgrounds. |
| border-base | `#A8A29E` | Used at variable opacity. Stone 400. |
| accent-primary | `#D97757` | Primary CTA, active controls, chart highlight. |
| accent-secondary | `#CA8A04` | Secondary accent for links, info callouts. |
| success | `#84CC16` | Positive states. Lime-shifted for warm harmony. |
| warning | `#F59E0B` | Caution states. |
| danger | `#DC2626` | Error states, destructive actions. |
| info | `#60A5FA` | Info states, informational chips. |
| inlineCode | `#F97316` | Code text within prose. Orange, high contrast on dark warm. |
| toggleActive | `#84CC16` | Toggle/switch active track. Matches success. |
| selection | `rgba(217,119,87,0.25)` | `::selection` background. Sienna at 25%. |

**Per-Agent Accent System (Warm):** Six agent colors at equal OKLCH lightness (L=0.72, C=0.14):

| Agent | Hex | Hue | Usage |
|---|---|---|---|
| Agent 1 | `#D97757` | 30 (sienna) | Primary agent, default accent |
| Agent 2 | `#CA8A04` | 85 (gold) | Secondary agent |
| Agent 3 | `#84CC16` | 125 (olive) | Tertiary agent |
| Agent 4 | `#06B6D4` | 195 (cyan) | Fourth agent |
| Agent 5 | `#818CF8` | 260 (indigo) | Fifth agent |
| Agent 6 | `#E879A8` | 340 (rose) | Sixth agent |

### Cool Mode ("Terminal")

| Token | Hex | Role |
|---|---|---|
| page | `#000000` | Deepest background. Pure black, zero warmth. |
| bg | `#0A0A0A` | Primary surface. Barely lifted from black. |
| surface | `#161616` | Elevated cards, inputs, popovers. Vercel surface. |
| recessed | `#050505` | Code blocks, inset data wells. Near-black. |
| active | `#262626` | Active/pressed items, selected rows. |
| text-primary | `#EDEDED` | Headings, body text. Vercel white. |
| text-secondary | `rgba(237,237,237,0.64)` | Sidebar items, secondary labels. text-primary at 64%. |
| text-muted | `rgba(237,237,237,0.38)` | Placeholders, timestamps, metadata. text-primary at 38%. |
| text-onAccent | `#FFFFFF` | Text on vivid blue accent backgrounds. |
| border-base | `#525252` | Used at variable opacity. Neutral 600. |
| accent-primary | `#0070F3` | Primary CTA, active controls. Vercel blue. |
| accent-secondary | `#00D4FF` | Secondary accent for links, data highlights. |
| success | `#22C55E` | Positive states. |
| warning | `#F59E0B` | Caution states. |
| danger | `#EF4444` | Error states, destructive actions. |
| info | `#3B82F6` | Info states. |
| inlineCode | `#00D4FF` | Code text within prose. Cyan, terminal-native. |
| toggleActive | `#22C55E` | Toggle/switch active track. Matches success. |
| selection | `rgba(0,112,243,0.25)` | `::selection` background. Vivid blue at 25%. |

**Per-Agent Accent System (Cool):** Six agent colors at equal OKLCH lightness (L=0.72, C=0.16):

| Agent | Hex | Hue | Usage |
|---|---|---|---|
| Agent 1 | `#0070F3` | 220 (blue) | Primary agent, default accent |
| Agent 2 | `#00D4FF` | 190 (cyan) | Secondary agent |
| Agent 3 | `#22C55E` | 145 (green) | Tertiary agent |
| Agent 4 | `#F59E0B` | 45 (amber) | Fourth agent |
| Agent 5 | `#A855F7` | 275 (purple) | Fifth agent |
| Agent 6 | `#EC4899` | 330 (pink) | Sixth agent |

### Opacity System

Border opacity on `border-base`:
- **subtle:** 12% — Internal dividers, grid lines within cards
- **card:** 20% — Card-level borders, panel edges
- **hover:** 30% — Hovered elements, interactive feedback
- **focus:** 100% (accent) — Focus ring uses full accent color, not border-base

---

## Typography

### Warm Mode ("Gazette")

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Space Grotesk | 18px | 700 | 1.2 | 0.14em | `text-transform: uppercase` | Hero titles, page names. ALL CAPS. |
| Heading | Space Grotesk | 13px | 700 | 1.3 | 0.10em | `text-transform: uppercase` | Section titles, panel headers. ALL CAPS. |
| Body | JetBrains Mono | 13px | 400 | 1.5 | normal | `font-feature-settings: "zero"` | Primary reading text, data tables. |
| Body Small | JetBrains Mono | 11px | 400 | 1.45 | normal | `font-feature-settings: "zero"` | Sidebar items, form labels. |
| Button | Space Grotesk | 11px | 600 | 1.4 | 0.06em | `text-transform: uppercase` | Button labels. ALL CAPS. |
| Input | JetBrains Mono | 13px | 400 | 1.4 | normal | `font-feature-settings: "zero"` | Form input text. |
| Label | Space Grotesk | 9px | 500 | 1.3 | 0.08em | `text-transform: uppercase` | Metadata, timestamps, axis labels. ALL CAPS. |
| Code | JetBrains Mono | 12px | 400 | 1.5 | normal | `font-feature-settings: "liga", "zero"` | Inline code, code blocks. |
| Caption | JetBrains Mono | 9px | 400 | 1.33 | normal | -- | Footnotes, disclaimers, tiny data annotations. |

### Cool Mode ("Terminal")

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Inter | 17px | 600 | 1.2 | -0.02em | -- | Hero titles, page names. Sentence case. |
| Heading | Inter | 13px | 600 | 1.3 | -0.01em | -- | Section titles, panel headers. |
| Body | Geist Mono | 13px | 400 | 1.5 | normal | -- | Primary reading text, data tables. |
| Body Small | Geist Mono | 11px | 400 | 1.45 | normal | -- | Sidebar items, form labels. |
| Button | Inter | 11px | 500 | 1.4 | 0.01em | -- | Button labels. |
| Input | Geist Mono | 13px | 400 | 1.4 | normal | -- | Form input text. |
| Label | Inter | 9px | 500 | 1.3 | 0.04em | `text-transform: uppercase` | Metadata, timestamps, axis labels. |
| Code | Geist Mono | 12px | 400 | 1.5 | normal | -- | Inline code, code blocks. |
| Caption | Geist Mono | 9px | 400 | 1.33 | normal | -- | Footnotes, disclaimers, tiny data annotations. |

**Strict 3-size hierarchy:** Small (9-11px), Medium (12-13px), Large (17-18px). Nothing between, nothing outside.

---

## Elevation

**Strategy:** `borders-only`

Flat theme. Depth via border weight and surface tint, not shadows. Warm mode: ZERO shadows. Cool mode: ONE shadow (popover only).

| Surface | Warm BG | Cool BG | Shadow | Usage |
|---|---|---|---|---|
| page | `#1C1917` | `#000000` | none | Main page canvas |
| bg | `#292524` | `#0A0A0A` | none | Primary surface, sidebar bg |
| surface | `#353130` | `#161616` | none | Cards, inputs, elevated panels |
| recessed | `#0C0A09` | `#050505` | none | Code blocks, data wells |
| active | `#44403C` | `#262626` | none | Active/pressed, selected rows |
| overlay | `#353130` | `#161616` | shadow-popover (Cool only) | Popovers, dropdowns |

**Shadow-popover (Cool only):** `0 4px 12px rgba(0,0,0,0.5), 0 0 0 1px rgba(82,82,82,0.20)`

---

## Borders

**ALL border-radius: 0px.** No exceptions. Rectangles only.

| Pattern | Width | Opacity | Usage |
|---|---|---|---|
| internal | 1px | 12% | Dividers within cards, grid lines, separators. |
| card | 1.5px | 20% | Card edges, panel boundaries, input borders. |
| heavy | 2px | 30% | Section dividers, header underlines, emphasis borders. |
| input-hover | 1.5px | 30% | Input hover. |
| input-focus | 1.5px | 100% (accent) | Input focus. Full accent color. |
| accent-left | 2px | 100% (accent) | Left-border accent on active sidebar items, callouts. |

**Focus Ring:** 2px solid accent-primary, 2px offset. Warm: `#D97757`, Cool: `#0070F3`

---

## Motion

**Core philosophy:** Quantized motion. ALL transitions use `steps(n)`. `cubic-bezier` BANNED (one exception: card entrance uses `linear`).

### Easings

| Name | Value | Character |
|---|---|---|
| instant | `steps(1)` | Single-frame snap. Default for all interactions. |
| tick-2 | `steps(2)` | Two-frame blink. Loading indicators. |
| tick-4 | `steps(4)` | Four-frame stutter. Progress bars. |
| tick-8 | `steps(8)` | Eight-frame march. Signature step animation. |
| tick-16 | `steps(16)` | Sixteen-frame sequence. Smooth-ish for large movements. |
| card-entrance | `linear` | ONLY exception. 200ms linear for initial card entrance. |

**Tick interval:** 800ms base. An 8-step animation over 800ms = 100ms per frame.

### Duration x Component

| Component | Duration | Easing |
|---|---|---|
| Button hover bg | 0ms | `steps(1)` |
| Sidebar item hover | 0ms | `steps(1)` |
| Toggle thumb position | 0ms | `steps(1)` |
| Input focus border | 0ms | `steps(1)` |
| Card entrance | 200ms | `linear` |
| Progress bar advance | 800ms | `steps(8)` |
| Status indicator blink | 800ms | `steps(2)` |
| Data cell update flash | 400ms | `steps(4)` |
| Step block fill | 1600ms | `steps(16)` |

**Active Press Scale:** NONE. No `transform: scale()`. Active states use color/bg change only, snapped via `steps(1)`.

---

## Component Quick-Reference

### Primary Button

| State | Properties |
|---|---|
| Rest | bg `accent-primary`, color `text-onAccent`, radius 0px, h 32px, padding `0 12px` |
| Hover | bg accent lightened 8% (Warm: `#E0916F`, Cool: `#1A80F5`), transition `steps(1)` |
| Active | bg accent darkened 10% (Warm: `#C46845`, Cool: `#005BC2`) |
| Focus | outline `2px solid accent-primary`, offset 2px |

### Text Input

| State | Properties |
|---|---|
| Rest | bg `surface`, border `1.5px solid border-base at 20%`, radius 0px, h 36px, padding `0 8px`, caret-color `accent-primary` |
| Hover | border at 30%, transition `steps(1)` |
| Focus | border `1.5px solid accent-primary`, box-shadow `0 0 0 1px accent-primary` (Cool only) |

### Card

| State | Properties |
|---|---|
| Rest | bg `surface`, border `1.5px solid border-base at 20%`, radius 0px, shadow none |
| Hover | border at 30%, bg lightened 1 stop (Warm: `#3D3937`, Cool: `#1A1A1A`), transition `steps(1)` |

### Toggle/Switch (Rectangular)

- **Track:** 36x18px, 0px radius
- **Track off:** bg `active`, border `1.5px solid border-base at 20%`
- **Track on:** bg `toggleActive` (Warm: `#84CC16`, Cool: `#22C55E`)
- **Thumb:** 14x14px square, bg `text-primary`, 0px radius
- **Transition:** `all 0ms steps(1)` — thumb snaps between positions, no slide

---

## Layout

| Token | Value |
|---|---|
| Content max-width | 768px |
| Narrow max-width | 640px |
| Sidebar width | 260px |
| Header height | 40px |
| Spacing unit | 4px |

**Spacing scale:** 4, 8, 12, 16, 24, 32, 48px — strictly 4px-aligned.

**Density:** Dense. 4-8px internal padding on cards. 4px gaps between list items. 12-16px section spacing.

---

## Section Index

- **Identity & Philosophy** — Bloomberg terminal aesthetic, dual thermal modes, quantized motion
- **Color System** — Warm/Cool palettes, per-agent accent system, opacity system
- **Typography Matrix** — Space Grotesk + JetBrains Mono (Warm), Inter + Geist Mono (Cool)
- **Elevation System** — Borders-only, flat surfaces, zero shadows (Warm) / one popover shadow (Cool)
- **Border System** — 0px radius everywhere, 1px/1.5px/2px width hierarchy
- **Component States** — Buttons, inputs, cards, sidebar items, chips, toggle
- **Motion Map** — Quantized `steps(n)` timing, 800ms tick interval, no cubic-bezier
- **Layout Tokens** — 4px grid, dense spacing, 768px content max-width
- **Accessibility Tokens** — Focus ring, disabled states, selection, scrollbar, reduced motion
- **Overlays** — Popover, modal, tooltip specs
- **Visual Style** — 5 pixel components (mosaic bar, 3x3 grid, bar chart, step blocks, 7x7 icons), paper grain (Warm), data viz philosophy
- **Signature Animations** — Pixel ticker tape, grid cell flash, status blink, step block fill, card entrance
- **Mode Variant** — Warm vs Cool comparison, light mode variant
- **Mobile Notes** — Effects to disable, adjustments, performance notes
- **Implementation Checklist** — 27 checkpoints for production deployment
