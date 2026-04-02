# Handling Design Feedback

> How to process vague, conflicting, or iterative design feedback. Adapted from superpowers feedback-handling methodology and applied to visual design.

## Vague feedback translation table

When the user gives subjective feedback, translate it to concrete design actions before changing anything.

| User says | They probably mean | Concrete actions |
|---|---|---|
| "Make it pop" / "more energy" | Low contrast, flat hierarchy, no focal point | Increase contrast between text and background. Add a saturated accent color. Introduce motion (entry animation, hover effects). Increase size difference between heading and body. |
| "Feels flat" / "needs depth" | No elevation hierarchy, uniform surfaces | Add layered surfaces (card elevation). Introduce subtle shadows or glows. Add texture (grain overlay, mesh gradient). Vary z-index / overlap elements. |
| "Boring" / "too plain" / "generic" | Symmetrical layout, no visual rhythm, predictable | Break symmetry (7/5 split instead of 6/6). Add visual tension (oversized element, unexpected color). Vary card sizes. Add decorative elements with purpose. Run the anti-slop checklist. |
| "Too busy" / "cluttered" / "overwhelming" | Too many competing elements, no white space | Remove decorative elements. Increase spacing between sections. Reduce color palette to 2-3 colors. Establish clearer hierarchy (one focal point per viewport). Reduce font weights/sizes in use. |
| "More professional" / "more polished" | Inconsistent spacing, default fonts, rough edges | Audit spacing rhythm (make it consistent). Upgrade to a deliberate font pairing. Align elements to grid. Add subtle transitions. Fix any accessibility issues. |
| "More modern" / "fresher" | Dated patterns, heavy borders, boxy layout | Reduce border usage (use spacing instead). Soften with larger border-radius on containers. Use a contemporary font pairing. Add glassmorphism or blur effects sparingly. |
| "More minimal" / "cleaner" | Too many colors/fonts/decorative elements | Strip to essentials. One typeface family. Monochrome + one accent. Remove borders, reduce shadows. Generous white space. |
| "Warmer" / "friendlier" | Cool or neutral palette, rigid grid, sharp corners | Shift palette toward warm tones (amber, coral, warm gray). Round corners. Add organic shapes or illustrations. Use a humanist sans-serif or serif. |
| "Colder" / "more serious" / "more corporate" | Warm colors, playful elements, casual typography | Shift to cool neutrals (slate, blue-gray). Sharpen corners. Remove illustrations. Use a geometric sans-serif. Increase white space. |
| "I don't like it" (no specifics) | Could be anything -- need to diagnose | Use the diagnostic framework below. |

## Diagnostic framework for unspecified dissatisfaction

When the user can't articulate what's wrong, narrow it down by category. Use the `ask_user_input` tool:

**First pass -- identify the category:**

"Which of these feels closest to the issue?"
- Color palette / mood (too dark, too bright, wrong vibe)
- Layout / structure (things in wrong places, spacing off)
- Typography (fonts feel wrong, hard to read)
- Density (too much stuff, or too empty)
- Overall style (doesn't match what they had in mind)

**Second pass -- narrow within category:**

Based on their answer, ask one targeted follow-up. For example, if "color palette":
- "Is it the background color, the accent color, or the overall warmth/coolness?"

Two questions maximum. Then propose a specific change and ask if that's the direction.

## Preservation protocol for partial edits

When the user says "change X but keep Y":

1. **Before editing:** Explicitly identify what's locked. State it: "I'll change [X] while keeping [Y] intact."
2. **During editing:** Treat locked elements as constraints, not suggestions.
3. **After editing:** Verify the locked elements survived. If anything had to change for structural reasons, flag it: "I had to adjust [Y slightly] because [X change] affected the layout. Here's what changed."

**Common preservation failures to watch for:**
- Changing the color palette resets custom hover/active states to defaults
- Layout restructuring breaks responsive behavior that was already working
- Font swap changes line heights which shifts all vertical spacing
- Animation changes that affect adjacent elements via layout shift

## When to push back on design feedback

Push back (with reasoning) when:

- Feedback would break accessibility (removing focus indicators, insufficient contrast)
- Feedback contradicts an earlier approved design decision (flag the contradiction, ask which to follow)
- Feedback would create significant technical debt ("make every card a different size" → unmaintainable)
- Feedback is physically impossible in the medium ("make the font bigger AND fit more content in the same space")

**How to push back on design:** Frame it as a tradeoff, not a refusal. "I can increase the font size, but we'd need to either reduce the content or expand the container. Which would you prefer?"

## No performative agreement

Don't say "Great eye!" or "Love that direction!" when receiving design feedback. Just acknowledge and act:

- "Got it -- increasing contrast and adding entry animations." (then do it)
- "Understood. Here's the updated version with warmer tones." (then show it)
- "That contradicts the palette we approved earlier. Want to revise the palette or keep it?" (then wait)
