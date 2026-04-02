# Future Medieval — Full Reference

## Table of Contents

- [Identity & Philosophy](#identity--philosophy) — Line 36
- [Color System](#color-system) — Line 68
  - [Palette](#palette) — Line 72
  - [Special Tokens](#special-tokens) — Line 93
  - [Opacity System](#opacity-system-border-on-var--border-base) — Line 102
  - [Color Rules](#color-rules) — Line 112
- [Typography Matrix](#typography-matrix) — Line 122
  - [Font Loading](#font-loading) — Line 152
- [Elevation System](#elevation-system) — Line 161
  - [Surface Hierarchy](#surface-hierarchy) — Line 170
  - [Shadow Tokens](#shadow-tokens) — Line 180
  - [Separation Recipe](#separation-recipe) — Line 193
- [Border System](#border-system) — Line 199
  - [Widths](#widths) — Line 203
  - [Opacity Scale](#opacity-scale-on-var--border-base) — Line 212
  - [Patterns](#patterns) — Line 222
  - [Focus Ring](#focus-ring) — Line 236
- [Component States](#component-states) — Line 260
  - [Buttons (Primary)](#buttons-primary) — Line 264
  - [Buttons (Ghost / Icon)](#buttons-ghost--icon) — Line 275
  - [Text Input](#text-input) — Line 286
  - [Chat Input Card](#chat-input-card) — Line 296
  - [Cards](#cards) — Line 306
  - [Sidebar Items](#sidebar-items) — Line 316
  - [Chips](#chips) — Line 328
  - [Toggle / Switch](#toggle--switch) — Line 338
  - [User Bubble](#user-bubble) — Line 355
- [Motion Map](#motion-map) — Line 370
  - [Easings](#easings) — Line 376
  - [Duration x Easing x Component](#duration-x-easing-x-component) — Line 387
  - [Active Press Scale](#active-press-scale) — Line 410
- [Layout Tokens](#layout-tokens) — Line 422
  - [Spacing Scale](#spacing-scale) — Line 433
  - [Density](#density) — Line 438
  - [Radius Scale](#radius-scale) — Line 451
  - [Responsive Notes](#responsive-notes) — Line 467
- [Accessibility Tokens](#accessibility-tokens) — Line 475
  - [Reduced Motion](#reduced-motion) — Line 503
- [Overlays](#overlays) — Line 541
  - [Popover / Dropdown](#popover--dropdown) — Line 545
  - [Modal](#modal) — Line 561
  - [Tooltip](#tooltip) — Line 571
- [Visual Style](#visual-style) — Line 585
  - [Vellum Grain](#vellum-grain) — Line 587
  - [Candlelight Ambient Wash](#candlelight-ambient-wash) — Line 617
  - [Material](#material) — Line 637
- [Signature Animations](#signature-animations) — Line 647
  - [1. Gold Border Draw (Gilded Edge Reveal)](#1-gold-border-draw-gilded-edge-reveal) — Line 649
  - [2. Ink Bleed Text Reveal](#2-ink-bleed-text-reveal) — Line 698
  - [3. Manuscript Page Turn (Panel Transition)](#3-manuscript-page-turn-panel-transition) — Line 737
  - [4. Illuminated Initial Drop Cap](#4-illuminated-initial-drop-cap) — Line 768
  - [5. Wax Seal Press (Confirmation Action)](#5-wax-seal-press-confirmation-action) — Line 815
- [Dark Mode Variant (Light Mode)](#dark-mode-variant-light-mode) — Line 860
  - [Light Mode: Open Scriptorium](#light-mode-open-scriptorium) — Line 863
- [Mobile Notes](#mobile-notes) — Line 893
  - [Effects to Disable on Mobile](#effects-to-disable-on-mobile) — Line 895
  - [Effects to Simplify on Mobile](#effects-to-simplify-on-mobile) — Line 903
  - [Sizing Adjustments](#sizing-adjustments) — Line 911
  - [Performance Budget](#performance-budget) — Line 921
- [Data Visualization](#data-visualization) — Line 933
- [Implementation Checklist](#implementation-checklist) — Line 947

---

## Identity & Philosophy

This theme lives inside the private library of a wizard who studied UX design. The room is tall, vaulted, and lit by enchanted candles that never gutter. Shelves of bound vellum codices line the walls. The reading desk holds an open manuscript -- its pages dark, its text bone-white, its borders traced in hammered gold leaf. The margins contain verdigris annotations in a steady hand. An oxblood wax seal marks the chapter heading. Everything in this room is old, purposeful, and exquisitely crafted. And somehow, it runs on a design system.

The core visual tension is between **medieval craft** and **modern usability**. This is not a novelty theme that sacrifices readability for atmosphere. It is a formal, warm-dark interface where every gold border, every decorative initial, and every ceremonial transition serves a functional purpose. The blackletter typeface (Cinzel Decorative) is the signature, but it appears only at the highest level of the typographic hierarchy -- major page titles, hero greetings. Everything below that level is set in Crimson Pro, a highly readable serif designed for extended screen reading. The restraint is the point: a wizard's library is organized, not chaotic.

The surfaces are layered vellum -- dark parchment pages stacked on a near-black desk. Depth is communicated through warm shadow between the layers and through gilded gold borders that catch imaginary candlelight. The gold is structural, not decorative: it marks card edges, input borders, active states, and focus rings. It is the thread that binds the manuscript pages together.

Motion in this theme is **ceremonial**. Elements are unveiled, not thrown. Gold borders draw themselves into existence via `stroke-dashoffset`. Text appears with a slow ink-bleed shadow. Panels slide open like heavy oak doors. Nothing is casual, nothing is instant. The minimum transition is 200ms. Reveals and page entries range 600-1200ms. This is the pace of ritual, not the pace of software.

**Decision principle:** "When in doubt, ask: would a master scribe approve? If it is hasty, garish, or careless, it does not belong in the codex."

**What this theme is NOT:**
- Not a novelty/costume theme -- this is a production interface, not a Renaissance fair booth. Every decorative element must serve a UX function.
- Not blackletter-heavy -- Cinzel Decorative appears ONLY on display-level headings. Using it for body text, buttons, labels, or any element smaller than 28px destroys readability and breaks the theme.
- Not gold-saturated -- gold is an accent, not a surface color. A gold background on a button or card is garish. Gold marks edges, borders, and small highlights.
- Not fantasy-cluttered -- no ornamental corner flourishes, no faux-aged paper textures, no scrollwork borders, no torches. The enchantment is in the restraint.
- Not low-contrast -- dark vellum backgrounds with bone-white text must maintain WCAG AA at every level. The darkness is warm, not muddy.

---

## Color System

Colors are drawn from the physical materials of an illuminated manuscript: the dark vellum of aged parchment, the bone-calcium white of dried ink, the hammered gold leaf of borders and initials, the oxblood of wax seals and rubrication, and the verdigris patina of copper-based annotations. Every color has a material origin.

### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Scriptorium Dark | `#12100B` | L=0.08 C=0.012 h=70 | Deepest background. The oak desk beneath everything. Near-black with a warm amber undertone -- the darkness of a candle-lit room, not a screen. |
| bg | Vellum Shadow | `#1A1510` | L=0.11 C=0.015 h=65 | Primary surface background. Sidebar, main content area. The dark side of a vellum page not yet touched by candlelight. |
| surface | Manuscript Page | `#242019` | L=0.15 C=0.018 h=60 | Elevated cards, inputs, popovers. The working surface of a manuscript page -- warm dark parchment with just enough lightness to distinguish from the desk beneath it. |
| recessed | Binding Gutter | `#0D0B08` | L=0.06 C=0.010 h=65 | Code blocks, inset areas. The deep shadow between bound pages. Darker and cooler than the page surface. |
| active | Candlelit Vellum | `#2E2820` | L=0.18 C=0.020 h=58 | Active/pressed items, selected states. The warmest dark surface -- vellum directly lit by a nearby candle, picking up golden warmth. |
| text-primary | Bone White | `#EAE2D0` | L=0.90 C=0.025 h=80 | Headings, body text. Not pure white -- the warm cream of aged bone or dried calligraphy ink on vellum. The brightest element in the room. |
| text-secondary | Faded Ink | `#A89888` | L=0.65 C=0.025 h=65 | Sidebar items, secondary labels. The color of old iron gall ink that has faded over centuries -- still readable, no longer dominant. |
| text-muted | Ghost Script | `#786858` | L=0.46 C=0.030 h=60 | Placeholders, timestamps, metadata. The faintest text in the manuscript -- marginal notes, pencil annotations, barely-there guides. |
| text-onAccent | Scriptorium Dark | `#12100B` | L=0.08 C=0.012 h=70 | Text on accent-colored backgrounds. Dark against gold or oxblood surfaces. |
| accent-primary | Gilded Gold | `#C9A84C` | L=0.73 C=0.12 h=85 | Primary accent, brand color, primary CTA. The color of hammered gold leaf applied by a master gilder. Used for borders, active indicators, links, and the primary action button. Not used as a surface fill -- gold is an edge material, not a page material. |
| accent-secondary | Verdigris | `#5A7A6C` | L=0.50 C=0.05 h=160 | Secondary accent, links, informational highlights. The green patina of aged copper clasps and hinges on the manuscript's binding. Cool counterpoint to the dominant warmth. Used for hyperlinks, secondary actions, and informational labels. |
| border-base | Tarnished Gold | `#A08A50` | L=0.60 C=0.08 h=82 | Base border color used at variable opacity. A desaturated gold -- borders in this theme are gilded edges seen in dim candlelight. At low opacity, they read as warm structure; at high opacity, they glow. |
| oxblood | Wax Seal | `#6B2D34` | L=0.30 C=0.10 h=18 | Highlight and emphasis color. The deep red-brown of sealing wax and rubricated chapter titles. Used for notification badges, important markers, destructive action accents, and editorial highlights. Not used broadly -- oxblood is a seal, not a wash. |
| success | Herbalist Green | `#4A7A52` | L=0.48 C=0.08 h=145 | Positive states. The deep green of pressed herbs in a botanical manuscript -- alive but subdued. |
| warning | Amber Resin | `#B89040` | L=0.63 C=0.10 h=80 | Caution states. The warm amber of tree resin used to seal manuscripts. Close to gold but distinguishable. |
| danger | Rubrication Red | `#8A3838` | L=0.35 C=0.12 h=22 | Error states, destructive actions. The red ink used by scribes for important passages and corrections. More saturated than oxblood, signaling urgency. |
| info | Verdigris | `#5A7A6C` | L=0.50 C=0.05 h=160 | Informational states. Same as accent-secondary. The annotator's color. |

### Special Tokens

| Token | Value | Role |
|---|---|---|
| inlineCode | `#C9A84C` at 80% opacity | Code text within prose. Gold-tinted, as if the code were a magical formula illuminated in the manuscript. |
| toggleActive | `#C9A84C` | Toggle/switch active track. Gilded -- the enchantment is activated. |
| selection | `rgba(201, 168, 76, 0.18)` | `::selection` background. A faint gold wash, as if the reader marked the passage with gold dust. |
| candlelight-ambient | `radial-gradient(ellipse at 70% 20%, rgba(201, 168, 76, 0.025), transparent 55%)` | Environmental candlelight wash. An extremely subtle golden tint from the upper-right, as if a candle sits on the desk. Applied to the page layer. |

### Opacity System (Border on `var(--border-base)`)

| Level | Opacity | Usage |
|---|---|---|
| subtle | 12% | Dormant edges, hairline separators. The faintest gold leaf, barely catching the light. |
| card | 22% | Card borders, panel edges. The gilded edge of a manuscript page. Present and warm. |
| hover | 32% | Hovered elements. The border catches candlelight -- gold brightens. |
| focus | 42% | Focused elements. Clear, luminous gold. The reader's eye is here. |
| glow | 55% | Special emphasis. Reserve for active tab indicators, primary action borders. The gold is radiant. |

### Color Rules

- **Gold is structural, not decorative.** It marks borders, edges, active states, focus rings, and small typographic highlights (initial letters). It is never used as a card background, button fill surface, or large area wash. Gold leaf in a manuscript outlines and separates -- it does not fill.
- **Oxblood is earned.** The wax seal red appears only for emphasis that demands attention: notification badges, chapter/section markers, destructive action indicators. Using it for general highlights or decoration dilutes its authority. A seal means something.
- **Verdigris is the scholar's color.** It marks annotations, links, informational asides -- the things a reader adds, not the things the scribe wrote. It is always secondary to gold and oxblood in visual weight.
- **No pure black, no pure white.** The darkest value is `#0D0B08` (recessed), the lightest is `#EAE2D0` (text-primary). Everything lives in the warm analog range of candlelight. Pure black is void; pure white is a lightbulb. Neither belongs in a library.
- **Warmth increases with elevation.** Deeper/lower surfaces are cooler and darker. Higher/closer surfaces pick up more candlelight warmth (higher chroma, warmer hue). This mimics real physics: objects closer to the candle on the desk are warmer.
- **Grain is present but restrained.** A faint vellum texture overlay gives surfaces their parchment character, but it is subtler than a darkroom grain -- parchment is smoother than film.

---

## Typography Matrix

Cinzel Decorative for display headings (the blackletter signature -- decorative capitals inspired by Roman inscriptions and medieval illumination), Crimson Pro for all body and UI text (a high-quality text serif with variable weight, excellent screen rendering, and the warmth of humanist calligraphy), Fira Code for code and data (clear, modern, with ligatures that evoke arcane notation).

**Critical blackletter rule:** Cinzel Decorative is used ONLY for the Display role (hero titles, page names) at 36px or above. It is never used for Heading, Body, Button, Label, or any other role. Its decorative nature makes it unreadable below ~28px and inappropriate for functional text. The restraint is the signature -- one line of blackletter at the top of a page, presiding over clean readable text below, like a decorated initial presiding over a manuscript column.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | decorative (Cinzel Decorative) | 36px | 400 | 1.15 | 0.04em | -- | Hero titles, page names, major greetings. The illuminated initial of the page. Cinzel Decorative at 400 weight (its default) with generous letter-spacing for legibility. Maximum one per viewport. |
| Heading | serif (Crimson Pro) | 24px | 600 | 1.3 | 0.005em | -- | Section titles, settings headers. Crimson Pro at semi-bold provides clean, authoritative headings without the decorative drama of Cinzel. |
| Subheading | serif (Crimson Pro) | 18px | 500 | 1.35 | normal | -- | Subsection titles, card headers. Crimson Pro at medium weight. |
| Body | serif (Crimson Pro) | 16px | 400 | 1.6 | normal | -- | Primary reading text, UI body. Crimson Pro at regular weight. The 1.6 line-height gives text room to breathe -- this is a library, not a terminal. Generous leading mirrors the spacious line-spacing of manuscript columns. |
| Body Small | serif (Crimson Pro) | 14px | 400 | 1.5 | normal | -- | Sidebar items, form labels, secondary text. |
| Button | serif (Crimson Pro) | 14px | 600 | 1.4 | 0.02em | -- | Button labels, emphasized small UI text. Crimson Pro at semi-bold with slight tracking for compact readability. The button text has the authority of a scribe's rubric. |
| Input | serif (Crimson Pro) | 14px | 400 | 1.4 | normal | -- | Form input text. Serif input text maintains the manuscript character. The pen writes on parchment, not a screen. |
| Code | mono (Fira Code) | 0.9em | 400 | 1.5 | normal | liga | Inline code, code blocks, data values. Fira Code's ligatures make code feel like arcane notation -- `!=` becomes a single glyph, `=>` becomes an arrow, `<=` becomes a sigil. |
| Label | serif (Crimson Pro) | 12px | 500 | 1.33 | 0.03em | -- | Section labels, metadata, timestamps. Tracked for legibility at small size. Uses Crimson Pro to maintain the all-serif identity. |
| Caption | serif (Crimson Pro) | 12px | 400 | 1.33 | 0.01em | -- | Disclaimers, footnotes, marginal references. The smallest text in the codex. |

**Typographic decisions:**

- **Cinzel Decorative is the ceremony.** Its presence at the top of a page declares: "This is the beginning of something." Its absence everywhere else declares: "The content is what matters." One display line of Cinzel Decorative per viewport. Never repeated, never stacked, never miniaturized.
- **Crimson Pro is the workhorse.** Designed by Jacques Le Bailly, it is a Garamond-inspired text face with a large x-height, open counters, and variable weight axis (200-900). It reads cleanly at 12-24px on screens while maintaining the calligraphic warmth of its historical models. It carries the manuscript identity without sacrificing usability.
- **Fira Code is the arcane notation.** Its programming ligatures (`=>`, `!=`, `<=`, `>=`, `===`) resemble alchemical or mathematical symbols when viewed through the manuscript lens. Code in this theme feels like a spell formula.
- **No sans-serif in the type system.** The entire typographic hierarchy is serif + mono. Sans-serif would break the manuscript character. If a sans-serif context is absolutely required (e.g., a dense data table), use the system sans-serif stack at 13px as a last resort.
- **Line-height 1.6 for body.** More generous than the standard 1.5. Manuscripts have generous interlinear spacing. The extra leading creates a meditative reading rhythm.
- `-webkit-font-smoothing: antialiased` is mandatory. Subpixel rendering causes color fringing on serif type over dark backgrounds.
- `text-wrap: pretty` for body text, `text-wrap: balance` for headings and display.

### Font Loading

```html
<link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Fira+Code:wght@400&display=swap" rel="stylesheet">
```

**Fallback chain:** `"Cinzel Decorative", "Georgia", serif` | `"Crimson Pro", "Georgia", serif` | `"Fira Code", "Courier New", ui-monospace, monospace`

---

## Elevation System

**Strategy:** `layered-shadows`

Depth is created through warm-toned composite shadows between layered vellum surfaces. Each surface is a "page" stacked on the desk, and the shadow between pages is warm and soft -- cast by candlelight, not by a fluorescent overhead. The gold borders on elevated elements create an additional depth signal through luminance contrast: a bright gold hairline against a dark surface reads as "this element is closer to the light."

There are no glows in this theme. Glows are digital. The enchantment here is analog -- hammered gold, cast shadows, layered pages. Light comes from above and slightly to the right (the candle on the desk), so shadows fall downward and to the left.

### Surface Hierarchy

| Surface | Background | Shadow | Border | Usage |
|---|---|---|---|---|
| page | `#12100B` (L=0.08) | none | none | The desk. The deepest surface. |
| bg | `#1A1510` (L=0.11) | none | none | Sidebar, main content well. First vellum layer. |
| surface | `#242019` (L=0.15) | shadow-sm | `var(--border-base)` at 22% | Cards, inputs, panels. The manuscript page laid on the desk. |
| recessed | `#0D0B08` (L=0.06) | none (inset) | `var(--border-base)` at 10% | Code blocks, inset fields. The gutter between pages. |
| active | `#2E2820` (L=0.18) | shadow-sm | `var(--border-base)` at 28% | Active/selected items. The page the reader's finger rests on. |
| overlay | `#242019` (L=0.15) | shadow-popover | `var(--border-base)` at 32% | Popovers, dropdowns. A loose page floating above the desk. |

### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-none | `none` | Flat elements at desk level. |
| shadow-sm | `0 1px 3px rgba(12, 10, 6, 0.30), 0 1px 2px rgba(12, 10, 6, 0.20)` | Cards at rest. Warm, close shadow -- a page resting on another page. |
| shadow-md | `0 3px 8px rgba(12, 10, 6, 0.35), 0 1px 3px rgba(12, 10, 6, 0.25)` | Cards on hover. The page lifts slightly from the desk. |
| shadow-input | `0 2px 6px rgba(12, 10, 6, 0.25), 0 0 0 0.5px rgba(160, 138, 80, 0.12)` | Input card at rest. Warm shadow plus faint gold ring. |
| shadow-input-hover | `0 3px 10px rgba(12, 10, 6, 0.30), 0 0 0 0.5px rgba(160, 138, 80, 0.22)` | Input card on hover. Shadow deepens, gold ring brightens. |
| shadow-input-focus | `0 4px 14px rgba(12, 10, 6, 0.35), 0 0 0 1px rgba(160, 138, 80, 0.32)` | Input card focused. Deepest input shadow, gold ring at full presence. |
| shadow-popover | `0 4px 16px rgba(12, 10, 6, 0.45), 0 2px 6px rgba(12, 10, 6, 0.30)` | Popovers, menus, dropdowns. A heavy warm shadow -- the loose page casts a distinct shadow on the desk below. |
| shadow-modal | `0 8px 32px rgba(12, 10, 6, 0.55), 0 4px 12px rgba(12, 10, 6, 0.35)` | Modal containers. The deepest shadow -- a heavy folio held above the desk. |

### Separation Recipe

Layered warm shadows + gilded gold border edges at low opacity. No visible dividers or rules. Each surface level is a separate vellum page, and the depth between them is communicated by: (1) the warm composite shadow between surfaces, (2) the slight warmth increase of higher surfaces, and (3) the gold border hairline that catches the candlelight. The gold border at 12-22% opacity is the primary structural separator -- it defines edges without demanding attention. Shadows provide the subconscious depth cue. Together they create layered vellum without any flat-on-flat stacking.

---

## Border System

Borders in this theme are gilded edges -- the thin gold leaf applied to the margins of a manuscript page. The border color is a desaturated gold that, at low opacity, reads as warm structural delineation and at higher opacity reads as decorative illumination. The opacity determines the border's role: functional structure at low opacity, decorative emphasis at high opacity.

### Widths

| Token | Value | Usage |
|---|---|---|
| hairline | 0.5px | Panel edges, sidebar separators. The thinnest gold leaf line. |
| default | 1px | Card borders, input borders. Standard manuscript ruling. |
| medium | 1.5px | Emphasized borders, active states, section dividers. |
| heavy | 2px | Focus-adjacent rings, toggle tracks, primary action borders. The bold ruling of a chapter heading. |

### Opacity Scale (on `var(--border-base)`)

| Level | Opacity | Usage |
|---|---|---|
| subtle | 12% | Dormant panel edges, rest-state separators. Nearly invisible -- gold that has worn away over centuries. |
| card | 22% | Card borders at rest. Present and warm, catching faint candlelight. |
| hover | 32% | Hovered elements. The gold brightens as the candle shifts closer. |
| focus | 42% | Focused element border. The reader's attention is here -- the gold responds. |
| glow | 55% | Active tab indicators, primary action borders. Full gilded emphasis. |

### Patterns

| Pattern | Width | Color / Opacity | Usage |
|---|---|---|---|
| panel-edge | 0.5px | `var(--border-base)` at 12% | Sidebar edges, quiet page margins |
| card | 1px | `var(--border-base)` at 22% | Card borders at rest -- the gilded edge of a page |
| card-hover | 1px | `var(--border-base)` at 32% | Card on hover -- candlelight catches the gold |
| card-active | 1.5px | `var(--border-base)` at 42% | Active/selected card -- emphasis through width and opacity |
| input | 1px | `var(--border-base)` at 22% | Input rest state |
| input-hover | 1px | `var(--border-base)` at 32% | Input hover |
| input-focus | 1px | `var(--accent-primary)` at 40% | Input focus -- gilded gold border |
| separator | 0.5px | `var(--border-base)` at 10% | Internal dividers within cards, between list items |
| chapter-rule | 1.5px | `var(--accent-primary)` at 25% | Section dividers between major content areas. A gold ruling across the page. |

### Focus Ring

The focus ring uses gilded gold -- consistent with the theme's primary accent -- with a scriptorium-dark gap ring to prevent bleed on warm surfaces:

- **Layer 1:** `0 0 0 2px var(--page)` -- gap ring in page color (dark)
- **Layer 2:** `0 0 0 4px rgba(201, 168, 76, 0.55)` -- gold ring at glow opacity
- **Offset:** 2px effective (via the gap ring)

**Full CSS:**

```css
:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--page),
    0 0 0 4px rgba(201, 168, 76, 0.55);
}
```

The gold focus ring is brighter than standard focus indicators because the dark background absorbs light. At 55% opacity, the gold ring is clearly visible without being harsh. It catches the eye the way a gold initial catches the eye in a manuscript column.

---

## Component States

All component states follow the ceremonial motion philosophy. Transitions are slower than standard UI conventions -- the fastest component transition is 150ms (sidebar hover), and most hover/focus transitions sit in the 200-400ms range. Gold border opacity shifts are the primary state change signal, reinforced by surface warmth changes and shadow escalation.

### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `var(--accent-primary)` (`#C9A84C`), border `1px solid rgba(201, 168, 76, 0.60)`, color `var(--text-onAccent)`, radius 6px, h 34px, padding `0 16px`, font button (Crimson Pro 14px/600), box-shadow `0 1px 3px rgba(12, 10, 6, 0.30)`, text-shadow `0 1px 0 rgba(201, 168, 76, 0.15)` |
| Hover | bg lightens to `#D4B45A`, box-shadow `0 2px 6px rgba(12, 10, 6, 0.35), 0 0 0 1px rgba(201, 168, 76, 0.20)` -- the gold surface catches more light |
| Active | transform `scale(0.97)`, bg darkens to `#B89840`, box-shadow `0 1px 2px rgba(12, 10, 6, 0.25)` -- pressed into the page |
| Focus | focus ring: `0 0 0 2px var(--page), 0 0 0 4px rgba(201, 168, 76, 0.55)` |
| Disabled | opacity 0.4, pointer-events none, box-shadow none, filter `grayscale(0.3)` -- the gold tarnishes and fades |
| Transition | background-color 250ms ease-out, transform 120ms ease-out, box-shadow 350ms ease-out |

### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border `1px solid var(--border-base)` at 22%, color `var(--text-secondary)`, radius 6px, size 34x34px, box-shadow none |
| Hover | bg `var(--active)`, border at 32%, color `var(--text-primary)` -- the vellum warms beneath the icon |
| Active | transform `scale(0.97)`, bg `var(--surface)` |
| Focus | focus ring (gold) |
| Disabled | opacity 0.4, pointer-events none |
| Transition | all 300ms ease-out |

### Text Input

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, border `1px solid var(--border-base)` at 22%, radius 8px, h 44px, padding `0 14px`, color `var(--text-primary)`, placeholder `var(--text-muted)`, caret-color `var(--accent-primary)`, box-shadow `var(--shadow-input)` |
| Hover | border at 32%, box-shadow `var(--shadow-input-hover)` -- gold ring brightens |
| Focus | border `1px solid var(--accent-primary)` at 40%, box-shadow `var(--shadow-input-focus)`, focus ring, outline none |
| Disabled | opacity 0.4, pointer-events none, bg `var(--bg)`, cursor not-allowed, box-shadow none |
| Transition | border-color 200ms ease-out, box-shadow 350ms ease-out |

### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, radius 20px, border `1px solid var(--border-base)` at 22%, box-shadow `var(--shadow-input)` |
| Hover | border at 32%, box-shadow `var(--shadow-input-hover)` |
| Focus-within | border `1px solid var(--accent-primary)` at 35%, box-shadow `var(--shadow-input-focus)` |
| Transition | all 350ms ease-out |

### Cards

| State | Properties |
|---|---|
| Rest | bg `var(--surface)`, border `1px solid var(--border-base)` at 22%, radius 8px, box-shadow `var(--shadow-sm)` |
| Hover | border at 32%, box-shadow `var(--shadow-md)` -- the page lifts from the desk, gold edge catches light |
| Active (clickable) | border at 42%, bg `var(--active)` |
| Transition | border-color 250ms ease-out, box-shadow 400ms ease-out, background-color 300ms ease-out |

Note: The card shadow transition (400ms) is intentionally slow -- the page lifts ceremonially from the desk, not snapping up. The border-color responds slightly faster (250ms) because gold catching candlelight is the first visual signal of interaction.

### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `var(--text-secondary)`, radius 6px, h 34px, padding `6px 14px`, font bodySmall (Crimson Pro 14px/400) |
| Hover | bg `var(--bg)`, color `var(--text-primary)` |
| Active (current) | bg `var(--active)`, color `var(--accent-primary)`, font-weight 600, border-left `2px solid var(--accent-primary)` at 50% |
| Active press | transform `scale(0.985)` |
| Transition | color 150ms ease-out, background 200ms ease-out |

The active sidebar item has a gold left border -- like a gilded margin rule marking the current chapter in the codex.

### Chips

| State | Properties |
|---|---|
| Rest | bg `var(--bg)`, border `1px solid var(--border-base)` at 15%, radius 16px, h 30px, padding `0 12px`, font bodySmall (Crimson Pro 14px/400), color `var(--text-secondary)` |
| Hover | border at 25%, color `var(--text-primary)`, bg `var(--surface)` |
| Active (selected) | bg `rgba(201, 168, 76, 0.10)`, border-color `var(--accent-primary)` at 30%, color `var(--accent-primary)` -- the chip is gilded |
| Active press | transform `scale(0.98)` |
| Transition | all 250ms ease-out |

### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 38px |
| Track height | 22px |
| Track radius | 9999px (full) |
| Track off bg | `var(--bg)` |
| Track off border | `1px solid var(--border-base)` at 22% |
| Track on bg | `var(--accent-primary)` -- gilded gold. The enchantment is active. |
| Track on border | `1px solid rgba(201, 168, 76, 0.60)` |
| Track on box-shadow | `inset 0 1px 2px rgba(12, 10, 6, 0.20)` -- subtle inset, the gold surface has dimension |
| Thumb | 18px circle, `var(--text-primary)` (bone white) |
| Thumb shadow | `0 1px 3px rgba(12, 10, 6, 0.30)` |
| Transition | 300ms ease-out -- slow, deliberate. Toggling an enchantment is a commitment. |
| Focus-visible | focus ring on track |

### User Bubble

| Property | Value |
|---|---|
| bg | `var(--active)` |
| radius | 16px |
| padding | 10px 16px |
| max-width | 75ch |
| color | `var(--text-primary)` |
| alignment | right |
| border | `1px solid var(--border-base)` at 15% |
| box-shadow | `var(--shadow-sm)` |

---

## Motion Map

The future medieval motion philosophy is **ceremonial unveiling**. Nothing snaps into place. Elements are revealed -- borders draw themselves, text emerges from ink-shadow, panels slide open like heavy doors. The fastest micro-interaction is 150ms. Most transitions sit in the 250-500ms range. Page-level reveals reach 800-1200ms. This is deliberate: the pace communicates gravitas, not sluggishness. A wizard does not rush.

Four custom easings define the motion vocabulary, each named for a bookbinding process:

### Easings

| Name | Value | Character |
|---|---|---|
| inscribe | `cubic-bezier(0.25, 0.1, 0.25, 1.0)` | Slow ramp, gentle arrival. The pace of a scribe dipping pen in ink and drawing a letter. Used for most state transitions. |
| unveil | `cubic-bezier(0.22, 1.0, 0.36, 1.0)` | Long deceleration tail. The heavy curtain drawn back from a window -- fast start, then a long, settling reveal. Used for page entries and panels. |
| press | `cubic-bezier(0.0, 0.0, 0.58, 1.0)` | Decisive start, gradual finish. A wax seal being pressed into place. Used for active/press states. |
| bind | `cubic-bezier(0.4, 0.0, 0.2, 1.0)` | Standard ease-in-out. The steady rhythm of thread passing through binding holes. Used for toggle/chip/general transitions. |
| illuminate | `cubic-bezier(0.0, 0.5, 0.5, 1.0)` | Front-loaded acceleration, then gradual halt. The moment gold leaf catches candlelight. Used for hover gold-brightening. |
| processional | `cubic-bezier(0.16, 1.0, 0.3, 1.0)` | Rapid onset, very long settle. A procession entering a hall -- the doors open quickly, the figures pass slowly. Used for staggered reveals. |

### Duration x Easing x Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 150ms / 200ms | inscribe | Color changes before background. Ink dries faster than the page turns. |
| Button hover warmth | 250ms | illuminate | Gold surface brightens gradually, catching the light. |
| Button press scale | 120ms | press | Decisive stamp. The wax seal. |
| Toggle slide | 300ms | bind | Steady, deliberate. An enchantment's state changes with gravitas. |
| Input focus border | 200ms | inscribe | Gold border inscribes itself around the field. |
| Input shadow deepen | 350ms | inscribe | Shadow deepens after border -- layered reveal. |
| Card hover shadow | 400ms | illuminate | The page lifts ceremonially from the desk. |
| Card border brighten | 250ms | inscribe | Gold edge responds before shadow deepens. |
| Chip select | 250ms | bind | Standard ceremonial pace. |
| Ghost icon hover | 300ms | inscribe | |
| Panel slide-in | 700ms | unveil | Heavy oak doors opening. Long deceleration. |
| Modal enter | 600ms | unveil | The portal opens -- slow, grand. |
| Modal exit | 400ms | inscribe | Closes faster than it opens. |
| Hero/page entry | 1000ms | unveil | The manuscript page turns. Full ceremonial reveal. |
| Popover appear | 350ms | unveil | A small scroll unfurls. |
| Tooltip show | 200ms | inscribe | |
| Gold border draw | 800ms | processional | Signature animation. Border traces itself into existence. |
| Ink bleed text | 600ms | unveil | Text shadow expands like ink on vellum. |
| Stagger interval | 80ms | -- | Delay between sequential element reveals. |

### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Barely perceptible. The library is quiet. |
| Chips | 0.98 | Subtle. |
| Buttons | 0.97 | Standard. The press of a seal. |
| Tabs | 0.96 | Pronounced. |
| Cards (clickable) | 0.995 | Nearly imperceptible -- cards are large vellum surfaces. |

---

## Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 740px | Main content column. Slightly narrower than standard -- the reading column of a manuscript page. |
| Narrow max-width | 640px | Focused content, landing views. The intimate reading width. |
| Sidebar width | 272px | Fixed sidebar. The marginalia column. |
| Header height | 48px | Top bar. |
| Spacing unit | 4px | Base multiplier. |

### Spacing Scale

4, 6, 8, 12, 16, 24, 32, 48, 64px

The scale extends to 64px for generous section spacing. Manuscripts have wide margins and generous interlinear spacing. The interface should feel spacious, not cramped -- a scholar's reading room, not a clerk's ledger.

### Density

**Comfortable.** This theme prioritizes reading comfort and ceremonial spacing over information density. Card padding is generous (16-20px). List gaps are 10-12px. The interface does not crowd. A codex is meant to be read slowly, one page at a time.

| Context | Padding | Gap |
|---|---|---|
| Card internal | 16-20px | -- |
| List items | -- | 10px |
| Section spacing | -- | 32-48px |
| Form field groups | -- | 16px |
| Sidebar item | 6px 14px | 2px |

### Radius Scale

| Token | Value | Usage |
|---|---|---|
| none | 0px | -- |
| sm | 4px | Small elements, badges, tooltips |
| md | 6px | Buttons, sidebar items, menu items |
| lg | 8px | Cards, inputs |
| xl | 12px | Popovers |
| 2xl | 16px | Modal containers, user bubbles |
| input | 8px | Form inputs, textareas |
| pill | 20px | Chat input card |
| full | 9999px | Avatars, toggles, chips |

Radii are conservative and consistent with the manuscript identity. Sharp corners would feel too brutalist; over-rounded would feel too modern and soft. The 6-8px range is the sweet spot -- the gentle, slightly uneven edge of hand-cut vellum.

### Responsive Notes

- **lg (1024px+):** Full sidebar (272px) + content column (740px max). All ambient effects active (vellum grain, candlelight wash). Gold border animations at full duration.
- **md (768px):** Sidebar collapses to overlay panel (slides in at 700ms unveil easing). Content fills width at 640px max. Candlelight wash shifts to center.
- **sm (640px):** Single column. Card radius reduces from 8px to 6px. Chat input radius reduces from 20px to 14px. Section spacing reduces from 48px to 32px. Gold border draw animation duration reduces from 800ms to 400ms.

---

## Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring | `0 0 0 2px var(--page), 0 0 0 4px rgba(201, 168, 76, 0.55)` -- gold ring with dark gap |
| Disabled opacity | 0.4 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Disabled filter | `grayscale(0.3)` -- the gold tarnishes on disabled elements |
| Selection bg | `rgba(201, 168, 76, 0.18)` |
| Selection color | `var(--text-primary)` (unchanged) |
| Scrollbar width | thin |
| Scrollbar thumb | `var(--border-base)` at 30% -- a warm gold scrollbar thumb |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

**Contrast verification:**
- `#EAE2D0` (text-primary) on `#12100B` (page): ~14.8:1 -- passes AAA
- `#EAE2D0` on `#242019` (surface): ~9.6:1 -- passes AAA
- `#A89888` (text-secondary) on `#12100B`: ~6.5:1 -- passes AA
- `#A89888` on `#242019` (surface): ~4.6:1 -- passes AA
- `#786858` (text-muted) on `#12100B`: ~3.6:1 -- passes AA for large text (14px+ bold or 18px+). Used only for labels/captions/placeholders at 12px+ weight 500, which qualify.
- `#C9A84C` (accent-primary) on `#12100B`: ~7.8:1 -- passes AA
- `#C9A84C` on `#242019` (surface): ~5.5:1 -- passes AA
- `#5A7A6C` (verdigris) on `#12100B`: ~4.0:1 -- passes AA for large text. For small text contexts, lighten to `#6A8A7C` (5.0:1).

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.15s !important;
  }

  /* Disable gold border draw animation */
  .border-draw {
    stroke-dashoffset: 0 !important;
    animation: none !important;
  }

  /* Disable ink bleed text shadow */
  .ink-bleed {
    text-shadow: none !important;
    animation: none !important;
  }

  /* Disable manuscript unfurl */
  .manuscript-unfurl {
    opacity: 1 !important;
    transform: none !important;
    animation: none !important;
  }

  /* Disable vellum grain breathing */
  .vellum-grain {
    animation: none !important;
  }

  /* Keep surface warmth and gold border opacity transitions (color changes, not motion) */
  /* background-color and border-color transitions retained at 150ms */
}
```

---

## Overlays

### Popover / Dropdown

- **bg:** `var(--surface)` (`#242019`)
- **border:** `1px solid var(--border-base)` at 28%
- **radius:** 12px
- **box-shadow:** `var(--shadow-popover)` -- warm, heavy shadow beneath the floating page
- **backdrop-filter:** `blur(16px)` -- the room behind softens when you focus on the floating scroll
- **padding:** 6px
- **z-index:** 50
- **min-width:** 192px, **max-width:** 320px
- **Menu item:** 6px 8px padding, radius 6px, h 34px, font bodySmall (Crimson Pro 14px), color text-secondary
- **Menu item hover:** bg `var(--active)`, color text-primary, border-left `2px solid var(--accent-primary)` at 20% (faint gold marker on hover)
- **Transition:** 150ms inscribe easing
- **Entry animation:** opacity 0 to 1, translateY(6px) to 0, 350ms unveil easing

### Modal

- **Overlay bg:** `rgba(12, 10, 6, 0.72)` -- warm, heavy darkness. The library's candles dim.
- **Overlay backdrop-filter:** `blur(8px)` -- the world beyond the modal becomes indistinct.
- **Content bg:** `var(--surface)`
- **Content border:** `1px solid var(--border-base)` at 28%
- **Content box-shadow:** `var(--shadow-modal)` -- deep warm shadow
- **Content radius:** 16px
- **Entry:** opacity 0 to 1 + scale 0.95 to 1.0, 600ms unveil easing. The modal unfurls like a scroll.
- **Exit:** opacity 1 to 0 + scale 1.0 to 0.97, 400ms inscribe easing.

### Tooltip

- **bg:** `var(--active)` (`#2E2820`)
- **color:** `var(--text-primary)`
- **font:** label size (Crimson Pro 12px), weight 500
- **radius:** 6px
- **padding:** 4px 10px
- **border:** `1px solid var(--border-base)` at 18%
- **box-shadow:** `0 2px 8px rgba(12, 10, 6, 0.35)` -- warm, small shadow
- **No arrow.** Positioned via offset. The tooltip is a marginal note, not a callout.

---

## Visual Style

### Vellum Grain

Vellum grain is the material signature -- a faint, fibrous texture overlay that gives every surface the tactile quality of animal-skin parchment. It is subtler than film grain (parchment is smoother than film) but present enough to prevent surfaces from feeling digitally flat.

**Technique:** SVG feTurbulence filter applied as a `::after` pseudo-element on the page container, composited with `mix-blend-mode: multiply` at very low opacity. The `multiply` blend mode is important -- it darkens slightly, reinforcing the material warmth. `soft-light` would be appropriate for film; `multiply` is appropriate for hide/parchment.

```css
.page::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 2;
  opacity: 0.025;
  mix-blend-mode: multiply;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='vellum'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23vellum)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  animation: grain-shift 12s ease-in-out infinite;
}

@keyframes grain-shift {
  0%, 100% { opacity: 0.025; transform: translate(0, 0); }
  33% { opacity: 0.028; transform: translate(0.5px, -0.5px); }
  66% { opacity: 0.022; transform: translate(-0.5px, 0.5px); }
}
```

The grain shift is barely perceptible: opacity oscillates between 2.2% and 2.8%, position shifts by 0.5px. Over a 12s cycle it creates a living, breathing surface without drawing conscious attention.

Key differences from film grain: lower `baseFrequency` (0.65 vs 0.85) produces a coarser, fiber-like pattern. Fewer octaves (3 vs 4) makes it smoother. `multiply` blend mode deepens into the warm background rather than adding luminance.

### Candlelight Ambient Wash

An extremely subtle golden radial gradient simulates candlelight from the upper-right corner of the desk:

```css
.page::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background: radial-gradient(
    ellipse at 70% 15%,
    rgba(201, 168, 76, 0.02),
    transparent 50%
  );
}
```

At 2% opacity, the candlelight wash is nearly invisible but gives the upper-right quadrant a faint golden warmth that distinguishes it from the cooler lower-left. This asymmetric lighting is key to the theme's dimensional quality -- a symmetrically lit room feels digital; an asymmetrically lit room feels real.

### Material

- **Grain:** Subtle (2-3%). `feTurbulence` fractalNoise, stitchTiles, 3 octaves.
- **Grain technique:** SVG feTurbulence inlined as data URI. `multiply` blend mode.
- **Gloss:** Matte. Vellum has tooth and texture. No reflections, no sheen, no glass effects.
- **Blend mode:** `multiply` for grain overlay. `normal` for all surface backgrounds.
- **Shader bg:** No. The enchantment is in the materials, not in digital effects.

---

## Signature Animations

### 1. Gold Border Draw (Gilded Edge Reveal)

The defining animation of the theme. When a card, panel, or container enters the viewport, its gold border is not instantly present -- it draws itself, tracing the perimeter of the element like a scribe applying gold leaf to a manuscript margin. The border traces clockwise from the top-left corner.

**Technique:** SVG `rect` overlaid on the element with `stroke-dasharray` equal to the perimeter and `stroke-dashoffset` animating from full perimeter to 0.

```css
.border-draw-container {
  position: relative;
}

.border-draw-container .gilded-border {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.border-draw-container .gilded-border rect {
  fill: none;
  stroke: rgba(201, 168, 76, 0.35);
  stroke-width: 1;
  rx: 8;
  ry: 8;
  stroke-dasharray: var(--perimeter);
  stroke-dashoffset: var(--perimeter);
  animation: draw-border 800ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes draw-border {
  0% {
    stroke-dashoffset: var(--perimeter);
    stroke: rgba(201, 168, 76, 0.10);
  }
  60% {
    stroke: rgba(201, 168, 76, 0.35);
  }
  100% {
    stroke-dashoffset: 0;
    stroke: rgba(201, 168, 76, 0.22);
  }
}
```

The border starts faint (10% opacity) and brightens to 35% during the draw, then settles to 22% (the card rest-state opacity). This mimics the process of gold leaf application: the leaf is brightest when first applied and tarnishes slightly as it sets.

**Duration:** 800ms, `processional` easing. Stagger at 120ms per card in a grid.
**Reduced motion:** Border appears instantly at rest-state opacity. No animation.

### 2. Ink Bleed Text Reveal

When major headings enter the viewport, their text shadow expands outward like ink bleeding into parchment fibers. The text itself appears crisp, but a warm dark shadow blooms slowly behind it, grounding the letters into the page surface.

```css
@keyframes ink-bleed {
  0% {
    opacity: 0;
    text-shadow: 0 0 0 rgba(18, 16, 11, 0);
    transform: translateY(4px);
  }
  30% {
    opacity: 0.6;
    text-shadow: 0 0 2px rgba(18, 16, 11, 0.15);
    transform: translateY(2px);
  }
  60% {
    opacity: 0.9;
    text-shadow: 0 1px 4px rgba(18, 16, 11, 0.25);
    transform: translateY(0.5px);
  }
  100% {
    opacity: 1;
    text-shadow: 0 1px 6px rgba(18, 16, 11, 0.20);
    transform: translateY(0);
  }
}

.ink-bleed {
  animation: ink-bleed 600ms cubic-bezier(0.22, 1, 0.36, 1) both;
}
```

The text shadow expands from 0 to 6px blur radius, peaking at 25% opacity before settling to 20%. The blur simulates ink spreading through parchment fibers. The opacity peaks at 60% of the animation duration -- the ink is darkest when wet and lightens as it dries.

**Duration:** 600ms, `unveil` easing.
**Reduced motion:** Text appears instantly with static text-shadow at final values.

### 3. Manuscript Page Turn (Panel Transition)

When a major content panel or modal opens, it enters with a slight 3D perspective rotation, as if a heavy manuscript page is being turned from the right side. The panel rotates from `rotateY(-3deg)` to `rotateY(0)` while sliding in, creating the impression of a page settling flat.

```css
@keyframes page-turn {
  0% {
    opacity: 0;
    transform: perspective(800px) rotateY(-3deg) translateX(30px);
  }
  40% {
    opacity: 0.7;
    transform: perspective(800px) rotateY(-1deg) translateX(10px);
  }
  100% {
    opacity: 1;
    transform: perspective(800px) rotateY(0deg) translateX(0);
  }
}

.manuscript-page-turn {
  animation: page-turn 700ms cubic-bezier(0.22, 1, 0.36, 1) both;
  transform-origin: left center;
}
```

The rotation is extremely subtle (3 degrees maximum) -- enough to create the physical impression of a turning page without disorienting the reader. The `transform-origin: left center` places the "binding" on the left edge.

**Duration:** 700ms, `unveil` easing.
**Reduced motion:** Disabled. Panel appears with simple opacity fade (300ms).

### 4. Illuminated Initial Drop Cap

When a major section loads, the first letter of the primary heading can be styled as a drop cap that fades in with a gold glow, referencing the illuminated initials of medieval manuscripts. The letter scales from 0.8 to 1.0 while its color transitions from muted to gold.

```css
@keyframes illuminated-initial {
  0% {
    opacity: 0;
    color: var(--text-muted);
    transform: scale(0.85);
    text-shadow: 0 0 0 rgba(201, 168, 76, 0);
  }
  50% {
    opacity: 0.8;
    color: var(--accent-primary);
    transform: scale(0.95);
    text-shadow: 0 0 8px rgba(201, 168, 76, 0.15);
  }
  80% {
    text-shadow: 0 0 12px rgba(201, 168, 76, 0.10);
  }
  100% {
    opacity: 1;
    color: var(--accent-primary);
    transform: scale(1);
    text-shadow: 0 0 6px rgba(201, 168, 76, 0.06);
  }
}

.illuminated-initial::first-letter {
  font-family: 'Cinzel Decorative', serif;
  font-size: 2.4em;
  float: left;
  line-height: 0.85;
  margin-right: 8px;
  margin-top: 4px;
  color: var(--accent-primary);
  animation: illuminated-initial 1000ms cubic-bezier(0.22, 1, 0.36, 1) both;
}
```

The gold glow peaks at 50% of the animation (15% opacity, 8px radius) then settles to a barely-perceptible 6% at 6px -- the gold leaf catches the candlelight for a moment, then rests. The initial uses Cinzel Decorative at 2.4x the parent font size, creating a proper drop cap.

**Duration:** 1000ms, `unveil` easing.
**Reduced motion:** Initial appears immediately in gold. No scale, no glow animation.

### 5. Wax Seal Press (Confirmation Action)

For confirmation actions (submit, save, approve), a brief animation mimics a wax seal being pressed: the button compresses, pauses, then releases with a subtle oxblood flash on the border, signaling the action is sealed.

```css
@keyframes seal-press {
  0% {
    transform: scale(1);
    box-shadow: 0 1px 3px rgba(12, 10, 6, 0.30);
    border-color: rgba(201, 168, 76, 0.60);
  }
  25% {
    transform: scale(0.95);
    box-shadow: 0 0 1px rgba(12, 10, 6, 0.20);
    border-color: rgba(201, 168, 76, 0.40);
  }
  50% {
    transform: scale(0.95);
    box-shadow: 0 0 1px rgba(12, 10, 6, 0.20);
    border-color: rgba(107, 45, 52, 0.50);
  }
  75% {
    transform: scale(0.98);
    box-shadow: 0 1px 2px rgba(12, 10, 6, 0.25);
    border-color: rgba(107, 45, 52, 0.35);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 1px 3px rgba(12, 10, 6, 0.30);
    border-color: rgba(201, 168, 76, 0.60);
  }
}

.seal-press {
  animation: seal-press 500ms cubic-bezier(0.0, 0.0, 0.58, 1) forwards;
}
```

The key moment is at 50%: the button is held compressed (scale 0.95) while the border color transitions from gold to oxblood -- the wax seal is being stamped. The oxblood then fades back to gold as the seal is complete. The pause at scale 0.95 between 25-50% creates the physical sensation of pressing down and holding.

**Duration:** 500ms, `press` easing.
**Reduced motion:** Button flashes oxblood border briefly (150ms) without scale animation.

---

## Dark Mode Variant (Light Mode)

This is a **dark-native** theme. The enchanted library IS dark -- lit by candles, not by fluorescents. A light mode would be like opening the curtains on a scriptorium window. The manuscripts are still there, but the atmosphere changes.

### Light Mode: Open Scriptorium

| Token | Dark (Native) | Light (Open Scriptorium) | Notes |
|---|---|---|---|
| page | `#12100B` | `#F5F1E8` | Warm cream, like unwritten vellum in daylight |
| bg | `#1A1510` | `#EDE8DE` | Warm off-white, the working desk |
| surface | `#242019` | `#FFFFFF` | Pure white -- a fresh page |
| recessed | `#0D0B08` | `#E5E0D6` | Warm grey, like a stack of pages in shadow |
| active | `#2E2820` | `#DDD6CA` | Slightly darker warm cream |
| text-primary | `#EAE2D0` | `#1A1612` | Near-black, warm brown ink |
| text-secondary | `#A89888` | `#6A5E4E` | Muted warm brown |
| text-muted | `#786858` | `#9A8E7E` | Light warm grey |
| accent-primary | `#C9A84C` | `#9A7A28` | Darker gold for contrast on light surfaces |
| accent-secondary | `#5A7A6C` | `#3A5A4C` | Darker verdigris |
| border-base | `#A08A50` | `#C8B890` | Warm sand-gold |
| oxblood | `#6B2D34` | `#8A3A42` | Slightly brighter for light contrast |

**Light mode rules:**
- Vellum grain overlay: Reduced to 1.5% opacity. Light mode surfaces are smooth fresh parchment, not aged vellum.
- Candlelight ambient wash: Disabled. Natural daylight is even, not directional.
- Gold border draw animation: Retained but with darker gold stroke color (`rgba(154, 122, 40, 0.30)`).
- Ink bleed text shadow: Retained with adjusted shadow color (`rgba(26, 22, 18, 0.12)`).
- Shadows activate: Since surface-shifts are harder to perceive on light backgrounds, light mode uses warm shadows: `0 1px 3px rgba(26, 22, 18, 0.06)` on cards, `0 2px 10px rgba(26, 22, 18, 0.10)` on popovers.
- Border opacity increases: subtle goes from 12% to 15%, card from 22% to 28%, hover from 32% to 38%, focus from 42% to 48%. Borders need more presence on light surfaces.
- Typography remains unchanged. The serif stack (Cinzel Decorative + Crimson Pro) works equally well on light paper -- this is their natural habitat.
- Illuminated initial glow: Disabled in light mode. Gold initials are simply gold-colored, without the glow effect (glow is invisible on light backgrounds).
- Decision principle shifts: "When in doubt, ask: would this look right in a well-lit scriptorium?" The intimacy of candlelight gives way to the clarity of day.

---

## Mobile Notes

### Effects to Disable on Mobile

- **Vellum grain overlay** -- Remove entirely. SVG feTurbulence with `mix-blend-mode: multiply` is expensive on mobile GPUs.
- **Candlelight ambient wash** -- Remove. Saves a compositing layer.
- **Gold border draw animation** -- Replace with instant gold borders. `stroke-dashoffset` animation is GPU-intensive on many elements.
- **Manuscript page turn** -- Disable 3D perspective rotation. Use simple opacity fade (300ms).
- **Illuminated initial glow** -- Disable animated glow. Display static gold initial.

### Effects to Simplify on Mobile

- **Ink bleed text reveal** -- Reduce duration from 600ms to 300ms. Remove blur. Keep opacity-only.
- **Wax seal press** -- Reduce from 500ms to 250ms.
- **Card hover transitions** -- Reduce from 400ms to 200ms (no hover on touch, but focus transitions benefit).
- **Vellum grain (if retained on high-end)** -- Freeze at 2.5% opacity. No animation.

### Sizing Adjustments

- All interactive elements maintain 44px minimum touch target.
- Body text stays 16px (Crimson Pro renders well at this size on mobile).
- Display text (Cinzel Decorative): 28px minimum on mobile (reduced from 36px).
- Card radius: 8px reduces to 6px.
- Chat input radius: 20px reduces to 14px.
- Card padding: 16-20px reduces to 12-16px.
- Section spacing: 48px reduces to 32px.
- Sidebar: Hidden behind a scroll-icon toggle, slides in as overlay panel (400ms fade, no page-turn).

### Performance Budget

- Maximum box-shadow blur radius across visible elements: 32px.
- No `backdrop-filter` on elements below the overlay z-index (only modals and popovers get blur).
- `will-change` applied during animations only, removed after completion.
- `@supports not (mix-blend-mode: multiply)` fallback: disable grain entirely.
- `@supports not (backdrop-filter: blur(1px))` fallback: increased overlay bg opacity to 0.85.
- Gold border draw (SVG stroke-dashoffset): disabled entirely on mobile. Static borders only.

---

## Data Visualization

| Property | Value |
|---|---|
| Categorical | Gilded Gold `#C9A84C`, Verdigris `#5A7A6C`, Oxblood `#6B2D34`, Amber Resin `#B89040`, Herbalist Green `#4A7A52` -- 5 colors at balanced perceptual weight on dark vellum |
| Sequential | Single-hue ramp from `#2E2820` (warmest dark) through `#C9A84C` (gold) to `#EAE2D0` (bone white) |
| Diverging | Gold `#C9A84C` (warm end) to `#5A7A6C` Verdigris (cool end) through `#12100B` neutral dark center |
| Grid | Low-ink: `var(--border-base)` at 8% opacity. Grid lines are nearly invisible manuscript rulings. |
| Max hues per chart | 2 (gold + verdigris). Additional dimensions use opacity or size, not new hues. |
| Philosophy | Smooth. Data should be inscribed, not plotted. Prefer area charts (illuminated regions) over bar charts. Prefer continuous fills over discrete steps. |
| Label font | Fira Code at 11px, `var(--text-muted)` color. Data labels are marginal annotations. |
| Axis | `var(--border-base)` at 12%. Faint manuscript rulings. Let the data lead. |

---

## Implementation Checklist

- [ ] Google Fonts loaded: Cinzel Decorative (400), Crimson Pro (400, 500, 600, 700, italic 400), Fira Code (400)
- [ ] CSS custom properties defined for all palette tokens (page, bg, surface, recessed, active, text-primary/secondary/muted, accent-primary/secondary, border-base, oxblood, semantic colors)
- [ ] Surface warmth gradient verified: page (coolest) < bg < surface < active (warmest)
- [ ] Shadow tokens defined: shadow-sm, shadow-md, shadow-input (rest/hover/focus), shadow-popover, shadow-modal
- [ ] Vellum grain SVG feTurbulence applied as `::after` pseudo on page container, `mix-blend-mode: multiply`, 2.5% opacity
- [ ] Grain shift animation running at 12s cycle
- [ ] Candlelight ambient wash applied as radial-gradient in `::before` pseudo, upper-right origin, 2% gold opacity
- [ ] Border opacity system implemented (12%, 22%, 32%, 42%, 55% on `var(--border-base)`)
- [ ] Gold border patterns verified: card at 22%, hover at 32%, focus at 42%
- [ ] Focus ring on all interactive elements: `0 0 0 2px var(--page), 0 0 0 4px rgba(201, 168, 76, 0.55)`
- [ ] Cinzel Decorative used ONLY for display role (36px+). Not on headings, buttons, labels, or body.
- [ ] All non-display typography uses Crimson Pro serif stack
- [ ] Gold border draw animation implemented with SVG stroke-dashoffset (800ms processional easing)
- [ ] Ink bleed text shadow animation implemented on headings (600ms unveil easing)
- [ ] Manuscript page turn animation for panels (700ms unveil easing, 3deg rotateY)
- [ ] Illuminated initial drop cap with gold color transition (1000ms unveil easing)
- [ ] Wax seal press animation for confirmation buttons (500ms press easing)
- [ ] Component hover transitions using `illuminate` easing (front-loaded)
- [ ] Card hover shadow transition at 400ms (ceremonially slow)
- [ ] `-webkit-font-smoothing: antialiased` on root
- [ ] `text-wrap: pretty` on body text, `text-wrap: balance` on headings/display
- [ ] All typography uses serif stack only (no sans-serif in the system except system fallback)
- [ ] Scrollbar styled: thin, `var(--border-base)` at 30% thumb, transparent track
- [ ] Touch targets >= 44px on all interactive elements
- [ ] Motion map durations verified: slowest at 1000ms (hero/page entry), fastest at 120ms (button press scale)
- [ ] `::selection` styled with gold accent at 18%
- [ ] `::placeholder` color matches `var(--text-muted)` token
- [ ] `prefers-reduced-motion` media query: disables gold border draw, ink bleed, page turn, initial glow, grain animation; retains color transitions at 150ms
- [ ] Light mode variant tokens defined and switchable via class or `data-theme` attribute
- [ ] Light mode: grain reduced, candlelight disabled, shadows activated, gold darkened, border opacity increased
- [ ] Text contrast verified: text-primary 14.8:1 (AAA), text-secondary 6.5:1 (AA), text-muted 3.6:1 (AA large text)
- [ ] Mobile: grain overlay removed, candlelight removed, gold border draw disabled, page turn disabled
- [ ] Mobile: animation durations reduced (ink bleed 300ms, seal press 250ms)
- [ ] Mobile: Cinzel Decorative display size reduced to 28px minimum
- [ ] `@supports not (mix-blend-mode: multiply)` fallback: grain disabled
- [ ] `@supports not (backdrop-filter: blur(1px))` fallback: increased overlay bg opacity to 0.85
- [ ] State transitions tested with correct theme-specific easings (inscribe, unveil, press, bind, illuminate, processional)
- [ ] Active sidebar item has gold left-border marker (2px, 50% opacity)
- [ ] Oxblood color used only for emphasis (notifications, destructive hints, chapter markers) -- never as general accent
