# VFIG/Qwen3-VL case study workflow

Target: `XunmeiLiu/VFIG-4B`, a scientific-figure-to-SVG VLM derived from `Qwen/Qwen3-VL-4B-Instruct`.

Goal: run locally on Apple Silicon with MLX/MLX-VLM when feasible, validate generated SVG, and document commands/errors/patches.

## 1. Audit the repo

Use `mlx-model-repo-audit`.

Expected findings to verify live:

- The model card says the base model is `Qwen/Qwen3-VL-4B-Instruct`.
- The intended task is scientific/technical figure image to SVG code.
- The model uses `AutoProcessor` and an image-text prompt, so this is a VLM workflow.
- The model card’s inference logic trims output to the first `<svg>...</svg>` block.
- Check whether an MLX conversion already exists. At research time, Hugging Face’s quantized-derived listing for VFIG showed GGUF variants, not an obvious MLX Community VFIG variant.
- Check Qwen3-VL MLX Community variants to confirm base architecture support in `mlx-vlm`.

Do not start with `mlx-lm` or the text-only `transformers-to-mlx` skill. The image processor and media tokens are central to the task.

## 2. Create a Transformers baseline

Use the model card’s official path first. Save the sample image, prompt, generation settings, decoded text, and extracted SVG.

Baseline prompt:

```text
Convert this figure into valid SVG code.
```

Important settings from the model card to preserve or consciously change:

- `trust_remote_code=True` if required by the model card.
- BF16 model dtype when hardware supports it.
- `max_new_tokens=8192` or another documented limit.
- `do_sample=False` for deterministic validation.
- Chat template with image then text.
- Output trimming to the `<svg>...</svg>` block.

## 3. Attempt MLX-VLM conversion

Use `mlx-vlm-conversion`.

First check current commands:

```bash
python -m pip install -U mlx mlx-vlm transformers accelerate pillow huggingface_hub
python -m mlx_vlm.generate --help
python -m mlx_vlm.convert --help
```

Candidate conversion:

```bash
python -m mlx_vlm.convert \
  --hf-path XunmeiLiu/VFIG-4B \
  --mlx-path ./models/vfig-4b-mlx \
  --dtype bfloat16
```

Then load and generate from `./models/vfig-4b-mlx` on the same sample figure. If conversion fails, test the base `Qwen/Qwen3-VL-4B-Instruct` through MLX-VLM to separate base-architecture support from VFIG-specific fine-tune issues.

## 4. Validate SVG output

Use the bundled SVG checker:

```bash
python .agents/skills/mlx-vlm-conversion/scripts/svg_sanity_check.py \
  ./outputs/vfig_mlx_output.txt \
  --write-svg ./outputs/vfig_mlx_output.svg
```

Then render/open the SVG in a browser or Inkscape if available. Syntax validity is necessary but not enough; the figure should visually correspond to the input.

## 5. Quantize only after the unquantized path is understood

Use `mlx-quantization-quality`.

Candidate after baseline passes:

```bash
python -m mlx_vlm.convert \
  --hf-path XunmeiLiu/VFIG-4B \
  --mlx-path ./models/vfig-4b-mlx-4bit \
  --quantize \
  --q-bits 4 \
  --q-group-size 64 \
  --dtype bfloat16
```

For SVG generation, quality failures can be subtle: malformed paths, missing text labels, wrong axes, or diagrams that parse but do not resemble the source. Compare against the unquantized MLX output and the Transformers baseline.

## 6. Troubleshoot with evidence

Use `mlx-troubleshooting-repro` when a concrete failure occurs.

Classify the failure phase:

- Conversion: weight mismatch, unsupported layer, adapter issue.
- Load: missing processor/tokenizer/config or quantization mode mismatch.
- Preprocessing: image not accepted or prompt media format wrong.
- Generation: image ignored, incoherent output, early stopping.
- Validation: no complete SVG, XML parse error, invalid visual render.

Capture package versions, exact commands, error logs, and the smallest image that reproduces the issue.

## 7. Package only after validation

Use `mlx-hub-packaging` if the conversion should be reused or uploaded.

README should include:

- Source model and base model.
- MLX-VLM version and conversion command.
- Quantization settings if any.
- Usage command with image and prompt.
- SVG validation method and example output.
- Limitations: scientific figures only, possible visual mismatch, long generation requirements, hardware/memory caveats.
- License and attribution.
