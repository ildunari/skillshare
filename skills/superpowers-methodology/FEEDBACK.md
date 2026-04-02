# Superpowers Methodology -- Skill Feedback Log

> **MUST-READ DIRECTIVE:** Read this file every time this skill is loaded. Apply all lessons below when executing the methodology. Entries are tagged by category and dated.

<!-- CATEGORIES: decomposition, planning, execution, review, debugging, tdd, feedback, design-phase, workflow, meta -->

<!-- FORMAT: Date | Category | Entry (one actionable observation per line) -->

<!-- Max 75 entries. When this limit is reached, compact: merge duplicates, promote recurring patterns to reference files, archive resolved items. Reset to ~30 entries. -->

---

## When to add a feedback entry

Add an entry when any of these happen during a conversation:

- A methodology step prevented a mistake that would have otherwise occurred (positive reinforcement -- so you know which rules are load-bearing)
- A methodology step was followed but the outcome was still wrong (gap in the reference file)
- The user corrected something the methodology should have caught
- A rationalization surfaced that isn't in the existing rationalizations table
- A routing decision was wrong (loaded the wrong reference for the task type)
- A phase was skipped and it caused problems (or was correctly skipped and saved time)

Do NOT add entries for: one-off user preferences, tool/platform bugs, things outside the skill's scope.

---

## Example entries (remove these once real entries exist)

2025-02-13 | review | Two-stage review caught a missing error handler that spec compliance alone would have missed. The code-quality pass (stage 2) found it under the "production readiness" category. Reinforces: never skip stage 2 even when stage 1 passes clean.

2025-02-13 | debugging | User reported "it's still broken" after 2 fix attempts. Attempted a 3rd patch instead of escalating per the 3-fix rule. The 3rd patch created a new bug in adjacent functionality. The 3-fix escalation rule is not a suggestion -- it's a structural stop.

2025-02-13 | design-phase | Skipped design-before-code for a "simple" 3-component artifact. User wanted a different layout after seeing the first draft, requiring a full rebuild. 10 minutes of design questions would have saved 20 minutes of rebuilding. The "this is too simple" anti-pattern is real and frequent.

2025-02-13 | feedback | Implemented user feedback literally without the verify-before-implementing step. "Make it faster" turned out to mean perceived speed (loading states) not algorithmic performance. Restating the change in concrete terms before making it would have caught this.

2025-02-13 | tdd | Wrote implementation before the test "because it was obvious." Test passed immediately, proving nothing. Had to delete and rewrite. The TDD discipline reference warns about this explicitly -- "obvious" implementations still need failing tests to verify the requirement was understood correctly.
