---
name: self-evolve-personality-skills_KM
description: >-
  Use when Kosta wants to create, test, or iteratively improve a contextual writing-voice/personality skill — email voice, professor/lab voice, friend text voice, official/admin tone, outreach voice, or any persona/style skill — using generator/reviewer/patcher agents, exemplar corpora, style rubrics, held-out benchmarks, and plateau-based self-evolution.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
    - claude-hermes
  hermes:
    command_priority: 432
---
# Self-Evolve Personality Skills

Use this to build and improve **contextual voice skills**, not one monolithic "Kosta voice." The goal is a reusable skill that helps an agent write in the right register for a situation while preserving facts, intent, and boundaries.

Good targets: `kosta-email-lab`, `kosta-email-official`, `kosta-email-friends`, `kosta-text-casual`, `kosta-cold-outreach`, `kosta-professor-reply`. Avoid one giant voice skill unless the user explicitly wants it.

## Core architecture

Run a fresh-context loop with three separated lanes:

1. **Generator** — reads only the candidate personality skill plus the task batch. It writes outputs as if it were the future agent using the skill.
2. **Reviewer** — reads the exemplar corpus, rubric, task specs, and outputs. It scores fidelity and names concrete misses with quotes.
3. **Patcher** — reads the candidate skill and aggregate reviewer findings. It edits the skill, but it does not see hidden holdout exemplars directly.

Restart or spawn fresh agents every loop. Do not let the generator slowly learn Kosta's voice from conversation residue; the only persistent knowledge should be the skill under test.

## Run root

Create a sandbox before changing any canonical skill:

```text
~/.hermes/evolution-runs/personality-skills/YYYYMMDD-HHMMSS/<target-skill>/
  SPEC.md
  corpus/
    train/
    dev/
    holdout/
    README.md
  skill-original/
  skill-candidate/
  benchmark/
    tasks.jsonl
    rubric.json
    judge_prompt.md
    generator_prompt.md
    patcher_prompt.md
  iteration-001/
    generator_outputs.jsonl
    review.json
    patch.diff
    score.json
  SUMMARY.md
```

Keep private emails/messages local. Redact or exclude secrets, addresses, health details, student info, unpublished research, and anything Kosta would not want copied into a benchmark artifact.

## Corpus design

Use real examples when Kosta provides them or when authorized local/email/docs access exists. Otherwise start with synthetic tasks and mark the corpus as weak.

Split examples by audience and situation:

- friend / casual text
- professor / PI / lab
- administrative / official
- collaborator / peer scientist
- vendor / support
- cold outreach / networking
- apology / delay / scheduling / refusal / follow-up

For each exemplar, save metadata without overloading the skill body:

```json
{
  "id": "lab-followup-001",
  "audience": "professor",
  "channel": "email",
  "relationship": "PI/advisor",
  "purpose": "follow up after delay",
  "stakes": "medium",
  "register": "warm-professional",
  "source": "user-provided",
  "text_path": "corpus/train/lab-followup-001.txt"
}
```

## Skill shape

A personality skill should contain compact operational guidance, not a dump of examples.

Recommended structure:

```text
SKILL.md
references/
  voice-model.md        # audience-specific style rules and anti-patterns
  examples-index.jsonl  # metadata only, no huge bodies unless needed
  rubric.md
assets/
  task-batches.jsonl
```

`SKILL.md` should answer:

- When this voice applies and when it does not.
- What the output should preserve from the user's intent.
- How register changes by audience.
- What Kosta's voice tends to do: sentence shape, directness, warmth, hedging, signoffs, punctuation, density.
- What Kosta's voice avoids: corporate filler, fake warmth, over-polished grammar, invented details, over-apology, unnecessary exclamation points, stiff templates.

Do not include private exemplar text in always-loaded `SKILL.md`. Keep examples in local-only references and load them only during evolution or when Kosta explicitly asks.

## Benchmark task design

Build 20-40 tasks for a serious run. Include both common and adversarial cases:

- quick scheduling reply
- professor update after a delay
- official administrative request
- warm friend text
- concise vendor/support escalation
- polite refusal
- ambiguous draft that needs cleanup without changing intent
- emotionally loaded message where over-apology would be bad
- high-stakes email where invented facts are dangerous
- message where Kosta wants brevity, not polish

Each task should define:

```json
{
  "id": "professor-delay-003",
  "audience": "professor",
  "channel": "email",
  "prompt": "Write the email from these facts...",
  "facts": ["..."],
  "must_preserve": ["..."],
  "must_not_invent": ["..."],
  "style_target": "warm-professional, concise, accountable but not groveling",
  "max_words": 180,
  "split": "dev"
}
```

Keep a held-out split. The generator and patcher never see hidden exemplar bodies or judge notes for holdout cases.

## Reviewer rubric

Score 0-5 per dimension, then compute a weighted 0-100 score:

- **Voice fidelity**: sounds like Kosta for this audience, not generic polished AI.
- **Audience/register fit**: friend vs professor vs official tone is correctly shifted.
- **Intent preservation**: keeps the user's actual ask, constraints, and emotional posture.
- **Fact discipline**: invents nothing; does not silently strengthen/weaken claims.
- **Naturalness**: human rhythm, contractions/fragments where appropriate, no sterile template feel.
- **Brevity/density**: concise without becoming abrupt; no filler.
- **Boundary handling**: asks when missing facts block a sendable draft; otherwise makes reasonable low-risk assumptions.
- **Anti-pattern avoidance**: no corporate filler, over-apology, generic praise, fake enthusiasm, or excessive signoff ceremony.

Auto-fail any output that invents factual content, includes private details not in the task, changes the relationship/stakes, or sounds like a generic customer-service template.

## Loop policy

Default: 10-30 loops, stop after 4 plateau loops, or follow Kosta's requested budget such as 50 loops.

A loop is valid only if it:

1. runs all current dev tasks and at least a rotating sample of train tasks;
2. keeps holdout examples hidden from generator/patcher;
3. records scores and reviewer quotes;
4. patches only the candidate skill/reference files;
5. reruns at least the failed cases after patching.

Only make the benchmark harder when the dev score is stable. Add new tasks for uncovered registers instead of just making the skill more verbose.

## Agent prompts

Use the bundled prompt templates:

- `references/generator-prompt.md`
- `references/reviewer-prompt.md`
- `references/patcher-prompt.md`

The controller fills placeholders with paths and task batches. Keep prompts outcome-focused; do not ask agents to reveal chain-of-thought.

## Applying results

When the loop converges:

1. Compare `skill-original/` vs `skill-candidate/`.
2. Inspect every hunk. Reject bloat and private exemplar leakage.
3. Run the benchmark one final time on dev plus holdout.
4. Apply approved changes to canonical Skillshare source.
5. Run `skillshare sync -g --json`.
6. Load the installed skill with `skill_view` from Hermes GPT.
7. Commit Skillshare source if it is git-backed.

Final report: target skill, run root, iteration count, best score, plateau reason, changed files, verification, and what audience/register remains weakest.
