---
name: hermes__shared-durable-state-architecture
description: >
  Design or migrate Hermes toward a root-shared durable-state model under
  ~/.hermes/shared/ when operational state should survive repo updates and must
  not stay trapped in ~/.hermes/hermes-agent. Use when deciding where logbooks,
  shared specs, manifests, registries, or other durable non-repo operational
  state should live.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Shared Durable-State Architecture for Hermes

Use this when the question is **where state should live** so Hermes stays update-proof, not just **how to run an update safely**.

## When to use

- The user wants a safe home for non-repo operational state
- Durable state keeps landing inside `~/.hermes/hermes-agent`
- A logbook, shared spec, registry, or migration record should outlive repo churn
- You need to decide between memory, skills, shared durable-state, profile/runtime state, and repo edits
- You are about to move canonical state out of repo `ops/` paths

## Core model

Separate these classes explicitly:

1. **Repo code / instruction layer**
   - `~/.hermes/hermes-agent`
   - Real Hermes code, tests, repo docs, repo-root `HERMES.md`
   - Durable local repo customizations should live as real commits on a maintained local branch such as `local/studio-customizations`, not as patch replay artifacts

2. **Root-shared durable state**
   - `~/.hermes/shared/`
   - Canonical non-repo operational state that should survive repo updates
   - Prefer a subtree like `~/.hermes/shared/durable-state/`

3. **Profile-scoped runtime state**
   - Active `HERMES_HOME` paths like profile config, cron state, memories, logs, env/config
   - Keep profile-specific behavior here

4. **Durable user facts and preferences**
   - Shared `USER.md` and memory tools
   - Facts belong in memory; procedures do not

5. **Reusable procedures / decision trees**
   - Skills

6. **Preservation artifacts**
   - `~/.hermes/patches/`
   - Replay layer only, not the primary home for canonical state

## Critical distinction: root-shared vs profile-scoped

Do not blur these.

- **Profile-scoped** means tied to the active `HERMES_HOME`
- **Root-shared** means anchored under the Hermes root regardless of active profile

If code or docs mix `get_hermes_home()` semantics with literal `~/.hermes/shared/...` semantics, call that out explicitly and resolve it before migrating state.

## Keep v1 lean

Do not overbuild governance on day one.

For the first pass, prefer:
- one orientation doc
- one normative top-level spec
- one machine-readable map source of truth
- one placement registry if it adds clarity

Avoid duplicated control planes that say the same thing in two formats.

## Short HERMES.md rule shape

The repo-root instruction should stay short. Good shape:
- when work involves durable operational state outside the repo, use the shared durable-state area under `~/.hermes/shared/`
- before creating, moving, or editing anything there, read this skill first
- do not invent new homes ad hoc when an existing classified home already exists
- save durable user facts/preferences to memory proactively instead of leaving them only in transcripts

## Migration rule

Treat this as an **instruction cutover**, not just a path move.

If you move canonical state out of the repo, patch every place that teaches the old model:
- `HERMES.md`
- repo docs/specs
- helper scripts
- cron prompts/jobs
- skills that encode old paths
- troubleshooting skills for old path assumptions

Do not move files first and hope the prompt layer catches up later.

## First maintenance cron rule

The first maintenance cron for shared durable-state must be **audit-only**.

It may:
- read the spec and map
- scan the tree for drift or misplaced files
- report violations
- suggest fixes

It should not, at first:
- move files aggressively
- invent new homes for unknown files
- rewrite specs or maps automatically

## Read next

For the live durable-state contract, read the shared docs directly:
- `~/.hermes/shared/durable-state/SPEC.md`
- `~/.hermes/shared/durable-state/REGISTRY.md`
- `~/.hermes/shared/durable-state/specs/placement-rules.md`
- `~/.hermes/shared/durable-state/specs/change-log-spec.md`
