---
name: project-context-seeder
description: >
  Create, review, audit, rewrite, or holistically refresh AGENTS.md, CLAUDE.md,
  or equivalent AI-coding instruction files for a repository, monorepo, package,
  or subproject. Use this when the user wants project-wide AI coding guidance,
  wants to compare existing agent docs against the real repo, wants to prepare a
  codebase for Claude Code/Codex/AI-assisted development, or wants equivalent
  outputs such as `.cursorrules` or Copilot-style instructions from grounded repo
  analysis. Trigger for requests like "make an AGENTS.md", "review my CLAUDE.md",
  "set up this repo for Codex", or "prepare this codebase for AI agents" even if
  the user does not mention exact file names. Do not use for tiny targeted edits
  like fixing a typo, adding one rule, removing one section, or updating a single
  command. Use it only for create/rewrite/review/audit/whole-file refresh work.
---

# Project Context Seeder

Create grounded, high-utility `AGENTS.md` and `CLAUDE.md` files for real repositories.

This skill is the instruction-first replacement for deterministic generators that only
extract static facts or require provider-specific API setup. It accepts a detailed user
prompt, maps the repository, determines what evidence matters, asks only for missing
strategic context, and then writes two **different** instruction files:

## Routing table

| If the user wants... | Use this skill? | Notes |
|---|---|---|
| New `AGENTS.md` / `CLAUDE.md` files | Yes | Fresh create |
| Audit or rewrite stale agent docs | Yes | Review against repo reality |
| Equivalent AI-instruction outputs (`.cursorrules`, Copilot-style guidance) | Yes | Same grounding workflow |
| One tiny edit to an existing instruction file | No | Too narrow; treat as normal edit work |
| General repo analysis unrelated to agent instructions | No | Use a more appropriate analysis workflow |

For more trigger examples and edge cases, read `references/routing-examples.md`.

- `AGENTS.md` for Codex / GPT-style coding agents
- `CLAUDE.md` for Claude Code

Do **not** treat these as shallow format variants of the same text. They share source
facts, but they serve different models and need different writing strategies.

## Core operating principles

1. **Ground first, then guide.**
   Collect high-confidence facts from the repository before drafting rules. Commands,
   stack choices, package boundaries, and directory roles should come from evidence,
   not guesswork.

2. **Ask only for missing strategy.**
   Ask the user about things the repository cannot reveal reliably: team preferences,
   review gates, deployment risk, autonomy level, approval rules, or model-specific tone.
   Do not ask for facts you can inspect directly.

3. **Separate facts from policy.**
   Repository facts belong in stack, commands, structure, and architecture sections.
   Human preferences belong in constraints, workflow, and boundaries sections.

4. **Different surface, different prompt.**
   `AGENTS.md` should be optimized for Codex / GPT behavior.
   `CLAUDE.md` should be optimized for Claude behavior.
   Reuse the same evidence, but rewrite for the target model family.

5. **Never invent hidden conventions.**
   If a command, workflow rule, or architectural boundary cannot be verified, either:
   - omit it,
   - mark it as an assumption needing confirmation, or
   - ask the user directly.

6. **Explain the model-surface difference in practice.**
   GPT-family agent files usually need sharper scope limits, explicit stop conditions, and clearer approval boundaries.
   Claude-oriented files usually benefit from concise workflow framing, conditional guidance, and rationale for non-obvious rules.
   Do not make the files different only in tone; make them different in operational guidance.

## The workflow

All `references/` paths in this skill are relative to the directory containing this `SKILL.md` file.

### Phase 1 — Intake

Start by collecting the minimum useful context.

Read `references/intake-template.md` and use it to determine:
- what the user wants these files to accomplish,
- whether this is a whole repo or a subproject,
- whether they want fresh files, a rewrite, or an audit,
- whether they prefer strict or proactive agent behavior,
- whether there are existing instruction files to preserve or replace.

If the user has already given a detailed brief, do not ask redundant questions.

### Phase 2 — Repository mapping

Read `references/repo-analysis-checklist.md` and inspect the repo.

Your goal is to build a compact, evidence-backed model of:
- languages and frameworks,
- package managers and build tools,
- build / test / lint / run commands,
- project layout and major directories,
- monorepo or multi-app boundaries,
- risky areas, generated code, vendored code, or forbidden zones,
- docs and context files worth reading before drafting.

Prefer deterministic evidence sources:
- `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `justfile`,
  Docker files, CI workflows, and repo docs
- top-level directories and obvious entry points
- existing `AGENTS.md`, `CLAUDE.md`, and neighboring context docs if present

For large repos, inspect selectively. You do not need exhaustive coverage; you need
sufficient signal to write trustworthy instructions.

Default stopping rule:
- Start with top-level docs, manifests, CI, and existing instruction files.
- Then inspect only enough representative implementation files to understand the app shape,
  command surface, and risky areas.
- As a default heuristic, read roughly 10-20 high-value files total before drafting.
- If the repo is huge, prioritize manifests, CI, entry points, and package-level READMEs over
  deep source sampling.
- If evidence remains weak after that pass, say so explicitly and label the weak points rather
  than pretending certainty.

### Phase 2.5 — Evidence gate

Before drafting, verify you have enough evidence to proceed responsibly. As a minimum, try to read:
- one build or package manifest,
- one CI config or project README,
- and one representative source file or package-level README.

If one of those categories does not exist, say so explicitly instead of pretending the repo exposed it.

### Phase 3 — Decide the file strategy

Choose one of these paths:

| Condition | Strategy |
|---|---|
| No usable instruction files exist yet | **Fresh create** |
| Existing files exist, but many commands/facts/rules are stale, generic, or misleading | **Rewrite** |
| Monorepo or multi-package repo where some packages genuinely differ in stack, commands, risk, or workflow | **Layered update** |
| Existing files are mostly correct and need selective tightening, recalibration, or cleanup | **Audit + patch** |

State your chosen path briefly before drafting.

When rewriting existing files, re-verify every command, path, and architectural claim before carrying it forward. Do not preserve any old claim you cannot re-confirm from the repo or the user.
For non-inspectable policy claims in existing files — such as review conventions, deployment habits, or team workflow rules — ask the user before silently preserving or discarding them.

### Phase 4 — Draft `AGENTS.md`

Read `references/agents-md-playbook.md` and `references/example-output.md` before drafting.

Write `AGENTS.md` for Codex / GPT agents using these rules:
- Use a clear markdown structure that covers context, commands, architecture, working rules, constraints, and output expectations as needed.
- Keep the file focused on **invariants**: project context, key commands,
  package boundaries, constraints, workflow defaults, and output expectations.
- Put durable project rules in the file, not ephemeral session state.
- Use direct, simple language. Avoid personality padding.
- Add explicit scope limits so GPT-family agents do not overbuild.
- Distinguish clearly between:
  - things always allowed,
  - things that require approval,
  - things never allowed.
- If the repo is a monorepo, describe root rules separately from package-specific rules.
- Keep procedural overload low. If a long step-by-step workflow is needed, recommend a skill
  or supporting doc instead of bloating `AGENTS.md`.

### Phase 5 — Draft `CLAUDE.md`

Read `references/claude-md-playbook.md` and `references/example-output.md` before drafting.

Write `CLAUDE.md` for Claude Code using these rules:
- Keep it concise, practical, and easy to obey.
- Use WHAT / WHY / HOW organization when helpful.
- Prefer softer conditional guidance with rationale rather than aggressive emphasis.
- Frame constraints positively when possible.
- Include approved alternatives for hard prohibitions.
- Point Claude to deeper docs instead of dumping too much detail inline.
- Include the exact commands Claude should run when practical.
- Be explicit about risky areas, generated code, approval gates, and verification expectations.

### Phase 6 — Reconcile and verify

Before presenting or writing files, ensure:
- commands are real,
- file paths exist,
- architecture notes reflect the current repo,
- `AGENTS.md` and `CLAUDE.md` agree on facts,
- they differ appropriately in calibration and wording,
- any assumptions are labeled.

Then use `references/output-template.md` as the delivery format.

Use this confidence protocol while drafting:
- `[verified]` for commands, paths, or rules directly confirmed from the repo or user
- `[inferred]` for strong conclusions drawn from multiple repo signals
- `[assumed]` for points that could not be proven and need confirmation

Do not overuse these labels everywhere. Apply them to claims that materially affect workflow, safety, or correctness.

## File placement conventions

Unless the user asks for a different placement:
- Single-repo projects: write `AGENTS.md` and `CLAUDE.md` at the repo root.
- Monorepos: write root files at the repo root, and write scoped package-level files at the relevant package root, e.g. `packages/api/AGENTS.md`.
- Only add scoped package-level files when the package meaningfully differs from the root in at least two of these dimensions: primary language, build system, test runner, deployment target, CI pipeline, or risk/workflow constraints.
- If a package differs in only one minor way, prefer a short note in the root file instead of creating a new scoped file.

## Writing rules for each file

Use the playbooks as the authoritative source for structure, tone, and size:
- `references/agents-md-playbook.md`
- `references/claude-md-playbook.md`

Before drafting either file, read the relevant playbook and follow it rather than relying on memory.

## How to use the user's detailed prompt

Treat the user's brief as a **policy overlay**, not as ground truth about the repo.

Use it to shape:
- desired agent autonomy,
- tone and depth,
- review strictness,
- testing expectations,
- team practices,
- output preferences,
- what the files are supposed to optimize for.

Do not let the brief overwrite inspectable facts unless the user explicitly says the repo is
in transition and wants the files to describe the target state.

## Clarifying question threshold

Ask follow-up questions only when one of these is true:
- the user wants behavior that the repo cannot imply,
- multiple contradictory workflows exist,
- existing files conflict with the requested direction,
- approval rules or destructive-action rules are unclear,
- the requested scope spans multiple subprojects with different owners.

Otherwise, proceed.

## Anti-patterns

Never:
- output the same prose into both files with tiny wrappers,
- invent commands from framework stereotypes,
- infer architecture solely from directory names when files contradict it,
- dump every discovered fact into the instruction files,
- write universal commandments that ignore repo-specific reality,
- overload `CLAUDE.md` with giant reference manuals,
- overload `AGENTS.md` with long procedures better handled by skills or docs.

## Suggested deliverables

Depending on the user's request, produce one or more of:
- `AGENTS.md`
- `CLAUDE.md`
- a short audit report explaining weaknesses in existing files
- a root file plus scoped subproject files
- supporting docs when the project needs progressive disclosure

## Report structure

When presenting results, use this order:
1. Brief repo summary
2. File strategy chosen
3. `AGENTS.md` draft or audit findings
4. `CLAUDE.md` draft or audit findings
5. Assumptions and follow-ups

If you are writing files directly, still summarize the key decisions before or after the write.

## Example prompts this skill should handle

**Example 1 — fresh create**
User: "Map this repo and create a serious AGENTS.md plus CLAUDE.md for ongoing development."

**Example 2 — rewrite**
User: "These agent docs are generic and bad. Rewrite them so Codex and Claude both behave correctly."

**Example 3 — prompt-led initialization**
User: "I want agents to be proactive, but ask before infra changes or new dependencies. Analyze the repo and turn that into project instruction files."

**Example 4 — monorepo**
User: "Make root instructions for the monorepo and scoped instructions for the API package and web app."

## Final response checklist

When done, report:
- what you inspected,
- what files you created or changed,
- what assumptions remain,
- what the user should review next.
