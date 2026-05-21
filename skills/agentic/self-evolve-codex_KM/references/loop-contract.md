# Loop Contract

Use this reference to turn an open-ended self-improvement request into a bounded Codex goal.

## Goal Integration

If the environment exposes goal tools, use them:

1. Check whether a goal is already active.
2. Create a goal only when the user asked for a goal or a long-running self-improvement loop.
3. Put the durable objective, target, metrics, max runs/timebox, plateau rule, and stop conditions in the goal text.
4. Do not mark the goal complete until the finalist is applied or the run is explicitly stopped as blocked.

If the environment only supports slash commands, draft either:

```text
/goal Improve <target> on <metrics>. Run at most <N> iterations or until <plateau rule>. Keep a run log, benchmark every iteration, and stop when <done condition>.
```

or a `GOAL.md` file the user can pass to `/goal`.

## Run Root

Default layout:

```text
~/.codex/evolution-runs/self-evolve-codex/YYYYMMDD-HHMMSS/<target-name>/
  GOAL.md
  RUNLOG.md
  DECISIONS.md
  metrics.jsonl
  original/
  candidate/
  iteration-001/
    patch.diff
    eval-output/
    judge.md
  iteration-002/
  finalist/
```

Put dynamic state here, not only in chat. Long-running Codex work will compact; the run folder is the recovery point.

## Editable Surface

Borrow the autoresearch discipline:

- Identify one primary editable surface.
- Keep benchmark fixtures and scoring scripts read-only during the run.
- If a metric must change, snapshot the old metric and record the reason in `DECISIONS.md`.
- Make one meaningful change per iteration so score movement is interpretable.

For skill work, the editable surface is usually the candidate skill folder. For prompt work, it may be one prompt file plus its eval fixtures.

## Baseline First

The first run must score the original target. If the baseline command cannot run, stop and fix the harness or report the blocker. Do not start tuning without a baseline; otherwise there is no honest comparison.

## Candidate Policy

Keep a candidate when:

- primary score improves;
- a critical structural failure is fixed without hurting score;
- score is flat but token cost, complexity, or maintenance risk drops materially.

Discard or revert when:

- score worsens without a clear compensating fix;
- the candidate edits protected clauses;
- it broadens the scope or changes the benchmark;
- it adds generic prose, vague mandates, or unsupported tools.

## Applying Results

Only after the loop chooses a finalist:

1. Review the finalist diff against `original/`.
2. Apply the minimal approved hunks to the canonical source.
3. Re-run the same benchmark on canonical source.
4. Sync or publish only when validation passes and the user requested distribution.
