# Self-Evolve Codex Goal

## Objective

Improve `[target name/path]` on `[metrics]` without changing the protected intent.

## Target

- Canonical source:
- Candidate copy:
- Editable surface:
- Read-only benchmark fixtures:

## Metrics

- Required checks:
- Primary score:
- Secondary score or token/runtime measure:
- Behavioral eval prompts:

## Limits

- Maximum iterations:
- Wall-clock budget:
- Parallelism:
- Protected clauses:
- External side effects allowed:

## Stop Conditions

Stop when any of these is true:

- target score is reached;
- max iterations or wall-clock budget is reached;
- plateau rule fires;
- further improvement requires changing the metric, protected intent, or product contract;
- a safety boundary or dependency blocker prevents honest progress.

## Loop

1. Run and record the baseline.
2. Inspect the largest failure.
3. Make one focused candidate change.
4. Re-run the same benchmark.
5. Keep, discard, or revise based on score and artifact evidence.
6. Log every iteration in `RUNLOG.md` and `metrics.jsonl`.
