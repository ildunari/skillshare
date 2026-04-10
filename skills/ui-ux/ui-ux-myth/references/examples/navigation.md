# Navigation examples (usable + distinctive)

## Example A: Conventional top nav (left aligned) + mobile drawer

Principles:
- Keep nav conventional (Jakob’s Law).
- Mobile: drawer or sheet; close on Esc; trap focus if modal.

### HTML skeleton

```html
<a class="SkipLink" href="#main">Skip to content</a>

<header class="Header">
  <div class="Container Header__row">
    <a class="Brand" href="/">Acme</a>

    <nav class="Nav Nav--desktop" aria-label="Primary">
      <a href="/features">Features</a>
      <a href="/pricing">Pricing</a>
      <a href="/docs">Docs</a>
    </nav>

    <div class="Header__actions">
      <a class="Button Button--ghost" href="/login">Sign in</a>
      <a class="Button" href="/get-started">Get started</a>

      <button class="IconButton NavToggle" aria-label="Open menu" aria-expanded="false">
        ☰
      </button>
    </div>
  </div>
</header>

<main id="main">...</main>
```

### CSS (responsive)

```css
.Nav--desktop { display: none; }
.NavToggle { display: inline-flex; }

@media (min-width: 800px) {
  .Nav--desktop { display: flex; gap: 1.25rem; }
  .NavToggle { display: none; }
}
```

### Mobile drawer notes

If you implement a drawer:
- it’s effectively a dialog (focus trap + aria-modal)
- close on overlay click + Esc
- restore focus to the toggle button

See: [../references/accessibility.md](../references/accessibility.md)

---

## Example B: Bottom nav (mobile-first apps)

Best for 3–5 primary destinations.

Rules:
- icons + labels (not icons alone)
- current page indicated via `aria-current="page"`

```html
<nav class="BottomNav" aria-label="Primary">
  <a href="/home" aria-current="page">Home</a>
  <a href="/search">Search</a>
  <a href="/library">Library</a>
  <a href="/settings">Settings</a>
</nav>
```
