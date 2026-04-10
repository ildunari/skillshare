# Forge Agent Examples

Load this file when the user wants concrete launch patterns, copyable commands,
or examples of when to choose one Forge lane over another.

## Common Recipes

### Plan in Forge with Muse

```bash
forge-agent plan "write a decision-complete implementation plan for this repo change"
```

Use this when the user wants Forge to think through the work without starting
implementation.

### Code in Forge

```bash
forge-agent code --cwd /path/to/repo "implement the requested fix"
```

Use this when the user wants the general coding lane to do the implementation
work in a specific repository.

### Apple-Specific Work in Apple Dev

```bash
forge-agent run --agent apple-dev --cwd /path/to/app "fix the SwiftUI navigation glitch, verify the macOS build still passes, and keep the change scoped to the affected screen"
```

Use this when the task is mainly Swift, SwiftUI, UIKit/AppKit, Xcode, signing,
or App Store Connect work.

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
