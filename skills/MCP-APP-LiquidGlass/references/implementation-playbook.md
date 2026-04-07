# Implementation playbook

## Decision matrix

### Use CSS + Motion only when:
- the request is for production app UI
- the user wants premium polish, not literal optical realism
- you need many components to share one system

Recipe:
- translucent background
- subtle border and inner shadow
- 1–2 highlight gradients
- backdrop blur/saturation
- Motion hover/press/entrance

### Use CSS + SVG filters when:
- the user explicitly wants liquid distortion
- only a few hero surfaces need the effect
- you can localize the filter region

Recipe:
- base shell
- absolute filter layer with `backdrop-filter`
- inline SVG filter using blur/color matrix/displacement
- content layer with slightly more stable contrast

### Use WebGL or dedicated libraries when:
- the user wants a hero lens, premium product showcase, or experimental interface
- realistic refraction is a core feature, not icing

Recipe:
- isolate the effect to one main surface
- keep surrounding UI quieter
- include fallback markup or a simplified blur shell

## Visual token starter

Use one token system and reuse it everywhere.

```css
:root {
  --lg-radius-xl: 28px;
  --lg-radius-2xl: 36px;
  --lg-border: rgba(255,255,255,0.22);
  --lg-fill: rgba(255,255,255,0.10);
  --lg-fill-strong: rgba(255,255,255,0.16);
  --lg-shadow: 0 10px 30px rgba(0,0,0,0.22);
  --lg-inner-highlight: inset 0 1px 0 rgba(255,255,255,0.34);
  --lg-blur: 18px;
  --lg-saturate: 1.35;
  --lg-sheen: radial-gradient(
    circle at 20% 10%,
    rgba(255,255,255,0.45),
    rgba(255,255,255,0.12) 24%,
    transparent 52%
  );
}
```

## Base surface recipe

```tsx
<div className="relative overflow-hidden rounded-[28px] border border-white/20 bg-white/10 shadow-2xl backdrop-blur-xl backdrop-saturate-150">
  <div className="pointer-events-none absolute inset-0 opacity-90 [background:radial-gradient(circle_at_20%_10%,rgba(255,255,255,0.38),rgba(255,255,255,0.1)_22%,transparent_48%)]" />
  <div className="pointer-events-none absolute inset-px rounded-[27px] border border-white/15" />
  <div className="relative z-10">...</div>
</div>
```

Use this when the user needs the feel of liquid glass but not full displacement.

## Motion starter patterns

### Hover / press button

```tsx
<motion.button
  whileHover={{ scale: 1.02, y: -1 }}
  whileTap={{ scale: 0.985, y: 0 }}
  transition={{ type: "spring", stiffness: 320, damping: 22 }}
/>
```

### Pointer-follow sheen

```tsx
const px = useMotionValue(50)
const py = useMotionValue(50)
const sx = useSpring(px, { stiffness: 220, damping: 24 })
const sy = useSpring(py, { stiffness: 220, damping: 24 })

const handleMove = (e: React.PointerEvent<HTMLDivElement>) => {
  const rect = e.currentTarget.getBoundingClientRect()
  px.set(((e.clientX - rect.left) / rect.width) * 100)
  py.set(((e.clientY - rect.top) / rect.height) * 100)
}
```

Then feed those values into a radial-gradient highlight or small rotateX/rotateY tilt.

### Tilt without gimmicks

Keep tilt tiny:
- rotateX: -5 to 5
- rotateY: -7 to 7
- scale: 1.01 to 1.03

Anything beyond that starts looking like a toy unless the user asked for playful motion.

## SVG filter starter

Use this for premium surfaces, not every component.

```html
<svg width="0" height="0" aria-hidden="true">
  <defs>
    <filter id="liquidGlass" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur" />
      <feColorMatrix in="blur" type="matrix"
        values="1 0 0 0 0
                0 1 0 0 0
                0 0 1 0 0
                0 0 0 18 -8" result="goo" />
      <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="2" seed="4" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="10" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
</svg>
```

Notes:
- Keep `scale` modest for app UI.
- Restrict filter area.
- Use stronger distortion only on selected states or hero panels.

## Typical components for MCP apps

### Command dock
- rounded pill or capsule shell
- spring hover on buttons
- subtle glow around active connection state
- composer field on a steadier inner panel

### Tool result card
- outer glass shell
- inner matte content plate
- optional highlight only on hover/focus

### Inspector drawer
- stronger blur on the drawer shell
- readable monospace/data content inside a flatter inner layer

### Floating action cluster
- dock layout
- one primary liquid-glass button
- secondary actions quieter

## What to say when the user wants “Apple liquid glass”

Do not promise literal parity with native Apple rendering.
Say you can recreate the feel using layered blur, SVG displacement/reflection,
and spring-driven interaction, with browser fallbacks where needed.

## Fallback guidance

If SVG displacement is unsupported or too expensive:
- keep blur
- keep border/highlight system
- remove distortion
- preserve motion polish

That usually retains 70–80% of the desired aesthetic at a fraction of the risk.
