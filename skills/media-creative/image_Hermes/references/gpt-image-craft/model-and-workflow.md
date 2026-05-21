# Model and workflow reference

## Contents

- [When to use ChatGPT Images vs API](#when-to-use-chatgpt-images-vs-api)
- [Model choice](#model-choice)
- [Quality choice](#quality-choice)
- [Size and aspect ratio](#size-and-aspect-ratio)
- [Generation vs editing](#generation-vs-editing)
- [Responses API vs Image API](#responses-api-vs-image-api)
- [Output formats and transparency](#output-formats-and-transparency)
- [Streaming and partials](#streaming-and-partials)
- [Limitations to design around](#limitations-to-design-around)
- [When to use deterministic tools first](#when-to-use-deterministic-tools-first)
- [Provenance and metadata](#provenance-and-metadata)

## When to use ChatGPT Images vs API

Use ChatGPT Images for interactive ideation, user-facing creative work, prompt refinement, quick edits, and “I know it when I see it” exploration. It is excellent when the user wants you to collaborate visually.

Use the API when the user needs reproducible specs, batch generation, app integration, controlled parameters, saved prompts, logged outputs, or deterministic checks around resolution, quality, and cost.

Use “images with thinking” in ChatGPT when the image depends on reasoning, research, layout planning, multi-step source transformation, or complex educational/explanatory structure. It is not necessary for every simple prompt.

## Model choice

Recommended default: `gpt-image-2`.

Use it for customer-facing images, photorealism, structured visuals, text-heavy image work, editing-heavy workflows, reference-image workflows, scientific/educational visuals, and brand-sensitive assets where fewer retries are worth the extra quality.

Fallback choices:

- Use a faster or cheaper model only for high-volume rough drafts, preview thumbnails, or exploratory variants.
- Use a transparency-capable workflow/model for true alpha output if required. Do not force `background: transparent` on `gpt-image-2`.
- Preserve legacy prompts during migration first, then retune based on real output comparisons.

## Quality choice

- `low`: Fast drafts, mood exploration, thumbnails, simple stickers, early variants, large batches.
- `medium`: Default for finished prompts, product concepts, portraits, most marketing visuals.
- `high`: Dense labels, graphs, diagrams, UI mockups, small text, academic figures, exact copy, close-up realism, identity-sensitive edits, outputs intended for slides or print.
- `auto`: Reasonable when the caller does not need parameter control.

Cost/latency and quality move together. Make the first pass cheaper when the user wants many directions, then regenerate the chosen direction at higher quality.

## Size and aspect ratio

GPT Image 2 accepts flexible `WIDTHxHEIGHT` sizes when the dimensions satisfy current constraints. Useful sizes:

- `1024x1024`: square default, avatars, icons, thumbnails, simple compositions.
- `1536x1024`: landscape, slides, diagrams, charts, UI, wide scenes.
- `1024x1536`: portrait, posters, character sheets, mobile mockups, book covers.
- `2048x1152`: 16:9 detail pass, hero images, deck-style outputs.
- `2560x1440`: upper reliable 16:9 target for highly detailed work.
- Higher resolutions near 4K can be experimental and more variable.

Practical rules:

- Square is usually fastest and easiest for simple assets.
- Use landscape for charts, slides, dashboards, timelines, and process diagrams.
- Use portrait for posters, social stories, character sheets, app screens, and infographics.
- Use a target aspect ratio that matches the final destination. Cropping after generation can destroy composition and text.

## Generation vs editing

Use generation when creating a new image from text.

Use editing when the user provides reference images or wants to preserve identity, layout, product geometry, brand elements, pose, camera angle, room geometry, or an existing scene.

Editing prompts should separate locked elements from allowed changes:

```text
Preserve: face, identity, pose, camera angle, lighting, background, product label.
Change only: replace the jacket with the provided garment.
Integration: realistic fabric folds, shadows, color temperature, occlusion.
Do not add: new accessories, text, logos, watermarks, or new background elements.
```

For masks, describe the final image as a whole, not just the masked area. The model needs surrounding context to integrate the edit.

## Responses API vs Image API

Use Image API for one-shot image generation or one-shot edits. It is direct and parameter-centric.

Use Responses API when:

- the image is part of a multi-turn conversation;
- the user wants iterative image refinement;
- the model should decide whether to generate or edit;
- image outputs need to stay in context for follow-up prompts;
- the user wants prompt revision, reasoning, or tool orchestration around image generation.

When using a tool model with image generation, the model may revise the prompt. Preserve the original user intent and inspect revised prompts when exact text, scientific labels, or brand copy matter.

## Output formats and transparency

Common output formats:

- `png`: default, good for lossless detail and text-heavy outputs.
- `jpeg`: faster/smaller for photorealistic images where transparency is not needed.
- `webp`: useful for web delivery and compression workflows.

GPT Image 2 should be treated as not supporting true transparent backgrounds in the API at research time. For icon/sticker/sprite workflows:

1. Generate on a flat, high-contrast, opaque background.
2. Ask for a crisp silhouette with no shadows or glow unless needed.
3. Remove background with a deterministic editor/background-removal step.
4. Validate alpha after export rather than trusting a checkerboard-looking preview.

Avoid prompts like “transparent checkerboard background”; that often bakes the checkerboard into the image.

## Streaming and partials

Streaming partial images are useful for interactive applications, progress previews, and user-facing generation interfaces. They are not a substitute for final quality inspection. Partial images may arrive fewer times than requested if final generation completes quickly.

## Limitations to design around

Design prompts assuming these remain possible:

- Small text may still be wrong or poorly placed.
- Multi-line text can drift, duplicate, or invent characters.
- Recurring characters, logos, and brand elements may vary across generations.
- Structured layouts can misplace elements even when the prompt is clear.
- Exact charts and graphs can look plausible while being numerically wrong.
- Transparent backgrounds can be unreliable or unsupported depending on model and interface.
- Long prompts can create conflicts. Debug by changing one thing per follow-up.

## When to use deterministic tools first

Use code, design software, or source data first when the task requires:

- exact data values, axes, scales, formulas, or statistical interpretation;
- pixel-perfect UI for production implementation;
- print-ready typography with exact fonts and kerning;
- regulatory, medical, legal, or scientific accuracy;
- accessible charts with alt text and verifiable labels;
- reusable transparent sprite sheets with clean alpha.

Then use image generation for style exploration, hero imagery, visual metaphors, layout inspiration, or finished-looking mockups that will be inspected and corrected.

## Provenance and metadata

Generated images may include provenance metadata such as C2PA depending on the platform. Do not promise metadata removal. If the user asks about authenticity or provenance, explain that metadata can help certify origin/history but should not be the only verification method.
