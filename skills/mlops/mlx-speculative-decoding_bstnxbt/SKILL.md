---
name: mlx-speculative-decoding_bstnxbt
description: >
  Decide whether and how to add speculative decoding (DFlash, MTP, autoregressive draft-model) to a model running on MLX on Apple Silicon. Use when the user asks about speculative decoding, draft models, DFlash, MTP drafters, faster generation through speculation, or `--draft-model` for `mlx-lm`/`mlx-vlm`. Do not use for unrelated quantization or conversion work; route those through the relevant MLX skill first.
targets: [hermes-default, hermes-gpt, claude-hermes]
metadata:
  hermes:
    tags: [mlx, apple-silicon, speculative-decoding, dflash, mtp, draft-model, performance]
---
# MLX speculative decoding decision skill

## Context

Speculative decoding can multiply generation throughput when a small "draft" model proposes tokens that a large "target" model verifies in parallel. On Apple Silicon, the picture is messy as of mid-2026: support is partial, fragmented across runtimes, very chip-dependent, and easy to make slower than baseline. This skill exists so an agent does not waste an afternoon porting code or chasing benchmarks that don't transfer to the user's actual machine.

## Available runtimes (mid-2026 reality)

- **`mlx-lm` (`--draft-model` / `--num-draft-tokens`)** — supports vanilla autoregressive speculative decoding, but only for the architectures it has model classes for. Hybrid Qwen3.5-style cache rollback for spec decoding lives in open PR #1111 (not merged); MTP for Qwen3.5/3.6 in open PR #990. Even when working, MoE targets often see only 1.04–1.15× because the active-param baseline is already fast and a 1.7B draft is too heavy relative to active compute.
- **`mlx-vlm` (the runtime for image-text-to-text VLMs)** — has **no `--draft-model` flag and no internal speculative hooks** as of 0.4.4. Gemma 4 MTP is the first speculative path merged (PR #1112, May 2026), and it is Gemma-specific. Generic speculative for VLMs is an open feature request (issue #981).
- **`dflash-mlx` (PyPI: `dflash-mlx 0.1.0`)** — purpose-built Apple Silicon DFlash runtime with `dflash-benchmark` and `dflash-serve` CLIs. Supports tested pairings like `mlx-community/Qwen3.6-35B-A3B-4bit` + `z-lab/Qwen3.6-35B-A3B-DFlash`. Published numbers are M5 Max only; do not assume they transfer to older silicon.
- **DFlash drafters** (e.g. `z-lab/Qwen3.6-35B-A3B-DFlash`) are **block-diffusion drafters with custom code**, not vanilla autoregressive small models. They cannot be plugged into `mlx-lm --draft-model`; only `dflash-mlx` (and CUDA SGLang) consumes them.

## Decision flow

```
User asks for speculative decoding
  → Identify the target model's arch (qwen3, qwen3_5_moe, gemma_4, etc.)
  → Identify the user's chip (M2/M3/M4/M5 Max/Ultra)
  → Pick path:
      Gemma 4 family on Apple Silicon → mlx-vlm PR #1112 / mlx-community gemma-4 assistant
      Qwen3.6 35B-A3B on M5 Max+ → try dflash-mlx + z-lab DFlash drafter
      Qwen3.6 35B-A3B on older silicon (M2/M3) → smoke-test dflash-mlx with proper hygiene before assuming gain
      Hybrid Qwen3.5/3.6 + mlx-lm → cherry-pick PR #1111, expect 1.04–1.15× on MoE
      Anything else → likely no production-ready path; ship baseline
```

## DFlash smoke test (the cheapest first step)

Always run this before committing time to spec decoding on Apple Silicon. It takes ~3 minutes once models are cached.

```bash
python -m venv .venv-dflash
source .venv-dflash/bin/activate
pip install -U dflash-mlx huggingface_hub hf_xet

# dflash-benchmark calls `git rev-parse HEAD`. Make sure cwd is a git repo with at least one commit.
git init -q . && touch .gitkeep && git add .gitkeep && \
  git -c user.email=local@local -c user.name=local commit -qm init

dflash-benchmark \
  --model mlx-community/Qwen3.6-35B-A3B-4bit \
  --draft z-lab/Qwen3.6-35B-A3B-DFlash \
  --prompt "Write a long detailed essay about transformer attention." \
  --max-tokens 1024 --repeat 1 --no-eos
```

Record `speedup`, `acceptance_ratio`, and the `acceptance_first_20_avg` vs `acceptance_last_20_avg` trend. A collapsing acceptance trend means the drafter is mismatched to the target.

## Decision thresholds

| Result | Decision |
|---|---|
| Speedup **>1.3×** AND acceptance **>80%** | Use it as production. |
| Speedup **1.1–1.3×** OR acceptance **60–80%** | Keep as experimental mode behind a flag. Ship baseline as default. |
| Speedup **<1.1×** | Do not ship. Revisit when chip/runtime support improves. |
| Speedup **<1.0×** (slower than baseline) | Stop. Document the result so it doesn't get re-tried by the next agent. |
| Output mismatches greedy baseline at temperature 0 | Stop. Investigate tokenizer/config mismatch before trusting any number. |

## Realistic per-chip expectations (mid-2026)

| Chip | DFlash on Qwen3.6-35B-A3B-4bit | Notes |
|---|---|---|
| **M2 Max 64 GB** | **~0.51× median** (3 runs, 60s cooldown, against a Qwopus3.6 fine-tune of Qwen3.6-35B-A3B at `--max-tokens 1024`) | Verified locally 2026-05-06. Tight variance across runs (0.49 / 0.51 / 0.51), acceptance ~73%. Holds across both the public base (`mlx-community/Qwen3.6-35B-A3B-4bit`) and a fine-tune. dflash-mlx 0.1.0 verify/draft kernels appear unoptimized for this chip generation. Re-test on each `dflash-mlx` release. |
| **M3 Max** | unmeasured | Do not assume similar to M2 Max — spec performance is kernel-version-sensitive. |
| **M5 Max 64 GB** | 1.33–2.20× depending on output length | Per dflash-mlx README. Best gain at output ~1024 tokens, decays at 8k+. |

For autoregressive `mlx-lm` spec decoding on hybrid Qwen3.5-MoE: published 1.04–1.15× on MoE, requires PR #1111 cherry-pick for hybrid cache rollback. Not worth porting `qwen3_5_moe` from `mlx-vlm` to `mlx-lm` purely to chase this — the math doesn't work out for a 90-minute budget.

## Drafter selection

For autoregressive speculative decoding on `mlx-lm`:

- **Same family, same tokenizer, smallest dense model** is almost always right. For Qwen3.5/3.6 fine-tunes, prefer Qwen3.5-0.8B in MLX form over Qwen3-1.7B.
- **Verify tokenizer compatibility before benchmarking.** Hash `tokenizer.json` of target and draft. Different hash = stop.
- **MoE active params matter more than total.** A 1.7B autoregressive drafter against a 3B-active MoE target is *too heavy* — the drafter eats the win.
- **Avoid generic small models from a different family.** Qwen3 vanilla against a Qwen3.6 fine-tune with reasoning training will see acceptance below 50% on real prompts.

For DFlash:

- **Use the matching `z-lab` drafter** trained for the exact target family. Drafters are not interchangeable across model versions.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `dflash-benchmark` exits with `git rev-parse` fatal | cwd not a git repo with at least one commit | `git init && commit` an empty file |
| Speedup <1.0× on M2/M3 Max | dflash-mlx kernels not yet optimized for this chip | Don't ship; revisit after a release |
| Acceptance ratio `>0.7` but speedup still <1.0× | Per-cycle drafter overhead dominates | Try longer `--max-tokens` (1024+); if still <1.0×, abandon |
| `mlx-lm --draft-model` produces gibberish on Qwen3.5 hybrid | Hybrid cache rollback bug (issue #846 / PR #1111) | Cherry-pick PR #1111 or wait for merge |
| `mlx-vlm --draft-model` not recognized | mlx-vlm has no speculative support yet (as of 0.4.4) | Use `mlx-lm` if arch is supported, else `dflash-mlx`, else baseline |

## Done condition

Stop when one of the following is true:

- A speculative variant beats baseline by >1.3× with >80% acceptance and matches greedy output at temperature 0. Promote to production.
- Speedup is <1.0× or acceptance is <60% on a representative prompt. Document it and ship baseline.
- The user's arch + chip combination is not supported by any current runtime. Document the gap and ship baseline.

In all "ship baseline" cases, write a short note in `PRODUCTION.md` (or equivalent) so the next agent does not retry this.

## References

- `dflash-mlx` repo: https://github.com/bstnxbt/dflash-mlx
- DFlash paper repo: https://github.com/z-lab/dflash
- `mlx-lm` PR #1111 (hybrid spec decoding fix): https://github.com/ml-explore/mlx-lm/pull/1111
- `mlx-lm` PR #990 (Qwen3.5/3.6 MTP): https://github.com/ml-explore/mlx-lm/pull/990
- `mlx-lm` issue #1132 (warn-when-spec-hurts on MoE): https://github.com/ml-explore/mlx-lm/issues/1132
- `mlx-vlm` PR #1112 (Gemma 4 MTP): https://github.com/Blaizzy/mlx-vlm/pull/1112
- `mlx-vlm` issue #981 (general spec/MTP request): https://github.com/Blaizzy/mlx-vlm/issues/981
- `z-lab/Qwen3.6-35B-A3B-DFlash`: https://huggingface.co/z-lab/Qwen3.6-35B-A3B-DFlash
