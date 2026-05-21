## 17. Ceramic Glaze UI

> Soft ceramic surfaces with a controlled glaze highlight — calm but tactile, like a handmade bowl you can't stop touching.

**Best for:** Wellness apps, creative tools, simulation UIs, meditation timers, habit trackers, calm productivity.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Bisque Clay | `#F3EDE5` | Primary canvas. Warm matte ceramic base. |
| Alt Background | Kiln White | `#FAF7F2` | Cards, modals, elevated surfaces. |
| Primary Glaze | Cobalt Blue | `#3B6B9C` | Primary interactive elements, links, active states. |
| Secondary Glaze | Celadon Green | `#7BA393` | Secondary accents, tags, success states. |
| Neutral Mid | Warm Taupe | `#8C7E72` | Secondary text, icons, inactive states. |
| Surface Shadow | Clay Shadow | `#D6CCC2` | Borders, subtle separators. |
| Text | Fired Earth | `#2C2420` | Body text, headings. Deep warm brown. |
| Highlight | Amber Glaze | `#D4A054` | Warnings, emphasis, selection highlights. |

### Typography
- **Display:** DM Sans (600 weight) — rounded terminals feel ceramic-smooth, modern warmth
- **Body:** Figtree — open apertures, friendly, high readability at small sizes
- **Mono:** Geist Mono — clean numerals for data and parameters

### Visual Style
- **Matte Surface:** No gloss, no shine on UI elements. Surfaces feel like unglazed stoneware — flat fills with minimal shadow.
- **Glaze Bloom:** Optional slow reaction-diffusion shader (WebGL or Canvas) for large empty states and loading screens. Colors drawn from palette at 10–15% opacity. Must respect `prefers-reduced-motion`.
- **Rounded Everything:** `border-radius: 12px` on cards, `8px` on buttons, `full` on avatars. Organic, no sharp corners.
- **Compositing:** Where glaze elements overlap surfaces, use a subtle `multiply` blend at low opacity to create depth without shadows.

### Animation Philosophy
- **Easing:** Viscous spring — `stiffness: 180, damping: 24`. Or `cubic-bezier(0.34, 1.56, 0.64, 1)` for slight overshoot.
- **Timing:** Medium. UI transitions 300–400ms. Ambient glaze animations 15–30s cycle (very slow).
- **Motion Character:** Tactile, weighted. Elements feel like they have mass — they settle, they don't snap.
- **Physics:** Medium damping, slight overshoot on modals and drawers. Like placing a ceramic piece down carefully.

### Signature Animations
1. **Glaze Pour** — New elements enter with a radial opacity reveal (center-out), like glaze pooling and settling. 400ms.
2. **Kiln Breathe** — Ambient background subtly shifts warmth: bisque clay oscillates ±2% lightness over 20s. Purely decorative.
3. **Tactile Press** — Buttons `scale(0.96)` on press with 80ms response, spring back over 250ms. Satisfying haptic feedback feel.
4. **Ceramic Slide** — Panels slide with deceleration curve — fast start, slow settle, like sliding a bowl across a table.
5. **Glaze Shimmer** — On hover over primary elements, a very subtle lightness shift (+3% L in OKLCH) sweeps left-to-right over 300ms.

### UI Components
- **Buttons:** Cobalt fill for primary (`border-radius: 8px`), clay border for secondary. Text in DM Sans 500. Hover: lighten 8%. Active: `scale(0.96)` with shadow reduction.
- **Sliders:** Track is clay-shadow colored, 4px, `border-radius: full`. Thumb is cobalt circle (16px) with 2px kiln-white border. Value in Geist Mono.
- **Cards:** Kiln white background, no border. `border-radius: 12px`. Subtle shadow: `0 2px 8px rgba(44,36,32,0.06)`. Padding 20px.
- **Tooltips:** Fired earth background, kiln white text. Figtree small. `border-radius: 6px`.
- **Dividers:** Clay shadow at 40% opacity. 1px. Or 32px whitespace gap.

### Dark Mode Variant

Ceramic Glaze UI has a full dark mode — not an afterthought, a first-class variant. Dark clay body with luminous glaze accents — the kiln at night, where glaze glows more intensely against fired earth.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F3EDE5` Bisque Clay | `#121010` fired dark earth | Warm ceramic dark — kiln interior after firing |
| Card / surface | `#FAF7F2` Kiln White | `#1E1915` kiln interior | Elevated lighter, like clay catching kiln-glow |
| Border | `#D6CCC2` Clay Shadow | `#302A24` dark clay edge | Warm mid-tone, tactile feel preserved |
| Border heavy | `#D6CCC2` at full | `#3A322C` fired edge | Heavier dividers for section structure |
| Primary text | `#2C2420` Fired Earth | `#F3EDE5` at 87% bisque becomes light text | APCA Lc ~83 on `#1E1915` — bisque clay glow, warm |
| Secondary text | `#8C7E72` Warm Taupe | `#A89A8E` lifted taupe | Readable secondary, ceramic warmth |
| Dim text | `#8C7E72` at lower opacity | `#706660` warm clay grey | Icons, inactive states — present but muted |
| Highlight | `#D4A054` Amber Glaze | `#D4A054` stays | Amber mid-tone — warm and visible on both grounds |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Cobalt Blue | `#3B6B9C` | `#5A8DC4` brightened | Glaze brightens on dark clay — more luminous, more ceramic |
| Celadon Green | `#7BA393` | `#90B8A8` brightened | Celadon lifts to glow against dark earth |
| Amber Glaze | `#D4A054` | `#D4A054` stays | Warm mid-tone accent — already works on dark |
| Warm Taupe | `#8C7E72` | `#A89A8E` lifted | Needs more presence on dark surfaces |

#### Shadow & Depth Adaptation
- Light: `0 2px 8px rgba(44,36,32,0.06)` — subtle warm shadow, ceramic weight
- Dark: Shadow deepens to `0 2px 8px rgba(0,0,0,0.25)`. On cards, add subtle top-edge highlight: `inset 0 1px 0 rgba(243,237,229,0.04)` — glaze catching light on the rim

#### Texture & Grain Adaptation
- Light: Matte surface, no gloss. Glaze bloom shader for empty states at 10–15% opacity
- Dark: Matte surface absolutely preserved — dark mode ceramic is unglazed stoneware, not polished obsidian. Glaze bloom shader colors shift to darker palette variants, opacity drops to 6–8%. The bloom effect actually looks more dramatic on dark — constrain it

#### Dark Mode Rules
- Rounded corners preserved everywhere — `border-radius: 12px` cards, `8px` buttons. The signature softness transcends mode
- Glaze accents (cobalt, celadon) become the primary visual interest — they glow against dark clay
- Matte rule is non-negotiable: no glossy surfaces, no glass-morphism, no sheen effects in dark mode
- Kiln Breathe ambient animation: oscillation shifts from lightness to warmth — hue rotates ±2° instead of L ±2%
- "Dark clay body with luminous glaze accents — the glaze glows more at night"

### Mobile Notes
- Disable glaze bloom shader (performance). Replace with a static low-opacity radial gradient.
- Reduce spring overshoot to zero (stability on lower-end devices).
- Touch targets: minimum 48px for all interactive elements (generous for the calm aesthetic).
