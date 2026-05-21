# Game assets, icons, sprites, and small images

## Contents

- [Small asset rule](#small-asset-rule)
- [Pixel art](#pixel-art)
- [Sprite sheet](#sprite-sheet)
- [Tile set](#tile-set)
- [Item icons](#item-icons)
- [App icon](#app-icon)
- [Sticker or emoji](#sticker-or-emoji)
- [Isometric game asset](#isometric-game-asset)
- [Voxel or low-poly asset](#voxel-or-low-poly-asset)
- [HUD or game UI](#hud-or-game-ui)
- [Texture or material swatch](#texture-or-material-swatch)

## Small asset rule

Small assets need readability more than detail. Specify silhouette, outline, palette, background, grid, and extraction plan. Avoid tiny internal text and excessive texture.

For true transparent output, use an opaque, high-contrast background and remove it later unless the chosen model/workflow supports alpha.

## Pixel art

Template:

```text
Create pixel art of [subject].
Style: crisp 32-bit pixel art, limited palette, clean silhouette, dark 1-pixel outline, no anti-aliasing, no blur.
Canvas: square, centered subject, plain solid background for extraction.
Mood: [cozy/fantasy/sci-fi/horror].
Constraints: no text, no gradient blur, no painterly rendering, no extra props.
```

## Sprite sheet

Template:

```text
Create a sprite sheet for an original [character].
Grid: [columns] x [rows], equal cells, one centered sprite per cell.
Required poses: [list].
Style: [pixel art/vector/hand-painted], readable silhouette, consistent proportions, consistent outfit and palette.
Background: plain solid color for later extraction.
Constraints: no text labels, no overlapping cells, no shadows crossing cell boundaries, no anti-aliasing if pixel art.
```

## Tile set

Template:

```text
Create a seamless game tile set for [environment].
Grid: [number] square tiles, equal spacing.
Tiles: [grass, dirt, path, water, corner, edge, obstacle].
Style: [pixel art/isometric/vector], consistent scale and palette.
Constraints: tiles must be readable individually, no text, no perspective mismatch, no merged borders.
```

## Item icons

Template:

```text
Create a set of [number] game item icons for [genre].
Items: [list].
Style: consistent icon system, centered objects, readable silhouettes, shared lighting direction, limited palette.
Background: plain solid or subtle circular badge.
Constraints: no text, no extra items, no inconsistent perspective, no real trademarks.
```

## App icon

Template:

```text
Create an app icon for [app].
Concept: [single clear metaphor].
Style: simple vector-like shape, strong silhouette, readable at small size, modern color palette, subtle depth only if needed.
Canvas: centered icon with padding, no text.
Constraints: original mark, no existing logos, no tiny details, no watermark.
```

## Sticker or emoji

Template:

```text
Create a cute sticker-style illustration of [subject/action].
Style: bold outline, expressive face, simple shading, high readability, centered.
Background: plain solid color for extraction later.
Optional text: "[short exact text]" only if requested.
Constraints: no watermark, no extra text, no clutter, no fake transparency checkerboard.
```

## Isometric game asset

Template:

```text
Create an isometric game asset of [object/building].
View: consistent 3/4 isometric angle, centered, no perspective distortion.
Style: [cozy/strategy/RPG/sci-fi], clean edges, readable shape language, consistent lighting.
Background: plain solid color.
Constraints: no text, no UI, no surrounding scene unless requested.
```

## Voxel or low-poly asset

Template:

```text
Create a [voxel/low-poly] 3D-style asset of [subject].
Style: simplified geometry, clean silhouette, readable material blocks, consistent lighting, game-ready presentation.
Canvas: centered object on plain background.
Constraints: no text, no complex scene, no ultra-realistic details.
```

## HUD or game UI

Template:

```text
Create a game HUD concept for [genre/platform].
Elements: [health, stamina, inventory, minimap, quest tracker].
Style: [fantasy parchment / sci-fi neon / cozy minimal], readable labels, consistent iconography.
Canvas: 16:9 gameplay overlay mockup.
Constraints: no tiny text, no lorem ipsum, no real game logos, no obstructive clutter.
```

## Texture or material swatch

Template:

```text
Create a seamless-looking material swatch sheet for [game/environment].
Swatches: [stone, grass, wood, metal, cloth].
Style: [pixel art / hand-painted / stylized PBR concept], consistent lighting, tileable impression.
Constraints: no text labels unless requested, no perspective, no shadows that break tiling.
```
