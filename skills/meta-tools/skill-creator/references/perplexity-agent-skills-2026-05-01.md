# Perplexity Agent Skills design guide — distilled notes

Source: https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity
Read date: 2026-05-08

## Core thesis

Skills are not ordinary documentation or code. They are context architecture for models: a folder of routing metadata, concise loaded instructions, and progressively loaded runtime resources. Good skills optimize for the agent's failure modes, not for human tutorial completeness.

## High-value principles

- A skill is a directory, not just `SKILL.md`: use `scripts/` for deterministic repeated logic, `references/` for heavy conditional docs, `assets/` for templates/schemas, and optional config for first-run setup.
- The description is a routing trigger, not a summary. It should say when to load the skill, preferably in language users actually type. Good descriptions are terse, often starting with "Load when..." and usually target 50 words or fewer.
- Skill loading is progressive. Index cost is paid every session, loaded `SKILL.md` cost is paid after trigger, and runtime files are paid only when read. Put unbounded details in runtime files.
- Every sentence is a tax. Ask: "Would the agent get this wrong without this instruction?" If not, delete or move it out of the loaded body.
- Write evals before or alongside the skill. Include positive trigger cases, near-miss negative cases, and known failures. Negative examples are especially powerful because skills can hurt other skills by loading off-target.
- The body should not recite obvious commands. It should carry durable taste, gotchas, boundary conditions, and judgment the model would otherwise miss.
- Gotchas are the highest-value maintenance surface. After shipping, prefer appending targeted gotchas over rewriting the routing description or bloating the workflow.
- Description changes after merge are risky. If you change routing text, add or update routing evals, including negatives for adjacent skills.
- Run multiple eval types when possible: routing/load precision and recall, accessory-file read checks, and end-to-end task completion. For broadly deployed skills, test across model families because GPT/Sonnet/Opus may route differently.

## Review checklist derived from the article

1. Need: Does this skill solve a durable failure, taste gap, hidden workflow, or consistency issue? If it only documents commands the model already knows, it should probably not exist.
2. Routing: Does the description describe user intent and trigger phrases rather than summarizing the body? Is it short enough for index cost?
3. Boundaries: Are adjacent-skill or no-skill near misses covered by negative evals?
4. Loaded body: Does every sentence prevent a likely failure? Are obvious tutorials removed?
5. Progressive disclosure: Are heavy conditionals moved into `references/`, deterministic repeated work into `scripts/`, and templates into `assets/`?
6. Gotchas: Are known failures captured as concise negative guidance?
7. Maintenance: Are description changes backed by routing evals? Are gotcha additions kept append-mostly and small?
