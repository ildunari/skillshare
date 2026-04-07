import * as React from "react"
import { motion, useMotionValue, useSpring, useTransform } from "motion/react"

type LiquidGlassButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  label?: string
}

export default function LiquidGlassButton({
  label,
  className = "",
  children,
  ...props
}: LiquidGlassButtonProps) {
  const mx = useMotionValue(50)
  const my = useMotionValue(50)

  const sx = useSpring(mx, { stiffness: 240, damping: 22 })
  const sy = useSpring(my, { stiffness: 240, damping: 22 })

  const rotateX = useTransform(sy, [0, 100], [4, -4])
  const rotateY = useTransform(sx, [0, 100], [-6, 6])
  const sheen = useTransform(
    [sx, sy],
    ([x, y]) => `radial-gradient(circle at ${x}% ${y}%, rgba(255,255,255,0.48), rgba(255,255,255,0.18) 20%, rgba(255,255,255,0.08) 34%, transparent 58%)`
  )

  const onPointerMove = (e: React.PointerEvent<HTMLButtonElement>) => {
    const rect = e.currentTarget.getBoundingClientRect()
    mx.set(((e.clientX - rect.left) / rect.width) * 100)
    my.set(((e.clientY - rect.top) / rect.height) * 100)
  }

  const onPointerLeave = () => {
    mx.set(50)
    my.set(50)
  }

  return (
    <motion.button
      {...props}
      onPointerMove={onPointerMove}
      onPointerLeave={onPointerLeave}
      whileHover={{ scale: 1.02, y: -1 }}
      whileTap={{ scale: 0.985, y: 0 }}
      transition={{ type: "spring", stiffness: 320, damping: 22 }}
      style={{ rotateX, rotateY, transformStyle: "preserve-3d" }}
      className={[
        "relative isolate overflow-hidden rounded-full border border-white/20",
        "bg-white/10 px-5 py-3 text-sm font-medium text-white shadow-[0_12px_40px_rgba(0,0,0,0.25)]",
        "backdrop-blur-xl backdrop-saturate-150",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/70",
        className,
      ].join(" ")}
    >
      <motion.span
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{ backgroundImage: sheen }}
      />
      <span className="pointer-events-none absolute inset-px rounded-full border border-white/15" />
      <span className="pointer-events-none absolute inset-0 rounded-full shadow-[inset_0_1px_0_rgba(255,255,255,0.35)]" />
      <span className="relative z-10">{children ?? label ?? "Run tool"}</span>
    </motion.button>
  )
}
