# Pass 1 — Token Extraction

You are extracting design tokens from a UI screenshot. You have the element inventory from Pass 0.

## Context Provided
- Original screenshot image
- Pass 0 inventory JSON (elements, groups, patterns, platform guess)

## Instructions

For each element in the inventory, extract:

### Colors
- **Background color**: hex value of the element's fill. Sample the center of the element's bbox.
- **Foreground/text color**: hex value of text or icon color.
- **Border color**: if a visible border exists.
- For each color, note if it's solid or part of a gradient.

### Typography (for text elements)
- **Font family guess**: based on platform priors and glyph shapes.
  - iOS default: SF Pro (Display for > 20px, Text for ≤ 20px)
  - Android default: Roboto
  - Web: could be anything — note your best guess with confidence
- **Font size**: estimate in px. Use the bbox height × 0.75 as baseline.
- **Font weight**: 100–900 scale. Assess stroke thickness relative to height.
- **Line height**: bbox height ÷ number of visible lines.
- **Letter spacing**: `normal` unless visibly expanded/condensed.

### Spacing
- Measure distances between adjacent elements in the same group.
- Express in px (will be snapped to grid later).
- Note padding (element edge to content) vs margin (element to sibling).

### Borders & Radii
- Border width in px (0 if none visible).
- Border style: `solid`, `dashed`, `none`.
- Border radius: estimate from corner curvature. Use classification: `sharp` (<2px), `small` (2–6), `medium` (6–12), `large` (12–24), `pill` (height/2).

### Shadows
- If a shadow is visible: estimate `offsetX`, `offsetY`, `blur`, `spread`, `color`.
- Shadows are HARD to extract from screenshots. If uncertain, output your best guess with confidence < 0.5.

### Gradients
- If an element has a gradient fill, note: `linear` or `radial`, estimated angle/center, and color stops.

## Output Schema

```json
{
  "palette": [
    {"hex": "#FFFFFF", "role": "surface", "frequency": 0.35, "confidence": 0.95},
    {"hex": "#111827", "role": "text-primary", "frequency": 0.15, "confidence": 0.90}
  ],
  "elementTokens": [
    {
      "elementId": "elem_001",
      "tokens": {
        "backgroundColor": {"value": "#2563EB", "confidence": 0.92},
        "textColor": {"value": "#FFFFFF", "confidence": 0.88},
        "fontSize": {"value": 16, "unit": "px", "confidence": 0.75},
        "fontWeight": {"value": 600, "confidence": 0.65},
        "fontFamily": {"value": "SF Pro Text", "confidence": 0.60},
        "borderRadius": {"value": 12, "unit": "px", "confidence": 0.70},
        "paddingX": {"value": 24, "unit": "px", "confidence": 0.60},
        "paddingY": {"value": 12, "unit": "px", "confidence": 0.55}
      }
    }
  ],
  "spacingObservations": [
    {
      "between": ["elem_001", "elem_002"],
      "distance": 16,
      "unit": "px",
      "confidence": 0.70
    }
  ],
  "typographyScale": [
    {"role": "display", "size": 32, "weight": 700, "lineHeight": 40},
    {"role": "body", "size": 16, "weight": 400, "lineHeight": 24}
  ],
  "shadows": [
    {
      "elementId": "elem_005",
      "offsetX": 0, "offsetY": 2, "blur": 8, "spread": 0,
      "color": "rgba(0,0,0,0.12)",
      "confidence": 0.45
    }
  ],
  "gradients": [
    {
      "elementId": "elem_008",
      "type": "linear",
      "angle": 135,
      "stops": [
        {"color": "#667eea", "position": 0},
        {"color": "#764ba2", "position": 1}
      ],
      "confidence": 0.55
    }
  ]
}
```

## Critical Rules

- Always include `confidence` with every extracted value
- Ground-truth range: 0.95–1.0 (from DevTools/Figma)
- Measured (pixel sampling): 0.8–0.95
- LLM inference: 0.5–0.8
- Uncertain guess: < 0.5
- Shadows and gradients should almost NEVER exceed 0.7 confidence from screenshots
- When two colors are very similar (ΔE < 5), flag them for potential merge
- Use platform priors but mark them explicitly: `"source": "platform_prior"`
