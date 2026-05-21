## 8. Brutalist Concrete

> Raw, exposed, honest — Tadao Ando meets Swiss International typography. Nothing hides.

**Best for:** Data-heavy dashboards, developer tools, technical simulations, CLI visualizations, system monitors, debugging UIs.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Raw Concrete | `#B8B4AE` | Exposed, textured, honest. |
| Surface | Lighter Concrete | `#CECAC4` | Elevated panels, input fields. |
| Primary | Near Black | `#1A1A1A` | Text, data, primary elements. |
| Accent | Structural Red | `#E63946` | Warnings, critical data, CTA. Sparingly. |
| Secondary | Rebar Grey | `#8C8680` | Grid lines, borders, secondary text. |
| Exposed | Raw White | `#F5F0EB` | Data fields, input backgrounds, white space. |
| Grid | Formwork Line | `#A09A94` | Visible grid structure, like concrete formwork. |
| Text | Near Black | `#1A1A1A` | Same as primary. Monochrome palette. |

### Typography
- **Display:** Space Grotesk (700) — geometric, techy, distinctive. Or: any heavy grotesque.
- **Body:** Space Grotesk (400) — same family, different weight. Brutalism = one typeface.
- **Mono:** JetBrains Mono — the ONLY other face. Data, values, code.

**Rule:** Maximum two typefaces. This theme's typography IS its identity.

### Visual Style
- **Exposed Grid:** Visible grid lines at all times. 1px rebar grey lines creating a modular grid. Content aligns to it visibly. The grid is not hidden — it's a feature.
- **Concrete Texture:** SVG `feTurbulence` overlay (subtle, 2-3% opacity, `baseFrequency="0.8"`) creating concrete grain. Or CSS noise pattern.
- **No Rounded Corners:** `border-radius: 0` on everything. Sharp right angles only. This is non-negotiable for this theme.
- **Raw Borders:** 2px solid borders in near-black. Visible, structural, like rebar. No shadows.
- **Monochrome + One:** 95% greyscale. Red accent used for ONE purpose only (usually critical state or primary CTA).

### Animation Philosophy
- **Easing:** `linear` or `steps(n)`. Mechanical, precise, machine-like. No organic curves.
- **Timing:** Fast, decisive. 150-200ms. Or zero — instant state changes. Brutalism doesn't fuss.
- **Motion Character:** Mechanical, utilitarian. Slide, snap, done. No overshoot, no spring, no bounce.
- **Physics:** None. This theme rejects physics simulation for UI. Things appear or they don't.

### Signature Animations
1. **Hard Cut** — No transition. Elements appear/disappear instantly. `display: none → block`. Brutally honest.
2. **Typewriter Data** — Numeric values type in character-by-character at 30ms/char. Monospace ensures alignment.
3. **Grid Reveal** — On load, the grid lines draw themselves (stroke-dashoffset) before content appears on top.
4. **Red Flash** — Critical state changes flash the accent red for 200ms on the relevant element's border/background.
5. **Scan Line** — A thin horizontal line (1px, red, 20% opacity) sweeps top-to-bottom across the canvas every 4s. Monitor aesthetic.

### UI Components
- **Buttons:** Near-black fill, raw white text. `border-radius: 0`. 2px border. ALL CAPS text in Space Grotesk 600. Hover: invert (white fill, black text). Active: red border flash.
- **Sliders:** Thick track (6px, near-black). Square thumb (16×16px, raw white, 2px black border). No rounding anywhere.
- **Cards:** Lighter concrete fill. 2px near-black border. No shadow. No radius. Padding 16px. Grid-aligned.
- **Tooltips:** Near-black fill, raw white text. Monospace. Square corners. Functional.
- **Dividers:** 2px near-black lines. Full-width. Or exposed grid lines serve as dividers.

### Dark Mode Variant

Brutalist Concrete has a full dark mode — not an afterthought, a first-class variant. Night construction site. Raw concrete in darkness.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#B8B4AE` Raw Concrete | `#0E0E0E` Night Concrete | oklch(0.08 0.00 0) — pure neutral, zero warmth |
| Card / surface | `#CECAC4` Lighter Concrete | `#1A1A1A` Dark Slab | oklch(0.13 0.00 0) — elevated panels |
| Alt surface | `#F5F0EB` Raw White | `#242424` Deep Slab | oklch(0.17 0.00 0) — input fields, data areas |
| Border | `#8C8680` Rebar Grey | `#333333` Exposed Rebar | oklch(0.23 0.00 0) — 2px structural borders preserved |
| Border heavy | `#1A1A1A` Near Black | `#444444` Bright Rebar | oklch(0.30 0.00 0) — hover state, emphasis |
| Primary text | `#1A1A1A` Near Black | `#E8E6E2` Concrete Dust | oklch(0.92 0.005 80) at 87% — slightly warm white |
| Secondary text | `#8C8680` Rebar Grey | `#A09890` Lifted Rebar | oklch(0.68 0.01 60) — lightened for dark bg |
| Dim text | — | `#666666` Dark Rebar | oklch(0.44 0.00 0) — timestamps, metadata |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Structural Red | `#E63946` | `#E63946` (unchanged) | Structural red on raw concrete is iconic. No adjustment needed |
| Formwork Grid | `#A09A94` at visible | `#333333` at visible | Grid lines shift to lighter-than-bg to remain visible |
| Raw White (data) | `#F5F0EB` | `#E8E6E2` | Data fields use primary text color on dark surfaces |

#### Shadow & Depth Adaptation
- Light: No shadows. This is brutalism — `box-shadow: none`. Depth from 2px borders only
- Dark: STILL no shadows. ZERO decoration rule preserved. Dark mode does NOT mean adding glow. Depth from borders and surface color steps only. 2px solid borders in `#333333` define all card edges. The brutalist principle is absolute

#### Texture & Grain Adaptation
- Light: `feTurbulence` at 2-3% opacity, `baseFrequency="0.8"`, overlay blend mode
- Dark: Same `feTurbulence`, reduced to 2% opacity, `soft-light` blend mode. Same frequency and octaves — the concrete texture is still present but recalibrated for dark. Industrial identity depends on texture being visible but not dominant

#### Dark Mode Rules
- Zero warmth in the dark palette — `#0E0E0E` is pure neutral, not warm dark grey
- 2px structural borders preserved — they switch from near-black to `#333333` but maintain the same visual weight
- Grid lines at `#333333` remain visible on `#0E0E0E` background — the grid is essential structure, never hidden
- ZERO decoration rule is ABSOLUTE — dark mode does not add glow, bloom, or any effect that light mode doesn't have
- "Raw concrete in darkness. The red is still red. The grid is still visible. Nothing else"

### Mobile Notes
- This is the most performant theme. Zero blur, zero shadows, zero blend modes.
- Concrete texture overlay can be removed on mobile with zero visual cost.
- Hard cuts (no transitions) = zero animation overhead.
- Perfect for data-heavy dashboards on low-end devices.
