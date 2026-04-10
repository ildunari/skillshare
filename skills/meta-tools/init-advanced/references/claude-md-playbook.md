# CLAUDE.md Playbook

Use this reference when drafting `CLAUDE.md`.

## Purpose
`CLAUDE.md` is the standing instruction file for Claude Code. It should help Claude act effectively in the repository without drowning it in excessive instructions.

## Recommended structure

A practical shape is:
- `# Project: ...`
- `## Stack`
- `## What this project does`
- `## Key directories`
- `## Commands`
- `## Conventions`
- `## Workflow`
- `## What to read before complex tasks`

Use a tighter variant if the repo is small.

## Writing rules

1. **Keep it concise**
   Favor a short, high-signal file over a giant handbook.

2. **Use softer conditional language**
   Prefer wording like:
   - "Use X when Y, because Z"
   - "Before changing A, read B"
   - "If a task touches C, run D"

3. **Explain non-obvious constraints**
   Claude generalizes better when it understands why a rule exists.

4. **Frame constraints positively when possible**
   Say what to do, not just what to avoid.

5. **Pair hard prohibitions with alternatives**
   If something is off-limits, say what Claude should do instead.

6. **Use progressive disclosure**
   Link to deeper docs instead of placing too much detail in the file itself.

## Good content

Include:
- exact validation commands,
- major directories and their purpose,
- approval gates for destructive or high-risk actions,
- testing expectations,
- generated-code boundaries,
- references to deeper docs for complex subsystems.

## Size guidance

As a default target:
- medium single-repo `CLAUDE.md`: about 40-80 lines
- smaller repos: keep it tighter
- monorepo root files may be longer, but do not turn the file into a handbook

## Avoid

Avoid:
- all-caps emphasis except for genuine safety-critical hard stops,
- long anti-laziness language,
- huge command dumps with no guidance,
- copying AGENTS.md line for line.

## Calibration reminder

Claude-specific files should usually be:
- calmer in tone,
- more conditional,
- more explicit about why rules exist,
- lighter on rigid universal commands,
- easier to skim during live coding sessions.
