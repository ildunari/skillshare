# Conflict Taxonomy

Conflicts matter more than bloat in some stacks. Use this taxonomy to classify them.

## Types of conflict

### 1. Hard contradiction
Two directives cannot both be followed.

Examples:
- one file says use tabs, another says use spaces
- one file says always use markdown bullets, another says avoid bullets and write prose only

### 2. Policy drift
Same topic, different value or framing, but not necessarily impossible to reconcile.

Examples:
- one file prefers concise responses, another prefers detailed structured reports
- one file says use CLI over MCP, another says prefer source tools first

### 3. Intentional override
A lower-level file narrows or overrides a higher-level default for a good reason.

Examples:
- global default says use TypeScript; one project explicitly says this package is Swift-only

### 4. Redundant restatement
Same policy repeated in multiple layers.

This is not a contradiction, but it still wastes context and increases drift risk.

## Reporting rules

- When a conflict appears in the same plausible load stack, raise its priority.
- When the files are on disk but not likely to load together, report as maintenance drift rather than active runtime conflict.
- Prefer “possible override vs drift — review needed” over falsely asserting a contradiction.
