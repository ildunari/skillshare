# Mashrabiya Matrix — Complete Theme Specification

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 38
- [Color System](#color-system) — Line 62
  - [Palette](#palette) — Line 64
  - [Special Tokens](#special-tokens) — Line 85
  - [Lattice Pattern System](#lattice-pattern-system) — Line 96
  - [Opacity System](#opacity-system) — Line 125
  - [Color Rules](#color-rules) — Line 138
- [Typography Matrix](#typography-matrix) — Line 150
  - [Font Stack](#font-stack) — Line 152
  - [RTL Typography Rules](#rtl-typography-rules) — Line 171
  - [Bidirectional Content Handling](#bidirectional-content-handling) — Line 192
  - [Typographic Decisions](#typographic-decisions) — Line 224
  - [Font Loading](#font-loading) — Line 235
- [Elevation System](#elevation-system) — Line 257
  - [Surface Hierarchy](#surface-hierarchy) — Line 266
  - [Shadow Tokens](#shadow-tokens) — Line 277
  - [Separation Recipe](#separation-recipe) — Line 288
- [Border System](#border-system) — Line 292
  - [Widths](#widths) — Line 294
  - [Opacity Scale](#opacity-scale-on-border-base-turab-dust) — Line 304
  - [Border Patterns](#border-patterns) — Line 316
  - [Focus Ring](#focus-ring) — Line 330
- [Component States](#component-states) — Line 344
  - [Buttons (Primary)](#buttons-primary) — Line 348
  - [Buttons (Ghost / Icon)](#buttons-ghost--icon) — Line 361
  - [Text Input](#text-input) — Line 374
  - [Chat Input Card](#chat-input-card) — Line 387
  - [Cards](#cards) — Line 397
  - [Sidebar Items](#sidebar-items) — Line 408
  - [Chips](#chips) — Line 420
  - [Toggle / Switch](#toggle--switch) — Line 430
  - [Slider](#slider) — Line 446
  - [Divider / Horizontal Rule](#divider--horizontal-rule) — Line 461
- [Motion Map](#motion-map) — Line 475
  - [Easings](#easings) — Line 477
  - [Duration x Easing x Component](#duration-x-easing-x-component) — Line 489
  - [Active Press Scale](#active-press-scale) — Line 511
- [Overlays](#overlays) — Line 521
  - [Popover / Dropdown](#popover--dropdown) — Line 523
  - [Modal](#modal) — Line 545
  - [Tooltip](#tooltip) — Line 563
- [Layout Tokens](#layout-tokens) — Line 577
  - [Spacing Scale](#spacing-scale) — Line 589
  - [Radius Scale](#radius-scale) — Line 606
  - [Density](#density) — Line 620
  - [Responsive Notes](#responsive-notes) — Line 624
  - [RTL Layout Rules](#rtl-layout-rules) — Line 630
- [Accessibility Tokens](#accessibility-tokens) — Line 650
- [Visual Style](#visual-style) — Line 701
- [Signature Animations](#signature-animations) — Line 740
  - [1. Lattice Unfold](#1-lattice-unfold) — Line 742
  - [2. Geometric Frieze Draw](#2-geometric-frieze-draw) — Line 767
  - [3. Star Rotation Reveal](#3-star-rotation-reveal) — Line 816
  - [4. Centripetal Gather](#4-centripetal-gather) — Line 838
  - [5. Tile Mosaic Build](#5-tile-mosaic-build) — Line 867
- [Dark Mode Variant](#dark-mode-variant) — Line 897
  - [Dark Palette](#dark-palette) — Line 901
  - [Dark Mode Rules](#dark-mode-rules) — Line 921
- [Mobile Notes](#mobile-notes) — Line 935
  - [Effects to Disable](#effects-to-disable) — Line 937
  - [Adjustments](#adjustments) — Line 946
  - [Performance Notes](#performance-notes) — Line 959
- [Data Visualization](#data-visualization) — Line 971
- [Theme-Specific CSS Custom Properties](#theme-specific-css-custom-properties) — Line 987
- [Implementation Checklist](#implementation-checklist) — Line 1076
  - [Core Setup](#core-setup) — Line 1078
  - [RTL-Specific (CRITICAL)](#rtl-specific-critical) — Line 1087
  - [Typography](#typography) — Line 1101
  - [Lattice Patterns](#lattice-patterns) — Line 1108
  - [Visual System](#visual-system) — Line 1116
  - [Motion & Interaction](#motion--interaction) — Line 1127
  - [Layout](#layout) — Line 1133
  - [Accessibility](#accessibility) — Line 1138
  - [Mobile](#mobile) — Line 1145

---

## 18. Mashrabiya Matrix

> Light filtered through geometric lattice -- bilateral symmetry, mathematical ornament, and the architecture of sacred pattern.

**Best for:** RTL-first applications, Arabic/Farsi/Hebrew content platforms, Islamic art galleries, architectural portfolios, calligraphy tools, geometric pattern generators, educational platforms for Middle Eastern studies, prayer time apps, cultural heritage archives, bilateral composition experiments.

---

### Identity & Philosophy

This theme lives in the world of the mashrabiya -- the carved wooden lattice screen found across Islamic architecture from Cairo to Isfahan. The mashrabiya is not decoration. It is functional engineering: it controls light, provides privacy, channels airflow, and creates breathtaking shadow patterns that shift throughout the day as the sun moves. Mathematics is ornament. Ornament is structure. The geometric patterns are derived from compass-and-straightedge construction, producing infinite tessellations from a finite set of rules.

The design is RTL-first. `direction: rtl` is the default document flow. This is not a LTR design with RTL bolted on -- it is conceived from right-to-left. Reading begins at the right margin. Sidebars anchor to the right. Progress fills from right to left. Navigation flows right-to-left. The LTR variant is the adaptation, not the other way around. This inversion is the theme's most radical design decision and the one most likely to be compromised. It must not be.

Bilateral symmetry governs composition. Where Kintsugi embraces asymmetry (fukinsei), Mashrabiya Matrix embraces mirrored balance. Content panels reflect across a central axis. Decorative borders mirror on both sides. The lattice pattern itself is bilaterally symmetric -- a star radiates equally in all directions. This symmetry is not static rigidity; it is the dynamic equilibrium of Islamic geometric art, where complexity emerges from the repetition and reflection of simple forms.

Light is the protagonist. The mashrabiya exists to transform light. Colors are drawn from what light does when passing through carved wood into interior spaces: warm sand tones where light lands, deep indigo shadows where it doesn't, and turquoise tile glints where reflected light catches glazed ceramic. The palette is architectural -- these are colors you would find in the Alhambra, the Blue Mosque, or the courtyards of Fez.

Pattern replaces shadow as the elevation strategy. Traditional UI elevation uses shadow depth to signal hierarchy. This theme uses geometric SVG lattice patterns instead. Higher-elevation surfaces have more intricate, tighter lattice overlays. The pattern is the shadow. A card's importance is communicated by the density and complexity of its lattice border, not by a drop shadow beneath it.

**Decision principle:** "When in doubt, ask: does this honor the geometry? If the pattern is broken, the design is broken. If the symmetry is violated without purpose, restore it. If the light is harsh rather than filtered, soften it through the lattice."

**What this theme is NOT:**

- Not decorative pastiche -- the geometric patterns are structural, derived from mathematical construction, not clip-art borders. Every pattern must be constructible with compass and straightedge.
- Not LTR-adapted -- this is RTL-native. If `direction: rtl` is absent from the root element, the implementation has fundamentally failed.
- Not maximalist -- the lattice creates visual richness through repetition of simple forms, not through accumulation of different elements. One star pattern, repeated and reflected, is the entire visual vocabulary.
- Not dark -- this is a light theme. The mashrabiya filters sunlight into interior spaces. The base is warm sand/ivory, bathed in filtered daylight.
- Not orientalist kitsch -- no arabesques as decoration, no crescent-moon icons, no faux-calligraphy. The theme draws from mathematical and architectural tradition, not Western fantasy of "the East."
- Not Western serif -- this is not Manuscript or Kintsugi. The typography is Arabic-first, the geometry is Islamic, the spatial logic is RTL.

---

### Color System

#### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Rimal (Sand) | `#F0E6D3` | L=0.93 C=0.03 h=78 | Deepest background. Desert sand ground, the floor of the courtyard seen through the lattice. |
| bg | Qashani (Plaster) | `#F5EDE0` | L=0.95 C=0.02 h=75 | Primary surface. Lime-washed plaster wall, warm and slightly textured. |
| surface | Jiss (Gypsum) | `#FAF5EC` | L=0.97 C=0.01 h=72 | Elevated cards, inputs, popovers. Bright carved gypsum panel -- the lightest material in the space. |
| recessed | Tafl (Clay) | `#E5DACA` | L=0.89 C=0.03 h=76 | Code blocks, inset areas. Unfired clay tone, slightly darker than the plaster wall. |
| active | Khashab (Wood) | `#D9CEBC` | L=0.85 C=0.03 h=74 | Active/pressed items, user bubbles. Carved cedarwood tone -- the material of the mashrabiya itself. |
| text-primary | Hibr (Ink) | `#1B2838` | L=0.22 C=0.04 h=250 | Headings, body text. Deep blue-black ink used in Arabic calligraphy manuscripts. |
| text-secondary | Ramadi (Ash) | `#5A6370` | L=0.46 C=0.02 h=240 | Sidebar items, secondary labels. Blue-grey, like shadow on plaster. |
| text-muted | Dabaab (Haze) | `#8A8F96` | L=0.61 C=0.01 h=240 | Placeholders, timestamps, metadata. Morning haze over the medina. |
| text-onAccent | Jiss (Gypsum) | `#FAF5EC` | L=0.97 C=0.01 h=72 | Text on accent-colored backgrounds. Bright gypsum white. |
| border-base | Turab (Dust) | `#B0A898` | L=0.72 C=0.02 h=70 | Base border color used at variable opacity. Dust-colored, warm grey. |
| accent-primary | Firuzaj (Turquoise Tile) | `#2A9D8F` | L=0.60 C=0.10 h=175 | Interactive elements, primary CTAs, links. Color of glazed zellige tilework. |
| accent-secondary | Lajward (Lapis Gold) | `#C9A84C` | L=0.73 C=0.12 h=85 | Highlights, active indicators, selected states. Lapis lazuli ground with gold leaf. |
| success | Zaytun (Olive) | `#5E8A5E` | L=0.55 C=0.08 h=140 | Positive states. Olive tree green from the courtyard garden. |
| warning | Zaafaran (Saffron) | `#C49A3A` | L=0.68 C=0.12 h=80 | Caution states. Saffron yellow, the costliest spice. |
| danger | Yaqut (Ruby) | `#9B3A3A` | L=0.42 C=0.12 h=22 | Error states. Ruby gemstone red. |
| info | Nili (Indigo) | `#3D5A8A` | L=0.43 C=0.08 h=250 | Informational states. Natural indigo dye from indigofera tinctoria. |

#### Special Tokens

| Token | Hex | Role |
|---|---|---|
| inlineCode | `#5A7A6A` | Code text within prose. Muted teal-grey, legible on sand surfaces. |
| toggleActive | `#2A9D8F` | Toggle/switch active track. Turquoise tile. |
| selection | `rgba(42, 157, 143, 0.15)` | `::selection` background. Turquoise at low opacity. |
| lattice-pattern | `#B0A898` | SVG lattice line color. Same as border-base for consistency. |
| lattice-pattern-gold | `rgba(201, 168, 76, 0.20)` | Gold lattice highlight for elevated surfaces. |
| lattice-shadow | `rgba(27, 40, 56, 0.04)` | Light shadow cast by lattice pattern on surfaces. |

#### Lattice Pattern System

The mashrabiya lattice is the visual signature of this theme. SVG geometric patterns serve dual roles: decorative borders and depth indicators. Pattern density communicates elevation.

| Usage | Pattern | Density | Opacity | Notes |
|---|---|---|---|---|
| Page background | 8-point star tessellation | Sparse (48px repeat) | 3% | Barely visible ground pattern across entire page |
| Card borders | Interlocking hexagon band | Medium (24px repeat) | 8% | 4px-wide strip along card edges |
| Elevated surfaces | 12-point star rosette | Dense (16px repeat) | 5% | Subtle overlay on popovers and modals |
| Section dividers | Linear geometric frieze | Single row (12px height) | 15% | Horizontal band replacing `<hr>` elements |
| Active/selected | Star-and-cross pattern | Medium (20px repeat) | 12% | Pattern fill on active backgrounds |
| Decorative frame | Octagon-and-square grid | Dense (12px repeat) | 6% | Frame border on hero sections and featured cards |

**Base SVG lattice (8-point star):**

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <path d="M24 0L30 12L42 6L36 18L48 24L36 30L42 42L30 36L24 48L18 36L6 42L12 30L0 24L12 18L6 6L18 12Z"
    fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.08"/>
</svg>
```

**Lattice anti-patterns (never do these):**
- Lattice pattern at opacity above 15% -- it becomes visual noise, not texture
- Non-geometric organic shapes passed off as "Islamic pattern" -- every pattern must be compass-constructible
- Lattice used as content background behind text -- it destroys readability. Lattice is for borders, frames, and decorative bands only
- Different pattern types mixed on the same surface -- one pattern per context
- Asymmetric lattice borders -- the left/right (or in RTL, right/left) borders must always mirror

#### Opacity System

Border opacity (on `border-base` Turab dust):

| Level | Opacity | Usage |
|---|---|---|
| whisper | 6% | Ghost borders, lattice ground pattern |
| subtle | 12% | Panel edges, card outlines at rest |
| card | 20% | Default card and content borders |
| hover | 30% | Hovered elements, interactive state |
| focus | 40% | Focused inputs, active delineation |
| lattice | 8% | Geometric pattern overlay on surfaces |

#### Color Rules

- No pure greys. Every neutral carries a warm sand-ivory undertone from the plaster/gypsum palette.
- Turquoise is the action color. It appears on interactive elements only: buttons, links, toggles, focus rings. It is the glazed tile that catches the eye in a field of sand and plaster.
- Lapis gold is the emphasis color. It marks selection, active states, and highlights. It is more restrained than turquoise -- gold leaf is precious and used sparingly.
- The page-to-surface gradient moves from warm-dark (sand) to warm-light (gypsum). Elevation = brightness, same principle as Kintsugi but with different material metaphors.
- Maximum two accent colors visible at any moment: turquoise + gold. Never turquoise + semantic color competing for attention.
- No gradients. Surfaces are flat plaster and gypsum. The only visual texture comes from the lattice SVG patterns.
- Indigo text creates depth contrast against the warm sand palette. Blue-black on warm ivory is a pairing found in Islamic manuscripts and Quran illumination.

---

### Typography Matrix

#### Font Stack

Playfair Display is the display typeface -- a transitional serif with elegant stroke contrast and high x-height, chosen for its ability to complement Arabic script aesthetics. The thick-thin stroke variation echoes the naskh calligraphic tradition where stroke width varies with pen angle. IBM Plex Sans Arabic is the body and UI typeface -- a high-quality Arabic sans-serif designed for digital screens, with proper RTL shaping, ligature support, and consistent metrics between Arabic and Latin glyphs. IBM Plex Mono handles code display. This is the ONLY theme where the body font is Arabic-first: the font-family declaration lists the Arabic font before Latin alternatives.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | serif (Playfair Display) | 36px | 700 | 1.3 | -0.01em | `font-feature-settings: "liga" 1, "kern" 1; font-optical-sizing: auto` | Hero titles, page names. Arabic display at 34px to account for wider glyphs. |
| Heading | serif (Playfair Display) | 24px | 600 | 1.4 | normal | `font-feature-settings: "liga" 1` | Section titles, settings headers |
| Subheading | serif (Playfair Display) | 19px | 500 | 1.5 | 0.01em | -- | Subsection labels |
| Body | sans (IBM Plex Sans Arabic) | 16px | 400 | 1.7 | normal | `font-feature-settings: "liga" 1, "kern" 1, "calt" 1` | Primary reading text. Arabic body text is the default; Latin text inherits the same sizing. |
| Body Arabic | sans (IBM Plex Sans Arabic) | 17px | 400 | 1.8 | 0.02em | `font-feature-settings: "liga" 1, "kern" 1, "calt" 1, "rlig" 1` | Arabic/Farsi/Urdu body text. Required ligatures enabled for proper Arabic shaping. |
| Body Small | sans (IBM Plex Sans Arabic) | 14px | 400 | 1.6 | normal | -- | Sidebar items, secondary UI text |
| Button | sans (IBM Plex Sans Arabic) | 14px | 500 | 1.4 | 0.02em | -- | Button labels. Arabic buttons use the same weight. |
| Input | sans (IBM Plex Sans Arabic) | 15px | 400 | 1.5 | normal | -- | Form input text. 15px for Arabic script readability in form fields. |
| Label | sans (IBM Plex Sans Arabic) | 12px | 500 | 1.4 | 0.04em | `text-transform: none` | Metadata, timestamps. Never uppercase -- Arabic script has no case distinction. |
| Code | mono (IBM Plex Mono) | 0.9em | 400 | 1.6 | normal | `font-feature-settings: "liga" 0; direction: ltr` | Inline code, code blocks. Code is ALWAYS LTR regardless of document direction. |
| Caption | sans (IBM Plex Sans Arabic) | 12px | 400 | 1.5 | 0.02em | -- | Disclaimers, footnotes |

#### RTL Typography Rules

RTL text requires specific handling that differs from LTR typography. This is the foundational difference of this theme.

| Property | LTR Value | RTL Value | Reason |
|---|---|---|---|
| `direction` | `ltr` (variant) | `rtl` (default) | Arabic, Hebrew, Farsi read right-to-left |
| `text-align` | `left` | `right` (or `start`) | Natural text alignment follows reading direction |
| Body line-height | 1.7 | 1.8 | Arabic glyphs with diacritics need extra vertical space |
| Minimum body size | 16px | 17px | Arabic connected script is harder to read at small sizes |
| `unicode-bidi` | normal | `embed` on mixed-content blocks | Ensures correct bidi algorithm for mixed Arabic/Latin text |
| `word-break` | normal | `normal` | Arabic word boundaries work correctly with default algorithm |
| `text-wrap` | `pretty` | `auto` | `text-wrap: pretty` is optimized for Latin line-break aesthetics |
| `hyphens` | auto | `none` | Arabic script does not hyphenate |
| Letter-spacing heading | -0.01em | 0 | Arabic connected script should not be letter-spaced (breaks ligatures) |
| Labels uppercase | permitted | NEVER | Arabic has no case distinction; `text-transform: uppercase` produces broken rendering |
| Padding direction | `padding-left` for indents | `padding-inline-start` always | Logical properties ensure correct spacing in both directions |
| Margin direction | `margin-right` for gaps | `margin-inline-end` always | Same reason. ALWAYS use logical properties (inline-start, inline-end, block-start, block-end). |
| Code blocks | direction: ltr | direction: ltr | Code is ALWAYS LTR even in RTL documents. Apply `dir="ltr"` explicitly on all `<code>` and `<pre>` elements. |
| Number rendering | default | `font-variant-numeric: tabular-nums` | Arabic-Indic numerals may render in some fonts; tabular-nums ensures consistent widths for data display |

#### Bidirectional Content Handling

Mixed Arabic-Latin content is common in technical and educational contexts. Rules for handling:

```css
/* Root document direction */
html[data-theme="mashrabiya"] {
  direction: rtl;
  unicode-bidi: isolate;
}

/* Code always LTR */
code, pre, kbd, samp, .code-block {
  direction: ltr;
  unicode-bidi: isolate;
  text-align: left;
}

/* Explicit LTR for Latin-only sections */
[dir="ltr"] {
  direction: ltr;
  text-align: left;
}

/* Numbers in data displays */
.data-value, .metric, .timestamp {
  direction: ltr;
  unicode-bidi: isolate;
  font-variant-numeric: tabular-nums;
}
```

#### Typographic Decisions

- IBM Plex Sans Arabic is listed first in the font stack because this is an Arabic-first theme. The font includes Latin glyphs that harmonize with its Arabic designs, so mixed content renders consistently.
- 17px body text is the minimum for Arabic script readability on screen. Connected Arabic letterforms at smaller sizes lose the joins between characters.
- 1.7-1.8 line-height accounts for Arabic diacritical marks (tashkeel) that extend above and below the baseline. Without generous line-height, vowel marks collide with adjacent lines.
- `-webkit-font-smoothing: antialiased` always. Critical for Arabic stroke rendering.
- Labels and metadata are NEVER uppercase. Arabic and Hebrew have no uppercase/lowercase distinction.
- Playfair Display is used for display/headings only. Its high stroke contrast complements the thick-thin variation of Arabic naskh calligraphy. For Arabic display text, consider substituting with a display Arabic face like Aref Ruqaa or Amiri if available.
- `font-feature-settings: "calt" 1, "rlig" 1` enables contextual alternates and required ligatures -- essential for correct Arabic text shaping where character forms change based on position (initial, medial, final, isolated).
- All CSS positioning uses logical properties (`inline-start`/`inline-end`) rather than physical properties (`left`/`right`). This ensures the entire layout flips correctly when switching between RTL and LTR modes.

#### Font Loading

```html
<!-- Mashrabiya Matrix Theme -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
```

**Fallback chains:**
- Display: `"Playfair Display", "Amiri", "Noto Serif", Georgia, serif`
- Body (Arabic-first): `"IBM Plex Sans Arabic", "Noto Sans Arabic", "Tahoma", "Segoe UI", system-ui, sans-serif`
- Body (Latin fallback): `"IBM Plex Sans", system-ui, sans-serif`
- Mono: `"IBM Plex Mono", "SFMono-Regular", Consolas, monospace`

**Arabic font loading notes:**
- IBM Plex Sans Arabic is a moderately-sized font file (~600KB for full Arabic+Latin coverage). Use `font-display: swap` to prevent FOIT.
- Preload the 400-weight Arabic font for above-the-fold body text.
- For Farsi/Persian content, IBM Plex Sans Arabic includes Farsi-specific glyph variants. Add `&subset=arabic,latin` for optimized payload.
- For Hebrew RTL support, add `IBM Plex Sans Hebrew` or `Heebo` to the font stack.
- Playfair Display does not include Arabic glyphs. For Arabic display text, fall back to Amiri (a beautiful Naskh display face available on Google Fonts).

---

### Elevation System

**Strategy:** `pattern-based` (unique to this theme)

The mashrabiya creates its own shadow. Traditional elevation via box-shadow is replaced by layered SVG lattice patterns that communicate depth through pattern density and complexity. A surface at higher elevation has a more intricate lattice overlay -- as if the viewer is looking through a more finely carved screen. This is not pure decoration: the pattern density is the elevation signal, replacing the shadow token entirely for most surfaces.

Minimal shadows are retained only for floating overlays (popovers, modals) where the element is genuinely detached from the page surface.

#### Surface Hierarchy

| Surface | Background | Pattern | Shadow | Usage |
|---|---|---|---|---|
| page | `#F0E6D3` Rimal | 8-point star at 3% opacity, 48px repeat | none | Deepest background. Desert sand with barely visible geometry. |
| qashani | `#F5EDE0` Qashani | None (clean plaster wall) | none | Primary content surface |
| jiss | `#FAF5EC` Jiss | Hexagonal lattice border band at 8%, 4px wide | `0 1px 4px rgba(27,40,56,0.03)` | Elevated cards, inputs. Named for carved gypsum. |
| tafl | `#E5DACA` Tafl | None | `inset 0 1px 2px rgba(27,40,56,0.03)` | Recessed areas, code blocks |
| overlay | `#FAF5EC` Jiss | 12-point rosette at 5%, 16px repeat as border frame | `0 4px 20px rgba(27,40,56,0.08)` | Popovers, dropdowns. Gold-tinted pattern border. |

#### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-none | `none` | Page background, flat surfaces |
| shadow-lattice | `0 1px 4px rgba(27,40,56,0.03)` | Cards at rest. Minimal warm shadow -- the lattice pattern does most of the elevation work. |
| shadow-lattice-hover | `0 2px 8px rgba(27,40,56,0.05)` | Card hover. Slightly deeper. |
| shadow-lattice-focus | `0 2px 8px rgba(27,40,56,0.05), 0 0 0 2px rgba(42,157,143,0.4)` | Input focus. Lattice shadow + turquoise ring. |
| shadow-overlay | `0 4px 20px rgba(27,40,56,0.08)` | Popovers, modals. The deepest shadow in the theme. |
| shadow-inset | `inset 0 1px 2px rgba(27,40,56,0.03)` | Recessed surfaces, code blocks |

#### Separation Recipe

Pattern-based elevation is the primary separation mechanism. Each surface level is distinguished by: (1) brightness stepping through the sand-to-gypsum color ramp, and (2) the presence and density of geometric lattice patterns. Cards sit on a brighter surface than the page and feature lattice-border bands along their edges. Recessed areas are slightly darker with inset shadow. Overlays get both pattern frames and the only substantial drop shadows in the theme. Borders are thin (0.5px) at low opacity -- they define edges that the lattice patterns ornament. Visual hierarchy = surface brightness + lattice pattern density + minimal shadow depth.

---

### Border System

#### Widths

| Name | Width | Usage |
|---|---|---|
| hairline | 0.5px | Standard border width for most elements. |
| default | 1px | Input borders, lattice pattern bands, section dividers. |
| medium | 1.5px | Emphasis borders, active indicators (rare). |
| heavy | 2px | Focus ring width. Maximum border weight. |
| lattice-band | 4px | Width of decorative lattice pattern border strips on cards and sections. |

#### Opacity Scale (on `border-base` Turab dust)

| Level | Opacity | Usage |
|---|---|---|
| whisper | 6% | Ghost borders, barely-there edges |
| subtle | 12% | Hairline edges, default panel borders |
| card | 20% | Standard card and content borders |
| hover | 30% | Hovered elements |
| focus | 40% | Focused inputs, active delineation |

#### Border Patterns

| Pattern | Width | Color/Opacity | Usage |
|---|---|---|---|
| whisper | 0.5px | border-base at 6% | Near-invisible edges |
| subtle | 0.5px | border-base at 12% | Standard panel outline |
| card | 0.5px | border-base at 20% | Card and content boundaries |
| hover | 0.5px | border-base at 30% | Hovered cards |
| input | 1px | border-base at 12% | Form input borders at rest |
| input-hover | 1px | border-base at 25% | Input hover state |
| input-focus | 1px | accent-primary (turquoise) at 40% | Input focus state -- turquoise replaces grey |
| lattice-frame | 4px | lattice-pattern at 8% | Geometric pattern border strip on cards |
| gold-active | 1px | accent-secondary (lapis gold) at 40% | Active/selected element accent border |
| divider-geometric | 1px | border-base at 15% + lattice SVG overlay | Section dividers with embedded geometric pattern |

#### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(42, 157, 143, 0.45)` -- turquoise tile |
| Width | 2px solid |
| Offset | 2px |
| Implementation | `box-shadow: 0 0 0 2px var(--bg), 0 0 0 4px rgba(42,157,143,0.45)` |

The focus ring is turquoise, matching the primary accent. The inner ring gap uses the `bg` plaster color to separate the turquoise indicator from the element surface. This is consistent with the turquoise-tile-as-action-color principle.

---

### Component States

All components use logical properties (`padding-inline-start`, `margin-inline-end`, `border-inline-start`, etc.) to ensure correct rendering in both RTL (default) and LTR modes.

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `#2A9D8F` (Firuzaj turquoise), border none, color `#FAF5EC`, radius 6px, h 36px, padding `0 20px`, font button (IBM Plex Sans Arabic, 14px, 500), shadow none |
| Hover | bg `#248F82` (darker turquoise), shadow shadow-lattice |
| Active | bg `#1E8175`, transform `scale(0.97)` |
| Focus | turquoise focus ring appended |
| Disabled | opacity 0.45, pointer-events none, cursor not-allowed, filter `grayscale(20%)` |
| Transition | background 150ms symmetric-ease, transform 100ms symmetric-ease |

Note: Primary buttons use turquoise -- the glazed tile color that signals action and interactivity throughout the theme.

#### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border none, color `#5A6370` (Ramadi), radius 6px, size 36x36px |
| Hover | bg `rgba(42,157,143,0.06)` (turquoise whisper), color `#1B2838` |
| Active | bg `rgba(42,157,143,0.12)`, transform `scale(0.97)` |
| Focus | turquoise focus ring |
| Disabled | opacity 0.45, pointer-events none |
| Transition | background 200ms symmetric-ease, color 150ms symmetric-ease |

Ghost buttons get the faintest turquoise warmth on hover -- like light catching a tile surface at a shallow angle.

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `#FAF5EC` (Jiss), border `1px solid rgba(176,168,152,0.12)`, radius 6px, h 44px, padding `0 14px`, shadow none, color `#1B2838`, placeholder `#8A8F96`, caret-color `#2A9D8F` (turquoise caret), `direction: inherit` |
| Hover | border at 25% opacity |
| Focus | border `1px solid rgba(42,157,143,0.4)` (turquoise), shadow shadow-lattice-focus, outline none |
| Disabled | opacity 0.45, bg `#E5DACA` (Tafl), pointer-events none, cursor not-allowed |
| Transition | border-color 200ms symmetric-ease, box-shadow 250ms symmetric-ease |

The text cursor (caret) is turquoise. The input inherits the document's `direction` value, so it naturally supports RTL text entry. For explicitly LTR inputs (e.g., email, URL), add `dir="ltr"` to the input element.

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `#FAF5EC`, radius 16px, border `0.5px solid rgba(176,168,152,0.12)`, shadow shadow-lattice, padding 18px, `direction: rtl` |
| Hover | border at 20%, shadow shadow-lattice-hover |
| Focus-within | border `0.5px solid rgba(42,157,143,0.25)`, shadow shadow-lattice-focus |
| Transition | all 250ms symmetric-ease |

#### Cards

| State | Properties |
|---|---|
| Rest | bg `#FAF5EC`, border `0.5px solid rgba(176,168,152,0.20)`, radius 8px, shadow shadow-lattice, padding 20px. Optional: 4px lattice-frame border band on top edge. |
| Hover | border at 30%, shadow shadow-lattice-hover |
| Selected | border-inline-start `2px solid rgba(201,168,76,0.5)` (gold active line on the start edge -- right side in RTL) |
| Transition | border-color 200ms symmetric-ease, box-shadow 250ms symmetric-ease |

Selected cards receive a gold border on the inline-start edge (right in RTL, left in LTR). This adapts the Kintsugi "gold repair line" concept to RTL context: the marking is always on the leading edge of the reading direction.

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `#5A6370` (Ramadi), radius 6px, h 36px, padding `6px 16px`, font bodySmall, `text-align: start` (right in RTL) |
| Hover | bg `rgba(42,157,143,0.05)`, color `#1B2838` |
| Active (current) | bg `rgba(42,157,143,0.08)`, color `#1B2838`, border-inline-start `2px solid #2A9D8F` (turquoise leading-edge bar) |
| Active press | transform `scale(0.985)` |
| Transition | color 150ms symmetric-ease, background 200ms symmetric-ease |

Active sidebar items get a turquoise bar on the inline-start edge -- in RTL, this is the right side, which is the leading visual edge.

#### Chips

| State | Properties |
|---|---|
| Rest | bg `#F5EDE0` (Qashani), border `0.5px solid rgba(176,168,152,0.12)`, radius 6px, h 32px, padding `0 12px`, font bodySmall, color `#5A6370` |
| Hover | bg `#F0E6D3` (Rimal), border at 20%, color `#1B2838` |
| Selected | bg `rgba(42,157,143,0.08)`, border `0.5px solid rgba(42,157,143,0.20)`, color `#1B2838` |
| Active press | transform `scale(0.995)` |
| Transition | all 150ms symmetric-ease |

#### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 40px |
| Track height | 22px |
| Track radius | 9999px |
| Track off bg | `rgba(176,168,152,0.20)` |
| Track off ring | `0.5px solid rgba(176,168,152,0.12)` |
| Track on bg | `#2A9D8F` (Firuzaj turquoise) |
| Thumb | 18px `#FAF5EC` circle (Jiss gypsum white) |
| Thumb shadow | `0 1px 2px rgba(27,40,56,0.06)` |
| Ring hover | thickens to 1px |
| Transition | 200ms symmetric-ease |
| Focus-visible | turquoise focus ring |
| RTL note | Toggle slides right-to-left for ON in RTL mode. `transform-origin` and animation direction flip. |

#### Slider

| Property | Value |
|---|---|
| Track height | 2px |
| Track color | `rgba(176,168,152,0.25)` (Turab at 25%) |
| Track filled | `rgba(42,157,143,0.6)` (turquoise thread) |
| Fill direction | Fills from `inline-end` to `inline-start` in RTL (right to left). In LTR, standard left-to-right. |
| Thumb | 14px circle, `#FAF5EC` fill, `1px solid rgba(42,157,143,0.4)` border |
| Thumb hover | border widens to 1.5px, bg gains `rgba(42,157,143,0.05)` |
| Thumb active | scale(1.1) |
| Value display | IBM Plex Mono, 12px, direction: ltr (numbers are always LTR) |
| Transition | 200ms symmetric-ease |

#### Divider / Horizontal Rule

| Property | Value |
|---|---|
| Height | 12px (taller than typical -- contains geometric pattern) |
| Content | SVG geometric frieze pattern (linear band of interlocking shapes) |
| Pattern opacity | 15% |
| Background | transparent (pattern only, no solid line) |
| Margin | 32px 0 |
| Width | 100% (bilateral symmetry -- dividers are always full-width, never asymmetric) |

Dividers are geometric pattern bands, not solid lines. They represent the lattice screen's horizontal register -- a frieze of interlocking geometric shapes that separates sections.

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| symmetric-ease | `cubic-bezier(0.4, 0, 0.2, 1)` | Primary easing. Balanced acceleration and deceleration. Named "symmetric" because it mirrors the bilateral symmetry principle. |
| unfold | `cubic-bezier(0.19, 1, 0.22, 1)` | Expo ease-out. For elements expanding/unfolding from center. Like a geometric pattern being drawn outward from its center point. |
| lattice-open | `cubic-bezier(0.12, 0.8, 0.3, 1)` | Long gentle deceleration. For the lattice pattern reveal animations. The pattern unfurls slowly. |
| settle | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Standard settle. For elements completing motion and resting at final position. |
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Fallback. Same as symmetric-ease. |

This theme has NO spring animations. Springs imply organic elasticity, which contradicts the geometric precision of Islamic pattern design. Every motion is mathematically smooth and symmetric -- a curve, not a bounce.

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 150ms | symmetric-ease | Clean state transition, moderate speed |
| Button hover bg | 150ms | symmetric-ease | Turquoise tile state change |
| Button active scale | 100ms | settle | Press feedback, fast |
| Toggle slide | 200ms | symmetric-ease | Thumb slides between states |
| Chip hover | 150ms | symmetric-ease | Background warmth shift |
| Card shadow on hover | 250ms | symmetric-ease | Shadow deepens moderately |
| Input focus ring | 200ms | symmetric-ease | Turquoise ring appears |
| Lattice pattern reveal | 600ms | lattice-open | Geometric pattern draws itself |
| Panel open/close | 400ms | unfold | Sidebar, overlay panels unfold |
| Modal enter | 350ms | unfold | Scale(0.96) to scale(1) + opacity |
| Modal exit | 250ms | symmetric-ease | Faster exit than enter |
| Hero/page entry | 500ms | unfold | Content expands from center |
| Popover appear | 200ms | symmetric-ease | Menu/dropdown entry |
| View transition | 400ms | unfold | Cross-fade between views |
| Scroll reveal | 500ms | lattice-open | Content revealed on scroll |
| Toast notification | 300ms | symmetric-ease | Slides in from inline-end edge |

Durations are moderate -- not as fast as technical themes (Pixel Grid), not as slow as contemplative themes (Kintsugi). The geometric precision of the theme demands motion that is deliberate but not ponderous. 150-500ms is the active range.

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Subtle press feedback |
| Chips | 0.995 | Barely perceptible |
| Buttons | 0.97 | Standard |
| Tabs | 0.95 | Pronounced |
| Cards (clickable) | 0.99 | Gentle on large surfaces |

---

### Overlays

#### Popover / Dropdown

| Property | Value |
|---|---|
| bg | `#FAF5EC` (Jiss gypsum) |
| border | `0.5px solid rgba(176,168,152,0.25)` |
| radius | 8px |
| shadow | shadow-overlay |
| backdrop-filter | `blur(16px)` |
| padding | 6px |
| z-index | 50 |
| min-width | 192px |
| max-width | 320px |
| direction | inherit (RTL by default) |
| Menu item | 6px 12px padding (using `padding-inline`), radius 6px, h 36px, font bodySmall, color text-secondary |
| Menu item hover | bg `rgba(42,157,143,0.05)`, color text-primary |
| Separator | 12px-high geometric frieze pattern at 10% opacity, margin 4px 0 |
| Transition | 200ms symmetric-ease |
| Menu item icon | Mirrors to inline-start position in RTL. Icons are always on the leading edge. |

#### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(27,40,56,0.25)` (warm indigo scrim) |
| Overlay backdrop-filter | `blur(8px)` |
| Content bg | `#FAF5EC` (Jiss) |
| Content border | `0.5px solid rgba(176,168,152,0.20)` + optional 4px lattice-frame border |
| Content shadow | shadow-overlay |
| Content radius | 12px |
| Content padding | 28px |
| Content direction | rtl (inherited) |
| Close button position | `inset-inline-start: 16px; inset-block-start: 16px` (top-left in RTL -- the end position, not the start) |
| Entry | opacity `0` to `1` + scale `0.96` to `1`, 350ms unfold |
| Exit | opacity `1` to `0` + scale `1` to `0.98`, 250ms symmetric-ease |

Modal entry uses centrifugal motion -- expanding from center outward (scale 0.96 to 1). This aligns with the lattice-open animation philosophy: patterns radiate from their center. The close button is positioned at `inset-inline-start` which places it at the top-left corner in RTL documents (the visual "end" position where close/dismiss actions live in RTL conventions).

#### Tooltip

| Property | Value |
|---|---|
| bg | `#1B2838` (Hibr ink) |
| color | `#F5EDE0` (Qashani plaster) |
| font | label size (12px), IBM Plex Sans Arabic |
| radius | 4px |
| padding | 6px 12px |
| shadow | `0 2px 6px rgba(27,40,56,0.10)` |
| No arrow | Position via offset |
| Entry | opacity fade, 200ms symmetric-ease |
| direction | inherit (respects document RTL) |

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column. Standard width for balanced readability. |
| Narrow max-width | 640px | Focused content, long-form reading. |
| Sidebar width | 280px | Fixed sidebar. Anchored to `inline-end` edge (right side in RTL). |
| Header height | 48px | Top bar. Standard height. |
| Spacing unit | 4px | Base multiplier. Standard 4px grid. |

#### Spacing Scale

4, 6, 8, 12, 16, 20, 24, 32, 48, 64px

A moderate spacing scale. Not as expansive as Kintsugi (which forbids gaps smaller than 8px), not as tight as terminal themes. The 4px base unit allows fine-grained control for the geometric pattern alignments.

| Context | Typical Gap | Notes |
|---|---|---|
| Between paragraphs | 20px | Comfortable reading rhythm |
| Between form fields | 24px | Clear field separation |
| Between cards | 16px | Cards in grid layouts |
| Between sections | 48-64px | Section breathing room |
| Card internal padding | 20px | Moderate internal space |
| Page edge padding | 24-32px | Content does not touch viewport edges |
| Between sidebar items | 4px | Tight grouping for navigation |
| Header to content | 24px | Clear but not excessive |

#### Radius Scale

| Token | Value | Usage |
|---|---|---|
| none | 0px | -- |
| sm | 4px | Badges, small elements |
| md | 6px | Sidebar items, menu items, buttons, inputs, chips |
| lg | 8px | Cards, panels |
| xl | 12px | Modals, large panels, popover containers |
| 2xl | 16px | Chat input card |
| full | 9999px | Toggles, avatars |

Radii are geometric but softened. Not sharp (geometric purity would demand 0px, but usability requires rounded corners). Not pill-shaped (this is architectural, not playful). 6px is the workhorse radius.

#### Density

Comfortable. Content-to-whitespace ratio targets 50:50. The bilateral symmetry means layouts feel structured and intentional without being either sparse or dense. The geometric patterns add visual richness without content density.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (280px, anchored inline-end/right in RTL) + content column (768px max). Bilateral symmetry visible in layout.
- **md (768px):** Sidebar collapses to overlay panel (slides in from inline-end edge). Content column fills available width with 24px side padding. Lattice pattern borders reduce to top-edge-only on cards.
- **sm (640px):** Single column. Body text stays 16px Latin / 17px Arabic minimum. Card internal padding reduces from 20px to 16px. Section spacing reduces from 48-64px to 32-48px. Lattice background pattern on page disabled (performance). Lattice-frame card borders disabled (visual simplification).

#### RTL Layout Rules

| Element | RTL Behavior | LTR Behavior |
|---|---|---|
| Sidebar | Anchored to right edge | Anchored to left edge |
| Sidebar collapse direction | Slides out to right | Slides out to left |
| Content text alignment | `text-align: right` (or `start`) | `text-align: left` (or `start`) |
| Active indicator bar | Right edge (`border-inline-start`) | Left edge (`border-inline-start`) |
| Progress bar fill | Fills right-to-left | Fills left-to-right |
| Toast slide direction | Slides in from right | Slides in from left |
| Breadcrumb separator | `\` (reversed) or auto via `dir` | `/` (standard) |
| Carousel direction | Swipe left = next | Swipe right = next |
| Close button (modal) | Top-left corner | Top-right corner |
| Back arrow | Points right `→` | Points left `←` |
| Checkbox/radio label | Label on left of input | Label on right of input |

ALL of these must use CSS logical properties (`inline-start`, `inline-end`) so that changing the `dir` attribute on the root element automatically flips the entire layout.

---

### Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring color | `rgba(42, 157, 143, 0.45)` (turquoise tile) |
| Focus ring width | 2px solid |
| Focus ring offset | 2px (inner ring: `var(--bg)` plaster color) |
| Disabled opacity | 0.45 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled filter | `grayscale(20%)` -- subtle desaturation signals inactive state beyond opacity |
| Selection bg | `rgba(42,157,143,0.15)` (turquoise at 15%) |
| Selection color | `#1B2838` (Hibr text-primary) |
| Scrollbar width | thin |
| Scrollbar thumb | `rgba(42,157,143,0.25)` (turquoise-tinted) |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

**Contrast verification:**
- `text-primary` (#1B2838) on `surface` (#FAF5EC): 13.8:1 -- exceeds AAA
- `text-secondary` (#5A6370) on `surface` (#FAF5EC): 5.1:1 -- meets AA
- `text-muted` (#8A8F96) on `surface` (#FAF5EC): 3.4:1 -- meets AA for large text. For normal text, use only for metadata/timestamps at 12px+. To meet strict AA for body text, darken to `#787E86`.
- `accent-primary` turquoise (#2A9D8F) on `surface` (#FAF5EC): 3.8:1 -- meets AA for large text/UI components. Not suitable for body text. For turquoise text on light surfaces, darken to `#1E7A6F` for 5.2:1.
- `text-onAccent` (#FAF5EC) on `accent-primary` (#2A9D8F): 3.8:1 -- meets AA for large text and UI components (buttons). For small text on turquoise, use `#FFFFFF` for 4.5:1.

**Reduced motion:**

| Behavior | Value |
|---|---|
| Strategy | `fade-only` -- all spatial animations collapse to simple opacity fades |
| Duration override | All durations cap at 150ms |
| Lattice pattern animation | Static (no reveal/draw) |
| Centripetal/centrifugal motion | Collapses to opacity fade only |
| Lattice unfold | Static -- patterns visible immediately |
| Geometric frieze animations | Static |
| Signature animations | All disabled |

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 150ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

### Visual Style

- **Material:** Plaster and carved gypsum on cedarwood lattice. The surfaces are architectural -- lime-washed plaster walls (smooth, matte, warm white) framed by carved wooden screens (the mashrabiya). Not paper, not fabric, not glass. The material language is masonry and woodwork.

- **Lattice Pattern Overlay:** The page background carries a subtle 8-point star tessellation at 3% opacity. This is the ground pattern -- the geometric grid that underlies the entire design, like the faint star pattern visible on a plaster wall when sunlight filters through a mashrabiya screen.

```css
.mashrabiya-page {
  background-color: var(--page);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 48 48'%3E%3Cpath d='M24 4L28 14L38 10L34 20L44 24L34 28L38 38L28 34L24 44L20 34L10 38L14 28L4 24L14 20L10 10L20 14Z' fill='none' stroke='%23B0A898' stroke-width='0.5' opacity='0.08'/%3E%3C/svg%3E");
  background-size: 48px 48px;
}
```

- **Lattice Border Bands:** Card borders feature a 4px-wide strip of geometric pattern rather than (or in addition to) a solid border line. This is implemented as a `border-image` or pseudo-element with a repeating SVG pattern:

```css
.mashrabiya-card::before {
  content: '';
  position: absolute;
  inset-block-start: 0;
  inset-inline: 0;
  height: 4px;
  background-image: url("data:image/svg+xml,..."); /* Geometric frieze SVG */
  background-repeat: repeat-x;
  background-size: 24px 4px;
  opacity: 0.12;
  border-radius: 8px 8px 0 0;
}
```

- **Bilateral Symmetry Enforcement:** Decorative elements (lattice borders, pattern bands, frame ornaments) are always bilaterally symmetric. If a pattern appears on the inline-start edge of a card, it must appear identically on the inline-end edge. This mirrors the mashrabiya screen itself, which is always carved as a symmetric panel.

- **Grain:** None. Plaster and gypsum are smooth materials, unlike Kintsugi's fibrous washi paper. The visual texture comes entirely from the geometric patterns, not from surface noise.
- **Gloss:** Matte. Lime-washed plaster absorbs light. Carved gypsum is chalky and flat. Zero sheen.
- **Blend mode:** `normal` for all elements. No multiply overlays (unlike Kintsugi's paper grain).
- **Shader bg:** False. SVG patterns only.

---

### Signature Animations

#### 1. Lattice Unfold

The signature entry animation. Elements appear by having their geometric lattice pattern "unfold" from a central point outward -- as if the wooden screen is being carved in real-time, starting from the center star and radiating outward to the edges. This is centrifugal motion: center to periphery.

```css
@keyframes lattice-unfold {
  0% {
    clip-path: circle(0% at 50% 50%);
    opacity: 0;
  }
  30% {
    opacity: 1;
  }
  100% {
    clip-path: circle(100% at 50% 50%);
    opacity: 1;
  }
}
.lattice-reveal {
  animation: lattice-unfold 600ms cubic-bezier(0.19, 1, 0.22, 1) both;
}
```

Duration: 600ms, easing: unfold. The circular clip-path expands from a point, revealing the content as if a geometric pattern is being drawn outward from its center. Reduced motion: 150ms opacity-only fade.

#### 2. Geometric Frieze Draw

Section dividers draw themselves into existence from center outward. The pattern band extends simultaneously to the left and right from the center point, creating bilateral symmetry in the animation itself. Uses two pseudo-elements scaling outward from center.

```css
@keyframes frieze-draw-right {
  from {
    transform: scaleX(0);
    transform-origin: left center;
  }
  to {
    transform: scaleX(1);
    transform-origin: left center;
  }
}
@keyframes frieze-draw-left {
  from {
    transform: scaleX(0);
    transform-origin: right center;
  }
  to {
    transform: scaleX(1);
    transform-origin: right center;
  }
}
.geometric-divider {
  position: relative;
  display: flex;
  justify-content: center;
}
.geometric-divider::before,
.geometric-divider::after {
  content: '';
  flex: 1;
  height: 12px;
  background-image: url("data:image/svg+xml,..."); /* Frieze pattern */
  background-repeat: repeat-x;
  opacity: 0.15;
}
.geometric-divider::before {
  animation: frieze-draw-left 500ms cubic-bezier(0.19, 1, 0.22, 1) both;
}
.geometric-divider::after {
  animation: frieze-draw-right 500ms cubic-bezier(0.19, 1, 0.22, 1) both;
}
```

Duration: 500ms, easing: unfold. Bilateral: both halves animate simultaneously, creating mirror-image motion. Reduced motion: pattern appears instantly.

#### 3. Star Rotation Reveal

Cards and interactive elements rotate their lattice pattern overlay by 45 degrees as they enter view. The 8-point star rotates to its final position, creating a kaleidoscopic settling effect. The rotation is subtle (just 45 degrees -- one-eighth of a full rotation, aligning with the star's octagonal symmetry).

```css
@keyframes star-rotate-reveal {
  from {
    opacity: 0;
    transform: rotate(45deg) scale(0.95);
  }
  to {
    opacity: 1;
    transform: rotate(0deg) scale(1);
  }
}
.star-reveal {
  animation: star-rotate-reveal 400ms cubic-bezier(0.19, 1, 0.22, 1) both;
}
```

Duration: 400ms, easing: unfold. The 45-degree rotation locks to the geometric grid -- it is not an arbitrary angle but exactly one-eighth turn, reflecting the 8-point star's rotational symmetry. Reduced motion: 150ms opacity-only fade.

#### 4. Centripetal Gather

Content blocks on page load animate from the four edges toward the center, like the points of a star converging. Cards slide inward: top items slide down, bottom items slide up, start-edge items slide toward center, end-edge items slide toward center. All arrive at the same time, converging on the central axis.

```css
@keyframes gather-from-top {
  from { opacity: 0; transform: translateY(-24px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes gather-from-bottom {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes gather-from-start {
  from { opacity: 0; transform: translateX(24px); } /* positive X = from right in RTL */
  to { opacity: 1; transform: translateX(0); }
}
@keyframes gather-from-end {
  from { opacity: 0; transform: translateX(-24px); } /* negative X = from left in RTL */
  to { opacity: 1; transform: translateX(0); }
}
.gather-top { animation: gather-from-top 500ms cubic-bezier(0.12, 0.8, 0.3, 1) both; }
.gather-bottom { animation: gather-from-bottom 500ms cubic-bezier(0.12, 0.8, 0.3, 1) both; }
.gather-start { animation: gather-from-start 500ms cubic-bezier(0.12, 0.8, 0.3, 1) both; }
.gather-end { animation: gather-from-end 500ms cubic-bezier(0.12, 0.8, 0.3, 1) both; }
```

Duration: 500ms per element, easing: lattice-open. Stagger: 80ms between groups. This creates centripetal motion -- everything converges toward center, the gravitational center of the geometric composition. Reduced motion: 150ms opacity-only fade.

#### 5. Tile Mosaic Build

Loading states and progress indicators use a mosaic-tile build animation. Small square cells fill in one by one in a spiral pattern from center outward, building a mosaic tile surface. Each cell is a small square of turquoise that fades to the correct content color once the content loads.

```css
@keyframes tile-build {
  0% {
    background-color: rgba(42, 157, 143, 0.15);
    opacity: 0;
  }
  40% {
    background-color: rgba(42, 157, 143, 0.15);
    opacity: 1;
  }
  100% {
    background-color: transparent;
    opacity: 1;
  }
}
.mosaic-cell {
  animation: tile-build 600ms cubic-bezier(0.4, 0, 0.2, 1) both;
}
/* Spiral stagger applied via CSS custom property */
.mosaic-cell { animation-delay: calc(var(--spiral-index) * 30ms); }
```

Duration: 600ms per cell, stagger: 30ms in spiral order, easing: symmetric-ease. The spiral builds outward from center, reinforcing the centrifugal principle. Reduced motion: all cells appear simultaneously with 150ms opacity fade.

---

### Dark Mode Variant

Mashrabiya Matrix is fundamentally a light theme -- sunlight filtering through the lattice into interior spaces. However, a dark variant explores **nighttime architecture**: the mashrabiya seen from outside at night, when interior lamplight filters outward through the lattice, casting geometric light patterns into the dark street.

#### Dark Palette

| Token | Light Value | Dark Value | Shift Notes |
|---|---|---|---|
| page | `#F0E6D3` Rimal | `#12161C` Midnight Indigo | Deep blue-black night sky over the medina |
| bg | `#F5EDE0` Qashani | `#1A1F28` Dark Plaster | Interior wall in lamplight shadow |
| surface | `#FAF5EC` Jiss | `#222933` Twilight Stone | Elevated surfaces glow slightly from lamplight |
| recessed | `#E5DACA` Tafl | `#0E1218` Deep Night | Deepest shadow within the lattice |
| active | `#D9CEBC` Khashab | `#2A3140` Active Stone | Pressed elements catch lamplight |
| text-primary | `#1B2838` Hibr | `#E8E2D8` Warm Lantern | Text becomes warm lantern-lit parchment |
| text-secondary | `#5A6370` Ramadi | `#9AA0AA` Moonstone | Secondary text lightens, retains blue-grey cool |
| text-muted | `#8A8F96` Dabaab | `#636870` Night Haze | Muted text, moderate contrast |
| border-base | `#B0A898` Turab | `#3A4050` Night Border | Borders darken substantially |
| accent-primary | `#2A9D8F` Firuzaj | `#35B5A5` Lit Turquoise | Turquoise brightens slightly for contrast on dark |
| accent-secondary | `#C9A84C` Lajward | `#D4B55A` Bright Gold | Gold brightens for visibility on dark surfaces |
| success | `#5E8A5E` Zaytun | `#6B9D6B` Night Olive | Lifted for readability |
| warning | `#C49A3A` Zaafaran | `#D4AA4A` Bright Saffron | Brightened |
| danger | `#9B3A3A` Yaqut | `#B54A4A` Bright Ruby | Brightened |

#### Dark Mode Rules

- Surfaces lighten with elevation (standard dark mode convention): page (darkest) < bg < surface (lightest)
- Shadows transform to subtle warm glows: `shadow-lattice` becomes `0 1px 4px rgba(42,157,143,0.04)` (turquoise tint glow)
- Lattice patterns increase in opacity from 3% to 5% on page background (patterns become more visible at night, like seeing the lattice silhouetted against interior light)
- Border opacity scale shifts: whisper 8% → 10%, subtle 12% → 15%, card 20% → 25% (borders need more presence on dark backgrounds)
- Gold lattice accents (`lattice-pattern-gold`) increase opacity from 20% to 30%
- Turquoise accent brightens to `#35B5A5` for minimum 3:1 contrast on dark surfaces
- Focus ring turquoise adjusts to `rgba(53,181,165,0.50)` for visibility
- Scrollbar thumb darkens: `rgba(53,181,165,0.20)` (less obtrusive on dark backgrounds)
- `backdrop-filter: blur()` values remain the same (blur works identically on dark backgrounds)
- Paper texture: none (dark mode has no material texture -- it is the open night air, not a surface)
- Character shift: from filtered-sunlight-interior to lamplight-through-lattice-at-night. The same mathematical patterns, but the light source reverses: light comes from inside and filters outward.

---

### Mobile Notes

#### Effects to Disable
- Page background lattice pattern SVG -- replace with solid color `var(--page)` for performance
- Lattice-frame card border bands (4px pattern strips) -- simplify to solid 0.5px border
- Lattice unfold signature animation (#1) -- use simple opacity fade
- Geometric frieze draw animation (#2) -- dividers appear instantly
- Centripetal gather animation (#4) -- use simple stagger fade
- Tile mosaic build animation (#5) -- use standard skeleton shimmer

#### Adjustments
- Arabic body text stays 17px minimum (Arabic script readability is non-negotiable, same principle as Kintsugi's CJK rule)
- Card internal padding reduces from 20px to 16px
- Section spacing reduces from 48-64px to 32-40px
- Chat input card radius reduces from 16px to 12px
- Side padding stays at 20px minimum
- Sidebar overlay width: 300px (wider for touch targets in RTL)
- All interactive elements maintain minimum 44px touch target
- Header height stays 48px
- Scrollbar styling removed (native mobile scrolling)
- Turquoise focus rings remain (accessibility on mobile)
- RTL direction MUST be maintained on mobile -- do not switch to LTR on smaller viewports

#### Performance Notes
- SVG lattice pattern on page background is the main performance concern on mobile. Replace with solid color.
- The geometric pattern SVGs are small (~200 bytes each) but repeating patterns at high density can cause rendering jank on older mobile GPUs. Reduce pattern density on surfaces that scroll.
- `backdrop-filter: blur()` on modals only. Remove on popovers if performance suffers.
- IBM Plex Sans Arabic is ~600KB. Use `font-display: swap` and preload the 400-weight for body text.
- Signature animations use `clip-path` which is GPU-accelerated in modern browsers but should be disabled on mobile for safety.
- Total animation budget on mobile: 1 concurrent transition. Queue rather than overlap.
- `will-change: transform, opacity` only during active animations, never permanent.

---

### Data Visualization

| Property | Value |
|---|---|
| Categorical palette | `#2A9D8F` (Turquoise), `#C9A84C` (Gold), `#3D5A8A` (Indigo), `#5E8A5E` (Olive), `#9B3A3A` (Ruby) -- 5 colors max |
| Sequential ramp | Single-hue turquoise: `#D0EDE9` to `#2A9D8F` to `#1A5F57` |
| Diverging ramp | Olive green to sand to ruby: `#5E8A5E` to `#F5EDE0` to `#9B3A3A` |
| Grid lines | Low-ink: `border-base` at 6% opacity. Nearly invisible geometric grid. |
| Max hues per chart | 3 (prefer 2) |
| Philosophy | Geometric clarity. Clean axis lines. Data rendered with the precision of geometric construction. |
| Axis labels | IBM Plex Sans Arabic, 12px, text-secondary color, `direction: ltr` for numeric axes |
| Value labels | IBM Plex Mono, 12px, text-primary color, `direction: ltr` |
| RTL chart note | Y-axis labels on the RIGHT side of the chart in RTL mode. Time-series x-axes read right-to-left (most recent = left, oldest = right). |

---

### Theme-Specific CSS Custom Properties

```css
:root[data-theme="mashrabiya"],
html[dir="rtl"][data-theme="mashrabiya"] {
  /* Document direction */
  direction: rtl;
  unicode-bidi: isolate;

  /* Core surfaces */
  --page: #F0E6D3;
  --bg: #F5EDE0;
  --surface: #FAF5EC;
  --recessed: #E5DACA;
  --active: #D9CEBC;

  /* Text */
  --text-primary: #1B2838;
  --text-secondary: #5A6370;
  --text-muted: #8A8F96;
  --text-on-accent: #FAF5EC;

  /* Accents */
  --accent-primary: #2A9D8F;
  --accent-primary-hover: #248F82;
  --accent-primary-active: #1E8175;
  --accent-secondary: #C9A84C;

  /* Lattice system */
  --lattice-color: #B0A898;
  --lattice-gold: rgba(201, 168, 76, 0.20);
  --lattice-shadow: rgba(27, 40, 56, 0.04);

  /* Semantics */
  --success: #5E8A5E;
  --warning: #C49A3A;
  --danger: #9B3A3A;
  --info: #3D5A8A;

  /* Borders */
  --border-base: #B0A898;
  --border-whisper: rgba(176, 168, 152, 0.06);
  --border-subtle: rgba(176, 168, 152, 0.12);
  --border-card: rgba(176, 168, 152, 0.20);
  --border-hover: rgba(176, 168, 152, 0.30);
  --border-focus: rgba(176, 168, 152, 0.40);

  /* Focus */
  --focus-ring: 0 0 0 2px var(--bg), 0 0 0 4px rgba(42, 157, 143, 0.45);

  /* Shadows */
  --shadow-lattice: 0 1px 4px rgba(27, 40, 56, 0.03);
  --shadow-lattice-hover: 0 2px 8px rgba(27, 40, 56, 0.05);
  --shadow-lattice-focus: 0 2px 8px rgba(27, 40, 56, 0.05), 0 0 0 2px rgba(42, 157, 143, 0.4);
  --shadow-overlay: 0 4px 20px rgba(27, 40, 56, 0.08);
  --shadow-inset: inset 0 1px 2px rgba(27, 40, 56, 0.03);

  /* Motion */
  --ease-symmetric: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-unfold: cubic-bezier(0.19, 1, 0.22, 1);
  --ease-lattice-open: cubic-bezier(0.12, 0.8, 0.3, 1);
  --ease-settle: cubic-bezier(0.25, 0.1, 0.25, 1);
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-medium: 300ms;
  --duration-slow: 500ms;
  --duration-reveal: 600ms;

  /* Layout */
  --content-max-width: 768px;
  --narrow-max-width: 640px;
  --sidebar-width: 280px;
  --header-height: 48px;
  --spacing-unit: 4px;

  /* Typography */
  --font-display: "Playfair Display", "Amiri", "Noto Serif", Georgia, serif;
  --font-body: "IBM Plex Sans Arabic", "Noto Sans Arabic", "Tahoma", system-ui, sans-serif;
  --font-body-latin: "IBM Plex Sans", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;

  /* Special */
  --inline-code-color: #5A7A6A;
  --selection-bg: rgba(42, 157, 143, 0.15);
  --scrollbar-thumb: rgba(42, 157, 143, 0.25);
  --caret-color: #2A9D8F;
}
```

---

### Implementation Checklist

#### Core Setup
- [ ] `direction: rtl` set on `<html>` or root element as the DEFAULT document direction
- [ ] `unicode-bidi: isolate` on root element for proper bidirectional text handling
- [ ] Google Fonts loaded: IBM Plex Sans Arabic (400, 500, 600), Playfair Display (500, 600, 700 + italic), IBM Plex Mono (400)
- [ ] `-webkit-font-smoothing: antialiased` on root element
- [ ] `text-wrap: auto` for Arabic content (not `pretty`, which is Latin-optimized)
- [ ] CSS custom properties defined for all color tokens including lattice system

#### RTL-Specific (CRITICAL)
- [ ] ALL CSS positioning uses logical properties: `inline-start`/`inline-end` instead of `left`/`right`, `block-start`/`block-end` instead of `top`/`bottom` (for directional contexts)
- [ ] `padding-inline-start`/`padding-inline-end` instead of `padding-left`/`padding-right` everywhere
- [ ] `margin-inline-start`/`margin-inline-end` instead of `margin-left`/`margin-right` everywhere
- [ ] `border-inline-start` for active indicator bars (appears on right in RTL)
- [ ] `inset-inline-start`/`inset-inline-end` for absolute positioning
- [ ] `text-align: start` instead of `text-align: left`
- [ ] Sidebar anchored to `inline-end` (right side in RTL)
- [ ] Code blocks explicitly set to `direction: ltr` with `dir="ltr"` attribute
- [ ] Number/data displays set to `direction: ltr` with `unicode-bidi: isolate`
- [ ] `transform: scaleX(-1)` applied to directional icons (arrows, chevrons) that need to flip in RTL
- [ ] Progress bars and sliders fill from `inline-end` to `inline-start` in RTL
- [ ] `text-transform: uppercase` NEVER used (Arabic has no case)

#### Typography
- [ ] IBM Plex Sans Arabic listed FIRST in body font-family stack (Arabic-first)
- [ ] Arabic body text at 17px minimum
- [ ] Arabic body line-height at 1.8 (accounts for diacritical marks)
- [ ] `font-feature-settings: "liga" 1, "kern" 1, "calt" 1, "rlig" 1` on Arabic text for proper shaping
- [ ] `hyphens: none` for Arabic content (Arabic does not hyphenate)
- [ ] `word-break: normal` for Arabic content

#### Lattice Patterns
- [ ] Page background 8-point star SVG pattern at 3% opacity implemented
- [ ] Card lattice-frame border bands at 8% opacity on card top edges
- [ ] Geometric frieze pattern for section dividers at 15% opacity
- [ ] All lattice borders are bilaterally symmetric
- [ ] Lattice pattern opacity never exceeds 15% on any surface

#### Visual System
- [ ] Turquoise focus ring (`rgba(42,157,143,0.45)`) on all interactive elements
- [ ] Turquoise caret on text inputs (`caret-color: var(--caret-color)`)
- [ ] Gold (`accent-secondary`) used only for emphasis/selected states, not primary actions
- [ ] Border-radius 6px for standard interactive elements, 8px for cards, 12px for modals
- [ ] Shadow tokens applied: shadow-lattice at rest, shadow-lattice-hover on hover
- [ ] Border opacity system implemented: whisper/subtle/card/hover/focus at 6/12/20/30/40%
- [ ] `::selection` styled with turquoise at 15% opacity
- [ ] `::placeholder` color matches `text-muted` token
- [ ] Scrollbar thumb uses turquoise tint, transparent track

#### Motion & Interaction
- [ ] `prefers-reduced-motion` media query: all durations cap at 150ms, spatial animations collapse to opacity-only fades
- [ ] No spring animations (geometric precision demands smooth curves only)
- [ ] Centrifugal/centripetal signature animations implemented where applicable
- [ ] All transitions use symmetric-ease or unfold easings

#### Layout
- [ ] Content max-width 768px, sidebar 280px anchored inline-end
- [ ] Spacing scale based on 4px unit
- [ ] Touch targets >= 44px on all interactive elements

#### Accessibility
- [ ] WCAG AA contrast verified for all text tokens on all surface tokens
- [ ] Focus indicators visible on all interactive elements (turquoise ring)
- [ ] Disabled states include opacity + pointer-events + cursor + filter
- [ ] `lang` attribute set appropriately (`ar`, `fa`, `he`, `en`) for proper screen reader pronunciation
- [ ] Keyboard navigation flows correctly in RTL (Tab moves right-to-left through focusable elements)

#### Mobile
- [ ] Lattice SVG patterns disabled or simplified on mobile
- [ ] Arabic 17px body text preserved on all viewports
- [ ] Signature clip-path animations disabled on mobile
- [ ] RTL direction maintained on all viewport sizes (NEVER switch to LTR on mobile)
