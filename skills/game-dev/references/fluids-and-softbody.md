# Fluids & Soft Body

> Fluid simulation, cloth, soft bodies, and deformable physics for the browser.

## Stable Fluids (Jos Stam)

Grid-based Eulerian fluid simulation. The classic approach, implementable as ping-pong FBO shaders.

**Steps per frame:**
1. **Advect:** Move quantities (velocity, density) along the velocity field using semi-Lagrangian backtracing
2. **Diffuse:** Spread quantities to neighbors (Jacobi iteration or direct solve)
3. **Project:** Make velocity field divergence-free (pressure solve via Jacobi/Gauss-Seidel)
4. **Add forces:** User input (mouse), gravity, buoyancy

**Implementation:** Each step is a separate shader pass. Velocity stored as `vec2` in `RG` channels of a float texture. Pressure in a separate texture.

**Key insight:** Semi-Lagrangian advection is unconditionally stable (the "stable" in Stable Fluids) — allows large timesteps without explosion.

⤷ Full Stable Fluids: `grep -A 100 "Stable Fluids\|Stam\|fluid" references/deep/run-04-realtime-physics-sim.md`
⤷ Shader implementation: `grep -A 80 "advect\|Advect\|pressure" references/deep/run-07-webgl-glsl-shaders.md`

## MLS-MPM (Moving Least Squares Material Point Method)

Particle-grid hybrid for realistic fluids, snow, sand, and other materials. The state-of-the-art for browser physics.

**Key concepts:**
- **Particles** carry material state (position, velocity, deformation gradient, mass)
- **Grid** is temporary — built fresh each frame for force computation
- **P2G → Grid solve → G2P** pipeline each frame

**Performance:** 100k-300k particles achievable with WebGPU compute. WebGL2 GPGPU possible but harder.

**Why MLS-MPM over Stable Fluids:**
- Handles topology changes (splashing, merging)
- Naturally supports multiple materials
- Particle-based = easier boundary handling
- But more compute-intensive per particle

⤷ Full MLS-MPM: `grep -A 100 "MPM\|Material Point" references/deep/run-04-realtime-physics-sim.md`

## XPBD for Soft Bodies & Cloth

Extended Position-Based Dynamics — the workhorse for soft body simulation.

**Distance constraint (springs):**
```
Δx = (|x_1 - x_2| - restLength) * compliance_correction * direction
```

**Cloth setup:**
1. Grid of particles connected by distance constraints (structural + shear + bend)
2. Each frame: integrate gravity → solve constraints (4-10 iterations) → update velocities
3. Collision against floor/spheres via position projection

**Compliance** (`α = 1/(k·dt²)`) controls stiffness. `α = 0` = perfectly rigid. Higher = softer.

**Advantages over spring-mass:** No stiffness-dependent instability. Can use large timesteps. Unconditionally stable.

⤷ Full XPBD implementation: `grep -A 100 "XPBD\|position-based\|cloth" references/deep/run-04-realtime-physics-sim.md`

## WebGPU Compute for Physics

All the above methods benefit enormously from compute shaders:

| Method | WebGL2 Feasible? | WebGPU Gains |
|--------|-----------------|-------------|
| Stable Fluids | Yes (FBO shaders) | 2-3× via compute |
| MLS-MPM | Barely (complex P2G) | 10-50× (enables it) |
| XPBD cloth | CPU only practical | 10-100× (600k nodes) |
| SPH fluids | CPU ~5k particles | 100k+ via compute |

**Pattern:** Physics compute dispatch → render pipeline reads result buffer.

⤷ WebGPU compute physics: `grep -A 80 "WebGPU\|compute" references/deep/run-04-realtime-physics-sim.md`

## Quick Decision Guide

| Want... | Use... |
|---------|--------|
| Smoke/ink in water (visual) | Stable Fluids (ping-pong FBO) |
| Splashing liquid | MLS-MPM (WebGPU compute) |
| Cloth/fabric | XPBD (CPU for <1k particles, WebGPU for more) |
| Jelly/soft objects | XPBD with volume preservation |
| Sand/granular | MLS-MPM with Drucker-Prager yield |
| Rope/chain | XPBD distance constraints in a line |
