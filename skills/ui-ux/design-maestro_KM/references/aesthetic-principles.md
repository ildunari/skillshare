# Aesthetic Principles

> The core design philosophy loaded on every task. This is what separates "AI-generated" from "designer-built."

## The Anti-Slop Manifesto

These are the 10 most common tells that a design was AI-generated. **Never do these.**

| # | Anti-Pattern | Do This Instead |
|---|---|---|
| 1 | Three identical cards in a centered row | Vary card sizes. Bento grid. Feature one card larger. |
| 2 | Purple/violet gradient on white | Intentional palette from theme. Muted tones. Texture over gradient. |
| 3 | Inter/Roboto as sole typeface | Deliberate font pairing from `themes.md`. Display + body combo. |
| 4 | Centered-everything, uniform spacing | Left-align body text. Vary spacing: tight headings, generous sections. |
| 5 | Generic SaaS template (hero→features→testimonials→CTA) | Break the formula. Lead with problem. Asymmetric sections. Narrative flow. |
| 6 | Cookie-cutter pricing cards | Highlight recommended. Vary card sizes. Interactive toggles. |
| 7 | `rounded-xl` on everything | Mix: sharp corners for data, medium for cards, pill for buttons. |
| 8 | Meaningless gradient blobs | Purposeful decoration. Grain textures, mesh gradients tied to content. |
| 9 | Single icon set, no customization | Mix icon weights/sizes. Custom hero icons. Filled vs outlined strategically. |
| 10 | `shadow-md` on every elevated element | Vary elevation. Subtle borders. Inner shadows. Colored shadows matching bg. |

⤷ Full examples with code alternatives: `grep -A 100 "### 1." references/deep/anti-patterns.md`

## Visual Hierarchy

**Spacing rhythm:** Use a non-uniform scale. Don't make every section gap identical.
- Tight: between heading and subtext (4-8px)
- Medium: between related elements (16-24px)
- Generous: between sections (64-120px)
- Dramatic: hero to first section (80-160px)

**Typography scale:** Establish clear hierarchy with at least 3 distinct sizes.
- Display: 48-72px (heroes, page titles) — display font. `text-wrap: balance` eliminates orphaned last-line words.
- Heading: 24-36px (section titles) — display or body font bold. `text-wrap: balance` here too.
- Body: 16-18px (paragraphs) — body font regular. `text-wrap: pretty` for better line-breaking (avoids orphans).
- Small: 12-14px (captions, labels) — body font, reduced opacity

**Color application:**
- Primary: used sparingly (CTA buttons, key links, active states)
- Neutral palette does 80% of the work (text, borders, backgrounds, cards)
- Accent: one or two spots per viewport (badges, highlights, decorative elements)
- Never: random colors without semantic meaning

## Color Generation System

A single brand color should produce your entire palette. No ad-hoc hex values.

### OKLCH scale from one hue

Given a brand color, generate a 50–950 scale by varying L (lightness) and C (chroma) at constant H (hue):

| Step | Lightness (L) | Chroma (C) | Use |
|---|---|---|---|
| 50 | 97% | 0.01 | Tinted backgrounds |
| 100 | 93% | 0.02 | Hover backgrounds |
| 200 | 87% | 0.04 | Subtle borders |
| 300 | 78% | 0.08 | Muted elements |
| 400 | 66% | 0.12 | Secondary text on dark |
| 500 | 55% | 0.15 | Base brand — your input color |
| 600 | 48% | 0.14 | Hover accents |
| 700 | 39% | 0.12 | Strong accents |
| 800 | 28% | 0.08 | Dark text on light |
| 900 | 18% | 0.05 | Headings, emphasis |
| 950 | 10% | 0.03 | Near-black tinted |

Adjust C at the extremes — high lightness and low lightness can't hold much chroma without clipping.

### Semantic color derivation

From your brand hue (H), derive status colors by shifting hue while keeping similar L and C:

- **Success:** H → 145 (green family), L ≈ 55%, C ≈ 0.15
- **Warning:** H → 85 (amber family), L ≈ 70%, C ≈ 0.15
- **Error:** H → 25 (red family), L ≈ 55%, C ≈ 0.18
- **Info:** H → 250 (blue family), L ≈ 55%, C ≈ 0.13

### Neutral generation

- **Warm neutrals:** C = 0.01–0.03, H = brand hue. Surfaces feel cohesive with accents.
- **Cool neutrals:** C ≈ 0.005, H ≈ 260. Clinical, technical.
- **True neutrals:** C = 0. Achromatic. Use when the brand color needs to pop against pure gray.

Match your neutrals to intent. A bakery app gets warm neutrals. A code editor gets cool.

### P3 wide gamut

For vibrant accents that pop on modern displays:

```css
.accent {
  background: oklch(65% 0.25 30); /* sRGB fallback */
}
@media (color-gamut: p3) {
  .accent {
    background: color(display-p3 0.95 0.3 0.2); /* wider gamut */
  }
}
```

Use P3 for brand colors, status indicators, and key CTAs. Not for text or borders.

### Contrast-safe pairs

Rule of thumb in OKLCH: a lightness difference of ≥40% between text and background produces roughly 4.5:1 contrast. For large text (3:1), ≥30% is usually sufficient. Always verify with a contrast checker — OKLCH perceptual uniformity helps but isn't a guarantee.

### `color-mix()` recipes

```css
--hover: color-mix(in oklch, var(--primary) 90%, black);
--active: color-mix(in oklch, var(--primary) 80%, black);
--disabled: color-mix(in oklch, var(--primary) 40%, var(--surface));
--tint: color-mix(in oklch, var(--primary) 10%, var(--surface));
--overlay: color-mix(in oklch, var(--primary) 15%, transparent);
```

These are compositional — they adapt when `--primary` or `--surface` change (e.g., dark mode toggle). No separate dark-mode color definitions needed for derived values.

## Spacing System

The audit calls inconsistent spacing "the clearest sign of no system." Here's the system.

### 4px base, named tokens

Every spacing value is a multiple of 4px. No arbitrary values.

| Token | Value | Use |
|---|---|---|
| `--space-0.5` | 2px | Hairline gaps, icon–badge offsets |
| `--space-1` | 4px | Tight internal padding (badges, chips) |
| `--space-1.5` | 6px | Icon–text gap (pick one, use everywhere) |
| `--space-2` | 8px | Button vertical padding, input padding, tight gaps |
| `--space-3` | 12px | Input horizontal padding, card internal gaps |
| `--space-4` | 16px | Component padding, default gap |
| `--space-5` | 20px | Card padding (small) |
| `--space-6` | 24px | Card padding (standard), section sub-gaps |
| `--space-8` | 32px | Section internal spacing |
| `--space-10` | 40px | Section separation (tight) |
| `--space-12` | 48px | Section separation (standard) |
| `--space-16` | 64px | Major section breaks |
| `--space-20` | 80px | Hero spacing |
| `--space-24` | 96px | Generous section separation |
| `--space-32` | 128px | Dramatic breathing room |

### Spacing-to-type relationship

- Paragraph spacing = 1.5 × body line-height
- Section spacing = 3–4 × body line-height
- Heading space above = section spacing (heading belongs to content below, not above)
- Heading space below = tight (the heading "owns" what follows)

### Component internal padding

- **Buttons:** Horizontal > vertical. `8px 16px` or `10px 20px`. Equal padding looks boxy.
- **Inputs:** Match button height. `8px 12px`.
- **Cards:** `20px` (compact) to `24px` (standard). Consistent within a project.
- **Badges/chips:** `2px 8px` (tight) to `4px 12px`.
- **Modals:** `24px` to `32px`. More generous than cards.

### Gap vs margin

- Use `gap` in flex/grid containers. It respects the container's flow.
- Use `margin-bottom` for flow content (paragraphs, headings in prose).
- Avoid `margin-top` in components — or use the owl selector `* + *` so margin only appears between siblings, never on the first child.

### Density modes

Same scale, different multiplier:
- **Compact** (data tables, dense dashboards): reduce all spacing by 25%
- **Normal** (most interfaces): base values
- **Comfortable** (marketing, reading): increase by 25%

Implement via a CSS custom property multiplier: `--density: 1` (normal), `0.75` (compact), `1.25` (comfortable). Apply as `calc(var(--space-4) * var(--density))`.

## Layout Principles

- **Asymmetry is strength.** A 7/5 column split is more interesting than 6/6.
- **Edge-to-edge isn't always bad.** Full-bleed images, backgrounds, and decorative elements create drama.
- **White space is a feature.** Resist filling every gap. Let elements breathe.
- **Grid breaks create focus.** One element breaking the grid draws the eye. Use intentionally.
- **Z-pattern for scanning.** Place key elements along the natural Z-reading path.
- **Container widths vary.** Content max-width ~65ch for reading. Full-width for visuals. Don't make everything `max-w-7xl`.
- **Full-height layouts use `dvh`.** `100vh` doesn't account for mobile browser chrome. Use `100dvh` (dynamic viewport height) as the default. `svh`/`lvh` for specific edge cases.
- **Stable scrollbar gutter.** `scrollbar-gutter: stable` on scrollable containers prevents layout shift when content grows long enough to trigger a scrollbar. Essential for centered layouts.

## Responsive Design

### Fluid spacing with clamp()

Don't use fixed breakpoint spacing that jumps. Use continuous fluid scales:

```css
--space-section: clamp(3rem, 6vw, 5rem);
--space-content: clamp(1.5rem, 3vw, 2rem);
--space-tight: clamp(0.75rem, 1.5vw, 1rem);
```

This eliminates most breakpoint-specific spacing overrides. Spacing adapts smoothly from mobile to desktop.

### Container queries as first-class

Components should respond to their container, not the viewport. A card in a sidebar shouldn't care about the window width — it should care about how much space the sidebar gives it.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}
@container card (min-width: 400px) {
  .card { flex-direction: row; }
}
@container card (max-width: 399px) {
  .card { flex-direction: column; }
}
```

Stable in all browsers 2023+. Use them for every reusable component.

### Responsive component patterns

| Component | Desktop | Tablet | Mobile |
|---|---|---|---|
| Navigation | Full sidebar (persistent) | Icon-only sidebar | Bottom sheet / hamburger |
| Data table | Full columns | Hide low-priority columns | Stack as cards |
| Dashboard grid | Multi-column CSS Grid | 2-column | Single column, horizontal scroll for charts |
| Form layout | Side labels + inputs | Stacked labels + inputs | Same as tablet |
| Card grid | 3-4 columns | 2 columns | Single column |

### Touch target scaling

Desktop hover affordances don't exist on mobile. Touch targets need physical size:

- **Minimum:** 44×44px on mobile (Apple HIG), 48×48px (Material)
- **Comfortable:** 48×48px for primary actions
- **Touch padding:** `min-height: 44px; padding: 8px` — the padding is part of the target, not just the visible element
- **Spacing between targets:** Minimum 8px gap to prevent mis-taps

### Viewport units

| Unit | Meaning | Use |
|---|---|---|
| `dvh` | Dynamic viewport height (shrinks/grows with browser chrome) | Default for full-height layouts |
| `svh` | Small viewport height (browser chrome visible) | Conservative sizing |
| `lvh` | Large viewport height (browser chrome hidden) | Rarely needed |
| `vh` | Legacy — doesn't account for mobile browser chrome | Avoid on mobile |

`dvh` is stable in all browsers 2023+. Use it as the default.

## Dark Mode Guide

Dark mode is NOT just inverted colors. It's a different design language:

| Aspect | Light Mode | Dark Mode |
|---|---|---|
| Background | White / off-white | `#0a0a0a` or `#121212` (never `#000`) |
| Surface hierarchy | Darker = recessed | **Lighter = elevated** (opposite) |
| Text | `#1a1a1a` at 100% | `#e0e0e0` at ~87% opacity |
| Accent colors | Full saturation | Reduce saturation 10-20% |
| Shadows | Drop shadows | **Glows / rings** (shadows invisible on dark) |
| Borders | `gray-200` | `gray-800` with reduced opacity |
| Images | Normal | Consider `brightness(0.9)` filter |

**Modern CSS shortcuts:**
- `color-scheme: light dark` on `:root` — tells the browser your page supports both schemes. Form controls, scrollbars, and system colors adapt automatically.
- `light-dark()` function — `color: light-dark(#1a1a1a, #e0e0e0)` eliminates media query duplication for simple color switches. Requires `color-scheme` to be set. Stable in all browsers 2024+.

### Status colors in dark mode

Colors that work on white don't work on `#0a0a0a`. Red becomes harsh. Green glows.

| Status | Light mode | Dark mode adjustment |
|---|---|---|
| Error | `oklch(55% 0.22 25)` | Lighten to L=65%, reduce C to 0.17 |
| Success | `oklch(50% 0.16 145)` | Lighten to L=65%, reduce C to 0.13 |
| Warning | `oklch(75% 0.15 85)` | Reduce C to 0.12, keep L similar |
| Info | `oklch(55% 0.15 250)` | Lighten to L=65%, reduce C to 0.12 |

### Gradients don't just invert

Light-mode gradients (white → color) become harsh in dark mode. Dark mode gradients need less color range and more subtlety. Replace `white → brand` with `surface-elevated → brand at 20% opacity`.

### Image treatment

`brightness(0.9)` alone isn't enough for all images. Highly saturated photos glow on dark backgrounds.

```css
.dark img {
  filter: brightness(0.9) saturate(0.9) contrast(0.95);
}
```

### Shadow → glow transformation

Shadows are invisible on dark. Replace with luminous rings:

```css
/* Light mode */
.card { box-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06); }

/* Dark mode — glow from accent color */
.dark .card {
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.06),
    0 0 20px oklch(50% 0.1 var(--brand-hue) / 0.08);
}
```

The glow color should derive from the accent, not be white. White glows feel cheap.

### Text rendering

Light text on dark backgrounds renders thicker due to subpixel antialiasing. Always apply on dark mode:

```css
.dark {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### System preference + manual toggle

Support both. Detection via media query, override via class:

```css
/* System preference */
@media (prefers-color-scheme: dark) {
  :root:not(.light) { /* dark tokens */ }
}
/* Manual toggle */
:root.dark { /* dark tokens */ }
```

Persist the toggle to React state (in artifacts) or `localStorage` (in standalone projects).

## Accessibility

Non-negotiable for every output:

### Basics

- **Contrast:** 4.5:1 for normal text, 3:1 for large text (18px+), 3:1 for UI components against adjacent colors
- **Focus:** Visible focus ring on all interactive elements (`focus-visible:ring-2`)
- **Keyboard:** All functionality reachable via Tab/Enter/Escape/Arrow keys
- **Touch:** Minimum 44×44px tap targets on mobile. Padding counts — `min-height: 44px; padding: 8px` is valid.
- **Motion:** Wrap all animations in `@media (prefers-reduced-motion: no-preference)`
- **ARIA:** Labels on icon buttons, `aria-expanded` on toggles, `role` on custom widgets
- **Semantic HTML:** Use `<nav>`, `<main>`, `<section>`, `<article>`, `<button>` — not div soup

### Focus management

- **Route changes:** Move focus to the new page's `<main>` or first `<h1>`. Without this, keyboard users are stranded at the top.
- **Modal open:** Trap focus inside. Tab should cycle through modal content only.
- **Modal close:** Return focus to the trigger element that opened it.
- **Dynamic content:** When a list item is deleted, focus the next item or the list container — not nothing.

### Skip navigation

Every page needs this. Visible on focus, hidden otherwise:

```css
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  z-index: 100;
  padding: 8px 16px;
}
.skip-link:focus {
  top: 0;
}
```

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

### Aria live regions

Dynamic updates — toasts, validation, loading states — are invisible to screen readers without `aria-live`:

- `aria-live="polite"` — announced at next pause (toasts, form validation results)
- `aria-live="assertive"` — interrupts current speech (errors, urgent alerts)
- `role="status"` — shortcut for `aria-live="polite"` + `aria-atomic="true"`

### Color-blind design (beyond data viz)

Never rely on color alone for status. Every colored status indicator needs a secondary signal:

- Error fields: red border **AND** error icon **AND** error text
- Success: green **AND** checkmark icon
- Online/offline: color dot **AND** text label ("Online" / "Away")
- Badge colors: add text labels or icons, not just color swatches

### Cognitive accessibility

- **Progressive disclosure.** Don't show everything at once. Collapse advanced options behind "More."
- **Plain language.** "Save" not "Persist." "Delete project" not "Confirm destructive action."
- **Undo over confirm.** "Message sent — Undo" is friendlier and faster than "Are you sure you want to send this message? OK / Cancel."
- **Forgiving input.** Accept multiple date formats, trim whitespace, auto-format phone numbers.

### Reduced motion: what to show instead

`prefers-reduced-motion` doesn't mean "no feedback." Replace motion with instant state changes:

| Full motion | Reduced alternative |
|---|---|
| Slide in from side | Instant appearance (opacity 0 → 1, no transform) |
| Staggered reveal | All items appear simultaneously |
| Parallax scrolling | Static positioning |
| Auto-playing animation | Paused by default, play button |
| Spring physics | Instant snap to final position |
| Counting number animation | Show final number immediately |

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

⤷ Full accessibility patterns: `grep -A 150 "## Accessibility Failures" references/deep/anti-patterns.md`

## Performance Checklist

- **Animate only:** `transform`, `opacity`, `filter` (GPU-composited properties)
- **Never animate:** `width`, `height`, `top`, `left`, `margin`, `padding` (trigger layout)
- **Fonts:** `font-display: swap` or `optional`. Preload critical fonts. Subset if possible.
- **Images:** Lazy load below-fold (`loading="lazy"`). Use modern formats (WebP/AVIF).
- **CSS:** Use `content-visibility: auto` for long pages. `contain: layout` on independent sections.
- **JS:** Prefer CSS animations over JS. Use `requestAnimationFrame` for Canvas/WebGL.
- **will-change:** Apply only temporarily before animation. Never leave on permanently.

⤷ Full performance anti-patterns: `grep -A 100 "## Performance Anti-Patterns" references/deep/anti-patterns.md`

## Pre-Flight Checklist

Run through before delivering any design output:

### AI-Slop Prevention
- [ ] No uniform three-card layouts
- [ ] Custom color palette (not default gradients)
- [ ] Font pairing with personality
- [ ] Varied spacing rhythm
- [ ] Custom layout structure (not template formula)
- [ ] Mixed border radius values
- [ ] Purposeful decorative elements
- [ ] Varied elevation system
- [ ] Custom `::selection` color matching accent palette

### Accessibility
- [ ] 4.5:1 contrast for text, 3:1 for UI components
- [ ] Visible focus indicators (box-shadow, not outline)
- [ ] Full keyboard navigation with focus management
- [ ] Alt text on images, ARIA labels on controls
- [ ] Reduced motion support (with meaningful alternatives, not just disabled)
- [ ] 44×44px touch targets
- [ ] Skip navigation link
- [ ] `aria-live` on dynamic content (toasts, validation)

### Performance
- [ ] Animate only transform/opacity/filter
- [ ] `font-display: swap`
- [ ] Lazy loading below fold
- [ ] No layout thrashing

### Dark Mode (if applicable)
- [ ] `#0a0a0a` not `#000`
- [ ] `color-scheme: light dark` set
- [ ] Desaturated accents
- [ ] Glows/rings instead of shadows (derived from accent, not white)
- [ ] Text at ~87% opacity with `-webkit-font-smoothing: antialiased`
- [ ] Status colors adjusted (lighter, less saturated)
- [ ] Contrast tested separately in dark mode
- [ ] Images filtered: `brightness(0.9) saturate(0.9)`
