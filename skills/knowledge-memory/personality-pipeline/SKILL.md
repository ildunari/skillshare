---
name: personality-pipeline
description: >
  Use when updating personality or identity files from prior session behavior,
  especially SOUL.md, USER.md, or INSTRUCTIONS.md. Also use for requests like
  "personality pipeline", "update personality files", "extract signals",
  "run personality extraction", or "personality maintenance", whether run manually
  or from scheduled automation.
---

# Personality Pipeline

Maintain the shared personality files at `~/.craft-agent/personality/` by extracting behavioral signals from past sessions and merging them into the appropriate files.

**Announce at start:** "Running the personality pipeline."

## Prerequisites

Before executing, read these files (they define what goes where):
- `~/.craft-agent/personality/SPEC.md`
- `~/.craft-agent/personality/scripts/extraction_prompt.md`

## Pipeline Phases

Execute these phases in order. If any phase fails critically, skip to Phase F (cleanup) to release the lock.

---

### Phase A: Preflight

1. **Lock check:** Read `~/.craft-agent/personality/.lock`. If it exists and is less than 30 minutes old, abort with message "Pipeline already running (locked at {timestamp})." If stale (>30 min), delete it and continue.

2. **Create lock:** Write current ISO timestamp to `.lock`.

3. **Read watermark:** Read `~/.craft-agent/personality/.last-processed`. If missing, set default watermark to 24 hours ago. The watermark contains:
   ```json
   {"timestamp": "ISO-8601", "sessions_processed": ["session-id-1", "session-id-2"]}
   ```

4. **List sessions:** Find session directories across all workspaces:
   ```bash
   ls -d ~/.craft-agent/workspaces/*/sessions/*/session.jsonl 2>/dev/null
   ```
   Filter to sessions created after the watermark timestamp (use directory modification time).

5. **Exclude active sessions:** Remove any session whose `session.jsonl` was modified in the last 5 minutes.

6. **Exclude already-processed:** Remove any session ID already in the watermark's `sessions_processed` list.

7. **Minimum threshold check:** If fewer than 2 sessions remain, or total estimated stripped tokens < 1000, log "Insufficient data — skipping run" and exit (go to Phase F cleanup, update watermark timestamp but not session list).

8. **Cap at 20:** If more than 20 sessions, keep the 20 oldest. The rest will be processed next run.

---

### Phase B: Pre-Processing

9. **Strip sessions:** For each session, run:
   ```bash
   python3 ~/.craft-agent/personality/scripts/strip_session.py <session.jsonl>
   ```
   Capture the output text. Skip sessions that produce empty output.

10. **Estimate tokens:** For each stripped session, estimate tokens as `len(text) / 4`.

11. **Create batches:** Group sessions into batches targeting ~5000 tokens per batch. A single large session can be its own batch. Order batches by session age (oldest first).

---

### Phase C: Extraction

12. **Read current files:** Read the current content of SOUL.md, USER.md, and INSTRUCTIONS.md.

13. **Read extraction prompt:** Read `~/.craft-agent/personality/scripts/extraction_prompt.md`.

14. **For each batch, call `call_llm`:**
    - Model: `claude-sonnet-4-6`
    - System prompt: the extraction prompt content
    - User prompt: include:
      - "Current SOUL.md content:" + file content (abbreviated if very long)
      - "Current USER.md content:" + file content
      - "Current INSTRUCTIONS.md content:" + file content
      - "Session transcripts to analyze:" + all stripped session text in the batch
    - Request JSON output
    - Use `thinking: true` for better signal extraction

15. **Dispatch batches in parallel** when possible (multiple `call_llm` calls in one message).

16. **Parse results:** For each batch response, parse the JSON. If parsing fails, log the error and skip that batch.

17. **Persist intermediate state:** After each successful batch, append results to `.pipeline-state.json` for crash recovery.

---

### Phase D: Merge

18. **Collect all signals** from all batch results.

19. **Filter low-quality signals:** Drop any signal where confidence is "low" AND session_quality < 2.

20. **Deduplicate:** Group signals by (file, section). Within each group, check for semantic duplicates against each other and against existing file content. Drop duplicates.

21. **Resolve contradictions:**
    - For USER.md facts: require 2+ signals from different sessions to override an existing entry. A single contradicting signal gets logged but not applied.
    - For SOUL.md/INSTRUCTIONS.md: newer signal wins. Update the existing entry.

22. **Apply signals as additive edits** (not full rewrites):
    - `add`: Append the new entry to the appropriate section.
    - `update`: Find the matching existing entry and replace it.
    - `remove`: Delete the entry (only if confidence is "high" and 2+ signals agree).
    - Skip any entry marked `<!-- anchor -->`.

23. **Create .bak files** before writing:
    ```bash
    cp SOUL.md SOUL.md.bak
    cp USER.md USER.md.bak
    cp INSTRUCTIONS.md INSTRUCTIONS.md.bak
    ```

24. **Write updated files** using the Edit tool for surgical changes, not full file rewrites.

---

### Phase E: Verification

25. **Run structural validator:**
    ```bash
    python3 ~/.craft-agent/personality/scripts/validate_files.py
    ```

26. **If validation fails:**
    - If a file exceeds max line/word cap: trim the lowest-confidence, oldest non-anchor entries until under cap. Re-validate.
    - If structural issues (missing sections, bad format): restore from `.bak` and log the error.

27. **If validation passes:** Continue to Phase F.

---

### Phase F: Commit & Cleanup

28. **Git commit** (if any files changed):
    ```bash
    cd ~/.craft-agent/personality
    git add SOUL.md USER.md INSTRUCTIONS.md
    git commit -m "pipeline: extract signals from N sessions (YYYY-MM-DD)

    Sessions: session-id-1, session-id-2, ...
    Signals applied: X (SOUL: A, USER: B, INSTRUCTIONS: C)

    Co-Authored-By: Craft Agent <agents-noreply@craft.do>"
    ```

29. **Update watermark:** Write new `.last-processed` with current timestamp and all processed session IDs (merge with existing list, keep last 200 IDs to prevent unbounded growth).

30. **Write pipeline log entry** — append to `pipeline.log`:
    ```
    Run: YYYY-MM-DD HH:MM AM/PM TZ
    Sessions processed: N (workspace breakdown)
    Sessions skipped: N (reasons)
    Signals extracted: N (SOUL: A, USER: B, INSTRUCTIONS: C)
    Signals applied: N (duplicates dropped: D)
    Files changed: list of changed files with +/- line counts
    Validation: PASS/FAIL
    ```

31. **Cleanup:** Delete `.lock`, `.pipeline-state.json`, and `.bak` files.

---

## Weekly Compaction Variant (Sundays)

When the automation prompt says "weekly compaction", run this variant instead of the daily pipeline:

1. **Skip Phases B-C** (no new signal extraction).
2. **Read all three personality files** in full.
3. **Systemic review** using your own judgment (Opus model):
   - Identify and merge semantically duplicate entries across all files.
   - Remove entries that are clearly stale or no longer accurate.
   - Ensure entries are in the correct file per SPEC.md placement rules.
   - Verify scope tags are correct and canonical.
   - Check that no file exceeds its caps.
   - Preserve all anchor entries.
   - Preserve the existing voice/tone of SOUL.md.
4. **Write changes** using Edit tool (surgical, not full rewrite).
5. **Validate, commit, and log** as in Phases E-F.
6. **Generate CHANGELOG entry** — append to `~/.craft-agent/personality/CHANGELOG.md`:
   ```
   ## YYYY-MM-DD — Weekly Compaction
   - [SOUL.md] Added/removed/modified: description
   - [USER.md] Added/removed/modified: description
   - [INSTRUCTIONS.md] No changes
   ```

---

## Error Recovery

- If `call_llm` fails for a batch: skip that batch, continue with others. Log the failure.
- If ALL batches fail: exit gracefully. Watermark unchanged. Log "All extraction batches failed."
- If git commit fails: not critical — the files are still updated. Log warning.
- If disk space < 1MB: abort before any writes. Log "Insufficient disk space."
- If personality directory is not a git repo: run `git init` and continue.

## Model Selection

- **Daily orchestrator session:** Sonnet (specified in automations.json)
- **Extraction call_llm:** Sonnet with thinking
- **Weekly compaction session:** Opus (specified in automations.json)
