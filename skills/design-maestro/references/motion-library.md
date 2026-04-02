# Motion Library

> Animation aesthetic guidance — which animations to use and why. For implementation details (tool selection, library-specific code, production patterns, failure modes), load the **userinterface-wiki** skill.

---

## Core Principles

1. **Natural:** Spring physics > linear easing. Things in the real world don't move linearly.
2. **Fast:** Enter in 200-300ms, exit in 150-200ms. Users notice >400ms as sluggish.
3. **Purposeful:** Every animation communicates something. Entrance = "I'm new." Stagger = "We're related." Spring = "I'm interactive."
4. **Performant:** Only animate `transform`, `opacity`, `filter`. Everything else triggers layout reflow.
5. **Interruptible:** Use spring animations that can be redirected mid-flight.
6. **Accessible:** Every animation needs a `prefers-reduced-motion` variant.

### Claude Artifact Constraints

Framer Motion is available in Claude React artifacts — `import { motion, AnimatePresence, useMotionValue, useSpring, useTransform, LayoutGroup } from "framer-motion"` works without CDN setup. CSS fallbacks are only needed for HTML (non-React) artifacts.

---

## Recipe Index

### 1. Entry Animations

| Recipe | When to Use | Aesthetic Effect |
|---|---|---|
| Staggered Reveal | Lists, card grids, related elements | Communicates hierarchy and relationship |
| Spring Physics | Modals, popovers, interactive elements | Feels alive and responsive |
| Slide + Fade | Section entries, page loads | Clean, professional reveal |

→ Implementation: userinterface-wiki `references/framer-motion.md` (variants, staggerChildren) or `references/css-native.md` (@starting-style)

### 2. Scroll-Triggered

| Recipe | When to Use | Aesthetic Effect |
|---|---|---|
| CSS Scroll-Driven | Simple reveals (Chrome 115+, Safari 26+) | Tied to user's pace, feels natural |
| Intersection Observer + FM | Cross-browser scroll reveals | Reliable, predictable entry |
| Sticky + Progress | Storytelling sections, timelines | Guided narrative flow |

→ Implementation: userinterface-wiki `references/css-native.md` (scroll-driven) or `references/gsap-production.md` (ScrollTrigger)

### 3. Micro-Interactions

| Recipe | When to Use | Aesthetic Effect |
|---|---|---|
| Button Press | All buttons | Tactile confirmation |
| Like/Heart Burst | Social actions, favorites | Delight, emotional reward |
| Hover Card Tilt | Featured cards, portfolio items | Depth, premium feel |

→ Implementation: userinterface-wiki `references/pattern-recipes.md` (particle button, spotlight border)

### 4. Page Transitions

| Recipe | When to Use | Aesthetic Effect |
|---|---|---|
| Crossfade | Most page transitions | Smooth continuity |
| View Transitions API | Modern browsers, progressive | Native-feeling navigation |
| Shared Element Morph | List→detail, card→page | Identity preservation |

→ Implementation: userinterface-wiki `references/css-native.md` (view transitions) or `references/framer-motion.md` (layoutId)

### 5. Loading States

| Recipe | When to Use | Aesthetic Effect |
|---|---|---|
| Skeleton Shimmer | Any async content | System is working, content coming |
| Progress Bar | File uploads, long operations | Measurable progress builds trust |
| Optimistic UI | Social actions, toggles, saves | Instant response, confident system |

### 6. Gesture Handling

| Recipe | When to Use | Aesthetic Effect |
|---|---|---|
| Drag-and-Drop | Kanban, list reordering, file upload | Direct manipulation, control |
| Swipe Gestures | Card stacks, dismissable items | Mobile-native feel |
| Pinch-to-Zoom | Image viewers, maps | Spatial exploration |

→ Implementation: userinterface-wiki `references/framer-motion.md` (drag, gesture system)

### 7. Text Animations

| Recipe | When to Use | Aesthetic Effect |
|---|---|---|
| Typewriter | Chat UIs, terminal aesthetics | Progressive revelation |
| Character Stagger | Hero headlines, dramatic reveals | Theatrical entrance |
| Counting Number | Stats, dashboards, metrics | Data coming alive |

→ Implementation: userinterface-wiki `references/pattern-recipes.md` (text scramble, char reveal)

### 8. Layout Animations

| Recipe | When to Use | Aesthetic Effect |
|---|---|---|
| List Reordering | Todo lists, sortable items | Spatial consistency |
| Accordion | FAQ, settings, expandable | Content breathing |
| Tab Transitions | Tabbed content, wizards | Directional context |

→ Implementation: userinterface-wiki `references/flip-technique.md` or `references/css-native.md` (interpolate-size)

---

## Performance Rules

- Animate only `transform`, `opacity`, `filter` (GPU-composited)
- Use `will-change` temporarily — add before, remove after animation
- Prefer CSS animations for simple effects
- Use `requestAnimationFrame` for Canvas/WebGL, never `setInterval`
- Never animate `width`, `height`, `top`, `left`, `margin`, `padding`
- Never leave `will-change` on permanently
- Always respect `prefers-reduced-motion`

## When to Go Deeper

Load `references/deep/motion-performance.md` for:
- Perpetual/looping animations (status dots, live feeds, carousels)
- Magnetic/cursor-tracking interactions
- Bento grids with live motion (Bento 2.0 architecture)
- Stagger on async data (tree contract pattern)
- Spring physics calibration tables
- GSAP vs Framer Motion separation contract

## Browser Support (early 2026)

| Feature | Chrome/Edge | Safari | Firefox |
|---|---|---|---|
| CSS Transitions/Animations | ✅ | ✅ | ✅ |
| Web Animations API | ✅ | ✅ | ✅ |
| Scroll-Driven Animations | ✅ 115+ | ✅ 26+ | Disabled by default |
| View Transitions (same-doc) | ✅ 111+ | ✅ 18+ | ✅ 144+ |
| `@starting-style` | ✅ 117+ | ✅ 17.4+ | ✅ 129+ |
| `interpolate-size` | ✅ 129+ | ✅ 26+ | Not yet |
| Framer Motion | ✅ | ✅ | ✅ |

For detailed support data: load userinterface-wiki → browser support matrix.
