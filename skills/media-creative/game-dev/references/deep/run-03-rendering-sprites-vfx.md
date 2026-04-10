# Advanced 2D Rendering Techniques for Browser Games: Canvas 2D and WebGL 2 Architecture (2024-2025)

## Executive Summary and Key Findings

Recent developments in browser graphics (2024-2025) indicate a bifurcated best-practice landscape where **Canvas 2D** remains viable for UI-heavy or low-entity-count applications through rigorous CPU-side optimization (dirty rectangles, offscreen layering), while **WebGL 2** has become the standard for high-fidelity 2D rendering. Key architectural shifts include the adoption of **Data-Oriented Design (SoA)** for JavaScript particle systems to maximize cache locality, and the usage of **Texture Arrays** in WebGL 2 to eliminate texture switching overhead in tilemaps.

For lighting, the industry has moved beyond simple additive blending toward **normal-mapped sprites** and **SDF (Signed Distance Field) raymarching** for dynamic soft shadows, bridging the gap between 2D and 3D lighting models. Frameworks like PixiJS v8 demonstrate that performance is now dominated by batching strategies—minimizing draw calls by interleaving geometry and utilizing multi-texture binding. The following report details the implementation of these techniques from scratch, synthesizing current academic and industry standards.

---

## 1. Canvas 2D Performance Architecture

While often considered slower than WebGL, the Canvas 2D API allows for high performance if the interaction with the DOM and the rasterizer is carefully managed. The primary bottleneck in Canvas 2D is the CPU-to-GPU transfer and the immediate-mode rasterization cost.

### 1.1 Layer Separation and Offscreen Buffering
The most effective optimization is **layer separation**. A monolithic canvas requires a full redraw of the scene for any change. By stacking multiple `<canvas>` elements (or using `OffscreenCanvas`), rendering frequencies can be decoupled.
*   **Static Layers:** Backgrounds or tilemaps that do not change should be rendered once to an offscreen canvas. This buffer is then drawn to the main canvas using `drawImage`, which is a fast blit operation compared to re-issuing thousands of vector commands.
*   **Dynamic Layers:** Sprites and particles are drawn on a separate, transparent canvas on top.
*   **Optimization:** When using `OffscreenCanvas`, rendering can be offloaded to a Web Worker. This decouples the rendering loop from the main thread, preventing UI blocking and jank during heavy logic processing.

### 1.2 Dirty Rectangles
For scenes where only a small subset of pixels changes (e.g., a character moving across a static background), full-screen clearing (`clearRect(0, 0, w, h)`) is wasteful. The **dirty rectangle** technique involves tracking the bounding boxes of changed objects.
*   **Implementation:**
    1.  Calculate the union of the bounding box of the object at frame $t$ and frame $t-1$.
    2.  Clip this rectangle to the canvas bounds.
    3.  `clearRect` only this specific region.
    4.  Redraw the background and the object within this region.
*   **Validity:** This technique is computationally worth the complexity only when the "dirty" area covers less than roughly 20-30% of the screen. Beyond this threshold, the overhead of managing rectangles exceeds the cost of a full clear.

### 1.3 Avoiding Sub-pixel Rendering
Canvas 2D attempts to anti-alias drawing commands that land on non-integer coordinates. This forces the browser to perform extra alpha blending calculations.
*   **Technique:** Always round coordinates to integers (`Math.floor` or bitwise `| 0`) before calling `drawImage`. This ensures a 1:1 mapping between source texels and destination pixels, significantly speeding up the rasterizer.

---

## 2. Sprite and Animation Systems (WebGL 2 Focus)

A production-quality sprite renderer in WebGL relies on minimizing draw calls through **batching**. Frameworks like PixiJS implement this by buffering geometry on the CPU and uploading it in chunks.

### 2.1 The Batch Rendering Pipeline
Instead of issuing a `gl.drawElements` call for every sprite, a batch renderer accumulates vertices into a single large Vertex Buffer Object (VBO).
*   **Geometry Merging:** Each sprite contributes 4 vertices and 6 indices (for a quad) to a typed array (e.g., `Float32Array`).
*   **Texture Swapping:** To render sprites with different textures in a single batch, modern engines use multi-texturing. An array of texture units (0–15) is bound. The vertex shader receives a `aTextureId` attribute, which the fragment shader uses to select the correct sampler.
    *   *Constraint:* If the batch fills up or a sprite requires a texture not currently bound, the batch must be "flushed" (drawn) and reset.
*   **Index Buffer Layout:** A static Index Buffer Object (IBO) is uploaded once, containing a repeating pattern of quad indices (0, 1, 2, 0, 2, 3, 4, 5, 6...). This avoids re-uploading indices every frame.

### 2.2 Advanced Sprite Effects via Shaders
Implementing effects "from scratch" requires custom fragment shaders.

#### 2.2.1 Palette Swapping
In retro games, changing character colors (e.g., player 1 vs. player 2) is done via palette swapping.
*   **Implementation:**
    1.  Create a "Swap Texture" (Palette LUT) of size $256 \times N$, where $N$ is the number of palettes.
    2.  The sprite texture is grayscale, where the red channel value ($0.0$ to $1.0$) corresponds to an index ($0$ to $255$).
    3.  **Shader Logic:**
        ```glsl
        float paletteIndex = texture(u_spriteTexture, v_uv).r;
        vec2 lutUV = vec2(paletteIndex, u_currentPaletteRow / u_totalPalettes);
        vec4 color = texture(u_paletteTexture, lutUV);
        ```
    4.  This allows changing the entire color scheme by updating a single uniform float `u_currentPaletteRow`.

#### 2.2.2 Dissolve Effect
Used for death animations or teleportation.
*   **Implementation:**
    1.  Use a "Noise Texture" (e.g., Perlin noise clouds).
    2.  Pass a `u_threshold` uniform ($0.0$ to $1.0$) that increases over time.
    3.  **Shader Logic:**
        ```glsl
        float noiseVal = texture(u_noiseTexture, v_uv).r;
        if (noiseVal < u_threshold) discard;
        ```
    4.  **Edge Glow:** To add a burning edge, check if `noiseVal` is close to `u_threshold` (e.g., `noiseVal < u_threshold + 0.05`) and output an emission color instead of the sprite color.

#### 2.2.3 Outline Effect
*   **Canvas 2D:** The "poor man's" approach is drawing the image 8 times at offsets $(-1, -1)$ to $(1, 1)$, then drawing the sprite on top with `globalCompositeOperation = 'source-over'`.
*   **WebGL:** A fragment shader samples the texture's alpha channel in the 4 cardinal directions (neighbor sampling). If the current pixel is transparent but a neighbor is opaque, render the outline color. Alternatively, use Signed Distance Fields (SDF) for high-quality, resolution-independent outlines.

---

## 3. Tilemap Rendering Techniques

Rendering large maps efficiently requires strategies that bypass the standard sprite batching limits.

### 3.1 Data Textures and Single Quad Rendering
For massive tilemaps (e.g., $1024 \times 1024$), creating geometry for every tile is inefficient.
*   **Technique:** Render a single fullscreen quad.
*   **Data Texture:** Upload the tilemap data (tile indices) as a texture (e.g., `R8UI` or `RGBA8` format). Pixel $(x, y)$ in this texture holds the ID of the tile at map coordinate $(x, y)$.
*   **Shader Logic:**
    1.  Calculate `mapCoord` from screen UVs.
    2.  Fetch `tileID` from the Data Texture.
    3.  Calculate UVs within the Tileset Atlas based on `tileID`.
    4.  Sample the color.

### 3.2 Texture Arrays (WebGL 2)
Standard atlases suffer from "bleeding" (sampling neighboring tiles) during mipmapping or linear filtering. WebGL 2 introduces **Texture Arrays** (`TEXTURE_2D_ARRAY`).
*   **Implementation:** Instead of a giant flat atlas, store tiles as "layers" in a 3D texture object.
*   **Sampling:** `texture(u_tiles, vec3(uv, layerIndex))`.
*   **Benefit:** Hardware clamping handles edges perfectly; no padding/bleeding logic is required in the shader. This is the gold standard for modern 2D engines.

### 3.3 Autotiling Algorithms
*   **Bitmasking:** Checks the 4 or 8 neighbors of a tile. A binary value is constructed (e.g., North=1, East=2, South=4, West=8). The sum (0–15) is the index into the tileset.
*   **Wang Tiles:** Uses edge-matching or corner-matching rules. Each edge is assigned a color; tiles must be placed so shared edges match colors. This is superior for organic terrain as it breaks repetition better than simple bitmasking.

### 3.4 Isometric Depth Sorting
Isometric rendering requires strict draw ordering to preserve depth perception.
*   **Topological Sort:** Modeling dependencies as a graph (Sprite A is "behind" Sprite B) and sorting. This is robust but computationally expensive ($O(N^2)$).
*   **Z-Buffering:** In WebGL, you can enable the depth test.
    *   *Challenge:* 2D sprites are transparent quads. A transparent pixel writes to the Z-buffer, occluding things behind it.
    *   *Solution:* Use `discard` in the fragment shader for alpha $< 0.1$. This prevents transparent pixels from writing depth. Assign Z values based on the sprite's "ground" Y coordinate ($Z = Y \times 0.001$).

---

## 4. 2D Lighting and Shadows

Modern "atmosphere" in 2D games combines geometry-based shadows with normal-mapped surfaces.

### 4.1 2D Normal Mapping (Tangent Space)
To make flat sprites react to dynamic lights, **normal maps** encode surface angles.
*   **Generation:** Tools like **Laigter** or **SpriteIlluminator** generate normal maps from 2D images.
*   **Shader Logic:**
    1.  The shader receives a light position and the sprite's normal map.
    2.  The normal vector $N$ is unpacked from the texture `(rgb * 2.0 - 1.0)`.
    3.  The light direction $L$ is calculated ($LightPos - FragmentPos$).
    4.  **Diffuse:** $max(dot(N, L), 0.0)$ determines brightness.
    5.  This creates volumetric appearance on flat sprites.

### 4.2 2D Raycasting (Hard Shadows)
Used for "Fog of War" or flashlight effects.
*   **Algorithm (Red Blob Games):**
    1.  Collect all wall endpoints.
    2.  Cast rays from the light source to each endpoint (plus slight offsets $\pm \epsilon$).
    3.  Sort intersections by angle.
    4.  Construct a polygon mesh (triangle fan) from the intersections and render it as a mask/stencil.

### 4.3 SDF Shadows (Soft Shadows)
Raymarching Signed Distance Fields (SDF) allows for high-performance soft shadows without constructing geometry.
*   **Implementation:**
    1.  Generate a 2D SDF of the scene (where each pixel stores distance to the nearest occluder).
    2.  In the fragment shader, march a ray from the pixel to the light.
    3.  At each step, sample the SDF. If distance $< \epsilon$, the light is blocked.
    4.  **Soft Shadows:** The "penumbra" is calculated by tracking the closest approach of the ray to any object ($k \cdot min(dist / traveled)$). This technique allows for mathematically perfect variable softness.

---

## 5. Particle Effects: Data-Oriented Architecture

For browser games aiming for 10,000+ particles, the object-oriented approach (`class Particle { x, y, vx, vy }`) causes cache thrashing.

### 5.1 Structure of Arrays (SoA)
Switching to a **Data-Oriented Design** ensures memory contiguity and SIMD-friendly processing (even if JS engines abstract SIMD, TypedArrays help).
*   **Layout:**
    ```javascript
    const MAX_PARTICLES = 10000;
    const x = new Float32Array(MAX_PARTICLES);
    const y = new Float32Array(MAX_PARTICLES);
    const vx = new Float32Array(MAX_PARTICLES);
    const vy = new Float32Array(MAX_PARTICLES);
    const life = new Float32Array(MAX_PARTICLES);
    ```
*   **Update Loop:** Processing simple arrays sequentially is significantly faster for the JIT compiler than iterating arrays of objects, reducing garbage collection pressure to near zero.

### 5.2 GPU Particles
For extreme counts (100k+), simulation must move to the GPU.
*   **Technique:** Use **Transform Feedback** (WebGL 2).
    1.  Two buffers (ping-pong): Source and Destination.
    2.  Vertex shader reads position/velocity, applies physics, and outputs new values.
    3.  Hardware captures the output into the Destination buffer.
    4.  Swap buffers for the next frame.
    5.  Render the buffer as `gl.POINTS`.

---

## 6. Post-Processing Pipelines

Post-processing involves rendering the scene to a **Framebuffer Object (FBO)**, binding that texture, and rendering a fullscreen quad with an effect shader.

### 6.1 Bloom (Glow)
*   **Multi-pass Approach:**
    1.  **Threshold Pass:** Render scene to texture. Shader outputs black if brightness < threshold.
    2.  **Blur Pass:** Downsample and blur the threshold texture. Gaussian blur is standard, but **Kawase blur** (iterative downsampling) is more efficient for real-time.
    3.  **Composite:** Additively blend the blurred texture back onto the original scene.

### 6.2 CRT and Retro Effects
*   **Scanlines:** Use a sine wave based on screen Y coordinate: `sin(uv.y * resolution.y * PI)`.
*   **Chromatic Aberration:** Sample the red, green, and blue channels at slightly offset coordinates:
    ```glsl
    float r = texture(u_tex, uv + offset).r;
    float g = texture(u_tex, uv).g;
    float b = texture(u_tex, uv - offset).b;
    ```
*   **Distortion:** Modify UVs to curve away from the center to simulate screen curvature.

### 6.3 Canvas 2D "Hacks"
While WebGL is preferred, Canvas 2D allows basic effects via the `filter` property.
*   `ctx.filter = 'blur(5px) contrast(1.2)';`
*   *Warning:* This triggers a software or GPU filter pass that can be slow if changed every frame or applied to large areas. For bloom, drawing a pre-blurred image (asset) using `globalCompositeOperation = 'lighter'` is a performant fake.

## Conclusion

For modern 2D browser games (2024-2025), **WebGL 2 is the definitive choice for the rendering backend**, offering features like **Texture Arrays** and **Transform Feedback** that solve historical bottlenecks in tilemap and particle rendering. **Canvas 2D** remains relevant largely for static UI layers or games where implementation speed outweighs raw entity count. The optimal architecture uses a **hybrid approach**: a WebGL layer for the game world (using batching, SDF shadows, and normal mapping) overlaid with a Canvas 2D layer for crisp text and UI. Implementation should prioritize **Data-Oriented Design (SoA)** for physics/particles and **Batch Rendering** for sprites to maximize frame rates.