## 31. Gazette Pixel

> Broadsheet newspaper set in dark concrete with pixel-art instrumentation — editorial authority meets 8-bit telemetry. Every element earns its ink.

**Best for:** Mission control dashboards, multi-agent monitors, DevOps status walls, CI/CD pipelines, system health panels, real-time telemetry, chat-ops interfaces, terminal-adjacent UIs, any artifact showing multiple concurrent processes or agents.

---

### Identity & Philosophy

Gazette Pixel is the collision of two visual traditions that shouldn't work together but do: the broadsheet newspaper — with its columnar KPIs, masthead hierarchy, and ink-on-paper authority — and the pixel grid — with its LED-matrix status blocks, mosaic status bars, and discrete quantized data. Both traditions share an obsession with information density, structural honesty, and zero decoration.

The theme is natively dark. Not "dark mode" — this IS the mode. It lives on warm charcoal, not cool blue-black. The warmth matters: this is a newsroom at 2 AM, not a spaceship. Copper light, not fluorescent.

**Core tension:** Editorial elegance vs. raw pixel quantization. The typography is refined (Space Grotesk at 800 weight, tight tracking, uppercase mastheads). The data is deliberately crude (3px pixel blocks, mosaic bars, LED grids). This contrast is the identity. If everything is refined, it's just a dark dashboard. If everything is pixelated, it's retro kitsch. The magic is the gap between them.

**Decision principle:** When in doubt, ask "would a night editor at a broadsheet approve this?" If it's decorative, cut it. If it communicates, keep it. Every pixel of ink costs money.

---

### Color Palette

Built on the Anthropic dark warmth family. No cool greys, no blue-blacks, no true blacks. Everything has a warm undertone — stone, charcoal, clay, not steel.

| Role | Color | Hex | OKLCH (approx) | Usage |
|---|---|---|---|---|
| Background | Warm Charcoal | `#1C1917` | L=0.15 C=0.01 h=60 | Primary canvas. The newsprint stock — dark, warm, papery. |
| Surface | Dark Stone | `#292524` | L=0.20 C=0.01 h=50 | Cards, panels, elevated surfaces. Slightly lighter than bg. |
| Border | Ash Rule | `#3a3530` | L=0.26 C=0.01 h=45 | All structural borders, dividers, grid lines, column rules. |
| Primary Text | Warm Cream | `#E7E1D9` | L=0.91 C=0.01 h=70 | Body text, headlines, KPI values. The "ink" color. |
| Focus Text | Coral Parchment | `#F0C4AB` | L=0.83 C=0.06 h=55 | Focus descriptions, active task text, highlighted prose. Warmer than cream. |
| Dim Text | Worn Ink | `#6B6560` | L=0.45 C=0.01 h=50 | Labels, timestamps, secondary info, unit markers. |
| Accent: Sienna | Anthropic Sienna | `#C15F3C` | L=0.55 C=0.13 h=40 | Primary accent. Healthy status, active agent, pixel icon fill, progress blocks. |
| Accent Dim | Deep Sienna | `#6a3020` | L=0.32 C=0.08 h=35 | Dimmed/inactive version of sienna. Unfilled step blocks, inactive mosaic cells. |
| Error | Signal Red | `#c4453a` | L=0.50 C=0.14 h=25 | Errors, failures, alarm states. Replaces sienna accent when status=red. |
| Warning | Muted Amber | `#a08030` | L=0.58 C=0.10 h=80 | Slow/degraded states. Replaces sienna when status=yellow. |
| Canvas | Deep Background | `#141210` | L=0.10 C=0.01 h=55 | Page-level background behind all cards. The "press room" darkness. |

**Color rules:**
1. **Status overrides accent.** The agent accent color is used for healthy state. When an agent enters warning or error, ALL accent-colored elements swap to amber or red respectively — icon, mosaic bar, status grid, step blocks, KPI highlight, phase label. This is a full-card semantic shift, not a badge.
2. **Per-agent accent variation.** In multi-agent layouts, each agent type gets its own accent hue while maintaining the same lightness/chroma relationship. See Agent Accent System below.
3. **No gradients.** Flat fills only. Newspaper ink doesn't gradient. Pixel blocks don't gradient. The only "gradient" is the luminance step between bg → surface → border (3 discrete levels).
4. **Red is earned.** Signal red appears ONLY for genuine errors. Never decorative, never "just for contrast." If nothing is broken, zero red pixels on screen.

#### Agent Accent System

When multiple agents share the screen, each role gets a unique accent color. All accents maintain OKLCH L≈0.50–0.58, C≈0.08–0.14 — they're equally prominent, equally muted, equally "inky."

| Agent Role | Accent | Hex | Character |
|---|---|---|---|
| Coder | Forest Teal | `#6B8A8B` | Cool, technical, stable |
| Researcher | Warm Clay | `#A0522D` | Earthy, methodical, digging |
| Assistant | Anthropic Sienna | `#C15F3C` | Primary, communicative |
| Monitor | Slate Blue | `#7088A0` | Vigilant, cool, observant |
| Deployer | Burnt Orange | `#C1783C` | Active, pushing, shipping |
| Reviewer | Muted Gold | `#B89848` | Evaluative, judicial |
| Scheduler | Sage Green | `#7A9A6A` | Methodical, timed, natural |
| Debugger | Copper | `#B87333` | Diagnostic, warm, focused |

Each accent has a corresponding `accentDim` at roughly half lightness for inactive/unfilled states (step block backgrounds, unlit mosaic cells).

---

### Typography

Two families. No exceptions. The theme's typographic identity is the contrast between a geometric grotesque at heavy weights (the "headline") and a monospace at regular weight (the "data").

- **Display/Headlines:** Space Grotesk 800 — ALL CAPS, letter-spacing `0.06em–0.14em`. Used for: agent labels, phase names, masthead titles, column headers, status labels. The newspaper headline voice.
- **Body:** Space Grotesk 400 — Sentence case. Used for: focus descriptions, narrative text, longer labels. The article body voice.
- **Data/Mono:** JetBrains Mono 500–700 — Used for: KPI numbers, commands, file paths, evidence tags, timestamps, any machine-generated text. The teletype voice.

**Typography rules:**
1. **KPI numbers are always JetBrains Mono at 17–18px, weight 800.** They're the biggest numbers on the card. They command attention through size and weight, not color.
2. **Labels above KPIs are Space Grotesk 700 at 8–9px, ALL CAPS, letter-spacing 0.14em.** They're small, quiet, structural — like column headers in a financial table.
3. **Phase/status labels are Space Grotesk 800 at 13px, ALL CAPS, letter-spacing 0.06em, colored with agent accent.** The only colored text element.
4. **Commands and paths use JetBrains Mono at 10px, dim text color.** They're whispered, not shouted. Metadata, not data.
5. **Maximum three font sizes per card.** Small (8–10px labels/meta), medium (11–13px body/phase), large (17–18px KPI). No size between these. The jumps are deliberate.

#### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

---

### Visual Style

#### The Pixel Grid System

The defining visual element. All data visualization, status indicators, and progress tracking is rendered through discrete pixel blocks — small rectangles arranged in grids. Nothing is smooth, nothing is anti-aliased, nothing curves. Data is quantized.

**Pixel Block specifications:**
- Individual blocks: 3–8px wide, 3–4px tall, gap 1px
- Colors: binary (accent color or border/dim color). No opacity variation, no intermediate shades.
- Rendering: Pure CSS `div` elements. No canvas, no SVG, no images. Each block is a real DOM element with a real background color.

**Five pixel components:**

1. **Mosaic Status Bar (top of card):** 40 blocks across the full card width, each `flex: 1`, height 4px. A configurable fill function determines which blocks light up. The pattern varies per agent role:
   - Coder: left-stack (first 4 lit — "loading")
   - Monitor: dense fence (every 2nd — "heartbeat")  
   - Deployer: right-fill (progress indicator — fills toward completion)
   - Scheduler: regular tick (every 4th — "metronome")
   - Debugger: bookends (first 2 + last 2 — "brackets")
   - Error override: every 3rd (sparse alarm pulse)
   - Warning override: every 5th (occasional concern)

2. **3×3 Status Grid:** 9 blocks, 4×4px each, gap 1px. Positioned in the card header. Each agent role fills a different pattern:
   - Checkerboard, cross, frame, full, triangle, diagonal, corners, diamond
   - Colors swap to error red or warning amber on status change

3. **Pixel Bar Chart:** 10 columns × 6 rows grid of small blocks (6–8px wide × 3px tall, gap 1px). Columns fill from bottom based on data values. This replaces smooth bar charts. The quantization IS the visualization — you can count exact rows.

4. **Step Blocks:** Square progress indicators (10–12px, gap 3px). Filled blocks = completed steps, unfilled = remaining. 1px border on unfilled blocks at 20% accent opacity. No rounded corners, no circles — squares only.

5. **Pixel Icons (agent identity):** 7×7 grids of 3px blocks with 1px gaps. Each agent role has a unique icon: angle brackets (coder), magnifying glass (researcher), chat bubble (assistant), eye (monitor), up-arrow (deployer), checkmark (reviewer), clock (scheduler), crosshair (debugger). Icons are rendered in the agent's accent color.

#### Concrete Grain Texture

Inherited from Brutalist Concrete (#08) but subtler on dark backgrounds:
- SVG `feTurbulence`: `baseFrequency="0.8"`, `numOctaves="2"`, `type="fractal"`
- Composited at 2–3% opacity via `feComposite` with `soft-light` blend
- Applied as a full-card overlay (or page-level if performance allows)
- On dark surfaces this reads as warm stone grain, not digital noise
- **Optional.** Cards work without it. Remove on mobile or when rendering >8 cards.

#### Structural Borders

- Card border: 2px solid `#3a3530` (ash rule)
- Internal dividers: 1px solid `#3a3530`
- KPI column dividers: 1px solid `#3a3530`
- Focus text left-border: 3px solid accent at 27% opacity (`accent + "44"`)
- **No shadows.** No `box-shadow`, no `drop-shadow`, no elevation. Borders ARE the elevation system. A 2px border means "this is a card." A 1px border means "this is a section within a card."
- **No rounded corners.** `border-radius: 0` everywhere. Non-negotiable. This extends to buttons, inputs, tooltips, modals — everything.

#### Card Anatomy (top to bottom)

```
┌─────────────────────────────────────────────┐
│ ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │  ← Mosaic status bar (40 blocks, 4px tall)
├─────────────────────────────────────────────┤
│ [PIX]  AGENT NAME          [▪▪▪] OK        │  ← Header: pixel icon + name + 3×3 grid + status
│        channel/target                       │
├─────────────────────────────────────────────┤
│ PHASE LABEL                                 │  ← Phase in accent color, ALL CAPS
│ ■■□□□□□□□□                                  │  ← Step blocks (if applicable)
│ ▎ Focus description text in coral           │  ← Left-bordered focus text
│                                             │
│  EVT/M  │   ERR   │   AGE                  │  ← KPI columns (newspaper layout)
│   8.2   │    0    │   12s                   │
│                                             │
│ ▪▪▪▪▪▪▪▪▪▪                                 │  ← Pixel bar chart (10×6 grid)
│ ▪▪▪▪▪▪▪▪▪▪                                 │
│                                             │
│ $ npm run build                   [exec]    │  ← Command + evidence tag
└─────────────────────────────────────────────┘
```

#### Newspaper Column KPI Layout

KPIs are displayed in equal-width columns separated by 1px vertical rules — exactly like a financial data table in a broadsheet. Each column contains:
- Top: label (8px, ALL CAPS, 0.14em tracking, dim text)
- Bottom: value (17px, weight 800, cream or red if error)
- Columns are `flex: 1` with `text-align: center`
- Separated by `borderRight: 1px solid border-color`
- The top border of the KPI section is 2px (heavier rule, like a table header separator)

---

### Animation Philosophy

**Easing:** `steps(n)` or `linear`. Never `ease-in-out`, never spring, never bounce. This is a printing press, not a physics sim.

**Timing:** Fast and utilitarian. 150–250ms for state changes. 800ms tick interval for live data updates.

**Motion character:** Mechanical, discrete, quantized. Things don't slide — they step. Values don't interpolate — they snap. Pixels don't fade — they appear. The pixel grid aesthetic extends to time: motion is sampled, not continuous.

**Physics model:** None. Rejected on principle. Newspaper pages don't bounce. LED matrices don't spring. Pixel blocks don't have inertia.

**Reduced motion:** Replace stagger with instant. Replace tick-based updates with static last-known-value. Replace entrance animation with `opacity: 1` (no transform). The theme is almost reduced-motion by default — there's very little to remove.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

### Signature Animations

1. **Staggered Entrance** — Cards appear with `translateY(6px) → 0` and `opacity: 0 → 1` over 250ms, staggered at 40–50ms per card. The only "smooth" animation in the theme. After this, everything is discrete. The entrance earns its smoothness by being the ONLY smooth moment.

2. **Tick-Based Data Refresh** — Every 800ms, a global tick increments. Pixel bars, KPI values, and status indicators update on the tick — not continuously. Values snap to their new state. You can see the moment of update. This is intentional: it communicates "this is live sampled data" rather than "this is a smooth interpolation."

3. **Mosaic Status Pulse** — On status change (green→yellow or green→red), the 40-block mosaic bar at the top of the card swaps its fill pattern in a single frame. No transition. The pattern itself communicates severity — sparse blocks for warning, dense blocks for alarm.

4. **Red Flash on Error** — When a KPI value enters error state, the number renders in signal red (`#c4453a`) on the next tick. No transition, no fade — instant color swap. The abruptness IS the alert.

5. **Focus Text Reveal** — The left-border on focus text (3px accent at 27% opacity) appears with the card entrance. If focus text changes during a session, the new text replaces the old instantly — no typing animation, no fade. Newspaper columns don't animate their text.

6. **Pixel Bar Growth** — On initial render, pixel bar columns fill from bottom up, one row per tick (800ms × 6 rows = ~5 seconds for full chart). After initial render, updates happen per-tick (individual cells appear/disappear). This is the only "building" animation — it echoes a dot-matrix printer filling a chart.

---

### UI Components

**Cards:** `background: #1C1917`, `border: 2px solid #3a3530`, `border-radius: 0`. Internal padding 12px. Min-width 300px. No shadow, no hover effect, no elevation change. Cards are panels on a page — they don't lift.

**Buttons (if needed):** Dark stone fill (`#292524`), cream text, 2px ash border, `border-radius: 0`, ALL CAPS Space Grotesk 600, 10px letter-spacing 0.1em. Hover: accent border color. Active: accent background, deep canvas text. No transitions on hover — instant swap.

**Inputs (if needed):** Dark stone fill, 1px ash border, cream text in JetBrains Mono. No placeholder animation. Focus: accent border (instant swap), no glow, no outline. Caret color: accent.

**Tooltips:** `#292524` fill, cream text, JetBrains Mono 10px. 2px ash border. Square corners. Positioned with 4px offset. No arrow/triangle — brutalist tooltips don't point.

**Badges/Tags:** Inline text in JetBrains Mono 10px, dim text color, wrapped in brackets: `[exec]`, `[gateway]`, `[ci_run]`. No background, no border, no pill shape. The brackets ARE the container.

**Dividers:** 1px ash (`#3a3530`) for section dividers. 2px ash for major section breaks (above KPI columns). Full-width within the card padding.

**Grid layout:** `display: grid`, `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`, gap 10px. Cards are not draggable, not resizable, not collapsible. The grid is the layout — it doesn't change.

---

### Compositing & Rendering

- **Blend modes:** None (or `soft-light` only for the optional grain texture). Flat compositing. Pixels are opaque.
- **Filters:** Only `feTurbulence` for grain. No blur, no drop-shadow, no saturate.
- **Opacity:** Used sparingly. Accent at 27% (`+ "44"` hex suffix) for focus text border. Grain at 2–3%. Otherwise, everything is fully opaque.
- **Z-index:** Flat. No stacking context tricks. Cards don't overlap. Tooltips are the only elevated element.
- **Anti-aliasing:** Irrelevant — pixel blocks are integer-sized rectangles. No sub-pixel rendering concerns. This is one of the theme's performance advantages.

---

### Data Visualization Guidance

This theme has a specific philosophy: **quantized over smooth, counted over interpolated.**

- **Bar charts → Pixel bar grids.** Never use smooth SVG/canvas bars. Use the pixel bar component (N columns × M rows of discrete blocks). The viewer counts lit blocks, not estimates height.
- **Line charts → Sparklines.** Thin SVG polyline (1–2px stroke) in accent color on transparent background. No fill, no dots, no axes. Just the signal. If precision matters, pair the sparkline with a numeric KPI.
- **Progress → Step blocks.** Never use a smooth progress bar. Use N square blocks where K are filled. The viewer counts completed steps.
- **Status → 3×3 pixel grid or mosaic bar.** Never use a colored circle/dot. Use a 3×3 grid of blocks in a meaningful pattern, or the 40-block mosaic bar with a role-specific fill pattern.
- **Gauges → Numeric KPI.** This theme does not use circular gauges, radial progress, or arc meters. If you need to show a percentage, show the number. "47%" in JetBrains Mono 800 at 17px communicates faster than any gauge.
- **Color encoding:** Max 2 hues per visualization (accent + error, or accent + warning). No rainbow palettes. No multi-hue categorical schemes. If you need to distinguish more than 2 categories, use pattern/shape variation on the pixel blocks, not color.

---

### Information Hierarchy

The theme enforces a strict 5-level hierarchy. Each level has exactly one visual treatment — no mixing.

| Level | Element | Treatment |
|---|---|---|
| 1 — Identity | Agent icon + name | Pixel icon in accent + Space Grotesk 800 14px CAPS |
| 2 — State | Phase label + status | Accent-colored text 13px CAPS + 3×3 pixel grid |
| 3 — Data | KPI values | JetBrains Mono 800 17px cream (or red if error) |
| 4 — Context | Focus text | Space Grotesk 400 11px coral, left-bordered |
| 5 — Meta | Commands, tags, timestamps | JetBrains Mono 400 10px dim + bracket notation |

**Rule:** Information flows top-to-bottom through these levels. The eye should hit identity → state → data → context → meta in exactly that order. If a card puts meta above data or context above state, the hierarchy is broken.

---

### Multi-Agent Layout Decisions

When displaying multiple agents (the theme's primary use case):

1. **All cards are identical in structure.** Same height regions, same KPI column count, same pixel component sizes. The ONLY differences between cards are: icon shape, accent color, mosaic bar pattern, 3×3 grid pattern, and data values.
2. **Status cards don't get bigger.** An erroring agent's card is the same size as a healthy one. The red color shift is sufficient — don't give it more visual weight through size.
3. **Grid, not list.** Always `auto-fit` grid, never vertical stack. The value of multi-agent monitoring is simultaneous visibility. If cards stack vertically, you lose the dashboard and get a feed.
4. **Legend bar above cards.** A horizontal strip showing each agent's pixel icon + label + accent color. This establishes the color key before the viewer hits the card grid.
5. **Page-level title bar.** Minimal: title (Space Grotesk 800 14px CAPS cream) + subtitle (10px dim, agent count + theme name). No logo, no nav, no controls.

---

### Light Mode Variant

Gazette Pixel has a full light mode — not an afterthought, a first-class variant. The dark theme is the newsroom at 2 AM; the light theme is the morning broadsheet in full daylight — same layout, newsprint warmth, ink density.

#### Structural Color Map

| Role | Dark (native) | Light (variant) | Notes |
|---|---|---|---|
| Page background | `#1C1917` warm charcoal | `#F0EBE3` warm newsprint | oklch(0.94 0.01 70) — broadsheet paper stock in daylight |
| Card / surface | `#292524` dark stone | `#FFFFFF` fresh broadsheet | Clean white — crisp morning edition |
| Border | `#3a3530` ash rule | `#D8D0C8` ink rule | oklch(0.85 0.01 60) — dried ink column rule |
| Border heavy | `#3a3530` (2px) | `#C0B8AE` heavy rule | Heavier section dividers, KPI top rules |
| Primary text | `#E7E1D9` warm cream | `#1C1917` press ink | oklch(0.15 0.01 60) — the charcoal bg becomes the ink color |
| Focus text | `#F0C4AB` coral parchment | `#8B4513` saddlebrown | Warm, editorial highlight — darker for readability |
| Dim text | `#6B6560` worn ink | `#9A9590` faded print | Labels, timestamps, byline text |
| Canvas | `#141210` press room | `#E8E2DA` newsstand | oklch(0.91 0.01 65) — page-level bg behind cards |
| Pixel dim | `#222222` dark cell | `#E8E2DA` light cell | Visible grid skeleton on white — unlit blocks |
| Step dim | `#2D2D2D` | `#DDD6CC` | Unfilled step blocks on light |

#### Accent Shifts — Per-Agent

All accents darken 20-30% for white-background contrast. Each must pass APCA Lc >= 50 on `#FFFFFF`.

| Agent Role | Dark Accent | Light Accent | Character |
|---|---|---|---|
| Coder | `#6B8A8B` Forest Teal | `#4A6A6B` Deep Teal | Cooled, technical |
| Researcher | `#A0522D` Warm Clay | `#7A3A1A` Dark Clay | Earthier, grounded |
| Assistant | `#C15F3C` Sienna | `#A04828` Burnt Sienna | Darkened, still warm |
| Monitor | `#7088A0` Slate Blue | `#506878` Deep Slate | Cooler, watchful |
| Deployer | `#C1783C` Burnt Orange | `#985828` Dark Orange | Subdued push |
| Reviewer | `#B89848` Muted Gold | `#8A7030` Dark Gold | Aged, judicial |
| Scheduler | `#7A9A6A` Sage Green | `#5A7A4A` Deep Sage | Grounded, steady |
| Debugger | `#B87333` Copper | `#905A22` Dark Copper | Diagnostic warmth |

| Status | Dark | Light | Notes |
|---|---|---|---|
| Error | `#c4453a` signal red | `#c4453a` (unchanged) | Red is universal — no shift needed |
| Warning | `#a08030` muted amber | `#806020` dark amber | Darkened for white bg contrast |

#### Shadow & Depth Adaptation

- **Dark:** No shadows. No `box-shadow`, no elevation. Borders ARE the elevation system. 2px border = card, 1px border = section.
- **Light:** Minimal hairline shadow: `box-shadow: 0 1px 2px rgba(28,25,23,0.04)`. The border system remains primary — shadows are supplemental, not structural. Border hierarchy (2px card / 1px section) preserved unchanged.

#### Texture & Grain Adaptation

- **Dark:** Concrete grain at 2-3% opacity, `soft-light` blend, `feTurbulence baseFrequency="0.8"`.
- **Light:** Grain drops to 1.5% opacity, switches to `multiply` blend. Reads as newsprint paper fiber texture — the slight roughness of broadsheet stock. Warmer than digital noise, subtler than dark mode's concrete feel.

#### Light Mode Rules

1. **Pixel dim cells become visible.** Unlit mosaic blocks, pixel bar cells, and step blocks use `#E8E2DA` on white — clearly visible as a grid skeleton. The quantized data structure is always apparent, even with no data.
2. **All per-agent accents darken 20-30%.** Earth-toned accents that work on dark charcoal are too pale on white. Each shifts to a darker variant while preserving its hue character.
3. **Error red is unchanged.** `#c4453a` passes contrast on both dark and light backgrounds. Red is red — no mode shift needed for urgency.
4. **Borders remain primary, shadows supplemental.** The light variant does NOT adopt shadow-based elevation. Borders stay the structural system. The hairline shadow is atmospheric, not architectural.
5. "Morning broadsheet in full daylight — same layout, newsprint warmth, ink density."

---

### Mobile Notes

- **Drop grain texture.** The `feTurbulence` SVG filter is the only performance cost. Remove it on mobile with zero visual impact.
- **Reduce mosaic bar to 20 blocks** (from 40). Same patterns, half resolution. Still communicates the pattern.
- **Maintain pixel block sizes.** 3px blocks with 1px gaps are already near minimum. Don't scale them smaller — they become unreadable.
- **Card min-width: 280px** on mobile (down from 300px). Single-column layout on phones, 2-column on tablets.
- **Touch targets: 44px.** Pixel blocks are decorative/informational, not interactive — no touch target concerns. If any element becomes tappable, wrap it in a 44px hit area.
- **Performance:** This theme is inherently fast. No blur, no shadows, no blend modes (aside from optional grain), no canvas, no WebGL. Pixel blocks are plain `div` elements. Tick-based updates at 800ms are lower frequency than 60fps animation. A page of 8 cards with 40-block mosaic bars + 10×6 pixel bar grids = ~3,800 DOM elements total — well within budget.

---

### Implementation Checklist

- [ ] Space Grotesk + JetBrains Mono loaded (Google Fonts)
- [ ] `border-radius: 0` on ALL elements (global reset)
- [ ] No `box-shadow` anywhere
- [ ] Pixel blocks are `div` elements, not canvas/SVG
- [ ] Status color override: error/warning replaces accent on ALL card elements
- [ ] KPI columns separated by 1px borders, not gaps
- [ ] Staggered entrance: 40–50ms per card, `translateY(6px)`, 250ms duration
- [ ] Tick interval: 800ms for all data updates
- [ ] `prefers-reduced-motion` media query present
- [ ] Grid: `auto-fit`, `minmax(300px, 1fr)`, gap 10px
- [ ] Grain texture: optional, 2–3% opacity, `feTurbulence 0.8 numOctaves 2`
