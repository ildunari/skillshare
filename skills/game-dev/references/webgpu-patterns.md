# WebGPU Patterns

> Compute shaders, buffer management, and the WebGL2 fallback strategy.

## Feature Detection

```javascript
async function initGPU() {
  if (!navigator.gpu) return null; // No WebGPU — fall back to WebGL2
  const adapter = await navigator.gpu.requestAdapter();
  if (!adapter) return null;
  const device = await adapter.requestDevice();
  return { adapter, device };
}
```

**Browser support (as of late 2025):** Chrome 113+, Edge 113+, Firefox 141+, Safari 26+ (macOS/iOS). Always provide WebGL2 fallback for broader reach.

## Architecture: Compute + Render

```
┌─────────────────────────────────────────────┐
│  Compute Pass                               │
│  ┌──────────┐     ┌──────────┐             │
│  │ Buffer A │ ──> │ Buffer B │  (ping-pong) │
│  │ (read)   │     │ (write)  │             │
│  └──────────┘     └──────────┘             │
└───────────────────────┬─────────────────────┘
                        │ Buffer B becomes vertex input
┌───────────────────────▼─────────────────────┐
│  Render Pass                                │
│  Vertex Shader reads Buffer B → Fragment    │
│  Output to canvas                           │
└─────────────────────────────────────────────┘
```

## Compute Shader Basics (WGSL)

```wgsl
struct Particle {
  pos: vec2f,
  vel: vec2f,
  life: f32,
  _pad: f32, // align to 16 bytes
};

struct Params {
  dt: f32,
  count: u32,
  gravity: vec2f,
};

@group(0) @binding(0) var<storage, read> particlesIn: array<Particle>;
@group(0) @binding(1) var<storage, read_write> particlesOut: array<Particle>;
@group(0) @binding(2) var<uniform> params: Params;

@compute @workgroup_size(256)
fn main(@builtin(global_invocation_id) id: vec3u) {
  let i = id.x;
  if (i >= params.count) { return; }
  
  var p = particlesIn[i];
  p.vel += params.gravity * params.dt;
  p.pos += p.vel * params.dt;
  p.life -= params.dt;
  particlesOut[i] = p;
}
```

## Buffer Setup (JS Side)

```javascript
const particleByteSize = 6 * 4; // 6 floats × 4 bytes (with padding)
const bufferSize = maxParticles * particleByteSize;

const bufferA = device.createBuffer({
  size: bufferSize,
  usage: GPUBufferUsage.STORAGE | GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
});
const bufferB = device.createBuffer({
  size: bufferSize,
  usage: GPUBufferUsage.STORAGE | GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
});
```

**Usage flags:** `STORAGE` for compute read/write, `VERTEX` for render pipeline input, `COPY_DST` for initial data upload via `device.queue.writeBuffer()`.

## Bind Groups

```javascript
const bindGroupLayout = device.createBindGroupLayout({
  entries: [
    { binding: 0, visibility: GPUShaderStage.COMPUTE, buffer: { type: 'read-only-storage' } },
    { binding: 1, visibility: GPUShaderStage.COMPUTE, buffer: { type: 'storage' } },
    { binding: 2, visibility: GPUShaderStage.COMPUTE, buffer: { type: 'uniform' } },
  ],
});

// Create two bind groups for ping-pong
const bindGroupAtoB = device.createBindGroup({
  layout: bindGroupLayout,
  entries: [
    { binding: 0, resource: { buffer: bufferA } },  // read
    { binding: 1, resource: { buffer: bufferB } },  // write
    { binding: 2, resource: { buffer: paramsBuffer } },
  ],
});
// ... and bindGroupBtoA (reversed)
```

## Dispatch

```javascript
const commandEncoder = device.createCommandEncoder();

// Compute pass
const computePass = commandEncoder.beginComputePass();
computePass.setPipeline(computePipeline);
computePass.setBindGroup(0, currentBindGroup);
computePass.dispatchWorkgroups(Math.ceil(particleCount / 256));
computePass.end();

// Render pass
const renderPass = commandEncoder.beginRenderPass(renderPassDescriptor);
renderPass.setPipeline(renderPipeline);
renderPass.setVertexBuffer(0, currentOutputBuffer);
renderPass.draw(6, particleCount); // 6 vertices per quad, instanced
renderPass.end();

device.queue.submit([commandEncoder.finish()]);

// Swap for next frame
[currentBindGroup, nextBindGroup] = [nextBindGroup, currentBindGroup];
[currentOutputBuffer, nextOutputBuffer] = [nextOutputBuffer, currentOutputBuffer];
```

## Workgroup Sizing

- **Default:** `@workgroup_size(256)` — works everywhere
- **1D problems** (particles): `dispatchWorkgroups(ceil(count / 256))`
- **2D problems** (textures/grids): `@workgroup_size(16, 16)` → `dispatchWorkgroups(ceil(w/16), ceil(h/16))`
- **Shared memory:** Use `var<workgroup>` for tile-based algorithms (prefix sum, reduction)

## Texture Compute (Alternative to Storage Buffers)

For grid-based sims (fluids, reaction-diffusion), use `texture_storage_2d`:

```wgsl
@group(0) @binding(0) var texIn: texture_2d<f32>;
@group(0) @binding(1) var texOut: texture_storage_2d<rgba32float, write>;

@compute @workgroup_size(16, 16)
fn main(@builtin(global_invocation_id) id: vec3u) {
  let coords = vec2i(id.xy);
  let val = textureLoad(texIn, coords, 0);
  // ... compute new value
  textureStore(texOut, coords, newVal);
}
```

## WebGL2 Fallback Strategy

When WebGPU isn't available:
1. **Particles:** Use Transform Feedback (see `gpu-particles.md`)
2. **Grid sims:** Use FBO ping-pong with fragment shaders (see `shaders-and-rendering.md`)
3. **Physics compute:** Fall back to CPU (potentially with WASM/Rapier)

**Detection pattern:**
```javascript
const gpu = await initGPU();
if (gpu) { initWebGPU(gpu.device); }
else { initWebGL2Fallback(); }
```

⤷ Full WebGPU examples: `grep -A 100 "WebGPU\|webgpu\|WGSL" references/deep/run-05-gpu-particles.md`
⤷ WebGPU physics: `grep -A 80 "WebGPU\|compute" references/deep/run-04-realtime-physics-sim.md`
