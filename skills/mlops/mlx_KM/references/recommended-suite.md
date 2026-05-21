# Recommended MLX agent skill suite

## 1. `mlx-model-repo-audit`

Purpose: decide whether a model is already MLX-compatible, which MLX stack applies, and what risks exist before conversion.

Use when: the user provides a Hugging Face model ID, asks whether an MLX version exists, asks which MLX package to use, or wants to compare a fine-tune with a base model.

Boundary: stops before conversion.

## 2. `mlx-llm-conversion`

Purpose: convert, run, and validate text-only LLMs with `mlx-lm`.

Use when: repo audit confirms a text-only causal/chat LLM or an existing MLX LLM variant.

Boundary: not for VLMs, audio/video, embeddings, or rerankers.

## 3. `mlx-vlm-conversion`

Purpose: convert, run, and validate image/audio/video/omni models with `mlx-vlm`, including processor preservation and task-specific output checks.

Use when: the model has image/audio/video inputs, media processor files, or multimodal generation behavior.

Boundary: not for text-only LLMs unless the user asks about the language submodule only.

## 4. `mlx-embedding-reranker`

Purpose: run and validate embedding and reranker models with `mlx-embeddings` or a current MLX embedding stack.

Use when: the task is vectors, similarity search, retrieval, ranking, or multimodal embedding.

Boundary: not for generative chat or image-to-text generation.

## 5. `mlx-quantization-quality`

Purpose: choose quantization settings and validate quality/resource tradeoffs.

Use when: memory, speed, bit-width, mxfp/nvfp, group size, or quantized variants are in scope.

Boundary: not the primary conversion skill; it runs after stack and baseline are known.

## 6. `mlx-local-benchmarking`

Purpose: measure local Apple Silicon inference performance and peak memory with reproducible workloads.

Use when: a model already runs and the user wants latency, throughput, memory, or variant comparisons.

Boundary: not for compatibility auditing or initial conversion.

## 7. `mlx-troubleshooting-repro`

Purpose: diagnose errors and create minimal reproducible examples for GitHub issues.

Use when: there is a concrete error, bad output, OOM, loading failure, processor mismatch, or upstream issue report.

Boundary: not for pre-conversion planning unless an error already exists.

## 8. `mlx-hub-packaging`

Purpose: package and document successful MLX conversions for local reuse or Hugging Face upload.

Use when: validation has passed and the user wants a reusable or published model repo.

Boundary: not before load/generation/quality validation.
