<!-- Deep reference: animation recipes. Not auto-loaded. -->
<!-- Access via: grep -A N "SECTION_HEADER" references/deep/animation-recipes.md -->
# Animation & Motion Design

## Key Principles from Research

Based on Emil Kowalski's animation principles and modern web best practices:

### 1. **Great animations feel natural**
- Use spring physics instead of linear easing
- Spring animations create organic, lifelike motion
- Recommended spring config: `stiffness: 300, damping: 28`

### 2. **Great animations are fast**
- Keep animations under 300ms for snappy feel
- Use `ease-out` for perceived responsiveness
- Fast animations improve perceived performance

### 3. **Great animations have purpose**
- Never animate keyboard-initiated actions (used 100+ times/day)
- Use animations to indicate state changes
- Pace animations through the experience

### 4. **Great animations are performant**
- Animate only `transform` and `opacity` when possible (compositor-only)
- Use CSS/WAAPI for hardware acceleration on busy main threads
- Avoid animating `width`, `height`, `padding`, `margin` (triggers layout/paint)

### 5. **Great animations are interruptible**
- Framer Motion supports interruptible animations by default
- CSS transitions can be interrupted smoothly
- CSS keyframes cannot be interrupted mid-animation

### 6. **Great animations are accessible**
- Always respect `prefers-reduced-motion`
- Reduce to opacity-only or remove motion entirely
- Over 50% of mobile sites now use this media query (2024)

---

## 1. Entry Animations

### 1.1 Staggered Reveal (Parent/Child Orchestration)

**Framer Motion (Primary):**

```jsx
import { motion } from "framer-motion"

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.3,
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

export const StaggerList = () => {
  return (
    <motion.ul
      variants={container}
      initial="hidden"
      animate="show"
      style={{ listStyle: "none", padding: 0 }}
    >
      {items.map((item, i) => (
        <motion.li key={i} variants={item}>
          {item.text}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

**CSS Alternative:**

```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.list-item {
  opacity: 0;
  animation: fadeInUp 0.4s ease-out forwards;
}

.list-item:nth-child(1) { animation-delay: 0.3s; }
.list-item:nth-child(2) { animation-delay: 0.4s; }
.list-item:nth-child(3) { animation-delay: 0.5s; }
.list-item:nth-child(4) { animation-delay: 0.6s; }
.list-item:nth-child(5) { animation-delay: 0.7s; }
```

**Reduced Motion Variant:**

```jsx
import { motion, useReducedMotion } from "framer-motion"

export const AccessibleStagger = () => {
  const shouldReduceMotion = useReducedMotion()

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: shouldReduceMotion ? 0 : 0.1,
      }
    }
  }

  const item = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 20 },
    show: { opacity: 1, y: 0 }
  }

  return (
    <motion.ul variants={container} initial="hidden" animate="show">
      {items.map((item, i) => (
        <motion.li key={i} variants={item}>{item.text}</motion.li>
      ))}
    </motion.ul>
  )
}
```

**CSS Reduced Motion:**

```css
@media (prefers-reduced-motion: reduce) {
  .list-item {
    animation: fadeIn 0.2s ease-out forwards;
  }
  .list-item:nth-child(n) { animation-delay: 0s; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

**Performance:** Animates `opacity` and `transform: translateY()` — both compositor-only properties.

**Real-world example:** Linear's task list reveals, Vercel's dashboard cards

---

### 1.2 Spring Physics with Elastic Overshoot

**Framer Motion:**

```jsx
import { motion } from "framer-motion"

const springConfig = {
  type: "spring",
  stiffness: 300,
  damping: 28,
  restDelta: 0.00001,
  restSpeed: 0.00001,
}

export const SpringEntry = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={springConfig}
    >
      Content
    </motion.div>
  )
}
```

**CSS Alternative (Using linear() easing for spring approximation):**

```css
/* Modern CSS spring approximation using linear() easing function (2024) */
@keyframes springEntry {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.spring-element {
  animation: springEntry 0.5s linear(
    0, 0.006, 0.025 2.8%, 0.101 6.1%, 0.539 18.9%, 0.721 25.3%, 0.849 31.5%,
    0.937 38.1%, 0.968 41.8%, 0.991 45.7%, 1.006 50.1%, 1.015 55%, 1.017 63.9%,
    1.001
  );
}
```

**Reduced Motion:**

```jsx
const transition = shouldReduceMotion
  ? { duration: 0.2 }
  : springConfig
```

**Performance:** `scale` and `opacity` are GPU-accelerated.

**Real-world example:** iOS Dynamic Island animations, Family app drawer

---

### 1.3 Slide + Fade Combo

**Framer Motion:**

```jsx
export const SlideInFade = ({ direction = "left" }) => {
  const variants = {
    hidden: {
      opacity: 0,
      x: direction === "left" ? -100 : direction === "right" ? 100 : 0,
      y: direction === "up" ? -100 : direction === "down" ? 100 : 0
    },
    visible: {
      opacity: 1,
      x: 0,
      y: 0,
      transition: { duration: 0.3, ease: "easeOut" }
    }
  }

  return (
    <motion.div
      variants={variants}
      initial="hidden"
      animate="visible"
    >
      Content
    </motion.div>
  )
}
```

**CSS Alternative:**

```css
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-100px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.slide-in-left {
  animation: slideInLeft 0.3s ease-out;
}
```

<!-- TODO: add reduced-motion variant -->

---

## 2. Scroll-Triggered Animations

### 2.1 CSS Scroll-Driven Animations (Modern, Pure CSS)

**Pure CSS (Chrome 116+, Firefox with flag):**

```css
/* Scroll progress indicator */
#progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 5px;
  background: linear-gradient(to right, #4f46e5, #06b6d4);
  transform-origin: left;

  animation: progressBar linear;
  animation-timeline: scroll(root block);
  animation-range: 0% calc(100% - 500px); /* Exclude footer */
}

@keyframes progressBar {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

**Reveal on Scroll (View Timeline):**

```css
.reveal-on-scroll {
  animation: fadeInUp linear;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(100px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Parallax Layers:**

```css
.parallax-slow {
  animation: parallaxMove linear;
  animation-timeline: view();
}

@keyframes parallaxMove {
  to { transform: translateY(-50px); }
}
```

**Reduced Motion:**

```css
@media (prefers-reduced-motion: reduce) {
  .reveal-on-scroll {
    animation: fadeIn 0.2s;
    animation-timeline: view();
  }

  .parallax-slow {
    animation: none;
  }
}
```

**Performance:** CSS scroll-driven animations run on the compositor thread, independent of main thread JavaScript.

**Browser Support:** Chrome 116+, Firefox 114+ (flag), Safari (not yet, use polyfill: https://github.com/flackr/scroll-timeline)

**Real-world examples:** Smashing Magazine's scroll progress, Awwwards showcase sites

---

### 2.2 Intersection Observer with Framer Motion

**Framer Motion (JavaScript fallback):**

```jsx
import { motion, useInView } from "framer-motion"
import { useRef } from "react"

export const RevealOnScroll = ({ children }) => {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.3 })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  )
}
```

**With Reduced Motion:**

```jsx
import { useReducedMotion } from "framer-motion"

export const AccessibleReveal = ({ children }) => {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true })
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: shouldReduceMotion ? 0.2 : 0.5 }}
    >
      {children}
    </motion.div>
  )
}
```

---

### 2.3 Sticky Sections with Progress

**CSS Scroll-Driven:**

```css
.sticky-section {
  position: sticky;
  top: 0;

  animation: stickyProgress linear;
  animation-timeline: scroll(root);
  animation-range: 0% 100%;
}

@keyframes stickyProgress {
  0% { opacity: 0; }
  25% { opacity: 1; }
  75% { opacity: 1; }
  100% { opacity: 0; }
}
```

<!-- TODO: add reduced-motion variant -->

---

## 3. Micro-Interactions

### 3.1 Button Press (Scale + Shadow Shift)

**Framer Motion:**

```jsx
export const AnimatedButton = ({ children, onClick }) => {
  return (
    <motion.button
      onClick={onClick}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      style={{
        padding: "12px 24px",
        border: "none",
        borderRadius: "8px",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        color: "white",
        cursor: "pointer",
        boxShadow: "0 4px 14px rgba(102, 126, 234, 0.4)",
      }}
    >
      {children}
    </motion.button>
  )
}
```

**CSS Alternative:**

```css
.button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
  transition: all 0.15s ease-out;
}

.button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.button:active {
  transform: scale(0.95);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}
```

**Reduced Motion:**

```css
@media (prefers-reduced-motion: reduce) {
  .button {
    transition: opacity 0.2s;
  }

  .button:hover {
    transform: none;
    opacity: 0.9;
  }

  .button:active {
    transform: none;
    opacity: 0.8;
  }
}
```

**Performance:** `transform: scale()` and `box-shadow` (shadow uses GPU on modern browsers).

**Real-world example:** Stripe dashboard buttons, Vercel deploy button

---

### 3.2 Like/Heart Burst Effect

**Framer Motion:**

```jsx
import { motion, useAnimation } from "framer-motion"
import { useState } from "react"

export const HeartButton = () => {
  const [liked, setLiked] = useState(false)
  const controls = useAnimation()

  const handleClick = () => {
    setLiked(!liked)
    if (!liked) {
      controls.start({
        scale: [1, 1.5, 1],
        transition: { duration: 0.3 }
      })
    }
  }

  return (
    <motion.button
      onClick={handleClick}
      whileTap={{ scale: 0.9 }}
      style={{ background: "none", border: "none", cursor: "pointer" }}
    >
      <motion.div animate={controls}>
        <svg width="24" height="24" viewBox="0 0 24 24">
          <motion.path
            d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
            fill={liked ? "#e74c3c" : "none"}
            stroke={liked ? "#e74c3c" : "#95a5a6"}
            strokeWidth="2"
            initial={false}
            animate={{
              fill: liked ? "#e74c3c" : "none",
              stroke: liked ? "#e74c3c" : "#95a5a6"
            }}
          />
        </svg>
      </motion.div>

      {/* Burst particles */}
      {liked && (
        <motion.div
          style={{ position: "absolute", inset: 0 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 1, 0] }}
          transition={{ duration: 0.6 }}
        >
          {[...Array(8)].map((_, i) => (
            <motion.div
              key={i}
              style={{
                position: "absolute",
                width: 4,
                height: 4,
                borderRadius: "50%",
                background: "#e74c3c",
                left: "50%",
                top: "50%",
              }}
              initial={{ scale: 0, x: 0, y: 0 }}
              animate={{
                scale: [0, 1, 0],
                x: Math.cos((i / 8) * Math.PI * 2) * 20,
                y: Math.sin((i / 8) * Math.PI * 2) * 20,
              }}
              transition={{ duration: 0.6 }}
            />
          ))}
        </motion.div>
      )}
    </motion.button>
  )
}
```

**CSS Alternative (Simplified):**

```css
@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

.heart-button.liked {
  animation: heartBeat 0.3s ease-in-out;
}

.heart-button.liked svg {
  fill: #e74c3c;
}
```

**Reduced Motion:**

```jsx
const shouldReduceMotion = useReducedMotion()

// Skip burst animation
{liked && !shouldReduceMotion && (
  // burst particles...
)}
```

**Real-world example:** Twitter/X like animation, Instagram heart

---

### 3.3 Hover Card Tilt (3D Perspective)

**Framer Motion:**

```jsx
import { motion, useMotionValue, useTransform } from "framer-motion"

export const TiltCard = ({ children }) => {
  const x = useMotionValue(0)
  const y = useMotionValue(0)

  const rotateX = useTransform(y, [-100, 100], [10, -10])
  const rotateY = useTransform(x, [-100, 100], [-10, 10])

  const handleMouse = (event) => {
    const rect = event.currentTarget.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2

    x.set(event.clientX - centerX)
    y.set(event.clientY - centerY)
  }

  const handleMouseLeave = () => {
    x.set(0)
    y.set(0)
  }

  return (
    <motion.div
      onMouseMove={handleMouse}
      onMouseLeave={handleMouseLeave}
      style={{
        perspective: 1000,
        transformStyle: "preserve-3d",
      }}
    >
      <motion.div
        style={{
          rotateX,
          rotateY,
          transformStyle: "preserve-3d",
        }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
      >
        {children}
      </motion.div>
    </motion.div>
  )
}
```

**CSS Alternative:**

```css
.tilt-card {
  perspective: 1000px;
}

.tilt-card-inner {
  transform-style: preserve-3d;
  transition: transform 0.1s ease-out;
}

.tilt-card:hover .tilt-card-inner {
  transform: rotateX(var(--rotate-x, 0deg)) rotateY(var(--rotate-y, 0deg));
}
```

```javascript
// JavaScript for CSS version
const card = document.querySelector('.tilt-card')
const inner = document.querySelector('.tilt-card-inner')

card.addEventListener('mousemove', (e) => {
  const rect = card.getBoundingClientRect()
  const x = e.clientX - rect.left - rect.width / 2
  const y = e.clientY - rect.top - rect.height / 2

  inner.style.setProperty('--rotate-x', `${-y / 10}deg`)
  inner.style.setProperty('--rotate-y', `${x / 10}deg`)
})

card.addEventListener('mouseleave', () => {
  inner.style.setProperty('--rotate-x', '0deg')
  inner.style.setProperty('--rotate-y', '0deg')
})
```

**Reduced Motion:**

```css
@media (prefers-reduced-motion: reduce) {
  .tilt-card-inner {
    transform: none !important;
  }
}
```

**Performance:** `transform: rotateX/rotateY` are GPU-accelerated.

**Real-world example:** Apple product cards, Awwwards showcase sites

---

## 4. Page Transitions

### 4.1 Crossfade with Framer Motion

**Framer Motion:**

```jsx
import { AnimatePresence, motion } from "framer-motion"

export const PageTransition = ({ children, pathname }) => {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

<!-- TODO: add reduced-motion variant -->

---

### 4.2 View Transitions API (Native Browser)

**React Router Integration:**

```jsx
import { useNavigate } from "react-router-dom"

export const ViewTransitionLink = ({ to, children }) => {
  const navigate = useNavigate()

  const handleClick = (e) => {
    e.preventDefault()

    if (!document.startViewTransition) {
      navigate(to)
      return
    }

    document.startViewTransition(() => {
      navigate(to)
    })
  }

  return (
    <a href={to} onClick={handleClick}>
      {children}
    </a>
  )
}
```

**CSS:**

```css
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}

::view-transition-old(root) {
  animation-name: fade-out;
}

::view-transition-new(root) {
  animation-name: fade-in;
}

@keyframes fade-out {
  to { opacity: 0; }
}

@keyframes fade-in {
  from { opacity: 0; }
}
```

**Reduced Motion:**

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation-duration: 0.1s;
  }
}
```

**Browser Support:** Chrome 111+, Edge 111+, Safari (not yet)

**Real-world example:** Astro documentation site transitions

---

### 4.3 Shared Element Morphing (layoutId)

**Framer Motion:**

```jsx
import { motion, AnimatePresence } from "framer-motion"
import { useState } from "react"

export const SharedElementDemo = () => {
  const [selected, setSelected] = useState(null)

  return (
    <div>
      {items.map(item => (
        <motion.div
          key={item.id}
          layoutId={item.id}
          onClick={() => setSelected(item)}
        >
          <motion.img src={item.thumbnail} layoutId={`img-${item.id}`} />
        </motion.div>
      ))}

      <AnimatePresence>
        {selected && (
          <motion.div
            layoutId={selected.id}
            onClick={() => setSelected(null)}
          >
            <motion.img src={selected.fullSize} layoutId={`img-${selected.id}`} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
```

**Performance:** Uses FLIP technique (First, Last, Invert, Play) — measures layout changes and animates transforms.

**Real-world example:** App Store card expansion, Framer website

<!-- TODO: add reduced-motion variant -->

---

## 5. Loading States

### 5.1 Skeleton Screen (Shimmer Gradient)

**React (shadcn/ui pattern):**

```jsx
export const Skeleton = ({ className, ...props }) => {
  return (
    <div
      className={`animate-pulse rounded-md bg-muted ${className}`}
      {...props}
    />
  )
}

// Usage
export const ArticleSkeleton = () => (
  <div className="space-y-3">
    <Skeleton className="h-4 w-[250px]" />
    <Skeleton className="h-4 w-[200px]" />
    <Skeleton className="h-4 w-[150px]" />
  </div>
)
```

**CSS with Shimmer:**

```css
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 0px,
    #e0e0e0 40px,
    #f0f0f0 80px
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite linear;
  border-radius: 4px;
}

.skeleton-text {
  height: 16px;
  margin-bottom: 8px;
}

.skeleton-text:last-child {
  width: 60%;
}
```

**Reduced Motion:**

```css
@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    background: #f0f0f0;
  }
}
```

**Performance:** Uses CSS `background-position` animation — GPU-accelerated.

**Real-world example:** LinkedIn feed loading, Facebook content placeholders

---

### 5.2 Progress Bar with Personality (Linear-style)

**Framer Motion:**

```jsx
import { motion } from "framer-motion"

export const ProgressBar = ({ progress = 0 }) => {
  return (
    <div className="w-full h-1 bg-gray-200 rounded-full overflow-hidden">
      <motion.div
        className="h-full bg-gradient-to-r from-blue-500 to-purple-600"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.3, ease: "easeOut" }}
      />
    </div>
  )
}
```

**CSS Alternative:**

```css
.progress-bar {
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  transition: width 0.3s ease-out;
  width: var(--progress, 0%);
}
```

**Reduced Motion:** Transition remains fast (0.3s) — acceptable for reduced motion.

**Real-world example:** Linear progress indicators, Vercel deploy progress

---

### 5.3 Optimistic UI Updates

**Framer Motion:**

```jsx
import { motion, AnimatePresence } from "framer-motion"

export const TodoList = () => {
  const [todos, setTodos] = useState([])

  const addTodo = async (text) => {
    const tempId = Date.now()
    const optimisticTodo = { id: tempId, text, pending: true }

    setTodos(prev => [...prev, optimisticTodo])

    try {
      const result = await api.createTodo(text)
      setTodos(prev => prev.map(t =>
        t.id === tempId ? { ...result, pending: false } : t
      ))
    } catch (error) {
      setTodos(prev => prev.filter(t => t.id !== tempId))
    }
  }

  return (
    <ul>
      <AnimatePresence>
        {todos.map(todo => (
          <motion.li
            key={todo.id}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            style={{ opacity: todo.pending ? 0.5 : 1 }}
          >
            {todo.text}
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  )
}
```

**Real-world example:** Twitter post submission, Notion block creation

<!-- TODO: add reduced-motion variant -->

---

## 6. Gesture Handling

### 6.1 Drag-and-Drop (@dnd-kit)

**@dnd-kit (Recommended for React):**

```jsx
import { DndContext, closestCenter } from "@dnd-kit/core"
import { SortableContext, useSortable, arrayMove } from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"

const SortableItem = ({ id, children }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {children}
    </div>
  )
}

export const SortableList = () => {
  const [items, setItems] = useState(["1", "2", "3"])

  const handleDragEnd = (event) => {
    const { active, over } = event

    if (active.id !== over.id) {
      setItems((items) => {
        const oldIndex = items.indexOf(active.id)
        const newIndex = items.indexOf(over.id)
        return arrayMove(items, oldIndex, newIndex)
      })
    }
  }

  return (
    <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <SortableContext items={items}>
        {items.map(id => (
          <SortableItem key={id} id={id}>
            Item {id}
          </SortableItem>
        ))}
      </SortableContext>
    </DndContext>
  )
}
```

**Reduced Motion:**

```jsx
const shouldReduceMotion = useReducedMotion()

const style = {
  transform: CSS.Transform.toString(transform),
  transition: shouldReduceMotion ? "none" : transition,
}
```

**Real-world example:** Trello boards, Notion page reordering

---

### 6.2 Swipe Gestures (Framer Motion)

**Framer Motion:**

```jsx
import { motion, useMotionValue, useTransform } from "framer-motion"

export const SwipeCard = ({ onSwipe, children }) => {
  const x = useMotionValue(0)
  const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0])
  const rotate = useTransform(x, [-200, 200], [-20, 20])

  const handleDragEnd = (event, info) => {
    if (Math.abs(info.offset.x) > 100) {
      onSwipe(info.offset.x > 0 ? "right" : "left")
    }
  }

  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={handleDragEnd}
      style={{ x, opacity, rotate }}
    >
      {children}
    </motion.div>
  )
}
```

**Real-world example:** Tinder swipe cards, mobile app carousels

<!-- TODO: add reduced-motion variant -->

---

### 6.3 Pinch-to-Zoom

**Framer Motion:**

```jsx
import { motion, useMotionValue, useTransform } from "framer-motion"

export const PinchZoom = ({ children }) => {
  const scale = useMotionValue(1)

  return (
    <motion.div
      style={{ scale }}
      onWheel={(e) => {
        e.preventDefault()
        const delta = e.deltaY
        scale.set(Math.max(1, Math.min(3, scale.get() - delta * 0.01)))
      }}
    >
      {children}
    </motion.div>
  )
}
```

<!-- TODO: add reduced-motion variant -->

---

## 7. Text Animations

### 7.1 Typewriter Effect

**Motion.dev Typewriter (Premium component):**

```jsx
import { Typewriter } from "motion-plus"

export const TypewriterDemo = () => {
  return (
    <Typewriter speed="normal" variance={0.5}>
      Hello world! This is a realistic typing animation.
    </Typewriter>
  )
}
```

**CSS Alternative (Simple):**

```css
@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}

@keyframes blink {
  50% { border-color: transparent; }
}

.typewriter {
  overflow: hidden;
  border-right: 2px solid;
  white-space: nowrap;
  animation:
    typing 3.5s steps(40, end),
    blink 0.75s step-end infinite;
}
```

**Reduced Motion:**

```css
@media (prefers-reduced-motion: reduce) {
  .typewriter {
    animation: none;
    width: 100%;
    border-right: none;
  }
}
```

**Real-world example:** Developer portfolio hero sections

---

### 7.2 Character Stagger

**Framer Motion:**

```jsx
export const StaggerText = ({ text }) => {
  const letters = text.split("")

  const container = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.03 }
    }
  }

  const child = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <motion.h1
      variants={container}
      initial="hidden"
      animate="visible"
    >
      {letters.map((letter, i) => (
        <motion.span key={i} variants={child}>
          {letter === " " ? "\u00A0" : letter}
        </motion.span>
      ))}
    </motion.h1>
  )
}
```

<!-- TODO: add reduced-motion variant -->

---

### 7.3 Counting Number Animation

**Motion.dev AnimateNumber:**

```jsx
import { AnimateNumber } from "motion-plus"

export const Counter = ({ value }) => {
  return (
    <AnimateNumber
      value={value}
      speed="normal"
      format={(n) => Math.floor(n).toLocaleString()}
    />
  )
}
```

**Framer Motion Alternative:**

```jsx
import { motion, useSpring, useTransform } from "framer-motion"
import { useEffect } from "react"

export const CountingNumber = ({ value, duration = 2 }) => {
  const spring = useSpring(0, { duration: duration * 1000 })
  const display = useTransform(spring, (current) =>
    Math.floor(current).toLocaleString()
  )

  useEffect(() => {
    spring.set(value)
  }, [spring, value])

  return <motion.span>{display}</motion.span>
}
```

**Reduced Motion:**

```jsx
const shouldReduceMotion = useReducedMotion()

useEffect(() => {
  if (shouldReduceMotion) {
    spring.set(value)
    spring.jump(value) // Skip animation
  } else {
    spring.set(value)
  }
}, [value])
```

**Real-world example:** GitHub star counters, analytics dashboards

---

## 8. Layout Animations

### 8.1 List Reordering (AnimatePresence + layoutId)

**Framer Motion:**

```jsx
import { motion, AnimatePresence } from "framer-motion"

export const AnimatedList = ({ items, onRemove }) => {
  return (
    <ul>
      <AnimatePresence>
        {items.map(item => (
          <motion.li
            key={item.id}
            layout
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.2 }}
          >
            {item.text}
            <button onClick={() => onRemove(item.id)}>Remove</button>
          </motion.li>
        ))}
      </AnimatePresence>
    </ul>
  )
}
```

**CSS Alternative (Grid auto-flow):**

```css
.list {
  display: grid;
  gap: 8px;
  grid-auto-rows: auto;
}

.list-item {
  transition: all 0.3s ease-out;
}

.list-item.removing {
  opacity: 0;
  transform: scale(0.8);
}
```

<!-- TODO: add reduced-motion variant -->

---

### 8.2 Accordion Expand/Collapse (Height Animation)

**Modern CSS (2024 - interpolate-size):**

```css
/* Enable smooth height animation to/from auto */
:root {
  interpolate-size: allow-keywords;
}

.accordion-content {
  height: 0;
  overflow: hidden;
  transition: height 0.3s ease-out;
}

.accordion.open .accordion-content {
  height: auto;
}
```

**Framer Motion Alternative:**

```jsx
import { motion, AnimatePresence } from "framer-motion"

export const Accordion = ({ title, children, isOpen, toggle }) => {
  return (
    <div>
      <button onClick={toggle}>{title}</button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            style={{ overflow: "hidden" }}
          >
            {children}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
```

**Reduced Motion:**

```css
@media (prefers-reduced-motion: reduce) {
  .accordion-content {
    transition: opacity 0.2s;
  }

  .accordion.open .accordion-content {
    height: auto;
  }
}
```

**Real-world example:** FAQ sections, navigation menus

---

### 8.3 Tab Content Transitions

**Framer Motion:**

```jsx
import { motion, AnimatePresence } from "framer-motion"

export const Tabs = ({ tabs, activeTab, onChange }) => {
  return (
    <div>
      <div className="tab-buttons">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={activeTab === tab.id ? "active" : ""}
          >
            {tab.label}
            {activeTab === tab.id && (
              <motion.div
                className="active-indicator"
                layoutId="activeTab"
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
              />
            )}
          </button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          {tabs.find(t => t.id === activeTab)?.content}
        </motion.div>
      </AnimatePresence>
    </div>
  )
}
```

**Real-world example:** shadcn/ui Tabs, Radix UI Tabs

<!-- TODO: add reduced-motion variant -->

---

## Performance Best Practices Summary

### DO:
- Animate `transform` and `opacity` (compositor-only)
- Use `will-change` sparingly for promoted layers
- Use CSS/WAAPI for hardware acceleration on busy threads
- Keep animations under 300ms for snappiness
- Use `ease-out` for responsive feel
- Test on low-end devices

### DON'T:
- Animate `width`, `height`, `padding`, `margin` (triggers layout)
- Animate `box-shadow` heavily (paint-intensive on older browsers)
- Use `will-change` everywhere (memory overhead)
- Create long animations (>500ms) for frequent actions
- Forget `prefers-reduced-motion`

---

## Browser Support Summary (Feb 2025)

| Feature | Chrome | Firefox | Safari | Polyfill |
|---------|--------|---------|--------|----------|
| CSS Scroll-Driven | 116+ | 114+ (flag) | No | [flackr/scroll-timeline](https://github.com/flackr/scroll-timeline) |
| View Transitions API | 111+ | No | No | N/A |
| `interpolate-size` | 129+ | No | No | N/A |
| Framer Motion | All | All | All | N/A |
| Web Animations API | All | All | All | N/A |

---

## Accessibility Checklist

- [ ] All animations respect `prefers-reduced-motion`
- [ ] Reduced motion variants use opacity-only or remove motion entirely
- [ ] Animations never block critical user actions
- [ ] Loading states have proper ARIA labels
- [ ] Interactive elements maintain focus states during animation
- [ ] Animations don't trigger vestibular disorders (avoid spinning, rapid movement)
