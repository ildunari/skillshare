# Forge Sage Examples

Load this file when the user wants copyable Sage, review, or validation commands that include enough context to be operationally useful.

## Investigate with Sage

```bash
forge-agent research --cwd /path/to/repo "
Trace the auth failure without making changes.

Context:
- This is a multi-service app with a web client and API backend.
- Users can sign in, but some requests fail after login.

Read first:
- README or root docs
- auth-related middleware and route handlers
- recent auth-related diff if present

Focus:
- where auth state is created, forwarded, and lost
- likely root cause
- smallest safe fix direction

Output:
- concise trace of the failure path
- suspected root cause
- file references for each important finding
"
```

Use this when the user says "use Sage" or wants a read-only investigation.

## Review the Latest Change

```bash
forge-agent review --cwd /path/to/repo "
Review the latest change for bugs and regressions.

Context:
- The recent change updates Forge skill routing and examples.
- The goal is better delegated review prompts, not new runtime behavior.

Read first:
- git diff --stat
- full git diff
- any touched SKILL.md and reference files

Focus:
- broken references
- weak or misleading guidance
- missing context that would cause poor handoffs

Ignore:
- style-only wording nits
- unrelated cleanup ideas

Output:
- substantive findings only
- rank by severity
- include replacement wording when useful
- say \"no substantive issues found\" if clean
"
```

Use this when the user wants a bug/regression review after implementation.

## Validate the Current Repo

```bash
forge-agent check --cwd /path/to/repo "
Run the right validation for this project.

Context:
- This repo contains reusable AI skills synced to multiple targets.
- A recent rename may affect generated target copies.

Focus:
- broken sync assumptions
- missing files after rename
- validation or audit issues that would block rollout

Output:
- checks run
- failures with likely cause
- concrete next action for each failure
"
```

Use this when the user wants Forge to discover and run the relevant validation.

## Print the Exact Command Without Running It

```bash
forge-agent --print review --cwd /path/to/repo "
Review the latest change for important risks.

Read first:
- git diff --stat
- full diff

Focus:
- correctness
- regressions
- broken references
"
```

Use this when the user wants the exact launch command first.
