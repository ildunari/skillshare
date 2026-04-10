---
title: Use CSS linear() for Spring Approximations
impact: MEDIUM
impactDescription: CSS linear() easing (Baseline 2024) enables spring-like motion without JavaScript, reducing dependency on animation libraries for simple interactions.
tags: css, spring, linear-easing, performance
---

## Use CSS linear() for Spring Approximations

CSS `linear()` creates piecewise-linear timing functions that approximate springs, bounces, and elastic curves without JS. Baseline support: Chrome 113+, Safari 17.2+, Firefox 112+.

**Incorrect (JS library just for spring easing):**

```tsx
// Loading Framer Motion just for a button press spring
import { motion } from "framer-motion";
<motion.button whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 450, damping: 40 }} />
```

**Correct (CSS spring preset for simple interactions):**

```css
:root {
  --spring-snappy: linear(
    0, 0.079, 0.24, 0.413, 0.567, 0.692, 0.787, 0.857,
    0.906, 0.94, 0.962, 0.977, 0.986, 0.992, 0.996, 0.998,
    0.999, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
  );
  --spring-snappy-dur: 520ms;
}

.button:active {
  transform: scale(0.97);
  transition: transform var(--spring-snappy-dur) var(--spring-snappy);
}
```

Use JS springs (Framer Motion, GSAP) when you need interruptibility, gesture velocity preservation, or complex orchestration. CSS `linear()` is for standalone spring-feel transitions.

Reference: `references/css-native.md`
