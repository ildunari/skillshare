# Comprehensive Analysis of 2D Collision Detection and Physics Response for Browser Games

**Date:** October 25, 2023
**Target Audience:** Game Engine Developers, Academic Researchers in Computer Graphics
**Subject:** High-Performance 2D Physics Implementation in JavaScript (No External Libraries)

## Executive Summary

Developing a robust 2D physics engine in a garbage-collected environment like JavaScript requires a distinct departure from naive object-oriented approaches toward data-oriented design and specific algorithmic choices that minimize allocation overhead. Research into the current landscape of 2D game development indicates a convergence on **Sequential Impulse** solvers for stability and **Spatial Hashing** for broadphase performance in browser environments. While naive $O(N^2)$ checks suffice for trivial scenes (<100 objects), efficient scaling demands spatial partitioning.

For collision detection, the **Separating Axis Theorem (SAT)** remains the industry standard for convex polygons due to its numerical stability, while **Sutherland-Hodgman clipping** is the requisite technique for generating the contact manifolds (contact points and normals) necessary for realistic stacking and friction. Platformer-specific physics often diverges from rigid body simulation, favoring "swept" checks and raycasting to handle slopes and one-way platforms precisely without the "floaty" behavior of pure physics solvers.

The following report details the mathematical foundations and implementation strategies for a self-contained JavaScript physics engine, synthesizing methodologies from Box2D, dyn4j, and academic resources.

---

## 1. Broadphase Strategies

The broadphase collision detection step aims to reduce the set of potential collision pairs from $N^2$ to a manageable subset. In JavaScript 2D engines, the choice of data structure significantly impacts performance due to memory access patterns and object allocation overhead.

### 1.1 Comparative Analysis of Spatial Data Structures

Research suggests three primary approaches: Brute Force, Quadtrees, and Spatial Hashing.

*   **Brute Force:** Checking every object against every other object.
    *   *Performance Profile:* $O(N^2)$.
    *   *Crossover Point:* Current benchmarks and implementations suggest that brute force becomes a bottleneck at approximately **80–100 dynamic objects** in a browser environment. Below this threshold, the overhead of building a complex structure often outweighs the benefits of culling.

*   **Quadtrees:** Recursively dividing the 2D space into four quadrants.
    *   *Usage:* Historically popular, but often outperformed by grids in JavaScript due to the overhead of traversing tree nodes and pointer-chasing.
    *   *Strengths:* Excellent for sparse data sets or worlds with highly variable object sizes.
    *   *Weaknesses:* Requires rebuilding or heavy updating when objects move. If the tree is not optimized (e.g., using linear quadtrees or array-based storage), the recursion depth and object references can cause garbage collection pressure.

*   **Spatial Hashing (Grid):** Dividing the world into a uniform grid and mapping objects to cells.
    *   *Usage:* Widely recommended for dynamic 2D games where objects are relatively uniform in size.
    *   *Performance:* $O(1)$ insertion and lookup in the average case. Benchmarks indicate Spatial Hashing sustains performance for dense scenes (e.g., 20,000 agents) where Quadtrees begin to falter due to depth traversal.
    *   *Implementation Note:* In JavaScript, using a 1D array or a `Map` with a hashed key (e.g., `x + y * width`) is often faster than 2D arrays, avoiding nested array lookups.

### 1.2 Recommended Implementation: Spatial Hash

For a generic 2D browser game engine in 2024, a **Spatial Hash** is the optimal choice for the broadphase. It minimizes object allocation compared to tree structures and handles the high quantity of moving bodies typical in games better than Quadtrees.

**Key Implementation Details:**
1.  **Cell Size:** Should be set to the size of the largest object in the game to avoid objects spanning too many cells.
2.  **Clearing:** Instead of deleting and reallocating the grid every frame, reuse arrays or integer pools to maintain performance.

---

## 2. Narrowphase Detection

Once the broadphase identifies potential pairs, the narrowphase determines if they actually intersect and computes the geometric data required to resolve the collision.

### 2.1 The Separating Axis Theorem (SAT)

The standard "toolkit" for shape-vs-shape tests relies heavily on SAT. SAT states that if two convex objects are not colliding, there exists an axis onto which their projections do not overlap.

*   **Robustness:** SAT is mathematically robust for all convex polygons. It handles edge-cases better than simplistic bounding box overlaps.
*   **Algorithm:**
    1.  Test axes perpendicular to the edges of Polygon A.
    2.  Test axes perpendicular to the edges of Polygon B.
    3.  Project vertices of both shapes onto the current axis.
    4.  Check for overlap in the 1D projections (Intervals).
    5.  **Early Exit:** If any axis shows a gap (no overlap), the shapes are not colliding.

**Minimum Translation Vector (MTV):**
If overlapping on all axes, the axis with the *smallest* overlap depth is the direction required to push the objects apart. This vector, combined with the overlap magnitude, forms the penetration vector needed for collision response.

### 2.2 Generating Contact Manifolds

A common pitfall in simple engines is generating only a boolean "true/false" or a single center point. Realistic physics, especially for stacking, requires a **Contact Manifold**: a set of points (usually 1 or 2 in 2D) where the forces are applied.

**The Clipping Algorithm (Sutherland-Hodgman):**
To generate contact points similar to Box2D, one must "clip" the incident face of one polygon against the reference face of the other.

**Step-by-Step Manifold Generation:**
1.  **Identify Faces:** Find the "Reference Face" on one body (the face most perpendicular to the collision normal) and the "Incident Face" on the other body.
2.  **Clip 1:** Clip the Incident Face against the side planes of the Reference Face. This ensures we only consider the portion of the edge that is actually adjacent to the other object.
3.  **Clip 2:** Keep only the points that are below the Reference Face.
4.  **Result:** The remaining points are the contact points. Each point includes a normal, a position, and a penetration depth.

**Code Logic for Contact Identification:**
```javascript
// Pseudo-code logic based on Box2D Lite
function computeManifold(polyA, polyB, normal) {
    // 1. Find incident edge on polyB (most anti-parallel to normal)
    let incidentEdge = findIncidentEdge(polyB, normal);

    // 2. Find reference edge on polyA
    let referenceEdge = findReferenceEdge(polyA, normal);

    // 3. Clip incident edge against the side planes of the reference edge
    let clippedPoints = clip(incidentEdge, referenceEdge.sidePlane1);
    clippedPoints = clip(clippedPoints, referenceEdge.sidePlane2);

    // 4. Filter points: Remove points 'above' the reference face
    let contacts = [];
    for (let p of clippedPoints) {
        let separation = dot(p - referenceEdge.v1, normal);
        if (separation <= 0) {
            contacts.push({ point: p, depth: separation, normal: normal });
        }
    }
    return contacts;
}
```

---

## 3. Collision Response

Modern 2D physics engines (Box2D, Chipmunk, Matter.js) predominantly use an **Impulse-Based** approach (specifically, a Sequential Impulse Solver).

### 3.1 Impulse vs. Projection

*   **Projection:** Simply moving objects apart so they don't overlap.
    *   *Result:* "Mushy" collisions, lack of conservation of momentum, impossible to simulate realistic bounce or friction.
*   **Impulse-Based:** Changing the *velocity* of objects instantly to resolve the constraint.
    *   *Result:* Realistic conservation of momentum, restitution (bounciness), and stable friction.

### 3.2 The Impulse Formula

To resolve a collision, we calculate a scalar impulse $J$ effectively "hitting" the objects to separate them. The formula for the impulse magnitude $j$ is derived from Newton's Law of Restitution and conservation of momentum:

$$ j = \frac{-(1 + e)(v_{rel} \cdot n)}{ \frac{1}{m_a} + \frac{1}{m_b} + \frac{(r_a \times n)^2}{I_a} + \frac{(r_b \times n)^2}{I_b} } $$

Where:
*   $e$ = Coefficient of restitution (bounciness).
*   $v_{rel}$ = Relative velocity between the contact points.
*   $n$ = Collision normal.
*   $m$ = Mass.
*   $I$ = Moment of Inertia (resistance to rotation).
*   $r$ = Vector from center of mass to contact point.

### 3.3 Friction and Angular Effects

Friction is applied as a separate impulse tangent to the collision normal.
1.  **Tangent Vector:** Perpendicular to the collision normal.
2.  **Tangent Impulse:** Calculated similarly to the normal impulse but using the tangent vector.
3.  **Clamping:** Real-world friction is limited by the normal force (Coulomb friction). The friction impulse must be clamped between $- \mu \cdot j_{normal}$ and $+ \mu \cdot j_{normal}$.

This application of angular impulse ($r \times n$) in the denominator ensures that objects rotate correctly when hit off-center.

### 3.4 Stacking Stability

Stacking is the "stress test" for any physics engine. Naive impulse solvers cause stacks to jitter or collapse because gravity adds energy every frame that the solver doesn't perfectly remove.

**Solutions for Stability:**
1.  **Warm Starting:** Use the impulses from the *previous* frame as the starting guess for the current frame. This allows the solver to "remember" the forces keeping the stack upright.
2.  **Iterative Solver:** Run the impulse resolution loop multiple times (e.g., 10 iterations) per frame. This propagates the forces through the stack.
3.  **Baumgarte Stabilization (Positional Correction):** Impulse solvers fix velocity, but objects might still be overlapping visually. Apply a small "pseudo-velocity" bias to push them apart slowly over time to fix the overlap without adding "real" kinetic energy.

---

## 4. Continuous Collision Detection (CCD)

### 4.1 The Tunneling Problem
Tunneling occurs when a fast-moving object travels completely through a thin object (like a wall) in a single time step. Discrete collision detection (checking positions at $t$ and $t+1$) fails to catch the intersection.

### 4.2 Approaches for Browser Games

*   **Raycasting:**
    *   *Usage:* Best for bullets or high-speed projectiles.
    *   *Method:* Cast a ray from position $P_{current}$ to $P_{next}$. If the ray hits a wall, stop the object there.
    *   *Cost:* Low.

*   **Swept AABB / Minkowski Sum:**
    *   *Usage:* Essential for platformer characters preventing falling through floors.
    *   *Method:* By expanding the bounding box of the static object by the size of the moving object (Minkowski Sum), the problem reduces to checking if a line segment (the movement ray) intersects the expanded box.
    *   *Logic:* Calculate the "Time of Impact" (TOI), a value between 0 and 1 representing *when* in the frame the collision occurred. Move the object only to that point.

**Recommendation:** For a general engine, implementing **Bilateral Advancement** (used in Box2D) is complex. For a self-contained JS engine, **Raycasting** for projectiles and **Swept AABB** for player characters is the standard, pragmatic approach.

---

## 5. Tilemap Collision (Platformer Specifics)

Platformers often require "tight" controls that realistic physics engines (like Box2D) make difficult due to friction and rotation. Custom tile-based physics is often preferred.

### 5.1 Player vs. Tilemap

Instead of checking the player against thousands of tile objects, translate the player's coordinate space to the grid coordinates.
*   *Algorithm:* Identify the grid cells the player overlaps (e.g., `floor(player.x / tileSize)`). Only check collisions against these specific cells.

### 5.2 Slopes

Handling slopes requires separating the X and Y axis resolution or using a heightmap approach.
*   **Heightmap Approach:** Within a tile, define the floor height as a function of X (e.g., `y = mx + b`). If the player's Y is below this height, snap them to the surface.
*   **AABB vs Slope:** Standard AABB does not work well. The "Separating Axis" logic can be adapted, but specifically treating the slope as a half-plane (line segment) provides smoother results.

### 5.3 One-Way Platforms

One-way platforms are "conditional" collisions.
*   **Logic:** A collision should only register if:
    1.  The player's velocity is downward ($v_y > 0$).
    2.  The player's "feet" were previously *above* the platform's top edge.
*   **Implementation:**
    ```javascript
    if (player.velocity.y > 0 && player.prevY + player.height <= platform.y) {
        // Resolve collision
    }
    ```

---

## 6. Implementation Summary & Toolkit

For a robust, self-contained JavaScript implementation in 2024-2025, the following architecture is recommended:

| Component | Recommendation | Why? |
| :--- | :--- | :--- |
| **Integration** | **Symplectic Euler** | More stable than standard Euler, conserves energy better for orbits/springs. |
| **Broadphase** | **Spatial Hash** | Faster than Quadtrees for uniform game objects; simple array/map implementation. |
| **Narrowphase** | **SAT + Clipping** | Robust detection (SAT) + accurate contact points for rotation (Clipping). |
| **Resolution** | **Sequential Impulse** | Handles friction, bounce, and stacking far better than projection methods. |
| **CCD** | **Raycast / Swept AABB** | Prevents tunneling for fast objects without the overhead of full TOI solvers. |

### 6.1 References for Algorithms (Prioritized)

1.  **Box2D Lite (Erin Catto):** The definitive reference for the **Sequential Impulse** solver and **Clipping** implementation. The C++ source is easily portable to JS.
2.  **dyn4j.org:** Provides the clearest textual explanations of **SAT** and **GJK** tailored for Java/JS style OOP.
3.  **Red Blob Games:** Essential for **Spatial Hashing** and grid mathematics concepts.
4.  **Metanet N Tutorial:** The gold standard for **Tilemap** and **Slope** logic in platformers.

This synthesis of approaches provides a "best-of-breed" physics engine capable of handling complex interactions (stacking, friction) while maintaining the performance required for browser-based play.