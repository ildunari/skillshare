# The 4-Layer CSS Architecture for Liquid Glass

Source: https://dev.to/fabiosleal/how-to-create-the-apple-liquid-glass-effect-with-css-and-svg-2o06
Source: https://blog.logrocket.com/how-create-liquid-glass-effects-css-and-svg/

---

## Layer Stack (bottom → top)

```
┌─────────────────────────────┐  z-index: 3  ← Layer 3: Content
│   Your text / icons / UI    │
├─────────────────────────────┤  z-index: 2  ← Layer 2: Specular rim
│  inset box-shadow highlight │
├─────────────────────────────┤  z-index: 1  ← Layer 1: Tint overlay
│  rgba semi-transparent fill │
├─────────────────────────────┤  z-index: 0  ← Layer 0: Distortion
│  backdrop-filter + SVG filt │
└─────────────────────────────┘
        (content behind)
```

---

## Minimal Implementation

```html
<div class="glass">
  <div class="glass__filter"></div>
  <div class="glass__tint"></div>
  <div class="glass__specular"></div>
  <div class="glass__content">
    <!-- Put your content here -->
  </div>
</div>

<svg style="display:none">
  <filter id="glass-filter" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.008" numOctaves="2" seed="92" result="noise"/>
    <feGaussianBlur in="noise" stdDeviation="2" result="blurred"/>
    <feDisplacementMap in="SourceGraphic" in2="blurred" scale="70"
      xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</svg>
```

```css
/* Container — must be relative + overflow:hidden */
.glass {
  position: relative;
  border-radius: 1.5rem;
  overflow: hidden;
}

/* Shared: all 3 pseudo-layers fill the container */
.glass__filter,
.glass__tint,
.glass__specular {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
}

/* Layer 0: distortion + blur */
.glass__filter {
  z-index: 0;
  backdrop-filter: blur(4px);
  filter: url(#glass-filter) saturate(120%) brightness(1.1);
  isolation: isolate;  /* prevents stacking context bleed */
}

/* Layer 1: semi-transparent tint */
.glass__tint {
  z-index: 1;
  background: rgba(255, 255, 255, 0.2);
}

/* Layer 2: specular highlight rim */
.glass__specular {
  z-index: 2;
  overflow: hidden;
  box-shadow:
    inset 1px 1px 0 rgba(255, 255, 255, 0.7),
    inset 0 0 6px rgba(255, 255, 255, 0.5);
}

/* Layer 3: content — sits above all visual layers */
.glass__content {
  position: relative;
  z-index: 3;
  padding: 1.25rem 1.5rem;
  color: white;
}
```

---

## CSS Custom Properties System

```css
:root {
  /* Glass appearance */
  --glass-bg:        rgba(255, 255, 255, 0.20);  /* tint opacity */
  --glass-highlight: rgba(255, 255, 255, 0.70);  /* specular rim */
  --glass-blur:      4px;                         /* backdrop blur */
  --glass-saturate:  120%;                        /* filter saturation */
  --glass-brightness:1.15;                        /* filter brightness */
  --glass-radius:    1.5rem;                      /* corner radius */
  --glass-shadow:    0 6px 6px rgba(0,0,0,0.2), 0 0 20px rgba(0,0,0,0.1);

  /* Text */
  --glass-text:      #ffffff;
  --glass-text-muted: rgba(255,255,255,0.6);

  /* Dark mode override */
  --glass-bg-dark:   rgba(0, 0, 0, 0.25);
  --glass-highlight-dark: rgba(255, 255, 255, 0.3);
}

/* Light background variant */
.glass--light {
  --glass-bg:        rgba(255, 255, 255, 0.45);
  --glass-text:      #1a1a1a;
  --glass-highlight: rgba(255, 255, 255, 0.9);
}

/* Dark background variant */
.glass--dark {
  --glass-bg:        rgba(0, 0, 0, 0.30);
  --glass-text:      #ffffff;
  --glass-highlight: rgba(255, 255, 255, 0.2);
}
```

---

## Size Variants

```css
.glass--sm   { border-radius: 1rem;   padding: 0.5rem 0.75rem; }
.glass--md   { border-radius: 1.5rem; padding: 1rem 1.25rem; }
.glass--lg   { border-radius: 2rem;   padding: 1.5rem 2rem; }
.glass--pill { border-radius: 9999px; padding: 0.5rem 1.5rem; }
.glass--card { border-radius: 1.5rem; min-width: 20rem; min-height: 12rem; }
```

---

## Interactive States

```css
/* Hover — scale up + enhanced glow */
.glass:hover {
  transform: scale(1.03);
  box-shadow: 0 12px 24px rgba(0,0,0,0.3), 0 0 40px rgba(0,0,0,0.15);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 2.2);
}

/* Active / pressed */
.glass:active {
  transform: scale(0.97);
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

/* Focus ring for accessibility */
.glass:focus-visible {
  outline: 2px solid rgba(255,255,255,0.6);
  outline-offset: 3px;
}
```

---

## Common Gotchas

1. **`overflow: hidden` is required** on `.glass` or the layers will bleed outside the border-radius.
2. **`isolation: isolate`** on `.glass__filter` prevents the `backdrop-filter` from compositing with unintended parent layers.
3. **`backdrop-filter: blur(0px)`** (not `blur(4px)`) on the filter layer is a valid trick when you want the SVG displacement to drive the warp and NOT add additional blur — the presence of `backdrop-filter` (even at 0) is needed to activate the backdrop compositing stack that allows `filter: url(...)` to see content behind.
4. **`border-radius: inherit`** on the inner layers ensures they follow the container's radius without being specified separately.
5. **z-index ordering** — don't forget `position: relative` on `.glass__content`, otherwise it won't stack above absolute siblings.
6. **Safari partial support** — the SVG displacement won't warp the backdrop in Safari, but blur + tint still renders fine (graceful degradation).

---

## Accessibility Checklist

- Ensure `--glass-text` has sufficient contrast ratio against `--glass-bg` (WCAG AA = 4.5:1)
- Use `@media (prefers-reduced-motion: reduce)` to disable animations:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .glass, .glass * { animation: none !important; transition: none !important; }
    body { animation: none !important; }
  }
  ```
- Never place interactive elements inside `.glass__filter` or `.glass__tint` layers — always put them in `.glass__content`.
- Use `pointer-events: none` on the 3 visual layers to avoid blocking mouse events.
