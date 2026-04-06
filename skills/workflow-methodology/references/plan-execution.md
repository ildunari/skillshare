# Plan execution

> Adapted from `superpowers/skills/executing-plans`. Original skill uses persistent filesystem, git worktrees, and subagent dispatch. This adaptation retains the batch-and-checkpoint workflow for iterative building in Claude.ai chat.

## Core principle

Batch execution with checkpoints for user review. Never try to do everything at once and hope for the best.

## The process

### Step 1: Load and review plan critically

Before building anything, read the plan/spec/requirements with adversarial eyes:

- **Are there gaps?** Missing acceptance criteria, unclear requirements, unstated assumptions?
- **Are there contradictions?** Requirements that conflict with each other?
- **Are there dependencies?** Tasks that must happen in a specific order?
- **Questions?** Anything unclear at all?

**If concerns exist:** Raise them BEFORE starting. Present them clearly and wait for resolution.

**If no concerns:** Proceed to execution.

### Step 2: Execute a batch

**Default batch size: 3 tasks.**

For each task in the batch:

1. Announce which task you're starting
2. Follow the spec exactly (the plan has bite-sized steps for a reason)
3. Run any verifications the spec calls for
4. Note any issues encountered

**Why batches of 3:** Small enough to course-correct without wasted work. Large enough to show meaningful progress. Adjust based on task complexity -- 1-2 for complex tasks, up to 5 for trivial ones.

### Step 3: Report

When the batch is complete, present:

- **What was implemented** (brief, specific)
- **Verification results** (what works, what was tested)
- **Any issues or concerns** discovered during implementation
- **"Ready for feedback."**

Then stop. Wait for the user's response. Don't barrel into the next batch.

### Step 4: Continue

Based on feedback:

- Apply requested changes
- Execute the next batch
- Repeat until complete

### Step 5: Final verification

After all tasks are done:

- Run the two-stage self-review (see `references/two-stage-review.md`)
- Present the completed work with a clear summary

## When to stop and ask

**Stop executing immediately when:**

- Hit a blocker mid-batch (missing dependency, unclear instruction, something doesn't work)
- The plan has critical gaps that prevent starting a task
- You don't understand an instruction
- Verification fails repeatedly
- Something you discover invalidates the plan

**The rule: Ask for clarification rather than guessing.** Guessing leads to wasted work and wrong implementations.

## When to revisit earlier steps

**Return to plan review when:**

- User updates the plan based on your feedback
- Fundamental approach needs rethinking after discovering something during implementation
- Requirements changed mid-stream

**Don't force through blockers.** Stop and ask.

## Adapting for chat context

In Claude Code, "batches" map to discrete code commits. In claude.ai chat, batches map to:

- **Artifacts:** Build the first 3 features, present the artifact, get feedback
- **Code files:** Create the first 3 modules, present them, iterate
- **Multi-part outputs:** First 3 sections of a document, then continue

The principle is the same: build incrementally, get feedback, course-correct.

## Red flags (things that should never happen)

- Executing all tasks without any checkpoint
- Proceeding after a blocker without asking
- Skipping verification because "it should work"
- Implementing something you don't understand
- Guessing at requirements instead of asking
- Silently deviating from the plan without noting why
