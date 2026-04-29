# Validation checklists

## `mlx-model-repo-audit`

- Model task is classified with evidence from metadata, files, and model card.
- Existing MLX variants were checked.
- Correct stack is recommended with confidence level.
- Tokenizer, processor, chat template, generation config, and special tokens are addressed.
- Fine-tune/base differences are noted when relevant.
- License, gated access, custom code, and adapter status are noted.
- Output stops before conversion and names the next skill.

## `mlx-llm-conversion`

- Model is confirmed text-only.
- Existing MLX variant was checked.
- CLI/API help was checked in the active environment.
- Baseline prompt/output exists or the lack of baseline is explained.
- Converted model loads and generates coherent text.
- Tokenizer/chat template/special token behavior is verified.
- Quantization, if any, is separately validated.
- Run notes include versions, commands, paths, prompts, and outputs.

## `mlx-vlm-conversion`

- Model is confirmed multimodal or processor-dependent.
- Existing MLX-VLM support or variants were checked.
- Transformers baseline exists when feasible.
- Processor/media preprocessing artifacts are preserved.
- MLX-VLM converted model loads and runs on real media.
- Output passes task-specific validation such as SVG/XML parsing or OCR checks.
- Quantized variant is compared with baseline if used.
- Errors are classified by phase and documented.

## `mlx-embedding-reranker`

- Task is embedding or reranking, not generation.
- Model/tokenizer or model/processor loads.
- Output shape, dtype, dimension, and normalization are recorded.
- Positive examples score above negatives.
- Batch and single-item behavior is checked.
- Downstream metric and vector-store settings are documented.

## `mlx-quantization-quality`

- Baseline exists before quantization decision.
- Candidate bit-widths/modes are justified by memory/speed goals.
- Quantized model loads and runs task-representative inputs.
- Quality is compared, not assumed.
- Resource gains are measured.
- Approved and rejected variants are documented.

## `mlx-local-benchmarking`

- Environment and package versions are recorded.
- Workload is representative and repeatable.
- Warm-up and measured trials are separated.
- Lazy evaluation is forced in custom MLX code.
- Peak memory and timing methods are stated.
- Output sanity is checked.
- Results include caveats and do not overgeneralize.

## `mlx-troubleshooting-repro`

- Failure phase is classified.
- Stack selection is rechecked.
- Package freshness and CLI help are checked.
- Minimal input reproduces the issue or best effort is documented.
- Baseline or unquantized comparison is attempted when feasible.
- Issue note includes environment, exact command/code, expected/actual behavior, and full logs.

## `mlx-hub-packaging`

- Model loads from final package path.
- Required files are present for the task.
- README/model card includes source, revision, license, conversion command, stack version, usage, validation, and limitations.
- Sensitive/local files are excluded.
- Upload decision is license-aware.
- Final package is reproducible by another agent/user.
