---
name: update-smart
description: >-
  Use when Kosta invokes /update_smart or asks for a smart Hermes update.
  Performs the Mac Studio branch-first Hermes update workflow: audit local repos,
  create rollback branches, preserve and replay local git customizations, update
  Hermes/WebUI/non-Hermes sidecars carefully, run verification, and avoid
  restarting the live gateway from inside Telegram unless explicitly safe.
version: 0.1.0
author: Hermes Agent
license: MIT
targets: [hermes-default, hermes-gpt]
metadata:
  hermes:
    command_priority: 450
    tags: [hermes, update, update-smart, local-git, maintenance]
---

# Smart Update

Use this skill for `/update_smart` or plain requests like “do a smart update,” “update Hermes smartly,” or “update using the local gits to put changes back.”

Important: this is **not** the built-in `/update` command. Built-in `/update` runs `hermes update --gateway`, which is useful for ordinary upstream updates but is too blunt for Kosta's local Mac Studio workflow. `/update_smart` means run an agent-led maintenance pass with local git preservation and verification.

## Scope

Default scope on Mac Studio:

- Hermes agent repo: `~/.hermes/hermes-agent`
- Hermes state repo: `~/.config/hermes-state`
- Skillshare canonical skills/allowlist: `~/.config/skillshare`
- hosted WebUI sidecar: `~/.hermes/hermes-webui`
- non-Hermes smart updater: `~/.hermes/profiles/gpt/scripts/non_hermes_update_audit.py`

Do not push remotes unless Kosta explicitly asks. Local commits are fine and preferred for preserving completed changes.

## Required workflow

1. Load `hermes-maintenance-and-distribution`, especially the smart local update reference.
2. Audit before touching anything:
   - current date/host/user
   - git branch, upstream, ahead/behind, status for the repos above
   - `hermes version` / `hermes update --check` when applicable
   - relevant LaunchAgent/LaunchDaemon status only if the update affects a service
3. Create rollback points before mutation:
   - timestamped backup branch in each touched git repo, e.g. `backup/pre-update-smart-YYYYMMDD-HHMMSS`
   - preserve meaningful uncommitted work by committing locally when it is real work, not by relying only on stash
4. Update Hermes using the branch-first local customization flow:
   - stay on the local customization branch, normally `local/studio-customizations`
   - fetch upstream/origin
   - merge upstream into the local branch deliberately; do not blindly reset local work to `origin/main`
   - resolve conflicts file-by-file, preserving intended local behavior
5. Reapply or preserve local behavior from git:
   - compare local branch changes against upstream
   - keep carried local patches that are still needed
   - drop only patches that upstream clearly absorbed or made obsolete
6. Install/rebuild/sync:
   - reinstall Hermes from the updated checkout as appropriate
   - sync skills through Skillshare, not manual profile copying, when skill distribution changed
   - update hosted WebUI via its sidecar path if needed
   - run the non-Hermes smart update audit if requested or relevant
7. Verify in layers:
   - syntax/compile checks for touched Python files
   - focused tests for changed behavior
   - `hermes version` and `hermes update --check`
   - service health endpoints for WebUI or other updated sidecars
   - avoid claiming completion if the live process is still running old code and needs a safe restart
8. Gateway safety:
   - If the current conversation is arriving through Telegram/Discord/webhook, do not restart the gateway unless Kosta explicitly accepts the interruption.
   - It is okay to leave updated code on disk and say a safe restart is needed.

## Output style

Keep the report short. Say what changed, what was verified, and what still needs attention. Include backup branch names and exact failing check excerpts only if something failed.

## Built-in `/update` comparison

If Kosta asks whether `/update` does this: answer no. `/update` currently spawns `hermes update --gateway`; it stashes local working tree changes, switches to `main`, pulls/resets from `origin/main`, then optionally restores the stash. That is not the same as Kosta's smart local-git workflow because it does not preserve the local customization branch as the primary branch, does not audit/replay local commits deliberately, and does not include WebUI/Skillshare/non-Hermes sidecar verification.
