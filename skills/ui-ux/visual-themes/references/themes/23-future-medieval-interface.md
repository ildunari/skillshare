## 23. Future Medieval Interface

> Arcane-modern: illuminated manuscript logic with modern UI constraints. Ornament frames hierarchy, not everything.

**Best for:** Games, narrative experiences, interactive fiction, art pieces, RPG character sheets, fantasy-themed tools.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Dark Vellum | `#1E1812` | Primary canvas. Deep parchment darkness. |
| Alt Background | Manuscript | `#2A231A` | Cards, panels, elevated surfaces. |
| Primary Text | Bone White | `#E8DCC8` | Body text. Warm off-white, like aged vellum. |
| Secondary Text | Faded Ink | `#9A8E7C` | Captions, secondary labels. |
| Accent 1 | Gilded Gold | `#C5973E` | Headings, interactive accents, progress. Illuminated letter energy. |
| Accent 2 | Oxblood | `#8C3030` | Highlights, alerts, emphasis. Deep, not bright. |
| Accent 3 | Verdigris | `#4A7A6A` | Links, secondary interactive states, success. |
| Border | Blackletter Rule | `#3A3228` | Dividers, card borders. Barely visible on dark. |

### Typography
- **Display:** Cinzel Decorative (700 weight, sparingly) — blackletter-adjacent, ceremonial. Use only for hero headings/titles.
- **Body:** Crimson Pro (400 weight) — highly legible text serif. The workhorse. Never use Cinzel for body.
- **Mono:** Fira Code — pragmatic, contrasts well with the ornate display face

### Visual Style
- **Vellum Grain:** Static noise overlay at 4% opacity on `::after`. Warmer and grainier than standard paper grain. `feTurbulence` `baseFrequency="0.7"`, 2 octaves.
- **Illuminated Borders:** Card and section borders use a thin gold line (1px `#C5973E` at 30%) with slightly brighter corners — like gold leaf catching light at page edges.
- **Ink Bleed:** Text has a very subtle `text-shadow: 0 0 1px rgba(197,151,62,0.15)` at display sizes. Not readable as glow — reads as ink spreading into vellum.
- **Ornament as Punctuation:** Decorative elements (SVG flourishes, section markers like ❧ or ✦) appear ONLY at section breaks and page boundaries. Never inline, never cluttering content.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.25, 0.1, 0.25, 1)` — stately ease. Nothing fast, nothing bouncy.
- **Timing:** Slow. Content reveals 500–700ms. UI interactions 250–350ms. Ceremonial pace.
- **Motion Character:** Ceremonial and reverent. Elements are unveiled, not thrown. Think of turning a heavy manuscript page.
- **Physics:** None. Gravity doesn't exist here — this is ritual, not physics.

### Signature Animations
1. **Illumination Reveal** — Headings fade in with gold color spreading from the first letter outward (CSS `background-clip: text` with animated gradient position). 600ms.
2. **Manuscript Unfurl** — Modals and panels enter with a vertical `clip-path` reveal (top-to-bottom) paired with 3% opacity increase. Like unrolling a scroll. 500ms.
3. **Gold Glint** — On hover over gilded elements, a specular highlight sweeps left-to-right (linear-gradient with white at 8% opacity, animated `background-position`). 300ms.
4. **Candle Flicker** — Ambient: gold accent elements very subtly oscillate brightness (±3% L) at irregular intervals (2–4s, random timing). Like candlelight. Disabled on reduced motion.
5. **Ink Settle** — New text content appears with opacity 0→1 and a 1px vertical drift, like ink settling into the page surface. 400ms.

### UI Components
- **Buttons:** Primary: gold text on manuscript bg, 1px gold border, `border-radius: 2px`. Secondary: verdigris text, 1px verdigris border. Hover: fill 5% gold/verdigris. Active: border brightens. Text in Crimson Pro 500.
- **Sliders:** Track is 1px gold line at 40% opacity. Thumb is 12px gold circle with 1px manuscript-colored border. Value in Fira Code.
- **Cards:** Manuscript background, 1px blackletter-rule border with gold corners (CSS border-image or pseudo-elements). `border-radius: 2px`. Padding 24px.
- **Tooltips:** Dark vellum background, bone-white text. Crimson Pro 13px. `border-radius: 2px`. Thin gold top-border.
- **Dividers:** Gold at 20% opacity. 1px. Or a centered flourish character (✦ or ❧) in faded ink color.

### Light Mode Variant

Future Medieval Interface has a full light mode — not an afterthought, a first-class variant. In fact, this IS the historical original. Illuminated manuscripts were light — golden ink on pale vellum, painted in daylight. The dark mode was the modern adaptation. Light mode is restoration.

#### Structural Color Map

| Role | Dark (native) | Light (variant) | Notes |
|---|---|---|---|
| Page background | `#1E1812` dark vellum | `#F0E8D8` aged vellum | oklch(0.93 0.02 80) — warm, yellow-ish parchment |
| Card / surface | `#2A231A` manuscript | `#FAF4EA` clean parchment | oklch(0.97 0.01 80) — fresh vellum, slightly brighter |
| Border | `#3A3228` blackletter rule | `#D0C4B0` binding thread | oklch(0.80 0.02 75) — visible but soft, like linen thread |
| Border heavy | — | `#B8AA94` aged binding | Heavier section dividers |
| Primary text | `#E8DCC8` bone white | `#2A2018` manuscript ink | oklch(0.18 0.02 60) — warm near-black, hand-lettered feel |
| Secondary text | `#9A8E7C` faded ink | `#6A5E4C` aged ink | Darker for legibility on vellum background |
| Dim text | — | `#8A8070` worn vellum | Labels, margin notes, scribal annotations |
| Vellum grain | 4% warm noise | 3% warm noise | Slightly reduced — parchment texture persists in light |

#### Accent Shifts

| Element | Dark (native) | Light (variant) | Reason |
|---|---|---|---|
| Gilded Gold | `#C5973E` | `#A07830` | oklch(0.55 0.10 75) — aged illumination, not gleaming. APCA Lc ~58 on vellum |
| Oxblood | `#8C3030` | `#6A2020` | oklch(0.32 0.12 25) — dried ink, deeper for contrast on light parchment |
| Verdigris | `#4A7A6A` | `#3A6050` | oklch(0.42 0.06 165) — patinated copper, darkened for legibility |

#### Shadow & Depth Adaptation

- **Dark:** No explicit shadows. Depth via luminance stepping (dark vellum → manuscript → border). Gold corners and `text-shadow` ink-bleed at display sizes.
- **Light:** Cards: `box-shadow: 0 1px 3px rgba(42,32,24,0.06)` — warm, like parchment lifting slightly from the desk. Gold corners are MORE visible on light (gold on vellum is the historical rendering). Ink-bleed `text-shadow` at display sizes shifts to `0 0 1px rgba(42,32,24,0.12)` — dark ink spreading into pale vellum.

#### Texture & Grain Adaptation

- **Dark:** Vellum grain at 4% opacity, warm `feTurbulence`. Ink bleed on display text. Decorative flourishes in faded ink.
- **Light:** Vellum grain reduces to 3% opacity with `multiply` blend — reads as actual parchment fiber, more authentic on light than dark. Ink bleed slightly increased on headings (ink spreads more visibly on pale surfaces). Gold illuminated borders become MORE prominent — this is their natural habitat. Manuscripts WERE illuminated in gold on pale vellum.

#### Light Mode Rules

1. **Gold illuminated borders amplify.** On dark, gold borders are subtle glints. On light vellum, they become the defining visual feature — exactly as they were in historical manuscripts. Increase gold border opacity from 30% to 50%.
2. **This is the historical original.** Illuminated manuscripts were always light. Gold leaf on pale vellum, painted in monastery daylight. The dark mode was the screen-first adaptation. Light mode is not a variant — it's a restoration.
3. **Ornament flourishes gain presence.** SVG flourishes and section markers (flourish, ✦) shift from faded ink (`#9A8E7C`) to manuscript ink (`#6A5E4C`). They read like actual hand-drawn decorations on parchment.
4. **Warm yellowed white, not cold white.** The page is `#F0E8D8` — aged vellum with a yellow cast. Cards are `#FAF4EA` — slightly cleaner parchment. Never `#FFFFFF`. The warmth is the material.
5. "This IS the historical original — manuscripts were light. The dark mode was the adaptation. Light mode is restoration."

### Mobile Notes
- Disable candle flicker ambient animation (performance + battery).
- Reduce vellum grain to 1 octave feTurbulence.
- Cinzel Decorative only on primary headings — use Crimson Pro for all other levels (font loading weight).
- Touch targets: 44px minimum with 8px padding.
