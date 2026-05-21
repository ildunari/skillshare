## 24. Chromed Bloom (Y3K Soft Metal)

> Futuristic chrome aesthetic tempered with warmth and readability — soft metal surfaces, iridescent edges, controlled gloss.

**Best for:** Consumer tech, product marketing, interactive demos, portfolio showcases, creative tools, launch pages.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Soft Silver | `#F2F0EE` | Primary canvas. Warm metallic neutral. |
| Alt Background | Polished White | `#FAFAFA` | Cards, elevated surfaces. |
| Primary Text | Graphite | `#1A1A20` | Body text. Deep with slight blue cast. |
| Secondary Text | Brushed Steel | `#7A7880` | Captions, metadata. Cool grey. |
| Accent Primary | Iridescent Violet | `#7C5CFC` | Primary CTAs, focus, selection. Shifts slightly on hover. |
| Accent Secondary | Rose Chrome | `#E8709C` | Secondary accents, badges, notifications. |
| Surface Chrome | Mirror | `#E8E6E4` | Metallic card surfaces, button fills. |
| Border | Hairline | `#D8D6D4` | Subtle dividers, card edges. |

### Typography
- **Display:** Sora (variable, 600–700 weight) — geometric, futuristic, excellent at large sizes
- **Body:** DM Sans (400 weight) — clean, modern, reads well against metallic surfaces
- **Mono:** Space Mono — retro-futuristic mono, distinctive character

### Visual Style
- **Soft Metal:** Surfaces use subtle linear gradients (2–3° tilt, 3% lightness variation top-to-bottom) to simulate brushed metal. Never flat, never glossy.
- **Iridescent Edge:** On hover over cards/interactive elements, a conic-gradient border sweeps through violet→rose→cyan at 15% opacity. `mix-blend-mode: overlay`. Animated `background-position` at 2s loop.
- **Specular Highlight:** Cards have a very faint white highlight at top-left (radial-gradient at 3% opacity), simulating studio lighting on metal.
- **No Neon:** Despite being futuristic, there are ZERO neon effects. Iridescence is soft, pastel-shifted, warm. This is Y3K, not cyberpunk.

### Animation Philosophy
- **Easing:** Magnetic spring — `stiffness: 200, damping: 18`. Objects feel attracted to their target position.
- **Timing:** Medium-fast. Micro: 120ms. Transitions: 250ms. Iridescent shifts: 2–3s continuous.
- **Motion Character:** Magnetic and smooth. Elements glide into position, attracted rather than thrown.
- **Physics:** Spring-based with medium damping. Slight overshoot (5%) that resolves quickly.

### Signature Animations
1. **Chrome Slide** — Elements enter with a horizontal slide + iridescent edge flashing briefly on arrival. 300ms spring.
2. **Metal Breathe** — Card surfaces subtly shift their gradient angle ±1° over 6s. Like light playing on chrome in a display case.
3. **Iridescent Sweep** — On hover, the border gradient rotates 180°. `background-position` animated over 400ms.
4. **Magnetic Snap** — Draggable elements use spring physics to snap to targets, with brief metallic highlight flash on connect.
5. **Bloom Entry** — Hero elements enter with `scale(0.9)` → `scale(1)` + `filter: brightness(1.1)` settling to `brightness(1)`. 400ms. Like light catching a polished surface.

### UI Components
- **Buttons:** Primary: iridescent violet fill, white text, `border-radius: 10px`. Secondary: 1px hairline border, graphite text, chrome surface fill. Hover: iridescent edge sweep. Active: `scale(0.97)`.
- **Sliders:** Track is 3px chrome-surface gradient. Thumb is 16px violet circle with white glow (`box-shadow: 0 0 8px rgba(124,92,252,0.3)`). Value in Space Mono.
- **Cards:** Polished white background with top-left specular highlight. 1px hairline border. `border-radius: 12px`. On hover: iridescent border sweep. Padding 20px.
- **Tooltips:** Graphite background, soft silver text. DM Sans 12px. `border-radius: 6px`.
- **Dividers:** Hairline at 50% opacity. 1px. Or a thin iridescent gradient line (3px, full-width, at 15% opacity).

### Dark Mode Variant

Chromed Bloom has a full dark mode — not an afterthought, a first-class variant. Luxury car showroom at night — chrome reflects, iridescence shimmers.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F2F0EE` Soft Silver | `#0A0A0E` Obsidian Chrome | oklch(0.06 0.005 280) — cool dark with faint violet cast |
| Card / surface | `#FAFAFA` Polished White | `#121216` Dark Mirror | oklch(0.10 0.005 280) — reflective dark surfaces |
| Alt surface | `#E8E6E4` Mirror | `#1A1A20` Deep Chrome | oklch(0.13 0.01 280) — secondary panels |
| Border | `#D8D6D4` Hairline | `#28282E` Brushed Edge | oklch(0.19 0.005 280) — subtle card edges |
| Border heavy | — | `#34343C` Bright Edge | oklch(0.24 0.005 280) — hover, emphasis |
| Primary text | `#1A1A20` Graphite | `#E4E2E8` Silver Text | oklch(0.92 0.005 280) at 87% opacity |
| Secondary text | `#7A7880` Brushed Steel | `#9A98A0` Lifted Steel | oklch(0.66 0.005 280) — captions |
| Dim text | — | `#6A6870` Dark Steel | oklch(0.46 0.005 280) — metadata |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Iridescent Violet | `#7C5CFC` | `#9478FF` (brighter) | Iridescent pop against dark — violet lifts to catch showroom light |
| Rose Chrome | `#E8709C` | `#F090B0` (brighter) | Rose glow intensifies on dark backgrounds |
| Specular highlight | 3% opacity white radial | 5% opacity white radial | Highlights slightly more prominent on dark chrome |
| Iridescent border sweep | violet→rose→cyan at 15% | violet→rose→cyan at 20% | Conic-gradient MORE dramatic on dark — wider sweep opacity |

#### Shadow & Depth Adaptation
- Light: Specular highlight gradients + soft shadows — studio lighting on polished metal
- Dark: Metal gradients darken their base while maintaining specular highlights. Chrome needs contrast: dark base + bright specular = showroom effect. Shadows become iridescent glows: `0 0 16px rgba(148,120,255,0.08)` on interactive elements. Surface hierarchy from luminance: lighter = elevated

#### Texture & Grain Adaptation
- Light: Subtle linear gradients (2-3 degree tilt, 3% lightness variation) simulating brushed metal
- Dark: Same brushed-metal gradients, inverted — dark base with slightly lighter top. Gradient variation increases to 5% to maintain the metallic shimmer on dark surfaces. Specular highlight (radial gradient) increases from 3% to 5% opacity. The iridescent border sweep (`conic-gradient`) is MORE dramatic on dark — the gradient catches more visual attention against the obsidian background

#### Dark Mode Rules
- Metal gradients preserve their directional character — light source remains upper-left, but base darkens while highlights maintain brightness
- Iridescent border sweep becomes the signature moment — `conic-gradient` rotating through violet→rose→cyan is more dramatic on dark than light
- Chrome surface feel maintained through gradient variation and specular highlights — flat fills would lose the Y3K metallic identity
- No-neon rule still applies — iridescence is soft and warm even on dark. This is showroom chrome, not cyberpunk neon
- "Luxury car showroom at night — chrome reflects, iridescence shimmers"

### Mobile Notes
- Disable iridescent border sweep animation (GPU-intensive gradient animation).
- Replace specular highlight gradients with flat fills.
- Touch targets: 48px minimum. Buttons should feel substantial and "metallic."
