## 2. Typography & design token systems

### 2.1 What separates "default dev type" from designed type

Most developer typography fails for predictable reasons: no typographic hierarchy (everything 14–16px with random bolding), uncontrolled line length, untuned line-height and spacing, numbers not treated as numbers (no tabular numerals, poor table alignment), and fallback fonts that shift layout.

Professional systems feel designed because they handle hierarchy (scale + weight + spacing), rhythm (consistent vertical metrics), optical correctness (size/weight changes that *look* consistent), and content modes (reading vs scanning vs dense data).

#### Micro-typography: the details that matter

These are the specific adjustments that distinguish professional work:

- **Letter-spacing (tracking):** Large type requires tighter tracking (negative values, e.g., `-0.02em`) to hold word shapes together optically. Uppercase text requires looser spacing (e.g., `0.05em`) to improve legibility — default spacing on caps looks suffocated.
- **Line-height (leading):** Must be inversely proportional to font size. Headers need tight leading (1.1–1.2); body text needs breathing room (1.5–1.6). Applying 1.5 to everything looks amateurish at display sizes.
- **Color texture:** Professional systems rarely use pure black (#000000) on pure white. Dark greys (#1A1A1A) or desaturated brand colors (very dark slate blue) reduce eye strain and halation effects.
- **Numeric treatment:** Use `font-feature-settings: 'tnum'` for tabular numerals in tables and dashboards. Ensure consistent glyph height and alignment rules.

### 2.2 Type pairing: beyond "sans + serif"

Professional pairing follows role logic, not clichés:

- **Text face:** Optimized for long reading, high legibility, high x-height.
- **Display/brand face:** Carries personality in headings, hero sections, labels.
- **Data face (optional):** Numeric clarity — often mono or a UI sans with tabular numerals.

What makes pairings feel sophisticated:

- **X-height synchronization:** When mixing typefaces, disparate x-heights create visual vibration. Professional practitioners match x-heights optically, sometimes adjusting `font-size` of the secondary face rather than matching em-box height.
- **Intentional contrast axes:** If two fonts are too similar (two geometric sans-serifs), the interface feels like a mistake. Pair on distinct contrast axes — geometric vs humanist structure, ultra-bold display vs neutral book-weight body, "severe" mechanical headers vs "friendly" rounded body.
- **Shared underlying DNA** (similar stroke contrast or letter skeleton) *or* a clearly deliberate "opposites" pairing — never an ambiguous middle ground.

**Reference:** Practical Typography (Butterick): https://practicaltypography.com/

### 2.3 Variable fonts and optical sizing

Variable fonts treat typography as a continuous design space rather than a handful of static files. Key axes: `wght` (weight), `wdth` (width), `slnt`/`ital` (slant/italic), and critically, `opsz` (optical size).

**Optical sizing** reproduces what metal type designers did historically: small sizes get thicker strokes and wider apertures for legibility; large sizes get delicate strokes and tight spacing for elegance. With `font-optical-sizing: auto`, a font will automatically thicken thin lines at 12px (so they don't disappear on low-contrast screens) and refine them at 60px (removing the "clunky" feel of scaled-up body text). State-of-the-art systems in 2025 map `opsz` values directly to fluid font-size tokens so optical weight adjusts in real-time as headlines scale from mobile to desktop.

**Font metric stabilization:** `font-size-adjust` keeps x-height consistent between primary and fallback fonts, reducing layout shift when web fonts load.

**References:**
- MDN font-optical-sizing: https://developer.mozilla.org/en-US/docs/Web/CSS/font-optical-sizing
- web.dev Variable Fonts: https://web.dev/articles/variable-fonts
- web.dev font-size-adjust: https://web.dev/blog/font-size-adjust

### 2.4 Fluid typography and modular scales

A theme type system needs a ratio (e.g., 1.125–1.333 depending on content density), consistent line-height rules, and spacing that respects vertical rhythm. The historical approach used fixed sizes at fixed breakpoints. The modern approach uses **fluid scales** via CSS `clamp()`.

**The Utopia model:** Define a scale ratio for mobile (e.g., Minor Third, 1.2) and a ratio for desktop (e.g., Perfect Fourth, 1.333). Using `clamp()`, the browser interpolates between them based on viewport width. A heading becomes `clamp(1.75rem, 1.5rem + 1.25vw, 2.5rem)`, scaling seamlessly without breakpoint jumps.

**Accessibility caveat:** Viewport-based scaling can interact with browser zoom in surprising ways. Utopia's maintainers have addressed WCAG-related concerns.
Reference: https://www.trysmudford.com/blog/utopia-wcag-warnings/

### 2.5 Modern CSS typography features

Two recent features that directly improve "designed" feel:

- **`text-wrap: balance`** creates better multiline headings without manual line breaks. MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap
- **`font-size-adjust`** reduces ugly fallback shifts. web.dev: https://web.dev/blog/font-size-adjust

### 2.6 Design tokens: architecture for real theming

A token system that supports genuine thematic variety requires at least three layers:

| Tier | Name | Description | Example |
|------|------|-------------|---------|
| **1** | **Primitive** (base/reference) | Context-agnostic raw values. The full palette of available options. | `blue-500: oklch(0.5 0.2 250)`, `space-400: 16px` |
| **2** | **Semantic** (alias/decision) | Context-aware names describing intent. The API designers and developers use. | `color-action-primary: {blue-500}`, `spacing-component-gap: {space-400}` |
| **3** | **Component** (scoped) | Specific overrides for a component, inheriting from semantic tokens. | `button-bg-color: {color-action-primary}` |

**Theme switching should primarily swap base and semantic tokens while component tokens remain stable.** To create a "Brutalist" theme vs a "Corporate" theme, you remap the semantic layer:
- Corporate: `color-background-base` → `neutral-100` (white)
- Brutalist: `color-background-base` → `slate-900` (dark grey)

Component logic stays untouched; visual reality shifts entirely.

**Naming convention:** The **CTI (Category-Type-Item)** structure is the prevailing standard: `color.background.button.primary.hover`. This predictable taxonomy lets AI generators programmatically assign values because the name describes exact context of use.

**What separates alive systems from "Bootstrap with different colors":**
- **Motion tokens:** Not just duration (ms) but physics — mass, stiffness, damping. Material 3 introduced "Expressive" vs "Standard" motion tokens.
- **Surface tokens:** Radius (`radius-none` for brutalist, `radius-full` for playful), border weight, shadow character (`shadow-hard` vs `backdrop-blur`).
- **Density tokens:** Comfortable vs compact modes for different content types.

### 2.7 The 2024–2025 shift: standardization and tooling maturity

- **DTCG (Design Tokens Community Group) format:** The W3C-adjacent standard is stabilizing. JSON-based, interoperable between Figma and code.
  Spec: https://tr.designtokens.org/format/
- **Figma Variables:** Enable system-native token workflows including modes/themes.
  Docs: https://help.figma.com/hc/en-us/articles/14506821864087-Create-and-use-variables
- **Style Dictionary:** Common pipeline tool for transforming tokens into platform outputs (CSS variables, JSON, etc.).
  Docs: https://amzn.github.io/style-dictionary/
- **Tokens Studio:** Figma-centric token management, often paired with export pipelines.
  Docs: https://docs.tokens.studio/

### 2.8 Spacing and sizing scales

Spacing systems feel harmonious when they have a consistent unit and a predictable progression. Many systems use a **4px base unit** because it maps well to common type sizes and device pixel densities.

The key isn't "4px" itself — it's consistency + limited degrees of freedom. The space *inside* a component must always be smaller than the space *between* components to establish the Law of Proximity.

**Fluid spacing (Utopia model):** Like fluid type, spacing uses `clamp()` to adjust whitespace by viewport. A gap between cards might be `space-m` which equals 20px on mobile and 40px on desktop — the interface feels native to the screen size rather than just resized.

**Reference:** Tailwind spacing: https://tailwindcss.com/docs/customizing-spacing

