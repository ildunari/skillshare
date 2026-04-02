# Existing Project Workflow

> Improving, extending, or fixing design on an existing codebase.

## Step 1: Analyze What Exists

Before changing anything, understand:
- **Tech stack:** React? Vue? Vanilla? Tailwind? Custom CSS? CSS modules?
- **Design system:** Are there existing tokens (colors, spacing, fonts)? Component library?
- **Current state:** What works well? What looks generic/broken?
- **Constraints:** Must maintain existing patterns? Can we introduce new dependencies?

### Quick Audit Checklist
- [ ] Font: Is it a deliberate choice or a default? Can we improve?
- [ ] Color: Is there a consistent palette or random colors?
- [ ] Spacing: Uniform or rhythmic? Can we add hierarchy?
- [ ] Components: Consistent styling or ad-hoc?
- [ ] Motion: Any animations present? Reduced-motion support?
- [ ] Dark mode: Supported? Done correctly?
- [ ] Accessibility: Focus indicators? Keyboard nav? Contrast?

## Step 2: Identify Wins

Prioritize changes by impact-to-effort ratio:

### Quick Wins (Minutes)
- Swap to a better font pairing (see `themes.md`)
- Add grain texture overlay to hero/backgrounds
- Fix spacing rhythm (vary section gaps)
- Add `font-display: swap` to font imports
- Add focus-visible styles

### Medium Effort (30min-1hr)
- Replace uniform card grids with bento layout
- Add entry animations (stagger reveals)
- Implement proper dark mode
- Add skeleton loading states
- Fix accessibility issues (contrast, ARIA, touch targets)

### Larger Effort (1hr+)
- Redesign hero section
- Add command palette navigation
- Implement page transitions
- Add data visualization polish
- Build a proper design token system

## Step 3: Match Existing Patterns

When adding new components to an existing project:
- **Use the same spacing scale** (don't introduce new values)
- **Match border-radius strategy** (if cards use rounded-lg, new cards should too)
- **Follow existing color semantics** (if blue = primary, don't use blue for a secondary action)
- **Maintain the same elevation system** (if shadows are subtle, don't add heavy shadows)
- **Use the same animation curves** (if existing motion uses ease-out, don't introduce spring)

## Step 4: Progressive Enhancement

Don't break what works. Layer improvements:

1. **First:** Fix broken things (accessibility, contrast, responsive issues)
2. **Then:** Improve existing things (better fonts, spacing, color)
3. **Finally:** Add new things (animations, effects, new patterns)

## Common Upgrades

### "Make it less generic" (Anti-slop pass)
1. Check all 10 anti-slop indicators from `aesthetic-principles.md`
2. For each violation found, grep the alternative from `references/deep/anti-patterns.md`
3. Apply fixes in order of visual impact

### "Add dark mode"
1. Define dark palette using guide in `aesthetic-principles.md`
2. Use CSS custom properties for all colors
3. Toggle via `class="dark"` on `<html>` or `@media (prefers-color-scheme: dark)`
4. Test contrast separately in dark mode

### "Make it feel more polished"
1. Add entry animations (stagger reveals from `motion-library.md`)
2. Add micro-interactions (button press, hover feedback)
3. Add texture (grain overlay, glassmorphism where appropriate)
4. Improve loading states (skeleton screens)
5. Polish empty states (illustration + CTA, not blank)
