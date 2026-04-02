---
name: ui-ux-implementation
description: |
  Use when the user wants real implementation work on a product UI: auditing an existing interface, translating requirements into a build plan, and shipping production-ready frontend code in HTML/CSS/JS, React, Vue, or Tailwind.

  Trigger on requests to build a new app interface from a spec, refactor or redesign an existing UI, make a screen feel less generic, improve accessibility or responsiveness, tighten a design system, or fix product UX problems like navigation, forms, hierarchy, and mobile layout.

  Do not use for pure marketing copy, brand strategy, or non-implementation visual brainstorming.
license: CC BY 4.0 — design principles adapted from Madina Gbotoe (madinagbotoe.com)
---

# UI/UX Implementation

**ARGUMENTS:** `$ARGUMENTS`

This is an end-to-end UI/UX *implementation* skill: it can audit an existing UI, translate requirements into a plan, and ship real code (not pseudocode). It keeps the original "research-backed, opinionated critic" energy — but now it's accountable for clean implementation.

## Inputs this skill accepts

- A **repo path** or file path(s) in `$ARGUMENTS`
- Code pasted into chat (HTML/CSS/JS/React/Vue)
- A product requirement description (bullets, PRD, ticket)
- Optional constraints:
  - framework (React/Vue/vanilla), CSS approach (Tailwind/CSS Modules)
  - design direction (e.g., "editorial", "terminal noir", "brutalist")
  - brand tokens, fonts, screenshots, component library constraints

If requirements are incomplete, ask **at most 3–6** high-value questions. Otherwise, state assumptions and proceed.

## Progressive disclosure: what to load (and when)

Load only what's needed for the task:

- Code/UI audit process: [references/analysis-patterns.md](references/analysis-patterns.md)
- Requirements extraction + clarifying questions: [references/requirements-gathering.md](references/requirements-gathering.md)
- Planning templates + sequencing: [references/planning-methodology.md](references/planning-methodology.md)
- Implementation patterns + code scaffolds: [references/implementation-guide.md](references/implementation-guide.md)

Research-backed design guidance (for decisions and critique):
- UX principles + citations: [references/design-principles.md](references/design-principles.md)
- Typography: [references/typography-guide.md](references/typography-guide.md)
- Color systems + theming: [references/color-systems.md](references/color-systems.md)
- Accessibility patterns: [references/accessibility.md](references/accessibility.md)
- Motion/animation: [references/animations.md](references/animations.md)

Framework specifics:
- React: [references/framework-patterns/react.md](references/framework-patterns/react.md)
- Vue: [references/framework-patterns/vue.md](references/framework-patterns/vue.md)
- Tailwind: [references/framework-patterns/tailwind.md](references/framework-patterns/tailwind.md)
- Vanilla CSS/HTML: [references/framework-patterns/vanilla-css.md](references/framework-patterns/vanilla-css.md)

Examples (only if you need calibrated patterns quickly):
- [references/examples/hero-section.md](references/examples/hero-section.md)
- [references/examples/navigation.md](references/examples/navigation.md)
- [references/examples/card-layouts.md](references/examples/card-layouts.md)

Optional scripts (only if you want faster repo triage):
- `scripts/ui_slop_scan.py` (flags common template signals)
- `scripts/component_inventory.py` (quick component inventory)

---

# Default operating rules

## 1) Research over vibes
When recommending layout, hierarchy, navigation placement, scanning patterns, or motion — tie it to research and user behavior. Cite sources in the report when relevant (URLs are enough).

## 2) Distinctive over generic
Actively avoid "AI slop" defaults (generic fonts, purple gradients, three-card grids everywhere). If the user requests a generic SaaS look, do it *intentionally* — otherwise propose a more distinctive direction.

## 3) Accessibility is non-negotiable
Ship WCAG AA as a baseline (keyboard, focus, labels, contrast, reduced motion). Use [references/accessibility.md](references/accessibility.md).

## 4) Implementation-first deliverables
Every critique must translate into:
- a **prioritized plan**
- **specific code edits** (diffs or file replacements)
- **validation steps** (a11y + responsive + performance)

---

# Workflow 1: Analyze an existing UI (audit + fixes)

Load: [references/analysis-patterns.md](references/analysis-patterns.md) and (as needed) [references/accessibility.md](references/accessibility.md), [references/design-principles.md](references/design-principles.md)

1. **Inventory (fast)**
   - Identify framework and styling system.
   - Map the component tree / layout regions (navigation, hero, content, forms).
   - Note design tokens (colors, type scale, spacing) — explicit or implied.

2. **Issues (ranked)**
   - List issues with **Priority: Critical / High / Medium / Low**
   - For each issue include:
     - *What's wrong* (specific)
     - *Why it matters* (user impact + research where applicable)
     - *Fix* (code-level, not theory)
     - *Effort* (S/M/L)

3. **Fix pack**
   - Implement the top **1–3** highest ROI changes first.
   - Prefer minimal, targeted diffs over full rewrites.

4. **Validation**
   - Keyboard pass (Tab/Shift+Tab/Enter/Esc)
   - Contrast and focus visible
   - Mobile layout + touch targets
   - Reduce motion support

**Audit output format (default):**
- Verdict (1 paragraph)
- Critical issues (with fixes + code)
- Aesthetic direction (what to preserve vs replace)
- Implementation plan (ordered checklist)
- Sources (URLs)

---

# Workflow 2: Build a new UI from requirements (plan → ship)

Load: [references/requirements-gathering.md](references/requirements-gathering.md), [references/planning-methodology.md](references/planning-methodology.md), then [references/implementation-guide.md](references/implementation-guide.md)

1. **Parse requirements**
   - Extract: primary user goal, key screens/sections, interactions, constraints.
   - If missing: ask up to 3–6 targeted questions; otherwise write assumptions.

2. **Define the design system (lightweight)**
   - Tokens: type scale, spacing scale, color roles, radii, shadows.
   - Interaction states: hover/active/focus/disabled/loading.

3. **Component breakdown**
   - Identify reusable components vs one-offs.
   - Decide state boundaries (local state vs lifted state).

4. **Responsive plan**
   - Mobile-first layout, breakpoints, and content prioritization.
   - Thumb-zone placement for primary actions when mobile-heavy.

5. **Implement**
   - Build skeleton + semantics first.
   - Style with tokens (avoid magic numbers).
   - Add interactions + states.
   - Add accessibility (ARIA only when needed).
   - Add motion polish (respect reduced-motion).

6. **Performance pass**
   - Reduce layout shift, optimize images, avoid heavy effects, keep CSS cheap.

---

# Workflow 3: Improve an existing UI (preserve → evolve)

Load: [references/analysis-patterns.md](references/analysis-patterns.md), [references/planning-methodology.md](references/planning-methodology.md)

1. **Audit current UI** (Workflow 1)
2. **Decide "preserve vs change"**
   - Preserve: information architecture, successful flows, known-good components.
   - Change: hierarchy, spacing, typography, navigation ergonomics, a11y gaps.
3. **Plan incremental refactor**
   - Phase 1: tokens + layout fixes (low risk)
   - Phase 2: component refactors (medium risk)
   - Phase 3: interaction/motion polish (optional)
4. **Implement incrementally**
   - Keep diffs reviewable.
   - Don't break API contracts unless explicitly requested.
5. **Validate** (a11y + responsive + perf)

---

# Quality gates

Before calling it done, confirm:

- **A11y:** keyboard works, focus visible, labels correct, contrast ok, reduced-motion ok
- **Responsive:** content order makes sense on narrow screens; no horizontal scroll
- **Performance:** no obvious CLS triggers; animations are transform/opacity; images sized
- **No AI slop:** typography and palette feel intentional; layout isn't "SaaS template #4"
- **Maintainability:** tokens + reusable components; avoids one-off styling sprawl
