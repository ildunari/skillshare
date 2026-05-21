# Iridescent — Quick Reference
> Futuristic chrome surfaces refracting light through conic-gradient halos — where holographic daydream meets brushed metal.

**Schema:** v2 | **Modes:** Holographic (cool prismatic) / Chrome (warm metallic) | **Full spec:** `full.md` (1071 lines)

---

## Color Tokens — Holographic Mode

| Token | Hex | Role |
|---|---|---|
| page | `#F5F5F8` | Deepest background. Cool near-white with faint blue undertone. |
| bg | `#FAFAFC` | Primary surface background. Slightly elevated from page. |
| surface | `#FFFFFF` | Elevated cards, inputs, popovers. Pure white for maximum prismatic contrast. |
| recessed | `#EEEEF2` | Code blocks, inset areas. Cool grey with lavender cast. |
| active | `#E8E8F0` | Active/pressed items, user bubbles. Deeper cool grey. |
| text-primary | `#1A1A2E` | Headings, body text. Deep navy-black for contrast. |
| text-secondary | `#5A5A7A` | Sidebar items, secondary labels. Muted indigo-grey. |
| text-muted | `#9494AC` | Placeholders, timestamps, metadata. Soft lavender-grey. |
| text-onAccent | `#FFFFFF` | Text on accent-colored backgrounds. |
| border-base | `#C0C0D0` | Base border color. Cool silver used at variable opacity. |
| accent-primary | `#7B68EE` | Brand accent, primary CTA. Medium slate blue — center of prismatic spectrum. |
| accent-secondary | `#00D4FF` | Secondary accent for links, informational highlights. Cool end of spectrum. |
| success | `#2DD4A8` | Positive states. Cooler green that harmonizes with prismatic palette. |
| warning | `#FFB020` | Caution states. Warm amber, complementary warm note. |
| danger | `#FF5A7E` | Error states, destructive actions. Pink-red, part of prismatic sweep. |
| info | `#38B6FF` | Info states. Bright sky blue. |
| inlineCode | `#7B68EE` | Code text within prose. Accent-aligned purple. |
| toggleActive | `#2DD4A8` | Toggle/switch active track. |
| selection | `rgba(123,104,238,0.18)` | ::selection background. Accent at 18%. |

## Color Tokens — Chrome Mode

| Token | Hex | Role |
|---|---|---|
| page | `#F3F2EF` | Deepest background. Warm greige. Brushed aluminum under tungsten. |
| bg | `#F9F8F6` | Primary surface background. Warm off-white. |
| surface | `#FFFFFF` | Elevated cards, inputs, popovers. Pure white for specular highlight contrast. |
| recessed | `#EAEAE6` | Code blocks, inset areas. Warm grey. |
| active | `#E2E1DC` | Active/pressed items. Deeper warm grey with golden cast. |
| text-primary | `#1E1E1E` | Headings, body text. True near-black. |
| text-secondary | `#6B6B65` | Sidebar items, secondary labels. Warm grey. |
| text-muted | `#A0A098` | Placeholders, timestamps, metadata. Silvered warm grey. |
| text-onAccent | `#FFFFFF` | Text on accent-colored backgrounds. |
| border-base | `#C5C5BD` | Base border color. Warm silver at variable opacity. |
| accent-primary | `#8B5CF6` | Brand accent, primary CTA. Slightly warmer violet than holographic. |
| accent-secondary | `#D4A853` | Secondary accent. Brushed gold for luxury warmth. |
| success | `#22C55E` | Positive states. Classic green. |
| warning | `#F59E0B` | Caution states. |
| danger | `#EF4444` | Error states. |
| info | `#6366F1` | Info states. Indigo-blue with metallic warmth. |
| inlineCode | `#8B5CF6` | Code text within prose. Accent-aligned purple. |
| toggleActive | `#22C55E` | Toggle/switch active track. |
| selection | `rgba(139,92,246,0.18)` | ::selection background. Accent at 18%. |

**Opacity System:** Borders use base border color at 12% (subtle), 20% (card), 30% (hover), 45% (focus). Conic gradients replace borders on hover/focus for interactive elements.

---

## Typography — All 9 Roles

### Holographic Mode

| Role | Family | Size | Weight | Line-height | Spacing | Usage |
|---|---|---|---|---|---|---|
| Display | Sora | 40px | 700 | 1.1 | -0.03em | Hero titles, page names, product names |
| Heading | Sora | 24px | 600 | 1.25 | -0.02em | Section titles, card headers |
| Subheading | Sora | 18px | 500 | 1.35 | -0.01em | Subsection titles, feature labels |
| Body | Manrope | 16px | 400 | 1.55 | -0.005em | Primary reading text, descriptions |
| Body Small | Manrope | 14px | 400 | 1.45 | normal | Sidebar items, form labels, secondary text |
| Button | Sora | 14px | 500 | 1.4 | 0.01em | Button labels, CTAs |
| Input | Manrope | 14px | 400 | 1.4 | normal | Form input text |
| Label | Manrope | 12px | 500 | 1.33 | 0.04em | Section labels, metadata, timestamps |
| Code | Fira Code | 0.9em | 400 | 1.5 | normal | Inline code, code blocks. Ligatures enabled. |
| Caption | Manrope | 12px | 400 | 1.33 | normal | Disclaimers, footnotes |

### Chrome Mode

| Role | Family | Size | Weight | Line-height | Spacing | Usage |
|---|---|---|---|---|---|---|
| Display | Sora | 40px | 800 | 1.1 | -0.03em | Hero titles. Extra bold for metallic weight. |
| Heading | Sora | 24px | 700 | 1.25 | -0.02em | Section titles |
| Subheading | Sora | 18px | 600 | 1.35 | -0.01em | Subsection titles |
| Body | Manrope | 16px | 400 | 1.55 | -0.005em | Primary reading text |
| Body Small | Manrope | 14px | 400 | 1.45 | normal | Sidebar items, form labels |
| Button | Sora | 14px | 600 | 1.4 | 0.015em | Button labels. Heavier for metallic authority. |
| Input | Manrope | 14px | 400 | 1.4 | normal | Form input text |
| Label | Manrope | 12px | 500 | 1.33 | 0.04em | Section labels, metadata |
| Code | Fira Code | 0.9em | 400 | 1.5 | normal | Inline code, code blocks |
| Caption | Manrope | 12px | 400 | 1.33 | normal | Disclaimers, footnotes |

**Font Loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@100..800&family=Manrope:wght@200..800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&display=swap" rel="stylesheet">
```

---

## Elevation — Layered Shadows with Metallic Undertones

**Strategy:** `layered-shadows` with mode-specific tints

### Key Shadow Tokens — Holographic Mode
- **shadow-sm:** `0 1px 2px rgba(123,104,238,0.04), 0 1px 3px rgba(0,0,0,0.03)` — Small elements, badges
- **shadow-card:** `0 1px 2px rgba(123,104,238,0.06), 0 4px 12px rgba(123,104,238,0.04), 0 0 0 1px rgba(192,192,208,0.12)` — Card rest
- **shadow-input-focus:** `0 2px 6px rgba(123,104,238,0.08), 0 6px 20px rgba(0,0,0,0.05), 0 0 0 2px rgba(123,104,238,0.35)` — Input focus
- **shadow-popover:** `0 2px 8px rgba(123,104,238,0.08), 0 12px 32px rgba(0,0,0,0.08), 0 0 0 1px rgba(192,192,208,0.20)` — Menus, dropdowns
- **shadow-hero:** `0 4px 12px rgba(123,104,238,0.10), 0 16px 48px rgba(123,104,238,0.08), 0 32px 64px rgba(0,0,0,0.04)` — Hero showcase

### Key Shadow Tokens — Chrome Mode
- **shadow-sm:** `0 1px 2px rgba(120,110,90,0.06), 0 1px 3px rgba(0,0,0,0.03)` — Small elements
- **shadow-card:** `0 1px 2px rgba(120,110,90,0.08), 0 4px 12px rgba(120,110,90,0.05), 0 0 0 1px rgba(197,197,189,0.15)` — Card rest
- **shadow-input-focus:** `0 2px 6px rgba(120,110,90,0.10), 0 6px 20px rgba(0,0,0,0.05), 0 0 0 2px rgba(139,92,246,0.30)` — Input focus
- **shadow-popover:** `0 2px 8px rgba(120,110,90,0.10), 0 12px 32px rgba(0,0,0,0.08), 0 0 0 1px rgba(197,197,189,0.20)` — Menus, dropdowns
- **shadow-hero:** `0 4px 12px rgba(120,110,90,0.12), 0 16px 48px rgba(120,110,90,0.08), 0 32px 64px rgba(0,0,0,0.04)` — Hero showcase

**Separation Recipe:** Tint-step backgrounds (page → bg → surface) + tinted layered shadows + conic-gradient border activation on interaction. No visible dividers. No backdrop-filter blur. Depth from shadow color and gradient borders.

---

## Border System

**Base Color:** `border-base` token (mode-dependent) at variable opacity

### Focus Ring
- **Holographic:** `rgba(123, 104, 238, 0.45)`, 2px solid, 2px offset, white inner ring
- **Chrome:** `rgba(139, 92, 246, 0.40)`, 2px solid, 2px offset, white inner ring

### Conic Gradient Activation
Static borders become conic gradients on hover:
- **Holographic:** 7-stop rainbow loop: `#ff6b6b, #ffa500, #ffd700, #7fff00, #00d4ff, #7b68ee, #ff6b9d, #ff6b6b`
- **Chrome:** 6-stop silver sweep: `#A0A0A0, #C8C8C8, #F0F0F0, #FFFFFF, #D0D0D0, #A0A0A0`

---

## Motion — Spring-Feel Easing

### Key Easings
- **default:** `cubic-bezier(0.4, 0, 0.2, 1)` — Standard ease-in-out
- **spring-out:** `cubic-bezier(0.22, 0.68, 0, 1.12)` — Signature easing, magnetic/spring snap
- **spring-heavy:** `cubic-bezier(0.16, 0.84, 0.1, 1.18)` — Heavier spring for hero elements
- **out-quart:** `cubic-bezier(0.165, 0.85, 0.45, 1)` — Snappy deceleration
- **metallic-snap:** `cubic-bezier(0.34, 1.56, 0.64, 1)` — Sharp overshoot, metal click feel

### Duration Range
80ms (sidebar item color) → 8000ms (hero conic rotation)

### Active Press Scale
- Nav items: `0.985` | Chips: `0.98` | Buttons: `0.96` | Tabs: `0.95`

### Reduced Motion
Conic rotation pauses (static angle at 45deg), spring easings replaced with standard ease, specular animations disabled.

---

## Component Quick-Reference

### Primary Button
- **Rest:** bg accent-primary, color text-onAccent, radius 10px, h 36px, shadow shadow-sm
- **Hover:** bg darkened 8%, shadow shadow-card, conic-gradient pseudo-border at 30% opacity
- **Active:** scale(0.96), shadow shadow-sm
- **Focus:** focus ring appended to shadow

### Text Input
- **Rest:** bg surface, border 1px at 15% opacity, radius 10px, h 44px, shadow shadow-input
- **Hover:** border at 28% opacity, shadow shadow-input-hover
- **Focus:** border 2px solid accent-primary at 50%, shadow shadow-input-focus (no conic — too distracting)

### Card
- **Rest:** bg surface, border 1px at 20% opacity, radius 12px, shadow shadow-card
- **Hover:** shadow shadow-card-hover, border-color transparent, conic-gradient pseudo-border at 100% opacity, specular-highlight overlay at 40% opacity

---

## Section Index (from full.md)

| Section | Line |
|---|---|
| Identity & Philosophy | 15 |
| Color System | 39 |
| The Conic Gradient System | 116 |
| Typography Matrix | 317 |
| Elevation System | 372 |
| Border System | 429 |
| Component States | 502 |
| Motion Map | 615 |
| Overlays | 663 |
| Layout Tokens | 705 |
| Accessibility Tokens | 744 |
| Visual Style | 769 |
| Signature Animations | 781 |
| Dark Mode Variant | 923 |
| Dual-Mode Comparison Table | 976 |
| Mobile Notes | 1021 |
| Implementation Checklist | 1050 |

---

## Decision Principle

"When in doubt, ask: does this surface look like it would reflect light? If it looks matte and static, add a conic highlight. If it looks garish, reduce saturation and let the angle do the work."

---

## Critical Dependencies

- `@property --angle` support (Chrome 85+, Firefox 128+, Safari 15.4+)
- `conic-gradient` (Chrome 69+, Firefox 83+, Safari 12.1+)
- Fallback: solid accent border if `@property` unsupported
