## 21. Mashrabiya Matrix

> Islamic geometric lattice as a systematic grid language — patterns inform layout, not just decoration.

**Best for:** Cultural institutions, educational simulations, data storytelling, museum interactives, architectural tools.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Sand Ivory | `#F4EFE4` | Primary canvas. Desert sand warmth. |
| Alt Background | Alabaster | `#FAF8F2` | Cards, elevated panels. |
| Primary Text | Deep Indigo | `#1A2744` | Body text, headings. Rich, authoritative. |
| Secondary Text | Sandstone | `#7A7060` | Captions, metadata, secondary labels. |
| Accent 1 | Turquoise Tile | `#1A8A7A` | Interactive elements, links, selection. |
| Accent 2 | Lapis Gold | `#C49A3C` | Highlights, ornamental accents, progress. |
| Lattice Line | Henna | `#B86B3A` | Geometric pattern strokes, dividers. |
| Border | Plaster | `#D8D0C4` | Card borders, input outlines. |

### Typography
- **Display:** Playfair Display (600 weight) — high-contrast serif with jewel-like precision
- **Body:** IBM Plex Sans Arabic / IBM Plex Sans — RTL-ready, clean, excellent Latin/Arabic pairing
- **Mono:** IBM Plex Mono — consistent family, strong tabular numerals

### Visual Style
- **Geometric Lattice:** SVG tiling patterns at 3–5% opacity as background texture. Patterns generated from Islamic geometric construction (circle-and-line method). Used in empty states, section backgrounds, and card headers.
- **Symmetry as Structure:** Layout favors bilateral or radial symmetry where content allows. Bento-grid arrangements echo compartmentalized Islamic design.
- **RTL-First:** All layouts account for bidirectional text. UI mirrors cleanly. Reading direction is never assumed.
- **Ornament Earns Its Place:** Geometric patterns appear only where they reinforce information hierarchy (section dividers, empty states, loading screens). Never wallpaper.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` (Material standard ease) — precise, controlled, respectful.
- **Timing:** Medium. Transitions 300–400ms. Lattice unfold effects 600–800ms.
- **Motion Character:** Symmetric and unfolding. Elements expand from center, open like a lattice. No bouncy motion.
- **Physics:** None. Mathematical precision, not physical simulation.

### Signature Animations
1. **Lattice Unfold** — Sections reveal with a radial clip-path expanding from center, paired with subtle scale 0.95→1. Like a geometric pattern being drawn outward. 600ms.
2. **Tile Stagger** — Grid items appear in a diagonal wave stagger (NW→SE or center→edges), 60ms delay each. Evokes tile-laying.
3. **Geometric Spin** — Loading indicator is a slowly rotating geometric star (8-point or 12-point) in turquoise, `transform: rotate()` at 3s/revolution.
4. **Henna Trace** — Dividers draw themselves with `stroke-dashoffset`, like a calligrapher's pen tracing a geometric rule. 400ms.
5. **Symmetry Mirror** — On hover over lattice-patterned elements, the pattern subtly shifts opacity in a radial pulse from the cursor position. 300ms.

### UI Components
- **Buttons:** Primary: turquoise fill, alabaster text, `border-radius: 6px`. Secondary: 1.5px deep-indigo border. Hover: darken turquoise 8%. Active: inset shadow. Text in IBM Plex Sans 500.
- **Sliders:** Track is 3px plaster line with `border-radius: full`. Thumb is 14px turquoise circle. Value in IBM Plex Mono.
- **Cards:** Alabaster background, 1px plaster border. `border-radius: 8px`. Optional: geometric lattice pattern in card header at 4% opacity. Padding 20px.
- **Tooltips:** Deep indigo background, sand ivory text. `border-radius: 4px`. IBM Plex Sans 12px.
- **Dividers:** Henna at 30% opacity, 1px. Or a thin geometric border pattern (SVG, repeating tile).

### Dark Mode Variant

Mashrabiya Matrix has a full dark mode — not an afterthought, a first-class variant. Moonlit courtyard: geometric lattice casts shadow patterns while lantern-glow filters through the screen.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F4EFE4` Sand Ivory | `#080C14` night sky indigo | Deep blue-black — the dark is cool here, not warm. Indigo night sky |
| Card / surface | `#FAF8F2` Alabaster | `#0E1420` deep blue-black | Elevated surfaces are slightly lighter indigo |
| Border | `#D8D0C4` Plaster | `#1E2838` lattice shadow | Cool dark border, geometric precision preserved |
| Border heavy | `#D8D0C4` at full | `#283448` deep lattice | Section dividers, card hover |
| Primary text | `#1A2744` Deep Indigo | `#F4EFE4` at 87% sand ivory glow | APCA Lc ~85 on `#0E1420` — warm text on cool ground, intentional |
| Secondary text | `#7A7060` Sandstone | `#A8A090` lifted sandstone | Readable secondary, warm tint preserved |
| Dim text | `#7A7060` at lower opacity | `#606858` muted sage-grey | Metadata, coordinates — quiet |
| Lattice pattern | dark strokes on light | light strokes on dark | SVG tiling pattern inverts — see texture section |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Turquoise Tile | `#1A8A7A` | `#30B0A0` brightened | Tile catches lantern light — more vivid at night |
| Lapis Gold | `#C49A3C` | `#D4AA50` brightened | Gold leaf illuminated by moonlight |
| Henna lattice | `#B86B3A` | `#D08050` brightened | Warm lattice lines need more presence on dark ground |
| Deep Indigo | `#1A2744` text | structural/border role | Indigo shifts from text to card backgrounds — already dark enough |

#### Shadow & Depth Adaptation
- Light: No explicit shadow — `1px plaster border` provides separation. Clean geometric approach
- Dark: Cards differentiate via indigo-tinted background steps (`#0E1420` on `#080C14`). Add subtle border glow on hover: `box-shadow: 0 0 8px rgba(48,176,160,0.06)` — turquoise lantern light

#### Texture & Grain Adaptation
- Light: SVG tiling patterns at 3–5% opacity as background. Dark strokes on light ground. Islamic geometric construction
- Dark: SVG tiling patterns invert — stroke shifts from dark-on-light to light-on-dark. `stroke` color becomes `rgba(244,239,228,0.04)` (sand ivory at very low opacity). Pattern density unchanged. The geometry is structural, not decorative — it must survive the mode switch intact

#### Dark Mode Rules
- Cool-dark is intentional here — `#080C14` has indigo undertone, unlike the warm darks of other themes. This reflects the night-sky setting
- RTL considerations absolutely preserved — mode switch must not affect directionality, padding, or layout mirrors
- Geometric lattice unfold animation: clip-path and scale values unchanged. Only colors shift
- Henna trace divider animation: stroke color inverts from dark-on-light to bright-on-dark, `stroke-dashoffset` timing unchanged
- "Moonlit courtyard — geometric lattice casts shadow patterns, lantern-glow through screen"

### Mobile Notes
- Simplify lattice SVG patterns to lower-detail versions (fewer vertices).
- Disable lattice unfold clip-path animation; use simple fade instead.
- Touch targets: 48px minimum. Generous padding for RTL/LTR mixed layouts.
