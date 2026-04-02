# Color systems (palette → tokens → theming)

Color should create *atmosphere*, not just “primary/secondary”.

## 1) Avoid the default palette traps

Common “template” signals:
- saturated SaaS blue (#0066FF vibes) on white
- purple gradients on white
- timid palettes with everything evenly weighted
- no dominant surface color; everything is “neutral”

## 2) Build a palette from roles, not swatches

Define **roles** first:

- Background (`--bg`)
- Primary surface (`--surface`)
- Secondary surface (`--surface-2`)
- Text (`--text`)
- Muted text (`--muted`)
- Accent (`--accent`)
- Border (`--border`)
- Focus (`--focus`)
- Status colors (`--success`, `--warning`, `--danger`)

Then pick actual values.

## 3) Example: “Terminal Noir” palette (dark, technical)

```css
:root {
  --bg: #070a0f;
  --surface: #0c1220;
  --surface-2: #101b33;

  --text: #e6e8ef;
  --muted: #a2a8ba;

  --accent: #f8d34b; /* warm sharp accent */
  --border: color-mix(in oklab, var(--text) 12%, transparent);
  --focus: color-mix(in oklab, var(--accent) 70%, white);

  --shadow: 0 14px 40px rgba(0,0,0,0.55);
}
```

## 4) Dark mode done right

- Avoid pure black `#000` and pure white `#fff` for large surfaces.
- Reduce contrast slightly for comfort while staying accessible.
- Use **colored shadows** or subtle tints to create depth.

## 5) Theme switching pattern (data attribute)

```html
<html data-theme="dark">
```

```css
:root { color-scheme: light dark; }

[data-theme="light"] {
  --bg: #fbfbf7;
  --surface: #ffffff;
  --surface-2: #f3f4f6;
  --text: #0b0f14;
  --muted: #475569;
  --accent: #0ea5e9;
  --shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
}
```

## 6) Background depth without generic blobs

### Layered gradients

```css
.PageBg {
  background:
    radial-gradient(800px 500px at 20% 10%, rgba(248, 211, 75, 0.12), transparent 60%),
    radial-gradient(900px 700px at 80% 40%, rgba(14, 165, 233, 0.10), transparent 60%),
    linear-gradient(180deg, var(--bg), color-mix(in oklab, var(--bg), black 12%));
}
```

### Subtle pattern (repeating lines)

```css
.Pattern {
  background-image:
    repeating-linear-gradient(
      45deg,
      rgba(255,255,255,0.04),
      rgba(255,255,255,0.04) 10px,
      transparent 10px,
      transparent 20px
    );
  mask-image: radial-gradient(circle at 30% 20%, black 0%, transparent 70%);
}
```

### Optional noise (small, cheap texture)

If you use noise, keep opacity very low and ensure it doesn’t reduce readability.

## 7) Contrast sanity checks (baseline)

- Text should generally meet **WCAG AA** (4.5:1 for normal text).
- UI components: 3:1 minimum for boundaries.

See [accessibility.md](accessibility.md) for testing guidance.

## 8) Tailwind usage (tokens-first)

If you use Tailwind, treat CSS variables as the truth and map Tailwind colors to them. See:
- [framework-patterns/tailwind.md](framework-patterns/tailwind.md)
