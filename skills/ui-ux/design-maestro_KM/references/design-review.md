# Design Review

> Severity-triaged visual quality assurance. Upgrades the binary pre-flight checklist in `aesthetic-principles.md` to a structured review with prioritized findings.

## When to use this

- Before presenting any substantial artifact (not for quick one-off snippets)
- When the user asks for a design review or audit
- When reviewing my own output on complex builds
- After major layout or palette changes to catch cascading issues

**For quick outputs:** The pre-flight checklist in `aesthetic-principles.md` is sufficient. Use this full review for artifacts that took 3+ turns to build or that will be used in production.

## Visual review rubric

### 1. Visual hierarchy

- Is there a clear focal point in each viewport?
- Does the eye follow a natural path (Z-pattern or F-pattern)?
- Is the heading → subheading → body → caption hierarchy clear?
- Are spacing rhythms non-uniform (tight near headings, generous between sections)?

### 2. Color and contrast

- Does the palette have semantic consistency (primary = action, neutral = structure)?
- Are accent colors used sparingly (1-2 per viewport, not everywhere)?
- WCAG AA contrast: 4.5:1 for body text, 3:1 for large text (18px+)?
- Dark mode (if applicable): desaturated accents, glows not shadows, `#0a0a0a` not `#000`?

### 3. Typography

- Is the font pairing deliberate (not default Inter/Roboto alone)?
- Are fonts actually loaded (`@import` or `<link>` present)?
- Is line-height appropriate (1.5-1.7 for body, 1.1-1.2 for display)?
- Is the type scale consistent (no random sizes outside the defined scale)?
- Is body text left-aligned (never centered for more than 2-3 lines)?

### 4. Responsiveness

- Does the layout work at 320px, 375px, 768px, 1024px, 1440px?
- Do images/media scale properly?
- Is touch target size adequate on mobile (44x44px minimum)?
- Does text remain readable at all breakpoints (no text overflow, no tiny fonts)?

### 5. Interaction states

- Do all interactive elements have hover, focus, active, and disabled states?
- Are focus indicators visible (`focus-visible:ring-2` or equivalent)?
- Are transitions smooth (not instant state jumps)?
- Full keyboard navigation (Tab/Enter/Escape/Arrow)?

### 6. Motion and performance

- Are animations purposeful (not decorative noise)?
- Is `prefers-reduced-motion` respected?
- Are only `transform`, `opacity`, and `filter` animated (GPU-composited)?
- No layout thrashing (`width`, `height`, `top`, `left` animated)?

### 7. Spatial integrity (charts and data viz)

This check applies whenever the artifact contains SVG charts, Canvas rendering, D3/visx/Recharts, or any visualization with computed label positions.

LLMs have no render loop — every coordinate is a prediction. These are the most common class of invisible defects that only appear after rendering.

- **No hardcoded chart dimensions.** `<LineChart width={600} height={300}>` is wrong. All Recharts charts must use `<ResponsiveContainer>`. Canvas must use `ResizeObserver`.
- **Labels gated by parent element size.** Text labels on treemap nodes, Sankey nodes, pie arcs, or bar segments must check that the parent element is large enough before rendering. Minimum thresholds: arc span ≥ 15° (0.26 rad), node height ≥ 20px, bar width ≥ 40px.
- **No two label systems at the same radial offset.** In circular charts, category labels and value labels need distinct radii with ≥20px separation.
- **Dense/variable data uses tooltips, not persistent labels.** If label count depends on user data, default to tooltip-on-hover and suppress inline labels.
- **Post-render collision check for force layouts and scatter plots.** After simulation stabilizes, use `getBBox()` to detect and hide overlapping labels.



| Severity | Threshold | Examples |
|---|---|---|
| **Critical** | Blocks usage, breaks accessibility, or creates a fundamentally broken experience | Text unreadable (contrast below 3:1), interactive elements unreachable by keyboard, layout completely broken on mobile, content overflow hiding information, no focus indicators |
| **Important** | Degrades quality significantly but doesn't block usage | Missing hover/active states, inconsistent spacing rhythm, font not loading (fallback visible), responsive layout awkward but functional, dark mode contrast issues, animation janking |
| **Minor** | Polish opportunities that don't affect functionality | Slightly off brand color, could use better font pairing, animation timing could be smoother, minor alignment inconsistency, decorative element could be improved |

## Structured output format

When presenting a design review explicitly (not silent self-review):

```
### Strengths
[What's well done -- cite specific elements]

### Issues

#### Critical (must fix)
[Each: what's wrong, where, why it matters, how to fix]

#### Important (should fix)
[Each: what's wrong, where, why it matters, how to fix]

#### Minor (nice to have)
[Brief notes]

### Assessment
Ready to present? [Yes / No / With fixes]
```

## Silent vs explicit review

**Silent review (default):** Run the review internally before presenting. Fix Critical and Important issues before showing the output. Don't report the review process to the user.

**Explicit review (when appropriate):**
- User asks "review this design" or "audit this"
- Complex artifact with findings worth discussing
- Tradeoffs exist that need user input (e.g., "fixing the responsive layout requires changing the grid, which affects the approved desktop layout")

## Integration with existing pre-flight checklist

The pre-flight checklist in `aesthetic-principles.md` is a subset of this review. The relationship:

1. **Pre-flight checklist** = quick binary scan (yes/no per item). Run on everything.
2. **This design review** = severity-triaged assessment with structured output. Run on complex work.

For most artifacts: run pre-flight silently. For substantial work: run full review, present findings if non-trivial.
