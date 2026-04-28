# Stage 4: Cohesion Analysis

Look across all previous findings and the skill as a whole for systemic issues
that no single stage would catch. This stage answers: "Does the skill hold
together as a coherent system, and what happens when things go wrong?"

## Checklist

### 4.1 Internal Consistency

**Cross-reference check:** Read through SKILL.md, all reference files, and all
scripts as a connected system.

- Do reference files contradict each other? (File A says "use format X", File B
  says "use format Y" for the same output)
- Do scripts implement what SKILL.md promises? (Instructions say "run the
  validation script" but the script checks something different than described)
- Does the routing table match reality? (Says "load X for task Y" but X doesn't
  contain guidance for task Y)
- Are terms used consistently? (Same concept called different names in different
  files, or same name used for different concepts)
- Do examples match the instructions they illustrate? (Example output doesn't
  follow the rules the skill just stated)

### 4.2 Completeness

**Coverage analysis:** Map the skill's stated purpose against its actual
instruction coverage.

- Does the description promise capabilities that the instructions don't deliver?
- Are there workflow paths that dead-end? (Skill describes a branching process
  but only one branch has detailed instructions)
- Are there input types the skill should handle but doesn't address? (e.g., a
  document skill that handles .docx but never mentions .pdf even though users
  would reasonably provide both)
- Does the skill handle the "first use" case? (Clear enough for someone who's
  never used it before, or does it assume familiarity?)

### 4.3 Edge Case Analysis

Imagine the skill being invoked in unusual but plausible scenarios:

- **Empty or minimal input:** User provides almost nothing. Does the skill
  guide the model to ask for more, or does it try to proceed and produce
  garbage?
- **Oversized input:** User provides a massive file or very long prompt. Does
  the skill handle context limits, or does it assume input fits comfortably?
- **Wrong input type:** User provides input the skill isn't designed for. Does
  the skill detect this and redirect, or does it blindly apply its workflow?
- **Partial completion:** What if the model gets partway through the workflow
  and the conversation ends? Is there any recovery path, or does the user
  start over?
- **Conflicting user instructions:** User asks for something that contradicts
  the skill's instructions. Does the skill define priority (user overrides
  skill, or skill holds firm)?
- **Multi-skill interaction:** Could this skill's instructions conflict with
  other skills that might be active in the same session? Are there scoping
  boundaries?

### 4.4 Adversarial Analysis

Think about what could go wrong even with well-intentioned users:

- **Ambiguous triggers:** Are there user messages that could plausibly trigger
  this skill AND another skill? Which should win, and is that documented?
- **Instruction injection:** Could a user's input file contain instruction-like
  text that tries to override the skill's behavior?
- **Misuse potential:** Could the skill be used in ways the author didn't
  intend? Is that a problem, and if so, are there guardrails?
- **Failure cascades:** If one step fails, does the failure propagate cleanly,
  or could it cause downstream steps to produce wrong results silently?

### 4.5 Cross-Stage Conflict Detection

Review all findings from Stages 1-3 together:

- Do any structural recommendations conflict with technical recommendations?
  (e.g., "move this to a reference file" but the technical review says "this
  needs to be always-loaded for script X to work")
- Do any prompt improvements conflict with the skill's architecture? (e.g.,
  "simplify these instructions" but the technical review identified those
  instructions as necessary for script behavior)
- Are there findings that suggest a deeper design issue? (Multiple symptoms
  across stages pointing to the same root cause)
- Consolidate duplicate findings across stages — same issue flagged from
  different angles should become one recommendation.

### 4.6 Supplementary Material Completeness (if provided)

If the user provided research or reference material, check cross-stage coverage:

- Has the supplementary material been fully addressed across Stages 2 and 3?
- Are there research findings that weren't flagged in earlier stages because
  they span multiple review dimensions?
- Consolidate all supplementary-material-related findings here.

### 4.7 Merge and Remove Candidates

Based on the full review:

- **Merge candidates:** Are there reference files that overlap enough to
  consolidate? Are there instructions that repeat across files?
- **Remove candidates:** Are there files, scripts, instructions, or sections
  that don't earn their place? (Not referenced, not useful, or actively
  harmful)
- **Split candidates:** Are there files that try to do too much and should
  be split for better progressive disclosure?
- **Promotion candidates:** Are there patterns in FEEDBACK.md that have been
  observed enough times to become permanent instructions or reference content?

## Severity Guide for Cohesion Issues

| Severity | Threshold |
|---|---|
| **Critical** | Internal contradictions that cause wrong behavior, dead-end workflows, failure cascades that silently produce wrong output |
| **Important** | Incomplete coverage of stated purpose, unhandled edge cases that are likely in practice, ambiguous triggers with competing skills |
| **Minor** | Redundant content, merge/split opportunities, theoretical edge cases, polish |

## Output

Update the Scratchpad with all cohesion findings. Each finding:
- Tag: `[COHESION]`
- Severity: Critical / Important / Minor
- What: the systemic issue
- Evidence: which files/sections are involved
- Impact: what happens when this issue manifests
- Suggested resolution

Then proceed to Stage 5 (Report Generation).
