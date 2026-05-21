---
title: Typography and color
scope: pptx-master
version: 1.0
---

# Typography and color

pptx-master uses a constrained typographic scale, spacing rhythm, and role-based palette system to keep decks consistent and readable.

The theme system lives in:

- `assets/palettes.json`
- `assets/themes.json`
- `references/visual-themes.md`

---

## Typography system

### Core hierarchy rules

- One dominant headline per slide (`h1`), one supporting level (`h2`), one body level.
- No more than 3 type sizes per slide, excluding chart labels and footnotes.
- Body text floor is `18pt` (`24pt` for accessibility-oriented decks).
- Assertion headline target: 5-12 words, at most 2 lines.

### Type scale defaults (16:9 deck)

| Token | Typical size | Min | Usage |
|---|---:|---:|---|
| `h1` | 38-44 pt | 34 pt | Primary slide assertion |
| `h2` | 28-34 pt | 24 pt | Card titles, section labels |
| `body` | 18-22 pt | 18 pt | Main narrative text |
| `caption` | 14-16 pt | 12 pt | Source lines, chart notes |
| `label` | 12-14 pt | 11 pt | Tags, small UI labels only |
| `hero_number` | 72-140 pt | 64 pt | A7 metric anchors |

### Line height and paragraph rhythm

- `h1`: `1.02-1.08`
- `h2`: `1.05-1.12`
- `body`: `1.18-1.28`
- `caption`: `1.15-1.25`

Paragraph spacing:

- Body paragraph spacing after: `0.20-0.32 in`
- Bullet spacing after: `0.10-0.18 in`
- Headline to first body block: `0.30-0.55 in`

### Font pairing and fallback

- Preferred pattern: one sans-serif family, weights `400/500/700`.
- Optional second family only for section-divider or quote headlines.
- Always define fallback families in tokens to reduce reflow on machines without brand fonts.
- If fallback changes line wraps, fix by editing copy or switching archetype before reducing body size.

## Archetype spacing cues

Use archetype-specific spacing as a quality guardrail.

| Archetype family | Headline top offset | Headline-to-content gap | Intra-block gap | Notes |
|---|---:|---:|---:|---|
| Hero (`A1`, `A4`, `A7`, `A22`) | 0.55-0.80 in | 0.45-0.80 in | 0.20-0.35 in | Preserve whitespace; do not stack dense bullets |
| Split (`A5`, `A6`, `A10`, `A20`) | 0.55-0.75 in | 0.30-0.55 in | 0.16-0.28 in | Keep mirrored columns with matched paddings |
| Grid/Card (`A8`, `A9`, `A23`) | 0.50-0.70 in | 0.28-0.45 in | 0.12-0.24 in | Card paddings should be consistent in each row |
| Process/Timeline (`A12`, `A13`, `A14`, `A15`) | 0.55-0.75 in | 0.32-0.55 in | 0.14-0.26 in | Node labels need extra breathing room near connectors |
| Diagram/Data (`A16`, `A17`, `A18`, `A19`) | 0.50-0.70 in | 0.25-0.45 in | 0.10-0.22 in | Prioritize label clarity over decorative spacing |
| Utility (`A2`, `A3`, `A24`) | 0.45-0.70 in | 0.30-0.60 in | 0.16-0.30 in | Section divider can exceed 55% whitespace |

Spacing violation indicators:

- More than 6 unique left-edge clusters on one slide
- Body blocks closer than `0.08 in`
- Headline sits closer to body than body blocks sit to each other
- Mixed card paddings in same grid row

## Color system

### Role-based tokens

Use semantic tokens instead of hard-coded hex:

- backgrounds: `bg`, `surface`
- text: `fg`, `muted`
- story: `primary`, `primary_light`, `primary_dark`
- status: `good`, `warn`, `bad`
- charts: `axis`, `gridline`, `annotation`

### Accent discipline

- Use one story color (`primary`) per slide.
- Use `accent_1` or `accent_2` only when a second semantic channel is truly needed.
- If a slide needs more than 3 attention colors, map extras to neutrals.

### Archetype color cues

- Hero slides (`A1`, `A4`, `A7`, `A22`): one focal color region plus neutral scaffold.
- Grid/card slides (`A8`, `A9`): neutral card surfaces with primary only for anchors.
- Comparison slides (`A10`, `A11`, `A20`): mirror both sides with equivalent saturation.
- Chart-first slides (`A17`, `A18`): one highlighted series, all context series muted.

## Gradients

Gradients are allowed in limited contexts:

- cover overlays (`A1`) to improve text readability on photos
- subtle header bars in dark themes

Rules:

- low contrast and low spatial frequency
- never used behind dense body paragraphs unless contrast passes
- expressed in IR as a gradient object (`style_tokens.fill`)

## Icons

Icons should be:

- consistent style (outline or solid, not mixed)
- used as semantic labels, not decoration
- tied to theme colors (`primary` or `muted`)

See `references/icon-library.md`.

## Accessibility and QA checks

- Enforce WCAG contrast targets:
  - normal text >= 4.5:1
  - large text >= 3.0:1
- Do not rely on color alone to convey meaning (add labels or shape cues).
- On dark themes, prefer slightly larger body text (`+1-2pt`) to offset projector bloom.

Automated checks:

- `scripts/preflight_ir.py` for contrast, density, and token consistency
- `scripts/preflight_pptx.py` for post-render QA
