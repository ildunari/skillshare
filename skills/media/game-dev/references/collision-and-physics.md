# Collision Detection & Physics

> 2D collision detection, impulse resolution, and physics solver patterns.

## Broadphase → Narrowphase Pipeline

1. **Broadphase:** Spatial hash grid (see `game-loop-and-architecture.md`) generates collision pairs
2. **Narrowphase:** Test each pair with SAT or circle-circle
3. **Resolution:** Apply impulse or positional correction

## AABB Overlap

```javascript
function aabbOverlap(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x &&
         a.y < b.y + b.h && a.y + a.h > b.y;
}
```

## Separating Axis Theorem (SAT)

For convex polygons. Test all edge normals of both shapes; if any axis has no overlap, shapes are separated.

**Key insight:** For AABBs, SAT simplifies to the 4-axis AABB test above. SAT's power is for rotated/irregular convex shapes.

Returns: overlap depth + collision normal (minimum translation vector).

**Sutherland-Hodgman clipping** generates the contact manifold (contact points) needed for stable stacking.

⤷ Full SAT implementation: `grep -A 100 "SAT" references/deep/run-02-collision-physics.md`
⤷ Clipping algorithm: `grep -A 60 "Sutherland" references/deep/run-02-collision-physics.md`

## Circle Collision

```javascript
function circleOverlap(a, b) {
  const dx = b.x - a.x, dy = b.y - a.y;
  const dist = Math.sqrt(dx*dx + dy*dy);
  const minDist = a.r + b.r;
  if (dist >= minDist) return null;
  const nx = dx/dist, ny = dy/dist;
  return { depth: minDist - dist, nx, ny };
}
```

## Impulse Resolution

The core formula for rigid body collision response:

```
j = -(1+e)(v_rel · n) / (1/m_a + 1/m_b + (r_a × n)²/I_a + (r_b × n)²/I_b)
```

Where: `e` = restitution (bounciness 0-1), `n` = collision normal, `r` = lever arm from center of mass to contact point, `I` = moment of inertia.

For circles without rotation, simplifies to:
```javascript
const j = -(1 + e) * vRelDotN / (1/massA + 1/massB);
a.vx += j * nx / massA;
a.vy += j * ny / massA;
b.vx -= j * nx / massB;
b.vy -= j * ny / massB;
```

⤷ Full impulse solver with rotation: `grep -A 80 "impulse" references/deep/run-02-collision-physics.md`

## Swept AABB (Continuous Collision)

Prevents tunneling for fast-moving objects. Finds the exact time `t` (0-1) of first contact along the velocity vector.

Use when: object moves more than half its width per frame (bullets, high-speed projectiles).

⤷ Full swept AABB: `grep -A 60 "Swept" references/deep/run-02-collision-physics.md`

## Sequential Impulse Solver

For stable stacking and friction. Iteratively solves constraints over multiple passes (4-8 iterations typical).

**Key properties:**
- Warm starting (reuse previous frame's impulses as initial guess)
- Accumulated impulse clamping (prevents over-correction)
- Good friction and stacking quality

**Use for:** Game physics where stacking boxes, friction, and "solid feel" matter.

⤷ Full SI solver: `grep -A 100 "Sequential" references/deep/run-02-collision-physics.md`

## XPBD (Extended Position-Based Dynamics)

Position-based solver with unconditional stability. Easier to implement than SI, better for soft constraints.

**Key properties:**
- Compliance parameter controls stiffness (0 = rigid, >0 = soft)
- Never explodes regardless of timestep
- Ideal for cloth, soft bodies, ropes, ragdolls

**Use for:** Simulation accuracy, soft bodies, visual physics. Less ideal for stacking.

⤷ Full XPBD: `grep -A 80 "XPBD" references/deep/run-04-realtime-physics-sim.md`

## Rapier (WASM Physics)

When you need serious physics without writing a solver:
- 5k-10k rigid bodies at 60fps
- GJK+EPA collision (shape-agnostic)
- Dynamic BVH broadphase (SIMD in WASM)
- Joint constraints, CCD, events

```javascript
import('@dimforge/rapier2d').then(RAPIER => {
  const world = new RAPIER.World({ x: 0, y: 9.81 });
  // ... create bodies and colliders
});
```

⤷ Rapier integration details: `grep -A 60 "Rapier" references/deep/run-04-realtime-physics-sim.md`

## Platformer-Specific

- **Resolve Y before X** for proper wall sliding
- **Coyote time** (~100ms grace period after leaving ledge) — see `game-feel-and-juice.md`
- **Ground detection:** Tiny raycast or overlap below feet, not velocity check
