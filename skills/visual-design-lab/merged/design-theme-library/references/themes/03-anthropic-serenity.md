## 3. Anthropic Serenity

> Clean, intellectual warmth — high-end editorial design that thinks slowly and carefully.

**Best for:** Strange attractors, particle systems, flow fields, generative patterns, mathematical visualizations.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Warm Beige | `#F0EBE3` | Primary canvas. Warm, inviting. |
| Alt Background | Wheat | `#F5F2EB` | Lighter variant for cards/panels. |
| Primary Particle | Burnt Sienna | `#C15F3C` | High-energy particles, focal points. |
| Secondary Particle | Soft Coral | `#E8B49C` | Fading particles, low-energy states. |
| Deep Contrast | Muted Forest | `#3F4E4F` | Dense accumulation, text, high-contrast needs. |
| Accent | Warm Clay | `#A0522D` | Interactive elements, highlights. |
| Border | Sand | `#D6CFC4` | Subtle dividers, card borders. |
| Text | Near Black | `#1A1A1A` | Body text, labels. Dark grey, not pure black. |

### Typography
- **Display:** Plus Jakarta Sans (600 weight) — refined, professional, warm
- **Body:** DM Sans — clean, readable, #1 Typewolf 2026
- **Mono:** Geist Mono — modern, Vercel aesthetic, pairs beautifully

### Visual Style
- **Matte Finish:** No glitter, no glow, no bloom. Particles are soft matte circles with alpha blending. Where particles overlap, colors blend like watercolor wash — use `multiply` or reduced-opacity layering.
- **Slow Motion:** Force physics to 0.5x speed. Majestic, not twitchy. "Thoughtful" is the operative word.
- **Density Mapping:** Color shifts from coral (sparse) → sienna (medium) → forest (dense). This creates natural depth from particle accumulation.
- **Negative Space:** Let the beige canvas breathe. Not every pixel needs a particle. Empty space is a feature.

### Animation Philosophy
- **Easing:** Gentle springs — `stiffness: 120, damping: 20`. Or `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-quint).
- **Timing:** Slow, deliberate. Particle reveals stagger at 0.05s intervals. Section transitions 600-800ms.
- **Motion Character:** Thoughtful, editorial. Elements move like well-considered typographic decisions — placed, not thrown.
- **Physics:** Low gravity, high air resistance. Particles float and settle.

### Signature Animations
1. **Watercolor Bleed** — New particle groups spread outward with decreasing opacity, like watercolor on wet paper.
2. **Editorial Stagger** — UI elements and data points enter in a staggered cascade (top-left to bottom-right, 80ms delay each).
3. **Thermal Shift** — Particles slowly shift color based on velocity: fast=sienna, slow=coral, stationary=faint sand. Continuous, not stepped.
4. **Breath Cycle** — The entire particle field subtly expands and contracts (±2% scale) over 8s, like breathing.
5. **Settle Drift** — New particles overshoot their target position slightly, then drift back with spring physics. Undersells the landing.

### UI Components
- **Buttons:** Rounded (6px). Sienna fill for primary, sand border for secondary. Text in Plus Jakarta Sans 500. Hover: darken 10%. Active: `scale(0.97)`.
- **Sliders:** Track is sand-colored 3px line. Thumb is sienna circle (14px). Value text in Geist Mono, right-aligned.
- **Cards:** Wheat background, 1px sand border. `border-radius: 8px`. Padding 20px. No shadow — border does the elevation.
- **Tooltips:** Muted forest background, warm beige text. Tiny DM Sans. 4px radius.
- **Dividers:** Sand color at 40% opacity. Or simply generous whitespace (48-64px gap).

### Dark Mode Variant

Anthropic Serenity has a full dark mode — not an afterthought, a first-class variant. Warm intellectual intimacy, like reading a long essay by the fire.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F0EBE3` Warm Beige | `#141210` warm charcoal | Fireside warmth — never cool or blue-black |
| Card / surface | `#F5F2EB` Wheat | `#1C1917` leather-dark | Elevated surfaces lighter, like firelit leather |
| Border | `#D6CFC4` Sand | `#332E28` warm mid-grey | Visible structure without harshness |
| Border heavy | `#D6CFC4` at full | `#443D35` warm tan edge | Section separators, card hover |
| Primary text | `#1A1A1A` Near Black | `#E8E0D4` at 87% warm ivory | APCA Lc ~80 on `#1C1917` — warm tint essential |
| Secondary text | `#1A1A1A` at lighter usage | `#BDB5A8` at 65% sand | Readable secondary, not competing |
| Dim text | via reduced opacity | `#7A7268` warm stone | Captions, metadata — quiet presence |
| Particle foreground | `#C15F3C` Sienna | `#C15F3C` unchanged | Mid-tone warm — pops naturally on dark |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Burnt Sienna | `#C15F3C` | `#C15F3C` (stays) | Already mid-tone and warm — works on both grounds |
| Soft Coral | `#E8B49C` | `#F0C4AB` lightened | Was subtle on light; needs more visibility on dark |
| Muted Forest | `#3F4E4F` | `#6B8A8B` lifted, desaturated | Was dark-on-light text/contrast; must lighten for dark-on-dark |
| Warm Clay | `#A0522D` | `#C06A3A` brightened | Interactive elements need more presence on dark canvas |

#### Shadow & Depth Adaptation
- Light: No shadow — `1px sand border` provides separation. Flat editorial feel
- Dark: Maintain borderless approach where possible. Cards lift via background difference (`#1C1917` on `#141210`). If shadow needed: `0 2px 8px rgba(0,0,0,0.3)` — dark, not warm-glow

#### Texture & Grain Adaptation
- Light: Matte watercolor-wash feel with `multiply` blending on overlapping particles
- Dark: Watercolor bleed MORE visible on dark canvas. Alpha blending shifts from `multiply` to `screen` — particles lighten where they overlap instead of darkening. Matte finish preserved: no bloom, no glow halos around particles. Density mapping inverts: coral (sparse) → sienna (medium) → desaturated sage (dense)

#### Dark Mode Rules
- Particle physics unchanged — same 0.5x speed, same springs. Only color rendering shifts
- The beige-canvas "breathing room" becomes dark-canvas breathing room — negative space still dominates
- Coral-to-sienna-to-forest density gradient must remain readable; test at full particle density
- Cards use background-color difference for elevation, not shadow — the editorial flatness survives
- "Warm intellectual intimacy, like reading a long essay by the fire"

### Mobile Notes
- Reduce particle count to 60% of desktop.
- Remove breath cycle animation (subtle scale changes cause layout recalculations on some mobile browsers).
- Stagger delays can be halved (40ms) for snappier feel on touch.
