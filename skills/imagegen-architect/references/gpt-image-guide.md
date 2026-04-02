# GPT Image 1.5 — Prompt Engineering Guide

> Target: ChatGPT native image generation (GPT-4o image gen) and `gpt-image-1` / `gpt-image-1.5` API models.
> DALL-E 3 is being discontinued May 12, 2026. All new work should target GPT Image 1.5.

## Model Profile

| Dimension | Value |
|---|---|
| **Speed** | 3-8 seconds per image |
| **Text rendering** | Excellent — legible paragraphs, labels, UI text |
| **Artistic range** | Broadest of the three — photorealism through stylized illustration |
| **Prompt style** | Natural prose paragraphs, not keyword lists |
| **Max useful prompt** | ~200 words before coherence degrades |
| **Aspect ratios** | 1:1, 16:9 (native), 9:16, 4:3, 3:4 |
| **Consistency mechanism** | Session memory + reference image upload |
| **API model strings** | `gpt-image-1` (production), `gpt-image-1-mini` (cost-effective) |

## Prompt Structure

GPT Image 1.5 is a conversational model. Write prompts as **descriptive paragraphs**, not comma-separated keywords. The model responds to creative-director-style briefs.

### Optimal Element Order

```
[Subject/main element] + [Action/state] + [Environment/setting] +
[Lighting/mood] + [Camera/composition] + [Style reference] +
[Technical specs] + [Exclusions]
```

### The Four High-Impact Elements

1. **Style and mood** — "cinematic" vs "editorial" vs "documentary" produce completely different visual languages
2. **Composition and detail** — Specific spatial relationships, clothing, colors reduce generic output
3. **Technical references** — Camera terms ("85mm lens," "f/1.4," "shallow depth of field") carry implied visual information
4. **Lighting and atmosphere** — "Soft diffuse" vs "golden hour" vs "high-contrast" fundamentally shape output

## Text Rendering

GPT Image 1.5's strongest competitive feature. Use it for:
- UI mockups with readable buttons, labels, navigation
- Infographics with legible data
- Marketing materials with headlines and body copy
- Banners and social media assets with text overlay

**Best practices for text:**
- Keep text to clear, short strings for best legibility
- Specify font style: "clean sans-serif," "bold condensed," "monospace"
- Specify alignment: "center-aligned header," "left-aligned body text"
- Use ALL-CAPS for buttons and emphasized labels
- Include padding/margin instructions: "ensure all text fits with comfortable padding"

**Known text issues:**
- Slight font inconsistency across sections — keep same session, repeat style description
- Non-Latin character sets render poorly
- Dense text can overflow — explicitly state margins

## Color Control

| Method | Reliability | Example |
|---|---|---|
| Descriptive name + hex backup | Best | "sapphire blue (#0F52BA)" |
| Descriptive name only | Good | "warm coral" |
| Hex code only | Weak | "#FF6B35" (model may drift) |
| Reference image | Strongest | Upload a palette swatch alongside prompt |

Always use descriptive color names as the primary method, with hex codes as parenthetical advisory backup.

## Style Consistency Across Generations

### Session Memory Strategy
Stay in the **same ChatGPT chat session** for all related generations. The model maintains visual context within a conversation — switching chats resets everything.

### Character/Component DNA Template
Create a reusable reference block:

```
Visual DNA:
- Primary identifiers: [core shapes, distinctive features, silhouette]
- Secondary identifiers: [color palette, material/texture, recurring elements]
- Tertiary elements: [background style, lighting preference, mood]
- Artistic style: [medium, technique, color treatment]
```

### Reference Image Workflow
For highest consistency:
1. Generate one "anchor" image that defines the style
2. Upload it alongside all subsequent prompts
3. Instruct: "Use this image as the style reference. Maintain the same visual treatment, proportions, and rendering. Apply only the changes described below."

### Multi-Image Series Pattern
```
Prompt 1: [Full style description + first subject]
Prompt 2: "Using the same style as the previous image, now show [variant]"
Prompt 3: "Same style. Now [next variant]"
```

## Anti-Rewrite Wrapper

ChatGPT internally rewrites prompts before generating. Usually this helps, but if the model keeps adding unwanted elements, prepend:

```
I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:
```

Use sparingly — only when the model is fighting your intent.

## UI/UX Asset Strengths

GPT Image 1.5 excels at:
- **Pixel-perfect UI mockups** — dashboard layouts, mobile screens, landing pages
- **Text-heavy assets** — infographics, banners, labeled diagrams
- **Stylized illustrations** — bold concept art, editorial illustrations, character design
- **Marketing collateral** — social media cards, ad creatives, thumbnails

Structure UI prompts with:
- Content type ("mobile app dashboard," "landing page hero")
- Technical requirements (device type, dimensions)
- Visual hierarchy (primary action, secondary elements)
- Color palette (hex codes for brand colors)
- Text elements (specific copy, button labels)
- Layout style ("minimal," "data-dense," "spacious")

## JSON-Based Structured Prompts (API/Programmatic Use)

For batch generation or programmatic workflows, structure as JSON then serialize:

```json
{
  "aspect_ratio": "16:9",
  "subject": {
    "primary": "modern dashboard interface",
    "secondary_elements": ["charts", "metrics cards", "navigation"]
  },
  "style": {
    "aesthetic": "minimalist",
    "color_palette": {"primary": "#2563EB", "accent": "#10B981"},
    "typography": "sans-serif, clean"
  },
  "lighting": "soft, professional",
  "quality": "high-detail, crisp text, professional"
}
```

## Known Limitations & Workarounds

| Limitation | Workaround |
|---|---|
| Complex multi-element scenes | Break into stages — generate base, then iterate conversationally |
| Non-Latin text | Stick to Latin characters or use stylized symbols |
| Inconsistent letter rendering | Same session, identical style descriptions, exact hex codes |
| Image cropping (tall formats) | Specify "include padding," prefer landscape/square over portrait |
| Text overflow | State margins, padding, "ensure all text fits" explicitly |
| Same prompt → different results | Upload reference image for anchoring |
| Hands/anatomy | Crop out of frame, describe generically ("relaxed at sides"), or regenerate |

## Rate Limits (as of early 2026)

- **ChatGPT Free:** 2-3 images/day
- **ChatGPT Plus/Pro:** Significantly higher (varies by plan)
- **API:** Per-account rate limits; use `gpt-image-1-mini` for cost efficiency during iteration

## Quick Reference: Prompt Checklist

Before finalizing any GPT Image 1.5 prompt:
- [ ] Written as natural prose, not keyword list
- [ ] Most important visual element appears first
- [ ] Aspect ratio specified early
- [ ] Colors use descriptive names + hex backup
- [ ] Lighting and mood explicitly stated
- [ ] Exclusions at the end ("No text, no watermark" etc.)
- [ ] Under 200 words
- [ ] If part of a series: reference image workflow planned
