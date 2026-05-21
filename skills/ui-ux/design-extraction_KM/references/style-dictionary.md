# Style Dictionary Integration

## SD v4 Key Differences from v3

| Feature | v3 | v4 |
|---------|----|----|
| Transform config | `format` (singular) | `hooks.formats` |
| Transform registration | `matcher` / `transformer` | `filter` / `transform` |
| DTCG support | No | Native `$value`/`$type` |
| sd-transforms compatibility | v0.x | v1.x (NOT v2.x which targets SD v5) |

## Setup

```bash
npm install style-dictionary@^4

# Optional: enhanced DTCG transforms from Tokens Studio
npm install @tokens-studio/sd-transforms@^1
```

## Build Commands

```bash
# Build all platforms (CSS, Tailwind, SwiftUI, Compose, SCSS)
node scripts/sd_build.mjs

# Build single platform
node scripts/sd_build.mjs --platform css

# Custom token source directory
node scripts/sd_build.mjs --source ./my-tokens
```

## Preparing Tokens

Extract tokens from the full design-spec JSON into standalone files for SD:

```bash
# Split into per-category files (color.json, space.json, etc.)
python scripts/dtcg_to_sd.py output.json --output tokens/ --split

# Expand composite tokens (typography → fontSize + fontWeight + ...)
python scripts/dtcg_to_sd.py output.json --output tokens/ --expand-composites --split

# Convert to legacy SD format (value/type instead of $value/$type) if needed
python scripts/dtcg_to_sd.py output.json --output tokens/ --legacy
```

## Platform Config

The SD config at `assets/sd-config.mjs` includes these custom hooks:

**Transforms** (hooks.transforms):
- `dtcg/color-hex` — Normalize hex to uppercase
- `dtcg/dimension-px` — Ensure px suffix on dimensions
- `dtcg/shadow-css` — Composite shadow → CSS shorthand
- `dtcg/gradient-css` — Composite gradient → CSS `linear-gradient()` / `radial-gradient()`
- `dtcg/typography-shorthand` — Composite typography → JSON string
- `swift/color` — Hex → SwiftUI `Color(red:green:blue:opacity:)`
- `swift/dimension` — Px → `CGFloat(N)`
- `compose/color` — Hex → Compose `Color(0xFFNNNNNN)`
- `compose/dimension` — Px → `N.dp`

**Formats** (hooks.formats):
- `custom/css-vars` — `:root { --name: value; }`
- `custom/tailwind` — Tailwind theme extend config
- `custom/swiftui` — `extension Color { static let ... }` + `extension CGFloat { ... }`
- `custom/compose` — `object Tokens { val ... }` with Compose imports
- `custom/scss-vars` — `$name: value;`

**Output platforms** → `dist/{css,tailwind,swift,compose,scss}/`

## Token Format Rules

SD v4 reads DTCG natively. Keep tokens clean:

```json
{
  "color": {
    "brand": {
      "primary": {
        "$type": "color",
        "$value": "#2563EB",
        "$description": "Primary brand color"
      }
    }
  }
}
```

Confidence and evidence belong in the separate `tokenMeta` block in the design spec — **never inside `$value`**. The `dtcg_to_sd.py` converter strips `tokenMeta` automatically when extracting tokens for SD.

## Extending with sd-transforms

For more advanced DTCG handling (color modifiers, math expressions, token references):

```javascript
import { register } from '@tokens-studio/sd-transforms';
register(sd); // Registers all Tokens Studio transforms
```

Use sd-transforms **v1.x** for SD v4. v2.x targets SD v5 and is incompatible.
