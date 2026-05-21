# Print & Paper — Quick Reference
> Physical craft made digital | 3 modes: Gouache, Paper Cut, Riso | Schema v2

## Identity
**Philosophy:** Craft vs. precision. Made-by-hand surfaces (matte fills, hard shadows, texture) with pixel-perfect engineering. Physical media: paint, paper, ink.

**Core rule:** ZERO gradients. Everything is flat color. Hard-edged shadows only (blur radius = 0).

**Decision principle:** "Could this be made with paint, paper, or ink? If it requires a screen, simplify it."

---

## Color Tokens (Complete)

### Gouache Mode
| Token | Hex | Role |
|---|---|---|
| page | `#E8E0D0` | Studio Wall — deepest background |
| bg | `#F5F0E6` | Poster Board — primary surface |
| surface | `#FFFBF2` | Cream Card — elevated |
| recessed | `#DDD5C4` | Raw Canvas — code blocks |
| active | `#D1C9B8` | Pressed Linen — active states |
| text-primary | `#1A1714` | India Ink — headings, body |
| text-secondary | `#5C5549` | Graphite — secondary labels |
| text-muted | `#948B7D` | Chalk Dust — placeholders |
| text-onAccent | `#FFF8EE` | Gesso White — text on accents |
| border-base | `#B8AD9A` | Kraft Edge — variable opacity |
| accent-primary | `#D94F3B` | Cadmium Red — CTA |
| accent-secondary | `#2E5BBA` | Ultramarine — secondary |
| success | `#2E8B57` | Viridian — positive |
| warning | `#E8A917` | Chrome Yellow — caution |
| danger | `#CC3333` | Vermillion — error |
| info | `#3A7CC2` | Cerulean — informational |
| inlineCode | `#9B4DCA` | Purple-violet code |
| toggleActive | `#2E5BBA` | Ultramarine toggle |
| selection | `rgba(217,79,59,0.18)` | ::selection bg |

### Paper Cut Mode
| Token | Hex | Role |
|---|---|---|
| page | `#C4A882` | Kraft Brown — worktable |
| bg | `#DDD0B8` | Light Kraft — base |
| surface | `#F8F4EC` | White Card — elevated |
| recessed | `#B89E7E` | Dark Kraft — inset |
| active | `#CABFA6` | Pressed Kraft — active |
| text-primary | `#201C16` | Cut Black — body |
| text-secondary | `#665D50` | Charcoal Paper — labels |
| text-muted | `#998C78` | Kraft Shadow — meta |
| text-onAccent | `#F8F4EC` | White Card — on color |
| border-base | `#A89880` | Cut Edge — borders |
| accent-primary | `#D4503C` | Red Paper — CTA |
| accent-secondary | `#2C4A7C` | Navy Paper — secondary |
| success | `#3B7A4A` | Forest Paper — positive |
| warning | `#D49B20` | Mustard Paper — caution |
| danger | `#B83030` | Brick Paper — error |
| info | `#4A80B0` | Sky Paper — info |
| inlineCode | `#7B5EA7` | Violet code |
| toggleActive | `#2C4A7C` | Navy toggle |
| selection | `rgba(212,80,60,0.20)` | ::selection bg |

### Riso Mode
| Token | Hex | Role |
|---|---|---|
| page | `#E8E0D0` | Newsprint — deepest |
| bg | `#F0EAD6` | French Paper — base |
| surface | `#FAF6EC` | Bright Stock — elevated |
| recessed | `#DDD5C2` | Aged Stock — inset |
| active | `#D0C8B6` | Thumbed Stock — active |
| text-primary | `#2A2030` | Rich Black — 3-ink mix |
| text-secondary | `#0078BF` | Blue Ink — labels |
| text-muted | `#8E98A4` | Faded Ink — meta |
| text-onAccent | `#FAF6EC` | Paper showing through |
| border-base | `#B0A898` | Halftone Edge — borders |
| accent-primary | `#FF4477` | Fluorescent Pink — Ink 1 |
| accent-secondary | `#0078BF` | Blue — Ink 2 |
| Ink 3 | `#FFE630` | Yellow — tertiary ink |
| Overprint: Violet | `#6B3FA0` | Pink + Blue |
| Overprint: Orange | `#FF7733` | Pink + Yellow |
| Overprint: Green | `#3D9B4A` | Blue + Yellow |
| inlineCode | `#6B3FA0` | Violet overprint |
| toggleActive | `#0078BF` | Blue Ink toggle |
| selection | `rgba(255,68,119,0.22)` | ::selection bg |

### Fixed Colors
- `alwaysBlack`: `#000000` (shadow base)
- `alwaysWhite`: `#FFFFFF` (emergency only)

### Opacity System
- **subtle**: 12% — lightest separation
- **card**: 22% — card borders, paper edges
- **hover**: 35% — hover states
- **focus**: 50% — focus borders

---

## Typography (All 9 Roles)

**Fonts:** Bricolage Grotesque (Display/Heading), Outfit (Body-Caption), IBM Plex Mono (Code)

### Gouache Mode
| Role | Family | Size | Weight | Line-height | Spacing | Features |
|---|---|---|---|---|---|---|
| Display | Bricolage | 42px | 700 | 1.1 | -0.02em | opsz 48 |
| Heading | Bricolage | 26px | 600 | 1.2 | -0.01em | opsz 28 |
| Subheading | Bricolage | 20px | 600 | 1.25 | normal | — |
| Body | Outfit | 16px | 400 | 1.55 | normal | — |
| Body Small | Outfit | 14px | 400 | 1.45 | normal | — |
| Button | Outfit | 14px | 600 | 1.4 | 0.02em | UPPERCASE |
| Input | Outfit | 14px | 450 | 1.4 | normal | — |
| Label | Outfit | 11px | 600 | 1.33 | 0.08em | UPPERCASE |
| Code | IBM Plex | 0.9em | 400 | 1.5 | normal | tabular-nums |
| Caption | Outfit | 12px | 400 | 1.33 | normal | — |

### Paper Cut Mode
| Role | Size | Weight | Spacing | Features |
|---|---|---|---|---|
| Display | 38px | 600 | -0.01em | opsz 40 |
| Heading | 24px | 500 | normal | — |
| Subheading | 18px | 500 | normal | — |
| Body | 16px | 400 | normal | — |
| Body Small | 14px | 400 | normal | — |
| Button | 14px | 500 | 0.01em | Sentence case |
| Input | 14px | 450 | normal | — |
| Label | 12px | 500 | 0.04em | UPPERCASE |
| Code | 0.9em | 400 | normal | tabular-nums |
| Caption | 12px | 400 | normal | — |

### Riso Mode
| Role | Size | Weight | Spacing | Features |
|---|---|---|---|---|
| Display | 40px | 800 | -0.03em | opsz 48, max ink |
| Heading | 24px | 700 | -0.01em | — |
| Subheading | 18px | 600 | normal | — |
| Body | 15px | 400 | 0.01em | Smaller for texture |
| Body Small | 13px | 400 | 0.01em | — |
| Button | 13px | 700 | 0.06em | UPPERCASE, tracked |
| Input | 14px | 450 | normal | — |
| Label | 11px | 700 | 0.1em | UPPERCASE, max track |
| Code | 0.85em | 400 | normal | tabular-nums |
| Caption | 11px | 400 | 0.01em | — |

**Font smoothing:** antialiased everywhere. Text-wrap: balance (headings), pretty (body).

---

## Elevation (Hard Shadows Only)

**Strategy:** Zero blur. Hard directional offsets (light from top-left, shadows bottom-right). Paper on table.

### Shadow Tokens
| Token | Value | Usage |
|---|---|---|
| shadow-sm | `2px 2px 0px rgba(0,0,0,0.12)` | Tags, chips |
| shadow-card | `3px 3px 0px rgba(0,0,0,0.15)` | Cards at rest |
| shadow-card-hover | `4px 4px 0px rgba(0,0,0,0.18)` | Cards hover |
| shadow-input | `2px 2px 0px rgba(0,0,0,0.10)` | Inputs rest |
| shadow-input-hover | `3px 3px 0px rgba(0,0,0,0.14)` | Inputs hover |
| shadow-input-focus | `3px 3px 0px rgba(0,0,0,0.18)` | Inputs focus |
| shadow-popover | `5px 5px 0px rgba(0,0,0,0.20)` | Menus, popovers |
| shadow-modal | `8px 8px 0px rgba(0,0,0,0.22)` | Modals |

**Mode adjustments:**
- **Gouache:** Multiply all opacity by 1.3x (bolder)
- **Riso:** Use pink-tinted shadows `rgba(255,68,119,0.15)` instead of black

**Backdrop-filter:** NONE. Physical materials don't frost.

---

## Border System

**Base colors:**
- Gouache: `#B8AD9A` (Kraft Edge)
- Paper Cut: `#A89880` (Cut Edge)
- Riso: `#B0A898` (Halftone Edge)

**Widths:** 1px (hairline), 1.5px (default), 2px (medium), 3px (heavy)

**Patterns:**
- subtle: 1px @ 12%
- card: 1.5px @ 22%
- hover: 2px @ 35%
- input: 2px @ 22%

**Focus ring:** 3px solid, 2px offset, blue per mode
- Gouache: `rgba(46,91,186,0.65)`
- Paper Cut: `rgba(44,74,124,0.60)`
- Riso: `rgba(0,120,191,0.60)`

---

## Motion

**Easings:**
- **stamp**: `cubic-bezier(0.34, 1.56, 0.64, 1)` — overshoot landing (signature)
- **snap**: `cubic-bezier(0.25, 0.1, 0, 1)` — quick state changes
- **settle**: `cubic-bezier(0.22, 1, 0.36, 1)` — panel open/close
- **press**: `cubic-bezier(0.4, 0, 0.2, 1)` — button presses

**Durations:**
- Sidebar: 80ms stamp
- Button hover: 100ms stamp
- Toggle: 120ms stamp
- Input: 120ms snap
- Ghost button: 120ms stamp
- Modal: 200ms stamp
- Panel: 350ms settle

**Active press:**
- Nav: scale(0.97)
- Chip: scale(0.96)
- Button: translate(2px, 2px) + shadow collapse
- Ghost: scale(0.92)

**Stagger delays:** Gouache 60ms, Paper Cut 80ms, Riso 50ms

---

## Component Quick Reference

### Button (Primary)
**Rest:** bg accent-primary, 2px border, 36px h, shadow-sm, radius 4px
**Hover:** shadow-card, translate(-1px, -1px) — paper lifts
**Active:** shadow none, translate(2px, 2px) — stamp flat
**Transition:** 100ms stamp

### Input (Text)
**Rest:** bg surface, 2px border @ card opacity, 44px h, shadow-input, radius 4px
**Hover:** border @ hover opacity, shadow-input-hover
**Focus:** 3px focus ring, shadow-input-focus
**Transition:** 120ms snap

### Card
**Rest:** bg surface, 1.5px border @ card opacity, shadow-card, radius 6px, padding 20px
**Hover:** shadow-card-hover, translate(-1px, -1px), border @ hover opacity
**Transition:** 120ms stamp

**Paper Cut override:** Add inner decorative border `inset 0 0 0 3px rgba(border-base, 0.08)`

### Toggle
**Track:** 40px × 22px, radius 4px (squared)
**Thumb:** 16px × 16px, radius 2px (squared), shadow-sm
**Transition:** 120ms stamp

---

## Layout

- **Content max-width:** 800px (wider for editorial/infographic)
- **Sidebar:** 280px, 2px border @ card opacity
- **Header:** 52px
- **Spacing:** 4, 6, 8, 12, 16, 20, 24, 32, 40, 48px

**Density:**
- Gouache: moderate
- Paper Cut: comfortable (layers need space)
- Riso: moderate-dense (print economical)

**Responsive:**
- lg (1024px): full layout
- md (768px): sidebar → overlay
- sm (640px): single column, shadows reduce 40%, borders -0.5px

---

## Signature Features

### Gouache Mode
- **Color blocking:** Bold matte fills, strong backgrounds
- **Typography:** ALL CAPS buttons + labels, heavy display (700)
- **Shadows:** 1.3x opacity (bolder)
- **Animation:** Paint stroke borders (400ms settle)

### Paper Cut Mode
- **Parallax depth:** Layers move at different scroll speeds
- **Layer logic:** Every element = discrete paper piece
- **Inner borders:** Cards get mat/frame effect
- **Shadows:** Standard opacity, consistent direction

### Riso Mode
- **3-ink system:** Pink `#FF4477`, Blue `#0078BF`, Yellow `#FFE630` only
- **Overprints:** Pink+Blue=Violet, Pink+Yellow=Orange, Blue+Yellow=Green
- **Registration offset:** 1-2px misalignment between ink layers
- **Halftone texture:** Dot pattern on large fills
- **Shadows:** Pink-tinted `rgba(255,68,119,0.15)`

---

## Accessibility

- **Focus ring:** 3px solid blue, 2px offset, all interactive
- **Disabled:** opacity 0.4, pointer-events none, shadow none
- **Selection:** mode accent @ 18-22% opacity
- **Scrollbar:** thin, border-base @ 40%
- **Min touch:** 44px mobile
- **Contrast:** WCAG AA (4.5:1 text)

**Reduced motion:**
- Instant for most
- No translateY, no overshoot, no parallax
- Stagger delays → 0ms
- Shadows instant

---

## Mobile Adjustments

**Disable:**
- Grain overlay (all modes)
- Paper Cut parallax
- Riso halftone dots (use solid @ opacity)
- Shadow bounce animation

**Reduce:**
- Shadows: -40% offset (3px→2px)
- Borders: -0.5px width
- Card padding: 24px→16px
- Stagger delays: halved

---

## Section Index (Full Spec)

| Section | Line |
|---|---|
| Identity & Philosophy | 20 |
| Color System | 41 |
| Typography Matrix | 164 |
| Elevation System | 237 |
| Border System | 286 |
| Component States | 327 |
| Motion Map | 446 |
| Overlays | 505 |
| Layout Tokens | 559 |
| Accessibility Tokens | 612 |
| Visual Style | 643 |
| Signature Animations | 727 |
| 3-Mode Comparison Table | 784 |
| Riso Ink System Reference | 812 |
| Dark Mode Variant | 846 |
| Data Visualization | 922 |
| Mobile Notes | 936 |
| Implementation Checklist | 965 |

**Full specification:** `./full.md` (987 lines)
