/**
 * LiquidGlassCard.tsx
 * Drop-in React card component using liquid-glass-react.
 * Install: npm install liquid-glass-react
 *
 * Source: https://github.com/rdev/liquid-glass-react
 */
'use client'

import LiquidGlass from 'liquid-glass-react'
import { useRef } from 'react'

// ─── Preset configurations ───────────────────────────────────────────────────

export const GLASS_PRESETS = {
  /** Standard card — dark background */
  card: {
    displacementScale: 70,
    blurAmount: 0.0625,
    saturation: 140,
    aberrationIntensity: 2,
    elasticity: 0.15,
    cornerRadius: 24,
  },
  /** Pill button */
  pill: {
    displacementScale: 64,
    blurAmount: 0.1,
    saturation: 130,
    aberrationIntensity: 2,
    elasticity: 0.35,
    cornerRadius: 100,
  },
  /** Prominent / hero panel */
  prominent: {
    displacementScale: 90,
    blurAmount: 0.08,
    saturation: 160,
    aberrationIntensity: 3,
    elasticity: 0.2,
    cornerRadius: 32,
  },
  /** Subtle / secondary */
  subtle: {
    displacementScale: 40,
    blurAmount: 0.04,
    saturation: 120,
    aberrationIntensity: 1,
    elasticity: 0.1,
    cornerRadius: 16,
  },
  /** Light background mode */
  light: {
    displacementScale: 60,
    blurAmount: 0.06,
    saturation: 130,
    aberrationIntensity: 1.5,
    elasticity: 0.12,
    cornerRadius: 20,
    overLight: true,
  },
} as const

// ─── Types ────────────────────────────────────────────────────────────────────

type GlassPreset = keyof typeof GLASS_PRESETS

interface LiquidGlassCardProps {
  children: React.ReactNode
  preset?: GlassPreset
  className?: string
  style?: React.CSSProperties
  onClick?: () => void
  /** Use when glass is inside a larger container and should track mouse over it */
  trackMouseOnParent?: boolean
  /** Override any preset prop directly */
  overrides?: Partial<typeof GLASS_PRESETS['card']>
}

// ─── Component ────────────────────────────────────────────────────────────────

export function LiquidGlassCard({
  children,
  preset = 'card',
  className,
  style,
  onClick,
  trackMouseOnParent = false,
  overrides,
}: LiquidGlassCardProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const config = { ...GLASS_PRESETS[preset], ...overrides }

  if (trackMouseOnParent) {
    // Wrap in a container that the glass tracks mouse over
    return (
      <div ref={containerRef} style={{ position: 'relative', ...style }}>
        <LiquidGlass
          {...config}
          mouseContainer={containerRef}
          className={className}
          onClick={onClick}
          style={{ width: '100%', height: '100%' }}
        >
          {children}
        </LiquidGlass>
      </div>
    )
  }

  return (
    <LiquidGlass
      {...config}
      className={className}
      style={style}
      onClick={onClick}
    >
      {children}
    </LiquidGlass>
  )
}

// ─── Convenience variants ─────────────────────────────────────────────────────

export function GlassButton({
  children,
  onClick,
  label,
}: {
  children?: React.ReactNode
  onClick?: () => void
  label?: string
}) {
  return (
    <LiquidGlassCard preset="pill" onClick={onClick}>
      <div style={{ padding: '8px 24px', fontWeight: 600, fontSize: '0.9rem' }}>
        {children ?? label}
      </div>
    </LiquidGlassCard>
  )
}

export function GlassPanel({
  children,
  style,
}: {
  children: React.ReactNode
  style?: React.CSSProperties
}) {
  return (
    <LiquidGlassCard preset="prominent" trackMouseOnParent style={style}>
      <div style={{ padding: '2rem' }}>{children}</div>
    </LiquidGlassCard>
  )
}

// ─── MCP Tool Output Panel ────────────────────────────────────────────────────

/**
 * Wraps an MCP tool's output in a Liquid Glass panel.
 * Usage:
 *   <MCPGlassPanel tool="search" result={toolOutput} />
 */
export function MCPGlassPanel({
  tool,
  result,
  children,
}: {
  tool?: string
  result?: unknown
  children?: React.ReactNode
}) {
  return (
    <LiquidGlassCard preset="card" style={{ width: '100%', maxWidth: '720px' }}>
      <div style={{ padding: '1.5rem' }}>
        {tool && (
          <div style={{
            fontSize: '0.75rem',
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            opacity: 0.5,
            marginBottom: '0.75rem',
          }}>
            {tool}
          </div>
        )}
        {children ?? (
          <pre style={{ fontSize: '0.85rem', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
            {typeof result === 'string' ? result : JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </LiquidGlassCard>
  )
}

// ─── Usage example ────────────────────────────────────────────────────────────
/*
import { LiquidGlassCard, GlassButton, GlassPanel, MCPGlassPanel, GLASS_PRESETS } from './LiquidGlassCard'

function App() {
  return (
    <div style={{ minHeight: '100vh', background: 'url(/bg.jpg) center/cover', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '1.5rem', padding: '2rem' }}>

      <LiquidGlassCard preset="card">
        <div className="p-6">
          <h2 className="text-white font-bold text-xl">Glass Card</h2>
          <p className="text-white/70 mt-2">Content inside liquid glass</p>
        </div>
      </LiquidGlassCard>

      <GlassButton onClick={() => alert('clicked!')}>
        Get Started
      </GlassButton>

      <GlassPanel>
        <h1 className="text-white font-bold text-2xl">Hero Panel</h1>
        <p className="text-white/70 mt-2">Full-width glass with mouse tracking</p>
      </GlassPanel>

      <MCPGlassPanel tool="search" result={{ query: 'liquid glass', results: 12 }} />

    </div>
  )
}
*/
