import * as React from "react"
import { motion } from "motion/react"

const actions = ["Prompt", "Tools", "Files", "Inspect", "Run"]

export default function LiquidGlassDock() {
  return (
    <div className="fixed inset-x-0 bottom-6 z-50 flex justify-center px-4">
      <motion.nav
        initial={{ opacity: 0, y: 24, scale: 0.96 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ type: "spring", stiffness: 240, damping: 24 }}
        className="relative isolate flex items-center gap-2 overflow-hidden rounded-full border border-white/20 bg-white/10 px-3 py-3 text-white shadow-[0_16px_48px_rgba(0,0,0,0.28)] backdrop-blur-2xl backdrop-saturate-150"
      >
        <span className="pointer-events-none absolute inset-0 [background:radial-gradient(circle_at_22%_8%,rgba(255,255,255,0.42),rgba(255,255,255,0.1)_20%,transparent_52%)]" />
        <span className="pointer-events-none absolute inset-px rounded-full border border-white/12" />
        <div className="relative z-10 flex items-center gap-2">
          {actions.map((action) => (
            <motion.button
              key={action}
              whileHover={{ y: -2, scale: 1.02 }}
              whileTap={{ y: 0, scale: 0.98 }}
              transition={{ type: "spring", stiffness: 320, damping: 22 }}
              className="rounded-full border border-white/10 bg-white/8 px-3.5 py-2 text-sm font-medium text-white/90 shadow-[inset_0_1px_0_rgba(255,255,255,0.12)]"
            >
              {action}
            </motion.button>
          ))}
        </div>
      </motion.nav>
    </div>
  )
}
