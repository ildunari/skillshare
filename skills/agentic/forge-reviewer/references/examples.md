# Forge Reviewer Examples

Load this file when the user wants copyable review or validation commands.

## Review the Latest Change

```bash
forge-agent review "review the latest change for bugs and regressions"
```

Use this when the user wants a bug- and regression-focused pass.

## Validate the Current Repo

```bash
forge-agent check "run the right validation for this project"
```

Use this when the user wants Forge to discover and run the relevant checks.

## Review in a Specific Repository

```bash
forge-agent review --cwd /path/to/repo "review the latest change for important risks"
```

Use this when the current working directory is not the repo that should be
reviewed.

## Print a Review Command Without Running It

```bash
forge-agent --print review "review the latest change"
```

Use this when the user wants the exact command first.
