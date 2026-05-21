## 11. Solarpunk Brass

> Organic technology — botanical circuits, living architecture, warm utopian craft.

**Best for:** Sustainability dashboards, growth simulations, ecosystem models, botanical art, environmental data, garden planners.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Warm Linen | `#FDF6E3` | Same base as Alchemist, but cleaner. Sunlit. |
| Surface | Pale Sage | `#E8F0E4` | Cards, panels. Faint botanical tint. |
| Primary | Forest Green | `#2D5016` | Growth data, healthy states, primary elements. |
| Secondary | Polished Brass | `#C9A84C` | Interactive elements, mechanical parts, accents. |
| Tertiary | Warm Wood | `#8B6914` | Structural elements, borders, frameworks. |
| Growth | Spring Green | `#4A7C59` | New growth, positive trends, patina. |
| Alert | Amber | `#D4940A` | Warnings, thresholds. Warm, not aggressive. |
| Text | Dark Bark | `#2C1810` | Deep warm brown. Earthy, readable. |

### Typography
- **Display:** Fraunces (600) — elegant, organic "wonky" variable axis = living, growing letterforms
- **Body:** DM Sans — clean, readable, doesn't compete with ornate display font
- **Mono:** IBM Plex Mono — industrial-organic crossover

### Visual Style
- **Organic + Geometric Hybrid:** Mix organic shapes (curved paths, leaf-like forms) with precise geometric structures (gear teeth, circuit traces). The fusion of nature and engineering.
- **Brass UI Elements:** All interactive controls use the brass/gold metallic color. Borders, slider thumbs, button outlines. Suggests precision instruments.
- **Botanical Texture:** Subtle leaf-vein patterns or circuit-trace patterns as background texture (SVG at 3-5% opacity). Organic wiring.
- **Warm Lighting:** Everything feels sunlit. Slightly warm color temperature. Shadows are warm brown, never cool grey.

### Animation Philosophy
- **Easing:** Growth curves — `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out-expo). Fast start, long settle. Like a plant unfurling.
- **Timing:** Moderate. Growth animations 600ms-1.2s. Mechanical movements 200-400ms. Nature is patient; machines are precise.
- **Motion Character:** Dual — organic elements grow/unfurl, mechanical elements rotate/click. Two motion languages coexisting.
- **Physics:** Organic physics for natural elements (spring + damping). Linear precision for mechanical elements.

### Signature Animations
1. **Vine Growth** — Data connections or path traces grow like vines: animated SVG stroke from root to leaf with slight curve oscillation.
2. **Gear Click** — Mechanical interactions (toggles, step counters) rotate with a satisfying gear-click feel: 60° snap rotation with tiny bounce.
3. **Leaf Unfurl** — Cards and panels enter by "unfurling" — scale from 0 on one corner with rotation, like a fern frond opening.
4. **Brass Polish** — On hover, brass elements get a brief highlight sweep (linear gradient animation, like light catching polished metal).
5. **Photosynthesis Pulse** — Active/healthy elements have a subtle green glow pulse (3-5s cycle), like energy being absorbed from sunlight.

### UI Components
- **Buttons:** Forest green fill, warm linen text. 2px brass border. `border-radius: 6px`. Hover: brass highlight sweep. Active: darken green, `scale(0.97)`.
- **Sliders:** Track is warm wood color (3px). Thumb is a polished brass circle (14px) with 1px dark border. Gear-tooth texture optional.
- **Cards:** Pale sage surface. 1px brass border. `border-radius: 8px`. Subtle warm shadow. Top border can be forest green (4px) for accent.
- **Tooltips:** Forest green bg, warm linen text. Brass left-border accent (3px). Leaf-corner detail optional.
- **Dividers:** Brass line (1px, 40% opacity). Or vine-pattern SVG divider for decorative sections.

### Dark Mode Variant

Solarpunk Brass has a full dark mode — not an afterthought, a first-class variant. Bioluminescent solarpunk: a greenhouse at twilight where technology grows and brass gleams.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#FDF6E3` Warm Linen | `#080E06` deep forest floor | Near-black with green undertone — canopy at night |
| Card / surface | `#E8F0E4` Pale Sage | `#0A1A08` dark canopy | Botanical tint survives as deep green-black |
| Border | via brass/wood | `#1E3018` dark leaf | Organic boundary, not mechanical |
| Border heavy | brass at full | `#2A4020` mossy edge | Heavier structure for section dividers |
| Primary text | `#2C1810` Dark Bark | `#E8E0D0` at 87% warm paper | APCA Lc ~83 on `#0A1A08` — warm linen glow |
| Secondary text | `#2C1810` at lighter weight | `#B8B0A0` at 68% parchment | Quiet secondary, still warm |
| Dim text | n/a | `#6A7A58` muted sage | Labels and metadata — botanical green-grey |
| Growth data | `#2D5016` Forest Green | `#3ECF8E` vivid green | Green pops dramatically on dark — bioluminescent |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Forest Green | `#2D5016` | `#3ECF8E` vivid green | Dark-on-light green → light-on-dark. Vivid green pops like bioluminescence |
| Polished Brass | `#C9A84C` | `#D4B860` brightened brass | Polished brass catches more light in darkness |
| Warm Wood | `#8B6914` | `#A08030` bark in lamplight | Lightened for visibility, warmth preserved |
| Spring Green | `#4A7C59` | `#68B880` luminous patina | Growth indicator brightens to glow on dark |
| Amber alert | `#D4940A` | `#E0A820` warm amber | Warning still warm, more visible on dark |

#### Shadow & Depth Adaptation
- Light: Subtle warm shadow (`rgba(44,24,16,0.06)`) — sunlit, directional
- Dark: Shadows replaced by green glow — `box-shadow: 0 0 12px rgba(62,207,142,0.06)`. Cards lift off dark canopy with bioluminescent edge-light. Brass borders get `0 0 6px rgba(212,184,96,0.08)` warm glow

#### Texture & Grain Adaptation
- Light: Botanical texture — leaf-vein / circuit-trace SVG patterns at 3–5% opacity as background
- Dark: Botanical texture drops to 2% opacity, blend mode shifts to `soft-light`. Vine growth SVGs: invert glow direction — green glow `box-shadow` replaces solid fill. Circuit-trace patterns render as luminous lines on dark, not etched lines on light

#### Dark Mode Rules
- Green is the primary light source — bioluminescent, not decorative. `#3ECF8E` is the hero accent
- Brass elements glow warm against the dark canopy — increase brightness, keep saturation
- Photosynthesis pulse animation intensifies: glow radius increases from 4px → 8px on dark backgrounds
- Vine growth SVGs shift from filled paths to glowing strokes — `stroke` replaces `fill`, add `filter: drop-shadow` in green
- "Bioluminescent solarpunk — technology grows, brass gleams"

### Mobile Notes
- Vine growth animations: pre-compute SVG paths, animate only `stroke-dashoffset`.
- Brass polish highlight: reduce to simple opacity change on mobile (gradient animation is fine but optional).
- Botanical texture overlay: remove on mobile for performance.
- Moderate complexity — performs well with above optimizations.
