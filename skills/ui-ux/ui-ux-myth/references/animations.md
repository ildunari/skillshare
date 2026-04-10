# Motion & micro-interactions (with code)

Motion should clarify state, provide feedback, and guide attention — not decorate.

## 1) When to animate

Good uses:
- state transitions (open/close, expand/collapse)
- feedback (loading → success, validation)
- attention (new item appears, toast)
- subtle delight (hover lift, pressed state)

Bad uses:
- auto-rotating content that fights reading
- animating everything
- slow UI transitions that delay interaction

Related research note:
- Auto-forwarding carousels reduce visibility and control (NN/g): https://www.nngroup.com/articles/auto-forwarding/

## 2) Timing guidelines (practical)

- Hover/press: **120–180ms**
- UI transition (panel expand): **180–260ms**
- Page entrance: **350–600ms** (once, subtle)
- Avoid >300ms for common UI elements

## 3) Prefer cheap properties

Animate:
- `transform`
- `opacity`

Avoid:
- animating `height` frequently (unless small and infrequent)
- animating shadows heavily on large surfaces
- `filter: blur()` on big regions

## 4) CSS-first patterns

### Hover lift (subtle)

```css
.Card {
  transition: transform 160ms ease-out, box-shadow 160ms ease-out;
  box-shadow: var(--shadow);
}

.Card:hover {
  transform: translateY(-3px);
}
```

### Pressed state

```css
.Button:active {
  transform: translateY(1px);
}
```

### Staggered reveal (only for landing moments)

```css
.Reveal {
  opacity: 0;
  transform: translateY(18px);
  animation: rise 520ms ease-out forwards;
}

.Reveal:nth-child(1) { animation-delay: 80ms; }
.Reveal:nth-child(2) { animation-delay: 160ms; }
.Reveal:nth-child(3) { animation-delay: 240ms; }

@keyframes rise {
  to { opacity: 1; transform: translateY(0); }
}
```

## 5) React + framer-motion (optional)

If framer-motion is available:

```tsx
import { motion } from "framer-motion";

export function FadeInSection({ children }: { children: React.ReactNode }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.section>
  );
}
```

## 6) Vue transitions

```vue
<template>
  <Transition name="fade-slide">
    <div v-if="open" class="Panel">...</div>
  </Transition>
</template>

<style>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 200ms ease, transform 200ms ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
```

## 7) Reduced motion

Always respect:

```css
@media (prefers-reduced-motion: reduce) {
  .Card, .Button, .Panel { transition: none !important; }
  .Reveal { animation: none !important; opacity: 1 !important; transform: none !important; }
}
```
