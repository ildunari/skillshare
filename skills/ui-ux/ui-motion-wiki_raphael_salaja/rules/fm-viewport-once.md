---
title: Set viewport.once for Scroll Reveals
impact: MEDIUM
impactDescription: Without viewport.once, elements re-animate every time they scroll in and out of view — jarring and distracting for reveal effects.
tags: framer-motion, whileinview, scroll, reveal
---

## Set viewport.once for Scroll Reveals

Framer Motion's `whileInView` without `viewport={{ once: true }}` re-animates elements every scroll pass. For reveal animations, fire once and stop observing.

**Incorrect (re-animates on every scroll):**

```tsx
<motion.section
  initial={{ opacity: 0, y: 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
/>
```

**Correct (fires once, stays visible):**

```tsx
<motion.section
  initial={{ opacity: 0, y: 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.3 }}
  transition={{ duration: 0.5, ease: [0.2, 0, 0, 1] }}
/>
```

`viewport.amount` controls what fraction of the element must be visible (0–1). `0.3` means 30% visible before triggering.

Reference: `references/framer-motion.md`
