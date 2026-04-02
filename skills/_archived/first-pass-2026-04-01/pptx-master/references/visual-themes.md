---
title: Visual themes
scope: pptx-master
version: 1.0
---

# Visual themes

This document defines a **theme system** for pptx-master: a small set of curated looks that (a) keep decks consistent, (b) are *computable* (the renderer can apply them deterministically), and (c) avoid the common “AI slide” tells (random colors, inconsistent radii, mismatched icon styles, and unbalanced typography).

The machine-readable sources of truth are:

- `assets/palettes.json` (color tokens, light + dark)
- `assets/themes.json` (theme = palette + typography + shape treatments + motion defaults)

---

## Design goals

### What “professional” means here

- **Consistency across slides:** one palette, one typographic scale, one corner-radius, one shadow style.
- **Hierarchy is obvious:** headline reads as headline, not just “bigger body text”.
- **Whitespace is intentional:** slides should feel *spacious*, not like documents.
- **Color is disciplined:** neutrals do most of the work; accent is used sparingly (one “story color” per slide).
- **Charts are executive-readable:** clear labels, light gridlines, high-contrast axes, and one highlighted series.

### Common “AI slide” failure modes this system prevents

- Too many competing accent colors.
- Overused icons with inconsistent stroke weights.
- Unmotivated gradients and heavy shadows.
- Text that is technically “inside the box” but feels cramped.

---

## Palette tokens

A palette is **role-based**, not arbitrary. Every palette provides the following tokens (both light and dark mode):

| Token | Meaning | Typical usage |
|---|---|---|
| `bg` | Slide background | default slide fill |
| `surface` | Secondary panel surface | cards, tables, annotation boxes |
| `fg` | Primary text | headlines, body |
| `muted` | Secondary text | captions, axis labels |
| `border` | Hairlines and separators | card outlines, table rules |
| `primary` | Story color | hero metric, highlighted series |
| `primary_dark` | Stronger primary | emphasis strokes, dark header bars |
| `primary_light` | Tint of primary | callout backgrounds |
| `accent_1`, `accent_2` | Secondary accents (rare) | icons, secondary callouts |
| `series_1..series_6` | Chart categorical series | multi-series charts |
| `good`, `warn`, `bad` | Status semantic colors | KPI deltas, risk markers |
| `gridline` | Chart gridlines | very light |
| `axis` | Chart axes and tick labels | darker than gridline |
| `annotation` | Annotation fills | highlight regions behind labels |

### Accessibility constraints

- Text contrast should meet WCAG 2.1 thresholds:
  - **Normal text:** ≥ 4.5:1
  - **Large text (≥ 24 pt regular or ≥ 18 pt bold):** ≥ 3.0:1  
  (See `references/constraints-qa.md` for the exact formula and enforcement approach.)
- `series_1..series_6` are chosen to be **colorblind-friendly** by default (Okabe–Ito / Tol-inspired qualitative colors).

---

## Theme tokens

A theme selects:

1. A palette (`palette.id` + `palette.mode`)
2. A typography scale
3. Shape treatments (radius, border width, shadow)
4. Motion defaults (slide transitions and build animations)

In practice:

- **Palette** sets color.
- **Theme** sets how the deck “feels” (sharp vs rounded, flat vs elevated, calm vs energetic).

---

## Included themes

All themes are defined in `assets/themes.json`.

### 1) Atlas (default)

- Palette: `consulting_blue` (light)
- Look: modern consulting, clean, restrained.
- Use when: general business decks, strategy, updates.

### 2) Noir

- Palette: `midnight_cyan` (dark)
- Look: dark-mode boardroom, high contrast.
- Use when: product launches, design reviews, conference talks.

### 3) Paper

- Palette: `sand_navy` (light)
- Look: editorial, minimal motion, subtle borders.
- Use when: research reports, academic-style decks, PDFs.

### 4) Pulse

- Palette: `warm_gray_coral` (light)
- Look: energetic and contemporary, slightly bolder radii/shadows.
- Use when: marketing narratives, customer storytelling.

### 5) Sage

- Palette: `forest_amber` (light)
- Look: calm, “sustainability” friendly.
- Use when: ESG decks, ops, people/HR, roadmap planning.

### 6) Plasma

- Palette: `plum` (dark)
- Look: expressive dark theme, slightly stronger motion defaults.
- Use when: creative/tech decks, demos, internal all-hands.

### 7) Mono

- Palette: `mono_ink` (light)
- Look: strict monochrome; use accent rarely.
- Use when: legal/compliance, minimalism, print-first.

### 8) Clinical

- Palette: `clinical_green` (light)
- Look: healthcare/biomed friendly, clean, trustworthy.
- Use when: medical, life sciences, regulatory, clinical ops.

---

## Theme selection decision tree

Pick one deck theme before writing slide copy.

```text
START
  |
  v
Is this a high-trust, data-heavy business deck? -> YES -> Atlas
  |                                               NO
  v
Is this a formal compliance/legal or print-first deck? -> YES -> Mono or Paper
  |                                                     NO
  v
Is this healthcare/science/regulatory? -> YES -> Clinical
  |                                       NO
  v
Is the tone energetic storytelling/marketing? -> YES -> Pulse
  |                                             NO
  v
Is this sustainability/ops/people narrative? -> YES -> Sage
  |                                              NO
  v
Do you need dark-stage presentation conditions? -> YES -> Noir or Plasma
  |                                               NO
  v
Fallback -> Atlas
```

Practical tie-breakers:

- Choose `Noir` over `Plasma` when readability and restraint matter more than expression.
- Choose `Paper` over `Mono` when you want softer editorial tone.
- Choose `Pulse` only when the story has clear visual emphasis moments.

Theme-lock rule:

- Use one theme per deck.
- Section-level theme overrides are exceptional and should be explicitly justified.
- If a section uses dark mode while the deck is light mode, that section should be a divider or hero moment.

---

## Dark mode rules

Dark themes are not “invert everything”.

- Keep **surface** slightly lighter than `bg` so cards read as panels.
- Use `muted` for secondary text, but ensure it stays above contrast threshold.
- Prefer **tints** (`primary_light`) for large annotation areas rather than fully saturated fills.
- In charts:
  - `gridline` stays subtle (low contrast),
  - `axis` must remain readable.

### Dark mode QA protocol

Run these checks whenever `palette.mode = dark`:

1. Contrast sweep on all text roles (`fg`, `muted`, `primary` over `bg`/`surface`).
2. Surface separation check (`surface` visibly distinct from `bg`).
3. Chart legibility check (`axis` and labels remain readable at projector brightness).
4. Highlight discipline check (one dominant color anchor per slide).
5. Thumbnail pass to catch bloom and halo artifacts around small text.

Common dark-mode failures and fixes:

| Failure | Symptom | Fix |
|---|---|---|
| Flat panels | Cards disappear into background | Increase `surface` luminance delta from `bg` |
| Glare accents | Saturated blocks overpower text | Replace solid fills with `primary_light` tint |
| Washed labels | Axis/caption unreadable on projector | Boost `muted` contrast, increase size by 1-2pt |
| Rainbow drift | Too many saturated series colors | Use one story series + muted context series |
| Halo text | Thin fonts blur on dark | Move to weight 500+, increase line-height slightly |

### Dark mode deployment guidance

- Prefer dark themes for hero moments, stage talks, demos, and product reveals.
- Avoid dark mode for dense appendix tables unless contrast and size are verified.
- For mixed-mode decks, place dark slides at section boundaries to maintain rhythm.

---

## Chart color strategy

Even though palettes provide `series_1..series_6`, for executive charts:

- Use **one highlighted series** (usually `primary`) for the story.
- Use `muted` / gray for context series.
- Avoid rainbow unless the categorical distinction matters.

Recommended mapping (renderer-level default):

- `story` → `primary`
- `context` → `muted`
- additional categorical series → `series_1..series_6` (starting at `series_1`)

---

## Sources and further reading

- Okabe–Ito colorblind-safe palette (widely used in scientific visualization): https://jfly.uni-koeln.de/color/
- Paul Tol qualitative palettes (color-deficiency friendly): https://personal.sron.nl/~pault/
- ColorBrewer palettes (mapping and cartography provenance): https://colorbrewer2.org/
