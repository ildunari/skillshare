# From-Scratch Workflow

> Building a new project, page, or artifact from zero.

## Step 1: Design Intent (Before Any Code)

Follow the **Intent First** and **Product Domain Exploration** frameworks in SKILL.md. Do not skip these — they are the difference between a crafted interface and a template.

1. **Answer the three intent questions** (references/design-philosophy.md → Intent First): Who is this human? What must they accomplish? What should this feel like? — with specifics, not generics.
2. **Produce the four domain outputs** (references/design-philosophy.md → Product Domain Exploration): domain concepts, color world, signature element, defaults to reject.
3. **State a direction** that references all four outputs. If someone could remove the product name and not identify what it's for — explore deeper.

Only then proceed to choosing fonts, colors, and layout.

## Step 2: Choose Foundation

### Theme Selection
If interactive artifact/simulation/game → pick from the 5 quick-access themes in `themes.md` or load the **visual-themes** skill for 32 curated theme packs with full palettes and component styling.
If website/app → select a font pairing from `themes.md` based on project type.

### Color Palette
1. Start with 1-2 brand colors (or choose from theme)
2. Generate neutrals using `oklch()` lightness scale:
   - Background: L=98% (light) or L=8% (dark)
   - Surface: L=95% or L=12%
   - Border: L=85% or L=22%
   - Text: L=15% or L=90%
   - Muted text: L=45% or L=60%
3. Primary accent: 1 saturated color. Use `color-mix()` for hover/active states.
4. **Never:** random gradients, more than 3 accent colors, or colors without semantic roles.

### Layout Strategy
- Choose a grid system (12-col CSS Grid for pages, Flexbox for components)
- Set max-width for content (`65ch` for reading, `1280px` for app layouts)
- Plan responsive approach: fluid spacing with `clamp()`, container queries for component-level

### CSS Architecture

**Custom property organization — three tiers:**

1. **Primitives** (raw values): `--blue-500: oklch(55% 0.18 250)`, `--space-4: 16px`, `--radius-m: 8px`
2. **Semantic** (role-based aliases): `--color-primary: var(--blue-500)`, `--color-surface: var(--gray-50)`, `--space-section: var(--space-16)`
3. **Component** (local overrides): `--button-bg: var(--color-primary)`, `--card-padding: var(--space-6)`

Changing `--blue-500` updates the primitive. Changing `--color-primary` updates the role. Changing `--button-bg` updates only buttons. No "I changed the blue and everything broke."

**Cascade layers:**

```css
@layer reset, base, tokens, components, utilities, overrides;
```

Specificity is managed by layer order, not selector weight. Stable in all browsers 2022+. Eliminates `!important` hacks.

**Tailwind organization (when using Tailwind):**
- Extract repeated patterns at 8+ utility classes on a single element
- Use `@apply` in component classes or extract to React components
- Never have 15+ utilities on one element — it's unreadable and unmaintainable

## Step 3: Build Structure

### HTML Artifacts (Single File)
```
1. Font import (<link> from Google Fonts)
2. CSS reset + custom properties (colors, spacing, fonts)
3. Layout structure
4. Component styles
5. Responsive adjustments
6. Motion (with reduced-motion)
7. JavaScript (minimal, at bottom)
```

### React Artifacts (Single .jsx)
```
1. Imports (React, hooks, libraries from CDN)
2. Constants (colors, config, data)
3. Sub-components (small, focused)
4. Main component (composition)
5. Tailwind classes (utility-first, no separate CSS)
6. Default export
```

## Step 4: Apply Polish

After the structure works, layer in:

1. **Typography:** Verify font pairing is loaded and applied. Check line-height (1.5-1.7 for body).
2. **Spacing:** Apply non-uniform rhythm. Tight near headings, generous between sections.
3. **Color:** Verify contrast ratios. Test dark mode if applicable.
4. **Motion:** Add entry animations (staggered reveal for lists). Scroll-triggered for below-fold.
5. **States:** Loading skeletons, empty states, hover/focus/active feedback.
6. **Accessibility:** Focus indicators, keyboard nav, ARIA labels, touch targets.
7. **Texture:** Subtle grain overlay, mesh gradient backgrounds, or glassmorphism where appropriate.

## Step 5: Pre-Flight Check

Run through the checklist in `aesthetic-principles.md` before delivering.

## Anti-Patterns to Avoid in New Projects

- Starting with a template and filling in content (builds generic)
- Choosing colors last (color should inform layout decisions)
- Skipping mobile-first (retrofitting responsive is harder)
- Adding motion after the fact (plan entry/exit animations with the layout)
- Using placeholder content in the final output (every element should feel intentional)
