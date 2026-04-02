# Hero section examples (distinctive, implementable)

Use these as starting points. Don’t copy-paste blindly — adapt tokens and content.

---

## Example A: Terminal Noir hero (dark, technical)

### HTML

```html
<header class="Hero PageBg">
  <div class="Container Hero__grid">
    <div class="Hero__copy">
      <p class="MetaLabel">Realtime Observability</p>
      <h1 class="HeroTitle">See the system the way it actually behaves.</h1>
      <p class="HeroSubtitle">
        Trace requests, correlate logs, and ship fixes with confidence — without drowning in dashboards.
      </p>
      <div class="Hero__actions">
        <a class="Button" href="#get-started">Get started</a>
        <a class="Button Button--ghost" href="#demo">Watch demo</a>
      </div>
    </div>

    <aside class="Hero__panel">
      <div class="Panel">
        <div class="Panel__header">
          <span class="Badge">LIVE</span>
          <span class="Panel__meta">p95 latency</span>
        </div>
        <div class="Panel__value">187ms</div>
        <div class="Panel__sparkline" aria-hidden="true"></div>
      </div>
    </aside>
  </div>
</header>
```

### CSS

```css
:root {
  --bg: #070a0f;
  --surface: #0c1220;
  --surface-2: #101b33;
  --text: #e6e8ef;
  --muted: #a2a8ba;
  --accent: #f8d34b;
  --radius: 14px;
  --shadow: 0 14px 40px rgba(0,0,0,0.55);
  --focus: color-mix(in oklab, var(--accent) 70%, white);

  --s-2: 0.5rem;
  --s-4: 1rem;
  --s-6: 1.5rem;
  --s-8: 2rem;
}

.PageBg {
  background:
    radial-gradient(800px 500px at 20% 10%, rgba(248, 211, 75, 0.12), transparent 60%),
    radial-gradient(900px 700px at 80% 40%, rgba(14, 165, 233, 0.10), transparent 60%),
    linear-gradient(180deg, var(--bg), color-mix(in oklab, var(--bg), black 12%));
}

.Hero {
  color: var(--text);
  padding-block: clamp(3rem, 5vw, 5rem);
}

.Container {
  width: min(1100px, 100% - 2rem);
  margin-inline: auto;
}

.Hero__grid {
  display: grid;
  gap: var(--s-8);
}

@media (min-width: 900px) {
  .Hero__grid {
    grid-template-columns: 1.4fr 1fr;
    align-items: start;
  }
}

.MetaLabel {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.875rem;
  color: var(--muted);
}

.HeroTitle {
  font-size: clamp(2.2rem, 4vw, 3.6rem);
  line-height: 1.05;
  margin-top: var(--s-4);
}

.HeroSubtitle {
  margin-top: var(--s-4);
  font-size: 1.125rem;
  line-height: 1.6;
  color: color-mix(in oklab, var(--text), var(--muted) 45%);
  max-width: 55ch;
}

.Hero__actions {
  margin-top: var(--s-6);
  display: flex;
  flex-wrap: wrap;
  gap: var(--s-4);
}

.Button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 1rem;
  border-radius: var(--radius);
  background: var(--accent);
  color: #0b0f14;
  font-weight: 650;
  text-decoration: none;
  box-shadow: var(--shadow);
}

.Button:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 3px;
}

.Button--ghost {
  background: transparent;
  color: var(--text);
  box-shadow: none;
  border: 1px solid color-mix(in oklab, var(--text) 18%, transparent);
}

.Panel {
  border-radius: calc(var(--radius) + 6px);
  background: color-mix(in oklab, var(--surface), black 8%);
  border: 1px solid color-mix(in oklab, var(--text) 12%, transparent);
  padding: var(--s-6);
  box-shadow: var(--shadow);
}

.Badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  background: rgba(248, 211, 75, 0.16);
  border: 1px solid rgba(248, 211, 75, 0.28);
  color: var(--accent);
}
```

---

## Example B: Editorial hero (paper, serif display)

Signature move: serif display + generous whitespace + strong hierarchy.

Use tokens from [references/typography-guide.md](../references/typography-guide.md) and [references/color-systems.md](../references/color-systems.md).
