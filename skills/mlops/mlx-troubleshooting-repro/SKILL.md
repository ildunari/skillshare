---
name: mlx-troubleshooting-repro
description: >
  Diagnose MLX conversion, loading, generation, quantization, processor, memory, and runtime failures on Apple Silicon, and create minimal reproducible examples for GitHub issues. Trigger when the user shows an MLX error, missing or unexpected weights, incoherent output, OOM, Metal crash, processor mismatch, bad quantized behavior, or asks how to file an upstream issue. Do not use it for routine conversion planning before an error exists; start with the repo audit skill.
compatibility: Cross-platform open skill format. Intended for Apple Silicon MLX workflows across mlx-lm, mlx-vlm, mlx-embeddings, Transformers, and Hugging Face model repos.
targets: [hermes-default, hermes-gpt]
---

## Context

Many MLX failures look similar but have different causes: unsupported architecture, wrong stack, bad tokenizer/processor, quantization mismatch, stale package versions, missing files, or true upstream bugs. Good troubleshooting narrows the failure phase and captures a repro small enough for maintainers to act on.

## Task

Diagnose the failure, propose a recovery path, and produce a reproducible issue bundle when upstream help is needed.

## Inputs

- Exact command or code that failed.
- Full error text, not only the last line.
- Model ID/path and revision if known.
- Stack: `mlx-lm`, `mlx-vlm`, `mlx-embeddings`, custom MLX, Transformers baseline.
- Machine details and package versions.
- Whether an unquantized or baseline run works.

## Diagnosis workflow

1. **Classify failure phase.** Download, repo audit, conversion, load, preprocessing, prompt templating, generation, output parsing, quantization, server/API, benchmark, upload.
2. **Verify stack selection.** VLMs and processor-heavy models should not be debugged as plain `mlx-lm` failures unless the text-only component is the target.
3. **Reduce variables.** Retry with latest packages, unquantized weights, a tiny prompt/media input, and local paths when possible.
4. **Inspect artifacts.** Check config, tokenizer, processor, generation config, safetensors index, missing files, and weight key mismatches.
5. **Compare baseline.** If Transformers works and MLX fails, capture both command outputs. If both fail, the issue may be model/repo usage rather than MLX.
6. **Search current upstream issues.** MLX support changes quickly; an error may already have an open issue, workaround, or merged fix.
7. **Create a minimal repro.** Include environment, exact commands, tiny input, expected behavior, actual behavior, and logs.
8. **Recommend next action.** Retry with modified command, switch stack, back off quantization, use existing MLX variant, patch locally, or file issue.

## Common failure map

| Error or symptom | Likely cause | First recovery |
|---|---|---|
| Unsupported model architecture | Library lacks model class | Check current docs/issues; try existing MLX variant; consider porting |
| Missing/unexpected weight keys | Config mismatch, adapter/merge issue, tied weights, checkpoint shard issue | Compare base/fine-tune config and safetensors index |
| Model loads but generated text is incoherent | Wrong tokenizer/chat template/special tokens or wrong stack | Print rendered prompt; inspect tokenizer files; rerun repo audit |
| VLM ignores image/audio | `mlx-lm` path or processor skipped | Use `mlx-vlm` and preserve processor artifacts |
| Quantized model fails or quality collapses | Unsupported mode or excessive compression | Retry unquantized; use quantization skill |
| OOM | Model too large, resolution/context too high, memory fragmentation | Smaller variant, lower media resolution/context, more conservative cache/settings |
| Server works but API client fails | Request schema mismatch or unsupported structured output path | Test CLI first; inspect server docs and request body |

## Repro bundle format

```markdown
# MLX issue repro: short title

## Summary
One sentence describing the failure phase and model.

## Environment
- Machine/chip/RAM:
- macOS:
- Python:
- Packages:
- Model ID/path/revision:

## Command or code
```bash
exact command
```

## Expected behavior

## Actual behavior
Full error log or invalid output summary.

## What I already tried
- Latest packages:
- Unquantized path:
- Baseline Transformers path:
- Smaller input:
- Related issues checked:

## Minimal input files
Names and how to obtain or generate them.
```

Use the bundled helper to create a starter note:

```bash
python scripts/make_repro_note.py \
  --title "Qwen3-VL conversion fails after quantization" \
  --model XunmeiLiu/VFIG-4B \
  --command "python -m mlx_vlm.convert ..." \
  --error-log ./error.log \
  --output ./mlx_issue_repro.md
```

## Done condition

Stop when the failure has a classified phase, a plausible root cause, a recovery path, and either a working fix or a minimal issue-ready repro. Do not claim an upstream bug until stack selection, package freshness, and a minimal input have been checked.
