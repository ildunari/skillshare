# Merge Protocol

Reference file for Phase 8 (Execute) of the Skill Library Curator. Load
when the user approves a merge plan and you're ready to execute.

## Pre-Merge Checklist

Before merging any skill group, verify:

- [ ] User has explicitly approved this merge group
- [ ] Relationship map confirms these are NOT designed pairs
- [ ] No command bindings will break (or rebinding is documented)
- [ ] No other skills depend on a skill being removed
- [ ] The canonical target is identified (existing skill to enhance, or
      new skill to create)

## Merge Procedure

### Step 1: Determine the Canonical Base

Choose the skill with:
1. Best-structured SKILL.md (clean progressive disclosure)
2. Most complete and maintained reference files
3. Clearest description (routing logic, not marketing)
4. Strongest scripts (if script-backed)
5. Most FEEDBACK.md entries (evidence of iteration)

If no existing skill is suitable as a base, synthesize a new one. This is
rare — usually one member of a merge group is clearly strongest.

### Step 2: Extract Value from Each Source

For every skill being merged into the canonical version, identify what it
contributes that the canonical version lacks:

- Unique edge-case handling or failure modes
- Better examples or reference material
- Scripts that handle work the canonical skill does manually
- Trigger phrases or use-case descriptions not covered
- Constraints, guardrails, or safety boundaries
- Domain-specific knowledge or heuristics

Document what's being preserved from each source in a provenance block.

### Step 3: Write the Merged Skill

Follow standard skill architecture:

```
canonical-skill-name/
├── SKILL.md          (< 500 lines, routing + core workflow)
├── FEEDBACK.md       (fresh, with provenance note)
└── references/       (detail moved here)
    ├── ...
```

**SKILL.md rules for merged skills:**
- Frontmatter description combines the best trigger coverage from all
  sources, rewritten as clean routing logic
- Include a provenance comment near the top:
  ```
  <!-- Merged from: skill-a, skill-b, skill-c (YYYY-MM-DD) -->
  ```
- Preserve the strongest constraints and edge-case handling
- Remove duplicate wording and weak filler
- Keep optional sections modular in references rather than bloating core
- If the merge combines a general skill with a specialist, preserve the
  specialist's narrower guidance as a reference file or conditional section

**Description rules:**
- Must cover all legitimate trigger contexts from all source skills
- Must include "supersedes" declarations for any skills it replaces
- Must include clear boundaries ("don't use when...")
- Should be slightly "pushy" per skill-creator guidance — undertriggering
  is worse than overtriggering

### Step 4: Handle Residual Skills

For each source skill that's being absorbed:

- If it has unique reference files, migrate them into the canonical skill's
  `references/` directory
- If it has unique scripts, migrate them into `scripts/`
- If it has FEEDBACK.md entries, review them and carry forward any entries
  that are still relevant to the merged skill
- Mark the source skill for archival or removal per the action plan

### Step 5: Package and Present

1. Copy the merged skill to a working directory
2. Run the skill-creator packaging script if available:
   ```bash
   python -m scripts.package_skill ./canonical-skill-name
   ```
3. If packaging script isn't available, manually create the .skill zip
4. Present the .skill file to the user for installation
5. Remind the user to click-install since AI-uploaded skills may not persist

### Step 6: Document System Prompt Impact

If the merge affects the user's system prompt (routing table, commands,
override declarations, preference rules), produce a concrete diff showing:
- Lines to change in the routing table
- Command rebindings needed
- New override/supersedes declarations
- Removed skill references

Present this as a copyable text block the user can apply to their
preferences.

## Merge Anti-Patterns

### The Swiss Army Knife

Merging 4+ skills into one mega-skill that tries to do everything. Signs:
- Description has 6+ trigger contexts
- SKILL.md exceeds 400 lines before references
- The workflow has 3+ major branching paths
- Different sections of the skill could operate independently

**Fix:** Merge into 2 skills instead of 1, or merge into 1 canonical skill
with clearly scoped reference files for each domain variant.

### The Lossy Merge

Merging skills and accidentally dropping edge-case handling, specialized
examples, or safety constraints from the less-prominent source.

**Fix:** Explicitly list what each source contributes (Step 2). After
writing the merge, verify each contribution is preserved.

### The Trigger Landgrab

Merged skill's description becomes so broad it triggers on queries meant
for unrelated skills.

**Fix:** Write "don't use when" boundaries. Test the description mentally
against 5 queries that should NOT trigger this skill.

### The Orphan Dependency

Removing a source skill that another skill references or depends on.

**Fix:** Check the relationship map. Update all references in dependent
skills to point to the new canonical skill.

## Naming Convention for Merged Skills

Use: `domain-job[-modifier]`

Good canonical names:
- `frontend-design` (merged from overlapping UI skills)
- `research-synthesis` (merged from similar research workflows)
- `doc-creation` (merged from overlapping document skills)

Bad canonical names:
- `ultimate-frontend-v3`
- `merged-design-research-viz-skill`
- `frontend-design-final-FINAL`
- `skill-2026-03`

If the canonical base already has a good name, keep it. Don't rename
purely because a merge happened — name stability helps the user.

## Post-Merge: Cross-Location Propagation

After merging skills, the canonical merged version needs to reach all agent
runtimes that had the original skills. Follow this checklist:

1. **Identify all locations** where the source skills existed (from the
   cross-location report in Phase 2)
2. **Update the canonical location first** — typically `~/.agents/skills/`
   for Claude Code or the primary Craft Agent workspace for Craft Agent
3. **Check symlinks** — if other locations are symlinked to the canonical
   copy, they'll update automatically. Verify with `ls -la`.
4. **Update skillsync manifest** — if the skill is in the sync manifest
   (`~/.craft-agent/shared/skill-sync/manifest.json`), update the entry
   to point to the merged skill name
5. **Run skillsync** — `~/.craft-agent/shared/skill-sync/sync.sh` to
   propagate to other Craft Agent workspaces
6. **Update independent copies** — for agent runtimes that use independent
   copies (Codex, Cursor, Osaurus), manually copy or note for the user
7. **Verify** — run `scripts/cross_location_diff.py` again to confirm all
   copies are now identical

## One-Shot Prompt Fallback

If the user wants a quick audit without installing this skill, use this
compressed prompt. Copy `references/one-shot-prompt.md` and present it.
