## 7. Midnight Observatory

> Deep space meets editorial cartography — celestial precision, warm gold on infinite navy.

**Best for:** Data visualizations, star maps, scientific simulations, time-series dashboards, astronomical models, network graphs.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Deep Navy | `#0B1426` | Infinite depth. The night sky. |
| Surface | Dark Indigo | `#141E33` | Elevated panels, cards. |
| Primary Data | Warm Gold | `#FFD700` | Key data points, stars, primary metrics. |
| Secondary Data | Muted Teal | `#4A9B9B` | Secondary data, grid lines, connections. |
| Tertiary | Dusty Rose | `#C4767A` | Tertiary data series, accents. |
| Data Point | Pure White | `#FFFFFF` | Individual data points, stars, markers. |
| Grid | Navy Light | `#1E2D4A` | Background grid, coordinate lines. |
| Text | Silver | `#B8C4D0` | Body text, labels. Readable on dark. |

### Typography
- **Display:** Instrument Sans (600) — modern, condensed energy, dashboard precision
- **Body:** Albert Sans — Scandinavian minimalism, clean on dark backgrounds
- **Mono:** JetBrains Mono — data values, coordinates, timestamps

### Visual Style
- **Star Field:** Background has sparse, tiny white dots (1-2px) at random positions with varying opacity (0.2-0.8). Subtle but essential for depth.
- **Golden Ratio:** Layout proportions use φ (1.618) for panel sizing, chart aspect ratios, and spacing. Celestial precision.
- **Constellation Lines:** Data connections are thin (1px) teal lines with slight opacity (0.4), like star-chart constellation guides.
- **Glow on Dark:** Data points use `box-shadow: 0 0 8px rgba(255,215,0,0.3)` for gold glow. No CSS glow filter (too expensive at scale).

### Animation Philosophy
- **Easing:** Slow ease-out — `cubic-bezier(0, 0, 0.2, 1)`. Elements drift in like celestial bodies.
- **Timing:** Medium-slow. Data reveals 400-600ms. Orbital animations 3-8s cycles.
- **Motion Character:** Gravitational, orbital. Elements arc into position rather than sliding linearly.
- **Physics:** Orbital mechanics. Ease-out with slight curve to trajectory.

### Signature Animations
1. **Star Appear** — Data points fade in from 0% opacity with a simultaneous gold glow bloom (box-shadow expanding from 0 to 8px).
2. **Constellation Draw** — Connection lines animate via `stroke-dashoffset`, tracing the path between data points like mapping constellations.
3. **Orbital Entry** — Charts and panels enter along a slight arc (bezier curve path) rather than straight slide, as if in orbit.
4. **Twinkle** — Idle data points have a very subtle opacity oscillation (0.7→1.0→0.7) at random, different frequencies per point (4-8s cycle). Like stars twinkling.
5. **Telescope Zoom** — Drill-down interactions zoom the canvas smoothly, with surrounding elements scaling away. Like looking through a telescope.

### UI Components
- **Buttons:** Dark indigo fill, gold border (1px). Text in Albert Sans, silver. Hover: gold fill at 10% opacity. Active: gold border brightens.
- **Sliders:** Track is teal line (2px) on dark. Thumb is gold circle (12px) with soft glow.
- **Cards:** Dark indigo surface. 1px border in navy-light. `border-radius: 8px`. Subtle inner glow on hover.
- **Tooltips:** Dark indigo bg, gold title text, silver body text. Precise, compact. JetBrains Mono for values.
- **Dividers:** 1px navy-light. Or constellation-style dotted line (2px dots, 8px gaps).

### Light Mode Variant

Midnight Observatory has a full light mode — not an afterthought, a first-class variant. The dark theme is the night sky; the light theme is the daytime observatory — brass instruments, paper star charts, sunlight through the dome.

#### Structural Color Map

| Role | Dark (native) | Light (variant) | Notes |
|---|---|---|---|
| Page background | `#0B1426` deep navy | `#F5F0E8` warm cream | Observatory warmth — aged plaster walls in sunlight |
| Card / surface | `#141E33` dark indigo | `#FFFFFF` white | Clean instrument panels, chart paper |
| Border | `#1E2D4A` navy light | `#DDD5C8` brass edge | Warm border matching the cream page tone |
| Border heavy | — | `#C8BEB0` dark brass | Heavier dividers, section separators |
| Primary text | `#B8C4D0` silver | `#1A2030` deep navy ink | Preserves the observatory's blue identity in text |
| Secondary text | — | `#5A6478` slate blue | Muted but still navy-family, legible |
| Dim text | — | `#8A8478` warm stone | Labels, timestamps, coordinate metadata |
| Star field dots | `#FFFFFF` at 20-80% opacity | N/A — removed | Stars cannot show on light; replaced by dot-grid |
| Grid lines | `#1E2D4A` navy light | `#DDD5C8` at 40% | Coordinate grid faintly visible on cream |

#### Accent Shifts

| Element | Dark (native) | Light (variant) | Reason |
|---|---|---|---|
| Warm Gold | `#FFD700` | `#B89830` | Brass instruments in daylight — muted, not gleaming. APCA Lc ~60 on white |
| Muted Teal | `#4A9B9B` | `#2E7A7A` | Darkened for contrast on cream. APCA Lc ~55 on white |
| Dusty Rose | `#C4767A` | `#A05A60` | Deeper rose for readability. APCA Lc ~50 on white |
| Data Points | `#FFFFFF` pure white | `#1A2030` deep navy | Inverted — markers are now dark on light |

#### Shadow & Depth Adaptation

- **Dark:** No explicit shadows. Depth via luminance stepping (navy layers). Glow on gold data points (`box-shadow: 0 0 8px rgba(255,215,0,0.3)`).
- **Light:** Subtle warm shadows replace glow. Cards: `box-shadow: 0 1px 4px rgba(26,32,48,0.06)`. Gold data points get no glow — instead a `1px solid #B89830` ring. Depth reads through shadow, not luminance.

#### Texture & Grain Adaptation

- **Dark:** Sparse star field (tiny white dots at random positions, varying opacity). Constellation lines at 40% opacity teal.
- **Light:** Star field replaced by a subtle celestial dot-grid pattern — evenly spaced small dots (`#DDD5C8` at 30% opacity, 24px grid) evoking graph paper or an astronomical chart. Constellation lines become thin ink lines (`#1A2030` at 25% opacity) — dark on light instead of glow on dark.

#### Light Mode Rules

1. **No stars on light.** The star field background is removed entirely. The dot-grid or compass-line pattern preserves the celestial-chart feel without absurd bright-sky stars.
2. **Gold becomes brass.** `#FFD700` is replaced by `#B89830` everywhere — buttons, data points, borders. Brass reads as gold's daytime cousin.
3. **Navy ink preserves identity.** Primary text uses `#1A2030` (deep navy), not pure black. This keeps the observatory's blue character in every line of text.
4. **Constellation lines invert.** Teal glow lines become thin dark ink lines. The connection pattern is identical; only the rendering changes.
5. "Daytime observatory — brass instruments, paper star charts, sunlight through the dome."

### Mobile Notes
- Star field: reduce to 50 points max (DOM nodes or canvas dots).
- Disable twinkle animation (saves per-frame calculations).
- Constellation line drawing can be pre-computed (static SVG).
- Gold glow shadows are cheap — this theme performs well on mobile.
