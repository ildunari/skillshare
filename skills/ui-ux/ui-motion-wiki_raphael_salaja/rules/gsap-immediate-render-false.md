---
title: Set immediateRender false on ScrollTrigger from()
impact: MEDIUM
impactDescription: gsap.from() sets the starting state immediately by default. In ScrollTrigger contexts, this flashes the "from" state before the trigger fires.
tags: gsap, scrolltrigger, immediate-render, flash
---

## Set immediateRender false on ScrollTrigger from()

`gsap.from()` sets the starting state immediately by default (`immediateRender: true`). With ScrollTrigger, this flashes the "from" state before the trigger fires, causing a visible pop.

**Incorrect (flashes starting state on page load):**

```js
gsap.from(".card", {
  y: 40,
  opacity: 0,
  scrollTrigger: { trigger: ".card", start: "top 85%" }
});
// Cards flash to opacity:0 on page load, then snap back
```

**Correct (defers rendering until trigger fires):**

```js
gsap.from(".card", {
  y: 40,
  opacity: 0,
  immediateRender: false,
  scrollTrigger: { trigger: ".card", start: "top 85%" }
});

// Or use fromTo() for explicit control
gsap.fromTo(".card",
  { y: 40, opacity: 0 },
  { y: 0, opacity: 1, scrollTrigger: { trigger: ".card", start: "top 85%" } }
);
```

Reference: `references/gsap-production.md`, `references/practitioner-knowledge.md`
