# Unresolved risks and when to re-check upstream

Re-check current docs, releases, issues, and model cards before acting in these areas:

1. **Exact `mlx-vlm.convert` syntax.** Conversion flags and quantization modes have changed recently and issue examples may be version-specific.
2. **Qwen3-VL support status.** MLX Community model cards show Qwen3-VL conversions, but support depth for fine-tunes and custom variants can change.
3. **VFIG-specific MLX availability.** At research time, obvious VFIG-derived quantized listings were GGUF, not MLX. Re-search before converting.
4. **Processor/chat template behavior.** Transformers and MLX-VLM processor utilities may differ by model and package version.
5. **Activation quantization and mxfp/nvfp.** Support differs by hardware/backend and may not apply uniformly to all models.
6. **Prequantized source formats.** AWQ/GPTQ/GGUF source weights are not guaranteed to convert to MLX; prefer original safetensors where possible.
7. **Server request schema.** MLX-VLM server options, structured outputs, and media input formats are fast-moving.
8. **Model licenses and gated repos.** Uploading converted or quantized variants may be restricted even when local conversion is allowed.
9. **Benchmark comparability.** MLX lazy evaluation and caching can make stale benchmark methods misleading.
10. **Existing agent skills.** Hugging Face’s `transformers-to-mlx` skill currently targets LLM ports; re-check before using it for anything outside `mlx-lm`.
