---
title: Match Tool to Motion Role
impact: CRITICAL
impactDescription: Using the wrong animation tool for the motion role leads to fighting the tool's strengths, producing brittle or underperforming code.
tags: tool-selection, architecture, motion-role
---

## Match Tool to Motion Role

Every UI animation serves one of four roles. The role determines the optimal tool. Don't force one library to do everything.

| Role | What it does | Best tools |
|------|-------------|------------|
| **Continuity** | Preserves identity across state/layout changes | View Transitions API, GSAP Flip, Framer Motion layoutId |
| **Feedback** | Confirms user action happened | CSS transitions, springs (Framer/CSS linear()), WAAPI |
| **Narrative** | Guides attention through content | GSAP timelines, ScrollTrigger, CSS scroll-driven |
| **Ornament** | Ambient polish reinforcing brand/mood | CSS @keyframes, WebGL shaders, Paper.js |

**Incorrect (mismatched tool for role):**

```tsx
// Using GSAP timeline for a simple button press (feedback role)
const tl = gsap.timeline();
tl.to(".btn", { scale: 0.97, duration: 0.1 })
  .to(".btn", { scale: 1, duration: 0.3, ease: "elastic.out(1, 0.3)" });
```

**Correct (spring for feedback, timeline for narrative):**

```tsx
// Feedback: spring (interruptible, natural)
<motion.button whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 400, damping: 30 }} />

// Narrative: GSAP timeline (choreographed sequence)
const tl = gsap.timeline({ scrollTrigger: { trigger: ".hero", scrub: 0.6 } });
tl.from(".title", { y: 24, opacity: 0 })
  .from(".cards", { y: 20, opacity: 0, stagger: 0.08 }, "-=0.3");
```

Reference: `references/tool-selection.md`
