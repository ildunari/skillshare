# Repair Playbook

Use this when a base, row, or final sheet fails QA.

## Diagnose First

Name the failure precisely:

- identity drift
- wrong camera
- wrong frame count
- duplicate frames
- motion unreadable
- clipped pose
- slot overlap
- accidental scenery
- chroma-key contamination
- text/labels/grid marks
- unwanted prop or missing prop
- loop pop

## Smallest Repair

1. Tighten prompt wording.
2. Regenerate one row.
3. Regenerate the base if all rows inherit a bad identity.
4. Redesign the action list only if the moveset itself is wrong.

## Common Fixes

### Identity Drift

Repeat the identity locks early in the prompt. Attach canonical base. Remove style words that invite redesign, such as "alternate", "variation", "new version", or "inspired by".

### Duplicate Frames

Specify distinct action beats by frame group. Use verbs with pose changes: lean, squash, stretch, lift, recoil, settle.

### Motion Blur Instead Of Animation

Ask for crisp discrete poses, no blur/smear/streaks, and clear silhouette changes.

### Chroma-Key Problems

Choose a key color absent from the asset. For fire/green/blue assets, avoid conflicting keys. Ask for no shadows, glows, haze, floor plane, or gradients on the background.

### Slot Overlap

Ask for one complete pose per slot, equal spacing, generous padding, and no overlap. Use a layout guide only as an invisible reference.

