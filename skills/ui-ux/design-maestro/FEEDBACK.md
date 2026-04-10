# Design Maestro — Feedback Log

> **MUST-READ when loading this skill.** This file captures observed issues, successful patterns, and improvement opportunities discovered during use. Read before building. Max 75 entries — compact old entries when approaching cap.

## Format

Each entry: `[CATEGORY] Date — observation (context)`

## Categories

- `[SLOP]` — AI-generated design patterns that slipped through
- `[TYPOGRAPHY]` — Font pairing, sizing, or spacing issues
- `[COLOR]` — Palette generation, contrast, or dark mode issues
- `[LAYOUT]` — Spacing, grid, responsive, or structural issues
- `[MOTION]` — Animation timing, performance, or accessibility issues
- `[A11Y]` — Accessibility failures or improvements
- `[PATTERN]` — UI pattern that worked well or failed
- `[THEME]` — Visual theme application issues
- `[PERF]` — Performance issues (render, load, animation)
- `[COPY]` — Micro-copy, labels, or content issues
- `[AI-UI]` — AI-native UI pattern issues (streaming, citations, tool use)
- `[ITERATION]` — Multi-turn refinement issues (patch vs rebuild, decision tracking, drift)
- `[FEEDBACK]` — Vague/conflicting user feedback handling (translation, diagnostics, preservation)
- `[CSS-DEBUG]` — CSS/layout debugging process issues (root cause, stacking contexts, responsive)
- `[REVIEW]` — Design review and visual QA issues (severity triage, missed checks)
- `[META]` — Skill structure, documentation, or process issues

## Entries

`[LAYOUT]` 2026-02-18 — AUDIT: Six hardcoded chart dimensions found in data-viz.md templates (ThemedChart, InteractiveLegendChart, LiveChart, CanvasLineChart, OptimisticLiveChart) using width={600}/height={300} or width={800}/height={400} directly on chart components. These ignore surrounding layout chrome and will overflow or mis-size in real containers. Fixed: wrapped Recharts examples with ResponsiveContainer; replaced canvas examples with ResizeObserver pattern. (deep/data-viz.md)

`[LAYOUT]` 2026-02-18 — AUDIT: Sankey diagram template rendered labels for ALL nodes regardless of node height. At small `nodePadding` or with many nodes, labels on thin nodes overlap adjacent labels and spill outside node bounds. Fixed: added `nodeHeight >= 20` gate before rendering `<text>`. (deep/data-viz.md, SankeyDiagram)

`[LAYOUT]` 2026-02-18 — AUDIT: PointMap template renders persistent city name labels at y={-12} for every marker. In dense geographic regions, labels collide. Added inline spatial note explaining tooltip-first strategy for variable-density data and the threshold for safe persistent labels (< 20 visible markers, sparse distribution). (deep/data-viz.md, PointMap)

`[LAYOUT]` 2026-02-18 — AUDIT: No skill-wide guidance on label collision or spatial integrity existed anywhere — not in SKILL.md, design-review.md, patterns-and-recipes.md, or aesthetic-principles.md. Added "Label Placement & Spatial Integrity" section to data-viz.md with 6 rules covering: responsive containers, ResizeObserver for canvas, size-gated labels, separated spatial lanes, tooltip-first for dense data, and getBBox post-render collision detection. Also added "Section 7: Spatial integrity" to design-review.md rubric. (deep/data-viz.md, design-review.md)

`[REVIEW]` 2026-02-18 — AUDIT: design-review.md rubric had 6 sections (hierarchy, color, typography, responsiveness, interaction, motion) but no section covering spatial/overlap defects in data visualizations. These are the most common class of silent defects in LLM-generated charts. Added Section 7. (design-review.md)

`[META]` 2026-02-22 — SKILL.md philosophy sections (Intent First, Domain Exploration, Per-Component Checkpoint, The Mandate) moved to `references/design-philosophy.md`. SKILL.md reduced from 424 to 290 lines. Routing table updated to point to design-philosophy.md for from-scratch builds and full design process. Cross-references from from-scratch.md and existing-project.md may still point to "SKILL.md → Intent First" — check and update on next load. (v2 restructure)

`[META]` 2026-02-13 — Deep file anchor system (stable `<!-- anchor:name -->` comments replacing fragile grep header targets) is a good idea but requires full reads of all 7 deep files (~15k lines). Deferred. (Audit §4.2)

`[META]` 2026-02-13 — Anti-patterns.md split (anti-slop vs accessibility vs dark-mode vs performance) would improve grep targeting but requires reading the full 3,500-line file. Deferred. (Audit §4.4)

`[FEEDBACK]` 2026-02-13 — User said "make it pop more." Translation table mapped correctly: increased heading/body contrast, added saturated accent, introduced staggered entry animations. User confirmed. Validates mapping: "pop" = contrast + saturation + motion. (design-feedback.md)

`[ITERATION]` 2026-02-13 — On turn 6, user requested palette change contradicting turn-2 approval. Flagged per design-iteration protocol. User chose to revise. Without the conflict flag, the old palette would have been silently overwritten. Decision tracking is load-bearing. (design-iteration.md)

`[CSS-DEBUG]` 2026-02-13 — Spent 3 CSS patches on z-index before diagnosing that a `transform` on a parent created a new stacking context. design-debugging.md explicitly lists `transform` as a stacking context creator. Should have diagnosed the category first. The Iron Law applies to CSS too. (design-debugging.md)

`[LAYOUT]` 2026-02-22 — Built a flow diagram artifact defaulting to landscape/horizontal node layout. User had to explicitly ask to make it portrait. For any artifact where mobile is likely (and it almost always is), default to vertical/portrait flow — horizontal layouts require horizontal scrolling on phones, which is awkward and breaks the reading direction. Ask about target device before laying out complex diagrams. (mcp-architecture diagrams)

`[LAYOUT]` 2026-02-22 — First version of a diagram artifact put all info panels (description, pros/cons, legend) inline in the main scroll area. This consumed most of the visible canvas on a phone screen and buried the diagram. Rule: on mobile, the diagram IS the primary content — everything else is secondary. Move supplemental info into a collapsible bottom sheet, drawer, or modal. Canvas should be full-screen minus a thin tab bar. (mcp-architecture diagrams)

`[PATTERN]` 2026-02-22 — Used a tap-to-toggle button for the bottom sheet open/close state. User wanted a real drag gesture — finger follows the sheet in real time, velocity-based snap on release, rubber-band past limits. A button is never an acceptable substitute for a drag handle on mobile sheets. When building bottom sheets for mobile: (1) track raw pointer/touch Y coordinates directly, (2) apply translateY with no transition during drag, (3) measure release velocity and snap to nearest or direction-of-fling, (4) add sqrt rubber-band resistance past open/closed limits. (mcp-architecture diagrams)

`[COLOR]` 2026-02-22 — Dark theme artifact appeared white/beige on iPhone because `body` background set via injected `<style>` wasn't being applied to the iframe root in Claude's artifact renderer. Fix: always set `background` explicitly on the outermost JSX container div, not just on `body`/`html` via injected style. Treat the root `<div>` as the canonical background surface, not the document. (mcp-architecture diagrams)

`[LAYOUT]` 2026-02-22 — Bottom node in portrait diagram was cut off because the canvas had a fixed-height scroll area with insufficient bottom padding. The bottom sheet overlay covered the last ~80px of content. Rule: bottom padding on scrollable canvas content must be at least `COLLAPSED_SHEET_HEIGHT + 40px`. For pan/zoom canvases (no native scroll), add the same padding inside the transform wrapper. (mcp-architecture diagrams)

`[PATTERN]` 2026-02-22 — Complex diagrams on mobile benefit from pinch-to-zoom + pan rather than trying to fit everything into the viewport at once. Implementation: wrap diagram in a container with `touch-action: none`, track 1-finger drag for pan and 2-finger pinch for zoom via raw touchstart/touchmove/touchend listeners. Apply `transform: translate(tx,ty) scale(s)` with `transformOrigin: "0 0"` on an inner wrapper. Zoom toward the pinch midpoint: `newTx = mid.x - scaleFactor * (mid.x - prevTx)`. Clamp scale between 0.4–3.5. Add a small "reset" button for when users get lost. Conflicts with bottom sheet drag resolved by a shared `sheetIsDragging` ref — canvas touch handlers bail early when the sheet is being dragged. (mcp-architecture diagrams)

`[MOTION]` 2026-02-23 — framer-motion IS fully available in Claude React artifacts. `import { motion, AnimatePresence, useMotionValue, useSpring, useTransform, LayoutGroup }` all work without any CDN config. Verified with stress test: drag, layoutId shared layout, spring physics, 3D tilt with useTransform, AnimatePresence mode=popLayout, stagger orchestration — zero errors. Updated `references/motion-library.md` to remove the wrong constraint. For HTML (non-React) artifacts, framer-motion still cannot be used — fall back to CSS/Web Animations API there.

`[A11Y]` 2026-02-22 — Browser pull-to-refresh fired when user dragged the bottom sheet upward from near the top of the page, dismissing the artifact instead of opening the sheet. Fix requires: `touch-action: none` on the sheet element AND `{ passive: false }` on touchstart/touchmove listeners so `preventDefault()` actually cancels the scroll. `passive: false` is non-negotiable — passive listeners cannot call preventDefault. Also set `overscroll-behavior: none` on body and `overscroll-behavior: none` on scroll containers. The diagram canvas scroll area should use `touch-action: pan-y` (not `none`) so it still scrolls the diagram content. (mcp-architecture diagrams)
