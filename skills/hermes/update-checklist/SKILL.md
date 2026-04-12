---
name: hermes-update-checklist
description: >-
  Prepare Hermes for a safe `hermes update` when there are local repo edits,
  patch artifacts, untracked files, multiple profiles, or machine-specific
  customizations that must survive the update. Use whenever the user asks about
  updating Hermes safely, preserving local changes across update, checking if
  current work is update-proof, refreshing `~/.hermes/patches`, auditing what
  the post-merge hook will restore, replaying local improvements after update,
  or verifying that default and gpt profiles still work afterward. Always use
  this before running `hermes update` on a dirty Hermes repo.
targets: [hermes-default, hermes-gpt]
---

# Hermes Update Checklist

Use this skill for Hermes self-updates on this machine when the repo is dirty or local behavior matters.

This is not just “run `hermes update`.” The real job is:
1. figure out what must survive,
2. make sure the preservation machinery actually covers it,
3. predict conflicts before touching the live repo,
4. update,
5. replay local changes deliberately,
6. verify that the updated system still works.

## What `hermes update` actually does

Verified from `hermes_cli/main.py`:
- If the repo is dirty, Hermes auto-stashes tracked and untracked changes.
- Hermes updates against `origin/main`.
- Hermes then tries to re-apply the stash.
- If stash restore conflicts, the stash is preserved and Hermes reports the problem.

Important: this is helpful, but it is not a semantic smart merge. It preserves work at the git level. It does not know which local changes are intentional, stale, or dangerous.

## The second layer on this machine: post-merge patch replay

Also verified live on this machine:
- `~/.hermes/hermes-agent/.git/hooks/post-merge` restores selected `.new` files from `~/.hermes/patches/`
- then tries to apply every top-level `~/.hermes/patches/*.patch`

So update survival here is two layers:
- Hermes auto-stash/restore
- local patch replay after merge

Treat `~/.hermes/patches/` as live system state, not as an archive.

## Core rule

Never assume current local work is update-proof just because:
- `hermes update` auto-stashes, or
- a patch file with a familiar name exists.

Check the live dirty tree against the live patch inventory every time.

Also classify *where* each durable change should live before updating.
If the question is really about storage/placement rather than update mechanics, read the shared durable-state skill first. The update checklist should stay procedural; the placement model lives in `hermes__shared-durable-state-architecture`.

## Trigger questions

Use this skill when the user says things like:
- “is it safe to update?”
- “will `hermes update` keep our changes?”
- “make sure nothing gets lost after update”
- “which files are protected by patches and which aren’t?”
- “why did this old file come back after update?”
- “verify we’re good to update”

## Phase 1 — Inventory what exists now

Start with evidence, not memory.

Run these checks first:

```bash
cd ~/.hermes/hermes-agent
git status --short
find ~/.hermes/patches -maxdepth 1 -type f | sort
```

Read the live hook if behavior matters:
- `~/.hermes/hermes-agent/.git/hooks/post-merge`

Also inspect profile-specific state if the current work depends on it:
- `~/.hermes/profiles/gpt/`
- `~/.hermes/config.yaml`
- `~/.hermes/profiles/gpt/config.yaml`
- profile `.env` files
- cron jobs under `~/.hermes/profiles/<profile>/cron/jobs.json`

### Required outcome of Phase 1

Produce four buckets:
1. tracked repo changes that must survive
2. untracked new files that must survive
3. machine/profile runtime changes outside git that must survive
4. stale patch artifacts that must NOT be restored after update

Do not continue until each current change has been classified.

## Phase 2 — Reconcile the dirty tree against canonical patches

Before trusting the patch system, compare the dirty repo to the patch inventory.

Use this pattern:

```bash
cd ~/.hermes/hermes-agent

for p in ~/.hermes/patches/*.patch; do
  [ -f "$p" ] || continue
  grep '^diff --git' "$p" | sed 's|^diff --git a/||; s| b/.*$||'
done | sort -u > /tmp/patched-files.txt

git diff --name-only HEAD | sort -u > /tmp/wt-files.txt
comm -23 /tmp/wt-files.txt /tmp/patched-files.txt
```

Interpret each uncovered file:
- real change to keep → promote into a canonical patch
- generated/noise file → explicitly decide to ignore it
- stale cruft → revert it before update

Do not leave meaningful files in a “maybe stash will save it” state unless you are intentionally accepting that risk.

## Phase 3 — Refresh preservation artifacts

### For tracked files

Refresh patches from the live intended diff, grouped by feature.

Pattern:

```bash
cd ~/.hermes/hermes-agent
git --no-pager diff -- path/to/file1 path/to/file2 > ~/.hermes/patches/feature-name.patch
```

Prefer feature-grouped patches over one giant anonymous patch.

Good groups look like:
- compact-progress / gateway UX
- mem0 / cron / profile recovery
- browser fix
- repo instruction files
- lockfile sync

### For untracked files

If the post-merge hook restores a `.new` file already, refresh that file from the live repo.

Pattern:

```bash
cp path/to/new_file ~/.hermes/patches/new_file.py.new
```

If the file is important, also create a real diff-from-empty patch so it can be recreated more robustly:

```bash
git diff --no-index -- /dev/null path/to/new_file > ~/.hermes/patches/new-file.patch
```

### For stale artifacts

Remove, rename, or archive anything you do NOT want restored after update.

This matters a lot for deleted tests/tools. A stale `.new` file can resurrect dead code after update.

## Phase 4 — Account for non-git runtime state

Not everything important lives in `~/.hermes/hermes-agent`.

Check and document any runtime state that the update will not manage for you:
- profile-local plugin/config symlinks
- profile `.env` contents and permissions
- installed Python packages in the Hermes venv
- active cron job definitions and schedules
- local skill placement / allowlist state
- gateway processes that may need restarting or sanity-checking

For each non-git dependency, record:
- what it is
- where it lives
- how to re-create it if missing after update
- how to verify it still works

## Phase 5 — Predict conflict surface before updating

For non-trivial local changes, do a dry-run in a scratch worktree before touching the real repo.

Use this exact pattern:

```bash
cd ~/.hermes/hermes-agent
git fetch origin
rm -rf /tmp/hermes-merge-test
git worktree add /tmp/hermes-merge-test origin/main
git --no-pager diff HEAD > /tmp/local-mods.patch
cd /tmp/hermes-merge-test
git apply --3way --check /tmp/local-mods.patch 2>&1
```

If it reports conflicts, inspect them in the worktree before running the real update.

This gives you a conflict map without risking the live repo or forcing an immediate restart cycle.

Cleanup:

```bash
cd ~/.hermes/hermes-agent
git worktree remove /tmp/hermes-merge-test --force
```

## Phase 6 — Independent verifier lane

Before declaring “good to update,” run an independent verification pass using a subagent.

The verifier should answer:
- which current changes are covered by top-level patch artifacts or `.new` restores
- which changes are only in autostash risk territory
- which patch files are stale or dangerous
- whether the dry-run conflict surface is acceptable
- what exact pre-update fixes are still required, if any

The verifier must not rely on the main agent’s conclusions. It should inspect the live repo, live patch directory, and live hook itself.

## Phase 7 — Update execution

Only run update after:
- patch artifacts are refreshed
- stale artifacts are cleaned up
- runtime dependencies are documented
- conflict prediction is acceptable
- the independent verifier says the pre-checks are green

Then run:

```bash
cd ~/.hermes/hermes-agent
hermes update
```

If running from messaging, remember `/update` uses the same underlying update logic plus file-based prompt forwarding.

## Phase 8 — Post-update replay and reconciliation

After update:
1. inspect git status immediately
2. inspect post-merge hook output if available
3. confirm expected local files/patches were restored
4. manually reapply any intentionally staged diffs that were not part of canonical top-level patches
5. resolve any conflicts deliberately, by feature group

If stash restore failed during update, do not hand-wave it. Identify which files came back and which didn’t.

## Phase 9 — Post-update verification checklist

Run verification in layers.

### Repo / syntax layer
- `git status --short`
- targeted `py_compile` or equivalent syntax checks for changed Python files
- verify expected untracked files still exist

### Tests layer
Run the most relevant targeted tests for the changed features.
At minimum, include tests touching:
- gateway compact progress behavior
- mem0 provider discovery / cron path if that work was touched
- browser CDP fix if that work was touched
- any new or restored tool/tests you preserved

### Runtime layer
Verify the user path, not just code shape:
- gateway process count is sane
- cron job definitions still point to the intended schedule/profile
- mem0/provider path still loads under the intended profile(s)
- any local tools restored by patches are actually present and importable

### Profile layer
If both default and gpt matter, verify both explicitly.
Do not assume one profile proving healthy means the other is fine.

Check:
- `~/.hermes/skills`
- `~/.hermes/profiles/gpt/skills`
- profile `.env`
- profile cron jobs
- profile-specific plugin/config symlinks or local files

## Phase 10 — Final readiness gate

Do not say “good to update” or “update-safe” until you can state, with evidence:
- what current changes exist
- how each one survives update
- what stale artifacts were cleaned up
- what still depends on manual replay
- what tests/checks passed
- what residual risks remain, if any

If all meaningful changes are either patch-protected, safely reproducible, or intentionally accepted as manual replay work, then give the go-ahead.

## Common failure modes

### 1. Stale `.new` file resurrects deleted code
Check `~/.hermes/patches/*.new` first.

### 2. Patch exists but is stale
A familiar patch filename means nothing unless it matches today’s intended diff.

### 3. Huge dirty tree with no feature grouping
Split it before update. Anonymous blobs are how work gets half-preserved.

### 4. Untracked file exists only in the live repo
If it matters, back it up explicitly. Don’t rely on luck.

### 5. Profile/runtime changes were never documented
If mem0, cron, plugins, or venv packages matter, record the rebuild steps.

### 6. One agent grading its own prep
Use the independent verifier lane.

## Good reporting format

When finishing an update-prep run, answer in plain English:
- what is currently protected
- what is still fragile
- what you fixed to make it update-proof
- what tests/checks proved it
- whether it is actually go-to-go

If not ready, stop with the smallest concrete blockers and the exact next fixes.
