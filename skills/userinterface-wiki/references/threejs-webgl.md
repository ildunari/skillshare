# Three.js and WebGL Animation for UI

> Bridging the animation-engine skill with game-dev for shader-driven backgrounds, 3D UI elements, particle decorations, and GPU-accelerated visual effects embedded in web interfaces. Covers Three.js scene lifecycle, uniform animation, shader backgrounds, and integration patterns with DOM UI layers.

## Contents
- When to Use (tool hierarchy) → Claude Artifact Constraints (CDN, React)
- Animation Loop Patterns → Uniform Animation (time, mouse, scroll)
- UI Integration: Shader Background → 3D in Card/Section → Fullscreen Quad
- Shader Techniques: Noise → Domain Warping → Mouse-Reactive → Color Systems
- Touch/Resize Handling → Cleanup/Dispose → Performance Budget → Reduced Motion

---

## When to Use

Use WebGL/Three.js animation when you need: animated shader backgrounds (noise fields, domain warping, gradient flows), 3D interactive elements embedded in UI (product viewers, globe visualizations, architectural walkthroughs), GPU particle systems as ambient decoration, post-processing effects (bloom, chromatic aberration, film grain), or any visual that exceeds what CSS/SVG can express. This reference covers the *animation* patterns — for deep shader writing, SDF raymarching, physics simulations, and compute pipelines, load the game-dev skill's references. **For raw WebGL2/Regl fullscreen shaders without Three.js**, the game-dev skill has standalone implementations; this file focuses on Three.js scene integration with DOM UI.

### Where this fits in the tool hierarchy

| Need | Tool |
|---|---|
| Ambient CSS shimmer, gradient rotation, pulse | CSS `@keyframes` — no WebGL needed |
| SVG morph, draw, motion path | GSAP plugins or Anime.js |
| Scroll-driven 3D camera, shader uniforms linked to scroll | Three.js + GSAP ScrollTrigger or scroll event bridge |
| Full-screen shader background | Raw WebGL2 fragment shader (no Three.js overhead) or Regl |
| 3D scene with objects, lights, materials | Three.js |
| High-performance particles (10K+) | Three.js with BufferGeometry + custom shaders, or PIXI.js for 2D |
| 2D vector art with animation | Paper.js (see `references/paperjs.md`) |

---

## Claude Artifact Constraints

### CDN imports for HTML artifacts

```html
<!-- Three.js r128 (UMD, artifact-safe) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<!-- For addons (OrbitControls, etc.) — use absolute CDN URLs -->
<!-- three/addons/ relative paths do NOT resolve in artifact sandboxes -->
```

**Pinned version:** Use r128 for artifacts. It's the last version with a clean UMD build on cdnjs. Newer versions (r150+) are ESM-only and require import maps that artifact sandboxes handle inconsistently.

**No addon barrel imports.** `import { OrbitControls } from "three/addons/controls/OrbitControls.js"` won't work. Either inline the control code, use a separate CDN URL, or skip orbit controls and implement mouse-driven camera manually.

### React artifacts

Three.js in React artifacts requires manual canvas management — there's no `@react-three/fiber` bundled. Use a `useRef` + `useEffect` pattern:

```jsx
import { useRef, useEffect } from "react";

export default function ShaderBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    // ... scene setup, animation loop
    return () => { renderer.dispose(); };
  }, []);

  return <canvas ref={canvasRef} className="absolute inset-0 -z-10" />;
}
```

Note: Three.js must be loaded via `<script>` in the HTML head for React artifacts, or bundled inline. It's not available as an npm import in the artifact sandbox.

---

## Animation Loop Patterns

### Basic requestAnimationFrame loop

```js
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const elapsed = clock.getElapsedTime();
  const delta = clock.getDelta();

  // Update uniforms
  material.uniforms.u_time.value = elapsed;

  // Update objects
  mesh.rotation.y += delta * 0.5;

  renderer.render(scene, camera);
}
animate();
```

### Uniform animation patterns

Uniforms are the bridge between JavaScript time/input and GPU shaders. Animate them per-frame for dynamic effects.

```js
const material = new THREE.ShaderMaterial({
  uniforms: {
    u_time: { value: 0 },
    u_mouse: { value: new THREE.Vector2(0, 0) },
    u_scroll: { value: 0 },
    u_resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) }
  },
  vertexShader: vertSrc,
  fragmentShader: fragSrc
});

// Per-frame updates
function animate() {
  material.uniforms.u_time.value = clock.getElapsedTime();
  // ...
}

// Mouse tracking (smooth)
let targetMouse = new THREE.Vector2();
document.addEventListener("mousemove", e => {
  targetMouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  targetMouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
});

// In animation loop — lerp for smooth follow
material.uniforms.u_mouse.value.lerp(targetMouse, 0.08);
```

### Scroll-linked uniform animation

Bridge scroll position into shader uniforms for scroll-driven visual effects:

```js
// Vanilla scroll bridge
let scrollProgress = 0;
window.addEventListener("scroll", () => {
  scrollProgress = window.scrollY / (document.body.scrollHeight - window.innerHeight);
});

// In animation loop
material.uniforms.u_scroll.value += (scrollProgress - material.uniforms.u_scroll.value) * 0.1;
```

With GSAP ScrollTrigger:

```js
ScrollTrigger.create({
  trigger: ".hero-section",
  start: "top top",
  end: "bottom top",
  onUpdate: self => {
    material.uniforms.u_scroll.value = self.progress;
  }
});
```

---

## Common UI Integration Patterns

### Pattern: Shader background behind DOM content

The most common WebGL-in-UI pattern. A full-viewport canvas sits behind HTML/CSS content.

```html
<style>
  canvas.bg {
    position: fixed;
    inset: 0;
    z-index: -1;
    width: 100vw;
    height: 100dvh;
  }
  .content {
    position: relative;
    z-index: 1;
  }
</style>

<canvas class="bg" id="bg"></canvas>
<div class="content">
  <!-- Normal DOM UI here -->
</div>
```

**Performance rule:** The shader runs every frame. Keep fragment shader complexity reasonable — avoid 100+ step raymarches for backgrounds. Domain warping with 4–6 octave fBm, simple gradient flows, and particle fields are good choices. If the background is subtle, reduce canvas resolution:

```js
const DPR = Math.min(devicePixelRatio, 1.5); // cap at 1.5x for backgrounds
renderer.setPixelRatio(DPR);
```

### Pattern: 3D element in a card/section

A Three.js canvas scoped to a specific UI region, not full-viewport.

```js
const container = document.querySelector(".product-viewer");
const rect = container.getBoundingClientRect();

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(rect.width, rect.height);
renderer.setClearColor(0x000000, 0); // transparent background
container.appendChild(renderer.domElement);

// Resize observer for responsive
const ro = new ResizeObserver(entries => {
  const { width, height } = entries[0].contentRect;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
});
ro.observe(container);
```

### Pattern: Fullscreen quad for fragment-only effects

When you only need a fragment shader (no 3D geometry), skip most of Three.js and render a fullscreen quad:

```js
const geometry = new THREE.PlaneGeometry(2, 2);
const material = new THREE.ShaderMaterial({
  uniforms: { u_time: { value: 0 }, u_resolution: { value: new THREE.Vector2() } },
  vertexShader: `void main() { gl_Position = vec4(position.xy, 0.0, 1.0); }`,
  fragmentShader: fragSrc
});
const mesh = new THREE.Mesh(geometry, material);

const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
scene.add(mesh);
```

Or skip Three.js entirely and use raw WebGL2 or Regl for zero-overhead fullscreen shaders. See the Regl and raw WebGL2 examples in the game-dev skill.

---

## Shader Techniques for UI Animation

These are the building blocks for animated visual effects. Full implementations live in game-dev references; here's the UI-relevant subset.

### Noise-based motion

```glsl
// Organic flowing gradients
float n = fbm(uv * 3.0 + u_time * 0.2);
vec3 color = palette(n, ...); // iq cosine palette

// Vertex displacement (breathing surfaces)
vec3 displaced = position + normal * noise(position * 2.0 + u_time * 0.5) * 0.1;
```

### Domain warping (nested distortion)

```glsl
// Triple-stacked for rich organic patterns
vec2 q = vec2(fbm(p + u_time * 0.3), fbm(p + vec2(5.2, 1.3)));
vec2 r = vec2(fbm(p + 4.0 * q + u_time * 0.1), fbm(p + 4.0 * q + vec2(1.7, 9.2)));
float f = fbm(p + 4.0 * r);
```

### Mouse-reactive effects

```glsl
// Gravitational pull on noise field
vec2 pull = (u_mouse - uv) * 0.3 / (1.0 + length(u_mouse - uv) * 2.0);
float n = fbm(uv + pull + u_time * 0.2);

// Ripple from mouse position
float dist = length(uv - u_mouse);
float ripple = sin(dist * 30.0 - u_time * 5.0) * exp(-dist * 4.0);
```

### Color systems

```glsl
// iq cosine palette (compact, tunable)
vec3 palette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
  return a + b * cos(6.28318 * (c * t + d));
}

// Warm editorial preset
palette(t, vec3(0.5), vec3(0.5), vec3(1.0, 0.7, 0.4), vec3(0.0, 0.15, 0.2));

// Cool midnight preset
palette(t, vec3(0.5, 0.5, 0.6), vec3(0.4, 0.3, 0.5), vec3(0.8, 0.8, 0.5), vec3(0.0, 0.1, 0.35));
```

---

## Touch and Resize Handling

All WebGL artifacts need these for mobile compatibility:

```js
// Prevent swipe-dismiss in artifact iframes
document.addEventListener("touchmove", e => e.preventDefault(), { passive: false });
document.addEventListener("gesturestart", e => e.preventDefault(), { passive: false });
```

```css
html, body {
  touch-action: none;
  overscroll-behavior: none;
  overflow: hidden;
}
canvas { touch-action: none; }
```

Touch input → uniform bridge:

```js
document.addEventListener("touchstart", e => {
  e.preventDefault();
  targetMouse.x = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
  targetMouse.y = -(e.touches[0].clientY / window.innerHeight) * 2 + 1;
}, { passive: false });

document.addEventListener("touchmove", e => {
  e.preventDefault();
  targetMouse.x = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
  targetMouse.y = -(e.touches[0].clientY / window.innerHeight) * 2 + 1;
}, { passive: false });
```

Resize handling:

```js
window.addEventListener("resize", () => {
  const w = window.innerWidth, h = window.innerHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  material.uniforms.u_resolution.value.set(w * DPR, h * DPR);
});
```

---

## Cleanup and Performance

### Dispose pattern

Three.js doesn't garbage-collect GPU resources. Always dispose when unmounting:

```js
function cleanup() {
  renderer.dispose();
  scene.traverse(obj => {
    if (obj.geometry) obj.geometry.dispose();
    if (obj.material) {
      if (obj.material.map) obj.material.map.dispose();
      obj.material.dispose();
    }
  });
}
```

### Performance budget for UI backgrounds

| Complexity | Target | Example |
|---|---|---|
| Simple gradient flow | 60fps, any device | 2-3 octave noise, no raymarching |
| Domain warping | 60fps, mid-range+ | 5-7 octave fBm, nested distortion |
| Raymarched SDF | 30-60fps, depends on step count | Keep MAX_STEPS ≤ 80 for backgrounds |
| Particle system (Three.js Points) | 60fps up to ~50K particles | BufferGeometry, no per-particle JS |

**Cap pixel ratio** for background canvases at 1.5x. Nobody notices 2x vs 1.5x on a blurred noise field, but the GPU absolutely does.

---

## Reduced Motion

WebGL animations are almost always ornamental. Under reduced motion, either:

1. **Freeze to a static frame** — render once, stop the loop
2. **Slow dramatically** — reduce time uniform speed by 90%+
3. **Replace with CSS gradient** — if the shader is essentially a gradient, a CSS equivalent suffices

```js
const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function animate() {
  if (!prefersReduced) {
    requestAnimationFrame(animate);
    material.uniforms.u_time.value = clock.getElapsedTime();
  } else {
    // Render one frame with a fixed time value
    material.uniforms.u_time.value = 2.0; // pick an aesthetically pleasing moment
  }
  renderer.render(scene, camera);
}
animate();
```

---

## Cross-Skill Loading

When building WebGL-animated UI, load these references together:

| From this skill | Purpose |
|---|---|
| This file | Integration patterns, uniform animation, UI layering |
| `tool-selection.md` | Confirm WebGL is the right choice (not CSS/SVG) |
| `reduced-motion.md` | Accessibility policy |

| From game-dev skill | Purpose |
|---|---|
| Shader references | fBm, SDF, raymarching, noise implementations |
| GPU particle references | BufferGeometry particle systems |
| Performance tier guidance | Canvas2D vs WebGL2 vs WebGPU selection |

| From design-maestro skill | Purpose |
|---|---|
| Anti-slop checklist | Verify the visual isn't generic |
| Color/typography | Ensure shader colors match the UI theme |
| Theme files | Palette definitions for shader uniforms |
