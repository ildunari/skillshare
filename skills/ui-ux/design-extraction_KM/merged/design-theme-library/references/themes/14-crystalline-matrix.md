## 14. Crystalline Matrix

> Diamond facets, prismatic light splitting, geometric precision — math made visible.

**Best for:** Fractal explorers, geometric simulations, Voronoi/Delaunay, data structures, crystal growth, molecular visualization.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Crystal White | `#F0F4F8` | Cool, bright, clean. Slight blue tint. |
| Surface | Ice | `#E8ECF0` | Faceted panels, elevated cards. |
| Primary | Prismatic Rainbow | gradient | Light splitting through crystal — cyan/magenta/yellow. |
| Secondary | Platinum | `#E5E4E2` | Structural lines, borders, mesh wireframes. |
| Accent | Diamond Spark | `#FFFFFF` | Pure white flash on facet edges catching light. |
| Deep | Graphite | `#2C2C2C` | Text, deep contrast, shadow facets. |
| Facet Shadow | Cool Blue-Grey | `#98A8B8` | Shading on non-light-facing facets. |
| Border | Silver Wire | `#C0C4C8` | Wireframe edges, structural lines. |

### Typography
- **Display:** Instrument Sans (600) — modern, condensed, precision
- **Body:** Albert Sans — Scandinavian minimalism, crystal clarity
- **Mono:** Geist Mono — geometric, modern, for data values

### Visual Style
- **Faceted Surfaces:** All shapes are rendered as faceted (low-poly) rather than smooth. Voronoi cells get explicit edge lines. Circles become polygons (12-24 sides).
- **Prismatic Light:** Color comes from simulated light refraction. Rainbow appears at edges where surfaces meet, using `conic-gradient` or `linear-gradient` with rainbow stops.
- **Wireframe Accent:** Behind solid shapes, a lighter wireframe version is visible (5-10% opacity), like seeing the crystal structure beneath the surface.
- **High Contrast Edges:** Where facets meet, edges are highlighted — either bright white (light-catching) or dark graphite (shadow edge). This creates the crystal facet effect.
- **Specular Highlights:** Small, bright white spots on surfaces facing the (simulated) light source. CSS: tiny white radial gradient positioned at the highlight point.

### Animation Philosophy
- **Easing:** Geometric — `cubic-bezier(0.5, 0, 0.5, 1)` (ease-in-out-quad). Symmetric, mathematical.
- **Timing:** Moderate. Geometric morphs 400-600ms. Sparkle flashes 100-200ms.
- **Motion Character:** Precise, angular. Rotations are exact (30°, 60°, 90°). No organic wobble.
- **Physics:** Rigid body. Things rotate and translate with precision, no deformation.

### Signature Animations
1. **Facet Rotation** — 3D geometric elements rotate slowly (10-15s/revolution) on one axis, with facet shading updating per frame. Like examining a gem.
2. **Light Catch Sparkle** — As elements rotate or the viewport scrolls, random facets briefly flash pure white (100ms) as they "catch the light."
3. **Crystal Growth** — New elements grow outward from a seed point — one facet at a time, staggered 50ms apart. Like real crystal formation.
4. **Prismatic Edge** — On hover, element borders briefly show a rainbow gradient sweep (animated `linear-gradient` position, 800ms).
5. **Shatter Transition** — When removing/transitioning elements, they break into triangular shards that scatter with slight rotation. Voronoi-based decomposition of the element.

### UI Components
- **Buttons:** Crystal white fill, graphite text. Platinum border (1px). `border-radius: 2px` (sharp, crystalline). Hover: prismatic edge animation. Active: facet inversion (dark fill, white text).
- **Sliders:** Track is silver wire 1px. Thumb is a small diamond shape (rotated square, 12px). Pure platinum.
- **Cards:** Ice surface. Silver wire border (1px). `border-radius: 2px`. Faceted shadow (two overlapping shadows at different angles to simulate facet depth).
- **Tooltips:** Crystal white, graphite text. Silver border. Geometric precision — tight padding, exact alignment.
- **Dividers:** Silver wire 1px. Or a row of tiny diamond shapes (◆) at 30% opacity.

### Dark Mode Variant

Crystalline Matrix has a full dark mode — not an afterthought, a first-class variant. Geode interior — prismatic light splitting in darkness is MORE dramatic, not less.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F0F4F8` Crystal White | `#060608` Obsidian | oklch(0.04 0.005 280) — near-black with cool blue cast |
| Card / surface | `#E8ECF0` Ice | `#0A0A10` Dark Crystal | oklch(0.07 0.005 280) — faceted panels |
| Alt surface | — | `#121218` Deep Facet | oklch(0.10 0.005 280) — secondary panels |
| Border | `#C0C4C8` Silver Wire | `#1E1E24` Facet Edge | oklch(0.15 0.005 280) — wireframe edges |
| Border heavy | — | `#2A2A32` Bright Edge | oklch(0.20 0.005 280) — hover, emphasis |
| Primary text | `#2C2C2C` Graphite | `#E0E4E8` Cool Platinum | oklch(0.92 0.005 240) — bright, crisp |
| Secondary text | `#98A8B8` Facet Shadow | `#8A90A0` Muted Crystal | oklch(0.62 0.01 260) — annotations |
| Dim text | — | `#5A5E6A` Deep Facet | oklch(0.42 0.01 260) — metadata |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Prismatic Rainbow | cyan→magenta→yellow gradient | INTENSIFIED — full saturation | Prismatic refraction is MORE dramatic against dark — the theme's defining effect |
| Platinum | `#E5E4E2` | `#3A3A40` Dark Platinum | Platinum becomes structural — no longer a surface color |
| Graphite | `#2C2C2C` (text) | `#1E1E24` (border) | Former text color becomes border infrastructure |
| Diamond Spark | `#FFFFFF` | `#FFFFFF` at higher contrast | Specular highlights become dramatic — white sparks on near-black |

#### Shadow & Depth Adaptation
- Light: Faceted shadow — two overlapping shadows at different angles simulating crystal depth
- Dark: Shadows disappear. Replace with prismatic edge glow — `0 0 12px rgba(rainbow)` using the prismatic gradient. Specular highlights become dramatic white points on near-black surfaces. Crystal facets are defined by edge luminance (bright edges on dark faces) rather than shadow (dark edges on bright faces)

#### Texture & Grain Adaptation
- Light: Wireframe overlay at 5-10% opacity behind solid shapes — crystal lattice structure
- Dark: Wireframe overlay at 8-12% opacity — more visible against dark, revealing the matrix structure. Crystal growth animation sparks increase in intensity. The prismatic `conic-gradient` and `linear-gradient` effects produce their most stunning results against the obsidian background

#### Dark Mode Rules
- Prismatic rainbow effects INTENSIFY on dark — increase saturation and consider widening the gradient spread
- Crystal growth animation: increase spark intensity by 1.5x — white sparks against obsidian are the drama
- Specular highlights (`#FFFFFF` points) become the primary depth cue — position them to define facet geometry
- Wireframe overlay increases opacity — the crystal lattice structure is more visible and beautiful against dark
- "Geode interior — prismatic light splitting in darkness is MORE dramatic, not less"

### Mobile Notes
- Facet rotation: use CSS `transform: rotate3d()` (GPU-composited).
- Sparkle flash: reduce frequency on mobile (every 2-3s instead of random).
- Shatter transition: reduce shard count to 6-8 on mobile (from 15-20).
- Wireframe overlay: remove on mobile (extra draw call).
