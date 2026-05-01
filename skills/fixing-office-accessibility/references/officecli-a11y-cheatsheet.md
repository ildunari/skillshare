# OfficeCLI accessibility cheatsheet

This is a focused accessibility cookbook. For general OfficeCLI usage, defer to the installed `pptx` and `word` base skills and the wiki:

- Command reference: https://github.com/iOfficeAI/OfficeCLI/wiki/Command-Reference
- Word reference: https://github.com/iOfficeAI/OfficeCLI/wiki/Word-Reference
- PowerPoint reference: https://github.com/iOfficeAI/OfficeCLI/wiki/PowerPoint-Reference
- Batch: https://github.com/iOfficeAI/OfficeCLI/wiki/command-batch
- Validate: https://github.com/iOfficeAI/OfficeCLI/wiki/command-validate
- Raw fallback: https://github.com/iOfficeAI/OfficeCLI/wiki/command-raw
- Watch: https://github.com/iOfficeAI/OfficeCLI/wiki/command-watch
- Mark: https://github.com/iOfficeAI/OfficeCLI/wiki/command-mark
- Goto: https://github.com/iOfficeAI/OfficeCLI/wiki/command-goto
- MCP: https://github.com/iOfficeAI/OfficeCLI/wiki/command-mcp

## Inspect before writing

```bash
officecli get report.docx '/body/p[8]' --json
officecli get deck.pptx '/slide[3]' --depth 2 --json
officecli view deck.pptx issues --json
officecli watch deck.pptx --open
officecli goto deck.pptx '/slide[3]'
officecli mark deck.pptx '/slide[3]/shape[5]' --label "review order"
```

OfficeCLI paths are DOM-like and 1-based, for example `/body/p[1]/picture[2]`, `/body/tbl[1]/tr[1]/tc[2]`, `/slide[3]/shape[2]`, `/slide[3]/picture[1]`, and `/slide[3]/table[1]/tr[2]/tc[1]`. PPT and Excel selectors can also target attributes, such as `shape[name=Title 1]`.


## MCP mode

`officecli mcp` exposes a unified `officecli` MCP tool with a `command` parameter. Supported command values include `create`, `view`, `get`, `query`, `set`, `add`, `remove`, `move`, `validate`, `batch`, `raw`, `merge`, and `help`. Prefer MCP when Claude Code is already configured for it and a long interactive session benefits from one resident OfficeCLI process. Prefer explicit terminal commands when you need copyable audit history, wrapper scripts, or shell-level backup/revert behavior.

## Alt text and decorative decisions

Preferred schema operations:

```bash
officecli set deck.pptx /slide[1]/picture[1] --prop alt="Sales funnel from lead to renewal"
officecli set report.docx '/body/p[3]/picture[1]' --prop alt="CEO speaking at the town hall"
```

For shapes, charts, SmartArt, and grouped graphics, first inspect the element and use the base `pptx` or `word` skill. If OfficeCLI help reports `alt` or `decorative` on that element type, use it:

```bash
officecli set deck.pptx '/slide[2]/shape[4]' --prop alt="Three-step onboarding process"
officecli set deck.pptx '/slide[2]/chart[1]' --prop alt="Revenue chart showing renewals increasing by quarter"
officecli set deck.pptx '/slide[2]/group[1]' --prop alt="SmartArt process from enroll to confirm"
officecli set deck.pptx '/slide[2]/picture[3]' --prop decorative=true
```

If the schema does not expose `alt` or decorative state for a chart, SmartArt, or group, use `raw`/`raw-set` only after confirming the relevant OOXML non-visual property. Document the fallback in the report.

## Tables and headers

Word repeating header row:

```bash
officecli set report.docx /body/tbl[1]/tr[1] --prop header=true
```

PPT tables expose the structural header semantic via the **table-level `firstRow` flag** (maps to `<a:tblPr firstRow="1"/>` in OOXML). This is the programmatic a11y fix — not visual bolding. Set it on the table, not the row:

```bash
# Verify the property name first (per the property-verification rule)
officecli help pptx set table

# Preferred: set firstRow at the table level
officecli set deck.pptx /slide[4]/table[1] --prop firstRow=true
```

If `firstRow` isn't exposed in `officecli help` for your version, fall back to raw-set against the table's `<a:tblPr>`:

```bash
officecli raw-set deck.pptx /ppt/slides/slide4.xml \
  --xpath "//a:graphicFrame//a:tbl/a:tblPr" --attr firstRow=1
```

Visual styling (bold cells, fills) does NOT make a table accessible — it only makes it look like a header. Skip those edits unless they're a separate finding.

Split only merges that harm accessibility. Word cell merge properties include `gridSpan`/`colspan` and `vmerge`; PPT cell merge properties include `gridSpan`, `rowSpan`, `hmerge`, `vmerge`, `merge.right`, and `merge.down`.

```bash
officecli set report.docx /body/tbl[2]/tr[1]/tc[1] --prop gridSpan=1
officecli set deck.pptx /slide[4]/table[1]/tr[2]/tc[1] --prop gridSpan=1 --prop rowSpan=1 --prop hmerge=false --prop vmerge=false
```

## Headings and slide titles

Promote or demote semantic Word headings by style. Do not edit body text unless the finding is about the title text itself.

```bash
officecli set report.docx /body/p[8] --prop style=Heading2
officecli set report.docx /body/p[12] --prop style=Normal
```

Set a slide title through the existing title placeholder/shape. If no title placeholder exists, inspect layout first and defer to the base `pptx` skill for adding the right placeholder.

```bash
officecli set deck.pptx '/slide[2]/shape[name=Title 1]' --prop text="Quarterly risk summary"
```

## Hyperlink text

Word hyperlink display text is schema-supported:

```bash
officecli set report.docx /body/p[12]/hyperlink[1] --prop text="Download the benefits guide"
```

PPT hyperlinks often live on shapes, paragraphs, or runs. Use the most specific text run when possible:

```bash
officecli set deck.pptx /slide[5]/shape[2]/run[1] --prop text="View enrollment rules"
officecli set deck.pptx /slide[5]/shape[2]/run[1] --prop link=https://example.com/enrollment
```

## Reading order and floating objects

Use `swap` for two elements and `move` for larger reordering. Validate after structural changes.

```bash
officecli swap deck.pptx '/slide[3]/shape[2]' '/slide[3]/shape[5]'
officecli move deck.pptx '/slide[3]/shape[5]' --before '/slide[3]/shape[2]'
officecli set report.docx '/body/p[3]/picture[1]' --prop wrap=inline
```

## Document metadata

```bash
officecli set report.docx / --prop title="2026 Benefits Guide"
officecli set deck.pptx / --prop title="Quarterly Risk Review"
```

## Batch and validation

Use batch for related writes to the same file. Batch mode opens and saves once, but partial changes may be saved if a later command fails. Use the bundled wrapper for backup and validation:

```bash
python scripts/apply_batch.py --file report.docx --commands a11y.commands.json --log a11y-changes.jsonl
```

Equivalent direct commands:

```bash
officecli batch report.docx --input a11y.commands.json --json
officecli validate report.docx --json
```

## Raw XML fallback

Use raw XML only when no schema operation exists. Record the reason in the change log.

```bash
officecli raw deck.pptx /ppt/slides/slide2.xml --pretty
officecli raw-set deck.pptx /ppt/slides/slide2.xml --xpath "//p:cNvPr[@id='7']" --attr descr="Process diagram"
officecli validate deck.pptx --json
```
