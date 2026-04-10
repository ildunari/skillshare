# MCP App Component Patterns

Reusable UI component patterns extracted from the official ext-apps examples. All components use the host-injected CSS custom properties from `design-tokens.md`.

## Table of Contents

1. [Button](#button)
2. [Info Notice](#info-notice)
3. [Card / Panel](#card--panel)
4. [Form Inputs](#form-inputs)
5. [Slider Row](#slider-row)
6. [Header Bar](#header-bar)
7. [Section Title](#section-title)
8. [Data Display](#data-display)
9. [Layout Patterns](#layout-patterns)
10. [Responsive Patterns](#responsive-patterns)
11. [Hover and Interaction Patterns](#hover-and-interaction-patterns)

---

## Button

Primary action button. Uses the app accent color, not the host's semantic colors (buttons are app-branded).

```css
button {
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  border-radius: var(--border-radius-md);
  color: var(--color-text-on-accent);
  font-weight: var(--font-weight-bold);
  font-family: inherit;
  font-size: inherit;
  background-color: var(--color-accent);
  cursor: pointer;
  width: 100%;
}

button:hover {
  background-color: color-mix(in srgb, var(--color-accent) 85%, var(--color-background-inverse));
}

button:focus-visible {
  outline: calc(var(--border-width-regular) * 2) solid var(--color-ring-primary);
  outline-offset: var(--border-width-regular);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

The `color-mix()` hover pattern darkens the accent in light mode and lightens it in dark mode by mixing toward the inverse background. This eliminates the need for separate hover color tokens.

### Secondary / Ghost Button

```css
.button-secondary {
  padding: var(--spacing-sm) var(--spacing-md);
  border: var(--border-width-regular) solid var(--color-border-primary);
  border-radius: var(--border-radius-md);
  background: var(--color-background-secondary);
  color: var(--color-text-primary);
  cursor: pointer;
}

.button-secondary:hover {
  background: var(--color-background-tertiary);
}
```

## Info Notice

Informational banner with a leading emoji indicator.

```css
.notice {
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--color-text-info);
  text-align: center;
  font-style: italic;
  background-color: var(--color-background-info);
  border-radius: var(--border-radius-md);
}

.notice::before {
  content: "ℹ️ ";
  font-style: normal;
}
```

Variants for other semantic states:

```css
.notice-danger {
  color: var(--color-text-danger);
  background-color: var(--color-background-danger);
}
.notice-danger::before { content: "⚠️ "; }

.notice-success {
  color: var(--color-text-success);
  background-color: var(--color-background-success);
}
.notice-success::before { content: "✅ "; }

.notice-warning {
  color: var(--color-text-warning);
  background-color: var(--color-background-warning);
}
.notice-warning::before { content: "⚠️ "; }
```

## Card / Panel

Secondary surface container for grouping related content.

```css
.card {
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-background-secondary);
  border: var(--border-width-regular) solid var(--color-border-primary);
  border-radius: var(--border-radius-lg);
  transition: background-color 0.15s ease;
}

.card-highlighted {
  background: var(--color-background-tertiary);
}
```

## Form Inputs

All form inputs inherit font properties from the body to maintain consistent sizing.

```css
textarea,
input[type="text"],
input[type="number"],
input[type="email"],
select {
  display: block;
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: var(--border-width-regular) solid var(--color-border-primary);
  border-radius: var(--border-radius-md);
  background: var(--color-background-primary);
  color: var(--color-text-primary);
  font-family: inherit;
  font-size: inherit;
}

input:focus,
textarea:focus,
select:focus {
  outline: calc(var(--border-width-regular) * 2) solid var(--color-ring-primary);
  outline-offset: var(--border-width-regular);
  border-color: var(--color-ring-primary);
}

input::placeholder {
  color: var(--color-text-tertiary);
}
```

## Slider Row

Grid-based slider layout used in dashboard-style apps (budget allocators, scenario modelers).

```css
.slider-row {
  display: grid;
  grid-template-columns: 95px 50px minmax(60px, 1fr) 56px 46px;
  align-items: center;
  gap: 6px;
  padding: 5px 8px;
  border-radius: var(--border-radius-md);
  background: var(--color-background-secondary);
  transition: background-color 0.15s ease;
}

.slider-row.highlighted {
  background: var(--color-background-tertiary);
}

/* Responsive: narrower screens */
@media (max-width: 500px) {
  .slider-row {
    grid-template-columns: 85px 40px minmax(30px, 1fr) 48px 38px;
    gap: 4px;
    padding: 3px 4px;
  }
}
```

> **Note:** The grid column widths use hardcoded pixel values for precise dashboard layout control. This is a pragmatic exception to the token-based spacing system — grid tracks need exact sizing to align slider elements. For simpler layouts, prefer `var(--spacing-*)` tokens.

### Range Input Styling

```css
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: var(--color-border-primary);
  border-radius: var(--border-radius-full);
  flex: 1;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--color-ring-primary);
  cursor: pointer;
}
```

## Header Bar

Compact header with title and action controls, 40px fixed height.

```css
.header {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
  border-bottom: var(--border-width-regular) solid var(--color-border-primary);
  flex-shrink: 0;
}

.header-title {
  font-size: var(--font-text-sm-size);
  font-weight: var(--font-weight-semibold);
  margin: 0;
  white-space: nowrap;
}
```

## Section Title

Small uppercase label for grouped content sections.

```css
.section-title {
  font-size: 11px;
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-secondary);
  margin: 0 0 4px 0;
}
```

> **Note:** The 11px font size is smaller than the smallest token (`--font-text-xs-size` = 12px). This is intentional for compact dashboard labels. For standard UI, use `var(--font-text-xs-size)` instead.

## Data Display

Inline code/value display within text.

```css
code {
  font-family: var(--font-mono);
  font-size: 1em;
  padding: 2px 4px;
  background: var(--color-background-secondary);
  border-radius: var(--border-radius-xs);
}
```

## Layout Patterns

### Single-Column (Basic Tool)

```css
.main {
  width: 100%;
  max-width: 425px;
  box-sizing: border-box;
}

.main > * {
  margin-top: 0;
  margin-bottom: 0;
}

.main > * + * {
  margin-top: var(--spacing-lg);
}
```

### Dashboard (Full Width, Fixed Height)

```css
.app-container {
  display: flex;
  flex-direction: column;
  height: 600px;
  width: 100%;
  max-width: 100%;
  max-height: 100%;
  overflow: hidden;
  padding: 12px;
  gap: 8px;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  overflow: hidden;
}
```

### Flex Row (Label + Value)

```css
.row {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-xs);
}
```

## Responsive Patterns

Most MCP App iframes are already narrow. Use these breakpoints for very compact displays:

```css
@media (max-width: 500px) {
  .app-container {
    padding: 8px;
    gap: 6px;
  }

  .header-title {
    font-size: 16px;
  }

  /* Shrink font sizes */
  .slider-label {
    font-size: 12px;
  }
}
```

For apps that might render in wider contexts (VS Code panels, desktop sidebars):

```css
@media (min-width: 600px) {
  .app-container {
    max-width: 600px;
    margin: 0 auto;
  }
}
```

## Hover and Interaction Patterns

### Theme-Aware Hover

Use `color-mix()` for hover states that automatically adapt to light/dark:

```css
.interactive:hover {
  background-color: color-mix(
    in srgb,
    var(--color-background-primary) 90%,
    var(--color-background-inverse)
  );
}
```

### Focus-Visible Pattern

Standard focus ring for keyboard navigation:

```css
.interactive:focus-visible {
  outline: calc(var(--border-width-regular) * 2) solid var(--color-ring-primary);
  outline-offset: var(--border-width-regular);
}
```

### Smooth Transitions

Apply to elements that change on theme switch or interaction:

```css
.transitions {
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
}
```
