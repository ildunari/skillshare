# Best Practices for Performant Browser-Based Game Development (2024-2025)

**Key Points:**
*   **The Game Loop:** Modern browser games must utilize `requestAnimationFrame` for rendering but decouple game logic using a **Fixed Timestep** pattern (often called the Accumulator pattern). This prevents physics instability on high-refresh-rate monitors (120Hz/144Hz) and mitigates the "spiral of death" when tabs are backgrounded.
*   **Input Handling:** **Pointer Events** (`pointerdown`, `pointermove`) are now the industry standard, superseding separate Mouse and Touch events for unified cross-device support. Responsiveness is achieved not just through raw input speed but through design patterns like **Coyote Time** and **Input Buffering**.
*   **Rendering Architecture:** Pixel-perfect rendering on modern displays requires handling `devicePixelRatio` manually. Camera systems should utilize **time-based Linear Interpolation (Lerp)** for movement and separate "trauma" vectors for screen shake to avoid permanently displacing the camera anchor.
*   **Performance:** Garbage Collection (GC) pauses are the primary cause of "jank" in JavaScript games. **Object Pooling** is essential for high-frequency entities (projectiles, particles). For collision detection, **Spatial Grids** are often superior to Quadtrees in JavaScript due to lower overhead and implementation complexity for dynamic objects.

---

## 1. The Modern Game Loop
The game loop is the heartbeat of any simulation. In the browser environment, developers face unique challenges: the event loop is single-threaded, refresh rates vary by device (60Hz vs. 144Hz), and browsers throttle background tabs to save battery. A naive approach using `requestAnimationFrame` for both logic and rendering binds game speed to frame rate, causing the simulation to run twice as fast on a 120Hz monitor as on a 60Hz one.

### 1.1 The Fixed Timestep with Variable Rendering
The authoritative standard for production-quality game loops is the **Fixed Timestep** pattern, popularized by Glenn Fiedler (Gaffer on Games). This pattern decouples the simulation time from the real-world frame time.

1.  **Accumulator:** Time elapsed since the last frame (`deltaTime`) is added to an accumulator.
2.  **Fixed Update:** While the accumulator contains more time than a fixed step (e.g., 1/60th of a second), the physics/logic is updated, and the fixed step is subtracted.
3.  **Variable Render:** The scene is rendered once per `requestAnimationFrame` callback, often using the remainder in the accumulator to interpolate positions for maximum smoothness.

### 1.2 Handling "The Spiral of Death"
When a user switches tabs, `requestAnimationFrame` pauses. Upon returning, the `deltaTime` can be massive (e.g., 5000ms). If the loop attempts to process 5000ms worth of 16ms fixed steps, the browser will hang, creating more lag, leading to an infinite "spiral of death".

**Best Practice:** Implement a "panic" limit or clamp on the frame time. If the frame time exceeds a threshold (e.g., 250ms), process only that maximum amount and discard the rest.

### 1.3 Implementation (Single-File Pattern)
This implementation manages timing, protects against the spiral of death, and provides `alpha` for interpolation.

```javascript
const GameLoop = {
    lastTime: 0,
    accumulator: 0,
    step: 1000 / 60, // Fixed logic update at 60Hz (16.66ms)
    maxFrameTime: 250, // Panic limit to prevent spiral of death

    start() {
        this.lastTime = performance.now();
        requestAnimationFrame(this.loop.bind(this));
    },

    loop(timestamp) {
        // Clamp delta time to prevent spiral of death
        let delta = timestamp - this.lastTime;
        if (delta > this.maxFrameTime) delta = this.maxFrameTime;
        
        this.lastTime = timestamp;
        this.accumulator += delta;

        // Consumer accumulator in fixed steps
        while (this.accumulator >= this.step) {
            Game.update(this.step); // Fixed logic tick
            this.accumulator -= this.step;
        }

        // Calculate alpha for interpolation (0.0 to 1.0)
        // Represents how far we are between the previous and next physics state
        const alpha = this.accumulator / this.step;
        
        Game.render(alpha);
        requestAnimationFrame(this.loop.bind(this));
    }
};
```

## 2. Input Handling
Input handling in 2024 requires abstracting hardware specificities into logical actions. The "janky prototype" often listens for key events directly in the update loop; the "production quality" loop uses a state manager with responsiveness buffers.

### 2.1 Unified Input: Pointer Events
Historically, developers had to manage `MouseEvent` and `TouchEvent` separately. The modern best practice is **Pointer Events** (`pointerdown`, `pointermove`, `pointerup`), which abstract mouse, touch, and stylus into a single API.

*   **Pointer Capture:** Essential for virtual joysticks. When a user touches a joystick and drags off the element, `element.setPointerCapture(e.pointerId)` ensures the element keeps receiving events until release.
*   **CSS Handling:** Apply `touch-action: none;` to the game canvas to prevent default browser gestures like scrolling or zooming while playing.

### 2.2 Advanced Platformer Mechanics: "Game Feel"
To make controls feel responsive rather than "correct," implementations must lie to the player slightly.

#### Coyote Time
Players perceive they are "on the ledge" slightly longer than the physics engine does. Coyote Time allows the player to jump for a few frames *after* walking off a platform.
*   **Implementation:** A timer (`coyoteTimer`) is reset to a value (e.g., 100ms) whenever the entity is grounded. In the update loop, decrement the timer. A jump is valid if `coyoteTimer > 0`, not just if `isGrounded` is true.

#### Input Buffering
Players often press the jump button milliseconds *before* landing. Without buffering, this input is eaten, and the player simply lands.
*   **Implementation:** When the jump button is pressed, set a `jumpBufferTimer` (e.g., 100ms). In the update loop, if the player lands and `jumpBufferTimer > 0`, execute the jump immediately.

#### Variable Jump Height
To allow for precise platforming, the jump height should depend on how long the button is held. This is often called "Action Canceling."
*   **Implementation:** If the player releases the jump button while moving upward (`velocity.y < 0`), multiply the vertical velocity by a dampening factor (e.g., 0.5) to cut the jump short.

## 3. Camera and Viewport
A polished camera system separates the "ideal" position from the "actual" position using math to smooth the transition.

### 3.1 Resolution Independence (HiDPI)
Browsers on Retina/HiDPI displays scale logical pixels. A canvas defined as `width="800"` in HTML will look blurry on a 2x pixel density screen because the browser upscales the bitmap.
*   **The Fix:** Scale the internal canvas resolution by `window.devicePixelRatio` and scale the CSS size to fit the window.
*   **ResizeObserver:** Use `ResizeObserver` to detect container changes rather than the `resize` event, which triggers excessively. This prevents layout thrashing.

```javascript
function resizeCanvas(canvas, context) {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    
    // Set actual render size to physical pixels
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    
    // Normalize coordinate system so 1 unit = 1 CSS pixel
    context.scale(dpr, dpr);
}
```

### 3.2 Smooth Camera Follow
Hard-locking the camera to the player creates motion sickness and jitter. The standard solution is **Linear Interpolation (Lerp)**.
*   **Time-Dependent Lerp:** A standard `x += (target - x) * 0.1` is frame-rate dependent. The correct time-based formula is:
    \[ \text{current} = \text{target} + (\text{current} - \text{target}) \times e^{-\text{decay} \times \text{dt}} \]
    Or the simplified approximation for small steps: `current = lerp(current, target, 1 - Math.pow(damping, dt))`.

### 3.3 Screen Shake
Screen shake should never modify the camera's actual position variable, as this causes drift. Instead, calculate a separate **shake offset** applied only during the render phase.
*   **Trauma Pattern:** Use a `trauma` value (0 to 1) that decays linearly over time. The shake offset is `trauma²` (or cubed) multiplied by a max offset. This creates a satisfying non-linear falloff where high impacts shake violently but settle quickly.

## 4. Entity Management and Performance
In JavaScript, memory allocation is the enemy of performance. Creating objects (`new Vector2()`, `new Bullet()`) inside the game loop triggers the Garbage Collector (GC). When GC runs, it pauses execution ("stop-the-world"), causing visible stutter.

### 4.1 Object Pooling
Instead of destroying and creating entities, a performant game maintains a pool of initialized objects.
*   **Mechanism:** An array of reusable objects. When a bullet is "fired," one is taken from the pool and initialized. When it hits a wall, it is deactivated (reset flags) and returned to the pool rather than deleted.
*   **Static Allocation:** For math-heavy games, avoid creating new vector objects for intermediate calculations. Use mutable static instances or modify active object properties directly.

### 4.2 Entity Component System (ECS)
ECS is preferred over Object-Oriented Programming (OOP) for scaling complexity. It favors composition over inheritance.
*   **Entity:** A simple integer ID.
*   **Component:** Pure data (e.g., `Position: {x, y}`, `Velocity: {dx, dy}`).
*   **System:** Pure logic that iterates over entities possessing specific components (e.g., `MovementSystem` iterates all entities with `Position` and `Velocity`).
*   **Benefits:** It solves the "diamond inheritance" problem and makes data serialization (saving games) trivial since components are just JSON-serializable data structures.

### 4.3 Spatial Partitioning
Collision detection is an $O(N^2)$ problem (checking every object against every other). Spatial partitioning reduces this significantly.
*   **Spatial Hash Grid:** For 2D browser games, a simple grid (Spatial Hash) is often superior to Quadtrees. Quadtrees require expensive rebuilding/rebalancing when objects move. A grid simply maps an entity's coordinate to a cell key (e.g., `x_y`). Only entities sharing cell keys are checked for collision.
*   **Grid vs. Quadtree:** Research suggests that unless the world is massive with highly non-uniform distribution, the overhead of a Quadtree in JavaScript (pointer chasing, object creation) often outweighs the benefits compared to a flat array-based grid.

## 5. Architectural Reference Implementation
Below is a synthesized structural reference for the AI agent, adhering to the "single-file" constraint while maintaining separation of concerns.

```javascript
/**
 * Single-File Game Architecture Reference
 * 1. Logic is decoupled from Rendering (Fixed Timestep).
 * 2. Input is buffered and unified.
 * 3. Entities are pooled to minimize GC.
 */

// --- 1. CORE: Input Manager ---
class Input {
    constructor() {
        this.keys = new Map();
        this.buffer = new Map(); // For buffering inputs
        // Use Pointer Events for unified Mouse/Touch
        window.addEventListener('keydown', e => this.keys.set(e.code, true));
        window.addEventListener('keyup', e => this.keys.set(e.code, false));
    }
    
    isPressed(code) { return this.keys.get(code) === true; }
    
    // Check if key was pressed within last N ms (Input Buffering)
    wasPressedRecently(code, timeWindow) {
        const timestamp = this.buffer.get(code);
        return timestamp && (performance.now() - timestamp < timeWindow);
    }
}

// --- 2. CORE: Entity Management (ECS + Pooling) ---
class EntityManager {
    constructor() {
        this.pool = []; // Inactive entities
        this.active = []; // Active entities
    }

    spawn() {
        const entity = this.pool.length > 0 ? this.pool.pop() : new Entity();
        entity.active = true;
        this.active.push(entity);
        return entity;
    }

    recycle(entity) {
        entity.active = false;
        // Ideally remove from 'active' array efficiently (swap & pop)
        const idx = this.active.indexOf(entity);
        if (idx > -1) {
            this.active[idx] = this.active[this.active.length - 1];
            this.active.pop();
        }
        this.pool.push(entity);
    }
}

// --- 3. CORE: The Game Loop ---
class Game {
    constructor() {
        this.input = new Input();
        this.entities = new EntityManager();
        this.accumulator = 0;
        this.lastTime = performance.now();
        this.step = 1/60; 
    }

    start() { requestAnimationFrame(t => this.loop(t)); }

    loop(timestamp) {
        let dt = (timestamp - this.lastTime) / 1000;
        this.lastTime = timestamp;
        
        // Panic check: prevent spiral of death
        if (dt > 0.25) dt = 0.25;
        
        this.accumulator += dt;
        
        while (this.accumulator >= this.step) {
            this.update(this.step);
            this.accumulator -= this.step;
        }
        
        // Render with interpolation factor
        this.render(this.accumulator / this.step);
        requestAnimationFrame(t => this.loop(t));
    }

    update(dt) {
        // Physics and Logic here
        // Example: Spatial Grid collision checks
    }

    render(alpha) {
        // Drawing here using (current * alpha) + (prev * (1-alpha))
    }
}
```