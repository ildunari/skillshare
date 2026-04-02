# Future Medieval — Quick Reference

> Arcane precision -- an enchanted library where illuminated manuscripts meet modern interfaces.

**Best for:** Fantasy-themed apps, tabletop RPG tools, worldbuilding wikis, book/library management, knowledge bases, lore compendiums, creative writing platforms, archival research tools, grimoire-style documentation, interactive fiction, museum/exhibition interfaces, ceremonial event platforms.

---

## Color Tokens (Complete)

| Token | Hex | Role |
|---|---|---|
| **page** | `#12100B` | Deepest background. The oak desk beneath everything. |
| **bg** | `#1A1510` | Primary surface background. Sidebar, main content area. |
| **surface** | `#242019` | Elevated cards, inputs, popovers. |
| **recessed** | `#0D0B08` | Code blocks, inset areas. |
| **active** | `#2E2820` | Active/pressed items, selected states. |
| **text-primary** | `#EAE2D0` | Headings, body text. Bone white. |
| **text-secondary** | `#A89888` | Sidebar items, secondary labels. Faded ink. |
| **text-muted** | `#786858` | Placeholders, timestamps, metadata. Ghost script. |
| **text-onAccent** | `#12100B` | Text on accent-colored backgrounds. |
| **accent-primary** | `#C9A84C` | Primary accent, brand color, primary CTA. Gilded gold. |
| **accent-secondary** | `#5A7A6C` | Secondary accent, links, informational highlights. Verdigris. |
| **border-base** | `#A08A50` | Base border color used at variable opacity. Tarnished gold. |
| **oxblood** | `#6B2D34` | Highlight and emphasis color. Wax seal red. |
| **success** | `#4A7A52` | Positive states. Herbalist green. |
| **warning** | `#B89040` | Caution states. Amber resin. |
| **danger** | `#8A3838` | Error states, destructive actions. Rubrication red. |
| **info** | `#5A7A6C` | Informational states. Same as accent-secondary. |
| **inlineCode** | `#C9A84C` at 80% | Code text within prose. |
| **toggleActive** | `#C9A84C` | Toggle/switch active track. |
| **selection** | `rgba(201, 168, 76, 0.18)` | ::selection background. |

**Border Opacity System** (on `border-base`):
- subtle: 12% | card: 22% | hover: 32% | focus: 42% | glow: 55%

---

## Typography Roles (All 9)

| Role | Family | Size | Weight | Line-height | Spacing | Usage |
|---|---|---|---|---|---|---|
| **Display** | Cinzel Decorative | 36px | 400 | 1.15 | 0.04em | Hero titles, page names. ONE per viewport. |
| **Heading** | Crimson Pro | 24px | 600 | 1.3 | 0.005em | Section titles, settings headers. |
| **Subheading** | Crimson Pro | 18px | 500 | 1.35 | normal | Subsection titles, card headers. |
| **Body** | Crimson Pro | 16px | 400 | 1.6 | normal | Primary reading text, UI body. |
| **Body Small** | Crimson Pro | 14px | 400 | 1.5 | normal | Sidebar items, form labels. |
| **Button** | Crimson Pro | 14px | 600 | 1.4 | 0.02em | Button labels. |
| **Input** | Crimson Pro | 14px | 400 | 1.4 | normal | Form input text. |
| **Code** | Fira Code | 0.9em | 400 | 1.5 | normal | Inline code, code blocks. Ligatures enabled. |
| **Label** | Crimson Pro | 12px | 500 | 1.33 | 0.03em | Section labels, metadata. |
| **Caption** | Crimson Pro | 12px | 400 | 1.33 | 0.01em | Disclaimers, footnotes. |

**Font Loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Fira+Code:wght@400&display=swap" rel="stylesheet">
```

---

## Elevation Summary

**Strategy:** `layered-shadows`

Warm composite shadows between layered vellum surfaces. Gold borders provide luminance contrast depth signal.

**Shadow Tokens:**
- `shadow-sm`: `0 1px 3px rgba(12, 10, 6, 0.30), 0 1px 2px rgba(12, 10, 6, 0.20)` — cards at rest
- `shadow-md`: `0 3px 8px rgba(12, 10, 6, 0.35), 0 1px 3px rgba(12, 10, 6, 0.25)` — cards on hover
- `shadow-input`: `0 2px 6px rgba(12, 10, 6, 0.25), 0 0 0 0.5px rgba(160, 138, 80, 0.12)` — input rest
- `shadow-input-hover`: `0 3px 10px rgba(12, 10, 6, 0.30), 0 0 0 0.5px rgba(160, 138, 80, 0.22)` — input hover
- `shadow-input-focus`: `0 4px 14px rgba(12, 10, 6, 0.35), 0 0 0 1px rgba(160, 138, 80, 0.32)` — input focus
- `shadow-popover`: `0 4px 16px rgba(12, 10, 6, 0.45), 0 2px 6px rgba(12, 10, 6, 0.30)` — popovers, menus
- `shadow-modal`: `0 8px 32px rgba(12, 10, 6, 0.55), 0 4px 12px rgba(12, 10, 6, 0.35)` — modals

---

## Border System

**Widths:** hairline 0.5px | default 1px | medium 1.5px | heavy 2px

**Opacity Scale** (on `var(--border-base)`):
- subtle: 12% | card: 22% | hover: 32% | focus: 42% | glow: 55%

**Focus Ring:**
```css
box-shadow: 0 0 0 2px var(--page), 0 0 0 4px rgba(201, 168, 76, 0.55);
```

---

## Motion Personality

**Ceremonial unveiling.** Minimum transition: 150ms. Most: 250-500ms. Page reveals: 800-1200ms.

**Easings:**
- `inscribe`: `cubic-bezier(0.25, 0.1, 0.25, 1.0)` — most state transitions
- `unveil`: `cubic-bezier(0.22, 1.0, 0.36, 1.0)` — page entries, panels
- `press`: `cubic-bezier(0.0, 0.0, 0.58, 1.0)` — active/press states
- `bind`: `cubic-bezier(0.4, 0.0, 0.2, 1.0)` — toggle/chip/general
- `illuminate`: `cubic-bezier(0.0, 0.5, 0.5, 1.0)` — hover gold-brightening
- `processional`: `cubic-bezier(0.16, 1.0, 0.3, 1.0)` — staggered reveals

**Key Durations:**
- Sidebar item: 150ms/200ms inscribe
- Button hover: 250ms illuminate
- Toggle: 300ms bind
- Card hover shadow: 400ms illuminate
- Panel slide: 700ms unveil
- Modal enter: 600ms unveil
- Hero/page entry: 1000ms unveil
- Gold border draw: 800ms processional

**Active Press Scale:**
- Nav: 0.985 | Chips: 0.98 | Buttons: 0.97 | Tabs: 0.96 | Cards: 0.995

---

## Component Quick Reference

### Primary Button
- **Rest:** bg `#C9A84C`, border 1px gold 60%, color `#12100B`, radius 6px, h 34px, shadow-sm
- **Hover:** bg `#D4B45A`, shadow deepens + gold ring
- **Active:** scale(0.97), bg `#B89840`
- **Transition:** bg 250ms, transform 120ms, shadow 350ms

### Text Input
- **Rest:** bg `#242019`, border 1px gold 22%, radius 8px, h 44px, shadow-input
- **Hover:** border 32%, shadow-input-hover
- **Focus:** border `#C9A84C` 40%, shadow-input-focus, focus ring
- **Transition:** border 200ms, shadow 350ms

### Card
- **Rest:** bg `#242019`, border 1px gold 22%, radius 8px, shadow-sm
- **Hover:** border 32%, shadow-md
- **Transition:** border 250ms, shadow 400ms (ceremonially slow)

---

## Section Index

1. [Identity & Philosophy](#identity--philosophy) — Line 36 in full.md
2. [Color System](#color-system) — Line 68
3. [Typography Matrix](#typography-matrix) — Line 122
4. [Elevation System](#elevation-system) — Line 161
5. [Border System](#border-system) — Line 199
6. [Component States](#component-states) — Line 260
7. [Motion Map](#motion-map) — Line 370
8. [Layout Tokens](#layout-tokens) — Line 422
9. [Accessibility Tokens](#accessibility-tokens) — Line 475
10. [Overlays](#overlays) — Line 541
11. [Visual Style](#visual-style) — Line 585
12. [Signature Animations](#signature-animations) — Line 647
13. [Dark Mode Variant](#dark-mode-variant-light-mode) — Line 860
14. [Mobile Notes](#mobile-notes) — Line 893
15. [Data Visualization](#data-visualization) — Line 933
16. [Implementation Checklist](#implementation-checklist) — Line 947

---

**Decision Principle:** "When in doubt, ask: would a master scribe approve? If it is hasty, garish, or careless, it does not belong in the codex."
