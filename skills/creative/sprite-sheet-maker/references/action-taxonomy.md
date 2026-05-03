# Action Taxonomy

Use this file when deciding which animation rows belong in a sprite sheet.

## Characters

### Platformer or side-view action

- `idle`: neutral breathing, blink, hair/cloth motion.
- `walk`: slower locomotion with clear foot contacts.
- `run`: faster locomotion with stronger lean and larger spacing.
- `jump`: anticipation, takeoff, peak, descent, land.
- `fall`: optional loop or held pose for long airtime.
- `crouch`: squash, defensive posture, or prepare action.
- `attack-light`: quick primary strike with short recovery.
- `attack-heavy`: larger windup, impact, recovery.
- `attack-ranged`: aim, fire/release, recoil, settle.
- `special`: signature ability, magic, charge, transformation, or gadget.
- `block` or `parry`: defensive anticipation and active pose.
- `hurt`: one readable recoil.
- `death` or `defeat`: non-looping collapse, dissolve, or exit.

### Top-down or four-direction RPG

- `idle-down`, `idle-up`, `idle-side`
- `walk-down`, `walk-up`, `walk-side`
- `attack-down`, `attack-up`, `attack-side`
- `cast-down`, `cast-up`, `cast-side`
- `hurt`, `defeat`

Generate side rows separately when asymmetry, held weapons, readable markings, or lighting makes mirroring unsafe.

## Props

- Torch/candle/lamp: `idle-flame`, `flare`, `dim`, `extinguish`, `relight`.
- Door/gate: `closed`, `open`, `opened`, optional `close`.
- Chest/container: `idle`, `open`, `opened`, optional `loot-glow`.
- Switch/button: `idle`, `press`, `active`, optional `reset`.
- Pickup/collectible: `idle`, `spark`, `collect`, optional `respawn`.
- Hazard: `idle`, `warning`, `active`, `cooldown`.

## Effects

- Projectile: `spawn`, `travel-loop`, `impact`, optional `dissipate`.
- Explosion: `anticipation`, `burst`, `smoke`, `fade`.
- Magic aura: `spawn`, `active-loop`, `pulse`, `dissipate`.
- Slash/swing: `windup`, `arc`, `impact`, `fade`.

Keep effects in separate sheets when they would need independent timing, blending, color channels, or collision boxes.

