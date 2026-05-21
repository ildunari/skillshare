## 32. TUI Block Grid

> Terminal UI meets pixel-art telemetry on Vercel-dark canvas — cool blacks, vivid accent pops, quantized data. A broadsheet dashboard rendered in discrete blocks.

**Best for:** Mission control dashboards, multi-agent monitors, DevOps status walls, CI/CD pipelines, real-time telemetry, terminal-adjacent UIs, agent orchestration panels, system health dashboards, chat-ops interfaces.

---

### Identity & Philosophy

TUI Block Grid is the cooler, more technical sibling of Gazette Pixel (#31). Where Gazette Pixel leans editorial-warm (charcoal, cream, sienna), TUI Block Grid leans engineering-cool (true black, pure white, vivid saturated accents). The newspaper metaphor fades; the terminal metaphor sharpens.

The name is literal: TUI (Text User Interface) + Block (pixel blocks as the atomic visual unit) + Grid (everything on a strict grid, cards on a grid, pixels on a grid, data on a grid). Three words, three constraints.

**Core identity:** Vercel's dark aesthetic — true black backgrounds, neutral grey borders, Inter typeface, minimal chrome — combined with the pixel-art data visualization system from Gazette Pixel. The result is something that looks like it belongs in a `vercel.com/dashboard` redesign but renders all its data through crude, countable pixel blocks.

**Key difference from Gazette Pixel (#31):** Temperature. Gazette Pixel is warm charcoal + cream + earth tones. TUI Block Grid is cool black + pure white + vivid primaries. Gazette Pixel is a newsroom at 2 AM. TUI Block Grid is a terminal in a clean office.

**Decision principle:** "Would this look native on vercel.com?" If yes, keep it. If it feels warm, earthy, or editorial — you've drifted into Gazette Pixel territory. Pull back to neutral.

---

### Color Palette

Pure neutral foundation. Zero warm undertone. Accents are vivid and saturated — they pop hard against the neutral base because there's no warmth to compete with.

| Role | Color | Hex | OKLCH (approx) | Usage |
|---|---|---|---|---|
| Page | True Black | `#000000` | L=0.00 | Page-level background behind all cards. |
| Background | Near Black | `#111111` | L=0.09 | Card background. Neutral, no color cast. |
| Border | Mid Grey | `#333333` | L=0.23 C=0.00 | Card borders, internal dividers, column rules. |
| Border Heavy | Light Grey | `#444444` | L=0.30 C=0.00 | Hover borders, KPI section top rule, header divider. |
| Primary Text | Near White | `#EDEDED` | L=0.94 C=0.00 | Headlines, KPI values, card titles. Pure neutral. |
| Focus Text | Zinc | `#A1A1AA` | L=0.68 C=0.01 h=270 | Focus descriptions, active task text. Cool-tinted. |
| Dim Text | Grey | `#666666` | L=0.44 C=0.00 | Labels, timestamps, commands, secondary info. |
| Pixel Dim | Dark Cell | `#222222` | L=0.15 C=0.00 | Unlit pixel bar cells, empty grid positions. |
| Step Dim | Darker Cell | `#2D2D2D` | L=0.20 C=0.00 | Unfilled step blocks. |
| Grid Dim | Grid Off | `#333333` | L=0.23 C=0.00 | Unlit 3×3 status grid cells. |
| Meta Dim | Faint | `#444444` | L=0.30 C=0.00 | Evidence tags, bracket notation. |
| Error | Vivid Red | `#FF4D4D` | L=0.62 C=0.20 h=25 | Error states, failure indicators. Bright and urgent. |
| Warning | Amber | `#F5A623` | L=0.75 C=0.15 h=70 | Warning/slow states. Warm pop on cool base. |

**Color rules:**
1. **Zero warm undertones in structural colors.** Backgrounds, borders, text — all pure neutral grey scale. The warmth comes only from warning amber; everything else is cool or neutral.
2. **Accents are vivid.** Unlike Gazette Pixel's muted earth tones, TUI Block Grid uses full-saturation primaries. They're meant to pop against the neutral base like status LEDs on a black panel.
3. **Status overrides accent.** Same rule as Gazette Pixel: when an agent enters error/warning, ALL accent-colored elements on that card swap to red/amber.
4. **No gradients.** Flat fills only.
5. **Red is earned.** Signal red appears only for genuine errors.

#### Agent Accent System

Vivid, saturated, high-contrast against `#111111` background. These are closer to Vercel's/GitHub's accent palette than Gazette Pixel's earth tones.

| Agent Role | Accent | Hex | Character |
|---|---|---|---|
| Coder | Emerald | `#3ECF8E` | Vercel green — success, build, ship |
| Researcher | Amber | `#F5A623` | Warm signal — searching, probing |
| Assistant | Red | `#FF4D4D` | Hot — communicating, or failing |
| Monitor | Blue | `#0070F3` | Vercel blue — primary, watching |
| Deployer | Orange | `#EE6723` | Active push — deploying, shipping |
| Reviewer | Purple | `#A855F7` | Evaluative — reviewing, judging |
| Scheduler | Cyan | `#06B6D4` | Cool systematic — queuing, timing |
| Debugger | Rose | `#F43F5E` | Diagnostic — tracing, investigating |

---

### Typography

Two families. Inter for the human voice, Geist Mono for the machine voice. This is the Vercel stack.

- **Display/Headlines:** Inter 600 — Sentence case (NOT all-caps like Gazette Pixel). Clean, modern, professional. letter-spacing `0.02–0.04em`.
- **Body:** Inter 400 — Standard reading weight. Used for focus descriptions.
- **Data/Mono:** Geist Mono 500–800 — ALL data, labels, commands, status text, KPI numbers, timestamps. The workhorse. Everything that comes from a machine or represents a measurement.

**Key typography differences from Gazette Pixel:**
- Inter replaces Space Grotesk (cleaner, more neutral, Vercel-native)
- Geist Mono replaces JetBrains Mono (same family as Inter in the Vercel ecosystem)
- Sentence case replaces ALL CAPS for agent labels (less brutalist, more modern)
- Phase labels and status text remain uppercase but in Geist Mono, not Space Grotesk

**Typography rules:**
1. **KPI numbers:** Geist Mono 700 at 18px. The largest elements on the card.
2. **Labels above KPIs:** Geist Mono 500 at 9px, uppercase, letter-spacing 0.12em, dim color.
3. **Phase labels:** Geist Mono 500 at 11px, uppercase, letter-spacing 0.08em, accent-colored.
4. **Agent name:** Inter 600 at 13px, sentence case. letter-spacing 0.04em.
5. **Commands/paths:** Geist Mono 400 at 11px, dim color. Whispered.
6. **Three font sizes only:** Small (9–11px), medium (12–13px), large (18px).

#### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

CSS variable: `--mono: 'Geist Mono', 'SF Mono', monospace;`

---

### Visual Style

#### The Pixel Grid System

Identical component architecture to Gazette Pixel (#31), adapted for the cooler palette:

**Five pixel components:**

1. **Mosaic Status Bar:** 40 blocks across card width, 4px tall. Same per-role fill patterns as Gazette Pixel. Unlit cells are transparent (showing card background through).

2. **3×3 Status Grid:** 9 blocks, 4×4px, gap 1px. Same per-role fill patterns. Unlit cells use `#333333` (grid dim) — visible on the `#111111` card background.

3. **Pixel Bar Chart:** 10 columns × 6 rows, 8px × 3px cells, gap 1px. Unlit cells `#222222`. Lit cells in active accent color.

4. **Step Blocks:** 10px squares, gap 3px. Filled = accent, unfilled = `#2D2D2D` with 1px border at 20% accent opacity.

5. **Pixel Icons:** 7×7 grids of 3px blocks, 1px gaps. Same icon designs as Gazette Pixel. Rendered in active accent color.

#### Structural Borders

- Card border: `1.5px solid #333333` — thinner than Gazette Pixel's 2px, more refined
- Internal dividers: `1px solid #333333`
- Header bottom divider: `1px solid #444444` (heavier)
- KPI section top rule: `2px solid #444444` (heaviest internal rule)
- Focus text left-border: `2px solid accent@19%` (`accent + "30"`)
- Card shadow: `0 1px 3px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.03)` — subtle depth + top-edge catch
- Hover: border brightens to `#444444`
- **No rounded corners.** `border-radius: 0` on everything.

#### Card Anatomy

```
┌─────────────────────────────────────────────┐
│ ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │  ← Mosaic bar (40 blocks, 4px)
├─────────────────────────────────────────────┤
│ [PIX]  Agent Name           [▪▪▪] OK       │  ← Header: icon + name (sentence case)
│        channel/target                       │
├─────────────────────────────────────────────┤
│ PHASE LABEL                                 │  ← Geist Mono, accent-colored
│ ■■□□□□□□□□                                  │  ← Step blocks
│ ▎ Focus description in zinc                 │  ← Left-bordered, cool grey
│                                             │
│  EVT/M  │   ERR   │   AGE                  │  ← KPI columns
│   8.2   │    0    │   12s                   │
│                                             │
│ ▪▪▪▪▪▪▪▪▪▪                                 │  ← Pixel bar chart
│                                             │
│ $ npm run build                   [exec]    │  ← Command + evidence
└─────────────────────────────────────────────┘
```

---

### Animation Philosophy

Identical to Gazette Pixel. Quantized, mechanical, discrete.

- **Easing:** `steps(n)` or `linear`. No springs, no bounce, no ease-in-out.
- **Timing:** Fast. 150–250ms for state changes. 800ms tick interval.
- **Motion character:** Mechanical, discrete. Values snap, don't interpolate.
- **Physics:** None. Rejected on principle.

**One addition:** The mode toggle (dark↔light) transitions at 300ms with standard easing on background, border, and text colors. This is the ONLY smooth transition — it's a UI preference change, not a data update, so smooth is appropriate.

**Reduced motion:**
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

1. **Staggered Entrance** — Cards appear with `translateY(4px) → 0` and `opacity: 0 → 1` over 200ms, staggered at 30ms per card. Slightly faster and shorter travel than Gazette Pixel (4px vs 6px, 200ms vs 250ms).

2. **Tick-Based Refresh** — 800ms global tick. Pixel bars, KPIs update on tick. Snap, not interpolate.

3. **Mosaic Pattern Swap** — Status change swaps the 40-block pattern in one frame.

4. **Border Hover** — Card border brightens from `#333` → `#444` on hover. 150ms transition. The only interactive animation on cards.

5. **Mode Transition** — Dark↔light toggle: page bg, card bg, borders, text, shadows all transition at 300ms. Pixel block colors swap instantly (no transition on data elements).

---

### UI Components

**Cards:** `background: #111111`, `border: 1.5px solid #333`, `box-shadow` for depth. `border-radius: 0`. Padding 14px. Min-width 300px.

**Toggle (mode switch):** Segmented control — two adjacent buttons ("Dark" / "Light") in a 1px bordered container. Active segment gets lighter background (`#222` dark / `#FFF` light). Geist Mono 600 at 10px. No border-radius. `border-radius: 0`.

**Buttons (if needed):** `#222` fill, `#EDEDED` text, 1px `#333` border. Hover: border `#444`. Active: accent background.

**Inputs (if needed):** `#111` fill, 1px `#333` border, Geist Mono. Focus: accent border, no glow.

**Tooltips:** `#222` fill, `#EDE` text, Geist Mono 10px. 1px `#333` border. Square corners.

**Badges/Tags:** Bracket notation in Geist Mono: `[exec]`, `[gateway]`. No background, no border, no pill.

---

### Light Mode Variant

TUI Block Grid has a **full light mode** — not an afterthought, a first-class variant. The toggle is built into the theme.

| Role | Dark (native) | Light (variant) |
|---|---|---|
| Page | `#000000` | `#F6F6F6` cool grey |
| Card bg | `#111111` | `#FFFFFF` pure white |
| Border | `#333333` | `#E0E0E0` |
| Border Heavy | `#444444` | `#CCCCCC` |
| Text | `#EDEDED` | `#111111` |
| Focus Text | `#A1A1AA` | `#555555` |
| Dim | `#666666` | `#777777` |
| Pixel Dim | `#222222` | `#E5E5E5` |
| Step Dim | `#2D2D2D` | `#DFDFDF` |
| Shadow | heavy black | `0 1px 3px rgba(0,0,0,0.05)` + hairline |
| Error | `#FF4D4D` | `#DC2626` (deeper) |
| Warning | `#F5A623` | `#D97706` (deeper) |

**Light mode accent shifts** — accents darken for white-bg contrast:

| Agent | Dark Accent | Light Accent |
|---|---|---|
| Coder | `#3ECF8E` | `#16A34A` |
| Researcher | `#F5A623` | `#B45309` |
| Assistant | `#FF4D4D` | `#DC2626` |
| Monitor | `#0070F3` | `#0062D1` |
| Deployer | `#EE6723` | `#C2410C` |
| Reviewer | `#A855F7` | `#7C3AED` |
| Scheduler | `#06B6D4` | `#0E7490` |
| Debugger | `#F43F5E` | `#E11D48` |

**Light mode rules:**
- Page is `#F6F6F6`, not white — cards (white) need to lift off the page
- Shadow shifts from dark depth to subtle outline (`0 0 0 1px rgba(0,0,0,0.03)`)
- Pixel dim cells become `#E5E5E5` — visible grid skeleton on white
- All transitions between modes at 300ms, except pixel block colors (instant)

---

### Multi-Agent Layout

Same rules as Gazette Pixel (#31):

1. All cards identical in structure. Only icon, accent color, pattern, and data vary.
2. Status cards don't get bigger. Red = same size, just red.
3. Grid, not list. `auto-fit`, `minmax(300px, 1fr)`, gap 8px.
4. Legend bar above cards. Each agent's pixel icon + label at 2px icon size.
5. Minimal title bar. Title + agent count left, mode toggle right.

---

### Information Hierarchy

| Level | Element | Treatment |
|---|---|---|
| 1 — Identity | Agent icon + name | Pixel icon in accent + Inter 600 13px sentence case |
| 2 — State | Phase + status | Geist Mono 500 11px uppercase accent + 3×3 pixel grid |
| 3 — Data | KPI values | Geist Mono 700 18px near-white |
| 4 — Context | Focus text | Inter 400 12px zinc, left-bordered |
| 5 — Meta | Commands, tags | Geist Mono 400 11px dim + brackets |

---

### Data Visualization

Same philosophy as Gazette Pixel: **quantized over smooth, counted over interpolated.**

- Bar charts → Pixel bar grids (10×6)
- Progress → Step blocks (squares)
- Status → 3×3 grid or mosaic bar
- Gauges → Numeric KPI
- Max 2 hues per visualization

---

### Mobile Notes

- Card min-width: 280px. Single column on phones.
- Mosaic bar: reduce to 20 blocks on screens < 360px.
- Touch targets: 44px for toggle buttons. Pixel blocks are non-interactive.
- Mode toggle stays accessible at top-right.
- Performance: identical to Gazette Pixel — no blur, no canvas, no WebGL. Pure DOM pixel blocks.
- The mode toggle's 300ms transitions are the heaviest animation. Everything else is instant swaps.

---

### Implementation Checklist

- [ ] Inter + Geist Mono loaded (Google Fonts)
- [ ] CSS variable `--mono` set to Geist Mono stack
- [ ] `border-radius: 0` on ALL elements
- [ ] Theme object with dark/light palettes including per-agent accent maps
- [ ] Mode toggle: segmented control, top-right of title bar
- [ ] 300ms transition on mode switch for bg, borders, text, shadows
- [ ] Pixel block colors: NO transition (instant swap on mode change)
- [ ] Agent accents darken in light mode for contrast
- [ ] Card shadow adapts per mode (heavy dark / subtle light)
- [ ] `prefers-reduced-motion` media query present
- [ ] Grid: `auto-fit`, `minmax(300px, 1fr)`, gap 8px
- [ ] Tick interval: 800ms
- [ ] Border: 1.5px (not 1px, not 2px)
