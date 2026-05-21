# Codex/GPT Image 2 reference-conditioned chart redraw

Use when Kosta explicitly asks to use Codex/GPT Image 2 to clean up blurry chart images as visuals.

## Positioning

This is a model redraw, not a factual restoration. It can make a chart look dramatically cleaner, but the output must be checked for label/data drift before use in grants or papers.

## Direct Responses pattern

The bundled `image_generate` wrapper is convenient but only exposes coarse aspect ratios. For reference-conditioned chart redraws with an input image and high/custom size, use the Codex/OpenAI provider helpers directly and stream the Responses `image_generation` tool.

Important details:

- Use the Codex backend client from `plugins/image_gen/openai-codex/__init__.py` via `importlib.util` because the directory name contains a hyphen.
- The ChatGPT/Codex backend requires streaming (`Stream must be set to true` on non-stream create).
- Include the chart as `input_image` with `detail: original` when possible.
- `gpt-image-2` accepts custom sizes through the backend even though the local OpenAI SDK pydantic type warns about literals. Use dimensions divisible by 16 and within current limits; near-max landscape examples: `3840x2016`, `3840x2032`.
- The stream may produce partial images before final. Preserve the latest partial so a usable output can still be saved if the stream closes after partial delivery.

## Prompt skeleton

```text
Edit the provided blurry scientific chart into a clean, high-resolution native chart rendering suitable for an NIH grant figure.

Hard constraints:
- Preserve the same chart layout, same data relationships, same bar/line positions, same error bars, same colors, same axes, tick marks, labels, legends, annotations, and spacing from the source image.
- Do not redesign, add new text, remove text, rename labels, change values, change colors, change panel layout, change bar heights, change error bars, or invent missing data.

Change only visual quality:
- Remove blur, JPEG artifacts, softness, tilt, uneven antialiasing, and compression noise.
- Re-render as if exported directly from scientific plotting software: flat, straight-on, orthographic, clean white background.
- Make all visible text, bars/lines/points, axes, ticks, legends, annotations, and error bars crisp and professionally typeset.
- No shadows, no perspective, no artistic style, no extra marks. Render visible text once, as faithfully as possible.
```

## Verification before sending

- Confirm output dimensions with PIL or `file`.
- Make a comparison contact sheet against the original.
- Tell Kosta plainly that it is a model redraw and needs visual checking for labels, bar heights, and error bars.
