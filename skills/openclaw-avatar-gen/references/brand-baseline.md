# OpenClaw Brand Visual Reference

## The Default Mascot (Baseline)

The OpenClaw brand mascot is a **3D voxel-art red crab** used across the project's identity.

### Visual Properties (analyzed from source image)
- **Rendering:** Voxel/isometric 3D, each surface facet is a visible cube. Not flat pixel art — actual 3D depth with lighting and shadow.
- **Palette:** Warm reds (shell primary), pink-red (shell secondary/belly), black (eyes), white (specular highlights). ~6–8 colors total including shadow tones. High saturation, low complexity.
- **Lighting:** Single soft key light from upper-left, diffuse fill. Soft contact shadow on ground plane. No hard rim lights or dramatic contrast.
- **Background:** Solid light blue (#B8D4E3 approximate). No gradients, no environment.
- **Pose:** Claws raised in symmetrical "ready" pose. Frontal view. Slight low-angle camera.
- **Expression:** Tiny smug smile. Black bead eyes with white specular highlights. Reads as "playful confidence" — not aggressive.
- **Composition:** Dead center, symmetrical, tight crop with breathing room.

### What Makes It Work
- Instantly readable as a crab at any size
- The voxel style is distinctive — not generic clip art, not realistic
- Limited palette keeps it clean and reproducible
- The raised-claw pose has character without requiring context
- Contact shadow grounds it without needing an environment

### Brand Constraints for Variants
- All agent avatars MUST be crabs (not other creatures)
- All agent avatars MUST use the same voxel rendering style
- All agent avatars MUST use the same lighting setup (soft key upper-left)
- All agent avatars MUST use solid color backgrounds
- Palette can shift but should stay within 6–8 total colors
- Signifiers should modify the crab, not replace it

## Anti-Patterns (Things That Break Brand Consistency)

| Don't | Why |
|---|---|
| Smooth/organic rendering | Breaks voxel identity |
| Realistic proportions | It's a mascot, not a nature doc |
| Gradient backgrounds | Breaks the clean studio look |
| Environment/scene | Avatars are characters, not illustrations |
| More than 2 props | Unreadable at 64px, cluttered |
| Text or labels | Profile pictures should be purely visual |
| Dark/moody lighting | The brand is approachable, not edgy |
| Non-crab creatures | Family consistency is non-negotiable |

## Size Rendering Notes

| Size | Context | What Must Read |
|---|---|---|
| 64×64 | Discord sidebar, small avatar | Silhouette + primary color + 1 signifier |
| 128×128 | Chat message avatar | Color detail + expression + both signifiers |
| 256×256 | Profile modal, settings | Full detail including accent lines and prop detail |
| 512×512 | Marketing, docs, README | Everything; this is the source resolution target |

Generate at 1024×1024 minimum, then verify it works downscaled to 64×64.
