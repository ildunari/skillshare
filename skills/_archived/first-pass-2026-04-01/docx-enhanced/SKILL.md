---
name: docx-enhanced
description: "Professional document creation, editing, and analysis for Word (.docx) files. Handles everything from creating new documents with publication-grade typography and layout, to editing existing files with tracked changes and comments, to extracting content for analysis. Use this skill whenever the user mentions Word docs, .docx files, grants, manuscripts, reports, memos, letters, or any task that produces a professional document deliverable. Also use when the user asks to fix formatting, add tracked changes, review a document, or create a template. Triggers on: 'write a report', 'make a Word doc', 'format this as a grant', 'create a memo', 'review this document', 'add tracked changes', 'fix the formatting', or any document-related request."
---

# DOCX: creation, editing, and design intelligence

Professional Word documents are defined by systematic consistency across four layers: information architecture (predictable sectioning, navigable front/back matter), style system (named styles covering everything, no direct formatting), page geometry (margins, headers/footers, sections used intentionally), and data presentation (tables that read like publications, figures with captions). This skill handles both the mechanical workflows and the design decisions.

## Environment

This skill targets Claude.ai and Claude Desktop sandbox environments. All tools referenced below are pre-installed and verified. No additional installation is required.

**Pre-installed and verified:**

| Tool | Version | Purpose |
|---|---|---|
| `docx` (npm) | 9.5.1 | Create new Word documents via JavaScript |
| `python-docx` | 1.2.0 | Read and edit existing Word documents via Python |
| `pandoc` | 3.1.3 | Convert between formats (Markdown ↔ DOCX, text extraction) |
| LibreOffice | 24.2 | Render DOCX → PDF (headless mode) |
| `poppler-utils` | 24.02 | Convert PDF → images (pdftoppm) |
| `defusedxml` | 0.7.1 | Safe XML parsing (used by bundled scripts) |
| `lxml` | 6.0.2 | XML manipulation (used by bundled scripts) |
| `Pillow` | 12.1 | Image processing |
| `matplotlib` / `seaborn` | 3.10 / 0.13 | Generate charts and figures for embedding |
| `graphviz` | system | Generate diagrams (dot → SVG/PNG) |
| ImageMagick | system | Image conversion and manipulation |
| Bundled ooxml scripts | — | Unpack/pack/validate DOCX archives |
| Bundled Document library | — | Python API for OOXML editing, comments, tracked changes |

**Not available in this environment** (mentioned in research literature but not usable here): docxtpl, docxcompose, Python-Redlines, docx-revisions, docx-editor, Open XML SDK (.NET), docx4j (Java), Aspose.Words, Mammoth.js, Typst, Ghostscript.

## Feedback loop

**Always read `FEEDBACK.md` when loading this skill.** It captures observed issues and successful patterns.

During use: detect quality drops or pattern failures → check if logged → scope to a category → draft an entry and ask the user before writing → write on approval → compact at 75 entries.

---

## Workflow decision tree

### Reading / analyzing content
Use "Text extraction" or "Raw XML access" below.

### Creating a new document
1. Read **this file** through the design rules section
2. Read [`references/design-system.md`](references/design-system.md) for element taxonomy and style specs
3. Read [`references/architecture-and-layout.md`](references/architecture-and-layout.md) for structure, tables, figures, domain constraints
4. Read [`docx-js.md`](docx-js.md) for implementation syntax (docx-js library)
5. Optionally read [`references/quality-pipeline.md`](references/quality-pipeline.md) for QA checks

### Editing an existing document
1. Read [`ooxml.md`](ooxml.md) for the Document library API and XML patterns
2. Follow the editing workflow below

### Redlining (tracked changes on someone else's document)
1. Follow the "Redlining workflow" below

### Making an existing document look more professional
1. Read [`references/design-system.md`](references/design-system.md) to understand what "professional" means
2. Read [`references/quality-pipeline.md`](references/quality-pipeline.md) to audit the document
3. Apply fixes using the editing workflow

---

## Reference routing table

Read reference files based on what the task requires. Don't bulk-read everything — pick what's relevant.

| Task | Read |
|---|---|
| Creating any new document | `references/design-system.md` + `references/architecture-and-layout.md` + `docx-js.md` |
| NIH grant, manuscript, legal doc | `references/architecture-and-layout.md` § Domain constraints |
| Designing tables or choosing table vs list | `references/architecture-and-layout.md` § Tables |
| Adding figures, callouts, sidebars | `references/architecture-and-layout.md` § Figures and visual elements |
| Choosing styles, fonts, colors, spacing | `references/design-system.md` |
| Running QA on a finished document | `references/quality-pipeline.md` |
| Choosing a profile quickly (business vs academic vs technical vs NIH) | `references/style-profiles.md` |
| Fast DOCX creation from Markdown | `references/pandoc-fast-path.md` |
| Document already contains tracked changes or comments | `references/tracked-changes.md` |
| Generating NIH grant section structure (Specific Aims / Research Strategy / Biosketch) | `references/grant-scaffolds.md` |
| Running or extending regression tests | `references/regression-testing.md` |
| Running automated QA checks on a finished document | `references/quality-pipeline.md` — then run `python scripts/qa/run_qa.py <file.docx>` |
| Comparing output against golden references | `assets/reference-outputs/README.md` — render PNGs are in `assets/reference-outputs/*/` |
| Editing or redlining an existing doc | `ooxml.md` |
| Understanding DOCX internals | `ooxml.md` § Technical guidelines |

---

## Design intelligence: quick-reference rules

These rules apply to **every** document you create. They're the difference between "AI-generated" and "professionally designed." Internalize these; detailed specs are in the reference files.

### The #1 rule: styles, not direct formatting

Every paragraph gets a named style. Every heading uses a heading style with outline level set. Direct formatting (manually setting font/size/bold on runs) is allowed only for inline emphasis. If you're setting `font` or `size` on a TextRun for anything other than italic/bold emphasis, you're doing it wrong — define or use a style instead.

Why this matters: direct formatting creates "style debt." It decouples the document from its style system, makes future edits unpredictable, and breaks TOC/navigation features.

### Domain classification

Classify the document's domain early — it determines margins, fonts, spacing, heading depth, and navigation.

| Signal | Domain | Key constraints |
|---|---|---|
| "grant", "specific aims", "NIH", "R01" | NIH grant | Use `assets/style-specs/nih_grant_basic.json` + `references/grant-scaffolds.md`. ≥11pt, ≥0.5in margins, ≤15 cpi, ≤6 lpi, NO headers/footers |
| "manuscript", "methods", "results", "journal" | Scientific manuscript | 12pt Times, double-spaced, 1in margins, ≤3 heading levels |
| "report", "strategy", "proposal", "quarterly" | Business report | 11pt sans, 1.15 spacing, branded, TOC for 6+ pages |
| "procedure", "specification", "technical" | Technical report | Callouts, code blocks, numbered procedures |
| "contract", "agreement", "article", "section" | Legal | Double-spaced body, multilevel numbering, signature blocks |

### Heading scale (business/technical default)

| Element | Size | Weight | Space before / after |
|---|---|---|---|
| Title | 24–30pt | Semibold | 0 / 12–18 |
| Heading 1 | 16–18pt | Bold | 18–24 / 6–10 |
| Heading 2 | 13–14pt | Bold | 12–18 / 4–8 |
| Heading 3 | 11–12pt | Bold | 10–12 / 4–6 |
| Body | 11pt | Regular | 0 / 6 |

Pick specific values from these ranges and use them consistently. Don't mix and match.

### Vertical rhythm

Pick a base unit (6pt is standard) and express all spacing as multiples: 0, 2, 4, 6, 8, 12, 18, 24. Headings, captions, tables, and figures all snap to this grid. Random spacing values (10pt here, 7pt there, blank lines elsewhere) are the single most visible "amateur doc" tell.

### Navigation decisions

| Component | Include when |
|---|---|
| Table of contents | Pages ≥ 6, OR headings ≥ 12, OR > 2 heading levels |
| Executive summary | Audience is a decision-maker; content has recommendations/costs/risks |
| Appendices | Large tables, raw data, or compliance materials would disrupt narrative |
| List of figures/tables | ≥ 5 figures or ≥ 5 tables |

### Heading depth

Default max = 3 (H1–H3). If you need H4, use it only as a run-in heading. If you need H5/H6, restructure instead — split the section, use a table, or convert micro-headings to bold lead-ins.

### Table vs list vs prose

| Use | When |
|---|---|
| Table | Data has ≥2 dimensions; ≥2 attributes compared across ≥3 items; values need alignment |
| Bullet list | 3–9 short items; ordering doesn't matter |
| Numbered list | Ordering matters (steps, priority, chronology) |
| Prose | Relationships matter more than fields; narrative or argument |

### Fonts

Limit to **two font families** — one for headings, one for body (or one family in different weights). Mixing fonts inconsistently is the "LLM doc smell."

- **Business/technical:** Aptos/Calibri/Arial for body; same or matching sans for headings; Consolas for code
- **Academic:** Times New Roman 12pt (or journal-required font)
- **NIH grants:** Arial, Helvetica, Palatino Linotype, or Georgia (≥11pt)

### Color

Use color sparingly — typically a single accent for H1/H2 text, table header backgrounds, and rule lines. Muted blues (#1F4E79, #2F5597) are safe defaults. Avoid multi-colored headings, heavy fills, and borders everywhere.

### The "amateur doc" smell test

| Smell | Fix |
|---|---|
| Everything is "Normal" with manual bolding | Use named styles for everything |
| Blank lines for spacing | Use paragraph SpaceBefore/SpaceAfter |
| Tables look like Excel dumps | Header shading, increased padding, minimal borders |
| Mixed fonts across paragraphs | Two font families max, theme-driven |
| No TOC on a 10-page report | Add TOC + page numbers |
| Figures randomly sized | Consistent widths, caption style, cross-references |

---

## Reading and analyzing content

### Text extraction

Convert to markdown using pandoc for readable text with structure preserved:

```bash
pandoc --track-changes=all path-to-file.docx -o output.md
# Options: --track-changes=accept/reject/all
```

### Raw XML access

For comments, complex formatting, document structure, embedded media, and metadata — unpack and read raw XML.

#### Unpacking a file
`python ooxml/scripts/unpack.py <office_file> <output_directory>`

#### Key file structures
- `word/document.xml` — main document contents
- `word/styles.xml` — style definitions
- `word/comments.xml` — comments referenced in document.xml
- `word/numbering.xml` — list numbering definitions
- `word/media/` — embedded images and media files
- Tracked changes use `<w:ins>` (insertions) and `<w:del>` (deletions) tags

---

## Creating a new Word document

Use **docx-js** (JavaScript, pre-installed as `docx` npm package). Before writing any code:

1. **Read [`docx-js.md`](docx-js.md)** completely — it covers syntax, critical formatting rules, and common pitfalls.
2. **Read [`references/design-system.md`](references/design-system.md)** for the element taxonomy and style specifications. Choose a style system (academic, business, or technical) and apply it consistently.
3. **Read [`references/architecture-and-layout.md`](references/architecture-and-layout.md)** for structure patterns, table design, figure placement, and domain-specific constraints.

### Creation workflow

1. **Classify domain** — determine which style profile applies (see domain classification above)
2. **Plan structure** — outline the document tree (front matter, body sections, back matter), decide on navigation components (TOC, exec summary, appendices)
3. **Select styles** — use one of the JSON style specs from `references/design-system.md` as your starting point. Map every element to a named style.
4. **Generate** — write the docx-js code. Every paragraph gets a style. Tables get table styles. Lists use proper numbering config. No direct formatting except inline emphasis.
5. **Validate** — check against the QA rules in `references/quality-pipeline.md` if high-fidelity output is needed.

### Fast creation path: Pandoc (Markdown → DOCX)

If the document is structurally simple (headings, paragraphs, lists, basic tables, inline figures), use the **Pandoc fast path**.

You get a styled DOCX in seconds by pairing Markdown with a prebuilt **reference DOCX**.

Read: `references/pandoc-fast-path.md`

**Command (copy/paste):**

```bash
pandoc input.md \
  --reference-doc=assets/pandoc/reference_business_report_modern.docx \
  --toc --toc-depth=2 \
  -o output.docx
```

**Profiles (reference docs):**
- Business: `assets/pandoc/reference_business_report_modern.docx`
- Technical: `assets/pandoc/reference_technical_report_engineering.docx`
- Academic: `assets/pandoc/reference_academic_manuscript_generic.docx`
- NIH: `assets/pandoc/reference_nih_grant_basic.docx`

If you change the JSON style specs and want to regenerate the reference docs:

```bash
python scripts/build_pandoc_reference.py --all
```

### Key docx-js rules (read full details in docx-js.md)

- Never use `\n` for line breaks — always separate Paragraph elements
- Never use unicode bullets — always use numbering config with `LevelFormat.BULLET`
- PageBreak must always be inside a Paragraph
- ImageRun requires `type` parameter
- Set column widths at both table level AND cell level
- Use `ShadingType.CLEAR` (never `ShadingType.SOLID`) for cell shading
- Override built-in heading styles using exact IDs: "Heading1", "Heading2", etc.
- Set `outlineLevel` on heading styles for TOC to work

---

## Editing an existing Word document

Use the **Document library** (Python, bundled at `scripts/document.py`). Before editing:

1. **Read [`ooxml.md`](ooxml.md)** completely — it covers the Document library API, XML patterns, and tracked change patterns.

### Editing workflow

1. Unpack: `python ooxml/scripts/unpack.py <office_file> <output_directory>`
2. Create and run a Python script using the Document library (see ooxml.md)
3. Pack: `python ooxml/scripts/pack.py <input_directory> <office_file>`

---

## Redlining workflow (tracked changes)

For reviewing someone else's document or any legal/academic/business document edit. **CRITICAL**: implement ALL changes systematically.

**Batching strategy**: group 3–10 related changes per batch. Test each batch before moving to the next.

**Principle: minimal, precise edits.** Only mark text that actually changes. Break replacements into: [unchanged text] + [deletion] + [insertion] + [unchanged text]. Preserve the original run's RSID for unchanged text.

Example — changing "30 days" to "60 days" in a sentence:
```python
# BAD - Replaces entire sentence
'<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del><w:ins><w:r><w:t>The term is 60 days.</w:t></w:r></w:ins>'

# GOOD - Only marks what changed, preserves original <w:r> for unchanged text
'<w:r w:rsidR="00AB12CD"><w:t>The term is </w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del><w:ins><w:r><w:t>60</w:t></w:r></w:ins><w:r w:rsidR="00AB12CD"><w:t> days.</w:t></w:r>'
```

### Tracked changes workflow

1. **Get markdown representation**:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **Identify and group changes**: Review the document and identify ALL changes needed, organizing them into logical batches:

   **Location methods** (for finding text in XML):
   - Section/heading numbers (e.g., "Section 3.2", "Article IV")
   - Paragraph identifiers if numbered
   - Grep patterns with unique surrounding text
   - Document structure (e.g., "first paragraph", "signature block")
   - **DO NOT use markdown line numbers** — they don't map to XML structure

   **Batch organization** (group 3–10 related changes per batch):
   - By section: "Batch 1: Section 2 amendments", "Batch 2: Section 5 updates"
   - By type: "Batch 1: Date corrections", "Batch 2: Party name changes"
   - By complexity: simple text replacements first, then structural changes
   - Sequential: "Batch 1: Pages 1–3", "Batch 2: Pages 4–6"

3. **Read documentation and unpack**:
   - **MANDATORY**: Read [`ooxml.md`](ooxml.md) completely. Pay special attention to "Document Library" and "Tracked Change Patterns."
   - Unpack: `python ooxml/scripts/unpack.py <file.docx> <dir>`
   - Note the suggested RSID from the unpack script

4. **Implement changes in batches**: For each batch of related changes:

   **a. Map text to XML**: grep for text in `word/document.xml` to verify how text is split across `<w:r>` elements.

   **b. Create and run script**: use `get_node` to find nodes, implement changes, then `doc.save()`. See **"Document Library"** section in ooxml.md for patterns.

   **Note**: always grep `word/document.xml` immediately before writing a script to get current line numbers — they change after each run.

5. **Pack**: `python ooxml/scripts/pack.py unpacked reviewed-document.docx`

6. **Verify**:
   ```bash
   pandoc --track-changes=all reviewed-document.docx -o verification.md
   grep "original phrase" verification.md   # should NOT find it
   grep "replacement phrase" verification.md # should find it
   ```

### Handling documents that already contain tracked changes/comments

Use this when your input DOCX already includes revisions (e.g., from a collaborator) and you need to **inspect** or **resolve** them before adding new edits.

1. **Report what's in the document**:
   ```bash
   python scripts/tracked_changes_report.py input.docx --output changes.json --pretty
   ```
   Review `changes.json` for:
   - Insertions/deletions by author/date
   - Formatting changes (`...PrChange`) that can silently alter appearance
   - Comments + the text range they attach to

2. **Accept/reject existing revisions** (optional, but recommended before you add new tracked changes):
   ```bash
   # Accept everything
   python scripts/tracked_changes_resolve.py input.docx --accept-all -o accepted.docx

   # Reject everything
   python scripts/tracked_changes_resolve.py input.docx --reject-all -o rejected.docx

   # Accept only changes from a specific author
   python scripts/tracked_changes_resolve.py input.docx --accept --author "Jane Doe" -o jane_accepted.docx

   # Reject a specific change id
   python scripts/tracked_changes_resolve.py input.docx --reject --id 42 -o reject_42.docx
   ```

3. **Resolve or delete comments**:
   ```bash
   # Mark comments as resolved (requires commentsExtended.xml)
   python scripts/tracked_changes_resolve.py input.docx --resolve-comments -o comments_resolved.docx

   # Delete comments (and their anchors)
   python scripts/tracked_changes_resolve.py input.docx --delete-comments -o comments_deleted.docx
   ```

4. **Then** apply your own edits (tracked or clean) using the Document Library / OOXML workflow.

Read: `references/tracked-changes.md` for the OOXML model, gotchas, and safe patterns when adding new changes on top of existing ones.

---

## Converting documents to images

For visual analysis, render DOCX → PDF → JPEG:

```bash
soffice --headless --convert-to pdf document.docx && pdftoppm -jpeg -r 150 document.pdf page
```

Options: `-r 150` (DPI), `-f N` (first page), `-l N` (last page), `-png` for PNG format.

---

## Generating figures and diagrams for documents

Charts and diagrams can be generated programmatically and embedded in documents:

```bash
# matplotlib chart → PNG
python3 -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.savefig('chart.png', dpi=300, bbox_inches='tight')"

# graphviz diagram → PNG
echo 'digraph { A -> B -> C }' | dot -Tpng -o diagram.png
```

Embed the resulting images via docx-js `ImageRun` (always specify `type` parameter) or via python-docx `document.add_picture()`.

---

## Code style guidelines

When generating code for DOCX operations: write concise code, avoid verbose variable names, avoid unnecessary print statements.
