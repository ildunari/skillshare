# Action Scoring

Every file or cluster should end with one primary recommendation.

## Action classes

- **KEEP** — unique, relevant, active, and justified
- **MERGE** — multiple files should become one canonical source with thin wrappers
- **EXTRACT** — long manuals, playbooks, or references should move out of always-loaded instructions
- **SPLIT** — one file is mixing standing rules with transient docs or setup notes
- **ARCHIVE** — stale but potentially useful historically
- **DELETE** — high-confidence junk, mirrors, vendor copies, or generated residue
- **REGENERATE** — generated artifact should come from a canonical source instead of manual edits
- **REWRITE** — prompt calibration or structure is wrong even if the file is unique

## Inputs to score

Use combinations of:
- path kind
- exact/near duplicate status
- load-stack impact
- directive count
- stale-hit count
- canonical-source confidence
- live file existence

## Reporting format

Each recommendation should include:
- action
- confidence
- risk
- estimated token savings
- estimated directive savings
- why this action was chosen

## Guardrail

Do not recommend DELETE purely because a file is large. Large and unique is an EXTRACT or SPLIT problem, not a delete problem.
