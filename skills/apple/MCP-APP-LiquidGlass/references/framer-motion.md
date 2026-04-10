# Framer Motion Recipes for Liquid Glass

## Table of contents

- [Core hooks](#core-hooks-used-with-liquid-glass)
- [Pattern 1: Mouse-tracking panel](#pattern-1-spring-elastic-mouse-tracking-glass-panel)
- [Pattern 2: Hover morph variants](#pattern-2-glass-element-with-hover-morph-variants)
- [Pattern 3: Animate SVG filter scale](#pattern-3-animate-svg-filter-scale-via-motionvalue)
- [Pattern 4: AnimatePresence mount/unmount](#pattern-4-animatepresence--glass-panel-mountunmount)
- [Pattern 5: Toggle switch](#pattern-5-toggle-switch-ios-26-style-3d-rotation)
- [Pattern 6: Direct value control](#pattern-6-usespring-for-direct-value-control)
- [Framer resources](#framer-design-tool-liquid-glass-resources)

Sources:
- https://motion.dev/docs/vue-use-spring
- https://blog.maximeheckel.com/posts/guide-animations-spark-joy-framer-motion/
- https://framer.university/resources/liquid-glass-element-in-framer
- https://www.framer.com/marketplace/components/liquid-glass-switch/
- https://www.framer.com/marketplace/components/chromaticlenseffect/

---

## Core Hooks Used with Liquid Glass

| Hook | Purpose |
|---|---|
| `useMotionValue` | Track mouse x/y position for glass element tracking |
| `useSpring` | Elastic "liquid" spring follow — mimics Apple's gel physics |
| `useTransform` | Map mouse pos → CSS transform or filter scale |
| `motion.div` | Animatable wrapper for glass containers |
| `AnimatePresence` | Mount/unmount glass panels with fluid transitions |

---

## Pattern 1: Spring-Elastic Mouse-Tracking Glass Panel

```tsx
'use client'
import { motion, useMotionValue, useSpring } from 'framer-motion'
import { useEffect } from 'react'

export function TrackingGlass({ children }) {
  const rawX = useMotionValue(0)
  const rawY = useMotionValue(0)

  // Spring config mimics Apple's "liquid" elastic feel
  const springConfig = { stiffness: 250, damping: 28, mass: 0.5 }
  const x = useSpring(rawX, springConfig)
  const y = useSpring(rawY, springConfig)

  useEffect(() => {
    const handleMouse = (e: MouseEvent) => {
      rawX.set(e.clientX - window.innerWidth / 2)
      rawY.set(e.clientY - window.innerHeight / 2)
    }
    window.addEventListener('mousemove', handleMouse)
    return () => window.removeEventListener('mousemove', handleMouse)
  }, [rawX, rawY])

  return (
    <motion.div
      style={{
        x,
        y,
        position: 'fixed',
        top: '50%',
        left: '50%',
        translateX: '-50%',
        translateY: '-50%',
      }}
      className="glass-container"
    >
      <div className="glass-filter" />
      <div className="glass-overlay" />
      <div className="glass-specular" />
      <div className="glass-content">{children}</div>
    </motion.div>
  )
}
```

---

## Pattern 2: Glass Element with Hover Morph Variants

```tsx
'use client'
import { motion } from 'framer-motion'

const glassVariants = {
  rest: {
    scale: 1,
    boxShadow: '0 6px 6px rgba(0,0,0,0.2), 0 0 20px rgba(0,0,0,0.1)',
  },
  hover: {
    scale: 1.03,
    boxShadow: '0 12px 24px rgba(0,0,0,0.3), 0 0 40px rgba(0,0,0,0.15)',
    transition: { type: 'spring', stiffness: 400, damping: 25 },
  },
  tap: {
    scale: 0.97,
    boxShadow: '0 2px 4px rgba(0,0,0,0.15)',
    transition: { type: 'spring', stiffness: 600, damping: 30 },
  },
}

export function GlassButton({ children, onClick }) {
  return (
    <motion.div
      className="glass-container"
      variants={glassVariants}
      initial="rest"
      whileHover="hover"
      whileTap="tap"
      onClick={onClick}
      style={{ cursor: 'pointer' }}
    >
      <div className="glass-filter" />
      <div className="glass-overlay" />
      <div className="glass-specular" />
      <div className="glass-content">{children}</div>
    </motion.div>
  )
}
```

---

## Pattern 3: Animate SVG Filter Scale via MotionValue

Bridges Framer Motion's MotionValue to SVG filter attributes for "live" refraction intensity.

```tsx
'use client'
import { motion, useMotionValue, useSpring, useMotionValueEvent } from 'framer-motion'
import { useRef } from 'react'

export function AnimatedFilterGlass({ children }) {
  const filterRef = useRef<SVGFEDisplacementMapElement>(null)
  const rawScale = useMotionValue(70)
  const springScale = useSpring(rawScale, { stiffness: 300, damping: 25 })

  // Pipe spring value into SVG filter attribute
  useMotionValueEvent(springScale, 'change', (v) => {
    filterRef.current?.setAttribute('scale', String(Math.round(v)))
  })

  return (
    <>
      <svg style={{ display: 'none' }}>
        <filter id="lg-animated" x="0%" y="0%" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.008 0.008"
            numOctaves={2} seed={92} result="noise"/>
          <feGaussianBlur in="noise" stdDeviation="2" result="blurred"/>
          <feDisplacementMap
            ref={filterRef}
            in="SourceGraphic"
            in2="blurred"
            scale="70"
            xChannelSelector="R"
            yChannelSelector="G"
          />
        </filter>
      </svg>

      <motion.div
        className="glass-container"
        onHoverStart={() => rawScale.set(120)}
        onHoverEnd={() => rawScale.set(70)}
        onTapStart={() => rawScale.set(40)}
        onTap={() => rawScale.set(70)}
      >
        <div className="glass-filter" style={{ filter: 'url(#lg-animated)' }}/>
        <div className="glass-overlay" />
        <div className="glass-specular" />
        <div className="glass-content">{children}</div>
      </motion.div>
    </>
  )
}
```

---

## Pattern 4: AnimatePresence — Glass Panel Mount/Unmount

```tsx
'use client'
import { motion, AnimatePresence } from 'framer-motion'

const panelVariants = {
  hidden: {
    opacity: 0,
    scale: 0.92,
    filter: 'blur(12px)',
    y: 20,
  },
  visible: {
    opacity: 1,
    scale: 1,
    filter: 'blur(0px)',
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 300,
      damping: 28,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.9,
    filter: 'blur(8px)',
    y: -10,
    transition: { duration: 0.2 },
  },
}

export function GlassModal({ isOpen, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="glass-container"
          variants={panelVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
        >
          <div className="glass-filter" />
          <div className="glass-overlay" />
          <div className="glass-specular" />
          <div className="glass-content">{children}</div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

---

## Pattern 5: Toggle Switch (iOS 26 style, 3D rotation)

Mimics the Framer marketplace Liquid Glass Switch component.

```tsx
'use client'
import { motion } from 'framer-motion'
import { useState } from 'react'

const SPRING = { type: 'spring', stiffness: 400, damping: 30 }

export function LiquidGlassToggle({ onChange }) {
  const [on, setOn] = useState(false)

  const toggle = () => {
    setOn(v => !v)
    onChange?.(!on)
  }

  return (
    <motion.div
      onClick={toggle}
      style={{
        width: 52,
        height: 32,
        borderRadius: 999,
        position: 'relative',
        cursor: 'pointer',
        backdropFilter: 'blur(10px)',
        background: on
          ? 'linear-gradient(135deg, rgba(0,180,120,0.7), rgba(0,130,90,0.5))'
          : 'linear-gradient(135deg, rgba(180,180,200,0.4), rgba(120,120,140,0.3))',
        boxShadow: 'inset 1px 1px 0 rgba(255,255,255,0.6), inset 0 0 4px rgba(255,255,255,0.4)',
        filter: 'url(#lg-dist)',
      }}
      animate={{ rotateY: on ? 8 : -8 }}
      transition={{ type: 'spring', stiffness: 300, damping: 25, duration: 0.7 }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      <motion.div
        layout
        style={{
          width: 26, height: 26,
          borderRadius: '50%',
          position: 'absolute',
          top: 3,
          background: 'rgba(255,255,255,0.9)',
          boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
        }}
        animate={{ x: on ? 22 : 2 }}
        transition={SPRING}
      />
    </motion.div>
  )
}
```

---

## Pattern 6: useSpring for Direct Value Control

```tsx
import { useSpring } from 'framer-motion'

// Track another motion value (canonical spring follow)
const mouseX = useMotionValue(0)
const springX = useSpring(mouseX, { stiffness: 300, damping: 30 })

// Jump immediately without spring
springX.jump(100)

// Update with spring
springX.set(200)

// Custom spring stiffness
const elasticSpring = useSpring(0, { stiffness: 150, damping: 20, mass: 0.8 })
```

---

## Framer (Design Tool) Liquid Glass Resources

These are no-code Framer design tool components, not the `framer-motion` library:

| Resource | URL | Type |
|---|---|---|
| Liquid Glass Switch | https://www.framer.com/marketplace/components/liquid-glass-switch/ | Premium toggle (iOS 26 style) |
| Chromatic Lens Effect | https://www.framer.com/marketplace/components/chromaticlenseffect/ | WebGL glass lens, physics merge |
| Framer University — Liquid Glass Element | https://framer.university/resources/liquid-glass-element-in-framer | Drag-reactive glass component |

**Framer (design tool) controls:**
- `Mode` — preset style (standard, custom)
- `Scale` — fluid distortion warping intensity
- `Blur` — backdrop blur level
- `Frost` — opacity/transparency depth
- `Alpha` — overall element opacity
- `Radius` — corner radius
- `Border` — edge thickness
- `Lightness` — brightness of glass
- `Dispersion` — chromatic color separation
