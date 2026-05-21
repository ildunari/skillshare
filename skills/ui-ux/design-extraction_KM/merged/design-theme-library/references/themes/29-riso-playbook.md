## 29. Riso Playbook

> Riso print meets modern UI: limited ink palette, playful overlays, registration offsets as a design motif.

**Best for:** Creative tools, portfolios, event microsites, generative art UIs, zine-style content, indie games.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Newsprint | `#F0EDE4` | Primary canvas. Warm uncoated paper. |
| Alt Background | Card Stock | `#E8E4DA` | Cards, panels, secondary surfaces. |
| Ink 1 (Primary) | Riso Blue | `#0078BF` | Primary actions, headings, key data. |
| Ink 2 (Secondary) | Riso Red | `#E0503C` | Secondary accents, CTAs, emphasis. |
| Overprint | Deep Purple | `#4A2878` | Where blue and red overlap. Used for headers, badges, tertiary accents. |
| Ink 3 (Tertiary) | Riso Yellow | `#F5C040` | Highlights, warnings, festive accents. |
| Text | Press Black | `#1A1A18` | Body text. Dense ink on paper. |
| Border | Plate Edge | `#C8C0B4` | Dividers, card borders. |

### Typography
- **Display:** Bricolage Grotesque (700–800 weight) — bold, quirky, poster energy
- **Body:** Work Sans (400 weight) — clean, readable, doesn't compete with display face
- **Mono:** Fira Code — technical credibility for data and code

### Visual Style
- **Limited Ink Rule:** Only 3 chromatic colors (blue, red, yellow) plus black. ALL other colors come from overlapping these inks (blue+red=purple, red+yellow=orange, blue+yellow=green). Use `mix-blend-mode: multiply` on overlapping colored elements.
- **Halftone Texture:** SVG dot pattern (`feTurbulence` + threshold) at 5% opacity on hero sections and image areas. Classic riso grain.
- **Registration Offset:** Headlines and hero text have a colored shadow duplicate offset 2–3px in a secondary ink. `text-shadow: 2px 2px 0 rgba(224,80,60,0.3)`. This is the signature motif.
- **Flat Fills Only:** No gradients, no blur, no glow. Every fill is a solid ink color. Depth comes from layering (multiply blend), not lighting.

### Animation Philosophy
- **Easing:** `steps(8)` for some decorative elements (print-feel) + `cubic-bezier(0.68, -0.55, 0.27, 1.55)` for entrances (bouncy overshoot).
- **Timing:** Snappy. Micro: 100ms. Entries: 250ms. Stagger: 30ms per item.
- **Motion Character:** Stamped and physical. Elements appear like they've been pressed onto the page. Quick overshoot → settle.
- **Physics:** Minimal — brief bounce on entry, quickly resolved. Playful but controlled.

### Signature Animations
1. **Print Registration Shift** — On page load, colored text shadows briefly misalign by ±4px, then snap to their final 2px offset. 300ms. Like a print press aligning.
2. **Ink Stamp** — Elements enter with `scale(1.2) → scale(1)` + `opacity(0→1)`. 200ms. Sharp bounce. Like rubber-stamping.
3. **Overprint Wipe** — Hero sections reveal with a horizontal band of color (blue) wiping left-to-right, followed by a second band (red) at slight delay. Where they overlap, purple appears via multiply blend. 500ms.
4. **Drum Roll** — List items enter in rapid stagger (30ms) with alternating tilt (`rotate(±1deg) → rotate(0)`). Like pages being fed through a print drum.
5. **Ink Splat** — Button clicks spawn a radial `background-image` in the button's ink color, expanding from click point and fading. 250ms.

### UI Components
- **Buttons:** Primary: riso blue fill, newsprint text, `border-radius: 4px`, 2px press-black border. Secondary: riso red border, press-black text. Hover: colored overlay at 10%. Active: `scale(0.95)` + inset shadow. Registration offset on hover.
- **Sliders:** Track is 3px plate-edge line. Thumb is 14px riso-blue square with 2px black border. Value in Fira Code.
- **Cards:** Card stock background, 2px press-black border. `border-radius: 3px`. Hard shadow: `3px 3px 0 rgba(26,26,24,0.12)`. Padding 16px. No softness.
- **Tooltips:** Press black background, newsprint text. Work Sans 12px. `border-radius: 2px`.
- **Dividers:** Plate edge at 60% opacity. 1px. Or a thick (3px) riso-blue line for section breaks.

### Dark Mode Variant

Riso Playbook has a full dark mode — not an afterthought, a first-class variant. Riso print on black paper: the inks glow, overprint blending switches from multiply to screen.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F0EDE4` Newsprint | `#0E0E0C` dark room | Warm near-black — unlit print shop |
| Card / surface | `#E8E4DA` Card Stock | `#141412` dark print stock | Warm dark surface, like black card stock |
| Border | `#C8C0B4` Plate Edge | `#242420` dark plate edge | Warm dark border, press-frame feel |
| Border heavy | `#C8C0B4` at full | `#343430` printing press edge | Section dividers, heavier plate lines |
| Primary text | `#1A1A18` Press Black | `#F0EDE4` at 87% newsprint glow | APCA Lc ~84 on `#141412` — warm paper light |
| Secondary text | `#1A1A18` at lighter weight | `#C0BCA8` warm off-white | Readable secondary, newsprint tone |
| Dim text | n/a | `#7A7868` warm ink grey | Metadata, tertiary — ink residue tone |
| Overprint | `#4A2878` Deep Purple (multiply) | `#7040A8` brightened (screen) | Blend mode fundamentally changes — see rules |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| Riso Blue | `#0078BF` | `#30A0E8` brightened | Brighter on dark — ink glows on black paper |
| Riso Red | `#E0503C` | `#F06050` brightened | Warmer, more vivid — red fluorescence |
| Riso Yellow | `#F5C040` | `#F8D060` brightened | Yellow radiates — brightest ink on dark ground |
| Overprint Purple | `#4A2878` | `#7040A8` brightened | Purple lifts significantly — was dark-on-light, needs light-on-dark |

#### Shadow & Depth Adaptation
- Light: Hard shadow `3px 3px 0 rgba(26,26,24,0.12)` — press-printed card feel
- Dark: Hard shadow remains: `3px 3px 0 rgba(0,0,0,0.3)` — deeper on dark stock. Cards feel like printed sheets stacked on a dark table

#### Texture & Grain Adaptation
- Light: SVG halftone-dot pattern at 5% opacity, `overlay` blend on hero sections. `multiply` blend on overlapping colored elements
- Dark: Halftone pattern inverts — light dots on dark, same density. Apply with `mix-blend-mode: screen` instead of `overlay`. CRITICAL blend mode change: all overprint effects switch from `multiply` to `screen`. On light paper, overlapping inks darken (multiply). On dark paper, overlapping inks lighten (screen). The 3-ink rule still applies — blue+red still makes purple, just via additive mixing instead of subtractive

#### Dark Mode Rules
- CRITICAL: `mix-blend-mode: multiply` → `screen` for ALL overprint color mixing. This is the fundamental physics change
- 3-ink rule absolutely preserved — still only blue, red, yellow + their overprint combinations. No new colors
- Registration offset on headlines preserved — same 2-3px offset, inks just glow brighter against dark paper
- Flat fills rule preserved — no gradients, no blur, no glow halos. The inks are luminous but still flat
- "Riso print on black paper — the inks glow. Overprint blending switches from multiply to screen"

### Mobile Notes
- Disable registration offset on body text (readability concern on small screens).
- Keep offset on hero headings only.
- Simplify overprint wipe to a standard fade.
- Touch targets: 48px minimum with generous padding.
