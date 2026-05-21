## 20. Kintsugi Ledger

> Japanese ledger paper meets repaired-gold seams — calm minimal surfaces with deliberate "repair lines" as accents for boundaries and progress.

**Best for:** Meditation apps, journaling, narrative games, boutique commerce, mindfulness tools, personal dashboards.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Washi Paper | `#F5F0E8` | Primary canvas. Warm neutral with imperceptible yellow undertone. |
| Alt Background | Rice White | `#FAF8F3` | Cards, input fields, elevated surfaces. |
| Primary Text | Sumi Ink | `#1C1B18` | Body text, headings. Deep warm near-black. |
| Secondary Text | Stone Grey | `#7A756D` | Captions, timestamps, secondary labels. |
| Kintsugi Gold | Urushi Gold | `#C4993C` | Focus rings, progress indicators, active borders. Very limited use. |
| Accent | Indigo Ink | `#3D4F7C` | Links, interactive elements, badges. |
| Border | Tategami | `#DDD7CC` | Dividers, card borders. Faint grid lines evoking ledger paper. |
| Selection | Pale Gold | `#F0E4C8` | Text selection, search highlights. |

### Typography
- **Display:** Shippori Mincho (Google Fonts) — elegant Japanese-friendly serif, works beautifully with Latin text
- **Body:** Noto Sans JP / Noto Sans (weight 400) — CJK-optimized, clean, high readability for mixed Latin/Japanese
- **Mono:** IBM Plex Mono — clean numerals, good at small sizes

### Visual Style
- **Paper Fiber:** Very subtle `feTurbulence` overlay (`baseFrequency="1.2"`, 1 octave, `type="fractalNoise"`) at 1.5% opacity. Suggests handmade paper fiber without being visible.
- **Gold Crack Lines:** Kintsugi gold appears as 1–2px lines for dividers, progress bars, and focus indicators. Think of gold filling the cracks — it marks boundaries and healing, not decoration.
- **Ledger Grid:** Optional faint horizontal ruled lines (border-bottom on rows, `#DDD7CC` at 30%) evoke traditional Japanese account books. Especially effective in tables.
- **Negative Space:** Extremely generous padding and margins. This theme breathes. Content-to-whitespace ratio should be 40:60 or lower.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-quint) — gentle deceleration, like ink absorbing into paper.
- **Timing:** Slow to medium. Content reveals 400–600ms. UI interactions 200–300ms. Nothing hurried.
- **Motion Character:** Ink spreading, not objects moving. Opacity and color shifts over position changes.
- **Physics:** None. This is contemplative — elements appear, they don't bounce or spring.

### Signature Animations
1. **Ink Spread Reveal** — Content blocks appear via opacity 0→1 with a subtle vertical clip-path reveal (bottom-to-top, like ink wicking upward). 500ms.
2. **Gold Thread** — Progress bars fill with a thin gold line that has a subtle brightness shimmer (CSS `background: linear-gradient` shifting via `background-position`). 1s for full bar.
3. **Paper Settle** — Modals and cards enter with 3px downward drift + fade, settling softly. 400ms ease-out-quint.
4. **Contemplative Fade** — View transitions use long crossfades (600ms) with no spatial movement. Content dissolves, not slides.
5. **Ledger Line Draw** — Table borders draw themselves with `stroke-dashoffset` animation, left-to-right, on scroll-reveal. 300ms per row.

### UI Components
- **Buttons:** Primary: indigo fill, rice-white text, `border-radius: 6px`. Secondary: 1px tategami border, sumi text. Hover: lighten indigo 8%. Active: `scale(0.98)`. Generous padding (12px 24px).
- **Sliders:** Track is 1px tategami line. Thumb is 10px gold circle with 1.5px sumi border. Value in IBM Plex Mono italic.
- **Cards:** Rice white background, no border by default. `border-radius: 8px`. Shadow: `0 1px 4px rgba(28,27,24,0.04)`. Padding 24px. Selected cards get a 1px gold bottom-border.
- **Tooltips:** Sumi ink background, washi paper text. Noto Sans 12px. `border-radius: 4px`.
- **Dividers:** Gold at 40% opacity, 1px. Or generous whitespace (48–64px).

### Dark Mode Variant

Kintsugi Ledger has a full dark mode — not an afterthought, a first-class variant. Black urushi lacquerware: gold repairs glow against total darkness. The cracks are the feature.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F5F0E8` Washi Paper | `#0C0B08` lacquer black | Intentionally near-black — authentic to urushi lacquer |
| Card / surface | `#FAF8F3` Rice White | `#141310` dark lacquer | Elevated surfaces barely lift — contemplative, minimal |
| Border | `#DDD7CC` Tategami | `#28251E` gold-dusted edge | Warm dark border, hint of gold in the undertone |
| Border heavy | `#DDD7CC` at full | `#332F26` aged lacquer edge | Section dividers, table rules |
| Primary text | `#1C1B18` Sumi Ink | `#F5F0E8` at 85% washi paper glow | Lower opacity (85% not 87%) for contemplative feel. APCA Lc ~80 on `#141310` |
| Secondary text | `#7A756D` Stone Grey | `#A09A8E` warm stone | Captions, timestamps — quiet secondary |
| Dim text | `#7A756D` at lower opacity | `#6A655C` aged paper grey | Tertiary labels — whispered, not silent |
| Selection highlight | `#F0E4C8` Pale Gold | `#2A2518` dark gold | Text selection inverts to dark warm gold highlight |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Kintsugi Gold | `#C4993C` | `#D4AA50` brightened | Gold SHINES on black lacquer — this is the whole point of kintsugi |
| Indigo Ink | `#3D4F7C` | `#5A70A0` brightened | Interactive elements need visibility lift on dark |
| Tategami borders | `#DDD7CC` | `#28251E` inverted | Border role preserved, luminance inverted |

#### Shadow & Depth Adaptation
- Light: `0 1px 4px rgba(28,27,24,0.04)` — barely-there warmth, contemplative
- Dark: Shadow becomes `0 1px 4px rgba(0,0,0,0.4)` — deeper on lacquer. Selected cards: gold bottom-border increases from 1px to 1.5px, adds `box-shadow: 0 2px 8px rgba(212,170,80,0.08)` gold glow

#### Texture & Grain Adaptation
- Light: `feTurbulence` paper fiber at 1.5% opacity — barely visible handmade paper texture
- Dark: Paper fiber drops to 1% opacity, blend shifts to `soft-light`. The lacquer surface is smoother than paper — texture becomes more subtle, not absent. Gold crack dividers become MORE prominent: increase `border-width` from 1px to 1.5px, add `box-shadow: 0 0 4px rgba(212,170,80,0.10)` glow on gold lines

#### Dark Mode Rules
- Gold crack dividers are MORE prominent on dark — kintsugi gold is revealed by darkness, not hidden by it
- Ledger grid lines shift from `#DDD7CC` at 30% to `#28251E` at 40% — maintain the ruled-paper structure
- Negative space rule intensifies: 40:60 content-to-whitespace ratio on light becomes 35:65 on dark. More emptiness, more contemplation
- Contemplative fade view transitions: lengthen from 600ms to 800ms on dark mode — slower, more meditative
- "Black urushi lacquerware — gold repairs glow against total darkness. The cracks are the feature"

### Mobile Notes
- Remove paper fiber feTurbulence (performance).
- Maintain generous whitespace — it's the identity, not waste.
- Touch targets: 48px minimum. The contemplative pace extends to generous tap areas.
