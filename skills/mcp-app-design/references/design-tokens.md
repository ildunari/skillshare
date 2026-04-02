# MCP App Design Tokens

Complete CSS custom property system for MCP App UIs. These values are the defaults from the official ext-apps `basic-host` example — actual values may differ per host (Claude.ai, VS Code, etc.), but the property names are standardized across all hosts.

## Table of Contents

1. [Background Colors](#background-colors)
2. [Text Colors](#text-colors)
3. [Border Colors](#border-colors)
4. [Ring Colors (Focus)](#ring-colors-focus)
5. [Typography — Families](#typography--families)
6. [Typography — Weights](#typography--weights)
7. [Typography — Text Sizes](#typography--text-sizes)
8. [Typography — Heading Sizes](#typography--heading-sizes)
9. [Typography — Line Heights](#typography--line-heights)
10. [Spacing](#spacing)
11. [Border Radius](#border-radius)
12. [Border Width](#border-width)
13. [Shadows](#shadows)
14. [Theme System](#theme-system)

---

## Background Colors

All background colors use `light-dark(light-value, dark-value)` for automatic theme adaptation.

| Variable | Light | Dark | Usage |
|---|---|---|---|
| `--color-background-primary` | `#ffffff` | `#1a1a1a` | Main page/app background |
| `--color-background-secondary` | `#f5f5f5` | `#2d2d2d` | Cards, panels, secondary surfaces |
| `--color-background-tertiary` | `#e5e5e5` | `#404040` | Hover states, highlighted rows |
| `--color-background-inverse` | `#1a1a1a` | `#ffffff` | Inverted surfaces (dark-on-light / light-on-dark) |
| `--color-background-ghost` | `rgba(255,255,255,0)` | `rgba(26,26,26,0)` | Transparent backgrounds that match the theme |
| `--color-background-info` | `#eff6ff` | `#1e3a5f` | Info banners, notices |
| `--color-background-danger` | `#fef2f2` | `#7f1d1d` | Error states, destructive action areas |
| `--color-background-success` | `#f0fdf4` | `#14532d` | Success states, confirmations |
| `--color-background-warning` | `#fefce8` | `#713f12` | Warning banners, caution areas |
| `--color-background-disabled` | `rgba(255,255,255,0.5)` | `rgba(26,26,26,0.5)` | Disabled elements |

## Text Colors

| Variable | Light | Dark | Usage |
|---|---|---|---|
| `--color-text-primary` | `#1f2937` | `#f3f4f6` | Body text, headings |
| `--color-text-secondary` | `#6b7280` | `#9ca3af` | Captions, labels, muted text |
| `--color-text-tertiary` | `#9ca3af` | `#6b7280` | Placeholder text, very muted |
| `--color-text-inverse` | `#f3f4f6` | `#1f2937` | Text on inverse backgrounds |
| `--color-text-ghost` | `rgba(107,114,128,0.5)` | `rgba(156,163,175,0.5)` | Ghost/watermark text |
| `--color-text-info` | `#1d4ed8` | `#60a5fa` | Info labels, links |
| `--color-text-danger` | `#b91c1c` | `#f87171` | Error messages |
| `--color-text-success` | `#15803d` | `#4ade80` | Success messages |
| `--color-text-warning` | `#a16207` | `#fbbf24` | Warning text |
| `--color-text-disabled` | `rgba(31,41,55,0.5)` | `rgba(243,244,246,0.5)` | Disabled text |

## Border Colors

| Variable | Light | Dark | Usage |
|---|---|---|---|
| `--color-border-primary` | `#e5e7eb` | `#404040` | Default borders (cards, inputs, dividers) |
| `--color-border-secondary` | `#d1d5db` | `#525252` | Stronger borders (active inputs, emphasized dividers) |
| `--color-border-tertiary` | `#f3f4f6` | `#374151` | Subtle borders (section separators) |
| `--color-border-inverse` | `rgba(255,255,255,0.3)` | `rgba(0,0,0,0.3)` | Borders on inverse surfaces |
| `--color-border-ghost` | `rgba(229,231,235,0)` | `rgba(64,64,64,0)` | Invisible borders (for layout consistency) |
| `--color-border-info` | `#93c5fd` | `#1e40af` | Info state borders |
| `--color-border-danger` | `#fca5a5` | `#991b1b` | Error state borders |
| `--color-border-success` | `#86efac` | `#166534` | Success state borders |
| `--color-border-warning` | `#fde047` | `#854d0e` | Warning state borders |
| `--color-border-disabled` | `rgba(229,231,235,0.5)` | `rgba(64,64,64,0.5)` | Disabled state borders |

## Ring Colors (Focus)

Used for focus outlines on interactive elements.

| Variable | Light | Dark | Usage |
|---|---|---|---|
| `--color-ring-primary` | `#3b82f6` | `#60a5fa` | Default focus ring (buttons, inputs) |
| `--color-ring-secondary` | `#6b7280` | `#9ca3af` | Secondary focus ring |
| `--color-ring-inverse` | `#ffffff` | `#1f2937` | Focus ring on inverse surfaces |
| `--color-ring-info` | `#2563eb` | `#3b82f6` | Info-context focus |
| `--color-ring-danger` | `#dc2626` | `#ef4444` | Danger-context focus |
| `--color-ring-success` | `#16a34a` | `#22c55e` | Success-context focus |
| `--color-ring-warning` | `#ca8a04` | `#eab308` | Warning-context focus |

## Typography — Families

| Variable | Value | Usage |
|---|---|---|
| `--font-sans` | `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` | All body text and UI elements |
| `--font-mono` | `ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', monospace` | Code, data values, technical content |

Note: The host may inject custom fonts via `applyHostFonts()`. Each host (Claude.ai, VS Code, etc.) has its own font stack that overrides these defaults — the exact fonts vary per host and may change over time.

## Typography — Weights

| Variable | Value | Usage |
|---|---|---|
| `--font-weight-normal` | `400` | Body text |
| `--font-weight-medium` | `500` | Emphasized labels, sub-headings |
| `--font-weight-semibold` | `600` | Section titles, important labels |
| `--font-weight-bold` | `700` | Headings, button text, strong emphasis |

## Typography — Text Sizes

| Variable | Size | Line Height Variable | Line Height |
|---|---|---|---|
| `--font-text-xs-size` | `0.75rem` (12px) | `--font-text-xs-line-height` | `1.4` |
| `--font-text-sm-size` | `0.875rem` (14px) | `--font-text-sm-line-height` | `1.4` |
| `--font-text-md-size` | `1rem` (16px) | `--font-text-md-line-height` | `1.5` |
| `--font-text-lg-size` | `1.125rem` (18px) | `--font-text-lg-line-height` | `1.5` |

## Typography — Heading Sizes

| Variable | Size | Line Height Variable | Line Height | HTML |
|---|---|---|---|---|
| `--font-heading-xs-size` | `0.75rem` (12px) | `--font-heading-xs-line-height` | `1.4` | — |
| `--font-heading-sm-size` | `0.875rem` (14px) | `--font-heading-sm-line-height` | `1.4` | `<h6>` |
| `--font-heading-md-size` | `1rem` (16px) | `--font-heading-md-line-height` | `1.4` | `<h5>` |
| `--font-heading-lg-size` | `1.25rem` (20px) | `--font-heading-lg-line-height` | `1.3` | `<h4>` |
| `--font-heading-xl-size` | `1.5rem` (24px) | `--font-heading-xl-line-height` | `1.25` | `<h3>` |
| `--font-heading-2xl-size` | `1.875rem` (30px) | `--font-heading-2xl-line-height` | `1.2` | `<h2>` |
| `--font-heading-3xl-size` | `2.25rem` (36px) | `--font-heading-3xl-line-height` | `1.1` | `<h1>` |

## Typography — Line Heights

Text line heights are slightly more generous than heading line heights because body text needs more breathing room for readability, while headings are tighter to feel more typographically cohesive.

## Spacing

Spacing is derived from the base text size rather than being a separate token set. This keeps spacing proportional to the typography scale.

| Variable | Calculation | Computed (at 16px base) |
|---|---|---|
| `--spacing-xs` | `calc(var(--spacing-unit) * 0.25)` | `4px` |
| `--spacing-sm` | `calc(var(--spacing-unit) * 0.5)` | `8px` |
| `--spacing-md` | `var(--spacing-unit)` | `16px` |
| `--spacing-lg` | `calc(var(--spacing-unit) * 1.5)` | `24px` |

Where `--spacing-unit` equals `var(--font-text-md-size)` (1rem / 16px).

## Border Radius

| Variable | Value | Usage |
|---|---|---|
| `--border-radius-xs` | `2px` | Subtle rounding (tags, badges) |
| `--border-radius-sm` | `4px` | Small elements (checkboxes, small buttons) |
| `--border-radius-md` | `6px` | Standard elements (buttons, inputs, cards) |
| `--border-radius-lg` | `8px` | Larger containers (panels, modals) |
| `--border-radius-xl` | `12px` | Prominent containers (hero cards, featured sections) |
| `--border-radius-full` | `9999px` | Pills, circular elements |

## Border Width

| Variable | Value |
|---|---|
| `--border-width-regular` | `1px` |

## Shadows

| Variable | Value | Usage |
|---|---|---|
| `--shadow-hairline` | `0 1px 2px 0 rgba(0,0,0,0.05)` | Barely visible lift (cards at rest) |
| `--shadow-sm` | `0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)` | Subtle elevation (buttons, small cards) |
| `--shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)` | Medium elevation (dropdowns, popovers) |
| `--shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)` | High elevation (modals, floating panels) |

## Theme System

### How theme switching works

1. The host pushes a theme (`"light"` or `"dark"`) to your app via `hostContext.theme`
2. Your app applies it with `applyDocumentTheme(theme)` which sets `data-theme` attribute and `color-scheme` property on `<html>`
3. CSS `light-dark()` values automatically resolve based on `color-scheme`
4. The host also pushes style variables via `hostContext.styles.variables` which override your CSS fallbacks

### CSS setup for theme support

```css
:root {
  color-scheme: light dark;
  /* Fallback values — host overrides these */
  --color-background-primary: light-dark(#ffffff, #1a1a1a);
  --color-text-primary: light-dark(#1f2937, #f3f4f6);
}

/* Smooth theme transitions */
html, body {
  transition: background-color 0.2s, color 0.2s;
}
```

### TypeScript setup for theme bridging

See `architecture.md` → "UI: Host Context and Theming" for the complete implementation. The three key functions:

| Function | Purpose |
|---|---|
| `applyDocumentTheme(theme)` | Sets `data-theme` attribute and `color-scheme` property on `<html>` |
| `applyHostStyleVariables(vars)` | Injects host CSS custom properties that override your `:root` fallbacks |
| `applyHostFonts(fontsCss)` | Applies host font stylesheet |

Wire all three into `onhostcontextchanged` and call them after `app.connect()`. For React apps, the `useHostStyles(app)` hook from `@modelcontextprotocol/ext-apps/react` handles all three automatically.
