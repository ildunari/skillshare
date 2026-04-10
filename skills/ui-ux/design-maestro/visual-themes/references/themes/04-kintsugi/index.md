# Kintsugi — Quick Reference

> Broken vessels mended with gold -- extreme negative space, washi paper warmth, and the quiet beauty of imperfection.

**Schema:** v2 | **Mode:** Light | **Full spec:** `full.md` (994 lines)

---

## Color Tokens

| Token | Hex | Role |
|---|---|---|
| **Neutrals** |||
| page | `#EDE8DC` | Tatami — Deepest background, warm straw-mat tone |
| bg | `#F5F0E6` | Washi — Primary surface, handmade mulberry paper |
| surface | `#FBF8F1` | Kozo White — Elevated cards, inputs, brightest paper |
| recessed | `#E5DFCF` | Torinoko — Code blocks, eggshell-toned paper |
| active | `#DDD6C4` | Kinari — Active/pressed items, natural silk tone |
| **Text** |||
| text-primary | `#1C1B18` | Sumi — Carbon black sumi ink (15.2:1 on surface) |
| text-secondary | `#6B665C` | Nezumi — Mouse-grey ink wash (4.8:1 on surface) |
| text-muted | `#8E8880` | Usuzumi — Diluted ink (3.6:1 on surface, AA large) |
| text-onAccent | `#FBF8F1` | Kozo White — Text on accent backgrounds |
| **Borders** |||
| border-base | `#B5ADA0` | Hai — Ash grey, used at variable opacity (8%-40%) |
| **Accents** |||
| accent-primary | `#C8A951` | Kintsugi Gold — The scar, focus rings, repair lines |
| accent-secondary | `#3D5A80` | Ai Indigo — Links, interactive elements, traditional dye |
| **Semantics** |||
| success | `#6B8F5E` | Matcha — Whisked green tea |
| warning | `#C4923A` | Kuchiba — Fallen-leaf amber |
| danger | `#9B4A3A` | Beni — Safflower red pigment |
| info | `#4A6E8A` | Hanada — Flower-field blue |
| **Special** |||
| inlineCode | `#7A6B3A` | Darkened gold for code text (5.8:1 contrast) |
| toggleActive | `#6B8F5E` | Matcha green for toggle track |
| selection | `rgba(200,169,81,0.18)` | Gold at 18% opacity for ::selection |
| kintsugi-gold | `#C8A951` | Primary gold value (CSS custom property) |
| kintsugi-gold-muted | `rgba(200,169,81,0.30)` | Gold 30% — divider lines |
| kintsugi-gold-subtle | `rgba(200,169,81,0.15)` | Gold 15% — hover tints |
| kintsugi-gold-focus | `rgba(200,169,81,0.50)` | Gold 50% — focus rings |
| kintsugi-gold-hover | `rgba(200,169,81,0.08)` | Gold 8% — ghost button hover bg |

### Gold Repair System

**Never:** Gold as button fill, card background, gradients, text (except inlineCode), icon fills, or multiple gold elements in one viewport.

**Always:** Gold is linear only — 1px lines, 2px focus rings, border accents, decorative crack patterns at 20-30% opacity.

### Border Opacity Scale

- **whisper:** 8% — Ghost borders
- **subtle:** 15% — Panel edges, card outlines at rest
- **card:** 20% — Standard card borders
- **hover:** 30% — Hovered elements
- **focus:** 40% — Focused inputs

---

## Typography

| Role | Family | Size | Weight | Line-height | Spacing | Usage |
|---|---|---|---|---|---|---|
| Display | Shippori Mincho | 36px | 500 | 1.25 | 0.02em | Hero titles (CJK: 32px) |
| Heading | Shippori Mincho | 24px | 500 | 1.4 | 0.01em | Section titles |
| Subheading | Shippori Mincho | 19px | 400 | 1.5 | 0.02em | Subsection labels |
| Body | Noto Serif / JP | 17px | 400 | 1.75 | normal | Primary reading text |
| Body CJK | Noto Serif JP | 17px | 400 | 1.8 | 0.05em | Japanese/Chinese/Korean |
| Body Small | Noto Serif | 15px | 400 | 1.6 | normal | Sidebar items, secondary UI |
| Button | Shippori Mincho | 14px | 500 | 1.4 | 0.04em | Button labels |
| Input | Noto Serif | 16px | 400 | 1.5 | normal | Form inputs |
| Label | Noto Serif | 12px | 400 | 1.4 | 0.06em | Metadata, timestamps (never uppercase) |
| Code | IBM Plex Mono | 0.88em | 400 | 1.6 | normal | Inline code, code blocks |
| Caption | Noto Serif | 12px | 400 | 1.5 | 0.02em | Disclaimers, footnotes |

**CJK-specific:** Line-height 1.8 (vs 1.75), letter-spacing 0.05em, `word-break: break-all`, `text-wrap: auto`, `hanging-punctuation: first last`, paragraph spacing 1.5em (vs 1em).

**Font Loading:** Shippori Mincho (400,500,600), Noto Serif (400,500+italic), Noto Serif JP (400,500), IBM Plex Mono (400). Always `-webkit-font-smoothing: antialiased`.

---

## Elevation

**Strategy:** Surface-shifts with minimal borders. Paper layers, brightness = elevation.

| Token | Value | Usage |
|---|---|---|
| shadow-none | `none` | Page background, flat surfaces |
| shadow-breath | `0 2px 8px rgba(28,27,24,0.03)` | Cards at rest |
| shadow-breath-hover | `0 3px 12px rgba(28,27,24,0.05)` | Card hover |
| shadow-breath-focus | `0 3px 12px rgba(28,27,24,0.05), 0 0 0 2px rgba(200,169,81,0.5)` | Input focus + gold ring |
| shadow-overlay | `0 4px 16px rgba(28,27,24,0.06)` | Popovers, modals |
| shadow-inset | `inset 0 1px 3px rgba(28,27,24,0.03)` | Recessed surfaces, code blocks |

**Separation:** Surface-brightness stepping (Tatami → Washi → Kozo White), 0.5px borders at 8-20% opacity, gold repair lines at 30% for major sections.

---

## Border System

**Widths:** 0.5px (hairline, standard), 1px (gold repair, inputs), 1.5px (rare emphasis), 2px (focus ring max).

**Focus Ring:** `rgba(200,169,81,0.50)` gold, 2px solid, 3px offset, implementation: `box-shadow: 0 0 0 3px #F5F0E6, 0 0 0 5px rgba(200,169,81,0.50)`. Inner ring is washi bg for separation.

---

## Component Quick-Reference

### Primary Button
- **Rest:** bg `#3D5A80` Ai Indigo, color `#FBF8F1`, radius 6px, h 40px, padding `0 28px`, font button, no shadow
- **Hover:** bg `#34506F`, shadow-breath
- **Active:** bg `#2C4560`, scale(0.98)
- **Focus:** Gold focus ring
- **Transition:** 300ms contemplative

### Text Input
- **Rest:** bg `#FBF8F1`, border 1px at 15%, radius 6px, h 48px, caret-color `#C8A951` (gold caret)
- **Hover:** border at 25%
- **Focus:** border gold at 40%, shadow-breath-focus
- **Transition:** 400ms contemplative (border), 500ms contemplative (shadow)

### Card
- **Rest:** bg `#FBF8F1`, border 0.5px at 15%, radius 8px, shadow-breath, padding 24px
- **Hover:** border at 20%, shadow-breath-hover
- **Selected:** border-bottom 1px gold at 40% (repair line at base)
- **Transition:** 400ms contemplative (border), 500ms contemplative (shadow)

---

## Motion

**Easings:**
- **contemplative:** `cubic-bezier(0.22, 1, 0.36, 1)` — Primary easing, gentle deceleration
- **incense:** `cubic-bezier(0.12, 0.8, 0.3, 1)` — Very slow start, long tail (reveals, page entries)
- **settle:** `cubic-bezier(0.25, 0.1, 0.25, 1)` — Standard settle

**NO spring animations.** Every motion decelerates smoothly without oscillation.

**Key Durations:**
- Sidebar item: 300ms contemplative
- Button hover: 300ms contemplative
- Button press: 200ms settle
- Toggle: 350ms contemplative
- Card shadow hover: 500ms incense
- Input focus ring: 400ms contemplative
- Panel open/close: 600ms incense
- Modal enter: 800ms incense
- Page entry: 1000ms incense

**Active Press Scale:** Nav 0.99, Chips 0.99, Buttons 0.98, Tabs 0.98, Cards 0.995 (smaller than most themes — gentle feedback).

**Reduced Motion:** All durations cap at 200ms, spatial animations → opacity-only fades, all signature animations disabled, washi texture static.

---

## Layout

- **Content max-width:** 640px (~55 chars/line at 17px serif)
- **Narrow max-width:** 520px (journal entries, meditation prompts)
- **Sidebar width:** 240px (narrower than most themes)
- **Header height:** 56px (taller for breathing room)
- **Spacing unit:** 8px (larger base than typical 4px)
- **Spacing scale:** 8, 16, 24, 32, 48, 64, 96, 128px (most spacious in roster)
- **Density:** Very sparse. Content-to-whitespace 35:65 or lower. If layout feels full, remove elements or increase spacing — never decrease.

**Radius:** sm 4px, md 6px, lg 8px, xl 12px, 2xl 16px, full 9999px. Minimum 4px (no sharp corners).

**Responsive:** lg (1024px+) full sidebar, md (768px) sidebar → overlay, sm (640px) single column with 17px CJK body minimum, 24px card padding, 48px+ section spacing, 24px side padding minimum.

---

## Section Index (full.md line numbers)

1. [Identity & Philosophy](#identity--philosophy) — Line 77
2. [Color System](#color-system) — Line 99
3. [Typography Matrix](#typography-matrix) — Line 179
4. [Elevation System](#elevation-system) — Line 245
5. [Border System](#border-system) — Line 281
6. [Component States](#component-states) — Line 328
7. [Motion Map](#motion-map) — Line 453
8. [Overlays](#overlays) — Line 503
9. [Layout Tokens](#layout-tokens) — Line 555
10. [Accessibility Tokens](#accessibility-tokens) — Line 608
11. [Visual Style](#visual-style) — Line 647
12. [Signature Animations](#signature-animations) — Line 712
13. [Dark Mode Direction](#dark-mode-direction) — Line 825
14. [Mobile Notes](#mobile-notes) — Line 845
15. [Data Visualization](#data-visualization) — Line 875
16. [Theme-Specific CSS](#theme-specific-css-custom-properties) — Line 890
17. [Implementation Checklist](#implementation-checklist) — Line 965

---

**Decision Principle:** "Would this feel right in a 400-year-old tea house? If hurried → slow it. If crowded → add space. If decorative → remove it. If perfect → break it slightly."

**Core Identity:** Wabi-sabi aesthetic. Gold is structural repair only (never fill). Space (ma) is the design. Slowest theme in roster (300-1000ms). CJK-first typography. Content occupies <40% of viewport.
