# 9. Vapor Silk — Quick Reference

> Pastel ambient mesh -- silk scarves drifting through warm light. The calmest possible interface.

**Best for:** Meditation apps, wellness platforms, ambient music players, journaling tools, mood trackers, gentle onboarding flows, reading apps, calm productivity, creative writing tools, personal dashboards.

**Decision principle:** "When in doubt, ask: does this feel like a deep breath? If it creates tension, urgency, or sharpness -- soften it. If it feels stagnant or lifeless -- add a slow drift."

---

## Color Tokens

| Token | Hex | Role |
|---|---|---|
| page | `#F3EDE5` | Deepest background -- sunlit floor beneath drifting scarves |
| bg | `#F9F5F0` | Primary surface -- open air of the conservatory |
| surface | `#FEFCF9` | Cards, inputs, elevated surfaces |
| recessed | `#EFE9E1` | Code blocks, inset areas |
| active | `#EDE5DF` | Active/pressed states, user bubble |
| text-primary | `#3D3630` | Headings, body text -- warm brown |
| text-secondary | `#7D756D` | Sidebar items, secondary labels |
| text-muted | `#ADA5A0` | Placeholders, timestamps |
| text-onAccent | `#FFF9F5` | Text on accent backgrounds |
| border-base | `#D5CBC0` | Base border (variable opacity) |
| accent-primary | `#B8899A` | Dusty mauve -- brand/CTA |
| accent-secondary | `#A594C0` | Soft lavender -- tags, highlights |
| accent-tertiary | `#96C0B0` | Pale mint -- success-adjacent |
| success | `#7FAF8A` | Sage mist -- positive states |
| warning | `#C5A050` | Warm honey -- caution |
| danger | `#C07A78` | Muted rose -- errors |
| info | `#8BA5BD` | Cloud blue -- informational |
| inlineCode | `#9B6B82` | Code text within prose |
| toggleActive | `#A594C0` | Toggle active track |
| selection | `rgba(184, 137, 154, 0.16)` | Text selection background |

**Border Opacity:** subtle 12%, card 20%, hover 28%, focus 38%

---

## Typography

| Role | Family | Size | Weight | Line-height | Usage |
|---|---|---|---|---|---|
| Display | Outfit | 38px | 300 | 1.25 (47.5px) | Hero titles, page titles |
| Heading | Outfit | 24px | 420 | 1.35 (32.4px) | Section titles, headers |
| Body | Figtree | 16px | 400 | 1.6 (25.6px) | Primary reading text |
| Body Small | Figtree | 14px | 400 | 1.5 (21px) | Sidebar, form labels |
| Button | Figtree | 14px | 480 | 1.4 (19.6px) | Button labels |
| Input | Figtree | 14px | 420 | 1.4 (19.6px) | Form input text |
| Label | Figtree | 12px | 400 | 1.33 (16px) | Metadata, timestamps |
| Code | Space Mono | 0.9em | 400 | 1.55 | Inline code, data |
| Caption | Figtree | 12px | 400 | 1.33 (16px) | Disclaimers, footnotes |

**Fonts:** Outfit (Display/Heading), Figtree (Body/UI), Space Mono (Code)

---

## Elevation

**Strategy:** Tint-stepping + ultra-soft shadows with extreme blur (32px)

**Key Shadows:**
- `shadow-sm` — `0 2px 8px rgba(61, 54, 48, 0.03)` — Cloud-wisp
- `shadow-card` — `0 4px 32px rgba(61, 54, 48, 0.025), 0 0 0 0.5px rgba(213, 203, 192, 0.20)` — Floating on clouds
- `shadow-card-hover` — `0 6px 32px rgba(61, 54, 48, 0.035), 0 0 0 0.5px rgba(213, 203, 192, 0.28)` — Hover deepens
- `shadow-card-focus` — `0 6px 32px rgba(61, 54, 48, 0.05), 0 0 0 0.5px rgba(213, 203, 192, 0.28)` — Focus full depth
- `shadow-popover` — `0 4px 24px rgba(61, 54, 48, 0.08), 0 1px 6px rgba(61, 54, 48, 0.04)` — Menu overlays

**Backdrop Blur:** popover 20px, modal 16px, badge 8px

---

## Borders

**Base Color:** `#D5CBC0` (Petal Veil) at variable opacity

**Widths:** hairline 0.5px, default 1px, medium 1.5px, heavy 2px (focus ring only)

**Focus Ring:** `rgba(165, 148, 192, 0.52)`, 2px solid, 2px offset (lavender)

---

## Motion

**Easings:**
- `silk` — `cubic-bezier(0.25, 0.1, 0.25, 1)` — Signature gentle easing
- `silk-out` — `cubic-bezier(0.16, 0.9, 0.4, 1)` — Slightly faster arrival
- `silk-drift` — `cubic-bezier(0.33, 0, 0.67, 1)` — Ambient background motion
- `silk-reveal` — `cubic-bezier(0.12, 0.8, 0.3, 1)` — Panels, modals, page entries
- `ambient` — `linear` — Background mesh gradient (25s cycles)

**Durations:**
- Sidebar items: 200ms (silk-out)
- Buttons: 250ms (silk)
- Cards: 350ms (silk)
- Ghost buttons: 400ms (silk)
- Chat input: 500ms (silk)
- Page reveals: 800ms (silk-reveal)
- Mesh gradient: 25000ms (ambient)

**Press Scale:** nav 0.985, chips 0.995, buttons 0.98, tabs 0.96

**Reduced Motion:** Fade-only, disable ambient gradient, no spatial transforms

---

## Key Components

### Primary Button
- Rest: transparent bg, border 0.5px at 28% opacity, 12px radius, 36px height
- Hover: recessed bg, shadow-sm
- Active: scale(0.98)
- Transition: 250ms silk

### Text Input
- Rest: surface bg, 1px border at 12% opacity, 16px radius, 44px height
- Hover: border 28% opacity, shadow-sm
- Focus: lavender ring, border 28%
- Caret: mauve (`#B8899A`)
- Transition: 300ms silk

### Card
- Rest: surface bg, 0.5px border at 20%, 16px radius, shadow-sm, 24px padding
- Hover: border 28%, shadow-md
- Transition: 350ms silk

---

## Section Index (full.md)

- [Identity & Philosophy](#identity--philosophy) — Line 16
- [Color System](#color-system) — Line 39
- [Typography Matrix](#typography-matrix) — Line 104
- [Elevation System](#elevation-system) — Line 150
- [Border System](#border-system) — Line 197
- [Component States](#component-states) — Line 235
- [Motion Map](#motion-map) — Line 383
- [Overlays](#overlays) — Line 439
- [Layout Tokens](#layout-tokens) — Line 494
- [Accessibility Tokens](#accessibility-tokens) — Line 545
- [Visual Style](#visual-style) — Line 575
- [Signature Animations](#signature-animations) — Line 638
- [Dark Mode Variant](#dark-mode-variant) — Line 842
- [Data Visualization](#data-visualization) — Line 896
- [Mobile Notes](#mobile-notes) — Line 912
- [Implementation Checklist](#implementation-checklist) — Line 941

---

## Theme Character

**Core tension:** Softness vs structure. Radically soft (pastels, max border-radius, extreme blur shadows, 800ms+ transitions) while remaining functional.

**Ambient presence:** Interface breathes via slow-drifting mesh gradients (25s cycles). Motion below conscious awareness.

**Silk materiality:** Every surface has draped fabric quality -- soft, luminous, gentle folds via layered pastel shadows and generous curves.

**What this theme is NOT:**
- Not sharp/angular (zero hard edges, zero square corners)
- Not saturated (all colors <50% saturation HSL)
- Not fast (minimum 200ms transitions, 800ms reveals)
- Not cold (warm cream base, never cool gray)
- Not glassmorphic (opaque pastels, not transparent panels)

**Signature visual:** Ambient mesh gradient background -- 4 radial-gradient layers (mauve/lavender/mint at 3-6% opacity) drifting over 25s cycle.

**Performance:** Mobile-friendly when animation disabled. No WebGL, no particle systems. Primary expense: backdrop-blur (reduced on mobile).
