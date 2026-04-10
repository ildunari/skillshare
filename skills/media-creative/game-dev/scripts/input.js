/**
 * input.js - Unified Input Manager using Pointer Events
 * 
 * Handles mouse, touch, and pen input through a single API
 * Use with CSS: canvas { touch-action: none; }
 * 
 * Usage:
 *   const input = new Input(canvas);
 *   const pointer = input.primary();
 *   if (pointer && pointer.pressed) {
 *     console.log(pointer.x, pointer.y);
 *   }
 */

class Input {
  /**
   * @param {HTMLElement} el - Canvas or container element
   */
  constructor(el) {
    this.pointers = new Map(); // pointerId -> {x, y, pressed, type}
    this.keys = new Set(); // Currently pressed keys
    
    // Pointer Events (unified mouse/touch/pen)
    el.addEventListener('pointerdown', e => this.onDown(e));
    el.addEventListener('pointermove',  e => this.onMove(e));
    el.addEventListener('pointerup',    e => this.onUp(e));
    el.addEventListener('pointercancel',e => this.onUp(e));
    el.addEventListener('lostpointercapture', e => this.onUp(e));
    
    // Keyboard
    window.addEventListener('keydown', e => this.onKeyDown(e));
    window.addEventListener('keyup',   e => this.onKeyUp(e));
  }
  
  /**
   * Convert event to canvas-relative coordinates
   * @private
   */
  posFromEvent(e, rect) {
    return { 
      x: e.clientX - rect.left, 
      y: e.clientY - rect.top 
    };
  }
  
  /**
   * Handle pointer down
   * @private
   */
  onDown(e) {
    // Capture pointer to receive events even if it leaves the element
    e.currentTarget.setPointerCapture?.(e.pointerId);
    
    const rect = e.currentTarget.getBoundingClientRect();
    const p = this.posFromEvent(e, rect);
    
    this.pointers.set(e.pointerId, { 
      ...p, 
      pressed: true, 
      type: e.pointerType // 'mouse', 'touch', or 'pen'
    });
  }
  
  /**
   * Handle pointer move
   * @private
   */
  onMove(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const p = this.pointers.get(e.pointerId);
    if (p) {
      Object.assign(p, this.posFromEvent(e, rect));
    }
  }
  
  /**
   * Handle pointer up/cancel
   * @private
   */
  onUp(e) {
    this.pointers.delete(e.pointerId);
  }
  
  /**
   * Get the primary (first) pointer
   * @returns {Object|null} {x, y, pressed, type} or null if no pointers
   */
  primary() {
    const first = [...this.pointers.values()][0];
    return first || null;
  }
  
  /**
   * Get all active pointers (for multi-touch)
   * @returns {Array} Array of {x, y, pressed, type}
   */
  all() {
    return [...this.pointers.values()];
  }
  
  /**
   * Check if a pointer exists at a given ID
   * @param {number} id - Pointer ID
   * @returns {Object|null} Pointer data or null
   */
  get(id) {
    return this.pointers.get(id) || null;
  }
  
  /**
   * Handle key down
   * @private
   */
  onKeyDown(e) {
    this.keys.add(e.key.toLowerCase());
    
    // Prevent default for game keys (arrow keys, space, etc.)
    if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', ' '].includes(e.key.toLowerCase())) {
      e.preventDefault();
    }
  }
  
  /**
   * Handle key up
   * @private
   */
  onKeyUp(e) {
    this.keys.delete(e.key.toLowerCase());
  }
  
  /**
   * Check if a key is currently pressed
   * @param {string} key - Key name (case-insensitive)
   * @returns {boolean}
   */
  isKeyPressed(key) {
    return this.keys.has(key.toLowerCase());
  }
  
  /**
   * Check if any of the given keys are pressed
   * @param {Array<string>} keys - Array of key names
   * @returns {boolean}
   */
  isAnyKeyPressed(...keys) {
    return keys.some(k => this.isKeyPressed(k));
  }
}

/**
 * Virtual Joystick (Thumbstick) for Mobile
 * 
 * Usage:
 *   const stick = new VirtualStick(canvas, 64);
 *   // In game loop:
 *   const { x, y } = stick.vec; // x,y are -1 to 1
 *   player.x += x * speed * dt;
 *   player.y += y * speed * dt;
 */
class VirtualStick {
  /**
   * @param {HTMLElement} el - Canvas or container
   * @param {number} radius - Joystick radius in pixels
   */
  constructor(el, radius = 64) {
    this.center = null;  // {x, y} when active, null when released
    this.radius = radius;
    this.vec = { x: 0, y: 0 }; // -1 to 1 normalized direction
    
    el.addEventListener('pointerdown', e => {
      this.center = this._pos(el, e);
      this._update(el, e);
    });
    
    el.addEventListener('pointermove', e => {
      if (this.center) this._update(el, e);
    });
    
    el.addEventListener('pointerup', () => {
      this.center = null;
      this.vec = { x: 0, y: 0 };
    });
    
    el.addEventListener('pointercancel', () => {
      this.center = null;
      this.vec = { x: 0, y: 0 };
    });
  }
  
  /**
   * Get pointer position relative to element
   * @private
   */
  _pos(el, e) {
    const r = el.getBoundingClientRect();
    return { x: e.clientX - r.left, y: e.clientY - r.top };
  }
  
  /**
   * Update joystick vector
   * @private
   */
  _update(el, e) {
    if (!this.center) return;
    
    const p = this._pos(el, e);
    const dx = p.x - this.center.x;
    const dy = p.y - this.center.y;
    const mag = Math.hypot(dx, dy) || 1;
    const clamp = Math.min(1, mag / this.radius);
    
    this.vec = {
      x: (dx / mag) * clamp,
      y: (dy / mag) * clamp
    };
  }
  
  /**
   * Render the joystick (call in game render loop)
   * @param {CanvasRenderingContext2D} ctx - Canvas context
   */
  render(ctx) {
    if (!this.center) return;
    
    const { x, y } = this.center;
    const dx = this.vec.x * this.radius;
    const dy = this.vec.y * this.radius;
    
    ctx.save();
    
    // Outer ring
    ctx.globalAlpha = 0.3;
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, this.radius, 0, Math.PI * 2);
    ctx.stroke();
    
    // Inner knob
    ctx.globalAlpha = 0.6;
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(x + dx, y + dy, this.radius * 0.3, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.restore();
  }
}
