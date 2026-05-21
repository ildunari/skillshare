# CSS-Native Animation (2025–2026)

> The platform absorbed entire categories of "library-needed" work. This file covers what CSS can now do natively, when to use it, and where the edges still cut.

## Contents
- Entry/Exit: `@starting-style` + `allow-discrete` (Baseline 2024)
- Intrinsic Sizes: `interpolate-size` + `calc-size()` (accordion pattern)
- Scroll-Driven Animations: scroll()/view() timelines, parallax, progress bars, fallbacks
- View Transitions: same-document (Baseline Oct 2025), gotchas
- CSS `linear()` Easing: spring presets (snappy, balanced, bouncy)
- CSS `@property`: animatable custom properties, gradient angles
- Scroll-Triggered (Chrome 145+) → The CSS-First Decision Rule

---

## Entry and Exit: `@starting-style` + `allow-discrete`

### What changed
Historically, `display: none` elements had no box to animate from. CSS couldn't express "animate into existence." Now it can.

- `@starting-style` defines the pre-render starting state for an element appearing.
- `transition-behavior: allow-discrete` permits transitions on discrete properties like `display`.
- Combined, they handle entry effects for dialogs, popovers, and any element toggling `display`.

**Baseline 2024.** Chrome 117+, Safari 17.4+, Firefox 129+. Safe to use without fallback in modern targets.

### Production pattern: animated popover + dialog

```css
/* Safe defaults — visible end state */
[popover], dialog {
  opacity: 0;
  transform: translateY(8px) scale(0.98);
}

/* Open states */
[popover]:popover-open,
dialog[open] {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Progressive enhancement: entry/exit transitions */
@supports (transition-behavior: allow-discrete) {
  [popover], dialog {
    transition:
      opacity 180ms ease,
      transform 220ms cubic-bezier(0.2, 0, 0, 1),
      display 220ms ease allow-discrete,
      overlay 220ms ease allow-discrete;
  }

  @starting-style {
    [popover]:popover-open,
    dialog[open] {
      opacity: 0;
      transform: translateY(12px) scale(0.98);
    }
  }
}

@media (prefers-reduced-motion: reduce) {
  [popover], dialog {
    transition: opacity 100ms linear !important;
    transform: none !important;
  }
}
```

### Key details
- The `overlay` property can't be set manually, but listing it in transitions delays top-layer removal so exit transitions can complete.
- `@starting-style` goes inside `@supports` — older browsers ignore the whole block gracefully.
- This replaces the old "double-rAF hack" for enter animations from `display: none`.

### Where it breaks
- No JavaScript interception point for complex choreography during the transition.
- Exit animations require the transition on `display` + `overlay` to work on top-layer elements; without them, the element disappears before the transition completes.

---

## Animating Intrinsic Sizes: `interpolate-size` + `calc-size()`

### What changed
"Animate height from 0 to auto" was a decade-long pain point. The platform now offers an opt-in.

- `interpolate-size: allow-keywords` at `:root` — page-level opt-in enabling smooth transitions to/from `auto`, `min-content`, `max-content`, `fit-content`.
- `calc-size()` — per-property opt-in for the same capability, without global side effects.

**Chrome 129+, Safari 26+. Firefox not yet.**

### Production pattern: accordion

```css
/* Page-level opt-in — add to your reset */
:root {
  interpolate-size: allow-keywords;
}

.accordion-content {
  height: 0;
  overflow: hidden;
  transition: height 350ms cubic-bezier(0.2, 0, 0, 1);
}

.accordion[open] .accordion-content {
  height: auto; /* This now animates smoothly */
}

@media (prefers-reduced-motion: reduce) {
  .accordion-content { transition: none; }
}
```

### Per-component alternative with `calc-size()`

```css
.panel {
  height: calc-size(0px); /* collapsed */
  overflow: hidden;
  transition: height 300ms ease;
}

.panel[data-open] {
  height: calc-size(auto); /* expands smoothly */
}
```

### Where it breaks
- Firefox doesn't support it yet — progressive enhancement required.
- `interpolate-size: allow-keywords` is global; it could cause unexpected interpolation on elements that currently snap between size keywords. Audit before adding to an existing codebase.

---

## Scroll-Driven Animations

### Core primitives
CSS scroll-driven animations attach keyframe progress to scroll position instead of time. Two timeline types:

- **Scroll Timeline** (`animation-timeline: scroll()`) — progress = scroll position of a scrolling container. Full container scroll = full animation.
- **View Timeline** (`animation-timeline: view()`) — progress = an element's visibility in its scroll ancestor. Entry → full visibility → exit = animation range.

Named timelines (`scroll-timeline-name`, `view-timeline-name`) let you share timelines across elements.

`animation-range` constrains where the animation plays within the timeline (e.g., `entry 0% entry 100%`, `cover 20% cover 80%`).

**Chrome 115+, Safari 26+. Firefox disabled by default. Always `@supports` gate.**

### Pattern: sticky header shrink on scroll

```css
@supports (animation-timeline: scroll()) {
  @keyframes shrinkHeader {
    from { transform: scaleY(1); padding-block: 16px; }
    to   { transform: scaleY(0.85); padding-block: 8px; }
  }

  .site-header {
    position: sticky;
    top: 0;
    transform-origin: top;
    animation: shrinkHeader linear both;
    animation-timeline: scroll(root block);
    animation-range: 0px 200px;
  }
}
```

### Pattern: scroll progress bar

```css
@supports (animation-timeline: scroll()) {
  @keyframes fillProgress { to { transform: scaleX(1); } }

  .progress-bar {
    transform: scaleX(0);
    transform-origin: left;
    animation: fillProgress linear both;
    animation-timeline: scroll(root block);
  }
}
```

### Pattern: view-timeline reveal on scroll

```css
@supports (animation-timeline: view()) {
  @keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .reveal {
    animation: fadeSlideIn linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
```

### Pattern: parallax layers

```css
@supports (animation-timeline: scroll()) {
  @keyframes parallaxSlow { to { transform: translateY(60px); } }
  @keyframes parallaxFast { to { transform: translateY(180px); } }

  .layer-slow {
    animation: parallaxSlow linear both;
    animation-timeline: scroll(root block);
  }
  .layer-fast {
    animation: parallaxFast linear both;
    animation-timeline: scroll(root block);
  }
}
```

### Fallback strategies

```css
/* CSS-only fallback: no animation, content still visible */
.reveal { opacity: 1; transform: none; }

/* Enhanced: scroll-driven entry */
@supports (animation-timeline: view()) {
  .reveal {
    animation: fadeSlideIn linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
```

For JS fallback when CSS scroll-driven isn't supported:
```js
// IntersectionObserver toggle (cross-browser)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('in-view');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### ScrollTimeline polyfill
```html
<script src="https://cdn.jsdelivr.net/npm/scroll-timeline-polyfill@latest/dist/scroll-timeline.js"></script>
```
Enables `ScrollTimeline`/`ViewTimeline` with WAAPI and CSS syntax. But: adds testing burden and can reintroduce jank in polyfilled environments.

### Where it breaks
- **Firefox**: disabled by default across desktop and mobile as of early 2026. Not shippable as the sole implementation.
- **Polyfill complexity**: Chrome's own case study warns polyfills increase testing needs and can introduce failure/jank.
- **Main-thread interaction**: the whole point is off-main-thread performance. If you fall back to JS scroll handlers, you lose the performance benefit.

---

## View Transitions

### What changed
Same-document view transitions became **Baseline October 2025** (Chrome 111+, Safari 18+, Firefox 144+). Cross-document view transitions remain "Limited availability."

View transitions create snapshot pseudo-elements (`::view-transition-old(name)`, `::view-transition-new(name)`) that animate between states. The browser handles the screenshot/composite/crossfade; you customize with CSS.

### Production pattern: tab content swap

```js
// JS trigger
function switchTab(newContent) {
  if (!document.startViewTransition) {
    updateDOM(newContent);
    return;
  }

  document.startViewTransition(() => {
    updateDOM(newContent);
  });
}
```

```css
/* CSS choreography */
::view-transition-old(root) {
  animation: fadeOut 200ms ease both;
}
::view-transition-new(root) {
  animation: fadeIn 200ms ease both;
}

@keyframes fadeOut { to { opacity: 0; } }
@keyframes fadeIn { from { opacity: 0; } }

/* Named elements for shared-element continuity */
.card-thumbnail {
  view-transition-name: hero-image;
}
```

### Gotchas practitioners document
- **Hover-triggered transitions break mouse events.** The transition layer sits above the UI during the transition, firing `mouseleave` on the original element. Don't trigger view transitions on hover.
- **Firefox initial implementation may lack `view-transition-types`.** Use progressive enhancement; check for the specific features you need.
- **Cross-document transitions require same-origin** and have navigation constraints. Treat as experimental.
- **Snapshot model means no live content during transition.** Content is frozen in screenshots; if you need live elements during the transition, view transitions aren't the right tool.

---

## CSS `linear()` Easing

Custom piecewise-linear timing functions that approximate springs, bounces, and elastic curves without JS. Generate values using tools like the `linear()` easing generator, not by hand.

### Ready-to-use spring presets

```css
/* Snappy (stiffness ~450, damping ~40), duration ≈ 520ms */
:root {
  --spring-snappy: linear(
    0, 0.079, 0.24, 0.413, 0.567, 0.692, 0.787, 0.857,
    0.906, 0.94, 0.962, 0.977, 0.986, 0.992, 0.996, 0.998,
    0.999, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
  );
  --spring-snappy-dur: 520ms;
}

/* Balanced (stiffness ~170, damping ~26), duration ≈ 910ms */
:root {
  --spring-balanced: linear(
    0, 0.088, 0.26, 0.437, 0.588, 0.708, 0.797, 0.861,
    0.906, 0.937, 0.958, 0.973, 0.982, 0.988, 0.993, 0.995,
    0.997, 0.998, 0.999, 0.999, 1.0, 1.0, 1.0, 1.0, 1.0
  );
  --spring-balanced-dur: 910ms;
}

/* Bouncy (stiffness ~120, damping ~14), duration ≈ 1350ms */
:root {
  --spring-bouncy: linear(
    0, 0.145, 0.429, 0.705, 0.905, 1.02, 1.068, 1.072,
    1.055, 1.034, 1.015, 1.003, 0.997, 0.995, 0.995, 0.997,
    0.998, 0.999, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
  );
  --spring-bouncy-dur: 1350ms;
}

/* Usage */
.button:active {
  transform: scale(0.97);
  transition: transform var(--spring-snappy-dur) var(--spring-snappy);
}
```

**Baseline support**: Chrome 113+, Safari 17.2+, Firefox 112+. Safe to use.

---

## CSS `@property` for Animatable Custom Properties

`@property` (Baseline 2024) registers custom properties with a type, enabling smooth interpolation of gradients, angles, percentages that would otherwise snap between values.

### Pattern: animated gradient angle

```css
@property --gradient-angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.gradient-border {
  background: conic-gradient(from var(--gradient-angle), #7dd3fc, #a78bfa, #fb7185, #7dd3fc);
  animation: spin 4s linear infinite;
}

@keyframes spin {
  to { --gradient-angle: 360deg; }
}
```

Without `@property`, the custom property would snap between values instead of interpolating smoothly.

---

## Scroll-Triggered Animations (Chrome 145+, 2026)

CSS scroll-triggered animations land in Chrome 145 — declarative triggers that fire when an element enters/exits the viewport. Positioned as "say goodbye to IntersectionObserver for this type of effect."

**Not yet cross-browser.** Treat as progressive enhancement with IntersectionObserver fallback.

---

## The CSS-First Decision Rule

Use CSS-native animation when ALL of these are true:

1. The effect is state-based (open/closed), timeline-based (time loop), or view-based (scroll range)
2. It can be expressed declaratively without runtime measurement
3. Browser support covers your targets (or graceful degradation is acceptable)
4. No pointer-position tracking or gesture velocity is needed
5. No complex cross-element orchestration is needed

Use JS when ANY of these are true:
- Runtime input streams (pointer position, velocity, gesture)
- Runtime measurement (element dimensions for FLIP)
- Cross-browser parity for scroll-linked effects
- Complex multi-element choreography with labels/callbacks
- Interruption semantics beyond what CSS transitions provide
