# GPT-5.5 Prompting Guidance

Current as of 2026-04-30. Primary sources: OpenAI GPT-5.5 docs and release notes.

## Primary sources

- OpenAI, “Using GPT-5.5”: https://developers.openai.com/api/docs/guides/latest-model
- OpenAI, “GPT-5.5 prompt guidance”: https://developers.openai.com/api/docs/guides/prompt-guidance/
- OpenAI, GPT-5.5 model page: https://developers.openai.com/api/docs/models/gpt-5.5
- OpenAI, “Introducing GPT-5.5” (2026-04-23; API/safeguards update 2026-04-24): https://openai.com/index/introducing-gpt-5-5/
- OpenAI, GPT-5.5 system card (2026-04-23; updated 2026-04-24): https://openai.com/index/gpt-5-5-system-card/
- OpenAI Cookbook, GPT-5-Codex prompting guide (2025-09-23): https://cookbook.openai.com/examples/gpt-5-codex_prompting_guide

## Core calibration

GPT-5.5 should not be treated as a drop-in prompt target for GPT-5.2/5.4-era stacks. Start from the smallest prompt that preserves the product contract, then tune with evals.

Use an outcome-first structure:

```markdown
## Outcome
What the model should accomplish.

## Success criteria
Observable conditions that make the task complete.

## Constraints
Scope limits, safety limits, allowed side effects, and forbidden actions.

## Evidence / grounding rules
What must be cited, verified, searched, or checked.

## Stopping rules
When enough context/evidence/tool use is enough.

## Output contract
Expected format, length, sections, schema, or UI artifact.
```

## What to change from older GPT-5.x prompts

- Remove legacy process scaffolding unless the process itself is the product requirement.
- Replace broad “be thorough / do not skip anything” with observable success criteria and stopping rules.
- Keep `MUST`, `NEVER`, and `ONLY` for true invariants: safety boundaries, schema requirements, required fields, and irreversible side-effect rules.
- Convert judgment calls into decision rules: “Ask for clarification only when missing context would materially change the answer or create risk.”
- Separate personality from collaboration style. Personality is tone; collaboration is when to ask, act, search, verify, or stop.

## Reasoning effort

GPT-5.5 supports `reasoning.effort`: `none`, `low`, `medium`, `high`, `xhigh`; `medium` is the default.

- Use `none` for latency-critical simple tasks that do not need multi-step reasoning.
- Use `low` for efficient search/planning/tool use when latency matters.
- Use `medium` as the default baseline.
- Use `high` when evals show quality gains on complex agentic/coding/research tasks.
- Use `xhigh` only for the hardest async/eval-limit tasks.

Do not raise effort to compensate for a vague prompt. Fix the outcome, evidence, and stopping rules first.

## Verbosity and final-answer shape

GPT-5.5 is concise and direct by default. Control final answer length with `text.verbosity` plus concrete output limits.

Useful patterns:

- `text.verbosity: low` for crisp product/chat responses.
- “For simple answers, use ≤2 sentences.”
- “For complex work, use: result first, changed files, verification, open risks.”
- Avoid relying only on “be concise”; specify what concise means for the surface.

## Tool use, preambles, and Codex caveat

For GPT-5.5 Responses workflows, short user-visible preambles can improve streaming UX before multi-step or tool-heavy work.

Do not apply that blindly to `gpt-5-codex`. The official GPT-5-Codex guide says it does not emit preambles, does not support `verbosity`, and performs best with minimal developer prompts, concise tool descriptions, and narrow tools.

Split guidance:

- `gpt-5-codex`: use the official minimal-prompt Codex pattern; no verbosity parameter; no preamble instruction.
- GPT-5.5 used in Codex-like agent surfaces: use GPT-5.5 outcome-first guidance plus Codex operational constraints; verify actual surface behavior because no separate GPT-5.5-Codex guide was found.

## Grounding and citations

For grounded tasks, specify:

- which claims need citations;
- acceptable source types;
- minimum evidence threshold;
- retrieval budget;
- missing-evidence behavior.

Good pattern: “Search up to 3 high-quality sources; stop early if 2 independent sources agree. If evidence is insufficient, say so and give the best-supported answer, not a categorical denial.”

## Structured outputs and cache-friendly layout

- Prefer API Structured Outputs over prompt-described JSON schemas where possible.
- Put stable policies, instructions, and examples before dynamic request context.
- Put per-request details near the end.
- Avoid changing dates/user-specific values in the static prefix unless the application requires them.
- GPT-5.5 knows the current UTC date; do not automatically add “Current date” boilerplate. Add explicit date/time context only for business timezone, policy-effective date, user-local date, or cutoff needs.
