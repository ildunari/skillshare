## 15. Warm Darkroom

> Analog photography meets digital — chemical processes, grain, intimate warmth in controlled darkness.

**Best for:** Photo galleries, documentary visualizations, timeline/history artifacts, atmospheric simulations, narrative experiences.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Warm Black | `#1A1210` | Not pure black — warm, like a darkroom. |
| Surface | Dark Wood | `#2A1E18` | Panels, cards. Warm, elevated. |
| Safe Light | Darkroom Red | `#4A1010` | Ambient glow. Very subdued, never bright. |
| Primary | Sepia | `#D4A574` | Main content, highlights, warm data. |
| Secondary | Paper White | `#F5F0E8` | Text, bright elements. Photographic paper. |
| Tertiary | Chemical Blue | `#2A4858` | Cool accents, secondary data, links. |
| Grain | Noise | varies | Film grain overlay on everything. |
| Border | Darkroom Trim | `#3A2820` | Warm, barely visible edges. |

### Typography
- **Display:** DM Serif Display — dramatic, photographic, editorial
- **Body:** Spectral — optimized digital serif, long-form readability, photographic captions
- **Mono:** IBM Plex Mono — technical, chemical data, timestamps

### Visual Style
- **Film Grain:** Constant noise overlay across the entire canvas. SVG `feTurbulence` (high frequency, `baseFrequency="0.9"`) at 4-6% opacity, `overlay` blend. This is the defining texture.
- **Vignette:** Radial gradient from center (transparent) to edges (20% black). Every viewport. Creates intimate, focused light.
- **Sepia Toning:** All visual elements trend toward the warm sepia/amber spectrum. Even blues are warm-leaning (`#2A4858` not `#0000FF`).
- **Chemical Stains:** Occasional decorative elements: irregular shapes in darkroom red or chemical blue at 5-8% opacity, like developer stains on the darkroom wall.
- **Photographic Paper:** Text and content containers use paper white (`#F5F0E8`) with warm tone, like actual photographic paper.

### Animation Philosophy
- **Easing:** Slow ease-in — `cubic-bezier(0.4, 0, 1, 1)`. Things emerge gradually, like an image developing in chemical solution.
- **Timing:** Slow, patient. Reveals 1-2s. Fades 800ms. The darkroom is a place of patience.
- **Motion Character:** Chemical, developing. Elements don't move spatially — they appear by developing (opacity, contrast, detail emerging from darkness).
- **Physics:** None. This theme is about revelation, not movement.

### Signature Animations
1. **Photo Develop** — The defining animation. Elements start as flat, uniform warm black, then gradually reveal: first faint outlines (10% opacity), then shadows (30%), then midtones (60%), then highlights (100%). 2-3s total. Like watching a photo develop in chemical bath.
2. **Grain Breathe** — The film grain overlay subtly shifts (animated `seed` attribute on feTurbulence, or background-position shift on noise texture) every 2s. Living grain.
3. **Dodge & Burn** — On hover, elements get brighter in the center ("dodging") and darker at edges ("burning") — animated radial gradient overlay.
4. **Safe Light Pulse** — The ambient darkroom red glow subtly pulses (3-5% opacity oscillation) over 6-8s. Atmospheric.
5. **Chemical Wash** — Section transitions use a horizontal color sweep: sepia tone washes across, then resolves to the new content. Like toning a print.

### UI Components
- **Buttons:** Chemical blue fill, paper white text. No border. Soft warm shadow. `border-radius: 4px`. Hover: sepia fill. Active: darken, `scale(0.97)`.
- **Sliders:** Track is sepia 2px line on warm black. Thumb is paper white circle (12px) with warm glow shadow.
- **Cards:** Dark wood surface. No border (darkness is the border). `border-radius: 6px`. Subtle inner warm glow on hover. Generous padding.
- **Tooltips:** Dark wood bg, sepia text. Warm, intimate. Small serif font.
- **Dividers:** Sepia line at 20% opacity. Or a chemical-stain decorative SVG.

### Light Mode Variant

Warm Darkroom has a full light mode — not an afterthought, a first-class variant. The dark theme is the developing process; the light theme is the finished print. Sepia print on fiber paper in gallery light.

#### Structural Color Map

| Role | Dark (native) | Light (variant) | Notes |
|---|---|---|---|
| Page background | `#1A1210` warm black | `#F5F0E8` fiber-base paper | oklch(0.95 0.01 70) — photographic paper, warm off-white |
| Card / surface | `#2A1E18` dark wood | `#FAF4EC` glossy print area | oklch(0.97 0.01 75) — slightly brighter than page, like a mounted print |
| Border | `#3A2820` darkroom trim | `#DDD5C8` print border | oklch(0.87 0.01 65) — the mat board edge around a framed photo |
| Border heavy | — | `#C8BEB0` frame edge | Heavier section dividers |
| Primary text | `#F5F0E8` paper white | `#2A1E18` warm sepia-black | oklch(0.18 0.02 55) — the dark wood color becomes the ink |
| Secondary text | — | `#5A4A3A` warm brown | Muted, photographic caption tone |
| Dim text | — | `#8A7E72` faded paper | Labels, timestamps, chemical annotations |
| Safe light ambient | `#4A1010` darkroom red | N/A — removed | Darkroom red has no meaning in gallery light |

#### Accent Shifts

| Element | Dark (native) | Light (variant) | Reason |
|---|---|---|---|
| Sepia | `#D4A574` (main content) | `#8C6A44` (text accent) | Becomes accent, not primary. Darkened for Lc ~55 on paper bg |
| Darkroom Red | `#4A1010` | `#8C4A30` terra cotta | Red disappears — replaced by warm terra cotta that reads as fired clay |
| Paper White | `#F5F0E8` (text, bright elements) | IS the background | Full inversion — the paper is now the page itself |
| Chemical Blue | `#2A4858` | `#2A4858` (cool accent, more visible) | Unchanged — it was already dark enough. Now pops as a cool counterpoint |

#### Shadow & Depth Adaptation

- **Dark:** No explicit shadows. Darkness IS the border. Vignette radiates inward (edges darken to 20% black). Warm glow shadows on interactive elements.
- **Light:** Vignette still present but inverted — edges fade to near-white (`rgba(245,240,232,0.6)` at edges, transparent center). Cards: `box-shadow: 0 1px 4px rgba(42,30,24,0.06)` — warm, subtle, like a print casting a faint shadow on mat board. The vignette now focuses attention inward by brightening edges, not darkening them.

#### Texture & Grain Adaptation

- **Dark:** Constant film grain overlay — `feTurbulence` at `baseFrequency="0.9"`, 4-6% opacity, `overlay` blend. Coarse, atmospheric, darkroom-authentic.
- **Light:** Grain persists but lighter and higher-frequency. `baseFrequency="1.1"`, 2-3% opacity, `multiply` blend. This reads as photographic paper texture — the fine surface grain of a fiber-base print — not as digital noise. The grain is present but polite.

#### Light Mode Rules

1. **Darkroom red vanishes.** `#4A1010` has no place in gallery light. Replace with terra cotta `#8C4A30` for warm accents — it reads as fired clay or aged leather, not a safe light.
2. **Sepia shifts from primary to accent.** In dark mode, sepia is the main content color. In light mode, warm sepia-black (`#2A1E18`) carries the text. `#D4A574` sepia is darkened to `#8C6A44` and used only for accents, highlights, and decorative elements.
3. **Paper white IS the background.** The paper white (`#F5F0E8`) that served as text color in dark mode is now the page itself. This is a complete inversion — the photographic paper becomes the canvas.
4. **Vignette inverts, not removes.** The radial vignette is essential to the darkroom identity. On light, it fades edges to near-white instead of near-black. Same focus effect, opposite luminance.
5. "The finished print, not the developing process. Sepia print on fiber paper in gallery light."

### Mobile Notes
- Film grain: reduce feTurbulence to 1 octave and 3% opacity on mobile.
- Vignette: CSS `radial-gradient` background is GPU-composited and cheap.
- Photo develop animation: simplify to 2-step (0%→50%→100%) instead of 4-step on mobile.
- Safe light pulse: remove on mobile (subtle enough to not be missed).
- Chemical wash transition: replace with simple crossfade on mobile.
