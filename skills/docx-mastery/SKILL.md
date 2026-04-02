---
name: "Word Document Mastery"
description: >
  Professional creation, editing, formatting, analysis, and redlining of Word (.docx) documents.
  Use this skill whenever the user mentions Word docs, .docx files, grants, manuscripts,
  reports, memos, letters, or any task that produces a professional document deliverable.
  Also use when the user asks to fix formatting, add tracked changes, review a document,
  create a template, or extract content from a Word file. Triggers on:
  "write a report", "make a Word doc", "create a memo", "format this as a grant",
  "add tracked changes", "fix the formatting", "review this document",
  "create a letter", "NIH grant", "manuscript", "redline this", or any request
  where the deliverable is a .docx file or involves editing one.
compatibility: >
  Requires python-docx and/or docx (npm). LibreOffice + Poppler for visual rendering.
  pandoc for Markdown → DOCX fast path. See Dependencies section.
---

<!-- Merged from "doc" and "docx-enhanced". Both source directories archived. -->

# Word Document Mastery

Professional Word documents are defined by systematic consistency across four layers: information architecture (predictable sectioning, navigable front/back matter), style system (named styles covering everything, no direct formatting), page geometry (margins, headers/footers, sections used intentionally), and data presentation (tables that read like publications, figures with captions). This skill handles both the mechanical workflows and the design decisions.

## Workflow decision tree

### Reading / analyzing content
Use "Text extraction" or "Raw XML access" below.

### Creating a new document
1. Read this file through the design rules section
2. Read [`references/design-system.md`](references/design-system.md) for element taxonomy and style specs
3. Read [`references/architecture-and-layout.md`](references/architecture-and-layout.md) for structure, tables, figures, domain constraints
4. Read [`docx-js.md`](docx-js.md) for implementation syntax (docx-js library)
5. Optionally read [`references/quality-pipeline.md`](references/quality-pipeline.md) for QA checks

### Editing an existing document
1. Read [`ooxml.md`](ooxml.md) for the Document library API and XML patterns
2. Follow the editing workflow below

### Redlining (tracked changes on someone else's document)
Follow the Redlining workflow section below.

### Making an existing document look more professional
1. Read [`references/design-system.md`](references/design-system.md) to understand what "professional" means
2. Read [`references/quality-pipeline.md`](references/quality-pipeline.md) to audit the document
3. Apply fixes using the editing workflow

---

## Feedback loop

**Always read `FEEDBACK.md` when loading this skill.** It captures observed issues and successful patterns.

During use: detect quality drops or pattern failures → check if logged → scope to a category → draft an entry and ask the user before writing → write on approval → compact at 75 entries.

---

## Reference routing table

Read reference files based on what the task requires. Don't bulk-read everything.

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
| NIH grant section structure | `references/grant-scaffolds.md` |
| Running regression tests | `references/regression-testing.md` |
| Running automated QA | `references/quality-pipeline.md` — then `python scripts/qa/run_qa.py <file.docx>` |
| Editing or redlining an existing doc | `ooxml.md` |
| Understanding DOCX internals | `ooxml.md` § Technical guidelines |

---

## Design intelligence: quick-reference rules

These rules apply to every document you create.

### The #1 rule: styles, not direct formatting

Every paragraph gets a named style. Every heading uses a heading style with outline level set. Direct formatting is allowed only for inline emphasis. If you're setting `font` or `size` on a TextRun for anything other than italic/bold, define or use a style instead.

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

### Vertical rhythm

Pick a base unit (6pt is standard) and express all spacing as multiples: 0, 2, 4, 6, 8, 12, 18, 24. Headings, captions, tables, and figures all snap to this grid.

### Navigation decisions

| Component | Include when |
|---|---|
| Table of contents | Pages ≥ 6, OR headings ≥ 12, OR > 2 heading levels |
| Executive summary | Audience is a decision-maker; content has recommendations/costs/risks |
| Appendices | Large tables, raw data, or compliance materials would disrupt narrative |
| List of figures/tables | ≥ 5 figures or ≥ 5 tables |

### Table vs list vs prose

| Use | When |
|---|---|
| Table | Data has ≥2 dimensions; ≥2 attributes compared across ≥3 items |
| Bullet list | 3–9 short items; ordering doesn't matter |
| Numbered list | Ordering matters (steps, priority, chronology) |
| Prose | Relationships matter more than fields; narrative or argument |

### Fonts

Limit to two font families — one for headings, one for body.

- **Business/technical:** Aptos/Calibri/Arial for body; Consolas for code
- **Academic:** Times New Roman 12pt (or journal-required font)
- **NIH grants:** Arial, Helvetica, Palatino Linotype, or Georgia (≥11pt)

### The "amateur doc" smell test

| Smell | Fix |
|---|---|
| Everything is "Normal" with manual bolding | Use named styles for everything |
| Blank lines for spacing | Use paragraph SpaceBefore/SpaceAfter |
| Tables look like Excel dumps | Header shading, increased padding, minimal borders |
| Mixed fonts across paragraphs | Two font families max, theme-driven |
| No TOC on a 10-page report | Add TOC + page numbers |

---

## Reading and analyzing content

### Text extraction

```bash
python -m markitdown path-to-file.docx
# Or with pandoc (preserves structure, handles tracked changes):
pandoc --track-changes=all path-to-file.docx -o output.md
```

### Raw XML access

For comments, complex formatting, document structure, embedded media, and metadata — unpack and read raw XML.

```bash
python ooxml/scripts/unpack.py <office_file> <output_directory>
```

Key file structures:
- `word/document.xml` — main document contents
- `word/styles.xml` — style definitions
- `word/comments.xml` — comments referenced in document.xml
- `word/numbering.xml` — list numbering definitions
- `word/media/` — embedded images and media files
- Tracked changes use `<w:ins>` (insertions) and `<w:del>` (deletions) tags

---

## Creating a new Word document

Use **docx-js** (JavaScript, `docx` npm package). Before writing any code, read:
1. [`docx-js.md`](docx-js.md) — syntax, critical formatting rules, and common pitfalls
2. [`references/design-system.md`](references/design-system.md) — element taxonomy and style specifications
3. [`references/architecture-and-layout.md`](references/architecture-and-layout.md) — structure patterns, table design, figure placement, domain-specific constraints

### Creation workflow

1. **Classify domain** — determine which style profile applies
2. **Plan structure** — outline the document tree (front matter, body sections, back matter), decide on navigation components
3. **Select styles** — map every element to a named style
4. **Generate** — write the docx-js code. No direct formatting except inline emphasis.
5. **Validate** — check against QA rules in `references/quality-pipeline.md`

### Fast creation path: Pandoc (Markdown → DOCX)

For structurally simple documents (headings, paragraphs, lists, basic tables, inline figures), use the Pandoc fast path. Read: `references/pandoc-fast-path.md`

```bash
pandoc input.md \
  --reference-doc=assets/pandoc/reference_business_report_modern.docx \
  --toc --toc-depth=2 \
  -o output.docx
```

Profiles (reference docs):
- Business: `assets/pandoc/reference_business_report_modern.docx`
- Technical: `assets/pandoc/reference_technical_report_engineering.docx`
- Academic: `assets/pandoc/reference_academic_manuscript_generic.docx`
- NIH: `assets/pandoc/reference_nih_grant_basic.docx`

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

Use the **Document library** (Python, bundled at `scripts/document.py`). Before editing, read [`ooxml.md`](ooxml.md) completely.

### Editing workflow

1. Unpack: `python ooxml/scripts/unpack.py <office_file> <output_directory>`
2. Create and run a Python script using the Document library (see ooxml.md)
3. Pack: `python ooxml/scripts/pack.py <input_directory> <office_file>`

---

## Redlining workflow (tracked changes)

For reviewing someone else's document or any legal/academic/business document edit.

**Principle: minimal, precise edits.** Only mark text that actually changes. Break replacements into: [unchanged text] + [deletion] + [insertion] + [unchanged text]. Preserve the original run's RSID for unchanged text.

**Batching strategy**: group 3–10 related changes per batch. Test each batch before the next.

### Workflow

1. **Get markdown representation**:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **Identify and group changes**: Review the document and identify ALL changes needed, organizing them into logical batches by section or type.

3. **Read documentation and unpack**:
   - **MANDATORY**: Read [`ooxml.md`](ooxml.md) completely, especially "Document Library" and "Tracked Change Patterns"
   - Unpack: `python ooxml/scripts/unpack.py <file.docx> <dir>`

4. **Implement changes in batches**: For each batch:
   - Map text to XML: grep `word/document.xml` for text to verify how text is split across `<w:r>` elements
   - Create and run script using `get_node` to find nodes, implement changes, then `doc.save()`

5. **Pack**: `python ooxml/scripts/pack.py unpacked reviewed-document.docx`

6. **Verify**:
   ```bash
   pandoc --track-changes=all reviewed-document.docx -o verification.md
   ```

### Handling documents that already contain tracked changes/comments

1. **Report what's in the document**:
   ```bash
   python scripts/tracked_changes_report.py input.docx --output changes.json --pretty
   ```

2. **Accept/reject existing revisions** (optional, recommended before adding new tracked changes):
   ```bash
   python scripts/tracked_changes_resolve.py input.docx --accept-all -o accepted.docx
   python scripts/tracked_changes_resolve.py input.docx --reject-all -o rejected.docx
   python scripts/tracked_changes_resolve.py input.docx --accept --author "Jane Doe" -o jane_accepted.docx
   ```

3. **Resolve or delete comments**:
   ```bash
   python scripts/tracked_changes_resolve.py input.docx --resolve-comments -o comments_resolved.docx
   python scripts/tracked_changes_resolve.py input.docx --delete-comments -o comments_deleted.docx
   ```

Read: `references/tracked-changes.md` for the OOXML model and safe patterns.

---

## Visual validation (rendering to images)

For layout review, render DOCX → PDF → images:

```bash
# LibreOffice headless
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir $OUTDIR $INPUT_DOCX
# Or:
soffice --headless --convert-to pdf document.docx

# PDF to PNG/JPEG
pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME
# Or JPEG:
pdftoppm -jpeg -r 150 document.pdf page

# Bundled helper:
python3 scripts/render_docx.py /path/to/file.docx --output_dir /tmp/docx_pages
```

Re-render and inspect every page at 100% zoom before final delivery.

---

## Generating figures and diagrams

```bash
# matplotlib chart → PNG
python3 -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.savefig('chart.png', dpi=300, bbox_inches='tight')"

# graphviz diagram → PNG
echo 'digraph { A -> B -> C }' | dot -Tpng -o diagram.png
```

Embed via docx-js `ImageRun` (always specify `type` parameter) or via python-docx `document.add_picture()`.

---

## Quality expectations

- Deliver a client-ready document: consistent typography, spacing, margins, and clear hierarchy.
- Avoid formatting defects: clipped/overlapping text, broken tables, unreadable characters, or default-template styling.
- Charts, tables, and visuals must be legible with correct alignment.
- Use ASCII hyphens only. Avoid U+2011 (non-breaking hyphen) and other Unicode dashes.
- Citations and references must be human-readable; never leave tool tokens or placeholder strings.

---

## Code style guidelines

Write concise code. Avoid verbose variable names and redundant operations. Avoid unnecessary print statements.

---

## Dependencies

```bash
# Python
uv pip install python-docx pdf2image
# Or:
python3 -m pip install python-docx pdf2image

# Node
npm install docx  # for docx-js creation

# System (macOS)
brew install libreoffice poppler pandoc

# System (Ubuntu/Debian)
sudo apt-get install -y libreoffice poppler-utils pandoc
```

## Environment (temp/output conventions)

- Use `tmp/docs/` for intermediate files; delete when done.
- Write final artifacts under `output/doc/` when working in a project repo.
- Keep filenames stable and descriptive.
