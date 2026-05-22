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

## Batch catalog thumbnails

For second-brain/catalog thumbnails, do not prompt from the title alone. Read the entry content/code summary and name the concrete UI pattern, components, and interaction. A batch of 94 technically successful files can still be a bad result if every image is a generic phone mockup.

Kosta specifically prefers creative renderings of the code output / visual essence over literal phone-screen app mockups. Avoid the reflexive `SwiftUI → iPhone screen → polished app UI` chain. For effects and components, make the effect/component the subject: geometry, material, masks, layers, motion state, shadows, spacing, and the rendered composition. Only include a phone/device frame when the source code truly depends on the device surface; otherwise crop to the component or use an abstract render.

Before a large batch, generate 3-5 samples from different categories and visually inspect them. If the user criticized a previous batch, delete or quarantine the old assets before regenerating so stale low-quality images do not remain linked. Use Lightning only for drafts; use the full Qwen/CacheDiT lane or another quality lane for final replacement batches.

For iterative repair, keep prompts short and run an adversarial review loop: score each image 0-5 against the intended visual essence, name the single dominant failure, revise only the failing prompts, and stop when two reviewers agree the remaining issues have plateaued. When Kosta asks for self-evolution/self-improvement, do not treat 2-3 passes as enough: run at least 10 loops, at most 30 loops, or stop only after 4 consecutive plateau loops. Track loop number, score, dominant failure, prompt delta, image path, elapsed time, token/call estimate if available, and plateau count. Use a persistent Claude Code reviewer/worker (`claude -p -c`) for caching benefits; give it concise intended descriptions and image paths, not long prompt essays. When GPT prompt-architect guidance is requested, simplify rather than expand: one short intent line, 1-2 visible constraints, explicit scope boundaries/exclusions, and a manifest of score/failure/fix.

If a correction arrives embedded in tool output or background-process output, treat it as an active user correction before continuing. Do not let a “process completed” notification hide user feedback like “delete these images” or “send representative samples.”

For UI thumbnails, avoid words that invite Qwen to render fake explanatory text: `label`, `callout`, `annotation`, `before/after`, `heading`, `caption`. Even when the prompt says “no text,” those words often produce garbled pseudo-labels. Prefer icon-only rows, placeholder bars, arrows, panels, ghosted duplicate shapes, and cropped UI states.

Use this compact schema for code-pattern/catalog thumbnails:

```text
High-quality visual-essence thumbnail for a SwiftUI code pattern. Pattern: "<specific pattern>". Rendered subject: <the component/effect itself — geometry, material, masks, layers, shadows, spacing, motion state>. Surface: <component crop / abstract render / macOS window / device frame only if the code depends on it>. Focus on what the rendered code output could look like, not a hypothetical app screen using it. No code, no watermark, no logos, no labels, no callout text, no random readable text, no gibberish labels.
```

Bad default: “SwiftUI catalog thumbnail as a flat 2D UI storyboard / app interface / iPhone screen.” That still tends to produce plausible phone mockups. Prefer “rendered component/effect as the subject.”

### UI-essence failure modes to pin in the prompt

Six failures recur even with the schema above; all need explicit in-prompt language, not just negatives:

- **Literal device backdrops creep in.** Saying “floating macOS desktop window” or “app screen” pulls Qwen toward rendering a literal MacBook keyboard, phone bezel, or monitor frame *behind* the subject — even when the rest of the prompt is abstract. Add an explicit positive negative: `no laptop, no keyboard, no device frame` (or `no phone, no bezel` for mobile). For the backdrop, name the abstract thing you want (`soft abstract pastel desktop wallpaper gradient`, `clean off-white studio`) instead of relying on words like “desktop” or “workspace.”
- **Edge-anchored panels flip orientation.** “Side drawer,” “bottom sheet,” “snackbar,” and similar edge-anchored overlays often render with the wrong aspect or wrong edge. Pin three things together: aspect (`tall vertical, taller than wide` or `wide horizontal, wider than tall`), edge (`attached to the left edge` / `pinned to the bottom edge`), and an explicit negative for the wrong orientation (`no horizontal drawer`). Describe the scene as a layered composition (`darkened dimmed background rectangle filling the frame, partially covered on the left half by …`) rather than a motion verb (`sliding in from the side`) — Qwen interprets composition more reliably than implied motion.
- **Edge-anchored drawers render as physical glass doors.** Even with "no horizontal drawer" pinned, Qwen still produces a hinged glass-door composition when the prompt mentions "drawer" or "overlay." You need an explicit "flat 2D UI surface, no hinges" in the positive prompt plus negatives `hinged door, swinging door, glass door, door hinges`. The orientation rule alone is not enough — it fixes the aspect but not the affordance.
- **Glass-tile geometry drifts to oval/lens.** When the subject is "a translucent glass tile" or "rounded glass shape," Qwen frequently renders an oval or circular lens. Pin geometry explicitly (`rounded rectangle, gentle corner radius`, or `rounded square`) and negate the failure modes (`no oval, no circular tile, no lens`). Same pattern applies to any rounded-rectangle UI element described loosely.
- **Avatar placeholders default to photo-realistic faces.** "Small circular avatar" in a UI prompt almost always produces a stock-photo human face. Pin the placeholder explicitly: `small solid filled gray circle, abstract placeholder, no face, no photo` and negate `human face, photograph, portrait, person, woman, man, eyes, hair, realistic skin`. Same risk applies to "profile picture," "user icon," "contact photo."
- **"Flat card" doesn't pin orientation.** When a card or sticker should lie flat on a surface, the word "flat" alone tends to produce a tilted or folded card. Pin the camera angle (`lying flat on a surface, viewed from slightly above`) and negate the failure modes (`folded card, tilted card, card standing on edge, leaning card`). For peel/curl compositions, also specify which corner peels.
- **Element counts drift unless tied to spatial hints.** "Two pill buttons" can render as one; "three pill bars" can become four. Pair the count with a spatial layout (`exactly two small pill buttons side by side`, `three short horizontal pill bars stacked vertically`) and negate the common drift (`single pill, only one button`). Spatial-hint anchoring beats bare count words.

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
