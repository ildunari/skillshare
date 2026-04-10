# Forge Agent Examples

Load this file when the user wants concrete launch patterns, copyable commands,
or examples of when to choose one Forge lane over another.

## Common Recipes

### Plan in Forge

```bash
forge-agent plan "write a decision-complete implementation plan for this repo change"
```

Use this when the user wants Forge to think through the work without starting
implementation.

### Code in Forge

```bash
forge-agent code --cwd /path/to/repo "implement the requested fix"
```

Use this when the user wants the coding lane to do the implementation work in a
specific repository.

### Investigate with Sage

```bash
forge-agent research --cwd /path/to/repo "trace the auth failure without making changes; read the auth middleware, route handlers, and the latest diff first; focus on where state is lost; return likely root cause with file references"
```

Use this when the user says "use Sage" or wants Forge's read-only investigation lane.

### Review or Validate After Implementation

```bash
forge-agent review "review the latest change for bugs and regressions"
forge-agent check "run the right validation for this project"
```

Use `review` when the user wants bug and regression eyes. Use `check` when the
user wants the project validation lane.

### Inspect Agents or Tools

```bash
forge-agent list agents
forge-agent list tools forge
forge-agent info
```

Use this before recommending an agent or when the user asks what Forge can do
on the current machine.

### Resume Safely

```bash
forge-agent resume <conversation-id>
```

Prefer an explicit conversation ID when the user cares about context isolation.

### Print the Exact Command

```bash
forge-agent --print code "implement the requested change"
```

Use this when the user wants the exact launch command without executing it.

### Interactive Zsh-backed Session

```bash
forge-zsh
```

Use this only when the user wants to stay inside Forge interactively rather than
dispatching a one-shot task.
