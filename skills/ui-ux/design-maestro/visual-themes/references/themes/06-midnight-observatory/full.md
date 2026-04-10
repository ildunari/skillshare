# Midnight Observatory — Full Specification

> Schema v2 | 1019 lines | Last updated: 2026-02-16

## Table of Contents

| Section | Line |
|---|---|
| Identity & Philosophy | 36 |
| Color System | 58 |
| Typography Matrix | 141 |
| Elevation System | 185 |
| Border System | 231 |
| Component States | 280 |
| Motion Map | 420 |
| Overlays | 471 |
| Layout Tokens | 528 |
| Accessibility Tokens | 582 |
| Visual Style | 626 |
| Signature Animations | 671 |
| Light Mode Variant | 804 |
| Mobile Notes | 840 |
| Data Visualization | 873 |
| Implementation Checklist | 988 |

---

## 6. Midnight Observatory

> Deep space meets scientific cartography — warm gold constellations projected on infinite navy, the hum of precise instruments.

**Best for:** Data visualizations, star maps, scientific simulations, time-series dashboards, astronomical models, network graphs, observatory control panels, celestial mechanics tools, research data platforms, signal processing interfaces.

---

### Identity & Philosophy

This theme lives in the world of a planetarium control room at 2 AM. The dome overhead projects gold constellations onto infinite navy void. The instruments hum with precision. The air smells of old star atlases and warm electronics. Every surface is dark, every data point glows. The person here is a scientist, a navigator, a cartographer of the sky — someone who works with precise data rendered beautifully against darkness.

The signature visual identity is **emission on void**: light sources against deep space. Nothing is illuminated from above (no drop shadows, no ambient light). Instead, data and interactive elements emit their own glow, the way stars and instrument panels do in darkness. Gold is the primary emission color — warm, scientific, the color of brass instruments, gilt star charts, and celestial projection systems. Teal is the connective tissue — the color of constellation guide lines, grid overlays, and secondary data channels. Dusty rose marks tertiary data and occasional accents, like nebula regions on a deep-sky chart.

The depth strategy is **glow-based**. In a dark observatory, elevation is not shadow beneath an object but light emitted by it. Higher-importance elements glow more intensely. The deepest background (`#0B1426`) is infinite — it has no floor, no edge, no gradient. It simply recedes. Cards and surfaces are dark indigo islands floating in that void, defined not by shadows below them but by subtle border delineation and, on interaction, inner glow.

Typography is tight, condensed, data-optimized. Instrument Sans brings the condensed dashboard energy of instrument panels — tight letter-spacing, multiple data columns fitting cleanly. Albert Sans provides Scandinavian clean body text that reads well on dark backgrounds at small sizes. JetBrains Mono handles all data values, coordinates, and timestamps with tabular numerals for column alignment.

**Decision principle:** "When in doubt, ask: would this look right projected on the dome of a planetarium? If it breaks the darkness, dim it. If it lacks precision, tighten it. If it feels decorative rather than instrumental, remove it."

**What this theme is NOT:**
- Not neon/cyberpunk — gold is warm brass, not electric yellow. No saturated neon greens, pinks, or blues. No scan lines, no CRT effects, no glitch aesthetics.
- Not gaming — this is scientific, not entertainment. No HUD overlays, no progress XP bars, no achievement badges.
- Not gradient-heavy — the night sky is a flat void, not a gradient. No navy-to-purple gradients, no aurora effects, no colorful nebula backgrounds.
- Not sparse — this is a control room, not a meditation app. Data density is moderate to high. The darkness provides visual breathing room, not emptiness.
- Not flat — glow-based depth is real depth. Elements at different elevation levels must be distinguishable through their glow intensity and surface brightness.
- Not cold — gold gives this theme warmth despite the dark base. Cold steel-blue or grey-only palettes miss the identity. The brass-and-gold warmth of real astronomical instruments is essential.

---

### Color System

#### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Void | `#080E1C` | L=0.12 C=0.03 h=260 | Deepest background. Infinite dark space beyond the dome. |
| bg | Deep Navy | `#0B1426` | L=0.15 C=0.04 h=255 | Primary surface background. The observatory wall. |
| surface | Dark Indigo | `#141E33` | L=0.19 C=0.04 h=250 | Elevated cards, inputs, popovers. Instrument panel face. |
| recessed | Abyss | `#0A0F1E` | L=0.11 C=0.03 h=258 | Code blocks, inset areas. Deeper than page — a cutaway to void. |
| active | Pressed Indigo | `#1A2844` | L=0.22 C=0.05 h=248 | Active/pressed items, user bubbles. Indigo energized by interaction. |
| text-primary | Silver Light | `#D4DCE8` | L=0.88 C=0.02 h=240 | Headings, body text. Bright enough for WCAG AA on all surfaces. |
| text-secondary | Pale Steel | `#8A96A8` | L=0.64 C=0.03 h=240 | Sidebar items, secondary labels. Dim starlight. |
| text-muted | Twilight Grey | `#5A6578` | L=0.45 C=0.03 h=240 | Placeholders, timestamps, metadata. Faintest readable value. |
| text-onAccent | Void | `#0B1426` | L=0.15 C=0.04 h=255 | Dark text on gold-filled backgrounds (buttons, badges). |
| border-base | Navy Light | `#2A3B5C` | L=0.30 C=0.06 h=248 | Base border color used at variable opacity. Star chart grid ink. |
| accent-primary | Observatory Gold | `#FFD700` | L=0.90 C=0.18 h=95 | Primary data points, stars, CTA buttons, focus rings. Warm brass. |
| accent-secondary | Chart Teal | `#4A9B9B` | L=0.62 C=0.08 h=190 | Constellation lines, secondary data, connections. |
| accent-tertiary | Nebula Rose | `#C4767A` | L=0.58 C=0.10 h=15 | Tertiary data series, occasional accents. Dusty rose. |
| success | Signal Green | `#4CAF6E` | L=0.65 C=0.12 h=150 | Positive states. System operational. |
| warning | Amber Alert | `#E8A830` | L=0.76 C=0.14 h=80 | Caution states. Instrument warning. |
| danger | Red Giant | `#D14B4B` | L=0.52 C=0.16 h=20 | Error states, critical alerts. Dying star. |
| info | Cool Blue | `#4A88C4` | L=0.58 C=0.10 h=240 | Informational states. Instrument readout blue. |

#### Special Tokens

| Token | Hex | Role |
|---|---|---|
| inlineCode | `#E8C84A` | Code text within prose. Slightly muted gold, legible on dark surfaces. |
| toggleActive | `#4A9B9B` | Toggle/switch active track. Chart Teal — data flow is "on." |
| selection | `rgba(255, 215, 0, 0.18)` | `::selection` background. Gold at low opacity on dark. |
| starWhite | `#FFFFFF` | Pure white for individual data points, star markers, highest-emphasis elements. |
| gridLine | `#1E2D4A` | Background grid lines, coordinate system. Between surface and border-base. |

#### Gold Emission System

Gold is the soul of this theme. It represents data, focus, navigation, and primary importance. Its usage is emission-based — gold always glows from within, never fills large areas:

| Usage | Form | Opacity/Intensity | Notes |
|---|---|---|---|
| Data points | Small filled circles (4-8px) | 100% fill + glow shadow | `box-shadow: 0 0 8px rgba(255,215,0,0.3)` |
| Focus rings | 2px ring | 60% | Gold ring on all focused elements |
| Primary CTA buttons | Gold fill | 100% fill | Only button type with gold background |
| Active borders | 1px bottom or left border | 50% | Current/selected state indicator |
| Star markers | 1-2px dots | 20-80% varied | Background star field decoration |
| Chart axis labels | Text color | 100% on values, 60% on labels | Hierarchy through opacity |
| Progress indicators | 2px horizontal line | 100% fill with glow | Thin gold thread |
| Hover gold tint | Background tint | 6-10% | Faint gold warmth on hover |
| Scrollbar thumb | Solid track | 30% | Gold-tinted scroll indicator |

**Gold anti-patterns (never do these):**
- Gold as card background fill (cards are dark indigo, always)
- Gold gradient of any kind (gold is a point source, not a field)
- Gold used on more than 15% of any viewport area (gold is data-density-limited)
- Gold text on gold backgrounds
- Multiple competing gold glow sources at similar intensity in the same region

#### Opacity System

Border opacity (on `border-base` Navy Light):

| Level | Opacity | Usage |
|---|---|---|
| ghost | 10% | Faintest grid lines, background structure |
| subtle | 20% | Panel edges, card outlines at rest |
| card | 30% | Default card and content borders |
| hover | 45% | Hovered elements, interactive state |
| focus | 60% | Focused inputs, active delineation |

Note: opacity values are higher than in light themes because dark backgrounds require stronger border delineation for contrast.

#### Color Rules

- No pure black backgrounds. The deepest value is `#080E1C` (Void) — it has a blue tint that reads as infinite depth rather than digital black.
- Gold is the only warm color in the base palette. All neutrals carry a cool blue-navy undertone. Gold's warmth against this coolness creates the signature tension.
- The teal accent (`#4A9B9B`) is never used for text. It is structural — lines, connections, secondary data series. If teal appears as body text, the implementation has failed.
- The dusty rose (`#C4767A`) is the rarest accent. It appears only in data visualization as a third series color, or as a highlight for exceptional states (not errors — use `danger` red for errors).
- Semantic colors are adapted for dark backgrounds — brighter and more saturated than in light themes to maintain WCAG AA contrast.
- No gradients on surfaces. The void is flat. Cards are flat. Depth comes from glow, not color transitions.
- White (`#FFFFFF`) is used sparingly for maximum-emphasis data points only. Primary text uses Silver Light, not white — pure white on dark backgrounds causes eye strain at paragraph scale.

---

### Typography Matrix

#### Font Stack

Instrument Sans is the display typeface — a modern condensed sans-serif with the tight energy of instrument panel labels. Its condensed proportions allow dense data display without feeling cramped. Albert Sans provides the Scandinavian clean body text — readable at small sizes on dark backgrounds, with clear letterforms that perform well under antialiasing. JetBrains Mono is the data typeface — tabular numerals, clear distinction between similar characters (0/O, 1/l/I), and ligatures disabled for precise data rendering.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | sans (Instrument Sans) | 36px | 600 | 1.15 | -0.02em | -- | Hero metrics, dashboard titles. Tight, impactful. |
| Heading | sans (Instrument Sans) | 22px | 600 | 1.25 | -0.01em | -- | Section titles, panel headers |
| Subheading | sans (Instrument Sans) | 17px | 500 | 1.35 | normal | -- | Subsection labels, card titles |
| Body | sans (Albert Sans) | 15px | 400 | 1.55 | 0.01em | -- | Primary reading text. Slightly smaller than default — data environments value density. |
| Body Small | sans (Albert Sans) | 13px | 400 | 1.45 | 0.01em | -- | Sidebar items, secondary UI text, form labels |
| Button | sans (Instrument Sans) | 13px | 600 | 1.4 | 0.03em | `text-transform: none` | Button labels. Condensed but not small-caps. |
| Input | sans (Albert Sans) | 14px | 400 | 1.4 | normal | -- | Form input text |
| Label | sans (Instrument Sans) | 11px | 500 | 1.3 | 0.06em | `text-transform: uppercase` | Metadata, axis labels, timestamps. Uppercase feels instrumental. |
| Code | mono (JetBrains Mono) | 13px | 400 | 1.5 | normal | `font-variant-numeric: tabular-nums; font-feature-settings: "liga" 0` | Data values, coordinates, code blocks |
| Caption | sans (Albert Sans) | 11px | 400 | 1.35 | 0.02em | -- | Disclaimers, footnotes, chart annotations |

#### Typographic Decisions

- 15px body is slightly smaller than the standard 16px. This is intentional — observatory/dashboard contexts need higher information density, and Albert Sans remains fully legible at 15px on dark backgrounds.
- Labels are uppercase with generous letter-spacing (0.06em). This mimics real instrument panel labeling — ALTITUDE, AZIMUTH, DECLINATION — and reinforces the scientific identity.
- Display text uses -0.02em tracking. Instrument Sans at large sizes has naturally open spacing; tightening it creates the dense, precise feel of instrument readouts.
- `-webkit-font-smoothing: antialiased` is critical. Light text on dark backgrounds without antialiasing looks chunky and over-rendered. This is non-negotiable.
- `text-wrap: balance` for headings, `pretty` for body text. Balance prevents orphaned words in short headings; pretty optimizes line breaks for readability.
- JetBrains Mono with `"liga" 0` — ligatures are disabled because in data contexts, `!=` must render as two distinct characters, not a combined glyph. Data is literal.

#### Font Loading

```html
<!-- Midnight Observatory Theme -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Albert+Sans:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**Fallback chains:**
- Display/Heading: `"Instrument Sans", "SF Pro Condensed", "Roboto Condensed", system-ui, sans-serif`
- Body: `"Albert Sans", "Inter", system-ui, sans-serif`
- Mono: `"JetBrains Mono", "SF Mono", "Cascadia Mono", "Consolas", ui-monospace, monospace`

---

### Elevation System

**Strategy:** `glow`

In a dark observatory, depth is defined by light emission, not shadow. Objects at higher elevation levels glow more brightly. The deepest background emits no light — it is void. Cards emit faint light at their edges. Focused elements bloom with gold emission. This inverts the typical elevation model: instead of "higher = more shadow below," it is "higher = more light emitted."

#### Surface Hierarchy

| Surface | Background | Border | Glow/Shadow | Usage |
|---|---|---|---|---|
| void | `#080E1C` Void | none | none | Deepest background. Space beyond the dome. |
| page | `#0B1426` Deep Navy | none | none | Primary canvas. Observatory wall. |
| panel | `#141E33` Dark Indigo | `0.5px solid border-base/20%` | none | Cards, inputs, elevated panels. |
| recessed | `#0A0F1E` Abyss | `0.5px solid border-base/10%` | `inset 0 1px 4px rgba(0,0,0,0.3)` | Code blocks, inset data areas. |
| overlay | `#1A2844` Pressed Indigo | `0.5px solid border-base/30%` | `0 0 24px rgba(0,0,0,0.4), 0 0 1px rgba(255,215,0,0.08)` | Popovers, dropdowns. Faintest gold edge glow. |

#### Shadow/Glow Tokens

| Token | Value | Usage |
|---|---|---|
| glow-none | `none` | Flat surfaces, page background |
| glow-data | `0 0 8px rgba(255,215,0,0.25)` | Gold data point emission. The signature glow. |
| glow-data-intense | `0 0 12px rgba(255,215,0,0.4), 0 0 4px rgba(255,215,0,0.6)` | Hovered/focused data points. Brighter bloom. |
| glow-card-rest | `0 1px 4px rgba(0,0,0,0.2)` | Card at rest. Very subtle downward shadow for grounding. |
| glow-card-hover | `0 2px 8px rgba(0,0,0,0.25), inset 0 0 0 1px rgba(255,215,0,0.04)` | Card hover. Shadow deepens + faint gold inner edge. |
| glow-card-focus | `0 2px 12px rgba(0,0,0,0.3), 0 0 0 2px rgba(255,215,0,0.25)` | Card focus. Shadow deepens + gold focus ring. |
| glow-input-rest | `0 1px 4px rgba(0,0,0,0.15)` | Input at rest. |
| glow-input-hover | `0 2px 6px rgba(0,0,0,0.2), inset 0 0 0 1px rgba(42,59,92,0.3)` | Input hover. Inner border brightens. |
| glow-input-focus | `0 2px 8px rgba(0,0,0,0.25), 0 0 0 2px rgba(255,215,0,0.4)` | Input focus. Gold emission ring. |
| glow-popover | `0 4px 24px rgba(0,0,0,0.5), 0 0 1px rgba(255,215,0,0.06)` | Popovers, dropdowns. Deep shadow + whisper of gold edge. |
| glow-inset | `inset 0 1px 4px rgba(0,0,0,0.3)` | Recessed surfaces. Pushed into the void. |

#### Backdrop Filters

| Context | Value | Notes |
|---|---|---|
| popover | `backdrop-filter: blur(16px) saturate(1.2)` | Slight saturation boost keeps navy tones alive through blur |
| modal | `backdrop-filter: blur(8px)` | Softer blur on the scrim behind modals |
| none | `backdrop-filter: none` | Default — no blur |

#### Separation Recipe

Glow-based emission + surface brightness stepping. The primary separation mechanism is the brightness difference between surface tones (`#080E1C` void → `#0B1426` navy → `#141E33` indigo → `#1A2844` pressed). Borders are visible but subtle (navy light at 20-30% opacity). On hover and focus, elements announce themselves by emitting faint gold glow at their edges — not from external light sources, but from within. The void background means no visible divider lines are needed between major sections; the infinite depth itself provides separation.

---

### Border System

#### Widths

| Name | Width | Usage |
|---|---|---|
| hairline | 0.5px | Standard border width. Thin lines on instrument panels. |
| default | 1px | Card borders, input borders, gold accent lines |
| medium | 1.5px | Strong emphasis, constellation lines (rare) |
| heavy | 2px | Focus ring width. Maximum border weight. |

#### Opacity Scale (on `border-base` Navy Light)

| Level | Opacity | Usage |
|---|---|---|
| ghost | 10% | Background grid, faintest structural lines |
| subtle | 20% | Panel edges, card outlines at rest |
| card | 30% | Standard card and content borders |
| hover | 45% | Hovered elements |
| focus | 60% | Focused inputs, active delineation |

#### Border Patterns

| Pattern | Width | Color/Opacity | Usage |
|---|---|---|---|
| ghost | 0.5px | border-base at 10% | Background grid structure |
| subtle | 0.5px | border-base at 20% | Default card and panel outlines |
| card | 0.5px | border-base at 30% | Prominent card borders |
| hover | 0.5px | border-base at 45% | Hovered cards, brightened edges |
| input | 1px | border-base at 20% | Form input borders at rest |
| input-hover | 1px | border-base at 35% | Input hover state |
| input-focus | 1px | gold at 40% | Input focus — gold emission replaces navy border |
| gold-accent | 1px | observatory gold at 50% | Active/selected element bottom border |
| gold-glow | 1px | observatory gold at 25% | Subtle gold accent on important dividers |
| constellation | 1px | chart teal at 40% | Data connection lines between points |

#### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(255, 215, 0, 0.50)` — observatory gold |
| Width | 2px solid |
| Offset | 2px |
| Implementation | `box-shadow: 0 0 0 2px #0B1426, 0 0 0 4px rgba(255,215,0,0.50)` |

The focus ring is gold, not blue. The inner ring uses the `bg` Deep Navy color to separate the gold indicator from the element, preventing visual bleed. On dark backgrounds, gold focus rings are more visible and harmonious than the default blue.

---

### Component States

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `#FFD700` (Observatory Gold), border none, color `#0B1426` (Void), radius 6px, h 34px, padding `0 18px`, font button (Instrument Sans, 13px, 600), shadow `0 0 8px rgba(255,215,0,0.15)` |
| Hover | bg `#FFE033` (lighter gold), shadow `0 0 12px rgba(255,215,0,0.3)` (glow intensifies) |
| Active | bg `#E8C400` (pressed gold), transform `scale(0.97)`, shadow `0 0 4px rgba(255,215,0,0.2)` (glow contracts) |
| Focus | gold focus ring appended |
| Disabled | opacity 0.4, pointer-events none, cursor not-allowed, shadow none (glow dies) |
| Transition | background 150ms gravitational, box-shadow 200ms gravitational, transform 100ms settle |

Primary buttons are the only elements with a solid gold background. They are the brightest objects in the viewport — stars among planets. The glow shadow reinforces the emission identity.

#### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border none, color `#8A96A8` (Pale Steel), radius 6px, size 34x34px |
| Hover | bg `rgba(255,215,0,0.06)` (gold whisper tint), color `#D4DCE8` (Silver Light) |
| Active | bg `rgba(255,215,0,0.12)`, transform `scale(0.97)` |
| Focus | gold focus ring |
| Disabled | opacity 0.4, pointer-events none |
| Transition | background 200ms gravitational, color 150ms gravitational |

Ghost buttons gain the faintest gold warmth on hover — like starlight catching a brass instrument surface.

#### Buttons (Secondary / Outlined)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid rgba(42,59,92,0.4)` (border-base at card opacity), color `#D4DCE8`, radius 6px, h 34px, padding `0 18px`, font button |
| Hover | border `1px solid rgba(42,59,92,0.6)`, bg `rgba(42,59,92,0.08)` |
| Active | border `1px solid rgba(42,59,92,0.7)`, transform `scale(0.97)` |
| Focus | gold focus ring |
| Disabled | opacity 0.4, pointer-events none |
| Transition | border-color 150ms gravitational, background 150ms gravitational |

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `#141E33` (Dark Indigo), border `1px solid rgba(42,59,92,0.20)`, radius 6px, h 40px, padding `0 14px`, shadow glow-input-rest, color `#D4DCE8`, placeholder `#5A6578`, caret-color `#FFD700` (gold caret) |
| Hover | border at 35% opacity, shadow glow-input-hover |
| Focus | border `1px solid rgba(255,215,0,0.4)` (gold border), shadow glow-input-focus, outline none |
| Disabled | opacity 0.4, bg `#0A0F1E`, pointer-events none |
| Transition | border-color 200ms gravitational, box-shadow 250ms gravitational |

The caret is gold — as the user types, they write with starlight.

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `#141E33`, radius 16px, border `0.5px solid rgba(42,59,92,0.20)`, shadow glow-card-rest, padding 18px |
| Hover | border at 30%, shadow glow-card-hover |
| Focus-within | border `0.5px solid rgba(255,215,0,0.20)`, shadow glow-card-focus |
| Transition | all 250ms gravitational |

#### Cards

| State | Properties |
|---|---|
| Rest | bg `#141E33`, border `0.5px solid rgba(42,59,92,0.20)`, radius 8px, shadow glow-card-rest, padding 20px |
| Hover | border at 30%, shadow glow-card-hover |
| Selected | border-bottom `1px solid rgba(255,215,0,0.4)` (gold accent line at base) |
| Transition | border-color 200ms gravitational, box-shadow 300ms gravitational |

Selected cards receive a gold bottom border — a constellation connector marking them as part of the active data set.

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `#8A96A8` (Pale Steel), radius 6px, h 34px, padding `6px 16px`, font bodySmall |
| Hover | bg `rgba(255,215,0,0.05)`, color `#D4DCE8` |
| Active (current) | bg `rgba(255,215,0,0.08)`, color `#FFD700`, font-weight 500 |
| Active press | transform `scale(0.985)` |
| Transition | color 100ms gravitational, background 150ms gravitational |

Active sidebar items glow with gold text — the selected star in the catalog.

#### Chips

| State | Properties |
|---|---|
| Rest | bg `#0B1426` (Deep Navy), border `0.5px solid rgba(42,59,92,0.20)`, radius 6px, h 30px, padding `0 12px`, font bodySmall, color `#8A96A8` |
| Hover | bg `#141E33`, border at 30%, color `#D4DCE8` |
| Selected | bg `rgba(255,215,0,0.08)`, border `0.5px solid rgba(255,215,0,0.25)`, color `#FFD700` |
| Active press | transform `scale(0.995)` |
| Transition | all 150ms gravitational |

#### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 38px |
| Track height | 20px |
| Track radius | 9999px |
| Track off bg | `rgba(42,59,92,0.35)` |
| Track off ring | `0.5px solid rgba(42,59,92,0.25)` |
| Track on bg | `#4A9B9B` (Chart Teal) |
| Track on ring | `0.5px solid rgba(74,155,155,0.4)` |
| Thumb | 16px `#D4DCE8` circle |
| Thumb shadow | `0 1px 3px rgba(0,0,0,0.3)` |
| Ring hover | thickens to 1px |
| Transition | 200ms gravitational |
| Focus-visible | gold focus ring |

The toggle track uses teal for "on" — data flow is active, the connection is live.

#### Slider

| Property | Value |
|---|---|
| Track height | 2px |
| Track color | `rgba(42,59,92,0.35)` (Navy Light at 35%) |
| Track filled | `rgba(255,215,0,0.7)` (gold thread) |
| Thumb | 14px circle, `#141E33` fill, `1.5px solid rgba(255,215,0,0.6)` border |
| Thumb hover | glow `0 0 6px rgba(255,215,0,0.3)` |
| Thumb active | scale(1.1) |
| Value display | JetBrains Mono, 11px, `#FFD700` |
| Transition | 150ms gravitational |

The slider track is a gold thread — a measurement line on a celestial chart being adjusted.

#### Data Table Row

| State | Properties |
|---|---|
| Rest | bg transparent, border-bottom `0.5px solid rgba(42,59,92,0.12)`, padding `10px 16px`, font bodySmall |
| Hover | bg `rgba(255,215,0,0.03)`, border-bottom at 20% |
| Selected | bg `rgba(255,215,0,0.06)`, border-left `2px solid rgba(255,215,0,0.4)` |
| Transition | background 100ms gravitational |

Table rows gain a faint gold tint on hover — barely perceptible, like starlight grazing a chart surface.

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| gravitational | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | Primary easing. Objects decelerate as if under gravitational pull — fast departure, long coast to rest. |
| orbital | `cubic-bezier(0.4, 0.0, 0.0, 1.0)` | Arcing entry paths. Slightly anticipatory start, smooth exponential settle. For panel entries and major reveals. |
| settle | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Standard settle. For elements coming to rest after press/release interactions. |
| drift | `cubic-bezier(0.0, 0.0, 0.1, 1.0)` | Ultra-slow deceleration. For ambient animations and long orbital cycles. Nearly linear start, very long tail. |
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Fallback ease-in-out. Used when no themed easing applies. |

This theme has NO spring/bounce animations. Celestial bodies do not bounce. Every motion decelerates smoothly under gravitational influence — fast departure, long coast, gentle landing.

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 100ms | gravitational | Quick stellar switch |
| Button hover bg | 150ms | gravitational | Gold glow intensifies promptly |
| Button active scale | 100ms | settle | Press feedback, snappy |
| Toggle slide | 200ms | gravitational | Thumb orbits to position |
| Chip hover | 150ms | gravitational | Background shifts |
| Card glow on hover | 300ms | gravitational | Glow bloom unfolds gradually |
| Input focus ring | 250ms | gravitational | Gold ring appears with deliberate glow |
| Constellation line draw | 600ms | orbital | Lines trace between data points |
| Panel open/close | 400ms | orbital | Sidebar, overlay panels arc in |
| Modal enter | 500ms | orbital | Scale + fade along arc trajectory |
| Modal exit | 300ms | gravitational | Faster exit than enter |
| Hero/page entry | 600ms | orbital | Content materializes with arc motion |
| Popover appear | 200ms | gravitational | Menu/dropdown entry |
| Data point appear | 400ms | gravitational | Gold glow bloom in |
| Star twinkle cycle | 4000-8000ms | drift | Ambient opacity oscillation per data point |
| Orbital ambient rotation | 3000-8000ms | drift | Slow ambient rotation of decorative elements |
| View transition | 400ms | orbital | Cross-fade between views |
| Toast notification | 300ms | gravitational | Slides in from top |

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Subtle mechanical click |
| Chips | 0.995 | Barely perceptible |
| Buttons | 0.97 | Standard instrument button press |
| Tabs | 0.96 | Slightly more pronounced panel switch |
| Cards (clickable) | 0.99 | Minimal on large surfaces |

Press scales are standard. The mechanical precision of instrument controls means press feedback should feel definitive but not dramatic.

---

### Overlays

#### Popover / Dropdown

| Property | Value |
|---|---|
| bg | `#1A2844` (Pressed Indigo — one step above surface) |
| border | `0.5px solid rgba(42,59,92,0.35)` |
| radius | 10px |
| shadow | glow-popover |
| backdrop-filter | `blur(16px) saturate(1.2)` |
| padding | 6px |
| z-index | 50 |
| min-width | 192px |
| max-width | 320px |
| Menu item | 6px 10px padding, radius 6px, h 34px, font bodySmall, color text-secondary |
| Menu item hover | bg `rgba(255,215,0,0.06)`, color text-primary |
| Separator | 1px solid `rgba(42,59,92,0.20)`, margin 4px 0 |
| Transition | 200ms gravitational |

Popover menus float above the observatory surface with a deep shadow that reinforces the void beneath. The faint gold tint on hover items is a starlight reflex.

#### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(0,0,0,0.55)` (deep space scrim) |
| Overlay backdrop-filter | `blur(8px)` |
| Content bg | `#141E33` (Dark Indigo) |
| Content border | `0.5px solid rgba(42,59,92,0.35)` |
| Content shadow | `0 8px 32px rgba(0,0,0,0.5), 0 0 1px rgba(255,215,0,0.06)` |
| Content radius | 12px |
| Content padding | 28px |
| Entry | opacity `0` to `1` + scale `0.96` to `1`, 500ms orbital |
| Exit | opacity `1` to `0` + scale `1` to `0.98`, 300ms gravitational |

The modal scrim is 55% opacity — dark enough that the underlying content fades into deep space, reinforcing the void identity. The faint gold edge glow on the modal container distinguishes it from the darkness.

#### Tooltip

| Property | Value |
|---|---|
| bg | `#1A2844` (Pressed Indigo) |
| color | `#D4DCE8` (Silver Light) |
| font | label size (11px, Instrument Sans, 500) |
| radius | 4px |
| padding | 5px 10px |
| shadow | `0 2px 8px rgba(0,0,0,0.35)` |
| border | `0.5px solid rgba(42,59,92,0.25)` |
| No arrow | Position via offset |
| Entry | opacity fade, 150ms gravitational |
| z-index | 60 |

Tooltips are compact instrument readouts — small, precise, data-forward.

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column. Standard width for dashboard content. |
| Narrow max-width | 640px | Focused content. Single-chart views, detailed readouts. |
| Wide max-width | 1200px | Dashboard grid layouts with multiple panels. |
| Sidebar width | 256px | Fixed sidebar. Instrument catalog / navigation panel. |
| Header height | 48px | Top bar. Compact — instrument panels waste no vertical space. |
| Spacing unit | 4px | Base multiplier. Tight grid for data density. |

#### Spacing Scale

4, 6, 8, 12, 16, 20, 24, 32, 48px

This is a moderate-density spacing scale. The smallest gap is 4px (half-unit for tight data labels). The most common gaps are 8-16px. Section breaks use 32-48px. The theme achieves breathing room through the dark void background, not through large spacing values.

| Context | Typical Gap | Notes |
|---|---|---|
| Between data labels | 4-6px | Tight instrument-panel spacing |
| Between form fields | 16px | Standard vertical rhythm |
| Between cards | 12-16px | Cards float in void with moderate gaps |
| Between sections | 32-48px | Major transitions |
| Card internal padding | 20px | Moderate internal space |
| Page edge padding | 24-32px | Content never touches viewport edges |
| Between sidebar items | 2px | Nearly touching — catalog density |
| Header to content | 16px | Minimal gap — transition to workspace |

#### Radius Scale

| Token | Value | Usage |
|---|---|---|
| none | 0px | Data table cells, grid items |
| sm | 4px | Badges, tooltip, small elements |
| md | 6px | Buttons, sidebar items, menu items, inputs |
| lg | 8px | Cards, panels |
| xl | 10px | Popovers, large panels |
| 2xl | 16px | Chat input card, modals (12px) |
| full | 9999px | Toggles, circular data points, avatars |

Radii are moderate. The aesthetic is precision instruments — not pill-shaped (too soft) and not sharp (too brutal). Gentle rounding that says "engineered, not stamped."

#### Density

Moderate to dense. This is a data-forward theme. Control panels pack information efficiently. The dark void background provides visual breathing room that compensates for tight element spacing — elements feel less crowded on dark backgrounds than on light ones at equivalent pixel density.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (256px) + content column (768px max) or wide dashboard grid (1200px). Multiple charts visible simultaneously.
- **md (768px):** Sidebar collapses to icon-only rail (48px) or overlay panel. Content column fills available width. Dashboard grids reflow from multi-column to 1-2 columns. Chart aspect ratios may shift.
- **sm (640px):** Single column. Sidebar becomes bottom navigation bar or hamburger overlay. Cards stack vertically. Data tables switch to card-based display for mobile readability. Touch targets expand to 44px minimum. Star field density reduces.

---

### Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring color | `rgba(255, 215, 0, 0.50)` (Observatory Gold) |
| Focus ring width | 2px solid |
| Focus ring offset | 2px (inner ring: `#0B1426` deep navy) |
| Focus ring implementation | `box-shadow: 0 0 0 2px #0B1426, 0 0 0 4px rgba(255,215,0,0.50)` |
| Disabled opacity | 0.4 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled shadow/glow | none (emission dies on disabled elements) |
| Selection bg | `rgba(255, 215, 0, 0.18)` |
| Selection color | `#D4DCE8` (Silver Light — text stays readable) |
| Scrollbar width | thin |
| Scrollbar thumb | `rgba(255, 215, 0, 0.25)` (gold-tinted) |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

**Contrast verification:**
- `text-primary` (#D4DCE8) on `surface` (#141E33): 9.1:1 — exceeds AAA
- `text-primary` (#D4DCE8) on `bg` (#0B1426): 11.2:1 — exceeds AAA
- `text-secondary` (#8A96A8) on `surface` (#141E33): 4.6:1 — meets AA
- `text-secondary` (#8A96A8) on `bg` (#0B1426): 5.5:1 — meets AA
- `text-muted` (#5A6578) on `surface` (#141E33): 2.6:1 — large text only (used for metadata/timestamps at label size). For stricter compliance, use `#6A7588` which achieves 3.2:1.
- `accent-primary` gold (#FFD700) on `bg` (#0B1426): 10.8:1 — exceeds AAA. Gold is highly readable on dark backgrounds.
- `text-onAccent` (#0B1426) on `accent-primary` (#FFD700): 10.8:1 — exceeds AAA. Dark text on gold buttons is fully accessible.

**Reduced motion:**

| Behavior | Value |
|---|---|
| Strategy | `reduced-distance` — spatial animations reduce distance by 75%, durations cap at 200ms |
| Star twinkle | Disabled (static opacity) |
| Constellation line draw | Lines appear instantly (no stroke-dashoffset animation) |
| Orbital entry paths | Collapse to simple opacity fade, 200ms |
| Gold glow bloom | Instant glow, no bloom animation |
| Data point reveal stagger | All points appear simultaneously, opacity fade only |
| Ambient orbital cycles | Disabled |
| Signature animations | All disabled or reduced to opacity-only |

---

### Visual Style

- **Material:** Instrument panel. Not plastic, not glass, not paper. The surfaces evoke dark anodized aluminum with a matte-satin finish. No reflections, no gloss, no transparency effects on surfaces. Cards are opaque panels mounted on the void.

- **Star Field Background:** The page background includes sparse, tiny white dots at random positions with varying opacity. This is the signature atmospheric effect — the observatory dome showing the sky beyond the instruments.

```css
.observatory-starfield {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
/* Stars rendered via JS as positioned elements or canvas dots:
   - 40-80 star points on desktop, 20-40 on mobile
   - Size: 1px (most) to 2px (few)
   - Opacity: 0.15 to 0.6 (varied)
   - Color: #FFFFFF
   - Optional: subtle twinkle animation on 10-15 stars (opacity 0.4→0.7→0.4, 4-8s cycle each)
*/
```

The star field is NOT a CSS gradient or image pattern. It must be randomly positioned to avoid repetition. Canvas rendering is preferred for performance; DOM elements are acceptable for fewer than 80 points.

- **Constellation Grid:** Optional background grid overlay on data-heavy views. Thin lines forming a coordinate system:

```css
.observatory-grid {
  background-image:
    linear-gradient(rgba(30,45,74,0.15) 1px, transparent 1px),
    linear-gradient(90deg, rgba(30,45,74,0.15) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
}
```

Grid lines use `gridLine` color at 15% opacity. Grid cell size is 48px (12x spacing unit). The grid is a coordinate reference system, not decoration — use it on chart backgrounds and data panels, not on navigation or content areas.

- **Grain:** None. The void is clean. No feTurbulence noise, no film grain. The darkness is smooth and infinite.
- **Gloss:** Matte-satin. Surfaces have a very subtle reflective quality (1-2% brightness boost on borders and edges) but no visible shine or highlights. Think dark anodized metal, not painted plastic.
- **Blend mode:** `normal` for all elements. `screen` for star field points if rendered as overlays. No multiply, no soft-light.
- **Shader bg:** False. No WebGL backgrounds. The star field is CSS or Canvas 2D.

---

### Signature Animations

#### 1. Star Appear (Gold Glow Bloom)

Data points and key elements fade into existence with a simultaneous gold glow bloom. The element goes from invisible to visible while a gold box-shadow expands from nothing to full glow radius. The effect is a star "turning on" in the void.

```css
@keyframes star-appear {
  0% {
    opacity: 0;
    box-shadow: 0 0 0px rgba(255,215,0,0);
  }
  40% {
    opacity: 0.8;
    box-shadow: 0 0 4px rgba(255,215,0,0.15);
  }
  100% {
    opacity: 1;
    box-shadow: 0 0 8px rgba(255,215,0,0.25);
  }
}
.star-enter {
  animation: star-appear 400ms cubic-bezier(0.0, 0.0, 0.2, 1.0) both;
}
```

Duration: 400ms, easing: gravitational. The glow leads the opacity slightly — the light arrives before the object fully materializes, as starlight would. Reduced motion: instant opacity, no glow animation.

#### 2. Constellation Draw

Connection lines between data points animate via `stroke-dashoffset`, tracing the path from origin to destination. The line "draws itself" as if a cartographer is mapping a new constellation with a gold-tipped pen.

```css
.constellation-line {
  stroke: #4A9B9B;
  stroke-width: 1px;
  stroke-dasharray: var(--line-length);
  stroke-dashoffset: var(--line-length);
  animation: draw-line 600ms cubic-bezier(0.4, 0.0, 0.0, 1.0) forwards;
}
@keyframes draw-line {
  to {
    stroke-dashoffset: 0;
  }
}
```

Duration: 600ms, easing: orbital. The `--line-length` CSS variable must be set to the path's `getTotalLength()` value via JavaScript. Lines draw from source to destination, not from center outward. Reduced motion: lines appear instantly (no stroke animation).

#### 3. Orbital Entry

Charts, panels, and major UI sections enter along a subtle arc trajectory rather than a straight slide. The element translates both horizontally and vertically along a curve, as if swinging into orbital position. This is achieved by combining `translateY` with a slight `translateX` shift and `opacity`.

```css
@keyframes orbital-entry {
  0% {
    opacity: 0;
    transform: translateY(24px) translateX(-8px) scale(0.97);
  }
  100% {
    opacity: 1;
    transform: translateY(0) translateX(0) scale(1);
  }
}
.orbit-enter {
  animation: orbital-entry 500ms cubic-bezier(0.4, 0.0, 0.0, 1.0) both;
}
```

Duration: 500ms, easing: orbital. The arc comes from the combination of different translateX and translateY distances with the ease curve creating a non-linear path. The slight scale-up from 0.97 adds depth — the element approaches from slightly farther away. Reduced motion: 200ms opacity-only fade.

#### 4. Twinkle

Idle data points have a very subtle opacity oscillation at random, different frequencies per point. This creates the effect of stars twinkling in the void — alive, but not demanding attention.

```css
@keyframes twinkle {
  0%, 100% { opacity: var(--star-base-opacity, 0.6); }
  50% { opacity: var(--star-peak-opacity, 0.95); }
}
.twinkle-star {
  animation: twinkle var(--twinkle-duration, 5s) cubic-bezier(0.0, 0.0, 0.1, 1.0) infinite;
  animation-delay: var(--twinkle-delay, 0s);
}
/* Apply varied durations per point:
   --twinkle-duration: random between 4s and 8s
   --twinkle-delay: random between 0s and 4s
   --star-base-opacity: random between 0.3 and 0.6
   --star-peak-opacity: random between 0.7 and 1.0
*/
```

Duration: 4-8s per cycle (varied), easing: drift. The randomized durations and delays prevent synchronization — stars twinkle independently. Only 10-15 stars should twinkle at any time; the rest remain static. Reduced motion: all twinkling disabled. Stars remain at their base opacity.

#### 5. Telescope Zoom

Drill-down interactions (clicking a data point to see detail, expanding a chart) zoom the canvas smoothly. The clicked element scales up while surrounding elements scale slightly down and fade, creating a depth-of-field effect like adjusting a telescope's focus.

```css
@keyframes telescope-zoom-in {
  0% {
    transform: scale(1);
    filter: blur(0px);
  }
  100% {
    transform: scale(1.08);
    filter: blur(0px);
  }
}
@keyframes telescope-bg-defocus {
  0% {
    transform: scale(1);
    opacity: 1;
    filter: blur(0px);
  }
  100% {
    transform: scale(0.96);
    opacity: 0.3;
    filter: blur(2px);
  }
}
.zoom-target {
  animation: telescope-zoom-in 500ms cubic-bezier(0.4, 0.0, 0.0, 1.0) forwards;
}
.zoom-context {
  animation: telescope-bg-defocus 500ms cubic-bezier(0.4, 0.0, 0.0, 1.0) forwards;
}
```

Duration: 500ms, easing: orbital. The background elements defocus (blur 2px + scale down + fade) while the target zooms slightly. The combined effect creates a parallax depth that mimics optical magnification. Reduced motion: target element highlights with gold border only, no zoom/scale/blur animation.

---

### Light Mode Variant

Midnight Observatory is natively dark. A light variant explores the aesthetic of **daylight observatory** — a sun-lit dome with brass instruments visible in warm natural light. The navy void becomes warm cream sky, the gold accents remain, and the data density is preserved.

#### Palette Swap

| Token | Dark Value | Light Value | Notes |
|---|---|---|---|
| page | `#080E1C` Void | `#F0EDE5` Parchment | Warm cream, like aged star chart paper |
| bg | `#0B1426` Deep Navy | `#F7F4EE` Linen | Primary surface |
| surface | `#141E33` Dark Indigo | `#FFFFFF` White | Cards, inputs |
| recessed | `#0A0F1E` Abyss | `#E8E4DB` Stone | Code blocks, inset areas |
| active | `#1A2844` Pressed Indigo | `#DDD8CE` Warm Grey | Active items |
| text-primary | `#D4DCE8` Silver Light | `#1A1A2E` Ink Navy | Dark navy text retains theme identity |
| text-secondary | `#8A96A8` Pale Steel | `#5A6070` Steel | Secondary labels |
| text-muted | `#5A6578` Twilight Grey | `#8A8E98` Slate | Metadata |
| text-onAccent | `#0B1426` Void | `#1A1A2E` Ink Navy | Text on gold |
| border-base | `#2A3B5C` Navy Light | `#C8C0B0` Warm Tan | Base border color |
| accent-primary | `#FFD700` Observatory Gold | `#C4960A` Aged Gold | Slightly darker gold for light bg contrast |
| accent-secondary | `#4A9B9B` Chart Teal | `#2E7A7A` Deep Teal | Darker teal for readability |
| accent-tertiary | `#C4767A` Nebula Rose | `#A85458` Deep Rose | Darker rose |

#### Light Mode Rules

- Elevation strategy shifts from glow-based to subtle-shadow-based. Cards get traditional `box-shadow` instead of inner glow.
- Gold no longer glows — it appears as solid lines and fills at reduced saturation. The emission identity is replaced by brass-instrument materiality.
- Star field background is removed. The background becomes a subtle warm texture or plain warm cream.
- Constellation grid lines become light navy (`rgba(26,26,46,0.08)`) on warm cream.
- Data points use filled circles with dark borders instead of glow effects.
- Focus ring gold darkens to `rgba(196,150,10,0.5)` for contrast on light surfaces.
- Shadows appear: cards get `0 1px 3px rgba(26,26,46,0.06)`, popovers get `0 4px 16px rgba(26,26,46,0.10)`.
- Typography remains identical — Instrument Sans, Albert Sans, JetBrains Mono.
- Border opacity scale reduces (subtle 10%, card 15%, hover 20%, focus 30%) because light backgrounds need less border emphasis.

---

### Mobile Notes

#### Effects to Disable
- Star field: reduce to 20-40 points maximum (performance). Disable twinkle animation entirely.
- Constellation line drawing animations: pre-render as static SVG paths. No `stroke-dashoffset` animation.
- Telescope zoom effect: replace with simple highlight (gold border flash). No blur filter animation.
- Background grid overlay: remove entirely on mobile. Grid lines at 15% opacity are invisible on small screens anyway.
- Backdrop-filter on popovers: remove `blur(16px)`. Keep solid background.

#### Adjustments
- Body text stays 15px minimum (dark backgrounds at mobile viewing distances need at least this).
- Card internal padding reduces from 20px to 16px.
- Section spacing reduces from 32-48px to 24-32px.
- Sidebar becomes bottom navigation bar with 5 max items, 48px height, icon-only (label on active).
- All interactive elements maintain minimum 44px touch target.
- Header height stays 48px.
- Popover max-width becomes 280px (viewport-constrained).
- Modal padding reduces from 28px to 20px. Radius reduces from 12px to 10px.
- Data tables switch to card-based display on screens narrower than 640px.
- Chart aspect ratios may change from landscape to portrait on mobile.
- Gold glow shadows are cheap — `box-shadow` with rgba is well-optimized on mobile GPUs.

#### Performance Notes
- Star field is the main performance concern. Canvas 2D rendering is strongly preferred over DOM elements on mobile. Cap at 30 points.
- Gold glow `box-shadow` effects are GPU-composited and inexpensive even at scale.
- The moderate animation durations (150-500ms) produce reasonable paint budgets.
- `will-change: transform, opacity` only during active animations, never permanent.
- Constellation line SVG paths should be pre-computed and cached. No runtime `getTotalLength()` calculations on mobile.
- Total concurrent animation budget on mobile: 2 simultaneous transitions maximum.
- Font loading: Instrument Sans, Albert Sans, and JetBrains Mono are moderate-size fonts (~100-200KB total). Use `font-display: swap` and preload the weights used above the fold (Instrument Sans 600, Albert Sans 400).

---

### Data Visualization

| Property | Value |
|---|---|
| Categorical palette | `#FFD700` (Gold), `#4A9B9B` (Teal), `#C4767A` (Rose), `#4A88C4` (Cool Blue), `#4CAF6E` (Signal Green) — 5 colors at perceptually balanced brightness on dark backgrounds |
| Sequential ramp | Single-hue gold: `rgba(255,215,0,0.15)` to `#FFD700` to `#B8980A` (muted-to-full-to-dark gold) |
| Diverging ramp | Teal to navy to rose: `#4A9B9B` to `#141E33` to `#C4767A` |
| Grid lines | Ghost: `border-base` at 10% opacity. Nearly invisible coordinate reference. |
| Max hues per chart | 3 (prefer 2: gold + teal as default pair) |
| Axis labels | Instrument Sans, 11px, uppercase, `#5A6578` (text-muted) with 0.06em tracking |
| Value labels | JetBrains Mono, 12px, `#D4DCE8` (text-primary), `tabular-nums` |
| Data point glow | `0 0 6px rgba(color, 0.3)` — every data point emits faint glow matching its series color |
| Tooltip data | JetBrains Mono for values, Instrument Sans for labels |
| Philosophy | Precise, glow-on-dark. Data points are stars; connections are constellations. Every chart should feel like a star chart projected on the dome. |

---

### Theme-Specific CSS Custom Properties

```css
:root[data-theme="midnight-observatory"] {
  /* Core surfaces */
  --page: #080E1C;
  --bg: #0B1426;
  --surface: #141E33;
  --recessed: #0A0F1E;
  --active: #1A2844;

  /* Text */
  --text-primary: #D4DCE8;
  --text-secondary: #8A96A8;
  --text-muted: #5A6578;
  --text-on-accent: #0B1426;

  /* Observatory gold system */
  --observatory-gold: #FFD700;
  --observatory-gold-glow: rgba(255, 215, 0, 0.25);
  --observatory-gold-glow-intense: rgba(255, 215, 0, 0.40);
  --observatory-gold-focus: rgba(255, 215, 0, 0.50);
  --observatory-gold-hover: rgba(255, 215, 0, 0.06);
  --observatory-gold-accent: rgba(255, 215, 0, 0.40);
  --observatory-gold-subtle: rgba(255, 215, 0, 0.08);

  /* Accents */
  --accent-primary: #FFD700;
  --accent-secondary: #4A9B9B;
  --accent-tertiary: #C4767A;

  /* Semantics */
  --success: #4CAF6E;
  --warning: #E8A830;
  --danger: #D14B4B;
  --info: #4A88C4;

  /* Borders */
  --border-base: #2A3B5C;
  --border-ghost: rgba(42, 59, 92, 0.10);
  --border-subtle: rgba(42, 59, 92, 0.20);
  --border-card: rgba(42, 59, 92, 0.30);
  --border-hover: rgba(42, 59, 92, 0.45);
  --border-focus: rgba(42, 59, 92, 0.60);

  /* Focus */
  --focus-ring: 0 0 0 2px var(--bg), 0 0 0 4px var(--observatory-gold-focus);

  /* Glow tokens */
  --glow-none: none;
  --glow-data: 0 0 8px rgba(255, 215, 0, 0.25);
  --glow-data-intense: 0 0 12px rgba(255, 215, 0, 0.4), 0 0 4px rgba(255, 215, 0, 0.6);
  --glow-card-rest: 0 1px 4px rgba(0, 0, 0, 0.2);
  --glow-card-hover: 0 2px 8px rgba(0, 0, 0, 0.25), inset 0 0 0 1px rgba(255, 215, 0, 0.04);
  --glow-card-focus: 0 2px 12px rgba(0, 0, 0, 0.3), 0 0 0 2px rgba(255, 215, 0, 0.25);
  --glow-input-rest: 0 1px 4px rgba(0, 0, 0, 0.15);
  --glow-input-hover: 0 2px 6px rgba(0, 0, 0, 0.2), inset 0 0 0 1px rgba(42, 59, 92, 0.3);
  --glow-input-focus: 0 2px 8px rgba(0, 0, 0, 0.25), 0 0 0 2px rgba(255, 215, 0, 0.4);
  --glow-popover: 0 4px 24px rgba(0, 0, 0, 0.5), 0 0 1px rgba(255, 215, 0, 0.06);
  --glow-inset: inset 0 1px 4px rgba(0, 0, 0, 0.3);

  /* Grid */
  --grid-line: #1E2D4A;

  /* Special */
  --star-white: #FFFFFF;
  --inline-code: #E8C84A;
  --selection-bg: rgba(255, 215, 0, 0.18);

  /* Motion */
  --ease-gravitational: cubic-bezier(0.0, 0.0, 0.2, 1.0);
  --ease-orbital: cubic-bezier(0.4, 0.0, 0.0, 1.0);
  --ease-settle: cubic-bezier(0.25, 0.1, 0.25, 1);
  --ease-drift: cubic-bezier(0.0, 0.0, 0.1, 1.0);
  --duration-flash: 100ms;
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-medium: 300ms;
  --duration-slow: 500ms;
  --duration-reveal: 600ms;

  /* Layout */
  --content-max-width: 768px;
  --narrow-max-width: 640px;
  --wide-max-width: 1200px;
  --sidebar-width: 256px;
  --header-height: 48px;
  --spacing-unit: 4px;

  /* Typography */
  --font-display: "Instrument Sans", "SF Pro Condensed", "Roboto Condensed", system-ui, sans-serif;
  --font-body: "Albert Sans", "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", "Cascadia Mono", "Consolas", ui-monospace, monospace;
}
```

---

### Implementation Checklist

- [ ] Google Fonts loaded: Instrument Sans (400, 500, 600, 700), Albert Sans (400, 500, italic 400), JetBrains Mono (400, 500)
- [ ] CSS custom properties defined for all color tokens including the gold system (`--observatory-gold`, `--observatory-gold-glow`, `--observatory-gold-focus`, etc.)
- [ ] Focus ring uses gold (`rgba(255,215,0,0.50)`) on all interactive elements, not browser default blue
- [ ] Gold caret color on text inputs (`caret-color: var(--observatory-gold)`)
- [ ] `-webkit-font-smoothing: antialiased` and `-moz-osx-font-smoothing: grayscale` on root element (critical for light-on-dark text)
- [ ] `text-wrap: balance` for headings, `pretty` for body text
- [ ] Font-display: swap on all font loads
- [ ] Star field background rendered (Canvas 2D preferred, DOM acceptable for <80 points)
- [ ] Star field point count: 40-80 on desktop, 20-40 on mobile
- [ ] Constellation grid overlay available for data views (48px grid, gridLine color at 15%)
- [ ] Border-radius applied: 6px default (buttons/inputs), 8px cards, 10px popovers, 12px modals
- [ ] Glow tokens applied per state: glow-card-rest at rest, glow-card-hover on hover, glow-card-focus on focus
- [ ] Border opacity system implemented: ghost/subtle/card/hover/focus at 10/20/30/45/60%
- [ ] Gold glow on data points: `box-shadow: 0 0 8px rgba(255,215,0,0.25)`
- [ ] Gold accent borders on selected/active elements (bottom or left, 1px at 40-50%)
- [ ] Input focus transitions from navy border to gold border
- [ ] No gold background fills except on primary CTA buttons
- [ ] Background page color `#080E1C` (Void), not pure `#000000`
- [ ] `prefers-reduced-motion` media query: twinkle disabled, constellation draw disabled, orbital entry collapses to opacity fade, glow bloom instant, durations cap at 200ms
- [ ] Scrollbar thumb uses gold tint (`rgba(255,215,0,0.25)`), transparent track
- [ ] Touch targets >= 44px on all interactive elements
- [ ] All transitions use gravitational or orbital easings as specified in motion map
- [ ] `::selection` styled with gold at 18% opacity
- [ ] `::placeholder` color matches `text-muted` token (#5A6578)
- [ ] Label text uses uppercase + 0.06em tracking (Instrument Sans identity)
- [ ] JetBrains Mono used for all data values with `font-variant-numeric: tabular-nums` and `font-feature-settings: "liga" 0`
- [ ] WCAG AA contrast verified for all text tokens on their target surfaces
- [ ] Mobile: star field reduced, twinkle disabled, constellation draw static, telescope zoom replaced with highlight
- [ ] No gradients on surfaces — void is flat, cards are flat
- [ ] No spring/bounce animations — all motion decelerates gravitationally
