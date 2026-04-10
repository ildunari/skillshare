# Forge Sage Examples

Load this file when the user wants copyable Sage investigation commands that
include enough context to be operationally useful.

## Investigate with Sage

```bash
forge-agent research --cwd /path/to/repo "
Trace the auth failure without making changes.

Context:
- This is a multi-service app with a web client and API backend.
- Users can sign in, but some requests fail after login.

Question:
- Where is auth state created, forwarded, and lost?

Read first:
- README or root docs
- auth-related middleware and route handlers
- recent auth-related diff if present

Focus:
- the exact failure path
- likely root cause
- smallest safe fix direction

Output:
- concise trace of the failure path
- suspected root cause
- file references for each important finding
"
```

Use this when the user says "use Sage" or wants a read-only investigation.

## Map a Codepath

```bash
forge-agent research --cwd /path/to/repo "
Map how a user action moves through this system.

Context:
- We need to understand the save flow before changing it.

Question:
- Starting from the UI action, what functions, services, and side effects are involved?

Read first:
- the affected screen or route
- the save action handler
- any service or persistence layer it calls

Output:
- ordered codepath summary
- key state transitions
- file references
- likely risk points if we modify this flow
"
```

Use this when the user wants architecture or behavior mapped before making a change.

## Print the Exact Command Without Running It

```bash
forge-agent --print research --cwd /path/to/repo "
Trace the bug without making changes.

Read first:
- the relevant diff
- the affected module

Output:
- likely root cause with file references
"
```

Use this when the user wants the exact launch command first.
