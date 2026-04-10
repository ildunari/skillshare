# Delegation Guide

Reference for Phase 5 (Execute) of the Instruction Optimizer. Load this when
the user has approved the manifest and you're ready to dispatch sub-agents
for cleanup.

## Cost Model

The entire point of sub-agent delegation is cost efficiency. The orchestrator
(you) runs on the expensive model (Opus) and does the thinking — reading the
manifest, forming batches, writing precise prompts, reviewing results. The
workforce sub-agents run on cheap models (Haiku or Sonnet) and do the
mechanical work — editing files according to specific instructions.

### Why This Saves Money

A typical instruction optimization run touches 10-30 files. If Opus reads
every file, analyzes it, and edits it, that's ~50K-150K input tokens of
file content alone. By delegating the actual edits to Haiku:

- Haiku input tokens cost ~1/60th of Opus input tokens
- Haiku output tokens cost ~1/60th of Opus output tokens
- The orchestrator only reads the manifest (~2K tokens) and reviews
  summaries (~500 tokens per batch)

Rough savings: 80-90% reduction in cost for the execution phase.

### Model Selection Guide

| Task | Recommended model | Why |
|------|------------------|-----|
| File discovery (Phase 0) | Script (free) | Deterministic, no LLM needed |
| File reading + metadata (Phase 1) | Haiku or script | Mechanical extraction |
| Hierarchy mapping (Phase 2) | Sonnet | Needs semantic understanding |
| Deep analysis (Phase 3) | Sonnet or Opus | Judgment-heavy |
| Manifest generation (Phase 4) | Opus (orchestrator) | Synthesis across files |
| File editing (Phase 5) | Haiku | Mechanical, instruction-following |
| Result verification (Phase 5) | Sonnet | Needs to catch errors |

## Batch Formation

### Grouping Strategy

Group files into batches of 3-5 files each. Grouping criteria, in priority order:

1. **Priority level** — P0 files first, then P1, then P2. Never mix priorities
   in a batch (you want to verify P0 results before starting P1).

2. **Change type similarity** — Group files that need the same kind of changes:
   - "Remove redundant instructions" batch
   - "Update stale model references" batch
   - "Shorten verbose explanations" batch
   - "Extract content to skills" batch

3. **Hierarchy chain** — Files in the same precedence chain (global + project +
   subdir for one project) should be in the same batch so the sub-agent can see
   the full context and avoid creating new redundancies.

4. **File size** — Don't put 5 large files (>200 lines each) in one batch. The
   sub-agent's context will overflow. Mix large and small, or split large files
   into their own batch.

### Batch Size Limits

| Sub-agent model | Max total lines per batch | Max files per batch |
|----------------|--------------------------|---------------------|
| Haiku | ~800 lines | 5 files |
| Sonnet | ~1500 lines | 5 files |

If a single file exceeds the batch limit, give it its own dedicated sub-agent.

## Sub-Agent Prompt Templates

### Template 1: Remove / Shorten (Most Common)

Use for: removing redundant lines, shortening verbose explanations, cutting
instructions that restate default behavior.

```
You are editing agent instruction files to reduce token usage. Your changes
must preserve the meaning and intent of every instruction you keep.

## Files to Edit

[For each file, include:]

### File: [full path]
Current content:
```
[paste full file content]
```

Changes to make:
[paste the numbered recommendations from the manifest]

## Rules

- Apply ONLY the listed changes. Do not add new content or restructure
  sections beyond what's specified.
- When shortening, use conditional form ("When X, do Y") rather than
  imperative commands with emphasis.
- Do not remove instructions that are unique to this file and not found
  at a higher hierarchy level.
- Preserve all headings and section structure unless a recommendation
  explicitly says to remove a section.
- Output the complete edited file content for each file.

## Output Format

For each file, output:
1. The complete edited file (in a code block with the filename as label)
2. A summary: lines before → lines after, what changed
```

### Template 2: Extract to Skill

Use for: pulling content out of instruction files into new skill files.

```
You are extracting content from instruction files into standalone skills.

## Extraction Task

### Source File: [full path]
Lines to extract: [line range]
Content to extract:
```
[paste the content block]
```

### Target Skill: [skill name]
Location: [skill directory path]

## Instructions

1. Create SKILL.md for the new skill with:
   - name: [skill name]
   - description: [describe when to trigger — be specific and slightly pushy]
   - The extracted content, restructured as skill instructions

2. Edit the source file to:
   - Remove the extracted content
   - Add a brief note: "For [topic], use the [skill-name] skill" (one line)

3. Output both files complete.

## Rules

- The skill description is the primary triggering mechanism — make it specific
  about when to use the skill.
- Keep the skill under 500 lines. If the extracted content is longer, use
  progressive disclosure with reference files.
- The source file should still make sense after extraction. Don't leave
  orphaned headings or broken references.
```

### Template 3: Update Stale Content

Use for: updating model references, API patterns, tool names.

```
You are updating stale references in agent instruction files.

## Files to Update

### File: [full path]
```
[paste full file content]
```

Stale references to fix:
[list each stale reference with its replacement]

Example replacements:
- "Claude 3.5 Sonnet" → "Claude Sonnet 4.6"
- "Opus 4.1" → "Opus 4.6"
- "GPT-4 Turbo" → "GPT-5.4"
- "Gemini 1.5 Pro" → "Gemini 2.5 Pro" (verify currency)

## Rules

- Only update the specific references listed. Do not rewrite surrounding text.
- If a stale reference is part of a larger instruction that is also stale,
  flag it in your summary rather than rewriting the instruction.
- Output the complete edited file.
```

### Template 4: Cross-Platform Calibration

Use for: fixing ALL-CAPS emphasis, anti-laziness language, personality padding.

```
You are recalibrating instruction files for modern Claude 4.5/4.6 and
GPT-5.x models. These models respond better to explained conditionals
than to aggressive emphasis.

## File: [full path]
Runtime: [claude-code | codex-cli | gemini-cli]
```
[paste full file content]
```

## Calibration Changes

[list specific calibration issues from the manifest]

## Calibration Rules

For Claude 4.5/4.6 files:
- Replace ALL-CAPS emphasis (CRITICAL, MUST, ALWAYS, NEVER) with explained
  conditionals: "When X happens, do Y because Z"
- Remove anti-laziness language ("be thorough", "explore all", "don't skip")
- Remove personality padding ("you are a world-class expert")
- Keep genuine safety constraints in third-person form: "Claude does not..."

For GPT-5.x / AGENTS.md files:
- Apply the same de-emphasis changes
- Add explicit scope boundaries if missing ("Only modify files in...")
- Add done-conditions if missing ("Stop after completing the requested change")
- Remove micro-step instructions for tasks within native capability

## Output Format

Output the complete edited file, then a summary of changes made.
```

## Orchestration Flow

### Step 1: Pre-flight

Before dispatching any sub-agents:

1. **Confirm approved actions** — Re-read the manifest. Only proceed with
   actions the user has explicitly approved. If the user said "do the P0s",
   only batch P0 items.

2. **Create backups** — For each file that will be edited:
   ```bash
   cp /path/to/CLAUDE.md /path/to/CLAUDE.md.backup-$(date +%Y%m%d)
   ```
   Or, if the project uses git, ensure all files are committed first so
   changes can be reverted with `git checkout`.

3. **Verify file access** — Ensure you can read and write all target files.
   Some may be in read-only directories or require elevated permissions.

### Step 2: Dispatch Batches

For each batch:

1. **Select the prompt template** that matches the change type
2. **Fill in file contents and recommendations** from the manifest
3. **Dispatch the sub-agent** with `model: "haiku"` for mechanical edits,
   `model: "sonnet"` for anything requiring judgment

**Claude Code dispatch example:**
```
Agent tool call:
  model: "haiku"
  prompt: [filled template]
  description: "Edit batch 1: remove redundancy in global files"
```

**Parallel dispatch:** Independent batches (different files, no hierarchy
overlap) can be dispatched in parallel. Batches within the same hierarchy
chain should be sequential (edit global first, then project, then subdir).

### Step 3: Review Results

After each batch completes:

1. **Read the sub-agent's output** — it should contain the edited file
   content and a change summary
2. **Verify the edits** by checking:
   - No instructions were incorrectly removed (compare against manifest)
   - The file still parses as valid markdown
   - No new redundancies were introduced
   - Line count decreased (or at least didn't increase)
3. **Apply the edits** — Write the edited content to the actual files
4. **Report to the user** — "Batch 1 complete: edited 3 files, saved ~180 tokens"

### Step 4: Post-flight

After all batches are complete:

1. **Run the discovery script again** to get updated metrics
2. **Compare before/after** — total tokens, total lines, per-file changes
3. **Report final results** to the user:
   - Files edited
   - Total tokens saved
   - Percentage reduction
   - Any files that need manual attention

## Handling Failures

**Sub-agent produces bad edits:**
- Don't apply the edits
- Restore from backup if already applied
- Re-dispatch with more specific instructions or use Sonnet instead of Haiku

**Sub-agent misunderstands the task:**
- The prompt template was probably too vague
- Add an explicit "DO NOT" section with the specific mistake it made
- Re-dispatch

**File has changed since discovery:**
- Re-read the file before dispatching
- If it changed significantly, re-run analysis for that file
- If it changed trivially, proceed with the edit

**Permission denied:**
- Report to the user
- Skip the file and continue with the rest
- Include in the final report as "requires manual attention"

## Extraction Workflow (Detailed)

When the manifest recommends extracting content from an instruction file
into a skill, the full workflow is:

1. **Orchestrator decides:** Read the extraction recommendation. Determine
   the skill name, description, and target location.

2. **Dispatch extraction sub-agent:** Use Template 2 above. The sub-agent
   produces both the new skill and the edited source file.

3. **Orchestrator reviews:** Check that:
   - The skill has proper YAML frontmatter
   - The description will trigger correctly
   - The source file reference to the skill is clear
   - No content was lost in the extraction

4. **Create the skill directory and file:**
   ```bash
   mkdir -p <skill-location>/<skill-name>
   ```
   Write the SKILL.md file.

5. **Edit the source instruction file** to remove the extracted content
   and add the skill reference.

6. **Report:** Tell the user what was extracted, where the new skill lives,
   and how to invoke it.

## Cost Tracking

Keep a running tally of sub-agent dispatches for the user:

```
Batch 1: Haiku, 3 files, ~2K input tokens, ~1K output tokens
Batch 2: Haiku, 4 files, ~3K input tokens, ~1.5K output tokens
Batch 3: Sonnet, 2 files (complex), ~4K input tokens, ~2K output tokens
Total workforce cost: ~$0.02 (vs ~$1.20 if orchestrator did everything)
```

This transparency helps the user understand the cost savings and decide
whether to continue with lower-priority batches.
