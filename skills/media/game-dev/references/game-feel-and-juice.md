# Game Feel & Juice

> Screen shake, hit stop, coyote time, camera systems, and the feedback hierarchy that makes games feel alive.

## Core Principle

Juice is layered on **after** the simulation works correctly. The hierarchy: get it working → get it feeling good → get it looking good.

## Trauma-Based Screen Shake

The gold standard. A single `trauma` float (0-1) drives shake intensity. Squared falloff feels natural.

```javascript
class TraumaShake {
  constructor() { this.trauma = 0; this.decay = 2.0; }
  
  add(amount) { this.trauma = Math.min(1, this.trauma + amount); }
  
  update(dt) {
    this.trauma = Math.max(0, this.trauma - this.decay * dt);
    const shake = this.trauma * this.trauma; // quadratic falloff
    return {
      x: (Math.random() * 2 - 1) * shake * 16, // max 16px offset
      y: (Math.random() * 2 - 1) * shake * 12,
      angle: (Math.random() * 2 - 1) * shake * 0.05 // radians
    };
  }
}
```

**Better noise:** Replace `Math.random()` with Perlin/simplex noise sampled at `time * frequency` for smoother, more directional shake.

**Trauma amounts:** Light hit = 0.2, heavy hit = 0.5, explosion = 0.8, death = 1.0.

⤷ Full shake systems: `grep -A 80 "shake\|Shake\|trauma" references/deep/run-08-game-feel-juice.md`

## Hit Stop (Freeze Frames)

Pause the game for a few frames on impactful events. Sells the weight of hits.

```javascript
let hitStopTimer = 0;
function triggerHitStop(durationMs) { hitStopTimer = durationMs; }
function fixedUpdate(dt) {
  if (hitStopTimer > 0) { hitStopTimer -= dt * 1000; return; } // skip physics
  // ... normal update
}
```

**Durations:** Light = 30-50ms (2-3 frames). Medium = 80-120ms. Heavy = 150-200ms.

**Selective freeze:** Freeze the attacker/target but keep particles/effects running for visual richness during the pause.

⤷ Full hit stop patterns: `grep -A 40 "hit stop\|freeze frame" references/deep/run-08-game-feel-juice.md`

## Platformer Feel

### Coyote Time (~100ms)
Allow jumping for a brief window after walking off a ledge:
```javascript
let coyoteTimer = 0;
if (onGround) coyoteTimer = 0.1; // seconds
else coyoteTimer -= dt;
const canJump = coyoteTimer > 0;
```

### Jump Buffering (~100ms)
Register jump input slightly before landing:
```javascript
let jumpBuffer = 0;
if (jumpPressed) jumpBuffer = 0.1;
else jumpBuffer -= dt;
if (onGround && jumpBuffer > 0) { jump(); jumpBuffer = 0; }
```

### Variable Jump Height
Release jump button early = lower jump:
```javascript
if (jumpReleased && vel.y < 0) vel.y *= 0.5; // cut upward velocity
```

### Other Platformer Tweaks
- **Faster fall:** Increase gravity when falling (`vy > 0`) by 1.5-2×
- **Hang time:** Reduce gravity near jump apex (`abs(vy) < threshold`) for floaty peak
- **Dash recovery:** Brief invincibility + speed boost, with 2-3 frame anticipation animation

⤷ Full platformer tuning: `grep -A 80 "coyote\|Coyote\|jump buffer\|platformer" references/deep/run-08-game-feel-juice.md`

## Camera Systems

### Frame-Rate Independent Smoothing
```javascript
camera.x = lerp(camera.x, target.x, 1 - Math.pow(damping, dt));
camera.y = lerp(camera.y, target.y, 1 - Math.pow(damping, dt));
```
`damping = 0.01` for tight follow, `0.0001` for cinematic drift. This formula gives identical results regardless of frame rate.

### Look-Ahead
Offset the camera target in the direction of player movement:
```javascript
lookAheadTarget.x = player.x + player.vx * lookAheadTime;
```

### Dead Zone
Don't move camera until player exceeds a threshold distance from screen center. Prevents micro-jitter on small movements.

### Bounds Clamping
```javascript
camera.x = clamp(camera.x, levelLeft + halfScreenW, levelRight - halfScreenW);
```

⤷ Full camera systems: `grep -A 60 "camera\|Camera" references/deep/run-08-game-feel-juice.md`

## Feedback Hierarchy

Categorize game events by impact level and apply proportional feedback:

| Level | Events | Visual | Audio | Feel |
|-------|--------|--------|-------|------|
| **Low** | Pickup, footstep, UI hover | Subtle flash/scale | Quiet SFX | None |
| **Medium** | Hit, jump, dash | Particles, flash | Impact SFX | Light shake (0.2) |
| **High** | Kill, explosion, boss hit | Screen flash, debris, slow-mo | Layered SFX | Heavy shake (0.5-0.8), hit stop |

**Rule:** Every event should have feedback from at least 2 channels (visual + audio, or visual + feel).

## Slow Motion

```javascript
let timeScale = 1.0;
function triggerSlowMo(scale, duration) { timeScale = scale; /* restore after duration */ }
function fixedUpdate(dt) { dt *= timeScale; /* ... */ }
```

**Pair with:** Hit stop (slow-mo after the freeze), screen shake, radial blur post-process.

## Particle Juice Patterns

- **Impact sparks:** 5-15 fast particles in a cone along the collision normal
- **Death explosion:** 20-40 particles in all directions + screen shake + hit stop
- **Trail:** 1-2 particles per frame behind moving objects, short life, additive blend
- **Dust puff:** 3-5 slow particles at feet on land/dash, gravity affected

⤷ Full juice catalog: `grep -A 100 "juice\|Juice\|feedback" references/deep/run-08-game-feel-juice.md`
