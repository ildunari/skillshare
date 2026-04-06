# Pass 3 — Layout Analysis

You are analyzing the spatial layout structure of the UI from the screenshot and previous passes.

## Context Provided
- Original screenshot
- Pass 0 inventory (elements, groups, patterns)
- Pass 1 tokens (spacing observations, palette)
- Pass 2 components (grouped components, token definitions)

## Instructions

### 1. Layout Hierarchy

Build a tree structure showing how components are nested:
```
root
├── header (NavBar)
│   ├── logo (Image)
│   └── nav_items (Container → horizontal)
├── main_content (Container → vertical)
│   ├── hero_section (Container)
│   │   ├── heading (Text)
│   │   └── subheading (Text)
│   └── form_section (Form → vertical)
│       ├── email_input (TextField)
│       ├── password_input (TextField)
│       └── submit_button (Button)
└── footer (Container)
```

For each node:
- `direction`: `vertical` or `horizontal`
- `alignment`: `start`, `center`, `end`, `stretch`
- `spacingToken`: reference to a space token (e.g., `space.4`)

### 2. Grid Detection

Analyze the screenshot for grid structure:
- **Column count**: how many content columns? (1, 2, 3, 4, 6, 12 are common)
- **Gutter width**: space between columns in px
- **Margins**: left/right page margins in px
- **Spacing unit**: base spacing multiplier (usually 4px or 8px)

### 3. Spacing Scale Validation

Verify that observed spacing values fit a consistent scale:
- Common scales: 4px base (4, 8, 12, 16, 20, 24, 32, 40, 48, 64)
- Material Design: 4dp base
- iOS: 8pt base (8, 16, 24, 32)
- Flag any spacing that doesn't fit the scale

### 4. Responsive Hints

If the layout suggests responsive behavior:
- Wide elements with percentage-like widths suggest fluid layout
- Fixed-width containers suggest max-width constraints
- Stacked vs side-by-side suggests breakpoint behavior

## Output Schema

```json
{
  "hierarchy": {
    "id": "root",
    "type": "root",
    "direction": "vertical",
    "alignment": "stretch",
    "children": [
      {
        "id": "header",
        "type": "container",
        "componentRef": "cmp_nav",
        "direction": "horizontal",
        "alignment": "center",
        "spacingToken": "space.4",
        "children": []
      },
      {
        "id": "main",
        "type": "section",
        "direction": "vertical",
        "alignment": "center",
        "spacingToken": "space.6",
        "children": [
          {"id": "cmp_001", "type": "element", "children": []},
          {"id": "cmp_002", "type": "element", "children": []}
        ]
      }
    ]
  },
  "grid": {
    "columnCount": 1,
    "gutterPx": 0,
    "marginPx": 16,
    "spacingUnitPx": 8,
    "spacingScale": [4, 8, 12, 16, 24, 32],
    "confidence": 0.80
  },
  "constraints": [
    {
      "type": "alignment",
      "elements": ["cmp_001", "cmp_002", "cmp_003"],
      "value": "left-aligned with 16px margin",
      "confidence": 0.85
    },
    {
      "type": "spacing",
      "elements": ["cmp_002", "cmp_003"],
      "value": "consistent 16px vertical gap",
      "confidence": 0.78
    },
    {
      "type": "containment",
      "elements": ["cmp_001"],
      "value": "full-width within 16px margins",
      "confidence": 0.82
    }
  ],
  "responsiveHints": [
    "Single-column layout suggests mobile-first or narrow viewport",
    "Full-width button suggests touch-friendly design"
  ],
  "offGridWarnings": [
    {
      "between": ["cmp_001", "cmp_002"],
      "observed": 14,
      "nearestOnGrid": 16,
      "delta": 2,
      "note": "May be sub-pixel rendering artifact"
    }
  ]
}
```

## Critical Rules

- The hierarchy MUST be a valid tree — every component appears exactly once
- Spacing tokens MUST reference values from Pass 2's `tokenDefinitions`
- Grid analysis should snap values to nearest 4px multiple
- Mark responsive hints as speculative — they require multiple viewport screenshots to confirm
- If layout is ambiguous between flexbox and grid, prefer the simpler model
