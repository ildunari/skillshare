# Framer Motion Deep Reference

> The default animation engine in Claude React artifacts. Covers the full API surface: motion components, variants, AnimatePresence, layout animations, gesture system, hooks, spring physics, and the production gotchas that tutorials skip.

## Contents
- Core: Motion Components → Variants → AnimatePresence (modes, gotchas) → Layout Animations (layout, layoutId)
- Interaction: Gesture System (hover, tap, drag, whileInView) → Hooks (useMotionValue, useTransform, useSpring, useScroll)
- Tuning: Spring Physics Configuration → Reduced Motion → Production Patterns (tabs, lists, grids) → Failure Modes

---

## When to Use

Use Framer Motion when you're in a React artifact or React project and need: declarative enter/exit animations (AnimatePresence), layout-aware transitions (layout prop, layoutId), gesture-driven motion (drag, hover, tap), spring physics with interruptibility, scroll-triggered reveals (whileInView), or motion value pipelines that avoid re-renders. Import as `import { motion, AnimatePresence } from "framer-motion"` in Claude React artifacts (it's bundled).

---

## Core: Motion Components

Any HTML or SVG element can be animated by prefixing with `motion.`:

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, ease: [0.2, 0, 0, 1] }}
/>
```

### The three animation states

| Prop | When it applies | Use for |
|---|---|---|
| `initial` | First render (set `false` to skip mount animation) | Enter effects |
| `animate` | Current target state | Any state-driven animation |
| `exit` | When removed from tree (requires `AnimatePresence` wrapper) | Leave effects |

### Conditional animation

```jsx
<motion.div
  animate={isOpen ? "open" : "closed"}
  variants={{
    open: { height: "auto", opacity: 1 },
    closed: { height: 0, opacity: 0 }
  }}
/>
```

---

## Variants: Orchestrated Component Trees

Variants propagate through component trees. Parent controls timing; children inherit state labels.

```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.1,
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0 }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i.id} variants={item} />
  ))}
</motion.ul>
```

### Stagger patterns

```jsx
// Reverse stagger (last item first)
staggerChildren: 0.06,
staggerDirection: -1

// Custom per-child delay via dynamic variants
const item = {
  hidden: { opacity: 0 },
  show: (i) => ({
    opacity: 1,
    transition: { delay: i * 0.05 }
  })
};
<motion.div custom={index} variants={item} />
```

---

## AnimatePresence: Exit Animations

Wrap any conditionally rendered components. Without `AnimatePresence`, React unmounts immediately — no exit animation possible.

```jsx
<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.2 }}
    />
  )}
</AnimatePresence>
```

### Modes

| Mode | Behavior | Use when |
|---|---|---|
| `"sync"` (default) | Enter and exit happen simultaneously | Crossfade, overlapping transitions |
| `"wait"` | Exit completes before enter starts | Tab content, route transitions, modals |
| `"popLayout"` | Exiting element removed from layout flow immediately | Lists where items should reflow during exit |

### Gotchas

- **Every direct child needs a unique `key`.** Without it, AnimatePresence can't track which element left.
- **`mode="wait"` blocks the enter animation.** If exit is slow, the UI feels unresponsive. Keep exits short (150–200ms).
- **Nested AnimatePresence** is fragile. Prefer a single AnimatePresence at the route/page level.
- **Exit animations don't fire on page navigation** in non-SPA contexts. This is a React lifecycle constraint, not a Framer Motion bug.

---

## Layout Animations

### The `layout` prop

Adding `layout` to a motion component makes it animate smoothly when its layout position or size changes. Framer Motion uses FLIP under the hood.

```jsx
<motion.div layout className={isExpanded ? "large" : "small"} />
```

This handles: reordering in lists, expanding/collapsing panels, grid rearrangement, tab indicator sliding. The actual CSS change is instant — Framer Motion measures before/after and animates the transform.

### `layoutId`: Shared Element Transitions

Elements with the same `layoutId` animate between each other across mounts/unmounts.

```jsx
// Thumbnail in grid
<motion.img layoutId={`hero-${item.id}`} src={item.thumb} />

// Full view (different component, same layoutId)
<motion.img layoutId={`hero-${item.id}`} src={item.full} />
```

Wrap in `AnimatePresence` for smooth cross-fade between the old and new element.

### Layout animation gotchas

- **`layout` animates transforms, not actual CSS properties.** This means border-radius, box-shadow, and text can distort during the transition. Use `layout="position"` to only animate position (not size) when distortion is unacceptable.
- **`layoutScroll`** — Add to any scrollable ancestor of layout-animated elements. Without it, scroll position changes cause layout animations to misfire.
- **`layoutDependency`** — Pass a value that changes when layout should re-measure. Helps when Framer Motion misses a layout change.
- **Performance:** Layout animations measure the DOM. With many layout-animated elements (50+), measure performance. Use `layout="position"` or remove `layout` from elements that don't actually move.

---

## Gesture System

```jsx
<motion.button
  whileHover={{ scale: 1.02, backgroundColor: "#f0f0f0" }}
  whileTap={{ scale: 0.98 }}
  whileFocus={{ boxShadow: "0 0 0 3px rgba(66, 153, 225, 0.6)" }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-10%" }}
/>
```

### Drag

```jsx
<motion.div
  drag              // Enable both axes
  drag="x"          // Constrain to x axis
  dragConstraints={{ left: -100, right: 100, top: -50, bottom: 50 }}
  dragElastic={0.2}  // 0 = hard constraint, 1 = fully elastic
  dragMomentum={true}
  dragTransition={{ bounceStiffness: 300, bounceDamping: 20 }}
  onDragEnd={(e, info) => {
    if (Math.abs(info.offset.x) > 100) handleSwipe(info.offset.x);
  }}
/>
```

### `whileInView` for scroll-triggered reveals

```jsx
<motion.section
  initial={{ opacity: 0, y: 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.3, margin: "0px 0px -80px 0px" }}
  transition={{ duration: 0.5, ease: [0.2, 0, 0, 1] }}
/>
```

**`viewport.once: true`** — fires once, then stops observing. This is what you want for reveal animations. Without it, elements re-animate every time they scroll in/out.

**`viewport.amount`** — fraction of the element that must be visible (0–1). `0.3` means 30% visible before triggering.

---

## Hooks: Motion Values and Transforms

Motion values are Framer Motion's render-free reactive primitives. They update without triggering React re-renders.

### `useMotionValue`

```jsx
const x = useMotionValue(0);
// Pass to style: <motion.div style={{ x }} />
// Read: x.get()
// Set: x.set(100)
// Listen: x.on("change", v => console.log(v))
```

### `useTransform`

Derive one motion value from another with mapping:

```jsx
const scrollY = useMotionValue(0);
const opacity = useTransform(scrollY, [0, 300], [1, 0]);
const scale = useTransform(scrollY, [0, 300], [1, 0.9]);
// Opacity goes from 1→0 as scrollY goes from 0→300
```

Non-linear transforms:

```jsx
const rotate = useTransform(x, [-200, 200], [-15, 15]);
const backgroundColor = useTransform(
  x, [-200, 0, 200],
  ["#ff008c", "#7700ff", "#00d4ff"]
);
```

### `useSpring`

Wraps a motion value in spring physics:

```jsx
const x = useMotionValue(0);
const springX = useSpring(x, { stiffness: 300, damping: 30 });
// springX follows x with spring dynamics
// <motion.div style={{ x: springX }} />
```

### `useScroll`

```jsx
const { scrollY, scrollYProgress } = useScroll();
// scrollY — absolute scroll position (pixels)
// scrollYProgress — 0 to 1 normalized progress

// Target a specific container:
const { scrollYProgress } = useScroll({
  target: containerRef,
  offset: ["start end", "end start"]
});
```

### Composing hooks (parallax example)

```jsx
function ParallaxHero() {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, -150]);
  const opacity = useTransform(scrollY, [0, 300], [1, 0]);

  return (
    <motion.div style={{ y, opacity }}>
      <h1>Hero Content</h1>
    </motion.div>
  );
}
```

---

## Spring Physics Configuration

Springs are the default transition type for physical values (x, y, scale, rotate). Duration-based transitions are the default for non-physical values (opacity, color).

### Presets and tuning

```jsx
// Snappy UI feedback
transition={{ type: "spring", stiffness: 400, damping: 30 }}

// Smooth settle (modal open)
transition={{ type: "spring", stiffness: 250, damping: 25 }}

// Bouncy (playful UI, card flip)
transition={{ type: "spring", stiffness: 200, damping: 15 }}

// Overdamped (no bounce, still springy feel)
transition={{ type: "spring", stiffness: 300, damping: 40 }}

// Quick switch (toggle, tab indicator)
transition={{ type: "spring", stiffness: 500, damping: 35 }}
```

| Param | What it controls | Range guidance |
|---|---|---|
| `stiffness` | How fast the spring moves toward target | 100–600 typical. Higher = faster. |
| `damping` | How quickly oscillation settles | 10–50 typical. Lower = bouncier. |
| `mass` | Inertia of the animated value | 0.5–3. Higher = heavier/slower. Usually leave at 1. |
| `velocity` | Initial velocity (units/sec) | Auto-detected from gestures. Set manually for chained animations. |
| `restDelta` | Distance threshold to "snap" to final value | Default 0.01. Lower for precision animations. |
| `restSpeed` | Speed threshold to "snap" | Default 0.01. |

### Duration-based spring (hybrid)

```jsx
// When you want spring feel but need predictable duration
transition={{ type: "spring", duration: 0.4, bounce: 0.2 }}
// bounce: 0 = no bounce (critically damped), 1 = maximum bounce
```

---

## Reduced Motion

```jsx
import { useReducedMotion } from "framer-motion";

function Card() {
  const prefersReduced = useReducedMotion();

  return (
    <motion.div
      initial={prefersReduced ? false : { opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={prefersReduced
        ? { duration: 0 }
        : { type: "spring", stiffness: 300, damping: 25 }
      }
    />
  );
}
```

Or globally with `MotionConfig`:

```jsx
import { MotionConfig, useReducedMotion } from "framer-motion";

function App() {
  const reduced = useReducedMotion();
  return (
    <MotionConfig reducedMotion="user">
      {/* All descendants respect system preference */}
      <Layout />
    </MotionConfig>
  );
}
```

`reducedMotion` values: `"user"` (respect system setting), `"always"` (force reduced), `"never"` (ignore setting — don't use this in production).

---

## Production Patterns

### Tab indicator that slides between tabs

```jsx
{tabs.map(tab => (
  <button key={tab.id} onClick={() => setActive(tab.id)}>
    {tab.label}
    {active === tab.id && (
      <motion.div
        layoutId="tab-indicator"
        className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500"
        transition={{ type: "spring", stiffness: 400, damping: 30 }}
      />
    )}
  </button>
))}
```

### List reorder with exit

```jsx
<AnimatePresence mode="popLayout">
  {items.map(item => (
    <motion.div
      key={item.id}
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ type: "spring", stiffness: 350, damping: 25 }}
    >
      {item.content}
    </motion.div>
  ))}
</AnimatePresence>
```

### Staggered card grid reveal

```jsx
const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.05 } }
};
const card = {
  hidden: { opacity: 0, y: 12, scale: 0.97 },
  show: {
    opacity: 1, y: 0, scale: 1,
    transition: { type: "spring", stiffness: 300, damping: 24 }
  }
};

<motion.div
  className="grid grid-cols-3 gap-4"
  variants={container}
  initial="hidden"
  whileInView="show"
  viewport={{ once: true, amount: 0.2 }}
>
  {cards.map(c => <motion.div key={c.id} variants={card} />)}
</motion.div>
```

---

## Failure Modes and Gotchas

| Issue | What happens | Fix |
|---|---|---|
| Missing `key` on AnimatePresence children | Exit animations don't fire, elements teleport | Always use unique, stable keys |
| `layout` on many elements | Jank from DOM measurement overhead | Use `layout="position"` or remove from static elements |
| `whileInView` without `once: true` | Elements re-animate on every scroll pass | Add `viewport={{ once: true }}` for reveal effects |
| Spring animation feels "mushy" | Stiffness too low relative to damping | Increase stiffness or reduce damping |
| `layoutId` across different parent trees | Animation path goes through origin (0,0) | Ensure shared layout ancestor, or use `LayoutGroup` |
| `exit` without `AnimatePresence` | Nothing happens — element just unmounts | Wrap conditional renders in `AnimatePresence` |
| Motion values in dependency arrays | Infinite re-render loops | Never put motion values in `useEffect` deps; use `.on("change")` |
| `initial={false}` forgotten | Mount animation plays on page load when not wanted | Set `initial={false}` to skip first-render animation |
| Style prop type mismatch | `x: "100px"` vs `x: 100` — string values don't spring | Use numbers for physical properties, strings for CSS values |
