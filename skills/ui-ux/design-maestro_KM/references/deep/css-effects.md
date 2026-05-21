<!-- Deep reference: CSS effects. Not auto-loaded. -->
<!-- Access via: grep -A N "SECTION_HEADER" references/deep/css-effects.md -->
# Advanced CSS Techniques

## 1. Glassmorphism (Backdrop Filter)

### Description
Creates frosted glass effects using backdrop-filter blur with proper layering for nearby element consideration. Enables depth and realism through translucent surfaces that blur content behind them.

### Code Example
```css
header {
  position: relative;
  background: hsl(0deg 0% 100% / 0.5);
}

.backdrop {
  position: absolute;
  inset: 0;
  height: 200%;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px); /* Safari */
  background: linear-gradient(
    to bottom,
    hsl(0deg 0% 95%),
    transparent 50%
  );
  mask-image: linear-gradient(
    to bottom,
    black 0% 50%,
    transparent 50% 100%
  );
  -webkit-mask-image: linear-gradient(
    to bottom,
    black 0% 50%,
    transparent 50% 100%
  );
  pointer-events: none;
}

/* 3D edge effect (optional enhancement) */
.backdrop-edge {
  --thickness: 4px;
  position: absolute;
  inset: 0;
  height: 100%;
  transform: translateY(100%);
  background: hsl(0deg 0% 100% / 0.1);
  backdrop-filter: blur(12px) brightness(0.96);
  -webkit-backdrop-filter: blur(12px) brightness(0.96);
  mask-image: linear-gradient(
    to bottom,
    black 0,
    black var(--thickness),
    transparent var(--thickness)
  );
  pointer-events: none;
}

/* Feature query for progressive enhancement */
@supports (backdrop-filter: blur(16px)) or (-webkit-backdrop-filter: blur(16px)) {
  header {
    background: hsl(0deg 0% 100% / 0.5);
  }
}

/* Fallback for unsupported browsers */
@supports not (backdrop-filter: blur(16px)) {
  header {
    background: hsl(0deg 0% 100% / 0.95);
  }
}
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 76+     | Supported (requires -webkit- prefix until 144+) |
| Firefox | 103+    | Supported |
| Safari  | 9+      | Supported (requires -webkit- prefix) |

**Baseline Status:** Widely available since September 2024

### Fallback Strategy
1. Use `@supports` feature queries to provide semi-opaque fallback backgrounds
2. For browsers without backdrop-filter, increase background opacity from 0.5 to 0.95
3. mask-image fallback: 96.3% support (as of Dec 2024)
4. Use overflow: hidden on Firefox/Safari (not Chrome due to order-of-operations bug)

### Performance Notes
- **Paint cost:** Medium-High (blur is expensive)
- **Composite cost:** High (creates new stacking context, GPU-accelerated)
- **Layout cost:** Low (positioned elements don't trigger layout)
- **Mobile considerations:**
  - Can cause performance issues on low-end devices
  - Test on actual mobile hardware
  - Consider reducing blur radius on mobile (8px vs 16px)
  - Avoid stacking multiple backdrop-filter layers

### Real-World Example
- **Site:** Josh W. Comeau blog header
- **Implementation:** Extended backdrop with mask-image for nearby element blur, 3D edge effect with brightness filter

### Sources
- [Can I Use: backdrop-filter](https://caniuse.com/css-backdrop-filter) — Browser support data
- [Josh Comeau: Next-level frosted glass with backdrop-filter](https://www.joshwcomeau.com/css/backdrop-filter/) — Production implementation guide (Dec 2024)

---

## 2. Mesh Gradients

### Description
Multi-layer gradient compositions simulating mesh gradient effects using CSS radial/conic gradients or SVG. Creates organic, fluid color transitions.

### Code Example (Pure CSS Approach)
```css
.mesh-gradient {
  background:
    radial-gradient(at 27% 37%, hsla(215, 98%, 61%, 1) 0, transparent 50%),
    radial-gradient(at 97% 21%, hsla(125, 98%, 72%, 1) 0, transparent 50%),
    radial-gradient(at 52% 99%, hsla(354, 98%, 61%, 1) 0, transparent 50%),
    radial-gradient(at 10% 29%, hsla(256, 96%, 67%, 1) 0, transparent 50%),
    radial-gradient(at 97% 96%, hsla(38, 60%, 74%, 1) 0, transparent 50%),
    radial-gradient(at 33% 50%, hsla(222, 67%, 73%, 1) 0, transparent 50%),
    radial-gradient(at 79% 53%, hsla(343, 68%, 79%, 1) 0, transparent 50%);
}

/* Animated mesh gradient */
@keyframes mesh-animation {
  0%, 100% {
    background-position: 0% 0%, 100% 0%, 50% 100%, 0% 50%, 100% 100%, 30% 50%, 70% 50%;
  }
  50% {
    background-position: 100% 100%, 0% 100%, 50% 0%, 100% 50%, 0% 0%, 70% 50%, 30% 50%;
  }
}

.animated-mesh {
  background: /* same as above */;
  background-size: 200% 200%;
  animation: mesh-animation 15s ease infinite;
}
```

### Code Example (SVG Approach)
```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:rgb(255,100,150);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(100,150,255);stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="400" height="400" fill="url(#grad1)"/>
</svg>
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | All     | Supported (CSS gradients) |
| Firefox | All     | Supported (CSS gradients) |
| Safari  | All     | Supported (CSS gradients) |

### Fallback Strategy
Mesh gradients using standard CSS properties have universal support. No fallback needed for basic implementation. For animated versions:
```css
@media (prefers-reduced-motion: reduce) {
  .animated-mesh {
    animation: none;
  }
}
```

### Performance Notes
- **Paint cost:** Medium (multiple gradients = multiple paint operations)
- **Composite cost:** Low-Medium (can be GPU-accelerated if promoted)
- **Layout cost:** Low
- **Mobile considerations:**
  - Limit to 5-7 radial gradients maximum
  - Avoid animating background-position on low-end devices
  - Use `will-change: background-position` sparingly

### Real-World Example
- **Site:** Stripe.com homepage
- **Implementation:** 5-6 radial gradients with subtle animation, color-adjusted for brand

### Sources
- [Medium: Moving Mesh Gradient Backgrounds](https://medium.com/design-bootcamp/bringing-life-to-your-website-with-moving-mesh-gradient-backgrounds-20b7e26844a2) — Implementation guide
- [Better Gradient: Mesh Gradient Guide](https://better-gradient.com/guide) — Generator tool documentation

---

## 3. Noise/Grain Textures

### Description
SVG feTurbulence filters applied as CSS backgrounds, enhanced with contrast/brightness filters to create realistic grainy overlays. Reduces banding in gradients, adds texture.

### Code Example
```html
<!-- noise.svg (inline or external file) -->
<svg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'>
  <filter id='noiseFilter'>
    <feTurbulence
      type='fractalNoise'
      baseFrequency='0.65'
      numOctaves='3'
      stitchTiles='stitch'/>
  </filter>
  <rect width='100%' height='100%' filter='url(#noiseFilter)'/>
</svg>
```

```css
.grainy-gradient {
  background:
    linear-gradient(to right, #7f5fff, transparent),
    url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
  filter: contrast(170%) brightness(1000%);
}

/* Chrome-specific adjustment */
@media all and (-webkit-min-device-pixel-ratio:0) and (min-resolution: .001dpcm) {
  .grainy-gradient {
    filter: contrast(290%) brightness(1000%);
  }
}

/* Alternative: CSS mask approach for better color control */
.masked-grain {
  background: radial-gradient(circle at 50% 50%, #7f5fff, #fa709a);
  mask:
    url('noise.svg'),
    radial-gradient(circle at 50%, transparent 25%, #000 65%);
}
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 5+      | Supported (SVG as background) |
| Firefox | 24+     | Supported |
| Safari  | 5+      | Supported |

SVG filters + CSS filter property = universal modern browser support.

### Fallback Strategy
```css
@supports not (filter: contrast(170%)) {
  .grainy-gradient {
    background: linear-gradient(to right, #7f5fff, #fa709a);
    /* Solid gradient without noise */
  }
}
```

### Performance Notes
- **Paint cost:** Medium (SVG filter rendering + CSS filters)
- **Composite cost:** Medium (filter creates new layer)
- **Layout cost:** Low
- **Mobile considerations:**
  - Data URI approach is performant (no extra HTTP request)
  - Keep SVG viewBox small (200x200 max)
  - Avoid on large background areas (>1000px)
  - Static noise performs well; animated noise = high cost

### Real-World Example
- **Site:** Codrops article examples
- **Implementation:** Noise overlay on gradient backgrounds for anti-banding

### Sources
- [CSS-Tricks: Grainy Gradients](https://css-tricks.com/grainy-gradients/) — Canonical implementation (Sep 2021)
- [Codrops: SVG feTurbulence](https://tympanus.net/codrops/2019/02/19/svg-filter-effects-creating-texture-with-feturbulence/) — Filter deep-dive
- [fffuel nnnoise generator](https://fffuel.co/nnnoise/) — SVG noise tool

---

## 4. Aurora/Northern Lights Gradients

### Description
Animated conic/radial gradients using oklch color space for perceptually uniform color transitions, creating ethereal, shifting light effects.

### Code Example
```css
@keyframes aurora {
  0%, 100% {
    background-position: 0% 50%, 100% 50%, 50% 100%;
  }
  50% {
    background-position: 100% 50%, 0% 50%, 50% 0%;
  }
}

.aurora-effect {
  background:
    radial-gradient(ellipse at 30% 50%, oklch(0.7 0.3 280), transparent 50%),
    radial-gradient(ellipse at 70% 50%, oklch(0.7 0.3 180), transparent 50%),
    radial-gradient(ellipse at 50% 80%, oklch(0.6 0.25 330), transparent 60%),
    linear-gradient(180deg, #001a33 0%, #000811 100%);
  background-size: 200% 200%, 200% 200%, 200% 200%, 100% 100%;
  animation: aurora 20s ease-in-out infinite;
}

/* Alternative with @property for smoother interpolation */
@property --aurora-hue-1 {
  syntax: '<number>';
  initial-value: 280;
  inherits: false;
}

@property --aurora-hue-2 {
  syntax: '<number>';
  initial-value: 180;
  inherits: false;
}

@keyframes hue-shift {
  0%, 100% {
    --aurora-hue-1: 280;
    --aurora-hue-2: 180;
  }
  50% {
    --aurora-hue-1: 330;
    --aurora-hue-2: 240;
  }
}

.aurora-modern {
  background:
    radial-gradient(ellipse at 30% 50%, oklch(0.7 0.3 var(--aurora-hue-1)), transparent 50%),
    radial-gradient(ellipse at 70% 50%, oklch(0.7 0.3 var(--aurora-hue-2)), transparent 50%),
    #001a33;
  animation: hue-shift 15s ease-in-out infinite;
}
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 111+    | Supported (oklch) |
| Firefox | 113+    | Supported (oklch) |
| Safari  | 15.4+   | Supported (oklch) |

oklch() = Baseline Newly Available (2024)

### Fallback Strategy
```css
.aurora-effect {
  /* Fallback with rgb/hsl */
  background:
    radial-gradient(ellipse at 30% 50%, hsl(280, 70%, 60%), transparent 50%),
    radial-gradient(ellipse at 70% 50%, hsl(180, 70%, 60%), transparent 50%),
    #001a33;
}

@supports (background: oklch(0.5 0.2 180)) {
  .aurora-effect {
    /* oklch version here */
  }
}
```

### Performance Notes
- **Paint cost:** High (multiple animated gradients)
- **Composite cost:** Medium-High (can be promoted to GPU)
- **Layout cost:** Low
- **Mobile considerations:**
  - Use `will-change: background-position` (remove after animation)
  - Reduce to 2-3 gradient layers on mobile
  - Consider `prefers-reduced-motion` to disable
  - oklch calculation is negligible performance cost vs HSL

### Real-World Example
- **Site:** Dalton Walsh portfolio
- **Implementation:** 3-layer aurora with SCSS functions for color generation

### Sources
- [Medium: OKLCH Color Space 2025](https://medium.com/@alexdev82/oklch-the-modern-css-color-space-you-should-be-using-in-2025-52dd1a4aa9d0) — oklch explanation
- [DEV.to: CSS Aurora Effect](https://dev.to/oobleck/css-aurora-effect-569n) — Implementation guide
- [Evil Martians: OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl) — Why oklch (2024)

---

## 5. Animated Gradient Borders

### Description
Rotating conic gradients confined to border-box using background layering, animated via @property for smooth custom property transitions.

### Code Example
```css
@property --gradient-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

@keyframes rotate-border {
  to {
    --gradient-angle: 360deg;
  }
}

.animated-border {
  --border-width: 2px;

  background:
    /* Inner fill */
    linear-gradient(#1a1a1a, #1a1a1a) padding-box,
    /* Rotating gradient border */
    conic-gradient(
      from var(--gradient-angle),
      transparent 0%,
      #00d4ff 10%,
      #ff00ea 30%,
      transparent 50%
    ) border-box;

  border: var(--border-width) solid transparent;
  border-radius: 8px;
  animation: rotate-border 3s linear infinite;
}

/* Hover state: pause and expand */
.animated-border:hover {
  animation-play-state: paused;
  --gradient-angle: 45deg;
}

/* Multi-color shimmer variant */
.shimmer-border {
  background:
    linear-gradient(#000, #000) padding-box,
    conic-gradient(
      from var(--gradient-angle),
      #ff00ea 0deg,
      #00d4ff 90deg,
      #ff00ea 180deg,
      #00d4ff 270deg,
      #ff00ea 360deg
    ) border-box;
  border: var(--border-width) solid transparent;
  animation: rotate-border 2s linear infinite;
}
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 85+     | Supported (@property), 69+ (conic-gradient) |
| Firefox | 128+    | Supported (@property), 83+ (conic-gradient) |
| Safari  | 15.4+   | Supported (@property + conic-gradient) |

@property = Baseline Newly Available (July 2024)

### Fallback Strategy
```css
/* Static gradient border for browsers without @property */
.animated-border {
  background:
    linear-gradient(#1a1a1a, #1a1a1a) padding-box,
    linear-gradient(135deg, #00d4ff, #ff00ea) border-box;
  border: 2px solid transparent;
}

@supports (background: conic-gradient(red, blue)) and (animation-timeline: scroll()) {
  .animated-border {
    /* Animated version */
  }
}
```

### Performance Notes
- **Paint cost:** Medium (conic-gradient recalculation each frame)
- **Composite cost:** Low-Medium (can be composited if isolated)
- **Layout cost:** Low
- **Mobile considerations:**
  - Animation is GPU-accelerated via transform
  - @property interpolation adds minimal overhead
  - Safe to use on buttons/cards (small surface area)
  - Avoid on large containers (>500px edges)

### Real-World Example
- **Site:** Bejamas (bejamas.com)
- **Implementation:** 4-color conic gradient with 3s rotation, pauses on hover

### Sources
- [Ryan Mulligan: CSS @property and the New Style](https://ryanmulligan.dev/blog/css-property-new-style/) — @property deep-dive (Sep 2024)
- [Bejamas: Animated Gradient Borders](https://bejamas.com/hub/guides/css-animated-gradient-border) — 4 techniques comparison
- [Bram.us: Animating CSS Gradient Border](https://www.bram.us/2021/01/29/animating-a-css-gradient-border/) — Original technique

---

## 6. Text Effects (Gradient Clipping, Strokes, Variable Fonts)

### Description
Multi-layered text styling using background-clip, text-stroke, and variable font axis animations for dynamic typography.

### Code Example
```css
/* Gradient text with background-clip */
.gradient-text {
  background: linear-gradient(90deg, #00d4ff, #ff00ea, #ffd000);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent; /* Fallback */
}

/* Animated gradient text */
@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.animated-gradient-text {
  background: linear-gradient(90deg, #00d4ff, #ff00ea, #ffd000, #00d4ff);
  background-size: 200% auto;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-shift 3s linear infinite;
}

/* Text stroke (outline) */
.stroke-text {
  color: transparent;
  -webkit-text-stroke: 2px #00d4ff;
  text-stroke: 2px #00d4ff;
}

/* Variable font animation */
@font-face {
  font-family: 'InterVariable';
  src: url('Inter-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-style: oblique 0deg 10deg;
}

@keyframes breathe {
  0%, 100% { font-variation-settings: 'wght' 400; }
  50% { font-variation-settings: 'wght' 700; }
}

.variable-font-text {
  font-family: 'InterVariable', sans-serif;
  animation: breathe 2s ease-in-out infinite;
}

/* Combined: gradient + stroke + variable font */
.ultimate-text {
  font-family: 'InterVariable', sans-serif;
  font-size: 4rem;
  background: linear-gradient(90deg, #ff00ea, #00d4ff);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  -webkit-text-stroke: 1px rgba(255, 255, 255, 0.3);
  animation: breathe 3s ease-in-out infinite;
}
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 3+ (background-clip), 120+ (text-stroke standard), All (variable fonts) |
| Firefox | 49+ (background-clip), 132+ (text-stroke), 62+ (variable fonts) |
| Safari  | 4+ (background-clip), All (-webkit-text-stroke), 11+ (variable fonts) |

background-clip: text requires -webkit- prefix universally

### Fallback Strategy
```css
.gradient-text {
  color: #00d4ff; /* Solid color fallback */
}

@supports (background-clip: text) or (-webkit-background-clip: text) {
  .gradient-text {
    background: linear-gradient(90deg, #00d4ff, #ff00ea);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }
}

/* Variable font fallback */
.variable-font-text {
  font-family: 'InterVariable', 'Inter', sans-serif;
  font-weight: 400;
}

@supports (font-variation-settings: 'wght' 400) {
  .variable-font-text {
    animation: breathe 2s ease-in-out infinite;
  }
}
```

### Performance Notes
- **Paint cost:** Medium (gradient recalculation on each frame if animated)
- **Composite cost:** Low (text layers are typically composited)
- **Layout cost:** Low (no layout triggers)
- **Mobile considerations:**
  - background-clip: text is well-optimized
  - Animated gradients: use `will-change: background-position` sparingly
  - Variable fonts: slightly larger file size but excellent performance
  - text-stroke: minimal performance impact

### Real-World Example
- **Site:** Stripe.com homepage
- **Implementation:** Gradient text on hero headlines, variable font weight transitions

### Sources
- [Prismic: CSS Text Animations](https://prismic.io/blog/css-text-animations) — 40 examples (2024)
- [FreeFrontend: 133 CSS Text Effects](https://freefrontend.com/css-text-effects/) — Curated collection
- [Amresh Prajapati: Top 20 CSS Text Animations](https://amreshprajapati.com/top-20-best-css-text-animations/) — Variable font examples

---

## 7. Container Queries

### Description
Component-level responsive design based on container dimensions rather than viewport, enabling truly reusable components.

### Code Example
```css
/* Define container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Alternative shorthand */
.sidebar {
  container: sidebar / inline-size;
}

/* Query the container */
@container card (width > 700px) {
  .card {
    display: grid;
    grid-template-columns: 2fr 1fr;
  }

  .card h2 {
    font-size: 2em;
  }
}

@container card (width <= 700px) {
  .card {
    display: block;
  }

  .card h2 {
    font-size: 1.2em;
  }
}

/* Container query units */
.responsive-text {
  font-size: clamp(1rem, 5cqi, 3rem);
  padding: 2cqh 4cqi;
}

/* Real-world pattern: responsive card grid */
.product-grid {
  container-type: inline-size;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

@container (width > 600px) {
  .product-card {
    aspect-ratio: 1 / 1.2;
  }
}

@container (width > 900px) {
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

/* Container query units reference:
   cqw: 1% of container width
   cqh: 1% of container height
   cqi: 1% of container inline size
   cqb: 1% of container block size
   cqmin: smaller of cqi or cqb
   cqmax: larger of cqi or cqb
*/
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 105+    | Supported |
| Firefox | 110+    | Supported |
| Safari  | 16+     | Supported |

Baseline Widely Available since February 2023

### Fallback Strategy
```css
/* Mobile-first approach without container queries */
.card {
  display: block;
}

.card h2 {
  font-size: 1.2em;
}

/* Media query fallback for larger viewports */
@media (min-width: 768px) {
  .card {
    display: grid;
    grid-template-columns: 2fr 1fr;
  }

  .card h2 {
    font-size: 2em;
  }
}

/* Feature detection */
@supports (container-type: inline-size) {
  .card-container {
    container-type: inline-size;
  }

  @container (width > 700px) {
    .card {
      display: grid;
      grid-template-columns: 2fr 1fr;
    }
  }
}
```

### Performance Notes
- **Paint cost:** Low (no additional painting overhead)
- **Composite cost:** Low
- **Layout cost:** Medium (container queries can trigger more frequent layout calculations than media queries, but modern browsers optimize this)
- **Mobile considerations:**
  - Excellent for component libraries (truly portable components)
  - No performance penalty on mobile
  - Use inline-size over size when possible (only constrains one axis)
  - Pair with CSS containment for performance gains

### Real-World Example
- **Site:** web.dev article layouts
- **Implementation:** Responsive article cards that adapt to sidebar vs full-width contexts

### Sources
- [MDN: CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries) — Official documentation
- [web.dev: Container Queries in Action](https://web.dev/articles/baseline-in-action-container-queries) — Implementation guide
- [Medium: Container Queries 2025](https://medium.com/@vyakymenko/css-2025-container-queries-and-style-queries-in-real-projects-c38af5a13aa2) — Real-world patterns

---

## 8. CSS Scroll-Driven Animations

### Description
Animations driven by scroll position using animation-timeline: scroll() or view(), eliminating JavaScript for scroll-triggered effects.

### Code Example
```css
/* Scroll timeline on container */
.scroll-container {
  scroll-timeline: --main-timeline;
}

/* Animate based on container scroll */
.scroll-animated {
  animation: fade-in linear;
  animation-timeline: --main-timeline;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Using scroll() function (no named timeline required) */
.parallax-bg {
  animation: parallax linear;
  animation-timeline: scroll(block nearest);
}

@keyframes parallax {
  to { transform: translateY(-200px); }
}

/* View-based timeline (element entering/exiting viewport) */
.reveal-on-scroll {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 25% cover 50%;
}

@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(100px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Practical example: sticky header shadow */
header {
  position: sticky;
  top: 0;
  animation: header-shadow linear;
  animation-timeline: scroll(root);
  animation-range: 0 100px;
}

@keyframes header-shadow {
  to {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
}

/* Horizontal scroll indicator */
.progress-bar {
  width: 0%;
  height: 4px;
  background: linear-gradient(90deg, #00d4ff, #ff00ea);
  position: fixed;
  top: 0;
  left: 0;
  animation: progress linear;
  animation-timeline: scroll(root);
}

@keyframes progress {
  to { width: 100%; }
}
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 115+    | Supported |
| Firefox | 111+ (behind flag until 131+) | Supported in 131+ |
| Safari  | 18+ (2024) | Supported (TP in 17.5) |

Baseline Newly Available (2024)

### Fallback Strategy
```css
/* Fallback: use Intersection Observer in JS or static state */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(100px);
  transition: opacity 0.6s, transform 0.6s;
}

.reveal-on-scroll.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Feature detection */
@supports (animation-timeline: scroll()) {
  .reveal-on-scroll {
    animation: reveal linear both;
    animation-timeline: view();
  }

  .reveal-on-scroll.is-visible {
    /* Remove JS-applied class styles */
    opacity: revert;
    transform: revert;
  }
}
```

### Performance Notes
- **Paint cost:** Low-Medium (depends on animation complexity)
- **Composite cost:** Low (scroll-linked animations are highly optimized, run on compositor thread)
- **Layout cost:** Low (no layout triggered by scroll itself)
- **Mobile considerations:**
  - Excellent performance (GPU-accelerated, compositor-driven)
  - No JS scroll event listeners = better performance than Intersection Observer
  - Respects prefers-reduced-motion automatically when animation is disabled
  - Use animation-range to limit active scroll ranges (better than full-page animations)

### Real-World Example
- **Site:** Apple product pages
- **Implementation:** View-based timelines for progressive image reveals and parallax effects

### Sources
- [MDN: Scroll-Driven Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) — Official documentation (Jan 2026)
- [CSS-Tricks: Scroll-Based Animations with view()](https://css-tricks.com/creating-scroll-based-animations-in-full-view/) — Practical guide
- [Codrops: Practical Introduction](https://tympanus.net/codrops/2024/01/17/a-practical-introduction-to-scroll-driven-animations-with-css-scroll-and-view/) — Real examples (Jan 2024)

---

## 9. View Transitions API

### Description
Smooth animated transitions between DOM states (same-document) or navigation (cross-document), natively handles element morphing and fade effects.

### Code Example (Same-Document)
```javascript
// Basic same-document transition
function updateView() {
  document.startViewTransition(() => {
    // DOM updates here
    document.querySelector('.content').innerHTML = newContent;
  });
}

// Named transitions for specific elements
document.startViewTransition(() => {
  updateDOM();
}).ready.then(() => {
  console.log('Transition ready');
});
```

```css
/* Default cross-fade for all elements */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}

/* Isolate specific element for custom animation */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: 0.5s;
  animation-timing-function: ease-in-out;
}

/* Custom animation: slide + fade */
@keyframes slide-from-right {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
}

@keyframes slide-to-left {
  to {
    transform: translateX(-100%);
    opacity: 0;
  }
}

::view-transition-old(slide) {
  animation: slide-to-left 0.4s ease-in;
}

::view-transition-new(slide) {
  animation: slide-from-right 0.4s ease-out;
}

/* View transition types (Chrome 125+) */
@supports (view-transition-name: none) {
  @media (prefers-reduced-motion: no-preference) {
    .slide-transition {
      view-transition-name: slide;
    }
  }
}
```

### Code Example (Cross-Document - Experimental)
```html
<!-- Page 1 -->
<style>
  @view-transition {
    navigation: auto;
  }

  .product-image {
    view-transition-name: product-hero;
  }
</style>

<!-- Page 2 (same view-transition-name morphs elements) -->
<style>
  @view-transition {
    navigation: auto;
  }

  .detail-image {
    view-transition-name: product-hero;
  }
</style>
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 111+ (same-doc), 126+ (cross-doc behind flag) | Supported (same-doc) |
| Firefox | 129+ (behind flag) | Partial |
| Safari  | 18+ (same-doc) | Supported (since Oct 2024) |

**Same-document:** Baseline Newly Available (October 2024)
**Cross-document:** Experimental (Chrome 126+ with flag)

### Fallback Strategy
```javascript
// Feature detection + graceful degradation
function updateWithTransition(updateCallback) {
  if (document.startViewTransition) {
    document.startViewTransition(updateCallback);
  } else {
    // Fallback: instant update
    updateCallback();
  }
}

// CSS: ensure content is visible without transitions
.content {
  /* Default visible state */
  opacity: 1;
}

@supports (view-transition-name: none) {
  /* Transition-specific styles */
}
```

### Performance Notes
- **Paint cost:** Medium-High (captures snapshots of old and new states)
- **Composite cost:** Medium (composites old/new layers during transition)
- **Layout cost:** Low (transition happens after layout)
- **Mobile considerations:**
  - Memory cost: snapshots can be large on high-DPI screens
  - Limit number of named view-transitions (max 5-10 per transition)
  - Use view-transition-class to group elements (Chrome 126+)
  - Test on actual devices (can cause jank on low-end hardware)
  - Respects prefers-reduced-motion (skips animation)

### Real-World Example
- **Site:** Chrome DevRel demos (view-transitions.chrome.dev)
- **Implementation:** Image gallery with morphing transitions, SPA navigation

### Sources
- [Chrome Developers: View Transitions 2025 Update](https://developer.chrome.com/blog/view-transitions-in-2025) — Latest features
- [MDN: View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) — Official documentation
- [web.dev: Same-Document View Transitions Baseline](https://web.dev/blog/same-document-view-transitions-are-now-baseline-newly-available) — Oct 2024 announcement

---

## 10. @starting-style (Entry Animations)

### Description
Defines initial styles for CSS transitions on newly created elements, enabling fade-in/slide-in effects without JavaScript or keyframes.

### Code Example
```css
/* Basic fade-in on element creation */
.dialog {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.3s, transform 0.3s;

  @starting-style {
    opacity: 0;
    transform: scale(0.9);
  }
}

/* Slide in from top */
.notification {
  translate: 0 0;
  transition: translate 0.4s ease-out;

  @starting-style {
    translate: 0 -100px;
  }
}

/* Combined with display: none transitions (Chrome 116+) */
.modal {
  display: none;
  opacity: 0;
  transition:
    opacity 0.3s,
    display 0.3s allow-discrete,
    overlay 0.3s allow-discrete;

  @starting-style {
    opacity: 0;
  }
}

.modal[open] {
  display: block;
  opacity: 1;
}

/* Practical example: dynamic list items */
.list-item {
  opacity: 1;
  translate: 0 0;
  transition: opacity 0.3s, translate 0.3s;

  @starting-style {
    opacity: 0;
    translate: -20px 0;
  }
}

/* Gotcha: specificity matters! */
/* This WON'T work if higher-specificity rule sets opacity elsewhere */
.box {
  transition: opacity 500ms;

  @starting-style {
    opacity: 0; /* May be overridden by #id selector */
  }
}

/* Solution: use !important or increase specificity */
.box {
  @starting-style {
    opacity: 0 !important; /* Nuclear option */
  }
}

/* Alternative: use keyframes (more reliable) */
@keyframes fade-in {
  from { opacity: 0; }
}

.box {
  animation: fade-in 500ms;
}
```

### Browser Support (2025)

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 117+    | Supported |
| Firefox | 129+    | Supported |
| Safari  | 17.5+   | Supported |

Baseline Widely Available since August 2024

### Fallback Strategy
```css
/* Fallback: instant appearance (acceptable UX degradation) */
.notification {
  opacity: 1;
  translate: 0 0;
}

/* Or use keyframes for broader support */
@keyframes slide-in {
  from { translate: 0 -100px; }
}

.notification {
  animation: slide-in 0.4s ease-out;
}

@supports (selector(@starting-style)) {
  .notification {
    animation: none;
    transition: translate 0.4s ease-out;

    @starting-style {
      translate: 0 -100px;
    }
  }
}
```

### Performance Notes
- **Paint cost:** Low (same as regular transitions)
- **Composite cost:** Low (compositor-driven if using transform/opacity)
- **Layout cost:** Low (triggered once on element creation)
- **Mobile considerations:**
  - Identical performance to regular CSS transitions
  - Use transform/opacity for GPU acceleration
  - Avoid animating layout properties (width, height, top, left)
  - **Specificity gotcha:** @starting-style isn't promoted like @keyframes, can be overridden by higher-specificity rules

### Real-World Example
- **Site:** Josh W. Comeau blog (particle effects)
- **Implementation:** Initially used @starting-style, reverted to keyframes due to specificity issues with inline styles

### Sources
- [Josh Comeau: The Big Gotcha with @starting-style](https://www.joshwcomeau.com/css/starting-style/) — Specificity deep-dive (Sep 2025)
- [MDN: @starting-style](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@starting-style) — Official documentation
- [CSS-Tricks: @starting-style](https://css-tricks.com/almanac/rules/s/starting-style/) — Quick reference

---

## 11. Popover API + Anchor Positioning

### Description
Native popover/tooltip/dropdown positioning with CSS anchor-positioning, eliminating JavaScript libraries like Popper.js.

### Code Example (Popover)
```html
<button popovertarget="my-popover">Open Popover</button>
<div id="my-popover" popover>
  <p>This is a popover!</p>
</div>
```

```css
/* Basic popover styling */
[popover] {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Entry/exit animations with @starting-style */
[popover]:popover-open {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.2s, transform 0.2s, display 0.2s allow-discrete;

  @starting-style {
    opacity: 0;
    transform: scale(0.95);
  }
}

/* Backdrop */
[popover]::backdrop {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}
```

### Code Example (Anchor Positioning - Experimental)
```html
<button id="anchor-btn">Button</button>
<div id="tooltip" popover>Tooltip content</div>
```

```css
/* Anchor positioning (Chrome 125+, behind flag in other browsers) */
#anchor-btn {
  anchor-name: --button-anchor;
}

#tooltip {
  position: fixed;
  position-anchor: --button-anchor;

  /* Position below button, centered */
  top: calc(anchor(bottom) + 8px);
  left: anchor(center);
  translate: -50% 0;

  /* Auto-adjust if overflow */
  position-try-fallbacks: flip-block, flip-inline;
}

/* Alternative positioning options */
#tooltip-top {
  position-anchor: --button-anchor;
  bottom: calc(anchor(top) - 8px);
  left: anchor(center);
  translate: -50% 0;
}

/* Anchor positioning with arrow */
#tooltip::before {
  content: '';
  position: absolute;
  bottom: 100%;
  left: 50%;
  translate: -50% 0;
  border: 8px solid transparent;
  border-bottom-color: white;
}
```

### Browser Support (2025)

**Popover API:**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 114+    | Supported |
| Firefox | 125+    | Supported |
| Safari  | 17+     | Supported |

Baseline Widely Available since April 2024

**Anchor Positioning (CSS Anchor Position API):**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 125+ (behind flag) | Partial |
| Firefox | No support (planned for 2025) | No |
| Safari  | No support (Interop 2025 focus) | No |

Experimental (Interop 2025 target = expected cross-browser Q4 2025)

### Fallback Strategy
```css
/* Popover fallback: dialog element or hidden div */
[popover] {
  /* Modern browsers: native popover */
}

@supports not (selector([popover])) {
  [popover] {
    display: none;
  }

  [popover][data-open] {
    display: block;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/* Anchor positioning fallback: manual positioning */
#tooltip {
  position: fixed;
  top: calc(var(--anchor-top) + var(--anchor-height) + 8px);
  left: calc(var(--anchor-left) + var(--anchor-width) / 2);
  transform: translateX(-50%);
}

@supports (top: anchor(bottom)) {
  #tooltip {
    position-anchor: --button-anchor;
    top: calc(anchor(bottom) + 8px);
    left: anchor(center);
    translate: -50% 0;
  }
}
```

### Performance Notes
- **Paint cost:** Low (popover API is optimized)
- **Composite cost:** Low (top-layer rendering)
- **Layout cost:** Low-Medium (anchor positioning recalculates on anchor movement, but optimized)
- **Mobile considerations:**
  - Popover API: excellent performance, native accessibility
  - Anchor positioning: recalculates on scroll/resize (monitor performance)
  - Use inert on background content when popover is open
  - Touch targets: ensure 44x44px minimum for popover triggers

### Real-World Example
- **Site:** Chrome DevRel demos
- **Implementation:** Tooltip system with anchor positioning for complex layouts

### Sources
- [Chrome Developers: Anchor Positioning API](https://developer.chrome.com/docs/css-ui/anchor-positioning-api) — Official guide
- [MDN: Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API/Using) — Documentation
- [InfoQ: Interop 2025 Features](https://www.infoq.com/news/2025/04/interop-2025-key-features/) — Anchor positioning roadmap

---

## 12. CSS Nesting, :has() Selector, Subgrid

### Description
Modern layout and selector capabilities: native CSS nesting (no preprocessor), parent/sibling selection via :has(), and nested grid alignment with subgrid.

### Code Example (Nesting)
```css
/* Native CSS nesting (Chrome 120+, Firefox 117+, Safari 16.5+) */
.card {
  padding: 1rem;
  background: white;
  border-radius: 8px;

  & h2 {
    font-size: 1.5rem;
    color: #333;
  }

  & p {
    color: #666;
    line-height: 1.6;
  }

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  &.featured {
    border: 2px solid #00d4ff;
  }

  /* Nested media queries */
  @media (width < 600px) {
    padding: 0.5rem;

    & h2 {
      font-size: 1.2rem;
    }
  }
}

/* Nesting without & (direct child) */
.nav {
  ul {
    list-style: none;
  }

  li {
    display: inline-block;
  }
}
```

### Code Example (:has() Selector)
```css
/* Parent selector: style form if it has error */
form:has(.error) {
  border: 2px solid red;
}

/* Previous sibling selector */
h2:has(+ .warning) {
  color: orange;
}

/* Conditional styling: card with image */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}

.card:not(:has(img)) {
  display: block;
}

/* State-based parent styling */
.checkbox-group:has(:checked) {
  background: #e8f5e9;
}

/* Complex: form validation */
form:has(input:invalid) button[type="submit"] {
  opacity: 0.5;
  pointer-events: none;
}

/* :has() with :nth-child (quantity queries) */
/* Style parent if it has exactly 3 children */
ul:has(li:nth-child(3):last-child) {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
```

### Code Example (Subgrid)
```css
/* Classic problem: aligning nested grid items */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.card {
  display: grid;
  grid-template-rows: subgrid; /* Inherits parent row tracks */
  grid-row: span 3; /* Card spans 3 rows */
}

/* All cards align their headers, content, and footers */
.card h3 { grid-row: 1; }
.card .content { grid-row: 2; }
.card .footer { grid-row: 3; }

/* Full example: magazine layout */
.article-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: auto auto auto;
  gap: 2rem;
}

.article {
  display: grid;
  grid-template-columns: subgrid;
  grid-column: span 12;

  @media (width >= 768px) {
    grid-column: span 6;
  }

  @media (width >= 1024px) {
    grid-column: span 4;
  }
}

.article__image {
  grid-column: 1 / -1;
}

.article__title {
  grid-column: 1 / -1;
}

.article__meta {
  grid-column: 1 / 7;
}

.article__action {
  grid-column: 7 / -1;
  justify-self: end;
}
```

### Browser Support (2025)

**CSS Nesting:**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 120+    | Supported |
| Firefox | 117+    | Supported |
| Safari  | 16.5+   | Supported |

Baseline Widely Available since August 2023

**:has() Selector:**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 105+    | Supported |
| Firefox | 121+    | Supported |
| Safari  | 15.4+   | Supported |

Baseline Widely Available since December 2023

**Subgrid:**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 117+    | Supported |
| Firefox | 71+     | Supported |
| Safari  | 16+     | Supported |

Baseline Widely Available since September 2023

### Fallback Strategy
```css
/* Nesting fallback: flatten selectors */
.card {
  padding: 1rem;
}

.card h2 {
  font-size: 1.5rem;
}

/* :has() fallback: use classes */
.form-with-error {
  border: 2px solid red;
}

/* Add class via JS: form.classList.toggle('form-with-error', hasError) */

/* Subgrid fallback: manual alignment */
.card {
  display: grid;
  grid-template-rows: auto 1fr auto; /* Manual row sizing */
}

@supports (grid-template-rows: subgrid) {
  .card {
    grid-template-rows: subgrid;
    grid-row: span 3;
  }
}
```

### Performance Notes
- **Paint cost:** Low (no additional painting for nesting/:has())
- **Composite cost:** Low
- **Layout cost:**
  - Nesting: No overhead (syntactic sugar)
  - :has(): Medium (reverse tree traversal, but highly optimized in modern browsers)
  - Subgrid: Low (more efficient than manual alignment)
- **Mobile considerations:**
  - Nesting: Zero performance impact
  - :has(): Slight cost for complex queries (e.g., :has(> div > .class)), but negligible in practice
  - Subgrid: Excellent for responsive layouts, no mobile-specific concerns

### Real-World Example
- **Site:** web.dev redesign (2024)
- **Implementation:** :has() for conditional card layouts, subgrid for article grids

### Sources
- [LogRocket: Different Ways to Use :has()](https://blog.logrocket.com/blog/different-ways-to-use-css-has/) — :has() guide
- [Medium: CSS Nesting Complete Guide](https://medium.com/@omken/css-nesting-the-complete-guide-with-examples-bdc63fb0856b) — Nesting examples
- [MDN: Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid) — Official documentation
- [Can I Use: CSS Nesting](https://caniuse.com/css-nesting) — Browser support

---

## 13. Color Manipulation (oklch, Relative Color Syntax, color-mix)

### Description
Perceptually uniform color spaces (oklch), dynamic color derivation (relative color syntax), and color blending (color-mix) for advanced theming.

### Code Example (oklch)
```css
/* oklch(lightness chroma hue) */
:root {
  /* Perceptually uniform lightness */
  --color-primary: oklch(0.6 0.25 250); /* Blue */
  --color-primary-light: oklch(0.8 0.25 250); /* Lighter, same hue */
  --color-primary-dark: oklch(0.4 0.25 250); /* Darker, same hue */

  /* No muddy gradients */
  --gradient-clean: linear-gradient(
    to right,
    oklch(0.7 0.3 30),  /* Orange */
    oklch(0.6 0.3 180)  /* Cyan */
  );

  /* Wide gamut (P3 colors) */
  --color-vivid: oklch(0.7 0.4 150); /* Exceeds sRGB */
}

/* Comparison: HSL vs OKLCH */
.hsl-gradient {
  background: linear-gradient(to right, hsl(0, 100%, 50%), hsl(120, 100%, 50%));
  /* Result: muddy middle (brown) */
}

.oklch-gradient {
  background: linear-gradient(to right, oklch(0.6 0.3 30), oklch(0.6 0.3 150));
  /* Result: vibrant transition */
}
```

### Code Example (Relative Color Syntax)
```css
:root {
  --brand-color: oklch(0.6 0.25 250);
}

/* Derive lighter/darker variants */
.button-primary {
  background: var(--brand-color);
  color: oklch(from var(--brand-color) calc(l + 0.3) c h); /* 30% lighter */
}

.button-primary:hover {
  background: oklch(from var(--brand-color) calc(l - 0.1) c h); /* 10% darker */
}

/* Adjust saturation */
.muted {
  color: oklch(from var(--brand-color) l calc(c * 0.5) h); /* 50% less saturated */
}

/* Rotate hue */
.complementary {
  color: oklch(from var(--brand-color) l c calc(h + 180)); /* Opposite hue */
}

/* Alpha manipulation */
.transparent-bg {
  background: oklch(from var(--brand-color) l c h / 0.1); /* 10% opacity */
}

/* Complex: generate full palette */
:root {
  --primary: oklch(0.55 0.22 250);
  --primary-50: oklch(from var(--primary) 0.95 calc(c * 0.5) h);
  --primary-100: oklch(from var(--primary) 0.9 calc(c * 0.7) h);
  --primary-200: oklch(from var(--primary) 0.8 calc(c * 0.85) h);
  --primary-500: var(--primary);
  --primary-900: oklch(from var(--primary) 0.25 c h);
}
```

### Code Example (color-mix)
```css
/* Mix two colors */
.blend {
  background: color-mix(in oklch, #00d4ff 50%, #ff00ea 50%);
}

/* Create tints/shades */
.tint {
  background: color-mix(in oklch, var(--brand-color) 80%, white 20%);
}

.shade {
  background: color-mix(in oklch, var(--brand-color) 70%, black 30%);
}

/* Dynamic theming */
:root {
  --surface: white;
  --on-surface: black;
}

[data-theme="dark"] {
  --surface: black;
  --on-surface: white;
}

.card {
  background: var(--surface);
  color: var(--on-surface);
  border: 1px solid color-mix(in oklch, var(--on-surface) 20%, transparent);
}

/* Color space matters: srgb vs oklch */
.srgb-mix {
  background: color-mix(in srgb, red, blue); /* Purple (muddy) */
}

.oklch-mix {
  background: color-mix(in oklch, oklch(0.6 0.3 30), oklch(0.6 0.3 270));
  /* Vibrant mix */
}
```

### Browser Support (2025)

**oklch():**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 111+    | Supported |
| Firefox | 113+    | Supported |
| Safari  | 15.4+   | Supported |

Baseline Newly Available (2024)

**Relative Color Syntax:**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 119+    | Supported |
| Firefox | 128+    | Supported |
| Safari  | 16.4+   | Supported |

Baseline Newly Available (2024)

**color-mix():**

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 111+    | Supported |
| Firefox | 113+    | Supported |
| Safari  | 16.2+   | Supported |

Baseline Newly Available (2024)

### Fallback Strategy
```css
/* oklch fallback */
:root {
  --color-primary: hsl(250, 60%, 55%); /* HSL fallback */
}

@supports (color: oklch(0.6 0.25 250)) {
  :root {
    --color-primary: oklch(0.6 0.25 250);
  }
}

/* Relative color syntax fallback */
.button-hover {
  background: hsl(250, 60%, 45%); /* Manually calculated darker */
}

@supports (background: oklch(from white l c h)) {
  .button-hover {
    background: oklch(from var(--brand-color) calc(l - 0.1) c h);
  }
}

/* color-mix fallback: manual mixing or Sass */
.blend {
  background: #7f6fd4; /* Pre-calculated mix */
}

@supports (background: color-mix(in oklch, red, blue)) {
  .blend {
    background: color-mix(in oklch, #00d4ff 50%, #ff00ea 50%);
  }
}
```

### Performance Notes
- **Paint cost:** Low (no difference vs rgb/hsl)
- **Composite cost:** Low
- **Layout cost:** Low
- **Mobile considerations:**
  - oklch/color-mix have zero runtime performance cost (resolved at parse time)
  - Relative color syntax: minimal calculation overhead
  - Wide gamut colors (P3) only visible on compatible displays (iPhone 13+, modern laptops)
  - No battery/performance impact

### Real-World Example
- **Site:** web.dev (Google)
- **Implementation:** oklch-based design tokens, relative color syntax for automatic dark mode variants

### Sources
- [MDN: oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch) — Official documentation
- [web.dev: Color Theme with Baseline CSS](https://web.dev/articles/baseline-in-action-color-theme) — Relative colors + color-mix guide
- [Ahmad Shadeed: CSS Relative Colors](https://ishadeed.com/article/css-relative-colors/) — Practical examples
- [Can I Use: Relative Colors](https://caniuse.com/css-relative-colors) — Browser support
