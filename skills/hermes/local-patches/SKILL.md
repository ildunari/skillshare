---
name: hermes-local-patches
description: >-
  Preserve local hermes-agent customizations across `hermes update` by using the
  real update behavior (auto-stash + stash restore) together with the local
  `~/.hermes/patches` post-merge reapply hook. Use when auditing whether local
  changes will survive an update, refreshing patch artifacts before updating,
  debugging why old files came back after update, or carrying forward untracked
  files like local tools/tests.
targets: [hermes-default, hermes-gpt]
---

# Hermes Local Patches

Use this when the user asks things like:
- "will `hermes update` keep my changes?"
- "how do we preserve local Hermes edits across update?"
- "why did this deleted file come back after update?"
- "what does the post-merge hook actually do?"

## What `hermes update` really does

Verified from `hermes_cli/main.py`:

1. If the repo is dirty, Hermes auto-stashes local changes with:
   - `git stash push --include-untracked -m hermes-update-autostash-...`
2. Hermes updates against `origin/main`.
3. Hermes then tries to restore the stash with:
   - `git stash apply <stash-ref>`
4. If stash restore conflicts, Hermes preserves the stash and reports the conflict.

Important: this is **not** a semantic smart merge. It is git stash/apply mechanics. It preserves work, but it does not understand intent.

## The second layer: post-merge local patch reapply

On this machine, `~/.hermes/hermes-agent/.git/hooks/post-merge` adds a second preservation layer after every merge/update.

It does two things:

1. Restores certain `.new` files from `~/.hermes/patches/`
   - Example: `telegram_actions_tool.py.new` -> `tools/telegram_actions_tool.py`
2. Reapplies every `*.patch` file in `~/.hermes/patches/`
   - tries `git apply --check`
   - then `git apply`
   - then `git apply --3way`
   - if reverse-check succeeds, treats it as already present
   - otherwise reports manual rebase needed

So the true update-survival model is:
- Hermes auto-stash + restore
- then post-merge patch replay

## Critical lesson: stale patch artifacts can resurrect dead files

This is the main practical pitfall.

If `~/.hermes/patches/` still contains an old `.new` file or patch for something you intentionally removed, the hook can bring it back after update.

Concrete example discovered on this machine:
- `test_tts_kokoro.py.new` was still sitting in `~/.hermes/patches/`
- the live repo had intentionally deleted `tests/tools/test_tts_kokoro.py`
- that stale restore artifact had to be archived so future updates would not bring the dead test back

Translation: the patch directory is a source of truth too. If it is stale, update preserves stale things.

## Safe pre-update workflow

Before running `hermes update`:

1. Inspect the live repo status
```bash
cd ~/.hermes/hermes-agent
git status --short
```

2. Inspect the patch inventory
```bash
find ~/.hermes/patches -maxdepth 1 -type f | sort
```

3. Read the post-merge hook if behavior is in doubt
```bash
read_file ~/.hermes/hermes-agent/.git/hooks/post-merge
```

4. Check for stale `.new` artifacts that would restore deleted files
   - especially tests, local tools, or temporary experiments

5. Refresh patch files from the current intended working tree
   - do not assume old patch files still represent current reality

6. Remove or archive artifacts for changes you no longer want preserved

## Refreshing the patch set

There is no universal one-command generator for all local changes. Regenerate deliberately by concern.

Typical pattern for an existing patch:
```bash
cd ~/.hermes/hermes-agent
git --no-pager diff path/to/file1 path/to/file2 > ~/.hermes/patches/some-feature.patch
```

Typical pattern for an untracked new file you want restored after update:
```bash
cp path/to/new_file ~/.hermes/patches/new_file.py.new
```

After refreshing, sanity-check sizes so you do not accidentally save an empty patch:
```bash
wc -l ~/.hermes/patches/*.patch ~/.hermes/patches/*.new
```

## How to think about change groups

Do not rely on one giant anonymous dirty tree.

Split local work into logical preservation units such as:
- gateway compact-progress work
- mem0/cron recovery
- browser fix
- Telegram power-tool file
- repo instruction/context files
- dependency lockfile sync

That makes post-update replay and conflict resolution much easier.

## When to trust auto-stash alone vs patch replay

Auto-stash alone is usually enough for:
- small edits on top of nearby upstream code
- changes you are happy to manually reconcile if conflicts happen

Patch replay is better for:
- long-lived local customizations
- untracked new files that git stash/apply may preserve awkwardly in practice
- machine-specific Hermes modifications you expect to survive many updates
- features referenced by other local skills or hooks

## Troubleshooting

If update "succeeded" but local behavior disappeared:
- check whether the stash restore conflicted and was skipped
- check post-merge hook output
- manually inspect `~/.hermes/patches/`
- verify the relevant patch file still matches the current intended code

If an old file mysteriously reappears after update:
- inspect `~/.hermes/patches/*.new`
- inspect the post-merge hook target mappings
- remove the stale `.new` file and re-run cleanup

If a patch stops applying cleanly:
```bash
cd ~/.hermes/hermes-agent
git apply --reject ~/.hermes/patches/<name>.patch
```
Then manually rebase the rejects and regenerate the patch.

## Practical rule

Before any meaningful Hermes update on this machine, treat `~/.hermes/patches/` as part of the live system state, not just an archive.

If you do not audit and refresh that directory, `hermes update` can faithfully preserve the wrong things.

If the real problem is that state lives in the wrong home to begin with, stop and read `hermes__shared-durable-state-architecture` before adding more replay artifacts. Patches are the preservation layer, not the ideal canonical home for durable operational state.
