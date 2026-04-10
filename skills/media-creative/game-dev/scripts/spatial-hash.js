/**
 * spatial-hash.js - Spatial Hash Grid for Broad-Phase Collision
 * 
 * Efficiently query nearby objects in O(1) instead of checking all pairs O(n²)
 * Use for games with >50 dynamic objects
 * 
 * Usage:
 *   const hash = new SpatialHash(64); // 64px cell size
 *   hash.clear();
 *   entities.forEach(e => hash.insert(e.id, e.bounds));
 *   const nearby = hash.query(player.bounds);
 */

class SpatialHash {
  /**
   * @param {number} cellSize - Size of each grid cell (e.g., 64px)
   */
  constructor(cellSize = 64) {
    this.cell = cellSize;
    this.map = new Map(); // cellKey -> [entity IDs]
  }
  
  /**
   * Generate cell key from x,y coordinates
   * @private
   */
  key(x, y) {
    return (x << 16) ^ y;
  }
  
  /**
   * Convert world coordinate to cell coordinate
   * @private
   */
  cellCoord(v) {
    return Math.floor(v / this.cell);
  }
  
  /**
   * Insert an object into the spatial hash
   * @param {*} id - Unique identifier for this object
   * @param {Object} aabb - Bounding box {x, y, w, h}
   */
  insert(id, aabb) {
    const x0 = this.cellCoord(aabb.x);
    const y0 = this.cellCoord(aabb.y);
    const x1 = this.cellCoord(aabb.x + aabb.w);
    const y1 = this.cellCoord(aabb.y + aabb.h);
    
    // Insert into all cells the AABB overlaps
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const k = this.key(x, y);
        if (!this.map.has(k)) {
          this.map.set(k, []);
        }
        this.map.get(k).push(id);
      }
    }
  }
  
  /**
   * Query all objects that might collide with this AABB
   * @param {Object} aabb - Query bounds {x, y, w, h}
   * @returns {Array} Array of unique entity IDs
   */
  query(aabb) {
    const seen = new Set();
    const out = [];
    
    const x0 = this.cellCoord(aabb.x);
    const y0 = this.cellCoord(aabb.y);
    const x1 = this.cellCoord(aabb.x + aabb.w);
    const y1 = this.cellCoord(aabb.y + aabb.h);
    
    // Check all cells this AABB overlaps
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const arr = this.map.get(this.key(x, y));
        if (!arr) continue;
        
        // Collect unique IDs
        for (const id of arr) {
          if (!seen.has(id)) {
            seen.add(id);
            out.push(id);
          }
        }
      }
    }
    
    return out;
  }
  
  /**
   * Clear all entries (call before rebuilding each frame)
   */
  clear() {
    this.map.clear();
  }
}

/**
 * Example usage in a game loop:
 * 
 * const hash = new SpatialHash(64);
 * const entities = [ ... ]; // Array of game objects with {id, x, y, w, h}
 * 
 * function update() {
 *   // Rebuild hash each frame
 *   hash.clear();
 *   entities.forEach(e => hash.insert(e.id, {x: e.x, y: e.y, w: e.w, h: e.h}));
 *   
 *   // Check collisions only against nearby entities
 *   for (const e of entities) {
 *     const nearby = hash.query({x: e.x, y: e.y, w: e.w, h: e.h});
 *     for (const id of nearby) {
 *       if (id !== e.id) {
 *         const other = entities.find(ent => ent.id === id);
 *         // Do narrow-phase collision check
 *       }
 *     }
 *   }
 * }
 */
