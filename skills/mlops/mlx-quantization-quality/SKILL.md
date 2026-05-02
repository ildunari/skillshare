---
name: mlx-quantization-quality
description: >
  Decide, apply, and validate MLX quantization choices for LLMs, VLMs, embeddings, and rerankers. Trigger when the user asks about 8-bit, 6-bit, 5-bit, 4-bit, 3-bit, mxfp, nvfp, group size, memory reduction, speed, quality loss, or comparing quantized MLX models. Do not use it as the primary conversion skill; use it after the model stack and baseline are known.
compatibility: Cross-platform open skill format. Intended for Apple Silicon MLX workflows across mlx-lm, mlx-vlm, mlx-embeddings, and MLX Community model variants.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

## Context

Quantization is a trade-off, not a checkbox. A quantized model can load and still fail the task. The safest workflow is to establish a full-precision or known-good baseline, then quantify memory/speed gains and quality loss with task-specific tests.

## Task

Recommend a quantization plan, apply it using the relevant MLX stack, and validate that quality remains acceptable.

## Inputs

- Model ID or local converted path.
- Stack: `mlx-lm`, `mlx-vlm`, `mlx-embeddings`, or existing MLX variant.
- Target Mac memory and speed goals.
- Quality bar: acceptable output drift, benchmark, or task-specific checks.
- Baseline outputs or a plan to obtain them.

## Decision guide

- **Need maximum fidelity or first debug pass:** use bf16/fp16 or unquantized where feasible.
- **General local chat or VLM inference:** start with 8-bit or 4-bit only after baseline validation exists.
- **Small memory budget:** 4-bit or 3-bit may be necessary, but expect more task-specific validation.
- **Embeddings/rerankers:** validate ranking quality carefully; small numeric drift can change top-k results.
- **Structured outputs, code, SVG, OCR, math, scientific diagrams:** prefer conservative quantization and validate exact formats.
- **Prequantized non-MLX formats:** do not assume AWQ, GPTQ, GGUF, or other packed formats can be converted directly. Prefer original safetensors/bf16/fp16 checkpoints for MLX conversion.

## Workflow

1. **Record baseline.** Save prompt/media/query sets, generation settings, outputs, scores, memory, and speed for unquantized or known-good model.
2. **Choose candidate precisions.** Pick one conservative candidate and one aggressive candidate if memory pressure requires it.
3. **Convert or select variant.** Use the relevant stack’s current CLI/API. Verify help before relying on option names.
4. **Load and run.** Loading is necessary but not enough.
5. **Compare quality.** Use task-specific checks: text coherence, exact JSON/SVG/XML parse, OCR string match, embedding ranking, or benchmark subset.
6. **Compare resource gains.** Measure model size, peak memory, prompt/generation speed, and latency.
7. **Document decision.** State which quantization is approved and which failed, with evidence.

## Command patterns

`mlx-lm` quantized conversion pattern:

```bash
python -m mlx_lm.convert \
  --hf-path Qwen/Qwen3-4B-Instruct-2507 \
  --mlx-path ./models/qwen3-4b-4bit \
  -q
```

`mlx-vlm` quantized conversion pattern:

```bash
python -m mlx_vlm.convert \
  --hf-path Qwen/Qwen3-VL-4B-Instruct \
  --mlx-path ./models/qwen3-vl-4b-4bit \
  --quantize \
  --q-bits 4 \
  --q-group-size 64 \
  --dtype bfloat16
```

Before running, check:

```bash
python -m mlx_lm.convert --help
python -m mlx_vlm.convert --help
```

## Quality report format

```markdown
# Quantization decision: model-id

## Recommendation
Approved variant: bf16, 8-bit, 4-bit, etc.
Reason:

## Baseline
- Model/path:
- Prompts/media/queries:
- Settings:
- Output summary:
- Memory/speed:

## Candidates
| Variant | Size | Peak memory | Speed | Quality result | Decision |
|---|---:|---:|---:|---|---|

## Failure notes
What broke, exact command, error/output, and recovery.
```

## Failure modes and recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Quantized model fails to load | Unsupported quantization mode, layer shape/group-size mismatch | Retry default quantization; use less exotic mode; check upstream issues |
| Output is fluent but wrong | Quality loss in task-sensitive model | Back off to 8-bit/bf16; validate with harder examples |
| Embedding top-k changes unexpectedly | Numeric drift affects ranking | Evaluate on labeled retrieval mini set; use higher precision |
| Vision model loses details | Vision/language projection quantization too aggressive | Try unquantized vision path if supported; use 8-bit or bf16 |
| Speed worsens | Kernel or cache path not optimized for chosen mode | Benchmark multiple variants; choose measured result, not assumed result |

## Done condition

Stop when the selected quantization has measured resource benefits and passes the stated quality checks, or when no acceptable quantized variant exists. Do not upload or recommend a quantized model based only on size reduction.
