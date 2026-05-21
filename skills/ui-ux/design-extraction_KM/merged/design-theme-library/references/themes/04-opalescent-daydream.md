## 4. Opalescent Daydream

> Light through glass, soap bubbles, holographic foil — clean, airy, explosively colorful.

**Best for:** N-body gravity simulations, orbital mechanics, wave interference, electromagnetic field visualizations.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Ghost White | `#F8F9FA` | Clean, bright canvas. Lets color pop. |
| Alt Background | Lavender Mist | `#E6E6FA` | Variant for softer, dreamier areas. |
| Holo Cyan | Electric Cyan | `#00FFFF` | Particles at low velocity. |
| Holo Magenta | Soft Magenta | `#FF77FF` | Particles at medium velocity. |
| Holo Yellow | Pale Yellow | `#FFFFE0` | Particles at high velocity. |
| Convergence | Pure White | `#FFFFFF` | Where particles overlap (additive blending). |
| UI Chrome | Silver | `#C0C0C0` | Controls, borders — nearly invisible. |
| Text | Soft Grey | `#6B7280` | Labels. Low-key, doesn't compete with color. |

### Typography
- **Display:** Sora — contemporary, futuristic, holographic energy
- **Body:** Manrope — geometric, distinctive, clean
- **Mono:** Space Mono — quirky, prismatic character

### Visual Style
- **Holographic Gradient:** Particles don't have single colors. Each shifts between cyan→magenta→yellow based on velocity, position, or phase. Use `hsl()` interpolation for smooth shifts.
- **Chromatic Aberration:** Slight RGB channel offset (2-3px) at canvas edges. Simulate by rendering the scene three times with slight offsets in R, G, B channels, or use a CSS filter hack.
- **Soft Bokeh:** Particles are not hard dots. Radial gradient circles — bright center fading to transparent edge. Like out-of-focus photography lights.
- **Additive Blending:** `globalCompositeOperation = 'screen'` or `'lighter'`. Overlapping particles blend to white, mimicking overexposed photography.

### Animation Philosophy
- **Easing:** Elastic springs — `stiffness: 200, damping: 15, mass: 0.8`. Overshoot and settle, like bubbles.
- **Timing:** Medium-fast for particles (continuous physics), slow for UI (400-600ms).
- **Motion Character:** Weightless, dreamy, iridescent. Elements float and drift.
- **Physics:** Low gravity, elastic collisions, orbital paths.

### Signature Animations
1. **Prismatic Scatter** — On interaction (click/tap), particles burst outward with chromatic separation — R, G, B channels scatter in slightly different directions before reconverging.
2. **Orbital Wobble** — Particles in orbit have a subtle perpendicular oscillation (±2px), like light refracting through glass.
3. **Bokeh Pulse** — Particle size gently oscillates (±10% radius) at different frequencies per particle, creating a "breathing sparkle" field.
4. **Rainbow Sweep** — On load or reset, a rainbow gradient sweeps across the canvas left-to-right in 1.5s, coloring particles as it passes.
5. **Convergence Flash** — When particles cluster, the overlap zone flashes to white with a soft 200ms bloom, then settles.

### UI Components
- **Buttons:** Silver border (1px), transparent fill. Text in Manrope 400, soft grey. Hover: fill fades to 3% lavender. Active: border becomes holographic gradient (animated via `@property`).
- **Sliders:** Track is silver 1px. Thumb is a small prismatic circle — CSS conic-gradient in cyan/magenta/yellow. 10px diameter.
- **Cards:** Barely-there. 1px silver border at 30% opacity. Ghost white fill. `border-radius: 12px`. Maximum transparency.
- **Tooltips:** Lavender mist background, soft grey text. Nearly invisible until needed.
- **Dividers:** 1px silver at 15% opacity. Or no dividers — just whitespace.

### Dark Mode Variant

Opalescent Daydream has a full dark mode — not an afterthought, a first-class variant. Dark IS the natural medium for holographic effects. Prisms splitting light in deep space.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F8F9FA` Ghost White | `#06060E` Void Violet | oklch(0.05 0.01 280) — near-black with faint violet cast |
| Card / surface | `#FFFFFF` / `#E6E6FA` | `#0A0A14` Deep Space | oklch(0.08 0.01 280) — elevated surfaces barely lift |
| Alt surface | `#E6E6FA` Lavender Mist | `#10101C` Space Mist | oklch(0.10 0.01 280) — secondary panels |
| Border | `#C0C0C0` Silver at 30% | `#1E1E2A` Dark Edge | oklch(0.15 0.01 280) — holographic frame edge |
| Border heavy | — | `#2A2A3A` Bright Edge | oklch(0.20 0.01 280) — hover/emphasis |
| Primary text | `#6B7280` Soft Grey | `#A0A4B0` Muted Silver | oklch(0.70 0.005 260) at 87% opacity |
| Secondary text | — | `#707480` Space Grey | oklch(0.52 0.01 270) — metadata, labels |
| Dim text | — | `#4A4E5A` Deep Mist | oklch(0.37 0.01 270) — timestamps |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Holo Cyan | `#00FFFF` | `#00FFFF` (unchanged) | Additive blending is MORE dramatic on dark backgrounds |
| Holo Magenta | `#FF77FF` | `#FF77FF` (unchanged) | Full saturation — holographic effects intensify on dark |
| Holo Yellow | `#FFFFE0` | `#FFFFE0` (unchanged) | Maintains the full prismatic spectrum |
| UI Chrome | `#C0C0C0` Silver | `#4A4A5A` Dark Chrome | Chrome becomes structural — no longer competes with holo |
| Convergence | `#FFFFFF` | `#FFFFFF` (unchanged) | White convergence point is even more stunning on black |

#### Shadow & Depth Adaptation
- Light: Barely-there shadows — the theme is about weightlessness and transparency
- Dark: Shadows disappear entirely. Replace with faint holographic glow rings — `0 0 20px rgba(0,255,255,0.06)` on cards. Surface depth from border luminance only. Holographic elements emit their own light

#### Texture & Grain Adaptation
- Light: No grain — clean, airy, bright
- Dark: No grain. Dark mode is cleaner still — a void for holographic light to play in. `globalCompositeOperation = 'screen'` and `'lighter'` produce their most dramatic results against pure dark. This is the additive blending sweet spot

#### Dark Mode Rules
- ALL holographic colors remain at full saturation — dark backgrounds are where additive blending truly shines
- Chromatic aberration effect intensifies — increase RGB channel offset from 2-3px to 3-5px for maximum prismatic drama
- Bokeh particles appear to self-illuminate against the void. Increase bokeh brightness by 20%
- Silver chrome (`#C0C0C0`) darkens to structural `#4A4A5A` — UI recedes so holo effects dominate
- "The natural home for holographic effects — prisms in deep space"

### Mobile Notes
- Cap bokeh particle count at 200 (radial gradients are expensive).
- Disable chromatic aberration (requires triple rendering).
- Reduce bokeh radius by 40% for performance.
- Additive blending still works on mobile Canvas2D.
