## 12. Neon Noir

> Restrained cyberpunk — Blade Runner 2049's color discipline. 90% monochrome, 10% electric.

**Best for:** Real-time data, monitoring dashboards, game UIs, night-mode artifacts, system status, security visualizations.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Charcoal Black | `#0D0D0D` | True dark. Not pure black — subtle warm tint. |
| Surface | Smoke | `#1A1A2E` | Panels, cards. Faint blue undertone. |
| Primary Neon | Hot Pink | `#FF2D78` | Primary data, CTA, critical alerts. SPARINGLY. |
| Secondary Neon | Electric Blue | `#0094FF` | Secondary data, links, selection states. |
| Monochrome | Light Grey | `#E0E0E0` | Body text, standard data. The workhorse. |
| Dim | Mid Grey | `#666680` | Inactive elements, secondary text, grid. |
| Scan Line | Neon at 5% | varies | Subtle horizontal scan-line texture. |
| Border | Dark Edge | `#2A2A3E` | Card/panel borders. Barely visible. |

### Typography
- **Display:** Space Grotesk (700) — geometric, techy, neon-sign energy
- **Body:** DM Sans (400) — clean, disappears into the design
- **Mono:** Fira Code — the star. Code, data, values ALL in mono. Ligatures for style.

### Visual Style
- **Selective Color Rule:** The defining principle. 90% of the UI is greyscale (charcoal, smoke, grey). Neon colors (pink, blue) are used ONLY for: active/interactive elements, critical data, primary CTA, and nothing else. Every use of neon must be earned.
- **Scan Lines:** Subtle horizontal lines across the canvas (1px lines at 2-3% opacity, every 4px). CSS `repeating-linear-gradient`. Creates CRT monitor feel.
- **Glow on Interaction Only:** Neon glow (box-shadow) appears only on hover/active states. At rest, neon elements are flat color with no glow. This restraint is what separates this from generic cyberpunk.
- **Monochrome Photography:** Any imagery or visual elements are desaturated/greyscale. Only data and UI are selectively colored.

### Animation Philosophy
- **Easing:** Sharp — `cubic-bezier(0.65, 0, 0.35, 1)`. Precise, mechanical. Like a well-oiled machine.
- **Timing:** Fast. 150-250ms. This is a monitoring/realtime theme — information appears quickly.
- **Motion Character:** Precise, electric. Brief flickers, sharp fades. Like neon signs switching on.
- **Physics:** None for UI. Data animations use linear interpolation (lerp), not physics.

### Signature Animations
1. **Neon Flicker** — New neon elements rapidly flicker opacity (0→1→0→1→1) over 300ms on entry, like a neon tube warming up.
2. **Glitch Micro** — On error states, a brief (100ms) horizontal displacement (±2px) with RGB channel separation. Subtle digital glitch.
3. **Pulse Beacon** — Critical alerts pulse their neon glow: `box-shadow` animates from 4px→12px→4px over 2s.
4. **Data Stream** — Numeric values update by rapidly cycling through random digits before landing on the correct value (slot-machine effect, 200ms).
5. **Scan Sweep** — Periodically, a horizontal bright line sweeps top-to-bottom at low opacity (2-3%). Background atmosphere.

### UI Components
- **Buttons:** Primary: hot pink fill, charcoal text. No glow at rest. Hover: glow appears (`0 0 12px rgba(255,45,120,0.4)`). `border-radius: 4px`. Secondary: transparent, 1px pink border. Hover: fill at 10%.
- **Sliders:** Track is dim grey 2px. Active portion neon pink. Thumb is a small square (12px) in hot pink. Glow on drag only.
- **Cards:** Smoke surface. 1px dark edge border. `border-radius: 4px`. No shadow. Hover: border becomes neon at 30% opacity.
- **Tooltips:** Smoke bg, light grey text. Neon-colored top border (2px). Mono font for values.
- **Dividers:** 1px dark edge. Or scan-line continuation.

### Light Mode Variant

Neon Noir has a full light mode — not an afterthought, but a concession. This is the hardest theme to invert. The 90% monochrome rule is preserved and even MORE critical on light — restrained accent color on a cool-grey, almost brutalist canvas.

#### Structural Color Map

| Role | Dark (native) | Light (variant) | Notes |
|---|---|---|---|
| Page background | `#0D0D0D` charcoal black | `#F0F0F0` cool light grey | oklch(0.95 0.00 0) — NOT warm. Cool, flat, industrial |
| Card / surface | `#1A1A2E` smoke | `#FFFFFF` white | Clean, sterile panels |
| Border | `#2A2A3E` dark edge | `#D8D8DE` cool silver edge | oklch(0.87 0.01 270) — faint purple-grey tint preserving noir |
| Border heavy | — | `#C0C0C8` darker silver | Section separators, heavier rules |
| Primary text | `#E0E0E0` light grey | `#1A1A2E` dark with purple tint | Preserves the noir undertone in every line of body text |
| Secondary text | — | `#50506A` cool mid-grey | Muted, slightly purple |
| Dim text | `#666680` mid grey | `#8888A0` cool dim | Labels, timestamps, secondary info — purple-tinged |
| Scan line bg | neon at 5% | dark at 2% | Inverted: dark lines on light canvas |

#### Accent Shifts

| Element | Dark (native) | Light (variant) | Reason |
|---|---|---|---|
| Hot Pink | `#FF2D78` | `#C42060` | oklch(0.50 0.18 360) — must pass APCA Lc 60+ on white. Darkened, not desaturated |
| Electric Blue | `#0094FF` | `#0068CC` | oklch(0.52 0.16 255) — deeper blue for white-bg contrast |

#### Shadow & Depth Adaptation

- **Dark:** No shadows. No `box-shadow`, no elevation. Borders define structure. Neon glow (`box-shadow: 0 0 12px`) appears ONLY on hover/active.
- **Light:** Minimal shadow: cards get `box-shadow: 0 1px 2px rgba(26,26,46,0.04)` — barely visible, cool-toned. Neon glow is GONE entirely on light. Replaced by: `border-left: 3px solid accent` for emphasis, filled badges for status, underlines for links. No glow on any element in light mode.

#### Texture & Grain Adaptation

- **Dark:** Scan lines — horizontal 1px lines at 2-3% opacity every 4px via `repeating-linear-gradient`. CRT monitor feel.
- **Light:** Scan lines persist but inverted — dark lines (`#1A1A2E`) at 2% opacity on the light canvas. Barely perceptible. The CRT feel is muted but still present as a structural texture, not an atmospheric effect.

#### Light Mode Rules

1. **Neon CANNOT glow on light.** Every hover glow, neon bloom, and radiating `box-shadow` is removed. Replace with: `border-left` accents (3px solid), filled flat badges, and underlines. No exceptions.
2. **90% mono rule is even MORE critical.** On dark, neon pops naturally. On light, colored elements fight with the bright canvas. Keep accent usage to CTA buttons, active states, and primary data highlights only. Everything else is grey-scale.
3. **Cool grey, not warm.** Page background is `#F0F0F0` (pure neutral to cool). Card background is `#FFFFFF`. Borders are `#D8D8DE` (faint purple-grey tint). Zero warmth anywhere.
4. **Text preserves the noir undertone.** Primary text is `#1A1A2E` (dark with purple tint), not pure black. This single decision keeps the noir atmosphere alive on light.
5. "Neon Noir's light mode is a concession. Keep it minimal, cool-grey, almost brutalist — with restrained accent color."

### Mobile Notes
- This is very performant. Minimal effects, no blur, no blend modes.
- Scan lines: use CSS background-image (GPU-composited). Zero JS cost.
- Neon glow: `box-shadow` is cheap. Keep it.
- Flicker animation: reduce to 2 cycles (not 4) on mobile to avoid visual fatigue on handheld.
