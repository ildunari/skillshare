---
title: Use layout="position" to Prevent Distortion
impact: MEDIUM
impactDescription: Framer Motion layout prop animates size via scale transforms, which distorts text, border-radius, box-shadow, and children during transitions.
tags: framer-motion, layout, distortion, flip
---

## Use layout="position" to Prevent Distortion

The `layout` prop in Framer Motion uses FLIP under the hood — it animates size changes via `scale()` transforms. This distorts text, border-radius, box-shadow, and children. Use `layout="position"` to only animate position, not size.

**Incorrect (content distortion during layout animation):**

```tsx
// Text and border-radius warp during the transition
<motion.div layout className={isExpanded ? "large-card" : "small-card"}>
  <h3>This text will stretch</h3>
</motion.div>
```

**Correct (position-only animation avoids distortion):**

```tsx
// Only position animates — size change is instant
<motion.div layout="position" className={isExpanded ? "large-card" : "small-card"}>
  <h3>This text stays crisp</h3>
</motion.div>
```

Use full `layout` only when scale distortion is acceptable (simple colored shapes, images). For text-heavy cards, panels, or UI with border-radius, prefer `layout="position"`.

Reference: `references/framer-motion.md`, `references/flip-technique.md`
