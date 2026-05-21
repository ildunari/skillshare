# Iridescent — Full Specification
> Schema v2 | 1071 lines | Last updated: 2026-02-16

## Table of Contents
| Section | Line |
|---|---|
| Identity & Philosophy | 15 |
| Color System | 39 |
| The Conic Gradient System | 116 |
| Typography Matrix | 317 |
| Elevation System | 372 |
| Border System | 429 |
| Component States | 502 |
| Motion Map | 615 |
| Overlays | 663 |
| Layout Tokens | 705 |
| Accessibility Tokens | 744 |
| Visual Style | 769 |
| Signature Animations | 781 |
| Dark Mode Variant | 923 |
| Dual-Mode Comparison Table | 976 |
| Mobile Notes | 1021 |
| Implementation Checklist | 1050 |

---

## 16. Iridescent

> Futuristic chrome surfaces refracting light through conic-gradient halos — where holographic daydream meets brushed metal.

**Best for:** Consumer tech, portfolio sites, product showcases, creative agencies, fashion/luxury, Web3, automotive, lifestyle brands, design studios, editorial fashion.

---

### Identity & Philosophy

This theme lives in the world of a concept car reveal at a design expo — gleaming chrome surfaces under gallery lighting, holographic foil catching prismatic color at every angle, surfaces that shift between cool rainbow iridescence and warm metallic sheen depending on viewing angle. The defining visual technique is `conic-gradient` — sweeping angular gradients that create the illusion of light rotating across a surface. Borders shimmer. Highlights drift. Surfaces feel polished, reflective, alive.

The theme operates in two modes, each a complete visual system:

**Holographic mode** is the cool-spectrum variant. Soap-bubble iridescence, prismatic light splitting through glass, pastel rainbow shifts that feel weightless and ethereal. The palette is desaturated pastels against near-white backgrounds. Effects are translucent, layered, atmospheric. Think holographic stickers, soap bubbles, oil-on-water rainbow film, the back of a CD in sunlight.

**Chrome mode** is the warm-spectrum variant. Brushed metal, specular highlights, reflective silver-to-white gradients with warm undertones. Heavier, more premium, grounded. Think polished automotive chrome, luxury tech hardware, titanium Apple devices, brushed stainless steel. The palette is warm greys and silvers against a slightly warm off-white canvas.

The core tension is futurism vs. tactility. The conic gradients and spring animations signal "future" — but the metallic materiality signals "you can touch this." Neither mode is flat. Both have physical presence expressed through specular highlights, reflective borders, and shadow tokens that carry metallic undertones.

**Decision principle:** "When in doubt, ask: does this surface look like it would reflect light? If it looks matte and static, add a conic highlight. If it looks garish, reduce saturation and let the angle do the work."

**What this theme is NOT:**
- Not a rave poster — iridescent effects are SUBTLE at rest and intensify on interaction
- Not constantly shimming — animation is triggered, not ambient (except the slow `--angle` rotation on hero elements)
- Not dark-first — both modes are light-background-native; the iridescent effects need neutral backgrounds to pop
- Not flat — every interactive surface has a specular quality, achieved through gradients and shadows, not blur
- Not glassmorphism — no `backdrop-filter` blur as a structural element; this is about reflection and refraction, not translucency
- Not maximalist — the conic gradient is the ONE signature effect; everything else stays restrained

---

### Color System

The color system has two complete palettes. Both share the same semantic colors and structural approach but differ in temperature and accent character.

#### Holographic Mode Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Holo Canvas | `#F5F5F8` | Deepest background. Cool near-white with faint blue undertone. Neutral enough to let prismatic borders pop. |
| bg | Holo Surface | `#FAFAFC` | Primary surface background. Slightly elevated from page. |
| surface | Holo Panel | `#FFFFFF` | Elevated cards, inputs, popovers. Pure white for maximum prismatic contrast. |
| recessed | Holo Inset | `#EEEEF2` | Code blocks, inset areas. Cool grey with lavender cast. |
| active | Holo Active | `#E8E8F0` | Active/pressed items, user bubbles. Deeper cool grey. |
| text-primary | Holo Ink | `#1A1A2E` | Headings, body text. Deep navy-black for contrast. |
| text-secondary | Holo Secondary | `#5A5A7A` | Sidebar items, secondary labels. Muted indigo-grey. |
| text-muted | Holo Muted | `#9494AC` | Placeholders, timestamps, metadata. Soft lavender-grey. |
| text-onAccent | On Prism | `#FFFFFF` | Text on accent-colored backgrounds. |
| border-base | Holo Separator | `#C0C0D0` | Base border color. Cool silver used at variable opacity. |
| accent-primary | Prism Violet | `#7B68EE` | Brand accent, primary CTA. Medium slate blue — the center of the prismatic spectrum. |
| accent-secondary | Prism Cyan | `#00D4FF` | Secondary accent for links, informational highlights. Cool end of the spectrum. |
| success | Holo Mint | `#2DD4A8` | Positive states. Cooler green that harmonizes with prismatic palette. |
| warning | Holo Amber | `#FFB020` | Caution states. Warm amber, the complementary warm note. |
| danger | Holo Rose | `#FF5A7E` | Error states, destructive actions. Pink-red, part of the prismatic sweep. |
| info | Holo Azure | `#38B6FF` | Info states. Bright sky blue. |

#### Chrome Mode Palette

| Token | Name | Hex | Role |
|---|---|---|---|
| page | Chrome Canvas | `#F3F2EF` | Deepest background. Warm greige. Slightly warm undertone like brushed aluminum under tungsten. |
| bg | Chrome Surface | `#F9F8F6` | Primary surface background. Warm off-white. |
| surface | Chrome Panel | `#FFFFFF` | Elevated cards, inputs, popovers. Pure white for specular highlight contrast. |
| recessed | Chrome Inset | `#EAEAE6` | Code blocks, inset areas. Warm grey. |
| active | Chrome Active | `#E2E1DC` | Active/pressed items. Deeper warm grey with golden cast. |
| text-primary | Chrome Ink | `#1E1E1E` | Headings, body text. True near-black. |
| text-secondary | Chrome Secondary | `#6B6B65` | Sidebar items, secondary labels. Warm grey. |
| text-muted | Chrome Muted | `#A0A098` | Placeholders, timestamps, metadata. Silvered warm grey. |
| text-onAccent | On Metal | `#FFFFFF` | Text on accent-colored backgrounds. |
| border-base | Chrome Separator | `#C5C5BD` | Base border color. Warm silver at variable opacity. |
| accent-primary | Chrome Violet | `#8B5CF6` | Brand accent, primary CTA. Slightly warmer violet than holographic. |
| accent-secondary | Chrome Gold | `#D4A853` | Secondary accent. Brushed gold for luxury warmth. |
| success | Chrome Emerald | `#22C55E` | Positive states. Classic green. |
| warning | Chrome Amber | `#F59E0B` | Caution states. |
| danger | Chrome Red | `#EF4444` | Error states. |
| info | Chrome Steel | `#6366F1` | Info states. Indigo-blue with metallic warmth. |

#### Special Tokens (Both Modes)

| Token | Holographic Value | Chrome Value | Role |
|---|---|---|---|
| inlineCode | `#7B68EE` | `#8B5CF6` | Code text within prose. Accent-aligned purple. |
| toggleActive | `#2DD4A8` / `#22C55E` | `#22C55E` | Toggle/switch active track. |
| selection | `rgba(123,104,238,0.18)` / `rgba(139,92,246,0.18)` | `rgba(139,92,246,0.18)` | `::selection` background. Accent at 18%. |

#### Opacity System

Borders use the base border color at progressive opacity levels:

| Context | Opacity | Usage |
|---|---|---|
| subtle | 12% | Hairline edges, section dividers |
| card | 20% | Card borders at rest |
| hover | 30% | Hovered elements |
| focus | 45% | Focused elements (before conic gradient replaces it) |

**Conic gradient override:** On interactive elements at hover and focus, the standard border-color-at-opacity is replaced by a `conic-gradient` border. This is the theme's signature — static borders become prismatic on interaction.

#### Color Rules

- **Conic gradients are the only gradients.** No linear gradients on surfaces. Backgrounds are flat. The conic gradient lives on borders and highlight overlays.
- **Iridescence is earned.** At rest, elements use standard flat borders. On hover/focus/active, the conic gradient activates. Not everything shimmers constantly.
- **Hero elements may have persistent conic borders** — one or two per page at most. The hero card or primary CTA can shimmer continuously with a slow rotation.
- **Semantic colors are slightly shifted** to harmonize with the prismatic spectrum (mint instead of green, rose instead of red). They still pass WCAG contrast requirements.
- **Mode switching:** Holographic and Chrome share the same structural layout. Only palette tokens, conic gradient hue stops, and shadow warmth change between modes. A CSS custom property toggle (`--mode: holographic | chrome`) drives the switch.

---

### The Conic Gradient System

This is the defining CSS technique of the Iridescent theme. Every other theme achieves its identity through color, typography, or material. This theme achieves its identity through angular gradients that simulate light rotating across a reflective surface.

#### The `@property` Hack

CSS cannot natively animate `conic-gradient` angles. The workaround is the `@property` rule, which registers `--angle` as an animatable custom property:

```css
@property --angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}
```

Once registered, `--angle` can be used inside `conic-gradient()` and animated via CSS transitions or keyframes.

#### Holographic Conic Gradient

The full-spectrum prismatic sweep. Seven stops creating a smooth rainbow loop:

```css
/* Holographic border — full prismatic spectrum */
.holo-border {
  --angle: 0deg;
  border: 2px solid transparent;
  border-image: conic-gradient(
    from var(--angle),
    #ff6b6b,   /* Red */
    #ffa500,   /* Orange */
    #ffd700,   /* Gold */
    #7fff00,   /* Chartreuse */
    #00d4ff,   /* Cyan */
    #7b68ee,   /* Slate blue */
    #ff6b9d,   /* Pink */
    #ff6b6b    /* Back to red — seamless loop */
  ) 1;
  border-radius: 0; /* border-image doesn't support border-radius */
}

/* Alternative: background-based approach that supports border-radius */
.holo-border-rounded {
  --angle: 0deg;
  position: relative;
  border-radius: 12px;
}
.holo-border-rounded::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  padding: 2px;
  background: conic-gradient(
    from var(--angle),
    #ff6b6b, #ffa500, #ffd700, #7fff00, #00d4ff, #7b68ee, #ff6b9d, #ff6b6b
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}
```

#### Chrome Conic Gradient

Monochromatic metallic sweep. Six stops cycling through silver tones:

```css
/* Chrome border — metallic sweep */
.chrome-border {
  --angle: 0deg;
  border: 2px solid transparent;
  border-image: conic-gradient(
    from var(--angle),
    #A0A0A0,   /* Dark silver */
    #C8C8C8,   /* Mid silver */
    #F0F0F0,   /* Bright silver */
    #FFFFFF,   /* Specular white */
    #D0D0D0,   /* Cooling silver */
    #A0A0A0    /* Back to dark — seamless loop */
  ) 1;
}

/* With border-radius support */
.chrome-border-rounded::before {
  background: conic-gradient(
    from var(--angle),
    #A0A0A0, #C8C8C8, #F0F0F0, #FFFFFF, #D0D0D0, #A0A0A0
  );
  /* Same mask technique as holographic */
}
```

#### Animated Rotation

The `--angle` variable rotates continuously for hero elements, or snaps to a position on hover for interactive elements:

```css
/* Continuous slow rotation for hero elements */
@keyframes conic-spin {
  from { --angle: 0deg; }
  to { --angle: 360deg; }
}

.hero-conic {
  animation: conic-spin 8s linear infinite;
}

/* Snap rotation on hover — angle jumps 90deg toward cursor */
.interactive-conic {
  --angle: 0deg;
  transition: --angle 0.6s cubic-bezier(0.22, 0.68, 0, 1.12); /* spring-feel overshoot */
}
.interactive-conic:hover {
  --angle: 90deg;
}

/* Reduced motion: disable rotation, keep static gradient */
@media (prefers-reduced-motion: reduce) {
  .hero-conic { animation: none; --angle: 45deg; }
  .interactive-conic { transition: none; --angle: 0deg; }
}
```

#### Specular Highlight Overlay

A secondary conic gradient layered on top of surfaces to simulate a specular light catch:

```css
/* Specular highlight — subtle light catch on surface */
.specular-highlight::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: conic-gradient(
    from var(--angle),
    transparent 0deg,
    rgba(255,255,255,0.08) 60deg,
    rgba(255,255,255,0.15) 90deg,
    rgba(255,255,255,0.08) 120deg,
    transparent 180deg,
    transparent 360deg
  );
  pointer-events: none;
  mix-blend-mode: overlay;
  opacity: 0;
  transition: opacity 0.4s ease;
}
.specular-highlight:hover::after {
  opacity: 1;
}
```

#### `mix-blend-mode` Color Shifting

For holographic mode, a secondary color layer using blend modes creates shifting hues:

```css
/* Holographic color shift — soft prismatic wash on cards */
.holo-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(
    135deg,
    rgba(123,104,238,0.04),
    rgba(0,212,255,0.04),
    rgba(255,107,107,0.03)
  );
  mix-blend-mode: color;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.5s ease;
}
.holo-card:hover::after {
  opacity: 1;
}
```

#### Browser Support

- `@property`: Chrome 85+, Firefox 128+, Safari 15.4+. This is the critical dependency.
- `conic-gradient`: Chrome 69+, Firefox 83+, Safari 12.1+. Universal.
- **Fallback:** If `@property` is unsupported, the gradient renders statically at `--angle: 0deg`. Still looks good, just does not rotate. Use `@supports (syntax: '<angle>')` or feature detection.

```css
/* Fallback for browsers without @property support */
@supports not (syntax: '<angle>') {
  .hero-conic {
    border: 2px solid #7B68EE; /* Solid accent border as fallback */
  }
}
```

---

### Typography Matrix

Sora is the geometric, futuristic variable font that defines this theme's typographic character. Its wide apertures, geometric circles, and uniform stroke width evoke the same futuristic precision as the conic gradients. Manrope handles body text with its clean geometric construction and excellent x-height. Fira Code brings ligatures to the monospace role.

#### Holographic Mode Typography

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Sora | 40px | 700 | 1.1 | -0.03em | wght 700 | Hero titles, page names, product names |
| Heading | Sora | 24px | 600 | 1.25 | -0.02em | wght 600 | Section titles, card headers |
| Subheading | Sora | 18px | 500 | 1.35 | -0.01em | wght 500 | Subsection titles, feature labels |
| Body | Manrope | 16px | 400 | 1.55 | -0.005em | -- | Primary reading text, descriptions |
| Body Small | Manrope | 14px | 400 | 1.45 | normal | -- | Sidebar items, form labels, secondary text |
| Button | Sora | 14px | 500 | 1.4 | 0.01em | wght 500 | Button labels, CTAs. Slightly tracked out for presence. |
| Input | Manrope | 14px | 400 | 1.4 | normal | -- | Form input text |
| Label | Manrope | 12px | 500 | 1.33 | 0.04em | -- | Section labels, metadata, timestamps. Tracked wider. |
| Code | Fira Code | 0.9em | 400 | 1.5 | normal | liga, calt | Inline code, code blocks. Ligatures enabled. |
| Caption | Manrope | 12px | 400 | 1.33 | normal | -- | Disclaimers, footnotes |

#### Chrome Mode Typography

Same families and sizes. The only changes are weight distribution — Chrome mode uses slightly heavier weights for a more grounded, premium feel:

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | Sora | 40px | 800 | 1.1 | -0.03em | wght 800 | Hero titles. Extra bold for metallic weight. |
| Heading | Sora | 24px | 700 | 1.25 | -0.02em | wght 700 | Section titles |
| Subheading | Sora | 18px | 600 | 1.35 | -0.01em | wght 600 | Subsection titles |
| Body | Manrope | 16px | 400 | 1.55 | -0.005em | -- | Primary reading text |
| Body Small | Manrope | 14px | 400 | 1.45 | normal | -- | Sidebar items, form labels |
| Button | Sora | 14px | 600 | 1.4 | 0.015em | wght 600 | Button labels. Heavier for metallic authority. |
| Input | Manrope | 14px | 400 | 1.4 | normal | -- | Form input text |
| Label | Manrope | 12px | 500 | 1.33 | 0.04em | -- | Section labels, metadata |
| Code | Fira Code | 0.9em | 400 | 1.5 | normal | liga, calt | Inline code, code blocks |
| Caption | Manrope | 12px | 400 | 1.33 | normal | -- | Disclaimers, footnotes |

#### Typographic Decisions

- **Sora variable** is loaded with the full weight axis (100-800), enabling continuous weight interpolation. Display text in Chrome mode uses wght 800, the heaviest available, to convey metallic mass.
- **Negative letter-spacing** on display and heading text creates the tight, futuristic geometric feel. Sora is designed for this.
- **Button text is slightly tracked outward** (0.01-0.015em) — unusual, but it gives button labels a precision-machined quality that complements the metallic surfaces.
- **Label text is heavily tracked** (0.04em) — all-uppercase is NOT used (it reads as shouting), but wide tracking at small size creates a quiet, technical label feel.
- **Font-smoothing:** `antialiased` always. Critical for Sora's thin strokes at small sizes.
- **Text-wrap:** `balance` for headings, `pretty` for body.

#### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@100..800&family=Manrope:wght@200..800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&display=swap" rel="stylesheet">
```

**Fallback chain:** `"Sora", "Outfit", system-ui, sans-serif` (display) / `"Manrope", "Outfit", system-ui, sans-serif` (body) / `"Fira Code", "JetBrains Mono", ui-monospace, monospace` (code)

---

### Elevation System

**Strategy:** `layered-shadows` — with metallic undertones

Iridescent surfaces need shadows that carry color. In Holographic mode, shadows have a faint violet cast. In Chrome mode, shadows are warm grey with golden ambient undertones. This subtle color in shadows is what sells the metallic illusion — real chrome casts colored reflections into its own shadows.

#### Surface Hierarchy

| Surface | Background | Shadow | Special | Usage |
|---|---|---|---|---|
| page | page token (solid) | none | -- | Main page canvas |
| card | surface token | shadow-card | Conic border on hover | Cards, input areas |
| recessed | recessed token | shadow-inset | -- | Code blocks, inset areas |
| active | active token | none | -- | Active/pressed states |
| overlay | surface token | shadow-popover | Conic border always visible | Popovers, dropdowns |
| hero | surface token | shadow-hero | Continuous conic rotation | Hero card, primary showcase |

#### Shadow Tokens — Holographic Mode

Shadows carry a faint violet-blue cast from the prismatic palette:

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `0 1px 2px rgba(123,104,238,0.04), 0 1px 3px rgba(0,0,0,0.03)` | Small elements, badges |
| shadow-card | `0 1px 2px rgba(123,104,238,0.06), 0 4px 12px rgba(123,104,238,0.04), 0 0 0 1px rgba(192,192,208,0.12)` | Card rest state. Violet-tinged ambient + hairline ring. |
| shadow-card-hover | `0 2px 4px rgba(123,104,238,0.08), 0 8px 24px rgba(123,104,238,0.06), 0 0 0 1px rgba(192,192,208,0.20)` | Card hover. Shadow deepens and spreads with violet cast. |
| shadow-input | `0 1px 3px rgba(123,104,238,0.05), 0 4px 16px rgba(0,0,0,0.03), 0 0 0 1px rgba(192,192,208,0.15)` | Input card rest |
| shadow-input-hover | `0 2px 6px rgba(123,104,238,0.06), 0 6px 20px rgba(0,0,0,0.04), 0 0 0 1px rgba(192,192,208,0.25)` | Input card hover |
| shadow-input-focus | `0 2px 6px rgba(123,104,238,0.08), 0 6px 20px rgba(0,0,0,0.05), 0 0 0 2px rgba(123,104,238,0.35)` | Input card focus. Violet focus glow replaces ring. |
| shadow-popover | `0 2px 8px rgba(123,104,238,0.08), 0 12px 32px rgba(0,0,0,0.08), 0 0 0 1px rgba(192,192,208,0.20)` | Menus, dropdowns |
| shadow-hero | `0 4px 12px rgba(123,104,238,0.10), 0 16px 48px rgba(123,104,238,0.08), 0 32px 64px rgba(0,0,0,0.04)` | Hero showcase card. Maximum depth with prominent violet cast. |
| shadow-inset | `inset 0 1px 3px rgba(123,104,238,0.06)` | Recessed surfaces. Subtle inner shadow with violet tint. |
| shadow-none | `none` | Flat surfaces |

#### Shadow Tokens — Chrome Mode

Shadows carry warm grey-gold undertones:

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `0 1px 2px rgba(120,110,90,0.06), 0 1px 3px rgba(0,0,0,0.03)` | Small elements |
| shadow-card | `0 1px 2px rgba(120,110,90,0.08), 0 4px 12px rgba(120,110,90,0.05), 0 0 0 1px rgba(197,197,189,0.15)` | Card rest state. Warm metallic ambient. |
| shadow-card-hover | `0 2px 4px rgba(120,110,90,0.10), 0 8px 24px rgba(120,110,90,0.07), 0 0 0 1px rgba(197,197,189,0.25)` | Card hover |
| shadow-input | `0 1px 3px rgba(120,110,90,0.06), 0 4px 16px rgba(0,0,0,0.03), 0 0 0 1px rgba(197,197,189,0.15)` | Input card rest |
| shadow-input-hover | `0 2px 6px rgba(120,110,90,0.08), 0 6px 20px rgba(0,0,0,0.04), 0 0 0 1px rgba(197,197,189,0.25)` | Input card hover |
| shadow-input-focus | `0 2px 6px rgba(120,110,90,0.10), 0 6px 20px rgba(0,0,0,0.05), 0 0 0 2px rgba(139,92,246,0.30)` | Input card focus. Violet focus glow. |
| shadow-popover | `0 2px 8px rgba(120,110,90,0.10), 0 12px 32px rgba(0,0,0,0.08), 0 0 0 1px rgba(197,197,189,0.20)` | Menus, dropdowns |
| shadow-hero | `0 4px 12px rgba(120,110,90,0.12), 0 16px 48px rgba(120,110,90,0.08), 0 32px 64px rgba(0,0,0,0.04)` | Hero showcase card |
| shadow-inset | `inset 0 1px 3px rgba(120,110,90,0.06)` | Recessed surfaces |
| shadow-none | `none` | Flat surfaces |

#### Separation Recipe

Surface hierarchy through tinted layered shadows + conic-gradient border activation on interaction. At rest, surfaces separate through subtle tint-step backgrounds (page -> bg -> surface) and single-layer hairline rings. On interaction, the conic gradient border activates, creating a dramatic prismatic/metallic edge that makes the surface "pop." No visible dividers between content areas. No `backdrop-filter` blur — depth comes from shadow color and gradient borders, not translucency. The shadow tint (violet for Holographic, warm gold for Chrome) creates the illusion that surfaces are reflecting colored light from the conic gradient borders.

---

### Border System

#### Widths and Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| subtle | 1px | `border-base` at 12% | Section dividers, hairlines |
| card | 1px | `border-base` at 20% | Card borders at rest |
| hover | 1px | `border-base` at 30% | Hovered elements (before conic activates) |
| conic-hover | 2px | Conic gradient (mode-dependent) | Interactive element hover — replaces static border |
| conic-active | 2px | Conic gradient, angle shifted | Interactive element active/focus |
| input | 1px | `border-base` at 15% | Form input borders at rest |
| input-hover | 1px | `border-base` at 28% | Input hover |
| input-focus | 2px | Accent-primary at 50% | Input focus (solid accent, not conic — too distracting for text entry) |

#### Focus Ring — Holographic Mode

- **Color:** `rgba(123, 104, 238, 0.45)` — Prism Violet at 45%
- **Width:** 2px solid
- **Offset:** 2px
- **Implementation:** `box-shadow: 0 0 0 2px #FFFFFF, 0 0 0 4px rgba(123,104,238,0.45)`
- The white inner ring prevents the violet from bleeding into the element's surface

#### Focus Ring — Chrome Mode

- **Color:** `rgba(139, 92, 246, 0.40)` — Chrome Violet at 40%
- **Width:** 2px solid
- **Offset:** 2px
- **Implementation:** `box-shadow: 0 0 0 2px #FFFFFF, 0 0 0 4px rgba(139,92,246,0.40)`

#### Conic Border Activation Pattern

This is the key interaction: static borders become conic gradients on hover.

```css
/* Card border — static at rest, conic on hover */
.iridescent-card {
  --angle: 0deg;
  position: relative;
  border: 1px solid rgba(var(--border-base-rgb), 0.20);
  border-radius: 12px;
  transition: border-color 0.15s ease;
}

/* Conic border pseudo-element — hidden at rest */
.iridescent-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  padding: 2px;
  background: var(--conic-gradient);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease, --angle 0.6s cubic-bezier(0.22, 0.68, 0, 1.12);
}

/* Hover: reveal conic border, hide static border */
.iridescent-card:hover {
  border-color: transparent;
}
.iridescent-card:hover::before {
  opacity: 1;
  --angle: 90deg;
}
```

---

### Component States

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg accent-primary, border none, color text-onAccent, radius 10px, h 36px, padding `0 20px`, font button (Sora 500/600), shadow shadow-sm |
| Hover | bg accent-primary darkened 8% via `color-mix(in oklch, var(--accent-primary) 88%, black)`, shadow shadow-card, conic-gradient pseudo-border fades in at 30% opacity |
| Active | transform `scale(0.96)`, shadow shadow-sm (shadow reduces on press) |
| Focus | box-shadow: focus ring (violet) appended to existing shadow |
| Disabled | opacity 0.45, pointer-events none, cursor not-allowed, no conic effects |
| Transition | background 120ms spring-out, transform 100ms spring-out, box-shadow 200ms ease |

#### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border none, color text-secondary, radius 8px, size 36x36px |
| Hover | bg `rgba(var(--border-base-rgb), 0.08)`, color text-primary, specular-highlight pseudo at 50% opacity |
| Active | bg `rgba(var(--border-base-rgb), 0.14)`, transform `scale(0.96)` |
| Focus | focus ring |
| Disabled | opacity 0.45, pointer-events none |
| Transition | background 250ms out-quart, color 250ms out-quart |

#### Buttons (Secondary / Iridescent)

The signature button. Transparent at rest with a subtle border, conic-gradient border on hover.

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid border-base at 20%`, color text-primary, radius 10px, h 36px, padding `0 20px`, font button, shadow none |
| Hover | border-color transparent, conic-gradient pseudo-border at 100% opacity, bg surface token, shadow shadow-card, specular-highlight overlay at 60% opacity |
| Active | transform `scale(0.96)`, shadow shadow-sm |
| Focus | conic-gradient border stays visible + focus ring overlaid |
| Disabled | opacity 0.45, pointer-events none, no conic effects |
| Transition | all 200ms spring-out |

#### Text Input

| State | Properties |
|---|---|
| Rest | bg surface, border `1px solid border-base at 15%`, radius 10px, h 44px, padding `0 14px`, color text-primary, placeholder text-muted, caret-color accent-primary, shadow shadow-input |
| Hover | border at 28% opacity, shadow shadow-input-hover |
| Focus | border `2px solid accent-primary at 50%`, shadow shadow-input-focus, outline none. No conic gradient — too distracting during text entry. |
| Disabled | opacity 0.45, pointer-events none, shadow none |
| Transition | border-color 150ms ease, box-shadow 200ms ease |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg surface, radius 20px, border `1px solid border-base at 15%`, shadow shadow-card |
| Hover | shadow shadow-card-hover, border at 25% |
| Focus-within | shadow shadow-input-focus, conic-gradient pseudo-border fades in subtly at 40% opacity. The card gets the signature shimmer when active. |
| Transition | all 250ms spring-out |

#### Cards

| State | Properties |
|---|---|
| Rest | bg surface, border `1px solid border-base at 20%`, radius 12px, shadow shadow-card |
| Hover | shadow shadow-card-hover, border-color transparent, conic-gradient pseudo-border at 100% opacity, specular-highlight overlay at 40% opacity. The card shimmers on hover. |
| Transition | box-shadow 250ms spring-out, opacity (pseudo) 400ms ease |

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color text-secondary, radius 8px, h 34px, padding `6px 14px`, font bodySmall |
| Hover | bg `rgba(var(--border-base-rgb), 0.08)`, color text-primary |
| Active (current) | bg active token, color text-primary, font-weight 500, left-border `2px solid accent-primary` |
| Active press | transform `scale(0.985)` |
| Transition | color 80ms out-quart, background 80ms out-quart |

#### Chips

| State | Properties |
|---|---|
| Rest | bg `rgba(var(--border-base-rgb), 0.06)`, border `1px solid border-base at 15%`, radius 20px (pill), h 32px, padding `0 14px`, font bodySmall, color text-secondary |
| Hover | bg `rgba(var(--border-base-rgb), 0.12)`, border at 25%, color text-primary, faint conic shimmer on border at 30% opacity |
| Selected | bg accent-primary at 10%, border accent-primary at 30%, color accent-primary |
| Active press | transform `scale(0.98)` |
| Transition | all 150ms ease |

#### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 40px |
| Track height | 22px |
| Track radius | 9999px (full) |
| Track off bg | `rgba(var(--border-base-rgb), 0.20)` |
| Track off ring | `1px solid border-base at 15%` |
| Track on bg | Holographic: `#2DD4A8` / Chrome: `#22C55E` |
| Track on ring | `1px solid` (success color darkened 10%) |
| Thumb | 18px white circle |
| Thumb shadow | `0 1px 3px rgba(0,0,0,0.10), 0 1px 2px rgba(0,0,0,0.06)` |
| Ring hover | thickens to 1.5px, track bg lightens 5% |
| Transition | 200ms spring-out |
| Focus-visible | mode-appropriate focus ring |

#### Popover Menu Items

| State | Properties |
|---|---|
| Rest | bg transparent, color text-secondary, radius 8px, h 34px, padding `6px 10px`, font bodySmall |
| Hover | bg `rgba(var(--border-base-rgb), 0.08)`, color text-primary |
| Active | bg `rgba(var(--border-base-rgb), 0.14)` |
| Transition | 80ms ease |

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. General purpose. |
| spring-out | `cubic-bezier(0.22, 0.68, 0, 1.12)` | Spring-feel with slight overshoot. The signature easing — simulates magnetic/spring snap. |
| spring-heavy | `cubic-bezier(0.16, 0.84, 0.1, 1.18)` | Heavier spring with more overshoot. For hero elements and page transitions. |
| out-quart | `cubic-bezier(0.165, 0.85, 0.45, 1)` | Snappy deceleration. Sidebar interactions. |
| out-expo | `cubic-bezier(0.19, 1, 0.22, 1)` | Smooth open/close for panels. |
| metallic-snap | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Sharp overshoot then settle. Like a metal click. Toggle snaps. |

For Motion (framer-motion) spring-based animations:
- **Standard:** `type: "spring", stiffness: 280, damping: 22` — card appearances, conic border reveals
- **Magnetic:** `type: "spring", stiffness: 400, damping: 28` — button presses, chip selections (magnetic snap feel)
- **Float:** `type: "spring", stiffness: 120, damping: 18` — hero element entrance, page transitions (floaty, iridescent)
- **Snap:** `type: "spring", stiffness: 600, damping: 35` — toggles, quick state changes (metallic click)

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 80ms | out-quart | Quick state change, color only |
| Button hover bg | 120ms | spring-out | Background tint with slight spring |
| Toggle snap | 150ms | metallic-snap | Sharp metallic click feel |
| Chip select | 150ms | spring-out | Selection with magnetic feel |
| Card shadow escalation | 250ms | spring-out | Shadow deepens with spring overshoot |
| Conic border reveal | 400ms | ease (opacity), spring-out (angle) | Gradient fades in, angle springs to position |
| Specular highlight | 400ms | ease | Light catch fades in smoothly |
| Input card focus | 200ms | default | Border and shadow transition |
| Ghost icon button | 250ms | out-quart | Background tint reveal |
| Panel open/close | 450ms | spring-heavy | Spring entrance with float |
| Hero card entrance | 600ms | spring-heavy | Dramatic spring with conic spin-up |
| Conic rotation (continuous) | 8000ms | linear | Perpetual rotation for hero elements |
| `--angle` hover snap | 600ms | spring-out | Angle property springs to new position |

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Barely perceptible |
| Chips | 0.98 | Slightly more visible |
| Buttons | 0.96 | Pronounced press with spring bounce-back |
| Tabs | 0.95 | Most pronounced |
| Cards (clickable) | 0.99 | Very subtle — cards are large |

---

### Overlays

#### Popover / Dropdown

- **bg:** surface token (pure white)
- **border:** `1px solid border-base at 20%` + conic-gradient pseudo-border at 60% opacity (always visible — popovers are elevated enough to warrant persistent shimmer)
- **radius:** 14px
- **shadow:** shadow-popover
- **padding:** 6px
- **z-index:** 50
- **min-width:** 200px, **max-width:** 320px
- **overflow-y:** auto
- **Menu item:** 6px 10px padding, radius 8px, h 34px, font bodySmall, color text-secondary
- **Menu item hover:** bg `rgba(var(--border-base-rgb), 0.08)`, color text-primary
- **Entry:** scale `0.95` to `1.0` + opacity `0` to `1`, 250ms spring-out
- **Exit:** opacity `1` to `0` + scale `1.0` to `0.97`, 150ms ease
- **Transition:** 80ms ease (item interactions)

#### Modal

- **Overlay bg:** `rgba(0,0,0,0.30)`
- **Overlay backdrop-filter:** `blur(8px)` — subtle background defocus
- **Content bg:** surface token
- **Content border:** conic-gradient pseudo-border at 40% opacity (subtle persistent shimmer)
- **Content shadow:** shadow-hero (maximum depth)
- **Content radius:** 16px
- **Entry:** scale `0.92` to `1.0` + opacity `0` to `1` + y `12px` to `0`, 400ms spring-heavy
- **Exit:** opacity `1` to `0` + scale `1.0` to `0.96`, 200ms ease

#### Tooltip

- **bg:** text-primary color (inverted — dark tooltip on light theme)
- **color:** `#FFFFFF`
- **font:** label size (12px), Manrope 500
- **radius:** 6px
- **padding:** 5px 10px
- **shadow:** shadow-sm
- **No arrow.** Position via offset.
- **Entry:** opacity `0` to `1` + y `4px` to `0`, 120ms ease

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column |
| Narrow max-width | 672px | Landing/focused content |
| Sidebar width | 280px | Fixed sidebar |
| Header height | 52px | Top bar |
| Spacing unit | 4px | Base multiplier |

#### Spacing Scale

4, 6, 8, 10, 12, 16, 24, 32px

#### Density

Comfortable. Generous whitespace lets the conic gradient borders breathe. 14-16px internal card padding, 8px gaps between list items, 24-32px section spacing. Iridescent effects need surrounding negative space to feel premium rather than cluttered.

#### Radius Scale

| Token | Value | Usage |
|---|---|---|
| none | 0px | -- |
| sm | 4px | Badges, small tags |
| md | 8px | Sidebar items, menu items, ghost buttons |
| lg | 12px | Cards, popovers |
| xl | 14px | Overlay containers |
| 2xl | 20px | Chat input card, hero panels |
| input | 10px | Form inputs, textareas |
| full | 9999px | Avatars, toggles, chips, pills |

#### Responsive Notes

- **lg (1024px+):** Full sidebar (280px) + content column. Conic borders at full 2px width. Hero elements animate with continuous rotation.
- **md (768px):** Sidebar collapses to overlay panel (slides in with spring-heavy easing). Conic border width reduces to 1.5px.
- **sm (640px):** Single column. Card radii reduce from 12px to 8px. Chat input radius reduces from 20px to 14px. Conic rotation pauses on hero elements (static gradient). `--angle` transitions still work on hover.

---

### Accessibility Tokens

| Token | Holographic Value | Chrome Value |
|---|---|---|
| Focus ring color | `rgba(123, 104, 238, 0.45)` — Prism Violet at 45% | `rgba(139, 92, 246, 0.40)` — Chrome Violet at 40% |
| Focus ring width | 2px solid | 2px solid |
| Focus ring offset | 2px (white inner ring) | 2px (white inner ring) |
| Focus ring CSS | `0 0 0 2px #FFF, 0 0 0 4px rgba(123,104,238,0.45)` | `0 0 0 2px #FFF, 0 0 0 4px rgba(139,92,246,0.40)` |
| Disabled opacity | 0.45 | 0.45 |
| Disabled pointer-events | none | none |
| Disabled cursor | not-allowed | not-allowed |
| Disabled conic effects | removed entirely — no shimmer on disabled elements | same |
| Selection bg | `rgba(123,104,238,0.18)` | `rgba(139,92,246,0.18)` |
| Selection color | text-primary (unchanged) | text-primary (unchanged) |
| Scrollbar width | thin | thin |
| Scrollbar thumb | `rgba(192,192,208,0.35)` | `rgba(197,197,189,0.35)` |
| Scrollbar track | transparent | transparent |
| Min touch target | 44px | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) | WCAG AA |

**Conic gradient accessibility note:** The animated conic-gradient borders are purely decorative. They do not convey information. All state changes (hover, focus, active, disabled) are also communicated through shadow depth changes, color shifts, or structural changes (scale, border-width) that remain visible when the conic effect is disabled. Under `prefers-reduced-motion`, the `--angle` animation stops, but the static gradient border is preserved as a visual indicator.

**Contrast check:** Holographic — `#1A1A2E` on `#F5F5F8` = 14.8:1. Chrome — `#1E1E1E` on `#F3F2EF` = 14.2:1. Both well above AA. Secondary text: `#5A5A7A` on `#F5F5F8` = 5.6:1 (AA pass). `#6B6B65` on `#F3F2EF` = 4.9:1 (AA pass).

---

### Visual Style

- **Grain:** None. Chrome and holographic surfaces are polished and pristine. Any noise would undermine the reflective quality.
- **Gloss:** Soft sheen to gloss. The specular-highlight pseudo-element creates directional light catch on hover. This is the closest the theme gets to a physical material — a faint white conic sweep that simulates studio lighting on a chrome surface.
- **Blend mode:** `overlay` for specular highlights, `color` for holographic hue-shift overlays. These are applied via pseudo-elements, not on primary surfaces. Primary content compositing is always `normal`.
- **Shader bg:** False. No WebGL backgrounds. The conic-gradient CSS technique provides all the visual complexity needed. A WebGL shader would be overkill and hurt performance.
- **Material quality:** The material is polished metal (Chrome mode) or holographic foil (Holographic mode). Both are smooth, reflective, precision-finished. Surfaces catch light at angles. Edges are crisp. The conic gradient border IS the material — it is the visual evidence that the surface is reflective.
- **Color temperature:** Holographic mode skews cool (blue-violet shadows, cool grey backgrounds). Chrome mode skews warm (golden shadows, warm grey backgrounds). The temperature difference is the primary distinguishing characteristic between modes.

---

### Signature Animations

#### 1. Conic Border Reveal

The defining micro-interaction. When a card is hovered, its static border fades to transparent and a conic-gradient pseudo-element fades in, with the `--angle` springing from 0deg to 90deg. The gradient appears to "spin up" as it materializes. On mouse leave, the gradient fades out and the static border returns.

```css
@property --angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.conic-card {
  --angle: 0deg;
  position: relative;
  border: 1px solid rgba(var(--border-base-rgb), 0.20);
  border-radius: 12px;
  transition: border-color 0.2s ease;
}

.conic-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  padding: 2px;
  background: conic-gradient(from var(--angle), var(--conic-stops));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease, --angle 0.6s cubic-bezier(0.22, 0.68, 0, 1.12);
}

.conic-card:hover {
  border-color: transparent;
}
.conic-card:hover::before {
  opacity: 1;
  --angle: 90deg;
}
```

Uses: 400ms ease (opacity) + 600ms spring-out (`--angle`). The staggered timing is deliberate — the border appears before the angle settles, creating a "shimmer then lock" sequence.

#### 2. Specular Glint

On hover, a white conic sweep crosses the card surface like studio lighting catching polished metal. The sweep is a conic-gradient with a narrow white arc at variable opacity, rotated from 0 to 120deg over 400ms.

```css
.specular-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: conic-gradient(
    from var(--angle),
    transparent 0deg,
    rgba(255,255,255,0.06) 50deg,
    rgba(255,255,255,0.12) 80deg,
    rgba(255,255,255,0.06) 110deg,
    transparent 160deg,
    transparent 360deg
  );
  mix-blend-mode: overlay;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.specular-card:hover::after {
  opacity: 1;
}
```

This is Chrome mode's primary interaction signature. Holographic mode uses the same technique but with the full-spectrum conic gradient at very low opacity (0.03-0.06) instead of white.

#### 3. Magnetic Spring Press

Buttons and interactive elements press with a spring easing that overshoots slightly on release — the element scales down to 0.96 on press, then springs back to 1.0 with a subtle overshoot to 1.01 before settling. This creates a magnetic, clicky feel that complements the metallic aesthetic.

```css
.magnetic-press {
  transition: transform 0.15s cubic-bezier(0.22, 0.68, 0, 1.12);
}
.magnetic-press:active {
  transform: scale(0.96);
}
/* On release, the spring-out easing naturally overshoots past 1.0 */
```

For Motion: `whileTap={{ scale: 0.96 }}` with `transition: { type: "spring", stiffness: 600, damping: 30 }`.

#### 4. Hero Conic Rotation

The hero element (primary showcase card, landing page feature) has a continuous slow-rotating conic-gradient border. The rotation is 8 seconds per revolution, linear. This is the ONE element on the page that shimmers constantly, making it the undeniable focal point.

```css
@keyframes conic-spin {
  from { --angle: 0deg; }
  to { --angle: 360deg; }
}

.hero-showcase {
  position: relative;
}
.hero-showcase::before {
  /* conic gradient pseudo-border */
  animation: conic-spin 8s linear infinite;
  opacity: 0.7; /* Slightly transparent — not full intensity */
}

@media (prefers-reduced-motion: reduce) {
  .hero-showcase::before {
    animation: none;
    --angle: 45deg; /* Static diagonal position */
  }
}
```

#### 5. Staggered Prismatic Entry

Page sections enter with a staggered reveal where each card's conic border activates sequentially, creating a "wave of light" across the grid. Cards fade in with `opacity 0→1` + `translateY(16px→0)` over 400ms with spring-heavy easing, staggered at 100ms intervals. Each card's conic border does a single 180deg sweep during entry, then settles to its rest state.

For Motion:
```jsx
const container = {
  show: { transition: { staggerChildren: 0.1 } }
};
const item = {
  hidden: { opacity: 0, y: 16, "--angle": "0deg" },
  show: {
    opacity: 1, y: 0, "--angle": "180deg",
    transition: { type: "spring", stiffness: 280, damping: 22 }
  }
};
```

---

### Dark Mode Variant

**Not natively dark.** Both Holographic and Chrome modes are light-background-native. The dark variant inverts the canvas while preserving mode identity.

#### Dark Palette — Holographic

| Token | Light Value | Dark Value | Notes |
|---|---|---|---|
| page | `#F5F5F8` | `#121218` | Deep cool black-navy |
| bg | `#FAFAFC` | `#1A1A24` | Elevated dark surface |
| surface | `#FFFFFF` | `#222230` | Card surface — dark with blue cast |
| recessed | `#EEEEF2` | `#0E0E14` | Deep recessed |
| active | `#E8E8F0` | `#2A2A3A` | Active press |
| text-primary | `#1A1A2E` | `#F0F0F8` | Near-white with cool cast |
| text-secondary | `#5A5A7A` | `rgba(220,220,240,0.65)` | Cool grey at 65% |
| text-muted | `#9494AC` | `rgba(220,220,240,0.35)` | Cool grey at 35% |
| border-base | `#C0C0D0` | `#404058` | Lighter separator for dark |
| accent-primary | `#7B68EE` | `#9B8AFE` | Brighter violet for dark bg |
| accent-secondary | `#00D4FF` | `#38E8FF` | Brighter cyan |
| success | `#2DD4A8` | `#3EEAB8` | Brighter mint |
| warning | `#FFB020` | `#FFC040` | Brighter amber |
| danger | `#FF5A7E` | `#FF7A9E` | Brighter rose |

#### Dark Palette — Chrome

| Token | Light Value | Dark Value | Notes |
|---|---|---|---|
| page | `#F3F2EF` | `#141412` | Deep warm black |
| bg | `#F9F8F6` | `#1C1C18` | Elevated dark surface |
| surface | `#FFFFFF` | `#24241E` | Card surface — dark with warm cast |
| recessed | `#EAEAE6` | `#0C0C0A` | Deep recessed |
| active | `#E2E1DC` | `#2E2E26` | Active press |
| text-primary | `#1E1E1E` | `#F2F2EE` | Near-white with warm cast |
| text-secondary | `#6B6B65` | `rgba(235,235,225,0.65)` | Warm grey at 65% |
| text-muted | `#A0A098` | `rgba(235,235,225,0.35)` | Warm grey at 35% |
| border-base | `#C5C5BD` | `#484840` | Lighter separator |
| accent-primary | `#8B5CF6` | `#A78BFA` | Brighter violet |
| accent-secondary | `#D4A853` | `#E8BC67` | Brighter gold |
| success | `#22C55E` | `#34D071` | Brighter green |
| warning | `#F59E0B` | `#FBBF24` | Brighter amber |
| danger | `#EF4444` | `#F87171` | Brighter red |

#### Dark Mode Rules

- Conic gradient hue stops remain the same — the rainbow/metallic sweep works on dark backgrounds without modification
- Conic gradient opacity increases by 15% in dark mode (dark backgrounds absorb more light, gradients need to be more prominent)
- Shadow colors shift: violet-tint shadows in Holographic become more saturated (`rgba(123,104,238,0.12)` base); warm shadows in Chrome become more golden (`rgba(212,168,83,0.10)` base)
- Specular-highlight pseudo-elements increase white-arc opacity by 20% for dark mode (the light catch needs to be brighter against dark surfaces)
- Focus ring remains mode-appropriate violet — works well on both light and dark
- Scrollbar thumb: Holographic `rgba(220,220,240,0.25)`, Chrome `rgba(235,235,225,0.25)`
- Selection bg: same accent at 25% (increased from 18% for visibility on dark)
- inlineCode: Holographic `#9B8AFE` (brightened violet), Chrome `#A78BFA`

---

### Dual-Mode Comparison Table

| Dimension | Holographic | Chrome |
|---|---|---|
| Temperature | Cool (blue-violet) | Warm (gold-grey) |
| Conic gradient | Full rainbow spectrum (7 stops) | Monochrome silver sweep (6 stops) |
| Shadow tint | Violet cast (`rgba(123,104,238,...)`) | Warm gold cast (`rgba(120,110,90,...)`) |
| Accent primary | `#7B68EE` Medium Slate Blue | `#8B5CF6` Violet |
| Accent secondary | `#00D4FF` Cyan | `#D4A853` Gold |
| Page background | `#F5F5F8` Cool near-white | `#F3F2EF` Warm greige |
| Display weight | 700 (bold) | 800 (extra bold) |
| Button weight | 500 (medium) | 600 (semibold) |
| Specular highlight | Rainbow hue-shift overlay at very low opacity | White-arc conic sweep at medium opacity |
| Blend mode usage | `color` blend for hue shift | `overlay` blend for light catch |
| Feel | Ethereal, weightless, prismatic | Premium, grounded, metallic |
| Reference | Soap bubbles, holographic stickers, CD backs | Automotive chrome, titanium devices, luxury tech |
| Success color | `#2DD4A8` Mint (cooler) | `#22C55E` Emerald (standard) |
| Border separator | `#C0C0D0` Cool silver | `#C5C5BD` Warm silver |

#### CSS Custom Property Toggle

```css
:root {
  --mode: holographic;

  /* Mode-dependent tokens resolved via fallback */
  --conic-stops: #ff6b6b, #ffa500, #ffd700, #7fff00, #00d4ff, #7b68ee, #ff6b9d, #ff6b6b;
  --page: #F5F5F8;
  --bg: #FAFAFC;
  --shadow-tint: 123, 104, 238;
  /* ... all mode-dependent tokens */
}

[data-mode="chrome"] {
  --conic-stops: #A0A0A0, #C8C8C8, #F0F0F0, #FFFFFF, #D0D0D0, #A0A0A0;
  --page: #F3F2EF;
  --bg: #F9F8F6;
  --shadow-tint: 120, 110, 90;
  /* ... chrome overrides */
}
```

---

### Mobile Notes

#### Effects to Disable
- Hero conic rotation (signature #4) — pauses to static gradient at 45deg
- Specular glint animation (signature #2) — disabled; static specular highlight at 50% opacity
- Staggered prismatic entry (signature #5) — collapses to simple fade-in with no conic sweep
- Depth parallax (if implemented) — disabled entirely
- `mix-blend-mode` overlays — removed on mobile for GPU performance

#### Adjustments
- Conic-gradient pseudo-element border width: 2px reduces to 1.5px
- Card border-radius: 12px reduces to 8px
- Chat input border-radius: 20px reduces to 14px
- Shadow complexity: hero shadow reduces from 3 layers to 2 layers
- `--angle` transition duration increases by 30% (slower springs feel smoother on 60Hz mobile displays)
- All interactive elements maintain minimum 44px touch target
- Body text stays 16px (already comfortable for mobile)
- Conic border reveal on tap: holds for 300ms before fade-out (touch needs longer dwell time than hover)

#### Performance Notes
- `conic-gradient` is GPU-composited and performs well on modern mobile browsers
- The `mask-composite` technique for rounded conic borders is the heaviest operation — limit to 3-4 visible elements with conic borders on screen simultaneously
- `@property` animation is well-optimized in WebKit; no performance concerns on iOS Safari 15.4+
- Apply `will-change: transform, opacity` only during conic border transitions, never permanently
- Total pseudo-element count per visible card: maximum 2 (conic border + specular highlight). On mobile, remove specular highlight pseudo (reduce to 1).
- Prefer `border-image` (which doesn't support border-radius) over the `mask-composite` technique on mobile for simpler elements like badges and chips — it's significantly cheaper.

---

### Implementation Checklist

- [ ] Google Fonts loaded: Sora (variable 100-800), Manrope (variable 200-800), Fira Code (variable 300-700)
- [ ] `@property --angle` registered with `syntax: '<angle>'`
- [ ] CSS custom properties defined for all color tokens (both Holographic and Chrome palettes)
- [ ] Mode toggle via `[data-mode]` attribute with complete token override
- [ ] `conic-gradient` border pseudo-element pattern implemented (with `mask-composite` for rounded corners)
- [ ] `@supports not (syntax: '<angle>')` fallback defined (solid accent border, no rotation)
- [ ] Border-radius scale applied per component (4, 6, 8, 10, 12, 14, 20px)
- [ ] Shadow tokens applied per mode with correct tint color (violet for Holographic, warm gold for Chrome)
- [ ] Shadow escalation on hover/focus for cards and inputs
- [ ] Conic border reveal animation: opacity fade + `--angle` spring on hover
- [ ] Specular highlight pseudo-element with `mix-blend-mode: overlay` on cards
- [ ] Spring easing curves defined in CSS: `cubic-bezier(0.22, 0.68, 0, 1.12)` as primary
- [ ] Border opacity system implemented (12%, 20%, 30%, 45% on `border-base`)
- [ ] Focus ring per mode: Holographic `rgba(123,104,238,0.45)`, Chrome `rgba(139,92,246,0.40)` with white inner ring
- [ ] `prefers-reduced-motion`: conic rotation pauses (static angle), spring easings replaced with standard ease, specular animations disabled
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] Scrollbar styled: thin, mode-appropriate thumb color, transparent track
- [ ] Touch targets >= 44px on all interactive elements
- [ ] State transitions match motion map durations and easings
- [ ] `::selection` styled with accent at 18%
- [ ] `::placeholder` opacity matches text-muted token
- [ ] Dark mode variant: all tokens swap, conic opacity increases 15%, specular brightness increases 20%
- [ ] Hero element: continuous `conic-spin` at 8s/revolution with `prefers-reduced-motion` pause
- [ ] Dual-mode comparison verified: switching `data-mode` attribute cleanly swaps all visual characteristics
- [ ] Mobile: specular highlight pseudo removed, conic border width reduced, hero rotation paused
- [ ] `conic-gradient` stops verified: Holographic = 7-stop rainbow loop, Chrome = 6-stop silver loop
