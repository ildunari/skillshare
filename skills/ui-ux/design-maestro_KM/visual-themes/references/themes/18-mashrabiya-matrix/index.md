# Mashrabiya Matrix — Quick Reference

**Tagline:** Light filtered through geometric lattice -- bilateral symmetry, mathematical ornament, and the architecture of sacred pattern.

**Best for:** RTL-first applications, Arabic/Farsi/Hebrew content platforms, Islamic art galleries, architectural portfolios, calligraphy tools, geometric pattern generators, educational platforms for Middle Eastern studies, prayer time apps, cultural heritage archives, bilateral composition experiments.

**Core Philosophy:** RTL-native design with `direction: rtl` as default. Pattern-based elevation using geometric lattice overlays. Bilateral symmetry. No springs, only smooth mathematical curves. Turquoise = action, gold = emphasis.

---

## Color Tokens (Complete)

| Token | Hex | OKLCH | Role |
|---|---|---|---|
| **page** | `#F0E6D3` | L=0.93 C=0.03 h=78 | Rimal (Sand). Deepest background, desert sand courtyard floor |
| **bg** | `#F5EDE0` | L=0.95 C=0.02 h=75 | Qashani (Plaster). Primary surface, lime-washed plaster wall |
| **surface** | `#FAF5EC` | L=0.97 C=0.01 h=72 | Jiss (Gypsum). Elevated cards/inputs/popovers, carved gypsum |
| **recessed** | `#E5DACA` | L=0.89 C=0.03 h=76 | Tafl (Clay). Code blocks, inset areas, unfired clay tone |
| **active** | `#D9CEBC` | L=0.85 C=0.03 h=74 | Khashab (Wood). Active/pressed items, carved cedarwood |
| **text-primary** | `#1B2838` | L=0.22 C=0.04 h=250 | Hibr (Ink). Headings, body text, calligraphy blue-black |
| **text-secondary** | `#5A6370` | L=0.46 C=0.02 h=240 | Ramadi (Ash). Sidebar items, secondary labels, blue-grey |
| **text-muted** | `#8A8F96` | L=0.61 C=0.01 h=240 | Dabaab (Haze). Placeholders, timestamps, morning haze |
| **text-onAccent** | `#FAF5EC` | L=0.97 C=0.01 h=72 | Jiss (Gypsum). Text on accent backgrounds |
| **border-base** | `#B0A898` | L=0.72 C=0.02 h=70 | Turab (Dust). Base border, used at variable opacity |
| **accent-primary** | `#2A9D8F` | L=0.60 C=0.10 h=175 | Firuzaj (Turquoise Tile). Interactive elements, CTAs, links |
| **accent-secondary** | `#C9A84C` | L=0.73 C=0.12 h=85 | Lajward (Lapis Gold). Highlights, active indicators, selected states |
| **success** | `#5E8A5E` | L=0.55 C=0.08 h=140 | Zaytun (Olive). Positive states, courtyard olive tree |
| **warning** | `#C49A3A` | L=0.68 C=0.12 h=80 | Zaafaran (Saffron). Caution states, saffron spice |
| **danger** | `#9B3A3A` | L=0.42 C=0.12 h=22 | Yaqut (Ruby). Error states, ruby gemstone |
| **info** | `#3D5A8A` | L=0.43 C=0.08 h=250 | Nili (Indigo). Informational states, natural indigo dye |
| **inlineCode** | `#5A7A6A` | — | Muted teal-grey for code within prose |
| **toggleActive** | `#2A9D8F` | — | Toggle/switch active track (turquoise tile) |
| **selection** | `rgba(42, 157, 143, 0.15)` | — | `::selection` background, turquoise at 15% |
| **lattice-pattern** | `#B0A898` | — | SVG lattice line color (same as border-base) |
| **lattice-pattern-gold** | `rgba(201, 168, 76, 0.20)` | — | Gold lattice highlight for elevated surfaces |
| **lattice-shadow** | `rgba(27, 40, 56, 0.04)` | — | Light shadow cast by lattice on surfaces |

**Border Opacity Scale:** whisper 6% | subtle 12% | card 20% | hover 30% | focus 40% | lattice 8%

**Color Rules:**
- No pure greys — all neutrals carry warm sand-ivory undertone
- Turquoise = action (buttons, links, toggles, focus rings)
- Lapis gold = emphasis (selection, active states, highlights)
- Elevation = brightness (sand → gypsum)
- No gradients. Flat plaster/gypsum surfaces.
- Blue-black text on warm ivory = Islamic manuscript palette

---

## Typography (All 9 Roles + Caption)

| Role | Family | Size | Weight | LH | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| **Display** | serif (Playfair Display) | 36px | 700 | 1.3 | -0.01em | `liga, kern, opsz:auto` | Hero titles, page names (Arabic: 34px) |
| **Heading** | serif (Playfair Display) | 24px | 600 | 1.4 | normal | `liga` | Section titles, settings headers |
| **Subheading** | serif (Playfair Display) | 19px | 500 | 1.5 | 0.01em | — | Subsection labels |
| **Body** | sans (IBM Plex Sans Arabic) | 16px | 400 | 1.7 | normal | `liga, kern, calt` | Primary reading text (Latin/Arabic default) |
| **Body Arabic** | sans (IBM Plex Sans Arabic) | 17px | 400 | 1.8 | 0.02em | `liga, kern, calt, rlig` | Arabic/Farsi/Urdu body (required ligatures for shaping) |
| **Body Small** | sans (IBM Plex Sans Arabic) | 14px | 400 | 1.6 | normal | — | Sidebar items, secondary UI text |
| **Button** | sans (IBM Plex Sans Arabic) | 14px | 500 | 1.4 | 0.02em | — | Button labels |
| **Input** | sans (IBM Plex Sans Arabic) | 15px | 400 | 1.5 | normal | — | Form input text (15px for Arabic readability) |
| **Label** | sans (IBM Plex Sans Arabic) | 12px | 500 | 1.4 | 0.04em | `text-transform: none` | Metadata, timestamps (NEVER uppercase) |
| **Code** | mono (IBM Plex Mono) | 0.9em | 400 | 1.6 | normal | `liga: 0, direction: ltr` | Inline code, blocks (ALWAYS LTR) |
| **Caption** | sans (IBM Plex Sans Arabic) | 12px | 400 | 1.5 | 0.02em | — | Disclaimers, footnotes |

**Font Stack:**
- Display: `"Playfair Display", "Amiri", "Noto Serif", Georgia, serif`
- Body (Arabic-first): `"IBM Plex Sans Arabic", "Noto Sans Arabic", "Tahoma", system-ui, sans-serif`
- Mono: `"IBM Plex Mono", "SFMono-Regular", Consolas, monospace`

**RTL Typography Critical Rules:**
- `direction: rtl` on root (default). LTR is the variant.
- Arabic body minimum 17px, line-height 1.8 (diacritics need space)
- ALWAYS use logical properties: `inline-start`/`inline-end`, `padding-inline`, `margin-inline`, `border-inline-start`
- Code blocks: `direction: ltr` always (apply `dir="ltr"` explicitly)
- Numbers/data: `direction: ltr` + `unicode-bidi: isolate`
- NEVER `text-transform: uppercase` (Arabic has no case)
- NEVER letter-space Arabic headings (breaks ligatures)
- `hyphens: none` for Arabic
- `-webkit-font-smoothing: antialiased` required

---

## Elevation System

**Strategy:** Pattern-based (unique to this theme). Lattice density = elevation, not shadow depth.

| Surface | Bg | Pattern | Shadow | Usage |
|---|---|---|---|---|
| page | `#F0E6D3` | 8-pt star 3% opacity, 48px repeat | none | Page background |
| qashani | `#F5EDE0` | None | none | Primary content surface |
| jiss | `#FAF5EC` | Hexagon band 8%, 4px wide | `0 1px 4px rgba(27,40,56,0.03)` | Cards, inputs |
| tafl | `#E5DACA` | None | `inset 0 1px 2px rgba(27,40,56,0.03)` | Code blocks |
| overlay | `#FAF5EC` | 12-pt rosette 5%, 16px repeat | `0 4px 20px rgba(27,40,56,0.08)` | Popovers, modals |

**Shadow Tokens:**
- `shadow-lattice`: `0 1px 4px rgba(27,40,56,0.03)` — cards at rest
- `shadow-lattice-hover`: `0 2px 8px rgba(27,40,56,0.05)` — card hover
- `shadow-lattice-focus`: `0 2px 8px rgba(27,40,56,0.05), 0 0 0 2px rgba(42,157,143,0.4)` — input focus
- `shadow-overlay`: `0 4px 20px rgba(27,40,56,0.08)` — popovers, modals
- `shadow-inset`: `inset 0 1px 2px rgba(27,40,56,0.03)` — recessed surfaces

---

## Border System

**Widths:** hairline 0.5px | default 1px | medium 1.5px | heavy 2px | lattice-band 4px

**Opacity Scale (on border-base):** whisper 6% | subtle 12% | card 20% | hover 30% | focus 40%

**Focus Ring:** `rgba(42, 157, 143, 0.45)` turquoise, 2px solid, 2px offset
- Implementation: `box-shadow: 0 0 0 2px var(--bg), 0 0 0 4px rgba(42,157,143,0.45)`

---

## Component Quick-Reference

### Primary Button
- **Rest:** bg `#2A9D8F` (turquoise), color `#FAF5EC`, radius 6px, h 36px, padding `0 20px`, shadow none
- **Hover:** bg `#248F82`, shadow `shadow-lattice`
- **Active:** bg `#1E8175`, `scale(0.97)`
- **Focus:** turquoise focus ring
- **Disabled:** opacity 0.45, grayscale(20%), pointer-events none
- **Transition:** bg 150ms symmetric-ease, transform 100ms symmetric-ease

### Text Input
- **Rest:** bg `#FAF5EC`, border `1px solid rgba(176,168,152,0.12)`, radius 6px, h 44px, padding `0 14px`, caret-color `#2A9D8F`, `direction: inherit`
- **Hover:** border at 25% opacity
- **Focus:** border `1px solid rgba(42,157,143,0.4)` (turquoise), shadow `shadow-lattice-focus`
- **Disabled:** opacity 0.45, bg `#E5DACA`, pointer-events none
- **Transition:** border-color 200ms, box-shadow 250ms symmetric-ease

### Card
- **Rest:** bg `#FAF5EC`, border `0.5px solid rgba(176,168,152,0.20)`, radius 8px, shadow `shadow-lattice`, padding 20px. Optional: 4px lattice-frame top edge.
- **Hover:** border at 30%, shadow `shadow-lattice-hover`
- **Selected:** `border-inline-start: 2px solid rgba(201,168,76,0.5)` (gold, right edge in RTL)
- **Transition:** border-color 200ms, box-shadow 250ms symmetric-ease

---

## Motion Map

**Easings:**
- `symmetric-ease`: `cubic-bezier(0.4, 0, 0.2, 1)` — primary, balanced
- `unfold`: `cubic-bezier(0.19, 1, 0.22, 1)` — expand/unfold from center
- `lattice-open`: `cubic-bezier(0.12, 0.8, 0.3, 1)` — lattice pattern reveal, slow unfurl
- `settle`: `cubic-bezier(0.25, 0.1, 0.25, 1)` — standard settle

**Key Durations:**
- Sidebar item: 150ms symmetric-ease
- Button hover: 150ms symmetric-ease
- Toggle: 200ms symmetric-ease
- Card hover: 250ms symmetric-ease
- Lattice reveal: 600ms lattice-open
- Panel open/close: 400ms unfold
- Modal enter: 350ms unfold

**Active Press:** nav 0.985 | chip 0.995 | button 0.97 | tab 0.95

**NO SPRINGS.** Only smooth mathematical curves.

---

## Layout Tokens

- **Content max-width:** 768px
- **Narrow max-width:** 640px
- **Sidebar width:** 280px (anchored `inline-end` = right in RTL)
- **Header height:** 48px
- **Spacing unit:** 4px
- **Spacing scale:** 4, 6, 8, 12, 16, 20, 24, 32, 48, 64px
- **Radius scale:** sm 4px | md 6px | lg 8px | xl 12px | 2xl 16px | full 9999px
- **Density:** Comfortable (50:50 content-to-whitespace)

**RTL Layout Rules:**
- Sidebar: right edge in RTL, slides out to right
- Active indicators: `border-inline-start` (right edge in RTL)
- Progress bars: fill right-to-left in RTL
- Toasts: slide in from right in RTL
- Modals: close button at top-left in RTL (visual "end")

---

## Accessibility

- **Focus ring:** `rgba(42, 157, 143, 0.45)` turquoise, 2px solid, 2px offset
- **Disabled:** opacity 0.45, pointer-events none, cursor not-allowed, grayscale(20%)
- **Selection:** bg `rgba(42,157,143,0.15)`, color `#1B2838`
- **Scrollbar:** thumb `rgba(42,157,143,0.25)`, track transparent, width thin
- **Min touch target:** 44px
- **Contrast:** WCAG AA minimum
  - text-primary on surface: 13.8:1 (AAA)
  - text-secondary on surface: 5.1:1 (AA)
  - accent-primary on surface: 3.8:1 (AA large text/UI)
- **Reduced motion:** fade-only, durations cap at 150ms, lattice animations static

---

## Section Index (from full.md)

1. **Identity & Philosophy** — Line 38
2. **Color System** — Line 62 (Palette | Special Tokens | Lattice Pattern System | Opacity System | Color Rules)
3. **Typography Matrix** — Line 150 (Font Stack | RTL Typography Rules | Bidirectional Content Handling | Typographic Decisions | Font Loading)
4. **Elevation System** — Line 257 (Surface Hierarchy | Shadow Tokens | Separation Recipe)
5. **Border System** — Line 292 (Widths | Opacity Scale | Border Patterns | Focus Ring)
6. **Component States** — Line 344 (Primary Buttons | Ghost Buttons | Text Input | Chat Input Card | Cards | Sidebar Items | Chips | Toggle/Switch | Slider | Divider/HR)
7. **Motion Map** — Line 475 (Easings | Duration×Easing×Component | Active Press Scale)
8. **Overlays** — Line 521 (Popover/Dropdown | Modal | Tooltip)
9. **Layout Tokens** — Line 577 (Spacing Scale | Radius Scale | Density | Responsive Notes | RTL Layout Rules)
10. **Accessibility Tokens** — Line 650
11. **Visual Style** — Line 701 (Material, Lattice Overlays, Bilateral Symmetry, Grain/Gloss)
12. **Signature Animations** — Line 740 (Lattice Unfold | Geometric Frieze Draw | Star Rotation Reveal | Centripetal Gather | Tile Mosaic Build)
13. **Dark Mode Variant** — Line 897 (Dark Palette | Dark Mode Rules)
14. **Mobile Notes** — Line 935 (Effects to Disable | Adjustments | Performance Notes)
15. **Data Visualization** — Line 971
16. **Theme-Specific CSS Custom Properties** — Line 987
17. **Implementation Checklist** — Line 1076 (Core Setup | RTL-Specific | Typography | Lattice Patterns | Visual System | Motion & Interaction | Layout | Accessibility | Mobile)

---

**Visual Identity:** Plaster and carved gypsum on cedarwood lattice. Matte finish. No grain. SVG geometric patterns only. Bilateral symmetry enforced. RTL-native. Turquoise = action, gold = emphasis. Pattern density = elevation.

**Anti-patterns:** No decorative pastiche. No LTR-adapted layouts. No maximalism. No dark base. No orientalist kitsch. No Western serif. No springs. No gradients. No uppercase labels. No letter-spacing on Arabic text.
