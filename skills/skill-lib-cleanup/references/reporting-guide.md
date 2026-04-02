# Reporting Guide

Every cleanup report should separate these questions:
1. What is in canonical source?
2. What is in downstream installs?
3. What is out of sync?
4. What is overlapping in function?
5. What is safe to archive or delete?

## Required sections
- executive summary
- canonical source status
- distribution drift matrix
- duplicate / near-duplicate families
- routing collisions
- action dashboard
- delete/archive ladder
- visuals

## Guardrails
- Do not present all same-name copies as merge candidates.
- Do not recommend deleting canonical source by default.
- Keep distribution drift separate from similarity and merge analysis.
