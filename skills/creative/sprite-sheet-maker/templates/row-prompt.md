Asset: <name>
Animation row: <row-id>, <frame-count> frames, <loop/non-loop>
Use: sprite-sheet row for <game/camera/style>
Input images:
- Image 1: canonical base identity reference
Preserve exactly: <identity lock list>
Action beats:
- Frame(s) 1-2: <anticipation/start>
- Frame(s) 3-4: <main action>
- Frame(s) 5-6: <peak/recovery>
Layout: one horizontal strip, equal spacing, one complete pose per slot, centered inside each slot, no overlap
Background: perfectly flat chroma-key; do not use that color in the sprite
Avoid: text, labels, frame numbers, visible guides, scenery, detached shadows, motion blur, cropped limbs, duplicate frames, new props unless requested

