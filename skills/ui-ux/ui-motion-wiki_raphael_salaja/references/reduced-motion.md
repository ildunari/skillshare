# Reduced Motion: A Parallel Design System

> Reduced motion isn't "disable all animation." It's a separate motion system with different communication priorities. Every animation pattern in this skill has a reduced-motion variant. This file defines the policy layer and canonical transformations.

---

## Core Philosophy

Serious motion practitioners treat `prefers-reduced-motion: reduce` as a design constraint that produces a different — but complete — experience. Motion that communicates meaning gets replaced with static equivalents. Motion that's purely ornamental gets removed.

WCAG 2.2 "Animation from Interactions" (2.3.3) is explicit: avoid unnecessary animation, provide controls to disable non-essential animation, or honor system reduce-motion preferences. Parallax, scroll-driven camera moves, and auto-scrolling content are specifically cited as vestibular triggers.

**Key principle: "reduced" ≠ "none."** Small, supportive animations can still improve comprehension — short opacity fades, subtle state changes. The line is: does this motion risk triggering vestibular harm, or is it genuinely helpful for understanding?

---

## Shared Detection Primitives

### CSS

```css
@media (prefers-reduced-motion: reduce) {
  :root { scroll-behavior: auto; }
  /* Pattern-specific overrides below */
}
```

### JavaScript

```js
function prefersReducedMotion() {
  return (
    typeof window !== "undefined" &&
    window.matchMedia?.("(prefers-reduced-motion: reduce)").matches
  );
}
```

### GSAP policy layer (recommended for GSAP codebases)

```js
const mm = gsap.matchMedia();

mm.add({
  full: "(prefers-reduced-motion: no-preference)",
  reduced: "(prefers-reduced-motion: reduce)"
}, (context) => {
  const { reduced } = context.conditions;

  if (reduced) {
    // Set end states immediately, no animation
    gsap.set(".hero", { opacity: 1, y: 0 });
    gsap.set(".reveal-item", { opacity: 1, y: 0 });
    // Kill any ScrollTrigger-based scrubbing/pinning
    ScrollTrigger.getAll().forEach(st => st.kill(true));
    return;
  }

  // Full animation code here
});
```

### Framer Motion (React)

```jsx
import { useReducedMotion } from "framer-motion";

function Component() {
  const shouldReduce = useReducedMotion();

  return (
    <motion.div
      initial={shouldReduce ? false : { opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={shouldReduce ? { duration: 0 } : { type: "spring" }}
    />
  );
}
```

---

## Canonical Pattern Transformations

Every motion pattern maps to a reduced-motion equivalent. These are deterministic — apply them consistently.

| Full motion pattern | Reduced motion equivalent | Why |
|---|---|---|
| **Crossfade page transition** | Instant switch or ≤100ms opacity-only | Spatial movement causes vestibular response |
| **Shared element morph** | Crossfade old/new at rest positions (no position interpolation) | Eliminate spatial tracking |
| **Stagger reveals** | All items appear together, short opacity fade or instant | Remove sequential movement |
| **Scroll parallax** | Static positions, `animation: none`, kill ScrollTriggers | Parallax explicitly cited as vestibular trigger |
| **Auto-scrolling marquee** | Pause animation, provide manual controls | Non-essential autoplay motion |
| **Swipe gesture navigation** | Provide button-based alternative, keep swipe optional | Motion shouldn't be required for navigation |
| **Typewriter effect** | Render full text immediately | Remove per-character sequential reveal |
| **Character stagger** | Show full text instantly | Same — eliminate sequential motion |
| **Magnetic / cursor-tracking** | Hover-only state change (no tracking movement) | Remove continuous positional motion |
| **Particle effects** | Scale-only or color-only feedback | Remove spatial explosion |
| **Spring overshoot** | Linear ease, short duration | Remove bouncing/oscillation |
| **Zoom parallax** | Static scale, no scroll-linked zoom | Zoom movement is vestibular trigger |
| **Horizontal scroll hijack** | Native horizontal overflow with optional snap | Remove scroll direction takeover |
| **Sticky pin + scrub** | Normal scroll, no pinning | Remove scroll-locked sequences |
| **Mesh gradient background** | Static gradient, no animation | Remove ambient continuous motion |
| **Foil/holographic shimmer** | Static gradient, no panning | Remove continuous motion |
| **Goo/blob merging** | Static shapes, filter removed | Remove continuous animation + heavy filter |
| **Ripple click** | Short opacity pulse or no ripple | Reduce to minimal feedback |
| **Kinetic marquee** | Static text, no translation | Remove auto-scrolling |
| **Gradient border rotation** | Static gradient, no spin | Remove continuous rotation |

---

## Implementation Templates

### CSS entry animation with reduced-motion

```css
.reveal {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 400ms ease, transform 400ms ease;
}

.reveal.in-view {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .reveal {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

### WAAPI with reduced-motion branch

```js
function animateReveal(el) {
  if (prefersReducedMotion()) {
    el.style.opacity = "1";
    el.style.transform = "none";
    return null;
  }

  return el.animate(
    [
      { opacity: 0, transform: "translateY(16px)" },
      { opacity: 1, transform: "translateY(0)" }
    ],
    { duration: 400, easing: "ease-out", fill: "both" }
  );
}
```

### ScrollTrigger with reduced-motion kill

```js
if (prefersReducedMotion()) {
  // Show all content in final state
  gsap.set(".reveal-item", { opacity: 1, y: 0 });
  // Don't create any ScrollTriggers
} else {
  ScrollTrigger.batch(".reveal-item", {
    start: "top 85%",
    onEnter: (batch) => gsap.to(batch, {
      opacity: 1, y: 0, stagger: 0.06
    })
  });
}
```

### CSS scroll-driven with reduced-motion

```css
@supports (animation-timeline: view()) {
  .reveal {
    animation: fadeIn linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .reveal {
    animation: none !important;
    opacity: 1;
    transform: none;
  }
}
```

---

## Failure Modes Practitioners Warn About

### "One-size-fits-all disable" breaks state
If animations were performing state-setting work (e.g., `gsap.set()` calls, layout prep inside timelines), globally zeroing durations or killing animations can break the UI state. Use structured condition layers (GSAP `matchMedia`, Framer `useReducedMotion`) that set end states correctly.

### Reduced motion must be testable
Use DevTools > Rendering > "Emulate prefers-reduced-motion: reduce" to verify behavior. Don't ship without testing the reduced path.

### Adoption remains inconsistent
The 2025 Web Almanac reports `prefers-reduced-motion` media query usage shows little change — many production sites still don't implement it. That's not an excuse; it's context for why this matters more, not less.

### Don't animate "important text" by default
GSAP forum moderator guidance: if text is important, don't split and animate it. This is both a legibility concern and an accessibility one. The reduced-motion version should always be "full text visible" — but consider whether the full-motion version should also limit text animation to decorative elements.

---

## Interaction Between Reduced Motion and Other Features

- **`scroll-behavior: smooth`** — reset to `auto` under reduced motion. Smooth scrolling is itself a motion preference.
- **View transitions** — still function under reduced motion, but CSS should set `::view-transition-old` and `::view-transition-new` animations to `none` or opacity-only.
- **`@starting-style`** — entry transitions still work but should be shortened to ≤100ms opacity-only under reduced motion.
- **Lottie/Rive** — set `autoplay: false`, show static frame. State machine inputs can still change states without animated transitions.
