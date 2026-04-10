# Design Iteration Protocol

> How to manage multi-turn artifact refinement. Covers patch vs rebuild decisions, design decision tracking, iteration phase awareness, and diminishing returns detection.

## Iteration phases

Design work follows a natural arc. Knowing which phase you're in determines how to respond to feedback.

| Phase | What's happening | How to respond to feedback |
|---|---|---|
| **First draft** | Establishing foundations: palette, typography, grid, component structure | Be ready for wholesale changes. Nothing is locked yet. |
| **Structural refinement** (turns 2-3) | Adjusting layout, hierarchy, component placement, responsive behavior | Patch in place if change is < 30% of the artifact. Rebuild foundations if feedback targets the grid/palette/typography. |
| **Detail polish** (turns 4-6) | Tweaking spacing, colors, animations, hover states, edge cases | Almost always patch. Rebuilding at this stage loses accumulated polish. |
| **Final QA** (turns 7+) | Checking accessibility, responsive behavior, edge cases, performance | Only patch. If structural issues surface here, flag them explicitly rather than silently rebuilding. |

## Patch vs rebuild decision tree

```
User requests a change
       │
       ▼
Does it affect a foundation layer?
(color palette, grid system, typography, component architecture)
       │
       ├── No → Patch in place. Edit the specific elements.
       │
       └── Yes → How much of the artifact does it touch?
                │
                ├── < 30% → Patch. Change the foundation, fix cascading effects.
                │
                ├── 30-70% → Ask: "This affects most of the design.
                │              Rebuild with the new direction, or patch and accept
                │              some inconsistency?"
                │
                └── > 70% → Rebuild. The new direction is a new design.
                            Carry forward any approved details from previous version.
```

**When in doubt:** Patch. Rebuilding loses accumulated decisions and polish. Only rebuild when the foundations are genuinely wrong.

## Design decision tracking

As decisions are made across turns, track them mentally. When a requested change would undo a previous approval, flag it.

**What to track:**

- Color palette (approved specific colors/mood)
- Typography choices (approved font pairing)
- Layout structure (approved grid/component placement)
- Interaction model (approved hover/click behavior)
- Explicit user preferences ("I like the card style" = locked)
- Explicit rejections ("No gradients" = constraint)

**When to flag conflicts:**

```
User (turn 2): "I love the warm orange palette, keep that."
User (turn 5): "Can we try something cooler and more corporate?"

Response: "The warm orange palette you approved in turn 2 would conflict
with a cool corporate direction. Want to revise the palette, or keep
the warmth and make it more 'polished corporate' instead?"
```

Don't silently override earlier decisions. Surface the conflict.

## First draft presentation

When presenting the first draft, include brief rationale alongside the artifact:

- **Why this palette:** "Warm neutrals with terracotta accent -- editorial calm matching your brief."
- **Why this layout:** "Asymmetric 7/5 grid -- gives the hero more weight without centering everything."
- **Why this typography:** "Instrument Serif for display, Inter for body -- contrast between editorial headers and clean readability."

This makes subsequent feedback more targeted. The user can say "I like the typography but not the palette" instead of "I don't like it" (which requires the diagnostic framework from `design-feedback.md`).

## Diminishing returns detection

After 5+ iterations on the same artifact, explicitly check:

"We've been through [N] rounds of refinement. Are we close enough to ship, or is there a specific remaining issue I should focus on?"

This prevents infinite polish loops where each turn makes marginal changes that don't converge on a final state.

**Signs of diminishing returns:**
- Changes are getting smaller (1-2 elements per turn)
- User feedback is becoming less specific ("maybe slightly darker?")
- Changes start contradicting earlier changes
- User says "it's almost there" for 3+ consecutive turns

## Carrying state across long conversations

In long conversations (10+ turns), earlier design decisions may scroll out of context. When this happens:

- Refer back to the design decisions that were established
- If you're unsure whether something was approved, ask rather than assume
- For very long sessions, suggest saving a snapshot summary of approved decisions

## Integration with superpowers methodology

Design iteration follows the same feedback-handling rules as code:

- **Verify before implementing:** Check that the requested change makes sense before blindly applying it (see `design-feedback.md` translation table)
- **No performative agreement:** Don't say "Love it!" -- just make the change
- **Push back when warranted:** Flag accessibility violations, contradictions with earlier approvals, or physically impossible requests
- **Severity matters:** Not every piece of feedback requires action. "Maybe try a slightly different blue" is Minor. "I can't read the text" is Critical.
