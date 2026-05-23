# Game Loop & Architecture

> Core patterns for every simulation and game. Load this on every task.

## Fixed Timestep Loop

The only correct game loop pattern. Decouples physics (deterministic, fixed rate) from rendering (variable, interpolated).

```javascript
const STEP = 1/60;
const MAX_ACC = 0.25; // Spiral-of-death cap
let acc = 0, last = performance.now() / 1000;

function loop(nowMs) {
  const now = nowMs / 1000;
  acc += Math.min(MAX_ACC, now - last);
  last = now;
  while (acc >= STEP) { fixedUpdate(STEP); acc -= STEP; }
  render(acc / STEP); // alpha for interpolation
  requestAnimationFrame(loop);
}
```

**Why MAX_ACC matters:** If the tab is backgrounded, `dt` can spike to seconds. Without capping, the physics loop tries to catch up with hundreds of steps → freezes → more dt → death spiral.

**Why interpolation matters:** Without `alpha` blending between current and previous state, motion stutters on monitors whose refresh rate isn't a multiple of 60Hz.

⤷ Full game loop patterns: `grep -A 60 "Game Loop" references/deep/run-01-game-engine-fundamentals.md`

## Entity Architecture

### Structure-of-Arrays (SoA)

For performance-critical systems (particles, physics bodies), store components in parallel typed arrays:

```javascript
const MAX = 10000;
const x = new Float32Array(MAX);
const y = new Float32Array(MAX);
const vx = new Float32Array(MAX);
const vy = new Float32Array(MAX);
let count = 0;
```

**Why not Array-of-Structs:** AoS creates individual objects → GC pressure. SoA uses flat typed arrays → zero GC, cache-friendly iteration, directly uploadable to GPU buffers.

### Object Pool + Swap-and-Pop

```javascript
function kill(i) {
  count--;
  x[i] = x[count]; y[i] = y[count];
  vx[i] = vx[count]; vy[i] = vy[count];
}
```

No splice, no filter, no allocation. O(1) removal by swapping the dead element with the last live one.

⤷ Full ECS and pooling: `grep -A 80 "ECS" references/deep/run-01-game-engine-fundamentals.md`

## Spatial Hash Grid

The recommended broadphase for JS. O(1) average insertion and query.

```javascript
class SpatialHash {
  constructor(cellSize) {
    this.cellSize = cellSize;
    this.cells = new Map();
  }
  _key(x, y) { return `${x|0},${y|0}`; }
  clear() { this.cells.clear(); }
  insert(id, aabb) {
    const cs = this.cellSize;
    for (let gx = Math.floor(aabb.x/cs); gx <= Math.floor((aabb.x+aabb.w)/cs); gx++)
      for (let gy = Math.floor(aabb.y/cs); gy <= Math.floor((aabb.y+aabb.h)/cs); gy++) {
        const k = this._key(gx, gy);
        if (!this.cells.has(k)) this.cells.set(k, []);
        this.cells.get(k).push(id);
      }
  }
  query(aabb) {
    const cs = this.cellSize, result = new Set();
    for (let gx = Math.floor(aabb.x/cs); gx <= Math.floor((aabb.x+aabb.w)/cs); gx++)
      for (let gy = Math.floor(aabb.y/cs); gy <= Math.floor((aabb.y+aabb.h)/cs); gy++) {
        const bucket = this.cells.get(this._key(gx, gy));
        if (bucket) bucket.forEach(id => result.add(id));
      }
    return result;
  }
}
```

**Cell size rule of thumb:** 2× the largest entity's bounding dimension.

⤷ Full spatial hash details: `grep -A 40 "Spatial" references/deep/run-01-game-engine-fundamentals.md`

## State Machine

```javascript
const STATES = { MENU: 0, PLAYING: 1, PAUSED: 2, GAME_OVER: 3 };
let state = STATES.MENU;
function fixedUpdate(dt) {
  if (state === STATES.PLAYING) { /* sim logic */ }
}
```

⤷ Scene management patterns: `grep -A 40 "State" references/deep/run-01-game-engine-fundamentals.md`

## Page Visibility (Mandatory)

```javascript
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { paused = true; }
  else { last = performance.now() / 1000; paused = false; }
});
```

Reset `last` on resume to prevent dt spike.
