# Ethereal Porcelain — Quick Reference

> Cool gallery neutrals with subsurface scattering -- surfaces glow faintly from within, like porcelain held to light.

**Schema:** v2 | **Mode:** light-native | **Full spec:** `full.md` (979 lines)

## Color Tokens

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Gallery Slate | `#E4E1DC` | Deepest background -- the gallery wall |
| bg | Cool Linen | `#ECEAE6` | Primary surface |
| surface | Porcelain | `#F5F3F0` | Cards, inputs, elevated surfaces |
| recessed | Dove Grey | `#E0DDD8` | Code blocks, inset areas |
| active | Ash | `#D8D5CF` | Active/pressed states, selected items |
| text-primary | Graphite | `#2C2C2E` | Headings, body text |
| text-secondary | Pewter | `#6B6B70` | Sidebar items, secondary labels |
| text-muted | Silver | `#9A9A9E` | Placeholders, timestamps, metadata |
| text-onAccent | Porcelain White | `#FAF9F7` | Text on accent backgrounds |
| border-base | Cool Veil | `#B8B5AE` | Base border (used at variable opacity) |
| accent-primary | Antique Gold | `#B8A88A` | Gallery-frame gold, CTA, highlights |
| accent-secondary | Steel Blue | `#7A8B9A` | Links, secondary actions |
| accent-rgb | -- | `184, 168, 138` | RGB decomposition for subsurface glow |
| success | Celadon | `#5A8A6A` | Positive states |
| warning | Aged Amber | `#A08040` | Caution states |
| danger | Muted Rose | `#B85A5A` | Error states |
| info | Slate Blue | `#5B7FA5` | Informational states |
| inlineCode | -- | `#8A7A5A` | Code text within prose |
| toggleActive | -- | `#5B7FA5` | Toggle/switch active track |
| selection | -- | `rgba(184, 168, 138, 0.16)` | `::selection` background |
| subsurfaceGlow | -- | `rgba(184, 168, 138, 0.04)` | Base inner glow color |
| alwaysBlack | -- | `#000000` | Shadow base (mode-independent) |
| alwaysWhite | -- | `#FFFFFF` | On-dark emergencies only |

## Font Stack

| Role | Family | Weight | Size | Line-Height |
|---|---|---|---|---|
| Display | DM Serif Display | 400 | 40px | 1.15 (46px) |
| Heading | DM Serif Display | 400 | 26px | 1.25 (32.5px) |
| Subheading | Satoshi | 700 | 18px | 1.35 (24.3px) |
| Body | Satoshi | 400 | 16px | 1.6 (25.6px) |
| Body Small | Satoshi | 400 | 14px | 1.45 (20.3px) |
| Button | Satoshi | 500 | 14px | 1.4 (19.6px) |
| Input | Satoshi | 400 | 14px | 1.4 (19.6px) |
| Label | Satoshi | 500 | 11px | 1.33 (14.6px) |
| Code | Fira Code | 400 | 0.9em | 1.5 (21.6px) |
| Caption | Satoshi | 400 | 12px | 1.33 (16px) |

## Elevation Summary

**Strategy:** Subsurface-glow + subtle composite shadows

| Token | Value |
|---|---|
| shadow-sm | `0 1px 2px rgba(44, 44, 46, 0.04)` |
| shadow-md | `0 4px 8px -2px rgba(44, 44, 46, 0.06), 0 2px 4px -2px rgba(44, 44, 46, 0.03)` |
| shadow-card | `0 2px 12px rgba(44, 44, 46, 0.03), 0 0 0 0.5px rgba(184, 181, 174, 0.20)` |
| shadow-input | `0 2px 12px rgba(44, 44, 46, 0.03), 0 0 0 0.5px rgba(184, 181, 174, 0.20)` |
| shadow-input-focus | `0 4px 16px rgba(44, 44, 46, 0.07), 0 0 0 0.5px rgba(184, 181, 174, 0.28)` |
| shadow-popover | `0 4px 16px rgba(44, 44, 46, 0.10), 0 1px 4px rgba(44, 44, 46, 0.06)` |
| glow-rest | `inset 0 1px 4px rgba(184, 168, 138, 0.04), inset 0 -1px 4px rgba(184, 168, 138, 0.02)` |
| glow-hover | `inset 0 1px 8px rgba(184, 168, 138, 0.06), inset 0 -1px 6px rgba(184, 168, 138, 0.03)` |
| glow-active | `inset 0 1px 12px rgba(184, 168, 138, 0.08), inset 0 -1px 8px rgba(184, 168, 138, 0.04)` |

## Border System

**Base color:** `#B8B5AE` (Cool Veil) + variable opacity

**Focus ring:** `rgba(122, 139, 154, 0.50)` / 2px solid / 2px offset

| Pattern | Width | Opacity | Usage |
|---|---|---|---|
| subtle | 0.5px | 12% | Sidebar edges, hairlines |
| card | 0.5px | 20% | Card borders |
| hover | 0.5px | 28% | Hover states |
| input | 1px | 12% | Form input rest |
| input-hover | 1px | 28% | Input hover |

## Motion Personality

**Primary easing:** `cubic-bezier(0.25, 0.1, 0.25, 1.0)` (gallery-ease)

**Duration range:** 150ms – 800ms

**Active press scale:** 0.975 (buttons), 0.985 (nav), 0.995 (chips)

**Reduced motion:** fade-only (all spatial movement disabled)

## Key Component Quick-Reference

### Primary Button
- **Rest:** bg transparent, border `rgba(184, 181, 174, 0.28)`, color `#2C2C2E`, radius 6px, h 36px
- **Hover:** bg `#E0DDD8`, border unchanged
- **Focus:** outline `2px solid rgba(122, 139, 154, 0.50)`, offset 2px

### Text Input
- **Rest:** bg `#F5F3F0`, border `1px solid rgba(184, 181, 174, 0.12)`, shadow glow-rest, radius 8px, h 44px
- **Hover:** border `rgba(184, 181, 174, 0.28)`, shadow glow-hover
- **Focus:** outline steel-blue ring, shadow glow-active

### Card
- **Rest:** bg `#F5F3F0`, border `0.5px solid rgba(184, 181, 174, 0.20)`, shadow shadow-card + glow-rest, radius 10px
- **Hover:** border `rgba(184, 181, 174, 0.28)`, shadow shadow-card-hover + glow-hover
- **Transition:** 400ms gallery-ease

## Section Index for full.md

| Section | Lines | What's There |
|---|---|---|
| Identity & Philosophy | 36-56 | Gallery aesthetic, cool-warm tension, decision principle |
| Color System | 57-119 | Palette (17 tokens), special colors, opacity system, color rules |
| Typography Matrix | 120-167 | Font families, 10 role specs, font loading, family switch boundary |
| Elevation System | 168-278 | Strategy, surface hierarchy, shadow tokens, subsurface scattering tokens, CSS implementation |
| Border System | 279-317 | Base color, widths/patterns, focus ring, opacity scale |
| Component States | 318-454 | Buttons (3 types), inputs, cards, sidebar items, chips, toggle, user bubble |
| Motion Map | 455-509 | Easings (6 types), duration×easing×component map, active press scale, reduced motion |
| Overlays | 510-565 | Popover/dropdown, modal, tooltip specs |
| Layout Tokens | 566-615 | Content widths, spacing scale, density (spacious), responsive notes |
| Accessibility Tokens | 616-649 | Focus ring, disabled, selection, scrollbar, touch targets, contrast verification |
| Visual Style | 650-746 | Material (grain, gloss, blend mode), subsurface scattering technique (3 levels), rendering guidelines |
| Signature Animations | 747-882 | 5 animations: Porcelain Glow Pulse, Gallery Reveal, Kiln Glow, Light Shift, Vessel Turn |
| Dark Mode Variant | 883-912 | Suggested palette swaps, dark mode rules (directional guidance) |
| Data Visualization | 913-926 | Categorical/sequential/diverging palettes, grid style, philosophy (annotated) |
| Mobile Notes | 927-954 | Effects to disable, sizing adjustments, performance notes |
| Implementation Checklist | 955-979 | 25 verification items for complete theme implementation |
