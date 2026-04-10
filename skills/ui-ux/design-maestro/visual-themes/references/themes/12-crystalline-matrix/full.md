# Crystalline Matrix — Full Reference

<!-- Table of Contents -->

## Table of Contents

| Section | Line |
|---------|------|
| [Identity & Philosophy](#identity--philosophy) | 55 |
| [Color System](#color-system) | 69 |
| [Palette](#palette) | 71 |
| [Prismatic Border System](#prismatic-border-system) | 96 |
| [Special Colors](#special-colors) | 151 |
| [Fixed Colors](#fixed-colors) | 162 |
| [Opacity System](#opacity-system) | 169 |
| [Color Rules](#color-rules) | 180 |
| [Typography Matrix](#typography-matrix) | 193 |
| [Font Families](#font-families) | 195 |
| [Role Matrix](#role-matrix) | 207 |
| [Font Loading](#font-loading) | 225 |
| [Elevation System](#elevation-system) | 239 |
| [Surface Hierarchy](#surface-hierarchy) | 245 |
| [Shadow Tokens](#shadow-tokens) | 257 |
| [Facet Rendering Tokens](#facet-rendering-tokens) | 273 |
| [Wireframe Overlay Pattern](#wireframe-overlay-pattern) | 313 |
| [Backdrop Filter](#backdrop-filter) | 337 |
| [Separation Recipe](#separation-recipe) | 345 |
| [Border System](#border-system) | 349 |
| [Base Color](#base-color) | 351 |
| [Widths and Patterns](#widths-and-patterns) | 355 |
| [Width Scale](#width-scale) | 367 |
| [Focus Ring](#focus-ring) | 375 |
| [Component States](#component-states) | 388 |
| [Buttons (Primary)](#buttons-primary) | 390 |
| [Buttons (Accent/CTA)](#buttons-accentcta) | 400 |
| [Buttons (Ghost/Icon)](#buttons-ghosticon) | 412 |
| [Text Input (Settings Form)](#text-input-settings-form) | 424 |
| [Textarea](#textarea) | 437 |
| [Chat Input Card](#chat-input-card) | 446 |
| [Cards](#cards) | 457 |
| [Sidebar Items](#sidebar-items) | 467 |
| [Section Labels (Sidebar)](#section-labels-sidebar) | 479 |
| [Chips (Quick Actions)](#chips-quick-actions) | 491 |
| [Toggle/Switch](#toggleswitch) | 503 |
| [User Message Bubble](#user-message-bubble) | 517 |
| [Motion Map](#motion-map) | 533 |
| [Easings](#easings) | 535 |
| [Duration x Easing x Component](#duration-x-easing-x-component) | 547 |
| [Active Press Scale](#active-press-scale) | 570 |
| [Reduced Motion](#reduced-motion) | 577 |
| [Overlays](#overlays) | 591 |
| [Popover/Dropdown](#popoverdropdown) | 593 |
| [Modal](#modal) | 611 |
| [Tooltip](#tooltip) | 626 |
| [Layout Tokens](#layout-tokens) | 644 |
| [Spacing Scale](#spacing-scale) | 656 |
| [Density](#density) | 676 |
| [Responsive Notes](#responsive-notes) | 680 |
| [Accessibility Tokens](#accessibility-tokens) | 699 |
| [Visual Style](#visual-style) | 734 |
| [Material](#material) | 736 |
| [The Faceted Rendering Technique](#the-faceted-rendering-technique-full-reference) | 745 |
| [Wireframe Overlay Guidelines](#wireframe-overlay-guidelines) | 807 |
| [Rendering Guidelines](#rendering-guidelines) | 817 |
| [Signature Animations](#signature-animations) | 827 |
| [1. Facet Rotation (Ambient)](#1-facet-rotation-ambient) | 829 |
| [2. Light-Catch Sparkle (Vertex Highlight)](#2-light-catch-sparkle-vertex-highlight) | 868 |
| [3. Crystal Growth (Element Entry)](#3-crystal-growth-element-entry) | 911 |
| [4. Symmetric Mirror (Bilateral Entry)](#4-symmetric-mirror-bilateral-entry) | 950 |
| [5. Prismatic Border Sweep (Interaction Feedback)](#5-prismatic-border-sweep-interaction-feedback) | 981 |
| [Dark Mode Variant](#dark-mode-variant) | 1020 |
| [Dark Mode Palette](#dark-mode-palette) | 1025 |
| [Dark Mode Rules](#dark-mode-rules) | 1041 |
| [Data Visualization](#data-visualization) | 1055 |
| [Mobile Notes](#mobile-notes) | 1070 |
| [Effects to Disable](#effects-to-disable) | 1072 |
| [Sizing Adjustments](#sizing-adjustments) | 1083 |
| [Performance Notes](#performance-notes) | 1093 |
| [Implementation Checklist](#implementation-checklist) | 1103 |

---

## Identity & Philosophy

This theme lives inside a diamond. Not the gemstone on a ring -- the interior of a crystal lattice, where light enters through one facet, refracts through the molecular structure, and exits as prismatic spectra at every geometric edge. The world is cold, precise, and mathematical. Every surface is a crystal face -- flat, angular, subtly catching light at different angles. The wireframe overlay reveals the underlying structure, the scaffolding of geometry that gives form to the crystal.

The core tension is **precision vs prismatic chaos**. The palette is overwhelmingly monochrome: crystal whites, platinum greys, graphite depths. But at facet edges -- where surfaces meet, where borders define geometry -- prismatic rainbow spectra appear. This is not decorative color. It is structural color, the kind that exists only at boundaries. A `conic-gradient` rainbow appears on borders, not on surfaces. The rainbow is the reward for geometric precision, not a decoration applied to it.

Two registers define the theme's character. **Faceted surfaces** simulate crystal faces through subtle angular gradients -- each card, panel, and container has a faint directional gradient suggesting it is one face of a polyhedron. The angle varies between surfaces to suggest different facet orientations. **Wireframe overlays** use thin platinum lines to reveal structural relationships -- grid lines, connection paths, and geometric scaffolding that appear at reduced opacity, lending depth and mathematical authority.

**Decision principle:** "When in doubt, ask: does this look like it was computed? If it looks organic, hand-drawn, or warm, reject it. If it looks like a diagram rendered by a geometry engine, accept it."

**What this theme is NOT:**
- Not warm or organic -- this is cold, computed, crystallographic
- Not colorful -- the rainbow is structural and appears only at geometric edges; surfaces are monochrome
- Not glassy or glassmorphic -- crystal is opaque and faceted, not transparent and blurred
- Not rounded or soft -- geometry is angular; large border-radius is prohibited
- Not decorative -- wireframe overlays and prismatic borders serve structural communication, never ornamentation
- Not dark-native -- the base is a bright crystal white with graphite depth; it is a light theme with dark mode variant
- Not the same as Ethereal Porcelain (which is cool gallery, subsurface warmth) -- Crystalline Matrix is cold geometry, prismatic edges
- No gradients on surface fills -- surfaces are flat crystal faces. Gradients exist only on borders (prismatic) and as the subtle facet-angle effect

---

## Color System

### Palette

All neutrals carry a cool blue-grey undertone with zero chroma, like colorless crystal. The accent is a prismatic conic-gradient applied to borders, not a single-hue accent. When a single accent color is required (e.g., CTA buttons, active states), a cool sapphire blue is used -- the dominant wavelength when white light enters a crystal.

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Crystal Base | `#EAEDF0` | L=93.2 C=0.008 h=250 | Deepest background -- the crystal mass. Cool blue-white, like looking into the body of a clear quartz. |
| bg | Frost | `#F0F2F4` | L=95.0 C=0.006 h=250 | Primary surface background. A step lighter. The polished outer face of the crystal. |
| surface | Facet White | `#F7F8FA` | L=97.2 C=0.005 h=250 | Cards, inputs, elevated surfaces. The brightest facet -- the face that catches direct light. |
| recessed | Matrix Grey | `#E2E5E9` | L=90.8 C=0.009 h=250 | Code blocks, inset areas. Slightly darker, like a facet angled away from the light source. |
| active | Lattice Silver | `#D5D9DE` | L=87.0 C=0.010 h=250 | Active/pressed states, selected items. The facet in shadow. Noticeably cooler. |
| text-primary | Graphite | `#1A1D21` | L=16.0 C=0.008 h=250 | Headings, body text. Near-black with a cool steel undertone. Never warm, never pure black. |
| text-secondary | Platinum Grey | `#5C636E` | L=44.0 C=0.015 h=250 | Sidebar items, secondary labels. Cool mid-grey like brushed platinum. |
| text-muted | Wire Silver | `#8E95A0` | L=62.0 C=0.015 h=250 | Placeholders, timestamps, metadata. The color of a thin wireframe line. |
| text-onAccent | Crystal White | `#F7F8FA` | L=97.2 C=0.005 h=250 | Text on accent-colored backgrounds. Matches facet white. |
| border-base | Wireframe Platinum | `#A0A8B4` | L=69.0 C=0.018 h=250 | Base border color, applied at variable opacity. The wireframe line color. |
| accent-primary | Sapphire | `#3B6FD4` | L=50.0 C=0.140 h=260 | Primary CTA. Cool blue -- the dominant refracted wavelength. Used sparingly. |
| accent-secondary | Amethyst | `#7B5EA7` | L=46.0 C=0.120 h=300 | Secondary accent. Violet spectrum -- the complementary refraction. Links, secondary actions. |
| accent-rgb | -- | `59, 111, 212` | -- | RGB decomposition of accent-primary for use in rgba() calculations. |
| success | Emerald Facet | `#2D8B5E` | L=52.0 C=0.110 h=155 | Positive states. Cool green, like an emerald crystal inclusion. |
| warning | Citrine | `#B8902D` | L=62.0 C=0.130 h=80 | Caution states. Yellow topaz -- geometric, not organic. |
| danger | Ruby Flaw | `#C44040` | L=48.0 C=0.150 h=25 | Error states. A flaw in the crystal structure. Desaturated enough to not alarm. |
| info | Ice Blue | `#4A90C4` | L=56.0 C=0.100 h=240 | Informational states. Clear blue like aquamarine. |

### Prismatic Border System

The signature visual. Prismatic rainbow appears only at geometric edges -- borders, dividers, and structural lines. Never on surfaces.

| Token | Value | Usage |
|---|---|---|
| prismatic-gradient | `conic-gradient(from 0deg, #C44040, #B8902D, #2D8B5E, #4A90C4, #3B6FD4, #7B5EA7, #C44040)` | Full-spectrum prismatic border. Used via `border-image` or `background` on pseudo-elements. |
| prismatic-subtle | `conic-gradient(from 0deg, rgba(196,64,64,0.15), rgba(184,144,45,0.15), rgba(45,139,94,0.15), rgba(74,144,196,0.15), rgba(59,111,212,0.15), rgba(123,94,167,0.15), rgba(196,64,64,0.15))` | Subdued prismatic for resting state borders. Structural rainbow at whisper intensity. |
| prismatic-active | `conic-gradient(from 0deg, rgba(196,64,64,0.35), rgba(184,144,45,0.35), rgba(45,139,94,0.35), rgba(74,144,196,0.35), rgba(59,111,212,0.35), rgba(123,94,167,0.35), rgba(196,64,64,0.35))` | Intensified prismatic for hover/focus borders. The crystal catches more light. |

**Prismatic border implementation pattern:**

```css
/* Prismatic border via pseudo-element + mask */
.prismatic-border {
  position: relative;
  border: none;
  background: var(--surface);
}

.prismatic-border::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  background: conic-gradient(
    from 0deg,
    rgba(196,64,64,0.12),
    rgba(184,144,45,0.12),
    rgba(45,139,94,0.12),
    rgba(74,144,196,0.12),
    rgba(59,111,212,0.12),
    rgba(123,94,167,0.12),
    rgba(196,64,64,0.12)
  );
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  padding: 1px;
  pointer-events: none;
  transition: opacity 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.prismatic-border:hover::before {
  background: conic-gradient(
    from 0deg,
    rgba(196,64,64,0.28),
    rgba(184,144,45,0.28),
    rgba(45,139,94,0.28),
    rgba(74,144,196,0.28),
    rgba(59,111,212,0.28),
    rgba(123,94,167,0.28),
    rgba(196,64,64,0.28)
  );
}
```

### Special Colors

| Token | Value | Role |
|---|---|---|
| inlineCode | `#4A5568` | Code text within prose -- cool graphite, reads as "computed output" against the crystal surface. |
| toggleActive | `#3B6FD4` | Toggle/switch active track. Sapphire accent. |
| selection | `rgba(59, 111, 212, 0.14)` | `::selection` background. Sapphire at 14% opacity. Cool crystal highlight. |
| wireframeOverlay | `rgba(160, 168, 180, 0.08)` | Wireframe grid line color for structural overlays. Near-invisible geometry. |
| facetHighlight | `rgba(255, 255, 255, 0.5)` | Top-edge highlight simulating light catching a crystal facet edge. |
| facetShadow | `rgba(26, 29, 33, 0.03)` | Bottom-edge shadow simulating a facet angled away from light. |

### Fixed Colors

| Token | Hex | Role |
|---|---|---|
| alwaysBlack | `#000000` | Shadow base (mode-independent) |
| alwaysWhite | `#FFFFFF` | On-dark emergencies only (mode-independent) |

### Opacity System

One border base color (`#A0A8B4` Wireframe Platinum) at variable opacity produces the standard border vocabulary. The prismatic system overlays on top for accent edges.

| Level | Opacity | Usage |
|---|---|---|
| subtle | 10% | Sidebar edges, wireframe grid lines, lightest structural lines. Crystal prefers minimal visible boundaries -- structure is felt through facet angles. |
| card | 18% | Card borders (when not using prismatic). Restrained -- the facet angle gradient defines the surface, not the border. |
| hover | 26% | Hover states, popover borders. |
| focus | 36% | Focus borders, active emphasis. |

### Color Rules

- **Rainbow is structural.** Prismatic gradient appears only at borders, edges, and dividers -- never as a surface fill, never as background tint. The rainbow exists because of geometry, not decoration.
- **Monochrome dominates.** The palette is 90% cool grey/white and 10% spectral accent. If a screen reads as "colorful," something is wrong.
- **Sapphire is the default accent.** When a single color is needed (CTA, links, active toggles), use the sapphire blue -- the brightest wavelength from the prismatic split.
- **No warm tones on surfaces.** Every surface carries a cool blue-grey undertone. Warm colors exist only in the prismatic border and semantic states.
- **Facet angles vary.** Each card surface should have a slightly different linear-gradient angle (using `facetHighlight` and `facetShadow` at very low opacity) to suggest different crystal face orientations. Angles: 165deg, 170deg, 175deg, 180deg -- small variations only.
- **Wireframe lines are geometric.** Grid overlays, connection lines, and structural indicators use `wireframeOverlay` color. Always straight lines, never curves. Dashed patterns allowed: `1px dashed` or `2px 4px` dash-gap.

---

## Typography Matrix

### Font Families

| Slot | Font | Fallback | Role |
|---|---|---|---|
| sans (display/heading) | Instrument Sans | system-ui, -apple-system, sans-serif | Display, Heading. Condensed energy, precision-engineered. Cold, technical, geometric. |
| sans (body) | Albert Sans | system-ui, -apple-system, sans-serif | Body, Body Small, Button, Input, Label, Caption. Scandinavian minimalism. Clean, cold, efficient. |
| mono | Geist Mono | ui-monospace, SFMono-Regular, Menlo, Monaco, monospace | Code, data values. Modern monospace from Vercel. Pairs with the geometric precision of the theme. |

**Family switch boundary:** Instrument Sans handles Display and Heading -- the two roles where condensed energy and geometric authority are paramount. Albert Sans handles everything below -- its Scandinavian minimalism provides cold efficiency for functional text without warmth or personality. The two families share geometric DNA but differ in density: Instrument Sans is tighter, more engineered; Albert Sans is more open, more readable at small sizes.

**Why this pairing:** Instrument Sans evokes engineering diagrams, CAD software labels, and architectural blueprints -- text that exists to label geometry, not to tell stories. It is condensed without being compressed, precise without being rigid. Albert Sans is the body text of a scientific paper or a data sheet -- clean, legible, devoid of ornament. Together they create a typographic system that feels computed, not authored. Geist Mono completes the system with its modern geometric monospace, consistent with the Vercel/Linear ecosystem that defines contemporary developer aesthetics.

**Why not serif:** This theme has zero warmth. Serif fonts carry editorial warmth, literary history, or classical authority -- all wrong for the crystal interior. The geometric sans pairing is a deliberate anti-warmth decision.

### Role Matrix

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Instrument Sans | 36px | 600 | 1.1 (39.6px) | -0.03em | -- | Hero titles, page titles. Tight, condensed, geometric authority. |
| Heading | Instrument Sans | 22px | 600 | 1.2 (26.4px) | -0.015em | -- | Section titles, settings headers, card group titles. |
| Subheading | Albert Sans | 17px | 600 | 1.3 (22.1px) | -0.005em | -- | Card titles, subsection headers. Slightly lighter weight than heading for hierarchy. |
| Body | Albert Sans | 15px | 400 | 1.55 (23.3px) | normal | -- | Primary reading text. Slightly smaller than the 16px standard -- crystal density is tighter. |
| Body Small | Albert Sans | 13px | 400 | 1.4 (18.2px) | 0.005em | -- | Sidebar items, form labels, secondary UI text. |
| Button | Albert Sans | 13px | 500 | 1.4 (18.2px) | 0.02em | `text-transform: uppercase` | Button labels. Uppercase with tracking for geometric formality. |
| Input | Albert Sans | 14px | 400 | 1.4 (19.6px) | normal | -- | Form input text. |
| Label | Albert Sans | 10px | 600 | 1.3 (13px) | 0.08em | `text-transform: uppercase` | Section labels, metadata, timestamps. All-caps with generous tracking. Reads like a crystal axis label: X, Y, Z. |
| Code | Geist Mono | 0.9em (13.5px at 15px base) | 400 | 1.5 (20.3px) | normal | `font-variant-numeric: tabular-nums` | Inline code, code blocks, data values, coordinates, matrix notation. |
| Caption | Albert Sans | 11px | 400 | 1.3 (14.3px) | 0.01em | -- | Disclaimers, footnotes, axis labels on charts. |

**Typography philosophy:** The condensed-display/minimal-body split mirrors the typography of engineering drawings and scientific instruments. The display labels a structure; the body annotates it. Uppercase button and label roles echo the all-caps convention of technical labeling (CAUTION, SECTION A, NODE 47). Letter-spacing opens at small sizes for readability, tightens at large sizes for density -- the opposite of default behavior, which signals intentional design.

### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;500;600&family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
```

- **Font smoothing:** `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale` on `<html>`. Essential for light text on crystal-white backgrounds -- prevents fuzziness.
- **Font display:** `font-display: swap` on all families.
- **Text wrap:** `text-wrap: balance` for Display and Heading roles. `text-wrap: pretty` for Body paragraphs.

---

## Elevation System

**Strategy:** Faceted surfaces + wireframe overlays + prismatic edge highlights.

Separation between surfaces is achieved through facet-angle gradients combined with prismatic border highlighting. Every elevated surface carries a subtle directional linear-gradient simulating a crystal face catching light at a specific angle. The external shadows are crystalline -- sharp, geometric, not diffused. Wireframe overlays (thin dashed or solid platinum lines at very low opacity) create structural depth between grouped elements. Popovers add a `backdrop-filter: blur(16px)` and a prismatic border accent.

### Surface Hierarchy

| Surface | Background | Shadow | Facet Effect | Usage |
|---|---|---|---|---|
| page | `#EAEDF0` (page) | none | none | Deepest layer. The crystal body. |
| canvas | `#F0F2F4` (bg) | none | none | Primary working surface. |
| card | `#F7F8FA` (surface) | shadow-card | `linear-gradient(172deg, rgba(255,255,255,0.5) 0%, transparent 40%, rgba(26,29,33,0.015) 100%)` | Cards, inputs, elevated panels. A single crystal face catching light. |
| recessed | `#E2E5E9` (recessed) | none | `linear-gradient(180deg, rgba(26,29,33,0.02) 0%, transparent 30%)` | Code blocks, inset areas. Facet angled away from light. |
| active | `#D5D9DE` (active) | none | `linear-gradient(175deg, rgba(255,255,255,0.3) 0%, transparent 50%)` | Active sidebar item, user bubble. Facet in partial shadow. |
| overlay | `#F7F8FA` (surface) | shadow-popover | Prismatic border + facet gradient | Popovers, dropdowns, modals. The most prominent crystal face. |

### Shadow Tokens

Shadows in this theme are sharp and geometric -- not soft or diffused. Crystal does not scatter light; it refracts it. Shadows have minimal blur radius and slightly angular offsets.

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `0 1px 2px rgba(26, 29, 33, 0.05)` | Small elements, chips. |
| shadow-md | `0 2px 4px rgba(26, 29, 33, 0.06), 0 1px 2px rgba(26, 29, 33, 0.04)` | Medium elevation. |
| shadow-card | `0 1px 3px rgba(26, 29, 33, 0.04), 0 0 0 0.5px rgba(160, 168, 180, 0.18)` | Card rest state. Geometric, tight, low blur. The 0.5px ring simulates the wireframe outline. |
| shadow-card-hover | `0 2px 6px rgba(26, 29, 33, 0.06), 0 0 0 0.5px rgba(160, 168, 180, 0.26)` | Card hover. Shadow sharpens and deepens slightly. |
| shadow-card-focus | `0 2px 8px rgba(26, 29, 33, 0.08), 0 0 0 0.5px rgba(160, 168, 180, 0.26)` | Card focus-within. Maximum structural shadow. |
| shadow-input | `0 1px 3px rgba(26, 29, 33, 0.04), 0 0 0 0.5px rgba(160, 168, 180, 0.18)` | Input rest state. Same as card. |
| shadow-input-hover | `0 2px 6px rgba(26, 29, 33, 0.06), 0 0 0 0.5px rgba(160, 168, 180, 0.26)` | Input hover. |
| shadow-input-focus | `0 2px 8px rgba(26, 29, 33, 0.08), 0 0 0 1px rgba(59, 111, 212, 0.3)` | Input focus. The ring shifts to sapphire accent. |
| shadow-popover | `0 4px 12px rgba(26, 29, 33, 0.12), 0 1px 3px rgba(26, 29, 33, 0.06)` | Menus, popovers, dropdowns. Sharpest shadow in the system. |
| shadow-none | `none` | Flat surfaces, disabled states, recessed areas. |

### Facet Rendering Tokens

The faceted surface effect. Each elevated surface carries a subtle directional gradient simulating a crystal face orientation.

| Token | Value | Usage |
|---|---|---|
| facet-172 | `linear-gradient(172deg, rgba(255,255,255,0.5) 0%, transparent 40%, rgba(26,29,33,0.015) 100%)` | Primary card facet angle. Light from upper-left. |
| facet-168 | `linear-gradient(168deg, rgba(255,255,255,0.45) 0%, transparent 38%, rgba(26,29,33,0.018) 100%)` | Alternate card facet. Slightly different angle for visual variety. |
| facet-175 | `linear-gradient(175deg, rgba(255,255,255,0.4) 0%, transparent 42%, rgba(26,29,33,0.012) 100%)` | Tertiary facet angle. Subtle variation. |
| facet-recessed | `linear-gradient(180deg, rgba(26,29,33,0.02) 0%, transparent 30%)` | Recessed/inset facet. Angled away from light, darker at top. |

**Implementation pattern -- faceted surface:**

```css
.card {
  background:
    linear-gradient(172deg, rgba(255,255,255,0.5) 0%, transparent 40%, rgba(26,29,33,0.015) 100%),
    var(--surface);
  box-shadow:
    0 1px 3px rgba(26, 29, 33, 0.04),
    0 0 0 0.5px rgba(160, 168, 180, 0.18);
}

/* Second card in a group uses a different facet angle */
.card:nth-child(2n) {
  background:
    linear-gradient(168deg, rgba(255,255,255,0.45) 0%, transparent 38%, rgba(26,29,33,0.018) 100%),
    var(--surface);
}

/* Third card uses the third angle */
.card:nth-child(3n) {
  background:
    linear-gradient(175deg, rgba(255,255,255,0.4) 0%, transparent 42%, rgba(26,29,33,0.012) 100%),
    var(--surface);
}
```

### Wireframe Overlay Pattern

Structural wireframe grids appear behind content areas to reinforce the mathematical/geometric identity.

```css
/* Wireframe grid overlay on page background */
.wireframe-grid {
  background-image:
    linear-gradient(rgba(160, 168, 180, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(160, 168, 180, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
}

/* Wireframe grid with diagonal cross-hatching for emphasis areas */
.wireframe-grid-dense {
  background-image:
    linear-gradient(rgba(160, 168, 180, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(160, 168, 180, 0.04) 1px, transparent 1px),
    linear-gradient(45deg, rgba(160, 168, 180, 0.02) 1px, transparent 1px),
    linear-gradient(-45deg, rgba(160, 168, 180, 0.02) 1px, transparent 1px);
  background-size: 24px 24px, 24px 24px, 48px 48px, 48px 48px;
}
```

### Backdrop Filter

| Context | Value | Usage |
|---|---|---|
| popover | `backdrop-filter: blur(16px)` | Popover/dropdown containers. Sharp, not dreamy. |
| modal | `backdrop-filter: blur(8px)` | Modal overlay background. Less blur -- maintain the grid. |
| none | `backdrop-filter: none` | Default, non-overlay surfaces. |

### Separation Recipe

Facet-angle gradient + wireframe ring + geometric shadow. The page-to-bg step (from `#EAEDF0` to `#F0F2F4`) is the crystal body versus the polished face. The bg-to-surface step (from `#F0F2F4` to `#F7F8FA`) lifts cards and inputs -- a facet catching direct light. Each elevated surface then receives a unique facet-angle gradient (varying by 3-7 degrees) so that adjacent cards appear to be different faces of the same crystal. The 0.5px wireframe ring (from the shadow token) outlines every surface with platinum precision. No horizontal rules. No visible dividers between sections -- spacing and facet-angle changes create separation.

---

## Border System

### Base Color

`#A0A8B4` (Wireframe Platinum). This cool grey, applied at variable opacity, produces the standard wireframe border vocabulary. The prismatic conic-gradient system overlays on top for accent-state edges.

### Widths and Patterns

| Pattern | Width | Opacity | CSS Value | Usage |
|---|---|---|---|---|
| subtle | 0.5px | 10% | `0.5px solid rgba(160, 168, 180, 0.10)` | Sidebar right edge, wireframe grid lines. Near-invisible geometry. |
| card | 0.5px | 18% | `0.5px solid rgba(160, 168, 180, 0.18)` | Card borders (non-prismatic mode). |
| hover | 0.5px | 26% | `0.5px solid rgba(160, 168, 180, 0.26)` | Hover states, popovers. |
| input | 1px | 12% | `1px solid rgba(160, 168, 180, 0.12)` | Form input borders at rest. |
| input-hover | 1px | 26% | `1px solid rgba(160, 168, 180, 0.26)` | Form input borders on hover. |
| wireframe | 1px dashed | 8% | `1px dashed rgba(160, 168, 180, 0.08)` | Structural wireframe lines, grid overlays, connection indicators. |

### Width Scale

| Name | Value | Usage |
|---|---|---|
| hairline | 0.5px | Card edges, sidebar separation, wireframe grid. |
| default | 1px | Form input borders, wireframe structural lines. |
| medium | 1.5px | Heavy structural emphasis, section dividers. |
| heavy | 2px | Focus ring width, prismatic accent borders on hero elements. |

### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(59, 111, 212, 0.45)` |
| Width | 2px solid |
| Style | `outline: 2px solid rgba(59, 111, 212, 0.45)` |
| Offset | `2px` |
| Applies to | All interactive elements on `:focus-visible` |

Focus ring uses the sapphire accent at 45% opacity. This creates a cool blue outline that harmonizes with the monochrome palette while providing clear visibility. On elements with prismatic borders, the focus ring adds a clean sapphire frame outside the prismatic layer.

---

## Component States

### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: 1px solid rgba(160, 168, 180, 0.22)`, `color: #1A1D21 (text-primary)`, `border-radius: 4px`, `height: 32px`, `padding: 0 14px`, `font-size: 13px`, `font-weight: 500`, `font-family: Albert Sans`, `letter-spacing: 0.02em`, `text-transform: uppercase`, `cursor: pointer` |
| Hover | `bg: rgba(160, 168, 180, 0.06)`, `border-color: rgba(160, 168, 180, 0.30)` |
| Active | `transform: scale(0.97)`, `bg: rgba(160, 168, 180, 0.10)` |
| Focus | `outline: 2px solid rgba(59, 111, 212, 0.45)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `shadow: none`, `cursor: not-allowed` |
| Transition | `color, background-color, border-color, transform 120ms cubic-bezier(0.4, 0, 0.2, 1)` |

### Buttons (Accent/CTA)

| State | Properties |
|---|---|
| Rest | `bg: #3B6FD4 (accent-primary)`, `border: none`, `color: #F7F8FA (text-onAccent)`, `border-radius: 4px`, `height: 32px`, `padding: 0 18px`, `font-size: 13px`, `font-weight: 500`, `letter-spacing: 0.02em`, `text-transform: uppercase`, `cursor: pointer` |
| Hover | `bg: #2D5BB8` (12% darker sapphire) |
| Active | `transform: scale(0.97)`, `bg: #244DA0` |
| Focus | `outline: 2px solid rgba(59, 111, 212, 0.45)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `cursor: not-allowed` |
| Transition | `background-color, transform 120ms cubic-bezier(0.4, 0, 0.2, 1)` |

### Buttons (Ghost/Icon)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: none`, `color: #5C636E (text-secondary)`, `border-radius: 4px`, `width: 32px`, `height: 32px`, `padding: 0`, `cursor: pointer` |
| Hover | `bg: rgba(160, 168, 180, 0.08)`, `color: #1A1D21 (text-primary)` |
| Active | `transform: scale(0.97)` |
| Focus | `outline: 2px solid rgba(59, 111, 212, 0.45)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none` |
| Transition | `all 250ms cubic-bezier(0.165, 0.85, 0.45, 1)` |

### Text Input (Settings Form)

| State | Properties |
|---|---|
| Rest | `bg: #F7F8FA (surface)`, `border: 1px solid rgba(160, 168, 180, 0.12)`, `border-radius: 4px`, `height: 40px`, `padding: 0 12px`, `font-size: 14px`, `font-weight: 400`, `font-family: Albert Sans`, `color: #1A1D21 (text-primary)`, `caret-color: #3B6FD4 (accent-primary)`, `box-shadow: shadow-input`, facet-172 background gradient |
| Placeholder | `color: #8E95A0 (text-muted)` |
| Hover | `border-color: rgba(160, 168, 180, 0.26)`, `box-shadow: shadow-input-hover` |
| Focus | `outline: 2px solid rgba(59, 111, 212, 0.45)`, `outline-offset: 2px`, `border-color: rgba(59, 111, 212, 0.3)`, `box-shadow: shadow-input-focus` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `cursor: not-allowed`, `box-shadow: none` |
| Transition | `border-color, box-shadow 200ms cubic-bezier(0.4, 0, 0.2, 1)` |

Note: The caret uses the sapphire accent -- a blue cursor blinking against the crystal white surface. Precise, cold, computed.

### Textarea

| State | Properties |
|---|---|
| Rest | Same bg/border/radius as text input. `padding: 12px`, `line-height: 18.2px`, `min-height: 100px`, `resize: vertical`, `white-space: pre-wrap`, `box-shadow: shadow-input` |
| Hover/Focus/Disabled | Same escalation as text input |

### Chat Input Card

| State | Properties |
|---|---|
| Rest | `bg: #F7F8FA (surface)`, `border-radius: 12px`, `border: 1px solid transparent`, `box-shadow: shadow-card`, facet-172 background gradient |
| Hover | `box-shadow: shadow-card-hover` |
| Focus-within | `box-shadow: shadow-card-focus`. Prismatic border activates (see prismatic border implementation). |
| Inner textarea | `font-size: 15px`, `line-height: 23.3px`, `bg: transparent`, `color: text-primary`, `placeholder-color: text-muted`, `caret-color: #3B6FD4` |
| Transition | `box-shadow 250ms cubic-bezier(0.4, 0, 0.2, 1)` |

When the chat input receives focus, its border transitions from invisible to prismatic -- the rainbow appears at the geometric edge of the active input, signaling that the crystal structure is responding to interaction.

### Cards

| State | Properties |
|---|---|
| Rest | `bg: facet-172 gradient over #F7F8FA (surface)`, `border: 0.5px solid rgba(160, 168, 180, 0.18)`, `border-radius: 6px`, `box-shadow: shadow-card`, `padding: 20px` |
| Hover | `border-color: rgba(160, 168, 180, 0.26)`, `box-shadow: shadow-card-hover`. Prismatic border pseudo-element fades in at 0.12 opacity. |
| Focus | `outline: 2px solid rgba(59, 111, 212, 0.45)`, `outline-offset: 2px` (when card is clickable) |
| Transition | `border-color, box-shadow 250ms cubic-bezier(0.4, 0, 0.2, 1)` |

Cards alternate facet angles using `:nth-child()` selectors so adjacent cards appear as different faces of a crystal formation.

### Sidebar Items

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `color: #5C636E (text-secondary)`, `border-radius: 4px`, `height: 32px`, `padding: 6px 14px`, `font-size: 13px`, `font-weight: 400`, `font-family: Albert Sans`, `white-space: nowrap`, `overflow: hidden`, `cursor: pointer` |
| Hover | `bg: rgba(160, 168, 180, 0.06)`, `color: #1A1D21 (text-primary)` |
| Active (current) | `bg: rgba(160, 168, 180, 0.10)`, `color: #1A1D21 (text-primary)`. Left edge: `border-left: 2px solid #3B6FD4`. The sapphire marker. |
| Active press | `transform: scale(0.985)` |
| Disabled | `pointer-events: none`, `opacity: 0.4` |
| Transition | `color, background-color 80ms cubic-bezier(0.165, 0.85, 0.45, 1)` |
| Text truncation | Gradient fade mask: `mask-image: linear-gradient(to right, black 85%, transparent)`. Not `text-overflow: ellipsis`. |

### Section Labels (Sidebar)

| Property | Value |
|---|---|
| Font | Albert Sans, 10px, weight 600, color `#8E95A0 (text-muted)` |
| Line-height | 13px |
| Letter-spacing | 0.08em |
| Text-transform | uppercase |
| Padding | `0 8px 6px` |
| Margin-top | 6px |

Crystal-axis labels. All-caps, widely tracked, small, and precise -- like the X/Y/Z markers on a 3D coordinate system.

### Chips (Quick Actions)

| State | Properties |
|---|---|
| Rest | `bg: #F0F2F4 (bg)`, `border: 0.5px solid rgba(160, 168, 180, 0.12)`, `border-radius: 4px`, `height: 30px`, `padding: 0 10px`, `font-size: 13px`, `font-weight: 400`, `font-family: Albert Sans`, `color: #5C636E (text-secondary)`, `cursor: pointer` |
| Icon | 14x14px, inline-flex, gap 6px from label |
| Hover | `bg: #D5D9DE (active)`, `border-color: rgba(160, 168, 180, 0.22)`, `color: #1A1D21 (text-primary)` |
| Active press | `transform: scale(0.995)` |
| Transition | `all 150ms cubic-bezier(0.4, 0, 0.2, 1)` |

Small border-radius (4px) -- geometric, not rounded. Chips are crystal facets, not pebbles.

### Toggle/Switch

| Property | Value |
|---|---|
| Track | `width: 36px`, `height: 18px`, `border-radius: 9999px` |
| Track off | `bg: #D5D9DE (active)` |
| Track on | `bg: #3B6FD4 (sapphire)` |
| Track ring rest | `0.5px` ring using `rgba(160, 168, 180, 0.26)` |
| Track ring hover | `1px` ring (thickens on hover) |
| Thumb | `width: 14px`, `height: 14px`, `bg: #F7F8FA (surface)`, `border-radius: 9999px`, `box-shadow: 0 1px 2px rgba(26, 29, 33, 0.10)` |
| Transition | `background-color, transform 150ms cubic-bezier(0.4, 0, 0.2, 1)` |
| Focus-visible | Sapphire focus ring on the track |

### User Message Bubble

| Property | Value |
|---|---|
| bg | `#D5D9DE (active)` |
| border-radius | 8px (geometric, not pill-shaped) |
| padding | `10px 16px` |
| max-width | `80%` (capped at `70ch`) |
| color | `#1A1D21 (text-primary)` |
| font | Albert Sans, 15px, weight 400 |
| alignment | Right-aligned |
| border | `0.5px solid rgba(160, 168, 180, 0.12)` |
| box-shadow | `shadow-sm` |

User bubbles are crystal facets -- angular (8px radius, not rounded), bordered, with a subtle geometric shadow.

---

## Motion Map

### Easings

| Name | Value | Character |
|---|---|---|
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. Most UI transitions. Mechanical precision. |
| out-quart | `cubic-bezier(0.165, 0.85, 0.45, 1)` | Snappy deceleration. Sidebar items, ghost buttons. Crystal-sharp arrival. |
| out-expo | `cubic-bezier(0.19, 1, 0.22, 1)` | Near-instant arrival, long settle. Panel open/close, modals. |
| geometric-ease | `cubic-bezier(0.25, 0.0, 0.0, 1.0)` | The signature easing. Linear start (computed feel), exponential deceleration (geometric precision). Used for facet rotations and prismatic effects. Feels like a geometry engine rendering a calculation. |
| symmetric-ease | `cubic-bezier(0.42, 0, 0.58, 1)` | Perfectly symmetric ease-in-out. Used when symmetry is required -- mirror animations, balanced reveals. |
| crystal-spring | `stiffness: 350, damping: 28` | High-stiffness spring with firm damping. No wobble. Crystal does not bounce; it snaps into place and settles. |

### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 80ms | out-quart | Instant, computed. Crystal does not linger. |
| Button hover (primary/outlined) | 120ms | default | Background, border-color, color. Mechanical. |
| Toggle track color | 150ms | default | Background-color and thumb transform. |
| Chip hover | 150ms | default | All properties. |
| Card border/shadow hover | 250ms | geometric-ease | Border-color, box-shadow. The facet catches light. |
| Input border/shadow hover | 200ms | default | Border-color and shadow escalation. |
| Chat input card shadow | 250ms | geometric-ease | All properties including prismatic border activation. |
| Ghost icon button | 250ms | out-quart | Slightly faster than gallery themes. |
| Prismatic border activation | 300ms | geometric-ease | Prismatic conic-gradient fades in on focus. |
| Page/hero content entry | 400ms | geometric-ease | `opacity: 0, translateY(12px)` to `opacity: 1, translateY(0)`. Shorter travel than gallery themes. |
| Modal entry | 300ms | out-expo | `scale(0.96)` to `scale(1)` + fade. |
| Panel open/close | 500ms | out-expo | Sidebar collapse, settings panel expand. |
| Crystal stagger delay | 60ms | -- | Delay between staggered children. Fast cascade -- crystals grow quickly. |
| Menu item hover | 80ms | default | Popover item bg/color change. |
| Facet rotation (ambient) | 4000ms | geometric-ease | Slow angular gradient rotation on hero elements. |

### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items (sidebar) | `scale(0.985)` | Subtle. Crystal fractures are microscopic. |
| Chips | `scale(0.995)` | Almost invisible press. |
| Buttons (primary, ghost, accent) | `scale(0.97)` | Standard mechanical press. |
| Tabs | `scale(0.96)` | Pronounced for segmented controls. |

### Reduced Motion

| Behavior | Change |
|---|---|
| Strategy | `instant` -- all spatial movement removed, all transitions become instantaneous. Crystal is not fluid; it snaps. |
| All translateY entries | Replaced with instant opacity change (no vertical movement). |
| Scale presses | Disabled. Instant visual state change. |
| Stagger delays | Reduced to 0ms. All children appear simultaneously. |
| Ambient motion (facet rotation, light catch sparkle) | Disabled entirely. Static rendering. |
| Prismatic border transitions | Remain but simplified to opacity change only, 100ms max. |
| All hover transitions | Remain but capped at 100ms. |

---

## Overlays

### Popover/Dropdown

| Property | Value |
|---|---|
| bg | `#F7F8FA (surface)` with facet-172 gradient |
| backdrop-filter | `blur(16px)` |
| border | `0.5px solid rgba(160, 168, 180, 0.26)` |
| border-radius | 6px |
| box-shadow | `shadow-popover` |
| padding | 6px |
| min-width | 192px |
| max-width | 320px |
| z-index | 50 |
| overflow-y | auto (with `max-height: var(--available-height)`) |
| Menu item | `padding: 6px 10px`, `border-radius: 4px`, `height: 32px`, `font-size: 13px (body-small)`, `color: #5C636E (text-secondary)`, `cursor: pointer` |
| Menu item hover | `bg: rgba(160, 168, 180, 0.06)`, `color: #1A1D21 (text-primary)` |
| Menu item transition | `80ms cubic-bezier(0.4, 0, 0.2, 1)` |
| Separators | `1px solid rgba(160, 168, 180, 0.08)` between groups. Thin wireframe-style dividers. |

### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(26, 29, 33, 0.40)` (cool-tinted, not pure black. Crystal is not opaque.) |
| Overlay backdrop-filter | `blur(8px)` |
| Content bg | `#F7F8FA (surface)` with facet-172 gradient |
| Content shadow | `shadow-popover` |
| Content border | Prismatic border pseudo-element at 0.15 opacity. |
| Content border-radius | 8px |
| Content padding | 24px |
| Entry animation | `opacity: 0, scale(0.96)` to `opacity: 1, scale(1)`, 300ms out-expo |
| Exit animation | `opacity: 0`, 200ms default |
| z-index | 60 |

### Tooltip

| Property | Value |
|---|---|
| bg | `#1A1D21 (text-primary)` (inverted -- dark tooltip on light theme) |
| color | `#F7F8FA (text-onAccent)` |
| font-size | 10px (label role) |
| font-weight | 600 |
| letter-spacing | 0.08em |
| text-transform | uppercase |
| border-radius | 3px |
| padding | `3px 8px` |
| shadow | `0 1px 3px rgba(26, 29, 33, 0.15)` |
| Arrow | None. Position-only placement. |
| Delay | 300ms before showing. |
| z-index | 55 |

Tooltips are inverted: dark graphite background with crystal-white text. All-caps with heavy tracking matches the label/axis-marker convention. Small, precise, computed.

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 760px | Main content column. Slightly narrower -- crystal density. |
| Narrow max-width | 640px | Landing/focused content, settings pages. |
| Sidebar width | 260px | Fixed sidebar. Narrow -- structural scaffold, not content area. |
| Sidebar border | `0.5px solid rgba(160, 168, 180, 0.10)` | Right edge. Near-invisible wireframe line. |
| Header height | 44px | Top bar. Compact. |
| Spacing unit | 4px | Base multiplier. |

### Spacing Scale

`4, 6, 8, 12, 16, 20, 24, 32, 40px`

Base unit is 4px. The scale includes 6px for tight pairings (icon-text gap). Upper end stops at 40px -- crystal density does not permit the generous 48-64px spacings of gallery themes. Space is structural, not atmospheric.

Common applications:
- 4px: minimum gap, tight inline elements
- 6px: icon-text gap, sidebar section label padding
- 8px: standard element gap, chip padding, card inset compact
- 12px: input padding, standard card inset
- 16px: sidebar item horizontal padding, section gap
- 20px: card padding, standard content gap
- 24px: modal padding, content-to-sidebar gap
- 32px: major section separation
- 40px: hero spacing, page-level vertical rhythm

### Density

**moderate** -- Tighter than gallery/editorial themes but not cramped. Content-to-whitespace ratio approximately 55:45. The crystal lattice is structured and regular, not spacious. Information is arranged with mathematical regularity.

### Responsive Notes

| Breakpoint | Width | Behavior |
|---|---|---|
| lg | 1024px | Full sidebar + content. Default desktop layout. Crystal matrix grid visible. |
| md | 768px | Sidebar collapses to overlay. Content fills viewport with 20px horizontal padding. |
| sm | 640px | Single column. Cards stack vertically. Chips wrap. Input card full-width. Wireframe grid disabled. |

On mobile (below md):
- Sidebar becomes an overlay panel with the same bg, activated by menu button
- Content max-width becomes 100% with 16px horizontal padding (tighter than gallery themes)
- Header remains 44px but actions collapse into a popover menu
- Cards stretch to full width, padding reduces from 20px to 16px
- Prismatic border effects simplified to solid sapphire borders (conic-gradient is expensive on mobile)
- Facet gradients reduced to a single angle (no `:nth-child` variation)
- Crystal stagger delay reduces from 60ms to 30ms
- Display role reduces from 36px to `clamp(24px, 6vw, 36px)`

---

## Accessibility Tokens

| Token | Value | Notes |
|---|---|---|
| Focus ring color | `rgba(59, 111, 212, 0.45)` | Sapphire at 45% opacity. Harmonizes with monochrome palette while providing clear visibility. |
| Focus ring width | `2px solid` | Applied via `outline` |
| Focus ring offset | `2px` | Applied via `outline-offset` |
| Disabled opacity | `0.4` | Lower than standard 0.5 -- crystal clarity means even disabled elements are legible. Combined with `pointer-events: none` and `cursor: not-allowed` |
| Disabled shadow | `none` | Remove all shadows and facet effects on disabled elements |
| Selection bg | `rgba(59, 111, 212, 0.14)` | Sapphire at 14% -- `::selection`. Cool crystal highlight. |
| Selection color | `#1A1D21 (text-primary)` | Maintains readability on selection |
| Scrollbar width | `thin` | `scrollbar-width: thin` |
| Scrollbar thumb | `rgba(160, 168, 180, 0.28)` | Wireframe platinum at 28% opacity. |
| Scrollbar track | `transparent` | No visible track |
| Min touch target | 44px | All interactive elements on mobile |
| Contrast standard | WCAG AA | 4.5:1 for normal text, 3:1 for large text (18px+) |

**Contrast verification:**
- text-primary (`#1A1D21`) on surface (`#F7F8FA`): ~15.2:1 (passes AAA)
- text-secondary (`#5C636E`) on surface (`#F7F8FA`): ~5.8:1 (passes AA)
- text-muted (`#8E95A0`) on surface (`#F7F8FA`): ~3.5:1 (passes AA for large text; used only for metadata/timestamps at label size or larger)
- accent-primary (`#3B6FD4`) on surface (`#F7F8FA`): ~4.6:1 (passes AA)
- text-onAccent (`#F7F8FA`) on accent-primary (`#3B6FD4`): ~4.6:1 (passes AA)

**Scrollbar CSS:**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(160, 168, 180, 0.28) transparent;
}
```

---

## Visual Style

### Material

| Property | Value |
|---|---|
| Grain | None. Crystal is flawless. No noise, no texture, no fiber. Surfaces are mathematically smooth. |
| Grain technique | None. |
| Gloss | Matte-to-soft-sheen. Crystal faces catch light directionally (via facet gradients) but do not reflect -- they refract. The subtle highlight-to-shadow gradient on each surface simulates facet angle, not glossiness. |
| Blend mode | `normal` everywhere. Crystal is not blended; it is precise. |
| Shader bg | false. No WebGL backgrounds. The wireframe grid is pure CSS. |

### The Faceted Rendering Technique (Full Reference)

Crystal faceting is the signature rendering approach. Each elevated surface simulates a single face of a polyhedron by carrying a subtle directional linear-gradient from highlight (top-left) to shadow (bottom-right), with the angle varying between surfaces.

**Core mechanism:**

```css
/* A crystal face catching light from the upper-left */
.facet {
  background:
    /* Facet angle gradient -- simulates directional light on a flat crystal face */
    linear-gradient(
      172deg,
      rgba(255, 255, 255, 0.5) 0%,      /* Light catch at the edge */
      transparent 40%,                     /* Face body -- transparent to show bg */
      rgba(26, 29, 33, 0.015) 100%        /* Shadow at the opposite edge */
    ),
    var(--surface);                        /* Base surface color */
}
```

**Varying facet angles for adjacent elements:**

```css
/* Each card in a grid uses a different facet angle */
.card:nth-child(4n+1) { --facet-angle: 172deg; }
.card:nth-child(4n+2) { --facet-angle: 168deg; }
.card:nth-child(4n+3) { --facet-angle: 175deg; }
.card:nth-child(4n+4) { --facet-angle: 170deg; }

.card {
  background:
    linear-gradient(
      var(--facet-angle),
      rgba(255, 255, 255, 0.5) 0%,
      transparent 40%,
      rgba(26, 29, 33, 0.015) 100%
    ),
    var(--surface);
}
```

**Facet top-edge highlight for premium elements:**

```css
/* Simulates a sharp light catch at the top edge of a crystal face */
.premium-facet {
  border-top: 0.5px solid rgba(255, 255, 255, 0.5);
}
```

**Why angle variation matters:** In a real crystal formation, adjacent faces catch light at different angles. If all cards shared the same gradient angle, they would read as a flat surface with a gradient -- not as a polyhedron. The 3-7 degree variation between `:nth-child()` groups creates the illusion of a faceted solid without being visually distracting.

**Tuning guidance:**
- Card-sized elements: highlight at `0.5` opacity, shadow at `0.015`
- Large panels (hero, modal): highlight at `0.4`, shadow at `0.012` (less contrast -- larger faces are flatter)
- Recessed elements: shadow at top instead of highlight (`180deg` angle), `0.02` opacity (angled away from light)
- Input fields: same as cards, with sapphire caret for interaction
- Never let the facet gradient dominate the surface. It should be felt, not seen.

### Wireframe Overlay Guidelines

- Wireframe grids use `wireframeOverlay` color (`rgba(160, 168, 180, 0.08)`)
- Lines are always straight -- never curved, never organic
- Standard grid: 48px spacing, 1px width
- Dense grid: 24px spacing with 45-degree cross-hatching
- Wireframe overlays appear behind content, never on top
- Use `pointer-events: none` on all wireframe overlay elements
- On hero sections, wireframe grids can extend across the full viewport width to suggest the crystal lattice extends beyond the visible area

### Rendering Guidelines

- **No curves.** Border-radius values are small (3-6px). No pill shapes, no large radius. The crystal is geometric.
- **No warmth.** Every surface is cool. Every text color is cool. Warmth exists only inside the prismatic gradient.
- **Wireframe scaffolding is real.** When building layouts, the underlying grid structure (wireframe) should be subtly visible behind content areas. This is the crystal's internal structure showing through.
- **Data visualization:** Charts, graphs, and mathematical visualizations should render with thin strokes, geometric shapes, and the monochrome palette. Data colors use the prismatic spectrum (ruby, citrine, emerald, sapphire, amethyst) mapped to categorical values.
- **Coordinates and data:** Numerical values, coordinates, and computed results should always use Geist Mono with `tabular-nums`. Numbers are data; data is rendered precisely.

---

## Signature Animations

### 1. Facet Rotation (Ambient)

Hero cards and feature panels exhibit a slow, continuous rotation of their facet-angle gradient, as if the crystal is imperceptibly turning and the light catch moves across the face.

- **Technique:** CSS keyframe animation rotating the `--facet-angle` custom property.

```css
@property --facet-angle {
  syntax: '<angle>';
  initial-value: 172deg;
  inherits: false;
}

@keyframes facet-rotation {
  0%   { --facet-angle: 168deg; }
  25%  { --facet-angle: 172deg; }
  50%  { --facet-angle: 176deg; }
  75%  { --facet-angle: 172deg; }
  100% { --facet-angle: 168deg; }
}

.hero-card {
  animation: facet-rotation 5s cubic-bezier(0.25, 0.0, 0.0, 1.0) infinite;
  background:
    linear-gradient(
      var(--facet-angle),
      rgba(255, 255, 255, 0.5) 0%,
      transparent 40%,
      rgba(26, 29, 33, 0.015) 100%
    ),
    var(--surface);
}
```

- **Duration:** 5 seconds per full cycle. Slow, geometric, imperceptible.
- **Easing:** geometric-ease. Linear start with exponential deceleration.
- **Angle range:** 168deg to 176deg. Only 8 degrees of movement. The crystal barely turns.
- **Reduced motion:** Disabled. Static facet at 172deg.

### 2. Light-Catch Sparkle (Vertex Highlight)

At geometric intersection points (where borders meet, where card corners align), a brief prismatic flash appears -- a tiny rainbow sparkle that simulates light catching a crystal vertex.

- **Technique:** Pseudo-element positioned at corner with a small radial gradient that flashes on hover or scroll.

```css
@keyframes sparkle {
  0%   { opacity: 0; transform: scale(0.5); }
  20%  { opacity: 1; transform: scale(1); }
  100% { opacity: 0; transform: scale(1.5); }
}

.card::after {
  content: '';
  position: absolute;
  top: -2px;
  right: -2px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    rgba(196,64,64,0.6),
    rgba(184,144,45,0.6),
    rgba(45,139,94,0.6),
    rgba(59,111,212,0.6),
    rgba(123,94,167,0.6),
    rgba(196,64,64,0.6)
  );
  opacity: 0;
  pointer-events: none;
}

.card:hover::after {
  animation: sparkle 600ms cubic-bezier(0.25, 0.0, 0.0, 1.0) forwards;
}
```

- **Duration:** 600ms. Quick flash, slow fade.
- **Position:** Top-right corner of cards (vertex point).
- **Size:** 8px diameter. Tiny -- a point of light, not a glow.
- **Reduced motion:** Disabled. No sparkle.

### 3. Crystal Growth (Element Entry)

Elements enter the viewport by growing from a central seed point outward, as if a crystal is forming. The element starts as a point and expands to full size with a slight overshoot.

- **Technique:** `scale(0) opacity(0)` to `scale(1) opacity(1)` with `transform-origin: center`.

```css
@keyframes crystal-growth {
  0% {
    opacity: 0;
    transform: scale(0);
  }
  60% {
    opacity: 1;
    transform: scale(1.02);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.crystal-enter {
  animation: crystal-growth 400ms cubic-bezier(0.25, 0.0, 0.0, 1.0) both;
}

.crystal-enter:nth-child(1) { animation-delay: 0ms; }
.crystal-enter:nth-child(2) { animation-delay: 60ms; }
.crystal-enter:nth-child(3) { animation-delay: 120ms; }
```

- **Duration:** 400ms per element.
- **Easing:** geometric-ease.
- **Stagger:** 60ms between siblings. Fast cascade -- crystal lattice forms quickly.
- **Overshoot:** 2% at the 60% keyframe. Crystal slightly overshoots then settles. No bounce.
- **Total cascade example:** 8-item grid = 400ms + (7 x 60ms) = 820ms.
- **Reduced motion:** All items appear instantly. No scale animation. 150ms opacity-only fade.

### 4. Symmetric Mirror (Bilateral Entry)

When elements enter from the sides (e.g., a two-column comparison, a sidebar sliding in), the motion is perfectly symmetric. Left enters from left, right enters from right, both arrive simultaneously.

- **Technique:** Paired `translateX` animations with `symmetric-ease`.

```css
@keyframes enter-from-left {
  from { opacity: 0; transform: translateX(-20px); }
  to   { opacity: 1; transform: translateX(0); }
}

@keyframes enter-from-right {
  from { opacity: 0; transform: translateX(20px); }
  to   { opacity: 1; transform: translateX(0); }
}

.symmetric-left {
  animation: enter-from-left 350ms cubic-bezier(0.42, 0, 0.58, 1) both;
}

.symmetric-right {
  animation: enter-from-right 350ms cubic-bezier(0.42, 0, 0.58, 1) both;
}
```

- **Duration:** 350ms. Both sides arrive simultaneously.
- **Easing:** symmetric-ease. Perfectly balanced ease-in-out -- the mirror symmetry is in the timing as well as the direction.
- **Distance:** 20px. Equal and opposite.
- **Use cases:** Two-column layouts, before/after comparisons, sidebar + content entry.
- **Reduced motion:** Opacity-only fade, 150ms.

### 5. Prismatic Border Sweep (Interaction Feedback)

When a card or input receives focus, the prismatic conic-gradient border rotates 360 degrees once, as if the light source orbits the crystal face. Then it settles into a static prismatic state.

```css
@property --prismatic-start {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

@keyframes prismatic-sweep {
  from { --prismatic-start: 0deg; }
  to   { --prismatic-start: 360deg; }
}

.card:focus-within::before {
  background: conic-gradient(
    from var(--prismatic-start),
    rgba(196,64,64,0.25),
    rgba(184,144,45,0.25),
    rgba(45,139,94,0.25),
    rgba(74,144,196,0.25),
    rgba(59,111,212,0.25),
    rgba(123,94,167,0.25),
    rgba(196,64,64,0.25)
  );
  animation: prismatic-sweep 800ms cubic-bezier(0.25, 0.0, 0.0, 1.0) forwards;
}
```

- **Duration:** 800ms for one full rotation.
- **Easing:** geometric-ease. Starts mechanical, decelerates to a stop.
- **Trigger:** Focus-within on cards, inputs, and interactive containers.
- **Behavior:** Sweeps once (no loop), then holds the end state. The rainbow "settles" into position.
- **Reduced motion:** No rotation. Prismatic border appears instantly via 100ms opacity fade.

---

## Dark Mode Variant

This theme is natively light. The dark variant inverts the crystal: instead of light crystal on pale ground, it becomes a dark crystal lattice where prismatic light is trapped inside.

### Dark Mode Palette

| Token | Light Hex | Dark Hex | Notes |
|---|---|---|---|
| page | `#EAEDF0` | `#0E1015` | Deep space. The void between crystal formations. Near-black with cold blue undertone. |
| bg | `#F0F2F4` | `#14171C` | Primary dark surface. Cold dark graphite. |
| surface | `#F7F8FA` | `#1C2028` | Cards, inputs. Slightly lighter. A dark crystal face. |
| recessed | `#E2E5E9` | `#0A0D12` | Code blocks. Darker than bg -- a cavity in the crystal. |
| active | `#D5D9DE` | `#252A34` | Active items. Lighter to signal interaction on dark. |
| text-primary | `#1A1D21` | `#E8EAF0` | Primary text. Cool blue-white. |
| text-secondary | `#5C636E` | `#8A90A0` | Secondary text. Lifted platinum. |
| text-muted | `#8E95A0` | `#50586A` | Muted text. Darker in dark mode. |
| border-base | `#A0A8B4` | `#35394A` | Darker wireframe platinum. Same opacity system, darker base. |
| accent-primary | `#3B6FD4` | `#5B8EE8` | Lifted sapphire for dark-bg contrast. |
| accent-secondary | `#7B5EA7` | `#9B7EC7` | Lifted amethyst. |

### Dark Mode Rules

- **Facet gradients invert:** Instead of highlight-to-shadow, dark mode uses subtle lighter-to-base gradients. Highlight opacity drops to `0.08` (instead of `0.5`). The crystal face catches less light in the dark.
- **Wireframe overlays become brighter:** Grid lines use `rgba(80, 88, 106, 0.10)` -- slightly more visible against dark backgrounds to maintain the structural scaffold.
- **Prismatic borders intensify:** Conic-gradient opacity increases by ~5-8% in dark mode. The rainbow is more visible when light refracts through dark crystal.
- **Shadows become lighter and softer:** Card shadows use `rgba(0, 0, 0, 0.20)` instead of `rgba(26, 29, 33, 0.04)`. Popover shadow uses `rgba(0, 0, 0, 0.35)`.
- **Surface elevation goes lighter:** `page` < `bg` < `surface` < `active` -- each step is lighter in dark mode.
- **Facet top-edge highlight:** `border-top: 0.5px solid rgba(255, 255, 255, 0.06)` (reduced from 0.5 in light mode).
- **Light-Catch Sparkle becomes more dramatic:** Prismatic sparkle opacity increases to 0.8 in dark mode -- light is rarer and more precious in the dark crystal.
- **Selection color remains sapphire** but opacity increases to 20% for visibility.
- **Scrollbar thumb:** `rgba(80, 88, 106, 0.30)`.
- **Tooltip bg:** `#E8EAF0` (text-primary becomes bg); `color: #0E1015`. Inverted from light mode, but the other direction.

---

## Data Visualization

| Property | Value |
|---|---|
| Categorical palette | Sapphire `#3B6FD4`, Ruby `#C44040`, Citrine `#B8902D`, Emerald `#2D8B5E`, Amethyst `#7B5EA7`, Ice Blue `#4A90C4`. Max 6 hues (the prismatic spectrum). |
| Sequential ramp | Sapphire single-hue: `#C4D4F0` (lightest) -> `#8AAAE4` -> `#5B8EE8` -> `#3B6FD4` -> `#2D5BB8` (darkest) |
| Diverging ramp | Ruby-to-Sapphire: `#C44040` -> `#D88080` -> `#F0F2F4` (neutral center) -> `#8AAAE4` -> `#3B6FD4` |
| Grid style | visible. Axes in text-muted, gridlines in border-base at 8% opacity. Crystal grids are visible -- they are the structure. |
| Max hues per chart | 4. Prismatic, but not chaotic. |
| Philosophy | annotated. Labels on data points with Geist Mono. Minimal axes. Geometric precision in every label placement. |
| Number formatting | Geist Mono with `font-variant-numeric: tabular-nums`. Right-aligned in columns. |
| Chart strokes | 1.5px for primary series, 1px for secondary. No fill areas -- wireframe aesthetics. |

---

## Mobile Notes

### Effects to Disable

- **Prismatic conic-gradient borders:** Replace with solid sapphire borders (`1px solid rgba(59, 111, 212, 0.3)`). Conic-gradient rendering is expensive on mobile GPUs.
- **Facet angle variation (`:nth-child`):** Use a single facet angle (172deg) for all cards. Removes the per-card gradient calculation.
- **Facet Rotation animation:** Disable. Static facet gradient.
- **Light-Catch Sparkle:** Disable. No vertex sparkles on mobile.
- **Prismatic Border Sweep:** Disable. Prismatic border appears instantly on focus.
- **Wireframe grid overlay:** Disable on screens below 768px. Grid pattern is invisible at small scales anyway.
- **Backdrop blur on popovers:** Reduce from `blur(16px)` to `blur(8px)`.

### Sizing Adjustments

- **Touch targets:** All interactive elements minimum 44px. Sidebar items (32px on desktop) expand to 44px on mobile.
- **Card padding:** Reduce from 20px to 16px on screens below 640px.
- **Content padding:** 16px horizontal on mobile (vs centered max-width on desktop).
- **Typography:** Display role reduces from 36px to `clamp(24px, 6vw, 36px)`. All other roles remain fixed.
- **Crystal stagger delay:** Reduce from 60ms to 30ms. Mobile users expect faster pacing.
- **Spacing scale upper end:** 32px and 40px spacings reduce to 24px and 32px on mobile.
- **Border-radius:** Remains small (4-6px). No adjustment needed -- geometric shapes work at all sizes.

### Performance Notes

- This theme is moderately performance-conscious. The facet gradient (linear-gradient) is inexpensive. The prismatic border (conic-gradient + mask-composite) is the most expensive visual.
- Primary performance concern is the prismatic border on many simultaneous elements. On mobile, limit prismatic borders to the focused/active element only -- not all cards.
- Wireframe grid patterns are cheap (CSS background-image) but unnecessary at mobile scales.
- No WebGL, no particles, no Canvas -- this theme is CSS-only.
- The `@property` CSS feature (used for `--facet-angle` and `--prismatic-start` animations) is supported in Chrome 85+, Safari 15.4+, Firefox 128+. For older browsers, degrade to static values.

---

## Implementation Checklist

- [ ] **Fonts loaded:** Instrument Sans (400, 500, 600, 700), Albert Sans (400, 500, 600), Geist Mono (400, 500) with `font-display: swap`
- [ ] **CSS custom properties defined:** All color tokens, shadow tokens, facet gradient tokens, prismatic gradient tokens, border tokens, radius tokens, spacing scale, motion easings, layout values as `:root` variables
- [ ] **`@property` declarations present:** `--facet-angle` and `--prismatic-start` for animatable CSS custom properties
- [ ] **Font smoothing applied:** `-webkit-font-smoothing: antialiased` on `<html>`
- [ ] **Typography matrix implemented:** All 10 roles with correct family, size, weight, line-height, letter-spacing, features
- [ ] **Family switch boundary respected:** Instrument Sans for Display/Heading only. Albert Sans for all other roles.
- [ ] **Uppercase labels applied:** Button role uses `text-transform: uppercase`, `letter-spacing: 0.02em`. Label role uses `text-transform: uppercase`, `letter-spacing: 0.08em`.
- [ ] **Border-radius kept geometric:** none (0px), sm (3px), md (4px), lg (6px), xl (8px), 2xl (12px), input (4px), full (9999px for toggles only)
- [ ] **Faceted surfaces implemented:** All cards and elevated surfaces carry directional linear-gradient with varying facet angles via `:nth-child()`
- [ ] **Facet top-edge highlight:** `border-top: 0.5px solid rgba(255, 255, 255, 0.5)` on premium/hero cards
- [ ] **Prismatic borders implemented:** Conic-gradient via `::before` pseudo-element with mask-composite technique on cards (hover), chat input (focus), modals (always)
- [ ] **Wireframe grid overlay present:** CSS background-image grid pattern on page-level containers
- [ ] **Shadow tokens applied per state:** rest/hover/focus on cards and inputs, popover on menus. All shadows are geometric (low blur, sharp).
- [ ] **Border opacity system implemented:** All borders use wireframe platinum at correct opacity (subtle 10%, card 18%, hover 26%, focus 36%)
- [ ] **Focus ring on all interactive elements:** `outline: 2px solid rgba(59, 111, 212, 0.45)`, `outline-offset: 2px` on `:focus-visible`
- [ ] **Disabled states complete:** opacity 0.4 + pointer-events none + cursor not-allowed + shadow none + facet effect none
- [ ] **`prefers-reduced-motion` media query present:** All animations wrapped or checked. Facet rotation, sparkle, crystal growth, prismatic sweep disabled.
- [ ] **Scrollbar styled:** `scrollbar-width: thin`, `scrollbar-color: rgba(160, 168, 180, 0.28) transparent`
- [ ] **`::selection` styled:** `background: rgba(59, 111, 212, 0.14)`, `color: #1A1D21`
- [ ] **Touch targets >= 44px on mobile**
- [ ] **State transitions match motion map:** Each component uses its specified duration and easing. Geometric-ease for card/input shadow transitions.
- [ ] **Caret color set:** `caret-color: #3B6FD4` on all text inputs.
- [ ] **Dark mode variant tokens prepared:** CSS custom properties structured for `prefers-color-scheme: dark` or class-based theme switching.
- [ ] **Monochrome dominance verified:** Visual audit confirming palette is 90% cool grey/white, 10% prismatic/accent. Rainbow never dominates.
- [ ] **Data visualization tokens applied:** Prismatic categorical palette, sapphire sequential ramp, wireframe grid style, Geist Mono tabular-nums.
- [ ] **Mobile adjustments applied:** Prismatic borders simplified, facet variation disabled, wireframe grid removed, stagger reduced, touch targets expanded.
