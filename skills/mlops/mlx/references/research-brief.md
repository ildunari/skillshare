# Research brief: MLX model conversion and local inference on Apple Silicon

Checked: 2026-04-29.

## Executive summary

MLX is Apple’s array framework for Apple Silicon. Its unified-memory and lazy-evaluation design makes local inference attractive on Macs, but the right stack matters. Text-only LLMs should generally use `mlx-lm`; multimodal image/audio/video models should use `mlx-vlm`; embeddings and rerankers should use `mlx-embeddings` when supported. Do not assume a Hugging Face Transformers model can be treated as a text LLM just because it contains a language model submodule.

The most important operational finding is that Hugging Face’s `transformers-to-mlx` agent skill is currently scoped to language model ports for `mlx-lm`; its README says VLMs are not supported and that pointing it at a VLM converts only the LLM portion. For VFIG/Qwen3-VL-style models, an agent should use a VLM-specific workflow and validate processor behavior.

## Current ecosystem snapshot

### MLX core

MLX provides NumPy-like arrays, neural-network and optimizer modules, and APIs in Python, Swift, C++, and C. Apple describes it as optimized for Apple Silicon unified memory. MLX arrays do not require explicit CPU/GPU transfers, and lazy evaluation means benchmarks must force evaluation.

### `mlx-lm`

`mlx-lm` is the main package for text-only LLM inference, conversion, quantization, chat/generation, fine-tuning, distributed inference, and upload workflows. Current docs and package pages show commands such as:

```bash
python -m mlx_lm.generate --model mlx-community/Qwen3-4B-Instruct-2507-4bit --prompt "..."
python -m mlx_lm.convert --hf-path Qwen/Qwen3-4B-Instruct-2507 --mlx-path ./model-mlx -q
```

Use `mlx-lm` for causal/text LLMs. Do not use it as the primary path for image/audio/video models unless the user explicitly wants only the language submodule.

### `mlx-vlm`

`mlx-vlm` is the main package for VLM and omni-model inference/fine-tuning on Mac using MLX. Recent docs show CLI entry points for generation and servers, and the package exposes a conversion command. Community model cards show Qwen3-VL variants converted with `mlx-vlm`, including 3-bit, 4-bit, and 8-bit examples. Recent issues also show real conversion flags such as `--quantize`, `--q-bits`, `--q-group-size`, and `--dtype`, plus failures that require load/generation validation after conversion.

Use `mlx-vlm` for image-text-to-text, OCR, scientific figure-to-SVG, video, audio, and multimodal chat.

### `mlx-embeddings`

`mlx-embeddings` supports local vision and language embedding models, including text and multimodal examples. Docs show text embedding and Qwen3-VL multimodal embedding/reranking patterns via model-specific processors. Treat embedding/reranker validation as a retrieval problem: vector shapes, normalization, similarity/ranking sanity, and downstream metric compatibility matter more than generative text quality.

### Hugging Face and MLX Community

The `mlx-community` Hugging Face organization hosts ready-to-use MLX models and conversion examples. Model cards often include the conversion package and version used. Existing MLX variants should be checked before re-converting.

Hugging Face docs for MLX show high-bandwidth download advice, `mlx-lm` generation, conversion, quantization, and upload examples. Transformers integration docs also note that supported Transformers language models can load safetensor weights through `mlx-lm` without a separate weight-conversion step, but that statement is language-model-scoped and should not be generalized to VLMs.

## Stable vs fast-moving guidance

Stable:
- Choose the stack by task type: LLM vs VLM/omni vs embedding/reranker.
- Preserve tokenizer, processor, chat template, special tokens, generation config, and media preprocessing artifacts.
- Establish a baseline before quantization.
- Validate by loading and generating or scoring, not by conversion completion alone.
- Record exact commands, versions, model revisions, inputs, and outputs.

Fast-moving:
- Exact CLI flags for `mlx_vlm.convert`, quantization modes, server request schemas, structured-output support, and Qwen-family support status.
- Which model architectures are supported in the latest `mlx-lm`, `mlx-vlm`, or `mlx-embeddings` release.
- Community model availability and quality of quantized variants.
- Recent upstream issues around weight-key mismatches, special token handling, and mxfp/nvfp quantization.

## Key gotchas

- VLMs routed through `mlx-lm` may load only the text component or generate incoherent text because media preprocessing is absent.
- Conversion commands can succeed while the converted model later fails to load.
- Quantized models can load but produce degraded outputs, especially for structured tasks like SVG, OCR, JSON, math, and retrieval rankings.
- Model cards can lag package releases; always check installed CLI help and current issues.
- Prequantized formats like GGUF, AWQ, or GPTQ are not automatically safe sources for MLX conversion. Prefer original safetensors/bf16/fp16 checkpoints when converting to MLX.
