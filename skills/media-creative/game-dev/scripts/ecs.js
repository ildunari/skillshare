/**
 * ecs.js - Minimal Entity-Component System
 * 
 * Lightweight ECS for composition-based architecture
 * Fast enough for mid-size canvas games (<1000 entities)
 * 
 * Usage:
 *   // Define component stores
 *   const C = {
 *     Position: new Map(),
 *     Velocity: new Map(),
 *     Sprite: new Map(),
 *     Health: new Map()
 *   };
 *   
 *   // Create entity
 *   const player = createEntity(
 *     [C.Position, { x: 100, y: 100 }],
 *     [C.Velocity, { x: 0, y: 0 }],
 *     [C.Sprite, { img: playerImg, w: 32, h: 32 }],
 *     [C.Health, { current: 100, max: 100 }]
 *   );
 *   
 *   // Query entities
 *   for (const [id, pos, vel] of query(C.Position, C.Velocity)) {
 *     pos.x += vel.x * dt;
 *     pos.y += vel.y * dt;
 *   }
 */

// Entity ID generator
const nextId = (() => {
  let id = 0;
  return () => ++id;
})();

/**
 * Create a new entity with components
 * @param {...Array} comps - Component pairs [store, data]
 * @returns {number} Entity ID
 * 
 * Example:
 *   const e = createEntity(
 *     [C.Position, { x: 0, y: 0 }],
 *     [C.Velocity, { x: 100, y: 0 }]
 *   );
 */
function createEntity(...comps) {
  const e = nextId();
  comps.forEach(([store, data]) => store.set(e, data));
  return e;
}

/**
 * Destroy an entity (remove from all component stores)
 * @param {number} e - Entity ID
 * @param {...Map} stores - All component stores to check
 */
function destroyEntity(e, ...stores) {
  stores.forEach(store => store.delete(e));
}

/**
 * Query entities that have all specified components
 * @param {...Map} stores - Component stores to query
 * @yields {Array} [entityId, ...componentData]
 * 
 * Example:
 *   for (const [id, pos, vel] of query(C.Position, C.Velocity)) {
 *     console.log(`Entity ${id} at ${pos.x}, ${pos.y}`);
 *   }
 */
function* query(...stores) {
  const [head, ...rest] = stores;
  
  for (const [e, data] of head) {
    // Check if entity has all required components
    if (rest.every(s => s.has(e))) {
      yield [e, data, ...rest.map(s => s.get(e))];
    }
  }
}

/**
 * Check if entity has a component
 * @param {number} e - Entity ID
 * @param {Map} store - Component store
 * @returns {boolean}
 */
function hasComponent(e, store) {
  return store.has(e);
}

/**
 * Add component to entity
 * @param {number} e - Entity ID
 * @param {Map} store - Component store
 * @param {*} data - Component data
 */
function addComponent(e, store, data) {
  store.set(e, data);
}

/**
 * Remove component from entity
 * @param {number} e - Entity ID
 * @param {Map} store - Component store
 */
function removeComponent(e, store) {
  store.delete(e);
}

/**
 * Get component data
 * @param {number} e - Entity ID
 * @param {Map} store - Component store
 * @returns {*} Component data or undefined
 */
function getComponent(e, store) {
  return store.get(e);
}

/**
 * Example System Functions
 * Systems operate on entities with specific component combinations
 */

/**
 * Physics system - updates positions based on velocities
 * @param {number} dt - Delta time
 */
function physicsSystem(dt, C) {
  for (const [e, pos, vel] of query(C.Position, C.Velocity)) {
    pos.x += vel.x * dt;
    pos.y += vel.y * dt;
  }
}

/**
 * Gravity system - applies gravity to entities with velocity
 * @param {number} dt - Delta time
 * @param {number} gravity - Gravity constant (e.g., 2000)
 */
function gravitySystem(dt, gravity, C) {
  for (const [e, vel] of query(C.Velocity)) {
    vel.y += gravity * dt;
  }
}

/**
 * Render system - draws sprites at positions
 * @param {CanvasRenderingContext2D} ctx - Canvas context
 */
function renderSystem(ctx, C) {
  for (const [e, pos, spr] of query(C.Position, C.Sprite)) {
    const sx = spr.sx || 0;
    const sy = spr.sy || 0;
    const sw = spr.sw || spr.w;
    const sh = spr.sh || spr.h;
    
    ctx.drawImage(
      spr.img,
      sx, sy, sw, sh,
      Math.round(pos.x), Math.round(pos.y), sw, sh
    );
  }
}

/**
 * Lifetime system - removes entities after a certain time
 * @param {number} dt - Delta time
 */
function lifetimeSystem(dt, C, allStores) {
  const toDestroy = [];
  
  for (const [e, lifetime] of query(C.Lifetime)) {
    lifetime.remaining -= dt;
    if (lifetime.remaining <= 0) {
      toDestroy.push(e);
    }
  }
  
  // Destroy expired entities
  toDestroy.forEach(e => destroyEntity(e, ...allStores));
}

/**
 * Example: Complete ECS Setup
 * 
 * // 1. Define component stores
 * const C = {
 *   Position: new Map(),
 *   Velocity: new Map(),
 *   Sprite: new Map(),
 *   AABB: new Map(),
 *   Health: new Map(),
 *   Lifetime: new Map()
 * };
 * 
 * // 2. Create entities
 * const player = createEntity(
 *   [C.Position, { x: 400, y: 300 }],
 *   [C.Velocity, { x: 0, y: 0 }],
 *   [C.AABB, { w: 32, h: 32 }],
 *   [C.Health, { current: 100, max: 100 }]
 * );
 * 
 * const bullet = createEntity(
 *   [C.Position, { x: 400, y: 300 }],
 *   [C.Velocity, { x: 500, y: 0 }],
 *   [C.AABB, { w: 4, h: 4 }],
 *   [C.Lifetime, { remaining: 2.0 }]
 * );
 * 
 * // 3. Run systems in game loop
 * function update(dt) {
 *   physicsSystem(dt, C);
 *   lifetimeSystem(dt, C, Object.values(C));
 *   
 *   // Custom collision system
 *   for (const [e1, pos1, aabb1] of query(C.Position, C.AABB)) {
 *     for (const [e2, pos2, aabb2] of query(C.Position, C.AABB)) {
 *       if (e1 >= e2) continue;
 *       if (aabbIntersects(
 *         {x: pos1.x, y: pos1.y, w: aabb1.w, h: aabb1.h},
 *         {x: pos2.x, y: pos2.y, w: aabb2.w, h: aabb2.h}
 *       )) {
 *         // Handle collision
 *       }
 *     }
 *   }
 * }
 * 
 * function render(ctx) {
 *   renderSystem(ctx, C);
 * }
 */

/**
 * Performance Tips:
 * 
 * 1. For thousands of entities, use typed arrays (Struct-of-Arrays):
 *    const C = {
 *      Position: {
 *        x: new Float32Array(MAX_ENTITIES),
 *        y: new Float32Array(MAX_ENTITIES)
 *      }
 *    };
 * 
 * 2. Batch similar entities (all bullets, all enemies) for cache efficiency
 * 
 * 3. Use bitsets for component membership if querying many combinations
 * 
 * 4. Keep component data minimal - avoid nested objects
 */
