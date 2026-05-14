---
name: qwen-image-prompting
description: Load when creating or repairing Qwen-Image/Qwen-Image-2512 prompts, ComfyUI workflows, PPT/poster/infographic/textbook figures, charts, labels, legends, academic visuals, or text-heavy generated images. Use for Kosta's GamingPC full Qwen+CacheDiT lane and for deciding when Lightning is draft-only.
metadata:
  targets:
    - claude
    - codex
    - hermes-default
    - hermes-gpt
    - claude-hermes
    - cursor
    - gemini
    - droid
---

# Qwen-Image Prompting

Use this for Qwen-Image and Qwen-Image-2512, especially on Kosta's GamingPC ComfyUI setup for school, study, paper, poster, PDF, slide, chart, infographic, and textbook-style visuals.

## Default lane on Kosta's GamingPC

Use **full Qwen-Image-2512 FP8 + CacheDiT** for final text-heavy visuals. Use **Lightning 4-step LoRA only for draft candidates**, because local stress-test visual QA showed valid images but garbled dense titles/legends.

Known GamingPC files:

- ComfyUI root: `C:\Users\kosta\AIProjects\ComfyUI`
- Health script: `scripts\health-comfyui.ps1`
- Stress script: `scripts\stress-qwen-comfyui.ps1`
- Diffusion: `models\diffusion_models\qwen_image_2512_fp8_e4m3fn.safetensors`
- Text encoder: `models\text_encoders\qwen_2.5_vl_7b_fp8_scaled.safetensors`
- VAE: `models\vae\qwen_image_vae.safetensors`
- Draft LoRA: `models\loras\Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors`
- CacheDiT node: `CacheDiT_Model_Optimizer`; use model type `Qwen-Image`, warmup `5`, skip interval `3` for 50-step jobs.

## Prompt as a layout spec, not a vibe

For text-heavy images, write the prompt like a design brief with exact quoted text:

```text
Create a [16:9 PowerPoint slide / academic poster / textbook figure / infographic / chart] in [style].
Canvas/layout: [grid, columns, rows, hierarchy, margins].
Title text: "[exact title]"; location: [top center/etc.]; style: [bold sans-serif/etc.].
Section 1: [visual object], label "[exact label]", caption "[exact caption]".
Arrows/flow: [direction, labels, colors].
Legend: [exact legend entries].
Axes/chart labels: x-axis "[exact]", y-axis "[exact]", tick labels "[...]", units "[...]".
Use clean spacing, high contrast, readable typography, aligned margins.
No additional text beyond the quoted text.
```

Every visible word should be quoted exactly. Avoid “some labels,” “a legend,” “a list,” or “a chart” without giving the exact labels/numbers.

## Strong defaults for academic visuals

Use these phrases when appropriate:

- `clean textbook figure`, `PowerPoint lecture slide`, `white background`, `vector-like flat colors`, `thin consistent strokes`, `crisp readable labels`, `high contrast`, `generous margins`, `no extra text`
- For diagrams: specify panels, object positions, arrow direction, callout labels, legend entries, and what each color means.
- For charts: specify chart type, axes, units, tick labels, legend, colors, and whether values must be schematic or data-accurate.
- For posters/PDFs: split dense content into multiple figures/slides; do not ask one image to hold a full page of tiny text.

## Negative prompt

```text
low resolution, low quality, blurry text, distorted text, misspelled text, extra text, duplicated labels, unreadable small print, broken legends, incorrect axes, misaligned layout, cluttered spacing, cropped labels, random symbols, incorrect arrows, inconsistent legend colors, decorative filler text, watermark, noisy background
```

For charts/figures add: `fake data, incorrect tick labels, mismatched legend colors, overlapping labels, cropped axis title`.

## Settings

Final slide/poster/textbook figures:

- Full Qwen-Image-2512, 50 steps, CFG around `4.0`, official aspect ratio size.
- CacheDiT enabled for 50-step throughput: warmup `5`, skip interval `3`.
- 16:9 slides: `1664x928`; 4:3 figures: `1472x1104`; square: `1328x1328`; 3:2: `1584x1056`; 2:3: `1056x1584`.

Drafts:

- Qwen-Image Lightning 4-step LoRA, 4 steps, CFG `1.0`.
- Treat as layout/candidate generation only. Do not trust final labels from Lightning without visual QA.

## QA before accepting an image

Inspect visually at 100–200% zoom. Check:

- All quoted text appears exactly, with correct spelling, capitalization, punctuation, and units.
- No extra/unrequested text appears.
- Title, headings, labels, captions, legend, axes, and arrows match the prompt.
- Text is large enough at final slide/PDF size.
- Legend colors match chart/diagram elements.
- Arrows point to the right targets.
- No cropped labels, overlapping text, fake watermarks, pseudo-gibberish, or decorative filler.
- Scientific content is conceptually correct.

If exact text is critical, prefer generating a clean visual without dense text, then place final labels as editable PowerPoint/SVG/vector text.

## Sources checked

- Qwen-Image-2512 model card: `https://huggingface.co/Qwen/Qwen-Image-2512`
- Qwen-Image official repo and prompt-enhancement guidance: `https://github.com/QwenLM/Qwen-Image`
- ComfyUI Qwen-Image-2512 docs: `https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512`
- ComfyUI Qwen-Image docs: `https://docs.comfy.org/tutorials/image/qwen/qwen-image`
- LightX2V Qwen-Image-Lightning settings: `https://github.com/ModelTC/LightX2V-Qwen-Image-Lightning`
