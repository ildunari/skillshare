---
title: Feature-Detect Carefully — Existence ≠ Correctness
impact: HIGH
impactDescription: window.ScrollTimeline existing doesn't mean it works correctly for all properties. Safari/Firefox have bugs with specific combinations even when APIs are present.
tags: browser-support, feature-detection, progressive-enhancement
---

## Feature-Detect Carefully — Existence ≠ Correctness

Checking if an API exists (`window.ScrollTimeline !== undefined`) is not the same as verifying it works correctly. Known bugs: Safari opacity animations with ScrollTimeline never reach full opacity (Feb 2026), Firefox jumps immediately. Transforms work fine on both.

**Incorrect (existence-only detection):**

```js
if (window.ScrollTimeline) {
  // Assume everything works — but opacity breaks in Safari
  animation.timeline = new ScrollTimeline({ source: document.documentElement });
}
```

**Correct (robust detection with property-specific testing):**

```css
/* CSS: use @supports for declarative features */
@supports (animation-timeline: view()) {
  .reveal {
    animation: fadeIn linear both;
    animation-timeline: view();
  }
}
```

```js
// JS: test the specific combination you need
function supportsScrollTimeline() {
  if (!window.ScrollTimeline) return false;
  // For opacity-involving scroll animations, add browser-specific checks
  // or test with a hidden probe element
  return true;
}
```

Use `@supports` for CSS features. For JS APIs, test the specific property combinations you'll use, not just API existence.

Reference: `references/practitioner-knowledge.md`, `references/waapi-motion.md`
