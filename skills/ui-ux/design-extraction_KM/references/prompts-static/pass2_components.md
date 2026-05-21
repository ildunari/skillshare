# Pass 2 — Component Detection

You are grouping UI elements into components and assigning semantic token references.

## Context Provided
- Original screenshot
- Pass 0 inventory (elements, groups)
- Pass 1 token extraction (palette, element tokens, spacing)

## Instructions

### 1. Component Identification

Group related elements into components:

- **Button** = background rect + text (+ optional icon)
- **Input/TextField** = border rect + placeholder/value text + label above
- **Card** = container + title + body text + optional image + optional actions
- **NavBar** = horizontal container at top with logo/title + nav items
- **TabBar** = horizontal/vertical group of selectable items with active indicator
- **List Item** = repeating pattern: icon/avatar + text + optional accessory
- **Modal/Dialog** = overlay container with title + content + action buttons
- **Form** = vertical stack of labeled inputs + submit button

For each component:
- Assign a `type` from the taxonomy above
- Map its visual properties to token paths (e.g., `background → color.brand.primary`)
- Identify which state it's showing (default, hover, focus, active, disabled, error)
- Note any visible variants (primary vs secondary button, small vs large)

### 2. Token Reference Mapping

For each component style property, reference a token path:
```json
"tokenRefs": {
  "background": "color.brand.primary",
  "textColor": "color.surface",
  "borderRadius": "radius.md",
  "paddingX": "space.4",
  "paddingY": "space.2",
  "fontSize": "typography.body.fontSize",
  "fontWeight": "typography.body.fontWeight"
}
```

When the same raw value appears in multiple components, they MUST reference the SAME token.

### 3. Raw Fallback

Include raw pixel values as fallback for properties that couldn't be tokenized:
```json
"raw": {
  "borderWidth": 1,
  "boxShadow": "0 2px 8px rgba(0,0,0,0.12)"
}
```

## Output Schema

```json
{
  "components": [
    {
      "id": "cmp_001",
      "type": "Button",
      "name": "Primary CTA",
      "elementIds": ["elem_003", "elem_004"],
      "bbox": {"x": 0.08, "y": 0.60, "w": 0.84, "h": 0.07, "unit": "norm"},
      "styles": {
        "tokenRefs": {
          "background": "color.brand.primary",
          "textColor": "color.surface",
          "borderRadius": "radius.md"
        },
        "raw": {
          "fontWeight": 600,
          "paddingVertical": 12,
          "paddingHorizontal": 24
        },
        "states": {
          "hover": {"background": "color.brand.primary-dark"},
          "disabled": {"opacity": 0.5}
        }
      },
      "text": "Sign in",
      "variants": [
        {"name": "secondary", "differences": {"background": "transparent", "borderColor": "color.brand.primary"}}
      ],
      "confidence": 0.82,
      "notes": "Hover/disabled states inferred from platform defaults"
    }
  ],
  "tokenDefinitions": {
    "color": {
      "surface": {"$type": "color", "$value": "#FFFFFF"},
      "brand": {
        "primary": {"$type": "color", "$value": "#2563EB"}
      },
      "text": {
        "primary": {"$type": "color", "$value": "#111827"},
        "muted": {"$type": "color", "$value": "#6B7280"}
      }
    },
    "space": {
      "1": {"$type": "dimension", "$value": "4px"},
      "2": {"$type": "dimension", "$value": "8px"},
      "3": {"$type": "dimension", "$value": "12px"},
      "4": {"$type": "dimension", "$value": "16px"},
      "6": {"$type": "dimension", "$value": "24px"}
    },
    "radius": {
      "sm": {"$type": "dimension", "$value": "8px"},
      "md": {"$type": "dimension", "$value": "12px"}
    },
    "typography": {
      "body": {
        "$type": "typography",
        "$value": {
          "fontFamily": "SF Pro Text",
          "fontSize": "16px",
          "fontWeight": 400,
          "lineHeight": "24px"
        }
      }
    }
  }
}
```

## Critical Rules

- Every component MUST reference tokens from `tokenDefinitions`, not inline raw values
- If the same hex color appears in 3+ places, it MUST be a named token
- Spacing values MUST be snapped to the detected spacing scale (4px grid default)
- States you haven't seen (hover, focus) should be `null` not guessed — add to `openQuestions`
- Include `confidence` per component: ground truth = 0.95+, hybrid = 0.7–0.9, screenshot-only < 0.7
