# Example Output Patterns

Use this file as a style calibration reference, not as boilerplate to copy blindly.

## Same repo fact, expressed differently

### Repo fact
- The project is a TypeScript web app with an API.
- Main validation commands are `npm test` and `npm run lint`.
- New dependencies and database migrations require approval.

### AGENTS.md style

```md
## Context
- TypeScript project with a web frontend and backend API.
- Prefer repo-root commands unless a package-specific command is explicitly required.

## Working Agreements
- Run `npm test` and `npm run lint` before finishing changes.
- Keep changes scoped to the requested task. Do not refactor adjacent areas without approval.

## Constraints
- Ask before adding dependencies.
- Ask before changing database migrations or CI workflows.
- Do not invent commands that are not present in the repo.
```

### CLAUDE.md style

```md
## What this project does
This is a TypeScript codebase with a web app and an API. Before making non-trivial changes, read the repo root docs and the package you are about to edit so your changes stay aligned with the current structure.

## Commands
- `npm test`
- `npm run lint`

## Workflow
Use `npm test` and `npm run lint` after meaningful changes because they catch the most likely regressions quickly.
If a task would add a dependency, change CI, or touch database migrations, pause and ask first rather than assuming that kind of change is routine here.
```

## Full minimal example pair

These are fuller examples showing overall structure for a small realistic repo.

### Example `AGENTS.md`

```md
# Project: Beacon API

## Context
- [verified] Node.js + TypeScript service for account, billing, and notification workflows.
- [verified] Main app code lives in `src/`; tests live in `tests/`.
- [inferred] Most routine feature work should stay inside one service area at a time.

## Commands
- [verified] `npm test`
- [verified] `npm run lint`
- [verified] `npm run build`

## Architecture
- [verified] `src/routes/` contains HTTP endpoints.
- [verified] `src/services/` contains business logic.
- [verified] `src/db/` contains database access and migration-related code.
- [assumed] Background jobs likely run from the worker entrypoint; confirm before changing job orchestration.

## Working Agreements
- Run `npm test` and `npm run lint` before finishing meaningful changes.
- Keep changes scoped to the requested task.
- Read the relevant service module before adding a new abstraction.

## Constraints
- Ask before adding production dependencies.
- Ask before changing CI or database migrations.
- Do not change generated files unless the task clearly requires regeneration.
- Stop after completing the requested change; do not broaden scope without approval.

## What to read before complex work
- Read the repo README before changing project-wide behavior.
- Read migration files before touching persistence logic.
- Read service-specific tests before refactoring business rules.
```

### Example `CLAUDE.md`

```md
# Project: Beacon API

## Stack
- Node.js
- TypeScript
- npm

## What this project does
This service handles account, billing, and notification workflows. Before making non-trivial changes, read the module you are about to edit and one nearby test file so your changes match the current conventions.

## Key directories
- `src/routes/` — request entrypoints
- `src/services/` — business logic
- `src/db/` — database access and migration-related code
- `tests/` — automated checks

## Commands
- `npm test`
- `npm run lint`
- `npm run build`

## Workflow
Use `npm test` and `npm run lint` after meaningful changes because they catch the most likely regressions quickly.
If a task would add a dependency, change CI, or touch database migrations, ask first rather than assuming that kind of change is routine here.
If repo evidence is weak, say what you confirmed, what you inferred, and what still needs confirmation.

## What to read before complex tasks
- Read the README before changing project-wide behavior.
- Read migration files before touching persistence logic.
- Read the nearest tests before refactoring business rules.
```

## Monorepo layering example

Use this pattern when the root and package really differ.

### Root `AGENTS.md` excerpt

```md
## Context
- Monorepo with a web app, API, and shared packages.

## Commands
- `pnpm test`
- `pnpm lint`

## Constraints
- Ask before changing shared package APIs used by multiple apps.
- Prefer package-level commands when working deeply inside one package.
```

### Scoped `packages/api/AGENTS.md` excerpt

```md
> Scoped rules for `packages/api`. See the repo root `AGENTS.md` for shared rules.

## Context
- [verified] Go API service with its own test and deployment workflow.

## Commands
- [verified] `go test ./...`

## Constraints
- Ask before changing public API contracts or deployment config for this service.
```

## Practical difference to preserve

- `AGENTS.md` should feel like durable operating rules for GPT/Codex-style agents.
- `CLAUDE.md` should feel like a concise working guide for Claude Code.
- The files may share facts, but they should not read like the same document with cosmetic rewrites.
