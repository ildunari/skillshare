---
title: Vary Reveal Patterns — Don't Default to Fade+Translate
impact: HIGH
impactDescription: Using the same opacity:0/translateY(20px) reveal for every element is a strong AI-generated-code tell and produces forgettable, templated interfaces.
tags: practitioner, reveals, variety, polish
---

## Vary Reveal Patterns — Don't Default to Fade+Translate

The most common AI-generated animation pattern is `opacity: 0, translateY(20px)` → `opacity: 1, translateY(0)` on every element. This produces monotonous, visually flat interfaces. Vary the reveal based on content type and importance.

**Incorrect (same reveal everywhere):**

```tsx
// Every single element uses identical fade+slide
<motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} />
<motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} />
<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} />
```

**Correct (varied reveals matched to content):**

```tsx
// Hero title: scale + fade (prominence)
<motion.h1 initial={{ opacity: 0, scale: 0.96 }}
  animate={{ opacity: 1, scale: 1 }} />

// Body text: simple opacity (subtle, doesn't compete)
<motion.p initial={{ opacity: 0 }}
  animate={{ opacity: 1 }} transition={{ delay: 0.1 }} />

// Cards: stagger from center with slight scale
<motion.div variants={card}
  initial={{ opacity: 0, y: 12, scale: 0.97 }}
  animate={{ opacity: 1, y: 0, scale: 1 }} />

// Image: clip-path wipe or mask reveal
```

Also vary: stagger direction (center, edges, importance-based), easing (ease-out for arrivals, spring for interactive), and duration (shorter for small elements, longer for large).

Reference: `references/practitioner-knowledge.md`
