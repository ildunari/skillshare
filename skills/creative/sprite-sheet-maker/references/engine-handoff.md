# Engine Handoff

Use this when the output is intended for a real game project.

## Manifest Fields

Every final manifest should include:

- `asset_name`
- `asset_type`
- `camera`
- `cell.width`, `cell.height`
- `sheet.columns`, `sheet.rows`, `sheet.background`
- `animations[].id`
- `animations[].frames`
- `animations[].loop`
- `animations[].frame_duration_ms` or timing notes
- `files.spritesheet`
- `files.contact_sheet`

## Unity Notes

- Use PNG for import; WebP can be an export artifact but Unity workflows often prefer PNG.
- Set Sprite Mode to Multiple.
- Set Pixels Per Unit consistently with the cell size.
- Disable filtering for pixel art; use point filtering and no compression.
- Use animation clips per row.

## Godot Notes

- Use SpriteFrames or AnimationPlayer depending on project style.
- For pixel art, disable filtering on import.
- Keep row ids and animation ids identical to the manifest.
- Separate effects into their own AnimatedSprite2D when timing differs from character movement.

## Web/Canvas Notes

- Keep `cellWidth`, `cellHeight`, `columns`, and row indexes in a JSON manifest.
- Use nearest-neighbor image rendering for pixel art.
- Preload spritesheets before first animation.
- Separate atlas data from animation timing so designers can tune timing without re-exporting art.

## Naming

Prefer lowercase ids with hyphens:

- `idle`
- `run`
- `jump`
- `attack-light`
- `attack-heavy`
- `hurt`
- `defeat`
- `idle-flame`
- `extinguish`

