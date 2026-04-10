# Design Debugging

> Systematic CSS and layout troubleshooting. Adapted from superpowers systematic-debugging methodology (4-phase process, root cause tracing, 3-fix escalation) applied to visual problems.

## The Iron Law (design edition)

```
NO CSS PATCHES WITHOUT DIAGNOSING THE CATEGORY FIRST
```

Adding `!important`, random margin/padding, or `z-index: 9999` without understanding why the layout is broken is the visual equivalent of guess-and-check debugging.

## CSS bug categories

Before attempting any fix, identify which category the bug falls into. Each category has a different diagnostic approach and fix strategy.

| Category | Symptoms | Diagnostic approach |
|---|---|---|
| **Specificity** | Styles not applying, overridden unexpectedly, `!important` needed | Check selector specificity chain. Look for inline styles, ID selectors, or more specific rules winning. Use browser DevTools "Computed" tab. |
| **Box model** | Elements wider/taller than expected, overflow, unexpected spacing | Check `box-sizing` (should be `border-box`). Inspect padding, margin, border. Check if parent constrains width. |
| **Stacking context** | z-index not working, elements appearing behind/in front unexpectedly | Map the stacking contexts. `transform`, `opacity < 1`, `position: fixed/sticky`, `filter`, and `will-change` all create new stacking contexts. Fix the structure, not the z-index number. |
| **Layout algorithm** | Flexbox/Grid not behaving as expected, items wrong size or position | Identify which layout algorithm is active (block, flex, grid). Check if child sizing (`flex-grow`, `flex-shrink`, `grid-template`) matches intent. Check if `min-width: 0` or `overflow: hidden` is needed for flex children. |
| **Overflow** | Content clipped, scrollbars appearing unexpectedly, container not growing | Find which ancestor has `overflow: hidden/auto/scroll`. Check if a fixed height is constraining a growing container. Inspect whether `min-height` vs `height` is appropriate. |
| **Responsive** | Layout breaks at specific viewport widths, elements overlap or collapse | Walk breakpoints systematically: 320 → 375 → 768 → 1024 → 1440. Identify the exact breakpoint where it breaks. Check media query order (mobile-first = `min-width`, desktop-first = `max-width`). |
| **Animation** | Jank, stutter, layout shift during animation, elements jumping | Check if animating layout-triggering properties (`width`, `height`, `top`, `left`, `margin`, `padding`). Only `transform`, `opacity`, and `filter` are GPU-composited. Check for layout thrashing (read-write-read-write cycles). |

## The 4-phase debug process for CSS

### Phase 1: Observe

- What exactly is wrong? Screenshot or describe precisely.
- When does it happen? (All viewports? Only mobile? Only on hover? Only after scroll?)
- Is it consistent or intermittent?
- What was the last change before it broke?

### Phase 2: Diagnose category

Using the table above, identify which CSS category the bug belongs to. This is the critical step that prevents shotgun debugging.

**If you can't identify the category:** The layout structure may be fundamentally confused. Skip to the 3-fix escalation check.

### Phase 3: Test minimally

Make the SMALLEST possible change to test your hypothesis. One property change at a time.

**Good:** "I think the overflow is caused by this parent having `height: 100%`. Let me change it to `min-height: 100%` and see if the content stops clipping."

**Bad:** "Let me add `overflow: visible`, increase the height, remove the padding, and change the position to see if something works."

### Phase 4: Fix at root cause

Fix the structural issue, not the symptom.

| Symptom fix (bad) | Root cause fix (good) |
|---|---|
| `z-index: 9999` | Restructure DOM so elements are in the correct stacking context |
| `!important` on a style | Increase specificity naturally or reduce specificity of the overriding rule |
| `margin-top: -20px` to fix alignment | Fix the padding/gap that's causing the misalignment |
| `overflow: hidden` to hide a scrollbar | Fix the content that's overflowing (usually a child wider than parent) |
| `width: calc(100% - 17px)` to account for scrollbar | Use `overflow-y: overlay` or restructure to avoid the scrollbar-dependent layout |

## The 3-fix escalation rule (CSS edition)

If 3 CSS patches haven't fixed the problem, the HTML/component structure is wrong. Stop patching CSS and restructure:

**Signals the structure is wrong:**
- Each CSS fix creates a new visual issue elsewhere
- Fixes require increasingly hacky workarounds (`calc()` with magic numbers, negative margins, absolute positioning of relatively-positioned elements)
- The same bug reappears at a different breakpoint after being "fixed" at one breakpoint
- You need `!important` to override your own styles

**What to do:** Simplify the DOM structure. Reduce nesting. Let the layout algorithm (flex/grid) do the work instead of fighting it with overrides. Often, removing CSS is more effective than adding it.

## Responsive debugging walkthrough

When layout breaks on specific viewports:

1. **Identify the exact breakpoint.** Not "mobile" -- is it 320px? 375px? 414px? Different phones have different widths.
2. **Check the cascade.** Is a media query firing that shouldn't be, or not firing when it should?
3. **Check container queries vs viewport queries.** The container might be the right size but the viewport query is using the wrong threshold.
4. **Check flex/grid overflow.** Items refusing to shrink below their `min-content` size is the #1 cause of horizontal scrollbars on mobile. Fix: `min-width: 0` on flex children, or `minmax(0, 1fr)` on grid tracks.
5. **Check images/media.** Missing `max-width: 100%` on images causes overflow. Missing `aspect-ratio` causes layout shift.

## Animation performance debugging

| Symptom | Likely cause | Fix |
|---|---|---|
| Smooth on desktop, janky on mobile | Animating layout properties or too many elements | Switch to `transform`/`opacity` only. Reduce animated element count. |
| Jank at start of animation | Browser computing layout before first frame | Add `will-change` just before animation starts (remove after). |
| Layout shift during animation | Animating `width`/`height`/`margin`/`padding` | Use `transform: scale()` instead of `width`/`height`. Use `transform: translate()` instead of `top`/`left`. |
| Scroll jank | Scroll event handler doing layout work | Use `IntersectionObserver` instead of scroll listeners. Use `scroll-behavior: smooth` in CSS instead of JS. |
| Flash of unstyled content | Fonts loading late, no `font-display` | Add `font-display: swap`. Preload critical fonts. Set explicit dimensions to prevent reflow. |
