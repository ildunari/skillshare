---
name: skill-lifecycle-automation
description: >-
  Operate Kosta's offline Hermes/Skillshare skill-lifecycle automation: nightly
  session evidence review, safe staged skill proposals, weekly cross-profile
  promotion, Skillshare sync verification, and cleanup of unused SkillClaw proxy
  surfaces. Use when changing cron jobs or scripts that improve skills from
  prior Hermes work.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
---

# Skill Lifecycle Automation

Kosta's preferred architecture keeps live Hermes profiles on their native models and uses skill evolution as an offline maintenance lane.

Do **not** route Hermes GPT/default/BrowserAgent through `skillclaw-model` unless Kosta explicitly asks to test the proxy path. SkillClaw's useful idea here is the lifecycle loop — session evidence → summarize → judge → propose → verify → apply — not replacing the live inference route.

## Current lanes

- Nightly suggest lane: read recent Hermes sessions and Skillshare state, produce candidate improvement reports/proposals under `~/.hermes/shared/skill-evolution/`.
- Safe apply lane: apply only tiny exact-string JSON proposals with `safe_apply: true`; ambiguous changes remain staged.
- Weekly promotion lane: review accumulated candidates, patch canonical Skillshare source, run `skillshare sync`, verify profile targets, and commit.

## Scripts

Profile scripts live under `~/.hermes/profiles/gpt/scripts/`:

- `hermes_skill_evolution_context.py` — read-only context collector for recent sessions, Skillshare status, git status, and pending proposals.
- `hermes_skill_evolution_safe_apply.py` — mechanical guardrail applier for tiny staged JSON proposals.

Run checks manually:

```bash
~/.hermes/profiles/gpt/scripts/hermes_skill_evolution_context.py --hours 24 --limit 12 --write-report
~/.hermes/profiles/gpt/scripts/hermes_skill_evolution_safe_apply.py --dry-run
```

## Canonical source and sync

Canonical shared skill source is:

```text
~/.config/skillshare/skills/
```

After any applied skill edit:

```bash
git -C ~/.config/skillshare diff --check
skillshare sync --json
```

Verify at least GPT sees the updated skill via `skill_view` or by checking the synced target file under `~/.hermes/profiles/gpt/skills/`.

## Model split

Use cheap models for broad reading and clustering, stronger models for judgment and editing:

- GLM-5.1: nightly collection, clustering, first-pass suggestions, mechanical summaries.
- GPT/Codex-class: weekly reviewer/editor, deciding whether changes belong in an existing skill, a new skill, memory, or nowhere.
- Optional second-model verifier: reject generic advice, weak evidence, broad rewrites, or changes that drop environment-specific facts.

## Apply policy

If `hermes_skill_evolution_safe_apply.py --dry-run` rejects a JSON proposal with a bogus target like `/Users/Kosta/.config/skillshare/skills/SKILL.md` while the proposal's `canonical_path` points at a real skill directory, treat that as an applier-path bug, not a substantive rejection. Manually inspect the JSON and apply only the same tiny evidence-backed hunk if the target file and old string match.

Safe automatic changes are narrow:

- exact command/path corrections observed in successful sessions
- missing verification steps for a known workflow
- reference notes documenting a repeated local quirk
- typo or stale wording fixes that do not change behavior

Reject or stage for human/strong-model review when a proposal:

- rewrites large sections
- creates a new broad skill from one weak session
- removes concrete paths, endpoints, ports, model IDs, or local facts
- adds generic “be careful” prose
- changes live gateway/model/provider routing
- edits outside Skillshare canonical source

## Unused SkillClaw cleanup stance

The SkillClaw client/proxy/dashboard LaunchAgents are not needed for this offline design. It is OK to disable/archive those LaunchAgents while keeping `~/.skillclaw/config.yaml` and local-share data as reference material.

Do not delete `~/.skillclaw` wholesale unless Kosta explicitly asks; archive first.
