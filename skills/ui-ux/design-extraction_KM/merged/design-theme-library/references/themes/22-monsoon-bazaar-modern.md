## 22. Monsoon Bazaar Modern

> South Asian poster energy made systematic — saturated inks, bold labels, halftone textures constrained by a modern token system.

**Best for:** Music/event apps, playful consumer products, creative coding showcases, festival UIs, food delivery, social platforms.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Raw Cotton | `#F8F4EE` | Primary canvas. Warm unbleached base. |
| Alt Background | Newsprint | `#EDE8E0` | Cards, panels, secondary surfaces. |
| Primary | Hot Magenta | `#D42A78` | Primary actions, hero elements, key CTAs. |
| Secondary | Deep Indigo | `#2D3A8C` | Secondary actions, tags, nav elements. |
| Accent | Saffron | `#E8A030` | Highlights, badges, festive accents, warnings. |
| Neutral Text | Ink Black | `#1A1A1A` | Body text, headings. True ink density. |
| Muted Text | Bazaar Grey | `#6E6860` | Captions, metadata, secondary text. |
| Border | Jute | `#D0C8BC` | Dividers, card borders, separators. |

### Typography
- **Display:** Bricolage Grotesque (700–800 weight) — quirky, bold, editorial poster energy
- **Body:** DM Sans (400 weight) — clean counterpoint, high readability
- **Mono:** Fira Code — technical credibility, ligatures optional

### Visual Style
- **Halftone Grain:** SVG `feTurbulence` + `feComponentTransfer` (threshold) creates halftone-dot texture at 4% opacity. Applied as `::after` overlay on hero sections and image cards.
- **Ink Edges:** Borders and dividers use slightly rough SVG paths (1-2px jitter) instead of perfect lines. Subtle imperfection that reads "printed."
- **Saturated Zones:** High-chroma colors occupy defined zones (headers, CTAs, badges) while body areas remain neutral. The system prevents "color explosion."
- **Registration Offset:** Optional decorative technique: a shadow duplicate of headline text offset 2-3px in a secondary color (magenta text + indigo shadow offset). Mimics print registration misalignment.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.68, -0.55, 0.27, 1.55)` — elastic overshoot for entries. `ease-out` for exits.
- **Timing:** Snappy. Micro: 100–150ms. Entrances: 300ms. Stagger: 40ms per item.
- **Motion Character:** Kinetic and printed. Elements stamp into place (overshoot then settle), not float.
- **Physics:** Minimal — some bounce overshoot, but quickly resolved. Energetic, not chaotic.

### Signature Animations
1. **Stamp Press** — Elements enter with `scale(1.15)` → `scale(1)` + overshoot bounce. 300ms. Like a print stamp hitting paper.
2. **Registration Jitter** — On hover, colored shadow duplicates briefly shift ±1px in x/y and reset. 200ms. Subtle print vibration.
3. **Halftone Wipe** — Hero sections reveal with a halftone-dot pattern mask transitioning from 0% to 100% coverage. CSS `mask-image` with animated `mask-position`. 500ms.
4. **Bazaar Stagger** — List items enter with a fast stagger (40ms) with alternating slide directions (odd from left, even from right). 250ms each.
5. **Ink Splash** — Button click spawns a radial ink splash (`background-image: radial-gradient`) expanding from click point, 300ms, then fading.

### UI Components
- **Buttons:** Primary: magenta fill, white text, `border-radius: 6px`, 2px ink-black border. Secondary: indigo border, ink-black text. Hover: lighten 8% + registration jitter. Active: `scale(0.95)` + inset shadow.
- **Sliders:** Track is 4px jute line. Thumb is 16px magenta square with 2px black border. Value in Fira Code bold.
- **Cards:** Newsprint background, 2px ink-black border. `border-radius: 4px`. Hard shadow: `3px 3px 0 rgba(26,26,26,0.1)`. Padding 16px.
- **Tooltips:** Ink black background, raw cotton text. DM Sans 12px. `border-radius: 3px`.
- **Dividers:** Jute at 60% opacity. 1px with slight SVG roughness. Or saffron accent line (1px) for section breaks.

### Dark Mode Variant

Monsoon Bazaar Modern has a full dark mode — not an afterthought, a first-class variant. Street-food market at midnight: colors are HOT and vivid, because the darkness makes them louder.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F8F4EE` Raw Cotton | `#0E0C08` dark newsprint | Warm near-black — unlit bazaar alley |
| Card / surface | `#EDE8E0` Newsprint | `#141210` night market stall | Warm dark surface, slightly elevated |
| Border | `#D0C8BC` Jute | `#282420` dark jute | Warm mid-dark, rope-like texture reference |
| Border heavy | `#D0C8BC` at full | `#3A3630` burlap edge | Section dividers, card hover |
| Primary text | `#1A1A1A` Ink Black | `#F8F4EE` at 87% cotton glow | APCA Lc ~85 on `#141210` — warm and dense |
| Secondary text | `#6E6860` Bazaar Grey | `#B0A898` lifted grey | Readable secondary, warm bazaar tone |
| Dim text | `#6E6860` at lower opacity | `#787068` warm stone | Captions, metadata — street-sign faded |
| Hero accents | saturated zones | MORE saturated | Night market colors are louder — see accent shifts |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Hot Magenta | `#D42A78` | `#E84090` brightened | Neon signage — magenta glows at night |
| Deep Indigo | `#2D3A8C` | `#5060C0` brightened | Poster ink under UV light — indigo fluoresces |
| Saffron | `#E8A030` | `#F0B040` brightened | Turmeric glow — saffron catches lamplight |
| Ink Black text | `#1A1A1A` | structural/shadow role | No longer text — becomes deep structure |

#### Shadow & Depth Adaptation
- Light: Hard shadow `3px 3px 0 rgba(26,26,26,0.1)` — printed poster feel
- Dark: Hard shadow remains but inverts: `3px 3px 0 rgba(0,0,0,0.3)` — deeper, crisper on dark ground. Alternative: warm outline `3px 3px 0 rgba(248,244,238,0.04)` for a back-lit poster effect

#### Texture & Grain Adaptation
- Light: SVG halftone-dot texture at 4% opacity. Ink edges with 1-2px jitter SVG paths
- Dark: Halftone inverts — light dots on dark ground (same density, inverted luminance). Apply as `::after` overlay with `mix-blend-mode: screen` instead of `overlay`. Ink edge jitter preserved — structural, not decorative. Registration offset preserved — structural, not decorative

#### Dark Mode Rules
- Colors get LOUDER, not quieter. This is a night market — darkness amplifies saturated color. Magenta, indigo, saffron all brighten
- Halftone inversion is critical: light dots on dark, not dark dots removed. Same grid density
- Registration offset on headlines preserved exactly — offset distance and color unchanged, just more vivid
- Saturated zones (headers, CTAs, badges) become even more vivid against dark body areas — the contrast between neutral and saturated increases
- "Street-food market at midnight. Colors are HOT and vivid — the darkness makes them louder"

### Mobile Notes
- Disable registration jitter animation (subtle effect lost on mobile, wastes GPU).
- Simplify halftone wipe to a standard fade reveal.
- Touch targets: 48px minimum. Buttons should be full-width on mobile for poster energy.
