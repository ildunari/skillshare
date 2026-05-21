# Prompt framework

## Contents

- [The visual brief stack](#the-visual-brief-stack)
- [Prompt forms](#prompt-forms)
- [Visual control levers](#visual-control-levers)
- [Exact text and typography](#exact-text-and-typography)
- [Reference image prompting](#reference-image-prompting)
- [Iteration tactics](#iteration-tactics)
- [Prompt critique checklist](#prompt-critique-checklist)
- [Common prompt rewrites](#common-prompt-rewrites)

## The visual brief stack

A strong image prompt answers these questions before adding style flourishes:

1. What is the asset? Example: textbook diagram, product ad, sprite sheet, cinematic portrait.
2. Who is it for? Example: high-school students, executives, mobile gamers, shoppers.
3. Where will it be used? Example: slide, poster, mobile UI, thumbnail, print handout.
4. What must be present? Exact subject, labels, copy, data, poses, products, references.
5. What must not change? Identity, composition, layout, product label, style, background.
6. What visual system should govern it? Medium, palette, typography, camera, lighting, texture.
7. How should success be judged? Readability, realism, brand fit, pixel clarity, factual accuracy.

Write prompts in this order when complexity is high:

```text
Goal:
Audience:
Canvas:
Subject:
Style system:
Composition:
Required content:
Constraints:
Quality bar:
```

## Prompt forms

### Minimal prompt

Good for casual images and ideation.

```text
A cozy watercolor illustration of a fox librarian organizing glowing books in a moonlit forest library, warm palette, gentle children's book mood.
```

### Descriptive paragraph

Good for photorealism, editorial art, and concept scenes.

```text
Create a photorealistic candid 35mm film photograph of an elderly sailor repairing a net on a small fishing boat at soft dawn light. Weathered hands, worn wood, sea mist, muted colors, shallow depth of field. The image should feel honest and unposed, not glamorous or cinematic.
```

### Labeled segments

Best for diagrams, UI, exact text, ads, sprites, edits, and structured layouts.

```text
Goal: one landscape slide for a fundraising deck.
Title text: "Market Opportunity"
Layout: left headline, right TAM/SAM/SOM diagram, bottom growth bar chart.
Style: clean white background, modern sans-serif, generous spacing.
Constraints: no stock photos, no decorative clutter, all text readable.
```

### JSON-like spec

Best for API pipelines and systems that assemble prompts.

```text
{
  "deliverable": "mobile app UI mockup",
  "audience": "busy parents",
  "canvas": "1024x1536 portrait",
  "style": "practical, polished, white background, soft accent color",
  "required_elements": ["header", "task cards", "calendar strip", "progress widget"],
  "constraints": ["no lorem ipsum", "no decorative clutter"]
}
```

### Shot list

Best for cinematic, storyboard, multi-panel comic, animation breakdown, or product sequences.

```text
Panel 1: establishing shot, rainy train platform, character alone under yellow light.
Panel 2: close-up of hand holding torn ticket.
Panel 3: wide shot as train arrives, reflections on wet ground.
Panel 4: final quiet moment, character steps forward, hopeful expression.
```

## Visual control levers

Use only the levers that matter for the task.

- Medium: photorealistic photo, vector illustration, watercolor, ink, pixel art, 3D render, collage.
- Composition: centered product, rule of thirds, grid, cutaway, layered infographic, isometric, close-up.
- Camera: eye-level, overhead, macro, 50mm look, wide establishing shot, candid phone photo.
- Lighting: soft daylight, studio softbox, overcast, flash snapshot, rim light, ambient interior.
- Material: paper fiber, brushed metal, glass refraction, plastic blister packaging, fabric weave.
- Typography: bold sans-serif, editorial serif, high-contrast labels, handwritten notes, monospaced UI.
- Palette: muted earth tones, medical blues, neon cyberpunk, grayscale, limited 16-color palette.
- Texture: film grain, risograph dot texture, pencil lines, clean flat vector, tactile clay.
- Constraints: no extra text, preserve label, avoid tiny text, no watermark, no extra objects.

## Exact text and typography

Text-in-image works best when treated like a production requirement:

```text
Exact text, render once and verbatim: "Fresh and clean"
Typography: bold sans-serif, high contrast, centered, clean kerning.
Do not add, translate, rephrase, duplicate, or stylize the words beyond the requested font style.
```

Use high quality for dense text. Keep text short. For multi-line copy, specify line breaks and hierarchy:

```text
Headline: "Build once. Ship everywhere."
Subhead: "A visual systems kit for product teams."
Footer: "Beta opens June 12"
```

For multilingual text, provide exact script and language, then request preservation of layout and no invented characters. Inspect output carefully.

## Reference image prompting

When editing or using references, specify roles:

```text
Image 1: preserve the person's identity, pose, camera angle, and lighting.
Image 2: use only as clothing reference.
Change: replace jacket with the garment from Image 2.
Integration: realistic fit, folds, shadows, and occlusion.
Do not change: face, body shape, background, expression, hairstyle, product label.
```

For style transfer:

```text
Use the reference image only for palette, line quality, texture, and composition rhythm. Generate a new original subject. Do not copy characters, logos, text, or distinctive protected elements.
```

For product composites:

```text
Preserve product geometry and label legibility exactly. Use reference items as source objects, not as loose inspiration.
```

## Iteration tactics

Change one thing per follow-up whenever possible:

- “Make the lighting warmer while keeping the same composition.”
- “Remove the extra subtitle; keep only the headline.”
- “Make labels larger and reduce decorative background detail.”
- “Restore the original face and only change the jacket.”
- “Keep the same sprite grid, but make each pose more readable at 32x32.”

Use an audit pass after generation:

1. Check exact text and labels.
2. Check subject count and placement.
3. Check factual/data correctness.
4. Check identity/product consistency.
5. Check background/alpha/export requirements.
6. Decide whether to refine prompt, edit image, or use deterministic post-processing.

## Prompt critique checklist

A prompt is likely under-specified if it lacks:

- deliverable type;
- audience/context;
- aspect ratio or canvas;
- required objects/text/data;
- style system;
- constraints for what to avoid or preserve.

A prompt is likely over-specified if it includes:

- many conflicting styles;
- exact camera physics that are not important;
- long mood adjectives but no layout;
- too much in-image text;
- multiple unrelated deliverables in one image;
- living artist or protected-character dependence instead of visual traits.

## Common prompt rewrites

Weak:

```text
Make a cool science infographic about mitochondria.
```

Stronger:

```text
Create a clean textbook infographic for high-school biology students explaining mitochondria as the cell's energy-conversion organelle. Use a white background, flat scientific icons, readable labels, and three labeled zones: outer membrane, inner membrane/cristae, matrix. Include arrows showing glucose and oxygen inputs and ATP, CO2, and H2O outputs. Avoid tiny text, extra organelles, and decorative clutter.
```

Weak:

```text
Make it realistic.
```

Stronger:

```text
Make it photorealistic, as if captured with a real camera in soft natural daylight. Preserve the same composition and subject placement, add believable surface texture and contact shadows, and avoid cinematic color grading or glossy retouching.
```

Weak:

```text
Make a sprite.
```

Stronger:

```text
Create a 4x4 pixel-art sprite sheet for an original forest courier character, each cell containing one centered 32-bit pixel sprite pose, crisp silhouette, limited palette, dark 1-pixel outline, no anti-aliasing, no text, plain solid background for later extraction.
```
