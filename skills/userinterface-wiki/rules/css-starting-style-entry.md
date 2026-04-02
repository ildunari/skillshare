---
title: Use @starting-style for Entry/Exit Animations
impact: HIGH
impactDescription: CSS can now animate elements appearing from display:none without JavaScript — replacing the old double-rAF hack and reducing library dependency.
tags: css, entry-animation, starting-style, allow-discrete, baseline-2024
---

## Use @starting-style for Entry/Exit Animations

`@starting-style` defines the pre-render starting state for elements appearing from `display: none`. Combined with `transition-behavior: allow-discrete`, CSS handles entry/exit for dialogs, popovers, and toggled elements. Baseline 2024 (Chrome 117+, Safari 17.4+, Firefox 129+).

**Incorrect (JavaScript for dialog entry):**

```js
// Double-rAF hack for enter animation
dialog.showModal();
requestAnimationFrame(() => {
  requestAnimationFrame(() => {
    dialog.classList.add("visible");
  });
});
```

**Correct (CSS-native entry/exit):**

```css
@supports (transition-behavior: allow-discrete) {
  dialog {
    opacity: 0;
    transform: translateY(8px) scale(0.98);
    transition:
      opacity 180ms ease,
      transform 220ms cubic-bezier(0.2, 0, 0, 1),
      display 220ms ease allow-discrete,
      overlay 220ms ease allow-discrete;
  }

  dialog[open] {
    opacity: 1;
    transform: translateY(0) scale(1);
  }

  @starting-style {
    dialog[open] {
      opacity: 0;
      transform: translateY(12px) scale(0.98);
    }
  }
}
```

The `overlay` property delays top-layer removal so exit transitions can complete. Place `@starting-style` inside `@supports` — older browsers ignore the whole block gracefully.

Reference: `references/css-native.md`
