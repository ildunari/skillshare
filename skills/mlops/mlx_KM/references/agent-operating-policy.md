# Agent operating policy for MLX work

## Core rule

Do not claim MLX success until the model has been loaded and tested on a task-representative input. Downloading, converting, or quantizing is not enough.

## Evidence ladder

Use the strongest evidence available:

1. Current upstream docs, releases, model cards, and issues.
2. Local environment checks: package versions and CLI help.
3. Repository file audit: config, tokenizer, processor, generation settings, weight files, adapters.
4. Baseline behavior in Transformers or an existing MLX model.
5. MLX load and real inference.
6. Task-specific validation: parsed SVG/JSON/XML, OCR comparison, retrieval ranking, visual render, etc.
7. Reproducible notes: commands, versions, paths, model revisions, errors, inputs, outputs.

## Stack selection policy

- Use `mlx-lm` for text-only LLMs.
- Use `mlx-vlm` for image/audio/video/omni models.
- Use `mlx-embeddings` for embedding and reranker models.
- If a model includes processors or media tokens, assume it is not a plain LLM until proven otherwise.

## Quantization policy

Start from a known-good baseline. Quantize only after the model’s behavior is understood. Approve a quantized variant only when it improves memory/speed and passes quality checks. Structured-output and scientific tasks deserve conservative precision.

## Reproducibility policy

Every meaningful run should leave a note with:

- Date and machine.
- Model ID, revision, and local path.
- Package versions.
- Command or code.
- Inputs and generation/scoring settings.
- Output and validation result.
- Errors and recovery attempts.

## Upstream issue policy

Before filing an issue, reduce the repro to a small input, current packages, exact command, full logs, and expected/actual behavior. Do not assert an upstream bug until stack selection, CLI help, package freshness, and a baseline have been checked.
