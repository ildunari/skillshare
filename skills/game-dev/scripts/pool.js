/**
 * pool.js - Object Pooling for Performance
 * 
 * Prevents garbage collection stutters by reusing objects
 * Use for frequently created/destroyed objects like particles, bullets, effects
 * 
 * Usage:
 *   const bulletPool = new Pool(() => ({ x:0, y:0, vx:0, vy:0, active:false }), 128);
 *   
 *   // Acquire from pool
 *   const bullet = bulletPool.acquire();
 *   bullet.x = player.x;
 *   bullet.y = player.y;
 *   bullet.active = true;
 *   
 *   // Release back to pool when done
 *   bulletPool.release(bullet);
 */

class Pool {
  /**
   * @param {Function} factory - Function that creates a new object
   * @param {number} initialSize - Initial pool size
   */
  constructor(factory, initialSize = 128) {
    this.factory = factory;
    this.free = [];
    
    // Pre-allocate objects
    for (let i = 0; i < initialSize; i++) {
      this.free.push(factory());
    }
  }
  
  /**
   * Get an object from the pool
   * Creates a new one if pool is empty
   * @returns {Object} Pooled object
   */
  acquire() {
    return this.free.pop() ?? this.factory();
  }
  
  /**
   * Return an object to the pool
   * @param {Object} obj - Object to return
   */
  release(obj) {
    obj.active = false; // Convention: mark as inactive
    this.free.push(obj);
  }
  
  /**
   * Get current pool statistics
   * @returns {Object} {free, total}
   */
  stats() {
    return {
      free: this.free.length,
      total: this.free.length
    };
  }
  
  /**
   * Clear the pool completely
   */
  clear() {
    this.free.length = 0;
  }
}

/**
 * Particle System using Object Pooling
 * 
 * Usage:
 *   const particles = new ParticleSystem(512);
 *   
 *   // Spawn explosion
 *   for (let i = 0; i < 20; i++) {
 *     const angle = Math.random() * Math.PI * 2;
 *     const speed = 100 + Math.random() * 100;
 *     particles.spawn(x, y, Math.cos(angle) * speed, Math.sin(angle) * speed, 1.0);
 *   }
 *   
 *   // In game loop:
 *   particles.update(dt);
 *   particles.render(ctx);
 */
class ParticleSystem {
  /**
   * @param {number} maxParticles - Maximum number of particles
   */
  constructor(maxParticles = 512) {
    this.pool = new Pool(() => ({
      x: 0,
      y: 0,
      vx: 0,
      vy: 0,
      life: 0,
      maxLife: 0,
      color: '#fff',
      size: 2,
      active: false
    }), maxParticles);
    
    this.particles = [];
  }
  
  /**
   * Spawn a new particle
   * @param {number} x - X position
   * @param {number} y - Y position
   * @param {number} vx - X velocity (pixels per second)
   * @param {number} vy - Y velocity (pixels per second)
   * @param {number} life - Lifetime in seconds
   * @param {Object} options - {color, size, gravity}
   */
  spawn(x, y, vx, vy, life, options = {}) {
    const p = this.pool.acquire();
    p.active = true;
    p.x = x;
    p.y = y;
    p.vx = vx;
    p.vy = vy;
    p.life = life;
    p.maxLife = life;
    p.color = options.color || '#fff';
    p.size = options.size || 2;
    p.gravity = options.gravity ?? 500; // pixels per second^2
    
    this.particles.push(p);
  }
  
  /**
   * Update all particles
   * @param {number} dt - Delta time in seconds
   */
  update(dt) {
    for (const p of this.particles) {
      if (!p.active) continue;
      
      // Update physics
      p.life -= dt;
      if (p.life <= 0) {
        p.active = false;
        this.pool.release(p);
        continue;
      }
      
      // Apply gravity
      p.vy += p.gravity * dt;
      
      // Move
      p.x += p.vx * dt;
      p.y += p.vy * dt;
    }
    
    // Remove inactive particles
    this.particles = this.particles.filter(p => p.active);
  }
  
  /**
   * Render all particles
   * @param {CanvasRenderingContext2D} ctx - Canvas context
   */
  render(ctx) {
    ctx.save();
    
    // Use additive blending for glowy effect
    ctx.globalCompositeOperation = 'lighter';
    
    for (const p of this.particles) {
      if (!p.active) continue;
      
      // Fade out based on remaining life
      const alpha = p.life / p.maxLife;
      ctx.globalAlpha = alpha;
      
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    }
    
    ctx.globalCompositeOperation = 'source-over';
    ctx.restore();
  }
  
  /**
   * Clear all particles
   */
  clear() {
    for (const p of this.particles) {
      if (p.active) this.pool.release(p);
    }
    this.particles = [];
  }
  
  /**
   * Get particle count
   * @returns {number} Active particle count
   */
  count() {
    return this.particles.length;
  }
}

/**
 * Example: Bullet pool usage
 * 
 * const bulletPool = new Pool(() => ({
 *   x: 0, y: 0, vx: 0, vy: 0, w: 4, h: 4, active: false
 * }), 64);
 * 
 * const bullets = [];
 * 
 * function shoot(x, y, angle, speed) {
 *   const bullet = bulletPool.acquire();
 *   bullet.active = true;
 *   bullet.x = x;
 *   bullet.y = y;
 *   bullet.vx = Math.cos(angle) * speed;
 *   bullet.vy = Math.sin(angle) * speed;
 *   bullets.push(bullet);
 * }
 * 
 * function updateBullets(dt) {
 *   for (const b of bullets) {
 *     b.x += b.vx * dt;
 *     b.y += b.vy * dt;
 *     
 *     // Remove if off-screen
 *     if (b.x < 0 || b.x > 800 || b.y < 0 || b.y > 600) {
 *       b.active = false;
 *       bulletPool.release(b);
 *     }
 *   }
 *   bullets = bullets.filter(b => b.active);
 * }
 */
