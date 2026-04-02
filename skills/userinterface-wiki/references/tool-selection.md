# Animation Tool Selection Engine

> Decision trees, support matrices, licensing, and the practitioner heuristics that determine which animation approach to use. This is the most important file in the skill — read it before recommending any animation approach.

---

## The Ecosystem in Early 2026

### GSAP — free, orchestration powerhouse
Webflow acquired GSAP in Oct 2024. As of April 30, 2025, GSAP is **100% free to all users** — including formerly paid plugins (ScrollTrigger, Flip, SplitText, DrawSVG, MorphSVG, MotionPath, Draggable, Observer). Any reference treating GSAP as cost-prohibitive is outdated.

### Motion (formerly Framer Motion) — no longer React-only
In Nov 2024, Framer Motion became independent as **Motion** (motion.dev). It now includes vanilla JS APIs alongside the React API. Any heuristic treating it as "React-only" is outdated. In Claude React artifacts, import from `"framer-motion"` (the older package name works and is what's bundled).

### CSS-native — the boundary moved significantly
`@starting-style` (Baseline 2024), `interpolate-size`, scroll-driven animations, view transitions (Baseline Oct 2025), and CSS `linear()` easing collectively eat categories of work that used to require JS. The platform absorbed IntersectionObserver-triggered reveals, smooth height animation, and same-document shared-element transitions.

### WAAPI — hybrid engine era
Motion has been using WAAPI under the hood for hardware-accelerated values for ~2 years (as of 2024). This introduces a new class of driver-specific bugs (opacity in ScrollTimeline, autoplay: false semantics drift). Feature detection ≠ feature correctness.

---

## Decision Trees

### By motion role

```
CONTINUITY (preserve identity across state changes)
├── Same-document view/route change
│   ├── Browser support OK → View Transitions API
│   └── Cross-browser needed → GSAP Flip + custom transition hooks
├── Within-page shared element
│   ├── React artifact → Framer Motion layoutId
│   └── Vanilla → GSAP Flip.getState() / Flip.from()
└── Card → modal morph
    ├── React → Framer Motion layoutId + AnimatePresence
    └── Vanilla → GSAP Flip (measure before, animate after)

FEEDBACK (confirm user action)
├── Button press / toggle
│   ├── Simple → CSS transition (transform + opacity)
│   └── Spring feel needed
│       ├── React → Framer Motion spring
│       └── Vanilla → CSS linear() spring preset or WAAPI
├── Ripple / particle burst
│   └── WAAPI Element.animate() (lightweight, no library)
└── Form validation shake
    └── CSS keyframe (simple, no JS needed)

NARRATIVE (guide attention through content)
├── Scroll-linked (progress = scroll position)
│   ├── Can gate behind @supports → CSS scroll-driven animations
│   ├── Cross-browser required → GSAP ScrollTrigger (scrub mode)
│   └── Lightweight vanilla → WAAPI + ScrollTimeline polyfill
├── Scroll-triggered (fire once on entry)
│   ├── React → Framer Motion whileInView
│   ├── Staggered groups → GSAP ScrollTrigger.batch()
│   └── Simple → IntersectionObserver + CSS class toggle
├── Choreographed sequence (multi-element, timed)
│   └── GSAP timeline (labels, position params, callbacks)
└── Storytelling (pin + scrub + reveal)
    └── GSAP ScrollTrigger (pin, scrub, snap)

ORNAMENT (ambient polish)
├── Auto-playing loops (shimmer, float, pulse)
│   └── CSS @keyframes (no JS needed, compositor-friendly)
├── Mesh gradient / ambient background
│   └── CSS @keyframes on transform (move blurred blobs)
├── Shader background (noise, domain warp, flow fields)
│   ├── Simple effect → Raw WebGL2 or Regl (fullscreen quad, zero overhead)
│   └── Needs post-processing → Three.js ShaderMaterial
├── Generative vector art (mandalas, organic compositions)
│   └── Paper.js (retained scene graph, boolean path ops, hit testing)
├── High-count 2D particles / sprites
│   └── PIXI.js (GPU-accelerated, additive blending)
├── Marquee
│   └── CSS @keyframes translateX (duplicate content for seamless loop)
└── Pointer-following effects (spotlight, tilt, magnetic)
    └── JS pointer events → CSS custom properties (no pure CSS path)
```

### By artifact environment

```
CLAUDE REACT ARTIFACT
├── Framer Motion is built in — use it freely
│   ├── motion.div, AnimatePresence, layoutId, variants
│   ├── useMotionValue, useSpring, useTransform (no re-renders)
│   └── whileHover, whileTap, whileInView, drag
├── CSS-native for simple cases (fewer bytes, no imports)
└── WAAPI for non-React-managed DOM elements

CLAUDE HTML ARTIFACT
├── CSS-native preferred (zero dependencies)
├── GSAP via cdnjs CDN when orchestration needed
├── WAAPI for vanilla imperative animation
├── Anime.js via jsdelivr CDN for lightweight timeline alternative
├── Three.js r128 via cdnjs for 3D scenes / shader materials
├── Regl via cdnjs for zero-overhead fullscreen shaders
├── Paper.js via cdnjs for vector art / interactive 2D graphics
└── PIXI.js v7 via cdnjs for GPU-accelerated 2D sprites / particles

FULL PROJECT (npm/bundler)
├── Everything available — choose by motion role
├── Tree-shake: import only what you use
└── Consider bundle impact (GSAP ~50KB, Motion ~25KB mini)
```

---

## Tool Comparison Matrix

| Capability | CSS-native | WAAPI | Framer Motion | GSAP | Anime.js v4 |
|---|---|---|---|---|---|
| Entry/exit | `@starting-style` ✓ | Manual ✓ | `AnimatePresence` ✓✓ | `from()`/timelines ✓ | `animate()` ✓ |
| Scroll-linked | `animation-timeline` ✓✓ | ScrollTimeline ✓ | `useScroll` ✓ | ScrollTrigger ✓✓ | `onScroll` sync ✓ |
| Scroll-triggered | Chrome 145+ ✓ | IntersectionObserver | `whileInView` ✓ | `ScrollTrigger.batch` ✓✓ | `onScroll` ✓ |
| Timeline orchestration | Limited | Promises only | Variants/stagger ✓ | Labels/position ✓✓✓ | `createTimeline` ✓✓ |
| Springs/physics | `linear()` approx | Manual | Built-in ✓✓✓ | With plugin ✓ | `spring()` ✓ |
| Interruptible | Transitions ✓ | Cancel/reverse ✓ | Built-in ✓✓ | overwrite modes ✓ | Pause/reverse ✓ |
| Layout animation | `interpolate-size` | No | `layout` prop ✓✓ | Flip plugin ✓✓ | Layout API ✓ |
| SVG morphing | No | No | No | MorphSVG ✓✓ | `svg.morphTo` ✓ |
| SVG draw | Dashoffset hack | Dashoffset | No | DrawSVG ✓✓ | `createDrawable` ✓ |
| Motion path | `offset-path` ✓ | No | No | MotionPath ✓ | `createMotionPath` ✓ |
| Reduced motion | `@media` ✓ | Manual check | `useReducedMotion` ✓ | `matchMedia()` ✓ | Manual check |
| Artifact-ready | Always ✓✓ | Always ✓✓ | React only ✓ | CDN needed | CDN needed |
| Bundle size | 0 KB | 0 KB | ~25 KB (mini) | ~50 KB + plugins | ~18 KB |

✓ = capable, ✓✓ = strong, ✓✓✓ = best-in-class for this capability

---

## Rendering Engine Selection (Visual / GPU Animation)

When the motion role is **ornament** and exceeds what CSS can express, or when the task is generative art / interactive graphics, choose a rendering engine:

| Need | Engine | Why |
|---|---|---|
| Fullscreen shader only (no geometry) | Raw WebGL2 or Regl | Zero abstraction overhead, single quad |
| 3D scene with objects + lights | Three.js | Scene graph, materials, post-processing |
| 3D with PBR, physics, post-processing | Babylon.js | Heavier but more built-in capabilities |
| GPU-accelerated 2D sprites/particles | PIXI.js v7 | Display list, additive blending, sprite batching |
| Vector art, path ops, generative compositions | Paper.js | Retained scene graph, boolean operations, hit testing |
| Creative coding sketches | p5.js | Simplest API, immediate mode, learning-friendly |

### CDN compatibility for Claude artifacts

All of these have UMD builds on cdnjs or jsdelivr. ESM-only libraries (OGL, Theatre.js) won't work in artifact sandboxes. PIXI v7 uses a synchronous `new PIXI.Application({...})` constructor — the async `app.init()` pattern from v8 breaks in artifacts.

### "When NOT to reach for WebGL"

- If the effect is a gradient animation → CSS `@keyframes` + `@property`
- If the effect is a shimmer or glow → CSS `filter` + `@keyframes`
- If the effect is a simple particle field → CSS `@keyframes` on positioned divs (up to ~50 particles)
- If the effect is scroll-linked → CSS scroll-driven animations or GSAP ScrollTrigger
- WebGL adds a canvas element, GPU context, and resize handling overhead. Don't pay that cost for effects CSS handles natively.

---

## Licensing and Cost (2026)

| Tool | License | Cost | Notes |
|---|---|---|---|
| GSAP + all plugins | Custom (Webflow) | **Free** | Changed April 2025. All plugins including formerly paid ones. |
| Framer Motion / Motion | MIT | Free | Independent from Framer since Nov 2024 |
| Anime.js v4 | MIT | Free | ESM-first, modular |
| Lottie-web | MIT | Free | Runtime only; content creation needs After Effects or equivalent |
| dotlottie-web | MIT | Free | Wasm-based renderer, worker support |
| Rive | Freemium | Free runtime, paid editor | State machines are the differentiator |
| WAAPI | Platform | Free | Browser-native |
| CSS | Platform | Free | Browser-native |

---

## When NOT to use each tool

### Don't use GSAP when:
- A CSS transition handles it (hover/focus/expand)
- You're in a React artifact and Framer Motion covers the need (saves a CDN load)
- The effect is purely time-based with no choreography needs
- You need server-side rendering without DOM

### Don't use Framer Motion when:
- You're in an HTML (non-React) artifact
- You need SVG morphing, draw, or motion path (GSAP excels here)
- You need robust scroll pinning with spacer management (ScrollTrigger is more battle-tested)
- The animation is purely CSS-expressible (extra JS for no benefit)

### Don't use CSS-native scroll-driven when:
- Firefox support matters (disabled by default as of early 2026)
- You need scroll pinning with precise spacer/layout management
- The scroll effect requires runtime measurements or cross-element coordination
- You need it to work without @supports fallbacks

### Don't use WAAPI directly when:
- You need timeline orchestration (no native timeline beyond promise chaining)
- You need springs/physics (write your own or use a library)
- The app already has Framer Motion or GSAP loaded

### Don't use Lottie when:
- The animation is a simple UI transition (CSS/WAAPI is lighter)
- You need runtime interactivity beyond play/pause/seek (use Rive)
- You'd be running many concurrent instances (CPU/GPU pressure)
- The animation can be expressed as CSS keyframes

---

## Failure Triggers to Encode

These are documented production failures that should shape tool recommendations:

| Trigger | What breaks | Mitigation |
|---|---|---|
| CSS `scroll-behavior: smooth` + GSAP ScrollTrigger | Sluggish scrolling, refresh conflicts | Use GSAP ScrollTo instead of CSS smooth scroll |
| ScrollTrigger `once: true` + kill | Scroll jump from spacer removal | Keep ScrollTrigger alive or handle spacer compensation |
| Multiple pinned ScrollTriggers + resize | Overlap/interference between triggers | Test resize explicitly; don't trust "auto refresh" |
| `window.ScrollTimeline` existence check | Safari/Firefox opacity bugs (Feb 2026) | Robust feature detection, not just existence |
| WAAPI `autoplay: false` + opacity | Animation plays despite autoplay:false | Known Motion issue (May 2025); test carefully |
| WAAPI `fill: "forwards"` without cleanup | Leaked animation objects, style conflicts | `commitStyles()` → `cancel()` pattern |
| GSAP `gsap.context()` nested inside `useGSAP()` | Double-scoping, confusing cleanup | `useGSAP()` already creates context; don't nest |
| React 18 StrictMode + GSAP without cleanup | Duplicate animations from double effect invocation | Always use `useGSAP()` or manual `context.revert()` |
| Lottie many concurrent instances | CPU/GPU pressure, jank | Limit instances; use dotLottie Worker renderer |
| View Transitions on hover | `mouseleave` fires because transition layer covers element | Known gotcha; avoid hover-triggered view transitions |

---

## Practitioner-Backed Heuristics

These aren't "best practices" from docs — they're patterns that survive production, extracted from GSAP forum threads, Motion GitHub issues, and Codrops/Awwwards case studies.

1. **Different motion problems have different optimal representations.** Timeline choreography (GSAP), authored vector playback (Lottie), physics simulation (springs), snapshot transitions (View Transitions). Don't force one tool to do everything.

2. **"What gets shared" and "what ships" are different filters.** A breathtaking demo might hide production constraints. A boring-looking production build might encode the patterns that survive resize, Safari, and real users.

3. **Excellence isn't maximal motion — it's controlled motion that earns attention.** The best 2025-2026 work explicitly pulls back animation so motion supports interaction without taking over.

4. **Motion that preserves identity across layout changes** (FLIP, view transitions, shared elements) is consistently the highest-signal pattern for "designed" feel.

5. **If text is important, don't split and animate it.** GSAP forum moderator guidance. Splitting text into character spans for animation hurts legibility and accessibility.

6. **Treat reduced motion as a design system, not a flag.** Replace, don't remove. Static equivalents for every motion pattern.
