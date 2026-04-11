## 5. Gouache & Clay

> Matte acrylic paint, hand-cut paper, modern editorial illustration — zero digital gloss.

**Best for:** Voronoi diagrams, Delaunay triangulation, terrain generation, map visualizations, geometric patterns.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background A | Earthy Terracotta | `#E07A5F` | Strong, warm canvas option. |
| Background B | Muted Sage | `#81B29A` | Cool, natural canvas option. |
| Primary | Eggshell White | `#F4F1DE` | Light elements, fills, foreground shapes. |
| Secondary | Deep Blue-Black | `#3D405B` | Dark elements, outlines, contrast fills. |
| Accent | Vibrant Ochre | `#F2CC8F` | Highlights, interactive states, key data. |
| Shadow | Burnt Umber | `#5C4033` | Hard drop shadows (offset, no blur). |
| Text | Blue-Black | `#3D405B` | Same as secondary — cohesive, flat palette. |
| Border | Darkened BG | varies | 15% darker than current background. |

### Typography
- **Display:** Bricolage Grotesque — creative, editorial quirk, woodblock-print energy
- **Body:** Figtree — warm, crisp, friendly
- **Mono:** Fira Code — craft-meets-code feel

### Visual Style
- **Zero Gloss:** Absolutely no glow, bloom, shine, or gradient sheen. Every surface is matte. "Dry paint on canvas" energy.
- **Rough Edges:** Slightly roughen geometric shape edges. Techniques: apply 1px jitter to polygon vertices via noise, or use SVG `feTurbulence` displacement at very low intensity to break mathematical perfection.
- **Hard Drop Shadows:** Every elevated element gets a hard, directional shadow — offset 4px right + 4px down, solid color (burnt umber or 20% opacity black), NO blur. This creates a "stacked paper" 2.5D effect.
- **Flat Color:** No gradients within shapes. Solid fills only. Color variation comes from juxtaposition, not blending.

### Animation Philosophy
- **Easing:** Snappy `cubic-bezier(0.34, 1.56, 0.64, 1)` — a slight overshoot that feels handmade, like paper snapping into place.
- **Timing:** Quick entries (200-300ms), deliberate exits (400ms). The "paper placing" feel should be decisive.
- **Motion Character:** Physical, crafty. Elements feel like they have weight and are being placed by hand. Paper-like.
- **Physics:** No physics simulation on UI. Elements don't bounce or spring — they place and stick.

### Signature Animations
1. **Paper Stack** — Elements enter by sliding in from off-screen with their hard shadow, as if being placed on a stack of paper. Shadow appears simultaneously.
2. **Cut-Out Flip** — Cards transition between states with a Y-axis 3D rotation (paper flipping over), revealing a different color on the "back."
3. **Stamp Press** — Interactive elements respond to click with `scale(0.95)` + shadow reduces to 2px offset, like pressing a rubber stamp onto paper.
4. **Fold Collapse** — Panels collapse by rotating on their top edge (perspective + rotateX), folding down like paper.
5. **Color Swap** — On state change, background color crossfades between terracotta ↔ sage over 800ms, like paint being washed over.

### UI Components
- **Buttons:** Blue-black fill, eggshell text. Hard shadow (4px offset burnt umber). `border-radius: 4px`. Hover: ochre fill. Active: shadow reduces to 2px.
- **Sliders:** Track is a thick line (4px) in blue-black. Thumb is an ochre square (not circle!) 16px. Hard shadow on thumb.
- **Cards:** Eggshell fill, blue-black 2px border. Hard shadow (4px offset). `border-radius: 4px`. Feels like a die-cut card.
- **Tooltips:** Ochre background, blue-black text. Hard shadow. Feels like a sticky note.
- **Dividers:** Thick (3px) blue-black lines. Or torn-edge SVG path for organic feel.

### Dark Mode Variant

Gouache & Clay has a full dark mode — not an afterthought, a first-class variant. Paper craft under a warm desk lamp. The matte quality is sacred.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | n/a (colored canvases) | `#100E0A` dark card stock | Warm near-black — NOT cool. Craft paper in a dim room |
| Card / surface (terracotta) | `#E07A5F` Earthy Terracotta | `#2C2420` deep clay | Terracotta identity preserved as dark warm brown |
| Card / surface (sage) | `#81B29A` Muted Sage | `#1A2E26` dark sage | Sage identity preserved as deep green-dark |
| Border | varies (15% darker than bg) | `#3A3430` warm dark edge | 15% lighter than dark bg — inversion rule |
| Primary text | `#3D405B` Blue-Black | `#F4F1DE` eggshell stays | Eggshell is the signature white — never swap it out |
| Secondary text | `#3D405B` at lower weight | `#C8C4B0` warm cream | Softer secondary on dark ground |
| Dim text | n/a | `#8A8676` warm khaki | Metadata, labels — matte and quiet |
| Shadow color | `#5C4033` Burnt Umber | `rgba(244,241,222,0.08)` cream glow | Inverted: dark shadows → light outlines |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Eggshell White | `#F4F1DE` primary fill | `#F4F1DE` stays as text | Signature color — role shifts from fill to text |
| Deep Blue-Black | `#3D405B` text/outlines | `#6B6E80` lighter mid-tone | Was dark on light; needs lightening for visibility |
| Vibrant Ochre | `#F2CC8F` highlights | `#F2CC8F` stays | Warm mid-lightness — works on both grounds |
| Burnt Umber | `#5C4033` shadows | `#4A4035` darkened further | Shadow role replaced by outlines; umber becomes subtle structure |

#### Shadow & Depth Adaptation
- Light: Hard drop shadows — 4px right + 4px down, solid burnt umber, NO blur. Stacked paper 2.5D
- Dark: Shadows invisible on dark ground. Replace with light-colored hard outlines: `3px 3px 0 rgba(244,241,222,0.08)` (cream glow). Same offset geometry, inverted luminance. The "stacked paper" feel becomes "cut paper on dark table"

#### Texture & Grain Adaptation
- Light: SVG `feTurbulence` displacement at low intensity for rough edges. Flat matte fills
- Dark: Rough edge displacement preserved — structure, not decoration. Matte finish absolutely preserved: no glossy dark mode trap. Zero bloom, zero glow beyond the hard-outline shadows. Flat fills remain flat — NO gradients sneak in during dark mode

#### Dark Mode Rules
- Two-canvas system preserved: terracotta cards (`#2C2420`) and sage cards (`#1A2E26`) on dark page (`#100E0A`)
- Hard shadow → hard outline is the critical inversion. Same 4px offset, different luminance direction
- Eggshell `#F4F1DE` is the anchor — it's text in dark mode, fill in light mode. Never replace it
- Zero gloss rule intensifies: dark mode tempts designers toward shiny surfaces. Resist absolutely
- "Paper craft under a warm desk lamp. The matte quality is sacred"

### Mobile Notes
- Hard shadows are cheap — this theme is inherently mobile-friendly.
- Rough edge displacement can be pre-baked (static SVG) instead of per-frame noise.
- Flat colors with no blend modes = excellent Canvas2D performance.
- This is one of the most performant themes. Use it when targeting low-end devices.
