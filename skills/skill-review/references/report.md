# Stage 5: Report Generation

Synthesize the Scratchpad findings into a final deliverable. The report should be
actionable — someone reading it should know exactly what to fix, in what order,
and why.

## Synthesis Process

1. **Deduplicate.** Merge findings from different stages that describe the same
   underlying issue. Keep the most specific description and the clearest fix.

2. **Validate severity.** Review all Critical findings — are they genuinely
   Critical by the thresholds defined in each stage? Inflate nothing. If a
   finding was marked Critical but doesn't meet the threshold on re-examination,
   downgrade it. Conversely, if a pattern of Important findings reveals a
   systemic issue, the pattern itself may be Critical even if individual items
   aren't.

3. **Identify root causes.** Some findings are symptoms of the same deeper
   problem. Group them under the root cause. For example, if multiple constraint
   issues stem from the skill being written for an older Claude model, the root
   cause is "skill not calibrated for 4.5/4.6" and the individual findings are
   evidence.

4. **Prioritize.** Within each severity level, order by impact — which fixes
   would produce the largest improvement in skill behavior?

5. **Write concrete rewrites.** For every Important and Critical finding,
   provide the specific replacement text — not just "rewrite this instruction"
   but the actual new instruction. The user should be able to copy-paste the
   fix directly into the skill.

## Report Template

Use this structure. The report is a markdown artifact delivered to the user.

```markdown
# Skill Review: [Skill Name]

## Summary

[2-3 sentences: what was reviewed, the skill's purpose, overall assessment.
End with a clear verdict: "Ready to use", "Needs fixes before use", or
"Needs significant rework".]

**Review scope:** [What was covered — all stages, or subset]
**Supplementary material:** [What the user provided, if anything]
**Verdict:** [Ready / Needs fixes / Needs rework]

## Strengths

[What the skill does well. Be specific — cite files, sections, patterns.
This is not filler; accurate strengths help the author understand what to
preserve during edits. 3-5 bullet points.]

## Critical Issues

[Issues that cause wrong behavior, broken workflows, or systematic failures.
These must be fixed.]

### [Issue title]

**Location:** [file:section or file:line]
**Impact:** [What goes wrong when this issue manifests]
**Evidence:** [Specific text or pattern from the skill]
**Fix:**
```
[Exact replacement text, ready to copy-paste]
```

[Repeat for each Critical issue]

## Important Issues

[Issues that degrade quality but don't break functionality. Should be fixed.]

[Same format as Critical]

## Minor Issues

[Polish items. Nice to have.]

[Briefer format — issue + suggested fix, no need for full evidence block]

## Structural Recommendations

[Merge, remove, split, or reorganize suggestions. File-level changes.]

| Action | Target | Rationale |
|---|---|---|
| Merge | [files] | [why] |
| Remove | [file/section] | [why] |
| Split | [file] | [into what] |
| Move | [content] → [destination] | [why] |

## Instruction Budget

**Current count:** [estimated number of discrete instructions]
**Budget status:** [Under budget / Approaching ceiling / Over budget]
**Recommendations:** [What to cut if over budget, or note that budget is fine]

## Next Steps

[Ordered list of recommended actions. What should the author do first?
If the skill would benefit from testing after fixes, suggest running
skill-creator's eval workflow.]
```

## Delivery

1. Create the report as a markdown artifact.
2. Present it to the user.
3. Offer to proceed with fixes: "Want me to implement these changes, or do you
   want to review the report first?"
4. Check this skill's FEEDBACK.md for any patterns that emerged during the
   review. If a new observation is worth logging, propose it.
