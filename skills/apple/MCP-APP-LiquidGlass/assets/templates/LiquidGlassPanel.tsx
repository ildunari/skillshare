import * as React from "react"
import { motion } from "motion/react"

type LiquidGlassPanelProps = React.HTMLAttributes<HTMLDivElement> & {
  title?: string
  subtitle?: string
}

export default function LiquidGlassPanel({
  title = "Inspector",
  subtitle = "Live MCP context",
  className = "",
  children,
  ...props
}: LiquidGlassPanelProps) {
  return (
    <motion.section
      {...props}
      initial={{ opacity: 0, y: 12, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ type: "spring", stiffness: 220, damping: 24 }}
      className={[
        "relative isolate overflow-hidden rounded-[28px] border border-white/20",
        "bg-white/10 p-4 text-white shadow-[0_18px_50px_rgba(0,0,0,0.28)]",
        "backdrop-blur-2xl backdrop-saturate-150",
        className,
      ].join(" ")}
    >
      <div className="pointer-events-none absolute inset-0 opacity-90 [background:radial-gradient(circle_at_18%_8%,rgba(255,255,255,0.42),rgba(255,255,255,0.14)_24%,transparent_52%)]" />
      <div className="pointer-events-none absolute inset-px rounded-[27px] border border-white/12" />
      <div className="relative z-10 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-sm font-semibold tracking-wide text-white/95">{title}</h2>
          <p className="mt-1 text-xs text-white/70">{subtitle}</p>
        </div>
        <div className="rounded-full border border-emerald-300/30 bg-emerald-200/10 px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.18em] text-emerald-100">
          Connected
        </div>
      </div>
      <div className="relative z-10 mt-4 rounded-[22px] border border-white/10 bg-black/20 p-4 text-sm text-white/88 shadow-[inset_0_1px_0_rgba(255,255,255,0.08)]">
        {children ?? (
          <div className="space-y-3">
            <div className="flex items-center justify-between rounded-2xl bg-white/6 px-3 py-2">
              <span>Last tool</span>
              <span className="text-white/65">search_docs</span>
            </div>
            <div className="flex items-center justify-between rounded-2xl bg-white/6 px-3 py-2">
              <span>Latency</span>
              <span className="text-white/65">420 ms</span>
            </div>
            <div className="rounded-2xl bg-white/6 p-3 text-white/70">
              Results and provenance sit on a calmer inner plate so the glass shell
              can stay flashy without making content unreadable.
            </div>
          </div>
        )}
      </div>
    </motion.section>
  )
}
