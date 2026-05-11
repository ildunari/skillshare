# Troubleshooting GPT image prompts

## Contents

- [Triage sequence](#triage-sequence)
- [Common failures and fixes](#common-failures-and-fixes)
- [When to use the audit script](#when-to-use-the-audit-script)
- [Rewrite patterns](#rewrite-patterns)

## Triage sequence

1. Check whether the task asks image generation to do something deterministic: exact chart values, exact map geography, exact legal/medical claims, or final production typography. If so, create or verify the factual artifact outside the image model first.
2. Check whether the prompt conflicts with the model's capabilities or parameters, especially transparency, unsupported sizes, or too much exact text.
3. Reduce prompt scope. Fix one failure at a time using editing follow-ups instead of regenerating from scratch.
4. Increase quality when small text, layout, identity preservation, or dense diagrams are important.
5. Inspect the output manually. Text, labels, hands, product labels, charts, and fine factual content remain the most common places for errors.

## Common failures and fixes

### Fake transparent background or checkerboard pattern

Symptom: The image contains a checkerboard pattern or opaque background instead of real alpha transparency.

Fix: For `gpt-image-2`, do not promise true transparent backgrounds. Prompt for a plain solid background that can be removed later, or use a separate background-removal step. Avoid asking the model to show checkerboard transparency because it may draw the checkerboard as pixels.

```text
Use a plain matte white background with no shadows beyond the product contact shadow. Do not draw a checkerboard, alpha grid, or transparency preview.
```

### Text is misspelled or extra words appear

Fix: Reduce text quantity, quote exact copy, specify that it should appear once, use high quality, and inspect. For long body copy, generate the layout without body text and add text in a design tool.

```text
Render this exact headline once and verbatim: "[headline]". Do not add any other text, captions, watermarks, labels, or signatures.
```

### Chart values are wrong

Fix: Use code or a charting tool for the chart. Then use image generation for background, annotation style, or explanatory surrounding artwork while preserving the chart image.

```text
Preserve the supplied chart exactly: data positions, axis labels, tick marks, line colors, legend, and source note. Add only the surrounding editorial frame and headline.
```

### Scientific diagram is pretty but inaccurate

Fix: Supply the exact structures, flow direction, required labels, and prohibited confusers. Ask for a diagram, not a decorative illustration.

```text
This is an educational diagram. Show only [structures]. Use arrows only from [start] to [end]. Do not include [common inaccurate extra].
```

### Labels are too small

Fix: Use fewer labels, larger canvas, landscape orientation, high quality, and grouping. Replace long labels with numbered callouts if needed.

### Identity or character consistency drifts

Fix: Use the same reference image where available, lock stable features, and request one change at a time. For original characters, use a reference sheet prompt before requesting scenes.

```text
Preserve the character's face shape, hair silhouette, outfit colors, proportions, and accessories. Change only the background and lighting.
```

### Product labels or brand packaging drift

Fix: Use an edit workflow rather than pure generation. Explicitly preserve product geometry and label text. Do not ask the model to recreate a complex label from memory.

### Realistic images look like CGI

Fix: Ask for everyday photographic cues: real camera, ordinary imperfections, natural light, unpolished environment, plausible shadows. Avoid stacking `cinematic`, `8k`, `hyperreal`, and other gloss cues when realism is the goal.

### Image is too dark

Fix: State exposure and lighting directly.

```text
Bright, evenly exposed image with visible subject detail, soft window light, no crushed shadows, no underexposed background.
```

### Pixel art or sprites are blurry

Fix: Specify pixel-art constraints and extraction setup.

```text
Crisp pixel art, hard square pixels, no anti-aliasing, no blur, limited palette, dark 1-pixel outline, each sprite isolated in an equal grid cell.
```

### UI mockup is visually nice but unusable

Fix: Treat the prompt like a product spec: screen name, user goal, exact labels, component hierarchy, empty states, and accessibility.

```text
Use only these UI labels: [labels]. No lorem ipsum. Buttons should be readable. Primary action: [action].
```

### The model adds watermarks, signatures, random logos, or extra captions

Fix: Put the copy constraints near the end, because late constraints are often honored in final rendering details.

```text
Text constraints: no watermark, no signature, no random logos, no extra captions, no text beyond "[exact text]".
```

### Composition is wrong

Fix: Use concrete layout words and spatial anchors. For complex layouts, describe it as a grid, split panel, top/middle/bottom structure, or numbered zones.

### Too many styles are mixed

Fix: Choose a primary visual system and one accent. Stacking many aesthetics often creates muddled outputs.

### Prompt is long but still misses important details

Fix: Convert the prompt into labeled sections. Put exact content and preservation constraints in their own lines.

### User wants a famous character, logo, or living artist's exact style

Fix: Offer an original alternative that captures broad traits without copying protected material.

```text
Create an original cheerful sidekick character with rounded shapes, expressive eyes, bright primary colors, and family-friendly adventure energy.
```

### User wants medical, legal, or scientific claims in an image

Fix: Use source-supplied text only, cite or verify outside the image, and keep the image educational rather than advisory.

## When to use the audit script

Use `scripts/image_prompt_audit.py` before sending a prompt that has any of these traits:

- exact text, exact data, charts, or tables
- custom size or API parameters
- product, logo, UI, or infographic work
- transparent background requests
- many style references in one prompt
- prompt longer than roughly 350 words

## Rewrite patterns

### From vague to usable

Weak:

```text
Make a cool science infographic about photosynthesis.
```

Better:

```text
Goal: Create a portrait infographic for high-school students explaining photosynthesis.
Canvas: 1024x1536.
Structure: title, central leaf cross-section, 4 labeled inputs/outputs, 3-step process.
Exact text: "Photosynthesis" plus labels "sunlight", "water", "carbon dioxide", "glucose", "oxygen".
Style: clean textbook infographic, green and white palette, readable labels, simple arrows.
Constraints: no fake statistics, no tiny paragraphs, no extra labels.
```

### From conflicting to focused

Weak:

```text
Make it photorealistic, pixel art, watercolor, cyberpunk, minimalist, highly detailed, transparent, with lots of text.
```

Better:

```text
Create a minimalist cyberpunk poster: one photorealistic subject in neon rain, large negative space, one short headline. Use an opaque dark background.
```

### From impossible exact chart to safe workflow

Weak:

```text
Generate a beautiful stock chart showing this exact quarterly data.
```

Better:

```text
First render the exact stock chart with code from the supplied quarterly data. Then use image generation to create a polished finance-report cover that embeds the chart image unchanged.
```
