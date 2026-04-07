## 19. Sunlit Concrete

> Industrial daylight: concrete, steel, safety labels. A physical control room that's readable and modern.

**Best for:** Industrial dashboards, IoT monitoring, logistics tracking, manufacturing UIs, warehouse management, fleet ops.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Daylight Concrete | `#EDEBE8` | Primary canvas. Slightly warm grey, like sunlit concrete. |
| Alt Background | Poured Slab | `#E0DDDA` | Cards, panels, secondary surfaces. |
| Primary Text | Asphalt | `#1F2124` | Body text, headings. Dark but not black. |
| Secondary Text | Rebar Grey | `#6B6E73` | Labels, metadata, inactive text. |
| Safety Orange | OSHA Orange | `#E67E22` | Warnings, alerts, high-priority metrics. |
| Safety Yellow | Caution | `#F5C842` | Secondary warnings, highlight zones. |
| Link Blue | Steel Blue | `#3578A0` | Links, informational actions. |
| Border | Expansion Joint | `#C8C4BF` | Dividers, gridlines, input borders. |

### Typography
- **Display:** Barlow Condensed (700 weight) — industrial condensed sans, bold presence in small spaces
- **Body:** Barlow (400–500 weight) — same family, clean at body sizes
- **Mono:** IBM Plex Mono — industrial heritage, excellent tabular numerals

### Visual Style
- **Concrete Texture:** Static noise overlay (`feTurbulence`, `baseFrequency="0.9"`, 1 octave) at 3% opacity. Gives surfaces concrete grit.
- **Hard Shadows:** Elements use `box-shadow: 4px 4px 0 rgba(0,0,0,0.08)` — directional, no blur, like sunlight casting sharp edges.
- **Safety Color System:** Orange and yellow are NEVER decorative. They mean "attention required." Blue is for navigation/info. Green (`#2D9D5C`) for success/normal. This is a safety-critical color language.
- **Large Metrics:** Key numbers rendered at 32–48px in Barlow Condensed 700. Dashboard KPIs should feel like industrial readouts.

### Animation Philosophy
- **Easing:** `linear` or `cubic-bezier(0.4, 0, 0.2, 1)` — mechanical, utilitarian.
- **Timing:** Fast. Micro: 100ms. Transitions: 200ms. Nothing slow. Operators need speed.
- **Motion Character:** Mechanical. Sharp starts, clean stops. No organic feel. Like pneumatic actuators.
- **Physics:** None. Deterministic, time-based transitions only.

### Signature Animations
1. **Alert Pulse** — Safety orange elements pulse opacity (100% → 60% → 100%) at 1.5s interval for active alerts. Stops when acknowledged.
2. **Gauge Fill** — Progress bars and gauges fill with a `scaleX` animation from left, 300ms, linear easing. Like a pressure gauge rising.
3. **Panel Drop** — Cards and panels enter from 10px above with ease-out at 200ms. Like a heavy panel being placed down.
4. **Status Flash** — When a metric changes state (normal → warning), the cell background flashes safety orange at 20% opacity for 800ms.
5. **Grid Scan** — On page load, table rows appear in a fast top-to-bottom stagger (30ms delay per row). Like a scanner reading inventory.

### UI Components
- **Buttons:** Primary: steel blue fill, white text, `border-radius: 2px` (nearly square). Secondary: 2px border in expansion joint color. Hover: darken 10%. Active: inset shadow. Large: 44px height minimum.
- **Sliders:** Track is 4px expansion-joint color. Thumb is 14px steel blue square (not circle — industrial). Value in IBM Plex Mono bold.
- **Cards:** Poured slab background, 1px expansion-joint border. `border-radius: 2px`. Hard shadow. Padding 16px. Compact.
- **Tooltips:** Asphalt background, white text. IBM Plex Mono small. `border-radius: 2px`. No arrow.
- **Dividers:** Expansion joint at 80% opacity. 2px for section breaks, 1px for within-section.

### Dark Mode Variant

Sunlit Concrete has a full dark mode — not an afterthought, a first-class variant. Night shift at the plant. Safety colors are MORE important in darkness — never mute them.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#EDEBE8` Daylight Concrete | `#0E0F10` Night Concrete | oklch(0.08 0.005 240) — slight cool cast, like concrete at night |
| Card / surface | `#E0DDDA` Poured Slab | `#1A1B1E` Dark Steel Panel | oklch(0.13 0.005 250) — industrial panel |
| Alt surface | — | `#232528` Deep Panel | oklch(0.17 0.005 250) — recessed areas |
| Border | `#C8C4BF` Expansion Joint | `#2E3034` Dark Joint | oklch(0.22 0.005 240) — panel seams |
| Border heavy | — | `#3E4044` Bright Joint | oklch(0.28 0.005 240) — section dividers |
| Primary text | `#1F2124` Asphalt | `#E0DDD8` Dusty Concrete | oklch(0.89 0.005 60) at 87% opacity |
| Secondary text | `#6B6E73` Rebar Grey | `#9A9DA2` Lifted Rebar | oklch(0.67 0.005 240) — labels, metadata |
| Dim text | — | `#6A6D72` Night Rebar | oklch(0.47 0.005 240) — timestamps |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| OSHA Orange | `#E67E22` | `#F09030` (brighter) | Safety colors MUST be vivid in dark — operator visibility is paramount |
| Caution Yellow | `#F5C842` | `#F5D060` (brighter) | Warning indicators brighten in dark to maintain urgency |
| Steel Blue | `#3578A0` | `#5A9BC8` (brighter) | Links and informational blue lifted for dark bg contrast |
| Success Green | `#2D9D5C` | `#40B870` (brighter) | Normal/success state slightly brighter for readability |

#### Shadow & Depth Adaptation
- Light: Hard directional shadows — `4px 4px 0 rgba(0,0,0,0.08)` — sunlight casting sharp edges
- Dark: Hard shadows become subtle directional highlights — `4px 4px 0 rgba(255,255,255,0.02)`. Maintain the directional character (upper-left light source implied) but inverted. Primary depth from border color: `#2E3034` expansion joints define panel edges against `#0E0F10` background

#### Texture & Grain Adaptation
- Light: `feTurbulence` at 3% opacity, `baseFrequency="0.9"`, 1 octave — concrete grit
- Dark: Same `feTurbulence` filter, reduced to 2% opacity, blend mode shift from overlay to `soft-light`. Same frequency and octaves. The concrete texture is essential to industrial identity — it persists in darkness but doesn't dominate. Surfaces should still feel like poured concrete, not smooth digital panels

#### Dark Mode Rules
- Safety colors BRIGHTEN in dark mode — `#F09030` orange, `#F5D060` yellow — never mute safety-critical indicators
- Concrete texture remains present — industrial identity depends on tactile surface feel even in night-shift darkness
- Large metric font sizes (32-48px Barlow Condensed 700) stay large — readability at distance is the point
- Hard directional shadow character preserved — just inverted from dark-on-light to light-on-dark
- "Night shift. Safety colors are MORE important in darkness — never mute them"

### Mobile Notes
- Remove concrete texture overlay (performance).
- Maintain large metric font sizes — they're the point of this theme.
- Touch targets: 48px minimum (operators may wear gloves — extra generous).
