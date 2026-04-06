---
name: ui-motion-wiki
description: "Production UI motion, interaction, and animation best practices for web interfaces. Use when implementing or reviewing animations (CSS, GSAP, Framer Motion, WAAPI, Anime.js), choosing animation tools, scroll-driven effects, view transitions, FLIP layout animation, spring physics, exit animations, reduced-motion accessibility, audio feedback, motion-aware typography, or interactive visual effects."
license: MIT
metadata:
  author: raphael-salaja
  version: "4.0.0"
---

# UI Motion Wiki

Production UI/UX best practices and animation pipeline for web interfaces. 175 rule files across 18 categories plus 14 deep reference files covering every major animation tool and technique.

## Always-On Rules

> These six principles apply to every animation task. Individual rule files in `rules/` expand each with code examples.

1. **CSS-first when CSS can express the intent.** Entry/exit (`@starting-style`), scroll-linked (scroll timelines), view transitions, intrinsic size animation, and spring approximations (`linear()`) are all CSS-native now. Reach for JS only when you need runtime input, cross-browser parity, or orchestration CSS can't express.
2. **Match animation tool to motion role.** Continuity (FLIP, view transitions), Feedback (springs, CSS transitions), Narrative (GSAP timelines, scroll-driven), Ornament (CSS keyframes, shaders). Don't force one tool to do everything.
3. **Reduced motion is a parallel design system.** Never just zero durations or kill animations. Replace motion with static equivalents that preserve meaning.
4. **Animate compositor-friendly properties.** `transform` and `opacity` are the fast path. Layout properties trigger reflow — avoid unless using `interpolate-size` or FLIP.
5. **Clean up after yourself.** GSAP contexts need `revert()`. WAAPI animations need `cancel()` after `commitStyles()`. ScrollTriggers need `kill()`. React effects need cleanup returns.
6. **Feature-detect, don't assume.** API existence ≠ correctness. Use `@supports` for CSS, robust detection for JS, and always have a fallback path.

---

## Feedback Loop

Read `FEEDBACK.md` when loading this skill to apply lessons from prior use. During use, if an animation pattern fails or a reference is outdated, propose a FEEDBACK.md entry.

---

## Rules

175 rule files across 18 categories, prioritized by impact. Each file in `rules/` has incorrect vs. correct code examples.

For the full rule listing: `references/rule-index.md`

| Priority | Category | Impact | Prefixes |
|----------|----------|--------|----------|
| 1 | Tool Selection & Motion Roles | CRITICAL | `tool-` |
| 2 | Animation Principles | CRITICAL | `timing-`, `physics-`, `staging-` |
| 3 | Reduced Motion Policy | CRITICAL | `a11y-reduced-motion-` |
| 4 | Timing Functions | HIGH | `spring-`, `easing-`, `duration-`, `none-` |
| 5 | CSS-Native Modern Animation | HIGH | `css-` |
| 6 | Exit Animations | HIGH | `exit-`, `presence-`, `mode-`, `nested-` |
| 7 | FLIP & Layout Animation | HIGH | `flip-`, `fm-layout-`, `view-transitions-` |
| 8 | Library Production Patterns | HIGH | `gsap-`, `fm-`, `waapi-` |
| 9 | Practitioner Knowledge | HIGH | `practitioner-` |
| 10 | Laws of UX | HIGH | `ux-` |
| 11 | Visual Design | HIGH | `visual-` |
| 12 | CSS Pseudo Elements | MEDIUM | `pseudo-`, `transition-`, `native-` |
| 13 | Audio Feedback | MEDIUM | `appropriate-`, `impl-`, `weight-` |
| 14 | Sound Synthesis | MEDIUM | `context-`, `envelope-`, `design-`, `param-` |
| 15 | Container Animation | MEDIUM | `container-` |
| 16 | Predictive Prefetching | MEDIUM | `prefetch-` |
| 17 | Typography | MEDIUM | `type-` |
| 18 | Morphing Icons | LOW | `morphing-` |

---

## Deep Reference Files

Production patterns, full API guides, and code recipes beyond what rules capture. Load the relevant files based on the task.

| Task | Load these references |
|------|----------------------|
| **Choosing an animation approach** | `references/tool-selection.md` |
| **CSS entry/exit, scroll-driven, view transitions, `linear()`, `@property`** | `references/css-native.md` |
| **Framer Motion: variants, AnimatePresence, layout, gestures, springs, hooks** | `references/framer-motion.md` |
| **GSAP: timelines, ScrollTrigger, Flip, React integration** | `references/gsap-production.md` |
| **WAAPI vanilla, Motion One, Motion mini** | `references/waapi-motion.md` |
| **Anime.js v4 patterns, v3→v4 migration** | `references/anime-v4.md` |
| **Lottie, dotLottie, Rive integration** | `references/lottie-rive.md` |
| **FLIP technique: manual, GSAP Flip, Framer Motion layout** | `references/flip-technique.md` |
| **Three.js/WebGL: shader backgrounds, uniform animation, DOM integration** | `references/threejs-webgl.md` |
| **Paper.js: vector animation, generative art, path operations** | `references/paperjs.md` |
| **Reduced motion policy, pattern-by-pattern mappings** | `references/reduced-motion.md` |
| **Visual effect recipes (foil, goo, gradient borders, particles, marquee)** | `references/pattern-recipes.md` |
| **Ecosystem wisdom, failure triggers, production gotchas** | `references/practitioner-knowledge.md` |
| **Full rule listing by category** | `references/rule-index.md` |

---

## Decision Engine (Quick Path)

For the full decision tree with browser support matrix, read `references/tool-selection.md`.

**Entry/exit animation** → CSS `@starting-style` (Baseline 2024) or Framer Motion `AnimatePresence`
**Scroll-linked** → CSS `animation-timeline: scroll()/view()` with `@supports` gate, or GSAP ScrollTrigger
**Page/view transitions** → View Transitions API (Baseline Oct 2025) or Framer Motion `layoutId`
**Timeline choreography** → GSAP `gsap.timeline()` or Framer Motion variants with `staggerChildren`
**Accordion / height: auto** → CSS `interpolate-size: allow-keywords` or Framer Motion `animate={{ height: "auto" }}`
**Physics / spring / gesture** → Framer Motion springs (React), CSS `linear()` spring presets, GSAP inertia
**Layout change (FLIP)** → Framer Motion `layout`/`layoutId` (React), GSAP Flip (vanilla), View Transitions API
**Designer-authored assets** → Lottie/dotLottie (linear playback), Rive (stateful/interactive)
**Shader backgrounds** → Raw WebGL2/Regl (fullscreen quad), Three.js ShaderMaterial (3D)
**Generative vector art** → Paper.js (retained scene graph), p5.js (creative coding)

---

## Browser Support Quick Matrix (early 2026)

| Feature | Chrome/Edge | Safari | Firefox | Artifact-safe? |
|---------|-------------|--------|---------|----------------|
| `@starting-style` | 117+ | 17.4+ | 129+ | Yes (CSS) |
| `transition-behavior: allow-discrete` | 117+ | 17.4+ | 129+ | Yes (CSS) |
| `interpolate-size` | 129+ | 26+ | Not yet | Progressive enhancement |
| `animation-timeline: scroll()` | 115+ | 26+ | Disabled by default | `@supports` gate required |
| View Transitions (same-doc) | 111+ | 18+ | 144+ | Yes with detection |
| WAAPI core | All modern | All modern | All modern | Yes |
| CSS `linear()` easing | 113+ | 17.2+ | 112+ | Yes (CSS) |
| CSS `@property` | 85+ | 15.4+ | 128+ | Yes (Baseline 2024) |

---

## Artifact Environment Quick Reference

| Environment | Animation tools available |
|-------------|--------------------------|
| **React artifact** | Framer Motion (`import { motion } from "framer-motion"`), CSS, inline WAAPI |
| **HTML artifact** | CSS-native, WAAPI, GSAP via CDN, Anime.js via CDN, Lottie via CDN, Three.js/Regl/PIXI.js/Paper.js via CDN |
| **Full project** | Everything — npm imports, bundlers, tree shaking |

### CDN URLs for HTML artifacts

```html
<!-- GSAP + plugins (all free since April 2025) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/Flip.min.js"></script>

<!-- Anime.js v4 -->
<script src="https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.min.js"></script>

<!-- Lottie -->
<script src="https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web@latest/dist/dotlottie-player.js"></script>

<!-- Three.js r128 (last clean UMD build on cdnjs) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<!-- Paper.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/paper.js/0.12.18/paper-full.min.js"></script>

<!-- Regl (zero-overhead WebGL) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/regl/2.1.0/regl.min.js"></script>

<!-- PIXI.js v7 (GPU-accelerated 2D) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pixi.js/7.3.2/pixi.min.js"></script>
```
