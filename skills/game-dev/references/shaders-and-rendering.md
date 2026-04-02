# Shaders & Rendering

> WebGL2 rendering pipeline, GLSL patterns, post-processing, and lighting for 2D games and simulations.

## WebGL2 Setup Checklist

1. Get context: `canvas.getContext('webgl2', { alpha: false, antialias: false, premultipliedAlpha: false })`
2. Compile vertex + fragment shaders → link program
3. Create VAO, bind buffers, set attribute pointers
4. Set uniforms (resolution, time, mouse)
5. `requestAnimationFrame` render loop

**Inline shaders in HTML artifacts:** Use `<script type="x-shader/x-vertex">` or template literals.

⤷ Full WebGL2 boilerplate: `grep -A 80 "WebGL" references/deep/run-07-webgl-glsl-shaders.md`
⤷ Template: `assets/simulation-base.html`

## FBO (Framebuffer Object) Ping-Pong

The universal pattern for shader-based simulations. Two textures, swap each frame.

```javascript
// Setup: create two framebuffers with textures
const fboA = createFBO(width, height);
const fboB = createFBO(width, height);
let read = fboA, write = fboB;

// Each frame:
gl.bindFramebuffer(gl.FRAMEBUFFER, write.fbo);
gl.activeTexture(gl.TEXTURE0);
gl.bindTexture(gl.TEXTURE_2D, read.texture);
gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); // fullscreen quad
[read, write] = [write, read]; // swap
```

**Texture format:** `gl.RGBA32F` for float precision (physics), `gl.RGBA8` for visual effects. Use `gl.getExtension('EXT_color_buffer_float')` for float render targets.

⤷ Full FBO setup: `grep -A 60 "FBO\|Framebuffer" references/deep/run-07-webgl-glsl-shaders.md`

## Essential GLSL Patterns

### Noise Functions

```glsl
// Simplex 2D (compact version — for full impl see deep reference)
// Use for: terrain, organic motion, domain warping
float snoise(vec2 v); // Returns -1 to 1

// fBm (fractal Brownian motion) — layered noise
float fbm(vec2 p) {
    float sum = 0.0, amp = 0.5;
    for (int i = 0; i < 6; i++) {
        sum += amp * snoise(p);
        p *= 2.0; amp *= 0.5;
    }
    return sum;
}
```

⤷ Full noise library (simplex2D, 3D, 4D): `grep -A 80 "noise\|simplex" references/deep/run-07-webgl-glsl-shaders.md`

### SDF Primitives

```glsl
float sdCircle(vec2 p, float r) { return length(p) - r; }
float sdBox(vec2 p, vec2 b) { vec2 d = abs(p)-b; return length(max(d,0.0)) + min(max(d.x,d.y),0.0); }
float sdSegment(vec2 p, vec2 a, vec2 b) {
    vec2 pa=p-a, ba=b-a;
    float h = clamp(dot(pa,ba)/dot(ba,ba), 0.0, 1.0);
    return length(pa - ba*h);
}
```

**Combining SDFs:** `min(a,b)` = union, `max(a,b)` = intersection, `max(a,-b)` = subtraction, `smin(a,b,k)` = smooth blend (see SKILL.md).

⤷ Full SDF library: `grep -A 100 "SDF\|sdf" references/deep/run-07-webgl-glsl-shaders.md`

### Post-Processing Pipeline

**Kawase Bloom** (faster than Gaussian, looks great):
1. Threshold pass: extract bright pixels (luminance > threshold)
2. Iterative downscale + blur (4-5 passes at halfres, quarterres, etc.)
3. Upscale + composite back to original

**ACES Tone Mapping** — see SKILL.md for the snippet. Apply after bloom, before gamma.

**Gamma correction:** `color = pow(color, vec3(1.0/2.2))` — always apply as final step.

⤷ Full bloom implementation: `grep -A 80 "bloom\|Bloom" references/deep/run-03-rendering-sprites-vfx.md`

### Normal-Mapped Sprites

Light 2D sprites as if they have depth:
1. Artist paints (or tool generates) normal map from sprite
2. Fragment shader samples normal map, computes diffuse + specular lighting
3. Light position passed as uniform (mouse position makes great interactive demo)

Tools: **Laigter** (free, generates normal maps from sprites), or compute in shader from heightmap.

⤷ Normal mapping: `grep -A 60 "normal map" references/deep/run-03-rendering-sprites-vfx.md`

### Sprite Batching

For games with many sprites, batch into a single draw call:
- Interleaved VBO: `[x,y,u,v,color]` per vertex
- Texture atlas: all sprites in one texture
- Dynamic buffer update each frame
- Can render 10k+ sprites in one `gl.drawElements` call

⤷ Batch rendering: `grep -A 80 "batch\|Batch" references/deep/run-03-rendering-sprites-vfx.md`

### Tilemap Rendering

**WebGL2 Texture Arrays** — render entire tilemaps in a single draw call:
- Each tile type is a layer in a `TEXTURE_2D_ARRAY`
- Vertex shader computes tile position from instance ID
- Fragment shader samples the correct layer based on tile data

⤷ Tilemap rendering: `grep -A 60 "Tilemap\|tilemap" references/deep/run-03-rendering-sprites-vfx.md`
