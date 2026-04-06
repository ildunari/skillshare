# Quality pipeline reference

QA checks, pipeline architecture, toolchain comparison, and template engineering for professional DOCX output.

## Table of contents

1. [Pipeline stages](#pipeline-stages)
2. [YAML decision tree](#yaml-decision-tree)
3. [Programmatic QA checks](#programmatic-qa-checks)
4. [Visual QA rubric](#visual-qa-rubric)
5. [Available toolchain](#available-toolchain)
6. [Template engineering](#template-engineering)

---

## Pipeline stages

The reliable pattern is **plan → compose → validate → render → review → revise**. Single-pass "generate everything and hope" produces amateur output.

### Stage 0 — Inputs and constraints

- Domain profile (NIH / manuscript / business / technical / legal)
- Target medium (screen PDF vs print)
- Page size (Letter/A4) and binding mode
- Page/word limits if applicable

### Stage 1 — Document planner (structure first)

- Classify domain early (metadata + content signals)
- Output: outline tree (H1/H2/H3), decisions on exec summary/TOC/appendices/glossary, sectioning plan
- Quality gate: heading depth ≤ domain limit (default 3); section length bounds enforced

### Stage 2 — Style selector / template binder

- Choose style system (Academic/Business/TechSpec/NIH/Legal) — see `design-system.md` § JSON specs
- Bind to a specific template (reference DOCX / DOTX) if available
- Map each element type to a style ID from the template/spec
- Key principle: the agent is *not allowed* to invent formatting — it only chooses from approved styles

### Stage 3 — Composer (DOCX generation)

- Every block tagged with a paragraph style; inline semantics use character styles
- Tables use table styles + consistent column rules
- Figures inserted with consistent sizing + caption style
- Fields inserted for TOC, page numbers, cross-references

### Stage 4 — Programmatic QA (no vision required)

Run the checks in the next section. Fix any failures before rendering.

### Stage 5 — Render + visual QA (layout-aware)

- Render DOCX → PDF → images using LibreOffice headless + pdftoppm (both available)
- Score against the visual rubric below
- If score < target: generate fix plan and loop

### Stage 6 — Revision loop (surgical fixes)

- Reapply correct style where a block drifted
- Split overly long paragraphs or restructure sections
- Redesign wide tables (split / rotate / shrink font)
- Insert missing captions, page breaks, section breaks

### Content vs formatting: separate concerns

A common architecture:
- **Content agent** — produces semantically structured intermediate representation (headings, paragraphs, tables, figure descriptions)
- **Layout/styling agent** — binds IR to template styles and makes geometry decisions
- **QA agent** — audits style usage and layout outputs; triggers fixes

This separation reduces the chance that the content agent "helpfully" inserts manual formatting that violates the style system.

---

## YAML decision tree

Encode the full pipeline logic:

```yaml
doc_pipeline:
  inputs:
    - domain: [nih_grant, scientific_manuscript, business_report, technical_report, legal]
    - audience: [reviewer, decision_maker, engineer, general]
    - constraints:
        page_limits: optional
        required_template: optional
        required_fonts: optional
  stage_1_plan:
    - choose_style_system(domain, template_if_available=true)
    - choose_structure_pattern(domain, audience)
    - decide_navigation:
        toc: (estimated_pages >= 6) OR (heading_count >= 12)
        exec_summary: (domain == business_report) OR (audience == decision_maker)
        appendices: (has_large_tables OR has_raw_data OR compliance_material)
        glossary: (defined_terms_count >= 10)
  stage_2_skeleton:
    - create_sections:
        - cover/front_matter_section (if toc or exec_summary)
        - body_section
        - appendix_section (if needed)
    - set_page_numbering:
        - front_matter: roman
        - body: arabic starting at 1
    - add_headers_footers_per_section
    - insert_fields: toc_field if toc, update_fields_on_open = true
  stage_3_content_mapping:
    for each section:
      - classify_block_element:
          table if data has >= 2 columns OR repeated key:value patterns
          list if 3+ short items or steps
          definition_list if "term: definition" patterns
          callout if NOTE/WARN semantics
          code_block if fenced code or inline commands
          figure if referenced image/diagram
          else body_paragraph
      - apply_style_for_element
  stage_4_layout_enforcement:
    - max_depth_default = 3
    - keep_with_next for all headings
    - no blank paragraphs for spacing
    - tables: caption required, header row required, numeric alignment right
    - figures: caption required, keep_with_next between figure and caption
  stage_5_quality_gates:
    - style_coverage >= 0.95
    - heading_level_jumps == 0
    - blank_paragraph_runs == 0
    - render_and_score if high-fidelity needed
```

---

## Programmatic QA checks

These checks catch most amateur artifacts cheaply. Implementable with python-docx + XML access or by inspecting docx-js output.

### Style consistency audit

- Percentage of paragraphs using approved styles ≥ 95%
- No "Normal" paragraphs in body unless intentionally allowed
- No direct formatting on runs except allowed character styles
- Direct formatting rate below threshold (≤ 3% of runs)

### Heading hierarchy validation

- No level jumps (H1 → H3 without H2)
- Heading count supports TOC inclusion threshold
- All headings have `keep_with_next` enabled
- No heading followed by very short paragraph (< 80 chars)

### Spacing verification

- Body paragraphs have correct space_after and line spacing
- No consecutive empty paragraphs
- Lists use list styles, not manual hyphens/bullets

### Table sanity checks

- Every table has a caption
- Header row exists when table has ≥ 2 columns
- Numeric columns right-aligned
- Estimated column widths sum ≤ available width
- Multi-page tables have repeating header rows

### Field integrity checks

- Headers/footers contain PAGE/NUMPAGES fields if present
- TOC field present when requested
- `updateFieldsOnOpen` enabled when TOC/cross-references exist

### Geometry and margin checks

- Page size matches domain requirement
- Margins within domain constraints (NIH ≥ 0.5in)
- Mirror margins/gutter enabled only if binding profile requires it

---

## Visual QA rubric

Render DOCX → PDF → page images. Score each page:

| Dimension | What to check |
|---|---|
| Vertical rhythm | Consistent spacing between paragraphs and headings |
| Alignment | Left edges line up; tables align with text block |
| Hierarchy | Headings clearly distinct; no "fake headings" via bold text |
| Table readability | Header emphasis, banding, padding |
| Figure system | Captions consistent; spacing stable |
| Navigation | Running header/footer consistent; page numbers present |
| Orphans/widows | Headings not orphaned; captions not separated from their figure/table |
| Whitespace balance | No huge gaps; no cramped pages |

To render for inspection:

```bash
soffice --headless --convert-to pdf document.docx && pdftoppm -jpeg -r 150 document.pdf page
```

---

## Available toolchain

These tools are pre-installed and verified in the Claude.ai / Claude Desktop sandbox environment. Use only these tools — do not reference or attempt to use tools not listed here.

### Creation tools

| Tool | Language | Best for |
|---|---|---|
| **docx (npm)** v9.5.1 | JavaScript | Creating new documents from scratch with full style control |
| **Pandoc** v3.1.3 | CLI | Converting Markdown → DOCX with a reference doc for styles |

### Editing tools

| Tool | Language | Best for |
|---|---|---|
| **python-docx** v1.2.0 | Python | Reading and modifying existing documents programmatically |
| **Bundled Document library** | Python | OOXML-level editing, tracked changes, comments |
| **Bundled ooxml scripts** | Python | Unpacking/packing/validating DOCX archives |

### Rendering and QA tools

| Tool | Purpose |
|---|---|
| **LibreOffice** v24.2 (headless) | DOCX → PDF rendering |
| **poppler-utils** (pdftoppm) | PDF → image conversion for visual QA |
| **ImageMagick** | Image processing and conversion |

### Figure generation tools

| Tool | Purpose |
|---|---|
| **matplotlib** v3.10 / **seaborn** v0.13 | Charts and data visualizations |
| **Graphviz** (dot) | Diagrams and flowcharts |
| **Pillow** v12.1 | Image processing |

### Tool capabilities and limitations

**python-docx known limitations:**
- Inline pictures only — no floating/anchored in high-level API
- TOC — not first-class; workaround: field codes + updateFieldsOnOpen
- Track changes — not fully supported (use bundled Document library instead)
- Comments — main document only (not header/footer/footnotes)
- Table borders/padding — some require template or XML editing
- List numbering restart — often requires understanding numbering definitions
- PAGE/NUMPAGES fields — fragile when documents are manipulated

**docx-js known limitations:**
- No template loading — creates from scratch only
- TOC requires `updateFieldsOnOpen` + user opens in Word/LibreOffice to update
- Images require explicit `type` parameter

### Pipeline patterns available in this environment

**Pattern A — docx-js generation + LibreOffice field update:**
Generate DOCX with docx-js → insert fields (TOC, page numbers) + `updateFieldsOnOpen` → render with LibreOffice for visual QA.

**Pattern B — Pandoc for baseline + python-docx for post-processing:**
Markdown → Pandoc with reference.docx → python-docx pass for section headers/footers, caption normalization, compliance checks.

**Pattern C — python-docx read + Document library edit:**
Read existing DOCX with python-docx for analysis → unpack with ooxml scripts → edit with Document library → pack and verify.

### Not available in this environment

These tools are referenced in DOCX literature but are **not installed** here. Do not attempt to use them:
docxtpl, docxcompose, Python-Redlines, docx-revisions, Open XML SDK (.NET), docx4j (Java), Aspose.Words, Mammoth.js, Typst, Ghostscript.

---

## Template engineering

### Template-first is the professional approach

The template's contents are ignored; its styles and properties (margins, page size, headers/footers) are used. This is how professional organizations operate: a locked template defines layout, content flows into it.

### Creating a reference template

Generate a Pandoc reference document and customize its styles:

```bash
pandoc --print-default-data-file reference.docx > my-reference.docx
```

Then unpack, modify `word/styles.xml`, and pack:

```bash
python ooxml/scripts/unpack.py my-reference.docx ref-unpacked
# Edit ref-unpacked/word/styles.xml
python ooxml/scripts/pack.py ref-unpacked my-reference.docx
```

### Style-safe authoring rules

1. No manual formatting in the template body — everything style-based
2. Tables for expansion have clear row markers and consistent style
3. Headers/footers contain fields but are minimal

### Pandoc reference.docx best practices

- Generate via `--print-default-data-file reference.docx` and modify styles only
- Use `custom-style` attributes on Div/Span/Table for custom paragraph styles
- Maintain style system in the reference doc; don't fix styling post-hoc

### Template failure modes

| Failure | Cause | Prevention |
|---|---|---|
| Template overrides lost | Normal style + direct formatting | Assign correct style; avoid direct formatting |
| Broken inheritance | Styles without `based_on` | Always specify `based_on` programmatically |
| Brand colors not applied | Hardcoded RGB instead of theme reference | Use theme color references |
| Cross-document differences | Multiple templates, no shared core | Common base template |
| Style drift from copies | Direct formatting from external sources | Style normalization pass |

### Versioning

Treat your style system like code: version templates (semantic versioning), keep a machine-readable style spec (JSON) alongside the template, run regression renders, enforce style usage with checks before shipping.
