## 27. Cartographer's Desk

> Map-room pragmatism: contour lines, layered paper, precise labeling. Built for data-dense dashboards and geospatial tools.

**Best for:** Maps, dashboards, investigative journalism, geospatial tools, supply chain viz, urban planning, climate data.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Chart Paper | `#F0EBE0` | Primary canvas. Warm, like aged map paper. |
| Alt Background | Vellum Layer | `#F8F4EC` | Cards, legend panels, inset maps. |
| Primary Text | Cartographer's Ink | `#1C2428` | Body text, labels. Dense, clear. |
| Secondary Text | Pencil Graphite | `#6A7070` | Secondary labels, annotations, coordinates. |
| Accent 1 | Meridian Blue | `#2E6A96` | Water features, primary links, selected states. |
| Accent 2 | Terrain Ochre | `#C08840` | Land features, warnings, highlighted regions. |
| Accent 3 | Forest Green | `#3A6848` | Vegetation, success states, positive data. |
| Contour Line | Elevation Brown | `#A08A70` | Contour patterns, topographic decoration, dividers. |

### Typography
- **Display:** Instrument Sans (600 weight) — dashboard precision, clean at all sizes
- **Body:** Albert Sans (400 weight) — high readability, pairs naturally with Instrument
- **Mono:** JetBrains Mono — coordinates, data labels, numeric readouts

### Visual Style
- **Contour Patterns:** Procedural contour line SVGs (concentric irregular ellipses in elevation-brown at 8% opacity) as section backgrounds. Generated with noise-displaced circles. Each section gets unique topology.
- **Map Paper Grain:** Static feTurbulence (`baseFrequency="0.6"`, 1 octave) at 2.5% opacity. Warm and fibrous.
- **Layered Paper:** Cards appear as paper layers stacked on the desk — each layer has a distinct 1px border + very subtle directional shadow (`2px 2px 0 rgba(0,0,0,0.04)`). No elevation blur.
- **Legend-Style Labels:** Labels use small caps (`font-variant: small-caps`) + generous letter-spacing (0.05em). Like a map legend.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` — standard ease, purposeful.
- **Timing:** Medium. Pan transitions 300ms. Zoom 250ms. Labels 200ms.
- **Motion Character:** Spatial continuity. Panning, zooming, parallax between paper layers. Everything has a position in 2D space.
- **Physics:** None. Cartographic — precise, measured, no chaos.

### Signature Animations
1. **Contour Draw** — On scroll-reveal, contour lines draw themselves with `stroke-dashoffset` from center outward. 800ms.
2. **Layer Parallax** — Stacked paper cards shift ±2px on mouse move (or device tilt), creating subtle desk parallax.
3. **Pin Drop** — Data points on maps appear with a drop animation: fall from 10px above with bounce (`scale(0.8) → scale(1.1) → scale(1)`). 300ms.
4. **Compass Rose Spin** — Loading indicator: a minimal compass rose that rotates at 2s/revolution with `ease-in-out`.
5. **Legend Slide** — Legend panels and sidebars slide from their edge with a paper-shuffle feel: 250ms, slight initial delay (50ms) as if lifting the paper stack.

### UI Components
- **Buttons:** Primary: meridian blue fill, vellum text, `border-radius: 3px`. Secondary: 1px elevation-brown border, cartographer's-ink text. Hover: darken 8%. Active: hard inset shadow (`inset 1px 1px 0 rgba(0,0,0,0.1)`).
- **Sliders:** Track is 2px elevation-brown line. Thumb is 12px meridian-blue circle with 1px ink border. Value in JetBrains Mono.
- **Cards:** Vellum background, 1px elevation-brown border. `border-radius: 3px`. Directional shadow. Padding 16px.
- **Tooltips:** Cartographer's ink background, chart paper text. JetBrains Mono 11px. `border-radius: 2px`. Contains coordinate-style data.
- **Dividers:** Elevation brown at 30% opacity. 1px. Or a thin contour-line SVG divider.

### Dark Mode Variant

Cartographer's Desk has a full dark mode — not an afterthought, a first-class variant. Midnight field survey: head-torch illumination on topographic maps, working under lamplight in the field.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F0EBE0` Chart Paper | `#0C0E10` night field | Slightly cool dark — field conditions at night |
| Card / surface | `#F8F4EC` Vellum Layer | `#14181C` dark map case | Cool-tinted dark surface, like a leather map case |
| Border | `#A08A70` Elevation Brown | `#242A30` dark leather edge | Cool dark mid-tone for structural boundaries |
| Border heavy | `#A08A70` at full | `#2A3038` steel edge | Section dividers, heavier topographic rules |
| Primary text | `#1C2428` Cartographer's Ink | `#E8E4DA` at 87% aged paper glow | APCA Lc ~82 on `#14181C` — warm text on cool ground |
| Secondary text | `#6A7070` Pencil Graphite | `#98968E` warm graphite | Annotations, coordinates — pencil on dark paper |
| Dim text | `#6A7070` at lower opacity | `#606868` cool grey | Tertiary labels — field notes in dim light |
| Contour decoration | `#A08A70` at 8% | `#605840` at 15% | Contour lines more visible on dark — headlamp pickup |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Meridian Blue | `#2E6A96` | `#4A8CC0` brightened | Water features glow — rivers catch moonlight |
| Terrain Ochre | `#C08840` | `#D09850` brightened | Contour lines catch lamplight — warm lift |
| Forest Green | `#3A6848` | `#50886A` brightened | Vegetation reads clearly under head-torch |
| Elevation Brown | `#A08A70` contours | `#605840` at 15% opacity | Topographic lines visible on dark paper |

#### Shadow & Depth Adaptation
- Light: `2px 2px 0 rgba(0,0,0,0.04)` — directional, subtle, like layered map sheets
- Dark: Shadow deepens to `2px 2px 0 rgba(0,0,0,0.2)`. Map-case layering: each card is a sheet on the dark desk. Add subtle top-edge catch: `inset 0 1px 0 rgba(232,228,218,0.03)` — lamplight on paper edge

#### Texture & Grain Adaptation
- Light: feTurbulence map paper grain at 2.5% opacity, `overlay` blend. Procedural contour SVGs at 8% opacity
- Dark: Map paper grain drops to 1.5% opacity, blend shifts to `soft-light`. Contour SVGs: stroke shifts from brown-on-cream to cream-on-dark — `stroke` color becomes `rgba(232,228,218,0.06)`. Same procedural generation, same noise displacement. Only the rendering direction inverts

#### Dark Mode Rules
- Slightly cool dark is intentional — night fieldwork has a blue-grey quality, unlike warm indoor themes
- Contour line SVGs are the signature element: they MUST survive the mode switch. Same topology, inverted rendering
- Legend-style labels (`font-variant: small-caps`, generous letter-spacing) preserved exactly — the cartographic voice is in the typography
- Layer parallax preserved: ±2px shift on mouse/tilt. Dark layers create stronger depth separation
- "Midnight field survey — head-torch illumination on topographic maps"

### Mobile Notes
- Disable contour line drawing animation (SVG complexity).
- Disable layer parallax (gyroscope is unreliable + battery drain).
- Simplify pin drop to a standard fade-in.
- Touch targets: 48px minimum for map interactions.
