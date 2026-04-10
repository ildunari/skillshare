---
title: Vary Duration by Element Size and Importance
impact: MEDIUM
impactDescription: Uniform 300ms on everything feels mechanical. Larger elements need longer to travel their distance; small interactions should be snappier.
tags: practitioner, duration, timing, polish
---

## Vary Duration by Element Size and Importance

A uniform duration across all animations makes the interface feel robotic. Scale duration to the element's visual weight, travel distance, and interaction importance.

**Incorrect (same duration everywhere):**

```css
.button, .modal, .card, .tooltip, .sidebar {
  transition: all 300ms ease;
}
```

**Correct (scaled by context):**

```css
/* Press/hover feedback: snappy */
.button { transition: transform 150ms cubic-bezier(0.2, 0, 0, 1); }

/* Small state change: quick */
.toggle { transition: background-color 200ms ease; }

/* Modal/drawer: moderate */
.modal { transition: opacity 250ms ease, transform 280ms cubic-bezier(0.2, 0, 0, 1); }

/* Page-level transition: can be longer */
.page-enter { animation: pageIn 350ms cubic-bezier(0.2, 0, 0, 1); }
```

Guidelines:
- Press/hover: 120–180ms
- Small state changes: 180–260ms
- User-initiated max: 300ms
- System transitions: up to 400ms
- If it feels slow, shorten the duration — don't change the curve

Reference: `references/practitioner-knowledge.md`
