# Intake Template

Use this reference at the start of the skill.

## Goal
Determine the minimum extra context needed before drafting `AGENTS.md` and `CLAUDE.md`.

The repository can reveal technical facts. Ask the user only about policy, preferences, or target behavior.

## First-pass questions

Ask only the questions that are still unanswered after reading the user request.

1. **Scope**
   - Is this for the whole repository, one package, or a specific subfolder?

2. **Operation**
   - Do you want fresh files, a rewrite of existing files, or an audit first?

3. **Autonomy level**
   - Should agents default to acting, default to asking, or use a mixed strategy?

4. **Risk / approval gates**
   - What should always require approval? Examples: new dependencies, schema migrations, deleting files, changing CI, production infra changes.

5. **Team workflow**
   - Are there must-follow testing, review, release, or branching rules that the repo itself will not reveal?

6. **Target state vs current state**
   - Should the files describe the repo as it exists now, or the repo as you want it to become soon?

## Optional questions

Ask only if needed:
- Which models or tools do you care about most?
- Should the files optimize for solo work, team work, or both?
- Are there parts of the repo that are experimental, generated, vendored, or hands-off?
- Do you want concise files or richer files with more explanation?

## Decision rule

Proceed directly to repo mapping when the prompt already gives you enough to move:
- the scope is explicit or obvious from context,
- the user clearly wants fresh create vs rewrite/audit,
- and the autonomy posture is clear enough to draft responsibly.

At that point, ask only for missing strategic context the repo cannot reveal well, such as approval gates, team workflow, or target-state-vs-current-state intent.

Do not re-ask for technical facts that inspection can answer.

## Output from intake

Before moving on, summarize in 5 bullets max:
- scope,
- desired outcome,
- autonomy level,
- important approval gates,
- unresolved questions.
