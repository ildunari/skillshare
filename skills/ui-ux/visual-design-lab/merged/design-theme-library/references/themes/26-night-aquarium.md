## 26. Night Aquarium

> Deep ocean calm with bioluminescent cues — dark teal depths, soft glow highlights, slow ambient drift.

**Best for:** Media players, ambient data art, night-mode creative tools, audio visualizers, relaxation apps, nighttime UIs.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Abyssal Teal | `#0A1A1E` | Primary canvas. Deep ocean darkness. |
| Alt Background | Deep Current | `#122428` | Cards, elevated surfaces. Slightly lighter depth. |
| Primary Text | Seafoam | `#D0E8E4` | Body text. Soft, easy on eyes in dark. |
| Secondary Text | Deep Mist | `#7A9A94` | Captions, metadata. Muted aquatic. |
| Accent 1 | Bioluminescent Cyan | `#40D8C0` | Primary interactive, links, focus. Organic glow. |
| Accent 2 | Jellyfish Pink | `#D87AAC` | Secondary accents, notifications, alerts. |
| Ambient Glow | Plankton Green | `#30C890` | Ambient particles, subtle background elements. |
| Border | Thermocline | `#1E3A3E` | Subtle dividers, card edges. Barely visible. |

### Typography
- **Display:** Manrope (variable, 600 weight) — geometric but friendly, clean on dark backgrounds
- **Body:** Sora (400 weight) — futuristic sans, excellent readability at small sizes on dark
- **Mono:** Fira Code — strong on dark, good at small sizes

### Visual Style
- **Depth Layering:** Three distinct depth planes: background (abyssal), content surface (deep current), floating elements (slightly lighter). Depth communicated via lightness, not shadow.
- **Organic Glow:** Interactive elements have a soft `box-shadow` glow (e.g., `0 0 12px rgba(64,216,192,0.15)`) that breathes — not a static neon ring. The glow expands slightly on hover.
- **Caustic Light:** Optional WebGL caustic pattern in the background — very slow (30s cycle), very faint (5% opacity). Like sunlight filtering through water. Fallback: animated radial gradient shifting position.
- **No Hard Edges:** `border-radius: 10px` minimum on all containers. The ocean doesn't have corners.

### Animation Philosophy
- **Easing:** Slow spring — `stiffness: 80, damping: 20`. Or `cubic-bezier(0.22, 1, 0.36, 1)`.
- **Timing:** Slow. Ambient: 15–30s cycles. UI: 300–400ms. Content reveals: 500ms.
- **Motion Character:** Organic and drifting. Elements float into position, settling like something suspended in water.
- **Physics:** Underwater model — high drag, no gravity, slow deceleration. Objects glide and slow gently.

### Signature Animations
1. **Depth Emerge** — Content blocks fade in + rise 8px upward (as if floating from deeper water). Stagger at 80ms. 500ms each.
2. **Bioluminescent Pulse** — Active elements breathe: glow shadow expands 20% → contracts over 3s interval. Continuous, subtle.
3. **Caustic Shimmer** — Background caustic light pattern shifts slowly, like underwater light refraction. WebGL or CSS gradient animation. 30s cycle.
4. **Jellyfish Drift** — Loading indicators: a soft jellyfish-pink orb that drifts in a gentle figure-8 path with opacity pulsing. Pure CSS with `@keyframes`.
5. **Current Flow** — Horizontal scroll containers have elements that gently sway ±1px vertically as they scroll, like objects in a current. Subtle parallax.

### UI Components
- **Buttons:** Primary: bioluminescent cyan fill at 90% opacity, abyssal text, `border-radius: 10px`. Secondary: 1px thermocline border, seafoam text. Hover: glow shadow expands. Active: `scale(0.97)` + glow brightens.
- **Sliders:** Track is 3px thermocline line with `border-radius: full`. Thumb is 14px cyan circle with glow. Value in Fira Code.
- **Cards:** Deep current background, 1px thermocline border. `border-radius: 12px`. Subtle glow on hover: `box-shadow: 0 0 20px rgba(64,216,192,0.05)`. Padding 20px.
- **Tooltips:** Deep current background, seafoam text. Sora 12px. `border-radius: 8px`. No border (depth separation only).
- **Dividers:** Thermocline at 30% opacity. 1px. Or negative space (40px gap).

### Light Mode Variant

Night Aquarium has a full light mode — not an afterthought, a first-class variant. The dark theme is the deep abyss at night; the light theme is the shallow tropical lagoon at midday. The organisms are the same, the light is different.

#### Structural Color Map

| Role | Dark (native) | Light (variant) | Notes |
|---|---|---|---|
| Page background | `#0A1A1E` abyssal teal | `#E8F4F0` shallow lagoon | oklch(0.96 0.02 170) — pale teal, sun-dappled shallows |
| Card / surface | `#122428` deep current | `#F0FAF6` bright water column | oklch(0.98 0.01 165) — near-white with green-aqua tint |
| Border | `#1E3A3E` thermocline | `#C0D8D0` coral edge | oklch(0.87 0.03 170) — soft aquatic border |
| Border heavy | — | `#A0C0B8` deeper coral edge | Heavier section separators |
| Primary text | `#D0E8E4` seafoam | `#1A3A34` deep teal ink | oklch(0.27 0.04 170) — dark with strong teal identity |
| Secondary text | `#7A9A94` deep mist | `#3A6A60` reef shadow | Readable, aquatic cast |
| Dim text | — | `#7A9A90` sea glass | Labels, timestamps, depth metadata |
| Caustic light | WebGL/gradient, 5% | Subtle warm caustic, 3% | Gentler — sunlight is direct, not scattered through deep water |

#### Accent Shifts

| Element | Dark (native) | Light (variant) | Reason |
|---|---|---|---|
| Bioluminescent Cyan | `#40D8C0` | `#1A8A78` | oklch(0.56 0.10 175) — deep reef teal. APCA Lc ~62 on white |
| Jellyfish Pink | `#D87AAC` | `#B85890` | oklch(0.52 0.12 345) — coral pink, darkened for contrast |
| Plankton Green | `#30C890` | `#1A7050` | oklch(0.46 0.10 160) — seaweed green, grounded for daylight |

#### Shadow & Depth Adaptation

- **Dark:** Depth via luminance (three planes: abyssal → deep current → floating). Organic glow — soft `box-shadow` that breathes (expands on hover). No hard edges. `border-radius: 10px` minimum.
- **Light:** Depth via subtle shadow. Cards: `box-shadow: 0 2px 8px rgba(26,58,52,0.06)` — cool-teal tinted shadow, aquatic feel. Organic glow replaced by organic colored shadow: `box-shadow: 0 2px 12px rgba(26,138,120,0.10)` on hover. The breathing expansion animation preserved — the shadow grows and contracts, not light. `border-radius: 10px` preserved.

#### Texture & Grain Adaptation

- **Dark:** Caustic light pattern (WebGL or animated radial gradient, 30s cycle, 5% opacity). Depth layering via three luminance planes.
- **Light:** Caustic pattern persists but gentler — warm-toned, 3% opacity, representing direct sunlight on shallow water (not deep-scattered light). The animation slows to 45s cycle. Depth layering via shadow intensity instead of luminance — foreground cards cast slightly stronger shadows than background elements.

#### Light Mode Rules

1. **Organic glow becomes organic shadow.** Every glowing `box-shadow` (radiating light in darkness) converts to a colored drop-shadow (teal-tinted shade on light). The hover expansion animation transfers to the shadow, not the glow.
2. **No hard edges — preserved.** `border-radius: 10px` minimum remains. The ocean still doesn't have corners.
3. **Drift animation preserved.** Current flow, jellyfish drift, and depth emerge animations all work on light. The motion is aquatic, not luminance-dependent. Springs with high drag, underwater physics — all transfer cleanly.
4. **Accent colors darken significantly.** All three accents shift 30-40% darker. Light water makes colors appear washed-out at dark-mode brightness — darker variants restore visual weight.
5. "Daylight reef, not deep abyss. The organisms are the same, the light is different."

### Mobile Notes
- Disable caustic shimmer WebGL shader; use static radial gradient instead.
- Disable bioluminescent pulse animation (continuous animation drains battery).
- Reduce glow box-shadows to 1 layer (performance).
- Touch targets: 48px minimum — generous, no sharp edges.
