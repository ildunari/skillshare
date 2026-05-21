## 1. Alchemist's Journal

> Living ink on ancient parchment — a Da Vinci notebook come to life.

**Best for:** Reaction-diffusion, Physarum (slime mold), organic growth simulations, L-systems, erosion models.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Cream / Vellum | `#FDF6E3` | Canvas base. Apply paper grain overlay. |
| Alt Background | Aged Parchment | `#FEFED0` | Variant for lighter areas or margins. |
| Primary Ink | Deep Charcoal | `#2F3337` | Living/active simulation elements. Never pure black. |
| Accent 1 | Antique Gold | `#D4AF37` | High-density areas, cores, energy peaks. |
| Accent 2 | Oxidized Copper | `#4B7F52` | Trails, fading paths, chemical residue. |
| Tertiary | Iron Gall Ink | `#3B2F2F` | Secondary structures, fine detail. |
| Border | Brass Wire | `#B8860B` | UI dividers, slider tracks, control outlines. |
| Text | Dark Umber | `#3E2723` | Labels, headings, values. |

### Typography
- **Display:** EB Garamond (Google Fonts) — elegant serif, alchemical manuscript feel
- **Body:** Libre Caslon Text — readable serif for labels and descriptions
- **Mono:** IM Fell English SC — for seed numbers and parameter values (or fallback to JetBrains Mono)

### Visual Style
- **Paper Texture:** SVG `feTurbulence` overlay (`baseFrequency="0.65"`, 2 octaves) at 3-5% opacity with `mix-blend-mode: overlay` on a `::after` pseudo-element. Creates watercolor paper grain.
- **Ink Bleeding:** Simulation elements should feel like they're bleeding into the paper. Use slight Gaussian blur (0.5-1px) on trail edges. Avoid hard pixel edges.
- **Compositing:** `multiply` blend mode for overlapping ink strokes. Trails darken where they cross.
- **Aging Effect:** Older/faded trails shift from charcoal toward copper-green, like oxidizing ink.

### Animation Philosophy
- **Easing:** `ease-in-out` with long tails. Nothing snaps. Ink flows, it doesn't teleport.
- **Timing:** Slow to medium. Growth animations 2-4s. UI transitions 400-600ms.
- **Motion Character:** Organic, ink-like. Think of a drop of ink spreading in water — outward expansion with irregular edges.
- **Physics:** Viscous fluid model. High damping, low bounce. Elements decelerate gracefully.

### Signature Animations
1. **Ink Bloom** — New elements appear as a spreading ink drop: radial scale from 0 with slight irregular edge distortion via noise displacement.
2. **Quill Stroke** — UI elements draw themselves on with `stroke-dashoffset` animation, like a quill writing them into existence.
3. **Oxidation Fade** — Completed/old elements slowly shift hue from charcoal → copper → faint green over 10-30s, mimicking chemical aging.
4. **Paper Fold Reveal** — Panels/sections unfold with a subtle 3D perspective rotation (5-10°) as if turning a page.
5. **Tremor Idle** — Subtle positional jitter (±0.5px) on organic elements, like living organisms breathing on the page.

### UI Components
- **Buttons:** Thin gold (#B8860B) border, 1px. No fill (transparent). On hover: fill fades to 5% gold. Active: border thickens to 2px. Text in EB Garamond. `border-radius: 2px` — nearly square, like brass instrument controls.
- **Sliders:** Track is a thin gold line (1px). Thumb is a small brass circle (12px) with 1px border. Value label in serif italic.
- **Cards/Panels:** No visible border. Subtle inner shadow (`inset 0 1px 3px rgba(59,47,47,0.08)`). Background is slightly lighter cream. Paper grain continues through.
- **Tooltips:** Parchment background with dark umber text. Thin gold top-border. Small serif text.
- **Dividers:** Thin horizontal rule in brass color at 30% opacity. Or a decorative flourish character (⁕ or ❧).

### Dark Mode Variant

Alchemist's Journal has a full dark mode — not an afterthought, a first-class variant. Think candlelit laboratory: warm sepia darkness, gold catching firelight, ink bleeding into shadow.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#FDF6E3` Cream / Vellum | `#0F0D08` near-black with warm sepia undertone | Candlelit laboratory floor — warmth survives |
| Card / surface | `#FEFED0` Aged Parchment | `#1A1510` aged wood | Surface hierarchy inverts: lighter = elevated |
| Border | `#B8860B` Brass Wire | `#332A1E` brass-wire darkened | Warm mid-tone, still reads as brass |
| Border heavy | `#B8860B` at full | `#4A3D2A` polished brass edge | Heavier separation on dark canvas |
| Primary text | `#2F3337` Deep Charcoal | `#E8DCC8` at 87% parchment glow | APCA Lc ~82 on `#1A1510` — warm, never cool white |
| Secondary text | `#3E2723` Dark Umber | `#C4B8A0` at 72% aged paper | Readable without competing with primary |
| Dim text | `#3B2F2F` Iron Gall Ink | `#8A7E68` warm umber mid-grey | Labels, metadata — present but quiet |
| Simulation ink | `#2F3337` Deep Charcoal | `#C5A059` aged gold on dark | Living elements glow instead of darken |
| Tertiary structures | `#3B2F2F` Iron Gall | `#6B5D4A` warm mid-brown | Fine detail, secondary paths |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Antique Gold | `#D4AF37` | `#E0C068` | Gold catches more light in darkness — brighter, warmer |
| Oxidized Copper | `#4B7F52` | `#5C9A68` | Oxidized copper luminescence — green brightens on dark |
| Brass Wire borders | `#B8860B` | `#997520` at 60% | Softer brass tone, border not accent |

#### Shadow & Depth Adaptation
- Light: `inset 0 1px 3px rgba(59,47,47,0.08)` — subtle inner shadow suggesting paper depth
- Dark: Replace directional shadows with warm gold glow — `0 0 8px rgba(212,175,55,0.05)`. Shadows are invisible on dark; glow replaces elevation

#### Texture & Grain Adaptation
- Light: SVG `feTurbulence` at 3–5% opacity, `mix-blend-mode: overlay` — watercolor paper grain
- Dark: Paper grain drops to 2% opacity, blend shifts to `soft-light`. Grain must remain visible — the manuscript is still parchment, just by candlelight. Ink-bleed effect intensifies: Gaussian blur radius increases 0.5px on trails, creating richer diffusion on dark ground

#### Dark Mode Rules
- Simulation elements shift from dark-ink-on-light to luminous-on-dark — they glow, they don't stain
- Oxidation aging cycle reverses direction: elements fade from bright gold → dim copper → faint warm grey
- Multiply compositing for overlapping trails switches to `screen` — ink strokes lighten where they cross on dark
- Gold and brass UI elements become the primary light source — increase brightness, not saturation
- "Think candlelit laboratory, not dark mode UI"

### Mobile Notes
- Reduce paper grain feTurbulence to 1 octave (performance).
- Simplify ink bleeding — remove Gaussian blur on trails, use opacity fade instead.
- Touch targets on brass controls: minimum 44px with 8px padding.
