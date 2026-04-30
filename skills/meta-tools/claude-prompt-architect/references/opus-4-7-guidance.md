# Claude Opus 4.7 Prompting Guidance

Current as of 2026-04-30. Primary sources: Anthropic docs, model notes, release notes, and Claude Code guidance.

## Primary sources

- Anthropic, “Prompting best practices for Claude 4 models” with Opus 4.7 section: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
- Anthropic, “What’s new in Claude Opus 4.7”: https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7
- Anthropic migration guide: https://docs.anthropic.com/en/docs/about-claude/models/migrating-to-claude-4
- Anthropic API release notes, Opus 4.7 launch (2026-04-16): https://docs.anthropic.com/en/release-notes/api
- Anthropic launch post (2026-04-16): https://www.anthropic.com/news/claude-opus-4-7
- Claude Code Opus 4.7 best practices (2026-04-16): https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code
- Anthropic model overview: https://docs.anthropic.com/en/docs/about-claude/models/overview

## Core calibration

Opus 4.7 is more literal, more direct, and more effort-sensitive than Opus 4.6. Existing 4.6 prompts are a decent starting point, but they should be re-baselined rather than blindly reused.

The practical rule: front-load task-specific context, prune evergreen prompt clutter, and tune `effort` before adding more words.

## Literalism and scope

Opus 4.7 will not reliably generalize a rule across every item unless the prompt says so. If a rule is global, make it global:

```text
Apply this requirement to every section and every generated file, not just the first example.
```

Avoid vague weakeners when behavior is required: “try to,” “if possible,” “consider,” “as appropriate.” Use them only when optionality is intended.

## Tone and warmth

Opus 4.7 is more direct and less validation-forward than Opus 4.6. That is useful for technical work, but customer-facing or coaching prompts should explicitly request warmth.

Good pattern:

```text
Use a warm, collaborative tone. Acknowledge the user’s framing briefly, then answer directly. Do not add generic reassurance.
```

## Context strategy

Do not use “minimal context” as a blanket rule.

- For Claude Code / agentic work, front-load first-turn context: intent, constraints, acceptance criteria, relevant files/locations, and allowed side effects.
- For persistent system/project instructions, prune aggressively. Broad evergreen instruction stacks still dilute compliance.
- Prefer examples and acceptance criteria over long generic checklists.

## Effort and thinking

Opus 4.7 uses adaptive thinking plus `output_config.effort`. Fixed thinking budgets are not supported.

Use:

```json
{
  "thinking": {"type": "adaptive"},
  "output_config": {"effort": "xhigh"}
}
```

Effort guidance:

- `xhigh`: default for serious coding, agentic, and multi-file tasks.
- `high`: minimum for intelligence-sensitive work.
- `medium`: cost-sensitive or well-scoped tasks.
- `low`: short, scoped, latency-sensitive work.
- `max`: hardest/high-stakes eval or reasoning tasks; expect overthinking and diminishing returns.

If reasoning is shallow, raise effort before adding prompt hacks like “think harder” everywhere.

## API/prompt architecture changes

- Opus 4.7 does not support fixed extended-thinking budgets like `thinking: {type: "enabled", budget_tokens: N}`.
- Non-default `temperature`, `top_p`, or `top_k` return API errors; steer style/determinism with prompts, examples, schemas, and evals instead.
- Tokenization changed. Re-benchmark prompt and context costs when migrating from 4.6.
- Use explicit dates/timezones when freshness matters. Unlike GPT-5.5, no official “current UTC date is already known” prompt rule was found.

## Tool use and subagents

Opus 4.7 tends to reason more and use tools/subagents less often by default than Opus 4.6. If tool use matters, specify when and why tools are required.

Good tool-use pattern:

```text
Before answering questions about current API behavior, check the official docs or release notes because stale API details create implementation bugs. If the docs do not resolve it, say what is uncertain.
```

Good subagent pattern:

```text
Work directly when the task fits in one coherent context. Spawn multiple subagents in the same turn when independent investigations can run in parallel or when isolated context materially reduces confusion or latency.
```

## Response length and progress updates

Opus 4.7 calibrates output length to perceived task complexity. For stable product behavior, specify the target shape with positive examples rather than “don’t be verbose.”

Official guidance says Opus 4.7 provides more regular progress updates in long agentic traces. Remove old “summarize every N tool calls” scaffolding unless the product still needs it; if it does, state the desired cadence and content briefly.

## Verification pattern

Opus 4.7 is stronger at verifying its own work, but prompts should still define the evidence required before declaring completion.

Good pattern:

```text
Before declaring the task complete, run or inspect the named verification path. Report the exact result and any remaining uncertainty.
```

## Migration checklist from Opus 4.6

- Replace fixed thinking budgets with adaptive thinking + effort.
- Remove non-default sampling parameters.
- Re-test prompts that rely on implicit generalization across lists/files/items.
- Re-tune tool and subagent triggers.
- Remove unnecessary warmth/validation scaffolding if directness is desired.
- Add warmth examples if directness is too blunt for the product.
- Re-benchmark token counts.
- Re-run evals before calling the migration complete.
