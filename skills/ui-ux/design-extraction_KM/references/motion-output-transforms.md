# Motion Token → Framework Output Transforms

> Given a `MotionToken`, here's how to generate implementation code for each target.

---

## CSS Transitions / Keyframes

### Simple from→to (single track, no spring)

```css
/* Token: tab_content_enter */
.tab-content-enter {
  opacity: 0;
  transform: translateX(24px);
  transition:
    opacity 200ms cubic-bezier(0.0, 0.0, 0.2, 1.0) 50ms,
    transform 200ms cubic-bezier(0.0, 0.0, 0.2, 1.0) 50ms;
}
.tab-content-enter.active {
  opacity: 1;
  transform: translateX(0);
}
```

### Mapping rules:
- `timing.durationMs` → `{duration}ms`
- `timing.delayMs` → delay after duration: `{delay}ms`
- `timing.easing.type === "cubic-bezier"` → `cubic-bezier(x1, y1, x2, y2)`
- `timing.easing.type === "spring"` → ⚠️ CSS has no native spring. Use `@keyframes` approximation or fall back to closest bezier preset.
- `timing.iterations === "infinite"` → `animation-iteration-count: infinite`
- `timing.direction === "alternate"` → `animation-direction: alternate`

### Stagger (CSS custom properties)

```css
/* Token: scroll_reveal_card (stagger group, eachDelayMs: 60) */
.card-reveal {
  --stagger-index: 0;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 250ms cubic-bezier(0.0, 0.0, 0.2, 1.0) calc(var(--stagger-index) * 60ms),
    transform 250ms cubic-bezier(0.0, 0.0, 0.2, 1.0) calc(var(--stagger-index) * 60ms);
}
.card-reveal:nth-child(1) { --stagger-index: 0; }
.card-reveal:nth-child(2) { --stagger-index: 1; }
.card-reveal:nth-child(3) { --stagger-index: 2; }
```

### Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  .tab-content-enter {
    transition-duration: 0ms;
    /* or: transition-duration: 100ms for "shorten" strategy */
  }
  .shimmer-skeleton {
    animation: none; /* "remove" strategy */
  }
}
```

---

## Framer Motion (React)

### Simple transition

```tsx
/* Token: tab_content_enter */
<motion.div
  initial={{ opacity: 0, x: 24 }}
  animate={{ opacity: 1, x: 0 }}
  transition={{
    duration: 0.2,      // 200ms → 0.2s
    delay: 0.05,        // 50ms → 0.05s
    ease: [0.0, 0.0, 0.2, 1.0],  // material-decelerate
  }}
/>
```

### Spring transition

```tsx
/* Token: tab_indicator_slide */
<motion.div
  animate={{ x: 96 }}
  transition={{
    type: "spring",
    stiffness: 420,
    damping: 38,
    mass: 1,
  }}
/>
```

### Orchestrated stagger

```tsx
/* Token group: card_reveal (stagger) */
const container = {
  animate: {
    transition: {
      staggerChildren: 0.06,  // eachDelayMs: 60 → 0.06s
    },
  },
};

const item = {
  initial: { opacity: 0, y: 20 },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.25,
      ease: [0.0, 0.0, 0.2, 1.0],
    },
  },
};

<motion.div variants={container} initial="initial" animate="animate">
  {cards.map(card => (
    <motion.div key={card.id} variants={item} />
  ))}
</motion.div>
```

### Reduced motion

```tsx
const prefersReducedMotion = useReducedMotion();

<motion.div
  animate={{ opacity: 1, x: 0 }}
  transition={prefersReducedMotion
    ? { duration: 0 }  // "remove" strategy
    : { type: "spring", stiffness: 420, damping: 38 }
  }
/>
```

---

## SwiftUI

### Simple animation

```swift
// Token: tab_content_enter
struct TabContent: View {
    @State private var isActive = false

    var body: some View {
        content
            .opacity(isActive ? 1 : 0)
            .offset(x: isActive ? 0 : 24)
            .animation(
                .timingCurve(0.0, 0.0, 0.2, 1.0, duration: 0.2)
                    .delay(0.05),
                value: isActive
            )
    }
}
```

### Spring animation

```swift
// Token: tab_indicator_slide
// Using platformHints.ios values
TabIndicator()
    .offset(x: indicatorOffset)
    .animation(
        .spring(response: 0.35, dampingFraction: 0.72),
        value: selectedTab
    )
```

### Stagger (ForEach with delay)

```swift
// Token group: card_reveal
ForEach(Array(cards.enumerated()), id: \.element.id) { index, card in
    CardView(card: card)
        .opacity(isVisible ? 1 : 0)
        .offset(y: isVisible ? 0 : 20)
        .animation(
            .timingCurve(0.0, 0.0, 0.2, 1.0, duration: 0.25)
                .delay(Double(index) * 0.06),
            value: isVisible
        )
}
```

### Reduced motion

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion

.animation(
    reduceMotion
        ? .linear(duration: 0)
        : .spring(response: 0.35, dampingFraction: 0.72),
    value: selectedTab
)
```

---

## Jetpack Compose

### Simple animation

```kotlin
// Token: tab_content_enter
val alpha by animateFloatAsState(
    targetValue = if (isActive) 1f else 0f,
    animationSpec = tween(
        durationMillis = 200,
        delayMillis = 50,
        easing = CubicBezierEasing(0f, 0f, 0.2f, 1f)
    )
)

val offsetX by animateDpAsState(
    targetValue = if (isActive) 0.dp else 24.dp,
    animationSpec = tween(
        durationMillis = 200,
        delayMillis = 50,
        easing = CubicBezierEasing(0f, 0f, 0.2f, 1f)
    )
)
```

### Spring animation

```kotlin
// Token: tab_indicator_slide
// Using platformHints.android values
val offsetX by animateDpAsState(
    targetValue = indicatorOffset,
    animationSpec = spring(
        dampingRatio = 0.72f,
        stiffness = 420f
    )
)
```

### Reduced motion

```kotlin
val reduceMotion = LocalReduceMotion.current
val animSpec = if (reduceMotion) {
    snap<Float>()
} else {
    spring(dampingRatio = 0.72f, stiffness = 420f)
}
```

---

## Transform Decision Table

| Schema Field | CSS | Framer Motion | SwiftUI | Compose |
|---|---|---|---|---|
| `durationMs: 200` | `200ms` | `duration: 0.2` | `duration: 0.2` | `durationMillis = 200` |
| `delayMs: 50` | `50ms` | `delay: 0.05` | `.delay(0.05)` | `delayMillis = 50` |
| `easing: cubic-bezier` | `cubic-bezier(...)` | `ease: [...]` | `.timingCurve(...)` | `CubicBezierEasing(...)` |
| `easing: spring` | ⚠️ Approximate | `type: "spring"` | `.spring(...)` | `spring(...)` |
| `iterations: "infinite"` | `infinite` | `repeat: Infinity` | `.repeatForever()` | `infiniteRepeatable` |
| `direction: "alternate"` | `alternate` | `repeatType: "reverse"` | `.autoreverses` | `RepeatMode.Reverse` |
| `stagger: 60ms` | `calc(var * 60ms)` | `staggerChildren: 0.06` | Manual delay per index | Manual delay per index |
| `fill: "forwards"` | `forwards` | — (default) | — (default) | — |
