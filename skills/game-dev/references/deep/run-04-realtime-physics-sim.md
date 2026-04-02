# Research Report: Real-Time Physics Simulation Techniques in the Web Browser (2024-2025)

## Key Points
*   **Paradigm Shift to WebGPU:** The transition from WebGL to WebGPU is the single most significant factor in 2024-2025 simulation capabilities. WebGPU allows for "Compute Shaders," enabling physics calculations (fluid dynamics, soft bodies, N-body) to remain entirely on the GPU, avoiding costly CPU-GPU data transfers. This has increased particle limits from thousands (CPU/JS) to millions (GPU).
*   **Rigid Body Stability:** For rigid bodies, **Extended Position-Based Dynamics (XPBD)** has emerged as a robust alternative to traditional impulse-based solvers (like Box2D), offering unconditional stability and physically meaningful compliance (inverse stiffness). However, impulse-based methods using Sequential Impulses (SI) remain the industry standard for stacking stability due to mature friction handling.
*   **Fluid Simulation Consensus:** The **Material Point Method (MPM)**, specifically Moving Least Squares MPM (MLS-MPM), is currently superior to Smoothed Particle Hydrodynamics (SPH) for browser-based interactive fluids. MPM avoids expensive nearest-neighbor searches by using a background grid, allowing for 100,000+ interactive particles on integrated graphics via WebGPU.
*   **Soft Body Dynamics:** XPBD is the dominant algorithm for cloth and soft bodies in the browser due to its ability to handle infinite stiffness and prevent "blowing up" under stress. WebGPU implementations of mass-spring systems can now handle ~600k nodes at 60fps, substantially outperforming WebGL.
*   **Performance Hierarchy:** Native JS < ASM.js/WASM < WebGL (GPGPU) < WebGPU Compute. For physics engines, **Rapier** (Rust-to-WASM) currently benchmarks significantly faster than JavaScript-native libraries like Matter.js or Cannon.js.

---

## 1. Introduction
The landscape of real-time physics simulation in the web browser has undergone a radical transformation between 2020 and 2025. Historically, browser physics was constrained by the single-threaded nature of JavaScript and the bottleneck of transferring data between the CPU (logic) and GPU (rendering). The introduction and maturation of **WebGPU** (fully supported in major browsers as of 2024) has unlocked General-Purpose GPU (GPGPU) computing capabilities that were previously restricted to native desktop applications using CUDA or OpenCL.

This report analyzes the state-of-the-art techniques for simulating rigid bodies, soft bodies, fluids, and large-scale N-body systems. It focuses on the mathematical foundations (integration schemes, constraint solvers), algorithmic choices (Eulerian vs. Lagrangian vs. Hybrid), and the practical implementation details required to achieve interactive frame rates (60 FPS) in a browser environment.

## 2. Rigid Body Dynamics

Rigid body simulation remains the backbone of interactive web applications, from games to interface design. The challenge lies in maintaining stability during complex interactions (stacking, high mass ratios) while maximizing the number of active bodies.

### 2.1 Mathematical Foundations and Solvers

The core of any rigid body engine is the time integration scheme and the constraint solver. Browser-based physics has largely consolidated around two approaches: **Sequential Impulses (SI)** and **Extended Position-Based Dynamics (XPBD)**.

#### 2.1.1 Sequential Impulses (SI) / Projected Gauss-Seidel (PGS)
Popularized by Erin Catto in **Box2D**, this method solves constraints at the velocity level. It models contacts as inequality constraints (objects cannot penetrate) and joints as equality constraints.
*   **Algorithm:** The solver iteratively applies impulses to satisfy constraints. Mathematically, this is equivalent to a Projected Gauss-Seidel (PGS) solver for a Linear Complementarity Problem (LCP).
*   **Stability:** Stacking stability is achieved through **Warm Starting** (using solutions from the previous frame as initial guesses) and **Baumgarte Stabilization** (feeding a fraction of position error back into the velocity bias).
*   **Why it works:** SI handles friction and restitution (bounciness) very accurately. However, position correction (Baumgarte) can introduce artificial energy (ghost forces).

#### 2.1.2 Extended Position-Based Dynamics (XPBD)
Developed by Matthias Müller, XPBD is a variation of Position-Based Dynamics (PBD) that solves constraints at the position level but derives updates in a way that corresponds to physical stiffness.
*   **The Innovation:** Traditional PBD is non-physical; stiffness depends on the time-step size ($\Delta t$). XPBD introduces **Compliance** ($\alpha = 1/k$), making stiffness independent of the simulation frequency.
*   **Advantages:** XPBD is **unconditionally stable**. It cannot "explode" like force-based simulations because it directly projects positions to valid states. It also handles infinite stiffness ($\alpha = 0$) naturally.
*   **Disadvantages:** Handling friction in XPBD is harder than in velocity-level solvers, often requiring explicit velocity updates post-projection. It can also suffer from "floating" artifacts if precision is low.

### 2.2 Collision Detection
Before solving physics, the engine must detect overlaps.
*   **Broadphase:** Spatial partitioning is essential. **Dynamic Bounding Volume Hierarchies (DBVH)** are the standard for 2024/2025 engines (e.g., Rapier uses SIMD-accelerated DBVH).
*   **Narrowphase:**
    *   **GJK (Gilbert-Johnson-Keerthi):** Used to detect collisions between convex shapes. It constructs a simplex inside the Minkowski Difference of two shapes.
    *   **EPA (Expanding Polytope Algorithm):** Used after GJK to determine penetration depth and contact normals for resolution.
    *   **SAT (Separating Axis Theorem):** Still viable for simple 2D box/polygon engines due to its simplicity and speed in low dimensions.

### 2.3 Implementation & Performance Limits

#### 2.3.1 JavaScript vs. WASM (WebAssembly)
Pure JavaScript engines (Matter.js, Planck.js) are limited by the JIT compiler and garbage collection overhead. The current state-of-the-art involves writing the physics core in systems languages (C++, Rust) and compiling to **WebAssembly (WASM)**.

*   **Rapier (Rust):** Rapier is currently the performance leader. It uses SIMD optimizations in WASM and a dedicated task scheduler. Benchmarks show Rapier is 2x to 5x faster than previous iterations and significantly outperforms Matter.js.
*   **Box2D v3 (C++):** Erin Catto’s latest work (Solver2D) focuses on SIMD and cache coherence, offering "Soft Step" solvers that combine the benefits of SI and soft constraints.

#### 2.3.2 Realistic Body Counts
*   **Pure JavaScript (Matter.js):** ~500–1,000 simple bodies at 60 FPS.
*   **WASM (Rapier/Box2D):** ~5,000–10,000 rigid bodies on desktop; ~1,000–3,000 on mobile.
*   **GPU (WebGPU):** Experimental rigid body solvers on GPU exist but are complex due to the serial nature of contact graph resolution. GPU is better suited for particles/fluids.

## 3. Soft Body and Deformable Physics

Soft body simulation involves deformable meshes (cloth, jelly) where the distance between vertices is not fixed but constrained.

### 3.1 Simulation Methods

#### 3.1.1 Mass-Spring Systems (MSS)
The object is modeled as particles connected by springs. Forces are calculated using Hooke's Law ($F = -k \cdot x$).
*   **Browser Viability:** While simple to implement, explicit integration (Forward Euler) explodes if springs are too stiff. Implicit integration is stable but computationally expensive (requires solving large linear systems).
*   **WebGPU:** MSS is highly parallelizable. Recent benchmarks show WebGPU MSS handling **640,000 nodes** at 60 FPS, compared to a limit of ~10,000 in WebGL.

#### 3.1.2 Position-Based Dynamics (PBD) & XPBD
XPBD is the consensus "best approach" for real-time browser soft bodies (Matthias Müller).
*   **Algorithm:**
    1.  Predict positions: $x^* = x + v \Delta t$.
    2.  Solve Constraints: Iteratively project $x^*$ to satisfy distance/volume constraints.
    3.  Update Velocity: $v = (x^* - x) / \Delta t$.
*   **Types of Constraints:**
    *   *Distance Constraints:* Cloth edges (non-stretchy).
    *   *Bending Constraints:* Cloth stiffness (dihedral angle).
    *   *Volume Constraints:* Pressure bodies (jelly/balloons).
*   **Hierarchical PBD (HPBD):** Uses a multi-grid approach to speed up convergence for large meshes, making the cloth behave less "stretchy" with fewer iterations.

### 3.2 WebGPU Implementation Strategy
To achieve high-resolution soft bodies (e.g., fashion/garment simulation):
1.  **Storage Buffers:** Store vertex positions, velocities, and topology (indices) in WebGPU Storage Buffers.
2.  **Compute Shader:** Run the XPBD constraint solver in a compute shader.
    *   *Graph Coloring:* To solve constraints in parallel without race conditions, edges are "colored" so that no two threads modify the same particle simultaneously.
3.  **Rendering:** Use the same buffers for vertex rendering (avoiding CPU readback).

**Performance Limit:** Up to **100,000 nodes** with self-collision is achievable on high-end desktop GPUs via WebGPU.

## 4. Fluid Simulation

Fluid simulation is the most computationally demanding task. The browser ecosystem has moved from simplified 2D implementations to full 3D simulations via WebGPU.

### 4.1 Approaches

#### 4.1.1 Eulerian (Grid-Based)
Based on **Jos Stam’s "Stable Fluids"**. The fluid is represented as density and velocity fields on a fixed grid.
*   **Algorithm:** Solves the Navier-Stokes equations using "Semi-Lagrangian Advection" (backtracing) and a pressure projection step (solving Poisson's equation).
*   **Pros:** Unconditionally stable; excellent for smoke, fire, and gaseous fluids.
*   **Cons:** Dissipation (fluid loses detail/energy) and poor definition of free surfaces (liquids).
*   **Browser:** Viable in WebGL for 2D/3D smoke. 3D grids rapidly consume memory ($N^3$ complexity).

#### 4.1.2 Lagrangian (SPH - Smoothed Particle Hydrodynamics)
The fluid is a collection of particles. Properties (density, pressure) are smoothed over a radius.
*   **Bottleneck:** **Neighborhood Search**. finding neighbors for interactions is $O(N^2)$. Spatial hashing reduces this to $O(N)$, but implementing dynamic spatial hashing on the GPU is complex.
*   **Status:** WebGPU makes SPH viable (30k-70k particles) by using bitonic sort or counting sort in compute shaders to organize particles, but it remains slower than hybrid methods.

#### 4.1.3 Hybrid: Material Point Method (MLS-MPM)
**The Consensus Winner for 2025.** Popularized by the **"Taichi"** language and **David Li's** demos.
*   **How it works:**
    1.  **P2G (Particle to Grid):** Transfer particle mass/momentum to a background grid.
    2.  **Grid Operations:** Solve forces/gravity on the grid (easy, no neighbor search needed).
    3.  **G2P (Grid to Particle):** Transfer velocities back to particles.
*   **Why for Browser:** It combines the visual detail of particles with the computational efficiency of grids. It avoids the complex neighbor search of SPH.
*   **Performance:** ~100,000 to 300,000 particles at 60 FPS on integrated/mid-range GPUs using WebGPU.

### 4.2 Rendering Strategy
To make particle fluids look like liquid:
*   **Screen-Space Fluid Rendering (SSFR):**
    1.  Render particles as spheres to a depth map.
    2.  **Smoothing:** Apply a Bilateral Filter or **Narrow-Range Filter** to smooth the depth map (removing the "bumpy" sphere look).
    3.  **Reconstruction:** Calculate normals from the smoothed depth and render with refraction/reflection.

## 5. Wave and Water Simulation

For large bodies of water (oceans, lakes) where individual particle simulation is inefficient.

### 5.1 Fast Fourier Transform (FFT)
Used in movies (*Titanic*) and AAA games.
*   **Math:** Decomposes the ocean surface into a sum of sine waves (Phillips spectrum). The Inverse FFT (IFFT) constructs the height map.
*   **Implementation:**
    *   **WebGL:** Do IFFT on CPU (slow) or use O($N^2$) DFT in shader.
    *   **WebGPU:** Use **Compute Shaders** to perform the butterfly operations of the FFT algorithm. This reduces complexity to $O(N \log N)$ on the GPU.
*   **Visuals:** Produces realistic, choppy waves with "cusps" (Jacobian modulation).

### 5.2 Heightfields / Shallow Water Equations
*   **Heightfield:** A 2D grid where each cell holds a height value. Simulation propagates waves using the 2D wave equation (neighbors pull each other).
*   **Interaction:** Highly effective for interactive ripples (e.g., character walking in water). Coupling with rigid bodies is easier than FFT: bodies simply displace the height column or act as boundary conditions.
*   **Limitation:** Cannot simulate overturning waves (surfing waves) as height is a function $y = f(x,z)$.

## 6. Gravitational and Orbital Mechanics (N-Body)

Simulating stars, galaxies, or charged particles.

### 6.1 Algorithms

#### 6.1.1 Direct Sum (Naive)
*   **Math:** Every particle interacts with every other particle ($O(N^2)$).
*   **Browser Limit:** ~10,000–20,000 particles using WebGL/WebGPU compute. Above this, frame rate drops significantly.

#### 6.1.2 Barnes-Hut
*   **Math:** Recursively divides space into quadrants (2D) or octants (3D). Groups distant particles into a single "center of mass." Reduces complexity to $O(N \log N)$.
*   **Browser Implementation:** requires building a Quadtree/Octree.
    *   **CPU (JS/WASM):** Feasible for ~50k–100k bodies.
    *   **GPU:** Building trees on GPU is difficult (requires stack management in shaders). However, simplified "Particle-in-Cell" or grid-based gravity approaches on WebGPU can simulate **millions** of particles.

### 6.2 Rendering
For N > 100,000, standard mesh rendering fails.
*   **Points/Billboards:** Use `gl.POINTS` or instanced quads.
*   **Additive Blending:** Essential for the "glowing core" look of galaxies.
*   **Vertex Pulling:** Instead of updating vertex buffers from CPU, the vertex shader reads positions directly from the simulation Storage Buffer.

## 7. Implementation Summary & Recommendations (2025)

| Simulation Type | Recommended Algorithm | Best Tech Stack | Performance Target (Desktop) | Key Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Rigid Body** | **Sequential Impulses** (Stacking) / **XPBD** (Stability) | **Rapier** (WASM) | 5k - 10k Bodies | Erin Catto / Dimforge |
| **Soft Body / Cloth** | **XPBD** (Compliance based) | **WebGPU Compute** | 100k - 600k Nodes | Matthias Müller |
| **Fluid (Interactive)** | **MLS-MPM** (Hybrid) | **WebGPU Compute** | 100k - 300k Particles | David Li / Matsuoka |
| **Ocean** | **FFT** (Compute Shader) | **WebGPU / WebGL 2** | 512x512 Grid + Foam | Tessendorf |
| **N-Body** | **Grid/Convolution** or **Barnes-Hut** | **WebGPU Compute** | 1M - 4M Particles | Bridson / 80.lv |

### Conclusion
For academic or high-fidelity simulation in 2025, **WebGPU is mandatory**. The ability to keep simulation state on the GPU (via Storage Buffers) eliminates the PCIe bus bottleneck that plagued WebGL physics. For standard game physics (boxes, walls), WASM-based engines like **Rapier** offer the best balance of ease-of-use and performance. For specialized effects (water, cloth), custom **XPBD** or **MPM** solvers written in WGSL (WebGPU Shading Language) are the state-of-the-art.

---

## References
 Discourse JuliaLang - Barnes-Hut Performance
 Jheer GitHub - Barnes-Hut D3 implementation
 Three.js Discourse - Physics engine comparisons
 Dev.to - Rapier vs Matter.js benchmarks
 Ten Minute Physics - Matthias Müller PBD/XPBD
 YouTube - XPBD Introduction by Matthias Müller
 WebGPU Showcase - Realistic Physics (Saharan)
 Reddit - Splash Fluid Simulation (MLS-MPM)
 Codrops - WebGPU Fluid Simulations (Matsuoka)
 GitHub - WebGL Stable Fluids (Jos Stam implementation)
 GitHub - FluidsGL (References Jos Stam)
 Jos Stam - Stable Fluids Paper
 Erin Catto - Understanding Constraints (GDC)
 Box2D - Solver2D and Solver variations
 Reddit - 100 Million Particle N-Body (GPU)
 DIVA Portal - WebGPU vs WebGL Particle Performance
 Arxiv - Cloth Simulation WebGPU
 Barth Paleologue - HXPBD Soft Body
 Arxiv - WebGPU Cloth Benchmark
 Barth Paleologue - Ocean Simulation WebGPU
 YouTube - Ten Minute Physics Rigid Body
 YouTube - Ten Minute Physics Rigid Body Series
 Medium - XPBD Multithreaded Engine
 Dimforge - Rapier 2025 Updates
 Codrops - MPM vs SPH explanation
 Reddit - Splash Fluid (MPM details)
 YouTube - Heightfield Water (Müller)
 Reddit - GPU Accelerated FFT Water
 GDC Vault - Fast Water Simulation (Müller)
 Winter.dev - GJK Algorithm
 Medium - GJK Algorithm Walkthrough
 Reddit - Constraint-based Cloth on WebGPU