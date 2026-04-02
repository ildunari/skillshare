# GSAP Production Reference

> Timeline orchestration, ScrollTrigger, Flip, React integration, and the practitioner-documented failure modes you won't find in tutorials.

## Contents
- When to Use → Core API (to/from/fromTo, timelines, staggers)
- ScrollTrigger: scrub+pin, batch reveal, horizontal scroll
- Flip Plugin: layout animation (measure → mutate → animate)
- React Integration: useGSAP(), contextSafe, critical mistakes
- matchMedia(): responsive + reduced motion → Documented Failure Modes
- Plugin Quick Reference → CDN Setup

---

## When to Use GSAP

Use GSAP when you need: deterministic sequencing across many targets (timelines/labels), robust scroll-driven effects (ScrollTrigger), layout-change animation (Flip), SVG tooling (DrawSVG/MorphSVG/MotionPath), or cross-input gesture plumbing (Observer/Draggable). All plugins are **free** as of April 2025.

## Core API

### `gsap.to()` / `gsap.from()` / `gsap.fromTo()`
- `to()` — animate from current computed values to specified end state. Best default for interaction-driven updates.
- `from()` — set starting state immediately, animate to current DOM layout. Useful for "enter" effects where DOM is already in natural position.
- `fromTo()` — both ends explicit. Use when start values shouldn't be read from DOM, or when repeated plays must begin from known baseline.

### Timelines
```js
const tl = gsap.timeline({
  defaults: { duration: 0.5, ease: "power2.out" }
});

tl.from(".title", { y: 24, opacity: 0 })
  .from(".subtitle", { y: 16, opacity: 0 }, "-=0.3")  // position parameter
  .addLabel("contentReady")
  .from(".card", { y: 20, opacity: 0, stagger: 0.08 }, "contentReady")
  .from(".cta", { scale: 0.9, opacity: 0 }, "contentReady+=0.2");
```

Position parameters: `"<"` (start of previous), `"-=0.3"` (0.3s before end of previous), `"contentReady"` (at label), `"contentReady+=0.2"` (0.2s after label).

### Staggers
```js
// Simple
gsap.from(".item", { y: 12, opacity: 0, stagger: 0.06 });

// Rich object form
gsap.from(".grid-item", {
  y: 12, opacity: 0,
  stagger: {
    each: 0.04,
    from: "center",   // "start", "end", "center", "edges", or index
    grid: [4, 6],      // row × col for grid-aware stagger
    axis: "x",         // stagger along x axis of grid
    ease: "power2.in"
  }
});
```

---

## ScrollTrigger Production Patterns

### Scrubbed hero with pin

```js
gsap.registerPlugin(ScrollTrigger);

const heroTl = gsap.timeline({
  scrollTrigger: {
    trigger: ".hero",
    start: "top top",
    end: "+=1200",
    scrub: 0.6,           // smooth scrubbing (higher = smoother but laggier)
    pin: true,
    anticipatePin: 1,      // prevents jump on pin start
    invalidateOnRefresh: true, // recalculate on resize
  }
});

heroTl
  .to(".hero-title", { scale: 0.9, opacity: 0.5, duration: 1, ease: "none" }, 0)
  .to(".hero-bg", { y: -80, duration: 1, ease: "none" }, 0);
```

### Batch reveal (performant list/grid)

```js
ScrollTrigger.batch(".reveal-item", {
  start: "top 85%",
  onEnter: (batch) => gsap.to(batch, {
    opacity: 1, y: 0,
    duration: 0.6, ease: "power2.out",
    stagger: { each: 0.06, from: "start" },
    overwrite: "auto"
  }),
  onLeaveBack: (batch) => gsap.to(batch, {
    opacity: 0, y: 16,
    duration: 0.3, ease: "power1.out",
    overwrite: "auto"
  }),
});
```

### Horizontal scroll driven by vertical scroll

```js
const panels = gsap.utils.toArray(".panel");

gsap.to(".panels-container", {
  xPercent: -100 * (panels.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".panels-wrapper",
    start: "top top",
    end: () => `+=${window.innerWidth * panels.length}`,
    scrub: 1,
    pin: true,
    pinSpacing: true,
    invalidateOnRefresh: true,
    snap: {
      snapTo: 1 / (panels.length - 1),
      duration: { min: 0.1, max: 0.3 },
      ease: "power1.inOut"
    }
  }
});
```

---

## Flip Plugin (Layout Animation)

GSAP Flip measures before/after layout states and animates the difference using transforms. More general than Framer Motion's `layoutId` — works in vanilla JS, not React-only.

```js
gsap.registerPlugin(Flip);

// 1. Capture current state
const state = Flip.getState(".card, .container");

// 2. Make DOM/layout changes
container.classList.toggle("grid-view");

// 3. Animate from old state to new
Flip.from(state, {
  duration: 0.6,
  ease: "power2.inOut",
  stagger: 0.04,
  absolute: true,     // prevent layout shifts during animation
  onComplete: cleanup
});
```

---

## React Integration: The Rules

### Use `useGSAP()` — not `useEffect()`

`useGSAP()` creates a GSAP context automatically, handles cleanup on unmount, and scopes selectors.

```jsx
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

function Component() {
  const containerRef = useRef(null);

  const { contextSafe } = useGSAP(() => {
    // Animations created here are auto-scoped and auto-cleaned
    gsap.from(".item", { y: 12, opacity: 0, stagger: 0.06 });
  }, { scope: containerRef }); // ".item" → containerRef.querySelectorAll(".item")

  // Event handlers that create animations MUST use contextSafe
  const handleClick = contextSafe(() => {
    gsap.to(".panel", { height: 0, duration: 0.3 });
  });

  return (
    <div ref={containerRef}>
      <div className="item">A</div>
      <div className="item">B</div>
      <button onClick={handleClick}>Close</button>
    </div>
  );
}
```

### Critical mistakes to avoid

**Don't nest `gsap.context()` inside `useGSAP()`.**
`useGSAP()` already creates a context. Nesting another is "BAD" per GSAP maintainers — causes double-scoping and confusing cleanup.

**Don't use `addEventListener` for animation-triggering handlers in React.**
Use React's `onClick`/etc and wrap with `contextSafe`. This ensures animations are scoped to the correct context and cleaned up properly.

**React 18 StrictMode runs effects twice in dev.**
Without proper cleanup, this creates duplicate animations. `useGSAP()` handles this automatically. If using `useEffect`, return a cleanup that calls `context.revert()`.

**Scope prevents cross-component selector collisions.**
Without `scope: ref`, a selector like ".box" hits ALL `.box` elements in the entire document tree, not just the ones in your component.

---

## GSAP `matchMedia()` — Responsive Animation

```js
const mm = gsap.matchMedia();

mm.add({
  isDesktop: "(min-width: 768px)",
  isMobile: "(max-width: 767px)",
  reduceMotion: "(prefers-reduced-motion: reduce)"
}, (context) => {
  const { isDesktop, isMobile, reduceMotion } = context.conditions;

  if (reduceMotion) {
    gsap.set(".hero", { opacity: 1, y: 0 });
    return; // no animation
  }

  if (isDesktop) {
    gsap.from(".hero", { y: 40, opacity: 0, duration: 0.8 });
  } else {
    gsap.from(".hero", { y: 20, opacity: 0, duration: 0.5 });
  }

  // Return cleanup (optional — matchMedia handles context revert automatically)
  return () => { /* custom cleanup */ };
});
```

Animations registered inside `mm.add()` are automatically reverted when the media query stops matching. This is the recommended policy layer for reduced motion across a GSAP codebase.

---

## Documented Failure Modes

### CSS smooth-scrolling + ScrollTrigger conflict
**Problem:** `scroll-behavior: smooth` on `html` causes sluggishness and refresh weirdness when combined with ScrollTrigger. Effectively it's like putting a CSS transition on the same property GSAP is controlling.
**Fix:** Remove `scroll-behavior: smooth` from the page. Use GSAP's `ScrollTo` plugin for in-page anchor navigation instead.

### ScrollTrigger `once: true` leaves extra space
**Problem:** Using `once: true` causes the trigger to fire once, but the spacer/pin space remains. Killing the ScrollTrigger to remove the space causes a visible scroll jump.
**Fix:** This is genuinely complex. Options: (a) don't kill it — let the space remain; (b) animate the space removal gradually; (c) restructure so pinning isn't needed for one-shot effects.

### Multiple pinned triggers + resize breaks layout
**Problem:** Documentation says ScrollTrigger refreshes on resize. In practice, multiple pinned sections can overlap/interfere after resize. A production team reported significant debugging time for this.
**Fix:** Test resize explicitly as a first-class concern. Use `invalidateOnRefresh: true`. Consider debounced manual `ScrollTrigger.refresh()` after dynamic content changes. Don't trust "it auto-refreshes" without testing.

### `immediateRender` gotcha with `from()`
**Problem:** `gsap.from()` sets the starting state immediately by default. In ScrollTrigger contexts, this can flash the "from" state before the trigger fires.
**Fix:** Set `immediateRender: false` on ScrollTrigger-driven `from()` tweens, or use `fromTo()` for explicit control.

---

## Plugin Quick Reference

| Plugin | What it does | Key API |
|---|---|---|
| **ScrollTrigger** | Scroll-driven triggers, scrub, pin, batch, snap | `scrollTrigger: { trigger, start, end, scrub, pin }` |
| **Flip** | Layout-change animation (measure before/after) | `Flip.getState()`, `Flip.from()` |
| **SplitText** | Split text into chars/words/lines | `new SplitText(el, { type: "chars,words" })` |
| **DrawSVG** | Animate SVG stroke drawing | `drawSVG: "0%"` → `drawSVG: "100%"` |
| **MorphSVG** | Morph between SVG shapes | `morphSVG: "#targetPath"` |
| **MotionPath** | Animate along SVG path | `motionPath: { path: "#path", align: "#path" }` |
| **Draggable** | Drag interactions with bounds/snap | `Draggable.create(el, { bounds, snap })` |
| **Observer** | Unified wheel/touch/pointer/scroll input | `Observer.create({ onUp, onDown, onLeft })` |
| **matchMedia** | Responsive animation variants | `gsap.matchMedia().add("(query)", fn)` |
| **context** | Cleanup primitive for animation groups | `gsap.context(fn, scope)`, `ctx.revert()` |

---

## CDN Setup for HTML Artifacts

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/Flip.min.js"></script>
<!-- Add other plugins as needed -->
<script>
  gsap.registerPlugin(ScrollTrigger, Flip);
</script>
```

All plugins are free. No registration or license key needed.
