# Liquid Glass — Quick Reference

> Frosted surfaces floating in light — precision depth through translucency.

**Schema:** v2 | **Mode:** Light-native | **Full spec:** `full.md` (680 lines)

---

## Color Tokens

| Token | Hex / Value | Role |
|---|---|---|
| **Neutrals** |
| page | `#F2F2F7` | Deepest background, Apple system grey 6 light |
| bg | `rgba(255,255,255,0.72)` | Primary glass surface, semi-transparent white |
| surface | `rgba(255,255,255,0.82)` | Elevated cards, inputs, popovers |
| recessed | `#E5E5EA` | Code blocks, inset areas, solid |
| active | `rgba(0,0,0,0.06)` | Active/pressed items, selection highlight |
| **Text** |
| text-primary | `#1D1D1F` | Headings, body text, Apple system label |
| text-secondary | `rgba(60,60,67,0.6)` | Sidebar items, secondary labels, 60% opacity |
| text-muted | `rgba(60,60,67,0.3)` | Placeholders, timestamps, metadata, 30% opacity |
| text-onAccent | `#FFFFFF` | Text on accent-blue backgrounds |
| **Borders** |
| border-base | `#3C3C43` | Used at 8-20% opacity, Apple separator |
| **Accents** |
| accent-primary | `#007AFF` | Primary CTA, active toggles, focus rings, System Blue |
| accent-secondary | `#5AC8FA` | Informational accents, System Blue Light |
| **Semantics** |
| success | `#34C759` | Positive states, toggle on-state, System Green |
| warning | `#FF9500` | Caution states, System Orange |
| danger | `#FF3B30` | Error states, destructive actions, System Red |
| info | `#007AFF` | Info states (same as accent) |
| **Special** |
| inlineCode | `#AD3DA4` | Code text within prose, Apple purple |
| toggleActive | `#34C759` | Toggle/switch active track, System Green |
| selection | `rgba(0,122,255,0.2)` | `::selection` background, System Blue at 20% |

**Glass Opacity Levels:**
- Level 1 (50%): Chips, sidebar, secondary glass
- Level 2 (72%): Primary cards, input areas, standard glass
- Level 3 (82%): Popovers, dropdowns, elevated glass
- Level 4 (92%): Modals, dialogs, nearly opaque

**Border Opacity (on `#3C3C43`):**
- Subtle: 8% | Card: 12% | Hover: 18% | Focus: 100% (System Blue)

---

## Typography

| Role | Family | Size | Weight | Line-height | Spacing | Usage |
|---|---|---|---|---|---|---|
| Display | Plus Jakarta Sans | 34px | 700 | 1.1 | -0.03em | Hero titles, page names |
| Heading | Plus Jakarta Sans | 22px | 600 | 1.27 | -0.015em | Section titles, settings headers |
| Subheading | Plus Jakarta Sans | 18px | 600 | 1.3 | -0.01em | Card titles, subsection headers |
| Body | DM Sans | 17px | 400 | 1.47 | -0.01em | Primary reading text, UI body |
| Body Small | DM Sans | 15px | 400 | 1.4 | -0.005em | Sidebar items, form labels |
| Button | Plus Jakarta Sans | 15px | 600 | 1.4 | -0.005em | Button labels |
| Input | DM Sans | 15px | 400 | 1.4 | normal | Form input text |
| Label | DM Sans | 13px | 400 | 1.3 | 0.01em | Section labels, metadata |
| Code | Geist Mono | 0.9em | 400 | 1.5 | normal | Inline code, code blocks |
| Caption | DM Sans | 12px | 400 | 1.33 | normal | Disclaimers, footnotes |

**Fonts:** Plus Jakarta Sans (400,500,600,700), DM Sans (400,500), Geist Mono (400)
**Critical:** `-webkit-font-smoothing: antialiased`, `text-wrap: pretty`

---

## Elevation

**Strategy:** `layered-shadows` — composite shadows (3-4 layers each) + `backdrop-filter` blur + opacity escalation

### Key Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-glass-1 | `0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03)` | Sidebar, secondary panels, barely-there lift |
| shadow-glass-2 | `0 0.5px 1px rgba(0,0,0,0.06), 0 2px 6px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06)` | Primary cards, input card, 3 layers |
| shadow-glass-3 | `0 0.5px 1px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.04), 0 12px 32px rgba(0,0,0,0.08), 0 24px 48px rgba(0,0,0,0.04)` | Popovers, dropdowns, 4 layers |
| shadow-glass-4 | `0 1px 2px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.06), 0 24px 48px rgba(0,0,0,0.08), 0 48px 96px rgba(0,0,0,0.06)` | Modals, maximum depth |
| shadow-input-focus | `0 0.5px 1px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.06), 0 0 0 2px rgba(0,122,255,0.4)` | Input card focus, blue ring |

### Backdrop-Filter Tokens

| Token | Value | Usage |
|---|---|---|
| glass-subtle | `blur(12px) saturate(1.5)` | Sidebar, low-priority glass |
| glass-standard | `blur(20px) saturate(1.8)` | Primary cards, standard glass panels |
| glass-elevated | `blur(24px) saturate(1.8)` | Popovers, menus |
| glass-heavy | `blur(40px) saturate(2.0)` | Modals, overlays |

**Refraction Highlights:** White `border-top` at 30-70% opacity per level (light catching glass edge)
**Opacity Escalation Rule:** Nested glass = +10% opacity per layer (prevents muddy stacking)

---

## Border System

**Base Color:** `#3C3C43` at variable opacity

| Pattern | Width | Opacity | Usage |
|---|---|---|
| glass-edge | 0.5px | 8% | Default glass panel edge, almost invisible |
| glass-card | 0.5px | 12% | Card-style glass, slightly more definition |
| glass-hover | 0.5px | 18% | Hovered glass panels |
| input | 1px | 12% | Form input borders, heavier for usability |
| input-focus | 1px | -- | `rgba(0,122,255,0.5)` blue border |

**Focus Ring:** `box-shadow: 0 0 0 2px #FFF, 0 0 0 4px rgba(0,122,255,0.4)` — 2px blue ring with 2px white offset

---

## Motion

**Easings:**
- `default`: `cubic-bezier(0.4, 0, 0.2, 1)` — standard system
- `apple-ease`: `cubic-bezier(0.25, 0.1, 0.25, 1)` — sharper deceleration
- `spring-gentle`: `cubic-bezier(0.2, 0.8, 0.2, 1.02)` — glass panel slides
- `out-quart`: `cubic-bezier(0.165, 0.85, 0.45, 1)` — snappy interactions
- `out-expo`: `cubic-bezier(0.19, 1, 0.22, 1)` — smooth open/close

**Duration × Component:**
- Sidebar item: 75ms out-quart
- Button hover: 100ms apple-ease
- Toggle/chip: 150ms default
- Glass card shadow: 200ms apple-ease
- Ghost icon buttons: 250ms out-quart
- Glass panel slide: 350ms spring-gentle
- Blur-focus modal: 300ms out-expo

**Active Press Scale:**
- Nav items: 0.985 | Chips: 0.98 | Buttons: 0.97 | Tabs: 0.96 | Cards: 0.99

---

## Component Quick-Reference

### Primary Button
**Rest:** bg `#007AFF`, color `#FFFFFF`, radius 8px, h 34px, padding `0 16px`, shadow none
**Hover:** bg `#0070EB`
**Active:** `scale(0.97)`, bg `#0064D2`
**Transition:** 100ms apple-ease

### Text Input
**Rest:** bg `rgba(255,255,255,0.72)`, border `1px solid rgba(60,60,67,0.12)`, radius 10px, h 44px, backdrop-filter `blur(20px) saturate(1.8)`, shadow shadow-input
**Focus:** border `rgba(0,122,255,0.5)`, shadow shadow-input-focus
**Transition:** border 150ms, shadow 200ms apple-ease

### Card
**Rest:** bg `rgba(255,255,255,0.72)`, border `0.5px solid rgba(60,60,67,0.12)`, radius 12px, backdrop-filter `blur(20px) saturate(1.8)`, shadow shadow-glass-2, border-top `0.5px solid rgba(255,255,255,0.5)`
**Hover:** shadow shadow-glass-3, border `rgba(60,60,67,0.18)` — card lifts
**Transition:** shadow 200ms, border 150ms apple-ease

---

## Section Index (Full Spec Line Numbers)

- **Identity & Philosophy** → Line 31
- **Color System** → Line 48
  - Palette → Line 50
  - Opacity System → Line 81
  - Glass Tint System → Line 101
- **Typography Matrix** → Line 123
- **Elevation System** → Line 156
  - Shadow Tokens → Line 177
  - Backdrop-Filter Tokens → Line 196
  - Refraction Highlights → Line 209
- **Border System** → Line 225
- **Component States** → Line 251
  - Buttons (Primary) → Line 253
  - Text Input → Line 289
  - Cards → Line 308
  - Sidebar Items → Line 316
  - Toggle/Switch → Line 335
- **Motion Map** → Line 352
- **Overlays** → Line 393
  - Popover → Line 395
  - Modal → Line 411
- **Layout Tokens** → Line 436
- **Accessibility Tokens** → Line 478
  - Reduced Motion → Line 497
- **Signature Animations** → Line 527
  - Glass Panel Slide → Line 529
  - Blur-Focus Modal → Line 549
  - Shadow Elevation Shift → Line 564
- **Dark Mode Variant** → Line 594
- **Mobile Notes** → Line 629
- **Implementation Checklist** → Line 653

---

## Critical Implementation Notes

1. **Glass requires content behind it** — without background variation, translucency reads as solid white
2. **Minimum 72% white opacity** ensures WCAG AA contrast (8.2:1 on `#F2F2F7`)
3. **Opacity escalation rule:** Nested glass = +10% per layer (popover on card = 92%, not 82%)
4. **`saturate(1.8)` is essential** — without it, blurred content looks dead
5. **Mobile:** Blur values -40%, opacity +10%, max 2 concurrent glass layers, total blur budget 50px
6. **`prefers-reduced-motion`:** Spatial animations collapse to fades, parallax disabled, `backdrop-filter` retained (it's static, not motion)
7. **Focus ring:** Always `0 0 0 2px #FFF, 0 0 0 4px rgba(0,122,255,0.4)` — white offset prevents bleed
8. **Refraction highlights:** White `border-top` at varying opacity per level (30-70%) — light catching glass edge
9. **Toggle override:** 51x31px (Apple dimensions), not schema default 36x20px
10. **Fallback:** `@supports not (backdrop-filter: blur(1px))` → near-opaque bg + standard shadows
