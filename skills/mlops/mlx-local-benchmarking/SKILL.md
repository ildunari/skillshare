---
name: mlx-local-benchmarking
description: >
  Benchmark local MLX inference on Apple Silicon for LLMs, VLMs, embeddings, rerankers, and quantized variants. Trigger when the user asks about tokens per second, latency, peak memory, Mac Studio performance, prompt processing speed, batch size, image or video inference speed, or comparing MLX model variants. Do not use it for compatibility auditing or conversion unless a runnable model already exists.
compatibility: Cross-platform open skill format. Intended for Apple Silicon machines running MLX, mlx-lm, mlx-vlm, or mlx-embeddings locally.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

## Context

MLX uses lazy evaluation and Apple Silicon unified memory. Benchmarks must force evaluation, separate cold-start from warm runs, record package versions, and use task-specific inputs. A single “it feels fast” result is not enough to compare model variants.

## Task

Produce a reproducible local benchmark plan and result summary for MLX inference.

## Inputs

- Runnable model path or ID.
- Stack: `mlx-lm`, `mlx-vlm`, `mlx-embeddings`, or custom MLX code.
- Hardware: Mac model/chip/RAM if known.
- Inputs: prompts, media, query/document batches, generation lengths.
- Metrics needed: latency, prompt TPS, generation TPS, peak memory, model load time, output quality sanity.

## Benchmark workflow

1. **Record environment.** Capture macOS version, chip/RAM, Python version, `mlx`, stack package versions, model revision, and quantization.
2. **Define workload.** Use representative prompt/media/query sets. Keep one tiny sanity input and one realistic input.
3. **Separate phases.** Measure load time, first-token or first-result latency, steady generation/processing speed, and end-to-end time.
4. **Warm up.** Run at least one warm-up pass because first runs include compilation and cache effects.
5. **Force evaluation.** In custom MLX code, use `mx.eval(...)` around outputs and model parameters where appropriate so lazy computation does not hide work.
6. **Measure memory.** Prefer MLX peak memory APIs for in-process code; for CLI commands, record process/system memory with an explicit caveat.
7. **Run multiple trials.** Use median and range rather than a single measurement.
8. **Keep quality checks attached.** Fast output that is invalid is not a successful benchmark.

## Command patterns

Environment snapshot:

```bash
python - <<'PY'
import platform, subprocess, sys
pkgs = ['mlx', 'mlx_lm', 'mlx_vlm', 'mlx_embeddings', 'transformers']
print('python', sys.version)
print('platform', platform.platform())
for pkg in pkgs:
    try:
        mod = __import__(pkg)
        print(pkg, getattr(mod, '__version__', 'unknown'))
    except Exception as e:
        print(pkg, 'not importable', e)
try:
    print(subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string'], text=True).strip())
except Exception:
    pass
PY
```

CLI benchmark wrapper:

```bash
python scripts/benchmark_command.py --runs 5 --warmup 1 -- \
  python -m mlx_lm.generate --model ./models/model-mlx --prompt "Explain MLX." --max-tokens 128
```

Custom MLX memory pattern:

```python
import mlx.core as mx

mx.reset_peak_memory()
# run model work here
mx.eval(output)
print('peak_memory_gb', mx.get_peak_memory() / 1e9)
```

## Result format

```markdown
# MLX benchmark: model/path

## Environment
- Machine:
- macOS:
- Python:
- Packages:
- Model revision/path:

## Workload
- Inputs:
- Generation or processing settings:
- Warm-up/trials:

## Results
| Metric | Value | Notes |
|---|---:|---|
| Load time |  |  |
| First output latency |  |  |
| Throughput |  |  |
| Peak memory |  |  |
| Output sanity | pass/fail |  |

## Interpretation
What the result means and what it does not prove.
```

## Failure modes and recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Unrealistically fast timing | Lazy evaluation not forced | Add `mx.eval`; time complete generation, not prompt setup |
| First run much slower | Compilation/cache warm-up | Report cold and warm separately |
| Memory appears too low | Measuring shell RSS instead of MLX peak | Use in-process MLX peak memory where possible |
| Variant comparison unfair | Different prompts, token counts, media sizes, or settings | Normalize workload and generation length |
| Output invalid | Benchmark measured failure path | Fix model/quantization before performance claims |

## Done condition

Stop when results include environment, workload, repeated measurements, quality sanity, and caveats. Do not generalize beyond the measured workload.
