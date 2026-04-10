# Tailwind patterns (tokens-first, not class soup)

Tailwind can ship fast, but it also makes it easy to produce generic UI. Use it intentionally.

## 1) Use CSS variables as the source of truth

Put tokens in `styles/tokens.css`:

```css
:root {
  --bg: #0b0f14;
  --surface: #0f172a;
  --text: #e5e7eb;
  --muted: #9ca3af;
  --accent: #facc15;
  --radius: 14px;
  --focus: color-mix(in oklab, var(--accent) 65%, white);
}
```

Then reference variables in Tailwind classes:

- `bg-[var(--bg)]`
- `text-[var(--text)]`
- `rounded-[var(--radius)]`

## 2) Extend theme for ergonomics (optional)

```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      borderRadius: {
        ui: "var(--radius)",
      },
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        text: "var(--text)",
        muted: "var(--muted)",
        accent: "var(--accent)",
        focus: "var(--focus)",
      },
    },
  },
};
```

Then use: `bg-bg text-text`.

## 3) Avoid “class strings as your design system”

### Extract repeated patterns

If you repeat a class list 3+ times, extract it.

Options:
- a small helper `cn()` + `variants` map
- `@layer components` in CSS
- a component wrapper

Example (CSS layer):

```css
@layer components {
  .ui-button {
    @apply inline-flex items-center justify-center gap-2 font-medium;
    @apply rounded-ui h-11 px-4;
    @apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2;
  }

  .ui-button-primary {
    @apply bg-accent text-black;
  }
}
```

## 4) Tailwind + typography

Don’t let everything be `text-base font-medium`.
Create real hierarchy (size jumps, weight contrast).

See:
- [../typography-guide.md](../typography-guide.md)

## 5) Responsiveness

Use content-driven breakpoints. A default pattern:

- Mobile: base
- Tablet: `md:`
- Desktop: `lg:`

Example:

```tsx
<div className="grid gap-6 md:grid-cols-[1.5fr_1fr]">
  <section>...</section>
  <aside className="md:sticky md:top-6">...</aside>
</div>
```

That asymmetry alone helps avoid template vibes.
