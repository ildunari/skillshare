# FLIP Animation Technique

> First, Last, Invert, Play — the universal pattern for animating layout changes that CSS transitions can't express. Manual implementation, GSAP Flip plugin, Framer Motion layout, and the edge cases that break each approach.

## Contents
- What FLIP Solves → Manual Implementation (vanilla JS, WAAPI, multi-element)
- GSAP Flip Plugin: basic, enter/leave, ScrollTrigger integration
- Framer Motion Layout: layout prop, layoutId, when sufficient vs GSAP
- Edge Cases: scale distortion, transform origin, margin collapse, scroll position, rAF timing
- Reduced Motion

---

## What FLIP Solves

CSS can't transition between two different layout states (e.g., an element moving from a grid to a modal, a list item reordering, a thumbnail expanding to full-screen). The element would simply snap to its new position. FLIP makes these transitions smooth by:

1. **First** — Record the element's current position/size
2. **Last** — Apply the DOM change (element is now in its final position)
3. **Invert** — Use transforms to visually place the element back at its First position
4. **Play** — Animate the inversion away (element appears to smoothly move to its Last position)

The key insight: the DOM change happens *immediately* and *synchronously*. The animation is purely visual — transforms don't trigger layout. This is why FLIP is fast.

---

## Manual Implementation (Vanilla JS)

### Basic FLIP

```js
function flip(element, mutation) {
  // FIRST — snapshot current bounds
  const first = element.getBoundingClientRect();

  // LAST — apply the DOM change
  mutation();

  // Measure new bounds
  const last = element.getBoundingClientRect();

  // INVERT — calculate the delta and apply as transform
  const dx = first.left - last.left;
  const dy = first.top - last.top;
  const sw = first.width / last.width;
  const sh = first.height / last.height;

  element.style.transformOrigin = "top left";
  element.style.transform =
    `translate(${dx}px, ${dy}px) scale(${sw}, ${sh})`;

  // Force browser to register the inversion (read layout)
  element.getBoundingClientRect();

  // PLAY — animate to identity transform
  element.style.transition = "transform 350ms cubic-bezier(0.2, 0, 0, 1)";
  element.style.transform = "";

  // Cleanup
  element.addEventListener("transitionend", () => {
    element.style.transition = "";
    element.style.transformOrigin = "";
  }, { once: true });
}

// Usage
flip(card, () => {
  container.classList.toggle("expanded");
});
```

### FLIP with WAAPI (cleaner, more control)

```js
function flipWaapi(element, mutation, options = {}) {
  const {
    duration = 350,
    easing = "cubic-bezier(0.2, 0, 0, 1)"
  } = options;

  const first = element.getBoundingClientRect();
  mutation();
  const last = element.getBoundingClientRect();

  const dx = first.left - last.left;
  const dy = first.top - last.top;
  const sw = first.width / last.width;
  const sh = first.height / last.height;

  const anim = element.animate([
    {
      transformOrigin: "top left",
      transform: `translate(${dx}px, ${dy}px) scale(${sw}, ${sh})`
    },
    {
      transformOrigin: "top left",
      transform: "none"
    }
  ], { duration, easing, fill: "none" });

  return anim.finished;
}
```

### Multi-element FLIP (list reorder)

```js
function flipAll(elements, mutation) {
  // FIRST — snapshot all
  const firsts = new Map();
  elements.forEach(el => {
    firsts.set(el, el.getBoundingClientRect());
  });

  // LAST — apply mutation
  mutation();

  // INVERT + PLAY each element
  elements.forEach(el => {
    const first = firsts.get(el);
    const last = el.getBoundingClientRect();

    const dx = first.left - last.left;
    const dy = first.top - last.top;

    if (Math.abs(dx) < 1 && Math.abs(dy) < 1) return; // didn't move

    el.animate([
      { transform: `translate(${dx}px, ${dy}px)` },
      { transform: "none" }
    ], {
      duration: 300,
      easing: "cubic-bezier(0.2, 0, 0, 1)"
    });
  });
}
```

---

## GSAP Flip Plugin

GSAP's Flip plugin handles the measurement/inversion automatically, including scale compensation, nested elements, and enter/leave animations. All plugins are free since April 2025.

### Basic Flip

```js
// Snapshot current state
const state = Flip.getState(".card");

// Apply DOM change
container.classList.toggle("reordered");

// Animate from old state to new
Flip.from(state, {
  duration: 0.5,
  ease: "power2.inOut",
  stagger: 0.04,
  absolute: true,    // position elements absolutely during animation
  scale: true,       // animate scale changes (not just position)
  onComplete: () => console.log("done")
});
```

### Enter and leave with Flip

```js
const state = Flip.getState(".item");

// Add/remove DOM elements
newItems.forEach(el => container.appendChild(el));
removedItems.forEach(el => el.remove());

Flip.from(state, {
  duration: 0.5,
  ease: "power2.out",
  stagger: 0.03,
  // Elements that weren't in the original state = "entering"
  onEnter: elements =>
    gsap.fromTo(elements, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4 }),
  // Elements no longer in DOM = "leaving"
  onLeave: elements =>
    gsap.to(elements, { opacity: 0, scale: 0.8, duration: 0.3 }),
  absolute: true
});
```

### Flip + ScrollTrigger

```js
const state = Flip.getState(".panel");
panels.forEach(p => p.classList.add("stacked"));

Flip.from(state, {
  duration: 1,
  ease: "none",
  scrollTrigger: {
    trigger: ".section",
    start: "top top",
    end: "+=1000",
    scrub: true,
    pin: true
  }
});
```

---

## Framer Motion Layout Animations

Framer Motion implements FLIP automatically when you use the `layout` prop. No manual measurement needed.

```jsx
// Position + size animation
<motion.div layout />

// Position only (prevents distortion of content)
<motion.div layout="position" />

// Shared element between components
<motion.div layoutId="shared-hero" />
```

### When Framer Motion's FLIP is sufficient

- List item reorder, add, remove
- Expanding/collapsing panels
- Tab indicator sliding
- Card → modal shared element
- Grid layout changes

### When to use GSAP Flip instead

- Non-React projects (HTML artifacts, vanilla)
- Need to coordinate FLIP with scroll pinning
- Many elements (100+) where GSAP's optimized measurement is faster
- Need enter/leave hooks with fine-grained control
- SVG elements (Framer Motion's layout doesn't work with SVG)

---

## Edge Cases and Failure Modes

### Scale distortion

FLIP uses `scale()` to animate size changes. This distorts children: text gets stretched, border-radius warps, shadows change size.

**Fixes:**
- Apply inverse scale to children during animation
- Use `layout="position"` in Framer Motion (skips size animation)
- GSAP Flip: use `nested: true` to auto-correct children
- For border-radius: animate it separately to compensate

### Transform origin

FLIP calculations assume `transform-origin: top left` (or 0 0). If your element has a different transform-origin, the inversion will be offset.

**Fix:** Always set `transformOrigin: "top left"` during the FLIP. Reset after.

### Margin collapse

`getBoundingClientRect()` measures the border box, not the margin box. If margins collapse or change between states, the animation will be offset by the margin delta.

**Fix:** Use padding instead of margins on FLIP targets, or account for margin changes in the delta calculation.

### Scroll position changes

If the DOM mutation causes a scroll position change (adding content above, changing heights), the "Last" measurement will be wrong because the viewport moved.

**Fix:** Measure scroll position before mutation. Compensate in the delta calculation. GSAP Flip handles this automatically.

### `position: fixed` and `position: sticky`

These elements exist in a different coordinate space than the document flow. `getBoundingClientRect()` gives viewport-relative coordinates, but the element's actual layout position may differ.

**Fix:** Account for scroll offset when FLIPing fixed/sticky elements. Or avoid FLIPing them — animate the content around them instead.

### rAF timing

The Invert step must happen in the same frame as the DOM mutation, before the browser paints. If a rAF boundary falls between mutation and inversion, the user sees a flash of the un-inverted state.

**Fix:** Do First → Last → Invert synchronously. The `getBoundingClientRect()` call after setting the inversion forces a layout read, ensuring the browser has the correct values before the next paint.

---

## Reduced Motion

FLIP animations are layout transitions — they communicate spatial relationships. Under reduced motion, replace with a simple opacity crossfade:

```css
@media (prefers-reduced-motion: reduce) {
  .flip-target {
    transition: opacity 150ms linear !important;
    transform: none !important;
  }
}
```

In Framer Motion:

```jsx
<motion.div
  layout
  transition={prefersReduced
    ? { layout: { duration: 0 } }
    : { type: "spring", stiffness: 350, damping: 25 }
  }
/>
```
