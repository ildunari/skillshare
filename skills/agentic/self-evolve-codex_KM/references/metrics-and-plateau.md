# Metrics And Plateau Rules

Self-evolution is only useful when the score is honest enough to steer the loop.

## Metric Stack

Use a layered score:

1. **Required checks**: frontmatter parses, files exist, links resolve, scripts compile, tests pass.
2. **Structural eval**: plugin-eval or skill-specific linter scores token cost, trigger quality, progressive disclosure, and broken references.
3. **Behavioral eval**: realistic prompts that compare original and candidate behavior.
4. **Human or judge review**: only for qualities that deterministic checks cannot capture.

For Codex skills, default to:

```bash
plugin-eval analyze <candidate-skill-path> --brief-out <run-root>/iteration-XXX/brief.json
```

Add task-specific commands when available, such as unit tests, `python -m py_compile`, or trigger evals.

## Score Record

Append one JSON object per iteration to `metrics.jsonl`:

```json
{
  "iteration": 1,
  "timestamp": "2026-05-12T00:00:00Z",
  "candidate": "iteration-001",
  "primary_score": 84,
  "required_checks": "pass",
  "token_cost_delta": -1200,
  "runtime_seconds": 42,
  "decision": "keep",
  "reason": "Fixed broken references and lowered invoke cost without losing routing clarity"
}
```

If the tool reports token usage or duration, record it. If it does not, write `null` rather than inventing a number.

## Plateau Rule

Use one of these unless the user specifies another:

- **Score plateau**: stop after 3 consecutive completed iterations improve the primary score by less than 2 points total.
- **Win plateau**: stop after 3 consecutive discarded candidates.
- **Time plateau**: stop 10 minutes before the requested wall-clock budget ends so there is time to collect artifacts and report.
- **Complexity plateau**: stop when further score gains require changing the product contract, benchmark, or protected clauses.

When the user says "max 20 runs or until plateau", translate it to:

```text
Run at most 20 scored iterations. Stop earlier if 3 consecutive completed iterations fail to improve the primary score by at least 2 points total, or if the best remaining ideas require changing the metric or protected intent.
```

## Goodhart Guardrails

Do not optimize only the visible score. Every run should preserve:

- the user's intent and protected constraints;
- simple, readable instructions;
- low trigger/invoke cost when quality is equal;
- safety boundaries for destructive, external, or shared writes;
- real behavior on at least one task prompt.

If the score improves but the skill becomes less trustworthy, mark the candidate `discard` and record why.
