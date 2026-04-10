# Design System Integration

> How to translate design system tokens, brand guidelines, and Figma/CSS specifications into image generation prompt constraints for consistent asset production.

## The Core Insight

Design tokens are prompt constraints. Every token in your design system has a natural language equivalent that can be embedded in an image gen prompt. The translation isn't always 1:1, but it's close enough to produce assets that feel native to the system.

## Token Translation Table

| Token Category | Design System Format | Image Gen Prompt Translation |
|---|---|---|
| **Primary color** | `--color-primary: #2563EB` | "primary blue (#2563EB)" — always name + hex backup |
| **Secondary color** | `--color-secondary: #10B981` | "accent emerald green (#10B981)" |
| **Neutral palette** | `--gray-50` through `--gray-900` | "warm grays" or "cool grays" — specify range, not every shade |
| **Font family** | `font-family: Inter` | "clean geometric sans-serif typography, Inter-style" |
| **Font family** | `font-family: 'Playfair Display'` | "elegant serif typography, high-contrast letterforms" |
| **Border radius** | `border-radius: 12px` | "rounded corners, soft geometry" |
| **Border radius** | `border-radius: 2px` | "sharp corners, crisp geometric edges" |
| **Spacing scale** | `--space-4: 16px; --space-8: 32px` | "generous whitespace" or "tight, compact spacing" |
| **Shadow** | `box-shadow: 0 4px 6px rgba(0,0,0,0.1)` | "subtle soft shadows, gentle depth" |
| **Shadow** | `box-shadow: none` | "flat design, no shadows" |
| **Elevation** | Material Design elevation levels | "layered surfaces with subtle depth" or "completely flat" |
| **Animation** | `transition: 200ms ease` | "smooth, subtle" (for animation frame context) |
| **Animation** | `transition: 500ms spring` | "bouncy, energetic" (for animation frame context) |
| **Dark mode** | `background: #0a0a0a` | "dark background (#0a0a0a), light elements, adequate contrast" |
| **Opacity** | `opacity: 0.6` | "semi-transparent, 60% opacity" |

## Building a Prompt Style Block from Design Tokens

### Step 1: Extract the Relevant Tokens

Not every design token matters for image generation. Focus on:
- **Colors:** Primary, secondary, accent, background, text (5-7 colors max)
- **Typography direction:** Serif vs sans-serif, geometric vs humanist, weight range
- **Geometry:** Corner radius (rounded vs sharp), shape language
- **Depth:** Flat vs elevated, shadow intensity
- **Mood:** The emotional direction the design system conveys

### Step 2: Write the Style Block

Create a reusable block that gets prepended to every prompt for this design system:

```
DESIGN SYSTEM STYLE BLOCK:
Color palette: [primary_name] (#hex), [secondary_name] (#hex), [accent_name] (#hex),
[background_name] (#hex). Limited to these colors plus black and white.
Typography direction: [sans-serif/serif], [geometric/humanist], [clean/decorative].
Geometry: [rounded/sharp] corners, [organic/geometric] shapes.
Depth: [flat/subtle shadow/layered elevation].
Mood: [warm/cool/neutral], [professional/playful/technical], [minimal/rich].
```

### Step 3: Validate with a Test Generation

Before committing to a batch, generate one test asset using the style block. Check:
- Do the colors read correctly? (If not, try descriptive names or upload a palette swatch)
- Does the typography direction match the system's personality?
- Does the geometry feel right?
- Does the overall mood align?

Adjust the style block based on the test, then lock it for the batch.

## Figma-Specific Integration

### Extracting Tokens from Figma

If the user has a Figma file with a design system:

1. **Use the ui-spec-extractor skill** to extract design tokens from a screenshot of the Figma component library
2. **Or read Figma variables directly** using the Figma MCP connector (`get_variable_defs`)
3. **Or ask the user** to export their design tokens as JSON (Figma → Tokens Studio → JSON export)

### Figma → Prompt Translation Workflow

```
Figma Variables/Styles
        ↓
Extract: colors, typography, spacing, corner radius, shadows
        ↓
Translate to natural language (Token Translation Table above)
        ↓
Assemble into Style Block
        ↓
Prepend Style Block to each asset prompt
        ↓
Generate → Review → Adjust Style Block if needed
```

## CSS Variables → Style Block

If the user provides CSS custom properties:

```css
:root {
  --color-primary: #2563EB;
  --color-secondary: #10B981;
  --color-accent: #F59E0B;
  --color-bg: #FAFAFA;
  --color-text: #1F2937;
  --font-heading: 'Inter', sans-serif;
  --font-body: 'Inter', sans-serif;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
}
```

Translates to:

```
DESIGN SYSTEM STYLE BLOCK:
Color palette: bright blue (#2563EB), emerald green (#10B981), warm amber (#F59E0B),
light gray background (#FAFAFA), dark charcoal text (#1F2937). Limited to these 5 colors.
Typography: clean geometric sans-serif (Inter-style), consistent weight.
Geometry: moderately rounded corners (not sharp, not pill-shaped), geometric shapes.
Depth: very subtle shadows, almost flat design.
Mood: professional, clean, modern, slightly warm neutral.
```

## Tailwind Config → Style Block

If the user provides a Tailwind config or uses Tailwind defaults:

```js
// tailwind.config.js
colors: {
  primary: '#6366F1',    // indigo
  secondary: '#EC4899',  // pink
  accent: '#14B8A6',     // teal
}
```

Translates to:

```
DESIGN SYSTEM STYLE BLOCK:
Color palette: vibrant indigo (#6366F1), hot pink (#EC4899), teal accent (#14B8A6).
Modern, bold color choices. Flat or minimal shadows.
Typography: system sans-serif, clean and readable.
Geometry: Tailwind-default rounded corners (moderate), utility-first aesthetic.
Mood: modern, vibrant, tech-forward.
```

## Brand Guidelines → Style Block

When working from a brand guide PDF or document:

### What to Extract
1. **Primary and secondary brand colors** (including acceptable variations)
2. **Typography** (brand fonts, backup fonts, hierarchy)
3. **Photography/illustration style** (if documented)
4. **Brand personality keywords** (usually in the "brand voice" section)
5. **Logo usage rules** (so you know what NOT to include in assets)
6. **Do/don't examples** (the most useful part — shows what the brand considers on-brand vs off-brand)

### Translation Priority
Brand personality keywords translate directly to mood descriptors:
- "Innovative and bold" → "modern, bold composition, strong color contrast"
- "Trustworthy and established" → "professional, stable, traditional composition, muted palette"
- "Playful and approachable" → "friendly, rounded shapes, warm colors, gentle mood"
- "Premium and refined" → "elegant, restrained palette, generous whitespace, subtle detail"

## Multi-Asset Consistency Protocol

When generating a set of assets for the same design system:

### Before Starting
1. Write the Style Block (one time)
2. Generate an anchor image (first asset, full style description)
3. Save the anchor — you'll upload it as reference for every subsequent generation

### During Generation
4. Every prompt = Style Block + Asset-specific content + Reference image upload
5. Never modify the Style Block between assets
6. If a generation drifts from the style, fix it with editing (Gemini) or regeneration (GPT/Grok) — don't adjust the Style Block to match the drift

### After Generation
7. Review all assets side by side
8. Check: Do they look like they belong together?
9. If not: identify which asset drifted and regenerate it, not the others
10. Document the final Style Block for future sessions

## Dark Mode Considerations

When generating assets for dark mode interfaces:

### Color Adjustments
- Reduce saturation slightly — vibrant colors on dark backgrounds appear more intense
- Use lighter variants of brand colors (e.g., if primary is #2563EB, dark mode might use #60A5FA)
- Ensure adequate contrast against the dark background (WCAG AA minimum)

### Prompt Additions for Dark Mode
```
Dark mode context: asset will be displayed on a near-black background (#0a0a0a to #1a1a2e).
Use lighter color variants for visibility. No white bleeds or pure white elements.
Ensure adequate contrast — minimum 4.5:1 against the dark background.
If the asset has a background, use [dark background color] to match the app's dark theme.
```

### Generating Both Modes
For assets that need light and dark variants:
1. Generate the light mode version first
2. Use conversational editing (Gemini) or session memory (GPT) to create the dark variant
3. Edit prompt: "Create a dark mode version of the previous image. Change the background to [dark color], adjust element colors for contrast against dark background, reduce saturation slightly."

## Platform-Specific Image Requirements

Quick reference for common platform asset specs:

| Platform | Asset | Dimensions | Notes |
|---|---|---|---|
| iOS | App icon | 1024x1024 | Rounded corners applied by OS |
| Android | Adaptive icon | 108x108dp (432x432px @4x) | Safe zone: inner 66dp circle |
| Web favicon | Favicon | 32x32, 16x16, 180x180 | Need multiple sizes |
| Web | OG image | 1200x630 | Social media preview |
| App Store | Screenshots | Various per device | Usually 1290x2796 (iPhone 15 Pro Max) |

Generate at the highest resolution the model supports, then resize/crop to target dimensions.
