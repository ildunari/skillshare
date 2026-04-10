---
name: branch-finish-release
description: "Use when implementation is complete, tests are verified, and you need to wrap up branch work by choosing merge, PR, keep-as-is, discard, or release-note generation. Supersedes `finishing-a-development-branch` and absorbs the branch-isolation cleanup guidance from `using-git-worktrees`."
---

# Branch Finish Release

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the branch-finish-release skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Stop. Don't proceed to Step 2.
**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally
- Switch to base branch, pull latest, merge feature branch
- Verify tests on merged result
- Delete feature branch
- Cleanup worktree (Step 5)

#### Option 2: Push and Create PR
- Push branch with `-u` flag
- Create PR with `gh pr create`
- Cleanup worktree (Step 5)

#### Option 3: Keep As-Is
- Report: "Keeping branch <name>. Worktree preserved at <path>."
- **Don't cleanup worktree.**

#### Option 4: Discard
- **Confirm first** - require typed 'discard' confirmation
- Delete branch, cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

If yes: `git worktree remove <worktree-path>`

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | Yes | - | - | Yes |
| 2. Create PR | - | Yes | Yes | - |
| 3. Keep as-is | - | - | Yes | - |
| 4. Discard | - | - | - | Yes (force) |

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Release Notes

When the user asks for release notes, a changelog, or "What's New" text (e.g., for an App Store submission), use this workflow after the branch work is complete.

### 1) Collect changes

Run the script from the repo root to gather commits and touched files since the last tag:

```bash
scripts/collect_release_changes.sh
# Or pass a specific range:
scripts/collect_release_changes.sh v1.2.3 HEAD
```

If no tags exist, the script falls back to full history. Script lives at `scripts/collect_release_changes.sh` (see `references/release-notes-guidelines.md` for language and filtering rules).

### 2) Triage for user impact

- Scan commits and touched files to identify **user-visible** changes.
- Group by theme: **New**, **Improved**, **Fixed**.
- **Drop** internal-only work: build scripts, refactors, dependency bumps, CI.

### 3) Draft the notes

- Write short, benefit-focused bullets (one sentence each).
- Use clear verbs and plain language; avoid internal jargon.
- Aim for 5–10 bullets unless the user requests a different length.
- Optional title: "What's New" or `<Product> <Version>`.

### 4) Validate

- Every bullet must map back to a real commit in the range.
- Check for duplicates and overly technical wording.
- Ask for clarification if any change is ambiguous or possibly internal-only.

**Resources:**
- `scripts/collect_release_changes.sh` — collects commits and touched files since last tag
- `references/release-notes-guidelines.md` — language, filtering, and QA rules

## Integration

## Branch Isolation Notes

If the work started in a git worktree, this skill now owns the cleanup path that used to live in `using-git-worktrees`. The preserved setup guidance lives under `merged/using-git-worktrees/`.

**Called by:**
- **[skill:subagent-driven-development]** - After all tasks complete
- **[skill:planning-protocol]** - After the implementation batches are complete

**Pairs with:**
- **[skill:branch-finish-release]** - Owns worktree cleanup after implementation is done
