# Anime.js v4 Reference

> Modular, ESM-first animation engine. Lightweight alternative to GSAP for timeline choreography, SVG utilities, and scroll-driven effects.

---

## When to Use

Use Anime.js v4 when you want a compact, composable API (import only what you need), timeline toolchain, SVG utilities, and you're not invested in GSAP's plugin ecosystem. Smaller bundle than GSAP (~18KB vs ~50KB+).

---

## Core API (v4)

### `animate(targets, params)`
```js
import { animate, stagger } from "animejs";

animate(".card", {
  opacity: { from: 0, to: 1 },
  y: { from: 20, to: 0 },
  delay: stagger(60),
  duration: 500,
  ease: "out(3)"
});
```

### Keyframes
```js
// Duration-based array
animate(".el", {
  y: [0, -20, 0],
  duration: 600
});

// Percentage-based objects
animate(".el", {
  keyframes: [
    { y: 0, at: "0%" },
    { y: -20, at: "40%" },
    { y: 0, at: "100%" }
  ]
});
```

### Promises and async sequencing
```js
// v4 exposes .then() for async/await
await animate(".step1", { opacity: 1, duration: 300 });
await animate(".step2", { opacity: 1, duration: 300 });
```

### Timelines
```js
import { createTimeline, stagger } from "animejs";

const tl = createTimeline({ autoplay: false });

tl.add(".title", {
  opacity: { from: 0, to: 1 },
  y: { from: 12, to: 0 },
  duration: 500,
  ease: "out(3)"
}, 0);

tl.add(".card", {
  opacity: { from: 0, to: 1 },
  y: { from: 10, to: 0 },
  delay: stagger(70),
  duration: 420
}, 120); // offset in ms

tl.play();
tl.seek(500);
tl.pause();
tl.restart();
```

### Stagger
```js
import { stagger } from "animejs";

stagger(40);                          // simple delay
stagger(40, { from: "center" });      // from center outward
stagger(40, { grid: [4, 6], axis: "x" }); // grid-aware
stagger(40, { ease: "in(2)" });       // eased stagger
```

### Spring easing
```js
import { animate, spring } from "animejs";

animate(".el", {
  scale: 1.1,
  ease: spring()  // can override duration based on settling time
});
```

### Scroll Observer (`onScroll`)
```js
import { animate, onScroll } from "animejs";

// Trigger-based (play timeline on enter)
onScroll({
  target: document.querySelector("[data-feature]"),
  enter: "bottom 85%",
  leave: "top 0%",
  repeat: false,
  onEnter: () => tl.play()
});

// Sync mode (animation progress = scroll progress)
animate(".progress-bar", {
  scaleX: [0, 1],
  transformOrigin: ["0% 50%", "0% 50%"],
  autoplay: onScroll({
    container: document.documentElement,
    axis: "y",
    sync: true,
    enter: "top top",
    leave: "bottom bottom"
  })
});
```

### SVG Tools
```js
import { svg } from "animejs";

// Motion path
const motionPath = svg.createMotionPath("#myPath");
animate(".dot", { motionPath }, { duration: 2000 });

// SVG morphing
animate("#shape1", { d: svg.morphTo("#shape2") }, { duration: 800 });

// Line draw
const drawable = svg.createDrawable("#stroke-path");
animate(drawable, { draw: [0, 1] }, { duration: 1000 });
```

### SplitText
```js
import { splitText } from "animejs";

const split = splitText(".heading", { words: true });
animate(split.words, {
  opacity: { from: 0, to: 1 },
  y: { from: 12, to: 0 },
  delay: stagger(40),
  duration: 500
});
// split.revert() — restore original DOM
```

### Layout API
v4 documents auto-animation between layout states, including `display`, flex/grid, and DOM order changes.

---

## v3 → v4 Migration Gotchas

| v3 | v4 | Breaking? |
|---|---|---|
| `anime({ targets, ... })` | `animate(targets, params)` | Yes — different function name and signature |
| Default import `import anime from 'animejs'` | Named exports `import { animate } from 'animejs'` | Yes — ESM-first, modular |
| `loop: true` (total iterations) | `loop` defines repeats (semantic change) | Yes — check loop counts |
| Single bundle | Modular subpaths, tree-shakeable | API structure change |

---

## CDN Setup for HTML Artifacts

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.min.js"></script>
```

Check for latest v4 CDN availability — the package structure may evolve. The jsdelivr path should resolve the UMD/IIFE build.

---

## When NOT to Use

- When you need mature scroll pinning (GSAP ScrollTrigger is more battle-tested for complex pin scenarios)
- When you need gesture physics beyond basic spring (GSAP + inertia or Framer Motion are stronger)
- When platform-native primitives handle it (CSS transitions, scroll-driven animations)
- When Framer Motion is already available (React artifacts)
