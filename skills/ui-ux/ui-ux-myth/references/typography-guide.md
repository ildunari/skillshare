# Typography guide (distinctive, readable, implementable)

Typography is the fastest way to make a UI feel intentional (or generic). Use it decisively.

## 1) Avoid the default “SaaS font stack”

Unless the user explicitly requests a neutral corporate vibe, avoid default choices like:
- Inter
- Roboto
- Open Sans
- Lato
- Montserrat

Those fonts aren’t “bad” — they’re just the most common template signal.

## 2) Pick a typography direction (choose one)

### A) Technical / terminal
- Display: **Space Grotesk**, **Sora**, **Space Grotesk**
- Mono accent: **JetBrains Mono**, **IBM Plex Mono**, **Fira Code**

### B) Editorial / premium
- Display: **Fraunces**, **Playfair Display**, **Newsreader**
- Body: **Source Serif 4**, **Crimson Pro**, **Literata**
- Pair with a clean sans for UI chrome (buttons/nav): **IBM Plex Sans**, **Source Sans 3**

### C) Modern startup (but not generic)
- Display: **Clash Display**, **Cabinet Grotesk**, **Bricolage Grotesque**, **Satoshi**
- Body: **Familjen Grotesk**, **Epilogue**, **Source Sans 3**

## 3) Pairing rules that actually work

- High contrast pairings are memorable:
  - serif + geometric sans
  - display grotesk + mono accent
- Use **weight extremes**:
  - light (200–300) for large display
  - heavy (700–800) for key emphasis
- Make **size jumps dramatic**:
  - headings should be *obviously* headings (often 2.5–3x body size)

## 4) Implement a type scale (don’t improvise)

A practical scale (CSS variables):

```css
:root {
  --text-xs: 0.8125rem;
  --text-sm: 0.9375rem;
  --text-md: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.375rem;
  --text-2xl: 1.875rem;
  --text-3xl: 2.5rem;
  --text-4xl: 3.25rem;

  --leading-tight: 1.15;
  --leading-body: 1.6;
}
```

Then apply consistently.

## 5) Readability constraints

- Don’t go below **14px** for body text unless there’s a strong reason.
- Aim for comfortable line length for paragraphs (roughly 45–80 characters).
- Increase line-height for dense content.

## 6) Loading fonts (Google Fonts example)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link
  href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=JetBrains+Mono:wght@400;600&display=swap"
  rel="stylesheet"
/>
```

Then in CSS:

```css
:root {
  --font-display: "Space Grotesk", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}
```

Prefer `font-display: swap` (Google does this via `display=swap`) and use sensible fallbacks.

## 7) Tailwind mapping (if applicable)

If using Tailwind, map fonts to token names:

```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      fontFamily: {
        display: ["var(--font-display)"],
        mono: ["var(--font-mono)"],
      },
    },
  },
};
```

## 8) “One big win” typography move

If time is limited:
- Make the hero headline big and decisive (clamp + tight leading)
- Use mono only for small accents (labels, metadata), not for paragraphs

Example:

```css
.HeroTitle {
  font-family: var(--font-display);
  font-weight: 700;
  line-height: var(--leading-tight);
  font-size: clamp(2.2rem, 4vw, 3.6rem);
}

.MetaLabel {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
```
