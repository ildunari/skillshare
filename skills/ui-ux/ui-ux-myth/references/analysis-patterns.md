# Code analysis patterns

Use this when you need to understand an existing UI codebase quickly and produce actionable fixes.

## 0) Fast intake checklist (2–5 minutes)

1. **Stack**
   - Framework: React / Vue / Svelte / vanilla
   - Rendering: CSR / SSR (Next/Nuxt) / static
   - Styling: Tailwind / CSS Modules / styled-components / plain CSS
   - UI libs: Radix, Headless UI, MUI, Chakra, etc.
2. **Entrypoints**
   - Where is the page composed? (routes, pages/, app/)
   - Where are primitives? (`components/ui`, `design-system`, `styles/`)
3. **Constraints**
   - Existing tokens? brand guidelines? dark mode? i18n?
   - Must preserve existing behavior? analytics events? API contracts?

## 1) Build a component + layout inventory

### What to extract

- **Page regions**: global nav, header/hero, main content, forms, footer
- **Component tree**: what composes what (top-down)
- **State boundaries**:
  - local component state
  - shared state (context/store)
  - URL state (query params, route)
- **Styling patterns**:
  - how spacing is done (scale? arbitrary?)
  - color usage (tokens vs hex)
  - typography (global vs per-component)
- **Interactions**: menus, dialogs, toasts, validation, loading patterns

### Quick scans (Bash + ripgrep)

Use these as starting points:

```bash
# Find entrypoints / routing
rg -n "createBrowserRouter|Routes\b|next/router|app/\(|pages/" .

# Find shared primitives
rg -n "components/ui|design-system|tokens|tailwind.config" .

# Find accessibility smells
rg -n "onClick\s*=\s*\{\(\)\s*=>|div\s+onClick|role=\"button\"" .

# Find font choices (slop detector)
rg -n "Inter|Roboto|Open Sans|Montserrat|Lato" .

# Find direct hex usage (token debt)
rg -n "#[0-9a-fA-F]{3,8}\b" .
```

If you can’t run bash, do manual reading with the same intent.

## 2) Evaluate issues across 5 axes

### A) Usability (behavior + heuristics)

- Navigation discoverability and consistency
- Visual hierarchy (what is “most important” and does it look like it?)
- Information scent (labels match user intent)
- Scannability (headings, chunking, meaningful subheads)
- Choice overload and progressive disclosure

Tie high-impact claims back to the research in:
- [design-principles.md](design-principles.md)

### B) Accessibility (WCAG AA baseline)

Non-negotiables:
- Semantic elements, correct labels
- Full keyboard support (including menus/dialogs)
- Visible focus
- Contrast minimums
- Reduced motion support
- Touch targets sized for mobile

Patterns + code: [accessibility.md](accessibility.md)

### C) UI quality (anti “AI slop”)

Flag:
- “SaaS template” sectioning (hero + 3 cards + alternating rows + testimonial strip)
- Centered paragraphs (esp. body text)
- Default font stacks (Inter/Roboto)
- Overused purple/blue gradients and blob backgrounds
- Identical border-radius on everything + same shadow on everything
- No meaningful typographic contrast (all 16–18px with mild weight changes)

Guidance:
- Typography: [typography-guide.md](typography-guide.md)
- Color: [color-systems.md](color-systems.md)
- Motion: [animations.md](animations.md)

### D) Maintainability

- Token usage vs magic numbers
- Component boundaries and reuse
- Classname sprawl (Tailwind) vs extracted components
- Duplication of layout primitives (Stack, Container, Grid)

### E) Performance

- Layout shift (missing image dimensions, async font swap without fallback)
- Heavy shadows/filters on big surfaces
- Unthrottled re-renders, large lists
- Unoptimized images / video autoplay

## 3) Prioritize: Impact × Effort

Use consistent severities:

- **Critical**: blocks task completion, causes a11y failure, or breaks core UX
- **High**: strongly harms discoverability, comprehension, or conversion
- **Medium**: quality/polish issues, minor friction
- **Low**: nice-to-have refinements, edge cases

Also include an **Effort** estimate:
- **S** (≤1h), **M** (half day–2d), **L** (>2d)

## 4) Report format (copy/paste)

```md
## Verdict
One paragraph: what works, what’s broken, overall direction.

## Inventory
- Framework:
- Styling:
- Key components:
- Tokens present? (Y/N)

## Issues (ranked)
### [Issue name] — Priority: High (Effort: S)
- What’s wrong:
- Why it matters:
- Evidence (optional): URL / principle
- Fix:
- Code (diff or snippet):

## Implementation plan
1. ...
2. ...

## Validation checklist
- [ ] Keyboard / focus
- [ ] Contrast
- [ ] Mobile layout
- [ ] Reduced motion
- [ ] Lighthouse / perf quick pass
```

## 5) “Fix with code” rules

- Prefer **semantic HTML** over ARIA.
- Prefer **minimal diffs** over rewrites.
- Fix **structure first**, then styling, then micro-interactions.
- When refactoring components, keep the public API stable unless asked.
- Always add **focus styles** when changing interactive elements.

## 6) Example: turning critique into a concrete fix

### Problem

```tsx
// Before: clickable div, no keyboard support, tiny hit target, generic styling
export function PriceCard({ plan, onSelect }) {
  return (
    <div className="card" onClick={() => onSelect(plan.id)}>
      <h3>{plan.name}</h3>
      <p>${plan.price}</p>
      <span>Choose</span>
    </div>
  );
}
```

### Fix (semantic button, focus, hit target, clearer hierarchy)

```tsx
export function PriceCard({ plan, onSelect }) {
  return (
    <section className="PriceCard" aria-labelledby={`plan-${plan.id}-title`}>
      <h3 id={`plan-${plan.id}-title`} className="PriceCard__title">
        {plan.name}
      </h3>

      <p className="PriceCard__price">
        <span className="PriceCard__priceValue">${plan.price}</span>
        <span className="PriceCard__priceUnit">/mo</span>
      </p>

      <button
        type="button"
        className="PriceCard__cta"
        onClick={() => onSelect(plan.id)}
      >
        Choose {plan.name}
      </button>
    </section>
  );
}
```

```css
.PriceCard__cta {
  min-height: 44px;
  min-width: 44px;
}

.PriceCard__cta:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 3px;
}
```

The point: every critique becomes a specific structural + interaction correction.


## Optional helpers (scripts)

If Python execution is available, you can use the bundled scripts:

```bash
# Heuristic scan for generic/template signals (fonts, gradients, centered text)
python scripts/ui_slop_scan.py --root .

# Inventory of components (React/Vue/Svelte)
python scripts/component_inventory.py --root src --out inventory.md
```

Treat results as a triage list, not a verdict.
