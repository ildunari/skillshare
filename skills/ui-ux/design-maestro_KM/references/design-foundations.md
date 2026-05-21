# Design Foundations

> Token architecture, designer-grade polish details, surface quality targets, and craft principles. Load on from-scratch builds, full redesigns, and any task where you're establishing a design system.

---

## Token Architecture

Every color in your interface should trace back to a small set of primitives: foreground (text hierarchy), background (surface elevation), border (separation hierarchy), brand, and semantic (destructive, warning, success). No random hex values — everything maps to primitives.

### Surface elevation hierarchy

Surfaces stack. A dropdown sits above a card which sits above the page. Build a numbered system:

- **Level 0:** Base background (the app canvas)
- **Level 1:** Cards, panels (same visual plane as base)
- **Level 2:** Dropdowns, popovers (floating above)
- **Level 3:** Nested dropdowns, stacked overlays
- **Level 4:** Highest elevation (rare)

In dark mode, higher elevation = slightly lighter. Each jump should be only a few percentage points of lightness — surface-100 at 7% lighter than base, surface-200 at 9%, surface-300 at 12%. You can barely see the difference in isolation. But when surfaces stack, the hierarchy emerges.

Key decisions:

- **Sidebars:** Same background as canvas, not different. Different colors fragment the visual space into "sidebar world" and "content world." A subtle border is enough separation.
- **Dropdowns:** One level above their parent surface. If both share the same level, the dropdown blends into the card and layering is lost.
- **Inputs:** Slightly *darker* than their surroundings, not lighter. Inputs are "inset" — they receive content. A darker background signals "type here" without heavy borders.
- **Context-aware bases:** Marketing pages might use darker/richer backgrounds. Dashboard uses neutral working background. The elevation system works the same — just starts from a different base.
- **Alternative/inset backgrounds:** Slightly darker recessed backgrounds for empty states, code blocks, inset panels, visual grouping without borders. Depth without shadows.

### Text hierarchy

Build four levels, not two:

- **Primary** — default text, highest contrast
- **Secondary** — supporting text, slightly muted
- **Tertiary** — metadata, timestamps, less important
- **Muted** — disabled, placeholder, lowest contrast

### Border progression

Use rgba, never solid hex. Low opacity (0.05–0.12 alpha in dark mode, slightly higher in light) blends with the background — it defines edges without demanding attention.

- **Default** — standard borders
- **Subtle** — softer separation
- **Strong** — emphasis, hover states
- **Stronger** — maximum emphasis, focus rings

Prefer `0.5px` hairline borders for the Vercel/Linear look. `1px` is often too heavy for refined interfaces.

### Dedicated control tokens

Form controls (inputs, checkboxes, selects) get their own tokens: control background, control border, control focus. Don't reuse surface tokens — let interactive elements be tuned independently.

---

## Designer-Grade Polish

These are the details that separate "looks fine" from "someone actually designed this." Apply on every build.

### Typography polish

- **Letter-spacing scales with size.** Tighter tracking (`-0.02em` to `-0.04em`) on display/headline text, normal or slightly wider on body and small text. Default tracking everywhere is an AI tell.
- **Font smoothing on dark backgrounds.** Always apply `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;` — without it, light text on dark looks chunky and over-rendered.
- **Responsive typography via clamp().** Use `font-size: clamp(1.5rem, 4vw, 3rem)` instead of breakpoint jumps. Fluid feels more natural.
- **Monospace for data.** Numbers, IDs, codes, timestamps belong in monospace with `font-variant-numeric: tabular-nums` for column alignment. Mono signals "this is data."

### Micro-interactions and states

- **Hover shifts are tiny.** 3–5% background lightness change. A hover that screams is a hover that's wrong.
- **Transition timing.** 150ms for micro-interactions (hover, focus). 200–250ms for layout changes (modals, panels). Always `ease-out` or `cubic-bezier(0.16, 1, 0.3, 1)` for deceleration. Never `ease-in-out` for UI — things should arrive fast, not ramp up.
- **Disabled states need three changes.** Reduced opacity + desaturated color + `cursor: not-allowed`. Most AI output only does opacity.
- **Table row hover.** Subtle background tint: `background: oklch(50% 0 0 / 0.04)`. Not a border, not bold.

### Focus and interaction

- **Focus rings via box-shadow, not outline.** `box-shadow: 0 0 0 2px var(--ring)` respects border-radius. `outline` doesn't on older browsers and looks janky.
- **Ring offset on dark backgrounds.** `box-shadow: 0 0 0 2px var(--bg), 0 0 0 4px var(--ring)` — the inner gap prevents the ring from bleeding into the element.
- **Button padding ratios.** Always more horizontal than vertical (`8px 16px` or `10px 20px`). Equal padding on buttons looks boxy.
- **Custom cursor on interactive cards.** `cursor: pointer` on clickable cards. Obvious but constantly forgotten.

### Visual refinement

- **Selection color.** `::selection { background: oklch(65% 0.15 250 / 0.3) }` — match to your accent. Default blue selection on a warm palette is a dead giveaway.
- **Placeholder opacity.** `::placeholder { opacity: 0.4 }` — browser defaults vary and are usually too dark.
- **Scrollbar styling.** `::-webkit-scrollbar` with thin, muted tracks. Default OS scrollbars on a polished dark UI are jarring.
- **Backdrop blur.** `backdrop-filter: blur(12px)` with `background: oklch(0% 0 0 / 0.6)` for overlays. Most people skip it or over-blur.
- **Icon containers.** Standalone icons get a subtle background container (circle or rounded square at ~6% opacity) for visual presence. Naked floating icons look unfinished.

### Alignment and spacing

- **Optical vs mathematical alignment.** A circle and a square at the same pixel size don't look the same size. Icons next to text need optical adjustment, not pixel-perfect centering.
- **Consistent icon-text gap.** Pick one value (6px or 8px) and use it everywhere for icon+text pairs. Varying this is an instant "no system" tell.
- **Dividers vs borders.** Full-width dividers inside cards should use `margin-inline` to respect card padding, or intentionally bleed to edges — but choose.
- **Loading skeletons match content shapes.** Skeleton blocks should be the exact dimensions of the content they replace. Generic rectangles everywhere is lazy.
- **Truncation strategy.** `line-clamp` for multi-line, `text-overflow: ellipsis` for single-line, gradient fade for elegant multi-line. Pick one per project, be consistent.

---

## Surface Quality Guide

Positive targets for common quality issues — what to aim for, with specific values.

- **Borders:** Reduce opacity until borders are felt rather than seen — rgba at 0.06–0.10 alpha in dark mode, slightly higher in light. If borders are the first thing you notice, dial back or switch to surface color differences.
- **Surface elevation:** Whisper-quiet transitions between levels — 2-3% lightness shifts per step. The hierarchy should emerge from stacking, not from dramatic jumps.
- **Spacing:** Derive all spacing from a consistent base unit (4px or 8px scale). Inconsistent spacing is the clearest sign of no design system.
- **Depth strategy:** Commit to one approach per project (borders-only, subtle shadows, layered shadows, or surface color shifts). Mixing approaches fragments the visual language.
- **Interaction states:** Every interactive element gets default, hover, active, focus, and disabled states. Every data display gets loading, empty, and error states.
- **Shadows:** Soft, diffused, low-opacity — `0 4px 12px rgba(0,0,0,0.08)` as a starting point. If the shadow draws attention to itself, it's too strong.
- **Border radius:** Scale radius with element size — 4-6px for small elements (buttons, inputs), 8-12px for cards, 16+ for hero containers. Large radius on small elements looks inflated.
- **Card surfaces:** Tint cards to match the background hue at slightly different lightness, not pure white on colored backgrounds. Pure white cards create holes in the visual field.
- **Decorative borders:** Keep borders functional (separation, grouping, focus). Thick decorative borders add visual noise without information.
- **Color with purpose:** Every color should communicate something — status, action, emphasis, identity. Unmotivated gradients and decorative color are noise. One accent color used with intention beats five used without thought. Semantic colors (success, warning, error, info) are a separate system and don't count against the accent budget.
- **Surface hue consistency:** Keep the same hue family across all surfaces, shifting only lightness for elevation. Different hues for different surfaces fragments the palette.
- **Transition easing:** Use `ease-out` or `cubic-bezier(0.16, 1, 0.3, 1)` for UI transitions — things should arrive fast and settle. `ease-in-out` creates a ramp-up that feels sluggish.
- **Display typography:** Tighten letter-spacing on headlines and display text (`-0.02em` to `-0.04em`). Default tracking on large text is an AI tell.

---

## Craft Foundations

### Infinite expression

Every pattern has infinite expressions. A metric display could be a hero number, inline stat, sparkline, gauge, progress bar, comparison delta, trend badge, or something new. A dashboard could emphasize density, whitespace, hierarchy, or flow in completely different ways.

Before building, ask: What's the one thing users do most here? What products solve similar problems brilliantly? Why would this interface feel designed for its purpose, not templated?

Linear's cards don't look like Notion's. Vercel's metrics don't look like Stripe's. Same concepts, infinite expressions.

### Color lives somewhere

Every product exists in a world. That world has colors. Before you reach for a palette, spend time in the product's world. What would you see if you walked into the physical version of this space? What materials? What light?

Beyond warm and cold: Is this quiet or loud? Dense or spacious? Serious or playful? Geometric or organic? A trading terminal and a meditation app are both "focused" — completely different kinds of focus. Find the specific quality, not the generic label.

Gray builds structure. Color communicates — status, action, emphasis, identity. Unmotivated color is noise. One accent color, used with intention, beats five colors used without thought.

### Depth strategy (pick ONE, commit)

- **Borders-only** — Clean, technical, dense. Linear, Raycast.
- **Subtle shadows** — Soft lift. Approachable products.
- **Layered shadows** — Premium, dimensional. Stripe, Mercury.
- **Surface color shifts** — Background tints establish hierarchy without shadows.

Don't mix approaches within a project.

### Controls deserve craft

Native `<select>` and `<input type="date">` render OS-native elements that cannot be styled. Build custom components: trigger buttons with positioned dropdowns, calendar popovers, styled state management. Custom select triggers must use `display: inline-flex` with `white-space: nowrap`.

### States are not optional

Every interactive element needs: default, hover, active, focus, disabled. Data needs: loading, empty, error. Missing states feel broken.
