## 25. Botanical Blueprint

> Scientific illustration meets botanical field notes — grids, annotations, gentle greens, "ink + watercolor" separation.

**Best for:** Education, scientific dashboards, simulations, biology tools, environmental data, research interfaces.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Field Paper | `#F5F3EE` | Primary canvas. Cool cream, like botanical illustration paper. |
| Alt Background | Grid Paper | `#EDEAE4` | Cards, data tables, secondary surfaces. |
| Primary Text | Specimen Ink | `#1E2A24` | Body text. Deep green-black, like botanical illustration ink. |
| Secondary Text | Graphite Note | `#5A6660` | Annotations, captions, secondary labels. |
| Accent 1 | Leaf Green | `#3A7A50` | Primary interactive, links, botanical data. |
| Accent 2 | Sepia Wash | `#A0784C` | Annotations, highlights, warm secondary accent. |
| Accent 3 | Blueprint Blue | `#4A7896` | Charts, technical diagrams, informational. |
| Border | Pencil Line | `#C8C4BA` | Grid lines, card borders, axes. |

### Typography
- **Display:** Albert Sans (600 weight) — clean, scientific clarity with slight warmth
- **Body:** Instrument Sans (400 weight) — designed for dashboards and data, excellent small-size legibility
- **Mono:** JetBrains Mono — measurements, coordinates, data labels

### Visual Style
- **Blueprint Grid:** Faint grid lines (pencil-line color at 15% opacity) drawn at 20px intervals on data-heavy sections. CSS `background-image: repeating-linear-gradient`. Creates the field-notebook substrate.
- **Watercolor Washes:** Hero areas and section headers use a low-opacity (`8–12%`) radial gradient in leaf-green or blueprint-blue, mimicking watercolor washes behind specimen drawings.
- **Annotation Style:** Labels, callouts, and measurement lines use sepia-wash color. Leader lines (1px, dashed) connect annotations to their targets. This is the theme's signature — information presented as annotated specimens.
- **Ink + Wash Separation:** Primary content (text, data, UI) is crisp ink-style. Background decoration is soft watercolor wash. The two layers never compete.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` — standard ease, clinical and controlled.
- **Timing:** Medium. Data transitions 300ms. Annotations draw at 400ms. Nothing dramatic.
- **Motion Character:** Diagrammatic. Elements slide along grid axes (vertical or horizontal, never diagonal). Transitions explain spatial relationships.
- **Physics:** None. This is measurement and observation, not play.

### Signature Animations
1. **Annotation Draw** — Labels appear with a leader-line drawing itself (`stroke-dashoffset`) from data point to label position, then text fades in. 500ms total.
2. **Specimen Slide** — Content blocks enter along grid axes (left-to-right or bottom-to-top), snapping to grid positions. 300ms ease-out.
3. **Watercolor Bleed** — Hero section wash gradients expand their radius over 800ms on page load, like watercolor spreading on wet paper.
4. **Measurement Reveal** — Data values count up from 0 to their actual value over 600ms, like a measurement being taken.
5. **Grid Fade** — Background grid lines fade in section-by-section as the user scrolls, as if the notebook is being drawn in real-time.

### UI Components
- **Buttons:** Primary: leaf green fill, field paper text, `border-radius: 4px`. Secondary: 1px pencil-line border, specimen-ink text. Hover: darken 8%. Active: `scale(0.98)`. Text in Instrument Sans 500.
- **Sliders:** Track is 2px pencil line. Thumb is 12px leaf-green circle with 1px specimen-ink border. Value in JetBrains Mono with unit labels (px, ms, %).
- **Cards:** Grid paper background, 1px pencil-line border. `border-radius: 4px`. Optional: faint grid lines continue through the card. Padding 16px.
- **Tooltips:** Specimen ink background, field paper text. JetBrains Mono 12px (data-centric tooltips). `border-radius: 3px`.
- **Dividers:** Pencil line at 40% opacity. 1px. Or a thin sepia annotation line with small caps label.

### Dark Mode Variant

Botanical Blueprint has a full dark mode — not an afterthought, a first-class variant. Botanical field station at midnight — specimens lit by filtered lamp.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F5F3EE` Field Paper | `#0A0E0C` Dark Field | oklch(0.07 0.01 150) — green-tinted black, like forest floor at night |
| Card / surface | `#EDEAE4` Grid Paper | `#141A16` Dark Foliage | oklch(0.11 0.01 150) — elevated specimen cards |
| Alt surface | — | `#1C221E` Deep Foliage | oklch(0.14 0.01 150) — secondary panels |
| Border | `#C8C4BA` Pencil Line | `#202A24` Dark Stem | oklch(0.18 0.01 150) — card edges, grid axes |
| Border heavy | — | `#2C3830` Bright Stem | oklch(0.23 0.01 150) — section dividers |
| Primary text | `#1E2A24` Specimen Ink | `#E4E8E4` Moonlit Paper | oklch(0.92 0.005 150) at 87% opacity |
| Secondary text | `#5A6660` Graphite Note | `#96A098` Night Note | oklch(0.67 0.01 150) — annotations, captions |
| Dim text | — | `#687068` Dark Note | oklch(0.47 0.01 150) — metadata, timestamps |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Leaf Green | `#3A7A50` | `#50A070` (brighter) | Bioluminescent — specimens glow with life in the dark field station |
| Sepia Wash | `#A0784C` | `#C09060` (brighter) | Lamplight notes — warm annotation ink under midnight lamplight |
| Blueprint Blue | `#4A7896` | `#6098B8` (brighter) | Cyanotype glow — technical diagram lines lift for dark bg contrast |
| Grid lines | `#C8C4BA` at 15% | white at 5% on dark | White lines replace grey — reversed grid visibility |

#### Shadow & Depth Adaptation
- Light: Minimal — 1px borders and slight background color shifts define depth
- Dark: Same minimalism. Depth from border color (`#202A24` dark stem) against surface color (`#141A16` dark foliage). No shadows added — this is a scientific theme, not decorative. Annotation leader lines (1px dashed) shift to `#96A098` night-note color for visibility

#### Texture & Grain Adaptation
- Light: Blueprint grid at 15% opacity, 20px intervals. Watercolor washes at 8-12% opacity in leaf-green and blueprint-blue
- Dark: Grid background shifts to white lines at 5% opacity on dark (instead of grey at 8% on light) — faint notebook grid visible by lamplight. Watercolor washes become subtle luminous patches at 4-6% opacity with `screen` blend mode — they glow faintly rather than wash. The ink + wash separation is preserved: crisp text/data (ink) sits on soft luminous patches (wash)

#### Dark Mode Rules
- Green-tinted black background (`#0A0E0C`) maintains the botanical identity — not neutral grey, distinctly organic
- Annotation style preserved: sepia leader lines (dashed, 1px) connect labels to specimens, now in brightened `#C09060` for lamplight warmth
- Watercolor washes shift from radial gradients to luminous patches — `screen` blend mode, lower opacity, creating subtle bioluminescent pools
- Grid lines at 5% white (not 8% grey) — the field notebook substrate remains visible but inverted for dark
- "Botanical field station at midnight — specimens lit by filtered lamp"

### Mobile Notes
- Hide blueprint grid lines (too fine for mobile displays).
- Simplify annotation draw to a standard fade-in.
- Touch targets: 44px minimum. Maintain annotation-style labels for data clarity.
