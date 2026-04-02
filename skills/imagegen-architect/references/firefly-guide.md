# Adobe Firefly Image Model 4 — Prompt Engineering Guide

> Target: Adobe Firefly Image Model 4 and Image Model 4 Ultra in the web Text-to-Image experience. Also applicable to Firefly within Photoshop/Illustrator generative fill.

## Model Profiles

| Dimension | Image Model 4 | Image Model 4 Ultra |
|---|---|---|
| **Best for** | Illustrations, icons, objects, single-subject portraits, animals | Photoreal scenes, human portraits, medium groups |
| **Speed** | Fast | Moderate |
| **Text rendering** | Improving, may need iterations | Better, still benefits from iteration |
| **Commercial safety** | Trained on licensed content — safe for commercial use | Same |
| **Unique controls** | Visual Intensity slider, Effects presets, Style/Composition references | Same |
| **Prompt style** | Structured formula, single deliverable | Same |

## Core Differentiator: Commercial Safety

Firefly is trained exclusively on Adobe Stock, openly licensed content, and public domain material. This makes it the safest choice for commercial work where IP concerns matter — marketing materials, client deliverables, brand assets. Other models (GPT, Gemini, Grok) have less clear training data provenance.

## Prompt Construction Formula

Follow this order, including elements as relevant:

```
[Subject] [Action] [Angle] [Lighting] [Background] [Color palette] [Style] [Image type]
```

Optionally add: camera/lens/tech cues (focal length, f-stop, shutter/ISO), texture, materials, environment physics.

### Element Breakdown

**Subject & scene:** Who/what, where/when, key attributes, pose/action, focal prominence. Prefer one clear focal subject — Firefly handles single subjects best.

**Composition & perspective:** Shot type (macro/close/medium/long), angle (eye/low/high/overhead), framing (centered/rule-of-thirds), depth/focus. Specify figure-to-frame ratio.

**Lighting & mood:** Time (golden hour/blue hour/night/studio), quality (soft/hard/rim/backlight/volumetric), shadow behavior, atmosphere (cinematic/airy/moody/editorial).

**Medium & style:** Photorealism, illustration, watercolor, ink, oil, pastel, 3D render, cel-shade, graphic poster. Describe generically — no named artists. Align with chosen Effect if present.

**Color & palette:** Warm/cool, muted/vibrant, mono/duotone. Include brand hex codes if provided. Ensure contrast for text legibility.

**On-image text:** Quote exact strings. Specify font character (geometric sans, flowing script), placement, contrast, hierarchy. Keep text concise.

**Background:** Environmental vs studio (paper sweep, cyclorama). Avoid clutter competing with text/subject.

**Negatives:** List unwanted elements (extra digits, warped text, lens flare, busy background, posterization).

## Firefly-Specific Controls

### Visual Intensity
A slider from snapshot-like (left) to stylized/tuned (right). Multiple stops between.

| Setting | When to Use |
|---|---|
| Low (left) | Reportage, naturalism, documentary feel |
| Mid (default) | General use, balanced output |
| High (right) | Glamorized product shots, editorial illustration, stylized portraits |

### Effects (Style Presets)
If the user names an Effect, echo that aesthetic in your prompt wording:
- **Minimalism/Scandinavian/Simple:** "clean lines, soft daylight, natural materials, uncluttered layout"
- **Cinematic/Film Noir:** "dramatic lighting, high contrast, deep shadows, filmic grain"
- **Watercolor/Impressionist:** "soft edges, visible brushwork, diffuse colors, painterly quality"

### Style References
When the user provides a style reference image, keep descriptors consistent with it. Don't contradict a cartoon Effect with "photorealistic" or vice versa.

### Composition References
Keep spatial language consistent with provided composition references (subject scale/placement, horizon, leading lines).

## Model Routing (Internal Decision)

- **Use Image Model 4** for: speed, illustrations, icons, basic objects, single-subject portraits, individual animals
- **Route to Image Model 4 Ultra** for: photoreal scenes, human portraits, medium groups where realism/precision is critical

## Iteration Strategy

Firefly works best with staged complexity:

```
v1: Core composition — subject, framing, lighting, style
v2: Add props, texture, effects
v3: Refine text, details, color grading
```

Don't pack everything into v1. Generate the base, then refine. Use "Generate similar" for variations, then Remix for targeted changes.

## Prompt Templates

### Product Packshot
```
High-res product photo of [item: material/finish/features] on [surface texture],
lit by [key softbox angle + fill + rim]. Shot [angle] on [lens], heroing [feature].
Real reflections/grounded shadow. Background [gradient/solid/context].
Post grade [treatment]. Aspect [ratio].
```

### Minimalist / Negative Space
```
Place [simplified subject] in [lower-third/top-right]; [X%] negative space
in [color/texture] for [mood]. [Directional light] casts [shadow].
Subject size [relative]. Balance [asymmetric/centered]. Aspect [ratio].
```

### Text/Logo on Image
```
Render '[exact text, ≤5 words]' in [font style/weight]; treatment [flat/gradient/texture/metallic].
Follow surface contours/perspective if applied. Integration [embossed/engraved/printed/projected].
High contrast; position [region].
```

### Poster with Heavy Text
```
Graphic poster for [event/product]; bold title "[TEXT]" centered, subtitle and date at bottom.
Grid-aligned layout with clear hierarchy. [Palette] palette, high contrast.
[Background scene/pattern]. Clean [style] style. Ensure crisp edges and legible lettering.
Avoid texture noise and lens effects.
```

### Architecture / Interior
```
[Lighting condition] [room/building type] with [architectural details] and [furnishing/materials].
[Shot type] from [vantage point] at [angle]. [Lighting quality] with [bounce/reflection].
Photoreal editorial style. [Floor/surface] with [reflection detail].
Balanced composition with [visual flow]. Uncluttered. Avoid [artifacts].
```

## Known Limitations

| Limitation | Workaround |
|---|---|
| Complex multi-subject scenes | Stage across iterations; one focal subject per v1 |
| Dense typography | Shorter wording, larger type, higher contrast, plainer backdrop |
| Groups of people | Route to Ultra; keep groups small (3-5) |
| Named artists/styles | Describe generically; use Effects presets instead |
| Complex text rendering | Iterate; simplify on failure; restate exact casing/placement |

## Quick Reference: Prompt Checklist

Before finalizing any Firefly prompt:
- [ ] Follows [Subject][Action][Angle][Lighting][Background][Palette][Style] formula
- [ ] Single clear focal subject (for v1)
- [ ] Under 150 words
- [ ] Negatives listed at end
- [ ] If text on image: exact string quoted, placement and contrast specified
- [ ] Style language consistent with any chosen Effect/reference
- [ ] No named artists — generic style descriptions only
- [ ] Model routed correctly (Model 4 vs Ultra)
