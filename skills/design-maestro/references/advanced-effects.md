# Advanced Visual Effects

> Compressed index for CSS atmospheric effects, WebGL/Three.js, GLSL shaders, and Canvas/SVG techniques.

## CSS Effects Quick Reference

| Effect | Browser Support | Mobile Safe? | Key Gotcha |
|---|---|---|---|
| Glassmorphism (`backdrop-filter`) | ✅ All (2024+) | ⚠️ Reduce blur on mobile | Needs `-webkit-` prefix on Safari. Reduce blur 16→8px on mobile. |
| Mesh Gradients | ✅ Universal | ⚠️ Max 5-7 layers | Animate `background-position` sparingly. Use `background-size: 200%`. |
| Noise/Grain (SVG feTurbulence) | ✅ Universal | ✅ Yes | Apply as `::after` pseudo with `mix-blend-mode: overlay`. Low opacity (0.03-0.08). |
| Aurora Gradients | ✅ Universal | ⚠️ Simplify on mobile | CSS `@keyframes` on `background-position`. `animation-duration: 15-25s`. |
| Animated Gradient Borders | ✅ (needs `@property`) | ✅ Yes | `conic-gradient` + `@property` for angle animation. Fallback: static border. |
| Text Gradient Clip | ✅ All (2024+) | ✅ Yes | `background-clip: text` + `color: transparent`. Add `-webkit-` prefix. |
| Variable Font Animation | ✅ Where font supports | ✅ Yes | Animate `font-variation-settings` with CSS transitions. Only works with variable fonts. |
| Container Queries | ✅ All (2023+) | ✅ Yes | `container-type: inline-size`. Component-level responsive. No `height` queries yet. |
| Scroll-Driven Animations | ✅ Chrome 115+, ✅ FF 130+ | ✅ Safari 26+, FF disabled by default | `animation-timeline: scroll()` or `view()`. Safari 26+ ships native support. |
| View Transitions API | ✅ Chrome 111+, ✅ Safari 18.2+ | ⚠️ Progressive enhance | `document.startViewTransition()`. Same-document and cross-document. ✅ FF 144+. |
| `@starting-style` | ✅ Chrome 117+, ✅ FF 129+, ✅ Safari 17.5+ | ✅ (where supported) | Entry animations without JS. Pair with `transition-behavior: allow-discrete`. |
| Popover API + Anchor | 🟡 Chrome 114+, partial Safari | ✅ (where supported) | Native `popover` attr. `anchor-name` CSS for positioning. Radix fallback. |
| CSS Nesting / `:has()` | ✅ All (2024+) | ✅ Yes | Native nesting `&`. `:has()` is the parent selector CSS never had. |
| `oklch()` / `color-mix()` | ✅ All (2024+) | ✅ Yes | Perceptually uniform. `color-mix(in oklch, var(--primary) 80%, black)` for shades. |

### Modern CSS (2025-2026)

These features are stable and should be used by default:

| Feature | What It Does | Browser Support | Key Usage |
|---|---|---|---|
| `text-wrap: balance` | Balances line lengths in headings (no orphaned last word) | ✅ All (2024+) | Apply to all `h1`–`h3`. `h1 { text-wrap: balance; }` |
| `text-wrap: pretty` | Better line-breaking for body text (avoids orphans) | ✅ All (2024+) | Apply to `p` and prose containers. |
| `@layer` | Cascade layers for specificity management | ✅ All (2022+) | `@layer reset, base, tokens, components, utilities, overrides;` Eliminates specificity wars. |
| `interpolate-size: allow-keywords` | Enables `transition: height 0.3s` with `height: auto` | ✅ Chrome 129+, Safari 26+ | Eliminates JS-measured height animations. Accordion/expand without hacks. |
| `field-sizing: content` | Auto-growing textareas and inputs | ✅ Chrome 123+ | `textarea { field-sizing: content; min-height: 3lh; }` No JS resize handlers. |
| `color(display-p3 ...)` | Wide gamut colors beyond sRGB | ✅ All (Safari 15+, Chrome 111+, FF 113+) | Brand accents, status colors. Always with sRGB fallback. |
| `light-dark()` | Automatic light/dark color switching | ✅ All (2024+) | `color: light-dark(#333, #ccc)` — requires `color-scheme: light dark`. |
| `linear()` timing function | Custom easing curves defined by points | ✅ All (2023+) | Bounce, spring, complex easing without JS. `linear(0, 0.5 30%, 1)` |
| `round()` / `mod()` / `rem()` | CSS math for snapping values | ✅ All (2024+) | `width: round(nearest, 100%, 8px)` snaps to 8px grid. |
| Relative color syntax | Programmatic color manipulation | ✅ All (2024+) | `oklch(from var(--brand) calc(l * 0.8) c h)` for derived shades. |
| `@scope` | Component-level style containment | ✅ Chrome 118+ | `@scope (.card) { h2 { ... } }` — styles scoped to component subtree. |

⤷ Full code + fallbacks for each: `grep -A 80 "## 1. Glassmorphism" references/deep/css-effects.md`

### When to Use What
- **Subtle atmosphere** (grain, gradient, blur): CSS only. No JS needed.
- **Interactive backgrounds** (particles, flow fields): Canvas 2D or Three.js.
- **3D elements in 2D pages**: Three.js with orthographic camera + `mix-blend-mode`.
- **Heavy computation** (ray marching, fluid sim): WebGL shaders. Desktop only for complex shaders.
- **Vector animation** (morphing, line drawing): SVG + GSAP or CSS transitions.

---

## WebGL / Three.js Patterns

### Particle Systems (Background)
- Three.js `Points` + `BufferGeometry` for 10k+ particles
- Map position, color, size to `Float32Array` buffers
- Animate in `requestAnimationFrame`, update buffer attributes
- **Mobile:** Cap at 5k particles, reduce to 2k on low-end
- ⤷ `grep -A 140 "### Full Working Implementation" references/deep/webgl-shaders.md`

### Shader Planes (Organic Backgrounds)
- Full-screen quad with custom fragment shader
- Use `uniform float uTime` for animation
- Perlin noise for organic movement, flow fields for directional patterns
- **Mobile:** Halve resolution (`renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5))`)
- ⤷ `grep -A 90 "### Full Shader Plane Implementation" references/deep/webgl-shaders.md`

### Post-Processing
- Use `pmndrs/postprocessing` (EffectComposer) for bloom, chromatic aberration, DOF
- Custom bloom: two-pass Gaussian blur on bright pixels
- **Budget:** Max 2-3 effects stacked. Each costs ~2ms GPU time.
- ⤷ `grep -A 60 "### Complete Post-Processing Setup" references/deep/webgl-shaders.md`

### 3D Composited into 2D
- Canvas overlay with `pointer-events: none`, `mix-blend-mode: screen`
- Or Three.js orthographic camera matched to DOM coordinates
- ⤷ `grep -A 40 "### Mix-Blend-Mode + Canvas Overlay" references/deep/webgl-shaders.md`

## GLSL Snippet Library

| Snippet | Use For | Grep Target |
|---|---|---|
| Voronoi / Worley Noise | Cell patterns, organic textures | `grep -A 30 "### 5.1 Voronoi" references/deep/webgl-shaders.md` |
| Ray Marching (SDF) | 3D primitives without meshes | `grep -A 50 "### 5.2 Ray Marching" references/deep/webgl-shaders.md` |
| SDF 2D Shapes | Circles, boxes, rings in shaders | `grep -A 50 "### 5.3 SDF 2D" references/deep/webgl-shaders.md` |
| Color Grading | Levels, curves, hue shift | `grep -A 40 "### 5.4 Color Grading" references/deep/webgl-shaders.md` |
| Film Grain + Vignette + CA | Post-process atmosphere | `grep -A 50 "### 5.5 Film Grain" references/deep/webgl-shaders.md` |

## Canvas 2D Patterns

| Pattern | Use For | Grep Target |
|---|---|---|
| Metaballs | Organic blob animations | `grep -A 110 "### Metaballs Complete" references/deep/webgl-shaders.md` |
| Procedural Particle Trails | Flowing particle systems | `grep -A 70 "### Procedural Particle Trails" references/deep/webgl-shaders.md` |

## SVG Effects

| Effect | Library | Grep Target |
|---|---|---|
| Shape Morphing | Flubber.js (free) or GSAP MorphSVG | `grep -A 30 "### 7.1 Flubber" references/deep/webgl-shaders.md` |
| Line Drawing Reveal | CSS `stroke-dashoffset` | `grep -A 45 "### 7.3 Stroke-Dashoffset" references/deep/webgl-shaders.md` |
| Turbulence Displacement | SVG `feTurbulence` + `feDisplacementMap` | `grep -A 40 "### 7.4 feTurbulence" references/deep/webgl-shaders.md` |
| Animated Clip-Path | CSS `clip-path` transitions | `grep -A 40 "### 7.5 Animated Clip-Path" references/deep/webgl-shaders.md` |

## Performance Budgets

### Desktop (60 FPS target)
- Particles: ≤50k, Draw calls: ≤100, Texture memory: ≤256MB
- Triangle count: ≤1M, Shader complexity: Medium-high OK

### Mobile (30-60 FPS target)
- Particles: ≤5k, Draw calls: ≤50, Texture memory: ≤64MB
- Triangle count: ≤100k, Shader complexity: Simple only
- **Always:** `devicePixelRatio` capped at 2, adaptive quality based on FPS monitoring

### Mobile Detection Pattern
```javascript
const isMobile = /Mobi|Android/i.test(navigator.userAgent) || window.innerWidth < 768;
const isLowEnd = navigator.hardwareConcurrency <= 4 || navigator.deviceMemory <= 4;
```

⤷ Full performance strategy + FPS monitoring: `grep -A 50 "### FPS Monitoring" references/deep/webgl-shaders.md`
