# Prompt Recipes

Use this for base prompts, row prompts, and repair prompts.

## Base Prompt Recipe

```text
Asset: <name>
Use: canonical game sprite reference for a later sprite sheet
Camera: <side-view/top-down/isometric/etc.>
Style: <art direction>
Subject: <compact identity description>
Silhouette: <large readable shape language>
Palette/materials: <limited palette and material cues>
Gameplay feel: <verbs/personality>
Output: one clean complete sprite pose, centered, full body/object visible, generous padding
Background: <flat chroma-key or neutral preview>
Preserve for all future rows: <identity lock list>
Avoid: text, UI, watermark, scene background, cropped parts, tiny unreadable detail
```

## Row Prompt Recipe

```text
Asset: <name>
Animation row: <row-id>, <frame-count> frames, <loop/non-loop>
Use: sprite-sheet row for <game/camera/style>
Input images:
- Image 1: canonical base identity reference
- Image 2: style/reference/layout image if present
Preserve exactly: <identity lock list>
Action beats:
- Frame(s) 1-2: <anticipation/start>
- Frame(s) 3-4: <main action>
- Frame(s) 5-6: <peak/recovery>
Layout: one horizontal strip, equal spacing, one complete pose per slot, centered inside each slot, no overlap
Background: perfectly flat chroma-key; do not use that color in the sprite
Avoid: text, labels, frame numbers, visible guides, scenery, detached shadows, motion blur, cropped limbs, duplicate frames, new props unless requested
```

## Repair Prompt Recipe

```text
Repair only the <row-id> row.
Keep the same asset identity as the canonical base and previous accepted rows.
The previous attempt failed because: <specific visual issue>.
Change only: <targeted fix>.
Preserve: <identity lock list>.
Do not redesign the character/prop/effect.
```

## Identity Lock Examples

- Same helmet shape, eye slit, scarf side, and lantern-spear silhouette.
- Same flame base, metal sconce, ember color order, and chunky outline.
- Same face markings, horn shape, body proportions, and side-specific scars.

## Layout Language

Use exact row language:

- "one horizontal strip"
- "equal slot spacing"
- "full body visible in every frame"
- "no frame overlaps another"
- "no visible grid or labels"
- "flat chroma-key background"

