# Planning methodology (before coding)

This is the bridge between “requirements” and “production code”.

## 1) Produce a 1-page implementation plan

Keep it concrete. No moodboards.

### Plan template

```md
## Overview
- Goal:
- Audience:
- Platform priority: Mobile / Desktop / Both
- Framework + styling:

## IA / Sections
1. Header (nav, brand, utility actions)
2. Hero (headline, supporting copy, primary CTA)
3. Core content (list/grid/form)
4. Secondary content (proof, FAQ, details)
5. Footer

## Components
Reusable:
- ...
One-off:
- ...

## Tokens (v1)
Typography:
- --font-display:
- --font-body:
- scale:
Spacing:
- base unit:
Color roles:
- --bg:
- --surface:
- --text:
- --muted:
- --accent:
Radii/shadows:
- ...

## Responsiveness
Breakpoints:
- mobile:
- tablet:
- desktop:
Layout changes:
- ...

## States + a11y
States:
- loading/empty/error
Keyboard:
- focus order:
- menu/dialog behavior:
Motion:
- prefers-reduced-motion rules

## Implementation order
1. Skeleton + semantics
2. Tokens + base styles
3. Layout + responsive
4. Interactions + states
5. A11y pass
6. Motion + polish
7. Perf pass
```

## 2) Break the UI into “layout primitives” + “features”

**Layout primitives** (reusable foundations):
- Container
- Stack (vertical rhythm)
- Grid
- Section header (eyebrow, title, subtitle)
- Button, Link, Input, Select, Badge

**Feature components** (domain-specific):
- Search results list
- Pricing table
- Settings panel
- Checkout summary

This keeps your design system from becoming “a pile of one-offs”.

## 3) Define tokens first (even if tiny)

If you don’t define tokens, you’ll ship magic numbers and inconsistent vibes.

### Vanilla CSS tokens

```css
:root {
  /* Typography */
  --font-body: ui-sans-serif, system-ui, sans-serif;
  --font-display: ui-serif, Georgia, serif;

  --text-1: 1rem;
  --text-2: 1.125rem;
  --text-3: 1.375rem;
  --text-4: 1.875rem;

  /* Spacing */
  --s-1: 0.25rem;
  --s-2: 0.5rem;
  --s-3: 0.75rem;
  --s-4: 1rem;
  --s-6: 1.5rem;
  --s-8: 2rem;
  --s-12: 3rem;

  /* Color roles */
  --bg: #0b0f14;
  --surface: #111827;
  --text: #e5e7eb;
  --muted: #9ca3af;
  --accent: #facc15;

  /* Interaction */
  --focus: color-mix(in oklab, var(--accent) 70%, white);
  --radius: 14px;
}
```

Then consume tokens everywhere.

## 4) Responsive plan: mobile-first, content-first

### Breakpoints (practical defaults)

- **Mobile:** ≤ 640px
- **Tablet:** 641–1024px
- **Desktop:** ≥ 1025px

Don’t overfit breakpoints. Let content drive layout changes.

### Plan the content order for mobile

On mobile:
- primary CTA in thumb reach
- avoid multi-column text
- collapse secondary details behind accordions

## 5) State design: enumerate before you implement

For each interactive unit, list states:

- default
- hover (desktop)
- focus-visible (keyboard)
- active/pressed
- disabled
- loading
- error
- empty
- success (if applicable)

Then implement them systematically.

## 6) Risk management: avoid “big rewrite” failure

If working in an existing codebase:
- isolate changes behind a feature flag if risky
- ship tokens + base styles first (low risk)
- refactor one component at a time
