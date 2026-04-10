# UI/UX Asset Prompt Patterns

> Reusable prompt templates and strategies for each UI asset type. These are model-agnostic structures — adapt length and style per the target model's guide.

## Universal Prompt Anatomy

Every UI asset prompt has these layers:

```
LAYER 1: Asset type + context       → "App icon for a fitness tracker"
LAYER 2: Style constraints          → "Flat design, geometric, 3-color palette"
LAYER 3: Composition                → "Centered, 20% padding, square canvas"
LAYER 4: Color specification        → "Coral (#FF6B6B), teal (#4ECDC4), white"
LAYER 5: Technical requirements     → "No gradients, clean edges, SVG-ready"
LAYER 6: Exclusions                 → "No text, no shadows, no background detail"
```

Not every prompt needs all six layers. Icons need all of them. Hero images skip Layer 5. Match to the asset.

---

## Icon Packs

### The Batch-First Strategy

Generate all icons in a **single large image** (grid layout), then split into individual assets. This produces dramatically better visual coherence than generating one icon at a time.

### Prompt Template: Icon Grid

```
[NUMBER] flat design [STYLE] icons for [CONTEXT] arranged in a [ROWS x COLS] grid.
Style: [AESTHETIC], [COLOR_PALETTE], [LINE/FILL_TREATMENT].
Objects: [LIST_EACH_ICON].
Properties: centered composition per cell, consistent [STROKE/FILL] weight,
uniform padding, same visual weight across all icons.
Background: [COLOR].
No text, no labels, no decorative elements.
```

**Example:**
```
6 flat design outline icons for a food delivery app arranged in a 2x3 grid.
Style: minimalist line art, monochrome dark charcoal (#333333), 2px uniform stroke, rounded line caps.
Objects: restaurant building, shopping bag, star rating, wallet, chat bubble, location pin.
Properties: centered composition per cell, consistent stroke weight, uniform padding, same visual weight.
Background: white.
No text, no labels, no decorative elements.
```

### Prompt Template: Single Icon

```
[CONCEPT] icon in [STYLE] style.
[SHAPE_CONSTRAINTS]: geometric shapes, [SPECIFIC_ELEMENTS].
[STROKE/FILL]: [WEIGHT] stroke, [COLOR], [FILL_TREATMENT].
Canvas: [DIMENSIONS], centered, [PADDING]% padding.
No shadows, no texture, no gradients. Clean edges for vector conversion.
```

### Icon Consistency Checklist
- Same stroke weight across all icons
- Same corner radius / line cap style
- Same visual weight (no icon dominates or recedes)
- Same level of detail (if one is simple, all are simple)
- Same padding and centering approach
- Same color treatment (all outline, all filled, all duotone)

---

## App Icons (Launcher Icons)

### Key Requirements
- Square 1:1 aspect ratio
- Must read at 32px (Android adaptive), 60px (iOS), and 1024px (App Store)
- Simple, bold silhouette — the "squint test"
- Single focal element, not a miniature scene
- No text (exception: single letter/monogram)

### Prompt Template

```
App launcher icon for [APP_NAME/CONCEPT].
Single [OBJECT/SYMBOL] centered on [BACKGROUND_COLOR] background.
Style: [AESTHETIC] — bold, simple, instantly recognizable.
Color: [PRIMARY] with [ACCENT] highlight. Maximum 3 colors.
Rounded corners (iOS superellipse style).
No text, no fine detail, no gradients.
Must be recognizable as a tiny silhouette.
```

---

## Onboarding Illustrations

### Key Requirements
- Friendly, approachable, inclusive
- Clear narrative: each illustration shows a benefit or action
- Consistent character style across the set
- Space for headline and body copy below/beside

### Prompt Template

```
Onboarding illustration for [APP_CONTEXT] showing [ACTION/BENEFIT].
Style: [AESTHETIC] — friendly, warm, approachable.
Character: [DESCRIPTION], [INCLUSIVE_REPRESENTATION], engaging expression.
Setting: [CONTEXT-APPROPRIATE_ENVIRONMENT].
Mood: warm, encouraging, [SPECIFIC_EMOTION].
Composition: [ALIGNMENT], clear hierarchy, generous whitespace.
Leave clear space at [POSITION] for text overlay.
Color palette: [COLORS] — consistent with brand.
Aspect ratio: [RATIO].
```

### Onboarding Set Consistency
Generate all illustrations in the same session. After the first image, reference it:
"Using the exact same illustration style, character proportions, and color palette as the previous image, now show [next scene]."

---

## Empty State / Error State Graphics

### Key Requirements
- Helpful, not frustrating — tone matters enormously
- Large, recognizable central icon or illustration
- Clear space for explanatory text
- Mood: "this is fine, here's what to do" not "something broke"

### Prompt Template

```
Empty state illustration for [CONTEXT: "no search results" / "inbox zero" / "first time setup"].
Style: minimal, friendly, [AESTHETIC].
Central element: [LARGE_RECOGNIZABLE_VISUAL].
Mood: [helpful / encouraging / lighthearted] — NOT sad or broken.
Color palette: [COLORS], muted, calming.
Composition: centered, generous whitespace, clear area below for copy.
Aspect ratio: [RATIO — usually 1:1 or 4:3].
No text in the illustration itself.
```

---

## Hero Images

### Key Requirements
- High visual impact, sets the mood for the page
- Clear text overlay space (usually left or center)
- Professional photography or illustration quality
- Aspect ratio: typically 16:9 or 21:9 for web

### Prompt Template

```
Hero image for [PRODUCT/FEATURE]: showing [KEY_BENEFIT/ACTION].
Style: [AESTHETIC] — [clean/bold/modern/warm], professional quality.
Composition: [LAYOUT — e.g., "subject left, negative space right for text overlay"].
[People if applicable: diverse, engaged, action-oriented].
Environment: [CONTEXT — workspace, lifestyle, abstract gradient].
Lighting: [QUALITY — bright, warm, dramatic], clean shadows.
Clear area at [POSITION] for headline overlay.
Aspect ratio: [RATIO].
Color mood: [PALETTE_DIRECTION].
```

---

## Animation Keyframes (Start/End Frames)

### The Two-Frame Strategy

Generate a **start frame** and an **end frame** that define the motion. Use AI interpolation tools (Neural Frames, KomikoAI, Magic Animator) to generate the in-between frames.

### Key Requirements
- Identical style, lighting, and proportions across both frames
- Clear state difference (position, scale, color, visibility)
- Flat, consistent lighting (dramatic shadows shift between frames and break interpolation)
- Same canvas size and composition boundaries

### Prompt Template: Start Frame

```
[CONTEXT] animation start frame.
[ELEMENT] in [INITIAL_STATE — position, size, color, opacity].
Style: flat design, consistent line weight, [AESTHETIC].
Lighting: even, flat (no dramatic shadows).
Background: [SOLID_COLOR].
Canvas: [DIMENSIONS], [ELEMENT_POSITION].
No motion blur, no transition effects — static frame only.
```

### Prompt Template: End Frame

```
[CONTEXT] animation end frame — same element as start frame.
[ELEMENT] in [FINAL_STATE — new position, size, color, opacity].
Style: IDENTICAL to start frame — same line weight, same colors, same rendering.
Lighting: even, flat (matching start frame exactly).
Background: [SAME_SOLID_COLOR].
Canvas: [SAME_DIMENSIONS], [NEW_ELEMENT_POSITION].
No motion blur — static frame only.
```

### Animation Frame Consistency Tips
- Generate both frames in the same session
- Upload the start frame as reference when generating the end frame
- Describe the change explicitly: "The only difference from the reference is [specific change]"
- Keep backgrounds simple — complex backgrounds make interpolation messy
- Specify easing/feeling in a separate note for the interpolation tool: "smooth ease-in-out," "bouncy spring," "snappy"

---

## Card Thumbnails

### Prompt Template

```
Thumbnail image for [CONTENT_TYPE] card: [SUBJECT].
Style: [AESTHETIC] — eye-catching, professional.
Composition: [FOCAL_POINT] centered, tight crop, [ASPECT_RATIO].
Color mood: [PALETTE].
No text overlay — image only.
Must work at both 300px and 600px width.
```

---

## Textures & Patterns (Backgrounds)

### Prompt Template

```
Seamless tileable [PATTERN_TYPE] pattern.
Style: [AESTHETIC] — [subtle/bold], [COLOR_PALETTE].
Density: [SPARSE/MODERATE/DENSE] distribution.
Tile-friendly: edges must flow seamlessly when repeated.
No focal point — uniform visual weight across the entire image.
Background: [BASE_COLOR].
Square canvas.
```

---

## SVG Conversion Pipeline

When assets will be converted to SVG, add these constraints to ANY prompt:

### Must-Include Keywords
- "Flat design" or "vector style"
- "Geometric shapes"
- "No gradients, no texture, no shadows"
- "Limited palette (3-5 colors)"
- "Clean edges, high contrast"
- "Solid fills" or "uniform stroke weight"
- "White background" or "transparent background"

### Post-Generation SVG Pipeline

**Step 1: Upscale (if needed)**
- Use AI upscaler (Upscayl, free) for small icons before vectorization

**Step 2: Vectorize**
| Tool | Best For |
|---|---|
| Vectorizer.AI | Fast cloud-based, handles complex images |
| Vector Magic | High quality, interactive manual refinement |
| Recraft AI Vectorizer | Built into Recraft ecosystem |
| Adobe Illustrator Image Trace | Professional refinement, full control |
| Inkscape Trace Bitmap | Free, open source |

**Step 3: Optimize**
- Run through SVGO (svgomg.net or `svgo` CLI)
- Target: <5KB for icons, <50KB for illustrations
- Remove unnecessary groups, flatten layer structure
- Standardize viewBox for responsive scaling
- Remove or standardize stroke widths

**Step 4: Cleanup**
- Edit in Illustrator, Inkscape, or Boxy SVG
- Adjust anchor points, consolidate overlapping paths
- Align strokes, verify transparency

---

## Transparency & Background Removal

### Native Transparency
Some tools generate transparent backgrounds natively:
- Leonardo.AI has a transparency toggle
- Prompt inclusion: "transparent background," "isolated subject," "no background"

### Two-Step Approach (Most Reliable)
1. Generate image with simple solid background
2. Remove background with: Photoroom, Adobe Express, or Remove.bg
3. Export as PNG with alpha channel

### SVG Transparency
After vectorization, transparency is inherent (no raster background). Use `opacity` or SVG masks for partial transparency.

---

## Batch Production Workflow

For generating a cohesive set of 6+ assets:

1. **Create a style reference block** — write once, reuse verbatim:
```
STYLE BLOCK (reuse for all generations):
Style: [AESTHETIC]. Color palette: [COLORS]. Line weight: [WEIGHT].
Corner style: [ROUNDED/SHARP]. Fill treatment: [SOLID/OUTLINE/DUOTONE].
Background: [COLOR]. Mood: [DESCRIPTOR].
```

2. **Generate anchor image** — the first asset with full style description
3. **Upload anchor as reference** for all subsequent generations
4. **Vary only the subject** — keep the style block identical
5. **Curate in batches** — generate 3-4 variants per asset, pick the best
6. **Document the prompts** — save the working prompt + style block for future regeneration
