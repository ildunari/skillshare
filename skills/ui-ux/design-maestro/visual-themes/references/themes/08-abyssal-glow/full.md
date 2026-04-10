# Abyssal Glow — Full Theme Reference

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 69
- [Color System](#color-system) — Line 92
  - [Mode Switching Pattern](#mode-switching-pattern) — Line 96
  - [Electric Mode Palette](#electric-mode-palette) — Line 128
  - [Organic Mode Palette](#organic-mode-palette) — Line 145
  - [Signal Mode Palette](#signal-mode-palette) — Line 162
  - [Shared Text Tokens](#shared-text-tokens) — Line 179
  - [Special Tokens](#special-tokens) — Line 188
  - [Opacity System](#opacity-system) — Line 196
  - [Color Rules](#color-rules) — Line 205
- [Typography Matrix](#typography-matrix) — Line 215
  - [Font Loading](#font-loading) — Line 239
- [Elevation System](#elevation-system) — Line 249
  - [Glow Pipeline](#glow-pipeline) — Line 255
  - [Glow Tokens](#glow-tokens) — Line 263
  - [Surface Hierarchy](#surface-hierarchy) — Line 292
  - [Separation Recipe](#separation-recipe) — Line 304
- [Border System](#border-system) — Line 310
  - [Widths](#widths) — Line 314
  - [Opacity Scale](#opacity-scale) — Line 323
  - [Patterns](#patterns) — Line 332
  - [Focus Ring](#focus-ring) — Line 344
- [Component States](#component-states) — Line 365
  - [Buttons (Primary)](#buttons-primary) — Line 369
  - [Buttons (Ghost / Icon)](#buttons-ghost--icon) — Line 380
  - [Text Input](#text-input) — Line 391
  - [Chat Input Card](#chat-input-card) — Line 401
  - [Cards](#cards) — Line 410
  - [Sidebar Items](#sidebar-items) — Line 418
  - [Chips](#chips) — Line 428
  - [Toggle / Switch](#toggle--switch) — Line 438
- [Motion Map](#motion-map) — Line 456
  - [Easings](#easings) — Line 460
  - [Duration × Easing × Component](#duration--easing--component) — Line 471
  - [Active Press Scale](#active-press-scale) — Line 490
- [Layout Tokens](#layout-tokens) — Line 502
  - [Spacing Scale](#spacing-scale) — Line 512
  - [Density](#density) — Line 516
  - [Radius Scale](#radius-scale) — Line 526
  - [Responsive Notes](#responsive-notes) — Line 540
- [Accessibility Tokens](#accessibility-tokens) — Line 548
  - [Reduced Motion](#reduced-motion) — Line 571
- [Overlays](#overlays) — Line 603
  - [Popover / Dropdown](#popover--dropdown) — Line 605
  - [Modal](#modal) — Line 618
  - [Tooltip](#tooltip) — Line 629
- [Visual Style](#visual-style) — Line 644
  - [Glow Rendering Pipeline](#glow-rendering-pipeline) — Line 646
  - [Vignette Fog](#vignette-fog) — Line 656
  - [Scan-Line Texture](#scan-line-texture) — Line 668
  - [Material](#material) — Line 690
- [Signature Animations](#signature-animations) — Line 699
  - [Electric Mode](#electric-mode) — Line 701
  - [Organic Mode](#organic-mode) — Line 734
  - [Signal Mode](#signal-mode) — Line 766
- [Mode Variant Comparison](#mode-variant-comparison) — Line 809
- [Mobile Notes](#mobile-notes) — Line 831
  - [Glow Simplification](#glow-simplification) — Line 833
  - [Effects to Disable on Mobile](#effects-to-disable-on-mobile) — Line 845
  - [Performance Budget](#performance-budget) — Line 853
- [Implementation Checklist](#implementation-checklist) — Line 866

---

## Identity & Philosophy

This theme treats darkness not as the absence of light but as a material -- a deep, rich canvas onto which light is painted. Every surface, every interactive element, every state change communicates through luminance: glows that bloom outward, borders that shimmer at the edge of visibility, accents that pulse like bioluminescent organisms in deep water. There are no traditional shadows here. Shadows are meaningless on a near-black canvas. Instead, elevation is expressed through glow intensity -- brighter elements are closer, dimmer elements recede.

The system ships with THREE complete visual modes, each a distinct emotional register built on the same glow-depth architecture:

- **Electric** -- Cyberpunk phosphor. Violet-black canvas, electric cyan and hot magenta. Fast, sharp, aggressive.
- **Organic** -- Bioluminescent ocean. Teal-black depths, soft cyan and jellyfish pink. Slow, breathing, alive.
- **Signal** -- Urban infrastructure. Grey-black asphalt, neon pink and neon blue. Medium-paced, utilitarian, precise.

All three share the same structural tokens (typography roles, spacing, component anatomy) but diverge in palette, motion timing, and ambient effects. Mode switching is handled via a `data-mode` attribute on the root element, swapping CSS custom properties.

**Decision principle:** "When in doubt, ask: does this element glow from within, or is it painted on? If it looks painted on, it does not belong. Light must emerge from the element itself."

**What this theme is NOT:**
- Not gradient-heavy -- glows are box-shadows and borders, not background gradients
- Not neon-maximalist -- restraint is critical; accent glow is earned, not default
- Not shadow-based -- zero `rgba(0,0,0,...)` drop shadows; all depth is luminous
- Not light-mode-friendly -- this is dark-native; a light variant would require a fundamentally different theme
- Not flat -- if your output has no `box-shadow` glow tokens, you have missed the entire point

---

## Color System

Colors are organized in three tiers: shared tokens (text, semantics) that remain constant across modes, per-mode tokens (page, bg, surface, accents, borders) that swap via `data-mode`, and computed glow tokens that reference `var(--accent-primary)` so they automatically adapt.

### Mode Switching Pattern

```css
:root, [data-mode="electric"] {
  --page: #050510;
  --bg: #0A0A1A;
  --surface: #101028;
  --accent-primary: #00E5FF;
  --accent-secondary: #FF00AA;
  --border-color: #1A3A4A;
  --glow-color: #00E5FF;
}
[data-mode="organic"] {
  --page: #04141A;
  --bg: #0A1E26;
  --surface: #0E2830;
  --accent-primary: #00DDCC;
  --accent-secondary: #FF66AA;
  --border-color: #0E3A3A;
  --glow-color: #00DDCC;
}
[data-mode="signal"] {
  --page: #0A0A0E;
  --bg: #121216;
  --surface: #1A1A22;
  --accent-primary: #FF0066;
  --accent-secondary: #0088FF;
  --border-color: #2A2A34;
  --glow-color: #FF0066;
}
```

### Electric Mode Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Violet Black | `#050510` | Deepest background. Near-black with violet undertone. OKLCH L=0.06. |
| bg | Dark Indigo | `#0A0A1A` | Primary surface background. Sidebar, main area. |
| surface | Deep Ultraviolet | `#101028` | Elevated cards, inputs, popovers. Slightly lifted from bg. |
| recessed | Void | `#030308` | Code blocks, inset areas. Darker than page. |
| active | Energized Indigo | `#181838` | Active/pressed items, selected states. Visible lift from surface. |
| accent-primary | Electric Cyan | `#00E5FF` | Primary CTA, active toggles, glow source. The signature color. |
| accent-secondary | Hot Magenta | `#FF00AA` | Secondary accent, destructive-adjacent warmth, toggle active. |
| border-color | Dim Cyan | `#1A3A4A` | Base border at variable opacity. Cyan-tinted edge. |
| success | Neon Green | `#00FF88` | Positive states. High-saturation green for dark backgrounds. |
| warning | Amber Glow | `#FFB800` | Caution states. Warm amber. |
| danger | Hot Red | `#FF2244` | Error states, destructive actions. |
| info | Electric Cyan | `#00E5FF` | Informational (same as accent-primary). |

### Organic Mode Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Teal-Black Ocean | `#04141A` | Deepest background. Deep ocean floor. OKLCH L=0.08. |
| bg | Midnight Reef | `#0A1E26` | Primary surface. Dark teal undertone. |
| surface | Deep Current | `#0E2830` | Elevated cards. Visible but quiet. |
| recessed | Abyss | `#020E12` | Code blocks, inset areas. Deepest dark. |
| active | Bio Pulse | `#143038` | Active/pressed items. Teal-shifted lift. |
| accent-primary | Bioluminescent Cyan | `#00DDCC` | Primary CTA. Warm cyan, organic feel. |
| accent-secondary | Jellyfish Pink | `#FF66AA` | Secondary accent. Soft, warm pink. |
| border-color | Deep Teal | `#0E3A3A` | Base border. Teal-green edge. |
| success | Sea Green | `#00DD88` | Positive states. Softer than Electric. |
| warning | Coral | `#FFAA44` | Caution states. Warm coral tone. |
| danger | Anemone Red | `#FF4466` | Error states. Slightly softer red. |
| info | Bioluminescent Cyan | `#00DDCC` | Informational. |

### Signal Mode Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Grey-Black Asphalt | `#0A0A0E` | Deepest background. Neutral, cold. OKLCH L=0.05. |
| bg | Charcoal | `#121216` | Primary surface. Pure neutral dark. |
| surface | Dark Steel | `#1A1A22` | Elevated cards. Cool grey. |
| recessed | Pitch | `#060608` | Code blocks, inset areas. |
| active | Gunmetal | `#222230` | Active/pressed items. |
| accent-primary | Neon Pink | `#FF0066` | Primary CTA. Hot, urgent, signal-red-pink. |
| accent-secondary | Neon Blue | `#0088FF` | Secondary accent. Cool information blue. |
| border-color | Steel Grey | `#2A2A34` | Base border. Neutral edge. |
| success | Signal Green | `#00EE66` | Positive states. |
| warning | Signal Amber | `#FFCC00` | Caution states. |
| danger | Signal Red | `#FF2233` | Error states. |
| info | Neon Blue | `#0088FF` | Informational. |

### Shared Text Tokens (All Modes)

| Token | Name | Hex | Role |
|---|---|---|---|
| text-primary | Bright White | `#E8ECF0` | Headings, body text. High luminance on dark canvas. |
| text-secondary | Cool Grey | `#8899AA` | Sidebar items, secondary labels. |
| text-muted | Dim Grey | `#667A8A` | Placeholders, timestamps, metadata. 4.6:1 contrast on `#050510`. |
| text-onAccent | Deep Black | `#050510` | Text on bright accent backgrounds. |

### Special Tokens (All Modes)

| Token | Value | Role |
|---|---|---|
| inlineCode | `var(--accent-primary)` at 80% lightness | Code text within prose. Mode-adaptive. |
| toggleActive | `var(--accent-primary)` | Toggle/switch active track. Glows. |
| selection | `var(--accent-primary)` at 25% opacity | `::selection` background. |

### Opacity System (Border on `var(--border-color)`)

| Level | Opacity | Usage |
|---|---|---|
| subtle | 10% | Dormant edges, separators at rest |
| card | 18% | Card borders, panel edges |
| hover | 25% | Hovered elements, interactive feedback |
| focus | 35% | Focused elements before glow ring takes over |

### Color Rules

- Accent color is the ONLY source of glow. Semantic colors (success, warning, danger) glow only in notification/status contexts, never on neutral UI.
- No traditional gradients on surfaces. Glow gradients exist only as `box-shadow` bloom.
- Text colors are mode-independent -- the same `#E8ECF0` / `#8899AA` / `#667A8A` across all three modes. This ensures readability regardless of mode.
- The page background must ALWAYS be below OKLCH L=0.10. If custom pages are designed, enforce this ceiling.
- Additive blending (`mix-blend-mode: screen`) is used for glow effects that overlap, preventing muddy color mixing.

---

## Typography Matrix

Sora for display and headings (geometric, futuristic, excellent at large sizes), Manrope for body text (humanist, readable, good x-height for small sizes on dark backgrounds), Fira Code for code and data (monospace, ligature-capable, technical feel).

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | sans (Sora) | 36px | 700 | 1.1 | -0.03em | -- | Hero titles, page names, large headings |
| Heading | sans (Sora) | 22px | 600 | 1.27 | -0.015em | -- | Section titles, settings headers |
| Subheading | sans (Sora) | 18px | 600 | 1.33 | -0.01em | -- | Subsection titles, card headers |
| Body | sans (Manrope) | 16px | 400 | 1.5 | normal | -- | Primary reading text, UI body |
| Body Small | sans (Manrope) | 14px | 400 | 1.43 | normal | -- | Sidebar items, form labels, secondary text |
| Button | sans (Sora) | 14px | 600 | 1.4 | 0.01em | -- | Button labels, emphasized small UI text |
| Input | sans (Manrope) | 14px | 400 | 1.4 | normal | -- | Form input text |
| Code | mono (Fira Code) | 0.9em | 400 | 1.5 | normal | liga, calt | Inline code, code blocks, data values |
| Label | sans (Manrope) | 12px | 500 | 1.33 | 0.04em | -- | Section labels, metadata, timestamps. Slightly tracked out for legibility at small size on dark bg. |

**Typographic decisions:**
- Sora's geometric letterforms echo the precision of glow effects. Its wide counters read well when text sits on near-black surfaces with luminous accents nearby.
- Manrope's x-height and open apertures are optimized for body-text readability on dark backgrounds where smaller text can lose definition.
- Fira Code's programming ligatures (`=>`, `!=`, `>=`) reinforce the developer-tool identity.
- Weight 600-700 for headings (not 400) because light text on dark backgrounds needs extra weight to maintain visual presence.
- `-webkit-font-smoothing: antialiased` is mandatory -- subpixel rendering on dark backgrounds causes color fringing.
- `text-wrap: pretty` for body text, `text-wrap: balance` for headings.

### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Manrope:wght@400;500&family=Fira+Code:wght@400&display=swap" rel="stylesheet">
```

**Fallback chain:** `"Sora", "Inter", system-ui, sans-serif` | `"Manrope", "Inter", system-ui, sans-serif` | `"Fira Code", "JetBrains Mono", ui-monospace, monospace`

---

## Elevation System

**Strategy:** `glow`

Elevation is expressed through luminance, not shadow. Higher surfaces glow more intensely. The glow pipeline is a 3-layer system: inner glow (surface luminance), outer glow (edge bloom), and bloom halo (atmospheric scatter). All glow values reference `var(--glow-color)` so they adapt automatically when the mode switches.

### Glow Pipeline (3 Layers)

Every elevated surface composes up to three glow layers in a single `box-shadow` declaration:

1. **Inner glow** -- Tight, high-opacity. Creates the sense that the surface itself emits light. Spread 0-2px, blur 4-8px.
2. **Outer glow** -- Medium spread. The visible "halo" around the element. Spread 0px, blur 12-30px.
3. **Bloom halo** -- Wide, very low opacity. Atmospheric scatter that tints the surrounding darkness. Spread 0px, blur 40-80px.

### Glow Tokens

| Token | CSS Value | Usage |
|---|---|---|
| glow-none | `none` | Flat surfaces, page background, dormant elements. |
| glow-subtle | `0 0 4px var(--glow-color, #00E5FF)` at 8% opacity | Borders at rest, separator shimmer. Barely visible. |
| glow-soft | `0 0 6px rgba(var(--glow-rgb), 0.10), 0 0 15px rgba(var(--glow-rgb), 0.06)` | Cards at rest. Two-layer: inner + outer. |
| glow-medium | `0 0 8px rgba(var(--glow-rgb), 0.15), 0 0 24px rgba(var(--glow-rgb), 0.08), 0 0 48px rgba(var(--glow-rgb), 0.04)` | Hovered cards, focused inputs. Full 3-layer pipeline. |
| glow-strong | `0 0 10px rgba(var(--glow-rgb), 0.20), 0 0 30px rgba(var(--glow-rgb), 0.12), 0 0 60px rgba(var(--glow-rgb), 0.06)` | Active buttons, primary CTA at rest. Prominent glow. |
| glow-intense | `0 0 12px rgba(var(--glow-rgb), 0.30), 0 0 40px rgba(var(--glow-rgb), 0.15), 0 0 80px rgba(var(--glow-rgb), 0.08)` | Focus rings, modal glow, maximum luminance state. |
| glow-accent-secondary | Same structure as above but using `var(--accent-secondary)` | Secondary accent glow for toggles, destructive actions, alternate highlights. |

**CSS custom property for RGB decomposition:**

```css
:root, [data-mode="electric"] {
  --glow-rgb: 0, 229, 255;    /* #00E5FF decomposed */
  --glow-sec-rgb: 255, 0, 170; /* #FF00AA decomposed */
}
[data-mode="organic"] {
  --glow-rgb: 0, 221, 204;
  --glow-sec-rgb: 255, 102, 170;
}
[data-mode="signal"] {
  --glow-rgb: 255, 0, 102;
  --glow-sec-rgb: 0, 136, 255;
}
```

### Surface Hierarchy

| Surface | Background | Glow | Usage |
|---|---|---|---|
| page | `var(--page)` | glow-none | Main canvas. Pure darkness. |
| bg | `var(--bg)` | glow-none | Sidebar, secondary areas. Slightly lifted. |
| surface | `var(--surface)` | glow-subtle (border only) | Cards, inputs, panels. |
| recessed | `var(--recessed)` | glow-none | Code blocks, inset areas. Darker than page. |
| active | `var(--active)` | glow-soft | Active/selected items. Gentle luminance. |
| overlay | `var(--surface)` | glow-medium | Popovers, dropdowns. Noticeable glow. |
| modal | `var(--surface)` | glow-strong | Modal panels. Strong luminous presence. |

### Separation Recipe

Luminous borders at low opacity + glow escalation on interaction. No visible dividers. Panels separate from the background through border luminance and surface tint -- the faintest cyan/teal/pink edge defines where a surface begins. On hover and focus, glow blooms outward, creating unmistakable depth. The darkness IS the separator.

---

## Border System

Borders in this theme are luminous edges -- faint colored lines that shimmer at the boundary between surface and void. The border color per mode is specifically chosen to complement the accent: cyan-tinted for Electric, teal-tinted for Organic, neutral steel for Signal.

### Widths

| Token | Value | Usage |
|---|---|---|
| hairline | 0.5px | Panel edges, separators. Barely there. |
| default | 1px | Card borders, input borders. Standard. |
| medium | 1.5px | Emphasized borders, active states. |
| heavy | 2px | Focus-adjacent, toggle tracks. |

### Opacity Scale (on `var(--border-color)`)

| Level | Opacity | Usage |
|---|---|---|
| subtle | 10% | Dormant panel edges, rest state separators |
| card | 18% | Card borders at rest |
| hover | 25% | Hovered cards, interactive elements |
| focus | 35% | Focused element border (before glow ring) |

### Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| panel-edge | 0.5px | `var(--border-color)` at 10% | Sidebar edges, quiet separators |
| card | 1px | `var(--border-color)` at 18% | Card borders at rest |
| card-hover | 1px | `var(--border-color)` at 25% | Card hover |
| input | 1px | `var(--border-color)` at 18% | Input rest state |
| input-hover | 1px | `var(--border-color)` at 25% | Input hover |
| input-focus | 1px | `var(--accent-primary)` at 40% | Input focus (colored) |
| separator | 0.5px | `var(--border-color)` at 10% | Internal dividers |

### Focus Ring (Glow Ring)

The focus ring is a 3-layer glow box-shadow that replaces the traditional solid ring:

- **Layer 1:** `0 0 0 2px var(--page)` -- gap ring in page color, prevents glow from bleeding into the element
- **Layer 2:** `0 0 0 4px var(--accent-primary)` at 50% -- solid colored ring
- **Layer 3:** `0 0 12px var(--accent-primary)` at 30% -- bloom halo

**Full CSS:**
```css
:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--page),
    0 0 0 4px rgba(var(--glow-rgb), 0.50),
    0 0 12px rgba(var(--glow-rgb), 0.30);
}
```

---

## Component States

All component states use glow escalation rather than background-color shifts. Hover brightens glow. Focus adds the glow ring. Active intensifies. Glow color adapts per mode via CSS custom properties.

### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `var(--accent-primary)`, border none, color `var(--text-onAccent)`, radius 8px, h 36px, padding `0 18px`, font button, box-shadow glow-strong |
| Hover | box-shadow glow-intense, brightness `filter: brightness(1.1)` |
| Active | transform `scale(0.97)`, box-shadow glow-medium (glow compresses on press) |
| Focus | glow ring appended: `0 0 0 2px var(--page), 0 0 0 4px rgba(var(--glow-rgb),0.5), 0 0 16px rgba(var(--glow-rgb),0.35)` |
| Disabled | opacity 0.35, pointer-events none, box-shadow glow-none, filter none |
| Transition | box-shadow 150ms ease-out, transform 100ms ease-out, filter 150ms ease-out |

### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid var(--border-color)` at 18%, color `var(--text-secondary)`, radius 6px, size 36x36px, box-shadow glow-none |
| Hover | border at 25%, color `var(--text-primary)`, box-shadow glow-subtle |
| Active | transform `scale(0.97)`, bg `var(--active)` |
| Focus | glow ring |
| Disabled | opacity 0.35, pointer-events none |
| Transition | all 150ms ease-out |

### Text Input

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, border `1px solid var(--border-color)` at 18%, radius 8px, h 44px, padding `0 14px`, color `var(--text-primary)`, placeholder `var(--text-muted)`, caret-color `var(--accent-primary)`, box-shadow glow-none |
| Hover | border at 25%, box-shadow glow-subtle |
| Focus | border `1px solid var(--accent-primary)` at 40%, box-shadow glow-medium + glow ring, outline none |
| Disabled | opacity 0.35, pointer-events none, bg `var(--bg)` |
| Transition | border-color 150ms ease-out, box-shadow 200ms ease-out |

### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, radius 20px, border `1px solid var(--border-color)` at 18%, box-shadow glow-soft |
| Hover | border at 25%, box-shadow glow-medium |
| Focus-within | border `1px solid var(--accent-primary)` at 35%, box-shadow glow-strong |
| Transition | all 200ms ease-out |

### Cards

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, border `1px solid var(--border-color)` at 18%, radius 12px, box-shadow glow-subtle |
| Hover | border at 25%, box-shadow glow-medium -- card glows outward on hover |
| Transition | box-shadow 200ms ease-out, border-color 150ms ease-out |

### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `var(--text-secondary)`, radius 8px, h 34px, padding `6px 14px`, font bodySmall |
| Hover | bg `var(--bg)`, color `var(--text-primary)`, box-shadow glow-subtle (faint edge glow) |
| Active (current) | bg `var(--active)`, color `var(--accent-primary)`, font-weight 500, box-shadow glow-soft |
| Active press | transform `scale(0.985)` |
| Transition | color 75ms ease-out, background 75ms ease-out, box-shadow 150ms ease-out |

### Chips

| State | Properties |
|---|---|
| Rest | bg `var(--bg)`, border `1px solid var(--border-color)` at 12%, radius 20px (pill), h 30px, padding `0 12px`, font bodySmall, color `var(--text-secondary)` |
| Hover | border at 20%, color `var(--text-primary)`, box-shadow glow-subtle |
| Active (selected) | bg `var(--accent-primary)` at 15%, border-color `var(--accent-primary)` at 30%, color `var(--accent-primary)` |
| Active press | transform `scale(0.98)` |
| Transition | all 150ms ease-out |

### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 40px |
| Track height | 22px |
| Track radius | 9999px (full) |
| Track off bg | `var(--bg)` |
| Track off border | `1px solid var(--border-color)` at 25% |
| Track on bg | `var(--accent-primary)` |
| Track on box-shadow | glow-medium (the toggle GLOWS when active) |
| Thumb | 18px circle, `var(--text-primary)` |
| Thumb shadow | `0 0 4px rgba(var(--glow-rgb), 0.3)` when on |
| Transition | 200ms ease-out |
| Focus-visible | glow ring on track |

---

## Motion Map

Each mode has a distinct motion personality. Electric is fast and sharp. Organic is slow and fluid. Signal is medium-paced and precise. The same component has different timing depending on the active mode.

### Easings

| Name | Value | Character | Primary Mode |
|---|---|---|---|
| sharp-out | `cubic-bezier(0.12, 0.8, 0.3, 1)` | Fast deceleration, aggressive stop | Electric |
| ease-out-quint | `cubic-bezier(0.22, 1, 0.36, 1)` | Slow, organic deceleration | Organic |
| ease-in-out | `cubic-bezier(0.4, 0, 0.2, 1)` | Balanced, utilitarian | Signal |
| snap | `cubic-bezier(0, 0.9, 0.3, 1)` | Near-instant with soft landing | Electric (micro) |
| breathe | `cubic-bezier(0.45, 0, 0.55, 1)` | Symmetrical, rhythmic | Organic (ambient) |
| linear-scan | `linear` | Constant rate, mechanical | Signal (scan effects) |

### Duration × Easing × Component (Per Mode)

| Component | Electric | Organic | Signal |
|---|---|---|---|
| Sidebar item bg/color | 60ms / sharp-out | 120ms / ease-out-quint | 80ms / ease-in-out |
| Button hover glow | 80ms / sharp-out | 200ms / ease-out-quint | 120ms / ease-in-out |
| Button press scale | 80ms / sharp-out | 150ms / ease-out-quint | 100ms / ease-in-out |
| Toggle slide | 120ms / sharp-out | 300ms / ease-out-quint | 180ms / ease-in-out |
| Input focus glow | 100ms / sharp-out | 250ms / ease-out-quint | 150ms / ease-in-out |
| Card hover glow | 120ms / sharp-out | 300ms / ease-out-quint | 180ms / ease-in-out |
| Chip select | 80ms / snap | 200ms / ease-out-quint | 120ms / ease-in-out |
| Ghost icon hover | 150ms / sharp-out | 350ms / ease-out-quint | 200ms / ease-in-out |
| Panel slide-in | 200ms / sharp-out | 600ms / ease-out-quint | 300ms / ease-in-out |
| Modal enter | 180ms / sharp-out | 500ms / ease-out-quint | 280ms / ease-in-out |
| Modal exit | 120ms / snap | 350ms / ease-out-quint | 200ms / ease-in-out |
| Hero/page entry | 200ms / sharp-out | 800ms / ease-out-quint | 350ms / ease-in-out |
| Popover appear | 100ms / sharp-out | 250ms / ease-out-quint | 150ms / ease-in-out |
| Tooltip show | 60ms / snap | 150ms / ease-out-quint | 80ms / ease-in-out |

### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Barely perceptible |
| Chips | 0.98 | Slightly more |
| Buttons | 0.97 | Standard |
| Tabs | 0.96 | Pronounced |
| Cards (clickable) | 0.99 | Very subtle -- cards are large |

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column |
| Narrow max-width | 672px | Landing/focused content |
| Sidebar width | 260px | Fixed sidebar |
| Header height | 48px | Top bar, transparent bg |
| Spacing unit | 4px | Base multiplier |

### Spacing Scale

4, 6, 8, 12, 16, 24, 32, 48px

### Density

**Per-mode density character:**

| Mode | Density | Notes |
|---|---|---|
| Electric | Moderate | Tighter spacing, more data-dense. 10-14px card padding, 6px list gaps. |
| Organic | Comfortable | Generous breathing room. 16-20px card padding, 10px list gaps. |
| Signal | Moderate-Dense | Utilitarian. 12-16px card padding, 8px list gaps. |

### Radius Scale

| Token | Value | Usage |
|---|---|---|
| none | 0px | -- |
| sm | 4px | Badges, small elements |
| md | 6px | Ghost buttons, menu items |
| lg | 8px | Sidebar items, primary buttons |
| xl | 12px | Cards, popovers |
| 2xl | 16px | Modal containers |
| input | 8px | Form inputs, textareas |
| pill | 20px | Chat input card, large pills |
| full | 9999px | Avatars, toggles, chips |

### Responsive Notes

- **lg (1024px+):** Full sidebar (260px) + content column. Glow effects at full intensity.
- **md (768px):** Sidebar collapses to overlay panel (slides in with glow-medium border). Content fills width.
- **sm (640px):** Single column. Card radius reduces from 12px to 8px. Chat input radius reduces from 20px to 12px. Glow effects simplify (see Mobile Notes).

---

## Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring | 3-layer glow ring (see Border System): `0 0 0 2px var(--page), 0 0 0 4px rgba(var(--glow-rgb),0.5), 0 0 12px rgba(var(--glow-rgb),0.3)` |
| Disabled opacity | 0.35 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled glow | glow-none (remove all glow on disabled elements) |
| Selection bg | `rgba(var(--glow-rgb), 0.25)` |
| Selection color | `var(--text-primary)` (unchanged) |
| Scrollbar width | thin |
| Scrollbar thumb | `var(--border-color)` at 30% |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

**Contrast verification:**
- `#E8ECF0` (text-primary) on `#050510` (Electric page): 16.8:1 -- passes AAA
- `#8899AA` (text-secondary) on `#050510`: 7.2:1 -- passes AA
- `#667A8A` (text-muted) on `#050510`: 4.6:1 -- passes AA for body text
- `#667A8A` on `#101028` (surface): 4.1:1 -- passes AA for large text (14px+ bold or 18px+); used only for labels/captions at 12px weight 500, which qualify as non-body. For surfaces where muted text must meet 4.5:1, increase to `#7088A0` (5.2:1).

### Reduced Motion (Per Mode)

```css
@media (prefers-reduced-motion: reduce) {
  /* ALL MODES: Collapse spatial transforms to instant, keep glow transitions */
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.1s !important;
  }

  /* ELECTRIC: Disable phosphor trail effect, disable glitch animation */
  [data-mode="electric"] .phosphor-trail { display: none; }
  [data-mode="electric"] [data-effect="glitch"] { animation: none; }

  /* ORGANIC: Disable breathing pulse, disable wave animation */
  [data-mode="organic"] .breath-pulse { animation: none; }
  [data-mode="organic"] .wave-ambient { animation: none; }
  [data-mode="organic"] .bioluminescent-drift { animation: none; }

  /* SIGNAL: Disable scan-line sweep, disable blink animation */
  [data-mode="signal"] .scan-line { animation: none; display: none; }
  [data-mode="signal"] .signal-blink { animation: none; }
  [data-mode="signal"] .sweep-effect { animation: none; }

  /* ALL MODES: Keep glow transitions (they are not motion, they are luminance changes) */
  /* box-shadow transitions are retained at reduced duration */
}
```

---

## Overlays

### Popover / Dropdown

- **bg:** `var(--surface)`
- **border:** `1px solid var(--border-color)` at 25%
- **radius:** 12px
- **box-shadow:** glow-medium (the popover glows)
- **padding:** 6px
- **z-index:** 50
- **min-width:** 192px, **max-width:** 320px
- **Menu item:** 6px 8px padding, radius 6px, h 32px, font bodySmall, color text-secondary
- **Menu item hover:** bg `var(--active)`, color text-primary, box-shadow glow-subtle (individual item glow)
- **Transition:** 75ms mode-easing

### Modal

- **Overlay bg:** `rgba(0,0,0,0.60)` -- heavier dim on dark backgrounds for contrast
- **Overlay backdrop-filter:** `blur(8px)` -- subtle defocus
- **Content bg:** `var(--surface)`
- **Content border:** `1px solid var(--border-color)` at 30%
- **Content box-shadow:** glow-strong (modal is a beacon of light)
- **Content radius:** 16px
- **Entry:** scale `0.95` to `1.0` + opacity `0` to `1`, with glow-none escalating to glow-strong. Duration per mode.
- **Exit:** opacity `1` to `0` + scale `1.0` to `0.97`, glow fades. Duration per mode (shorter than entry).

### Tooltip

Tooltips are high-contrast, glow-accented.

- **bg:** `var(--surface)`
- **color:** `var(--text-primary)`
- **font:** label size (12px), weight 500
- **radius:** 6px
- **padding:** 4px 10px
- **border:** `1px solid var(--border-color)` at 20%
- **box-shadow:** glow-subtle
- **No arrow.** Position via offset.

---

## Visual Style

### Glow Rendering Pipeline

The glow system is the theme's entire visual identity. Every piece of luminance follows this pipeline:

1. **Source color** -- `var(--accent-primary)` or `var(--accent-secondary)`, decomposed into RGB channels via `var(--glow-rgb)`.
2. **Inner glow** -- `0 0 [4-12]px rgba(var(--glow-rgb), [0.08-0.30])`. Tight, high-opacity layer simulating surface emission.
3. **Outer glow** -- `0 0 [15-40]px rgba(var(--glow-rgb), [0.06-0.15])`. Medium spread. The visible halo.
4. **Bloom halo** -- `0 0 [48-80]px rgba(var(--glow-rgb), [0.04-0.08])`. Wide, atmospheric. Tints the surrounding darkness.
5. **Additive compositing** -- Where glows overlap (e.g., two adjacent glowing cards), apply `mix-blend-mode: screen` on the glow layer to prevent muddy additive colors.

### Vignette Fog

Each mode applies a radial-gradient vignette to the page, creating the sense that darkness deepens at the edges:

| Mode | Vignette Value |
|---|---|
| Electric | `radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(5,5,16,0.4) 100%)` |
| Organic | `radial-gradient(ellipse at 50% 60%, transparent 50%, rgba(4,20,26,0.5) 100%)` -- shifted down, ocean depth feeling |
| Signal | `radial-gradient(ellipse at 50% 50%, transparent 60%, rgba(10,10,14,0.35) 100%)` -- tighter, tunnel vision |

Apply as a `::before` pseudo-element on the page container, `pointer-events: none`, `position: fixed`, `inset: 0`, `z-index: 1`.

### Scan-Line Texture (Signal Mode Only)

A subtle horizontal scan-line overlay mimicking CRT monitors:

```css
[data-mode="signal"] .page::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 2;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.03) 2px,
    rgba(0,0,0,0.03) 4px
  );
  mix-blend-mode: multiply;
}
```

### Material

- **Grain:** None. The darkness is smooth and absolute. Grain would soften the glow contrast.
- **Gloss:** Glow-sheen. Surfaces do not reflect light -- they emit it. The "gloss" is the glow bloom itself.
- **Blend mode:** `mix-blend-mode: screen` on overlapping glow elements. `normal` for all surface backgrounds.
- **Shader bg:** Optional. A slow-moving perlin noise field at extreme low opacity (`0.02`) can add life to the page background without competing with UI glow. Not required.

---

## Signature Animations

### Electric Mode (3 Animations)

**1. Phosphor Trail**
When a button or interactive element is clicked, a brief afterimage trails the glow, simulating phosphor persistence on CRT displays. The glow-strong box-shadow lingers for 120ms after the element returns to rest, fading exponentially.

- **Technique:** `@keyframes phosphor-decay` -- box-shadow holds at glow-strong for 40ms, then decays to glow-subtle over 80ms.
- **Timing:** 120ms total, `cubic-bezier(0.12, 0.8, 0.3, 1)` (sharp-out)
- **Easing:** Exponential decay (front-loaded)
- **Reduced motion:** Disabled entirely. Element returns to rest instantly.

```css
@keyframes phosphor-decay {
  0% { box-shadow: 0 0 12px rgba(var(--glow-rgb), 0.30), 0 0 40px rgba(var(--glow-rgb), 0.15), 0 0 80px rgba(var(--glow-rgb), 0.08); }
  33% { box-shadow: 0 0 12px rgba(var(--glow-rgb), 0.25), 0 0 40px rgba(var(--glow-rgb), 0.12), 0 0 80px rgba(var(--glow-rgb), 0.06); }
  100% { box-shadow: 0 0 4px rgba(var(--glow-rgb), 0.08); }
}
```

**2. Flicker Pulse**
The primary accent color flickers imperceptibly on idle elements every 8-12 seconds, simulating electrical instability. A single glow-subtle pulse that peaks at glow-soft and returns.

- **Technique:** `@keyframes flicker` -- opacity oscillates between 0.08 and 0.12 on the glow layer.
- **Timing:** 200ms per flicker, repeats every 8-12s (randomized via `animation-delay`).
- **Easing:** `steps(3)` -- discrete steps for an electrical feel.
- **Reduced motion:** Disabled. Static glow-subtle.

**3. Entry Cascade**
When a page loads, elements appear in a staggered cascade from top to bottom. Each element starts at `opacity: 0` and `translateY(8px)`, entering with sharp-out easing. Glow starts at glow-none and escalates to the element's rest glow. Stagger delay: 30ms per element.

- **Timing:** 200ms per element, 30ms stagger.
- **Easing:** sharp-out.
- **Reduced motion:** Elements appear instantly at full opacity, no translate. Glow appears at rest value.

### Organic Mode (3 Animations)

**1. Breathing Pulse**
All glowing surfaces exhibit a slow, rhythmic pulse -- glow intensity oscillates between 85% and 100% of rest value over 4-6 seconds, simulating biological respiration. This is the heartbeat of the Organic mode.

- **Technique:** `@keyframes breathe` -- box-shadow opacity oscillates sinusoidally.
- **Timing:** 5000ms, infinite loop.
- **Easing:** `cubic-bezier(0.45, 0, 0.55, 1)` (breathe -- symmetrical).
- **Reduced motion:** Disabled. Static glow at 100%.

```css
@keyframes breathe {
  0%, 100% { box-shadow: 0 0 6px rgba(var(--glow-rgb), 0.10), 0 0 15px rgba(var(--glow-rgb), 0.06); }
  50% { box-shadow: 0 0 6px rgba(var(--glow-rgb), 0.085), 0 0 15px rgba(var(--glow-rgb), 0.05); }
}
```

**2. Bioluminescent Drift**
Accent-colored glow sources slowly drift in position, as if carried by deep-water currents. Implemented as a slow `background-position` animation on a radial-gradient glow behind the content area.

- **Technique:** A `::before` pseudo with `radial-gradient(circle at var(--drift-x) var(--drift-y), rgba(var(--glow-rgb), 0.03), transparent 70%)`. `--drift-x` and `--drift-y` animate between 30%-70% over 20s.
- **Timing:** 20000ms, infinite, alternate.
- **Easing:** ease-in-out.
- **Reduced motion:** Disabled. Static position at 50% 50%.

**3. Wave Entry**
Page elements enter with a gentle wave -- each element arrives with a slow `translateY(12px)` to `0` and `opacity: 0` to `1`, but with ease-out-quint creating a long, decelerating tail. Stagger: 80ms per element.

- **Timing:** 600ms per element, 80ms stagger.
- **Easing:** ease-out-quint.
- **Reduced motion:** Instant opacity, no translate.

### Signal Mode (3 Animations)

**1. Scan-Line Sweep**
A horizontal line of accent-colored light sweeps down the page every 15-20 seconds, like a radar sweep or CRT refresh. The line is 2px tall, accent-primary at 8% opacity, moving from top to bottom.

- **Technique:** `@keyframes scan-sweep` -- `translateY(-100vh)` to `translateY(100vh)`.
- **Timing:** 3000ms per sweep, repeats every 18s.
- **Easing:** `linear`.
- **Reduced motion:** Disabled entirely.

```css
@keyframes scan-sweep {
  from { transform: translateY(-100vh); }
  to { transform: translateY(100vh); }
}
.scan-line {
  position: fixed;
  left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(var(--glow-rgb), 0.08), transparent);
  pointer-events: none;
  z-index: 3;
  animation: scan-sweep 3s linear 18s infinite;
}
```

**2. Glitch Error**
When an error state appears, the element briefly "glitches" -- a 150ms animation where the element's position jitters by 1-2px horizontally and the border color flashes between accent-primary and danger.

- **Technique:** `@keyframes glitch` -- `translateX` alternates between -1px, 2px, -2px, 1px, 0. Border-color alternates.
- **Timing:** 150ms, plays once on error trigger.
- **Easing:** `steps(5)` -- discrete, mechanical.
- **Reduced motion:** Disabled. Error state appears statically with danger border color.

**3. Data Cascade**
Elements enter with a strict top-to-bottom cascade, each snapping into place with ease-in-out timing. No translate -- elements simply fade in at their final position. Stagger: 50ms per element.

- **Timing:** 280ms per element, 50ms stagger.
- **Easing:** ease-in-out.
- **Reduced motion:** Instant opacity.

---

## Mode Variant Comparison

| Dimension | Electric | Organic | Signal |
|---|---|---|---|
| Page background | `#050510` Violet-black | `#04141A` Teal-black | `#0A0A0E` Grey-black |
| Accent primary | `#00E5FF` Cyan | `#00DDCC` Teal-cyan | `#FF0066` Pink |
| Accent secondary | `#FF00AA` Magenta | `#FF66AA` Soft pink | `#0088FF` Blue |
| Border tint | Cyan | Teal | Neutral grey |
| Fastest duration | 60ms | 120ms | 80ms |
| Slowest duration | 200ms | 800ms | 350ms |
| Primary easing | sharp-out | ease-out-quint | ease-in-out |
| Ambient animation | Flicker pulse | Breathing pulse | Scan-line sweep |
| Entry pattern | Fast cascade (30ms stagger) | Wave (80ms stagger) | Data cascade (50ms stagger) |
| Error animation | -- | -- | Glitch |
| Vignette | Tight, violet | Shifted down, deep | Tight, neutral |
| Scan-line overlay | No | No | Yes |
| Density | Moderate | Comfortable | Moderate-dense |
| Emotional register | Aggressive, electric | Calm, alive | Precise, utilitarian |
| Best for | Developer tools, gaming | Music, creative, wellness | Monitoring, dashboards |

---

## Mobile Notes

### Glow Simplification

Mobile GPUs handle box-shadow glow reasonably well but large blur radii are expensive. Simplify the 3-layer pipeline to 2 layers on mobile:

| Desktop Glow | Mobile Glow |
|---|---|
| glow-subtle (1 layer) | Unchanged |
| glow-soft (2 layers) | Reduce outer blur by 40% |
| glow-medium (3 layers) | Drop bloom halo. Keep inner + outer at 60% blur. |
| glow-strong (3 layers) | Drop bloom halo. Inner + outer at 70% blur. |
| glow-intense (3 layers) | Drop bloom halo. Inner + outer at 70% blur. Cap at glow-strong mobile values. |

### Effects to Disable on Mobile

- Vignette fog pseudo-element -- remove entirely (saves a compositing layer)
- Scan-line texture overlay (Signal mode) -- remove
- Bioluminescent drift (Organic mode) -- freeze at center position
- Phosphor trail (Electric mode) -- collapse to instant state change
- `mix-blend-mode: screen` on glow overlaps -- remove, use standard compositing

### Performance Budget

- Maximum concurrent glow layers (box-shadow count per visible element): 2
- Maximum total box-shadow blur radius across all visible elements: 60px (vs 120px desktop)
- `will-change: box-shadow` during animations only, removed after
- Card radius: 12px reduces to 8px
- Chat input radius: 20px reduces to 12px
- All interactive elements maintain 44px minimum touch target
- Body text stays 16px (already comfortable for mobile)
- Ambient animations (breathing, flicker, scan) disabled entirely on mobile

---

## Implementation Checklist

- [ ] Google Fonts loaded: Sora (600, 700), Manrope (400, 500), Fira Code (400)
- [ ] CSS custom properties defined for all three modes (Electric, Organic, Signal) under `data-mode` attribute
- [ ] `--glow-rgb` decomposed color channels defined per mode for `rgba()` usage in glow tokens
- [ ] All 7 glow tokens implemented as CSS custom properties referencing `var(--glow-rgb)`
- [ ] Glow escalation on hover/focus for all interactive components (cards, inputs, buttons)
- [ ] 3-layer glow pipeline documented and applied: inner glow + outer glow + bloom halo
- [ ] Focus glow ring (`0 0 0 2px var(--page), 0 0 0 4px rgba(var(--glow-rgb),0.5), 0 0 12px rgba(var(--glow-rgb),0.3)`) on all interactive elements
- [ ] Border opacity system implemented (10%, 18%, 25%, 35% on `var(--border-color)`)
- [ ] Luminous borders using per-mode border colors (cyan/teal/steel)
- [ ] Vignette fog applied per mode as `::before` pseudo on page container
- [ ] Scan-line texture applied in Signal mode only as `::after` pseudo
- [ ] `mix-blend-mode: screen` on overlapping glow elements
- [ ] `prefers-reduced-motion` selectors defined per mode (Electric: phosphor+flicker, Organic: breathe+drift+wave, Signal: scan+glitch+blink)
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] Scrollbar styled: thin, `var(--border-color)` at 30% thumb, transparent track
- [ ] Touch targets >= 44px on all interactive elements
- [ ] Motion map durations match per-mode table (Electric fast, Organic slow, Signal medium)
- [ ] Text contrast verified: text-primary 16.8:1, text-secondary 7.2:1, text-muted 4.6:1 minimum
- [ ] `::selection` styled with mode-adaptive accent at 25%
- [ ] `::placeholder` color matches `var(--text-muted)` token
- [ ] Breathing pulse animation (Organic), flicker (Electric), scan-sweep (Signal) implemented as ambient effects
- [ ] Mode switching tested: verify all custom properties swap cleanly when `data-mode` changes
- [ ] Mobile glow simplification: 3-layer pipeline reduced to 2-layer on screens below 768px
- [ ] `@supports not (backdrop-filter: blur(1px))` fallback: remove vignette, increase surface opacity
- [ ] State transitions tested per mode with correct mode-specific easing curves
