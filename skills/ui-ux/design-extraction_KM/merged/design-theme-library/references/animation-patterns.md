# Cross-Theme Animation Patterns

> Motion recipes organized by character, not by theme. Mix and match across themes. Every pattern includes a `prefers-reduced-motion` fallback.

## Motion Categories

### 1. Organic Motion
**Character:** Living, breathing, imperfect. Driven by noise, springs, and biological rhythms.
**Used by:** Alchemist's Journal, Anthropic Serenity, Bioluminescent Deep, Vapor Silk, Solarpunk Brass

| Pattern | Implementation | Easing | Reduced-Motion Fallback |
|---|---|---|---|
| **Breathing Scale** | `transform: scale()` oscillating via `sin(time * speed)` at 0.5-2% amplitude | Sine wave (continuous) | Static at scale(1) |
| **Drift** | Perlin noise displacement on x/y, 0.5-2px amplitude, 3-8s cycle | Noise-driven (no easing) | Static position |
| **Pulse Glow** | `box-shadow` spread oscillating via sine, or opacity 0.7→1.0→0.7 | `ease-in-out` | Static glow at midpoint |
| **Ink Spread** | Radial `scale(0)→scale(1)` with irregular edge via noise displacement SVG | `ease-out` 800ms | Instant appear, no scale |
| **Growth Unfurl** | `transform-origin: bottom-left`, scale + rotate from 0, spring easing | Spring: stiffness 120, damping 18 | Fade in 200ms |

**CSS Spring approximation:**
```css
.organic-spring { transition: transform 600ms cubic-bezier(0.34, 1.56, 0.64, 1); }
```

**JS noise drift (requestAnimationFrame):**
```javascript
// Perlin noise offset per frame
element.style.transform = `translate(${noise2D(id, time * 0.001) * 2}px, ${noise2D(id + 100, time * 0.001) * 2}px)`;
```

---

### 2. Mechanical Motion
**Character:** Precise, linear, utilitarian. No overshoot, no wobble. Machine-made.
**Used by:** Brutalist Concrete, Neon Noir, Crystalline Matrix

| Pattern | Implementation | Easing | Reduced-Motion Fallback |
|---|---|---|---|
| **Hard Cut** | `display: none→block` or `opacity: 0→1` in 0ms | None (instant) | Same (already minimal) |
| **Snap Rotate** | Exact angle increments (30°, 60°, 90°) with `steps(1)` timing | `steps(1)` or `linear` | Instant to final rotation |
| **Typewriter** | Character-by-character text reveal at fixed interval (20-40ms/char) | Linear interval | Full text appears instantly |
| **Scan Line** | Thin line (`height: 1px`) translates top→bottom via `transform: translateY()` | `linear` 3-5s | Hidden/removed |
| **Data Slot** | Numeric values cycle random digits before landing on final (100-200ms) | Linear per cycle | Instant final value |

**CSS scan line:**
```css
.scan-line {
  position: absolute; width: 100%; height: 1px;
  background: currentColor; opacity: 0.03;
  animation: scan 4s linear infinite;
}
@keyframes scan { from { transform: translateY(-100%); } to { transform: translateY(100vh); } }
```

---

### 3. Fluid Motion
**Character:** Smooth, continuous, silk-like. Long transitions, gentle curves, no stops.
**Used by:** Ethereal Porcelain, Vapor Silk, Opalescent Daydream, Liquid Glass

| Pattern | Implementation | Easing | Reduced-Motion Fallback |
|---|---|---|---|
| **Silk Wave** | Animated `background-position` on mesh gradient, 20-30s cycle | `linear` (continuous) | Static gradient |
| **Mist Fade** | `opacity: 0→1` + `filter: blur(2px)→blur(0)` combined, 600-1000ms | `ease-out` | Opacity only, 200ms |
| **Viscous Drag** | Element follows pointer/target with high lerp factor (0.05-0.1 per frame) | Frame-based lerp | Instant position |
| **Marble Pour** | Top-to-bottom fill reveal using `clip-path: inset(100% 0 0 0)→inset(0)` | `cubic-bezier(0.25, 0.1, 0.25, 1)` 1.2s | Instant appear |
| **Depth Parallax** | Multiple layers translate at different rates on scroll/mouse move | Proportional to input | Static (no parallax) |

**CSS mesh gradient animation:**
```css
.silk-bg {
  background: radial-gradient(at 20% 30%, var(--c1) 0%, transparent 60%),
              radial-gradient(at 80% 70%, var(--c2) 0%, transparent 60%),
              radial-gradient(at 50% 50%, var(--c3) 0%, transparent 60%);
  background-size: 200% 200%;
  animation: silk-drift 25s ease-in-out infinite alternate;
}
@keyframes silk-drift {
  0% { background-position: 0% 0%, 100% 100%, 50% 50%; }
  100% { background-position: 100% 100%, 0% 0%, 80% 20%; }
}
```

---

### 4. Luminous Motion
**Character:** Light-based. Glow, flicker, bloom, refraction. Darkness is the canvas.
**Used by:** Bioluminescent Deep, Neon Noir, Opalescent Daydream, Midnight Observatory

| Pattern | Implementation | Easing | Reduced-Motion Fallback |
|---|---|---|---|
| **Neon Flicker** | Rapid opacity toggling (0→1→0→1→1) over 200-400ms on entry | Stepped keyframes | Single fade-in 200ms |
| **Glow Bloom** | `box-shadow` spread animates from 0→12px→6px (settle) | Spring-like keyframes | Static glow at 6px |
| **Chromatic Split** | Element rendered 3x (R,G,B channels) with 2-3px offset, converging | `ease-out` 300ms | No split (single render) |
| **Star Twinkle** | Per-element opacity oscillation at random frequency (3-8s), phase-shifted | Sine wave (continuous) | Static opacity |
| **Additive Flash** | On collision/overlap, brief white flash via `background: white`, 100-200ms | `ease-out` | No flash |

**CSS neon flicker keyframes:**
```css
@keyframes neon-on {
  0%   { opacity: 0; }
  25%  { opacity: 1; }
  35%  { opacity: 0; }
  50%  { opacity: 1; }
  100% { opacity: 1; }
}
.neon-enter { animation: neon-on 300ms ease-out forwards; }
```

**JS star twinkle (Canvas):**
```javascript
// Per-particle: opacity = 0.7 + 0.3 * sin(time * particle.freq + particle.phase)
ctx.globalAlpha = 0.7 + 0.3 * Math.sin(performance.now() * 0.001 * p.freq + p.phase);
```

---

### 5. Physical Motion
**Character:** Tactile, material, gravity-aware. Paper, clay, craft. Things have weight.
**Used by:** Gouache & Clay, Paper Cut, Alchemist's Journal, Warm Darkroom

| Pattern | Implementation | Easing | Reduced-Motion Fallback |
|---|---|---|---|
| **Paper Stack** | Slide-in with hard shadow appearing simultaneously, from edge | Overshoot: `cubic-bezier(0.34, 1.56, 0.64, 1)` | Instant appear |
| **Fold/Unfold** | `perspective` + `rotateX` from 0→90° (fold) or reverse (unfold), origin at edge | `ease-in-out` 500ms | Fade out/in 200ms |
| **Stamp Press** | `scale(0.95)` + shadow offset reduces on `:active` | `ease` 100ms | No scale, color change only |
| **Shadow Lift** | Shadow offset grows on hover (4px→8px), creating levitation illusion | `ease-out` 200ms | Border highlight instead |
| **Tear Away** | Element exits with slight rotation (±5°) + acceleration off-screen | `ease-in` 300ms | Fade out 150ms |

**CSS paper fold:**
```css
.fold-exit {
  transform-origin: top center;
  animation: fold-down 500ms ease-in-out forwards;
}
@keyframes fold-down {
  0%   { transform: perspective(600px) rotateX(0deg); opacity: 1; }
  100% { transform: perspective(600px) rotateX(-90deg); opacity: 0; }
}
```

---

### 6. Data Motion
**Character:** Informational, purposeful. Every animation communicates a data change.
**Used by:** Midnight Observatory, Brutalist Concrete, Neon Noir, Solarpunk Brass, Crystalline Matrix

| Pattern | Implementation | Easing | Reduced-Motion Fallback |
|---|---|---|---|
| **Count Up** | Numeric interpolation from 0→target over 600-1000ms via `requestAnimationFrame` | `ease-out` | Instant final value |
| **Bar Growth** | `width` or `height` from 0→value%, using `transform: scaleX()` for performance | `ease-out` 400ms | Instant full width |
| **Connection Trace** | SVG line draws itself between data points via `stroke-dashoffset` | `ease-in-out` 800ms | Instant line |
| **Stagger Cascade** | Data elements enter sequentially, 40-80ms delay each | Per-element `ease-out` | All appear at once |
| **Value Highlight** | Changed values flash a background color (200ms) then fade back (400ms) | Sharp in, slow out | Bold text instead |

**JS count-up animation:**
```javascript
function countUp(el, target, duration = 800) {
  const start = performance.now();
  const initial = parseFloat(el.textContent) || 0;
  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3); // ease-out-cubic
    el.textContent = Math.round(initial + (target - initial) * eased);
    if (t < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
```

**CSS bar growth (performant):**
```css
.bar { transform: scaleX(0); transform-origin: left; transition: transform 400ms ease-out; }
.bar.active { transform: scaleX(1); }
```

---

## Reduced-Motion Master Rule

Wrap ALL motion in this media query. No exceptions across any theme:

```css
@media (prefers-reduced-motion: no-preference) {
  /* All animations here */
}
/* OR: disable all animations */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**For React (Framer Motion):**
```jsx
import { useReducedMotion } from 'framer-motion';
const shouldReduce = useReducedMotion();
const variants = shouldReduce ? {} : { initial: { opacity: 0 }, animate: { opacity: 1 } };
```

## Easing Quick Reference

| Name | Value | Character | Themes |
|---|---|---|---|
| Apple Spring | `cubic-bezier(0.2, 0.8, 0.2, 1)` | Responsive, slight bounce | Liquid Glass |
| Organic Spring | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Overshoot, handmade | Gouache & Clay, Paper Cut |
| Silk Smooth | `cubic-bezier(0.4, 0, 0.2, 1)` | Material Design feel | Vapor Silk |
| Editorial Ease | `cubic-bezier(0.22, 1, 0.36, 1)` | Ease-out-quint, editorial | Anthropic Serenity |
| Majestic | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Slow, heavy, sculpted | Ethereal Porcelain |
| Geometric | `cubic-bezier(0.5, 0, 0.5, 1)` | Symmetric, mathematical | Crystalline Matrix |
| Machine | `linear` | Precise, mechanical | Brutalist Concrete |
| Growth | `cubic-bezier(0.16, 1, 0.3, 1)` | Fast start, long settle | Solarpunk Brass |
| Electric | `cubic-bezier(0.65, 0, 0.35, 1)` | Sharp, decisive | Neon Noir |
| Chemical | `cubic-bezier(0.4, 0, 1, 1)` | Slow reveal, developing | Warm Darkroom |
