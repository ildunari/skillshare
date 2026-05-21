/**
 * LiquidGlassFilter.tsx
 * Pure CSS + SVG React component — ZERO external dependencies.
 * Works in Next.js App Router (add "use client" only for interactive variants).
 *
 * Sources:
 *   https://dev.to/fabiosleal/how-to-create-the-apple-liquid-glass-effect-with-css-and-svg-2o06
 *   https://blog.logrocket.com/how-create-liquid-glass-effects-css-and-svg/
 *   https://codepen.io/wprod/pen/raVpwJL
 */

import React, { useId } from 'react'

// ─── Filter presets ───────────────────────────────────────────────────────────

export type FilterType = 'fractal' | 'lens' | 'animated' | 'specular'

function FilterDef({
  id,
  type = 'fractal',
}: {
  id: string
  type?: FilterType
}) {
  if (type === 'lens') {
    return (
      <filter id={id} x="0%" y="0%" width="100%" height="100%"
              filterUnits="objectBoundingBox">
        <feComponentTransfer in="SourceAlpha" result="alpha">
          <feFuncA type="identity" />
        </feComponentTransfer>
        <feGaussianBlur in="alpha" stdDeviation="50" result="blur" />
        <feDisplacementMap in="SourceGraphic" in2="blur"
          scale="50" xChannelSelector="A" yChannelSelector="A" />
      </filter>
    )
  }

  if (type === 'animated') {
    return (
      <filter id={id} x="0%" y="0%" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.01 0.01"
          numOctaves={1} seed={5} result="turbulence">
          <animate attributeName="seed" from="1" to="200"
                   dur="8s" repeatCount="indefinite" />
        </feTurbulence>
        <feGaussianBlur in="turbulence" stdDeviation="3" result="softMap" />
        <feDisplacementMap in="SourceGraphic" in2="softMap"
          scale="120" xChannelSelector="R" yChannelSelector="G" />
      </filter>
    )
  }

  if (type === 'specular') {
    return (
      <filter id={id} x="0%" y="0%" width="100%" height="100%"
              filterUnits="objectBoundingBox">
        <feTurbulence type="fractalNoise" baseFrequency="0.01 0.01"
          numOctaves={1} seed={5} result="turbulence">
          <animate attributeName="seed" from="1" to="200"
                   dur="8s" repeatCount="indefinite" />
        </feTurbulence>
        <feComponentTransfer in="turbulence" result="mapped">
          <feFuncR type="gamma" amplitude={1} exponent={10} offset={0.5} />
          <feFuncG type="gamma" amplitude={0} exponent={1}  offset={0} />
          <feFuncB type="gamma" amplitude={0} exponent={1}  offset={0.5} />
        </feComponentTransfer>
        <feGaussianBlur in="turbulence" stdDeviation="3" result="softMap" />
        <feSpecularLighting in="softMap" surfaceScale={5}
          specularConstant={1} specularExponent={100}
          lightingColor="white" result="specLight">
          <fePointLight x={-200} y={-200} z={300} />
        </feSpecularLighting>
        <feComposite in="specLight" operator="arithmetic"
          k1={0} k2={1} k3={1} k4={0} result="litImage" />
        <feDisplacementMap in="SourceGraphic" in2="softMap"
          scale="150" xChannelSelector="R" yChannelSelector="G" />
      </filter>
    )
  }

  // Default: fractal noise
  return (
    <filter id={id} x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.008 0.008"
        numOctaves={2} seed={92} result="noise" />
      <feGaussianBlur in="noise" stdDeviation="2" result="blurred" />
      <feDisplacementMap in="SourceGraphic" in2="blurred"
        scale="70" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  )
}

// ─── Theme tokens ─────────────────────────────────────────────────────────────

interface GlassTheme {
  bg: string
  highlight: string
  blur: string
  saturate: string
  brightness: string
  radius: string
  shadow: string
}

const THEMES: Record<string, GlassTheme> = {
  dark: {
    bg: 'rgba(255,255,255,0.22)',
    highlight: 'rgba(255,255,255,0.72)',
    blur: '4px',
    saturate: '120%',
    brightness: '1.15',
    radius: '1.5rem',
    shadow: '0 6px 6px rgba(0,0,0,0.22), 0 0 22px rgba(0,0,0,0.12)',
  },
  light: {
    bg: 'rgba(255,255,255,0.5)',
    highlight: 'rgba(255,255,255,0.9)',
    blur: '8px',
    saturate: '130%',
    brightness: '1.05',
    radius: '1.5rem',
    shadow: '0 4px 16px rgba(0,0,0,0.1)',
  },
  subtle: {
    bg: 'rgba(255,255,255,0.12)',
    highlight: 'rgba(255,255,255,0.45)',
    blur: '2px',
    saturate: '110%',
    brightness: '1.08',
    radius: '1rem',
    shadow: '0 2px 8px rgba(0,0,0,0.15)',
  },
}

// ─── Main Component ───────────────────────────────────────────────────────────

interface LiquidGlassFilterProps {
  children: React.ReactNode
  /** Visual theme preset */
  theme?: keyof typeof THEMES
  /** Override individual theme tokens */
  themeOverrides?: Partial<GlassTheme>
  /** SVG filter type */
  filterType?: FilterType
  /** Corner radius override */
  radius?: string
  className?: string
  style?: React.CSSProperties
  /** Render as a different element */
  as?: keyof JSX.IntrinsicElements
}

export function LiquidGlassFilter({
  children,
  theme = 'dark',
  themeOverrides,
  filterType = 'fractal',
  radius,
  className,
  style,
  as: Tag = 'div',
}: LiquidGlassFilterProps) {
  const uid = useId().replace(/:/g, '')
  const filterId = `lg-${uid}`
  const t = { ...THEMES[theme], ...themeOverrides }
  const r = radius ?? t.radius

  const containerStyle: React.CSSProperties = {
    position: 'relative',
    borderRadius: r,
    overflow: 'hidden',
    boxShadow: t.shadow,
    ...style,
  }

  const filterLayerStyle: React.CSSProperties = {
    position: 'absolute', inset: 0,
    zIndex: 0,
    borderRadius: r,
    pointerEvents: 'none',
    backdropFilter: `blur(${t.blur})`,
    filter: `url(#${filterId}) saturate(${t.saturate}) brightness(${t.brightness})`,
    isolation: 'isolate',
  }

  const tintStyle: React.CSSProperties = {
    position: 'absolute', inset: 0,
    zIndex: 1, borderRadius: r,
    pointerEvents: 'none',
    background: t.bg,
  }

  const specularStyle: React.CSSProperties = {
    position: 'absolute', inset: 0,
    zIndex: 2, borderRadius: r,
    pointerEvents: 'none', overflow: 'hidden',
    boxShadow: `inset 1px 1px 0 ${t.highlight}, inset 0 0 6px ${t.highlight}`,
  }

  const contentStyle: React.CSSProperties = {
    position: 'relative',
    zIndex: 3,
  }

  return (
    <>
      <svg style={{ display: 'none' }}>
        <defs>
          <FilterDef id={filterId} type={filterType} />
        </defs>
      </svg>
      {/* @ts-ignore — dynamic tag */}
      <Tag className={className} style={containerStyle}>
        <div style={filterLayerStyle} />
        <div style={tintStyle} />
        <div style={specularStyle} />
        <div style={contentStyle}>{children}</div>
      </Tag>
    </>
  )
}

// ─── Convenience exports ──────────────────────────────────────────────────────

export function GlassCard({
  children,
  style,
}: {
  children: React.ReactNode
  style?: React.CSSProperties
}) {
  return (
    <LiquidGlassFilter theme="dark" style={{ padding: '1.5rem', ...style }}>
      {children}
    </LiquidGlassFilter>
  )
}

export function GlassPill({
  children,
  style,
}: {
  children: React.ReactNode
  style?: React.CSSProperties
}) {
  return (
    <LiquidGlassFilter
      theme="dark"
      radius="9999px"
      style={{ display: 'inline-flex', alignItems: 'center', cursor: 'pointer', ...style }}
    >
      <div style={{ padding: '0.55rem 1.5rem', fontWeight: 600, color: 'white', fontSize: '0.9rem' }}>
        {children}
      </div>
    </LiquidGlassFilter>
  )
}

export function GlassAnimatedPanel({
  children,
  style,
}: {
  children: React.ReactNode
  style?: React.CSSProperties
}) {
  return (
    <LiquidGlassFilter
      theme="dark"
      filterType="animated"
      radius="1.5rem"
      style={{ padding: '2rem', ...style }}
    >
      {children}
    </LiquidGlassFilter>
  )
}

// ─── Usage Example ────────────────────────────────────────────────────────────
/*
import {
  LiquidGlassFilter,
  GlassCard,
  GlassPill,
  GlassAnimatedPanel,
} from './LiquidGlassFilter'

function App() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'url(/bg.jpg) center/cover',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center', gap: '1.5rem'
    }}>

      <GlassCard style={{ maxWidth: '24rem' }}>
        <h2 style={{ color: 'white', fontWeight: 700 }}>Glass Card</h2>
        <p style={{ color: 'rgba(255,255,255,0.7)', marginTop: '0.5rem' }}>No external deps required.</p>
      </GlassCard>

      <GlassPill>Get Started</GlassPill>

      <GlassAnimatedPanel style={{ maxWidth: '30rem' }}>
        <p style={{ color: 'white' }}>Animated fluid glass panel</p>
      </GlassAnimatedPanel>

      <LiquidGlassFilter theme="light" filterType="specular" style={{ padding: '1.5rem', maxWidth: '24rem' }}>
        <p style={{ color: '#1a1a1a' }}>Light theme with specular lighting filter</p>
      </LiquidGlassFilter>

    </div>
  )
}
*/
