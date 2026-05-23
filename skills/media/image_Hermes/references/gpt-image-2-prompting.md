# GPT Image 2 prompting notes

Sources checked April 2026:

- OpenAI Developers Cookbook: GPT Image Generation Models Prompting Guide
  - https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- OpenAI API docs: image generation tool
  - https://platform.openai.com/docs/guides/tools-image-generation/
- OpenAI Academy: Creating images with ChatGPT
  - https://openai.com/academy/image-generation

## Model/path facts

- `gpt-image-2` is OpenAI's recommended default for new image workflows.
- In Hermes, the default generation tool is `image_generate`; it is configured separately to use the Codex/OpenAI provider.
- With the Responses/image-generation tool path, a mainline model can revise the prompt before image generation.
- `gpt-image-2` has quality tiers `low`, `medium`, `high`; Hermes' current `image_generate` schema may not expose those directly, so model/quality is controlled by config, not the skill body.
- `gpt-image-2` does not currently support transparent background requests. Generate on a plain background or post-process transparency.
- `input_fidelity` should be omitted for `gpt-image-2`; the model treats image inputs as high fidelity by default.

## Prompt anatomy

The most reliable structure is:

1. Intended artifact/use: photo, ad, UI screenshot, poster, infographic, product render, icon, etc.
2. Scene/background: where the image exists.
3. Subject: main object/person/action, scale, pose, expression.
4. Key details: materials, textures, visible props, palette, style.
5. Composition: framing, viewpoint, placement, negative space, aspect orientation.
6. Lighting: direction, quality, mood.
7. Literal text: exact quoted copy, typography, placement.
8. Constraints: what not to add, what must be preserved, no watermark/logos/extra text.

Use short labeled blocks for complex prompts. Use a short paragraph for simple requests.

## Best practices

- Prefer clear visual facts over generic quality words.
- For photorealism, say `photorealistic` directly. Camera/lens terms steer style loosely, not exact physics.
- For text, quote exact strings, specify font style/weight/color/placement, keep text short, and say `verbatim` / `no extra text`.
- For unusual words or brand-like strings, spell them letter by letter.
- For edits, always split: `Change:` and `Preserve:`. Repeat preserve constraints on each iteration.
- For multi-image/reference work, name inputs by order: “Image 1 is the subject; Image 2 is the style reference.” Then state exactly what transfers and what stays fixed.
- For UI screenshots, ask for a realistic shipped product screenshot, not a concept poster. Specify safe areas, hierarchy, exact labels, and no duplicate controls.
- For dense infographics, keep the number of labels modest. If precision matters, generate a design direction and rebuild final text/charts in real design/document tools.
- Iterate with one change at a time after a decent base image.

## Anti-patterns

Avoid relying on:

- `8K`, `ultra detailed`, `masterpiece`, `award winning`, keyword soup
- vague style words without visual details: `beautiful`, `modern`, `sleek`
- huge walls of requirements with conflicting constraints
- asking for lots of exact small text in one image
- “merge these images” when you mean “edit image 1 by adding element from image 2”
- transparent backgrounds with `gpt-image-2`

## Aspect ratio mapping for Hermes

Hermes `image_generate` currently exposes only:

- `landscape` — wide hero images, desktop UI, banners, cinematic scenes
- `portrait` — phone UI, posters, wallpapers, vertical social assets
- `square` — product shots, icons, avatars, general standalone images

Pick one and mention any important crop/framing constraints in the prompt.
