# Midnight Observatory — Quick Reference

> Deep space meets scientific cartography — warm gold constellations projected on infinite navy, the hum of precise instruments.

**Schema:** v2 | **Mode:** dark (natively dark, glow-based) | **Full spec:** `full.md` (1019 lines)

## Color Tokens

| Token | Hex | Role |
|---|---|---|
| page | `#080E1C` | Deepest background. Infinite dark space beyond the dome. |
| bg | `#0B1426` | Primary surface background. The observatory wall. |
| surface | `#141E33` | Elevated cards, inputs, popovers. Instrument panel face. |
| recessed | `#0A0F1E` | Code blocks, inset areas. Deeper than page — a cutaway to void. |
| active | `#1A2844` | Active/pressed items, user bubbles. Indigo energized by interaction. |
| text-primary | `#D4DCE8` | Headings, body text. Bright enough for WCAG AA on all surfaces. |
| text-secondary | `#8A96A8` | Sidebar items, secondary labels. Dim starlight. |
| text-muted | `#5A6578` | Placeholders, timestamps, metadata. Faintest readable value. |
| text-onAccent | `#0B1426` | Dark text on gold-filled backgrounds (buttons, badges). |
| border-base | `#2A3B5C` | Base border color used at variable opacity. Star chart grid ink. |
| accent-primary | `#FFD700` | Primary data points, stars, CTA buttons, focus rings. Warm brass. |
| accent-secondary | `#4A9B9B` | Constellation lines, secondary data, connections. |
| accent-tertiary | `#C4767A` | Tertiary data series, occasional accents. Dusty rose. |
| success | `#4CAF6E` | Positive states. System operational. |
| warning | `#E8A830` | Caution states. Instrument warning. |
| danger | `#D14B4B` | Error states, critical alerts. Dying star. |
| info | `#4A88C4` | Informational states. Instrument readout blue. |
| inlineCode | `#E8C84A` | Code text within prose. Slightly muted gold. |
| toggleActive | `#4A9B9B` | Toggle/switch active track. Chart Teal — data flow is "on." |
| selection | `rgba(255, 215, 0, 0.18)` | `::selection` background. Gold at low opacity on dark. |
| starWhite | `#FFFFFF` | Pure white for individual data points, star markers. |
| gridLine | `#1E2D4A` | Background grid lines, coordinate system. |

## Font Stack

| Role | Family | Weight | Size | Line-Height |
|---|---|---|---|---|
| Display | Instrument Sans | 600 | 36px | 1.15 |
| Heading | Instrument Sans | 600 | 22px | 1.25 |
| Subheading | Instrument Sans | 500 | 17px | 1.35 |
| Body | Albert Sans | 400 | 15px | 1.55 |
| Body Small | Albert Sans | 400 | 13px | 1.45 |
| Button | Instrument Sans | 600 | 13px | 1.4 |
| Input | Albert Sans | 400 | 14px | 1.4 |
| Label | Instrument Sans | 500 | 11px | 1.3 |
| Code | JetBrains Mono | 400 | 13px | 1.5 |
| Caption | Albert Sans | 400 | 11px | 1.35 |

## Elevation Summary

**Strategy:** glow

Gold emission defines depth. Higher-importance elements glow more intensely. No traditional drop shadows — light is emitted from within, not cast from above.

| Token | Value |
|---|---|
| glow-none | `none` |
| glow-data | `0 0 8px rgba(255,215,0,0.25)` |
| glow-data-intense | `0 0 12px rgba(255,215,0,0.4), 0 0 4px rgba(255,215,0,0.6)` |
| glow-card-rest | `0 1px 4px rgba(0,0,0,0.2)` |
| glow-card-hover | `0 2px 8px rgba(0,0,0,0.25), inset 0 0 0 1px rgba(255,215,0,0.04)` |
| glow-card-focus | `0 2px 12px rgba(0,0,0,0.3), 0 0 0 2px rgba(255,215,0,0.25)` |
| glow-input-rest | `0 1px 4px rgba(0,0,0,0.15)` |
| glow-input-hover | `0 2px 6px rgba(0,0,0,0.2), inset 0 0 0 1px rgba(42,59,92,0.3)` |
| glow-input-focus | `0 2px 8px rgba(0,0,0,0.25), 0 0 0 2px rgba(255,215,0,0.4)` |
| glow-popover | `0 4px 24px rgba(0,0,0,0.5), 0 0 1px rgba(255,215,0,0.06)` |
| glow-inset | `inset 0 1px 4px rgba(0,0,0,0.3)` |

## Border System

**Base color:** `#2A3B5C` Navy Light (used at variable opacity)

**Focus ring:** `rgba(255, 215, 0, 0.50)` / 2px solid / 2px offset

**Implementation:** `box-shadow: 0 0 0 2px #0B1426, 0 0 0 4px rgba(255,215,0,0.50)`

**Opacity scale:**
- ghost: 10% (faintest grid lines)
- subtle: 20% (panel edges, card outlines at rest)
- card: 30% (default card borders)
- hover: 45% (hovered elements)
- focus: 60% (focused inputs)

**Widths:**
- hairline: 0.5px (standard instrument panel borders)
- default: 1px (card borders, input borders, gold accent lines)
- medium: 1.5px (constellation lines, rare emphasis)
- heavy: 2px (focus ring width)

## Motion Personality

**Primary easing:** `cubic-bezier(0.0, 0.0, 0.2, 1.0)` — gravitational

**Secondary easing:** `cubic-bezier(0.4, 0.0, 0.0, 1.0)` — orbital

**Duration range:** 100ms – 600ms (flash to reveal)

**Active press scale:** 0.985 (nav items), 0.995 (chips), 0.97 (buttons), 0.96 (tabs), 0.99 (cards)

**Reduced motion:** reduced-distance strategy — spatial animations reduce distance by 75%, durations cap at 200ms, all ambient cycles disabled

**Signature character:** Celestial bodies do not bounce. Every motion decelerates smoothly under gravitational influence — fast departure, long coast, gentle landing. No spring/bounce animations.

## Key Component Quick-Reference

### Primary Button
- **Rest:** bg `#FFD700` (Observatory Gold), color `#0B1426`, radius 6px, h 34px, padding `0 18px`, shadow `0 0 8px rgba(255,215,0,0.15)`
- **Hover:** bg `#FFE033`, shadow `0 0 12px rgba(255,215,0,0.3)` (glow intensifies)
- **Active:** bg `#E8C400`, transform `scale(0.97)`, shadow `0 0 4px rgba(255,215,0,0.2)`
- **Focus:** gold focus ring appended
- **Transition:** background 150ms gravitational, box-shadow 200ms gravitational, transform 100ms settle

### Text Input
- **Rest:** bg `#141E33`, border `1px solid rgba(42,59,92,0.20)`, radius 6px, h 40px, padding `0 14px`, shadow glow-input-rest, color `#D4DCE8`, placeholder `#5A6578`, caret-color `#FFD700`
- **Hover:** border at 35% opacity, shadow glow-input-hover
- **Focus:** border `1px solid rgba(255,215,0,0.4)` (gold border), shadow glow-input-focus
- **Transition:** border-color 200ms gravitational, box-shadow 250ms gravitational

### Card
- **Rest:** bg `#141E33`, border `0.5px solid rgba(42,59,92,0.20)`, radius 8px, shadow glow-card-rest, padding 20px
- **Hover:** border at 30%, shadow glow-card-hover (deep shadow + faint gold inner edge)
- **Selected:** border-bottom `1px solid rgba(255,215,0,0.4)` (gold accent line)
- **Transition:** border-color 200ms gravitational, box-shadow 300ms gravitational

### Sidebar Item
- **Rest:** bg transparent, color `#8A96A8`, radius 6px, h 34px, padding `6px 16px`
- **Hover:** bg `rgba(255,215,0,0.05)`, color `#D4DCE8`
- **Active:** bg `rgba(255,215,0,0.08)`, color `#FFD700`, font-weight 500
- **Transition:** color 100ms gravitational, background 150ms gravitational

### Toggle/Switch
- **Track:** 38px × 20px, radius 9999px
- **Track off:** bg `rgba(42,59,92,0.35)`, ring `0.5px solid rgba(42,59,92,0.25)`
- **Track on:** bg `#4A9B9B` (Chart Teal), ring `0.5px solid rgba(74,155,155,0.4)`
- **Thumb:** 16px `#D4DCE8` circle, shadow `0 1px 3px rgba(0,0,0,0.3)`
- **Transition:** 200ms gravitational

## Section Index for full.md

| Section | Lines | What's There |
|---|---|---|
| Identity & Philosophy | 36–57 | World-building, decision principle, emission-on-void identity, anti-patterns |
| Color System | 58–140 | Palette table (17 tokens), gold emission system, opacity scale, color rules |
| Typography Matrix | 141–184 | 9 role specs, typographic decisions, font loading, fallback chains |
| Elevation System | 185–230 | Glow strategy, surface hierarchy, shadow/glow tokens, backdrop filters, separation recipe |
| Border System | 231–279 | Widths, opacity scale, border patterns, gold focus ring implementation |
| Component States | 280–419 | Buttons (primary/ghost/secondary), inputs, chat card, cards, sidebar items, chips, toggle, slider, table rows |
| Motion Map | 420–470 | 4 custom easings (gravitational, orbital, settle, drift), duration×easing×component table, active press scales |
| Overlays | 471–527 | Popover/dropdown, modal, tooltip specs with gold accent details |
| Layout Tokens | 528–581 | Content widths, spacing scale (4–48px), radius scale, density (moderate-dense), responsive notes |
| Accessibility Tokens | 582–625 | Focus ring, disabled states, selection, scrollbar, contrast verification, reduced motion strategy |
| Visual Style | 626–670 | Material (instrument panel), star field background (canvas implementation), constellation grid, grain (none), blend modes |
| Signature Animations | 671–803 | Star Appear (gold glow bloom), Constellation Draw, Orbital Entry, Twinkle, Telescope Zoom — all with code snippets |
| Light Mode Variant | 804–839 | Palette swap table (13 tokens), light mode rules (glow→shadow, star field removed) |
| Mobile Notes | 840–872 | Effects to disable, adjustments, performance notes (star field cap, animation budgets) |
| Data Visualization | 873–889 | Categorical palette (5 colors), sequential/diverging ramps, grid lines, axis labels, data point glow philosophy |
| CSS Custom Properties | 890–987 | Complete CSS variable definitions for all tokens |
| Implementation Checklist | 988–1019 | 32 checklist items covering fonts, glow tokens, border system, animations, accessibility |

## Philosophy

"When in doubt, ask: would this look right projected on the dome of a planetarium? If it breaks the darkness, dim it. If it lacks precision, tighten it. If it feels decorative rather than instrumental, remove it."

## Gold Emission System

Gold is the soul of this theme. It represents data, focus, navigation, and primary importance. Usage:
- **Data points:** Small filled circles (4-8px), 100% fill + glow shadow
- **Focus rings:** 2px ring at 60%
- **Primary CTA buttons:** Gold fill at 100% (only button type with gold background)
- **Active borders:** 1px bottom/left at 50%
- **Hover tint:** Background tint at 6-10%
- **Anti-patterns:** No gold card backgrounds, no gold gradients, no gold on >15% viewport area

## Visual Signature

**Emission on void.** Light sources against deep space. No drop shadows, no ambient light. Data and interactive elements emit their own glow, like stars and instrument panels in darkness. The void background (`#080E1C`) is infinite — no floor, no edge, no gradient. Cards are dark indigo islands defined by subtle borders and, on interaction, inner glow. Star field background (40-80 points on desktop, Canvas 2D preferred) with optional twinkle animation on 10-15 stars. Constellation grid overlay for data views (48px grid, `#1E2D4A` at 15%). No grain, matte-satin gloss, normal blend mode (screen for star overlays only).
