## 2. Ethereal Porcelain

> Fine ceramic art in a museum gallery — chaotic forces rendered as slow-moving sculpture.

**Best for:** Fluid dynamics (smoke/fire), Mandelbulb fractals, ray marching, volumetric rendering, marble simulations.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Soft Slate | `#E6E8EA` | Gallery wall. Neutral, lets the sculpture speak. |
| Alt Background | Warm Stone | `#D0D2D4` | Recessed areas, secondary panels. |
| Primary | Porcelain White | `#FFFFFF` | The fluid/fractal itself — the sculpture. |
| Highlight | Kintsugi Gold | `#C5A059` | High-vorticity, crack lines, chaos regions. |
| Shadow | Cool Grey | `#8A9597` | Ambient occlusion, depth shadows. |
| Warm Light | Candlelight | `#FFF4E0` | Simulated key light tint on facing surfaces. |
| Cool Fill | Twilight Blue | `#B8C4D0` | Simulated fill light tint on shadow side. |
| Text | Charcoal | `#3A3D40` | Gallery-label style text. |

### Typography
- **Display:** DM Serif Display — dramatic, high-contrast, museum-placard feel
- **Body:** Work Sans (light weight 300) — clean, minimal, gallery-label readability
- **Mono:** IBM Plex Mono (light) — technical data, coordinates

### Visual Style
- **Subsurface Scattering (SSS):** Render fluid/fractals as translucent heavy material — not glowing neon. Think milk in water, marble, moving porcelain. Use low-opacity white layers with slight color bleed at edges.
- **Kintsugi Effect:** Map gold to high-energy/chaotic regions. In fluid sims, gold appears at vorticity peaks. In fractals, gold fills cracks and detail bands. Use `screen` blend mode for gold on white.
- **Lighting:** Simulate studio softbox: warm key light from upper-left, cool fill from lower-right. Achieve via directional gradients on the canvas or per-particle color biasing.
- **Depth:** Subtle depth-of-field effect — elements closer to camera/center are sharp, edges have 1-2px blur.

### Animation Philosophy
- **Easing:** Smooth `cubic-bezier(0.25, 0.1, 0.25, 1.0)` — museum-slow, majestic.
- **Timing:** Slow. 0.5x physics speed for simulations. UI transitions 500-800ms. Nothing fast.
- **Motion Character:** Heavy, viscous, sculpted. Elements move like they have mass and inertia. Smoke looks like marble flowing.
- **Physics:** High viscosity, heavy damping. Objects drift rather than snap.

### Signature Animations
1. **Marble Pour** — Fluid enters the canvas as if being poured from above: downward gravity + lateral spread with SSS rendering.
2. **Kintsugi Crack** — When fractal detail increases or vorticity spikes, gold lines trace through like repairing cracks — animated `stroke-dashoffset` on SVG paths.
3. **Gallery Fade** — Sections/panels fade in from 0% opacity with a 1s ease, like gallery lights slowly illuminating a piece.
4. **Pedestal Rise** — Cards/panels enter with a subtle upward float (8px) + fade, as if rising onto a display pedestal.
5. **Breathing Glow** — Gold regions pulse subtly in opacity (0.7→1.0→0.7) over 4-6s, like living gold catching shifting light.

### UI Components
- **Buttons:** No border. Porcelain white fill with subtle shadow (`0 1px 4px rgba(0,0,0,0.08)`). Text in Work Sans 400. Hover: shadow deepens. Active: slight inset shadow.
- **Sliders:** Track is a 2px cool grey line. Thumb is a white circle with gold ring (2px border). Clean, minimal.
- **Cards:** White background, rounded corners (8px). Light box shadow (gallery-frame feel). Generous padding (24px).
- **Tooltips:** White with cool grey border. Small body text. Arrow points precisely.
- **Dividers:** 1px cool grey at 20% opacity. Generous spacing around them.

### Dark Mode Variant

Ethereal Porcelain has a full dark mode — not an afterthought, a first-class variant. The gallery closes, the spotlights come on, and porcelain glows from within.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#E6E8EA` Soft Slate | `#0A0C0E` Gallery Darkness | oklch(0.07 0.005 240) — near-black with cool undertone |
| Card / surface | `#FFFFFF` Porcelain White | `#1A1D20` Exhibition Plinth | oklch(0.14 0.005 240) — elevated surfaces lighter |
| Alt surface | `#D0D2D4` Warm Stone | `#252830` Deep Plinth | oklch(0.19 0.005 240) — recessed panels |
| Border | `#D0D2D4` at 20% | `#2E3234` Steel Frame | oklch(0.24 0.005 220) — structural display frame |
| Border heavy | implied by shadow | `#3A3E42` Bright Frame | oklch(0.29 0.005 220) — hover/emphasis borders |
| Primary text | `#3A3D40` Charcoal | `#D8DDE0` Cool Silver | oklch(0.89 0.005 240) at 87% opacity |
| Secondary text | `#8A9597` Cool Grey | `#A0A8AC` Lifted Grey | oklch(0.71 0.005 220) — lightened for dark bg |
| Dim text | — | `#6A7074` Museum Dim | oklch(0.49 0.005 220) — timestamps, metadata |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Kintsugi Gold | `#C5A059` | `#C5A059` (unchanged) | Gold reads beautifully on dark — warm metal catches spotlights |
| Candlelight tint | `#FFF4E0` | `#FFF4E0` at 8% | Key light becomes a subtle warm glow source, not surface fill |
| Twilight Blue fill | `#B8C4D0` | `#4A5868` | Cool fill darkens — shadow side is truly shadowed |
| Porcelain White (sculpture) | `#FFFFFF` | `#FFFFFF` at glow source | Objects glow against darkness — porcelain becomes the light |

#### Shadow & Depth Adaptation
- Light: Subtle box-shadows (`0 1px 4px rgba(0,0,0,0.08)`) — gallery frames lift off the wall
- Dark: Shadows invert to warm glows — `0 0 16px rgba(197,160,89,0.08)` for gold-adjacent elements, `0 0 12px rgba(255,255,255,0.04)` for porcelain elements. Surface hierarchy inverts: lighter surfaces = elevated

#### Texture & Grain Adaptation
- Light: No explicit grain — the SSS rendering provides visual texture
- Dark: SSS (subsurface scattering) becomes MORE dramatic. Increase glow radius by 1.5x. Porcelain objects emit light against darkness rather than absorbing it. Translucency is more visible when the environment is dark — think backlit alabaster

#### Dark Mode Rules
- Gold kintsugi lines need NO adjustment — warm metallic on dark is the natural museum lighting condition
- Subsurface scattering glow radius increases from light values — translucency reads stronger against dark backgrounds
- Cool grey structural elements (`#2E3234` borders) do more work — without shadows, borders define card edges
- Candlelight warm tint becomes a point light source (radial gradient at 5-8% opacity) rather than a surface wash
- "Night exhibition — porcelain glows from within, gold seams catch spotlights"

### Mobile Notes
- Disable depth-of-field blur effect (GPU-heavy filter).
- Reduce gold glow to static opacity (remove breathing animation).
- Simplify SSS to flat white with opacity layers instead of blur blending.
