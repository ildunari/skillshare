# Theme Schema v2 — Production Design System Spec

> Every theme in the design-maestro skill must conform to this schema. A theme is not a mood board — it is an engineering specification that produces consistent, polished output when Claude reads it and builds an artifact. If a dimension is missing, Claude will improvise, and improvisation produces inconsistency.

---

## Schema Overview

A theme is organized into **10 sections**. Each section has required fields (must be specified) and optional fields (specified when relevant to the theme's identity). The sections are:

1. **Identity** — Name, philosophy, best-for, decision principle
2. **Color System** — Palette tokens with roles, opacity system, state color shifts
3. **Typography Matrix** — Per-role specs: family, size, weight, line-height, spacing, features
4. **Elevation System** — Shadow tokens by state, depth strategy, backdrop-filter
5. **Border System** — Base color, width scale, opacity scale, focus ring
6. **Component States** — Per-component state machines with transition specs
7. **Motion Map** — Component category → duration → easing pairings
8. **Layout Tokens** — Content width, spacing scale, density, breakpoint behavior
9. **Accessibility Tokens** — Focus ring, disabled state, selection, scrollbar, reduced-motion
10. **Overlays** — Popover, modal, dropdown, tooltip specs

Plus existing sections that remain: **Visual Style**, **Signature Animations**, **Dark/Light Mode Variant**, **Mobile Notes**, and **Implementation Checklist**.

---

## JSON Schema (Machine-Readable Reference)

This schema is for validation and AI-assisted theme generation. Theme markdown files are the human-readable expression of the same data.

```json
{
  "meta": {
    "name": "ThemeName",
    "tagline": "One-line poetic description",
    "bestFor": ["domain1", "domain2"],
    "mood": ["adjective1", "adjective2", "adjective3"],
    "density": "sparse | comfortable | moderate | dense | very-dense",
    "temperature": "cold | cool | neutral | warm | hot",
    "formality": "playful | casual | professional | formal | ceremonial",
    "depthStrategy": "borders-only | subtle-shadows | layered-shadows | surface-shifts | glow",
    "decisionPrinciple": "When in doubt, ask: ..."
  },

  "color": {
    "space": "oklch | hsl",
    "neutrals": {
      "page":       { "value": "...", "hex": "#...", "role": "Deepest background / page canvas" },
      "bg":         { "value": "...", "hex": "#...", "role": "Primary surface background" },
      "surface":    { "value": "...", "hex": "#...", "role": "Elevated cards, inputs, popovers" },
      "recessed":   { "value": "...", "hex": "#...", "role": "Recessed areas, code blocks" },
      "active":     { "value": "...", "hex": "#...", "role": "Active/pressed items, user bubbles" }
    },
    "text": {
      "primary":    { "value": "...", "hex": "#...", "role": "Headings, body text, brightest" },
      "secondary":  { "value": "...", "hex": "#...", "role": "Sidebar items, secondary labels" },
      "muted":      { "value": "...", "hex": "#...", "role": "Placeholders, timestamps, metadata" },
      "onAccent":   { "value": "...", "hex": "#...", "role": "Text on accent-colored backgrounds" }
    },
    "accents": {
      "primary":    { "value": "...", "hex": "#...", "role": "Brand accent, primary CTA" },
      "secondary":  { "value": "...", "hex": "#...", "role": "Optional secondary accent" }
    },
    "semantics": {
      "success":    { "value": "...", "hex": "#..." },
      "warning":    { "value": "...", "hex": "#..." },
      "danger":     { "value": "...", "hex": "#..." },
      "info":       { "value": "...", "hex": "#..." }
    },
    "border": {
      "base":       { "value": "...", "hex": "#...", "role": "Base border color (used at variable opacity)" }
    },
    "fixed": {
      "alwaysBlack": "#000000",
      "alwaysWhite": "#ffffff"
    },
    "special": {
      "inlineCode":  { "hex": "#...", "role": "Code text color within prose" },
      "toggleActive": { "hex": "#...", "role": "Toggle/switch active track color" },
      "selection":    { "hex": "#...", "role": "::selection background" }
    },
    "opacitySystem": {
      "description": "How the theme uses opacity on the base border color for different contexts",
      "subtle":   0.15,
      "card":     0.25,
      "hover":    0.30,
      "focus":    0.40
    }
  },

  "typography": {
    "families": {
      "sans":  { "name": "...", "fallback": "system-ui, sans-serif", "googleFontsUrl": "..." },
      "serif": { "name": "...", "fallback": "Georgia, serif", "googleFontsUrl": "..." },
      "mono":  { "name": "...", "fallback": "ui-monospace, monospace", "googleFontsUrl": "..." }
    },
    "roles": {
      "display": {
        "family": "serif | sans | mono",
        "size": "38px",
        "weight": 290,
        "lineHeight": "1.2",
        "letterSpacing": "-0.02em",
        "features": ["opsz 48"],
        "usage": "Hero greetings, page titles"
      },
      "heading": {
        "family": "serif | sans",
        "size": "24px",
        "weight": 460,
        "lineHeight": "1.3",
        "letterSpacing": "normal",
        "usage": "Section titles, settings headers"
      },
      "body": {
        "family": "sans | serif",
        "size": "16px",
        "weight": 400,
        "lineHeight": "1.5",
        "letterSpacing": "normal",
        "usage": "Primary reading text, UI body"
      },
      "bodySmall": {
        "family": "sans",
        "size": "14px",
        "weight": 400,
        "lineHeight": "1.4",
        "letterSpacing": "normal",
        "usage": "Sidebar items, form labels, secondary UI text"
      },
      "button": {
        "family": "sans",
        "size": "14px",
        "weight": 460,
        "lineHeight": "1.4",
        "letterSpacing": "normal",
        "usage": "Button labels, emphasized small UI text"
      },
      "input": {
        "family": "sans",
        "size": "14px",
        "weight": 430,
        "lineHeight": "1.4",
        "usage": "Form input text"
      },
      "label": {
        "family": "sans",
        "size": "12px",
        "weight": 400,
        "lineHeight": "1.33",
        "letterSpacing": "0.02em",
        "textTransform": "none | uppercase",
        "usage": "Section labels, metadata, timestamps"
      },
      "code": {
        "family": "mono",
        "size": "0.9em",
        "weight": 360,
        "lineHeight": "1.5",
        "usage": "Inline code, code blocks, data values"
      },
      "caption": {
        "family": "sans",
        "size": "12px",
        "weight": 400,
        "lineHeight": "1.33",
        "usage": "Disclaimers, footnotes, bottom-of-page text"
      }
    },
    "fontSmoothing": "antialiased",
    "textWrap": "balance | pretty | auto"
  },

  "elevation": {
    "strategy": "borders-only | subtle-shadows | layered-shadows | surface-shifts | glow",
    "shadows": {
      "sm":          "0 1px 2px rgba(0,0,0,0.05)",
      "md":          "0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)",
      "input":       "0 4px 20px hsl(var(--black)/3.5%), 0 0 0 0.5px hsl(var(--border)/0.15)",
      "inputHover":  "0 4px 20px hsl(var(--black)/3.5%), 0 0 0 0.5px hsl(var(--border)/0.30)",
      "inputFocus":  "0 4px 20px hsl(var(--black)/7.5%), 0 0 0 0.5px hsl(var(--border)/0.30)",
      "popover":     "0 2px 8px hsl(var(--black)/24%)",
      "none":        "none"
    },
    "surfaces": [
      { "name": "page",     "bg": "neutrals.bg",      "shadow": "none",  "usage": "Main page, sidebar" },
      { "name": "card",     "bg": "neutrals.surface",  "shadow": "input", "usage": "Input card, menus, form inputs" },
      { "name": "recessed", "bg": "neutrals.recessed",  "shadow": "none",  "usage": "Code blocks, inset areas" },
      { "name": "active",   "bg": "neutrals.active",   "shadow": "none",  "usage": "Active item, user bubble" },
      { "name": "overlay",  "bg": "neutrals.surface",  "shadow": "popover", "usage": "Popovers, dropdowns" }
    ],
    "backdropBlur": {
      "popover": "24px",
      "modal": "12px",
      "none": "0px"
    },
    "separationRecipe": "How the theme achieves visual separation between surfaces — e.g. 'tint-step + subtle composite shadow, no visible dividers' or 'borders-only, no shadows' or 'layered glow on dark canvas'"
  },

  "borders": {
    "baseColor": "color.border.base",
    "widths": {
      "hairline": "0.5px",
      "default":  "1px",
      "medium":   "1.5px",
      "heavy":    "2px"
    },
    "opacityScale": {
      "subtle":  0.15,
      "card":    0.25,
      "hover":   0.30,
      "focus":   0.40
    },
    "patterns": {
      "subtle":     "0.5px solid border-base / subtle-opacity",
      "card":       "0.5px solid border-base / card-opacity",
      "hover":      "0.5px solid border-base / hover-opacity",
      "input":      "1px solid border-base / subtle-opacity",
      "inputHover": "1px solid border-base / hover-opacity"
    },
    "focusRing": {
      "color":  "rgba(116, 171, 226, 0.56)",
      "width":  "2px",
      "style":  "solid",
      "offset": "2px"
    }
  },

  "radius": {
    "none": "0px",
    "sm":   "4px",
    "md":   "6px",
    "lg":   "8px",
    "xl":   "12px",
    "2xl":  "20px",
    "input": "9.6px",
    "full": "9999px"
  },

  "components": {
    "button": {
      "primary": {
        "rest":     { "bg": "transparent", "border": "card", "color": "text.primary", "radius": "md", "height": "32px", "padding": "0 12px", "fontSize": "button", "shadow": "none" },
        "hover":    { "bg": "neutrals.recessed", "border": "hover", "color": "text.primary" },
        "active":   { "transform": "scale(0.97)", "shadow": "none" },
        "focus":    { "outline": "focusRing" },
        "disabled": { "opacity": 0.5, "pointerEvents": "none", "shadow": "none" },
        "transition": { "properties": "color, background, border-color", "duration": "100ms", "easing": "default" }
      },
      "ghost": {
        "rest":     { "bg": "transparent", "border": "none", "color": "text.secondary", "radius": "md", "size": "32px" },
        "hover":    { "bg": "neutrals.recessed", "color": "text.primary" },
        "transition": { "duration": "300ms", "easing": "out-quart" }
      }
    },
    "input": {
      "text": {
        "rest":     { "bg": "neutrals.surface", "border": "input", "radius": "input", "height": "44px", "padding": "0 12px", "fontSize": "input", "color": "text.primary", "placeholder": "text.muted", "caretColor": "text.primary" },
        "hover":    { "border": "inputHover" },
        "focus":    { "outline": "focusRing" },
        "transition": { "properties": "border-color", "duration": "150ms", "easing": "default" }
      },
      "chatCard": {
        "rest":     { "bg": "neutrals.surface", "radius": "2xl", "border": "transparent", "shadow": "input" },
        "hover":    { "shadow": "inputHover" },
        "focus":    { "shadow": "inputFocus" },
        "transition": { "properties": "all", "duration": "200ms", "easing": "default" }
      }
    },
    "card": {
      "rest":       { "bg": "neutrals.surface", "border": "card", "radius": "lg", "shadow": "sm" },
      "hover":      { "border": "hover", "shadow": "md" },
      "transition": { "properties": "border-color, box-shadow", "duration": "150ms", "easing": "default" }
    },
    "sidebarItem": {
      "rest":       { "bg": "transparent", "color": "text.secondary", "radius": "md", "height": "32px", "padding": "6px 16px", "fontSize": "bodySmall" },
      "hover":      { "bg": "neutrals.recessed", "color": "text.primary" },
      "active":     { "bg": "neutrals.active", "color": "text.primary" },
      "activePress": { "transform": "scale(0.985)" },
      "transition": { "properties": "color, background, border-color", "duration": "75ms", "easing": "out-quart" }
    },
    "chip": {
      "rest":       { "bg": "neutrals.bg", "border": "subtle", "radius": "lg", "height": "32px", "padding": "0 10px", "fontSize": "bodySmall", "color": "text.secondary" },
      "hover":      { "bg": "neutrals.active", "border": "neutrals.active", "color": "text.primary" },
      "activePress": { "transform": "scale(0.995)" },
      "transition": { "duration": "150ms", "easing": "default" }
    },
    "toggle": {
      "track":      { "width": "36px", "height": "20px", "radius": "full" },
      "trackOff":   { "bg": "neutrals.active" },
      "trackOn":    { "bg": "special.toggleActive" },
      "ring":       { "width": "0.5px", "color": "border-base / hover-opacity" },
      "ringHover":  { "width": "1px" },
      "transition": { "duration": "150ms", "easing": "default" }
    },
    "popover": {
      "container":  { "bg": "neutrals.surface", "border": "hover", "radius": "xl", "shadow": "popover", "backdropBlur": "popover", "padding": "6px", "minWidth": "192px", "maxWidth": "320px", "zIndex": 50 },
      "item":       { "padding": "6px 8px", "radius": "lg", "height": "32px", "fontSize": "bodySmall", "color": "text.secondary" },
      "itemHover":  { "bg": "neutrals.recessed", "color": "text.primary" },
      "transition": { "duration": "75ms", "easing": "default" }
    },
    "tooltip": {
      "bg": "neutrals.active | neutrals.surface",
      "color": "text.primary",
      "fontSize": "label",
      "radius": "sm | md",
      "padding": "4px 8px",
      "shadow": "popover | none"
    },
    "userBubble": {
      "bg": "neutrals.active",
      "radius": "xl",
      "padding": "10px 16px",
      "maxWidth": "85% | 75ch",
      "color": "text.primary",
      "alignment": "right"
    }
  },

  "motion": {
    "easings": {
      "default":   "cubic-bezier(0.4, 0, 0.2, 1)",
      "out-quart": "cubic-bezier(0.165, 0.85, 0.45, 1)",
      "out-expo":  "cubic-bezier(0.19, 1, 0.22, 1)",
      "spring":    "Describe spring params if used: stiffness, damping"
    },
    "durations": {
      "flash":    "35ms",
      "fast":     "75ms",
      "normal":   "150ms",
      "medium":   "200ms",
      "slow":     "300ms",
      "reveal":   "500ms"
    },
    "map": [
      { "component": "Sidebar item bg/color",    "duration": "fast",   "easing": "out-quart" },
      { "component": "Button hover",             "duration": "normal", "easing": "default" },
      { "component": "Toggle/chip/general",      "duration": "normal", "easing": "default" },
      { "component": "Input card shadow",        "duration": "medium", "easing": "default" },
      { "component": "Ghost icon buttons",       "duration": "slow",   "easing": "out-quart" },
      { "component": "Panel open/close",         "duration": "reveal", "easing": "out-expo" },
      { "component": "Hero/page entry",          "duration": "slow",   "easing": "out-quart" }
    ],
    "activePress": {
      "nav":    "scale(0.985)",
      "chip":   "scale(0.995)",
      "button": "scale(0.97)",
      "tab":    "scale(0.95)"
    },
    "reducedMotion": {
      "strategy": "instant | fade-only | reduced-distance",
      "disableAmbient": true,
      "disableParallax": true
    }
  },

  "layout": {
    "unit": 4,
    "spacingScale": [4, 6, 8, 10, 12, 16, 28, 32],
    "contentMaxWidth": "768px",
    "narrowMaxWidth": "672px",
    "sidebarWidth": "288px",
    "headerHeight": "48px",
    "density": "sparse | comfortable | moderate | dense | very-dense",
    "breakpoints": {
      "sm": "640px",
      "md": "768px",
      "lg": "1024px"
    },
    "responsiveNotes": "Description of how the layout adapts: what collapses, what reflows, what hides"
  },

  "accessibility": {
    "focusRing": {
      "color": "rgba(116, 171, 226, 0.56)",
      "width": "2px",
      "style": "solid",
      "offset": "2px"
    },
    "disabled": {
      "opacity": 0.5,
      "pointerEvents": "none",
      "shadow": "none",
      "cursor": "not-allowed"
    },
    "selection": {
      "bg": "accent.primary / 0.2",
      "color": "text.primary"
    },
    "scrollbar": {
      "width": "thin",
      "thumbColor": "border-base / 0.35",
      "trackColor": "transparent"
    },
    "minTouchTarget": "44px",
    "contrastMinimum": "WCAG AA (4.5:1 text, 3:1 large text)"
  },

  "material": {
    "grain": "none | subtle (1-2%) | moderate (3-5%)",
    "grainTechnique": "feTurbulence | noise texture | none",
    "gloss": "matte | soft-sheen | gloss",
    "blendMode": "normal | multiply | soft-light | screen",
    "shaderBg": false
  },

  "dataviz": {
    "categorical": "palette of N colors at equal perceptual weight",
    "sequential": "single-hue ramp",
    "diverging": "two-hue ramp",
    "grid": "low-ink | visible | exposed",
    "maxHuesPerChart": 2,
    "philosophy": "smooth | quantized | annotated"
  },

  "darkModeVariant": {
    "isNativelyDark": false,
    "palette": { "... swapped tokens ..." },
    "rules": "Describe what changes: surfaces lighten, accents shift, borders darken, shadows become glows, etc."
  },

  "mobile": {
    "disableEffects": ["list of effects to disable on mobile"],
    "adjustments": ["list of sizing/spacing changes"],
    "performanceNotes": "Key perf considerations for this theme"
  }
}
```

---

## Theme Markdown File Anatomy (Human-Readable)

Every theme `.md` file must include these sections in order. This is the template for writing new themes and upgrading existing ones.

```markdown
## N. Theme Name

> One-line tagline

**Best for:** domain1, domain2, domain3

---

### Identity & Philosophy
- What world does this theme live in?
- What is the core visual tension or identity?
- Decision principle: "When in doubt, ask: ..."
- What this theme is NOT (anti-patterns specific to this theme)

### Color System

#### Palette

| Token | Name | Hex | OKLCH | Role |
|---|---|---|---|---|
| page | ... | #... | L=... C=... h=... | Deepest background |
| bg | ... | #... | L=... C=... h=... | Primary surface |
| surface | ... | #... | L=... C=... h=... | Cards, inputs, elevated |
| recessed | ... | #... | L=... C=... h=... | Code blocks, inset |
| active | ... | #... | L=... C=... h=... | Active/pressed states |
| text-primary | ... | #... | ... | Headings, body |
| text-secondary | ... | #... | ... | Secondary labels |
| text-muted | ... | #... | ... | Placeholders, meta |
| border-base | ... | #... | ... | Used at variable opacity |
| accent-primary | ... | #... | ... | Brand/CTA |
| success | ... | #... | ... | Positive states |
| warning | ... | #... | ... | Caution states |
| danger | ... | #... | ... | Error states |

#### Opacity System
- Borders: base color at `15%` subtle, `25%` card, `30%` hover, `40%` focus
- (Or describe the theme's specific opacity approach)

#### Color Rules
- (Theme-specific color constraints, e.g. "Red is earned", "No gradients", etc.)

### Typography Matrix

| Role | Family | Size | Weight | Line-height | Spacing | Features | Usage |
|---|---|---|---|---|---|---|---|
| Display | serif | 38px | 290 | 1.2 | -0.02em | opsz 48 | Hero titles |
| Heading | serif | 24px | 460 | 1.3 | normal | | Section titles |
| Body | sans | 16px | 400 | 1.5 | normal | | Primary text |
| Body Small | sans | 14px | 400 | 1.4 | normal | | Sidebar, labels |
| Button | sans | 14px | 460 | 1.4 | normal | | Button text |
| Input | sans | 14px | 430 | 1.4 | normal | | Form fields |
| Label | sans | 12px | 400 | 1.33 | 0.02em | | Metadata |
| Code | mono | 0.9em | 360 | 1.5 | normal | | Inline code |
| Caption | sans | 12px | 400 | 1.33 | normal | | Disclaimers |

#### Font Loading
```html
<link href="..." rel="stylesheet">
```

### Elevation System

**Strategy:** (borders-only | subtle-shadows | layered-shadows | surface-shifts | glow)

#### Surface Hierarchy

| Surface | Background | Shadow | Usage |
|---|---|---|---|
| page | bg | none | Main page |
| card | surface | shadow-input | Cards, inputs |
| recessed | recessed | none | Code blocks |
| active | active | none | Active items |
| overlay | surface | shadow-popover | Popovers |

#### Shadow Tokens

| Token | Value | Usage |
|---|---|---|
| shadow-sm | ... | Small elements |
| shadow-input | ... | Input card rest |
| shadow-input-hover | ... | Input card hover |
| shadow-input-focus | ... | Input card focus |
| shadow-popover | ... | Menus, dropdowns |

#### Separation Recipe
(How the theme achieves visual separation — e.g. "tint-step + composite shadow, no dividers")

### Border System

#### Widths and Patterns

| Pattern | Width | Opacity | Usage |
|---|---|---|---|
| subtle | 0.5px | 15% | Sidebar edges, hairlines |
| card | 0.5px | 25% | Card borders |
| hover | 0.5px | 30% | Hover/focus states |
| input | 1px | 15% | Form input borders |
| input-hover | 1px | 30% | Input hover |

#### Focus Ring
- Color: `rgba(116, 171, 226, 0.56)`
- Width: 2px solid
- Offset: 2px

### Component States

#### Buttons (Primary)
| State | Properties |
|---|---|
| Rest | bg transparent, border card, color text-primary, radius md, h 32px |
| Hover | bg recessed, border hover |
| Active | scale(0.97) |
| Focus | focus ring |
| Disabled | opacity 0.5, pointer-events none |
| Transition | color/bg/border 100ms default easing |

#### Buttons (Ghost/Icon)
(Same table format)

#### Text Input
(Same table format — rest/hover/focus with border and shadow changes)

#### Cards
(Same table format — rest/hover with border and shadow escalation)

#### Sidebar Items
(Same table format — rest/hover/active with bg and color changes)

#### Chips
(Same table format)

#### Toggle/Switch
(Track dimensions, on/off colors, ring behavior, transition)

### Motion Map

#### Easings

| Name | Value | Character |
|---|---|---|
| default | cubic-bezier(0.4, 0, 0.2, 1) | Standard ease-in-out |
| out-quart | cubic-bezier(0.165, 0.85, 0.45, 1) | Snappy deceleration |
| out-expo | cubic-bezier(0.19, 1, 0.22, 1) | Smooth open/close |

#### Duration × Easing × Component

| Component | Duration | Easing | Notes |
|---|---|---|---|
| Sidebar item | 75ms | out-quart | Color and bg only |
| Button hover | 100ms | default | |
| Toggle/chip | 150ms | default | |
| Input card | 200ms | default | All properties |
| Ghost icon | 300ms | out-quart | |
| Panel open/close | 500ms | out-expo | |

#### Active Press Scale

| Element | Scale | Notes |
|---|---|---|
| Nav items | 0.985 | Subtle |
| Chips | 0.995 | Barely perceptible |
| Buttons | 0.97 | Standard |
| Tabs | 0.95 | Pronounced |

### Overlays

#### Popover/Dropdown
- bg: surface token
- backdrop-filter: blur(24px)
- border: 0.5px at hover opacity
- radius: xl (12px)
- shadow: popover shadow token
- padding: 6px
- z-index: 50
- Menu item: 6px 8px padding, radius lg, 32px height
- Menu item hover: bg recessed, color text-primary
- Transition: 75ms default

#### Modal
- Overlay bg: black at 50% opacity
- backdrop-filter: blur(12px)
- Content: surface bg, popover shadow, xl radius
- Entry: fade + scale(0.95→1), 200ms out-expo

#### Tooltip
- bg: active surface
- color: text-primary
- font: label size
- radius: sm
- padding: 4px 8px
- No arrow (or specify arrow style)

### Layout Tokens

| Token | Value | Usage |
|---|---|---|
| Content max-width | 768px | Main content column |
| Narrow max-width | 672px | Landing/focused content |
| Sidebar width | 288px | Fixed sidebar |
| Header height | 48px | Top bar |
| Spacing unit | 4px | Base multiplier |

#### Spacing Scale
4, 6, 8, 10, 12, 16, 28, 32px

#### Density
(sparse | comfortable | moderate | dense | very-dense)

#### Responsive Notes
(What collapses at sm/md/lg, what reflows, density changes on mobile)

### Accessibility Tokens

| Token | Value |
|---|---|
| Focus ring | rgba(116, 171, 226, 0.56), 2px solid, 2px offset |
| Disabled | opacity 0.5, pointer-events none, cursor not-allowed |
| Selection bg | accent-primary at 20% |
| Scrollbar width | thin |
| Scrollbar thumb | border-base at 35% |
| Scrollbar track | transparent |
| Min touch target | 44px |
| Contrast standard | WCAG AA |

### Visual Style
(Theme-specific rendering philosophy — grain, texture, compositing, blend modes.
This is where the theme's artistic identity lives. Keep it.)

### Signature Animations
(3–5 theme-specific animations. Keep these — they're the theme's personality.
Now each should reference the motion map's easing/duration tokens.)

### Dark Mode Variant (or Light Mode Variant)
(Complete palette swap table + rules for what changes)

### Mobile Notes
(Effects to disable, sizing adjustments, performance considerations)

### Implementation Checklist
- [ ] Fonts loaded
- [ ] CSS custom properties defined
- [ ] Border-radius applied correctly
- [ ] Shadow tokens applied per state
- [ ] Border opacity system implemented
- [ ] Focus ring on all interactive elements
- [ ] prefers-reduced-motion media query present
- [ ] Scrollbar styled
- [ ] Touch targets ≥ 44px
- [ ] State transitions match motion map
```

---

## Adapting the Schema Per Theme

Not every theme uses every field identically. The schema is the **maximum spec** — themes adapt it:

- **Themes with no shadows** (e.g., Monochrome Terminal): Set all shadow tokens to `none`. The `elevation.strategy` is `borders-only`. The component states still define border changes on hover/focus, just no shadow escalation.
- **Dark-native themes** (e.g., Abyssal Glow): The `darkModeVariant` section becomes `lightModeVariant`. The glow rendering system gets documented in the elevation section.
- **Themes with no border-radius** (e.g., Pixel Grid): Set all radius tokens to `0px`. Document this in the implementation checklist as a global override.
- **Themes with unique components** (e.g., Pixel Grid's mosaic bars, step blocks): Add a `### Theme-Specific Components` section after the standard components.

The rule: **every theme covers every section**, even if the answer is "none" or "not applicable." Explicit "none" is better than missing — it prevents Claude from improvising.

---

## Migration Guide: Upgrading a 4K Theme to Schema v2

For each existing theme file (~60 lines), the upgrade process:

1. **Keep:** Identity, Color Palette (expand with role tokens), Typography (expand to full matrix), Visual Style, Signature Animations, Dark Mode, Mobile Notes
2. **Add:** Elevation System, Border System, Component States, Motion Map, Layout Tokens, Accessibility Tokens, Overlays, Implementation Checklist
3. **Expand:** Color palette from 8 entries → 13+ with opacity system. Typography from 3 families → 9 role specs. Animation from 2 timing values → full duration×easing map.

Expected size per theme after upgrade: **12–20K** (from ~4K). The 21-theme roster at full depth: **~250–400K total** (from ~180K for 32 shallow themes). More content, fewer files, dramatically better output quality.
