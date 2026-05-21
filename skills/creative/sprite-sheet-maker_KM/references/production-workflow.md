# Production Workflow

Use this for end-to-end sprite-sheet runs.

## Folder Contract

```text
sprite-runs/<asset-slug>/
  brief.md
  manifest.json
  prompts/
    00-base.md
    rows/<row-id>.md
  references/
    user/
    canonical-base.png
    style/
    layout-guides/
  generated/
    base/
    rows/
  final/
    spritesheet.png
    spritesheet.webp
    frames/
    manifest.json
  qa/
    contact-sheet.png
    review.md
    animation-notes.md
```

## Phases

### 1. Brief

Capture role, camera, style, identity locks, animation list, cell size, and background strategy. Use `scripts/create_sprite_run.py` when useful.

### 2. Base

Generate the base first. Do not proceed if the base fails silhouette, palette, or camera requirements.

### 3. Pilot Rows

Generate `idle` first and the hardest action second. If these drift, fix before expanding the run.

### 4. Row Generation

Generate each row from the base and references. Use subagents for three or more independent rows.

### 5. Assembly

Use project tooling or deterministic scripts to assemble already-generated frames/rows. Do not fabricate visual frames locally.

### 6. QA

Check identity, motion, frame count, background cleanup, and engine handoff readiness.

### 7. Repair

Repair the smallest failed part: prompt, row, base, then action plan.

## Parent/Subagent Ownership

Parent owns:

- `manifest.json`
- canonical base selection
- final packaging
- QA acceptance
- repair decisions

Subagents may:

- generate one row
- inspect one row
- return selected source path and QA note

Subagents must not:

- edit manifests
- assemble sheets
- package final outputs
- invent frames with scripts

