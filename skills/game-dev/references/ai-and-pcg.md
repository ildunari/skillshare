# AI & Procedural Generation

> Game AI decision-making, pathfinding, and procedural content generation for browser games.

## Decision Making

### Behavior Trees
Modular, composable AI. Best for complex NPC behavior.

**Node types:**
- **Sequence** (→): Run children left-to-right. Fail on first failure. (AND logic)
- **Selector** (?): Run children left-to-right. Succeed on first success. (OR logic)  
- **Leaf:** Action (do something) or Condition (check something)
- **Decorator:** Modify child (Inverter, Repeater, Cooldown)

```
Selector [?]
├── Sequence [→] "Attack"
│   ├── Condition: "Target in range?"
│   ├── Condition: "Has ammo?"
│   └── Action: "Fire weapon"
├── Sequence [→] "Chase"
│   ├── Condition: "Target visible?"
│   └── Action: "Move toward target"
└── Action: "Patrol"
```

**Blackboard pattern:** Shared data object that all nodes read/write. Stores target position, alert state, etc.

**Tick budget:** Run BT at 10Hz (not every frame). Use a simple timer to skip ticks.

⤷ Full BT implementation: `grep -A 80 "Behavior Tree\|BehaviorTree" references/deep/run-09-ai-pcg.md`

### Utility AI
Score-based decision making. Best for needs-driven NPCs (Sims-style).

Each action gets a score based on current state. Highest score wins.

```javascript
const actions = [
  { name: 'eat',   score: () => (1 - hunger) * 0.8 + isNearFood * 0.2 },
  { name: 'sleep', score: () => (1 - energy) * 0.7 },
  { name: 'fight', score: () => threatLevel * 0.9 * hasWeapon },
];
const best = actions.reduce((a, b) => a.score() > b.score() ? a : b);
```

**Response curves:** Linear, quadratic, logistic, step. Shape the urgency of each need.

⤷ Full Utility AI: `grep -A 60 "Utility AI\|utility" references/deep/run-09-ai-pcg.md`

### Finite State Machines
Simplest approach. Fine for enemies with 2-4 states.
```javascript
const states = { PATROL: 0, CHASE: 1, ATTACK: 2 };
// Transition logic in update
if (state === states.PATROL && canSeePlayer) state = states.CHASE;
```

## Pathfinding

### A* (Single Agent)
Optimal path for one agent on a grid or navmesh.

**Heuristic:** Manhattan distance for 4-dir grid, Octile for 8-dir, Euclidean for navmesh.

**Performance:** Fine for grids up to ~200×200 with occasional re-paths. Cache paths when possible.

⤷ Full A*: `grep -A 80 "A\*\|pathfind" references/deep/run-09-ai-pcg.md`

### Flow Fields (Many Agents)
Precompute a direction vector at every grid cell pointing toward the goal. All agents just read their cell's direction. O(1) per agent per frame.

**Steps:**
1. BFS/Dijkstra from goal → cost field
2. Gradient of cost field → direction field
3. Each agent samples direction at its position and moves

**Use when:** >20 agents sharing the same destination (RTS, tower defense, crowd sim).

⤷ Full flow fields: `grep -A 60 "Flow Field\|flow field" references/deep/run-09-ai-pcg.md`

### Dijkstra Maps
Multiple goals simultaneously. Each cell stores distance to nearest goal. Useful for "flee from all enemies" or "find nearest resource."

## Procedural Generation

### BSP Dungeon Generation
1. Start with full rectangle
2. Recursively split into two halves (alternate H/V)
3. Place rooms inside leaf nodes
4. Connect rooms along split tree edges with corridors

**Control:** Min room size, split ratio randomness, corridor width.

### Cyclic Dungeon Generation (Dormans)
Graph-based approach ensuring dungeons have key-lock puzzles and multiple paths.

1. Build abstract graph with cycles (loops)
2. Assign keys and locks to edges/nodes
3. Realize graph as spatial rooms and corridors

⤷ Dungeon generation: `grep -A 80 "dungeon\|BSP\|Cyclic" references/deep/run-09-ai-pcg.md`

### Wave Function Collapse (WFC)
Constraint propagation for tile-based generation. Each cell starts with all possible tiles. Collapse the lowest-entropy cell, propagate adjacency constraints, repeat.

**Use for:** Tile-based maps, terrain, city layouts, texture synthesis.

### Perlin/Simplex Terrain
See `generative-art.md` for noise functions. Layer fBm for heightmaps, apply biome thresholds.

## Libraries

- **rot.js** — Roguelike toolkit (FOV, pathfinding, map gen, RNG)
- **Yuka** — Game AI library (steering behaviors, navmesh, state machines, BTs)
- **recast-navigation-js** — WASM navmesh generation
