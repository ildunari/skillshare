---
title: Use interpolate-size for Height Auto Animation
impact: HIGH
impactDescription: Animating to/from height:auto was a decade-long pain point requiring JS measurement. CSS can now handle it natively.
tags: css, accordion, height-auto, interpolate-size, calc-size
---

## Use interpolate-size for Height Auto Animation

`interpolate-size: allow-keywords` at `:root` enables smooth transitions to/from `auto`, `min-content`, `max-content`, `fit-content`. Use `calc-size()` for per-component opt-in without global side effects. Chrome 129+, Safari 26+. Firefox not yet — progressive enhancement required.

**Incorrect (JavaScript measurement for accordion):**

```tsx
// Measuring height with ResizeObserver then animating
const height = contentRef.current.scrollHeight;
contentRef.current.style.height = isOpen ? `${height}px` : "0px";
```

**Correct (CSS-native height animation):**

```css
:root {
  interpolate-size: allow-keywords;
}

.accordion-content {
  height: 0;
  overflow: hidden;
  transition: height 350ms cubic-bezier(0.2, 0, 0, 1);
}

.accordion[open] .accordion-content {
  height: auto; /* This now animates smoothly */
}

@media (prefers-reduced-motion: reduce) {
  .accordion-content { transition: none; }
}
```

**Caution:** `interpolate-size: allow-keywords` is global — it could cause unexpected interpolation on elements that currently snap between size keywords. Audit before adding to an existing codebase.

Reference: `references/css-native.md`
