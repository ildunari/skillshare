# Requirements gathering and interpretation

This module turns messy prompts into buildable requirements.

## 1) Parse the user ask into a spec

Extract these fields (even if you must infer and mark as assumptions):

### Product + audience
- **Primary user**: who uses this?
- **Primary job-to-be-done**: what are they trying to accomplish?
- **Context**: desktop-at-work, mobile-on-the-go, accessibility needs?

### Scope
- **Screens/sections**: what pages or UI regions exist?
- **Core interactions**: create/edit/search/filter/sort/upload/pay?
- **Content**: what exact copy/data needs to appear (or placeholders)?

### Constraints
- **Tech**: framework, styling approach, existing component library
- **Brand**: fonts, colors, tone, “vibe”
- **Non-functional**: performance budgets, i18n, SEO, analytics hooks
- **Deadline**: affects how much polish/animation is appropriate

### Success criteria (define “done”)
- What metric matters? conversion, task completion, time-to-first-value
- What must be true for the user to say “yes, ship it”?

## 2) Ask only high-value questions

If crucial info is missing, ask **at most 3–6** questions.

Prioritize questions that change implementation:

### A) Functional questions (ship blockers)
- What are the required user actions and states?
- What data fields exist and which are required?
- What error/empty/loading states do you need?

### B) Content questions (design depends on it)
- Do you have real copy? If not, can we use structured placeholders?
- What’s the longest likely label/value? (helps avoid layout breaks)

### C) Visual direction questions (avoid generic output)
- Pick one: **editorial**, **technical/terminal**, **playful**, **premium/minimal**, **brutalist**
- Any references (sites/apps) you want to borrow from *without copying*?

### D) Constraints questions (integration)
- Must we match existing design tokens/components?
- Tailwind allowed? CSS variables? dark mode required?

If the user doesn’t answer, proceed with explicit assumptions.

## 3) Write assumptions explicitly (when needed)

Use an “Assumptions” section:

```md
### Assumptions
- Mobile-first; desktop enhanced.
- Tailwind available.
- User wants a distinctive, technical aesthetic (monospace accent, dark surfaces).
- Content is placeholder but structured (real copy can drop in).
```

Assumptions are not excuses — they’re commitments that keep momentum.

## 4) Convert requirements into an implementation-ready checklist

Output:

- **Component list** (reusable vs one-off)
- **State list** (default, hover, focus, loading, error, empty)
- **Breakpoints** (mobile/tablet/desktop)
- **Accessibility** requirements (keyboard, aria, contrast)
- **Performance** notes (lazy images, avoid heavy filters)

Example:

```md
### Components
- <HeaderNav /> (reusable)
- <SearchBar /> (reusable)
- <ResultCard /> (reusable)
- <EmptyState /> (reusable)
- <FilterDrawer /> (mobile-only, reusable)

### States
- Search: idle → typing → loading → results | empty | error
- Card: default / hover / focus-visible / selected
```

## 5) “Design direction” mini-brief (anti-generic)

Before planning, force a decision on:

- **Typography vibe** (see [typography-guide.md](typography-guide.md))
- **Color atmosphere** (see [color-systems.md](color-systems.md))
- **Layout signature** (what makes it *not* a template?)

A quick prompt for yourself:

- What’s the **dominant surface** (light paper / dark terminal / tinted)?
- What’s the **accent** (one sharp color, used sparingly)?
- What’s the **hero gesture** (big type, asymmetric grid, or texture)?

## 6) Definition of done (baseline)

Unless the user says otherwise, “done” means:

- Responsive and tested at narrow + wide widths
- Keyboard navigable with visible focus
- Meets WCAG AA contrast for text and controls
- All interactive states implemented
- No obvious layout shift; images sized
- Code is organized (tokens + reusable components)
