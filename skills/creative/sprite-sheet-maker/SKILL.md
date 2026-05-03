---
name: sprite-sheet-maker
description: Create, repair, validate, and package game-ready sprite sheets for characters, props, effects, pickups, weapons, torches, creatures, UI mascots, and other animated game assets from text concepts or visual references. Use whenever the user wants a sprite sheet, spritesheet, animation sheet, game asset moveset, sprite-sheet character ideation, attack/jump/run/idle frames, pixel-art or stylized 2D animation rows, game-ready animation prompts, or OpenAI image generation for many consistent gameplay poses. This skill composes the installed $imagegen skill and provides references, templates, and scripts for identity-locked sprite production.
---

# Sprite Sheet Maker

> General sprite-sheet production skill for games and animated raster assets. It is the broad version of `$hatch-pet`: useful for torchlights, playable characters, enemies, props, pickups, effects, UI mascots, and full gameplay movesets.

## Core Idea

Turn a loose asset request into a production run:

1. Shape the creative brief with the user.
2. Pick the animation rows that fit the gameplay role.
3. Generate or preserve a canonical base image with `$imagegen`.
4. Generate each row from that base, one action at a time.
5. Assemble, validate, repair, and hand off a documented sprite sheet.

The model should feel like a game artist and technical asset producer, not a generic image prompt writer. The creative part chooses silhouettes, motion verbs, palettes, and animation promise. The technical part records cell sizes, rows, frame counts, background strategy, prompts, and QA.

## Always Load

Before doing generation or prompt work, load:

1. `${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/SKILL.md`
2. `references/openai-imagegen-workflow.md`
3. `references/production-workflow.md`
4. `references/qa-rubric.md`

Use `$imagegen` for visual generation. Deterministic scripts in this skill may create folders, manifests, prompts, layout notes, contact sheets, and validation reports, but they must not fake or synthesize sprite visuals.

## Load By Task

| User Need | Load These Files |
| --- | --- |
| Vague idea, brainstorming, character ideation | `references/creative-brief.md`, `references/art-direction.md` |
| Choosing moves, actions, row count | `references/action-taxonomy.md` |
| Writing base/row prompts | `references/prompt-recipes.md`, `templates/base-prompt.md`, `templates/row-prompt.md` |
| Three or more rows to generate | `templates/subagent-row-handoff.md` |
| Repairing bad output | `references/repair-playbook.md` |
| Unity/Godot/web handoff | `references/engine-handoff.md` |
| Building a run folder | `scripts/create_sprite_run.py`, `templates/manifest.json` |
| Checking a run folder | `scripts/validate_manifest.py`, `references/qa-rubric.md` |

## Defaults

Use these unless the user or project gives better constraints:

- Run folder: `sprite-runs/<asset-slug>/`
- Background: flat chroma-key first, alpha after cleanup when needed.
- Cell sizes: props/items `64x64`, small characters/effects `96x96`, standard characters `128x128`, large characters/bosses `192x192` or `256x256`.
- Frame counts: subtle loops 4-6, locomotion 6-8, attacks 6-10, effects 6-12.
- Final files: `final/spritesheet.png`, `final/spritesheet.webp`, `final/manifest.json`, `qa/contact-sheet.png`, `qa/review.md`.

Use `$hatch-pet` instead when the target is specifically a Codex app pet package with its fixed 8x9, 192x208 atlas and `pet.json`.

## Creative Calibration

Before creating rows, understand the asset:

- **Role:** playable character, enemy, prop, pickup, projectile, effect, mascot, UI avatar.
- **Camera:** side-view, top-down, isometric, three-quarter, front-facing, icon-like.
- **Style:** pixel-art, pixel-adjacent, cozy RPG, action roguelite, inked cartoon, hand-painted, low-poly rendered sprite, clean vector-like raster.
- **Gameplay feel:** heavy, nimble, magical, mechanical, haunted, silly, elegant, brutal, fragile, utility-only.
- **Technical target:** cell size, sheet dimensions, engine, alpha/chroma-key, naming convention, timing needs.

If the user only gives a vibe, ask at most three short questions. If the answers are not necessary to begin, make a tasteful first pass and state the assumptions in `brief.md`.

When ideating, offer 3-6 concepts. Each concept should include silhouette, palette, motion promise, and likely gameplay verbs. Recommend one direction when the tradeoff is clear.

## Normal Workflow

1. Create a brief and manifest. For a scaffolded run:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/sprite-sheet-maker/scripts/create_sprite_run.py" \
  --asset-name "<Name>" \
  --asset-type character \
  --camera side-view \
  --style "chunky pixel-art-adjacent action RPG sprite" \
  --description "<one sentence>" \
  --animations idle:6:loop,run:8:loop,jump:6,attack-light:6,hurt:4,defeat:8 \
  --cell 128x128 \
  --output-dir /absolute/path/to/sprite-runs/<slug>
```

2. Review `brief.md`, `manifest.json`, and generated prompt drafts. Tighten identity locks before generation.
3. Generate the base image using `$imagegen`, then save the selected output as `references/canonical-base.png`.
4. Generate `idle` first and the hardest motion row second. Inspect both before generating the rest.
5. For three or more independent rows, use subagents with `templates/subagent-row-handoff.md`; the parent owns manifest edits and final packaging.
6. Assemble final assets with project tooling, engine tooling, Aseprite, TexturePacker, or deterministic scripts. Do not create visual frames locally as a substitute for `$imagegen`.
7. Validate:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/sprite-sheet-maker/scripts/validate_manifest.py" \
  /absolute/path/to/sprite-runs/<slug>/manifest.json
```

8. Review the contact sheet or generated row images against `references/qa-rubric.md`.
9. Repair the smallest failing scope with `references/repair-playbook.md`.
10. Report saved files, generation path, prompts used, rows completed, rows needing repair, and engine handoff notes.

## Prompt Discipline

Use `$imagegen` prompts that are short, labeled, and asset-specific:

- Start with intended use and camera.
- Describe the subject and silhouette before surface detail.
- Keep palette and materials concrete.
- Preserve identity locks on every row.
- State layout constraints plainly: one horizontal row, equal slots, full body visible, no overlap.
- Avoid text, labels, grids, watermarks, scenery, accidental UI, detached shadows, and duplicate still frames.

OpenAI docs favor skimmable prompts, explicit constraints, multi-image role labels, and small iterative changes. Do not hide critical instructions in a giant paragraph.

## Subagent Boundary

Subagents may generate or inspect one row at a time. They must not edit `manifest.json`, assemble the final sheet, record canonical outputs, or package files. The parent keeps provenance centralized.

Each subagent receives:

- Run directory
- Row id and prompt file
- Canonical base image path
- Optional style/reference/layout images
- Exact return contract: selected generated source path plus a one-sentence QA note

## Output Report

When finished, report:

- Files changed or created.
- Rows planned and rows generated.
- OpenAI/imagegen path used.
- QA result and any repairs.
- Final saved paths.
- Recommended next steps tied to asset quality, engine integration, or skill iteration.

