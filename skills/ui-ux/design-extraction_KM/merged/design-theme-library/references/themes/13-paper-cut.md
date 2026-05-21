## 13. Paper Cut

> Physical craft digitized — layered construction paper, deliberate shadows, tangible depth.

**Best for:** Infographics, educational simulations, storytelling artifacts, terrain/map visualizations, explainer experiences, children's content.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Craft Paper | `#F5E6D3` | Kraft paper base. Warm, tactile. |
| Layer 1 | Deep Indigo | `#2C3E6B` | Deepest paper layer. Mountains, backgrounds. |
| Layer 2 | Coral Red | `#E8614D` | Mid-layer. Active elements, CTA, highlights. |
| Layer 3 | Sage Green | `#87A878` | Nature layer. Growth, positive, environmental. |
| Layer 4 | Cream | `#FFFEF5` | Top layer. Cards, text panels, foreground. |
| Shadow | Warm Brown | `#3D2B1F` | Hard parallax shadows between layers. |
| Accent | Mustard | `#D4A843` | Highlights, badges, interactive states. |
| Text | Deep Brown | `#2C1810` | On light layers. Warm, craft-feel. |

### Typography
- **Display:** Bricolage Grotesque (700) — crafty, woodblock-print, editorial quirk
- **Body:** Work Sans (400) — versatile, warm, pairs with quirky display
- **Mono:** Fira Code — if needed for data values

### Visual Style
- **Multi-Layer Depth:** Every composition has 3-5 explicit depth layers with parallax-offset colored shadows between them. Shadows are hard (no blur), colored (warm brown), and directional (consistent light source from upper-left).
- **Paper Texture:** Each layer has a slightly different paper texture — craft brown, construction paper, cardstock. Achieve via subtle noise overlay at varying intensities.
- **Cut Edges:** Shape edges are imperfect. Slight irregular contours achieved via SVG path jitter or `clip-path` with hand-drawn polygon coordinates.
- **Flat + Layered:** Colors within each layer are flat (no gradients). All depth perception comes from layering and shadows, not shading.

### Animation Philosophy
- **Easing:** Springy overshoot — `cubic-bezier(0.34, 1.56, 0.64, 1)`. Paper snapping into place.
- **Timing:** Medium. Layer reveals 400-600ms. Card interactions 200-300ms. Satisfying, not slow.
- **Motion Character:** Physical, tactile. Paper sliding, folding, stacking. Everything feels like it has physical presence.
- **Physics:** Simple gravity + friction. Elements slide into place and stop. No bouncing.

### Signature Animations
1. **Layer Slide** — Depth layers enter from different directions with different delays, creating a parallax build-up. Background layer first, foreground last. 100ms stagger.
2. **Paper Fold** — Cards transition by folding along an edge (CSS `perspective` + `rotateX`). The "back" of the card is a darker shade of the front color.
3. **Pop-Up Book** — Complex scene transitions where elements rise from flat to angled (like a pop-up book opening), using 3D transforms with consistent lighting.
4. **Tear Away** — Deleted/dismissed elements animate off-screen with a slight rotation (±5°) and acceleration, like paper being torn away.
5. **Shadow Shift** — On hover, an element's hard shadow grows (4px→8px offset) and shifts, creating the illusion of lifting off the surface.

### UI Components
- **Buttons:** Coral red fill, cream text. Hard shadow (4px offset, warm brown). `border-radius: 6px` (slightly soft, like die-cut paper). Hover: shadow grows to 6px. Active: shadow reduces to 2px.
- **Sliders:** Track is indigo 4px line. Thumb is a mustard circle (16px) with hard shadow. Feels like a paper tab on a rail.
- **Cards:** Cream surface, craft paper visible around edges. Hard shadow (6px). `border-radius: 8px`. Generous padding. Colored top border (4px) matching content category.
- **Tooltips:** Mustard fill, deep brown text. Hard shadow. Looks like a paper tag.
- **Dividers:** Torn-edge SVG paths. Or thick (3px) colored lines with paper-tab endpoints.

### Dark Mode Variant

Paper Cut has a full dark mode — not an afterthought, a first-class variant. Shadow-box puppet theatre: light shining through paper silhouettes, layered depth glowing from behind.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F5E6D3` Craft Paper | `#100E08` dark kraft | Deep warm brown-black — craft paper in a dark room |
| Card / surface | `#FFFEF5` Cream | `#1A1410` deep cardboard | Layered paper feel preserved in dark tones |
| Border | implicit via shadows | `#302818` brown edge | Warm brown borders replace shadow-based separation |
| Border heavy | n/a | `#3E3020` kraft edge | Section dividers, card hover |
| Primary text | `#2C1810` Deep Brown | `#F5E6D3` craft paper color becomes text | APCA Lc ~84 on `#1A1410` — the craft paper IS the text color |
| Secondary text | `#2C1810` at lighter weight | `#C8B8A0` warm parchment | Readable secondary, craft warmth |
| Dim text | n/a | `#8A7A64` aged cardboard | Labels, metadata — papery grey-brown |
| Layer colors | various paper layers | adjusted per layer | Each layer shifts, see accent table |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Deep Indigo | `#2C3E6B` | `#4A5E8B` lightened | Still recognizable as indigo, more visible on dark ground |
| Coral Red | `#E8614D` | `#E8614D` stays | Mid-tone warm — already pops on dark |
| Sage Green | `#87A878` | `#98B88A` lightened | Green was mid-tone on light; needs slight lift on dark |
| Mustard | `#D4A843` | `#D4A843` stays | Warm gold accent works on both grounds |
| Warm Brown shadow | `#3D2B1F` | `rgba(245,230,211,0.06)` craft glow | Shadow → luminous outline inversion |

#### Shadow & Depth Adaptation
- Light: Hard parallax shadows — 4–8px offset, `#3D2B1F` warm brown, NO blur. Multi-layer depth creates "stacked construction paper" effect
- Dark: Hard shadows become luminous outlines — `rgba(245,230,211,0.06)` light outlines at same offset geometry. The depth system inverts: instead of dark shadows pushing layers down, light edges lift layers up. Shadow-box puppet theatre: depth reads through back-lighting

#### Texture & Grain Adaptation
- Light: Each layer has different paper texture — craft brown, construction paper, cardstock. Noise overlay at varying intensities
- Dark: Paper texture drops to 2% opacity, blend mode shifts to `soft-light`. Cut edges (SVG path jitter) preserved — they're structural, not decorative. Construction-paper grain must remain perceptible — these are still paper layers, just in a dark shadow box

#### Dark Mode Rules
- Multi-layer depth system preserved: 3–5 layers, each a slightly different warm dark tone
- Shadow → luminous outline is the critical inversion. Same offset geometry, inverted luminance
- Craft paper color `#F5E6D3` becomes text color — the material identity transfers from background to foreground
- Pop-up book and paper fold 3D animations: light direction shifts. `perspective-origin` adjusts for back-lit feeling
- "Shadow-box puppet theatre — light shining through paper silhouettes"

### Mobile Notes
- Hard shadows are cheap — excellent mobile performance.
- Parallax layer sliding: reduce to 2-3 layers on mobile.
- Cut edge jitter: pre-compute SVG paths (static, no per-frame calculation).
- Pop-up book 3D transforms: test on target devices (CSS 3D perspective can be janky on older mobile WebKit).
