---
title: Clean Up Animation Resources
impact: HIGH
impactDescription: Leaked animations are production bugs — they cause memory pressure, style conflicts, and duplicate animations on re-mount.
tags: cleanup, gsap, waapi, react, memory-leak
---

## Clean Up Animation Resources

GSAP contexts need `revert()`. WAAPI animations need `cancel()` after `commitStyles()`. ScrollTriggers need `kill()`. React effects need cleanup returns. Leaked animations are production bugs.

**Incorrect (no cleanup):**

```tsx
// React: GSAP without cleanup
useEffect(() => {
  gsap.from(".item", { y: 12, opacity: 0, stagger: 0.06 });
}, []);

// Vanilla: WAAPI with fill: forwards (leaks animation object)
el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, fill: "forwards" });
```

**Correct (proper cleanup):**

```tsx
// React: useGSAP handles cleanup automatically
useGSAP(() => {
  gsap.from(".item", { y: 12, opacity: 0, stagger: 0.06 });
}, { scope: containerRef });

// Vanilla: commitStyles + cancel pattern
const anim = el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, fill: "both" });
anim.finished.catch(() => {}).finally(() => {
  anim.commitStyles();
  anim.cancel();
});
```

Reference: `references/gsap-production.md`, `references/waapi-motion.md`
