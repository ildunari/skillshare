---
title: IR schema
scope: pptx-master
version: 1.0
---

# IR schema

This document describes the **pptx-master intermediate representation (IR)** used to drive deterministic slide rendering.

The machine-readable schema is `references/ir.schema.json`.

## Backward compatibility

The schema is designed to be **backward compatible** with earlier IRs:

- Existing required fields (`deck.tokens`, `deck.slides`, `slide.id`, `slide.archetype`, `slide.headline`, `slide.elements`, `element.semantic_type`, `element.bbox`) remain valid.
- Most objects allow `additionalProperties` so older/extra fields do not break validation.

---

## Top-level

```json
{
  "deck": {
    "theme": { "id": "atlas", "mode": "light" },
    "density_profile": "comfortable",
    "narrative_arc": ["problem", "evidence", "plan", "decision"],
    "tokens": { "...": "..." },
    "slides": [ "...slides..." ]
  }
}
```

### `deck.theme` (optional)

A deck can reference a **visual theme** from `assets/themes.json`:

- `deck.theme.id`: theme id (e.g. `atlas`, `noir`, `paper`)
- `deck.theme.mode`: `light` or `dark` (optional; themes already declare their mode)

If `tokens` are present (recommended), the renderer may treat theme as a **default override**.

### `deck.density_profile` (optional)

Controls default whitespace choices and content capacity:

- `sparse` — lots of whitespace, fewer elements
- `comfortable` — default
- `dense` — more content, tighter spacing

### `deck.narrative_arc` (optional)

Ordered section list used by QA for section coverage and rhythm checks.

Allowed item shapes:

- string section name, e.g. `"problem"`
- object with section metadata, e.g. `{ "section": "problem", "goal": "Create urgency" }`

### `deck.speaker_notes_defaults` (optional)

A string, array of strings, or object. Used as a default notes template for each slide.

---

## Slides

Each slide:

- selects an `archetype`
- has a top-level `headline` string (even if it is also represented as a headline element)
- contains a list of `elements`

```json
{
  "id": "S03",
  "archetype": "A9",
  "section": "evidence",
  "parent_slide": "S02",
  "headline": "Key customer outcomes",
  "density_profile": "comfortable",
  "speaker_notes": [
    "Set context in one sentence.",
    "Then walk cards left-to-right."
  ],
  "animations": { "preset": "auto" },
  "elements": [ "...elements..." ]
}
```

### Slide theme overrides (optional)

`slide.theme` can override `deck.theme` for a single slide (rare; use sparingly).

### Slide hierarchy/notes fields (optional)

- `slide.section` — section tag aligned to `deck.narrative_arc`
- `slide.parent_slide` — parent/continuation linkage by slide id
- `slide.speaker_notes` — string, array of strings, or object (same shape as `deck.speaker_notes_defaults`)

---

## Elements

Elements are semantically typed boxes placed on the slide.

Minimum required fields:

- `semantic_type` (enum)
- `bbox` `{x,y,w,h}` in inches

Common fields:

- `id` — stable id for animation targeting (recommended)
- `content` — text content for text-like elements
- `style_tokens` — styling overrides and token refs
- `children` — nested elements (e.g. a card containing title/body children)
- `iconRef` — icon reference for icon elements
- `src` — image source for images
- `data` — chart/table data payload (renderer-specific)

### `semantic_type` (expanded)

The enum includes:

- text: `headline`, `text`, `caption`, `quote`
- media: `image`, `icon`, `logo`
- media variants: `picture`
- structure: `card`, `panel`, `badge`, `divider`
- utility text: `footer`, `number`, `node`
- data viz: `chart`, `table`, `axis`, `legend`, `callout`, `annotation`
- flows: `timeline_node`, `step`, `process_step`, `connector`, `arrow`, `line`
- people: `person`
- KPIs: `kpi`, `metric`, `sparkline`

---

## Style tokens

`style_tokens` is an object of **token references** and overrides, e.g.

```json
{
  "style_tokens": {
    "font": "body",
    "size": "body",
    "color": "fg",
    "fill": "surface",
    "radius": "card",
    "chart": { "gridline_opacity": 0.25 }
  }
}
```

### Gradients

`style_tokens.fill` may be either:

- a string token (`"surface"`, `"primary_light"`, etc.)
- a gradient object:

```json
{
  "fill": {
    "type": "linear",
    "angle_deg": 90,
    "stops": [
      { "pos": 0.0, "color": "#0B1020", "alpha": 1.0 },
      { "pos": 1.0, "color": "#0B1020", "alpha": 0.0 }
    ]
  }
}
```

---

## Animations

`slide.animations` describes build animations. Two common modes:

1) **Auto preset** (recommended):
```json
{ "preset": "auto" }
```

2) **Explicit steps**:
```json
{
  "defaults": { "effect": "fade", "duration_ms": 320, "stagger_ms": 60 },
  "steps": [
    { "targets": ["name:el:S03:card:0"], "effect": "fade" },
    { "targets": ["name:el:S03:card:1"], "effect": "fade" }
  ]
}
```

Supported `effect` values:

- `appear`, `fade`, `wipe`, `zoom`

Targets can be:

- `spid:7` (direct shape id)
- `name:...` or a name string (recommended)
- a bbox selector object `{bbox:{...}, text_contains:"..."}`

Animations are injected into the PPTX by `scripts/inject_animations.py`.

---

## Constraints (optional)

`deck.constraints` and `slide.constraints` allow future tuning and overrides (e.g., stricter contrast thresholds).  
The current renderer and preflight scripts treat these as optional hints.
