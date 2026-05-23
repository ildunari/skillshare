# GamingPC Qwen LoRA catalog — 2026-05-23

Current installed production LoRAs should be verified with:

```bash
curl -s http://100.93.10.54:8188/models/loras
curl -s http://100.93.10.54:8188/object_info | jq '.LoraLoader.input.required.lora_name[0]'
```

## Installed / being installed

These are the useful Qwen-Image LoRAs selected for Kosta's second-brain and figure-generation work. They live under `C:\Users\kosta\AIProjects\ComfyUI\models\loras` on GamingPC.

### `illustration-1.0-qwen-image.safetensors`

- Source: `https://huggingface.co/alvdansen/illustration-1.0-qwen-image`
- Size: about 774 MB.
- License shown by model card: `other`.
- Base: Qwen-Image adapter; not explicitly Qwen-Image-2512, so test before using in production batches.
- Trigger: no required trigger documented.
- Suggested strength: model `0.8–1.0`, clip `0.8–1.0`.
- Suggested settings: Euler/simple, CFG `3.5–4.0`, `30–60` full-Qwen steps.
- Use when: Obsidian hero cards need a warmer editorial/illustration/risograph or graphic-novel feel instead of raw Qwen's generic slick render.
- Avoid when: exact UI geometry/text must be preserved; it may stylize shapes.

### `[Qwen.Image]Isometric_Redmond.safetensors`

- Source: `https://huggingface.co/artificialguybr/ISOMETRIC-REDMOND-QWENIMAGE`
- Size: about 590 MB.
- License: Apache-2.0.
- Base: `Qwen/Qwen-Image-2512`; model card recommends ComfyUI.
- Trigger: `ISOMETRIC`, `ISOMETRICREDM`, or `IsometricRedm`.
- Suggested strength: model `0.75–0.95`, clip `0.75–0.95`.
- Use when: systems, infrastructure, agent tools, lab workflows, app architecture, folder/vault structures, and other concept maps should read as small isometric scenes.
- Avoid when: the target should remain flat 2D UI; isometric depth can fight exact layout.

### `[Qwen.Image]Stickers_Redmond.safetensors`

- Source: `https://huggingface.co/artificialguybr/STICKERS-REDMOND-QWEN-IMAGE`
- Size: about 590 MB.
- License: Apache-2.0.
- Base: `Qwen/Qwen-Image-2512`; model card recommends ComfyUI.
- Trigger: `Sticker` or `Stickers`.
- Suggested strength: model `0.65–0.9`, clip `0.65–0.9`.
- Use when: a note needs one clean isolated icon, motif, mascot-like object, or visual token on a simple background.
- Avoid when: complex diagrams, dense multi-panel layouts, or serious academic figures need restrained styling.

### `Qwen-Image-2512-Master-Pixel-Art-LoRA.safetensors`

- Source: `https://huggingface.co/prithivMLmods/Qwen-Image-2512-Pixel-Art-LoRA`
- Size: about 1.18 GB.
- License: Apache-2.0.
- Base: `Qwen/Qwen-Image-2512`.
- Trigger: `Pixel Art`.
- Suggested settings from card: `45–50` steps, default `1024x1024`; listed good size `1280x832`.
- Use when: retro/low-res category markers, game-like abstractions, playful tool icons, or intentionally stylized note covers.
- Avoid by default for biomedical/academic notes and normal second-brain covers; it is a strong style.

### `Wuli-Qwen-Image-2512-Turbo-LoRA-4steps-V3.0-bf16.safetensors`

- Source: `https://huggingface.co/Wuli-art/Qwen-Image-2512-Turbo-LoRA`
- Size: about 1.18 GB.
- License: Apache-2.0.
- Base: `Qwen/Qwen-Image-2512`; V3 model card says ComfyUI compatible.
- Trigger: none; this is a speed LoRA, not a style LoRA.
- Suggested settings: `4` steps, CFG `1.0`.
- Use when: draft exploration, fast candidate grids, or A/B prompt debugging.
- Avoid for final images unless QA proves it beats the current Lightning draft lane.

## Candidate not installed by default

### Qwen-Image EliGen LoRA

- Source: `https://civitai.com/models/1894878/qwen-image-eligen-lora`
- File: `Qwen-Image-EliGen-v2.safetensors`, about 450 MB.
- Use: regional/layout control with guide image/mask.
- Status: do not treat as a plain style LoRA; it likely needs an EliGen-compatible workflow/nodes. Install only when doing layout-control experiments.

## Routing rules

- Default final-quality lane remains **full Qwen-Image-2512 FP8 with no style LoRA** unless the visual goal benefits from a style adapter.
- For Obsidian second-brain covers:
  - Use `illustration-1.0` for general editorial card art.
  - Use `Isometric Redmond` for systems, architecture, tooling, workflows, and layered knowledge maps.
  - Use `Stickers Redmond` for single-object/icon covers.
  - Use `Pixel Art` only when a playful retro look is explicitly desirable.
- Use only one style LoRA at a time for production unless an A/B test proves stacking is better.
- Keep style LoRA strength moderate (`0.65–0.9`) for note covers. At `1.0+`, adapters tend to overpower content.
- Speed LoRAs (`Lightning`, `Wuli Turbo`) are draft lanes. Do not combine speed LoRAs with final-quality LoRA styling without a small A/B smoke test.

## Minimal ComfyUI wiring

Use standard `LoraLoader` when both model and CLIP should be modified:

```text
UNETLoader -> ModelSamplingAuraFlow -> LoraLoader.model -> KSampler.model
CLIPLoader -> LoraLoader.clip -> CLIPTextEncode.clip
```

For model-only speed/style tests, `LoraLoaderModelOnly` is available too, but use regular `LoraLoader` first because these Qwen style LoRA cards document normal adapter behavior.

Record `lora_name`, `strength_model`, `strength_clip`, `trigger`, `steps`, `CFG`, sampler, scheduler, seed, and image path in any A/B manifest.

## Smoke-test protocol before batch use

Before switching a large batch to any LoRA:

1. Pick 5 representative notes: one systems/tooling, one UI/design, one daily/log, one biomedical/research, one abstract guide/index.
2. Generate baseline full-Qwen plus one LoRA candidate at 3 seeds each.
3. Score each image 0–5 for note relevance, clean composition, text/gibberish violations, and style fit.
4. Adopt the LoRA only if it improves average score by at least `+0.5` and has no new systematic failure.
5. If a LoRA helps only one domain, route by folder/domain instead of making it global.
