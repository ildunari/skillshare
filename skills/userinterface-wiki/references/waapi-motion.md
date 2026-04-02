# WAAPI and Motion: Native-First Animation

> The Web Animations API is the browser-native animation engine. Motion One / motion.dev builds higher-level ergonomics on top. This file covers both, including the hybrid-engine bugs that emerge when WAAPI drivers partially replace JS drivers.

---

## WAAPI Core

### When to use
Use WAAPI when you need: dependency-free artifact animation, fine-grained runtime control (pause/play/reverse/seek/speed), or a predictable imperative API outside React. WAAPI runs through the browser's animation engine — you get the same compositor-thread optimizations as CSS animations for eligible properties.

### Essential API

```js
// Create and play immediately
const anim = el.animate(
  [
    { opacity: 0, transform: "translateY(12px)" },
    { opacity: 1, transform: "translateY(0)" }
  ],
  {
    duration: 220,
    easing: "cubic-bezier(0.2, 0, 0, 1)",
    fill: "both"
  }
);

// Lifecycle control
anim.pause();
anim.play();
anim.reverse();
anim.finish();
anim.cancel();
anim.currentTime = 100; // seek to 100ms
anim.playbackRate = 1.5; // speed up

// Promise-based sequencing
await anim.finished;
// anim.ready also available (resolves when animation is ready to play)
```

### Keyframe formats
```js
// Array of objects (most readable)
[{ transform: "scale(1)" }, { transform: "scale(1.1)" }, { transform: "scale(1)" }]

// Object of arrays (compact, same result)
{ transform: ["scale(1)", "scale(1.1)", "scale(1)"] }
```

### The `commitStyles()` pattern — CRITICAL

After a WAAPI animation finishes, the animated styles don't automatically persist as inline styles. If you used `fill: "forwards"`, the animation object stays alive holding those styles — which leaks memory and can cause conflicts.

The production pattern is: commit styles, then cancel.

```js
const anim = el.animate(
  [{ transform: "translateY(0)" }, { transform: "translateY(100px)" }],
  { duration: 300, fill: "both" }
);

anim.finished
  .catch(() => {}) // cancel() rejects .finished
  .finally(() => {
    anim.commitStyles(); // persist final computed styles as inline
    anim.cancel();       // remove the animation player
  });
```

This is a fundamental WAAPI concept that official docs often underemphasize. Motion One's creator cites discovering this behavior as part of the motivation for building a wrapper library.

### Advanced: `KeyframeEffect` for target swapping

```js
const effect = new KeyframeEffect(
  el,
  [{ opacity: 0 }, { opacity: 1 }],
  { duration: 200 }
);

// Later: swap target
effect.target = anotherEl;

const anim = new Animation(effect);
anim.play();
```

### Introspection
```js
// Get all active animations on the page
const allAnims = document.getAnimations();

// Get animations on a specific element
const elAnims = el.getAnimations();
```

---

## Production Example: Toast System

Interruption-safe enter/exit with `commitStyles`, reduced motion, and cleanup.

```js
function prefersReducedMotion() {
  return window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
}

function toastIn(el) {
  if (prefersReducedMotion()) {
    el.style.opacity = "1";
    el.style.transform = "translateY(0)";
    return null;
  }
  return el.animate(
    [
      { opacity: 0, transform: "translateY(12px)" },
      { opacity: 1, transform: "translateY(0)" }
    ],
    { duration: 220, easing: "cubic-bezier(0.2, 0, 0, 1)", fill: "both" }
  );
}

function toastOut(el) {
  if (prefersReducedMotion()) {
    el.remove();
    return Promise.resolve();
  }
  const anim = el.animate(
    [
      { opacity: 1, transform: "translateY(0)" },
      { opacity: 0, transform: "translateY(8px)" }
    ],
    { duration: 160, easing: "cubic-bezier(0.2, 0, 0, 1)", fill: "both" }
  );
  return anim.finished
    .catch(() => {})
    .finally(() => {
      anim.commitStyles?.();
      anim.cancel();
      el.remove();
    });
}

async function showToast(msg) {
  const el = document.createElement("div");
  el.className = "toast";
  el.textContent = msg;
  document.body.appendChild(el);
  const inAnim = toastIn(el);
  if (inAnim) await inAnim.finished;
  await new Promise(r => setTimeout(r, 3000));
  await toastOut(el);
}
```

---

## Motion One / motion.dev

Motion One (now represented in motion.dev's JS docs) wraps WAAPI + browser primitives for higher-level ergonomics at a small footprint.

### Key APIs
- `animate(targets, keyframes, options)` — enhanced `Element.animate()`
- `timeline()` — sequenced animation groups
- `scroll()` — scroll-linked value mapping (JS-driven)
- `inView()` — IntersectionObserver wrapper (tiny, off-main-thread)
- `stagger(value, options)` — delay spread across targets
- Spring and inertia timing options

### Script-tag import (for HTML artifacts)
```html
<script src="https://cdn.jsdelivr.net/npm/motion@latest/dist/motion.js"></script>
```

Check CDN availability — Motion's bundling may change. For React artifacts, Framer Motion is built in and is the better choice.

---

## Known WAAPI/Motion Bugs (2025–2026)

### ScrollTimeline opacity bug (Feb 2026)
**Issue:** Since Motion ~v12.30, the library uses native `ScrollTimeline` when `window.ScrollTimeline` exists. This causes scroll-linked opacity animations to break in Safari (never reaches full opacity) and Firefox (jumps to full immediately). Transforms like scale/rotate work fine.
**Root cause:** Feature-detection trap — "API exists" doesn't mean "API works correctly for all properties."
**Mitigation:** Test opacity specifically with scroll-linked animations in Safari/Firefox. Consider opting out of ScrollTimeline for opacity-involving scroll animations until engines stabilize.

### `autoplay: false` not honored with opacity (May 2025)
**Issue:** Motion's `animate()` doesn't honor `autoplay: false` when opacity is involved. Opting out of WAAPI (via a tiny `repeatDelay` hack) fixes it.
**Root cause:** WAAPI driver semantics differ from JS driver for certain sequencing parameters.
**Mitigation:** Test `autoplay: false` behavior explicitly. If sequencing is critical, verify with both drivers.

### General WAAPI driver semantics drift
Motion has used WAAPI under the hood for hardware-accelerated values for ~2 years. This hybrid architecture means: some properties run through the WAAPI driver, some through the JS driver, and their semantics can subtly differ for edge cases around timing, fill behavior, and composition.

**Practitioner rule:** If an animation behaves differently than expected, check whether the WAAPI driver is involved. The `repeatDelay` hack to force JS-only execution is a known diagnostic technique.

---

## Browser Support

WAAPI core (`Animation`, `commitStyles`, `finished`) is "widely available" across all modern browsers since ~2020. MDN labels it broadly supported.

ScrollTimeline/ViewTimeline (JS APIs) are still limited — Chrome has them, Safari/Firefox are partial or disabled. Feature-detect carefully; existence ≠ correctness.
