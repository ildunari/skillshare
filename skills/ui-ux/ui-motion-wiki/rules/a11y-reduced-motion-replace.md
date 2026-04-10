---
title: Replace Motion with Static Equivalents Under Reduced Motion
impact: CRITICAL
impactDescription: Setting animation:none or duration:0 can break UI state when animations perform state-setting work. Replace, don't remove.
tags: accessibility, reduced-motion, a11y, design-system
---

## Replace Motion with Static Equivalents Under Reduced Motion

`prefers-reduced-motion: reduce` is not "disable all animation." It's a parallel design system. Motion that communicates meaning gets replaced with static equivalents. Motion that's purely ornamental gets removed. Small, supportive animations (short opacity fades) can still improve comprehension.

**Incorrect (blanket disable breaks state):**

```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

**Correct (per-pattern replacements):**

```css
/* Stagger reveals → all items appear together */
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
}

/* Parallax → static positions */
@media (prefers-reduced-motion: reduce) {
  .parallax-layer { animation: none; transform: none; }
}

/* Spring overshoot → linear ease, short duration */
@media (prefers-reduced-motion: reduce) {
  .spring-element { transition: transform 100ms linear !important; }
}

/* Scroll-driven → content always visible */
@media (prefers-reduced-motion: reduce) {
  .scroll-reveal { animation: none !important; opacity: 1; }
}
```

| Full motion | Reduced motion equivalent |
|------------|--------------------------|
| Crossfade transition | Instant switch or ≤100ms opacity-only |
| Shared element morph | Crossfade at rest positions |
| Stagger reveals | All items appear together |
| Scroll parallax | Static positions |
| Auto-scrolling marquee | Paused, manual controls |
| Spring overshoot | Linear ease, short duration |
| Particle effects | Scale-only or color-only feedback |

Reference: `references/reduced-motion.md`
