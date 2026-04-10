/**
 * physics.js - Collision Detection and Physics Utilities
 * Production-ready collision detection for HTML5 Canvas games
 * 
 * Includes:
 * - AABB (Axis-Aligned Bounding Box) collision
 * - Circle collision
 * - Swept AABB (continuous collision for fast-moving objects)
 * - Resolution helpers (MTV - Minimal Translation Vector)
 */

/**
 * Check if two AABBs overlap
 * @param {Object} a - {x, y, w, h}
 * @param {Object} b - {x, y, w, h}
 * @returns {boolean} True if overlapping
 */
function aabbIntersects(a, b) {
  return a.x < b.x + b.w &&
         a.x + a.w > b.x &&
         a.y < b.y + b.h &&
         a.y + a.h > b.y;
}

/**
 * Resolve AABB collision - returns minimal translation vector (MTV)
 * @param {Object} a - Moving box {x, y, w, h}
 * @param {Object} b - Static box {x, y, w, h}
 * @returns {Object|null} MTV {x, y} to separate a from b, or null if not overlapping
 */
function resolveAABB(a, b) {
  const dx = (a.x + a.w/2) - (b.x + b.w/2);
  const px = (a.w + b.w)/2 - Math.abs(dx);
  if (px <= 0) return null;

  const dy = (a.y + a.h/2) - (b.y + b.h/2);
  const py = (a.h + b.h)/2 - Math.abs(dy);
  if (py <= 0) return null;

  // Return MTV along axis with smallest penetration
  if (px < py) {
    const sx = Math.sign(dx);
    return { x: px * sx, y: 0 };
  } else {
    const sy = Math.sign(dy);
    return { x: 0, y: py * sy };
  }
}

/**
 * Platformer-style collision resolution
 * Resolves Y axis first (gravity), then X axis (walls)
 * Sets entity.onGround when standing on a surface
 * 
 * @param {Object} entity - {x, y, w, h, onGround}
 * @param {Object} vel - {x, y} velocity to apply
 * @param {Array} solids - Array of static boxes {x, y, w, h}
 */
function moveAndCollideAxisSeparated(entity, vel, solids) {
  entity.onGround = false;
  
  // Y axis (vertical) - resolve gravity/jumping first
  entity.y += vel.y;
  for (const s of solids) {
    const mtv = resolveAABB(entity, s);
    if (mtv && mtv.y) {
      entity.y += -mtv.y;
      vel.y = 0;
      if (mtv.y > 0) entity.onGround = true; // Pushing up = standing on top
    }
  }
  
  // X axis (horizontal) - resolve wall sliding
  entity.x += vel.x;
  for (const s of solids) {
    const mtv = resolveAABB(entity, s);
    if (mtv && mtv.x) {
      entity.x += -mtv.x;
      vel.x = 0;
    }
  }
}

/**
 * Check if two circles overlap
 * @param {Object} a - {x, y, r} (center x, y and radius)
 * @param {Object} b - {x, y, r}
 * @returns {boolean} True if overlapping
 */
function circleIntersects(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  const r = a.r + b.r;
  return dx*dx + dy*dy <= r*r;
}

/**
 * Resolve circle collision - separate two overlapping circles
 * @param {Object} a - {x, y, r}
 * @param {Object} b - {x, y, r}
 */
function resolveCircle(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  let d2 = dx*dx + dy*dy;
  
  if (d2 === 0) {
    // Identical centers - nudge apart
    a.x += 0.01;
    return;
  }
  
  const d = Math.sqrt(d2);
  const overlap = a.r + b.r - d;
  
  if (overlap > 0) {
    const nx = dx / d;
    const ny = dy / d;
    // Separate equally (change to unequal if one is static)
    a.x += nx * (overlap/2);
    a.y += ny * (overlap/2);
    b.x -= nx * (overlap/2);
    b.y -= ny * (overlap/2);
  }
}

/**
 * Swept AABB collision - continuous collision detection
 * Prevents tunneling for fast-moving objects
 * 
 * @param {Object} m - Moving box {x, y, w, h}
 * @param {Object} v - Velocity {x, y}
 * @param {Object} s - Static box {x, y, w, h}
 * @returns {Object|null} {toi, nx, ny} where toi is time of impact [0,1] and (nx,ny) is collision normal
 */
function sweptAABB(m, v, s) {
  // Expand static box by moving box size, then raycast point -> expanded box
  const invEntryX = (v.x > 0 ? s.x - (m.x + m.w) : (s.x + s.w) - m.x);
  const invEntryY = (v.y > 0 ? s.y - (m.y + m.h) : (s.y + s.h) - m.y);
  const invExitX  = (v.x > 0 ? (s.x + s.w) - m.x : s.x - (m.x + m.w));
  const invExitY  = (v.y > 0 ? (s.y + s.h) - m.y : s.y - (m.y + m.h));

  const entryX = v.x === 0 ? -Infinity : invEntryX / v.x;
  const exitX  = v.x === 0 ?  Infinity : invExitX  / v.x;
  const entryY = v.y === 0 ? -Infinity : invEntryY / v.y;
  const exitY  = v.y === 0 ?  Infinity : invExitY  / v.y;

  const entryT = Math.max(Math.min(entryX, exitX), Math.min(entryY, exitY));
  const exitT  = Math.min(Math.max(entryX, exitX), Math.max(entryY, exitY));
  
  // No collision if:
  if (entryT > exitT ||  // Entry after exit
      entryT > 1 ||      // Beyond this frame
      entryT < 0) {      // Behind start
    return null;
  }

  // Calculate collision normal
  let nx = 0, ny = 0;
  if (entryX > entryY) {
    nx = (invEntryX < 0) ? 1 : -1;
  } else {
    ny = (invEntryY < 0) ? 1 : -1;
  }

  return { toi: entryT, nx, ny };
}

/**
 * Integrate movement with swept collision detection
 * Handles sliding along walls after collision
 * 
 * @param {Object} m - Moving box {x, y, w, h}
 * @param {Object} v - Velocity {x, y} per second
 * @param {Array} solids - Array of static boxes
 * @param {number} dt - Delta time (seconds)
 */
function integrateSwept(m, v, solids, dt) {
  const vel = { x: v.x * dt, y: v.y * dt };
  let tRem = 1.0;
  let iter = 0;
  
  // Iterate up to 4 times to handle sliding along multiple surfaces
  while (tRem > 0 && iter++ < 4) {
    let earliest = { toi: 1, nx: 0, ny: 0, hit: null };
    
    // Find earliest collision
    for (const s of solids) {
      const hit = sweptAABB(m, { x: vel.x * tRem, y: vel.y * tRem }, s);
      if (hit && hit.toi < earliest.toi) {
        earliest = { ...hit, hit: s };
      }
    }
    
    // No collision - move remaining distance
    if (!earliest.hit) {
      m.x += vel.x * tRem;
      m.y += vel.y * tRem;
      break;
    }
    
    // Move to contact point
    m.x += vel.x * tRem * earliest.toi;
    m.y += vel.y * tRem * earliest.toi;
    tRem *= (1 - earliest.toi);
    
    // Slide: null out velocity component along collision normal
    if (earliest.nx !== 0) vel.x = 0;
    if (earliest.ny !== 0) vel.y = 0;
  }
}

/**
 * Check AABB vs Circle collision
 * @param {Object} a - AABB {x, y, w, h}
 * @param {Object} c - Circle {x, y, r}
 * @returns {boolean} True if overlapping
 */
function aabbCircleOverlap(a, c) {
  // Find closest point on AABB to circle center
  const cx = Math.max(a.x, Math.min(c.x, a.x + a.w));
  const cy = Math.max(a.y, Math.min(c.y, a.y + a.h));
  const dx = c.x - cx;
  const dy = c.y - cy;
  return (dx*dx + dy*dy) <= c.r*c.r;
}

/**
 * Get all tile cells overlapping an AABB (for grid-based collision)
 * @param {Object} aabb - {x, y, w, h}
 * @param {number} tileSize - Size of each tile
 * @returns {Array} Array of {x, y} tile coordinates
 */
function tilesOverlapping(aabb, tileSize) {
  const x0 = Math.floor(aabb.x / tileSize);
  const y0 = Math.floor(aabb.y / tileSize);
  const x1 = Math.floor((aabb.x + aabb.w - 1) / tileSize);
  const y1 = Math.floor((aabb.y + aabb.h - 1) / tileSize);
  
  const cells = [];
  for (let y = y0; y <= y1; y++) {
    for (let x = x0; x <= x1; x++) {
      cells.push({x, y});
    }
  }
  return cells;
}
