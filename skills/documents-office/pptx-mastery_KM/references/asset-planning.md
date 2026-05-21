# Asset planning

Asset planning prevents late-stage slide rework by deciding image, icon, and chart needs before rendering.

## Asset planning workflow

1. Inventory needed assets per slide.
2. Classify each asset as required, optional, or decorative.
3. Select one style direction per section.
4. Validate rights, quality, and aspect ratio early.
5. Reserve fallback options for missing assets.

## Asset classes

| Class | Purpose | Typical archetypes | Minimum spec |
|---|---|---|---|
| Hero photo | Emotion/context | A1, A4, A22 | >= 1920 px on long edge |
| Product screenshot | Evidence | A5, A6, A20 | Clean crop, no UI clutter |
| Icon | Semantic labeling | A8, A9, A14, A23 | Single icon family, vector-preferred |
| Diagram | Structure | A16 | Consistent stroke and label style |
| Chart image/export | Data evidence | A17, A18 | Label legibility at final scale |

## Slide-level asset spec template

Use this template during planning:

```json
{
  "slide_id": "S07",
  "archetype": "A9_card_grid",
  "asset_plan": [
    {
      "role": "icon",
      "count": 4,
      "required": true,
      "style_family": "lucide-outline",
      "fallback": "text-only cards with token badges"
    }
  ]
}
```

## Image handling guardrails

- Do not add an image unless it supports the slide assertion.
- Prefer one strong image over multiple weak thumbnails.
- Avoid mixing photography and illustration styles in one section.
- Keep subject crop stable across related slides.
- Add overlays only when they improve readability.

## Asset coherence rules

- One icon family per deck.
- One photo treatment per section (natural color, duotone, or monochrome).
- One chart style system per deck (axes, gridline intensity, label format).
- If a section changes visual language, signal that with a section break.

## QA checks for assets

1. Relevance: Does the asset support the claim?
2. Resolution: Is effective size readable on projected output?
3. Consistency: Does style match neighboring slides?
4. Contrast: Is overlaid text readable?
5. Rights: Is usage licensed or approved?
