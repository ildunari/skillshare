---
name: hermes__telegram-gateway
description: >-
  Hermes Agent's Telegram gateway — bot identity, slash-command routing,
  callback handling, threading behavior, and the local custom Telegram features
  carried on this machine. Use when changing or verifying Telegram-specific
  Hermes behavior.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Hermes Telegram Gateway

Use this skill for Telegram bot behavior, adapter changes, callback workflows, and verification of local Telegram customizations.

## Local customization rule

Durable Telegram repo customizations on this machine belong on `local/studio-customizations`.

Do not preserve important Telegram behavior primarily by:
- top-level `~/.hermes/patches/*.patch`
- `.new` restores for repo files
- stash-only state
- archived patch exports

If losing a Telegram feature after update would be a problem, it should be committed on `local/studio-customizations`.

## Current carried local behaviors to verify there

Examples of local Telegram behavior that should now be branch-canonical rather than patch-canonical:
- context badge / compact-context callback flow
- compact tool-progress behavior and related config
- gateway `/tts` support
- `/newthread` support where applicable
- Telegram-specific helper tools committed inside the repo

## Update survival model for Telegram work

Normal flow:
1. commit Telegram repo changes on `local/studio-customizations`
2. update `main` from `origin/main`
3. merge `main` into `local/studio-customizations`
4. resolve conflicts in git
5. run focused Telegram verification

Do not assume a patch file or old stash is the real source of truth.

## Focused verification ideas

After Telegram changes or after an update, verify:
- callback payload handling still works
- final reply threading/topic behavior is intact
- any context badge or compact-progress symbols you expect are present
- targeted Telegram gateway tests still pass

## Narrow remaining patch use

A machine-local non-repo helper may still live outside the repo and be restored separately.
That is fine.

But repo files like `gateway/run.py`, `gateway/platforms/telegram.py`, `gateway/platforms/base.py`, tests, or Telegram tool files should not be maintained primarily through patch replay.

## If you find old replay artifacts

Treat them like migration residue.
Ask:
- does this represent real Telegram behavior we still care about?
- if yes, is it already committed on `local/studio-customizations`?
- if no, archive/retire it instead of keeping it live forever

If the answer is “it still matters and it is not on the branch yet,” promote it into the branch model before calling the setup stable.
