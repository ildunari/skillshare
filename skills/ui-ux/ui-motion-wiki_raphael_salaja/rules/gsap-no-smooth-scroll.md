---
title: No CSS smooth-scroll with ScrollTrigger
impact: HIGH
impactDescription: CSS scroll-behavior:smooth creates a transition on scroll position that fights ScrollTrigger, causing sluggish scrolling and refresh conflicts.
tags: gsap, scrolltrigger, scroll-behavior, conflict
---

## No CSS smooth-scroll with ScrollTrigger

`scroll-behavior: smooth` on `html` causes sluggishness and refresh weirdness when combined with GSAP ScrollTrigger. It's like putting a CSS transition on the same property GSAP is controlling.

**Incorrect (CSS smooth-scroll + ScrollTrigger conflict):**

```css
html { scroll-behavior: smooth; }
```

```js
gsap.to(".hero", {
  y: -100,
  scrollTrigger: { trigger: ".hero", scrub: 0.6 }
});
```

**Correct (remove smooth-scroll, use GSAP ScrollTo for navigation):**

```css
/* Remove scroll-behavior: smooth from pages using ScrollTrigger */
```

```js
// Use GSAP ScrollTo plugin for anchor navigation instead
gsap.to(window, { scrollTo: "#section", duration: 0.8, ease: "power2.out" });
```

Reference: `references/gsap-production.md`, `references/practitioner-knowledge.md`
