---
name: hermes-benchmark-wrapper_Hermes
description: Use when wiring an externally-validated benchmark into the Hermes self-improvement harness (or any harness following the same task-yaml + run-script contract). Covers loader, sample_tasks.yaml, deterministic validator design, integration with `run_one.sh`/`run_held_out.sh`, and the harness's bug-catch + relearn methodology.
version: 0.1.0
author: Hermes Agent
license: MIT
targets: [hermes-default, hermes-gpt, claude-hermes]
---
# Hermes Benchmark Wrapper

Use this when adding a new external benchmark (BFCL, FreshQA, polyglot, BrowseComp, PrimeVul, Terminal-Bench, τ²-bench, MermaidSeqBench, or similar) to the Hermes self-improvement harness.

The harness lives at `~/.hermes-sandbox/harness/`. The integration contract is `tasks.yaml`-shape entries that `run_one.sh` invokes against a chosen profile. Phase-3 (May 2026) wired 8 benchmarks against this contract — this skill codifies the pattern.

## Per-benchmark deliverables (under `harness/benches/<name>/`)

1. `upstream/` — shallow clone or sparse-checkout of the source repo. Apache-2.0 / MIT-compatible only. Stay under ~50MB per bench dir.
2. `loader.py` — reads the upstream dataset and emits `tasks.yaml`-style records. Must support a `--limit` or sample mode so we generate a tractable subset for `sample_tasks.yaml`.
3. `sample_tasks.yaml` — the actual subset (~5-12 tasks) wired into the harness. Each entry has `id`, `prompt` (with `{workspace}` placeholder for paths), optional `setup` (bash, populates workspace), optional `validate` (bash, exits 0 on pass).
4. `README.md` — install + smoke-test commands, license attribution, caveats (any timeouts, environment requirements, known-flaky tasks).
5. Optional: `validate.py` helper if validation needs Python (called from the yaml's `validate` field).

## Validator design rules

- **Deterministic exit codes only.** No LLM judges in the critical path.
- Prefer `grep -E` / language-native test runners (pytest, cargo test, go test, mmdc) / state-diff scripts.
- The agent's response tail is at `{workspace}/last_response.txt` — use for response-based validation.
- For state-mutation tasks (τ²-bench retail, BFCL), diff a final state file vs an expected state.
- For paired tasks (PrimeVul vuln/patched), validate the vuln half with CWE + "vulnerab" match; validate the patched half with "NO_VULNERABILITY" match.
- Validators must be quote-safe — wrap shell content carefully. Apostrophes in answer strings (`doesn't exist`, BTS `'Butter'`) must use `grep -F` or proper quoting.

## Task-yaml schema (must match)

```yaml
- id: <benchmark>_<short_descriptor>     # unique across the whole harness
  prompt: |
    <user-facing task description; can use {workspace} placeholder>
  setup: |
    # optional, bash, {workspace} expands at invocation
    mkdir -p {workspace}/...
  validate: |
    # bash, exit 0 == pass; can grep {workspace}/last_response.txt or run test commands
    cd {workspace} && pytest -q tests/test_outputs.py
```

## Smoke-test before claiming "wired"

1. From within `harness/benches/<name>/`, run a single representative task end-to-end via `bash ~/.hermes-sandbox/harness/run_one.sh <profile> <task_id> smoke-0`.
2. Confirm the scorecard at `~/.hermes-sandbox/<profile>/bench-results/iter-smoke-0/<task_id>.json` has expected `task_id`, plausible `tool_call_count`, and (after a quick agent run) `validate_pass: true` for the gold-answer case AND `validate_pass: false` for an obviously-wrong response.
3. Document the smoke command in the bench's README.

## Integration with the loop

- After wiring, merge `sample_tasks.yaml` entries into `tasks_v2_candidates.yaml`. Run one calibration pass per profile. Drop any task all 3 profiles pass cleanly (saturated — no headroom for self-improvement). Lock the final set as `tasks_v3.yaml`.
- The orchestrator at `orchestrate_p3.sh` reads `tasks_v3.yaml` and walks every task each iter. Reflection (`self_improve_p2.py`) sees the scorecards.

## Bug-catch + relearn (carry forward into every loop)

Phase-3 caught a silent reflection crash that zeroed 3 iterations. The harness now bakes in:

1. **Defensive scorecard loading** in `self_improve_p2.py`: filters known aux files (`tool_efficiency.json` is the canonical example) and validates shape (`task_id` required). Every skipped/unreadable record is logged to stderr via `[reflection-guard]` prefix. Never blindly glob `*.json` from a results dir.
2. **Crash detection** in `orchestrate_p3.sh`: every reflection exit code is checked. Non-zero + no "Empty edits block" sentinel writes `!!! REFLECTION CRASHED` to the run log and appends iter to `<sandbox>/reflection_crashes.log`.
3. **`relearn.py <profile> <iter>`**: when a bug is caught (post-fix), this restores the rules to that iter's pre-reflection snapshot and re-invokes reflection with the current (fixed) code. Recovers the lost reflection signal without re-running the whole loop.

If you're spawning a new benchmark-wrapper sub-agent, do NOT have them touch the bug-catch plumbing — that's harness-wide. Their scope ends at producing loader + sample_tasks + README for their one benchmark.

## Tool-efficiency audit hook

`tool_efficiency_audit.py <profile> <iter_label>` walks the iter's scorecards + session jsonls and writes `tool_efficiency.json` into the same iter directory. The reflection script then injects audit findings into the reflection prompt under a "TOOL EFFICIENCY AUDIT" header.

Phase-3 confirmed this signal flows through into rule edits — `gpt` independently created an `instructions/tool-efficiency.md` after seeing audit findings about redundant `firecrawl_*` calls. Causal chain validated.

## License & data handling

- License-check upstream BEFORE cloning. Apache 2.0, MIT, or BSD are safe.
- Encrypted datasets (BrowseComp) must use upstream-provided decryption helpers; do not embed keys.
- Dataset downloads from HuggingFace must be capped (`primevul_paired_test_head.jsonl` ~5MB is a good rule).
- Never wire a benchmark that requires keys you don't have authorization to use.

## Anti-patterns

- LLM judges in the validator. Disqualifying — the loop must trust scorecards.
- Validators that depend on the agent's exact phrasing for non-trivial answers. Use multi-keyword grep, not single-substring.
- Tasks that require `apt-get`, `sudo`, Docker compose, or persistent system mutation. Skip.
- Wrapping the entire upstream task set without sampling. Pick 5-12 cleanest.
- Forgetting the smoke test. Always run a single task end-to-end before reporting "wired."

## Reference implementations

All under `~/.hermes-sandbox/harness/benches/`:

- `bfcl/` — BFCL v3 multi-turn, official checker, Apache 2.0
- `freshqa/` — FreshQA false-premise + fast-changing, Apache 2.0
- `polyglot/` — Aider Polyglot 4-language, Exercism MIT
- `browsecomp/` — BrowseComp w/ SHA-XOR decryption, MIT
- `primevul/` — PrimeVul paired vuln/patched, MIT
- `terminal-bench/` — Terminal-Bench cherry-pick (8 tasks), Apache 2.0
- `tau2/` — τ²-bench retail (single-shot mode), MIT
- `mermaidseq/` — MermaidSeqBench DIY 8-feature, paper-derived

Each has loader + sample_tasks + README following the schema above.
