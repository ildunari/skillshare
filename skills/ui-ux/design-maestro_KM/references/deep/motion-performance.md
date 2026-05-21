<!-- Deep reference: motion performance architecture, spring physics, Bento 2.0, perpetual motion. Not auto-loaded. -->
<!-- Load when: building animated dashboards, Bento grids, perpetual micro-animations, or when any animation involves live/looping state. -->
<!-- Also load when: debugging animation jank, choosing between GSAP and Framer, or when a design needs to feel "alive." -->

# Motion Performance Architecture

> This file is about two things: how to build animations that don't break, and why certain motion patterns feel premium while others feel generated. Every section pairs design intent with implementation.

---

## When to Load This File

You should have reached for this file if any of the following describe your task:

- The interface has elements that animate continuously (live metrics, status indicators, carousels, activity feeds)
- You're building a Bento grid or SaaS feature showcase
- A component uses `useState` to drive animation and you're about to do that
- The brief says anything like: "make it feel alive," "show data updating in real time," "premium SaaS," "show activity," "show the product working"
- You're about to mix GSAP and Framer Motion in the same file
- You're building a dashboard with more than one animated element
- The design needs a typewriter, an auto-sorting list, a pulsing status dot, or a seamless carousel

If you're here because you just need a quick fade-in or hover spring — you don't need this file. That's in `references/motion-library.md`.

---

## Part 1: Framer Motion Performance Architecture

### 1.1 — useMotionValue vs useState for Continuous Animation

**Context trigger.** You'll need this whenever a UI element responds to mouse position, runs a continuous loop tied to a value (magnetic buttons, parallax, cursor-following elements), or needs to update faster than React's render cycle allows.

**The anti-pattern** is reaching for `useState` because it's familiar:

```jsx
// ❌ WRONG — useState causes re-renders on every mouse move
// On a 120hz screen this is 120 setState calls per second
// The parent re-renders, its siblings re-render, the tree churns
const [mouseX, setMouseX] = useState(0);
const [mouseY, setMouseY] = useState(0);

<div
  onMouseMove={(e) => {
    setMouseX(e.clientX);
    setMouseY(e.clientY);
  }}
  style={{ transform: `translate(${mouseX * 0.1}px, ${mouseY * 0.1}px)` }}
/>
```

**Why this destroys performance.** Every `setState` call schedules a React re-render. On mouse move events, this fires continuously. React batches some of this, but on complex trees it causes visual stutter, dropped frames, and on mobile it's catastrophic. The component and all its children reconcile on every pixel the mouse moves.

**The correct pattern** — `useMotionValue` + `useTransform` runs entirely outside React's render cycle, updating the DOM directly via Framer Motion's internal animation engine:

```jsx
// ✅ CORRECT — motion values bypass React's render cycle entirely
import { motion, useMotionValue, useTransform, useSpring } from "motion/react";

function MagneticButton({ children }) {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  // useTransform maps motion values to output values without re-rendering
  const translateX = useTransform(mouseX, [-50, 50], [-8, 8]);
  const translateY = useTransform(mouseY, [-50, 50], [-8, 8]);

  // Spring wraps the transform to add physical bounce
  const springX = useSpring(translateX, { stiffness: 300, damping: 30 });
  const springY = useSpring(translateY, { stiffness: 300, damping: 30 });

  function handleMouseMove(e: React.MouseEvent) {
    const rect = e.currentTarget.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    // Update motion values — this does NOT trigger a re-render
    mouseX.set(e.clientX - centerX);
    mouseY.set(e.clientY - centerY);
  }

  function handleMouseLeave() {
    // Spring back to 0 with physics
    mouseX.set(0);
    mouseY.set(0);
  }

  return (
    <motion.button
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{ x: springX, y: springY }}
      className="magnetic-button"
    >
      {children}
    </motion.button>
  );
}
```

**Design reasoning.** Magnetic buttons feel premium because they break the assumption that UI elements are fixed. The subtle pull toward the cursor communicates that the interface is aware of you. The spring-back is critical — without it, the button stays offset and looks broken. The spring physics make it feel like a physical object with weight.

**Artifact translation (CSS only — no Framer available):**

```css
/* Approximate version using CSS custom properties + JS */
/* Not as smooth as Framer, but acceptable for artifacts */
.magnetic-btn {
  transition: transform 0.15s cubic-bezier(0.16, 1, 0.3, 1);
}
```

```js
// In artifact, use direct DOM mutation — never setState for mouse tracking
const btn = document.querySelector('.magnetic-btn');
btn.addEventListener('mousemove', (e) => {
  const rect = btn.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width - 0.5) * 12;
  const y = ((e.clientY - rect.top) / rect.height - 0.5) * 12;
  // Direct DOM style mutation — zero React involvement
  btn.style.transform = `translate(${x}px, ${y}px)`;
});
btn.addEventListener('mouseleave', () => {
  btn.style.transform = 'translate(0px, 0px)';
});
```

---

### 1.2 — Component Isolation for Perpetual Loops

**Context trigger.** Any animation that runs forever — a pulsing dot, a scrolling carousel, a looping typewriter, a floating card — must be isolated in its own component. This is the single most important rule for dashboards that feel alive without feeling janky.

**Why isolation matters.** A perpetual animation using React state schedules a re-render every animation frame. If that state lives in a parent component, every sibling gets re-rendered too — even completely static ones. A dashboard with three perpetual animations sharing a parent is three continuous re-render loops hitting the entire component tree simultaneously.

**The anti-pattern:**

```jsx
// ❌ WRONG — perpetual loop in a parent that also renders static siblings
function Dashboard() {
  const [pulseActive, setPulseActive] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => setPulseActive(p => !p), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <MetricsCard />   {/* re-renders every second — it didn't change */}
      <ChartCard />     {/* re-renders every second — it didn't change */}
      <StatusDot active={pulseActive} />  {/* only this should update */}
      <TeamList />      {/* re-renders every second — it didn't change */}
    </div>
  );
}
```

**The correct pattern** — isolate the animation entirely, use CSS or Framer's internal engine, never bubble state upward:

```jsx
// ✅ CORRECT — perpetual motion is fully self-contained
// Parent never knows this component is animating
const StatusDot = React.memo(function StatusDot({ status }: { status: "live" | "idle" }) {
  return (
    <div className="relative flex items-center gap-2">
      {/* CSS animation — zero JS, zero re-renders, GPU composited */}
      <span className="relative flex h-2.5 w-2.5">
        {status === "live" && (
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
        )}
        <span className={`relative inline-flex h-2.5 w-2.5 rounded-full ${
          status === "live" ? "bg-emerald-500" : "bg-zinc-400"
        }`} />
      </span>
      <span className="text-xs text-zinc-500">{status === "live" ? "Live" : "Idle"}</span>
    </div>
  );
});
// React.memo ensures this doesn't re-render when parent's unrelated state changes

// ✅ If you need JS-driven perpetual animation, isolate its state completely:
const AnimatedCounter = React.memo(function AnimatedCounter({ target }: { target: number }) {
  // This state only causes THIS component to re-render, not its siblings
  const [displayed, setDisplayed] = useState(0);

  useEffect(() => {
    let frame: number;
    let start: number;
    const duration = 1200;

    function step(timestamp: number) {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      setDisplayed(Math.floor(eased * target));
      if (progress < 1) frame = requestAnimationFrame(step);
    }

    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame); // critical cleanup
  }, [target]);

  return <span className="font-mono tabular-nums">{displayed.toLocaleString()}</span>;
});
```

**Design reasoning.** Perpetual motion makes a dashboard feel like a real system rather than a screenshot. The pulse dot communicates "this is connected." The animated counter communicates "this number is meaningful." But uncontrolled re-renders make the interface feel sluggish even when the visual result looks fine. Isolation is what separates "a dashboard that shows live data" from "a dashboard that feels live."

---

### 1.3 — Stagger Orchestration: The Tree Contract

**Context trigger.** Stagger reveals are the default entrance for any list, card grid, or feature row. They look great. They also break silently if the architecture is wrong — the animation fires but the stagger disappears, all children mount at once.

**The rule:** Parent variants (`staggerChildren`) and their children variants must exist in the same Client Component. If you fetch data asynchronously and then try to stagger the results, the stagger will not work because the children mount after the parent's initial animation cycle completes.

**The anti-pattern:**

```jsx
// ❌ WRONG — async data fetch inside the motion parent
// The parent animates on mount. Data arrives 400ms later.
// Children mount after the stagger window has already closed.
async function FeatureList() {
  const features = await fetchFeatures(); // Server Component data fetch

  return (
    <motion.ul variants={container} initial="hidden" animate="show">
      {features.map(f => (
        <motion.li key={f.id} variants={item}>{f.name}</motion.li>
      ))}
    </motion.ul>
  );
}
```

**The correct pattern** — pass data as props into a dedicated client wrapper:

```jsx
// ✅ CORRECT — data flows in as props; the client component owns the animation
// Server Component (fetches data, passes to client)
async function FeatureSection() {
  const features = await fetchFeatures();
  return <AnimatedFeatureList features={features} />;
}

// Client Component (owns all animation state)
"use client";
const container = {
  hidden: { opacity: 0 },
  show: { transition: { staggerChildren: 0.09, delayChildren: 0.1 } }
};
const item = {
  hidden: { opacity: 0, y: 16, filter: "blur(4px)" },
  show: {
    opacity: 1, y: 0, filter: "blur(0px)",
    transition: { type: "spring", stiffness: 260, damping: 24 }
  }
};

function AnimatedFeatureList({ features }: { features: Feature[] }) {
  return (
    <motion.ul variants={container} initial="hidden" animate="show" className="space-y-3">
      {features.map((feature) => (
        <motion.li key={feature.id} variants={item} className="feature-item">
          <FeatureCard feature={feature} />
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

**Adding blur to the stagger.** The `filter: "blur(4px)"` → `filter: "blur(0px)"` on item entrance is a subtle premium touch. Items don't just fade in — they crystallize into focus. This is a Vercel/Linear-style reveal. Don't use it for dense lists (too much blur creates visual chaos), but for feature showcases and hero content it adds significant polish.

---

## Part 2: Spring Physics Canon

### 2.1 — The Baseline and Why It Exists

Spring physics feel premium because they mimic how real physical objects move — they overshoot slightly, correct, and settle. CSS easing curves like `ease-out` produce mathematically smooth deceleration that reads as "computer-made." Springs read as "physical."

**The premium baseline:**

```js
// Premium feel — weighted, decisive, settles cleanly
{ type: "spring", stiffness: 100, damping: 20 }

// Snappy/interactive — buttons, toggles, quick UI responses  
{ type: "spring", stiffness: 260, damping: 24 }

// Bouncy/playful — notification badges, success states, gamified UI
{ type: "spring", stiffness: 400, damping: 15 }

// Slow/weighty — modals, drawers, large layout transitions
{ type: "spring", stiffness: 60, damping: 18 }
```

**What each parameter actually does:**

- **`stiffness`** — how fast the spring tries to reach its target. High stiffness = snappy response. Low stiffness = sluggish start, heavy feel.
- **`damping`** — how quickly oscillation dies. Low damping = bouncy, overshoots multiple times. High damping = no bounce, more like ease-out. Critically: if damping is too high relative to stiffness, it degrades to a linear ease and loses the spring character entirely.
- **`mass`** — adds virtual weight. Rarely needed, but useful for large elements that should feel heavy. Default is 1.

**Calibration guide by interaction type:**

| Interaction | stiffness | damping | Design intent |
|---|---|---|---|
| Page-level modals, drawers | 60–80 | 18–22 | Heavy, considered, premium |
| Card hover tilt | 100–150 | 20–25 | Responsive but not jumpy |
| Button press / CTA | 260–300 | 22–26 | Snappy, confident |
| Notification badge pop | 380–420 | 14–18 | Attention-grabbing, celebratory |
| List reorder (layoutId) | 120–160 | 24–28 | Smooth, legible, doesn't distract |
| Magnetic button settle | 280–320 | 28–32 | Pulls naturally, spring-back feels physical |

**CSS artifact equivalent for spring feel:**

```css
/* No true springs in CSS — approximate with cubic-bezier */

/* Snappy (approximates high stiffness spring) */
transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);

/* Weighted/premium (approximates low stiffness spring) */
transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
/* The 1.56 value causes slight overshoot — this is what makes it spring-like */

/* Bouncy (approximates low damping spring) */
transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

---

## Part 3: GSAP / Framer Separation Contract

**The rule.** Never use GSAP and Framer Motion in the same component tree. This is not a preference — they fight over control of the same DOM nodes and produce unpredictable behavior including animation cancellation, race conditions, and transform conflicts.

**When to use Framer Motion:**
- Any component inside a React render tree
- UI transitions: modals, drawers, tabs, popovers
- List animations, layout transitions, page navigation
- Gesture-driven interactions (drag, swipe, magnetic)
- Stagger reveals on component mount
- Bento grids, card animations, perpetual micro-motion

**When to use GSAP:**
- Full-page scrolltelling where scroll position drives animation timeline
- Canvas or WebGL sequences where GSAP's timeline control is needed
- Complex multi-step choreography with precise timing across unrelated DOM elements
- When ScrollTrigger is the animation driver (GSAP's ScrollTrigger has no Framer equivalent)

**The isolation pattern for GSAP in a React app:**

```jsx
// ✅ CORRECT — GSAP lives in an isolated useEffect, cleans up on unmount
// It touches its own ref, never intersecting with Framer-animated siblings
"use client";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

function HeroScrollSequence() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // All animations scoped to containerRef
      gsap.timeline({
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top top",
          end: "+=200%",
          scrub: 1,
          pin: true,
        }
      })
        .to(".hero-text", { y: -80, opacity: 0, duration: 1 })
        .from(".product-shot", { scale: 0.8, opacity: 0, duration: 1 });
    }, containerRef);

    return () => ctx.revert(); // CRITICAL: cleans up all ScrollTrigger instances
  }, []);

  return (
    <div ref={containerRef} className="gsap-section">
      {/* Framer Motion components must NOT appear here or in any children */}
      <div className="hero-text">...</div>
      <div className="product-shot">...</div>
    </div>
  );
}

// Elsewhere in the same page — Framer Motion can be used freely
// as long as it's outside the HeroScrollSequence component tree
function FeatureCards() {
  return (
    <motion.div variants={container} initial="hidden" animate="show">
      {/* Framer is fine here — no GSAP anywhere in this subtree */}
    </motion.div>
  );
}
```

---

## Part 4: Bento 2.0 Architecture

### Design Philosophy

**Context trigger.** Bento grids are the right choice when you need to showcase multiple product capabilities simultaneously without the user having to scroll through them linearly. The format communicates richness — this product does more than one thing, and all of it is worth seeing. You'll know it's the right format when the brief says: "show the features," "product showcase," "feature overview," "landing page feature section."

**What separates Bento 2.0 from generic card grids:**

1. **Asymmetric layout** — cards span different column and row counts. Not 3 equal cards. Not 2 equal cards. An asymmetric grid where the most important capability gets the most space.
2. **Perpetual motion** — every card has something moving inside it, always. The dashboard feels like a live system.
3. **Spring physics throughout** — every state transition uses spring, not linear easing.
4. **Labels outside cards** — titles and descriptions sit below cards, not inside them. This maintains card as "display surface" and keeps the content clean.
5. **One design language** — same radius, same shadow style, same typography scale across all cards.

**The baseline grid structure:**

```jsx
// Recommended layout: 2 rows
// Row 1: wide card (span 2) + tall card (span 1) — 3 col total
// Row 2: medium card + medium card — 2 col total (or 3 with varied spans)

<div className="grid grid-cols-3 gap-4 max-w-5xl mx-auto">
  {/* Row 1 */}
  <div className="col-span-2 rounded-[2rem] bg-white border border-slate-200/60 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] p-8 min-h-[280px]">
    {/* Wide card — most important feature */}
  </div>
  <div className="col-span-1 rounded-[2rem] bg-white border border-slate-200/60 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] p-8 min-h-[280px]">
    {/* Tall card — second feature */}
  </div>

  {/* Row 2 */}
  <div className="col-span-1 rounded-[2rem] bg-white border border-slate-200/60 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] p-8 min-h-[200px]">
    {/* Medium card */}
  </div>
  <div className="col-span-2 rounded-[2rem] bg-white border border-slate-200/60 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)] p-8 min-h-[200px]">
    {/* Wide card — fourth feature */}
  </div>
</div>

{/* Labels: OUTSIDE the grid, below each card */}
<div className="grid grid-cols-3 gap-4 max-w-5xl mx-auto mt-4">
  <div className="col-span-2">
    <p className="text-sm font-medium text-zinc-800 tracking-tight">Feature name</p>
    <p className="text-xs text-zinc-400 mt-0.5">One line description</p>
  </div>
  {/* etc. */}
</div>
```

**The diffusion shadow** used above (`shadow-[0_20px_40px_-15px_rgba(0,0,0,0.06)]`) is a specific recipe. It's very wide, very soft, and barely visible. This creates depth without the card looking like it's floating — it looks like it's resting. Generic card shadows (`shadow-md`, `shadow-lg`) are too hard, too close, and make cards look like paper cutouts.

---

### Archetype 1: The Intelligent List

**Design intent.** A vertical list of items that auto-sorts itself using spring physics. Communicates "AI prioritization," "live feed," or "dynamic ranking." The items swap positions smoothly — not jumping, not fading, but physically sliding while maintaining identity via `layoutId`.

**When to use this archetype.** When showcasing: task prioritization, activity feeds, notification streams, AI recommendations, leaderboards, real-time rankings. Don't use it for static content — the movement needs to mean something.

**Anti-pattern.** A static list with occasional CSS fade transitions looks like a loading state gone wrong. The magic of this pattern is that items *move* — the user tracks where each item went.

```jsx
"use client";
import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";

type Task = { id: string; label: string; priority: number; tag: string; };

const INITIAL_TASKS: Task[] = [
  { id: "t1", label: "Review Q3 analysis", priority: 3, tag: "Analytics" },
  { id: "t2", label: "Deploy staging environment", priority: 1, tag: "Engineering" },
  { id: "t3", label: "Customer onboarding call", priority: 2, tag: "Sales" },
  { id: "t4", label: "Update API documentation", priority: 4, tag: "Docs" },
  { id: "t5", label: "Security audit review", priority: 5, tag: "Security" },
];

export const IntelligentList = React.memo(function IntelligentList() {
  const [tasks, setTasks] = useState(INITIAL_TASKS);

  useEffect(() => {
    const interval = setInterval(() => {
      setTasks(prev => {
        const shuffled = [...prev];
        // Swap two random adjacent items — feels like a priority shift, not chaos
        const i = Math.floor(Math.random() * (shuffled.length - 1));
        [shuffled[i], shuffled[i + 1]] = [shuffled[i + 1], shuffled[i]];
        return shuffled;
      });
    }, 2200); // Interval long enough to read the list between swaps
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-1.5">
      <AnimatePresence mode="popLayout">
        {tasks.map((task, index) => (
          <motion.div
            key={task.id}
            layoutId={task.id}           // This is what enables smooth position swapping
            layout                       // Tells Framer to animate layout changes
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 8 }}
            transition={{ type: "spring", stiffness: 200, damping: 28 }}
            className="flex items-center justify-between px-3 py-2.5 rounded-xl bg-zinc-50 hover:bg-zinc-100 transition-colors cursor-default group"
          >
            <div className="flex items-center gap-3 min-w-0">
              <span className="text-[10px] font-mono text-zinc-300 w-4 shrink-0">{index + 1}</span>
              <span className="text-sm text-zinc-700 truncate">{task.label}</span>
            </div>
            <span className="text-[10px] font-medium text-zinc-400 bg-zinc-100 group-hover:bg-zinc-200 px-2 py-0.5 rounded-full shrink-0 ml-2 transition-colors">
              {task.tag}
            </span>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
});
```

**Key details.** `mode="popLayout"` on `AnimatePresence` tells Framer to immediately remove exiting elements from the layout so they don't hold space while other items are rearranging. `layoutId` must be unique and stable — it's the item's identity across renders. The spring on the layout transition (`stiffness: 200, damping: 28`) is deliberately softer than a button spring — you want the movement to be readable, not startling.

**CSS artifact equivalent** — no `layoutId` available, simulate with position + transition:

```js
// In artifacts, use absolute positioning + CSS transitions
// Sort the array, update data-index attribute, CSS handles the rest
items.forEach((item, i) => {
  item.style.transform = `translateY(${i * 52}px)`; // 52px = item height + gap
  item.style.transition = 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
});
```

---

### Archetype 2: Command Input / Typewriter

**Design intent.** A search bar or AI input field that cycles through example prompts, demonstrating product capability before the user has typed anything. Communicates "this product is powerful and specific" by showing concrete, realistic prompts rather than placeholder text.

**When to use.** AI products, search-first interfaces, command palettes, any product where the primary interaction is text input and the capability isn't obvious. The typewriter makes the empty state into a demonstration.

**Anti-pattern.** Static placeholder text like "Ask me anything..." or "Search..." communicates nothing about what the product can actually do. A typewriter cycling through specific, realistic prompts is free onboarding.

```jsx
"use client";
import React, { useState, useEffect, useRef } from "react";

const EXAMPLE_PROMPTS = [
  "Summarize last week's team standup notes",
  "Draft a response to the Acme proposal",
  "Find all open issues tagged critical",
  "Compare Q2 vs Q3 conversion rates",
  "Schedule a review for the Henderson account",
];

export const CommandInput = React.memo(function CommandInput() {
  const [displayed, setDisplayed] = useState("");
  const [promptIndex, setPromptIndex] = useState(0);
  const [phase, setPhase] = useState<"typing" | "pause" | "erasing">("typing");
  const [isFocused, setIsFocused] = useState(false);
  const charIndex = useRef(0);

  useEffect(() => {
    if (isFocused) return; // Stop animating when user is interacting

    const currentPrompt = EXAMPLE_PROMPTS[promptIndex];

    if (phase === "typing") {
      if (charIndex.current < currentPrompt.length) {
        const timeout = setTimeout(() => {
          setDisplayed(currentPrompt.slice(0, charIndex.current + 1));
          charIndex.current++;
        }, 38 + Math.random() * 24); // Varied speed feels human
        return () => clearTimeout(timeout);
      } else {
        const timeout = setTimeout(() => setPhase("pause"), 1800);
        return () => clearTimeout(timeout);
      }
    }

    if (phase === "pause") {
      setPhase("erasing");
    }

    if (phase === "erasing") {
      if (charIndex.current > 0) {
        const timeout = setTimeout(() => {
          charIndex.current--;
          setDisplayed(currentPrompt.slice(0, charIndex.current));
        }, 18); // Erase faster than type — natural asymmetry
        return () => clearTimeout(timeout);
      } else {
        setPromptIndex((i) => (i + 1) % EXAMPLE_PROMPTS.length);
        setPhase("typing");
      }
    }
  }, [phase, promptIndex, displayed, isFocused]);

  return (
    <div className="relative">
      <div className={`
        flex items-center gap-3 px-4 py-3 rounded-2xl border transition-all duration-200
        ${isFocused
          ? "border-zinc-400 bg-white shadow-[0_0_0_4px_rgba(0,0,0,0.04)]"
          : "border-zinc-200 bg-zinc-50"}
      `}>
        {/* Search icon — inline SVG for artifact compatibility */}
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="text-zinc-400 shrink-0">
          <circle cx="7" cy="7" r="4.5" stroke="currentColor" strokeWidth="1.5"/>
          <path d="M10.5 10.5L13 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>

        <div className="flex-1 relative">
          <input
            className="w-full text-sm text-zinc-800 bg-transparent outline-none placeholder-transparent"
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
          />
          {/* Animated placeholder — only shows when input is empty and unfocused */}
          {!isFocused && (
            <div className="absolute inset-0 flex items-center pointer-events-none">
              <span className="text-sm text-zinc-400">{displayed}</span>
              {/* Blinking cursor */}
              <span className="inline-block w-px h-4 bg-zinc-400 ml-px animate-[blink_0.9s_step-end_infinite]" />
            </div>
          )}
        </div>

        {/* Processing shimmer — shows during "pause" phase */}
        {phase === "pause" && (
          <div className="flex gap-1 shrink-0">
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                className="w-1.5 h-1.5 rounded-full bg-zinc-300 animate-bounce"
                style={{ animationDelay: `${i * 0.15}s` }}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
});
```

---

### Archetype 3: Live Status with Breathing Indicators

**Design intent.** A scheduling or status interface that communicates activity through subtle, continuous motion. Status dots breathe (scale pulse), notifications appear with spring physics and auto-dismiss, time slots show occupancy.

**When to use.** Calendar integration demos, system health dashboards, team availability indicators, deployment status, any interface where the core value is knowing "what's happening right now."

**Anti-pattern.** Static colored dots. A green dot and a red dot tell you current state but not activity. Breathing communicates "actively monitoring." The difference between a light that's on and a heartbeat monitor.

```jsx
"use client";
import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";

type Status = "online" | "busy" | "away" | "offline";

const STATUS_CONFIG: Record<Status, { color: string; ping: string; label: string }> = {
  online:  { color: "bg-emerald-500", ping: "bg-emerald-400", label: "Online" },
  busy:    { color: "bg-rose-500",    ping: "bg-rose-400",    label: "In a meeting" },
  away:    { color: "bg-amber-400",   ping: "bg-amber-300",   label: "Away" },
  offline: { color: "bg-zinc-400",    ping: "bg-zinc-300",    label: "Offline" },
};

const BreathingDot = React.memo(function BreathingDot({ status }: { status: Status }) {
  const config = STATUS_CONFIG[status];
  const isActive = status !== "offline";

  return (
    <span className="relative flex h-2.5 w-2.5">
      {/* Ping animation — only for active statuses */}
      {isActive && (
        <span className={`animate-ping absolute inline-flex h-full w-full rounded-full ${config.ping} opacity-60`} />
      )}
      <span className={`relative inline-flex h-2.5 w-2.5 rounded-full ${config.color}`} />
    </span>
  );
});

// Notification badge with spring pop + auto-dismiss
const NotificationBadge = React.memo(function NotificationBadge({
  message, onDismiss
}: { message: string; onDismiss: () => void }) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, 3000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.7, y: 8 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.85, y: -4 }}
      transition={{ type: "spring", stiffness: 400, damping: 20 }} // Deliberate overshoot for attention
      className="absolute -top-2 -right-2 bg-zinc-900 text-white text-[10px] font-medium px-2 py-1 rounded-full whitespace-nowrap shadow-lg z-10"
    >
      {message}
    </motion.div>
  );
});

export function LiveStatusCard() {
  const [notification, setNotification] = useState<string | null>(null);
  const [statuses, setStatuses] = useState<Record<string, Status>>({
    "Alex K.":   "online",
    "Maya R.":   "busy",
    "Jordan T.": "away",
    "Sam L.":    "online",
  });

  // Simulate status changes
  useEffect(() => {
    const statusValues: Status[] = ["online", "busy", "away", "offline"];
    const interval = setInterval(() => {
      const names = Object.keys(statuses);
      const randomName = names[Math.floor(Math.random() * names.length)];
      const newStatus = statusValues[Math.floor(Math.random() * statusValues.length)];
      setStatuses(prev => ({ ...prev, [randomName]: newStatus }));
      setNotification(`${randomName} is now ${STATUS_CONFIG[newStatus].label}`);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative">
      <AnimatePresence>
        {notification && (
          <NotificationBadge
            key={notification + Date.now()} // Force remount on each new notification
            message={notification}
            onDismiss={() => setNotification(null)}
          />
        )}
      </AnimatePresence>

      <div className="space-y-3">
        {Object.entries(statuses).map(([name, status]) => (
          <div key={name} className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <BreathingDot status={status} />
              <span className="text-sm text-zinc-700">{name}</span>
            </div>
            <span className="text-xs text-zinc-400">{STATUS_CONFIG[status].label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

### Archetype 4: The Data Stream (Seamless Infinite Carousel)

**Design intent.** A horizontal strip of data points, metrics, or cards scrolling continuously. Communicates activity volume, breadth of integrations, or data richness. The scroll is ambient — present but not demanding attention.

**When to use.** Integration logos, recent activity feeds, metric tickers, partner logos, event streams. Works for any content where "there's a lot of it" is part of the message.

**Anti-pattern.** A carousel with prev/next buttons. This is for ambient content — the user doesn't need to control it. Arrows imply the user should interact; that's not the intent here.

**The seamless loop trick.** To avoid a visible jump when the carousel resets, duplicate the content array and animate to exactly `-50%` — at that point, you're showing the duplicate and the original is exactly behind it. Resetting to `0%` is invisible.

```jsx
"use client";
import React, { useRef } from "react";
import { motion, useAnimationFrame, useMotionValue } from "motion/react";

type DataPoint = { label: string; value: string; delta: string; positive: boolean };

const DATA_STREAM: DataPoint[] = [
  { label: "Revenue",      value: "$47.2K",   delta: "+12.4%", positive: true },
  { label: "Active Users", value: "3,841",    delta: "+8.7%",  positive: true },
  { label: "Churn Rate",   value: "1.8%",     delta: "-0.3%",  positive: true },
  { label: "MRR",          value: "$124.6K",  delta: "+6.2%",  positive: true },
  { label: "LTV",          value: "$2,847",   delta: "+22.1%", positive: true },
  { label: "CAC",          value: "$184",     delta: "-9.4%",  positive: true },
  { label: "NPS Score",    value: "72",       delta: "+4pts",  positive: true },
  { label: "Support Vol.", value: "234",      delta: "+18.2%", positive: false },
];

export const DataStream = React.memo(function DataStream() {
  const x = useMotionValue(0);
  const SPEED = 0.4; // px per frame — slower feels more ambient

  // useAnimationFrame runs outside React render cycle
  useAnimationFrame(() => {
    const current = x.get();
    const newX = current - SPEED;
    // Reset at -50% to create seamless loop
    if (Math.abs(newX) >= 50) {
      x.set(0);
    } else {
      x.set(newX);
    }
  });

  // Duplicate the data for the seamless loop
  const doubled = [...DATA_STREAM, ...DATA_STREAM];

  return (
    <div className="overflow-hidden w-full">
      <motion.div
        className="flex gap-3 w-max"
        style={{ x: `${x.get()}%` }} // Note: use inline style with motion value
      >
        {doubled.map((point, i) => (
          <div
            key={i}
            className="shrink-0 px-4 py-3 rounded-xl border border-zinc-200/80 bg-zinc-50"
          >
            <p className="text-[10px] text-zinc-400 font-medium uppercase tracking-wider">{point.label}</p>
            <div className="flex items-baseline gap-1.5 mt-0.5">
              <span className="text-base font-semibold text-zinc-800 tabular-nums">{point.value}</span>
              <span className={`text-[10px] font-medium ${point.positive ? "text-emerald-500" : "text-rose-500"}`}>
                {point.delta}
              </span>
            </div>
          </div>
        ))}
      </motion.div>
    </div>
  );
});
```

**CSS artifact version** using pure CSS animation:

```css
@keyframes scroll-left {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

.stream-track {
  display: flex;
  gap: 12px;
  width: max-content;
  animation: scroll-left 30s linear infinite;
}

.stream-track:hover {
  animation-play-state: paused; /* Pause on hover — nice touch */
}
```

---

### Archetype 5: Focus Mode (Contextual Document Highlight)

**Design intent.** A text document where a section gets highlighted (as if being analyzed) and a floating action toolbar appears alongside it. Communicates "AI is reading and acting on your content." Relevant for document editors, writing tools, research platforms, or any product that processes text.

**When to use.** AI writing assistants, document analysis tools, contract review, email drafting, any product where the core loop is "input text → AI responds." The animation makes the capability visceral.

**Anti-pattern.** Just showing a text document with a chat input beside it. The staggered highlight + toolbar float makes the AI feel present and active, not just adjacent.

```jsx
"use client";
import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";

const DOC_PARAGRAPHS = [
  { id: "p1", text: "The acquisition terms outlined in Section 4.2 require unanimous board approval before any transfer of intellectual property assets exceeding $2M in valuation." },
  { id: "p2", text: "Indemnification clauses in Schedule B extend to all subsidiary entities as defined by the parent company's organizational chart as of the effective date." },
  { id: "p3", text: "Governing law shall be interpreted under Delaware statute, with exclusive jurisdiction granted to courts in New Castle County." },
];

const TOOLBAR_ACTIONS = ["Summarize", "Flag Risk", "Compare", "Suggest Edit"];

export const FocusMode = React.memo(function FocusMode() {
  const [activeParagraph, setActiveParagraph] = useState<string | null>(null);
  const [showToolbar, setShowToolbar] = useState(false);
  const [toolbarAnchor, setToolbarAnchor] = useState(0); // y position

  useEffect(() => {
    const cycle = async () => {
      for (let i = 0; i < DOC_PARAGRAPHS.length; i++) {
        // Highlight paragraph
        setActiveParagraph(DOC_PARAGRAPHS[i].id);
        setToolbarAnchor(i);
        // Toolbar appears 400ms after highlight
        setTimeout(() => setShowToolbar(true), 400);

        await new Promise(r => setTimeout(r, 3000));

        // Clear before next
        setShowToolbar(false);
        await new Promise(r => setTimeout(r, 300));
        setActiveParagraph(null);
        await new Promise(r => setTimeout(r, 400));
      }
    };

    const interval = setInterval(() => cycle(), DOC_PARAGRAPHS.length * 3800);
    cycle(); // Run immediately
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative font-[Georgia,serif] text-zinc-700 space-y-4 text-sm leading-relaxed">
      {DOC_PARAGRAPHS.map((para, i) => (
        <div key={para.id} className="relative">
          <motion.p
            animate={{
              backgroundColor: activeParagraph === para.id
                ? "rgba(234, 179, 8, 0.08)"
                : "rgba(0,0,0,0)",
              borderLeftColor: activeParagraph === para.id
                ? "rgba(234, 179, 8, 0.6)"
                : "rgba(0,0,0,0)",
            }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="pl-3 border-l-2 rounded-sm"
          >
            {para.text}
          </motion.p>

          {/* Floating toolbar — appears when this paragraph is active */}
          <AnimatePresence>
            {activeParagraph === para.id && showToolbar && (
              <motion.div
                initial={{ opacity: 0, y: 6, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -4, scale: 0.95 }}
                transition={{ type: "spring", stiffness: 320, damping: 26 }}
                className="absolute -bottom-10 left-3 flex items-center gap-1 bg-zinc-900 rounded-lg p-1 shadow-xl z-10"
              >
                {TOOLBAR_ACTIONS.map((action, j) => (
                  <motion.button
                    key={action}
                    initial={{ opacity: 0, scale: 0.85 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: j * 0.06, type: "spring", stiffness: 300, damping: 24 }}
                    className="text-[10px] text-zinc-300 hover:text-white hover:bg-zinc-700 px-2 py-1 rounded-md transition-colors font-sans font-medium"
                  >
                    {action}
                  </motion.button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      ))}
    </div>
  );
});
```

---

## Part 5: Perpetual Micro-Motion Patterns

### When ambient motion is right

Perpetual motion should be used when the interface needs to communicate one of these things:
- **Connected** — this system is talking to a server, data is live
- **Active** — something is being processed, monitored, or watched
- **Rich** — there's more content/data than what's visible at rest
- **Intelligent** — the product is working even when the user isn't

Do not use perpetual motion decoratively — a spinning logo or a floating card for aesthetic reasons reads as noise. Every animation should have a semantic meaning the user can intuit.

### The four ambient patterns:

**Pulse** — communicates "connected" or "live." The outer ring expands and fades while the core remains solid. `animate-ping` in Tailwind handles this with zero JS.

```css
/* Tailwind: animate-ping is already perfect for this */
/* Custom version for non-Tailwind: */
@keyframes ping {
  75%, 100% { transform: scale(2); opacity: 0; }
}
.ping { animation: ping 1.2s cubic-bezier(0, 0, 0.2, 1) infinite; }
```

**Shimmer** — communicates "loading" or "processing." A gradient sweeps across the surface.

```css
@keyframes shimmer {
  from { background-position: -200% center; }
  to   { background-position: 200% center; }
}
.shimmer {
  background: linear-gradient(90deg, transparent 25%, rgba(255,255,255,0.4) 50%, transparent 75%);
  background-size: 200% 100%;
  animation: shimmer 1.8s ease-in-out infinite;
}
```

**Float** — communicates "interactive" or draws attention to a key element. Subtle vertical oscillation.

```css
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
}
.float { animation: float 3s ease-in-out infinite; }
/* Keep amplitude small (4-8px). More than that reads as broken. */
```

**Counter increment** — communicates live data. A number ticks upward in real time. Use `requestAnimationFrame` not `setInterval` for smooth animation.

```js
// Smooth counting with easing
function animateCounter(el, target, duration = 1200) {
  let start;
  function step(timestamp) {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    el.textContent = Math.floor(eased * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
```

---

## Quick-Reference: Which Pattern for Which Brief

| Brief says... | Reach for... |
|---|---|
| "feels alive" / "show it's live" | BreathingDot (Archetype 3) + Pulse pattern |
| "show the AI working" / "analysis" | Focus Mode (Archetype 5) |
| "show breadth of features" | Bento 2.0 grid with all 5 archetypes |
| "show activity" / "show volume" | Data Stream (Archetype 4) |
| "prioritization" / "smart sorting" | Intelligent List (Archetype 1) |
| "show what the product can do" | Command Input typewriter (Archetype 2) |
| "magnetic" / "cursor-aware" | useMotionValue pattern (Part 1.1) |
| "smooth entrance" for a list | Stagger orchestration (Part 1.3) |
| Button feels cheap / no weight | Spring physics baseline (Part 2.1) |
| Scroll animation + complex timing | GSAP, not Framer (Part 3) |
