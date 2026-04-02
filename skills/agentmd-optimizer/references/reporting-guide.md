# Reporting Guide

Use this guide when turning JSON outputs into a user-facing report.

## Required sections

1. **Executive summary**
   - total files
   - total tokens on disk
   - exact duplicate clusters
   - high-risk runtime stacks
   - high-confidence delete candidates

2. **Runtime/session impact**
   - report per runtime and per project root
   - do not imply that all discovered files load together

3. **Duplicate and drift analysis**
   - exact duplicates
   - near duplicates
   - semantic overlap / policy drift

4. **Action dashboard**
   - KEEP / MERGE / EXTRACT / SPLIT / ARCHIVE / DELETE / REGENERATE / REWRITE
   - confidence and risk with each recommendation

5. **Delete safety**
   - delete-now
   - probably-delete
   - archive-first
   - review-required

6. **Skill topology**
   - source vs install vs mirror vs artifact

## Visual recommendations

Prefer Mermaid diagrams for:
- load stacks
- duplicate clusters
- skill topology maps
- conflict maps

Prefer datatables for:
- delete candidates
- per-file stats
- per-runtime stack matrix

## Guardrails

- Separate **disk footprint** from **runtime impact**.
- Separate **duplicate storage waste** from **active session burden**.
- Mark stale findings clearly if files changed after the scan.
