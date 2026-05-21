---
title: WAAPI commitStyles then cancel Pattern
impact: HIGH
impactDescription: fill:forwards leaks animation objects that hold styles, causing memory pressure and style conflicts across multiple animations.
tags: waapi, cleanup, memory-leak, fill-forwards
---

## WAAPI commitStyles then cancel Pattern

After a WAAPI animation finishes, `fill: "forwards"` keeps the animation object alive holding styles. Multiple animations accumulate, causing conflicts and memory pressure. Use `commitStyles()` → `cancel()` instead.

**Incorrect (fill: forwards leaks):**

```js
el.animate(
  [{ transform: "translateY(0)" }, { transform: "translateY(100px)" }],
  { duration: 300, fill: "forwards" }
);
// Animation object stays alive, holding computed styles
```

**Correct (commit then cancel):**

```js
const anim = el.animate(
  [{ transform: "translateY(0)" }, { transform: "translateY(100px)" }],
  { duration: 300, fill: "both" }
);

anim.finished
  .catch(() => {}) // cancel() rejects .finished
  .finally(() => {
    anim.commitStyles(); // persist final styles as inline
    anim.cancel();       // remove the animation player
  });
```

Reference: `references/waapi-motion.md`
