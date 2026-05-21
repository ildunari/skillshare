## 28. Signal & Noise Lab

> Research lab aesthetic: clean surfaces with measured noise textures and instrument-like components. Built for simulations and analytics.

**Best for:** Lab dashboards, simulation UIs, analytics products, signal processing tools, research environments, ML experiment trackers.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Lab White | `#F4F4F0` | Primary canvas. Clinical white with warm undertone. |
| Alt Background | Bench Surface | `#ECECEA` | Cards, instrument panels, secondary surfaces. |
| Primary Text | Carbon | `#18181B` | Body text, headings. Dense, high contrast. |
| Secondary Text | Titanium | `#6B6B73` | Labels, units, secondary info. |
| Signal Blue | Oscilloscope Blue | `#2D78C8` | Primary data, active measurements, interactive elements. |
| Signal Warm | Spectrum Orange | `#D06830` | Secondary data series, warm channel. |
| Success | Calibrated Green | `#2D8C50` | In-range values, successful states. |
| Border | Instrument Grey | `#D0D0CC` | Panel borders, grid lines, axes. |

### Typography
- **Display:** Space Grotesk (600 weight) — technical, geometric, scientific precision
- **Body:** DM Sans (400 weight) — clean readability for dense instrument panels
- **Mono:** JetBrains Mono — readouts, values, units. The primary data font.

### Visual Style
- **Instrument Panels:** Cards styled as instrument readout panels — 1px border, `border-radius: 4px`, with a subtle top-bar (4px) in signal-blue for active panels. Clean, functional.
- **Anti-Banding Noise:** A very subtle noise texture (feTurbulence at 1.5% opacity) prevents banding in gradients and large flat areas. This is the "noise" in "signal & noise" — it's there for visual quality, not decoration.
- **Axis-Aligned Layout:** All content on strict 8px grid. Charts, readouts, and controls aligned to shared baselines. Misalignment is a bug.
- **Dual-Channel Color:** Signal blue (cool) and spectrum orange (warm) are the two primary data colors. They have equal perceptual weight in OKLCH. All other data colors derive from these two endpoints.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` — standard, functional, invisible.
- **Timing:** Fast. Readout updates: 100ms. Panel transitions: 200ms. Chart animations: 300ms.
- **Motion Character:** Instrumental. Transitions are functional — they show causality (this slider changed that value) not decoration.
- **Physics:** None. Instruments are precise, not playful.

### Signature Animations
1. **Readout Update** — Numeric values change with a brief blue flash (background `rgba(45,120,200,0.08)` for 300ms) and the number morphs via CSS `counter()` or JS interpolation. 200ms.
2. **Signal Trace** — Chart lines draw themselves left-to-right with `stroke-dashoffset`, like an oscilloscope signal being traced. 500ms.
3. **Panel Activate** — When a panel becomes active, its top-bar color fills from left-to-right (`scaleX(0→1)`) in signal blue. 200ms.
4. **Calibration Pulse** — On reset/recalculate, a brief horizontal scan line sweeps top-to-bottom across the panel (white at 5% opacity). 300ms. Like an instrument recalibrating.
5. **Data Cascade** — Chart points appear in a left-to-right stagger (20ms per point) following the x-axis temporal order. 300ms total.

### UI Components
- **Buttons:** Primary: signal blue fill, lab white text, `border-radius: 4px`. Secondary: 1px instrument-grey border, carbon text. Hover: darken 8%. Active: inset shadow. Compact: 32px height.
- **Sliders:** Track is 3px instrument grey. Thumb is 12px signal-blue circle. Value + unit label in JetBrains Mono right-aligned (e.g., "340 Hz").
- **Cards:** Bench surface background, 1px instrument border. `border-radius: 4px`. 4px top-bar in signal blue (active) or transparent (inactive). Padding 16px.
- **Tooltips:** Carbon background, lab white text. JetBrains Mono 11px. Shows value + unit + timestamp. `border-radius: 3px`.
- **Dividers:** Instrument grey at 60% opacity. 1px. Clean horizontal rules.

### Dark Mode Variant

Signal & Noise Lab has a full dark mode — not an afterthought, a first-class variant. Darkened lab — instruments emit light. The oscilloscope IS the light source.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F4F4F0` Lab White | `#0A0A0C` Dark Lab Bench | oklch(0.06 0.005 270) — neutral dark with faint cool cast |
| Card / surface | `#ECECEA` Bench Surface | `#111114` Instrument Panel | oklch(0.09 0.005 270) — dark instrument housing |
| Alt surface | — | `#18181C` Deep Panel | oklch(0.12 0.005 270) — recessed instrument areas |
| Border | `#D0D0CC` Instrument Grey | `#222228` Rack Mount | oklch(0.16 0.005 270) — panel borders, axes |
| Border heavy | — | `#303038` Bright Mount | oklch(0.22 0.005 270) — section dividers |
| Primary text | `#18181B` Carbon | `#E0E0E4` Readout Glow | oklch(0.90 0.005 270) at 87% opacity |
| Secondary text | `#6B6B73` Titanium | `#96969E` Lifted Titanium | oklch(0.65 0.005 270) — labels, units |
| Dim text | — | `#606068` Dark Titanium | oklch(0.42 0.005 270) — timestamps |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Oscilloscope Blue | `#2D78C8` | `#4A98E0` (brighter) | Phosphor glow — signal trace glows on dark oscilloscope screen |
| Spectrum Orange | `#D06830` | `#E08040` (brighter) | Warm channel brightens for visibility on dark panels |
| Calibrated Green | `#2D8C50` | `#40A860` (brighter) | In-range indicator lifts for dark background readability |
| Panel top-bar | 4px signal blue | 4px brighter blue `#4A98E0` | Active panels more prominent — instruments emit their own light |

#### Shadow & Depth Adaptation
- Light: Minimal — 1px borders and instrument-grey gridlines define structure
- Dark: Instrument panels gain subtle top-bar glow — active panels emit `0 -2px 8px rgba(74,152,224,0.1)` from their blue top-bar. This is the "instruments emit light" principle. Other depth from border color (`#222228`) against surface (`#111114`). No diffuse shadows

#### Texture & Grain Adaptation
- Light: Anti-banding noise via `feTurbulence` at 1.5% opacity — prevents gradient banding on large flat surfaces
- Dark: Anti-banding noise reduced to 1% opacity — less visible on dark surfaces, but still present to prevent banding in chart gradients. Blend mode unchanged. The noise is functional (anti-banding), not decorative — it's the "noise" in "signal & noise"

#### Dark Mode Rules
- Instrument panel cards with blue top-bar become the primary visual — the top-bar accent glows slightly, making active panels the light source in the dark lab
- Dual-channel color (blue/orange) both brighten proportionally — maintaining equal perceptual weight in OKLCH on dark backgrounds
- Anti-banding noise stays functional but reduces — dark surfaces band less, so less correction needed
- Axis-aligned layout and 8px grid preserved — instrument precision is mode-independent
- "Darkened lab — instruments emit light. The oscilloscope IS the light source"

### Mobile Notes
- Maintain compact spacing — data density is the identity.
- Disable signal trace animation (chart performance on mobile).
- Use shorter stagger delays (10ms per point).
- Touch targets: 44px minimum. Instrument controls can be slightly smaller than consumer UI.
