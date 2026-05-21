# Editorial Calm — Quick Reference

> Warm editorial matte -- the Anthropic aesthetic. A beautifully typeset magazine spread in a sunlit room.

**Schema:** v2 | **Mode:** dual (Canvas + Dashboard) | **Full spec:** `full.md` (760 lines)

## Color Tokens

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
| inlineCode | -- | `#B85C3A` | -- | Code text within prose -- darker terracotta, reads as "different register." |
| toggleActive | -- | `#2C84DB` | -- | Toggle/switch active track. Blue, distinct from terracotta accent. |
| selection | -- | `rgba(217, 119, 87, 0.18)` | -- | `::selection` background. Terracotta at 18% opacity. |
| alwaysBlack | -- | `#000000` | -- | Shadow base (mode-independent) |
| alwaysWhite | -- | `#FFFFFF` | -- | On-dark emergencies only (mode-independent) |

## Font Stack

| Role | Family | Weight | Size | Line-Height |
|---|---|---|---|---|
| Display | Plus Jakarta Sans | 290 | 38px | 1.2 (45.6px) |
| Heading | Plus Jakarta Sans | 460 | 24px | 1.3 (31.2px) |
| Subheading | Plus Jakarta Sans | 500 | 18px | 1.35 (24.3px) |
| Body | DM Sans | 400 | 16px | 1.5 (24px) |
| Body Small | DM Sans | 400 | 14px | 1.4 (19.6px) |
| Button | DM Sans | 460 | 14px | 1.4 (19.6px) |
| Input | DM Sans | 430 | 14px | 1.4 (19.6px) |
| Label | DM Sans | 400 | 12px | 1.33 (16px) |
| Code | Geist Mono | 360 | 0.9em (14.4px) | 1.5 (21.6px) |
| Caption | DM Sans | 400 | 12px | 1.33 (16px) |

## Elevation Summary

**Strategy:** Surface-shifts + subtle composite shadows

| Token | Value |
|---|---|
| shadow-sm | `0 1px 2px rgba(44, 41, 37, 0.04)` |
| shadow-md | `0 4px 6px -1px rgba(44, 41, 37, 0.06), 0 2px 4px -2px rgba(44, 41, 37, 0.04)` |
| shadow-input-rest | `0 4px 20px rgba(44, 41, 37, 0.03), 0 0 0 0.5px rgba(196, 186, 168, 0.25)` |
| shadow-input-focus | `0 4px 20px rgba(44, 41, 37, 0.06), 0 0 0 0.5px rgba(196, 186, 168, 0.30)` |
| shadow-popover | `0 2px 8px rgba(44, 41, 37, 0.12)` |

## Border System

**Base color:** `#C4BAA8` (Sand Veil) at variable opacity
**Focus ring:** `rgba(116, 171, 226, 0.56)` / 2px solid / offset 2px

## Motion Personality

**Primary easing:** `cubic-bezier(0.4, 0, 0.2, 1)`
**Duration range:** 75ms – 500ms
**Active press scale:** 0.97 (buttons), 0.985 (nav), 0.995 (chips)
**Reduced motion:** reduced-distance (opacity fade only, no translateY)

## Key Component Quick-Reference

### Primary Button
- Rest: bg `transparent`, text `#2C2925`, border `0.5px rgba(196,186,168,0.30)`, radius `6px`
- Hover: bg `#EDE8DF`, border `0.5px rgba(196,186,168,0.30)`
- Focus: ring `rgba(116,171,226,0.56)` 2px offset 2px

### Text Input
- Rest: bg `#FAF8F4`, border `1px rgba(196,186,168,0.15)`, radius `9.6px`
- Hover: border `1px rgba(196,186,168,0.30)`
- Focus: border `1px rgba(196,186,168,0.30)`, ring `rgba(116,171,226,0.56)` 2px offset 2px

### Card
- Rest: bg `#FAF8F4`, border `0.5px rgba(196,186,168,0.25)`, shadow `shadow-sm`, radius `8px`
- Hover: border `0.5px rgba(196,186,168,0.30)`, shadow `shadow-md`

## Section Index for full.md

Use these line ranges with offset/limit to read specific sections without loading the entire file:

| Section | Lines | What's There |
|---|---|---|
| Identity & Philosophy | 36-55 | Theme world, decision principle, anti-patterns |
| Color System | 56-117 | All color tokens, opacity system, semantic colors, color rules |
| Typography Matrix | 118-165 | 10 roles × 6 dimensions, variable font specs, font loading |
| Elevation System | 166-211 | Shadow tokens, surface hierarchy, backdrop filters, separation recipe |
| Border System | 212-250 | Base color, widths/patterns, opacity scale, focus ring |
| Component States | 251-381 | Buttons, inputs, cards, sidebar items, chips, toggles, user bubble |
| Motion Map | 382-433 | Easings, duration×easing×component, active press scale, reduced motion |
| Overlays | 434-486 | Popover/dropdown, modal, tooltip specs |
| Layout Tokens | 487-536 | Content widths, spacing scale, density, responsive breakpoints |
| Accessibility Tokens | 537-564 | Focus ring, disabled state, selection, scrollbar, touch targets |
| Visual Style | 565-616 | Material (grain, gloss), Canvas/Dashboard rendering, micro-grid |
| Signature Animations | 617-669 | Watercolor Bleed, Editorial Stagger, Thermal Shift, Breath Cycle, Settle Drift |
| Dark Mode Variant | 670-723 | Complete palette swap, dark mode rules, shadow adjustments |
| Data Visualization | 724-737 | Categorical palette, sequential ramp, diverging ramp, grid style |
| Mobile Notes | 738-764 | Effects to disable, sizing adjustments, performance notes |
| Implementation Checklist | 765-786 | 18 implementation checkpoints |
