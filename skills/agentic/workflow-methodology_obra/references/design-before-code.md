# Design before code

> Adapted from `superpowers/skills/brainstorming`. The hard gate, approach comparison, and section-by-section approval are the valuable methodology. Stripped: git commit of design docs, skill invocation chain (`writing-plans` handoff), project file exploration.

## The hard gate

Do NOT write code, create artifacts, scaffold projects, or take any implementation action until a design exists and the user has approved it. This applies regardless of perceived simplicity.

## Anti-pattern: "This is too simple to need a design"

Every non-trivial project goes through this process. A todo app, a single-function utility, a dashboard -- all of them. "Simple" projects are where unexamined assumptions cause the most wasted work.

The design can be short (a few sentences for truly simple things), but you MUST present it and get approval before building.

**When it IS okay to skip:** Genuinely trivial requests where the user knows exactly what they want and has specified it completely. "Make this button blue" does not need a design phase.

## The process

### 1. Ask clarifying questions -- one at a time

Understand purpose, constraints, success criteria. Don't overwhelm with multiple questions in one message.

- Prefer multiple choice questions when possible (easier to answer)
- Only one question per message unless questions are closely related
- Focus on understanding what success looks like
- Use `ask_user_input` tool for bounded choices

### 2. Propose 2-3 approaches with tradeoffs

Never commit to the first approach that comes to mind. Present options conversationally with your recommendation and reasoning.

**Structure:**
- Lead with your recommended option and explain why
- Present 1-2 alternatives with clear tradeoffs
- Be specific about what each approach sacrifices

**Example shape:**
```
I'd recommend Approach A (server-side rendering) because your
data updates infrequently and SEO matters. The tradeoff is
slower initial setup.

Alternative: Approach B (client-side SPA) would be faster to
build but worse for SEO and requires a loading spinner.

Alternative: Approach C (hybrid) gets you the best of both
but adds complexity you probably don't need yet. YAGNI.
```

### 3. Present design in sections, get approval per section

Scale each section to its complexity:
- Few sentences if straightforward
- Up to 200-300 words if nuanced

Ask after each section: "Does this look right so far?"

**Cover (as applicable):**
- Architecture / component structure
- Data flow / state management
- Key interactions / user flows
- Error handling approach
- What's explicitly OUT of scope (YAGNI)

Be ready to go back and revise if something doesn't make sense.

### 4. Get explicit approval, then build

Don't start building until the user has approved the design. A nod, "looks good," or "let's go" counts. Silence or "hmm" does not.

## Key principles

- **One question at a time.** Don't overwhelm.
- **Multiple choice preferred.** Easier to answer than open-ended.
- **YAGNI ruthlessly.** Remove unnecessary features from all designs.
- **Explore alternatives.** Always propose 2-3 approaches before settling.
- **Incremental validation.** Present sections, get approval per section.
- **Be flexible.** Go back and clarify when something doesn't make sense.

## When this pairs with other phases

After design approval, transition to the plan-execution phase for multi-step builds (see `references/plan-execution.md`). For simpler builds, go straight to implementation with the two-stage review at the end (see `references/two-stage-review.md`).

The design phase produces the "what." The plan phase produces the "how." The review phase verifies "did we actually."
