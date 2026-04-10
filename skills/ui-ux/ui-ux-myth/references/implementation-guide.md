# Implementation guide (shipping UI)

This module is where you turn a plan into production code.

## 1) Implementation sequence (don’t skip)

1. **Skeleton + semantics**
   - correct landmarks: header/main/footer
   - real buttons/links/inputs (not divs)
2. **Tokens + base styles**
   - establish typography, spacing rhythm, color roles
3. **Layout**
   - grid/stack/container primitives
4. **Interactions + states**
   - hover/focus/pressed/disabled/loading/error/empty
5. **Accessibility pass**
   - keyboard, focus, labels, reduced-motion
6. **Motion polish**
   - subtle, purposeful, fast
7. **Performance pass**
   - image sizes, avoid heavy effects, reduce rerenders

## 2) Component library patterns (reusability without bureaucracy)

### A) Primitives layer (design system)

Create or locate:
- `Button`
- `Link`
- `Input`, `Textarea`, `Select`
- `Badge`
- `Card` (careful: not everything should be a card)
- `Dialog` / `Popover` primitives (or use an accessible library)

**Rule:** primitives should be styleable via props (variant/size), but not explode into 40 variants.

### B) Composites layer (product components)

- `PricingCard`, `UserMenu`, `SearchResults`, `SettingsPanel`
- Compose primitives; keep product logic here.

## 3) Design tokens that work in any stack

### CSS variables + data-theme

```css
:root {
  --bg: #0b0f14;
  --surface: #0f172a;
  --surface-2: #111c35;
  --text: #e5e7eb;
  --muted: #9ca3af;
  --accent: #facc15;
  --danger: #fb7185;

  --radius: 14px;
  --shadow: 0 12px 30px rgba(0,0,0,0.35);

  --focus: color-mix(in oklab, var(--accent) 65%, white);
}

[data-theme="light"] {
  --bg: #fbfbf7;
  --surface: #ffffff;
  --surface-2: #f3f4f6;
  --text: #0b0f14;
  --muted: #475569;
  --shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
}
```

Consume these tokens in vanilla CSS *or* in Tailwind via config (see [framework-patterns/tailwind.md](framework-patterns/tailwind.md)).

## 4) Distinctive design guardrails (anti-template)

When implementing any section, force at least **one signature move**:

- Typographic contrast (display face + mono accent, or serif + grotesk)
- Asymmetric grid (2/3 + 1/3, or offset blocks)
- Texture/depth (subtle noise, patterned gradient, colored shadow)
- Non-generic rhythm (big jumps between type sizes, not 16→18→20)

But don’t sabotage usability: keep headings scannable and actions obvious.

## 5) Accessibility baked in (not patched)

Use [accessibility.md](accessibility.md) for patterns. Key rules:

- Use semantic elements first.
- Use `:focus-visible` styles on all interactive elements.
- Don’t rely on color alone for status.
- Respect `prefers-reduced-motion`.

## 6) Framework-specific scaffolds

### A) React component scaffold (no external UI lib required)

```tsx
import * as React from "react";

type ButtonVariant = "primary" | "secondary" | "ghost";
type ButtonSize = "sm" | "md" | "lg";

const base =
  "inline-flex items-center justify-center gap-2 rounded-[var(--radius)] font-medium " +
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--focus)] focus-visible:ring-offset-2 " +
  "disabled:opacity-50 disabled:pointer-events-none";

const variants: Record<ButtonVariant, string> = {
  primary: "bg-[var(--accent)] text-black shadow-[var(--shadow)] hover:translate-y-[-1px] active:translate-y-0",
  secondary: "bg-[var(--surface-2)] text-[var(--text)] hover:bg-[color-mix(in_oklab,var(--surface-2),white_6%)]",
  ghost: "bg-transparent text-[var(--text)] hover:bg-[color-mix(in_oklab,var(--surface),white_6%)]",
};

const sizes: Record<ButtonSize, string> = {
  sm: "h-9 px-3 text-sm",
  md: "h-11 px-4 text-sm",
  lg: "h-12 px-5 text-base",
};

export function Button({
  asChild,
  variant = "primary",
  size = "md",
  className = "",
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  asChild?: boolean;
  variant?: ButtonVariant;
  size?: ButtonSize;
}) {
  if (asChild) {
    // Optional: implement with a Slot pattern if you have one; otherwise remove asChild.
    throw new Error("asChild not implemented in this scaffold");
  }

  return (
    <button
      {...props}
      className={[base, variants[variant], sizes[size], className].join(" ")}
    />
  );
}
```

Notes:
- Uses tokens via CSS variables.
- Implements focus ring and disabled state.
- Keeps variants limited and intentional.

### B) Vue SFC scaffold

See [framework-patterns/vue.md](framework-patterns/vue.md) for patterns, including transitions and accessibility.

### C) Vanilla HTML/CSS scaffold

See [framework-patterns/vanilla-css.md](framework-patterns/vanilla-css.md) for modern CSS architecture and responsive patterns.

## 7) Responsive implementation (concrete patterns)

### Container + section rhythm (vanilla CSS)

```css
.Container {
  width: min(1100px, 100% - 2rem);
  margin-inline: auto;
}

.Section {
  padding-block: clamp(2.5rem, 4vw, 4rem);
}

.Stack > * + * {
  margin-top: var(--s-4);
}
```

### Responsive grid (vanilla CSS)

```css
.Grid {
  display: grid;
  gap: var(--s-6);
}

@media (min-width: 768px) {
  .Grid--2 {
    grid-template-columns: 1.5fr 1fr; /* asymmetric by default */
    align-items: start;
  }
}
```

## 8) UI state management patterns

### A) Local UI state (simple)
- input value
- modal open/closed
- active tab
- selected item

### B) Derived state (avoid duplication)
- `isEmpty = items.length === 0 && !isLoading`
- `canSubmit = isValid && !isSubmitting`

### C) Async state (standardize)
Use a small state machine-ish pattern:

```ts
type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };
```

This prevents “random booleans everywhere”.

## 9) Performance checklist (UI-focused)

- Avoid animating layout properties (width/height/top/left)
- Prefer transform/opacity animations
- Provide image dimensions, set `loading="lazy"` for below-the-fold
- Avoid huge blur/backdrop-filter on big surfaces
- Keep long lists virtualized if needed
- Don’t ship 6 font weights unless necessary; subset/self-host if possible

## 10) Final polish: micro-interactions (purposeful)

Use motion to:
- indicate state change (expand/collapse, selection)
- confirm action (toast, inline success)
- guide attention (staggered entrance *once*)

Avoid motion that fights reading (auto-rotating carousels).
