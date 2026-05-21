---
title: Don't Trigger View Transitions on Hover
impact: MEDIUM
impactDescription: The view transition layer sits above the UI during the transition, firing mouseleave on the original element — breaking hover states.
tags: view-transitions, hover, gotcha
---

## Don't Trigger View Transitions on Hover

View Transitions API creates snapshot pseudo-elements during the transition. This layer sits above the UI, causing `mouseleave` to fire on the original element mid-transition.

**Incorrect (hover-triggered view transition breaks mouse events):**

```js
card.addEventListener("mouseenter", () => {
  document.startViewTransition(() => {
    card.classList.add("expanded");
  });
});
// mouseleave fires immediately because transition layer covers the element
```

**Correct (click/navigation-triggered):**

```js
card.addEventListener("click", () => {
  if (!document.startViewTransition) {
    updateDOM();
    return;
  }
  document.startViewTransition(() => updateDOM());
});
```

Reference: `references/css-native.md`, `references/practitioner-knowledge.md`
