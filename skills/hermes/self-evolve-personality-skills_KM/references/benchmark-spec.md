# Personality self-evolve benchmark spec

## Splits

- `train`: examples/patterns the patcher may learn from.
- `dev`: tasks used for ordinary loop scoring.
- `holdout`: private tasks/exemplars the generator and patcher do not see. Reviewer can use them for scoring.

Never let the patcher see holdout exemplar bodies or hidden judge notes.

## Task JSONL schema

```json
{
  "id": "professor-delay-003",
  "audience": "professor",
  "channel": "email",
  "relationship": "PI/advisor",
  "purpose": "follow up after delay",
  "prompt": "Write the email from these facts...",
  "facts": ["..."],
  "must_preserve": ["..."],
  "must_not_invent": ["..."],
  "style_target": "warm-professional, concise, accountable but not groveling",
  "max_words": 180,
  "split": "dev"
}
```

## Recommended task mix for Kosta

For 20 tasks:

- 4 professor/lab updates
- 3 administrative/official emails
- 3 collaborator/peer scientist emails
- 3 friend/casual messages
- 2 vendor/support messages
- 2 refusal/boundary messages
- 2 scheduling/rescheduling messages
- 1 emotionally loaded apology/delay message

For 40 tasks, double the mix and add high-stakes no-invention cases.

## Score aggregation

Use weighted score out of 100:

```json
{
  "voice_fidelity": 0.22,
  "audience_register_fit": 0.16,
  "intent_preservation": 0.16,
  "fact_discipline": 0.16,
  "naturalness": 0.12,
  "brevity_density": 0.08,
  "boundary_handling": 0.05,
  "anti_pattern_avoidance": 0.05
}
```

Auto-fail overrides aggregate score.

## Plateau

Plateau if the best dev score improves by less than 1.0 point for 4 consecutive loops and no auto-fail category is newly fixed. If holdout score drops by more than 3 points while dev improves, suspect overfitting and revert the last patch.
