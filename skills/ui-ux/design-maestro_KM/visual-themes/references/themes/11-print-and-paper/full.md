# Print & Paper — Full Specification
> Schema v2 | 987 lines | Last updated: 2026-02-16

## Table of Contents
| Section | Line |
|---|---|
| Identity & Philosophy | 20 |
| Color System | 41 |
| Gouache Mode Palette | 43 |
| Paper Cut Mode Palette | 66 |
| Riso Mode Palette | 88 |
| Special Colors (All Modes) | 127 |
| Fixed Colors | 135 |
| Opacity System | 142 |
| Color Rules | 155 |
| Typography Matrix | 164 |
| Font Families | 166 |
| Role Matrix — Gouache Mode | 178 |
| Role Matrix — Paper Cut Mode | 193 |
| Role Matrix — Riso Mode | 209 |
| Font Loading | 224 |
| Elevation System | 237 |
| Surface Hierarchy | 243 |
| Shadow Tokens | 256 |
| Backdrop Filter | 276 |
| Separation Recipe | 280 |
| Border System | 286 |
| Base Color | 288 |
| Widths and Patterns | 297 |
| Width Scale | 309 |
| Focus Ring (Per Mode) | 318 |
| Component States | 327 |
| Buttons (Primary) | 329 |
| Buttons (Secondary/Outlined) | 346 |
| Buttons (Ghost/Icon) | 357 |
| Text Input | 368 |
| Chat Input Card | 377 |
| Cards | 388 |
| Sidebar Items | 399 |
| Chips | 411 |
| Toggle/Switch | 421 |
| User Message Bubble | 433 |
| Motion Map | 446 |
| Easings | 448 |
| Duration x Easing x Component | 460 |
| Active Press Scale | 482 |
| Reduced Motion | 491 |
| Overlays | 505 |
| Popover/Dropdown | 507 |
| Modal | 528 |
| Tooltip | 543 |
| Layout Tokens | 559 |
| Spacing Scale | 573 |
| Density | 588 |
| Responsive Notes | 596 |
| Accessibility Tokens | 612 |
| Visual Style | 643 |
| Material | 645 |
| Gouache Mode Rendering | 656 |
| Paper Cut Mode Rendering | 666 |
| Paper Cut Parallax CSS | 671 |
| Riso Mode Rendering | 688 |
| Signature Animations | 727 |
| 1. Paper Stamp (All modes) | 729 |
| 2. Layer Stack (Paper Cut mode) | 741 |
| 3. Ink Spread (Riso mode) | 752 |
| 4. Paint Stroke (Gouache mode) | 762 |
| 5. Shadow Bounce (All modes) | 773 |
| 3-Mode Comparison Table | 784 |
| Riso Ink System Reference | 812 |
| Primary Inks | 816 |
| Overprint Mixing Chart | 825 |
| Implementation Rules | 836 |
| Dark Mode Variant | 846 |
| Dark Mode Palette (Shared Structure, Per-Mode Values) | 850 |
| Dark Mode Rules | 896 |
| Dark Mode Shadow Tokens | 908 |
| Data Visualization | 922 |
| Mobile Notes | 936 |
| Effects to Disable | 938 |
| Sizing Adjustments | 947 |
| Performance Notes | 956 |
| Implementation Checklist | 965 |

---

## 11. Print & Paper

> Physical craft made digital — gouache paint, cut paper, and risograph ink on a shared workbench.

**Best for:** Infographics, editorial design, art projects, creative tools, educational materials, zines, campaign microsites, portfolio showcases, interactive storytelling, cultural event pages.

---

### Identity & Philosophy

This theme lives in a print studio. There are gouache jars open on the table, sheets of construction paper stacked in the tray, and a risograph machine humming in the corner. Everything made here is physical-first: flat color fills, hard directional shadows, paper edges you can feel. The screen is a lightbox showing work made by hands — paint applied with a palette knife, paper cut with a blade, ink pressed through a mesh screen.

The core visual tension is **craft vs. precision**. Every surface looks made-by-hand (matte fills, hard shadows, slight texture), but every token is engineered to the pixel. The result is warm and playful without being childish — think the editorial quality of a design magazine, not a kindergarten bulletin board. High-end craft. Think Risotto Studio prints, Nobrow Press publications, or a Noma Bar infographic.

Three modes share one structural system. **Gouache mode** is bold painted posters: strong matte backgrounds, flat saturated fills, thick hard shadows, maximum visual weight. **Paper Cut mode** is layered construction paper: kraft-and-white palette, stacked layers with parallax depth, die-cut edges that cast hard shadows suggesting physical paper. **Riso mode** is risograph printing: a strict 3-ink system with overprint mixing, halftone dot texture, deliberate registration offset (slight misalignment that signals analog process). All three modes share the same component architecture, spacing system, typography structure, and motion philosophy.

The single unifying rule across all modes: **ZERO gradients.** Nothing fades, blends, or transitions in color space. Every fill is flat. Every surface is a solid color. Every shadow is a hard-edged offset (no blur radius). This is the visual signature — the world of physical media where colors are opaque pigment, not projected light.

**Decision principle:** "When in doubt, ask: could this be made with paint, paper, or ink? If it requires a screen to exist, simplify it. If it could hang on a studio wall, keep it."

**What this theme is NOT:**
- Not gradient-anything. ZERO `linear-gradient`, `radial-gradient`, or `conic-gradient` on any surface, button, card, or background. Skeleton shimmer uses opacity animation, not gradient sweep.
- Not soft or blurred. Shadows are hard-edged offsets. No `blur()` on shadows. No gaussian anything.
- Not precious or fragile. This is bold, confident craft. Thick strokes, strong color, decisive composition.
- Not digitally native. No glassmorphism, no backdrop-blur, no frosted glass. Physical materials do not frost.
- Not monochrome or muted. Even the quietest mode (Paper Cut) uses decisive color contrast. Riso mode is limited to 3 inks but those inks are vivid.
- Not smooth in motion. Animation is snappy with overshoot — things stamp, land, and settle. Nothing floats or drifts.

---

### Color System

#### Gouache Mode Palette

Bold, saturated, matte. Colors that look like they came from paint tubes — Cadmium Red, Ultramarine, Chrome Yellow. Backgrounds are strong enough to be poster colors.

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Studio Wall | `#E8E0D0` | Deepest background. Warm raw linen canvas behind everything. |
| bg | Poster Board | `#F5F0E6` | Primary surface. Warm off-white matte board, the base sheet. |
| surface | Cream Card | `#FFFBF2` | Elevated cards, inputs, popovers. Bright cream stock. |
| recessed | Raw Canvas | `#DDD5C4` | Code blocks, inset areas. Unprimed canvas tone. |
| active | Pressed Linen | `#D1C9B8` | Active/pressed states, selected items. Compressed fabric. |
| text-primary | India Ink | `#1A1714` | Headings, body text. Dense carbon-black ink with warm cast. |
| text-secondary | Graphite | `#5C5549` | Sidebar items, secondary labels. Pencil-sketch gray. |
| text-muted | Chalk Dust | `#948B7D` | Placeholders, timestamps, metadata. Dusty warm gray. |
| text-onAccent | Gesso White | `#FFF8EE` | Text on accent-colored backgrounds. Warm gesso primer white. |
| border-base | Kraft Edge | `#B8AD9A` | Base border color, used at variable opacity. Raw kraft paper edge. |
| accent-primary | Cadmium Red | `#D94F3B` | Brand accent, primary CTA. Bold opaque paint red. |
| accent-secondary | Ultramarine | `#2E5BBA` | Secondary accent. Deep blue straight from the tube. |
| success | Viridian | `#2E8B57` | Positive states. Classic painter's green, desaturated for harmony. |
| warning | Chrome Yellow | `#E8A917` | Caution states. Opaque cadmium yellow tone. |
| danger | Vermillion | `#CC3333` | Error states. Hot, opaque, unmistakable. |
| info | Cerulean | `#3A7CC2` | Informational states. Studio blue, cooler than Ultramarine. |

#### Paper Cut Mode Palette

Kraft-and-white with layered construction paper colors. The palette suggests the physical materials: brown kraft, white card, and a limited set of colored papers.

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Kraft Brown | `#C4A882` | Deepest background. Raw kraft paper, the worktable. |
| bg | Light Kraft | `#DDD0B8` | Primary surface. Lighter kraft, the base sheet. |
| surface | White Card | `#F8F4EC` | Elevated cards, inputs. White construction paper layer. |
| recessed | Dark Kraft | `#B89E7E` | Code blocks, inset areas. Shadow side of kraft. |
| active | Pressed Kraft | `#CABFA6` | Active/pressed states. Kraft under thumb pressure. |
| text-primary | Cut Black | `#201C16` | Headings, body. Cut from black paper, dense and flat. |
| text-secondary | Charcoal Paper | `#665D50` | Secondary labels. Dark gray construction paper tone. |
| text-muted | Kraft Shadow | `#998C78` | Placeholders, metadata. Kraft in shadow. |
| text-onAccent | White Card | `#F8F4EC` | Text on colored paper backgrounds. |
| border-base | Cut Edge | `#A89880` | Border color. The visible edge of a paper layer. |
| accent-primary | Red Paper | `#D4503C` | Primary CTA. Red construction paper, slightly matte. |
| accent-secondary | Navy Paper | `#2C4A7C` | Secondary accent. Dark blue construction paper. |
| success | Forest Paper | `#3B7A4A` | Positive states. Green construction paper. |
| warning | Mustard Paper | `#D49B20` | Caution states. Yellow-ochre construction paper. |
| danger | Brick Paper | `#B83030` | Error states. Deep red paper. |
| info | Sky Paper | `#4A80B0` | Informational states. Light blue construction paper. |

#### Riso Mode Palette

Limited ink system. Three primary inks per composition, plus overprints (visual mixing where two inks overlap). The background is uncoated stock paper.

**Primary Inks:**

| Ink | Name | Hex | Role |
|---|---|---|---|
| Ink 1 | Fluorescent Pink | `#FF4477` | Primary ink. Hot pink, the riso signature. Used for CTA, accent, emphasis. |
| Ink 2 | Blue | `#0078BF` | Secondary ink. Medium blue, workhouse ink for text and structure. |
| Ink 3 | Yellow | `#FFE630` | Tertiary ink. Bright yellow for warmth, highlights, warnings. |

**Overprint Colors (visual mixing):**

| Mix | Result Name | Hex | Mixing | Role |
|---|---|---|---|---|
| Ink 1 + Ink 2 | Deep Violet | `#6B3FA0` | Pink over Blue at ~50% | Links, secondary emphasis, info states |
| Ink 1 + Ink 3 | Hot Orange | `#FF7733` | Pink over Yellow at ~60% | Warning states, warm accents |
| Ink 2 + Ink 3 | Green | `#3D9B4A` | Blue over Yellow at ~50% | Success states, positive indicators |
| Ink 1 + Ink 2 + Ink 3 | Rich Black | `#2A2030` | All three at ~70% | Text primary, deepest shadow |

**Surface Tokens (Riso):**

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Newsprint | `#E8E0D0` | Deepest background. Cheap uncoated stock. |
| bg | French Paper | `#F0EAD6` | Primary surface. Off-white uncoated stock. |
| surface | Bright Stock | `#FAF6EC` | Elevated cards, inputs. Brighter uncoated paper. |
| recessed | Aged Stock | `#DDD5C2` | Code blocks, inset areas. Paper in shadow. |
| active | Thumbed Stock | `#D0C8B6` | Active/pressed states. Paper worn from handling. |
| text-primary | Rich Black | `#2A2030` | Headings, body. All three inks overprinted. |
| text-secondary | Blue Ink | `#0078BF` | Secondary text. Single ink, the blue. |
| text-muted | Faded Ink | `#8E98A4` | Placeholders, metadata. Blue ink at reduced coverage. |
| text-onAccent | Bright Stock | `#FAF6EC` | Text on ink backgrounds. The paper showing through. |
| border-base | Halftone Edge | `#B0A898` | Border color. Edge of a halftone field. |
| accent-primary | Fluorescent Pink | `#FF4477` | Primary CTA. Pure Ink 1 at full coverage. |
| accent-secondary | Blue | `#0078BF` | Secondary accent. Pure Ink 2 at full coverage. |

#### Special Colors (All Modes)

| Token | Gouache | Paper Cut | Riso | Role |
|---|---|---|---|---|
| inlineCode | `#9B4DCA` | `#7B5EA7` | `#6B3FA0` | Code text within prose. Purple-violet register. |
| toggleActive | `#2E5BBA` | `#2C4A7C` | `#0078BF` | Toggle/switch active track. Blue family. |
| selection | `rgba(217,79,59,0.18)` | `rgba(212,80,60,0.20)` | `rgba(255,68,119,0.22)` | `::selection` background. Accent at low opacity. |

#### Fixed Colors

| Token | Hex | Role |
|---|---|---|
| alwaysBlack | `#000000` | Shadow offset base (mode-independent) |
| alwaysWhite | `#FFFFFF` | Emergency on-dark only (mode-independent) |

#### Opacity System

One border base color per mode, applied at variable opacity:

| Level | Opacity | Usage |
|---|---|---|
| subtle | 12% | Lightest separation, hairlines, background dividers |
| card | 22% | Card borders, paper layer edges |
| hover | 35% | Hover states, emphasized borders |
| focus | 50% | Focus borders, maximum non-ring visibility |

Note: Opacity values are higher than typical themes because hard-shadow aesthetics need stronger edge definition to look intentional rather than broken.

#### Color Rules

- **ZERO gradients.** No `linear-gradient`, `radial-gradient`, or `conic-gradient` on any surface. Background fills are solid. Button fills are solid. Card fills are solid. Skeleton loading uses opacity pulse, not gradient sweep.
- **Hard shadows only.** All `box-shadow` values use `0` for blur radius. Shadows are offset blocks of color, like the shadow cast by a piece of paper on a table.
- **Riso mode: 3-ink maximum.** Every color visible on screen must be traceable to one of the three primary inks or a documented overprint combination. No colors exist outside the ink system.
- **Riso mode: registration offset.** Elements using two or more inks show a 1-2px misalignment between ink layers. This is deliberate and signals analog process.
- **Paper Cut mode: layer logic.** Every colored surface must be explicable as a paper layer. Lighter layers sit on top of darker layers. Shadows fall downward-right, always.
- **Gouache mode: paint logic.** Colors are opaque. No transparency for decorative purposes. When surfaces overlap, the top surface completely covers the bottom. The only transparency is in the border/opacity system for functional UI edges.

---

### Typography Matrix

#### Font Families

| Slot | Font | Fallback | Role |
|---|---|---|---|
| display | Bricolage Grotesque | system-ui, -apple-system, sans-serif | Display, Heading. Quirky editorial grotesque with variable weight and optical sizing. Slightly irregular letterforms suggest hand-lettering. |
| body | Outfit | system-ui, -apple-system, sans-serif | Body, Body Small, Button, Input, Label, Caption. Warm geometric sans, readable at small sizes, personality without distraction. |
| mono | IBM Plex Mono | ui-monospace, SFMono-Regular, Menlo, monospace | Code, data values. Industrial monospace with humanist touches. Feels printed. |

**Why this pairing:** Bricolage Grotesque is the ideal display face for craft-made-digital. Its variable weight axis (200-800) and slightly irregular geometry give headlines the energy of hand-painted signage while remaining structurally precise. Outfit complements it as a warmer, rounder geometric sans that reads cleanly at body sizes — it has enough personality to feel intentional but not enough to compete with Bricolage's display presence. IBM Plex Mono was chosen over Fira Code or JetBrains Mono because its slightly humanist construction (open counters, ink traps) feels like it was designed for print rather than screens.

**Family switch boundary:** Bricolage Grotesque handles Display and Heading roles. Outfit handles everything from Body down. Never mix them beyond this boundary. An implementer seeing Bricolage at body size or Outfit at display size has made an error.

#### Role Matrix — Gouache Mode

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Bricolage Grotesque | 42px | 700 | 1.1 (46.2px) | -0.02em | `font-variation-settings: "opsz" 48, "wdth" 100` | Hero titles, poster headlines. Heavy, bold, impactful. |
| Heading | Bricolage Grotesque | 26px | 600 | 1.2 (31.2px) | -0.01em | `font-variation-settings: "opsz" 28` | Section titles, card group headers. |
| Subheading | Bricolage Grotesque | 20px | 600 | 1.25 (25px) | normal | -- | Card titles, subsection headers. |
| Body | Outfit | 16px | 400 | 1.55 (24.8px) | normal | -- | Primary reading text, UI body, descriptions. |
| Body Small | Outfit | 14px | 400 | 1.45 (20.3px) | normal | -- | Sidebar items, form labels, secondary text. |
| Button | Outfit | 14px | 600 | 1.4 (19.6px) | 0.02em | `text-transform: uppercase` | Button labels. ALL CAPS in Gouache mode for poster energy. |
| Input | Outfit | 14px | 450 | 1.4 (19.6px) | normal | -- | Form input text. Slightly heavier for field presence. |
| Label | Outfit | 11px | 600 | 1.33 (14.6px) | 0.08em | `text-transform: uppercase` | Section labels, metadata, timestamps. ALL CAPS, wide-tracked. |
| Code | IBM Plex Mono | 0.9em (14.4px) | 400 | 1.5 (21.6px) | normal | `font-variant-numeric: tabular-nums` | Inline code, code blocks, data values. |
| Caption | Outfit | 12px | 400 | 1.33 (16px) | normal | -- | Disclaimers, footnotes. |

#### Role Matrix — Paper Cut Mode

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Bricolage Grotesque | 38px | 600 | 1.15 (43.7px) | -0.01em | `font-variation-settings: "opsz" 40` | Hero titles. Slightly lighter than Gouache — paper is quieter. |
| Heading | Bricolage Grotesque | 24px | 500 | 1.25 (30px) | normal | -- | Section titles. |
| Subheading | Bricolage Grotesque | 18px | 500 | 1.3 (23.4px) | normal | -- | Card titles. |
| Body | Outfit | 16px | 400 | 1.55 (24.8px) | normal | -- | Primary reading text. Same as Gouache. |
| Body Small | Outfit | 14px | 400 | 1.45 (20.3px) | normal | -- | Sidebar items, secondary text. |
| Button | Outfit | 14px | 500 | 1.4 (19.6px) | 0.01em | -- | Button labels. Sentence case in Paper Cut (not CAPS). |
| Input | Outfit | 14px | 450 | 1.4 (19.6px) | normal | -- | Form input text. |
| Label | Outfit | 12px | 500 | 1.33 (16px) | 0.04em | `text-transform: uppercase` | Section labels. CAPS but narrower tracking than Gouache. |
| Code | IBM Plex Mono | 0.9em | 400 | 1.5 | normal | `font-variant-numeric: tabular-nums` | Code blocks. |
| Caption | Outfit | 12px | 400 | 1.33 (16px) | normal | -- | Footnotes. |

#### Role Matrix — Riso Mode

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Bricolage Grotesque | 40px | 800 | 1.05 (42px) | -0.03em | `font-variation-settings: "opsz" 48` | Hero titles. Heaviest weight — maximum ink coverage. |
| Heading | Bricolage Grotesque | 24px | 700 | 1.2 (28.8px) | -0.01em | -- | Section titles. Bold for ink presence. |
| Subheading | Bricolage Grotesque | 18px | 600 | 1.25 (22.5px) | normal | -- | Card titles. |
| Body | Outfit | 15px | 400 | 1.6 (24px) | 0.01em | -- | Primary reading text. Slightly smaller, wider spacing for legibility on textured stock. |
| Body Small | Outfit | 13px | 400 | 1.5 (19.5px) | 0.01em | -- | Sidebar items, secondary text. |
| Button | Outfit | 13px | 700 | 1.4 (18.2px) | 0.06em | `text-transform: uppercase` | Button labels. CAPS, heavily tracked for riso clarity. |
| Input | Outfit | 14px | 450 | 1.4 (19.6px) | normal | -- | Form input text. |
| Label | Outfit | 11px | 700 | 1.33 (14.6px) | 0.1em | `text-transform: uppercase` | Section labels. Maximum tracking — riso text needs breathing room. |
| Code | IBM Plex Mono | 0.85em | 400 | 1.55 | normal | `font-variant-numeric: tabular-nums` | Code blocks. Slightly smaller to account for halftone texture. |
| Caption | Outfit | 11px | 400 | 1.4 (15.4px) | 0.01em | -- | Footnotes, disclaimers. |

#### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Outfit:wght@100..900&family=IBM+Plex+Mono:wght@100;200;300;400;500;600;700&display=swap" rel="stylesheet">
```

- **Font smoothing:** `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale` on `<html>`.
- **Font display:** `font-display: swap` on all families.
- **Optical sizing:** `font-optical-sizing: auto` for Bricolage Grotesque (has `opsz` axis from 12 to 96).
- **Text wrap:** `text-wrap: balance` for headings, `text-wrap: pretty` for body.

---

### Elevation System

**Strategy:** Hard directional shadows (zero blur). No soft shadows anywhere. Depth is achieved by stacking flat layers with offset hard shadows, like pieces of paper on a table casting shadows in directional light.

#### Surface Hierarchy

| Surface | Background | Shadow | Usage |
|---|---|---|---|
| page | page token | none | Deepest layer. The worktable. |
| canvas | bg token | none | Primary working surface. The base sheet of paper. |
| card | surface token | shadow-card | Cards, inputs at rest. A sheet of paper sitting on the base. |
| recessed | recessed token | none | Code blocks, inset areas. Cut-out hole in the base sheet. |
| active | active token | none | Active items, pressed states. Paper pressed flat. |
| overlay | surface token | shadow-popover | Popovers, dropdowns. Paper floating high above. |

#### Shadow Tokens

All shadows are hard directional (blur radius = 0). Light source is top-left, so shadows fall to bottom-right.

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `2px 2px 0px rgba(0,0,0,0.12)` | Small elements, tags, chips. Slight paper lift. |
| shadow-card | `3px 3px 0px rgba(0,0,0,0.15)` | Cards at rest. One paper layer above base. |
| shadow-card-hover | `4px 4px 0px rgba(0,0,0,0.18)` | Cards on hover. Paper lifts slightly — shadow extends. |
| shadow-input | `2px 2px 0px rgba(0,0,0,0.10)` | Input fields at rest. Subtle depth. |
| shadow-input-hover | `3px 3px 0px rgba(0,0,0,0.14)` | Input hover. |
| shadow-input-focus | `3px 3px 0px rgba(0,0,0,0.18)` | Input focus. Maximum depth for active input. |
| shadow-popover | `5px 5px 0px rgba(0,0,0,0.20)` | Menus, popovers, dropdowns. Paper floating high. |
| shadow-modal | `8px 8px 0px rgba(0,0,0,0.22)` | Modal dialogs. Maximum elevation. |
| shadow-none | `none` | Flat surfaces, disabled states, recessed areas. |

**Gouache mode shadow adjustment:** Multiply all shadow opacity values by 1.3x. Gouache is bolder, shadows are more dramatic.

**Riso mode shadow adjustment:** Shadows use the primary ink color (Fluorescent Pink `#FF4477`) at 15% opacity instead of black. `3px 3px 0px rgba(255,68,119,0.15)`. This gives shadows a warm tint consistent with the riso printing process.

#### Backdrop Filter

| Context | Value | Usage |
|---|---|---|
| All contexts | `backdrop-filter: none` | NO backdrop blur in any mode. Physical materials do not frost. |

#### Separation Recipe

Hard shadow offset + tint-step. Layers separate through color stepping (darker base, lighter overlay) plus a hard directional shadow that says "this piece of paper is above that one." No visible hairline dividers between sections. Sidebar separation is a 2px solid border at card opacity (thicker than typical themes — the paper edge is visible). No blur, no glow, no gradient transitions. Everything is opaque flat fills casting hard shadows.

---

### Border System

#### Base Color

Per-mode border base colors applied at variable opacity:
- **Gouache:** `#B8AD9A` (Kraft Edge)
- **Paper Cut:** `#A89880` (Cut Edge)
- **Riso:** `#B0A898` (Halftone Edge)

All three are warm gray-brown tones that read as the edge of a piece of paper or the boundary of a printed area.

#### Widths and Patterns

| Pattern | Width | Opacity | Usage |
|---|---|---|---|
| subtle | 1px | 12% | Lightest separation, background structure |
| card | 1.5px | 22% | Card borders, paper layer edges |
| hover | 2px | 35% | Hover states, emphasized edges |
| input | 2px | 22% | Form input borders at rest |
| input-hover | 2px | 35% | Form input borders on hover |

Note: Widths are thicker than typical themes (1px minimum, not 0.5px). This is intentional — paper edges and print borders are heavier than digital hairlines. The theme should feel substantial, not delicate.

#### Width Scale

| Name | Value | Usage |
|---|---|---|
| hairline | 1px | Lightest structural lines. Still thicker than typical themes. |
| default | 1.5px | Standard card and component borders. |
| medium | 2px | Input borders, emphasized edges, hover states. |
| heavy | 3px | Accent borders, paper layer outlines, maximum emphasis. |

#### Focus Ring (Per Mode)

| Mode | Color | Width | Offset | Notes |
|---|---|---|---|---|
| Gouache | `rgba(46,91,186,0.65)` (Ultramarine) | 3px solid | 2px | Blue focus ring. Thicker than typical — poster scale. |
| Paper Cut | `rgba(44,74,124,0.60)` (Navy Paper) | 3px solid | 2px | Navy focus ring matches Paper Cut accent. |
| Riso | `rgba(0,120,191,0.60)` (Blue Ink) | 3px solid | 2px | Blue Ink focus ring. Stays within the ink system. |

Focus rings are 3px (not 2px) because the overall theme is heavier and bolder. A 2px ring would feel thin against 2-3px component borders.

---

### Component States

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | `bg: accent-primary`, `border: 2px solid accent-primary`, `color: text-onAccent`, `border-radius: 4px`, `height: 36px`, `padding: 0 16px`, `font-size: 14px`, `font-weight: 600`, `font-family: Outfit`, `box-shadow: shadow-sm`, `cursor: pointer` |
| Hover | `box-shadow: shadow-card`, `transform: translate(-1px, -1px)` (paper lifts up-left as shadow extends down-right) |
| Active | `box-shadow: none`, `transform: translate(2px, 2px)` (paper stamps flat — shadow collapses) |
| Focus | `outline: 3px solid focus-ring-color`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `box-shadow: none`, `cursor: not-allowed` |
| Transition | `transform, box-shadow 100ms cubic-bezier(0.34, 1.56, 0.64, 1)` (overshoot easing) |

**Gouache override:** Button text is `text-transform: uppercase`, letter-spacing `0.02em`.
**Riso override:** Button shadow uses pink-tinted shadow. Rest state includes 1px registration offset via `text-shadow: 1px 0px 0px rgba(0,120,191,0.3)` on the label.

#### Buttons (Secondary/Outlined)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: 2px solid border-base at hover opacity`, `color: text-primary`, `border-radius: 4px`, `height: 36px`, `padding: 0 16px`, `box-shadow: shadow-sm`, `cursor: pointer` |
| Hover | `bg: recessed`, `box-shadow: shadow-card`, `transform: translate(-1px, -1px)` |
| Active | `box-shadow: none`, `transform: translate(2px, 2px)` |
| Focus | `outline: 3px solid focus-ring-color`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `box-shadow: none` |
| Transition | `transform, box-shadow, background-color 100ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

#### Buttons (Ghost/Icon)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: none`, `color: text-secondary`, `border-radius: 4px`, `width: 36px`, `height: 36px`, `padding: 0`, `cursor: pointer` |
| Hover | `bg: recessed`, `color: text-primary` |
| Active | `transform: scale(0.92)` (strong stamp press for icon buttons) |
| Focus | `outline: 3px solid focus-ring-color`, `outline-offset: 2px` |
| Disabled | `opacity: 0.4`, `pointer-events: none` |
| Transition | `background-color, color 120ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

#### Text Input

| State | Properties |
|---|---|
| Rest | `bg: surface`, `border: 2px solid border-base at card opacity`, `border-radius: 4px`, `height: 44px`, `padding: 0 12px`, `font-size: 14px`, `font-weight: 450`, `font-family: Outfit`, `color: text-primary`, `caret-color: accent-primary`, `box-shadow: shadow-input` |
| Placeholder | `color: text-muted` |
| Hover | `border-color: border-base at hover opacity`, `box-shadow: shadow-input-hover` |
| Focus | `outline: 3px solid focus-ring-color`, `outline-offset: 2px`, `box-shadow: shadow-input-focus` |
| Disabled | `opacity: 0.4`, `pointer-events: none`, `cursor: not-allowed`, `box-shadow: none` |
| Transition | `border-color, box-shadow 120ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | `bg: surface`, `border-radius: 8px`, `border: 2px solid border-base at card opacity`, `box-shadow: shadow-card` |
| Hover | `box-shadow: shadow-card-hover`, `transform: translate(-0.5px, -0.5px)` |
| Focus-within | `box-shadow: shadow-card-hover`, `border-color: border-base at focus opacity` |
| Inner textarea | `font-size: 16px`, `line-height: 24.8px`, `bg: transparent`, `color: text-primary`, `placeholder-color: text-muted` |
| Transition | `transform, box-shadow, border-color 150ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Cards

| State | Properties |
|---|---|
| Rest | `bg: surface`, `border: 1.5px solid border-base at card opacity`, `border-radius: 6px`, `box-shadow: shadow-card`, `padding: 20px` |
| Hover | `box-shadow: shadow-card-hover`, `transform: translate(-1px, -1px)`, `border-color: border-base at hover opacity` |
| Focus | `outline: 3px solid focus-ring-color`, `outline-offset: 2px` (clickable cards) |
| Transition | `transform, box-shadow, border-color 120ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

**Paper Cut mode override:** Cards gain an additional inner decorative border: `box-shadow: shadow-card, inset 0 0 0 3px rgba(border-base, 0.08)`. This suggests a paper mat/frame around the content.

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `color: text-secondary`, `border-radius: 4px`, `height: 34px`, `padding: 6px 14px`, `font-size: 14px`, `font-weight: 400`, `font-family: Outfit`, `cursor: pointer` |
| Hover | `bg: recessed`, `color: text-primary` |
| Active (current) | `bg: active`, `color: text-primary`, `box-shadow: shadow-sm` |
| Active press | `transform: scale(0.97)` |
| Disabled | `pointer-events: none`, `opacity: 0.4` |
| Transition | `color, background-color 80ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

#### Chips

| State | Properties |
|---|---|
| Rest | `bg: bg`, `border: 1.5px solid border-base at subtle opacity`, `border-radius: 4px`, `height: 32px`, `padding: 0 10px`, `font-size: 14px`, `font-weight: 400`, `font-family: Outfit`, `color: text-secondary`, `box-shadow: shadow-sm` |
| Icon | 16x16px, inline-flex, gap 6px from label |
| Hover | `bg: active`, `border-color: border-base at card opacity`, `color: text-primary`, `box-shadow: shadow-card` |
| Active press | `transform: scale(0.96)`, `box-shadow: none` |
| Transition | `all 100ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

#### Toggle/Switch

| Property | Value |
|---|---|
| Track | `width: 40px`, `height: 22px`, `border-radius: 4px` (squared, not pill — physical switch) |
| Track off | `bg: recessed`, `border: 2px solid border-base at card opacity` |
| Track on | `bg: toggleActive` |
| Thumb | `width: 16px`, `height: 16px`, `bg: surface`, `border-radius: 2px` (squared thumb), `box-shadow: shadow-sm` |
| Transition | `background-color, transform 120ms cubic-bezier(0.34, 1.56, 0.64, 1)` |
| Focus-visible | Mode-specific focus ring (3px) |

Note: Toggle is squared (4px radius), not pill-shaped. Physical craft switches are rectangular.

#### User Message Bubble

| Property | Value |
|---|---|
| bg | `active` |
| border | `1.5px solid border-base at card opacity` |
| border-radius | 6px |
| padding | `10px 16px` |
| max-width | `85%` (capped at `70ch`) |
| color | `text-primary` |
| font | Outfit, 16px, weight 400 |
| alignment | Right-aligned |
| box-shadow | `shadow-sm` |

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| stamp | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Overshoot landing. The signature easing. Elements arrive with a slight bounce past target, then settle. Like stamping paper onto a surface. |
| snap | `cubic-bezier(0.25, 0.1, 0, 1)` | Quick snap. Slightly softer than step but still fast. For hover state changes. |
| settle | `cubic-bezier(0.22, 1, 0.36, 1)` | Out-quint. Gentle deceleration for larger movements. Panel open/close. |
| press | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. Button presses, basic transitions. |
| step-hard | `steps(1)` | Instant state change. Used for Riso mode registration offset animation. |

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 80ms | stamp | Color and bg. Fast with overshoot. |
| Button hover (lift) | 100ms | stamp | Transform + shadow. Paper lifts off surface. |
| Button active (press) | 60ms | press | Transform + shadow collapse. Stamp down. |
| Toggle track color | 120ms | stamp | Background-color and thumb transform. Snappy. |
| Chip hover | 100ms | stamp | All properties. Paper piece lifts. |
| Card border/shadow hover | 120ms | stamp | Border-color, box-shadow, transform. Paper lifts. |
| Input border hover | 120ms | snap | Border-color and shadow. |
| Chat input card | 150ms | snap | Shadow escalation and border change. |
| Ghost icon button | 120ms | stamp | Faster than typical themes — craft is direct. |
| Page/hero entry | 250ms | settle | `opacity: 0, translateY(16px)` to `opacity: 1, translateY(0)`. Paper sliding into frame. |
| Modal entry | 200ms | stamp | `scale(0.9)` to `scale(1)` + fade. Paper slapped onto table. |
| Panel open/close | 350ms | settle | Sidebar collapse, settings expand. Paper folding. |
| Stagger delay (Gouache) | 60ms | -- | Between staggered children. Fast cascade. |
| Stagger delay (Paper Cut) | 80ms | -- | Slightly slower — layers stacking. |
| Stagger delay (Riso) | 50ms | -- | Fastest — print press rhythm. |
| Menu item hover | 60ms | snap | Popover item bg/color change. |

#### Active Press Scale

| Element | Scale | Transform | Notes |
|---|---|---|---|
| Nav items (sidebar) | `scale(0.97)` | -- | Paper sheet pressed. |
| Chips | `scale(0.96)` | -- | Small paper piece stamped. More pronounced than typical. |
| Buttons (primary) | `translate(2px, 2px)` + `shadow: none` | Shadow collapses | Paper stamps flat against surface. Custom press — not scale. |
| Buttons (ghost) | `scale(0.92)` | -- | Strong stamp for icon buttons. Bold and physical. |
| Tabs | `scale(0.94)` | -- | Pronounced tab press. |

#### Reduced Motion (`prefers-reduced-motion: reduce`)

| Behavior | Change |
|---|---|
| Strategy | `instant` for most. No spatial movement, no overshoot. |
| All translateY entries | Replaced with 100ms opacity-only fade. |
| Press transforms | Disabled. Instant visual state change. No scale, no translate. |
| Stamp overshoot | Disabled. All `cubic-bezier(0.34, 1.56, ...)` replaced with `ease`. |
| Stagger delays | Reduced to 0ms. All children appear simultaneously. |
| Registration offset animation (Riso) | Disabled. Static offset only. |
| All hover transitions | Remain but capped at 80ms with standard easing. |
| Shadow changes | Instant. No transition on box-shadow. |

---

### Overlays

#### Popover/Dropdown

| Property | Value |
|---|---|
| bg | `surface` token |
| backdrop-filter | `none` (no blur — physical material) |
| border | `2px solid border-base at hover opacity` |
| border-radius | 6px |
| box-shadow | `shadow-popover` (`5px 5px 0px rgba(0,0,0,0.20)`) |
| padding | 6px |
| min-width | 200px |
| max-width | 320px |
| z-index | 50 |
| overflow-y | auto (with `max-height: var(--available-height)`) |
| Menu item | `padding: 6px 10px`, `border-radius: 4px`, `height: 34px`, `font-size: 14px (body-small)`, `font-family: Outfit`, `color: text-secondary`, `cursor: pointer` |
| Menu item hover | `bg: recessed`, `color: text-primary` |
| Menu item transition | `60ms snap easing` |
| Separators | `1.5px solid border-base at subtle opacity`. Visible physical dividers (unlike softer themes). |

#### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(0, 0, 0, 0.35)` |
| Overlay backdrop-filter | `none` (no blur) |
| Content bg | `surface` token |
| Content border | `2px solid border-base at hover opacity` |
| Content shadow | `shadow-modal` (`8px 8px 0px rgba(0,0,0,0.22)`) |
| Content border-radius | 6px |
| Content padding | 24px |
| Entry animation | `opacity: 0, scale(0.9)` to `opacity: 1, scale(1)`, 200ms stamp easing. Paper slapped onto table. |
| Exit animation | `opacity: 0`, 120ms press easing |
| z-index | 60 |

#### Tooltip

| Property | Value |
|---|---|
| bg | `active` token |
| color | `text-primary` |
| font-size | 12px (label role) |
| font-weight | 500 |
| font-family | Outfit |
| border | `1.5px solid border-base at card opacity` |
| border-radius | 4px |
| padding | `4px 10px` |
| box-shadow | `shadow-sm` (`2px 2px 0px rgba(0,0,0,0.12)`) |
| Arrow | None. Position-only placement. |
| Delay | 250ms before showing. |
| z-index | 55 |

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 800px | Main content column. Slightly wider for editorial infographic layouts. |
| Narrow max-width | 680px | Focused content, settings pages. |
| Sidebar width | 280px | Fixed sidebar. |
| Sidebar border | `2px solid border-base at card opacity` | Right edge. Thicker than typical — visible paper edge. |
| Header height | 52px | Top bar. Slightly taller for the bolder type scale. |
| Spacing unit | 4px | Base multiplier. |

#### Spacing Scale

`4, 6, 8, 12, 16, 20, 24, 32, 40, 48px`

Common applications:
- 4px: icon-text inline gap
- 6px: popover item padding, compact spacing
- 8px: standard element gap, chip padding
- 12px: input padding, button horizontal padding
- 16px: card content inset, sidebar item padding
- 24px: card padding, modal padding
- 32px: section separation
- 40px: major section gap (Gouache mode poster spacing)
- 48px: hero section padding

#### Density

| Mode | Density | Notes |
|---|---|---|
| Gouache | moderate | Poster layout — bold elements with deliberate spacing. Not sparse, not dense. |
| Paper Cut | comfortable | Layered paper needs room for shadows. More breathing space. |
| Riso | moderate-dense | Print layout is economical. Tighter line spacing, compact components. |

#### Responsive Notes

| Breakpoint | Width | Behavior |
|---|---|---|
| lg | 1024px | Full sidebar + content. Standard desktop. |
| md | 768px | Sidebar collapses to overlay. Content fills viewport. |
| sm | 640px | Single column. Cards stack. Hard shadows reduce from 3-5px to 2-3px offset. |

On mobile (below md):
- Sidebar becomes an overlay panel with same bg, activated by menu button
- Content max-width becomes 100% with 16px horizontal padding
- Header remains 52px but actions collapse into a popover menu
- Cards stretch to full width, padding reduces from 24px to 16px
- Shadow offsets reduce by 40% (e.g., `3px 3px` becomes `2px 2px`) to avoid overwhelming small screens
- Riso registration offset reduces from 1-2px to 0.5-1px

---

### Accessibility Tokens

| Token | Gouache Value | Paper Cut Value | Riso Value | Notes |
|---|---|---|---|---|
| Focus ring color | `rgba(46,91,186,0.65)` | `rgba(44,74,124,0.60)` | `rgba(0,120,191,0.60)` | Blue family per mode. |
| Focus ring width | `3px solid` | `3px solid` | `3px solid` | Thicker than standard. |
| Focus ring offset | `2px` | `2px` | `2px` | |
| Disabled opacity | `0.4` | `0.4` | `0.4` | Lower than typical (0.5) — bold theme needs stronger disabled signal. |
| Disabled shadow | `none` | `none` | `none` | Remove all shadows on disabled. |
| Disabled cursor | `not-allowed` | `not-allowed` | `not-allowed` | |
| Selection bg | `rgba(217,79,59,0.18)` | `rgba(212,80,60,0.20)` | `rgba(255,68,119,0.22)` | Mode accent at low opacity. |
| Selection color | `text-primary` | `text-primary` | `text-primary` | Maintains readability. |
| Scrollbar width | `thin` | `thin` | `thin` | |
| Scrollbar thumb | `rgba(border-base, 0.40)` | `rgba(border-base, 0.40)` | `rgba(border-base, 0.40)` | Slightly higher opacity for visibility on textured bg. |
| Scrollbar track | `transparent` | `transparent` | `transparent` | |
| Min touch target | 44px | 44px | 44px | All interactive elements on mobile. |
| Contrast standard | WCAG AA | WCAG AA | WCAG AA | 4.5:1 text, 3:1 large text. |

**Scrollbar CSS:**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(184, 173, 154, 0.40) transparent; /* Gouache — adjust per mode */
}
```

---

### Visual Style

#### Material

| Property | Gouache | Paper Cut | Riso |
|---|---|---|---|
| Grain | Moderate (3-4%) | Subtle (1-2%) | Moderate (4-5%) |
| Grain technique | SVG `feTurbulence` overlay (`baseFrequency="0.9"`, 2 octaves, `type="fractalNoise"`) at 3.5% opacity. Suggests canvas weave. | SVG `feTurbulence` (`baseFrequency="1.5"`, 1 octave) at 1.5% opacity. Paper fiber. | SVG `feTurbulence` (`baseFrequency="2.5"`, 1 octave) at 4.5% opacity. Risograph stochastic texture — finer, denser than paper grain. |
| Gloss | Matte. Zero reflections, zero sheen. Acrylic gouache dries to a dead-flat finish. | Matte. Construction paper is never glossy. | Matte. Riso ink soaks into uncoated stock and dries flat. |
| Blend mode | `normal` everywhere. Gouache is opaque paint — it covers. | `normal`. Paper layers are opaque. | `multiply` on overprint areas (where two inks overlap). `normal` on single-ink areas. |
| Shader bg | false | false | false |

#### Gouache Mode Rendering

- **Matte flat fills:** Every surface is a single solid color. No gradients. No inner glows. No ambient shadows.
- **Hard directional shadows:** All depth comes from hard offset shadows (3-5px down-right, zero blur). This creates a 2.5D "paper on table" effect.
- **Bold typography:** Display text is heavy (700 weight). Labels are ALL CAPS with wide tracking. The poster aesthetic demands strong typographic hierarchy.
- **Color blocking:** Large areas of solid color. Accent colors are used in panels, section backgrounds, and decorative blocks. Gouache is about bold color commitment.

#### Paper Cut Mode Rendering

- **Layer logic:** Every UI element must read as a discrete paper layer. Cards are white paper on kraft. Popovers are paper floating above. Modals are paper slapped onto the viewport.
- **Parallax depth:** On scroll, paper layers should move at slightly different rates to suggest physical stacking. Background kraft scrolls slower than content cards.
- **Die-cut edges:** Borders are thick enough (1.5-2px) to suggest the physical edge of cut paper.
- **Shadow consistency:** All shadows fall to bottom-right. Every element at the same elevation casts the same shadow. Inconsistent shadow direction breaks the paper illusion.
- **Kraft integration:** The kraft bg color is not just a background — it is the visible material between and around paper pieces. Let it show.

#### Paper Cut Parallax CSS

```css
.paper-cut-container {
  perspective: 1000px;
  overflow-y: auto;
}
.paper-layer-back {
  transform: translateZ(-50px) scale(1.05);
  /* Kraft bg layer, moves slower on scroll */
}
.paper-layer-mid {
  transform: translateZ(0px);
  /* Content cards, normal scroll speed */
}
.paper-layer-front {
  transform: translateZ(30px) scale(0.97);
  /* Floating elements, popovers, faster on scroll */
}
```

#### Riso Mode Rendering

- **3-ink system:** The entire visual composition uses only three inks: Fluorescent Pink `#FF4477`, Blue `#0078BF`, and Yellow `#FFE630`. Every other color is an overprint (two or more inks mixed on paper).
- **Overprint mixing:** Where two ink areas overlap, use CSS `mix-blend-mode: multiply` on the overlapping element. The visual result should approximate the physical mixing of transparent inks on paper.
- **Halftone texture:** Large filled areas should show halftone dot pattern. Implement via SVG filter or CSS repeating pattern:

```css
.riso-halftone {
  background-image: radial-gradient(circle, currentColor 1px, transparent 1px);
  background-size: 4px 4px;
}
```

Note: This is the ONE exception where a gradient-like pattern is permitted — it simulates halftone dots, not a color gradient. The dots are all one color at one opacity; it is a texture pattern, not a color transition. Alternative: use an SVG `<pattern>` with discrete dots for strict no-gradient compliance.

- **Registration offset:** Simulate riso misregistration by offsetting colored layers 1-2px:

```css
.riso-offset {
  position: relative;
}
.riso-offset::before {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 1px; /* 1px horizontal offset */
  color: #FF4477; /* Ink 1 */
  opacity: 0.7;
  mix-blend-mode: multiply;
  pointer-events: none;
}
```

- **Ink coverage:** Riso printing cannot do fine gradients. Solid areas are either full coverage (100% ink) or halftoned (dot pattern at reduced coverage). There is no smooth falloff.
- **Paper show-through:** In areas of low ink coverage, the paper color (`#F0EAD6`) shows through between halftone dots. This is the "white" of the design.

---

### Signature Animations

#### 1. Paper Stamp (All modes)

New elements enter by "stamping" onto the surface — arriving with slight overshoot and shadow appearing as the element lands.

- **Technique:** Element animates from `opacity: 0, scale(0.85), translateY(8px)` to `opacity: 1, scale(1), translateY(0)`. Shadow animates from `none` to `shadow-card` simultaneously.
- **Duration:** 250ms.
- **Easing:** stamp (`cubic-bezier(0.34, 1.56, 0.64, 1)`). The overshoot means the element briefly exceeds its final scale (~1.02) before settling to 1.0.
- **Paper Cut variant:** Add 50ms delay between shadow appearance and element arrival — shadow "lands" first, then paper slides in on top.
- **Reduced motion:** Instant appear. No scale, no translate.

#### 2. Layer Stack (Paper Cut mode)

Cards and panels enter in a stacked cascade where each layer slides in from slightly different angles, building up the paper stack.

- **Technique:** Staggered children enter with alternating `translateX` directions. Odd children from left (`-12px`), even children from right (`12px`), all with `translateY(8px)`. Each gains its hard shadow on arrival.
- **Stagger delay:** 80ms between layers.
- **Duration:** 200ms per layer.
- **Easing:** stamp.
- **Total for 6-layer stack:** 200ms + (5 x 80ms) = 600ms.
- **Reduced motion:** All layers appear simultaneously with 100ms opacity-only fade.

#### 3. Ink Spread (Riso mode)

Text and filled elements reveal by "printing" — ink coverage expands from 0% to 100% in a halftone-like progression.

- **Technique:** Element uses a CSS mask that transitions from a fine dot pattern (simulating sparse halftone) to solid coverage. Implement via animating `mask-size` from `2px 2px` to `0.5px 0.5px` (dots merge into solid).
- **Duration:** 300ms.
- **Easing:** settle (`cubic-bezier(0.22, 1, 0.36, 1)`).
- **Color sequence:** Each ink layer (Pink, then Blue, then Yellow) animates with 40ms offset, creating the feel of multi-pass printing.
- **Reduced motion:** Instant appear, no mask animation.

#### 4. Paint Stroke (Gouache mode)

Decorative borders or section dividers animate as if being painted — a colored line extends from left to right.

- **Technique:** `width` animates from `0%` to `100%` (use `scaleX(0)` to `scaleX(1)` with `transform-origin: left` for GPU performance). The line is 3-4px tall, using `accent-primary` color.
- **Duration:** 400ms.
- **Easing:** settle.
- **Trigger:** On scroll into view (Intersection Observer) or on page entry.
- **Reduced motion:** Line appears at full width instantly.

#### 5. Shadow Bounce (All modes)

When cards or elevated elements enter, their hard shadow briefly overshoots — extends 1-2px beyond final position, then settles back. This reinforces the physical paper metaphor (paper bounces slightly when placed).

- **Technique:** `box-shadow` animates through three keyframes:
  - 0%: `none`
  - 60%: `5px 5px 0px rgba(0,0,0,0.18)` (overshoot)
  - 100%: `3px 3px 0px rgba(0,0,0,0.15)` (settle to rest)
- **Duration:** 300ms.
- **Easing:** stamp.
- **Reduced motion:** Shadow appears at final value instantly.

---

### 3-Mode Comparison Table

| Dimension | Gouache | Paper Cut | Riso |
|---|---|---|---|
| **Background** | Strong matte (`#F5F0E6` Poster Board) | Kraft paper (`#DDD0B8` Light Kraft) | Uncoated stock (`#F0EAD6` French Paper) |
| **Color strategy** | Bold saturated primaries from paint tubes | Kraft + white + limited paper colors | 3 inks + overprints only |
| **Shadow opacity** | 1.3x standard (bolder) | Standard | Pink-tinted shadows |
| **Text transform** | Buttons + labels ALL CAPS | Labels only ALL CAPS | Buttons + labels ALL CAPS |
| **Display weight** | 700 (heavy) | 600 (medium-bold) | 800 (black) |
| **Body size** | 16px | 16px | 15px (tighter for print) |
| **Button label** | UPPERCASE, tracked | Sentence case | UPPERCASE, heavily tracked |
| **Toggle radius** | 4px (squared) | 4px (squared) | 4px (squared) |
| **Grain intensity** | 3-4% (canvas weave) | 1-2% (paper fiber) | 4-5% (riso stochastic) |
| **Blend mode** | normal (opaque paint) | normal (opaque paper) | multiply (on overprints) |
| **Registration offset** | None | None | 1-2px misalignment |
| **Halftone texture** | None | None | Yes (radial dot pattern) |
| **Stagger delay** | 60ms (fast poster) | 80ms (layer stacking) | 50ms (press rhythm) |
| **Density** | Moderate | Comfortable | Moderate-dense |
| **Parallax** | None | Yes (layer depth) | None |
| **Decorative borders** | Paint stroke animation | Die-cut edges (thick) | Ink line with offset |
| **Max content width** | 800px | 800px | 800px |
| **Unique feature** | Color blocking, bold fills | Paper layer parallax | 3-ink overprint system |
| **Feel** | Painted poster | Craft paper collage | Risograph print |

---

### Riso Ink System Reference

This section documents the complete ink mixing system for Riso mode. All colors visible in Riso mode must be traceable to this chart.

#### Primary Inks

| Ink | Name | Hex | Coverage | Usage |
|---|---|---|---|---|
| Ink 1 | Fluorescent Pink | `#FF4477` | Full / Halftone | Accent, CTA, emphasis, hot elements |
| Ink 2 | Blue | `#0078BF` | Full / Halftone | Structure, secondary text, cool elements |
| Ink 3 | Yellow | `#FFE630` | Full / Halftone | Highlights, warnings, warm accents |

#### Overprint Mixing Chart

| Combination | Visual Result | Hex | CSS Technique | Usage |
|---|---|---|---|---|
| Pink 100% + Blue 100% | Deep Violet | `#6B3FA0` | `mix-blend-mode: multiply` on overlapping layers | Links, visited states, secondary emphasis |
| Pink 100% + Yellow 100% | Hot Orange | `#FF7733` | `mix-blend-mode: multiply` | Warning states, warm highlights |
| Blue 100% + Yellow 100% | Green | `#3D9B4A` | `mix-blend-mode: multiply` | Success states, positive indicators |
| Pink 60% + Blue 40% | Warm Purple | `#9955AA` | `opacity: 0.6` on pink layer, `opacity: 0.4` on blue | Hover states on violet elements |
| Pink 100% + Blue 100% + Yellow 100% | Rich Black | `#2A2030` | Triple overlap with multiply | Text primary, deepest values |
| Any ink at 30% coverage | Halftone tint | Varies | Halftone dot pattern at 30% density | Backgrounds, subtle fills, disabled states |

#### Implementation Rules

1. **Never introduce a 4th ink.** If a new color is needed, it must be achievable through mixing the 3 existing inks at different coverage levels.
2. **Overprint areas use `mix-blend-mode: multiply`.** This is how physical ink mixing works — light is subtracted.
3. **Halftone = reduced coverage.** To make a lighter tint of any ink, use the halftone dot pattern at reduced density, not opacity. (In practice, CSS opacity is an acceptable shorthand, but the visual intent is halftone.)
4. **Registration offset is non-negotiable.** Where two or more inks overlap, a 1-2px offset between layers signals the analog process. Without it, the overprints look digital.
5. **Paper is the lightest value.** There is no "white ink." White is the paper (`#F0EAD6`) showing through.

---

### Dark Mode Variant

This theme is natively light across all three modes. The dark mode variant inverts the surface hierarchy while preserving the physical craft metaphor. Dark mode represents "working at night in the print studio" — surfaces become dark paper/board, inks and paint remain vivid.

#### Dark Mode Palette (Shared Structure, Per-Mode Values)

**Gouache Dark:**

| Token | Light Hex | Dark Hex | Notes |
|---|---|---|---|
| page | `#E8E0D0` | `#121010` | Dark studio wall. Near-black with warm cast. |
| bg | `#F5F0E6` | `#1E1A16` | Dark poster board. Warm charcoal. |
| surface | `#FFFBF2` | `#2A2520` | Dark card stock. Warm dark brown. |
| recessed | `#DDD5C4` | `#161310` | Dark recessed. Deeper than bg. |
| active | `#D1C9B8` | `#342E28` | Dark pressed state. Slightly lighter than surface. |
| text-primary | `#1A1714` | `#F5F0E6` | Warm cream. Inverted from light bg. |
| text-secondary | `#5C5549` | `#B8AFA0` | Warm light gray. |
| text-muted | `#948B7D` | `#7A726A` | Warm mid-gray. |
| accent-primary | `#D94F3B` | `#E0604C` | Cadmium Red, slightly lifted for dark contrast. |
| accent-secondary | `#2E5BBA` | `#4A7AD4` | Ultramarine, slightly lifted. |

**Paper Cut Dark:**

| Token | Light Hex | Dark Hex | Notes |
|---|---|---|---|
| page | `#C4A882` | `#14110E` | Dark kraft. Very deep warm brown. |
| bg | `#DDD0B8` | `#201C16` | Dark light kraft. |
| surface | `#F8F4EC` | `#2C2720` | Dark white card. Warm dark surface. |
| recessed | `#B89E7E` | `#161210` | Dark kraft shadow. |
| active | `#CABFA6` | `#383228` | Dark pressed kraft. |
| text-primary | `#201C16` | `#F0E8DA` | Warm cream text. |
| text-secondary | `#665D50` | `#AEA494` | Warm light brown. |
| text-muted | `#998C78` | `#786E60` | Warm mid-brown. |
| accent-primary | `#D4503C` | `#E06050` | Red paper, lifted. |
| accent-secondary | `#2C4A7C` | `#4A70AA` | Navy paper, lifted. |

**Riso Dark:**

| Token | Light Hex | Dark Hex | Notes |
|---|---|---|---|
| page | `#E8E0D0` | `#100E0C` | Dark newsprint. Near-black. |
| bg | `#F0EAD6` | `#1C1816` | Dark French paper. |
| surface | `#FAF6EC` | `#28241E` | Dark bright stock. |
| recessed | `#DDD5C2` | `#141210` | Dark aged stock. |
| active | `#D0C8B6` | `#342E26` | Dark thumbed stock. |
| text-primary | `#2A2030` | `#F0EAD6` | Paper color becomes text. |
| text-secondary | `#0078BF` | `#4A9AD6` | Blue ink, lifted for dark. |
| text-muted | `#8E98A4` | `#6A7480` | Faded ink on dark stock. |
| accent-primary | `#FF4477` | `#FF5588` | Fluorescent Pink. Slightly lifted. |
| accent-secondary | `#0078BF` | `#2A96DD` | Blue. Slightly lifted. |

#### Dark Mode Rules

- Surfaces darken as they recede: `page` (darkest) < `bg` < `surface` (lightest dark surface). Elevation is signaled by lightening.
- Accent colors lift slightly (+10-15% lightness) to maintain contrast on dark backgrounds.
- Hard shadows shift from black-based to slightly lighter: `rgba(0,0,0,0.25)` becomes `rgba(0,0,0,0.40)`. Shadows need more opacity to be visible on dark surfaces.
- Grain overlay switches to `screen` blend mode (was `normal` or `multiply` in light mode).
- Riso overprint areas still use `multiply` but on the ink layers, not on the dark surface itself. The dark paper becomes the base.
- Border opacity system remains the same percentages, but border base colors shift to lighter warm grays for visibility.
- Apply `-webkit-font-smoothing: antialiased` (essential for light text on dark).
- Paper Cut parallax depth is preserved; darker kraft just replaces lighter kraft as the visible material between layers.
- Registration offset (Riso) remains at 1-2px.

#### Dark Mode Shadow Tokens

| Token | Dark Value |
|---|---|
| shadow-sm | `2px 2px 0px rgba(0,0,0,0.20)` |
| shadow-card | `3px 3px 0px rgba(0,0,0,0.28)` |
| shadow-card-hover | `4px 4px 0px rgba(0,0,0,0.32)` |
| shadow-popover | `5px 5px 0px rgba(0,0,0,0.35)` |
| shadow-modal | `8px 8px 0px rgba(0,0,0,0.38)` |

All shadows remain hard directional (zero blur) in dark mode.

---

### Data Visualization

| Property | Gouache | Paper Cut | Riso |
|---|---|---|---|
| Categorical palette | Cadmium Red `#D94F3B`, Ultramarine `#2E5BBA`, Chrome Yellow `#E8A917`, Viridian `#2E8B57`, Cerulean `#3A7CC2` | Red Paper `#D4503C`, Navy `#2C4A7C`, Mustard `#D49B20`, Forest `#3B7A4A`, Sky `#4A80B0` | Pink `#FF4477`, Blue `#0078BF`, Yellow `#FFE630`, Violet (overprint) `#6B3FA0`, Green (overprint) `#3D9B4A` |
| Sequential ramp | Cadmium single-hue: `#F5D0C5` -> `#E8A090` -> `#D94F3B` -> `#B8382A` -> `#7A2018` | Red Paper single-hue: `#F0CCC5` -> `#E09888` -> `#D4503C` -> `#A83828` -> `#6C2018` | Pink single-coverage: halftone 20% -> 40% -> 60% -> 80% -> 100% of `#FF4477` |
| Diverging ramp | Ultramarine-to-Cadmium: `#2E5BBA` -> `#7A90C8` -> `#F5F0E6` (center) -> `#E8A090` -> `#D94F3B` | Navy-to-Red: `#2C4A7C` -> `#6A80A0` -> `#F8F4EC` (center) -> `#E09888` -> `#D4503C` | Blue-to-Pink: `#0078BF` -> `#6B3FA0` (overprint center) -> `#FF4477` |
| Grid style | low-ink. Axes in text-muted, gridlines in border-base at 8% opacity. | low-ink. Kraft-colored gridlines. | low-ink. Blue ink at 15% for gridlines. |
| Max hues per chart | 5 | 4 | 3 (inks only; overprints permitted as 4th/5th) |
| Philosophy | annotated. Labels on data points, strong typographic hierarchy. | annotated. Labels cut from paper, positioned near data. | quantized. Data shown in discrete ink steps, not smooth. |
| Number formatting | IBM Plex Mono, `font-variant-numeric: tabular-nums`, right-aligned. | Same. | Same. |

---

### Mobile Notes

#### Effects to Disable

- **Grain overlay (all modes):** Remove SVG `feTurbulence` filter on mobile. Canvas compositing is expensive on mobile Safari.
- **Paper Cut parallax:** Disable all `translateZ` and perspective transforms on mobile. Layers scroll normally.
- **Riso registration offset animation:** Keep static offset but disable any animated misregistration.
- **Shadow Bounce signature animation:** Disable overshoot. Shadows appear at final value directly.
- **Riso halftone dot pattern:** Replace `background-image` dot pattern with solid fill at reduced opacity. Repeating patterns at 4px scale cause rendering jitter on some mobile GPUs.

#### Sizing Adjustments

- **Shadow offsets:** Reduce all hard shadow offsets by 40% on screens below 640px. `3px 3px` becomes `2px 2px`. `5px 5px` becomes `3px 3px`. Large shadows overwhelm small mobile screens.
- **Border widths:** Reduce all borders by 0.5px on mobile. `2px` becomes `1.5px`. `1.5px` becomes `1px`.
- **Touch targets:** All interactive elements minimum 44px. Sidebar items at 34px on desktop expand to 44px on mobile.
- **Card padding:** Reduce from 24px to 16px on screens below 640px.
- **Content padding:** 16px horizontal on mobile.
- **Typography:** Display role reduces from mode-specific size to `clamp(28px, 7vw, 42px)`. Labels reduce from 11-12px to `max(11px, 2.8vw)`.
- **Stagger delays:** Halve all stagger delays on mobile for snappier feel.

#### Performance Notes

- This theme is moderately performance-friendly. Hard shadows (zero blur) are cheaper than blurred shadows.
- Primary concern is Riso mode halftone dot patterns on mobile — prefer solid fills with opacity.
- Paper Cut parallax uses CSS transforms (GPU-composited) but adds complexity on mobile scroll — disable.
- Grain overlay is the most expensive element. Disable on all mobile viewports.
- No WebGL, no canvas elements required for base theme. Canvas-based visualizations are additive.

---

### Implementation Checklist

- [ ] **Fonts loaded:** Bricolage Grotesque (variable, opsz 12-96, wght 200-800), Outfit (variable, 100-900), IBM Plex Mono (100-700) via Google Fonts with `font-display: swap`
- [ ] **CSS custom properties defined:** All color tokens per mode, shadow tokens, border tokens, radius tokens, spacing scale, motion easings, layout values as `:root` variables
- [ ] **Mode switching implemented:** CSS class or data attribute (`data-mode="gouache|papercut|riso"`) toggles all mode-specific tokens
- [ ] **Font smoothing applied:** `-webkit-font-smoothing: antialiased` on `<html>`
- [ ] **Typography matrix implemented:** All 10 roles per mode with correct family, size, weight, line-height, letter-spacing, text-transform
- [ ] **Family switch boundary respected:** Bricolage Grotesque for Display/Heading/Subheading only. Outfit for all other roles.
- [ ] **ZERO gradients enforced:** No `linear-gradient`, `radial-gradient`, or `conic-gradient` on any surface. Audit all CSS for gradient usage.
- [ ] **Hard shadows enforced:** All `box-shadow` values have `0` blur radius. No soft shadows anywhere.
- [ ] **Border-radius applied correctly:** sm (4px), md (6px), lg (8px). No pill shapes (9999px radius) except as explicit override. Toggle/switch uses 4px, not pill.
- [ ] **Shadow tokens applied per state:** rest/hover/active on buttons (lift/stamp pattern), rest/hover on cards, rest/hover/focus on inputs
- [ ] **Border opacity system implemented:** All borders use mode-specific base color at correct opacity (subtle 12%, card 22%, hover 35%, focus 50%)
- [ ] **Focus ring on all interactive elements:** 3px solid mode-specific blue, offset 2px, on `:focus-visible`
- [ ] **Disabled states complete:** opacity 0.4 + pointer-events none + cursor not-allowed + shadow none
- [ ] **`prefers-reduced-motion` media query present:** All stamp easings, parallax, registration offsets, and shadow bounce disabled
- [ ] **Scrollbar styled:** `scrollbar-width: thin`, `scrollbar-color: rgba(border-base, 0.40) transparent`
- [ ] **`::selection` styled per mode:** Mode-specific accent at 18-22% opacity
- [ ] **Touch targets >= 44px on mobile**
- [ ] **State transitions match motion map:** stamp easing for interactive elements, settle for large movements. No global `transition: all 0.2s`.
- [ ] **Riso 3-ink system validated:** Every visible color traceable to Ink 1, Ink 2, Ink 3, or documented overprint
- [ ] **Riso registration offset implemented:** 1-2px offset on overprint layers via CSS pseudo-elements or offset positioning
- [ ] **Riso halftone texture applied:** Large filled areas show dot pattern (SVG pattern or CSS radial)
- [ ] **Paper Cut parallax implemented:** CSS `perspective` + `translateZ` layers with scroll speed differentiation
- [ ] **Paper Cut parallax disabled on mobile:** Feature-detect or breakpoint gate
- [ ] **Grain overlay implemented per mode:** SVG feTurbulence at mode-specific frequency and opacity
- [ ] **Dark mode variant tested:** All token swaps applied, shadow opacity increased, text contrast verified WCAG AA
- [ ] **3-mode comparison tested:** All mode-specific overrides (typography, shadow, grain, special features) verified in isolation
- [ ] **Data visualization tokens applied:** Mode-specific categorical palette, sequential ramp, grid style, number formatting with IBM Plex Mono tabular-nums
