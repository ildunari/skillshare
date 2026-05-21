# Kintsugi — Full Theme Specification

**Table of Contents**

1. [Identity & Philosophy](#identity--philosophy) — Line 77
2. [Color System](#color-system) — Line 99
   - [Palette](#palette) — Line 101
   - [Special Tokens](#special-tokens) — Line 122
   - [Gold Repair System](#gold-repair-system) — Line 134
   - [Opacity System](#opacity-system) — Line 156
   - [Color Rules](#color-rules) — Line 168
3. [Typography Matrix](#typography-matrix) — Line 179
   - [Font Stack](#font-stack) — Line 181
   - [CJK Typography Rules](#cjk-typography-rules) — Line 199
   - [Typographic Decisions](#typographic-decisions) — Line 213
   - [Font Loading](#font-loading) — Line 224
4. [Elevation System](#elevation-system) — Line 245
   - [Surface Hierarchy](#surface-hierarchy) — Line 253
   - [Shadow Tokens](#shadow-tokens) — Line 263
   - [Separation Recipe](#separation-recipe) — Line 275
5. [Border System](#border-system) — Line 281
   - [Widths](#widths) — Line 283
   - [Opacity Scale](#opacity-scale) — Line 291
   - [Border Patterns](#border-patterns) — Line 302
   - [Focus Ring](#focus-ring) — Line 316
6. [Component States](#component-states) — Line 328
   - [Buttons (Primary)](#buttons-primary) — Line 330
   - [Buttons (Ghost / Icon)](#buttons-ghost--icon) — Line 342
   - [Text Input](#text-input) — Line 356
   - [Chat Input Card](#chat-input-card) — Line 368
   - [Cards](#cards) — Line 378
   - [Sidebar Items](#sidebar-items) — Line 389
   - [Chips](#chips) — Line 401
   - [Toggle / Switch](#toggle--switch) — Line 411
   - [Slider](#slider) — Line 428
   - [Divider / Horizontal Rule](#divider--horizontal-rule) — Line 442
7. [Motion Map](#motion-map) — Line 453
   - [Easings](#easings) — Line 455
   - [Duration × Easing × Component](#duration--easing--component) — Line 466
   - [Active Press Scale](#active-press-scale) — Line 489
8. [Overlays](#overlays) — Line 503
   - [Popover / Dropdown](#popover--dropdown) — Line 505
   - [Modal](#modal) — Line 525
   - [Tooltip](#tooltip) — Line 541
9. [Layout Tokens](#layout-tokens) — Line 555
   - [Spacing Scale](#spacing-scale) — Line 567
   - [Radius Scale](#radius-scale) — Line 585
   - [Density](#density) — Line 599
   - [Responsive Notes](#responsive-notes) — Line 603
10. [Accessibility Tokens](#accessibility-tokens) — Line 608
11. [Visual Style](#visual-style) — Line 647
12. [Signature Animations](#signature-animations) — Line 712
    - [1. Ink Wicking Reveal](#1-ink-wicking-reveal) — Line 714
    - [2. Gold Thread Fill](#2-gold-thread-fill) — Line 736
    - [3. Paper Settle](#3-paper-settle) — Line 760
    - [4. Contemplative Fade](#4-contemplative-fade) — Line 782
    - [5. Gold Repair Draw](#5-gold-repair-draw) — Line 801
13. [Dark Mode Direction](#dark-mode-direction) — Line 825
14. [Mobile Notes](#mobile-notes) — Line 845
    - [Effects to Disable](#effects-to-disable) — Line 847
    - [Adjustments](#adjustments) — Line 853
    - [Performance Notes](#performance-notes) — Line 865
15. [Data Visualization](#data-visualization) — Line 875
16. [Theme-Specific CSS Custom Properties](#theme-specific-css-custom-properties) — Line 890
17. [Implementation Checklist](#implementation-checklist) — Line 965

---

## 4. Kintsugi

> Broken vessels mended with gold -- extreme negative space, washi paper warmth, and the quiet beauty of imperfection.

**Best for:** Journaling, meditation apps, mindfulness tools, CJK content platforms, reflective personal applications, haiku editors, contemplative dashboards, digital tea ceremony spaces.

---

### Identity & Philosophy

This theme lives in the world of Japanese wabi-sabi -- the beauty of imperfection, impermanence, and incompleteness. The design metaphor is kintsugi: broken pottery repaired with lacquered gold, where the cracks become the most beautiful part. Every surface is handmade washi paper. Every divider is a gold repair line. Every interaction moves at the pace of incense smoke.

The space between things is the design. This is the most spacious theme in the roster -- content occupies less than 40% of the viewport. The negative space (ma, the Japanese concept of interval) is not emptiness; it is charged, intentional, and structural. Removing the space would break the theme more fundamentally than removing a color.

Gold is the singular accent. It does not fill areas. It does not create backgrounds. Gold is linear -- it appears as 1px lines, focus rings, border accents, and decorative crack patterns. Gold is the scar that makes something more beautiful than before it was broken. This restraint is absolute: if gold appears as a background fill, the implementation has failed.

Typography must honor CJK text. Japanese, Chinese, and Korean characters require wider line-height, larger base sizes, and fonts designed for vertical and horizontal reading. Shippori Mincho provides the Mincho (serif) elegance for display text. Body text uses Noto Serif JP for CJK and Noto Serif for Latin, ensuring seamless mixed-script rendering.

**Decision principle:** "When in doubt, ask: would this feel right in a 400-year-old tea house? If it feels hurried, slow it down. If it feels crowded, add space. If it feels decorative, remove it. If it feels perfect, break it slightly."

**What this theme is NOT:**
- Not decorative -- gold is structural repair, not ornamentation. No gold gradients, no gold fills, no gold icons.
- Not symmetrical -- Japanese aesthetic (fukinsei) favors asymmetric balance. Centered layouts feel wrong here.
- Not fast -- every transition is 300ms minimum. If something feels snappy, it is too fast.
- Not dark -- this is a warm light theme rooted in handmade paper. Darkness contradicts the washi material.
- Not dense -- if content feels packed, you have violated the core identity. Remove elements before reducing spacing.
- Not Western serif -- this is not Manuscript. The typography is CJK-first, the warmth is paper-fiber not parchment, the philosophy is Buddhist not Gutenbergian.

---

### Color System

#### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | Tatami | `#EDE8DC` | L=0.93 C=0.02 h=85 | Deepest background. Warm straw-mat tone beneath all content. |
| bg | Washi | `#F5F0E6` | L=0.95 C=0.02 h=82 | Primary surface. Handmade mulberry paper, warm and fibrous. |
| surface | Kozo White | `#FBF8F1` | L=0.97 C=0.01 h=80 | Elevated cards, inputs, popovers. Brightest kozo fiber paper. |
| recessed | Torinoko | `#E5DFCF` | L=0.90 C=0.03 h=84 | Code blocks, inset areas. Eggshell-toned traditional paper. |
| active | Kinari | `#DDD6C4` | L=0.87 C=0.03 h=82 | Active/pressed items, user bubbles. Natural undyed silk tone. |
| text-primary | Sumi | `#1C1B18` | L=0.20 C=0.01 h=90 | Headings, body text. Carbon black sumi ink. |
| text-secondary | Nezumi | `#6B665C` | L=0.48 C=0.02 h=80 | Sidebar items, secondary labels. Mouse-grey ink wash. |
| text-muted | Usuzumi | `#8E8880` | L=0.60 C=0.01 h=65 | Placeholders, timestamps, metadata. Diluted ink. WCAG AA on surface. |
| text-onAccent | Kozo White | `#FBF8F1` | L=0.97 C=0.01 h=80 | Text on accent-colored backgrounds. |
| border-base | Hai | `#B5ADA0` | L=0.73 C=0.02 h=75 | Base border color used at variable opacity. Ash grey. |
| accent-primary | Kintsugi Gold | `#C8A951` | L=0.74 C=0.12 h=85 | Gold repair lines, focus rings, active borders. The scar. |
| accent-secondary | Ai Indigo | `#3D5A80` | L=0.43 C=0.08 h=250 | Links, interactive elements. Traditional indigo dye. |
| success | Matcha | `#6B8F5E` | L=0.58 C=0.08 h=135 | Positive states. Whisked green tea. |
| warning | Kuchiba | `#C4923A` | L=0.68 C=0.12 h=75 | Caution states. Fallen-leaf amber. |
| danger | Beni | `#9B4A3A` | L=0.45 C=0.10 h=25 | Error states. Safflower red pigment. |
| info | Hanada | `#4A6E8A` | L=0.50 C=0.07 h=240 | Informational states. Flower-field blue. |

#### Special Tokens

| Token | Hex | Role |
|---|---|---|
| inlineCode | `#7A6B3A` | Code text within prose. Darkened gold, legible on paper surfaces. |
| toggleActive | `#6B8F5E` | Toggle/switch active track. Matcha green. |
| selection | `rgba(200, 169, 81, 0.18)` | `::selection` background. Gold at low opacity. |
| kintsugi-gold | `#C8A951` | CSS custom property `--kintsugi-gold`. The primary gold value. |
| kintsugi-gold-muted | `rgba(200, 169, 81, 0.30)` | Gold at 30% opacity for divider lines. |
| kintsugi-gold-subtle | `rgba(200, 169, 81, 0.15)` | Gold at 15% opacity for hover tints. |

#### Gold Repair System

Gold is the soul of this theme. Its usage is strictly controlled:

| Usage | Form | Opacity | Notes |
|---|---|---|---|
| Section dividers | 1px horizontal line | 30% | `border-bottom: 1px solid var(--kintsugi-gold-muted)` |
| Focus rings | 2px solid ring | 50% | Replaces blue focus rings entirely |
| Active borders | 1px bottom or left border | 40% | Indicates current/selected state |
| Progress bars | 2px line filling horizontally | 100% | Thin gold thread, not a thick bar |
| Card crack lines | Decorative SVG paths | 20-30% | Optional: thin gold lines suggesting repair across card surfaces |
| Hover gold tint | Background tint | 8-12% | Barely visible gold warmth on hover |
| Scrollbar thumb | Solid color | 35% | Gold-tinted scroll indicator |
| Horizontal rules | `<hr>` replacement | 25% | Gold line with generous vertical margin (48px+) |

**Gold anti-patterns (never do these):**
- Gold as button background fill
- Gold as card background
- Gold gradient of any kind
- Gold text (except as code highlight token at darkened value)
- Gold icon fills
- Multiple gold elements competing for attention in the same viewport

#### Opacity System

Border opacity (on `border-base` Hai grey):

| Level | Opacity | Usage |
|---|---|---|
| whisper | 8% | Ghost borders, barely-there edges |
| subtle | 15% | Panel edges, card outlines at rest |
| card | 20% | Default card and content borders |
| hover | 30% | Hovered elements, interactive state |
| focus | 40% | Focused inputs, active delineation |

#### Color Rules

- No pure greys. Every neutral carries a warm yellow-brown undertone from washi paper pigments.
- Gold is earned. It appears only where the kintsugi metaphor applies: boundaries, repairs, connections, focus.
- Semantic colors are muted earth tones. No saturated primary colors. Everything looks like it was made from natural pigments.
- The page-to-surface gradient moves from warm-dark (tatami) to warm-light (kozo white). Elevation = brightness.
- Maximum two colors visible at any moment besides neutrals: gold + one semantic or accent color.
- No gradients anywhere. Flat, matte surfaces only. Paper does not gradient.

---

### Typography Matrix

#### Font Stack

Shippori Mincho is the display typeface -- an elegant Mincho-style serif designed for Japanese and Latin text, with beautiful stroke terminals and excellent CJK coverage. Noto Serif / Noto Serif JP handles body text with optimized screen reading for both Latin and CJK scripts. IBM Plex Mono provides clean, functional code display.

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | serif (Shippori Mincho) | 36px | 500 | 1.25 | 0.02em | `font-feature-settings: "liga" 1, "kern" 1` | Hero titles, page names. CJK titles at 32px. |
| Heading | serif (Shippori Mincho) | 24px | 500 | 1.4 | 0.01em | `font-feature-settings: "liga" 1` | Section titles, settings headers |
| Subheading | serif (Shippori Mincho) | 19px | 400 | 1.5 | 0.02em | -- | Subsection labels |
| Body | serif (Noto Serif / Noto Serif JP) | 17px | 400 | 1.75 | normal | `font-feature-settings: "liga" 1, "kern" 1` | Primary reading text. CJK body at 17px minimum. |
| Body CJK | serif (Noto Serif JP) | 17px | 400 | 1.8 | 0.05em | `font-feature-settings: "kern" 1` | Japanese/Chinese/Korean body text. Extra line-height and tracking. |
| Body Small | serif (Noto Serif) | 15px | 400 | 1.6 | normal | -- | Sidebar items, secondary UI text |
| Button | serif (Shippori Mincho) | 14px | 500 | 1.4 | 0.04em | -- | Button labels. Restrained, not small-caps. |
| Input | serif (Noto Serif) | 16px | 400 | 1.5 | normal | -- | Form input text |
| Label | serif (Noto Serif) | 12px | 400 | 1.4 | 0.06em | `text-transform: none` | Metadata, timestamps. Never uppercase -- Japanese has no case. |
| Code | mono (IBM Plex Mono) | 0.88em | 400 | 1.6 | normal | `font-feature-settings: "liga" 0` | Inline code, code blocks |
| Caption | serif (Noto Serif) | 12px | 400 | 1.5 | 0.02em | -- | Disclaimers, footnotes |

#### CJK Typography Rules

CJK text requires specific handling that differs from Latin typography:

| Property | Latin Value | CJK Value | Reason |
|---|---|---|---|
| Body line-height | 1.75 | 1.8 | CJK characters are full-width squares that need extra vertical room |
| Body letter-spacing | normal | 0.05em | CJK glyphs benefit from slight breathing room between characters |
| Minimum body size | 16px | 17px | CJK stroke complexity requires larger rendering size |
| Word-break | normal | `word-break: break-all` | CJK has no word spaces; any character can break |
| Text-wrap | `pretty` | `auto` | `text-wrap: pretty` optimizes for Latin line-break aesthetics |
| Hanging punctuation | off | `hanging-punctuation: first last` | CJK punctuation should hang outside the text block |
| Paragraph spacing | 1em | 1.5em | CJK paragraphs without indentation need more vertical separation |

#### Typographic Decisions

- 17px body is the minimum for CJK readability on screen. Serif strokes at smaller sizes become illegible for complex characters.
- 1.75-1.8 line-height is generous even by CJK standards, but this theme demands extreme breathing room. Text floats in space.
- `-webkit-font-smoothing: antialiased` always. Critical for Mincho-style serif rendering.
- `text-wrap: pretty` for Latin body text. Use `auto` when CJK content is detected.
- Labels and metadata are NEVER uppercase. Japanese and Chinese have no uppercase/lowercase distinction; `text-transform: uppercase` produces broken rendering for CJK characters.
- Shippori Mincho is used for display/headings only. It is a Mincho (serif) face optimized for larger sizes. Body text uses Noto Serif JP for screen-optimized reading.
- When mixing Latin and CJK in the same line, the browser will select from the font stack. Noto Serif JP includes Latin glyphs that harmonize with its CJK designs.

#### Font Loading

```html
<!-- Kintsugi Theme -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;600&family=Noto+Serif:ital,wght@0,400;0,500;1,400&family=Noto+Serif+JP:wght@400;500&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
```

**Fallback chains:**
- Display: `"Shippori Mincho", "Hiragino Mincho ProN", "Yu Mincho", "MS PMincho", Georgia, serif`
- Body Latin: `"Noto Serif", Georgia, "Times New Roman", serif`
- Body CJK: `"Noto Serif JP", "Hiragino Mincho ProN", "Yu Mincho", "MS PMincho", serif`
- Mono: `"IBM Plex Mono", "SFMono-Regular", Consolas, monospace`

**CJK font loading notes:**
- Noto Serif JP is a large font file (~4MB for full CJK coverage). Use `font-display: swap` to prevent FOIT.
- Consider subsetting for applications that only need Japanese: `&subset=japanese,latin` reduces payload significantly.
- For Chinese support, add `Noto Serif SC` (Simplified) or `Noto Serif TC` (Traditional) to the font stack.
- For Korean support, add `Noto Serif KR`.
- Preload the Latin subset of Shippori Mincho for above-the-fold display text.

---

### Elevation System

**Strategy:** `surface-shifts` with minimal borders

Paper does not cast shadows. Paper layers. Elevation in this theme is expressed through brightness stepping between washi paper tones and ultra-subtle border definitions. The philosophy is surface-shift: higher elevation means brighter, warmer paper. Shadows are nearly absent -- when used at all, they are barely perceptible warm tints beneath surfaces.

#### Surface Hierarchy

| Surface | Background | Border | Shadow | Usage |
|---|---|---|---|---|
| page | `#EDE8DC` Tatami | none | none | Deepest background. Straw-mat ground. |
| washi | `#F5F0E6` Washi | `0.5px solid border-base/15%` | none | Primary content surface |
| shikishi | `#FBF8F1` Kozo White | `0.5px solid border-base/20%` | `0 2px 8px rgba(28,27,24,0.03)` | Elevated cards, inputs. Named for the poetry card. |
| torinoko | `#E5DFCF` Torinoko | `0.5px solid border-base/12%` | `inset 0 1px 3px rgba(28,27,24,0.03)` | Recessed areas, code blocks |
| overlay | `#FBF8F1` Kozo White | `0.5px solid var(--kintsugi-gold-muted)` | `0 4px 16px rgba(28,27,24,0.06)` | Popovers, dropdowns. Gold border accent. |

#### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-none | `none` | Page background, flat surfaces |
| shadow-breath | `0 2px 8px rgba(28,27,24,0.03)` | Cards at rest. Barely visible warm undertone. |
| shadow-breath-hover | `0 3px 12px rgba(28,27,24,0.05)` | Card hover. Slightly deeper breathing. |
| shadow-breath-focus | `0 3px 12px rgba(28,27,24,0.05), 0 0 0 2px rgba(200,169,81,0.5)` | Input focus. Breath shadow + gold ring. |
| shadow-overlay | `0 4px 16px rgba(28,27,24,0.06)` | Popovers, modals. Widest but still subtle. |
| shadow-inset | `inset 0 1px 3px rgba(28,27,24,0.03)` | Recessed surfaces, code blocks |

#### Separation Recipe

Surface-brightness stepping is the primary separation mechanism. Each elevation level is a different shade of washi paper, from the warm tatami ground through progressively lighter sheets. Borders are whisper-thin (0.5px) at very low opacity. Shadows are barely perceptible -- more of a warm color shift beneath surfaces than a traditional drop shadow. Gold repair lines (`--kintsugi-gold-muted` at 30%) serve as the most visible separators between major sections. Visual hierarchy = paper brightness + gold line placement.

---

### Border System

#### Widths

| Name | Width | Usage |
|---|---|---|
| hairline | 0.5px | Standard border width. This theme uses thin lines exclusively. |
| default | 1px | Gold repair lines, focus indicators, input borders |
| medium | 1.5px | Strong emphasis, section dividers (rare) |
| heavy | 2px | Focus ring width. Maximum border weight in this theme. |

#### Opacity Scale (on `border-base` Hai grey)

| Level | Opacity | Usage |
|---|---|---|
| whisper | 8% | Ghost borders on surfaces that barely need delineation |
| subtle | 15% | Hairline edges, default card borders |
| card | 20% | Standard card and panel borders |
| hover | 30% | Hovered elements |
| focus | 40% | Focused inputs, active delineation |

#### Border Patterns

| Pattern | Width | Color/Opacity | Usage |
|---|---|---|---|
| whisper | 0.5px | border-base at 8% | Near-invisible edges |
| subtle | 0.5px | border-base at 15% | Standard card outline |
| card | 0.5px | border-base at 20% | Content area boundaries |
| hover | 0.5px | border-base at 30% | Hovered cards |
| input | 1px | border-base at 15% | Form input borders |
| input-hover | 1px | border-base at 25% | Input hover state |
| gold-repair | 1px | kintsugi-gold at 30% | Section dividers, decorative repair lines |
| gold-active | 1px | kintsugi-gold at 50% | Active/selected element accent border |

#### Focus Ring

| Property | Value |
|---|---|
| Color | `rgba(200, 169, 81, 0.50)` -- kintsugi gold |
| Width | 2px solid |
| Offset | 3px (extra offset for breathing room) |
| Implementation | `box-shadow: 0 0 0 3px #F5F0E6, 0 0 0 5px rgba(200,169,81,0.50)` |

The focus ring is gold, not blue. This is a core identity decision. The inner ring uses the `bg` washi color to separate the gold indicator from the element surface. The 3px offset (rather than the typical 2px) reflects this theme's preference for extra spacing in every dimension.

---

### Component States

#### Buttons (Primary)

| State | Properties |
|---|---|
| Rest | bg `#3D5A80` (Ai Indigo), border none, color `#FBF8F1`, radius 6px, h 40px, padding `0 28px`, font button (Shippori Mincho, 14px, 500), shadow none |
| Hover | bg `#34506F` (darker indigo), shadow shadow-breath |
| Active | bg `#2C4560`, transform `scale(0.98)` |
| Focus | gold focus ring appended |
| Disabled | opacity 0.4, pointer-events none, cursor not-allowed |
| Transition | background 300ms contemplative, transform 200ms contemplative |

Note: Buttons use indigo, not gold. Gold is reserved for structural/repair elements. The button is a functional element that should not compete with gold's symbolic role.

#### Buttons (Ghost / Icon)

| State | Properties |
|---|---|
| Rest | bg transparent, border none, color `#6B665C` (Nezumi), radius 6px, size 40x40px |
| Hover | bg `rgba(200,169,81,0.08)` (gold whisper tint), color `#1C1B18` |
| Active | bg `rgba(200,169,81,0.15)`, transform `scale(0.98)` |
| Focus | gold focus ring |
| Disabled | opacity 0.4, pointer-events none |
| Transition | background 400ms contemplative, color 300ms contemplative |

Ghost buttons get the faintest gold warmth on hover -- the only place gold appears as a background, and only at 8% opacity.

#### Text Input

| State | Properties |
|---|---|
| Rest | bg `#FBF8F1` (Kozo White), border `1px solid rgba(181,173,160,0.15)`, radius 6px, h 48px, padding `0 16px`, shadow none, color `#1C1B18`, placeholder `#8E8880`, caret-color `#C8A951` (gold caret) |
| Hover | border at 25% opacity |
| Focus | border `1px solid rgba(200,169,81,0.4)` (gold border), shadow shadow-breath-focus, outline none |
| Disabled | opacity 0.4, bg `#E5DFCF`, pointer-events none |
| Transition | border-color 400ms contemplative, box-shadow 500ms contemplative |

The text cursor (caret) is gold. This is a subtle but distinctive detail -- as the user types, they write with gold.

#### Chat Input Card

| State | Properties |
|---|---|
| Rest | bg `#FBF8F1`, radius 16px, border `0.5px solid rgba(181,173,160,0.15)`, shadow shadow-breath, padding 20px |
| Hover | border at 20%, shadow shadow-breath-hover |
| Focus-within | border `0.5px solid rgba(200,169,81,0.3)`, shadow shadow-breath-focus |
| Transition | all 500ms contemplative |

#### Cards

| State | Properties |
|---|---|
| Rest | bg `#FBF8F1`, border `0.5px solid rgba(181,173,160,0.15)`, radius 8px, shadow shadow-breath, padding 24px |
| Hover | border at 20%, shadow shadow-breath-hover |
| Selected | border-bottom `1px solid rgba(200,169,81,0.4)` (gold repair line at base) |
| Transition | border-color 400ms contemplative, box-shadow 500ms contemplative |

Selected cards receive a gold bottom-border -- a repair line that marks them as "chosen." This is the kintsugi metaphor applied to interaction: selection is a kind of breaking and repairing.

#### Sidebar Items

| State | Properties |
|---|---|
| Rest | bg transparent, color `#6B665C` (Nezumi), radius 6px, h 40px, padding `8px 20px`, font bodySmall |
| Hover | bg `rgba(200,169,81,0.06)`, color `#1C1B18` |
| Active (current) | bg `rgba(200,169,81,0.10)`, color `#1C1B18`, border-left `2px solid rgba(200,169,81,0.5)` |
| Active press | transform `scale(0.99)` |
| Transition | color 300ms contemplative, background 400ms contemplative |

Active sidebar items get a gold left border -- a vertical repair line indicating "you are here."

#### Chips

| State | Properties |
|---|---|
| Rest | bg `#F5F0E6` (Washi), border `0.5px solid rgba(181,173,160,0.15)`, radius 6px, h 34px, padding `0 14px`, font bodySmall, color `#6B665C` |
| Hover | bg `#EDE8DC`, border at 25%, color `#1C1B18` |
| Selected | bg `rgba(200,169,81,0.10)`, border `0.5px solid rgba(200,169,81,0.25)`, color `#1C1B18` |
| Active press | transform `scale(0.99)` |
| Transition | all 300ms contemplative |

#### Toggle / Switch

| Property | Value |
|---|---|
| Track width | 44px |
| Track height | 24px |
| Track radius | 9999px |
| Track off bg | `rgba(181,173,160,0.2)` |
| Track off ring | `0.5px solid rgba(181,173,160,0.15)` |
| Track on bg | `#6B8F5E` (Matcha green) |
| Thumb | 20px `#FBF8F1` circle |
| Thumb shadow | `0 1px 3px rgba(28,27,24,0.06)` |
| Ring hover | thickens to 1px |
| Transition | 350ms contemplative |
| Focus-visible | gold focus ring |

#### Slider

| Property | Value |
|---|---|
| Track height | 1px |
| Track color | `rgba(181,173,160,0.3)` (Hai at 30%) |
| Track filled | `rgba(200,169,81,0.6)` (gold thread) |
| Thumb | 12px circle, `#FBF8F1` fill, `1px solid rgba(200,169,81,0.5)` border |
| Thumb hover | border widens to 1.5px |
| Thumb active | scale(1.1) |
| Value display | IBM Plex Mono, 12px |
| Transition | 300ms contemplative |

The slider track is a single gold thread -- the kintsugi repair line applied to range selection.

#### Divider / Horizontal Rule

| Property | Value |
|---|---|
| Height | 1px |
| Color | `rgba(200,169,81,0.25)` (gold at 25%) |
| Margin | 48px 0 (extreme vertical spacing) |
| Width | 100% or asymmetric (60% from left, 80% from right -- fukinsei balance) |

Dividers are gold repair lines, not grey rules. They represent the mended seam between content sections.

---

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| contemplative | `cubic-bezier(0.22, 1, 0.36, 1)` | Primary easing. Gentle deceleration like ink absorbing into paper fibers. Ease-out-quint. |
| incense | `cubic-bezier(0.12, 0.8, 0.3, 1)` | Very slow start, long gentle tail. For reveals and page entries. Like watching incense smoke rise. |
| settle | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Standard settle. For elements coming to rest after motion. |
| default | `cubic-bezier(0.4, 0, 0.2, 1)` | Fallback ease-in-out. Used only when no themed easing applies. |

This theme has NO spring animations. Springs imply bounce, elasticity, playfulness -- all antithetical to the contemplative identity. Every motion decelerates smoothly and settles without oscillation.

#### Duration × Easing × Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item bg/color | 300ms | contemplative | Slow color shift, no sudden changes |
| Button hover bg | 300ms | contemplative | Deliberate, visible transition |
| Button active scale | 200ms | settle | Press feedback, slightly faster |
| Toggle slide | 350ms | contemplative | Thumb slides contemplatively |
| Chip hover | 300ms | contemplative | Background warmth fades in |
| Card shadow on hover | 500ms | incense | Shadow deepens very slowly |
| Input focus ring | 400ms | contemplative | Gold ring appears gradually |
| Gold divider draw | 800ms | incense | Repair line draws across the page |
| Panel open/close | 600ms | incense | Sidebar, overlay panels |
| Modal enter | 800ms | incense | Long fade + subtle drift |
| Modal exit | 500ms | contemplative | Slightly faster exit than enter |
| Hero/page entry | 1000ms | incense | Content materializes like morning mist |
| Popover appear | 400ms | contemplative | Menu/dropdown entry |
| View transition | 600ms | incense | Cross-fade between views |
| Scroll reveal | 700ms | incense | Content revealed on scroll |
| Toast notification | 500ms | contemplative | Notification slides in |

Every duration in this theme is 200ms or longer. The minimum interaction speed is 200ms (active press). The maximum is 1000ms (page entry). This makes Kintsugi the slowest theme in the roster by a significant margin.

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.99 | Barely perceptible. Even press feedback is gentle. |
| Chips | 0.99 | Minimal |
| Buttons | 0.98 | Standard for this theme, but less than most themes |
| Tabs | 0.98 | Consistent with buttons |
| Cards (clickable) | 0.995 | Almost imperceptible on large surfaces |

Press scales are smaller than in other themes. Dramatic press feedback (0.95, 0.97) feels too aggressive for this contemplative space.

---

### Overlays

#### Popover / Dropdown

| Property | Value |
|---|---|
| bg | `#FBF8F1` (Kozo White) |
| border | `0.5px solid rgba(200,169,81,0.25)` (gold border, not grey) |
| radius | 8px |
| shadow | shadow-overlay |
| padding | 8px |
| z-index | 50 |
| min-width | 200px |
| max-width | 320px |
| Menu item | 8px 12px padding, radius 6px, h 40px, font bodySmall, color text-secondary |
| Menu item hover | bg `rgba(200,169,81,0.06)`, color text-primary |
| Separator | 1px gold-repair line at 20% opacity, margin 6px 0 |
| Transition | 400ms contemplative |

Popover borders use gold, not grey. The overlay's edge is a repair line -- it marks where the popup "breaks through" the surface beneath.

#### Modal

| Property | Value |
|---|---|
| Overlay bg | `rgba(28,27,24,0.20)` (very light warm scrim) |
| Overlay backdrop-filter | `blur(4px)` (subtle, paper-softening effect) |
| Content bg | `#FBF8F1` |
| Content border | `0.5px solid rgba(200,169,81,0.3)` (gold border) |
| Content shadow | shadow-overlay |
| Content radius | 12px |
| Content padding | 32px (generous internal spacing) |
| Entry | opacity `0` to `1` + translateY `8px` to `0`, 800ms incense |
| Exit | opacity `1` to `0`, 500ms contemplative |

The modal scrim is very light (20% opacity). The background should remain partially visible -- kintsugi does not hide what is behind. The gold border frames the modal as a repaired opening in the page.

#### Tooltip

| Property | Value |
|---|---|
| bg | `#1C1B18` (Sumi ink) |
| color | `#F5F0E6` (Washi) |
| font | label size (12px), Noto Serif |
| radius | 4px |
| padding | 6px 12px |
| shadow | `0 2px 6px rgba(28,27,24,0.08)` |
| No arrow | Position via offset |
| Entry | opacity fade, 300ms contemplative |

---

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 640px | Main content column. Narrow -- optimized for contemplative reading, ~55 characters per line at 17px serif. |
| Narrow max-width | 520px | Ultra-focused content. Journal entries, meditation prompts. |
| Sidebar width | 240px | Fixed sidebar. Narrower than most themes to maximize content breathing room. |
| Header height | 56px | Top bar. Taller for extra vertical breathing room. |
| Spacing unit | 8px | Base multiplier. Larger base unit than most themes (typically 4px). |

#### Spacing Scale

8, 16, 24, 32, 48, 64, 96, 128px

This is the most spacious scale in the roster. The smallest gap is 8px (one unit). The largest standard gap is 128px. Section breaks use 64-96px of vertical space. The absence of 4px and 6px values is deliberate -- this theme does not allow tight spacing.

| Context | Typical Gap | Notes |
|---|---|---|
| Between paragraphs | 24px | 1.5x the body font size |
| Between form fields | 32px | Wide vertical rhythm |
| Between cards | 32px | Cards float in space |
| Between sections | 64-96px | Major breathing room |
| Card internal padding | 32px | Generous internal space |
| Page edge padding | 48px | Content never touches edges |
| Between sidebar items | 8px | Minimum gap, only for related items |
| Header to content | 48px | Clear separation from navigation |

#### Radius Scale

| Token | Value | Usage |
|---|---|---|
| none | 0px | -- |
| sm | 4px | Badges, small elements |
| md | 6px | Sidebar items, menu items, buttons, inputs |
| lg | 8px | Cards, panels |
| xl | 12px | Modals, large panels |
| 2xl | 16px | Chat input card |
| full | 9999px | Toggles, avatars |

Radii are soft but not pill-shaped. The aesthetic is rounded pottery, not capsule buttons. Nothing below 4px (no sharp corners in this theme).

#### Density

Very sparse. This is the least dense theme in the roster. Content-to-whitespace ratio targets 35:65 or lower. Every element is surrounded by generous margins. If a layout feels "full," elements must be removed or spacing increased -- never decreased.

#### Responsive Notes

- **lg (1024px+):** Full sidebar (240px) + content column (640px max). Generous side margins.
- **md (768px):** Sidebar collapses to overlay panel. Content column expands but retains 32px+ side padding. Spacing scale reduces by one step (96px sections become 64px, etc.).
- **sm (640px):** Single column. Body text stays 17px minimum. Card internal padding reduces from 32px to 24px. Section spacing reduces from 64px to 48px. Side padding stays at 24px minimum. The theme should still feel spacious on mobile -- do not compact it to match typical mobile density.

---

### Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring color | `rgba(200, 169, 81, 0.50)` (kintsugi gold) |
| Focus ring width | 2px solid |
| Focus ring offset | 3px (inner ring: `#F5F0E6` washi bg color) |
| Disabled opacity | 0.4 |
| Disabled pointer-events | none |
| Disabled cursor | not-allowed |
| Selection bg | `rgba(200,169,81,0.18)` |
| Selection color | `#1C1B18` (Sumi, text-primary) |
| Scrollbar width | thin |
| Scrollbar thumb | `rgba(200,169,81,0.35)` (gold-tinted) |
| Scrollbar track | transparent |
| Min touch target | 48px (larger than standard 44px -- contemplative pace extends to generous tap areas) |
| Contrast standard | WCAG AA (4.5:1 text, 3:1 large text) |

**Contrast verification:**
- `text-primary` (#1C1B18) on `surface` (#FBF8F1): 15.2:1 -- exceeds AAA
- `text-secondary` (#6B665C) on `surface` (#FBF8F1): 4.8:1 -- meets AA
- `text-muted` (#8E8880) on `surface` (#FBF8F1): 3.6:1 -- meets AA for large text. For normal text on `bg` (#F5F0E6): 3.9:1. Use only for metadata/timestamps at 12px+ where WCAG permits 3:1 for large text, or increase to `#7A756D` for stricter compliance.
- `accent-primary` gold (#C8A951) on `surface` (#FBF8F1): 2.5:1 -- gold is NOT used for text (except `inlineCode` at darkened value `#7A6B3A` which achieves 5.8:1). Gold is structural, not textual.

**Reduced motion:**

| Behavior | Value |
|---|---|
| Strategy | `fade-only` -- all spatial animations collapse to simple opacity fades |
| Duration override | All durations cap at 200ms |
| Gold thread animation | Static (no shimmer) |
| Ink wicking reveal | Collapses to 200ms opacity fade |
| Paper settle | Static position, opacity-only |
| Contemplative fade | Duration reduces to 200ms |
| Washi paper texture | Static (no drift or animation) |
| Signature animations | All disabled |

---

### Visual Style

- **Material:** Washi paper. Not cotton stock (too Western), not rice paper (too thin), not cardboard (too coarse). Washi is handmade mulberry-bark paper with visible fiber inclusions, warm color from natural plant dyes, and a soft tactile quality. Surfaces should feel like you could touch them and feel fibers.

- **Washi Paper Texture:** Applied via SVG `feTurbulence` filter as a full-viewport overlay. The texture is extremely subtle -- it suggests the fiber structure of handmade paper without calling attention to itself.

```svg
<svg width="0" height="0" aria-hidden="true">
  <filter id="washi-grain">
    <feTurbulence
      type="fractalNoise"
      baseFrequency="0.9"
      numOctaves="3"
      stitchTiles="stitch"
      result="noise"
    />
    <feColorMatrix
      type="saturate"
      values="0"
      in="noise"
      result="mono"
    />
    <feBlend mode="multiply" in="SourceGraphic" in2="mono"/>
  </filter>
</svg>
```

Apply as a pseudo-element overlay on the page background:

```css
.kintsugi-page::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  filter: url(#washi-grain);
  opacity: 0.018; /* 1.8% -- barely perceptible */
  mix-blend-mode: multiply;
  z-index: 9999;
}
```

The `baseFrequency` of 0.9 creates a fine-grained fiber pattern (finer than Manuscript's 0.65, which simulates laid paper). The 1.8% opacity is intentionally lower than Manuscript's 3-4% -- washi paper is more delicate than Western laid paper.

- **Gold Crack Lines (Decorative):** Optional thin SVG paths that suggest kintsugi repair lines across card surfaces or between content blocks. These are not borders or dividers -- they are decorative crack patterns drawn with gold:

```css
.kintsugi-crack {
  background-image: url("data:image/svg+xml,..."); /* SVG path of irregular gold line */
  background-repeat: no-repeat;
  background-size: contain;
  opacity: 0.2;
  pointer-events: none;
}
```

The crack lines should be irregular, organic, branching -- not geometric. They suggest a history of breakage and repair. Use sparingly: one crack pattern per visible viewport maximum.

- **Grain:** Subtle (1.8% opacity). Washi fiber texture via feTurbulence.
- **Gloss:** Matte. Paper absorbs all light. Zero sheen, zero reflection.
- **Blend mode:** `multiply` for the paper grain overlay. `normal` for all other elements.
- **Shader bg:** False. No WebGL. SVG filter only.

---

### Signature Animations

#### 1. Ink Wicking Reveal

Content blocks appear with an upward wicking effect -- like ink being drawn up through paper fibers by capillary action. A vertical `clip-path` reveal expands from the bottom while opacity transitions from 0 to 1. The element appears to grow upward from its base, as ink wicks upward through wet paper.

```css
@keyframes ink-wick {
  from {
    clip-path: inset(100% 0 0 0);
    opacity: 0;
  }
  to {
    clip-path: inset(0 0 0 0);
    opacity: 1;
  }
}
.wick-reveal {
  animation: ink-wick 700ms cubic-bezier(0.12, 0.8, 0.3, 1) both;
}
```

Duration: 700ms, easing: incense. Reduced motion: 200ms opacity-only fade.

#### 2. Gold Thread Fill

Progress bars and loading indicators fill with a thin gold thread. The gold line has a subtle brightness shimmer that travels along its length via a shifting CSS gradient. The shimmer suggests molten gold being poured into a crack.

```css
.gold-thread {
  height: 2px;
  background: linear-gradient(
    90deg,
    var(--kintsugi-gold) 0%,
    #E0C56A 50%, /* brighter gold for shimmer */
    var(--kintsugi-gold) 100%
  );
  background-size: 200% 100%;
  animation: gold-shimmer 2s cubic-bezier(0.22, 1, 0.36, 1) infinite;
}
@keyframes gold-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

Duration: 2s full cycle, easing: contemplative. Reduced motion: static gold line, no shimmer.

#### 3. Paper Settle

Modals, cards, and panels enter with a gentle downward drift + fade -- like a sheet of washi paper settling onto a surface. The drift distance is very small (6px) and the motion is extremely gentle.

```css
@keyframes paper-settle {
  from {
    opacity: 0;
    transform: translateY(-6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.settle-enter {
  animation: paper-settle 800ms cubic-bezier(0.12, 0.8, 0.3, 1) both;
}
```

Duration: 800ms, easing: incense. The paper falls from above (negative translateY), unlike typical slides that come from below. Paper settles downward. Reduced motion: 200ms opacity-only.

#### 4. Contemplative Fade

View transitions and content changes use long crossfades with no spatial movement. Content dissolves rather than slides. This is the default transition for any content swap.

```css
@keyframes contemplative-fade {
  from { opacity: 0; }
  to { opacity: 1; }
}
.contemplate-enter {
  animation: contemplative-fade 600ms cubic-bezier(0.22, 1, 0.36, 1) both;
}
.contemplate-exit {
  animation: contemplative-fade 600ms cubic-bezier(0.22, 1, 0.36, 1) both reverse;
}
```

Duration: 600ms each direction, easing: contemplative. Reduced motion: 200ms fade.

#### 5. Gold Repair Draw

The signature animation. Gold repair lines (dividers, progress indicators, decorative cracks) draw themselves into existence from left to right, as if molten gold is flowing into the crack. Uses `stroke-dashoffset` for SVG lines or `scaleX` with `transform-origin: left` for CSS borders.

```css
@keyframes gold-repair {
  from {
    transform: scaleX(0);
    transform-origin: left;
  }
  to {
    transform: scaleX(1);
    transform-origin: left;
  }
}
.repair-line {
  animation: gold-repair 800ms cubic-bezier(0.12, 0.8, 0.3, 1) both;
}
```

Duration: 800ms, easing: incense. The line draws slowly, deliberately. Reduced motion: line appears instantly (no animation).

---

### Dark Mode Direction

Kintsugi is fundamentally a light theme -- washi paper is inherently light. However, a dark variant could explore the aesthetic of **urushi lacquerware**: deep lacquer-black surfaces with gold maki-e decoration.

**Direction (not full spec):**
- **Page/bg:** Urushi black `#141310` (warm lacquer darkness, not cold digital black)
- **Surface:** `#1E1D18` (dark warm brown, like aged lacquer)
- **Recessed:** `#0E0D0B` (deepest lacquer)
- **Text:** Washi `#F5F0E6` at 88% opacity for primary, 65% for secondary
- **Gold:** Brightens to `#D4B55A` for increased contrast on dark surfaces
- **Indigo accent:** Lifts to `#6A80B0` for readability
- **Borders:** `#302E28` used at same opacity scale
- **Shadows:** Transform from subtle warm shadows to subtle warm glows (`rgba(200,169,81,0.04)`)
- **Paper texture:** Inverts to a very subtle light noise on dark surfaces at 1% opacity
- **Character:** Shifts from washi paper to urushi lacquerware. The gold becomes maki-e gold decoration on lacquer. The metaphor changes from broken pottery to decorated lacquer boxes.

Full dark mode implementation is deferred. The theme's core identity is light-paper-forward.

---

### Mobile Notes

#### Effects to Disable
- Washi paper feTurbulence overlay -- static texture image fallback or disable entirely
- Gold crack decorative SVG lines -- remove on mobile
- Gold thread shimmer animation (signature #2) -- static gold fill
- Gold repair draw animation (signature #5) -- lines appear instantly

#### Adjustments
- Body text stays 17px minimum (CJK readability is non-negotiable)
- Card internal padding reduces from 32px to 24px
- Section spacing reduces from 64-96px to 48-64px (still generous by mobile standards)
- Chat input card radius reduces from 16px to 12px
- Side padding stays at 24px minimum (the spacious identity must survive mobile)
- Sidebar overlay width: 280px (slightly wider than desktop 240px for touch targets)
- All interactive elements maintain minimum 48px touch target
- Header height stays 56px
- Scrollbar styling removed (native mobile scrolling)
- Gold focus rings remain (important for accessibility even on mobile)

#### Performance Notes
- Washi paper SVG filter is the main performance concern. Disable on mobile or replace with a static PNG texture at 1x resolution.
- No `backdrop-filter` except on modal scrim (4px blur). Remove on mobile if janky.
- The slow animation durations (300-1000ms) are actually GPU-friendly -- they produce fewer paint operations per second than fast animations.
- `will-change: transform, opacity` only during active animations, never permanent.
- CJK font files are large. Use `font-display: swap` and lazy-load non-critical weights.
- Total animation budget on mobile: 1 concurrent transition. The contemplative pace means animations rarely overlap.

---

### Data Visualization

| Property | Value |
|---|---|
| Categorical palette | `#3D5A80` (Ai Indigo), `#6B8F5E` (Matcha), `#C8A951` (Gold), `#9B4A3A` (Beni), `#4A6E8A` (Hanada) -- 5 colors max |
| Sequential ramp | Single-hue gold: `#F5E6C0` to `#C8A951` to `#8A7235` |
| Diverging ramp | Matcha green to gold to Beni red: `#6B8F5E` to `#F5F0E6` to `#9B4A3A` |
| Grid lines | Low-ink: `border-base` at 8% opacity. Nearly invisible. |
| Max hues per chart | 3 (prefer 2) |
| Philosophy | Minimal annotation. Let the data breathe. Use gold sparingly for emphasis lines. |
| Axis labels | Noto Serif, 12px, text-secondary color |
| Value labels | IBM Plex Mono, 12px, text-primary color |

---

### Theme-Specific CSS Custom Properties

```css
:root[data-theme="kintsugi"] {
  /* Core surfaces */
  --page: #EDE8DC;
  --bg: #F5F0E6;
  --surface: #FBF8F1;
  --recessed: #E5DFCF;
  --active: #DDD6C4;

  /* Text */
  --text-primary: #1C1B18;
  --text-secondary: #6B665C;
  --text-muted: #8E8880;

  /* Kintsugi gold system */
  --kintsugi-gold: #C8A951;
  --kintsugi-gold-muted: rgba(200, 169, 81, 0.30);
  --kintsugi-gold-subtle: rgba(200, 169, 81, 0.15);
  --kintsugi-gold-focus: rgba(200, 169, 81, 0.50);
  --kintsugi-gold-hover: rgba(200, 169, 81, 0.08);

  /* Accents */
  --accent-primary: #C8A951;
  --accent-secondary: #3D5A80;

  /* Semantics */
  --success: #6B8F5E;
  --warning: #C4923A;
  --danger: #9B4A3A;
  --info: #4A6E8A;

  /* Borders */
  --border-base: #B5ADA0;
  --border-whisper: rgba(181, 173, 160, 0.08);
  --border-subtle: rgba(181, 173, 160, 0.15);
  --border-card: rgba(181, 173, 160, 0.20);
  --border-hover: rgba(181, 173, 160, 0.30);
  --border-focus: rgba(181, 173, 160, 0.40);

  /* Focus */
  --focus-ring: 0 0 0 3px var(--bg), 0 0 0 5px var(--kintsugi-gold-focus);

  /* Shadows */
  --shadow-breath: 0 2px 8px rgba(28, 27, 24, 0.03);
  --shadow-breath-hover: 0 3px 12px rgba(28, 27, 24, 0.05);
  --shadow-overlay: 0 4px 16px rgba(28, 27, 24, 0.06);

  /* Motion */
  --ease-contemplative: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-incense: cubic-bezier(0.12, 0.8, 0.3, 1);
  --ease-settle: cubic-bezier(0.25, 0.1, 0.25, 1);
  --duration-fast: 300ms;   /* "fast" in this theme is other themes' "slow" */
  --duration-normal: 500ms;
  --duration-slow: 800ms;
  --duration-reveal: 1000ms;

  /* Layout */
  --content-max-width: 640px;
  --narrow-max-width: 520px;
  --sidebar-width: 240px;
  --header-height: 56px;
  --spacing-unit: 8px;

  /* Typography */
  --font-display: "Shippori Mincho", "Hiragino Mincho ProN", "Yu Mincho", Georgia, serif;
  --font-body: "Noto Serif", Georgia, "Times New Roman", serif;
  --font-body-cjk: "Noto Serif JP", "Hiragino Mincho ProN", "Yu Mincho", serif;
  --font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
}
```

---

### Implementation Checklist

- [ ] Google Fonts loaded: Shippori Mincho (400, 500, 600), Noto Serif (400, 500 + italic), Noto Serif JP (400, 500), IBM Plex Mono (400)
- [ ] CSS custom properties defined for all color tokens including the gold system (`--kintsugi-gold`, `--kintsugi-gold-muted`, `--kintsugi-gold-subtle`, `--kintsugi-gold-focus`, `--kintsugi-gold-hover`)
- [ ] Focus ring uses gold (`rgba(200,169,81,0.50)`) on all interactive elements, not blue
- [ ] Gold caret color on text inputs (`caret-color: var(--kintsugi-gold)`)
- [ ] CJK font stack properly specified: `"Noto Serif JP"` in font-family for elements that may contain Japanese/Chinese/Korean text
- [ ] CJK-specific line-height (1.8) and letter-spacing (0.05em) applied when CJK content is detected (via `lang="ja"` / `lang="zh"` / `lang="ko"` attributes)
- [ ] `word-break: break-all` applied for CJK content containers
- [ ] Labels and metadata never use `text-transform: uppercase` (breaks CJK)
- [ ] `-webkit-font-smoothing: antialiased` on root element
- [ ] `text-wrap: pretty` for Latin body text, `auto` for CJK content
- [ ] Washi paper texture SVG filter implemented at 1.8% opacity with `mix-blend-mode: multiply`
- [ ] Gold repair lines used for section dividers (1px at 25% opacity, 48px+ margin)
- [ ] Gold bottom-border on selected cards
- [ ] Gold left-border on active sidebar items
- [ ] Border-radius minimum 4px (no sharp corners in this theme)
- [ ] Shadow tokens applied: shadow-breath at rest, shadow-breath-hover on hover
- [ ] Border opacity system implemented: whisper/subtle/card/hover/focus at 8/15/20/30/40%
- [ ] Spacing scale uses 8px base unit (minimum gap 8px, section gaps 64-96px)
- [ ] Content max-width 640px, sidebar 240px
- [ ] `prefers-reduced-motion` media query: all durations cap at 200ms, spatial animations collapse to opacity-only fades, all signature animations disabled, washi texture becomes static
- [ ] Scrollbar thumb uses gold tint (`rgba(200,169,81,0.35)`), transparent track
- [ ] Touch targets >= 48px on all interactive elements (larger than standard 44px)
- [ ] All transitions use contemplative (300ms+) or incense (500ms+) easing, nothing faster than 200ms except active press
- [ ] `::selection` styled with gold at 18% opacity
- [ ] `::placeholder` color matches `text-muted` token
- [ ] No gold background fills anywhere. Gold is linear only (lines, rings, borders).
- [ ] Asymmetric layout elements where appropriate (dividers at 60-80% width, left-aligned not centered)
- [ ] Mobile: washi texture disabled or replaced with static image, minimum 48px touch targets maintained, 17px CJK body text preserved
