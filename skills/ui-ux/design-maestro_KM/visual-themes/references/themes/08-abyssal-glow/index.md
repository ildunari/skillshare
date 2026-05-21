# Abyssal Glow — Quick Reference

> Darkness as canvas, light as language -- glow-based depth on near-black surfaces.

**Best for:** Developer tools, creative dashboards, music production UIs, cyberpunk-aesthetic apps, data monitoring panels, gaming interfaces, AI chat interfaces

**Mode Variants:** Electric (cyberpunk cyan), Organic (bioluminescent teal), Signal (urban pink/blue)

---

## Color Tokens

### Electric Mode

| Token | Hex | Role |
|---|---|---|
| page | `#050510` | Violet-black canvas (L=0.06) |
| bg | `#0A0A1A` | Primary surface, sidebar |
| surface | `#101028` | Elevated cards, inputs |
| recessed | `#030308` | Code blocks, inset areas |
| active | `#181838` | Active/pressed states |
| accent-primary | `#00E5FF` | Electric cyan CTA, glow source |
| accent-secondary | `#FF00AA` | Hot magenta accent |
| border-color | `#1A3A4A` | Cyan-tinted edge |
| success | `#00FF88` | Neon green |
| warning | `#FFB800` | Amber glow |
| danger | `#FF2244` | Hot red |
| info | `#00E5FF` | Electric cyan |

### Organic Mode

| Token | Hex | Role |
|---|---|---|
| page | `#04141A` | Teal-black ocean (L=0.08) |
| bg | `#0A1E26` | Midnight reef |
| surface | `#0E2830` | Deep current |
| recessed | `#020E12` | Abyss |
| active | `#143038` | Bio pulse |
| accent-primary | `#00DDCC` | Bioluminescent cyan |
| accent-secondary | `#FF66AA` | Jellyfish pink |
| border-color | `#0E3A3A` | Deep teal |
| success | `#00DD88` | Sea green |
| warning | `#FFAA44` | Coral |
| danger | `#FF4466` | Anemone red |
| info | `#00DDCC` | Bioluminescent cyan |

### Signal Mode

| Token | Hex | Role |
|---|---|---|
| page | `#0A0A0E` | Grey-black asphalt (L=0.05) |
| bg | `#121216` | Charcoal |
| surface | `#1A1A22` | Dark steel |
| recessed | `#060608` | Pitch |
| active | `#222230` | Gunmetal |
| accent-primary | `#FF0066` | Neon pink CTA |
| accent-secondary | `#0088FF` | Neon blue |
| border-color | `#2A2A34` | Steel grey |
| success | `#00EE66` | Signal green |
| warning | `#FFCC00` | Signal amber |
| danger | `#FF2233` | Signal red |
| info | `#0088FF` | Neon blue |

### Shared Text Tokens (All Modes)

| Token | Hex | Role |
|---|---|---|
| text-primary | `#E8ECF0` | Headings, body (16.8:1 contrast) |
| text-secondary | `#8899AA` | Secondary labels (7.2:1 contrast) |
| text-muted | `#667A8A` | Placeholders, metadata (4.6:1 contrast) |
| text-onAccent | `#050510` | Text on bright backgrounds |

### Special Tokens

| Token | Value |
|---|---|
| inlineCode | `var(--accent-primary)` at 80% lightness |
| toggleActive | `var(--accent-primary)` |
| selection | `var(--accent-primary)` at 25% opacity |

---

## Typography

| Role | Family | Size | Weight | Line-height | Spacing | Usage |
|---|---|---|---|---|---|---|
| Display | Sora | 36px | 700 | 1.1 | -0.03em | Hero titles, page names |
| Heading | Sora | 22px | 600 | 1.27 | -0.015em | Section titles |
| Subheading | Sora | 18px | 600 | 1.33 | -0.01em | Subsection titles |
| Body | Manrope | 16px | 400 | 1.5 | normal | Primary text, UI body |
| Body Small | Manrope | 14px | 400 | 1.43 | normal | Sidebar, form labels |
| Button | Sora | 14px | 600 | 1.4 | 0.01em | Button labels |
| Input | Manrope | 14px | 400 | 1.4 | normal | Form input text |
| Code | Fira Code | 0.9em | 400 | 1.5 | normal | Inline code, blocks |
| Label | Manrope | 12px | 500 | 1.33 | 0.04em | Metadata, timestamps |

**Fonts:** Sora (600, 700), Manrope (400, 500), Fira Code (400)

---

## Elevation System

**Strategy:** `glow` — No traditional shadows. Elevation = luminance intensity.

### Key Glow Tokens

| Token | Structure | Usage |
|---|---|---|
| glow-none | `none` | Flat surfaces, dormant elements |
| glow-subtle | 1-layer, 4px blur, 8% opacity | Borders at rest, separator shimmer |
| glow-soft | 2-layer (6px + 15px), 10%+6% | Cards at rest |
| glow-medium | 3-layer (8px + 24px + 48px), 15%+8%+4% | Hovered cards, focused inputs |
| glow-strong | 3-layer (10px + 30px + 60px), 20%+12%+6% | Primary CTA, active buttons |
| glow-intense | 3-layer (12px + 40px + 80px), 30%+15%+8% | Focus rings, modal glow |

**RGB Decomposition (per mode):**
- Electric: `--glow-rgb: 0, 229, 255`
- Organic: `--glow-rgb: 0, 221, 204`
- Signal: `--glow-rgb: 255, 0, 102`

---

## Border System

**Base color:** `var(--border-color)` — cyan-tinted (Electric), teal-tinted (Organic), neutral grey (Signal)

**Widths:** 0.5px (hairline), 1px (default), 1.5px (medium), 2px (heavy)

**Opacity Scale:**
- Subtle: 10% (dormant edges)
- Card: 18% (card borders at rest)
- Hover: 25% (interactive feedback)
- Focus: 35% (focused before glow ring)

**Focus Ring (Glow Ring):**
```css
box-shadow:
  0 0 0 2px var(--page),           /* gap ring */
  0 0 0 4px rgba(var(--glow-rgb), 0.50),  /* solid ring */
  0 0 12px rgba(var(--glow-rgb), 0.30);   /* bloom */
```

---

## Motion Personality

### Per-Mode Easings

| Mode | Primary Easing | Character | Duration Range |
|---|---|---|---|
| Electric | `cubic-bezier(0.12, 0.8, 0.3, 1)` (sharp-out) | Fast, aggressive | 60ms–200ms |
| Organic | `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-quint) | Slow, fluid | 120ms–800ms |
| Signal | `cubic-bezier(0.4, 0, 0.2, 1)` (ease-in-out) | Medium, precise | 80ms–350ms |

### Active Press Scale

- Nav items: 0.985
- Chips: 0.98
- Buttons: 0.97
- Tabs: 0.96

### Reduced Motion

- Electric: Disable phosphor trail, flicker pulse
- Organic: Disable breathing pulse, bioluminescent drift, wave entry
- Signal: Disable scan-line sweep, glitch error
- All modes: Keep glow transitions (luminance changes, not motion)

---

## Key Components

### Primary Button

| State | Properties |
|---|---|
| Rest | bg `var(--accent-primary)`, radius 8px, h 36px, padding `0 18px`, glow-strong |
| Hover | glow-intense, brightness 110% |
| Active | scale(0.97), glow-medium |
| Focus | glow ring |
| Disabled | opacity 0.35, glow-none |

### Text Input

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, border 1px `var(--border-color)` at 18%, radius 8px, h 44px, glow-none |
| Hover | border at 25%, glow-subtle |
| Focus | border `var(--accent-primary)` at 40%, glow-medium + glow ring |

### Card

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, border 1px at 18%, radius 12px, glow-subtle |
| Hover | border at 25%, glow-medium |

---

## Section Index

| Section | Line |
|---|---|
| Identity & Philosophy | 69 |
| Color System | 92 |
| Typography Matrix | 215 |
| Elevation System | 249 |
| Border System | 310 |
| Component States | 365 |
| Motion Map | 456 |
| Layout Tokens | 502 |
| Accessibility Tokens | 548 |
| Overlays | 603 |
| Visual Style | 644 |
| Signature Animations | 699 |
| Mode Variant Comparison | 809 |
| Mobile Notes | 831 |
| Implementation Checklist | 866 |

---

**Decision Principle:** "Does this element glow from within, or is it painted on? If it looks painted on, it does not belong."
