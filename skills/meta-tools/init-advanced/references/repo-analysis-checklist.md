# Repository Analysis Checklist

Use this checklist to gather grounded evidence before writing instruction files.

## 1. Read the top-level signal files

Start with the files most likely to reveal the project's real operating model:
- `README.md`
- package or build manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.)
- test and lint configuration
- CI workflows
- top-level docs
- existing `AGENTS.md` / `CLAUDE.md`

## 2. Map the project shape

Determine:
- single app, library, service, or monorepo
- major top-level directories and what they contain
- likely entry points
- generated, vendored, or build-output directories to avoid editing

## 3. Extract commands

Prefer explicit commands from manifests, scripts, make targets, docs, and CI.
Capture exact commands for:
- install / bootstrap
- dev / run
- build
- test
- lint / format / typecheck
- package-specific verification commands when relevant

If multiple command systems exist, explain which ones are canonical and why.

## 4. Infer stack and boundaries

Identify:
- languages
- frameworks
- package manager(s)
- build tools
- testing tools
- deployment or infrastructure clues
- database / migration systems
- package or service boundaries

## 5. Read representative implementation files

Inspect enough source to answer:
- what this project actually does,
- how code is organized,
- whether conventions are layered, feature-based, package-based, or mixed,
- where risky logic lives.

Sample a few high-value files rather than everything:
- entry points,
- core modules,
- routing / API layers,
- shared utilities,
- representative tests,
- package-specific READMEs.

## 6. Capture only actionable rules

Good instruction-file content includes:
- exact commands,
- important directories,
- approval gates,
- generated code boundaries,
- verification expectations,
- where to read more before complex work.

Avoid clutter such as:
- every dependency,
- every folder,
- speculative architecture descriptions,
- generic advice that applies to all repos.

## 7. Resolve uncertainty honestly

If evidence is weak:
- mark the point as an assumption,
- reduce its strength in the final file,
- or ask the user.

Never turn weak evidence into a hard rule.

## 8. Sparse or confusing repo fallback

If the repo is sparse, contradictory, or unusually hard to read:
- say that explicitly,
- prioritize only the highest-confidence commands and structure,
- avoid pretending you understand workflows the repo did not reveal,
- ask the user only for the missing policy or product context that would unblock a trustworthy draft.
