---
title: Use useGSAP() in React, Not useEffect
impact: HIGH
impactDescription: useEffect without cleanup causes duplicate animations in React 18 StrictMode. useGSAP() creates context automatically, handles cleanup, and scopes selectors.
tags: gsap, react, usegsap, cleanup, strict-mode
---

## Use useGSAP() in React, Not useEffect

`useGSAP()` creates a GSAP context automatically, handles cleanup on unmount, and scopes selectors to a ref. Never nest `gsap.context()` inside `useGSAP()` — it already creates one.

**Incorrect (useEffect without cleanup):**

```tsx
useEffect(() => {
  gsap.from(".item", { y: 12, opacity: 0, stagger: 0.06 });
  // No cleanup — duplicates in StrictMode, leaks on unmount
}, []);
```

**Correct (useGSAP with scope):**

```tsx
import { useGSAP } from "@gsap/react";

function Component() {
  const containerRef = useRef(null);

  const { contextSafe } = useGSAP(() => {
    gsap.from(".item", { y: 12, opacity: 0, stagger: 0.06 });
  }, { scope: containerRef });

  // Event handlers MUST use contextSafe
  const handleClick = contextSafe(() => {
    gsap.to(".panel", { height: 0, duration: 0.3 });
  });

  return <div ref={containerRef}>...</div>;
}
```

Without `scope`, a selector like ".item" hits ALL matching elements in the document, not just your component's.

Reference: `references/gsap-production.md`
