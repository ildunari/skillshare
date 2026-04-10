# GPU Particle Systems

> From CPU pools to Transform Feedback to WebGPU compute. Scaling from thousands to millions.

## CPU Particle System (Tier 1: up to ~50k)

SoA layout with swap-and-pop removal. See `game-loop-and-architecture.md` for the pattern.

```javascript
// Update loop (hot path — no allocations)
for (let i = 0; i < count; i++) {
  vx[i] += ax[i] * dt;  vy[i] += ay[i] * dt;
  px[i] += vx[i] * dt;  py[i] += vy[i] * dt;
  life[i] -= dt;
  if (life[i] <= 0) kill(i--); // swap-and-pop, recheck index
}
```

**Rendering:** Use `ctx.drawImage()` with a single pre-rendered radial gradient sprite. Batch via `globalCompositeOperation = 'lighter'` for additive blending.

## WebGL2 Transform Feedback (Tier 3: up to ~4M)

GPU-side particle update without compute shaders. The vertex shader reads from buffer A, writes updated state to buffer B, then they swap (ping-pong).

**Architecture:**
1. Two VBOs (vertex buffer objects) holding all particle state (pos, vel, life, etc.)
2. Transform Feedback captures the vertex shader output into the other VBO
3. Render pass draws from the just-updated buffer
4. Swap buffers each frame

**Key setup:**
```javascript
const tf = gl.createTransformFeedback();
gl.bindTransformFeedback(gl.TRANSFORM_FEEDBACK, tf);
gl.bindBufferBase(gl.TRANSFORM_FEEDBACK_BUFFER, 0, bufferB);
gl.beginTransformFeedback(gl.POINTS);
gl.drawArrays(gl.POINTS, 0, particleCount);
gl.endTransformFeedback();
// Swap A ↔ B for next frame
```

**Particle state encoding:** Pack into vec4 attributes:
- `a_posLife` = `vec4(x, y, z, life)`
- `a_velSeed` = `vec4(vx, vy, vz, seed)`

⤷ Full Transform Feedback setup: `grep -A 120 "Transform Feedback" references/deep/run-05-gpu-particles.md`
⤷ Template: `assets/particle-base.html`

## WebGPU Compute (Tier 4: 10M-30M+)

True GPGPU. Compute shader reads/writes storage buffers, render pipeline draws the result.

**Architecture:**
1. Two storage buffers (ping-pong)
2. Compute pass: dispatch workgroups to update particle state
3. Render pass: vertex shader reads from updated buffer, draws as points/quads

```wgsl
@compute @workgroup_size(256)
fn update(@builtin(global_invocation_id) id: vec3u) {
  let i = id.x;
  if (i >= params.count) { return; }
  var p = particlesIn[i];
  p.vel += params.gravity * params.dt;
  p.pos += p.vel * params.dt;
  p.life -= params.dt;
  particlesOut[i] = p;
}
```

**Workgroup sizing:** 256 is the safe default. Must be a multiple of the GPU's warp/wavefront size (32 NVIDIA, 64 AMD).

⤷ Full WebGPU compute particles: `grep -A 100 "WebGPU" references/deep/run-05-gpu-particles.md`
⤷ Template: `assets/webgpu-compute-base.html`

## Force Fields

Common forces to integrate in the update step:

| Force | Formula | Notes |
|-------|---------|-------|
| Gravity | `vel.y += G * dt` | Constant downward |
| Point attractor | `vel += normalize(target - pos) * strength / dist² * dt` | Inverse-square falloff |
| Curl noise | `vel += curl(noise3D(pos * scale)) * strength * dt` | Organic turbulence, divergence-free |
| Drag | `vel *= pow(damping, dt)` | Frame-rate independent decay |
| Vortex | `vel += perpendicular(toCenter) * strength / dist * dt` | Tangential force |
| Bounds | Reflect or wrap when outside domain | Simple position clamp + vel flip |

**Curl noise** is the gold standard for organic-looking particle motion. It's the curl of a 3D noise field, guaranteeing incompressible (divergence-free) flow.

⤷ Force field implementations: `grep -A 60 "Force" references/deep/run-05-gpu-particles.md`

## Spawn Strategies

- **Burst:** Emit N particles at once (explosion, impact)
- **Stream:** Emit N per second (fire, smoke, trail)
- **Ring/shape:** Position on circle/line/mesh surface at spawn
- **Recycle:** When `life <= 0`, reset position/velocity instead of destroying (keeps buffer count constant — critical for GPU systems where buffer size is fixed)

## Rendering Tricks

- **Point sprites:** Fastest. `gl_PointSize` in vertex shader. Limited to squares unless using texture.
- **Billboarded quads:** Two triangles per particle, always face camera. Better quality, 6× the vertex count.
- **Additive blending:** `gl.blendFunc(gl.SRC_ALPHA, gl.ONE)` — overlapping particles get brighter. Great for fire, magic, energy.
- **Soft particles:** Fade alpha near depth buffer intersections (requires depth texture). Prevents hard clipping against geometry.
- **Trails:** Store N previous positions per particle. Render as line strip or ribbon mesh.

⤷ Full rendering techniques: `grep -A 80 "Rendering" references/deep/run-05-gpu-particles.md`
