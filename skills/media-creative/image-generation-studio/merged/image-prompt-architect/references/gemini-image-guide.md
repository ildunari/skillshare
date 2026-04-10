# Gemini Image Generation — Prompt Engineering Guide

> Target: Google Gemini image generation models — **Nano Banana Pro** (Gemini 2.5 Flash Image / Gemini 3 Pro Image) and **Nano Banana 2** (Gemini 3.1 Flash Image). Also applies to Imagen 3 via Vertex AI.

## Model Profiles

| Dimension | Nano Banana 2 (3.1 Flash) | Nano Banana Pro (3 Pro) |
|---|---|---|
| **Speed** | Fastest (3-4 sec) | Fast (5-8 sec) |
| **Text rendering** | Excellent — strongest of all models | Excellent |
| **Photorealism** | Very strong | Best-in-class |
| **Reference images** | Up to 5 | Up to 14 |
| **Character consistency** | Up to 5 characters | Up to 5 characters |
| **Prompt style** | Narrative paragraphs | Narrative paragraphs |
| **Max useful prompt** | ~130 words | ~130 words |
| **Best for** | Fast iteration, icons, text-heavy, UI | Professional assets, photorealism, complex scenes |

## Core Prompting Principle

**Describe scenes as narratives, not keyword lists.** A detailed paragraph outperforms a comma-separated list of attributes every time.

### Optimal Prompt Structure

```
[Subject] + [Action/state] + [Environment/setting] +
[Style descriptor] + [Camera angle + lens + lighting] +
[Technical specs] + [Exclusions]
```

### Be a Cinematographer

Gemini responds exceptionally well to photography/cinema language:
- **Camera angle:** wide-angle, macro, low-angle, Dutch angle, overhead, eye-level
- **Lens type:** 85mm (portrait), 35mm (environmental), 50mm (standard), 200mm (telephoto compression)
- **Lighting:** soft key, harsh directional, three-point, rim lighting, backlighting, diffuse overcast
- **Time/mood:** golden hour, blue hour, harsh noon, twilight, overcast, studio

## Text Rendering (Gemini's Competitive Advantage)

Gemini's text rendering is the strongest across all current models. Capitalize on this for:
- Posters, invitations, social media assets
- Infographics, menus, diagrams
- Product mockups with labels
- UI mockups with readable navigation and buttons

**Best practices:**
- Keep text to 25 characters or less per line for optimal clarity
- Specify font style descriptively ("clean sans-serif," "bold display")
- Test 2-3 distinct text phrases to find optimal rendering
- Printed text is far more reliable than handwritten text

## Color Control

Image gen models do NOT reliably follow hex codes. Use the strongest method available:

| Priority | Method | When to Use |
|---|---|---|
| **A (best)** | Upload a palette swatch reference image (4-6 flat color blocks) | Always, if you can make the swatch |
| **B** | Upload an existing image as style/color reference | When matching an existing look |
| **C** | Descriptive color names + "limited palette of 5-6 hues total" | When no reference images available |
| **D (weakest)** | Hex codes as advisory hints in parentheses | As backup alongside names, never sole method |

For palette drift: generate first, then use **spot-color edit prompts** to correct individual colors without regenerating from scratch. This is a Gemini strength.

## Conversational Editing (Key Differentiator)

Gemini excels at iterative refinement. If an image is 80% correct, **don't regenerate from scratch** — ask for the specific change:

### Edit Prompt Template
```
Using the provided image, change only [specific element] to [new description].
Keep everything else exactly the same — same style, lighting, composition, and proportions.
Do not change the aspect ratio.
```

### Example Edit Prompts
```
Using the provided image, change only the background color to dark navy. Keep everything else exactly the same.
```
```
Using the provided image, change only the left icon to a settings gear. Keep everything else exactly the same.
```
```
Using the provided image, make the accent color amber-orange instead of blue. Keep everything else exactly the same.
```

### Doodle Edits
Gemini supports drawing/marking directly on images to target spatial edits. Circle the area you want changed and describe the modification. Often more precise than text-only editing for spatial changes.

## Multi-Reference Image Blending

Gemini handles multiple reference images well:
1. Upload 2-5 reference images (keep them thematically related)
2. Assign roles explicitly: "Use Image 1 for the composition, Image 2 for the color palette, Image 3 for the lighting style"
3. Include character names if faces are involved

## Character Consistency Strategy

1. Generate one reference image with detailed character description
2. Name the character explicitly in all subsequent prompts
3. Upload the reference as an input image for each generation
4. Generate multiple iterations if consistency drifts — manually pick best
5. Prefer iterative editing over regeneration for consistency

For multi-character scenes: upload separate references, assign distinct names, and Nano Banana 2 maintains up to 5 characters' consistency.

## UI/UX Asset Strengths

Gemini excels at:
- **Clean geometric icons** — flat design, minimalist line art, consistent stroke
- **Flat illustrations** — limited palette, no gradients, SVG-ready output
- **Product mockups** — photorealistic with excellent detail
- **Text-heavy assets** — strongest text rendering across models
- **Fast iteration** — 3-4 second generation for rapid design exploration

### Flat Design / SVG-Ready Prompt Recipe
1. Specify geometric simplicity: "minimalist line art," "flat design," "no shading"
2. Limit color palette: "3-color palette: [color1], [color2], [color3]"
3. Specify stroke details: "2px stroke width, no fill, rounded line caps"
4. Name specific elements: "house icon with simple roof, door, and one window"

### Example SVG-Ready Prompt
```
Minimalist line-art house icon. Flat design style. Geometric shapes only.
Rectangular base, triangular roof, square door centered, two small square windows.
2px stroke, dark charcoal color, no fill. Square 256px canvas, centered composition.
No shadows, no texture, no gradients. Clean edges for vector conversion.
```

## Known Limitations & Workarounds

| Limitation | Workaround |
|---|---|
| Hands/complex anatomy | Crop hands, use gloves/mittens, describe generically |
| Dense prompt causes hallucination | Split into multi-step: generate base, edit conversationally |
| Very small text (<12pt equiv) | Use larger text, specify "button label reads..." context |
| Multi-angle consistency | Generate each angle separately with reference image |
| Complex edits → artifacts | Prefer simple, atomic changes; regenerate if drift is too far |

## Rate Limits (as of early 2026)

- **Gemini App:** ~100 images/day (resets daily)
- **Developer API:** ~500 requests/day (resets midnight PT)
- **AI Studio:** ~500-1000/day
- Use all three platforms for maximum free-tier throughput
- Exponential backoff for 429 errors: 2s → 4s → 8s → 16s

## Quick Reference: Prompt Checklist

Before finalizing any Gemini prompt:
- [ ] Written as narrative prose, not keyword list
- [ ] Camera/lens/lighting terminology included for photorealism
- [ ] Under 130 words
- [ ] Colors use descriptive names (hex as advisory backup only)
- [ ] "No text" included explicitly if text is unwanted
- [ ] If part of a series: reference image upload planned
- [ ] Edit prompts prepared for post-generation refinement
- [ ] If flat design: geometric constraints and palette limits specified
