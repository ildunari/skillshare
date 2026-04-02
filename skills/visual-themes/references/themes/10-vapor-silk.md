## 10. Vapor Silk

> Soft, flowing, dreamlike — silk scarves in slow motion, pastel mist at golden hour.

**Best for:** Music visualizers, relaxation apps, ambient simulations, creative tools, mood boards, meditation experiences.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Warm Cream | `#FFF8F0` | Soft, warm base. Not stark white. |
| Surface | Blush Mist | `#FFF0F0` | Cards, panels. Barely-there pink tint. |
| Primary | Soft Lavender | `#E8E0F0` | Primary elements, active states. |
| Secondary | Blush Pink | `#FFD6E0` | Secondary elements, highlights. |
| Tertiary | Pale Mint | `#D4F0E8` | Tertiary data, positive indicators. |
| Accent | Dusty Mauve | `#C9A0B8` | CTA buttons, focused elements. |
| Gradient Mesh | Multi-pastel | various | Animated mesh of all palette colors for backgrounds. |
| Text | Warm Grey | `#5A5060` | Body text. Warm-tinted grey. |

### Typography
- **Display:** Outfit (500) — warm, modern, approachable
- **Body:** Figtree — warm, crisp, friendly readability
- **Mono:** Space Mono — quirky accent for values

### Visual Style
- **Gradient Mesh:** Background is a slow-moving mesh gradient (4-6 pastel color stops, animated `background-position` over 20-30s). Creates an always-shifting, dreamlike backdrop.
- **Zero Hard Edges:** Everything has generous `border-radius` (16-24px). Buttons are pills. Cards are rounded. Even images get border-radius.
- **Silk Layering:** Semi-transparent overlapping elements with slight blur. Not as heavy as Liquid Glass — more like silk layers (10% opacity fills, no backdrop-filter unless essential).
- **Soft Focus:** Edges of the viewport have a subtle blur gradient (CSS `mask-image` with gradient), creating a dreamy soft-focus border.

### Animation Philosophy
- **Easing:** Ultra-smooth — `cubic-bezier(0.4, 0, 0.2, 1)`. Or slow springs: `stiffness: 60, damping: 15`. Nothing snaps.
- **Timing:** Long, flowing. 800ms-1.5s for transitions. Background mesh: 20-30s. This theme exists outside of urgency.
- **Motion Character:** Silk-like. Elements flow, drape, settle. Think slow-motion fabric in wind.
- **Physics:** Air resistance dominant. Elements float with gentle deceleration, like feathers.

### Signature Animations
1. **Silk Wave** — Background mesh gradient undulates slowly via animated `background-position` and `background-size` changes. Continuous, mesmerizing.
2. **Mist Fade** — Elements enter with a long fade (800ms) combined with 0.5px blur transitioning to sharp. Like emerging from mist.
3. **Pastel Morph** — Interactive elements slowly shift their background between palette colors on hover (1.5s transition). Never snaps.
4. **Breath Scale** — Cards and panels subtly scale (1.0→1.005→1.0) over 6s cycles. Barely perceptible but creates life.
5. **Veil Transition** — Page/section transitions layer a semi-transparent silk veil (gradient overlay) that sweeps across before revealing new content.

### UI Components
- **Buttons:** Pill shape (`border-radius: 999px`). Dusty mauve fill, white text. No border. Soft shadow (`0 2px 12px rgba(201,160,184,0.2)`). Hover: lighten 10%. Active: `scale(0.97)`.
- **Sliders:** Track is a rounded pill (6px tall) with pastel gradient fill. Thumb is a white circle (24px) with soft mauve shadow.
- **Cards:** Blush mist surface. `border-radius: 20px`. No border. Soft shadow. Generous padding (24px).
- **Tooltips:** Lavender fill at 90% opacity. Warm grey text. Pill-shaped. Very soft.
- **Dividers:** None. Use generous whitespace (40-60px). If needed, a 1px gradient line fading from transparent → mauve → transparent.

### Dark Mode Variant

Vapor Silk has a full dark mode — not an afterthought, a first-class variant. Candlelit boudoir with silk draping — pastels become muted jewel tones.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#FFF8F0` Warm Cream | `#100C14` Deep Plum | oklch(0.08 0.02 310) — dark with violet/plum undertone |
| Card / surface | `#FFF0F0` Blush Mist | `#1A1520` Dark Silk | oklch(0.12 0.02 310) — elevated surfaces lift slightly |
| Alt surface | — | `#221C28` Silk Layer | oklch(0.16 0.02 310) — secondary panels |
| Border | implied (no borders) | `#2A2430` Mauve Shadow | oklch(0.19 0.02 310) — structure that light mode didn't need |
| Border heavy | — | `#352E3C` Bright Mauve | oklch(0.24 0.02 310) — hover, emphasis |
| Primary text | `#5A5060` Warm Grey | `#E8E0E8` Lavender White | oklch(0.92 0.01 310) at 87% opacity |
| Secondary text | — | `#B0A8B4` Muted Silk | oklch(0.72 0.01 310) — captions, metadata |
| Dim text | — | `#7A7080` Dusky Mauve | oklch(0.52 0.01 310) — timestamps |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Soft Lavender | `#E8E0F0` | `#6A5A7A` Jewel Lavender | Pastels darken to muted jewel tones — structural in dark mode |
| Blush Pink | `#FFD6E0` | `#B08090` Pink Ribbon | Warm pink becomes deeper, richer — boudoir warmth |
| Pale Mint | `#D4F0E8` | `#608878` Mint Shadow | Cool mint darkens to shadowed green — candlelight doesn't reach it |
| Dusty Mauve (CTA) | `#C9A0B8` | `#D4A8C4` Lifted Mauve | Accent brightens slightly — CTA must lift from dark surface |
| Mesh gradient stops | various pastels | darken all stops ~40% lightness | Same animation timing, darker palette — candlelit silk |

#### Shadow & Depth Adaptation
- Light: Soft shadows — `0 2px 12px rgba(201,160,184,0.2)` — silk layers floating
- Dark: Shadows become warm glows — `0 0 16px rgba(212,168,196,0.08)` — mauve aura around elevated cards. Surface hierarchy inverts: lighter surfaces are elevated. Border-radius stays generous (16-24px) — the soft, rounded identity is preserved

#### Texture & Grain Adaptation
- Light: Gradient mesh with pastel color stops, animated `background-position` over 20-30s
- Dark: Same mesh animation, same timing. All color stops darkened by ~40% lightness — lavender `#E8E0F0` becomes `#3A3050`, pink `#FFD6E0` becomes `#4A2838`, mint `#D4F0E8` becomes `#1A3A30`. The mesh becomes a slow-moving jewel-tone tapestry. Blend mode unchanged

#### Dark Mode Rules
- Pastels become muted jewel tones, NOT just darkened versions — each color shifts toward its deeper, richer cousin
- Mesh gradient animation continues at the same 20-30s cycle — the dreamy, flowing motion is essential to identity
- Pill-shaped buttons and generous border-radius preserved — softness is non-negotiable even in dark mode
- Borders become necessary in dark mode (invisible in light) — use `#2A2430` mauve shadow for subtle card edges
- "Candlelit boudoir with silk draping — pastels become muted jewel tones"

### Mobile Notes
- Mesh gradient animation is cheap (CSS only, GPU-composited `background-position`).
- Remove viewport blur mask on mobile (mask-image can be expensive).
- Reduce breath scale animation (layout-triggering `transform: scale` is fine, but test on target devices).
- This theme is moderately performant — the main cost is layered semi-transparent elements.
