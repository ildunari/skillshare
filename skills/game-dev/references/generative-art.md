# Generative Art

> Noise-based art, reaction-diffusion, fractals, agent-based systems, and domain warping.

## Noise Foundations

### fBm (Fractal Brownian Motion)
Layer noise at increasing frequency and decreasing amplitude:
```glsl
float fbm(vec2 p) {
    float sum = 0.0, amp = 0.5, freq = 1.0;
    for (int i = 0; i < 6; i++) {
        sum += amp * snoise(p * freq);
        freq *= 2.0; amp *= 0.5;
    }
    return sum;
}
```
**Octaves** control detail level. **Lacunarity** (frequency multiplier, default 2.0) and **gain** (amplitude multiplier, default 0.5) shape the character.

### Domain Warping
Feed noise into noise coordinates for organic, alien landscapes:
```glsl
f(p) = fBm(p + fBm(p + fBm(p)))
```
Each layer of warping adds more organic distortion. Animate the inner offsets over time for flowing motion.

⤷ Full noise and warping: `grep -A 100 "domain warp\|Domain Warp\|fBm" references/deep/run-06-algorithmic-generative-art.md`

## Reaction-Diffusion (Gray-Scott)

Two chemicals A and B react and diffuse on a 2D grid. Produces spots, stripes, mitosis, coral-like patterns.

**Equations:**
```
dA/dt = D_A·∇²A - A·B² + f·(1-A)
dB/dt = D_B·∇²B + A·B² - (k+f)·B
```

**Parameters:**
- `D_A` = 1.0, `D_B` = 0.5 (diffusion rates, A diffuses faster)
- `f` = feed rate (0.01-0.08), `k` = kill rate (0.045-0.07)
- **Pearson's classification:** Different (f,k) pairs produce wildly different patterns. Reference: `mrob.com/pub/comp/xmorphia/`

**Implementation:** Ping-pong FBO shader. Each texel is `vec4(A, B, 0, 1)`. Laplacian computed from 4 or 8 neighbors.

**Seeding:** Paint initial B concentration with mouse or geometric shapes. Start with A=1, B=0 everywhere, then add B seeds.

⤷ Full Gray-Scott shader: `grep -A 80 "Gray-Scott\|reaction-diffusion" references/deep/run-06-algorithmic-generative-art.md`
⤷ Template: `assets/simulation-base.html`

## Physarum (Slime Mold)

Agent-based simulation producing organic network patterns.

**Algorithm (per agent, per frame):**
1. **Sense:** Sample chemical trail at 3 points (ahead, ahead-left, ahead-right) at `sensorDistance`
2. **Rotate:** Turn toward strongest signal. If center strongest, go straight. Random jitter if equal.
3. **Move:** Step forward by `moveSpeed`
4. **Deposit:** Add chemical at new position
5. **Diffuse + Decay:** Blur the trail map and multiply by decay factor

**Implementation:** Agents stored in a buffer (compute shader or Transform Feedback). Trail map is a ping-pong FBO that gets blurred each frame.

**Key parameters:** `sensorAngle` (22.5°-45°), `sensorDistance` (9-35px), `rotationAngle` (22.5°-45°), `moveSpeed` (1-3px), `decayFactor` (0.9-0.99).

⤷ Full Physarum: `grep -A 80 "Physarum\|physarum\|slime" references/deep/run-06-algorithmic-generative-art.md`

## Fractals

### Mandelbrot / Julia Sets
```glsl
// Smooth iteration count for continuous coloring
float mandelbrot(vec2 c) {
    vec2 z = vec2(0.0);
    for (int i = 0; i < MAX_ITER; i++) {
        z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
        if (dot(z,z) > 256.0) {
            float nu = float(i) + 1.0 - log2(log(length(z)));
            return nu;
        }
    }
    return -1.0; // inside set
}
```

**Coloring:** Map `nu` through a palette. `0.5 + 0.5 * cos(2π * (t * freq + offset))` with different RGB offsets creates rich palettes.

**Julia sets:** Same iteration but `c` is a fixed parameter and `z` starts at the pixel coordinate. Animate `c` for morphing shapes.

⤷ Full fractal rendering: `grep -A 80 "Mandelbrot\|fractal\|Julia" references/deep/run-06-algorithmic-generative-art.md`

## Lenia

Continuous generalization of cellular automata (e.g., Game of Life). Uses kernel convolution with smooth growth functions instead of discrete neighbor counts. Produces lifelike "creatures" that move and interact.

⤷ Lenia details: `grep -A 60 "Lenia\|lenia" references/deep/run-06-algorithmic-generative-art.md`

## Fractal Flames

Iterated Function Systems with nonlinear "variation" functions (sinusoidal, spherical, swirl, horseshoe, etc.) + log-density histogram rendering. Extremely rich output.

⤷ Fractal flames: `grep -A 60 "Flame\|flame\|IFS" references/deep/run-06-algorithmic-generative-art.md`

## Cellular Automata

**Game of Life:** Classic, binary. Good intro to ping-pong texture sims.
**Multi-state:** Brian's Brain (3 states), Wireworld (4 states).
**Continuous:** Smooth Life, Lenia.

All implementable as ping-pong FBO shaders — each texel reads its neighbors, applies rules, writes new state.

## Color Palettes for Generative Art

```glsl
// Cosine palette (Inigo Quilez)
vec3 palette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
    return a + b * cos(6.28318 * (c * t + d));
}
```

Vary `a,b,c,d` vectors for different moods. `t` is typically normalized iteration count, density, velocity magnitude, or chemical concentration.
