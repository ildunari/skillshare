---
title: Register @property for Animatable Custom Properties
impact: MEDIUM
impactDescription: Without @property registration, custom properties snap between values instead of interpolating. Gradient animations, angle transitions, and percentage-based effects require it.
tags: css, property, gradients, animation
---

## Register @property for Animatable Custom Properties

CSS `@property` (Baseline 2024) registers custom properties with a type, enabling smooth interpolation of gradients, angles, and percentages that would otherwise snap.

**Incorrect (custom property snaps, no interpolation):**

```css
.gradient-border {
  --angle: 0deg;
  background: conic-gradient(from var(--angle), #7dd3fc, #a78bfa, #fb7185, #7dd3fc);
  animation: spin 4s linear infinite;
}

@keyframes spin {
  to { --angle: 360deg; } /* Snaps! Not smooth. */
}
```

**Correct (registered property interpolates smoothly):**

```css
@property --gradient-angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.gradient-border {
  background: conic-gradient(from var(--gradient-angle), #7dd3fc, #a78bfa, #fb7185, #7dd3fc);
  animation: spin 4s linear infinite;
}

@keyframes spin {
  to { --gradient-angle: 360deg; } /* Smooth rotation */
}
```

Reference: `references/css-native.md`
