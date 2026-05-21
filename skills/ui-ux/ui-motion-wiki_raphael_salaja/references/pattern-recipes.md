# Animation Pattern Recipes

> Production-ready implementations of high-signal effects. Each recipe includes: core mechanism, working code, failure modes, and reduced-motion variant. CSS-first where possible; JS only when the mechanism demands it.

## Contents
- Foil / Holographic Surfaces → Goo / Blob Merging → Gradient Borders (mask compositing)
- Wipe Reveals (mask-based) → Spotlight Border Card (cursor-following glow)
- Dock Magnification (proximity hover) → Text Scramble → Char-by-Char Reveal (no DOM splitting)
- Particle Explosion Button → Kinetic Marquee → Dynamic Island Pill Morph

---

## Foil / Holographic Surfaces

### Mechanism
Multi-layer gradient stack (conic + radial + repeating linear) with blend modes (`screen`, `color-dodge`, `difference`) to simulate prismatic refraction. A moving specular highlight layer sells "material." No images needed — just gradients + blend.

### Implementation (CSS-only shimmer)

```css
.foil-card {
  --dur: 6s;
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  isolation: isolate;
  background: radial-gradient(120% 120% at 20% 0%, #1b1b2a, #0b0b10);
  color: white;
  padding: 1.25rem;
}

/* Refraction layer */
.foil-card::before {
  content: "";
  position: absolute;
  inset: -35%;
  background:
    conic-gradient(from 0.2turn,
      #22d3ee, #a78bfa, #fb7185, #fbbf24, #34d399, #22d3ee),
    repeating-linear-gradient(115deg,
      rgba(255,255,255,0.25) 0 1px,
      transparent 1px 6px);
  background-blend-mode: screen, normal;
  mix-blend-mode: color-dodge;
  opacity: 0.55;
  filter: saturate(1.25);
  animation: foil-pan var(--dur) ease-in-out infinite alternate;
  pointer-events: none;
  z-index: -1;
}

/* Specular highlight */
.foil-card::after {
  content: "";
  position: absolute;
  inset: -40%;
  background: radial-gradient(circle at 30% 30%,
    rgba(255,255,255,0.85), transparent 55%);
  mix-blend-mode: screen;
  opacity: 0.35;
  animation: foil-pan calc(var(--dur) * 0.75) ease-in-out infinite alternate-reverse;
  pointer-events: none;
}

@keyframes foil-pan {
  0%   { transform: translate3d(-12%, -10%, 0) rotate(0.03turn); }
  100% { transform: translate3d(12%, 10%, 0) rotate(-0.03turn); }
}

@media (prefers-reduced-motion: reduce) {
  .foil-card::before, .foil-card::after { animation: none; }
}
```

### Failure modes
- Blend modes produce different tonal results depending on background stacking and color management.
- Increased compositing complexity — keep bounded to single cards, not full-page overlays.
- Nested opacity/transform stacking contexts can cause unexpected blend behavior.

### Enhancement: pointer-following (requires JS)
Add `pointermove` listener → set `--mx` / `--my` CSS variables → shift gradient origin. The CSS structure stays the same; JS just feeds it coordinates.

---

## Goo / Blob Merging

### Mechanism
Blur multiple shapes so edges overlap, then increase contrast so overlaps "snap" into a single thick shape. Two approaches: CSS `filter: blur() contrast()` on a container, or SVG filter pipeline with `feGaussianBlur` + `feColorMatrix`.

### Implementation (CSS blur + contrast)

```css
.goo {
  position: relative;
  width: 260px;
  height: 140px;
  border-radius: 999px;
  background: #101018;
  overflow: hidden;
  filter: blur(16px) contrast(20);
}

.blob {
  position: absolute;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #fff, #bbb);
}

.b1 { left: 20px; top: 25px; animation: float1 3.6s ease-in-out infinite; }
.b2 { left: 90px; top: 15px; animation: float2 4.1s ease-in-out infinite; }
.b3 { left: 160px; top: 35px; animation: float3 3.9s ease-in-out infinite; }

@keyframes float1 { 50% { transform: translate(55px, -12px); } }
@keyframes float2 { 50% { transform: translate(-35px, 18px); } }
@keyframes float3 { 50% { transform: translate(-60px, -8px); } }

@media (prefers-reduced-motion: reduce) {
  .blob { animation: none; }
}
```

### SVG filter alternative (finer control)
```html
<svg width="0" height="0" style="position:absolute">
  <filter id="goo">
    <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"/>
    <feColorMatrix in="blur" mode="matrix"
      values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="goo"/>
    <feComposite in="SourceGraphic" in2="goo" operator="atop"/>
  </filter>
</svg>
<div style="filter: url(#goo)"><!-- blobs here --></div>
```

### Failure modes
- Heavy paint/composite work — treat as "hero moment," not ubiquitous UI accent.
- SVG filter can be especially expensive on low-power devices.
- The contrast trick distorts colors of content inside the container.

---

## Gradient Borders (Mask Compositing)

### Why this matters
Mainstream tutorials push `border-image` or background-clip hacks. Both break with rounded corners + translucent/blurred interiors. The production answer is **mask-composite cutout**.

### Mechanism
A pseudo-element fills the full card area with a gradient background. A mask (`mask-composite: exclude` / `-webkit-mask-composite: xor`) cuts out the center, leaving only the border ring visible.

### Implementation

```css
.gradient-border-btn {
  --r: 16px;
  --bw: 2px;
  position: relative;
  border: 0;
  border-radius: var(--r);
  padding: 0.9rem 1.1rem;
  background: rgba(20, 20, 30, 0.75);
  color: white;
  isolation: isolate;
}

.gradient-border-btn::before {
  content: "";
  position: absolute;
  inset: 0;
  padding: var(--bw);
  border-radius: inherit;
  background: conic-gradient(from 0turn,
    #7dd3fc, #a78bfa, #fb7185, #fbbf24, #34d399, #7dd3fc);

  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;

  animation: spin 3.5s linear infinite;
  z-index: -1;
}

@keyframes spin { to { transform: rotate(1turn); } }

@media (prefers-reduced-motion: reduce) {
  .gradient-border-btn::before { animation: none; }
}
```

### With `@property` for gradient angle animation
```css
@property --border-angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.gradient-border-btn::before {
  background: conic-gradient(from var(--border-angle), /* colors */);
  animation: spin-angle 3s linear infinite;
}

@keyframes spin-angle { to { --border-angle: 360deg; } }
```

### Failure modes
- `mask-composite` / `-webkit-mask-composite` syntax differs across engines — use both prefixed and unprefixed.
- Progressive enhancement: ensure the element is readable without the gradient border.
- Gate behind `@supports` for mask-composite if targeting older browsers.

---

## Wipe Reveals (Mask-Based)

### Mechanism
Animate `mask-position` or `mask-size` on a gradient mask instead of moving/clipping DOM elements. Avoids layout reflow — just changes visibility via the compositing step.

```css
.wipe img {
  display: block;
  width: 100%;
  mask-image: linear-gradient(90deg, transparent 0%, #000 20%, #000 80%, transparent 100%);
  mask-size: 200% 100%;
  mask-position: 100% 0%;
  animation: wipe 1.1s cubic-bezier(.2,.8,.2,1) forwards;
}

@keyframes wipe {
  to { mask-position: 0% 0%; }
}

@media (prefers-reduced-motion: reduce) {
  .wipe img { animation: none; mask-position: 0 0; }
}
```

Combinable with scroll-driven timelines where supported.

---

## Spotlight Border Card (Cursor-Following Glow)

### Mechanism
JS sets CSS custom variables (`--mx`, `--my`) from pointer position. CSS paints a radial gradient at those coordinates on a pseudo-element.

```css
.card {
  position: relative;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.1);
  overflow: hidden;
}

.card::before {
  content: "";
  position: absolute;
  inset: -1px;
  background: radial-gradient(
    220px circle at var(--mx, 50%) var(--my, 50%),
    rgba(255,255,255,0.22),
    transparent 60%
  );
  opacity: 0;
  transition: opacity 140ms ease;
  pointer-events: none;
}

.card:hover::before { opacity: 1; }

@media (prefers-reduced-motion: reduce) {
  .card::before { transition: opacity 100ms linear; }
  /* Skip pointer tracking — keep hover-only glow */
}
```

```js
document.querySelectorAll(".card").forEach(card => {
  card.addEventListener("pointermove", e => {
    if (prefersReducedMotion()) return;
    const r = card.getBoundingClientRect();
    card.style.setProperty("--mx", `${((e.clientX - r.left) / r.width) * 100}%`);
    card.style.setProperty("--my", `${((e.clientY - r.top) / r.height) * 100}%`);
  });
});
```

---

## Dock Magnification (Proximity Hover Scale)

### Mechanism
`pointermove` + distance-based scale mapping. Each item scales based on cursor proximity, with a falloff radius.

```js
const MAX_SCALE = 1.9, MIN_SCALE = 1.0, RADIUS = 140;

dock.addEventListener("pointermove", (e) => {
  if (prefersReducedMotion()) return;
  const rect = dock.getBoundingClientRect();
  const px = e.clientX - rect.left;

  for (const el of items) {
    const r = el.getBoundingClientRect();
    const cx = (r.left + r.right) / 2 - rect.left;
    const d = Math.abs(px - cx);
    const t = 1 - Math.min(1, d / RADIUS);
    el.style.transform = `scale(${MIN_SCALE + (MAX_SCALE - MIN_SCALE) * t * t})`;
  }
});

dock.addEventListener("pointerleave", () => {
  items.forEach(el => el.style.transform = "scale(1)");
});
```

Reduced motion: hover-only scale (no proximity tracking).

---

## Typography: Text Scramble

```js
function scramble(el, finalText, duration = 600) {
  if (prefersReducedMotion()) { el.textContent = finalText; return; }

  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const start = performance.now();

  function tick(now) {
    const t = Math.min(1, (now - start) / duration);
    const revealed = Math.floor(t * finalText.length);
    let out = "";
    for (let i = 0; i < finalText.length; i++) {
      out += i < revealed ? finalText[i] : chars[Math.floor(Math.random() * chars.length)];
    }
    el.textContent = out;
    if (t < 1) requestAnimationFrame(tick);
    else el.textContent = finalText;
  }
  requestAnimationFrame(tick);
}
```

---

## Typography: Char-by-Char Reveal Without DOM Splitting

### Mechanism (from Ana Tudor)
Use `steps(var(--n))` easing with a gradient background clipped to text. The stepped easing creates per-character progression without wrapping each character in a span. Combine with `@supports (animation-timeline: scroll())` for scroll-linked reveal.

```css
.char-reveal {
  --n: 24; /* character count — set via preprocessor or data attribute */
  background: linear-gradient(90deg, currentColor 50%, transparent 50%);
  background-size: 200% 100%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: reveal 2s steps(var(--n)) forwards;
}

@keyframes reveal {
  from { background-position: 100% 0; }
  to   { background-position: 0 0; }
}
```

This avoids the default AI-agent move of creating character-soup spans.

---

## Micro-Interaction: Particle Explosion Button

```js
function burst(button) {
  if (prefersReducedMotion()) {
    button.animate(
      [{ transform: "scale(1)" }, { transform: "scale(1.06)" }, { transform: "scale(1)" }],
      { duration: 180, easing: "ease-out" }
    );
    return;
  }

  const rect = button.getBoundingClientRect();
  const cx = rect.left + rect.width / 2;
  const cy = rect.top + rect.height / 2;

  for (let i = 0; i < 12; i++) {
    const p = document.createElement("span");
    p.className = "particle";
    p.style.cssText = `position:fixed;left:${cx}px;top:${cy}px;width:6px;height:6px;border-radius:50%;background:currentColor;pointer-events:none;`;
    document.body.appendChild(p);

    const angle = (i / 12) * Math.PI * 2;
    const dist = 50 + Math.random() * 30;
    const dx = Math.cos(angle) * dist;
    const dy = Math.sin(angle) * dist;

    const anim = p.animate(
      [
        { transform: "translate(-50%,-50%) scale(1)", opacity: 1 },
        { transform: `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) scale(0.2)`, opacity: 0 }
      ],
      { duration: 500, easing: "cubic-bezier(0.2,0,0,1)", fill: "both" }
    );
    anim.finished.finally(() => p.remove());
  }
}
```

---

## Kinetic Marquee

```css
.marquee { overflow: hidden; white-space: nowrap; }
.marquee__track {
  display: inline-block;
  animation: marquee 14s linear infinite;
}

@keyframes marquee { to { transform: translateX(-50%); } }

@media (prefers-reduced-motion: reduce) {
  .marquee__track { animation: none; }
}
```

Duplicate content inside `.marquee__track` for seamless loop (two copies of the text, side by side).

---

## Dynamic Island Pill Morph

```css
.island {
  position: fixed;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  width: 160px;
  height: 40px;
  border-radius: 999px;
  background: #000;
  color: #fff;
  transition:
    width 520ms var(--spring-snappy),
    height 520ms var(--spring-snappy),
    border-radius 520ms var(--spring-snappy);
}

.island[data-expanded] {
  width: min(92vw, 420px);
  height: 220px;
  border-radius: 28px;
}

@media (prefers-reduced-motion: reduce) {
  .island { transition: opacity 120ms linear; }
}
```

Use `linear()` spring presets from `css-native.md` for the spring easing.
