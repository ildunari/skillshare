# React patterns (UI implementation)

Use this when implementing in React (including Next.js).

## 1) File + component organization

A pragmatic structure:

```
src/
  components/
    ui/            # primitives (Button, Input, Dialog)
    layout/        # Container, Stack, Grid, Section
    features/      # product components (Pricing, SearchResults)
  styles/
    tokens.css     # CSS variables (color/type/spacing)
    globals.css
```

Keep primitives stable. Features can evolve.

## 2) Component API patterns that scale

### Prefer “variant + size” over dozens of props

Example:
- `variant="primary|secondary|ghost"`
- `size="sm|md|lg"`

Avoid:
- `primary`, `secondary`, `danger`, `outline`, `rounded`, `pill`, `raised`, ... (prop explosion)

### Use composition for complex components

Compound components are good for:
- menus
- tabs
- forms with repeated sub-structure

But don’t over-engineer.

## 3) Accessibility defaults

- Use `button` for actions
- Use `a` for navigation
- Implement `:focus-visible` consistently
- For icon-only buttons, provide `aria-label`

Example:

```tsx
export function IconButton({
  label,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { label: string }) {
  return (
    <button type="button" aria-label={label} {...props}>
      {children}
    </button>
  );
}
```

## 4) Form patterns

- Prefer controlled inputs only when necessary
- Use `useId()` to wire labels/hints/errors

```tsx
import * as React from "react";

export function EmailField({
  value,
  onChange,
  error,
}: {
  value: string;
  onChange: (v: string) => void;
  error?: string;
}) {
  const id = React.useId();
  const hintId = `${id}-hint`;
  const errorId = `${id}-error`;

  return (
    <div>
      <label htmlFor={id}>Email</label>
      <input
        id={id}
        type="email"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        aria-describedby={[hintId, error ? errorId : null].filter(Boolean).join(" ")}
        aria-invalid={Boolean(error)}
      />
      <p id={hintId}>We’ll never share your email.</p>
      {error ? (
        <p id={errorId} role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
```

## 5) State management for UI

- Local UI state: `useState`
- Complex transitions: `useReducer` (or a small state machine)
- Global app state: only if needed (context/store)

Pattern:

```ts
type ViewState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "ready" }
  | { status: "error"; message: string };
```

This avoids boolean soup.

## 6) Performance notes

- Avoid rendering huge lists without virtualization.
- Avoid expensive `filter/backdrop-filter` on large surfaces.
- Memoize only when it actually prevents work (don’t cargo-cult `memo`).

## 7) Motion

If using framer-motion, keep it subtle and make it obey reduced-motion. See:
- [../animations.md](../animations.md)
