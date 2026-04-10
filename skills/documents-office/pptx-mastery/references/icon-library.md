---
title: Icon library
scope: pptx-master
version: 1.0
---

# Icon library

pptx-master uses icons as **supporting visuals**, not decoration. The goal is consistent stroke weight, consistent size, and predictable placement.

## Recommended default icon set

- **Lucide** (outline icons; consistent style; broad coverage)
- Set id in IR: `lucide`

Reference: https://lucide.dev/

> The renderer may implement other sets later, but `lucide` should be treated as the default.

---

## IR representation

Icons are represented as normal elements with `semantic_type: "icon"` plus an `iconRef`.

```json
{
  "id": "icon:0",
  "semantic_type": "icon",
  "iconRef": { "set": "lucide", "name": "activity", "style": "outline" },
  "bbox": { "x": 1.05, "y": 2.15, "w": 0.6, "h": 0.6 },
  "style_tokens": { "color": "primary" }
}
```

### `iconRef`

| Field | Required | Meaning |
|---|---:|---|
| `set` | ✅ | icon set id (`lucide`) |
| `name` | ✅ | icon name (`activity`, `shield`, `trending-up`, …) |
| `style` | optional | `outline` / `solid` / `duotone` (default `outline`) |

### Rendering rule of thumb

- Render SVG to PNG at **2× the displayed size** (or 3× for very thin strokes), then place it as an image.
- Always preserve aspect ratio.
- Use theme tokens for color:
  - primary icon on light theme: `primary`
  - secondary icon: `muted`
  - on dark theme: ensure contrast against `surface`/`bg`

---

## Sizing guidelines

| Context | Typical icon size |
|---|---|
| Icon grid (A8) | 0.7–0.9 in |
| Card title icon | 0.35–0.55 in |
| KPI tile accent | 0.45–0.65 in |
| Small inline (next to label) | 0.25–0.35 in |

---

## Style consistency rules

- Do not mix outline and solid icons in the same deck.
- Stroke weight should match the theme (default ~1.6–1.8 pt at 0.8 in icon size).
- Avoid emojis unless explicitly requested.

---

## Accessibility

- Icons should not be the only encoding for meaning.
- If the icon conveys essential information, include it in speaker notes or nearby text.

