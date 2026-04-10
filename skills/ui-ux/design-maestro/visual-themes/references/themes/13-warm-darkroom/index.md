# 13. Warm Darkroom — Quick Reference

> Chemical patience -- images emerge from darkness the way trust emerges from silence.

**Best for:** Photography portfolios, editorial longform, journal/diary apps, slow media platforms, analog-aesthetic tools, archival interfaces, memoir and storytelling apps, film review platforms, quiet productivity tools.

**Decision principle:** "When in doubt, ask: would this feel at home in a darkroom? If it demands attention, it does not belong. Light is earned, not given."

---

## Color Tokens (Complete)

| Token | Hex | OKLCH | Role |
|---|---|---|---|
| **Neutrals** |
| page | `#0E0C0A` | L=0.08 C=0.01 h=60 | Deepest background, sealed room |
| bg | `#171311` | L=0.11 C=0.012 h=55 | Primary surface, sidebar |
| surface | `#211C18` | L=0.14 C=0.015 h=50 | Cards, inputs, popovers |
| recessed | `#0A0908` | L=0.06 C=0.008 h=55 | Code blocks, inset areas |
| active | `#2A2420` | L=0.17 C=0.016 h=50 | Active/pressed, warmest dark |
| **Text** |
| text-primary | `#E8E0D4` | L=0.90 C=0.02 h=75 | Paper white, headings, body |
| text-secondary | `#A89A8A` | L=0.66 C=0.03 h=65 | Fixer residue, secondary labels |
| text-muted | `#7A6E62` | L=0.49 C=0.03 h=60 | Underdeveloped, placeholders |
| text-onAccent | `#0E0C0A` | L=0.08 C=0.01 h=60 | Dark on warm accent |
| **Accents** |
| accent-primary | `#C4956A` | L=0.68 C=0.08 h=65 | Sepia tone, primary CTA |
| accent-secondary | `#5A7A9A` | L=0.53 C=0.06 h=240 | Chemical blue, cool counterpoint |
| **Borders** |
| border-base | `#8A6A52` | L=0.48 C=0.06 h=55 | Used at 10-38% opacity |
| **Semantic** |
| success | `#5A8A5A` | L=0.55 C=0.08 h=140 | Developer green |
| warning | `#B8924A` | L=0.64 C=0.10 h=80 | Amber fix |
| danger | `#A04030` | L=0.40 C=0.12 h=25 | Stop bath red |
| info | `#5A7A9A` | L=0.53 C=0.06 h=240 | Chemical blue |
| **Environmental** |
| safe-light | `#8B3A2A` | L=0.35 C=0.12 h=28 | Ambient only, never interactive |
| **Special** |
| inlineCode | `#C4956A` at 85% lightness | Sepia-tinted code |
| toggleActive | `#C4956A` | Sepia, developed state |
| selection | `rgba(196, 149, 106, 0.20)` | Warm sepia wash |

**Border Opacity System:** subtle 10%, card 18%, hover 28%, focus 38%

---

## Typography (9 Roles)

| Role | Family | Size | Weight | Line-height | Spacing | Usage |
|---|---|---|---|---|---|---|
| Display | DM Serif Display | 36px | 400 | 1.15 | -0.02em | Hero titles, gallery exhibition feel |
| Heading | DM Serif Display | 24px | 400 | 1.25 | -0.01em | Section titles, settings headers |
| Subheading | Spectral | 18px | 500 | 1.35 | normal | Subsection titles, card headers |
| Body | Spectral | 16px | 400 | 1.65 | normal | Primary reading, editorial comfort |
| Body Small | Spectral | 14px | 400 | 1.5 | normal | Sidebar items, form labels |
| Button | Spectral | 14px | 600 | 1.4 | 0.01em | Button labels, quiet authority |
| Input | Spectral | 14px | 400 | 1.4 | normal | Form input, analog character |
| Code | IBM Plex Mono | 0.9em | 400 | 1.5 | normal | Inline code, data values |
| Label | Spectral | 12px | 500 | 1.33 | 0.03em | Metadata, timestamps |
| Caption | Spectral | 12px | 400 | 1.33 | normal | Footnotes, photo credits |

**Key:** All-serif stack. DM Serif Display for display/headings, Spectral for everything else, IBM Plex Mono for code. No sans-serif. `-webkit-font-smoothing: antialiased` mandatory. Line-height 1.65 for body = meditative reading rhythm.

**Fonts:** `https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400&display=swap`

---

## Elevation Summary

**Strategy:** `surface-shifts` — No traditional shadows. Depth = warmth gradient. Surfaces closer to viewer are warmer/lighter (catch more safe-light). Surfaces farther away are cooler/darker.

**Surface Hierarchy:**
- page (L=0.08, coolest) → bg (L=0.11) → surface (L=0.14, warm) → active (L=0.17, warmest)
- recessed (L=0.06, coldest) for code blocks

**Surface-Shift Tokens:**
- shift-warm: +3% lightness, +0.005 chroma (cards at rest)
- shift-warmer: +5% lightness, +0.008 chroma (hover)
- shift-warmest: +7% lightness, +0.012 chroma (focus/active)
- shift-cool: -2% lightness, -0.003 chroma (recessed)

**Vignette:** Radial gradient darkens page edges, centered at 50% 30% from top (overhead safe-light position).

**Separation Recipe:** Warmth-step surfaces + faint borders (10-18% opacity). No visible dividers. Darkness is the primary separator.

---

## Border System

**Base Color:** `#8A6A52` (Safe-Light Edge) used at variable opacity.

**Widths:** hairline 0.5px, default 1px, medium 1.5px, heavy 2px

**Opacity Scale:** subtle 10%, card 18%, hover 28%, focus 38%

**Focus Ring:** `0 0 0 2px var(--page), 0 0 0 4px rgba(196, 149, 106, 0.50)` — warm sepia ring with page-colored gap, solid (no glow).

---

## Motion Personality

**Philosophy:** Chemical reveal. Things develop, not appear. Slowest reveal theme in system. Patience is the aesthetic.

**Custom Easings:**
- **developer:** `cubic-bezier(0.25, 0.1, 0.25, 1)` — slow ramp, gentle settle, chemistry pace
- **stop-bath:** `cubic-bezier(0.0, 0.0, 0.58, 1.0)` — abrupt start, gradual finish
- **fixer:** `cubic-bezier(0.22, 1, 0.36, 1)` — long deceleration tail, final details resolve
- **rinse:** `cubic-bezier(0.45, 0, 0.55, 1)` — symmetrical, ambient loops
- **expose:** `cubic-bezier(0.0, 0.5, 0.5, 1.0)` — front-loaded, enlarger light hits paper

**Duration Range:** 120ms (sidebar hover, fastest) → 2500ms (chemical reveal, slowest). Most transitions 250-500ms.

**Signature:** Chemical reveal 2500ms with 3-stage opacity + blur + desaturation, 150ms stagger per element.

---

## Component Quick-Reference

### Button (Primary)
- Rest: bg `#C4956A`, color `#0E0C0A`, radius 6px, h 34px, font Spectral 14px/600
- Hover: bg `#D0A57A`, warmth bloom `0 0 12px rgba(196, 149, 106, 0.12)`, 250ms expose easing
- Active: `scale(0.97)`, 120ms stop-bath
- Focus: sepia ring
- Disabled: opacity 0.4, `grayscale(0.3)`

### Input (Text)
- Rest: bg `#211C18`, border 18%, radius 8px, h 44px, font Spectral 14px
- Hover: border 28%, bg `shift-warm`, 200ms developer
- Focus: border `#C4956A` at 35%, bg `shift-warmer`, sepia ring, 400ms fixer for bg
- Caret: `#C4956A`

### Card
- Rest: bg `#211C18`, border 18%, radius 8px
- Hover: border 28%, bg `shift-warm`, **500ms** expose (intentionally slow — develops like a print), border 250ms developer (responds first)

---

## Section Index (from full.md)

1. [Identity & Philosophy](#identity--philosophy) — line 9
2. [Color System](#color-system) — line 28 (Palette, Special Tokens, Opacity System, Color Rules)
3. [Typography Matrix](#typography-matrix) — line 83 (9 roles + Font Loading)
4. [Elevation System](#elevation-system) — line 119 (Surface Hierarchy, Surface-Shift Tokens, Vignette, Separation Recipe)
5. [Border System](#border-system) — line 190 (Widths, Opacity Scale, Patterns, Focus Ring)
6. [Component States](#component-states) — line 246 (Buttons, Input, Chat Input Card, Cards, Sidebar, Chips, Toggle, User Bubble)
7. [Motion Map](#motion-map) — line 350 (Easings, Duration x Easing x Component, Active Press Scale)
8. [Layout Tokens](#layout-tokens) — line 402 (Spacing Scale, Density, Radius, Responsive)
9. [Accessibility Tokens](#accessibility-tokens) — line 454 (Focus, Disabled, Selection, Scrollbar, Reduced Motion)
10. [Overlays](#overlays) — line 517 (Popover, Modal, Tooltip)
11. [Visual Style](#visual-style) — line 558 (Film Grain, Safe-Light Ambient Wash, Material)
12. [Signature Animations](#signature-animations) — line 628 (Chemical Reveal, Dodge and Burn, Film Grain Breathe, Tray Ripple, Contact Sheet Scan)
13. [Dark Mode Variant (Light Mode)](#dark-mode-variant-light-mode) — line 814 (Proof Sheet variant)
14. [Mobile Notes](#mobile-notes) — line 849 (Effects to Disable, Simplify, Sizing, Performance Budget)
15. [Data Visualization](#data-visualization) — line 886
16. [Implementation Checklist](#implementation-checklist) — line 900

---

## Key Constraints

- **Safe-light red:** Environmental only, never interactive (no buttons/links).
- **Sepia:** Earned. Marks complete/resolved states only.
- **Chemical blue:** Counterpoint. Info labels, code, secondary controls.
- **No pure black/white:** Range is `#0A0908` to `#E8E0D4`.
- **Grain mandatory:** 3-4% opacity, feTurbulence, soft-light blend, 8s breathe cycle.
- **Warmth gradient for depth:** Darker = cooler, lighter = warmer.
- **All-serif type:** No sans-serif anywhere (IBM Plex Mono is the "neutral" option).
- **Card hover 500ms:** Intentionally slow. Cards develop like prints.
- **Chemical reveal 2500ms:** 3-stage opacity + blur + desaturation, 150ms stagger.
- **Mobile:** Disable grain, vignette, safe-light wash, dodge-burn. Simplify reveal to 1200ms opacity-only.

---

## Light Mode: Proof Sheet (Summary)

- **page:** `#F4F0EA` (warm cream), **bg:** `#EBE6DE`, **surface:** `#FFFFFF`
- **text-primary:** `#1A1612` (near-black), **accent-primary:** `#9A6A3A` (darker sepia)
- **Disabled:** grain, vignette, safe-light wash
- **Changed:** Chemical reveal → 400ms fade. Surface-shifts → subtle warm shadows.
- **Border opacity:** +2-4% (subtle 12%, card 22%, hover 32%, focus 42%)
- **Decision principle shift:** "Would this look right on a gallery wall?"
