Generate the `<row-id>` sprite row for this sprite-sheet-maker run.

Run dir: <absolute path>
Prompt file: <absolute prompt file>
Input images:
- <absolute path> - canonical base identity
- <absolute path> - optional style/reference/layout image

Read and follow the row prompt exactly. Use `$imagegen` only for visual generation.

Before returning, inspect:
- requested frame count
- same identity as canonical base
- action reads at target cell size
- clean flat background or valid alpha strategy
- separated, complete, unclipped frames
- no text, labels, guide marks, scenery, or unintended props

Do not edit manifests, assemble the final sheet, package outputs, or synthesize frames with local scripts.

Return only:

```text
selected_source=<absolute generated image path>
qa_note=<one sentence>
```

