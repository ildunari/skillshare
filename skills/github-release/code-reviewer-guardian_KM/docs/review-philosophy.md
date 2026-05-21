
# Review Philosophy

**Order of review**: crashes & security → correctness → readability → architecture → performance → docs.

**Severity**:
- **P0** Critical (blocker): crashes, security/privacy violations, data corruption.
- **P1** High: concurrency hazards, retain cycles, boundary violations.
- **P2** Medium: maintainability, test gaps, style that hurts clarity.
- **P3** Low: nits and small idiomatic improvements.

**Workflow**:
1. Auto-run linters and analyzers.
2. Scan diff for high-risk files (touching concurrency/security/infra).
3. Walk the code path end-to-end; validate tests and acceptance criteria.
4. Provide actionable suggestions (with snippets or patches).
