<!-- Deep reference: WebGL/shaders. Not auto-loaded. -->
<!-- Access via: grep -A N "SECTION_HEADER" references/deep/webgl-shaders.md -->
# WebGL / Three.js / Shaders

## 1. Particle System Backgrounds (Three.js Points + BufferGeometry)

### Overview
Particle systems create dynamic, atmospheric backgrounds using GPU-accelerated point rendering. Modern implementations leverage `THREE.Points` with `BufferGeometry` for efficient rendering of thousands to millions of particles.

### Full Working Implementation

```javascript
import * as THREE from 'three';

class ParticleSystemBackground {
  constructor(container) {
    this.container = container;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    this.renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true
    });

    this.init();
  }

  init() {
    // Setup renderer
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.container.appendChild(this.renderer.domElement);

    // Position camera
    this.camera.position.z = 50;

    // Create particle system
    const particleCount = 5000;
    const geometry = new THREE.BufferGeometry();

    // Positions
    const positions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;

      // Random position in sphere
      const radius = 100;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);

      positions[i3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i3 + 2] = radius * Math.cos(phi);

      // Random velocity
      velocities[i3] = (Math.random() - 0.5) * 0.02;
      velocities[i3 + 1] = (Math.random() - 0.5) * 0.02;
      velocities[i3 + 2] = (Math.random() - 0.5) * 0.02;

      // Color gradient based on position
      const hue = (positions[i3 + 1] + 50) / 100;
      const color = new THREE.Color().setHSL(hue, 0.7, 0.6);
      colors[i3] = color.r;
      colors[i3 + 1] = color.g;
      colors[i3 + 2] = color.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Custom shader material for particles
    const material = new THREE.ShaderMaterial({
      vertexShader: `
        attribute vec3 color;
        attribute vec3 velocity;
        varying vec3 vColor;
        uniform float uTime;

        void main() {
          vColor = color;

          // Animate position based on velocity
          vec3 pos = position + velocity * uTime;

          // Size attenuation based on distance
          vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
          gl_PointSize = 3.0 * (300.0 / -mvPosition.z);
          gl_Position = projectionMatrix * mvPosition;
        }
      `,
      fragmentShader: `
        varying vec3 vColor;

        void main() {
          // Circular particle with soft edge
          vec2 center = gl_PointCoord - vec2(0.5);
          float dist = length(center);
          float alpha = 1.0 - smoothstep(0.3, 0.5, dist);

          gl_FragColor = vec4(vColor, alpha);
        }
      `,
      uniforms: {
        uTime: { value: 0 }
      },
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    this.particles = new THREE.Points(geometry, material);
    this.scene.add(this.particles);

    // Animation
    this.animate();

    // Handle resize
    window.addEventListener('resize', () => this.onResize());
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    this.particles.material.uniforms.uTime.value += 0.01;
    this.particles.rotation.y += 0.001;

    this.renderer.render(this.scene, this.camera);
  }

  onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }
}

// Usage
const particles = new ParticleSystemBackground(document.body);
```

### Performance Notes
- **Mobile Viability:** 2000-5000 particles at 60fps on modern mobile devices
- **Desktop:** 50,000+ particles achievable on discrete GPUs
- **GPU Memory:** ~48 bytes per particle (position + velocity + color)
- **Optimization:** Use `BufferGeometry` (not deprecated `Geometry`), limit `setPixelRatio` to 2, use `AdditiveBlending` for glow effects

### Real-World Examples
- Stripe.com background (subtle particle constellation)
- Vercel.com homepage (animated particle field)
- Awwwards winners using pmndrs/drei `<Points>` component

---

## 2. Shader Planes Behind UI: Noise-Based Gradients & Organic Movement

### Perlin/Simplex Noise Implementation

```glsl
// 2D Simplex Noise (Stefan Gustavson implementation)
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

float snoise(vec2 v) {
  const vec4 C = vec4(0.211324865405187,  // (3.0-sqrt(3.0))/6.0
                      0.366025403784439,  // 0.5*(sqrt(3.0)-1.0)
                     -0.577350269189626,  // -1.0 + 2.0 * C.x
                      0.024390243902439); // 1.0 / 41.0

  // First corner
  vec2 i  = floor(v + dot(v, C.yy));
  vec2 x0 = v -   i + dot(i, C.xx);

  // Other corners
  vec2 i1;
  i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;

  // Permutations
  i = mod289(i);
  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0))
                          + i.x + vec3(0.0, i1.x, 1.0));

  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
  m = m*m;
  m = m*m;

  // Gradients
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;

  m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);

  // Compute final noise value
  vec3 g;
  g.x  = a0.x  * x0.x  + h.x  * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}
```

### Full Shader Plane Implementation

```javascript
import * as THREE from 'three';

const shaderMaterial = new THREE.ShaderMaterial({
  vertexShader: `
    varying vec2 vUv;

    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform vec2 uResolution;
    varying vec2 vUv;

    // Simplex noise function (include full implementation from above)
    ${simplexNoiseGLSL}

    // Fractal Brownian Motion
    float fbm(vec2 st) {
      float value = 0.0;
      float amplitude = 0.5;
      float frequency = 1.0;

      for(int i = 0; i < 6; i++) {
        value += amplitude * snoise(st * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
      }
      return value;
    }

    void main() {
      vec2 st = vUv * 3.0;

      // Animated flow field
      vec2 flow = vec2(
        fbm(st + vec2(uTime * 0.1, 0.0)),
        fbm(st + vec2(0.0, uTime * 0.1))
      );

      // Multiple octaves of noise
      float noise1 = fbm(st + flow * 0.5);
      float noise2 = fbm(st * 2.0 - flow * 0.3);

      // Color mapping
      vec3 color1 = vec3(0.1, 0.2, 0.5); // Deep blue
      vec3 color2 = vec3(0.8, 0.3, 0.6); // Purple
      vec3 color3 = vec3(0.2, 0.8, 0.9); // Cyan

      vec3 finalColor = mix(color1, color2, noise1 * 0.5 + 0.5);
      finalColor = mix(finalColor, color3, noise2 * 0.3 + 0.3);

      // Vignette
      float vignette = 1.0 - length(vUv - 0.5) * 0.8;
      finalColor *= vignette;

      gl_FragColor = vec4(finalColor, 0.8);
    }
  `,
  uniforms: {
    uTime: { value: 0 },
    uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) }
  },
  transparent: true
});

// Create fullscreen plane
const geometry = new THREE.PlaneGeometry(2, 2);
const mesh = new THREE.Mesh(geometry, shaderMaterial);
scene.add(mesh);

// Animation loop
function animate() {
  shaderMaterial.uniforms.uTime.value += 0.01;
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

### Flow Field Implementation

```glsl
// Curl Noise for 2D flow fields
vec2 curlNoise(vec2 p) {
  float eps = 0.001;

  // Calculate noise derivatives
  float n1 = snoise(p + vec2(eps, 0.0));
  float n2 = snoise(p - vec2(eps, 0.0));
  float n3 = snoise(p + vec2(0.0, eps));
  float n4 = snoise(p - vec2(0.0, eps));

  // Compute curl
  float x = (n3 - n4) / (2.0 * eps);
  float y = -(n1 - n2) / (2.0 * eps);

  return vec2(x, y);
}

// Usage in fragment shader
vec2 flow = curlNoise(vUv * 5.0 + uTime * 0.2);
vec2 distortedUV = vUv + flow * 0.1;
```

### Performance Notes
- **Mobile:** Limit to 3-4 octaves of noise, avoid complex flow fields
- **Desktop:** 6-8 octaves achievable at 60fps
- **Memory:** Negligible (procedural generation on GPU)
- **Fallback:** Static gradient for low-end devices

---

## 3. 3D Elements Composited into 2D Pages

### Mix-Blend-Mode + Canvas Overlay Pattern

```html
<div class="hero">
  <canvas id="webgl-canvas"></canvas>
  <div class="content">
    <h1>Welcome</h1>
    <p>Your content here</p>
  </div>
</div>

<style>
.hero {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

#webgl-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  mix-blend-mode: screen; /* Try: multiply, overlay, hard-light */
  opacity: 0.7;
}

.content {
  position: relative;
  z-index: 2;
  color: white;
  padding: 100px;
  mix-blend-mode: difference; /* Text adapts to background */
}
</style>
```

### Three.js Orthographic Overlay

```javascript
// Create separate orthographic camera for 2D overlay elements
const overlayCamera = new THREE.OrthographicCamera(
  -window.innerWidth / 2,
  window.innerWidth / 2,
  window.innerHeight / 2,
  -window.innerHeight / 2,
  0,
  1000
);

const overlayScene = new THREE.Scene();

// Add 3D object that follows HTML elements
function sync3DWithHTML(element, mesh) {
  const rect = element.getBoundingClientRect();
  mesh.position.x = rect.left + rect.width / 2 - window.innerWidth / 2;
  mesh.position.y = -(rect.top + rect.height / 2 - window.innerHeight / 2);
}

// Render pipeline
function render() {
  // Main scene
  renderer.render(scene, camera);

  // Overlay scene (no clear)
  renderer.autoClear = false;
  renderer.render(overlayScene, overlayCamera);
  renderer.autoClear = true;
}
```

### Performance Notes
- **Mobile:** Use simpler geometry, reduce polygon count to <10k
- **Blending:** `screen` and `overlay` are GPU-efficient
- **Draw Calls:** Keep overlay scene to <20 objects

---

## 4. Post-Processing: Bloom, Chromatic Aberration, Depth of Field

### Complete Post-Processing Setup (pmndrs/postprocessing)

```javascript
import { EffectComposer } from 'postprocessing';
import { RenderPass } from 'postprocessing';
import { EffectPass } from 'postprocessing';
import { BloomEffect } from 'postprocessing';
import { ChromaticAberrationEffect } from 'postprocessing';
import { DepthOfFieldEffect } from 'postprocessing';

// Setup
const composer = new EffectComposer(renderer, {
  frameBufferType: THREE.HalfFloatType // High precision
});

// 1. Render Pass (draws the scene)
composer.addPass(new RenderPass(scene, camera));

// 2. Bloom Effect
const bloomEffect = new BloomEffect({
  intensity: 1.5,
  luminanceThreshold: 0.15,
  luminanceSmoothing: 0.9,
  mipmapBlur: true,
  radius: 0.85
});

// 3. Chromatic Aberration
const chromaticAberrationEffect = new ChromaticAberrationEffect({
  offset: new THREE.Vector2(0.001, 0.001),
  radialModulation: true,
  modulationOffset: 0.5
});

// 4. Depth of Field
const depthOfFieldEffect = new DepthOfFieldEffect(camera, {
  focusDistance: 0.0,
  focalLength: 0.05,
  bokehScale: 2.0,
  height: 480
});

// Combine into single pass (efficient!)
const effectPass = new EffectPass(
  camera,
  bloomEffect,
  chromaticAberrationEffect,
  depthOfFieldEffect
);

composer.addPass(effectPass);

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  composer.render();
}
```

### Custom Bloom Shader (Lightweight Alternative)

```glsl
// Brightness extraction pass
vec3 brightness = max(color - vec3(0.8), vec3(0.0));

// Gaussian blur (horizontal pass)
vec4 blur(sampler2D tex, vec2 uv, vec2 direction) {
  vec4 color = vec4(0.0);
  vec2 offset[3] = vec2[](
    vec2(-1.3846153846) * direction,
    vec2(0.0),
    vec2(1.3846153846) * direction
  );
  float weight[3] = float[](0.2270270270, 0.3162162162, 0.0702702703);

  for(int i = 0; i < 3; i++) {
    color += texture2D(tex, uv + offset[i] / uResolution) * weight[i];
  }
  return color;
}

// Final combine
vec3 bloom = blur(brightnessTex, vUv).rgb;
gl_FragColor = vec4(baseColor + bloom * 0.5, 1.0);
```

### Performance Budgets
- **Bloom:** ~2ms on desktop, ~5ms on mobile (with mipmap blur)
- **Chromatic Aberration:** <0.5ms (simple offset)
- **DOF:** ~4ms desktop, avoid on mobile unless critical
- **Combined:** Target <10ms total post-processing time

---

## 5. GLSL Snippet Patterns (Complete Implementations)

### 5.1 Voronoi / Worley Noise

```glsl
vec2 random2(vec2 p) {
  return fract(sin(vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)))) * 43758.5453);
}

float worleyNoise(vec2 uv, float columns, float rows) {
  vec2 index_uv = floor(vec2(uv.x * columns, uv.y * rows));
  vec2 fract_uv = fract(vec2(uv.x * columns, uv.y * rows));

  float minimum_dist = 1.0;

  // Check 3x3 neighboring cells
  for(int y = -1; y <= 1; y++) {
    for(int x = -1; x <= 1; x++) {
      vec2 neighbor = vec2(float(x), float(y));
      vec2 point = random2(index_uv + neighbor);

      // Animate point
      point = 0.5 + 0.5 * sin(uTime + 6.2831 * point);

      vec2 diff = neighbor + point - fract_uv;
      float dist = length(diff);
      minimum_dist = min(minimum_dist, dist);
    }
  }

  return minimum_dist;
}
```

### 5.2 Ray Marching Basics (SDF Spheres + Smooth Union)

```glsl
// Signed Distance Functions
float sdSphere(vec3 p, float radius) {
  return length(p) - radius;
}

float sdBox(vec3 p, vec3 b) {
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// Smooth min (polynomial smooth union)
float smin(float a, float b, float k) {
  float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
  return mix(b, a, h) - k * h * (1.0 - h);
}

// Scene SDF
float sceneSDF(vec3 p) {
  float sphere1 = sdSphere(p - vec3(0.0, 0.0, 0.0), 1.0);
  float sphere2 = sdSphere(p - vec3(sin(uTime) * 2.0, 0.0, 0.0), 0.8);
  return smin(sphere1, sphere2, 0.5);
}

// Ray marching
float rayMarch(vec3 ro, vec3 rd) {
  float t = 0.0;
  for(int i = 0; i < 100; i++) {
    vec3 p = ro + rd * t;
    float d = sceneSDF(p);
    if(d < 0.001) break;
    t += d;
    if(t > 100.0) break;
  }
  return t;
}

// Normal calculation
vec3 calcNormal(vec3 p) {
  vec2 e = vec2(0.001, 0.0);
  return normalize(vec3(
    sceneSDF(p + e.xyy) - sceneSDF(p - e.xyy),
    sceneSDF(p + e.yxy) - sceneSDF(p - e.yxy),
    sceneSDF(p + e.yyx) - sceneSDF(p - e.yyx)
  ));
}
```

### 5.3 SDF 2D Shapes (Circle, Box, Rounded Box, Ring)

```glsl
// Circle
float sdCircle(vec2 p, float r) {
  return length(p) - r;
}

// Box
float sdBox(vec2 p, vec2 b) {
  vec2 d = abs(p) - b;
  return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

// Rounded Box
float sdRoundedBox(vec2 p, vec2 b, vec4 r) {
  r.xy = (p.x > 0.0) ? r.xy : r.zw;
  r.x = (p.y > 0.0) ? r.x : r.y;
  vec2 q = abs(p) - b + r.x;
  return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r.x;
}

// Ring
float sdRing(vec2 p, vec2 n, float r, float th) {
  p.x = abs(p.x);
  p = mat2(n.x, n.y, -n.y, n.x) * p;
  return max(
    abs(length(p) - r) - th * 0.5,
    length(vec2(p.x, max(0.0, abs(r - p.y) - th * 0.5))) * sign(p.x)
  );
}

// Usage example
void main() {
  vec2 uv = (gl_FragCoord.xy - 0.5 * uResolution.xy) / uResolution.y;

  float d = sdRoundedBox(uv, vec2(0.3, 0.2), vec4(0.1, 0.05, 0.05, 0.1));
  vec3 color = (d > 0.0) ? vec3(0.9, 0.6, 0.3) : vec3(0.2, 0.3, 0.4);
  color *= 1.0 - exp(-3.0 * abs(d));
  color *= 0.8 + 0.2 * cos(140.0 * d);
  color = mix(color, vec3(1.0), 1.0 - smoothstep(0.0, 0.01, abs(d)));

  gl_FragColor = vec4(color, 1.0);
}
```

### 5.4 Color Grading (Levels, Curves, Hue Shift)

```glsl
// Levels adjustment
vec3 levels(vec3 color, float minInput, float gamma, float maxInput, float minOutput, float maxOutput) {
  vec3 col = clamp((color - minInput) / (maxInput - minInput), 0.0, 1.0);
  col = pow(col, vec3(1.0 / gamma));
  return mix(vec3(minOutput), vec3(maxOutput), col);
}

// RGB to HSV
vec3 rgb2hsv(vec3 c) {
  vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
  vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
  vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

  float d = q.x - min(q.w, q.y);
  float e = 1.0e-10;
  return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

// HSV to RGB
vec3 hsv2rgb(vec3 c) {
  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

// Hue shift
vec3 hueShift(vec3 color, float shift) {
  vec3 hsv = rgb2hsv(color);
  hsv.x = fract(hsv.x + shift);
  return hsv2rgb(hsv);
}

// Saturation
vec3 saturation(vec3 color, float amount) {
  vec3 hsv = rgb2hsv(color);
  hsv.y *= amount;
  return hsv2rgb(hsv);
}
```

### 5.5 Film Grain, Vignette, Chromatic Aberration

```glsl
// Film grain
float grain(vec2 uv, float strength, float time) {
  float x = (uv.x + 4.0) * (uv.y + 4.0) * (time * 10.0);
  return (mod((mod(x, 13.0) + 1.0) * (mod(x, 123.0) + 1.0), 0.01) - 0.005) * strength;
}

// Vignette
float vignette(vec2 uv, float strength, float extent) {
  float dist = distance(uv, vec2(0.5));
  return 1.0 - smoothstep(extent, extent + strength, dist);
}

// Chromatic aberration
vec3 chromaticAberration(sampler2D tex, vec2 uv, float amount) {
  vec2 direction = uv - vec2(0.5);
  vec3 color;
  color.r = texture2D(tex, uv + direction * amount).r;
  color.g = texture2D(tex, uv).g;
  color.b = texture2D(tex, uv - direction * amount).b;
  return color;
}

// Complete post-process example
void main() {
  vec2 uv = vUv;

  // 1. Chromatic aberration
  vec3 color = chromaticAberration(uTexture, uv, 0.002);

  // 2. Film grain
  color += vec3(grain(uv, 0.08, uTime));

  // 3. Vignette
  color *= vignette(uv, 0.5, 0.5);

  // 4. Color grading
  color = levels(color, 0.0, 1.1, 1.0, 0.0, 1.0);

  gl_FragColor = vec4(color, 1.0);
}
```

---

## 6. Canvas 2D API: Generative Backgrounds & Metaballs

### Metaballs Complete Implementation

```javascript
class Metaballs {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.width = canvas.width = window.innerWidth;
    this.height = canvas.height = window.innerHeight;

    this.balls = [];
    this.threshold = 0.5;

    this.init();
  }

  init() {
    // Create balls
    for(let i = 0; i < 6; i++) {
      this.balls.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        radius: 50 + Math.random() * 50
      });
    }

    this.animate();
  }

  metaballFunction(x, y) {
    let sum = 0;
    for(let ball of this.balls) {
      const dx = x - ball.x;
      const dy = y - ball.y;
      const distSq = dx * dx + dy * dy;
      sum += (ball.radius * ball.radius) / distSq;
    }
    return sum;
  }

  animate() {
    // Update positions
    for(let ball of this.balls) {
      ball.x += ball.vx;
      ball.y += ball.vy;

      if(ball.x < 0 || ball.x > this.width) ball.vx *= -1;
      if(ball.y < 0 || ball.y > this.height) ball.vy *= -1;
    }

    // Clear canvas
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Create image data for pixel manipulation
    const imageData = this.ctx.createImageData(this.width, this.height);
    const data = imageData.data;

    // Calculate metaball field (sample every 2 pixels for performance)
    const step = 2;
    for(let y = 0; y < this.height; y += step) {
      for(let x = 0; x < this.width; x += step) {
        const value = this.metaballFunction(x, y);

        if(value > this.threshold) {
          // Color based on field strength
          const intensity = Math.min(value / 2, 1);
          const color = this.getColor(intensity);

          // Fill 2x2 block
          for(let dy = 0; dy < step; dy++) {
            for(let dx = 0; dx < step; dx++) {
              const px = x + dx;
              const py = y + dy;
              if(px < this.width && py < this.height) {
                const index = (py * this.width + px) * 4;
                data[index] = color.r;
                data[index + 1] = color.g;
                data[index + 2] = color.b;
                data[index + 3] = 255;
              }
            }
          }
        }
      }
    }

    this.ctx.putImageData(imageData, 0, 0);
    requestAnimationFrame(() => this.animate());
  }

  getColor(intensity) {
    // Gradient from blue to cyan
    return {
      r: Math.floor(intensity * 100),
      g: Math.floor(intensity * 200),
      b: Math.floor(200 + intensity * 55)
    };
  }
}

// Usage
const canvas = document.getElementById('metaballs');
const metaballs = new Metaballs(canvas);
```

### Procedural Particle Trails

```javascript
class ParticleTrails {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', { alpha: false });
    this.width = canvas.width = window.innerWidth;
    this.height = canvas.height = window.innerHeight;

    this.particles = [];
    this.mouseX = this.width / 2;
    this.mouseY = this.height / 2;

    this.init();
  }

  init() {
    // Mouse tracking
    this.canvas.addEventListener('mousemove', (e) => {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
    });

    this.animate();
  }

  animate() {
    // Fade previous frame (trail effect)
    this.ctx.fillStyle = 'rgba(10, 10, 20, 0.1)';
    this.ctx.fillRect(0, 0, this.width, this.height);

    // Spawn new particles
    if(this.particles.length < 200) {
      this.particles.push({
        x: this.mouseX + (Math.random() - 0.5) * 50,
        y: this.mouseY + (Math.random() - 0.5) * 50,
        vx: (Math.random() - 0.5) * 4,
        vy: (Math.random() - 0.5) * 4,
        life: 1.0,
        size: Math.random() * 3 + 1
      });
    }

    // Update and render particles
    this.particles = this.particles.filter(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.1; // Gravity
      p.life -= 0.01;

      // Draw
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fillStyle = `hsla(${200 + p.life * 50}, 70%, 60%, ${p.life})`;
      this.ctx.fill();

      return p.life > 0;
    });

    requestAnimationFrame(() => this.animate());
  }
}
```

### Performance Notes
- **Metaballs:** 30fps on mobile with 4-6 balls, 60fps desktop with 10+
- **Sampling:** Use 2-4 pixel steps, not per-pixel
- **Memory:** Avoid creating new ImageData each frame
- **Alternative:** Use WebGL for metaballs (much faster)

---

## 7. SVG Effects: Morphing, Line-Drawing, feTurbulence

### 7.1 Flubber.js SVG Morphing

```html
<svg width="200" height="200">
  <path id="shape" d="M50,50 L150,50 L100,150 Z" fill="#4CAF50"/>
</svg>

<script type="module">
import flubber from 'flubber';

const shape = document.getElementById('shape');

// Define start and end shapes
const triangle = "M50,50 L150,50 L100,150 Z";
const circle = "M100,50 A50,50 0 1,1 99,50 Z";

// Create interpolator
const interpolator = flubber.interpolate(triangle, circle);

// Animate
function animate(timestamp) {
  const t = (Math.sin(timestamp / 1000) + 1) / 2; // 0-1 oscillation
  shape.setAttribute('d', interpolator(t));
  requestAnimationFrame(animate);
}

animate(0);
</script>
```

### 7.2 GSAP MorphSVG (Premium Plugin)

```javascript
import { gsap } from 'gsap';
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin';

gsap.registerPlugin(MorphSVGPlugin);

// Simple morph
gsap.to("#shape1", {
  duration: 2,
  morphSVG: "#shape2",
  ease: "power2.inOut",
  repeat: -1,
  yoyo: true
});

// Complex timeline
const tl = gsap.timeline({ repeat: -1 });
tl.to("#logo", { duration: 1, morphSVG: "#icon1" })
  .to("#logo", { duration: 1, morphSVG: "#icon2" })
  .to("#logo", { duration: 1, morphSVG: "#logo" });
```

### 7.3 Stroke-Dashoffset Line Drawing

```html
<svg width="500" height="300">
  <path id="line"
        d="M10,150 Q150,50 250,150 T490,150"
        fill="none"
        stroke="#2196F3"
        stroke-width="3"/>
</svg>

<style>
#line {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: draw 3s ease-in-out forwards;
}

@keyframes draw {
  to {
    stroke-dashoffset: 0;
  }
}
</style>

<script>
// JavaScript alternative
const path = document.getElementById('line');
const length = path.getTotalLength();

path.style.strokeDasharray = length;
path.style.strokeDashoffset = length;

let progress = 0;
function animate() {
  progress += 0.01;
  if(progress > 1) progress = 0;

  path.style.strokeDashoffset = length * (1 - progress);
  requestAnimationFrame(animate);
}
animate();
</script>
```

### 7.4 feTurbulence Displacement Animation

```html
<svg width="400" height="400">
  <filter id="turbulence">
    <feTurbulence
      type="turbulence"
      baseFrequency="0.02"
      numOctaves="3"
      result="turbulence"
      seed="2">
      <animate
        attributeName="baseFrequency"
        dur="20s"
        values="0.01;0.04;0.01"
        repeatCount="indefinite"/>
    </feTurbulence>

    <feDisplacementMap
      in="SourceGraphic"
      in2="turbulence"
      scale="20"
      xChannelSelector="R"
      yChannelSelector="G"/>
  </filter>

  <text x="50" y="200"
        font-size="60"
        fill="#FF5722"
        filter="url(#turbulence)">
    TURBULENCE
  </text>
</svg>
```

### 7.5 Animated Clip-Path

```html
<svg width="400" height="300">
  <defs>
    <clipPath id="clip">
      <rect id="clipRect" x="0" y="0" width="0" height="300"/>
    </clipPath>
  </defs>

  <image
    href="image.jpg"
    width="400"
    height="300"
    clip-path="url(#clip)"/>
</svg>

<script>
import { gsap } from 'gsap';

// Reveal animation
gsap.to("#clipRect", {
  duration: 2,
  attr: { width: 400 },
  ease: "power2.inOut"
});

// Shape-based clip path animation
gsap.timeline({ repeat: -1 })
  .to("#clipPath circle", {
    duration: 1,
    attr: { r: 200 }
  })
  .to("#clipPath circle", {
    duration: 1,
    attr: { r: 50 }
  });
</script>
```

---

## 8. Performance Guidance & Mobile Strategy

### GPU Memory Budgets

#### Desktop (Discrete GPU)
- **Textures:** 1-2GB safe
- **Geometry:** 500k-1M triangles @ 60fps
- **Particles:** 100k+ points
- **Post-processing:** 5-6 passes acceptable

#### Mobile (Integrated GPU)
- **Textures:** 128-256MB limit
- **Geometry:** 50k-100k triangles
- **Particles:** 5k-10k points
- **Post-processing:** 1-2 passes max

### OffscreenCanvas + Web Workers

```javascript
// main.js
const canvas = document.getElementById('webgl');
const offscreen = canvas.transferControlToOffscreen();

const worker = new Worker('renderer-worker.js');
worker.postMessage({ canvas: offscreen }, [offscreen]);

// renderer-worker.js
self.onmessage = (e) => {
  const canvas = e.data.canvas;
  const gl = canvas.getContext('webgl2');

  function render() {
    // WebGL rendering code
    gl.clear(gl.COLOR_BUFFER_BIT);
    // ... rendering logic

    requestAnimationFrame(render);
  }

  render();
};
```

### Mobile Detection & Fallback Strategy

```javascript
const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
const hasGoodGPU = await testGPUPerformance();

function testGPUPerformance() {
  return new Promise(resolve => {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl2');

    if(!gl) return resolve(false);

    // Test shader compilation time
    const start = performance.now();
    const shader = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(shader, complexShaderSource);
    gl.compileShader(shader);
    const duration = performance.now() - start;

    resolve(duration < 50); // <50ms = good GPU
  });
}

// Adaptive quality
const config = {
  particleCount: isMobile ? 2000 : 50000,
  postProcessing: hasGoodGPU,
  pixelRatio: isMobile ? 1 : Math.min(devicePixelRatio, 2),
  shadowMapSize: isMobile ? 512 : 2048,
  useHalfFloat: hasGoodGPU
};
```

### CSS Fallback for Low-End Devices

```css
/* Static gradient fallback */
.webgl-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Only show WebGL on capable devices */
@supports (mix-blend-mode: screen) and (backdrop-filter: blur(10px)) {
  .webgl-container canvas {
    display: block;
  }
}

@supports not (mix-blend-mode: screen) {
  .webgl-container canvas {
    display: none;
  }
}
```

### FPS Monitoring & Adaptive Quality

```javascript
class AdaptiveQuality {
  constructor() {
    this.fpsHistory = [];
    this.targetFPS = 60;
    this.currentQuality = 1.0;
  }

  update(deltaTime) {
    const fps = 1000 / deltaTime;
    this.fpsHistory.push(fps);

    if(this.fpsHistory.length > 60) {
      this.fpsHistory.shift();
    }

    // Check every 2 seconds
    if(this.fpsHistory.length === 60) {
      const avgFPS = this.fpsHistory.reduce((a, b) => a + b) / 60;

      if(avgFPS < 50) {
        this.currentQuality *= 0.9;
        this.applyQualitySettings();
      } else if(avgFPS > 58 && this.currentQuality < 1.0) {
        this.currentQuality = Math.min(1.0, this.currentQuality * 1.05);
        this.applyQualitySettings();
      }

      this.fpsHistory = [];
    }
  }

  applyQualitySettings() {
    // Reduce particle count
    particleSystem.setCount(Math.floor(50000 * this.currentQuality));

    // Adjust pixel ratio
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1 + this.currentQuality));

    // Toggle post-processing
    if(this.currentQuality < 0.7) {
      composer.removePass(bloomPass);
    }
  }
}
```

---

## 9. Real-World Examples & Case Studies

### Production Sites Using These Techniques (2024-2025)

1. **Stripe.com** - Subtle particle constellation background
   - Technique: 5k particles with BufferGeometry
   - Mobile: Disabled on devices with <2GB RAM

2. **Vercel.com** - Animated gradient mesh
   - Technique: Simplex noise + flow fields
   - Fallback: Static CSS gradient

3. **Apple Vision Pro Site** - 3D product composited over 2D layout
   - Technique: Orthographic overlay + mix-blend-mode
   - Mobile: Static images replace WebGL

4. **Awwwards SOTD Winners**
   - Common: Bloom + chromatic aberration
   - Trend: Selective bloom (only bright objects)

5. **Codrops Demos** (tympanus.net/codrops)
   - "Shape Lens Blur" - SDF-based effects
   - "Infinite Hyperbolic Helicoid" - Ray marching
   - "Grid Layout Transitions" - Canvas 2D particles

---

## 10. Performance Thresholds Summary

### Desktop Targets (60 FPS)

| Effect | Triangle Count | Draw Calls | GPU Time |
|--------|---------------|------------|----------|
| Particle system | 50k points | 1 | 2ms |
| Shader background | 2 triangles | 1 | 3ms |
| Bloom (5 passes) | - | 5 | 4ms |
| DOF | - | 3 | 5ms |
| Total budget | <500k | <50 | <16ms |

### Mobile Targets (30-60 FPS)

| Effect | Triangle Count | Draw Calls | GPU Time |
|--------|---------------|------------|----------|
| Particle system | 5k points | 1 | 4ms |
| Shader background | 2 triangles | 1 | 8ms |
| Simple post-process | - | 1-2 | 5ms |
| Total budget | <50k | <20 | <33ms |

---

## 11. Tools & Libraries Reference

### Core Libraries
- **Three.js** r170+ (latest stable)
- **@react-three/fiber** v9+ (React integration)
- **@react-three/drei** (Helper components)
- **postprocessing** v6.38+ (pmndrs/postprocessing)

### Shader Tools
- **ShaderToy** - Prototyping GLSL
- **GLSL Sandbox** - Live shader editor
- **lygia** - GLSL library with noise functions

### Animation
- **GSAP** v3.12+ (with MorphSVG)
- **Flubber** - SVG morphing
- **Anime.js** - Lightweight alternative

### Performance
- **Stats.js** - FPS monitor
- **Spector.js** - WebGL debugger
- **Chrome DevTools** - GPU profiling
