---
name: image
description: Use whenever Kosta invokes /image or asks Hermes to generate, draw, create, mock up, render, or edit an image using the default Codex/GPT Image 2 path. This is the preferred default image-generation skill; use ComfyUI only when the user explicitly asks for local models, LoRAs, SDXL/Flux workflows, or advanced node/control workflows. Turns loose requests into strong GPT Image 2 prompts and calls Hermes image_generate.
version: 0.1.0
author: Hermes Agent
license: MIT
targets: [hermes-default, hermes-gpt, claude-hermes]
metadata:
  hermes:
    command_priority: 500
    tags: [image-generation, gpt-image-2, codex, image, prompt]
---

# Image — Codex GPT Image 2

Use this as Kosta's default image command. `/image <request>` means: understand the desired artifact, write a good GPT Image 2 prompt, then call Hermes' `image_generate` tool.

Do **not** route ordinary `/image` requests to ComfyUI. ComfyUI is for explicit local/LoRA/workflow requests. The default path is Codex/OpenAI GPT Image 2 through Hermes `image_generate`.

## First move

If the request is clear enough, generate immediately. Do not ask style questions unless the missing choice would materially change the result.

Use these defaults:

- General image: `square`
- Hero/banner/wide scene/UI desktop: `landscape`
- Phone wallpaper/poster/mobile UI/portrait: `portrait`
- Provider/model: whatever Hermes `image_generate` is configured to use, currently Codex GPT Image 2 medium

## Prompt structure

Rewrite the user request into a concise production prompt. GPT Image 2 responds best to structure, not keyword sludge.

Use this order when it helps:

```text
Create/draw/render [artifact type and intended use].

Scene / background:
[where it exists, environment, mood]

Subject:
[main subject, pose/action, scale, expression, important relationships]

Visual details:
[materials, textures, era, palette, realism/style, visible props]

Composition:
[framing, viewpoint, placement, negative space, orientation]

Lighting:
[soft window light, golden hour, studio, high contrast, etc.]

Exact text, if any:
"TEXT TO RENDER" — [font style, color, placement]. No other text.

Constraints:
[no watermark, no logos/trademarks, no extra text, preserve X, avoid Y]
```

Short requests do not need the whole template. A crisp paragraph is fine when it carries the same information.

## GPT Image 2 rules that matter

- Use action words: **create**, **draw**, **render**, or **edit**. For edits, say “edit the image by changing X” rather than vague “combine/merge.”
- For photorealism, include **photorealistic** or “real photograph / professional photography / iPhone photo.” Do not rely on “8K, ultra detailed, masterpiece” boilerplate.
- Be concrete about visual facts: materials, shape, texture, placement, lighting, camera angle, and mood.
- For text in the image, put exact copy in quotes, specify typography and placement, and say **verbatim, no extra text**. Spell unusual words letter-by-letter if accuracy matters.
- For edits or reference-based work, separate **Change** from **Preserve**. Example: “Change only the background to a rainy Tokyo street. Preserve the person’s face, pose, clothing, camera angle, lighting direction, and color grade.”
- Iterate with small changes. If the first result is close, ask for one targeted edit rather than rewriting everything.
- For dense charts/spreadsheets/tiny labels, warn that image generation is the wrong final-format tool; use real document/design tooling if precision matters.
- GPT Image 2 does not support transparent backgrounds in the current API path. If transparency is requested, generate on a plain high-contrast background or use post-processing unless the configured provider changes.

## Calling the tool

Call:

```python
image_generate(prompt=<final prompt>, aspect_ratio="landscape" | "square" | "portrait")
```

After generation, return the image directly. Add only a short note if useful, e.g. “I kept it square and optimized for product-shot realism.”

## When to use high-effort prompting

Use the full structured prompt for:

- UI mockups, screenshots, app screens, product concepts
- Posters, ads, packaging, logos/marks, thumbnails with text
- Infographics and diagrams
- Photorealistic product/people/scene images
- Edits where identity, geometry, layout, or brand feel must be preserved

For UI/UX images, also follow the `gpt-image-2-uiux-prompting` skill if available.

## Examples

User: `/image a slick product shot of a black ceramic mug for a coffee brand`

Tool prompt:
```text
Create a photorealistic studio product photograph for a premium coffee brand.

Subject: a matte black ceramic mug with a subtle curved handle, empty, centered on a warm stone surface.
Visual details: soft ceramic texture, tiny rim highlights, faint coffee-bean shadows nearby, no visible logo.
Composition: square crop, mug centered with tasteful negative space, eye-level product photography.
Lighting: soft warm key light from upper left, gentle fill, natural contact shadow.
Constraints: no text, no watermark, no fake brand logo, no extra objects except subtle coffee beans/shadows.
```

User: `/image mobile onboarding screen for a meditation app, calm but not generic`

Tool prompt:
```text
Generate one realistic iPhone portrait screenshot of a native iOS meditation app onboarding screen.

Product intent: help a new user choose a calming daily practice without feeling like a wellness cliché.
Screen state: first onboarding screen with a single hero illustration, short headline, one primary CTA, and small secondary sign-in link.
Layout: native iOS safe areas, SF Pro-like typography, generous spacing, bottom CTA above the home indicator.
Visual style: calm editorial UI, warm off-white background, muted sage and clay accents, subtle grain, no stock-photo look.
Exact visible text: headline "Find your quiet minute", CTA "Start", secondary link "Sign in". No other text.
Constraints: straight-on screenshot, normal iPhone proportions, no device mockup frame, no poster layout, no duplicate buttons, no fake logos, no watermark.
```

## References

- `references/gpt-image-2-prompting.md` — current GPT Image 2 prompt rules and constraints.
