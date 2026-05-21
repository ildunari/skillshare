## 30. Quiet Lattice Dashboard

> Premium dashboard without low-contrast gimmicks — calm neutrals, micro-structure grids, extremely disciplined hierarchy.

**Best for:** Financial dashboards, admin panels, BI tools, SaaS analytics, enterprise software, reporting interfaces.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Quiet White | `#F7F7F5` | Primary canvas. Warm white, no blue cast. |
| Alt Background | Panel Grey | `#EFEDEA` | Cards, sidebars, table headers. |
| Primary Text | Near Black | `#171717` | Body text, headings. Maximum readability. |
| Secondary Text | Cool Grey | `#6E6E6E` | Labels, metadata, secondary text. |
| Accent | Calm Blue | `#3366AA` | Links, selection, primary actions. Trustworthy, not flashy. |
| Success | Understated Green | `#2E7D50` | Positive metrics, in-range states. |
| Warning | Amber | `#C87A20` | Attention-needed states. |
| Danger | Quiet Red | `#C04040` | Errors, critical alerts. Not screaming. |
| Border | Lattice Grey | `#DCDAD6` | Card borders, gridlines, axes. |

### Typography
- **Display:** Plus Jakarta Sans (600 weight) — refined, professional, warm without being decorative
- **Body:** DM Sans (400 weight) — clean, excellent readability in data-dense contexts
- **Mono:** Geist Mono — modern, aligned with the calm premium aesthetic

### Visual Style
- **Micro-Grid Structure:** Very faint grid lines (lattice grey at 8% opacity) at 20px intervals on dashboard sections. Creates subconscious alignment without visual noise. Invisible to casual users, reassuring to data readers.
- **Zero Decoration:** No texture, no grain, no gradients, no shadows on flat surfaces. Depth communicated via 1px borders and slight background color shifts.
- **Information Hierarchy:** Three levels: (1) KPI metrics in 32–40px Plus Jakarta 600, (2) section headings in 16–18px DM Sans 500, (3) body/labels in 13–14px DM Sans 400. No other levels. Strict.
- **Semantic Colors Only for Semantics:** Green/amber/red used ONLY for success/warning/danger states. Never decorative. Calm blue for all non-semantic interactive elements.

### Animation Philosophy
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` — invisible, standard.
- **Timing:** Almost instant. Micro: 80ms. Transitions: 150ms. Chart animations: 250ms.
- **Motion Character:** Nearly invisible. Motion exists to prevent disorientation, not to delight. If you notice the animation, it's too much.
- **Physics:** None. Instant state changes with tiny crossfades as the only concession to smoothness.

### Signature Animations
1. **Quiet Fade** — Content blocks fade in with 150ms `opacity(0→1)`. No movement. Just... there.
2. **Value Morph** — KPI numbers update by morphing from old → new value (CSS counter or JS interpolation) over 200ms. Brief 1px flash of calm-blue underline on change.
3. **Row Highlight** — Table rows get a panel-grey background on hover, transitioning at 80ms. Immediate, not animated.
4. **Chart Grow** — Bar chart bars grow from baseline with 250ms ease-out. Line charts draw left-to-right. Standard, expected, functional.
5. **Panel Reveal** — Detail panels and modals fade in at 150ms with no spatial movement. Close is instant (0ms) — modals should never feel like they're leaving.

### UI Components
- **Buttons:** Primary: calm blue fill, quiet white text, `border-radius: 6px`. Secondary: 1px lattice-grey border, near-black text. Hover: darken 6%. Active: `scale(0.98)`. Compact: 36px height.
- **Sliders:** Track is 2px lattice-grey line. Thumb is 12px calm-blue circle. Value in Geist Mono, right-aligned with unit.
- **Cards:** Panel grey background, 1px lattice-grey border. `border-radius: 6px`. No shadow. Padding 20px. Section title in DM Sans 500 14px.
- **Tooltips:** Near black background, quiet white text. Geist Mono 11px (shows exact values). `border-radius: 4px`. Arrow pointer.
- **Dividers:** Lattice grey at 50% opacity. 1px. Within cards: 40px whitespace gap (no visible divider).

### Dark Mode Variant

Quiet Lattice Dashboard has a full dark mode — not an afterthought, a first-class variant. Bloomberg terminal energy — premium quiet darkness, data speaks.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F7F7F5` Quiet White | `#0C0C0C` Quiet Dark | oklch(0.06 0.00 0) — neutral, no color cast |
| Card / surface | `#EFEDEA` Panel Grey | `#141414` Dark Panel | oklch(0.10 0.00 0) — elevated card surfaces |
| Alt surface | — | `#1C1C1C` Deep Panel | oklch(0.13 0.00 0) — sidebars, table headers |
| Border | `#DCDAD6` Lattice Grey | `#242424` Dark Lattice | oklch(0.17 0.00 0) — gridlines, card edges |
| Border heavy | — | `#303030` Bright Lattice | oklch(0.22 0.00 0) — section dividers |
| Primary text | `#171717` Near Black | `#E8E8E6` Near White | oklch(0.92 0.00 0) at 90% — higher opacity for dashboard readability |
| Secondary text | `#6E6E6E` Cool Grey | `#9A9A9A` Lifted Grey | oklch(0.65 0.00 0) — labels, metadata |
| Dim text | — | `#5E5E5E` Deep Grey | oklch(0.42 0.00 0) — tertiary info |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Calm Blue | `#3366AA` | `#5088CC` (brighter) | Interactive clarity — links and selections must pop on dark |
| Understated Green | `#2E7D50` | `#3A9A60` (brighter) | Positive metrics slightly brighter for dark bg |
| Amber warning | `#C87A20` | `#D09030` (brighter) | Attention states lift for visibility |
| Quiet Red | `#C04040` | `#D05050` (brighter) | Critical alerts slightly brighter — still not screaming |

#### Shadow & Depth Adaptation
- Light: Zero shadows — depth from 1px borders and background color shifts only
- Dark: STILL zero shadows. ZERO decoration rule preserved — dark mode is EVEN MORE restrained. Depth from border color (`#242424` dark lattice) against surface (`#141414` dark panel). The quiet discipline increases in dark mode — nothing competes with data

#### Texture & Grain Adaptation
- Light: Micro-grid at 8% opacity (`rgba(0,0,0,0.08)`) — lattice grey at 20px intervals, subconscious alignment
- Dark: Micro-grid shifts to white at 4% opacity (`rgba(255,255,255,0.04)`) — barely visible but present. The lattice structure persists as subconscious scaffolding. Lower opacity than light mode because white grid lines on dark are perceptually stronger than dark lines on light

#### Dark Mode Rules
- ZERO decoration rule is EVEN MORE strict in dark mode — no glows, no gradients, no texture beyond the micro-grid
- Text at 90% opacity (not 87%) — dashboard readability is paramount, data must be instantly scannable
- Semantic colors (green/amber/red) all brighten slightly but remain understated — `#3A9A60`, `#D09030`, `#D05050` — still calm, still professional
- Micro-grid at 4% white (half the perceptual strength of light mode's 8% black) — barely there, still structuring
- "Bloomberg terminal energy — premium quiet darkness, data speaks"

### Mobile Notes
- Maintain data density where possible — this is a professional tool.
- KPI metrics can scale down to 24–28px but keep Plus Jakarta Sans 600.
- Touch targets: 44px minimum but compact horizontal spacing preserved.
- Disable micro-grid pattern (not visible on mobile pixel density anyway).
