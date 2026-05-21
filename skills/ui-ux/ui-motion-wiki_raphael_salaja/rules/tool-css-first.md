---
title: CSS-First Animation
impact: CRITICAL
impactDescription: Reaching for JS libraries when CSS handles the effect adds bundle weight, complexity, and potential jank for no benefit.
tags: tool-selection, css, performance
---

## CSS-First Animation

Prefer CSS-native animation when CSS can express the intent. Entry/exit (`@starting-style`), scroll-linked (scroll timelines), view transitions, intrinsic size animation, and spring approximations (`linear()`) are all CSS-native now. Reach for JS only when you need runtime input streams, cross-browser parity the platform can't deliver, or orchestration CSS can't express.

**Incorrect (JS library for a CSS-expressible effect):**

```tsx
// Unnecessary Framer Motion for a simple hover
<motion.button
  whileHover={{ scale: 1.05 }}
  transition={{ duration: 0.2 }}
>
  Click me
</motion.button>
```

**Correct (CSS handles it natively):**

```css
.button {
  transition: transform 200ms cubic-bezier(0.2, 0, 0, 1);
}
.button:hover {
  transform: scale(1.05);
}
```

Use JS when ANY of these are true:
- Runtime input streams (pointer position, velocity, gesture)
- Runtime measurement (element dimensions for FLIP)
- Cross-browser parity for scroll-linked effects
- Complex multi-element choreography with labels/callbacks
- Interruption semantics beyond what CSS transitions provide

Reference: `references/tool-selection.md`, `references/css-native.md`
