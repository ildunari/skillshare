# React Components & npm Packages for Liquid Glass

---

## Package: `liquid-glass-react`
- GitHub: https://github.com/rdev/liquid-glass-react
- Install: `npm install liquid-glass-react`
- Browser support: Full in Chrome/Edge; partial displacement in Safari/Firefox

### Full Props Reference

| Prop | Type | Default | Description |
|---|---|---|---|
| `children` | `React.ReactNode` | — | Content inside the glass container |
| `displacementScale` | `number` | `70` | Intensity of displacement warp |
| `blurAmount` | `number` | `0.0625` | Frosting level (0 = clear, 1 = opaque) |
| `saturation` | `number` | `140` | Color saturation of the glass |
| `aberrationIntensity` | `number` | `2` | Chromatic aberration intensity |
| `elasticity` | `number` | `0.15` | Liquid elastic feel (0 = rigid) |
| `cornerRadius` | `number` | `999` | Border radius in pixels |
| `className` | `string` | `""` | Additional CSS classes |
| `padding` | `string` | — | CSS padding value |
| `style` | `React.CSSProperties` | — | Inline styles |
| `overLight` | `boolean` | `false` | Set true when glass is over light background |
| `onClick` | `() => void` | — | Click handler |
| `mouseContainer` | `React.RefObject<HTMLElement\|null>\|null` | `null` | Container to track mouse over |
| `mode` | `"standard"\|"polar"\|"prominent"\|"shader"` | `"standard"` | Refraction mode. `shader` is most accurate, least stable |
| `globalMousePos` | `{ x: number; y: number }` | — | Manual global mouse position |
| `mouseOffset` | `{ x: number; y: number }` | — | Fine-tune mouse position offset |

### Usage Examples

```tsx
import LiquidGlass from 'liquid-glass-react'
import { useRef } from 'react'

// — Card
export function GlassCard({ children }) {
  return (
    <LiquidGlass
      displacementScale={70}
      blurAmount={0.0625}
      saturation={140}
      aberrationIntensity={2}
      elasticity={0.15}
      cornerRadius={24}
    >
      <div className="p-6">{children}</div>
    </LiquidGlass>
  )
}

// — Pill button
export function GlassButton({ label, onClick }) {
  return (
    <LiquidGlass
      displacementScale={64}
      blurAmount={0.1}
      saturation={130}
      aberrationIntensity={2}
      elasticity={0.35}
      cornerRadius={100}
      padding="8px 24px"
      onClick={onClick}
    >
      <span className="text-white font-semibold">{label}</span>
    </LiquidGlass>
  )
}

// — Full-container mouse tracking (MCP panel)
export function GlassPanel({ children }) {
  const containerRef = useRef<HTMLDivElement>(null)
  return (
    <div ref={containerRef} className="w-full min-h-screen relative">
      <LiquidGlass
        mouseContainer={containerRef}
        elasticity={0.25}
        cornerRadius={20}
        displacementScale={60}
        style={{ position: 'absolute', inset: 0 }}
      >
        <div className="p-8">{children}</div>
      </LiquidGlass>
    </div>
  )
}

// — Prominent mode (more pronounced glass)
export function GlassHero({ children }) {
  return (
    <LiquidGlass
      mode="prominent"
      displacementScale={90}
      blurAmount={0.08}
      saturation={160}
      aberrationIntensity={3}
      elasticity={0.2}
      cornerRadius={32}
    >
      <div className="p-10">{children}</div>
    </LiquidGlass>
  )
}
```

---

## Package: `@developer-hub/liquid-glass`
- Docs: https://liquid-glass-js.com
- Install: `npm install @developer-hub/liquid-glass`

### Props

| Property | Type | Default | Description |
|---|---|---|---|
| `children` | `React.ReactNode` | — | Content inside glass |
| `displacementScale` | `number` | `100` | Displacement intensity (0–200) |
| `blurAmount` | `number` | `0.01` | Blur intensity (0–1) |
| `cornerRadius` | `number` | `999` | Border radius px |
| `className` | `string` | `""` | Extra CSS classes |
| `padding` | `string` | — | CSS padding |
| `style` | `React.CSSProperties` | — | Inline styles |
| `shadowMode` | `boolean` | `false` | Optimized for light backgrounds |
| `onClick` | `() => void` | — | Click handler |

```tsx
import { GlassCard } from '@developer-hub/liquid-glass'

// Default dark background
<GlassCard displacementScale={100} blurAmount={0.01} cornerRadius={999} padding="16px">
  <h2>Welcome to Liquid Glass</h2>
</GlassCard>

// Light background
<GlassCard shadowMode={true} cornerRadius={16} className="max-w-md mx-auto">
  <div className="p-8">
    <h3 className="text-xl font-bold mb-4">Premium Features</h3>
  </div>
</GlassCard>

// Interactive button
<GlassCard
  displacementScale={100} blurAmount={0.01}
  cornerRadius={10} padding="8px 16px"
  onClick={() => console.log('Glass button clicked!')}
>
  <span className="text-white font-medium">Get Started</span>
</GlassCard>
```

---

## Pure CSS+SVG React Component (no external deps)

```tsx
// LiquidGlassFilter.tsx — zero dependencies, works in RSC with "use client" for hover
import React from 'react'

interface LiquidGlassProps {
  children: React.ReactNode
  className?: string
  style?: React.CSSProperties
  filterId?: string
  bgColor?: string
  highlight?: string
  radius?: string
}

const FILTER_DEF = (id: string) => (
  <svg style={{ display: 'none' }}>
    <filter id={id} x="0%" y="0%" width="100%" height="100%">
      <feTurbulence
        type="fractalNoise"
        baseFrequency="0.008 0.008"
        numOctaves={2}
        seed={92}
        result="noise"
      />
      <feGaussianBlur in="noise" stdDeviation="2" result="blurred" />
      <feDisplacementMap
        in="SourceGraphic"
        in2="blurred"
        scale="70"
        xChannelSelector="R"
        yChannelSelector="G"
      />
    </filter>
  </svg>
)

export function LiquidGlassFilter({
  children,
  className = '',
  style,
  filterId = 'lg-dist',
  bgColor = 'rgba(255,255,255,0.25)',
  highlight = 'rgba(255,255,255,0.75)',
  radius = '2rem',
}: LiquidGlassProps) {
  return (
    <>
      {FILTER_DEF(filterId)}
      <div
        className={className}
        style={{
          position: 'relative',
          borderRadius: radius,
          overflow: 'hidden',
          boxShadow: '0 6px 6px rgba(0,0,0,0.2), 0 0 20px rgba(0,0,0,0.1)',
          ...style,
        }}
      >
        {/* Layer 0: distortion */}
        <div style={{
          position: 'absolute', inset: 0, zIndex: 0,
          backdropFilter: 'blur(4px)',
          filter: `url(#${filterId}) saturate(120%) brightness(1.15)`,
          isolation: 'isolate',
          borderRadius: 'inherit',
        }} />
        {/* Layer 1: tint */}
        <div style={{
          position: 'absolute', inset: 0, zIndex: 1,
          background: bgColor, borderRadius: 'inherit',
        }} />
        {/* Layer 2: specular */}
        <div style={{
          position: 'absolute', inset: 0, zIndex: 2,
          borderRadius: 'inherit', overflow: 'hidden',
          boxShadow: `inset 1px 1px 0 ${highlight}, inset 0 0 5px ${highlight}`,
        }} />
        {/* Layer 3: content */}
        <div style={{ position: 'relative', zIndex: 3 }}>
          {children}
        </div>
      </div>
    </>
  )
}
```

---

## MCP App Layout Pattern (Next.js App Router)

```tsx
// app/layout.tsx — wraps the MCP tool output area in a glass panel
import { LiquidGlassFilter } from '@/components/LiquidGlassFilter'

export default function MCPLayout({ children }) {
  return (
    <main className="min-h-screen bg-cover bg-center"
      style={{ backgroundImage: "url('/bg.jpg')" }}>
      <LiquidGlassFilter
        radius="1.5rem"
        className="max-w-3xl mx-auto mt-12 p-8"
      >
        {children}
      </LiquidGlassFilter>
    </main>
  )
}
```
