## 16. Ionized Parchment

> High-end longform publication that doubles as an app — editorial clarity on warm "paper" surfaces with precise ink-like accents.

**Best for:** Research tools, reading-heavy dashboards, knowledge bases, documentation, writing apps, note-taking interfaces.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Warm Ivory | `#F8F4EC` | Primary canvas. Warm paper feel without yellowing. |
| Alt Background | Bleached Linen | `#F0EBE0` | Cards, sidebars, secondary surfaces. |
| Primary Ink | Deep Navy Ink | `#1B2838` | Body text, primary headings. Never pure black. |
| Secondary Ink | Graphite | `#4A5568` | Secondary text, captions, metadata. |
| Accent 1 | Oxidized Copper | `#B87345` | Links, highlights, active states. Warm and restrained. |
| Accent 2 | Slate Blue | `#5A7A96` | Secondary interactive elements, tags, badges. |
| Border | Warm Sand | `#DDD5C8` | Dividers, card borders, input outlines. |
| Text Highlight | Pale Goldenrod | `#F5E6C8` | Text selection, search highlights. |

### Typography
- **Display:** Newsreader (Google Fonts, variable) — bookish serif with optical sizing, excellent for long-form headings
- **Body:** Source Serif 4 (variable) — high readability text serif, generous x-height
- **Mono:** JetBrains Mono — for code blocks, data, and inline references

### Visual Style
- **Paper Grain:** Static SVG `feTurbulence` overlay (`baseFrequency="0.8"`, 1 octave) at 2% opacity with `mix-blend-mode: overlay`. Barely perceptible — felt, not seen.
- **Letterpress Depth:** Headings use a very subtle `text-shadow: 0 1px 0 rgba(0,0,0,0.04)` to simulate ink impression. No dramatic embossing.
- **Ink-Clean Rendering:** All text renders crisp. No blur, no glow. Typography carries the entire visual identity.
- **Hierarchy Through Weight:** No color decoration for hierarchy. Use font-size scale, weight variation, and spacing to establish reading order.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.25, 0.1, 0.25, 1)` — standard ease, nothing theatrical.
- **Timing:** Fast for interactions (150–250ms), medium for view transitions (300–500ms). Readers don't want to wait.
- **Motion Character:** Invisible. Motion serves navigation continuity (where did that panel go?) not decoration.
- **Physics:** None. This is editorial — precise, not playful.

### Signature Animations
1. **Page Turn** — View Transitions use a subtle crossfade with 10px horizontal offset, evoking page turns without literal skeuomorphism.
2. **Ink Fade-In** — New content blocks fade from 0 to full opacity over 300ms with 5px upward drift. Staggered at 50ms per element.
3. **Margin Slide** — Sidebar/annotation panels slide from the margin edge (left or right) at 250ms with ease-out.
4. **Reading Progress** — A 2px copper-colored progress bar at the top of the viewport, width driven by scroll position. `transform: scaleX()` for performance.
5. **Focus Glow** — Interactive elements get a 2px `box-shadow` in pale copper (`rgba(184,115,69,0.3)`) on focus. Transitions in at 150ms.

### UI Components
- **Buttons:** Copper text on transparent, 1px copper border. `border-radius: 3px`. Hover: fill fades to 5% copper. Active: `scale(0.98)`. Text in Source Serif 4 italic.
- **Sliders:** Track is a 1px warm-sand line. Thumb is copper circle (12px). Value label in JetBrains Mono, right-aligned.
- **Cards:** Bleached linen background, 1px warm-sand border. `border-radius: 4px`. Padding 24px. No shadow — the border provides separation.
- **Tooltips:** Deep navy background, warm ivory text. Small Source Serif body. 3px radius.
- **Dividers:** Warm sand at 50% opacity. 1px. Or generous whitespace (40–56px gap).

### Dark Mode Variant

Ionized Parchment has a full dark mode — not an afterthought, a first-class variant. A first-edition reading room at midnight: leather-bound volumes by a single reading lamp.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F8F4EC` Warm Ivory | `#110F0C` deep espresso | Near-black with warm brown undertone — leather and wood |
| Card / surface | `#F0EBE0` Bleached Linen | `#1A1714` aged leather | Elevated surfaces lighter, like lamplight catching a book spine |
| Border | `#DDD5C8` Warm Sand | `#2D2820` dark stitching | Warm mid-tone borders, like bookbinding thread |
| Border heavy | `#DDD5C8` at full | `#3A342B` leather edge | Section dividers, input focus |
| Primary text | `#1B2838` Deep Navy Ink | `#E8DCC8` at 87% ivory glow | APCA Lc ~81 on `#1A1714` — warm parchment light |
| Secondary text | `#4A5568` Graphite | `#B8AC98` at 68% sand | Captions, metadata — warm and readable |
| Dim text | n/a | `#7A7060` aged parchment grey | Timestamps, tertiary info — quiet warmth |
| Navy ink role | `#1B2838` text color | `#2D2820` border/structure | Navy was text on light; becomes structure on dark. Text inverts to warm ivory |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Oxidized Copper | `#B87345` | `#D4935A` brightened | Copper catches lamplight — warmer, more luminous |
| Slate Blue | `#5A7A96` | `#7A9AB0` brightened | Cool accent needs lift to read on dark leather |
| Pale Goldenrod highlight | `#F5E6C8` | `#3A3020` warm dark highlight | Text selection inverts — dark gold highlight on dark ground |

#### Shadow & Depth Adaptation
- Light: No shadow — `1px warm-sand border` provides separation. Clean editorial approach
- Dark: Maintain borderless editorial feel. Cards differentiate via background (`#1A1714` on `#110F0C`). Reading progress bar copper glow: `box-shadow: 0 0 4px rgba(212,147,90,0.15)` — subtle lamplight

#### Texture & Grain Adaptation
- Light: Static SVG `feTurbulence` at 2% opacity, `overlay` blend. Letterpress `text-shadow: 0 1px 0 rgba(0,0,0,0.04)` on headings
- Dark: Paper grain drops to 1.5% opacity, blend shifts to `soft-light`. Letterpress text-shadow inverts: `text-shadow: 0 1px 0 rgba(232,220,200,0.03)` — subtle light inset from below, as if type is pressed into dark leather. Grain must remain — the surface is still paper/leather, not glass

#### Dark Mode Rules
- Typography still carries the entire visual identity — no decorative additions in dark mode
- Hierarchy through weight, size, and spacing preserved exactly. Color hierarchy simply inverts
- Navy ink `#1B2838` shifts from text role to structural/border role — it's too dark for text on dark
- Copper reading progress bar becomes more prominent: the warm line is a beacon in the dark room
- "First-edition reading room at midnight. Leather and lamp-glow"

### Mobile Notes
- Remove paper grain feTurbulence entirely (performance).
- Reading progress bar remains — it's lightweight (`scaleX` transform).
- Touch targets on copper controls: minimum 44px with 8px padding.
