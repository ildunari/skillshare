# Ethereal Porcelain — Full Specification

> Schema v2 | 979 lines | Last updated: 2026-02-16

## Table of Contents

| Section | Line |
|---|---|
| Identity & Philosophy | 36 |
| Color System | 57 |
| Typography Matrix | 120 |
| Elevation System | 168 |
| Border System | 279 |
| Component States | 318 |
| Motion Map | 455 |
| Overlays | 510 |
| Layout Tokens | 566 |
| Accessibility Tokens | 616 |
| Visual Style | 650 |
| Signature Animations | 747 |
| Dark Mode Variant | 883 |
| Data Visualization | 913 |
| Mobile Notes | 927 |
| Implementation Checklist | 955 |

---

## 2. Ethereal Porcelain

> Cool gallery neutrals with subsurface scattering -- surfaces glow faintly from within, like porcelain held to light.

**Best for:** Fluid dynamics simulations, fractals, mathematical art, scientific visualization, gallery/portfolio sites, museum exhibits, architectural presentations, photography portfolios.

---

### Identity & Philosophy

This theme lives in a contemporary art gallery. The walls are cool grey -- not warm cream, not sterile white. The lighting is diffused, indirect, calibrated. The work on display seems to emit its own quiet luminosity, as if the surfaces themselves are translucent and the light passes through rather than bouncing off. You lean closer to a porcelain vessel and notice the faintest warm glow where the wall behind bleeds through the material. That is subsurface scattering -- the defining visual technique of this theme.

The core tension is **cool vs warm**. The palette is overwhelmingly cool: slate backgrounds, blue-grey secondaries, charcoal text. But the accent colors -- antique gold, soft rose -- introduce warmth at strategic moments. This is the tension of a gallery frame around a painting, of gold leaf on cool marble. The cool dominates and the warm punctuates. Neither wins. The tension itself is the aesthetic.

Two registers define the theme's character. **Surface translucency** makes every card, panel, and container feel like it is made of fine porcelain rather than flat paper. This is achieved through inset box-shadows using warm accent colors at very low opacity, creating the illusion of light passing through. **Majestic pacing** makes every transition feel weighted and considered. Elements move slowly, deliberately, as if suspended in still air. Nothing snaps. Nothing bounces. Everything glides.

**Decision principle:** "When in doubt, ask: would this feel at home on a gallery wall? If it draws attention to itself, subdue it. If it disappears entirely, give it a faint inner glow."

**What this theme is NOT:**
- Not warm or cozy -- this is cool, considered, and architectural
- Not sterile or clinical -- the subsurface glow and gold accents bring life
- Not sparse to the point of emptiness -- spacious but curated, like a gallery with intention behind every placement
- Not bouncy or playful -- motion is slow, majestic, gravitational
- Not glassmorphic -- the translucency comes from within (inset glow), not from blur-through
- Not the same as Manuscript (which is warm cream, literary, dense) -- Porcelain is cool grey, gallery, spacious
- No pure black (`#000000`) or pure white (`#FFFFFF`) -- every neutral carries a cool undertone

---

### Color System

#### Palette

All neutrals carry a cool blue-grey undertone (hue 30-50 in HSL, low saturation). The accent primary is a cool antique gold that reads as gallery-frame warmth against the slate surfaces. The secondary accent is an analytical blue-grey that reinforces the cool foundation. The cool-warm tension is the palette's signature.

| Token | Name | Hex | HSL | Role |
|---|---|---|---|---|
| page | Gallery Slate | `#E4E1DC` | 34 10% 88% | Deepest background -- the gallery wall. Cool grey with the faintest warm undertone to prevent feeling sterile. |
| bg | Cool Linen | `#ECEAE6` | 40 13% 91% | Primary surface. A step lighter than the wall. The mounting board behind the work. |
| surface | Porcelain | `#F5F3F0` | 36 16% 95% | Cards, inputs, elevated surfaces. The porcelain itself -- bright, smooth, faintly luminous. |
| recessed | Dove Grey | `#E0DDD8` | 36 9% 86% | Code blocks, inset areas. Slightly darker than bg, signals depth without shadow. |
| active | Ash | `#D8D5CF` | 40 9% 83% | Active/pressed states, selected items. Noticeably darker to signal interaction. |
| text-primary | Graphite | `#2C2C2E` | 240 3% 17% | Headings, body text. Dark charcoal with a cool cast -- never warm, never pure black. |
| text-secondary | Pewter | `#6B6B70` | 240 2% 43% | Sidebar items, secondary labels, icon default color. Cool mid-grey. |
| text-muted | Silver | `#9A9A9E` | 240 2% 61% | Placeholders, timestamps, metadata. Recedes but remains legible. |
| text-onAccent | Porcelain White | `#FAF9F7` | 40 18% 97% | Text on accent-colored backgrounds. Warm white to complement gold. |
| border-base | Cool Veil | `#B8B5AE` | 42 6% 70% | Base border color, always used at variable opacity. Never applied as solid. |
| accent-primary | Antique Gold | `#B8A88A` | 38 20% 63% | Gallery-frame gold. Warm accent against cool surfaces. CTA, highlights, subsurface glow source. |
| accent-secondary | Steel Blue | `#7A8B9A` | 210 12% 54% | Cool blue-grey. Analytical counterpoint. Links, secondary actions, data visualization. |
| accent-rgb | -- | `184, 168, 138` | -- | RGB decomposition of accent-primary for use in rgba() subsurface glow values. |
| success | Celadon | `#5A8A6A` | 150 21% 45% | Positive states. Cool green with grey undertone. Gallery-appropriate, not electric. |
| warning | Aged Amber | `#A08040` | 40 43% 44% | Caution states. Muted gold-brown that harmonizes with the accent. |
| danger | Muted Rose | `#B85A5A` | 0 34% 54% | Error states. Desaturated, serious, not alarming. |
| info | Slate Blue | `#5B7FA5` | 212 30% 50% | Informational states. Cool blue, slightly desaturated. |

#### Special Colors

| Token | Value | Role |
|---|---|---|
| inlineCode | `#8A7A5A` | Code text within prose -- muted gold-brown, reads as "different register" against cool body text. |
| toggleActive | `#5B7FA5` | Toggle/switch active track. Uses the info/steel-blue tone, distinct from gold accent. |
| selection | `rgba(184, 168, 138, 0.16)` | `::selection` background. Accent gold at 16% opacity. Subtle warm highlight on cool surface. |
| subsurfaceGlow | `rgba(184, 168, 138, 0.04)` | Base inner glow color for the subsurface scattering effect on surfaces. |

#### Fixed Colors

| Token | Hex | Role |
|---|---|---|
| alwaysBlack | `#000000` | Shadow base (mode-independent) |
| alwaysWhite | `#FFFFFF` | On-dark emergencies only (mode-independent) |

#### Opacity System

One border base color (`#B8B5AE`) at variable opacity produces the entire border vocabulary:

| Level | Opacity | Usage |
|---|---|---|
| subtle | 12% | Sidebar edges, hairlines, lightest separation. Slightly lower than Editorial Calm -- gallery prefers less visible boundaries. |
| card | 20% | Card borders, file cards. Restrained, lets the subsurface glow define the edge. |
| hover | 28% | Hover states, popovers. |
| focus | 38% | Focus borders, active emphasis. |

#### Color Rules

- **Gold is earned.** Used only for accent actions (CTA, active highlights), subsurface glow calculations, and data visualization primaries. Never as decorative fill or background tint.
- **Cool-warm tension is intentional.** The palette is 80% cool grey and 20% warm gold/rose. Resist the temptation to add more warm tones -- the tension only works when cool dominates.
- **No gradients on surfaces.** Surface hierarchy comes from tint-stepping and the subsurface scattering technique. Linear or radial gradient fills on cards are forbidden.
- **Semantic colors are desaturated.** Success/warning/danger sit at reduced saturation so they coexist with the cool neutral palette. They should feel like they belong in a gallery, not a traffic light.
- **Subsurface glow uses accent-rgb.** All inner glow calculations use `rgba(184, 168, 138, ...)` -- the RGB decomposition of the antique gold accent. This creates the illusion that warm light passes through cool porcelain surfaces.

---

### Typography Matrix

#### Font Families

| Slot | Font | Fallback | Role |
|---|---|---|---|
| serif (display) | DM Serif Display | Georgia, "Times New Roman", serif | Display, Heading. High-contrast dramatic serif for gallery signage and titles. |
| sans (body) | Satoshi | system-ui, -apple-system, sans-serif | Body, Body Small, Button, Input, Label, Caption. Clean geometric sans with distinctive character. Not generic, not overused. |
| mono | Fira Code | ui-monospace, SFMono-Regular, Menlo, Monaco, monospace | Code, data values. Ligature-enabled monospace with excellent readability. |

**Family switch boundary:** DM Serif Display handles the two largest typographic roles (Display, Heading). Satoshi handles everything else (Subheading, Body, Body Small, Button, Input, Label, Caption). The contrast between a dramatic high-contrast serif and a clean geometric sans creates the gallery-signage aesthetic -- refined titles, functional labels.

**Why this pairing:** DM Serif Display evokes museum wall labels and gallery exhibition titles -- high-contrast, elegant, slightly warm in character which creates productive tension against the cool palette. Satoshi (by Indian Type Foundry) is a modern geometric sans that feels more distinctive than Inter or DM Sans without being distracting. Its slightly quirky letterforms (the distinctive 'a', the geometric 'g') add personality to body text while remaining highly readable. Fira Code brings ligature support for code display, important for scientific visualization contexts.

#### Role Matrix

| Role | Family | Size | Weight | Line-height | Letter-spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | DM Serif Display | 40px | 400 | 1.15 (46px) | -0.01em | `font-optical-sizing: auto` | Hero titles, page titles, exhibition headings. Slightly larger than Editorial Calm -- gallery scale. |
| Heading | DM Serif Display | 26px | 400 | 1.25 (32.5px) | -0.005em | -- | Section titles, settings headers, card group titles. |
| Subheading | Satoshi | 18px | 700 | 1.35 (24.3px) | 0.01em | -- | Card titles, subsection headers. Sans-serif to contrast with serif headings. |
| Body | Satoshi | 16px | 400 | 1.6 (25.6px) | normal | -- | Primary reading text. More generous line-height than Editorial Calm -- spacious gallery density. |
| Body Small | Satoshi | 14px | 400 | 1.45 (20.3px) | normal | -- | Sidebar items, form labels, secondary UI text. |
| Button | Satoshi | 14px | 500 | 1.4 (19.6px) | 0.01em | -- | Button labels. Slightly tracked for gallery-label formality. |
| Input | Satoshi | 14px | 400 | 1.4 (19.6px) | normal | -- | Form input text. |
| Label | Satoshi | 11px | 500 | 1.33 (14.6px) | 0.06em | `text-transform: uppercase` | Section labels, metadata, timestamps. Uppercase with generous tracking -- classic gallery label style. |
| Code | Fira Code | 0.9em (14.4px at 16px base) | 400 | 1.5 (21.6px) | normal | `font-variant-numeric: tabular-nums`, `font-variant-ligatures: contextual` | Inline code, code blocks, data values, scientific notation. |
| Caption | Satoshi | 12px | 400 | 1.33 (16px) | 0.01em | -- | Disclaimers, footnotes, bottom-of-page text. |

**Typography philosophy:** The serif-for-titles/sans-for-body split mirrors museum typography conventions. Gallery wall labels use a refined serif for the artwork title and a clean sans for the artist name, medium, and description. The uppercase label role with generous tracking (`0.06em`) echoes the all-caps labels found on gallery pedestals and museum plaques.

#### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&display=swap" rel="stylesheet">
```

Note: Satoshi is available from Indian Type Foundry / Fontshare at `https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap` or can be self-hosted. Fira Code is available via `https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap`.

- **Font smoothing:** `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale` on `<html>`.
- **Font display:** `font-display: swap` on all families.
- **Optical sizing:** `font-optical-sizing: auto` for DM Serif Display.
- **Text wrap:** `text-wrap: balance` for Display and Heading roles. `text-wrap: pretty` for Body paragraphs.

---

### Elevation System

**Strategy:** Subsurface-glow + subtle composite shadows.

Separation between surfaces is achieved through tint-stepping combined with the signature subsurface scattering effect. Every elevated surface (card, input, popover) carries a faint inset glow using the warm accent color at very low opacity. This glow, combined with a gentle external shadow, creates the illusion of translucent porcelain. The external shadows are deliberately understated -- depth comes from the inner glow, not from drop shadows. No visible dividers between major page sections. Popovers add `backdrop-filter: blur(20px)`.

#### Surface Hierarchy

| Surface | Background | Shadow | Inner Glow | Usage |
|---|---|---|---|---|
| page | `#E4E1DC` (page) | none | none | Deepest layer. The gallery wall. |
| canvas | `#ECEAE6` (bg) | none | none | Primary working surface. |
| card | `#F5F3F0` (surface) | shadow-card + subsurface-glow | `inset 0 1px 4px rgba(184,168,138, 0.04)` | Cards, inputs, elevated panels. The porcelain surface. |
| recessed | `#E0DDD8` (recessed) | none | none | Code blocks, inset areas. |
| active | `#D8D5CF` (active) | none | `inset 0 1px 2px rgba(184,168,138, 0.03)` | Active sidebar item, user bubble, pressed states. |
| overlay | `#F5F3F0` (surface) | shadow-popover + subsurface-glow-strong | `inset 0 1px 8px rgba(184,168,138, 0.05)` | Popovers, dropdowns, modals. |

#### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-sm | `0 1px 2px rgba(44, 44, 46, 0.04)` | Small elements. |
| shadow-md | `0 4px 8px -2px rgba(44, 44, 46, 0.06), 0 2px 4px -2px rgba(44, 44, 46, 0.03)` | Medium elevation. |
| shadow-card | `0 2px 12px rgba(44, 44, 46, 0.03), 0 0 0 0.5px rgba(184, 181, 174, 0.20)` | Card rest state. Gentler than Editorial Calm -- the glow provides most of the separation. |
| shadow-card-hover | `0 4px 16px rgba(44, 44, 46, 0.05), 0 0 0 0.5px rgba(184, 181, 174, 0.28)` | Card hover state. |
| shadow-card-focus | `0 4px 16px rgba(44, 44, 46, 0.07), 0 0 0 0.5px rgba(184, 181, 174, 0.28)` | Card focus-within. |
| shadow-input | `0 2px 12px rgba(44, 44, 46, 0.03), 0 0 0 0.5px rgba(184, 181, 174, 0.20)` | Input rest state. Same as card. |
| shadow-input-hover | `0 4px 16px rgba(44, 44, 46, 0.05), 0 0 0 0.5px rgba(184, 181, 174, 0.28)` | Input hover. |
| shadow-input-focus | `0 4px 16px rgba(44, 44, 46, 0.07), 0 0 0 0.5px rgba(184, 181, 174, 0.28)` | Input focus. |
| shadow-popover | `0 4px 16px rgba(44, 44, 46, 0.10), 0 1px 4px rgba(44, 44, 46, 0.06)` | Menus, popovers, dropdowns. |
| shadow-none | `none` | Flat surfaces, disabled states, recessed areas. |

#### Subsurface Scattering Tokens

The signature effect. These inset shadows use the warm accent color to create the illusion that light passes through the surface material.

| Token | Value | Usage |
|---|---|---|
| glow-rest | `inset 0 1px 4px rgba(184, 168, 138, 0.04), inset 0 -1px 4px rgba(184, 168, 138, 0.02)` | Default inner glow on cards and inputs. Barely visible, felt more than seen. |
| glow-hover | `inset 0 1px 8px rgba(184, 168, 138, 0.06), inset 0 -1px 6px rgba(184, 168, 138, 0.03)` | Intensified glow on hover. "More light passing through." |
| glow-active | `inset 0 1px 12px rgba(184, 168, 138, 0.08), inset 0 -1px 8px rgba(184, 168, 138, 0.04)` | Maximum glow on focus/active. The porcelain is backlit. |
| glow-popover | `inset 0 2px 12px rgba(184, 168, 138, 0.05), inset 0 -2px 8px rgba(184, 168, 138, 0.03)` | Popovers and overlays have a slightly stronger resting glow. |

**Implementation pattern -- composite shadow with subsurface glow:**

```css
/* Card at rest: external shadow + subsurface glow combined */
.card {
  background: var(--surface);
  box-shadow:
    /* Subsurface scattering (inner glow) */
    inset 0 1px 4px rgba(184, 168, 138, 0.04),
    inset 0 -1px 4px rgba(184, 168, 138, 0.02),
    /* External depth */
    0 2px 12px rgba(44, 44, 46, 0.03),
    0 0 0 0.5px rgba(184, 181, 174, 0.20);
}

/* Card on hover: glow intensifies, external shadow deepens */
.card:hover {
  box-shadow:
    /* Subsurface scattering intensified */
    inset 0 1px 8px rgba(184, 168, 138, 0.06),
    inset 0 -1px 6px rgba(184, 168, 138, 0.03),
    /* External depth deepened */
    0 4px 16px rgba(44, 44, 46, 0.05),
    0 0 0 0.5px rgba(184, 181, 174, 0.28);
}

/* Card on focus/active: maximum glow */
.card:focus-within {
  box-shadow:
    /* Subsurface scattering at maximum */
    inset 0 1px 12px rgba(184, 168, 138, 0.08),
    inset 0 -1px 8px rgba(184, 168, 138, 0.04),
    /* External depth at maximum */
    0 4px 16px rgba(44, 44, 46, 0.07),
    0 0 0 0.5px rgba(184, 181, 174, 0.28);
}
```

**Optional radial glow for hero surfaces:**

```css
/* For larger panels or hero cards, add a radial inner gradient */
.hero-card {
  background:
    radial-gradient(
      ellipse 80% 60% at 50% 30%,
      rgba(184, 168, 138, 0.03),
      transparent
    ),
    var(--surface);
}
```

#### Backdrop Filter

| Context | Value | Usage |
|---|---|---|
| popover | `backdrop-filter: blur(20px)` | Popover/dropdown containers. Slightly less than Editorial Calm -- gallery prefers clarity. |
| modal | `backdrop-filter: blur(10px)` | Modal overlay background. |
| badge | `backdrop-filter: blur(6px)` | Floating labels, file type badges. |
| none | `backdrop-filter: none` | Default, non-overlay surfaces. |

#### Separation Recipe

Tint-step + subsurface glow + whisper-thin composite shadow. The page-to-bg step (from `#E4E1DC` to `#ECEAE6`) establishes the gallery wall versus mounting board. The bg-to-surface step (from `#ECEAE6` to `#F5F3F0`) lifts cards and inputs -- the porcelain rising above the linen. The subsurface scattering effect (warm inset glow) then makes each elevated surface feel translucent rather than opaque. External shadows are deliberately restrained so the glow does the perceptual heavy lifting. Sidebar separation is a single 0.5px hairline at 12% opacity. No horizontal rules. No divider lines.

---

### Border System

#### Base Color

`#B8B5AE` (Cool Veil). This single cool grey tone, applied at variable opacity, produces the entire border vocabulary. At 12% on the cool linen background it is nearly invisible -- the gallery prefers minimal visible boundaries. At 28% it reads as a deliberate edge. At 38% it commands attention.

#### Widths and Patterns

| Pattern | Width | Opacity | CSS Value | Usage |
|---|---|---|---|---|
| subtle | 0.5px | 12% | `0.5px solid rgba(184, 181, 174, 0.12)` | Sidebar right edge, hairlines. Gallery-minimal. |
| card | 0.5px | 20% | `0.5px solid rgba(184, 181, 174, 0.20)` | Card borders. Restrained -- subsurface glow defines edges. |
| hover | 0.5px | 28% | `0.5px solid rgba(184, 181, 174, 0.28)` | Hover states, popovers. |
| input | 1px | 12% | `1px solid rgba(184, 181, 174, 0.12)` | Form input borders at rest. |
| input-hover | 1px | 28% | `1px solid rgba(184, 181, 174, 0.28)` | Form input borders on hover. |

#### Width Scale

| Name | Value | Usage |
|---|---|---|
| hairline | 0.5px | Card edges, sidebar separation, popover borders. |
| default | 1px | Form input borders. |
| medium | 1.5px | Heavy emphasis (rare). |
| heavy | 2px | Focus ring width. |

#### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(122, 139, 154, 0.50)` |
| Width | 2px solid |
| Style | `outline: 2px solid rgba(122, 139, 154, 0.50)` |
| Offset | `outline-offset: 2px` |
| Applies to | All interactive elements on `:focus-visible` |

Focus ring uses the steel-blue secondary accent at 50% opacity. This is a deliberate departure from the standard blue -- the gallery aesthetic demands that even functional elements harmonize with the palette. Steel blue provides sufficient contrast against all surface colors while feeling native to the cool grey world.

---

### Component States

#### Buttons (Primary/Outlined)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: 0.5px solid rgba(184, 181, 174, 0.28)`, `color: #2C2C2E (text-primary)`, `border-radius: 6px`, `height: 36px`, `padding: 0 16px`, `font-size: 14px`, `font-weight: 500`, `font-family: Satoshi`, `letter-spacing: 0.01em`, `cursor: pointer` |
| Hover | `bg: #E0DDD8 (recessed)`, `border-color: rgba(184, 181, 174, 0.28)` |
| Active | `transform: scale(0.975)`, `shadow: none` |
| Focus | `outline: 2px solid rgba(122, 139, 154, 0.50)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `shadow: none`, `cursor: not-allowed` |
| Transition | `color, background-color, border-color, transform 200ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Buttons (Accent/CTA)

| State | Properties |
|---|---|
| Rest | `bg: #B8A88A (accent-primary)`, `border: none`, `color: #FAF9F7 (text-onAccent)`, `border-radius: 6px`, `height: 36px`, `padding: 0 20px`, `font-size: 14px`, `font-weight: 500`, `letter-spacing: 0.01em`, `cursor: pointer` |
| Hover | `bg: #A89878` (15% darker gold) |
| Active | `transform: scale(0.975)` |
| Focus | `outline: 2px solid rgba(122, 139, 154, 0.50)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `cursor: not-allowed` |
| Transition | `background-color, transform 200ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Buttons (Ghost/Icon)

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `border: none`, `color: #6B6B70 (text-secondary)`, `border-radius: 6px`, `width: 36px`, `height: 36px`, `padding: 0`, `cursor: pointer` |
| Hover | `bg: #E0DDD8 (recessed)`, `color: #2C2C2E (text-primary)` |
| Active | `transform: scale(0.975)` |
| Focus | `outline: 2px solid rgba(122, 139, 154, 0.50)`, `outline-offset: 2px` |
| Disabled | `opacity: 0.5`, `pointer-events: none` |
| Transition | `all 400ms cubic-bezier(0.165, 0.85, 0.45, 1)` |

#### Text Input (Settings Form)

| State | Properties |
|---|---|
| Rest | `bg: #F5F3F0 (surface)`, `border: 1px solid rgba(184, 181, 174, 0.12)`, `border-radius: 8px`, `height: 44px`, `padding: 0 14px`, `font-size: 14px`, `font-weight: 400`, `font-family: Satoshi`, `color: #2C2C2E (text-primary)`, `caret-color: #B8A88A (accent-primary)`, `box-shadow: glow-rest` |
| Placeholder | `color: #9A9A9E (text-muted)` |
| Hover | `border-color: rgba(184, 181, 174, 0.28)`, `box-shadow: glow-hover + shadow-input-hover` |
| Focus | `outline: 2px solid rgba(122, 139, 154, 0.50)`, `outline-offset: 2px`, `border-color: rgba(184, 181, 174, 0.28)`, `box-shadow: glow-active + shadow-input-focus` |
| Disabled | `opacity: 0.5`, `pointer-events: none`, `cursor: not-allowed`, `box-shadow: none` |
| Transition | `border-color, box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1)` |

Note: The caret uses the gold accent color. This subtle touch brings warmth into the act of typing -- a small subsurface scattering moment at the point of interaction.

#### Textarea

| State | Properties |
|---|---|
| Rest | Same bg/border/radius as text input. `padding: 14px`, `line-height: 20.3px`, `min-height: 120px`, `resize: vertical`, `white-space: pre-wrap`, `box-shadow: glow-rest` |
| Hover/Focus/Disabled | Same escalation as text input |

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | `bg: #F5F3F0 (surface)`, `border-radius: 20px`, `border: 1px solid transparent`, `box-shadow: shadow-card + glow-rest` |
| Hover | `box-shadow: shadow-card-hover + glow-hover` |
| Focus-within | `box-shadow: shadow-card-focus + glow-active` |
| Inner textarea | `font-size: 16px`, `line-height: 25.6px`, `bg: transparent`, `color: text-primary`, `placeholder-color: text-muted`, `caret-color: #B8A88A` |
| Transition | `all 400ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Cards

| State | Properties |
|---|---|
| Rest | `bg: #F5F3F0 (surface)`, `border: 0.5px solid rgba(184, 181, 174, 0.20)`, `border-radius: 10px`, `box-shadow: shadow-card + glow-rest`, `padding: 24px` |
| Hover | `border-color: rgba(184, 181, 174, 0.28)`, `box-shadow: shadow-card-hover + glow-hover` |
| Focus | `outline: 2px solid rgba(122, 139, 154, 0.50)`, `outline-offset: 2px` (when card is clickable) |
| Transition | `border-color, box-shadow 400ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | `bg: transparent`, `color: #6B6B70 (text-secondary)`, `border-radius: 6px`, `height: 36px`, `padding: 8px 16px`, `font-size: 14px`, `font-weight: 400`, `font-family: Satoshi`, `white-space: nowrap`, `overflow: hidden`, `cursor: pointer` |
| Hover | `bg: #E0DDD8 (recessed)`, `color: #2C2C2E (text-primary)` |
| Active (current) | `bg: #D8D5CF (active)`, `color: #2C2C2E (text-primary)` |
| Active press | `transform: scale(0.985)` |
| Disabled | `pointer-events: none`, `opacity: 0.5` |
| Transition | `color, background-color 150ms cubic-bezier(0.165, 0.85, 0.45, 1)` |
| Text truncation | Gradient fade mask using `mask-image: linear-gradient(to right, black 85%, transparent)`. Not `text-overflow: ellipsis`. |

#### Section Labels (Sidebar)

| Property | Value |
|---|---|
| Font | Satoshi, 11px, weight 500, color `#9A9A9E (text-muted)` |
| Line-height | 14.6px |
| Letter-spacing | 0.06em |
| Text-transform | uppercase |
| Padding | `0 8px 8px` |
| Margin-top | 8px |

Gallery-style all-caps labels with generous tracking.

#### Chips (Landing Quick Actions)

| State | Properties |
|---|---|
| Rest | `bg: #ECEAE6 (bg)`, `border: 0.5px solid rgba(184, 181, 174, 0.12)`, `border-radius: 10px`, `height: 36px`, `padding: 0 14px`, `font-size: 14px`, `font-weight: 400`, `font-family: Satoshi`, `color: #6B6B70 (text-secondary)`, `cursor: pointer`, `box-shadow: glow-rest` |
| Icon | 16x16px, inline-flex, gap 8px from label |
| Hover | `bg: #D8D5CF (active)`, `border-color: rgba(184, 181, 174, 0.20)`, `color: #2C2C2E (text-primary)`, `box-shadow: glow-hover` |
| Active press | `transform: scale(0.995)` |
| Transition | `all 300ms cubic-bezier(0.4, 0, 0.2, 1)` |

#### Toggle/Switch

| Property | Value |
|---|---|
| Track | `width: 40px`, `height: 22px`, `border-radius: 9999px` |
| Track off | `bg: #D8D5CF (active)` |
| Track on | `bg: #5B7FA5 (toggleActive / steel blue)` |
| Track ring rest | `0.5px` ring using `rgba(184, 181, 174, 0.28)` |
| Track ring hover | `1px` ring (thickens on hover) |
| Thumb | `width: 18px`, `height: 18px`, `bg: #F5F3F0 (surface)`, `border-radius: 9999px`, `box-shadow: 0 1px 2px rgba(44,44,46, 0.08)`, centered vertically, slides on toggle |
| Transition | `background-color, transform 300ms cubic-bezier(0.4, 0, 0.2, 1)` |
| Focus-visible | Same steel-blue focus ring as all interactive elements |

#### User Message Bubble

| Property | Value |
|---|---|
| bg | `#D8D5CF (active)` |
| border-radius | 14px |
| padding | `12px 18px` |
| max-width | `80%` (also capped at `70ch`) |
| color | `#2C2C2E (text-primary)` |
| font | Satoshi, 16px, weight 400 |
| alignment | Right-aligned |
| box-shadow | `inset 0 1px 2px rgba(184, 168, 138, 0.03)` (subtle subsurface glow even on bubbles) |

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard ease-in-out. Most UI transitions. |
| out-quart | `cubic-bezier(0.165, 0.85, 0.45, 1)` | Deceleration. Sidebar items, ghost buttons. |
| out-quint | `cubic-bezier(0.22, 1, 0.36, 1)` | Gentle arrival. Page entries, content reveals. |
| out-expo | `cubic-bezier(0.19, 1, 0.22, 1)` | Near-instant arrival, long settle. Panel open/close, modals. |
| gallery-ease | `cubic-bezier(0.25, 0.1, 0.25, 1.0)` | The signature easing. Slow, smooth, slightly weighted. Like watching a gallery door close on hydraulic hinges. Used for subsurface glow transitions. |
| majestic-spring | `stiffness: 80, damping: 18` | Low-stiffness spring for slow, weighted motion. Particles and physics elements. |

#### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 150ms | out-quart | Slower than Editorial Calm. Gallery pace. |
| Button hover (primary/outlined) | 200ms | default | Background, border-color, color. |
| Toggle track color | 300ms | default | Background-color and thumb transform. Luxuriously slow. |
| Chip hover | 300ms | default | All properties including subsurface glow escalation. |
| Card border/shadow/glow hover | 400ms | gallery-ease | Border-color, box-shadow (external + subsurface glow). The signature transition. |
| Input border/glow hover | 300ms | default | Border-color and shadow/glow escalation. |
| Chat input card shadow/glow | 400ms | gallery-ease | All properties including subsurface glow. |
| Ghost icon button | 400ms | out-quart | Slow, considered for icon-only actions. |
| Page/hero content entry | 600ms | out-quint | `opacity: 0, translateY(16px)` to `opacity: 1, translateY(0)`. Majestic. |
| Modal entry | 400ms | out-expo | `scale(0.96)` to `scale(1)` + fade. Slower than Editorial Calm. |
| Panel open/close | 800ms | out-expo | Sidebar collapse, settings panel expand. Very slow, weighted. |
| Gallery stagger delay | 120ms | -- | Delay between staggered children. Slower cascade for dramatic effect. |
| Menu item hover | 150ms | default | Popover item bg/color change. |
| Subsurface glow pulse | 3000ms | gallery-ease | Ambient glow oscillation on hero surfaces (see Signature Animations). |

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items (sidebar) | `scale(0.985)` | Barely perceptible. Gallery restraint. |
| Chips | `scale(0.995)` | Almost invisible press. |
| Buttons (primary, ghost, accent) | `scale(0.975)` | Slightly less than Editorial Calm. Less "clicky," more "pressing into porcelain." |
| Tabs (settings) | `scale(0.96)` | Pronounced for segmented controls. |

#### Reduced Motion (`prefers-reduced-motion: reduce`)

| Behavior | Change |
|---|---|
| Strategy | `fade-only` -- all spatial movement removed, opacity transitions remain. |
| All translateY entries | Replaced with opacity-only fade (no vertical movement). |
| Scale presses | Disabled. Instant visual state change. |
| Stagger delays | Reduced to 0ms. All children appear simultaneously with shared 200ms fade. |
| Ambient motion (glow pulse, drift) | Disabled entirely. Static glow at rest level. |
| Subsurface glow transitions | Remain but simplified to opacity change only, capped at 150ms. |
| All transitions (hover, focus) | Remain but capped at 150ms. |

---

### Overlays

#### Popover/Dropdown

| Property | Value |
|---|---|
| bg | `#F5F3F0 (surface)` |
| backdrop-filter | `blur(20px)` |
| border | `0.5px solid rgba(184, 181, 174, 0.28)` |
| border-radius | 12px |
| box-shadow | `shadow-popover` + `glow-popover` (combined external shadow and subsurface glow) |
| padding | 8px |
| min-width | 200px |
| max-width | 320px |
| z-index | 50 |
| overflow-y | auto (with `max-height: var(--available-height)`) |
| Menu item | `padding: 8px 12px`, `border-radius: 8px`, `height: 36px`, `font-size: 14px (body-small)`, `color: #6B6B70 (text-secondary)`, `cursor: pointer` |
| Menu item hover | `bg: #E0DDD8 (recessed)`, `color: #2C2C2E (text-primary)` |
| Menu item transition | `150ms cubic-bezier(0.4, 0, 0.2, 1)` |
| Separators | Spacing only (10px gap between groups). No visible lines. Gallery-clean. |

#### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(44, 44, 46, 0.35)` (cool-tinted, not pure black. Lighter than Editorial Calm -- gallery prefers transparency.) |
| Overlay backdrop-filter | `blur(10px)` |
| Content bg | `#F5F3F0 (surface)` |
| Content shadow | `shadow-popover` + `glow-popover` |
| Content border-radius | 14px |
| Content padding | 28px |
| Entry animation | `opacity: 0, scale(0.96)` to `opacity: 1, scale(1)`, 400ms out-expo |
| Exit animation | `opacity: 0`, 250ms default |
| z-index | 60 |

#### Tooltip

| Property | Value |
|---|---|
| bg | `#D8D5CF (active)` |
| color | `#2C2C2E (text-primary)` |
| font-size | 11px (label role) |
| font-weight | 500 |
| letter-spacing | 0.06em |
| text-transform | uppercase |
| border-radius | 4px |
| padding | `4px 10px` |
| shadow | `0 1px 3px rgba(44, 44, 46, 0.08)` (minimal) |
| Arrow | None. Position-only placement. |
| Delay | 400ms before showing. Slower -- gallery pace. |
| z-index | 55 |

Tooltips use the gallery-label style (uppercase, tracked) for consistency with the museum signage aesthetic.

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 800px | Main content column. Slightly wider than Editorial Calm for gallery breathing room. |
| Narrow max-width | 680px | Landing/focused content, settings pages. |
| Sidebar width | 280px | Fixed sidebar. Slightly narrower than Editorial Calm -- gallery minimalism. |
| Sidebar border | `0.5px solid rgba(184, 181, 174, 0.12)` | Right edge separation. Near-invisible hairline. |
| Header height | 52px | Top bar. Slightly taller for gallery-scale proportion. |
| Spacing unit | 4px | Base multiplier. |

#### Spacing Scale

`4, 8, 12, 16, 20, 24, 32, 40, 48, 64px`

Base unit is 4px. The scale skips 6px and 10px from Editorial Calm and extends further (to 48px and 64px). Gallery density means more generous spacing at the larger end.

Common applications:
- 4px: icon-text inline gap
- 8px: standard element gap, chip padding
- 12px: input padding, compact card inset
- 16px: section padding, sidebar item horizontal padding
- 24px: card padding, standard section gap
- 32px: modal padding, content-to-sidebar gap
- 40px: major section separation
- 48-64px: hero spacing, gallery-scale vertical rhythm

#### Density

**spacious** -- Generous whitespace throughout. Content-to-whitespace ratio approximately 40:60. The gallery wall should be visible. Elements never crowd. White space is not empty; it is the primary surface material.

#### Responsive Notes

| Breakpoint | Width | Behavior |
|---|---|---|
| lg | 1024px | Full sidebar + content. Default desktop layout. Gallery proportions. |
| md | 768px | Sidebar collapses to overlay. Content fills viewport with 24px horizontal padding. |
| sm | 640px | Single column. Cards stack vertically. Chips wrap. Input card full-width. |

On mobile (below md):
- Sidebar becomes an overlay panel with the same bg, activated by menu button
- Content max-width becomes 100% with 20px horizontal padding (more generous than Editorial Calm)
- Header remains 52px but actions collapse into a popover menu
- Cards stretch to full width, padding reduces from 24px to 16px
- Subsurface glow effect intensity halved on mobile (performance consideration)
- Gallery stagger delay reduces from 120ms to 80ms for mobile pace
- Display role reduces from 40px to `clamp(28px, 7vw, 40px)`

---

### Accessibility Tokens

| Token | Value | Notes |
|---|---|---|
| Focus ring color | `rgba(122, 139, 154, 0.50)` | Steel blue at 50% opacity. Harmonizes with cool palette. |
| Focus ring width | `2px solid` | Applied via `outline` |
| Focus ring offset | `2px` | Applied via `outline-offset` |
| Disabled opacity | `0.5` | Combined with `pointer-events: none` and `cursor: not-allowed` |
| Disabled shadow | `none` | Remove all shadows (including subsurface glow) on disabled elements |
| Selection bg | `rgba(184, 168, 138, 0.16)` | Accent gold at 16% -- `::selection` |
| Selection color | `#2C2C2E (text-primary)` | Maintains readability on selection |
| Scrollbar width | `thin` | `scrollbar-width: thin` |
| Scrollbar thumb | `rgba(184, 181, 174, 0.30)` | Border-base at 30% opacity. Cooler than Editorial Calm. |
| Scrollbar track | `transparent` | No visible track |
| Min touch target | 44px | All interactive elements on mobile |
| Contrast standard | WCAG AA | 4.5:1 for normal text, 3:1 for large text (18px+) |

**Contrast verification:**
- text-primary (`#2C2C2E`) on surface (`#F5F3F0`): ~12.5:1 (passes AAA)
- text-secondary (`#6B6B70`) on surface (`#F5F3F0`): ~4.6:1 (passes AA)
- text-muted (`#9A9A9E`) on surface (`#F5F3F0`): ~3.2:1 (passes AA for large text; used only for metadata/timestamps at label size or larger)
- accent-primary (`#B8A88A`) on surface (`#F5F3F0`): ~3.1:1 (passes AA for large text; gold accent is used at heading size or as background with `text-onAccent`)

**Scrollbar CSS:**

```css
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(184, 181, 174, 0.30) transparent;
}
```

---

### Visual Style

#### Material

| Property | Value |
|---|---|
| Grain | None. Porcelain is smooth. No paper fiber, no noise. Surfaces should feel polished and unbroken. |
| Grain technique | None. |
| Gloss | Soft-sheen. Not matte (that is Editorial Calm), not gloss (that is Liquid Glass). A porcelain-like soft sheen -- surfaces catch light but do not reflect it. Achieved via the subsurface glow, not CSS reflections. |
| Blend mode | `normal` everywhere. No multiply blending. Porcelain surfaces are opaque except for the subsurface illusion. |
| Shader bg | false. No WebGL backgrounds. The gallery wall is static. |

#### The Subsurface Scattering Technique (Full Reference)

Subsurface scattering (SSS) is the physical phenomenon where light enters a translucent material, bounces around inside, and exits at a different point. In real porcelain, this makes thin areas glow warm when backlit. This theme simulates SSS using CSS inset box-shadows and optional radial gradients.

**Core mechanism:**

```css
/* Level 1: Basic SSS on any elevated surface */
.sss-surface {
  background: var(--surface);  /* #F5F3F0 -- the porcelain */
  box-shadow:
    /* Top inner glow -- simulates light entering from above */
    inset 0 1px 4px rgba(var(--accent-rgb), 0.04),
    /* Bottom inner glow -- simulates light scattering downward */
    inset 0 -1px 4px rgba(var(--accent-rgb), 0.02),
    /* External shadow for depth */
    0 2px 12px rgba(44, 44, 46, 0.03),
    0 0 0 0.5px rgba(184, 181, 174, 0.20);
}
```

**Level 2: Enhanced SSS with radial gradient (for larger surfaces):**

```css
.sss-surface-enhanced {
  background:
    /* Radial glow centered in upper third -- simulates concentrated light entry */
    radial-gradient(
      ellipse 70% 50% at 50% 25%,
      rgba(184, 168, 138, 0.03),
      transparent 70%
    ),
    var(--surface);
  box-shadow:
    inset 0 1px 6px rgba(184, 168, 138, 0.05),
    inset 0 -1px 4px rgba(184, 168, 138, 0.02),
    0 2px 12px rgba(44, 44, 46, 0.03),
    0 0 0 0.5px rgba(184, 181, 174, 0.20);
}
```

**Level 3: Animated SSS (hover intensification):**

```css
.sss-surface {
  transition: box-shadow 400ms cubic-bezier(0.25, 0.1, 0.25, 1.0);
}

/* On hover: "more light passing through" */
.sss-surface:hover {
  box-shadow:
    inset 0 1px 8px rgba(184, 168, 138, 0.06),
    inset 0 -1px 6px rgba(184, 168, 138, 0.03),
    0 4px 16px rgba(44, 44, 46, 0.05),
    0 0 0 0.5px rgba(184, 181, 174, 0.28);
}

/* On focus/active: maximum translucency */
.sss-surface:focus-within {
  box-shadow:
    inset 0 1px 12px rgba(184, 168, 138, 0.08),
    inset 0 -1px 8px rgba(184, 168, 138, 0.04),
    0 4px 16px rgba(44, 44, 46, 0.07),
    0 0 0 0.5px rgba(184, 181, 174, 0.28);
}
```

**Why warm glow on cool surfaces:** The magic of SSS is that the scattered light picks up the material's inherent color. Porcelain has a warm undertone beneath its cool glaze. Using the warm accent (`rgba(184, 168, 138, ...)`) for the inner glow against the cool surface (`#F5F3F0`) creates this physically-inspired illusion. The warmth should be barely perceptible -- felt, not seen. If the glow is visible to a casual observer, the opacity is too high.

**Tuning guidance:**
- Card-sized elements: `0.04` / `0.02` rest, `0.06` / `0.03` hover
- Large panels (hero, modal): `0.05` / `0.03` rest, `0.07` / `0.04` hover
- Input fields: Same as cards but with radial gradient for caret-area warmth
- Popovers: `0.05` / `0.03` rest (no hover needed -- popovers are transient)
- Never exceed `0.10` on any inner glow. The effect is ruined by excess.

#### Rendering Guidelines

- **No particles.** This is not a particle theme. The gallery wall is clean.
- **Scientific visualization:** Fluid dynamics, fractals, and mathematical art should be rendered on the porcelain surface (surface token) with the cool palette. Data colors use accent-primary (gold) for primary series, accent-secondary (steel blue) for secondary, and semantic colors for status.
- **Photography portfolios:** Images should sit on the surface token with the subsurface glow. The image itself is the artwork; the frame (border + glow) is the gallery presentation.
- **Negative space is sacred.** The gallery wall (page/bg tokens) should be visible. Let the cool grey breathe. An overcrowded gallery is a failure.

---

### Signature Animations

#### 1. Porcelain Glow Pulse (Ambient)

Hero cards and feature panels exhibit a subtle, slow oscillation in their subsurface glow intensity, as if the light source behind them is gently breathing.

- **Technique:** CSS keyframe animation alternating the inset box-shadow opacity between the rest value and a slightly elevated value.

```css
@keyframes porcelain-pulse {
  0%, 100% {
    box-shadow:
      inset 0 1px 6px rgba(184, 168, 138, 0.04),
      inset 0 -1px 4px rgba(184, 168, 138, 0.02),
      0 2px 12px rgba(44, 44, 46, 0.03),
      0 0 0 0.5px rgba(184, 181, 174, 0.20);
  }
  50% {
    box-shadow:
      inset 0 1px 8px rgba(184, 168, 138, 0.06),
      inset 0 -1px 6px rgba(184, 168, 138, 0.03),
      0 2px 12px rgba(44, 44, 46, 0.03),
      0 0 0 0.5px rgba(184, 181, 174, 0.20);
  }
}

.hero-card {
  animation: porcelain-pulse 6s cubic-bezier(0.25, 0.1, 0.25, 1.0) infinite;
}
```

- **Duration:** 6 seconds per full cycle (3s brighten, 3s dim).
- **Easing:** gallery-ease for smooth sine-like oscillation.
- **Reduced motion:** Disabled entirely. Static glow at rest level.

#### 2. Gallery Reveal (Entry)

Content enters with a slow, majestic fade-and-rise, like a sculpture being unveiled. Elements move upward from a lower position with a longer travel distance than typical UI entry animations.

- **Technique:** `opacity: 0, translateY(24px)` to `opacity: 1, translateY(0)`.
- **Duration:** 600ms per element.
- **Easing:** out-quint (`cubic-bezier(0.22, 1, 0.36, 1)`).
- **Stagger:** 120ms between siblings (top-to-bottom cascade).
- **Total cascade example:** 8-item gallery grid completes at 600ms + (7 x 120ms) = 1440ms. This is intentionally slow. The gallery reveal is a moment.

```css
@keyframes gallery-reveal {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.gallery-item {
  animation: gallery-reveal 600ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.gallery-item:nth-child(1) { animation-delay: 0ms; }
.gallery-item:nth-child(2) { animation-delay: 120ms; }
.gallery-item:nth-child(3) { animation-delay: 240ms; }
/* ... */
```

- **Reduced motion:** All items appear simultaneously with 200ms opacity-only fade. No vertical movement.

#### 3. Kiln Glow (Interaction Feedback)

When a user clicks or taps a card, the subsurface glow briefly intensifies to its maximum and then settles back -- as if the porcelain was pressed against a heat source and slowly cools.

- **Technique:** On `mousedown` / `touchstart`, set glow to `glow-active` level. On release, transition back to `glow-rest` over 800ms.

```css
.card:active {
  box-shadow:
    inset 0 1px 16px rgba(184, 168, 138, 0.10),
    inset 0 -1px 10px rgba(184, 168, 138, 0.06),
    0 2px 12px rgba(44, 44, 46, 0.03),
    0 0 0 0.5px rgba(184, 181, 174, 0.20);
  transition: box-shadow 50ms ease;
}

.card {
  transition: box-shadow 800ms cubic-bezier(0.25, 0.1, 0.25, 1.0);
}
```

- **Duration:** 50ms to peak (instant response), 800ms to settle (slow cooling).
- **Easing:** gallery-ease for the settle.
- **Reduced motion:** Instant state change, no gradual settle. Jump to rest state on release.

#### 4. Light Shift (Scroll-Linked)

As the user scrolls, the radial gradient position in hero surfaces shifts subtly, as if the light source moves with the viewer's perspective. This creates a parallax-like effect on the subsurface glow without moving any elements.

- **Technique:** CSS custom property `--scroll-y` updated via `scroll` event listener, used in `radial-gradient` position.

```css
.hero-card {
  background:
    radial-gradient(
      ellipse 80% 60% at calc(50% + var(--scroll-offset, 0px)) 30%,
      rgba(184, 168, 138, 0.04),
      transparent 70%
    ),
    var(--surface);
}
```

```javascript
// Lightweight scroll listener
window.addEventListener('scroll', () => {
  const offset = Math.sin(window.scrollY * 0.002) * 20; // +/- 20px
  document.documentElement.style.setProperty('--scroll-offset', `${offset}px`);
}, { passive: true });
```

- **Range:** Radial gradient center shifts +/- 20px horizontally.
- **Update rate:** Every scroll event (passive listener, no layout thrash).
- **Reduced motion:** Disabled. Static gradient centered at 50%.

#### 5. Vessel Turn (Page Transition)

When navigating between major views, content fades while subtly rotating 1-2 degrees, as if the viewer is walking around a displayed vessel to see another face.

- **Technique:** Exiting content fades to 0 with `rotateY(2deg)`. Entering content fades in from `rotateY(-2deg)`.
- **Duration:** 400ms exit, 500ms enter (asymmetric -- entering takes longer for dramatic effect).
- **Easing:** out-expo for exit, out-quint for entry.
- **Perspective:** `perspective: 1200px` on the parent container.
- **Reduced motion:** Crossfade only, no rotation.

---

### Dark Mode Variant

This theme is natively light. A dark variant is suggested but not fully specified. The following provides directional guidance for implementation.

#### Dark Mode Palette Direction

| Token | Light Hex | Dark Hex (suggested) | Notes |
|---|---|---|---|
| page | `#E4E1DC` | `#18181A` | Cool near-black with faint blue undertone. |
| bg | `#ECEAE6` | `#1E1E22` | Primary dark surface. Cool charcoal. |
| surface | `#F5F3F0` | `#28282C` | Cards, inputs. Slightly lighter. |
| recessed | `#E0DDD8` | `#1A1A1E` | Code blocks. Slightly darker than bg. |
| active | `#D8D5CF` | `#121214` | Active items. Darkest interactive. |
| text-primary | `#2C2C2E` | `#F0EEEB` | Primary text. Warm cream on cool dark. |
| text-secondary | `#6B6B70` | `#A0A0A5` | Secondary text. |
| text-muted | `#9A9A9E` | `#6A6A70` | Muted text. |
| border-base | `#B8B5AE` | `#4A4A50` | Darker cool grey. Same opacity system. |
| accent-primary | `#B8A88A` | `#C4B498` | Slightly lifted gold for dark-bg contrast. |
| accent-secondary | `#7A8B9A` | `#8A9BAA` | Slightly lifted steel blue. |

#### Dark Mode Rules

- Subsurface scattering inverts: instead of warm glow on cool light porcelain, the glow becomes slightly brighter (lighter) on dark surfaces. The accent-rgb values remain warm, but opacity may need to increase by 1-2% to be perceptible against dark backgrounds.
- Surfaces lighten as they elevate: `page (#18181A)` < `bg (#1E1E22)` < `surface (#28282C)`.
- Shadow percentages increase: card shadows use 6% rest / 10% focus (vs 3%/7% in light mode). Popover shadow uses 20%.
- The cool-warm tension remains: dark surfaces are cool blue-grey, accent glow is still warm gold.
- The soft-sheen quality of porcelain can be suggested on dark surfaces with a very subtle top-edge highlight: `border-top: 0.5px solid rgba(255, 255, 255, 0.04)`.

---

### Data Visualization

| Property | Value |
|---|---|
| Categorical palette | Antique Gold `#B8A88A`, Steel Blue `#7A8B9A`, Celadon `#5A8A6A`, Muted Rose `#B85A5A`, Aged Amber `#A08040`. Max 5 hues. |
| Sequential ramp | Gold single-hue: `#E8DCC8` (lightest) -> `#D4C4A4` -> `#B8A88A` -> `#9C8C6C` -> `#7A6C4E` (darkest) |
| Diverging ramp | Steel Blue-to-Gold: `#5B7FA5` -> `#8AAABB` -> `#E4E1DC` (neutral center) -> `#D4C4A4` -> `#B8A88A` |
| Grid style | low-ink. Axes in text-muted, gridlines in border-base at 6% opacity. Gallery-minimal. |
| Max hues per chart | 3. Restraint. A gallery chart is not a carnival. |
| Philosophy | annotated. Labels on data points, not legends. Minimal axes. The data should speak with the quiet authority of a museum placard. |
| Number formatting | Fira Code with `font-variant-numeric: tabular-nums`. Right-aligned in columns. |

---

### Mobile Notes

#### Effects to Disable

- **Subsurface glow intensity:** Halve all glow opacity values (0.04 becomes 0.02, 0.06 becomes 0.03, etc.). Inset box-shadows with multiple layers can cause composite layer pressure on mobile GPUs.
- **Porcelain Glow Pulse animation:** Disable. Continuous box-shadow animation is expensive on mobile.
- **Light Shift (scroll-linked):** Disable. Gradient recalculation on scroll can cause jank on older mobile devices.
- **Vessel Turn rotation:** Disable. Replace with crossfade only. 3D transforms in transitions can cause flickering on mobile Safari.
- **Backdrop blur on popovers:** Reduce from `blur(20px)` to `blur(10px)`. Keep modal blur at `blur(6px)`.

#### Sizing Adjustments

- **Touch targets:** All interactive elements minimum 44px. Sidebar items (36px on desktop) expand to 44px on mobile.
- **Card padding:** Reduce from 24px to 16px on screens below 640px.
- **Content padding:** 20px horizontal on mobile (vs centered max-width on desktop).
- **Typography:** Display role reduces from 40px to `clamp(28px, 7vw, 40px)`. All other roles remain fixed.
- **Gallery stagger delay:** Reduce from 120ms to 80ms. Mobile users expect snappier pacing.
- **Spacing scale upper end:** 48px and 64px spacings reduce to 32px and 40px on mobile.

#### Performance Notes

- This theme is moderately performance-conscious. The subsurface glow (inset box-shadow) is more expensive than simple drop shadows but less expensive than backdrop-filter blur.
- The primary performance concern is composite box-shadows (inset + external) on many simultaneous elements. On mobile, limit the number of simultaneously visible cards with active glow to 6-8.
- The Porcelain Glow Pulse is the most expensive animation (continuous box-shadow keyframes). Desktop only.
- No WebGL, no particles, no Canvas -- this theme is CSS-only, which keeps the base performance budget low.

---

### Implementation Checklist

- [ ] **Fonts loaded:** DM Serif Display (regular 400), Satoshi (400, 500, 700 via Fontshare or self-hosted), Fira Code (400, 500 via Google Fonts) with `font-display: swap`
- [ ] **CSS custom properties defined:** All color tokens (including `--accent-rgb: 184, 168, 138`), shadow tokens, subsurface glow tokens, border tokens, radius tokens, spacing scale, motion easings, layout values as `:root` variables
- [ ] **Font smoothing applied:** `-webkit-font-smoothing: antialiased` on `<html>`
- [ ] **Typography matrix implemented:** All 10 roles with correct family, size, weight, line-height, letter-spacing, features
- [ ] **Family switch boundary respected:** DM Serif Display for Display/Heading only. Satoshi for all other roles.
- [ ] **Gallery-label style applied:** Label role uses `text-transform: uppercase`, `letter-spacing: 0.06em`, `font-weight: 500`
- [ ] **Border-radius applied correctly:** sm (4px), md (6px), lg (8px), xl (12px), 2xl (20px), input (8px), full (9999px)
- [ ] **Subsurface scattering implemented:** All cards, inputs, and elevated surfaces have composite box-shadow with inset glow (warm accent-rgb at 0.04/0.02)
- [ ] **Subsurface glow escalates on interaction:** Rest -> hover -> focus/active with progressive opacity increase
- [ ] **Shadow tokens applied per state:** rest/hover/focus on cards and inputs, popover on menus
- [ ] **Border opacity system implemented:** All borders use base color at correct opacity level (subtle 12%, card 20%, hover 28%, focus 38%)
- [ ] **Focus ring on all interactive elements:** `outline: 2px solid rgba(122, 139, 154, 0.50)`, `outline-offset: 2px` on `:focus-visible`
- [ ] **Disabled states complete:** opacity 0.5 + pointer-events none + cursor not-allowed + shadow/glow none
- [ ] **`prefers-reduced-motion` media query present:** All animations wrapped or checked. Glow pulse, light shift, vessel turn disabled.
- [ ] **Scrollbar styled:** `scrollbar-width: thin`, `scrollbar-color: rgba(184, 181, 174, 0.30) transparent`
- [ ] **`::selection` styled:** `background: rgba(184, 168, 138, 0.16)`, `color: #2C2C2E`
- [ ] **Touch targets >= 44px on mobile**
- [ ] **State transitions match motion map:** Each component uses its specified duration and easing. Gallery-ease (`cubic-bezier(0.25, 0.1, 0.25, 1.0)`) for subsurface glow transitions.
- [ ] **Caret color set:** `caret-color: #B8A88A` on all text inputs for warm-accent interaction point.
- [ ] **Dark mode variant tokens prepared:** Even if not fully implemented, the CSS custom properties should be structured for easy theme switching.
- [ ] **Cool-warm tension verified:** Visual audit confirming palette is 80% cool, 20% warm. Gold never dominates.
- [ ] **Data visualization tokens applied:** Categorical palette, sequential ramp, grid style at 6% opacity, number formatting with Fira Code tabular-nums.
- [ ] **Mobile adjustments applied:** Subsurface glow halved, pulse disabled, stagger reduced, touch targets expanded.
