---
title: Gate Scroll-Driven Animations Behind @supports
impact: HIGH
impactDescription: CSS scroll-driven animations are not cross-browser yet. Shipping without @supports gates breaks Firefox and older Safari.
tags: css, scroll-driven, supports, progressive-enhancement
---

## Gate Scroll-Driven Animations Behind @supports

CSS `animation-timeline: scroll()/view()` attaches animation progress to scroll position. Chrome 115+, Safari 26+, but Firefox disabled by default. Always gate behind `@supports` with visible fallback.

**Incorrect (no fallback):**

```css
.reveal {
  opacity: 0;
  animation: fadeIn linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
```

**Correct (gated with fallback):**

```css
/* Fallback: content always visible */
.reveal { opacity: 1; transform: none; }

/* Enhanced: scroll-driven entry */
@supports (animation-timeline: view()) {
  .reveal {
    animation: fadeSlideIn linear both;
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

For cross-browser scroll effects, use GSAP ScrollTrigger or IntersectionObserver as fallback.

Reference: `references/css-native.md`
