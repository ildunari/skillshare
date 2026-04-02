# Vanilla HTML/CSS patterns (modern, maintainable)

Use this when implementing without a framework or when you want framework-agnostic styling rules.

## 1) Architecture: tokens → base → components → utilities

A simple structure:

```
styles/
  tokens.css      # CSS variables (colors/type/spacing/radii)
  base.css        # resets + element defaults
  layout.css      # Container, Stack, Grid, Section
  components.css  # buttons, cards, forms
```

Then import in order.

## 2) Use CSS layers (optional but helpful)

```css
@layer reset, tokens, base, layout, components, utilities;

@layer tokens {
  :root { --bg: #0b0f14; /* ... */ }
}

@layer base {
  body { background: var(--bg); color: var(--text); }
}
```

## 3) Layout primitives

### Container

```css
.Container {
  width: min(1120px, 100% - 2rem);
  margin-inline: auto;
}
```

### Stack (vertical rhythm)

```css
.Stack > * + * { margin-top: var(--s-4); }
.Stack--tight > * + * { margin-top: var(--s-2); }
```

### Grid (asymmetric by default)

```css
.Grid { display: grid; gap: var(--s-6); }

@media (min-width: 768px) {
  .Grid--split { grid-template-columns: 1.6fr 1fr; }
}
```

## 4) Responsive typography with clamp

```css
.HeroTitle {
  font-size: clamp(2.2rem, 4vw, 3.6rem);
  line-height: 1.1;
}
```

## 5) Buttons that feel good

```css
.Button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;

  min-height: 44px;
  padding: 0 1rem;
  border-radius: var(--radius);

  font-weight: 650;
  background: var(--accent);
  color: black;

  transition: transform 160ms ease, box-shadow 160ms ease;
  box-shadow: var(--shadow);
}

.Button:hover { transform: translateY(-1px); }
.Button:active { transform: translateY(1px); }

.Button:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 3px;
}
```

## 6) Forms

- Always show labels.
- Ensure focus is obvious.
- Make errors explicit and connected via `aria-describedby` (see [../accessibility.md](../accessibility.md)).

## 7) Container queries (optional, modern)

Use when a component’s layout depends on its container, not the viewport.

```css
.CardGrid {
  container-type: inline-size;
}

@container (min-width: 42rem) {
  .CardGrid { grid-template-columns: repeat(2, 1fr); }
}
```

## 8) Don’t reinvent complex widgets

For dialogs, comboboxes, date pickers: use an accessible library if possible. Hand-rolling is risky.
