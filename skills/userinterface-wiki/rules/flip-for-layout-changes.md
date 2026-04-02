---
title: Use FLIP for Layout Change Animation
impact: HIGH
impactDescription: CSS can't transition between different layout states (grid to modal, list reorder, thumbnail to fullscreen). FLIP makes these smooth using only transforms.
tags: flip, layout, gsap-flip, framer-motion-layout, performance
---

## Use FLIP for Layout Change Animation

First-Last-Invert-Play: record position, apply DOM change, use transforms to visually undo the change, then animate transforms away. The DOM change is instant — the animation is purely visual using compositor-friendly transforms.

**Incorrect (animating layout properties):**

```css
/* Triggers reflow on every frame — janky */
.card { transition: width 300ms, height 300ms, left 300ms, top 300ms; }
```

**Correct (FLIP with transforms):**

```tsx
// React: Framer Motion layout prop (automatic FLIP)
<motion.div layout className={isExpanded ? "large" : "small"} />

// React: Shared element transition
<motion.img layoutId={`hero-${item.id}`} src={item.thumb} />
```

```js
// Vanilla: GSAP Flip plugin
const state = Flip.getState(".card");
container.classList.toggle("grid-view");
Flip.from(state, {
  duration: 0.5,
  ease: "power2.inOut",
  stagger: 0.04,
  absolute: true
});
```

```js
// Vanilla: Manual FLIP with WAAPI (zero dependencies)
const first = el.getBoundingClientRect();
applyDOMChange();
const last = el.getBoundingClientRect();
const dx = first.left - last.left, dy = first.top - last.top;
el.animate([
  { transform: `translate(${dx}px, ${dy}px)` },
  { transform: "none" }
], { duration: 350, easing: "cubic-bezier(0.2, 0, 0, 1)" });
```

Use `layout="position"` in Framer Motion to avoid scale distortion on text/borders.

Reference: `references/flip-technique.md`
