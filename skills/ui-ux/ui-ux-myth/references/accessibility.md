# Accessibility (WCAG AA by default)

This file is practical patterns you can implement directly.

## Baseline requirements (ship blockers)

- **Keyboard navigation:** everything interactive reachable and usable via keyboard
- **Focus visible:** clear `:focus-visible` styles
- **Labels:** inputs have programmatic labels
- **Contrast:** text and key controls meet WCAG AA
- **Reduced motion:** respect `prefers-reduced-motion`
- **Touch targets:** controls sized for touch (common guideline: ~44×44)

Useful references:
- W3C target size understanding (44×44): https://www.w3.org/WAI/WCAG21/Understanding/target-size.html
- Apple HIG touch target guidance: https://developer.apple.com/design/human-interface-guidelines/buttons/

## 1) Semantic structure first

Prefer:

- `<header>`, `<nav>`, `<main>`, `<footer>`
- `<button>` for actions
- `<a href>` for navigation
- `<label for>` or `aria-labelledby` for form controls

Avoid “div soup” with ARIA pasted on top.

## 2) Focus styles (don’t rely on browser default)

```css
:focus { outline: none; }

:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 3px;
}

[data-focus-ring="false"] :focus-visible {
  outline: none;
}
```

If you remove focus, you must replace it.

## 3) Touch targets

```css
button, a, input, select, textarea {
  min-height: 44px;
}

.IconButton {
  width: 44px;
  height: 44px;
}
```

If a design requires smaller visuals, keep the *hit area* large via padding.

## 4) Forms: labels, errors, help text

### Correct labeling

```html
<label for="email">Email</label>
<input id="email" name="email" type="email" autocomplete="email" />
```

### Error message wiring (aria-describedby)

```html
<label for="email">Email</label>
<input
  id="email"
  name="email"
  type="email"
  aria-describedby="email-hint email-error"
  aria-invalid="true"
/>

<p id="email-hint" class="Hint">We’ll never share your email.</p>
<p id="email-error" class="Error" role="alert">Please enter a valid email.</p>
```

Rules:
- Use `aria-invalid="true"` only when invalid.
- Use `role="alert"` sparingly; don’t scream on every keystroke.

## 5) Menus and dialogs (common traps)

### Dialog basics

- Trap focus within the dialog while open
- Restore focus to the trigger on close
- Close on `Esc`
- Close button must be keyboard reachable and labeled

If you can use a well-tested dialog primitive (Radix, Headless UI), do it. If not, implement carefully.

### Minimal dialog semantics

```html
<button aria-haspopup="dialog" aria-controls="settings-dialog">Open settings</button>

<div
  id="settings-dialog"
  role="dialog"
  aria-modal="true"
  aria-labelledby="settings-title"
  hidden
>
  <h2 id="settings-title">Settings</h2>
  ...
  <button type="button">Close</button>
</div>
```

You still need focus management in JS.

## 6) Navigation accessibility

- Provide a **skip link**.
- Use semantic list navigation.

```html
<a class="SkipLink" href="#main">Skip to content</a>

<nav aria-label="Primary">
  <ul>
    <li><a href="/features">Features</a></li>
    <li><a href="/pricing">Pricing</a></li>
  </ul>
</nav>

<main id="main">...</main>
```

## 7) Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## 8) Testing checklist (quick but real)

Manual:
- Tab through the full page
- Ensure focus order matches visual order
- Check that every icon-only button has an accessible name
- Test mobile: can you hit primary actions without precision tapping?

Automated (if available):
- Lighthouse a11y audit
- axe (browser extension or test runner)
