## 9. Bioluminescent Deep

> Abyssal ocean — pure darkness punctuated by living, breathing light.

**Best for:** Particle systems, network visualizations, flow simulations, audio visualizers, neural network models, signal processing.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Abyss | `#050510` | Near-black with faint blue undertone. The void. |
| Surface | Deep Water | `#0A1628` | Elevated panels. Only slightly lighter than abyss. |
| Primary Glow | Electric Cyan | `#00F5FF` | Primary particles, key data, active connections. |
| Secondary Glow | Magenta Pulse | `#FF006E` | Secondary particles, alerts, energy bursts. |
| Tertiary | Deep Violet | `#7B2FBE` | Tertiary data, ambient glow, deep network nodes. |
| Bio Green | Plankton Green | `#00FF88` | Organic growth, positive signals, health indicators. |
| Ambient | Dark Blue | `#0D1B2A` | Subtle ambient light in the water column. |
| Text | Pale Cyan | `#B0E0E6` | Body text. Soft enough to not overpower glow. |

### Typography
- **Display:** Sora (600) — futuristic, contemporary, deep-tech
- **Body:** Manrope (400) — geometric, clean, readable on dark backgrounds
- **Mono:** Fira Code — ligatures for data streams, technical values

### Visual Style
- **Glow Rendering:** Every luminous element uses layered glow: inner color at full opacity + `box-shadow: 0 0 Npx color` for bloom. For particles on canvas: draw the particle, then draw a larger, transparent version behind it.
- **Additive Blending:** `globalCompositeOperation = 'lighter'` (Canvas) or `mix-blend-mode: screen` (CSS). Overlapping glows intensify to white. Essential.
- **Dark Canvas:** The abyss background is NEVER lighter than `#0A1628`. Glow only works against true darkness.
- **Fog/Scatter:** Simulate deep-water light scattering with a subtle radial gradient from center (slightly lighter) to edges (darker). Vignette effect.
- **Filament Connections:** Network lines are thin (0.5-1px) with glow matching their endpoint colors. Animated dash patterns suggest signal flow.

### Animation Philosophy
- **Easing:** Organic springs — `stiffness: 80, damping: 12`. Slow, drifting, deep-water feel.
- **Timing:** Slow. Glow pulses 2-4s. Drift animations 5-10s cycles. Fast things die fast in the deep ocean.
- **Motion Character:** Organic, pulsing, alive. Everything breathes, drifts, pulses. Nothing is static.
- **Physics:** Fluid dynamics with drag. Low-velocity drift with current influence.

### Signature Animations
1. **Bioluminescent Pulse** — Particles breathe: glow radius oscillates (80%→120%→80%) with a sine-wave rhythm at slightly different frequencies per particle (2-4s).
2. **Signal Trace** — Network connections animate a bright dot traveling along the path (like a neural signal). `stroke-dasharray: 4, 200` with animated `stroke-dashoffset`.
3. **Depth Emerge** — New elements start with zero glow and slowly increase glow intensity over 1.5s, like a creature emerging from the deep.
4. **Scatter Burst** — Interactions produce a radial burst of tiny particles (20-30) that drift outward and fade, like disturbing bioluminescent plankton.
5. **Current Drift** — Idle particles drift slowly in a consistent direction (subtle vector field), like deep-ocean currents. Perlin noise for variation.

### UI Components
- **Buttons:** Transparent fill, 1px cyan border with glow (`0 0 8px rgba(0,245,255,0.3)`). Text in pale cyan. Hover: fill with 10% cyan, glow intensifies. Active: flash to full cyan for 100ms.
- **Sliders:** Track is dark blue 2px line. Thumb is a glowing cyan dot (10px) with bloom shadow. Active portion of track glows.
- **Cards:** Deep water surface. 1px border in `rgba(0,245,255,0.15)`. Subtle inner glow on hover. `border-radius: 8px`.
- **Tooltips:** Deep water bg, pale cyan text. Faint cyan border glow. Compact.
- **Dividers:** Glowing line — 1px cyan at 15% opacity with 4px glow.

### Light Mode Variant

Bioluminescent Deep has a full light mode — not an afterthought, a first-class variant. The dark theme is the midnight abyss; the light theme is the shallow reef at noon — same creatures, sunlit water. The magic is different but present.

#### Structural Color Map

| Role | Dark (native) | Light (variant) | Notes |
|---|---|---|---|
| Page background | `#050510` abyss | `#E8F4F8` pale aqua | oklch(0.96 0.02 210) — underwater with sunlight filtering through |
| Card / surface | `#0A1628` deep water | `#FFFFFF` light water column | Clean white — the bright zone where light penetrates |
| Border | `rgba(0,245,255,0.15)` cyan glow | `#C4D8D8` seafoam edge | oklch(0.87 0.02 195) — soft aquatic border |
| Border heavy | — | `#A8C4C8` deeper seafoam | Heavier dividers, section breaks |
| Primary text | `#B0E0E6` pale cyan | `#0A2028` deep water ink | oklch(0.18 0.03 210) — near-black with blue undertone |
| Secondary text | — | `#3A5A60` muted teal | Readable secondary, aquatic cast |
| Dim text | — | `#6A8A90` sea mist | Labels, timestamps, ambient metadata |
| Ambient bg | `#0D1B2A` dark blue | `#D8EEF4` light wash | Subtle depth variation on page |

#### Accent Shifts

| Element | Dark (native) | Light (variant) | Reason |
|---|---|---|---|
| Electric Cyan | `#00F5FF` | `#0098A8` | oklch(0.62 0.12 200) — teal in daylight. APCA Lc ~62 on white |
| Magenta Pulse | `#FF006E` | `#C4004A` | oklch(0.48 0.18 10) — coral, darkened for white-bg contrast |
| Deep Violet | `#7B2FBE` | `#5A1A8C` | oklch(0.35 0.18 305) — deeper violet for legibility |
| Plankton Green | `#00FF88` | `#1A8A50` | oklch(0.56 0.13 155) — kelp green, grounded |

#### Shadow & Depth Adaptation

- **Dark:** Layered glow — particles drawn twice (inner full opacity + larger transparent bloom). `globalCompositeOperation = 'lighter'` / `mix-blend-mode: screen`. Radial vignette (center lighter, edges darker).
- **Light:** Glow replaced by colored drop-shadows. Particles: single-pass with `box-shadow: 0 0 8px rgba(0,152,168,0.25)` for cyan elements, `0 0 8px rgba(196,0,74,0.20)` for magenta. Additive blending makes no sense on light — replaced by `multiply` or normal compositing. Cards: `box-shadow: 0 2px 6px rgba(10,32,40,0.06)`. Vignette inverted: edges fade to near-white.

#### Texture & Grain Adaptation

- **Dark:** Fog/scatter via radial gradient (center slightly lighter, edges darker). Filament connections glow with endpoint colors. Animated dash patterns.
- **Light:** Fog/scatter becomes a subtle aquatic wash — soft radial gradient from center (`#E8F4F8`) to edges (`#D0E8F0`), 5% opacity difference. Filament connections become thin solid lines (`1px`) in darkened accent colors, no glow. Dash animation preserved — signal flow still visible against light water.

#### Light Mode Rules

1. **Glow becomes shadow.** Every `box-shadow` glow (radiating light on dark) converts to a colored drop-shadow (colored shade on light). Same elements, inverted light model.
2. **No additive blending on light.** `mix-blend-mode: screen` and `globalCompositeOperation: 'lighter'` are removed. Overlapping elements use `multiply` or normal compositing with opacity.
3. **Layered glow becomes layered wash.** The multi-layer glow rendering converts to soft transparent color washes — concentric `rgba` fills at decreasing opacity, creating depth without luminance.
4. **Particle colors darken uniformly.** All four accent colors shift to darker, more saturated variants. No accent stays at its dark-mode brightness.
5. "Snorkeling in shallow reef — same creatures, sunlit water. The magic is different but present."

### Mobile Notes
- **Critical:** Layered glow (drawing particles twice for bloom) is expensive. On mobile: single-pass particles with `box-shadow` glow only on key elements (not all particles).
- Reduce additive blending calls — batch particles where possible.
- Disable vignette radial gradient (saves one fullscreen draw).
- Cap particle count aggressively: 500 max mobile vs 5000 desktop.
