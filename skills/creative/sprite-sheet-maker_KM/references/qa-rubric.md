# Sprite Sheet QA Rubric

Use this after every base image and row strip.

## Identity

- The asset is recognizable as the same character, prop, or effect across rows.
- Shape language, face/markings, palette, materials, and held props remain consistent.
- Any side-specific asymmetry is intentional and documented.

## Animation

- Each row has the requested frame count.
- Looping rows have compatible first and last frames.
- Non-looping rows have anticipation, action/peak, and recovery/end.
- Frames are not duplicate stills with tiny offsets unless the action is intentionally subtle.
- The motion reads at target cell size.

## Sheet Usability

- Cell size and row/column count are documented.
- Every row has an id, purpose, frame count, loop flag, and timing note.
- Frames are separated, centered, and not clipped.
- Empty cells are transparent or intentionally unused.
- No visible grids, labels, frame numbers, UI, watermarks, or accidental scenery remain.

## Background And Alpha

- If using chroma key, the key color is flat and absent from the sprite.
- If using alpha, corners and unused cells are transparent.
- No shadows, glows, blur, smoke, or particles accidentally merge into the background unless those are part of the effect.

## Repair Priority

1. Fix prompt wording or identity locks.
2. Regenerate one bad row.
3. Regenerate the canonical base only if most rows drift from the concept.
4. Redesign the action list only if QA shows the moveset does not fit gameplay.

