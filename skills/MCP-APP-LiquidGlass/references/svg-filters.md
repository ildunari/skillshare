# SVG Filter Pipelines for Liquid Glass

Reference: https://blog.logrocket.com/how-create-liquid-glass-effects-css-and-svg/
Reference: https://dev.to/fabiosleal/how-to-create-the-apple-liquid-glass-effect-with-css-and-svg-2o06
Reference: https://diviengine.com/snippets/divi/liquid-glass-with-css-and-svg/

---

## SVG Filter Primitive Quick Reference

| Primitive | Purpose | Key Attributes |
|---|---|---|
| `feTurbulence` | Generate noise/texture map | `type`, `baseFrequency`, `numOctaves`, `seed` |
| `feGaussianBlur` | Blur a layer | `stdDeviation` |
| `feDisplacementMap` | Warp pixels using a map | `scale`, `xChannelSelector`, `yChannelSelector` |
| `feColorMatrix` | Adjust color/saturation/brightness | `type="saturate"`, `values` |
| `feSpecularLighting` | Simulate specular light reflection | `surfaceScale`, `specularConstant`, `specularExponent` |
| `fePointLight` | Light source for specular | `x`, `y`, `z` |
| `feImage` | Load external PNG as filter input | `href` |
| `feComposite` | Combine two layers with operator | `operator`, `k1-k4` |
| `feBlend` | Blend two layers | `mode` |
| `feComponentTransfer` | Per-channel gamma/linear transform | `feFuncR`, `feFuncG`, `feFuncB`, `feFuncA` |

### `feDisplacementMap` Channel Values
- `128` = neutral (no displacement)
- `> 128` = positive shift (right or down)
- `< 128` = negative shift (left or up)

---

## Filter 1: Organic Edge Distortion (fractal noise)
**Use case:** Standard liquid glass distortion on any component. No JS needed.

```html
<svg style="display:none">
  <filter id="lg-dist" x="0%" y="0%" width="100%" height="100%">
    <!-- 1. Generate fractal noise texture -->
    <feTurbulence
      type="fractalNoise"
      baseFrequency="0.008 0.008"
      numOctaves="2"
      seed="92"
      result="noise"
    />
    <!-- 2. Blur the noise for smoother, blob-like clumps -->
    <feGaussianBlur in="noise" stdDeviation="2" result="blurred"/>
    <!-- 3. Use blurred noise as displacement map on the source graphic -->
    <feDisplacementMap
      in="SourceGraphic"
      in2="blurred"
      scale="70"
      xChannelSelector="R"
      yChannelSelector="G"
    />
  </filter>
</svg>
```

**CSS usage:**
```css
.glass-filter {
  filter: url(#lg-dist) saturate(120%) brightness(1.15);
  backdrop-filter: blur(4px);
}
```

**Tuning:**
- Increase `baseFrequency` (e.g., `0.02`) → finer, more granular distortion
- Decrease `baseFrequency` (e.g., `0.003`) → larger, sweeping waves
- Increase `scale` → more intense warp
- Increase `numOctaves` → more complex noise (heavier perf)

---

## Filter 2: Alpha-Based Lens Warp (Dock/App Icon style)
**Use case:** macOS Dock-style glass container. Distortion driven by the alpha mask of the container shape itself.

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg">
  <filter id="lensFilter" x="0%" y="0%" width="100%" height="100%"
          filterUnits="objectBoundingBox">
    <!-- Extract alpha channel as mask -->
    <feComponentTransfer in="SourceAlpha" result="alpha">
      <feFuncA type="identity"/>
    </feComponentTransfer>
    <!-- Blur the alpha mask -->
    <feGaussianBlur in="alpha" stdDeviation="50" result="blur"/>
    <!-- Displace source graphic by the blurred alpha -->
    <feDisplacementMap
      in="SourceGraphic"
      in2="blur"
      scale="50"
      xChannelSelector="A"
      yChannelSelector="A"
    />
  </filter>
</svg>
```

**CSS usage:**
```css
.glass-filter {
  backdrop-filter: blur(4px);
  filter: url(#lensFilter) saturate(120%) brightness(1.15);
}
```

---

## Filter 3: Specular Lighting + Animated Distortion
**Use case:** Fully animated fluid glass. Simulates refraction AND a specular highlight from a point light.

```html
<svg style="display:none">
  <filter id="lg-specular" x="0%" y="0%" width="100%" height="100%"
          filterUnits="objectBoundingBox">
    <!-- 1. Animated turbulence — seed animates for fluid movement -->
    <feTurbulence
      type="fractalNoise"
      baseFrequency="0.01 0.01"
      numOctaves="1"
      seed="5"
      result="turbulence">
      <animate attributeName="seed" from="1" to="200"
               dur="8s" repeatCount="indefinite"/>
    </feTurbulence>

    <!-- 2. Gamma transform: push red channel, suppress green/blue -->
    <feComponentTransfer in="turbulence" result="mapped">
      <feFuncR type="gamma" amplitude="1" exponent="10" offset="0.5"/>
      <feFuncG type="gamma" amplitude="0" exponent="1"  offset="0"/>
      <feFuncB type="gamma" amplitude="0" exponent="1"  offset="0.5"/>
    </feComponentTransfer>

    <!-- 3. Blur the noise map for smooth distortion -->
    <feGaussianBlur in="turbulence" stdDeviation="3" result="softMap"/>

    <!-- 4. Specular lighting from a point above-left -->
    <feSpecularLighting
      in="softMap"
      surfaceScale="5"
      specularConstant="1"
      specularExponent="100"
      lighting-color="white"
      result="specLight">
      <fePointLight x="-200" y="-200" z="300"/>
    </feSpecularLighting>

    <!-- 5. Composite the light with noise -->
    <feComposite
      in="specLight"
      operator="arithmetic"
      k1="0" k2="1" k3="1" k4="0"
      result="litImage"/>

    <!-- 6. Final displacement using softMap -->
    <feDisplacementMap
      in="SourceGraphic"
      in2="softMap"
      scale="150"
      xChannelSelector="R"
      yChannelSelector="G"/>
  </filter>
</svg>
```

---

## Filter 4: Full Refraction + Reflection Pipeline (Figma displacement map)
**Use case:** Production-grade button with externally designed displacement map PNG and specular rim PNG.

```tsx
// React/TSX
<svg style={{ display: 'none' }}>
  <defs>
    <filter id="liquid-glass-button">
      {/* 1. Slight blur of source */}
      <feGaussianBlur in="SourceGraphic" stdDeviation="1" result="blurred_source"/>

      {/* 2. Load displacement map PNG (design in Figma — radial gradient with edge colors) */}
      <feImage href="/displacement-map.png"
        x="0" y="0" width={BTN_WIDTH} height={BTN_HEIGHT}
        result="displacement_map"/>

      {/* 3. Refraction: warp background through displacement map */}
      <feDisplacementMap
        in="blurred_source" in2="displacement_map"
        scale="55" xChannelSelector="R" yChannelSelector="G"
        result="displaced"/>

      {/* 4. Saturate the displaced layer for richer colors */}
      <feColorMatrix in="displaced" type="saturate" values="50"
        result="displaced_saturated"/>

      {/* 5. Load specular rim PNG (stroke gradient from Figma) */}
      <feImage href="/specular.png"
        x="0" y="0" width={BTN_WIDTH} height={BTN_HEIGHT}
        result="specular_layer"/>

      {/* 6. Soften the rim */}
      <feGaussianBlur in="specular_layer" stdDeviation="1"
        result="specular_layer_blurred"/>

      {/* 7. Mask saturated content by the blurred specular rim */}
      <feComposite
        in="displaced_saturated" in2="specular_layer_blurred"
        operator="in" result="specular_saturated"/>

      {/* 8. Final blend: specular + refracted base */}
      <feBlend in="specular_saturated" in2="displaced" mode="normal"/>
    </filter>
  </defs>
</svg>
```

**Figma workflow for displacement map PNG:**
1. Create rounded rectangle matching button dimensions
2. Apply radial gradient with red/green/yellow — neutral center, intense edges
3. Stack blurred rounded rects on top (blur 32px → inward)
4. Export group as PNG (`displacement-map.png`)

**Figma workflow for specular rim PNG:**
1. Same-size rounded rectangle, no fill, stroke only (1-2px)
2. Stroke gradient: bright top-left → dark bottom-right
3. Opacity ~50%
4. Export as PNG (`specular.png`)

---

## CSS Reference for Tailwind v4 + SVG Filter

```css
/* Tailwind @theme tokens */
@theme {
  --btn-radius:      60px;
  --btn-content-bg:  hsl(0 100% 100% / 15%);
  --liquid-glass-filters: url(#liquid-glass-button) brightness(150%);
}
```

```tsx
// Filter layer
<div className="absolute inset-0 backdrop-filter-[--liquid-glass-filters]" />
// Content layer
<div className="absolute inset-0 inline-flex items-center justify-center font-bold text-white bg-[--btn-content-bg]">
  {children}
</div>
```

---

## Animating Filter Properties with JavaScript

```js
// Animate displacement scale on hover
const filterEl = document.querySelector('feDisplacementMap')
element.addEventListener('mouseenter', () => {
  filterEl.setAttribute('scale', '120')
})
element.addEventListener('mouseleave', () => {
  filterEl.setAttribute('scale', '70')
})

// Animate with GSAP
gsap.to(filterEl, {
  attr: { scale: 120 },
  duration: 0.4,
  ease: 'power2.out'
})

// Animate turbulence baseFrequency
const turbEl = document.querySelector('feTurbulence')
gsap.to(turbEl, {
  attr: { baseFrequency: '0.02 0.02' },
  duration: 0.6,
  yoyo: true,
  repeat: -1
})
```
