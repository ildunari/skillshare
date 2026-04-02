## 7. Quick-reference checklists

### 7.1 Palette system

- Define neutrals as a tone ladder (perceptual L steps), not arbitrary grays
- Limit accent hues; treat accents as curves (tone vs chroma)
- Test contrast for body text, small UI labels, icon + control states, and focus rings
- Plan for dark mode polarity shifts, P3 enhancement, and out-of-gamut clipping
- Define semantic colors with consistent behavior (hover/active deltas, disabled states)
- Apply chroma bell curve: peak at mid-tones, taper at extremes

### 7.2 Typography

- Pick fonts by roles (text / display / data), not vibes
- Use variable fonts where it reduces complexity (weight, optical size)
- Ensure numeric readability: `tnum`, consistent glyph height, alignment rules
- Control line length and line-height per content mode
- Use `font-size-adjust` to reduce fallback shift
- Tighten tracking on large type, loosen on uppercase
- Avoid pure black on pure white; use desaturated dark/light alternatives

### 7.3 Token system

- Maintain base → semantic → component token layers
- Theme via semantic tokens; keep component tokens opinionated
- Document token intent and dos/don'ts
- Build a transform pipeline (Style Dictionary or equivalent)
- Include motion, radius, border, shadow, and density tokens — not just color

### 7.4 Motion

- Define intent classes: feedback / transition / attention / ambient
- Standardize durations and easing families
- Respect `prefers-reduced-motion` with a hard "no ambient" mode
- Define spring parameters (mass/stiffness/damping) for physics-based themes
- Test interruptibility for app-like interactions
- Keep scroll-driven motion optional and non-vestibular-triggering

### 7.5 Data visualization

- Provide separate scales: categorical, sequential, diverging
- Build data palettes in OKLCH, not brand RGB
- Don't rely on color alone; add labels, shapes, patterns
- Keep chart ink mostly neutral; use accent for highlights only
- Apply consistent typography rules to axes, labels, and tooltips
- Test in greyscale to verify non-color encoding works

### 7.6 Cultural inclusivity

- Research color semantics for target locales before hard-coding
- Provide density toggles (comfortable vs compact)
- Support RTL layouts as a first-class concern, not a CSS afterthought
- Ensure adequate line-height for CJK, Arabic, and Devanagari scripts
- Use semantic tokens so colors can be swapped without breaking component logic
- Accompany color meanings with icons or text labels
