---
title: Never Put Motion Values in useEffect Dependencies
impact: HIGH
impactDescription: Motion values update without React re-renders — putting them in useEffect dependency arrays causes infinite re-render loops.
tags: framer-motion, hooks, motion-values, react
---

## Never Put Motion Values in useEffect Dependencies

Framer Motion motion values (`useMotionValue`, `useSpring`, `useTransform`) update outside React's render cycle. Putting them in `useEffect` dependency arrays triggers infinite loops.

**Incorrect (infinite re-render loop):**

```tsx
const x = useMotionValue(0);

useEffect(() => {
  console.log("x changed:", x.get());
}, [x]); // Infinite loop — x is a stable reference but triggers effects
```

**Correct (use .on("change") listener):**

```tsx
const x = useMotionValue(0);

useEffect(() => {
  const unsubscribe = x.on("change", (latest) => {
    console.log("x changed:", latest);
  });
  return unsubscribe;
}, []); // Empty deps — subscribe once
```

Reference: `references/framer-motion.md`
