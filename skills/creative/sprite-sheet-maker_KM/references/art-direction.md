# Art Direction

Use this when choosing a sprite style or translating references into game assets.

## Style Families

### Pixel Art

- Strong grid discipline, limited palette, hard edges.
- Best when the final game also uses pixel-perfect rendering.
- Prompts should ask for pixel-art style, hard-edged sprite frames, limited colors, and no soft gradients.

### Pixel-Adjacent

- Chunky, readable, low-detail raster art with stepped edges.
- More forgiving for AI generation and later cleanup.
- Good default for generated sprite sheets.

### Inked Cartoon

- Clean outlines, flat fills, expressive poses.
- Works well for readable characters and props.
- Prompt for bold silhouette and simple shadow shapes, not illustration polish.

### Hand-Painted Small Sprite

- Soft fantasy/RPG feel, but easy to over-detail.
- Use only when target cells are 128px or larger.
- Prompt for broad value blocks and avoid tiny texture.

### Rendered-Then-Sprite

- Low-poly or clay-like 3D render flattened into sprite frames.
- Useful for faux-3D games.
- Keep lighting consistent; avoid realistic shadows that complicate alpha cleanup.

## Anti-Slop For Sprites

Avoid:

- Beautiful single illustration that cannot animate.
- Tiny accessories that vanish at target size.
- Complex fabric, fur, or smoke on small cells.
- New props appearing only in attack rows.
- Full scene art instead of isolated sprites.
- Motion blur instead of pose changes.
- Text or UI labels inside frames.

Prefer:

- Big silhouette first.
- One or two signature details.
- Limited palette with clear value separation.
- Pose language that explains the action without effects.
- Effects separated into their own rows/sheets when they need independent timing.

## Palette Prompts

Use palette as a gameplay signal:

- Fire/torch: hot core, darker rim, one accent spark color.
- Poison: cool green/yellow with dark outline and bubbling shapes.
- Ice: pale cyan/white with angular silhouettes.
- Heavy metal: dark neutral body, bright edge highlights, slow heavy motion.
- Ghost/magic: pale core, colored outline, but avoid soft transparent haze unless the engine supports it.

