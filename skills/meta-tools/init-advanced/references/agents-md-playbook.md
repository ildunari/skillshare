# AGENTS.md Playbook

Use this reference when drafting `AGENTS.md`.

## Purpose
`AGENTS.md` is the durable instruction layer for Codex / GPT-style coding agents.
It should preserve the project facts and behavioral boundaries that need to survive long sessions and context compaction.

## Recommended structure

Use a compact markdown structure like:
- `# Project: ...` (optional)
- `## Context`
- `## Commands`
- `## Architecture`
- `## Working Agreements`
- `## Constraints`
- `## Output Expectations` (optional)
- `## What to read before complex work` (optional)

Adapt section names if the repo already uses a better local pattern.

## Writing rules

1. **Use direct language**
   GPT-family models do better with simple instructions and explicit scope limits.

2. **Prefer invariants over procedures**
   Put durable project truths here. Move long workflows into skills or linked docs.

3. **Add done conditions**
   Examples:
   - Stop after implementing the requested change.
   - Do not refactor adjacent code without approval.
   - Run the relevant test command before finishing.

4. **Constrain scope explicitly**
   GPT-family agents often overbuild unless told where to stop.

5. **Use grounded commands only**
   Every command should be runnable as written or clearly labeled as an example / assumption.

6. **Separate approval levels clearly**
   Distinguish between:
   - normal autonomous actions,
   - actions that require approval,
   - forbidden actions.

## Good content

Include:
- project purpose,
- real commands,
- package boundaries,
- generated-code or vendored-code warnings,
- approval gates,
- project-specific review and testing norms,
- paths to deeper docs when the repo is large.

## Size guidance

As a default target:
- medium single-repo `AGENTS.md`: about 60-120 lines
- smaller repos: shorter is better
- monorepo root files may be longer, but only when the extra complexity is real

## Avoid

Avoid:
- personality padding,
- generic "be thoughtful" instructions,
- giant checklists for tasks the model already knows how to do,
- repeating linter rules already enforced elsewhere,
- overlong prose that crowds out the truly important rules.

## Monorepo guidance

For monorepos:
- put cross-repo rules at the root,
- put package-specific constraints near the package,
- avoid duplicating root instructions into every subproject file,
- call out shared libraries and downstream impact zones.
