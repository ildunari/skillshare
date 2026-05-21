---
name: workflow-protocols
description: >
  Micro-protocols for common engineering workflows: CI/build failure triage, incremental refactoring,
  API/SDK freshness verification, and context window management. Use when tests/CI/build/lint fails
  (ci-triage), when doing refactors/migrations/multi-file changes (minidiff), when implementing or
  debugging anything that depends on external APIs/SDKs/tools (research-freshness), or when the
  session is long and context needs management (context-control).
---

# Workflow Protocols

Four lightweight protocols for common engineering situations. Each is self-contained.

---

## 1. CI Triage

Use when tests/CI/build/lint fails.

### Workflow

1) **Reproduce** — Run the smallest command that reproduces it locally. If it only fails in CI, replicate the CI environment as closely as possible (OS, node/python version, env flags).

2) **Pin the failure** — Capture:
   - the exact failing command,
   - exit code,
   - the shortest failing excerpt that proves the failure (avoid dumping megabytes),
   - the CI job name and runner image/version when available.

3) **Identify the smallest fix** — Do not "fix" by broad reformatting or updating unrelated dependencies unless necessary.

4) **Validate** — Re-run the failing command, then the next nearest test target (unit suite or lint) to ensure no regressions. If the failure is CI-only, run the closest local equivalent and note the gap.

### Reporting

End with:
- What failed and why (one paragraph).
- What changed (files + intent).
- What ran (commands + pass/fail).
- If you changed versions, include the before/after.
- If CI-only, include the most likely cause and the exact signal you used.

---

## 2. Minidiff Refactor

Use for refactors/migrations/multi-file changes. Enforce incremental steps, tiny diffs, and continuous compilation/tests.

### Rules of Engagement

- Split work into mechanical steps that keep the project running between each step.
- Prefer "introduce new path, then switch callers, then delete old path" over a big-bang rewrite.
- Keep diffs reviewable: small patches, isolated concerns.
- Avoid mixed concerns; one refactor axis per step.

### Checklist

- Compile/build after each step (or run the closest equivalent).
- Run unit tests for touched areas.
- Use `/diff` and `/review` before considering the work "done."
- If there is no test coverage, add a minimal smoke test or runnable check.

### Output

Summarize: steps performed, key diffs, tests run, any follow-ups you intentionally deferred.

---

## 3. Research Freshness

Use when implementing or debugging anything that depends on external APIs/SDKs/tools and must be current.

Treat this as the "you don't get to guess" workflow.

### When to Invoke

Any time you are about to:
- write code that calls an external API or SDK,
- change build tooling, CLIs, or deployment scripts,
- migrate versions,
- rely on a flag, config key, or command you are not 100% certain is current.

### Tool Stack (in order)

1) **First-party web search** — Use first for "what changed recently" and broad recall.
2) **Context7** — Use for exact API signatures and versioned docs pages. Prefer official vendor docs and release notes.
3) **Exa** — Use as a quality override when first-party results are noisy or incomplete.
4) **Firecrawl** — Use only when you must extract content from JS-heavy sites or long pages. Extract the smallest relevant section.

### Anti-Hallucination Rules

- If you cannot verify a symbol/flag/endpoint from docs or real examples, do not use it.
- Prefer "show me the exact snippet / version line" over paraphrase.
- Confirm versions explicitly (package.json, lockfile, --version output, release note date).

### Output ("Freshness Receipts")

At the end of the task report, include:

```
Freshness receipts:
- Source: <doc URL or release note>  Version/date: <...>  Notes: <1 line>
- Source: <...>
```

---

## 4. Context Control

Use when the session is long or tool output is huge. Keep context lean.

### Tools to Use Selectively

- Use `/compact` only when context feels too heavy; do not auto-compact.
- `/fork` to explore alternatives without polluting the main thread.
- `/status` to confirm token usage, model, and writable roots.
- Tune `tool_output_token_limit` if you keep hitting "missing logs" vs "too much noise".

### Output Discipline

- Prefer targeted outputs: grep, tail, file+line references.
- If a log is large, summarize and point to the exact command/file/line that matters.
- Keep a short "state of play" paragraph in the transcript when the task spans multiple turns.

### Hand-off

When stopping mid-task, leave: current status, what's already verified, the next single command to run.
