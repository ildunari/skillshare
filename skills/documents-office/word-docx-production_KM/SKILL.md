---
name: "word-docx-production"
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
  pandoc for Markdown → DOCX fast path. markitdown for text extraction. See Dependencies section.
---

<!-- Merged from "doc" and "docx-enhanced". Both source directories archived. -->

# Word DOCX Production

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

## Prerequisite checks

Run this before starting work to catch missing tools early:

```bash
# Python libraries
python3 -c "import docx" 2>/dev/null && echo "python-docx OK" || echo "MISSING: pip install python-docx"
python3 -c "import markitdown" 2>/dev/null && echo "markitdown OK" || echo "MISSING: pip install markitdown"

# System tools
command -v pandoc >/dev/null && pandoc --version | head -1 || echo "MISSING: brew install pandoc"
command -v pdftoppm >/dev/null && echo "poppler OK" || echo "MISSING: brew install poppler"

# LibreOffice — macOS path varies
_soffice() {
  command -v soffice 2>/dev/null \
    || ls /Applications/LibreOffice.app/Contents/MacOS/soffice 2>/dev/null \
    || echo ""
}
[ -n "$(_soffice)" ] && echo "LibreOffice OK" || echo "MISSING: brew install --cask libreoffice"

# Node docx package (only if using docx-js path)
node -e "require('docx')" 2>/dev/null && echo "docx npm OK" || echo "MISSING: npm install docx"
```

If any tool is missing, install it (see Dependencies) before proceeding. Don't skip tools — silent failures produce corrupt or empty output.

---

## Reading and analyzing content

### Text extraction

```bash
# markitdown (preferred — handles tables, lists, inline formatting)
python3 -m markitdown path-to-file.docx

# pandoc fallback (preserves structure, handles tracked changes):
pandoc --track-changes=all path-to-file.docx -o output.md
# Verify: output.md should be non-empty
[ -s output.md ] || echo "WARNING: pandoc produced empty output"
```

### Raw XML access

For comments, complex formatting, document structure, embedded media, and metadata — unpack and read raw XML.

```bash
python ooxml/scripts/unpack.py <office_file> <output_directory>
# Verify unpacked correctly:
[ -f <output_directory>/word/document.xml ] || echo "FAILED: document.xml missing — unpack failed"
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
5. **Run automated QA** — execute the QA script; fix any reported violations before delivery:
   ```bash
   python scripts/qa/run_qa.py "$OUTPUT" 2>&1 | tail -30
   ```
6. **Validate visually** — render and inspect (see Visual validation section)

### Verify output after generation

```bash
# Confirm file was written and is non-trivially sized
OUTPUT=output/doc/my-document.docx
[ -f "$OUTPUT" ] || { echo "FAILED: output file not created"; exit 1; }
SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT")
[ "$SIZE" -gt 4096 ] || echo "WARNING: file is suspiciously small (${SIZE} bytes) — check for generation errors"

# Quick structural integrity check (requires python-docx)
python3 -c "
import docx, sys
try:
    d = docx.Document('$OUTPUT')
    print(f'OK: {len(d.paragraphs)} paragraphs, {len(d.tables)} tables')
except Exception as e:
    print(f'CORRUPT: {e}'); sys.exit(1)
"
```

### Fast creation path: Pandoc (Markdown → DOCX)

For structurally simple documents (headings, paragraphs, lists, basic tables, inline figures), use the Pandoc fast path. Read: `references/pandoc-fast-path.md`

```bash
# Verify reference doc exists before running
REF=assets/pandoc/reference_business_report_modern.docx
[ -f "$REF" ] || { echo "MISSING reference doc: $REF"; exit 1; }

pandoc input.md \
  --reference-doc="$REF" \
  --toc --toc-depth=2 \
  -o output.docx

[ -s output.docx ] || echo "FAILED: pandoc produced no output"
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

1. **Check script exists**:
   ```bash
   [ -f ooxml/scripts/unpack.py ] || echo "ERROR: ooxml/scripts/unpack.py not found — skill scripts missing"
   [ -f ooxml/scripts/pack.py ]   || echo "ERROR: ooxml/scripts/pack.py not found"
   ```

2. **Unpack**:
   ```bash
   UNPACK_DIR=$(mktemp -d /tmp/docx_unpack_XXXXXX)
   python ooxml/scripts/unpack.py <office_file> "$UNPACK_DIR"
   [ -f "$UNPACK_DIR/word/document.xml" ] || { echo "FAILED: unpack produced no document.xml"; exit 1; }
   ```

3. Create and run a Python script using the Document library (see ooxml.md)

4. **Pack**:
   ```bash
   python ooxml/scripts/pack.py "$UNPACK_DIR" output.docx
   [ -s output.docx ] || echo "FAILED: pack produced empty output"
   ```

5. **Verify**:
   ```bash
   python3 -c "import docx; d=docx.Document('output.docx'); print(f'OK: {len(d.paragraphs)} paragraphs')"
   ```

6. **Cleanup**: `rm -rf "$UNPACK_DIR"`

---

## Redlining workflow (tracked changes)

For reviewing someone else's document or any legal/academic/business document edit.

**Principle: minimal, precise edits.** Only mark text that actually changes. Break replacements into: [unchanged text] + [deletion] + [insertion] + [unchanged text]. Preserve the original run's RSID for unchanged text.

**Batching strategy**: group 3–10 related changes per batch. Verify each batch before the next.

### Workflow

1. **Get markdown representation**:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   [ -s current.md ] || echo "WARNING: empty output — check pandoc version (needs ≥2.x)"
   ```

2. **Identify and group changes**: Review the document and identify ALL changes needed, organizing them into logical batches by section or type.

3. **Read documentation and unpack**:
   - **MANDATORY**: Read [`ooxml.md`](ooxml.md) completely, especially "Document Library" and "Tracked Change Patterns"
   - Unpack:
     ```bash
     UNPACK_DIR=$(mktemp -d /tmp/docx_redline_XXXXXX)
     python ooxml/scripts/unpack.py <file.docx> "$UNPACK_DIR"
     [ -f "$UNPACK_DIR/word/document.xml" ] || { echo "FAILED: unpack"; exit 1; }
     ```

4. **Implement changes in batches**: For each batch:
   - Map text to XML: grep `word/document.xml` for text to verify how text is split across `<w:r>` elements
   - Create and run script using `get_node` to find nodes, implement changes, then `doc.save()`
   - **After each batch — pack to a staging file and verify before continuing**:
     ```bash
     BATCH_OUT=$(mktemp /tmp/docx_batch_XXXXXX.docx)
     python ooxml/scripts/pack.py "$UNPACK_DIR" "$BATCH_OUT"
     [ -s "$BATCH_OUT" ] || { echo "FAILED: batch pack empty — fix before continuing"; exit 1; }
     python3 -c "import docx; d=docx.Document('$BATCH_OUT'); print(f'batch OK: {len(d.paragraphs)} paragraphs')"
     rm -f "$BATCH_OUT"
     ```

5. **Pack**:
   ```bash
   python ooxml/scripts/pack.py "$UNPACK_DIR" reviewed-document.docx
   [ -s reviewed-document.docx ] || { echo "FAILED: pack empty"; exit 1; }
   ```

6. **Verify**:
   ```bash
   pandoc --track-changes=all reviewed-document.docx -o verification.md
   # Diff to confirm expected changes landed:
   diff current.md verification.md | head -40
   ```

7. **Cleanup**: `rm -rf "$UNPACK_DIR"`

### Handling documents that already contain tracked changes/comments

1. **Report what's in the document**:
   ```bash
   [ -f scripts/tracked_changes_report.py ] || echo "WARNING: script missing"
   python scripts/tracked_changes_report.py input.docx --output changes.json --pretty
   ```

2. **Accept/reject existing revisions** — **destructive: confirm with user before running** (irreversible without the original file):
   ```bash
   python scripts/tracked_changes_resolve.py input.docx --accept-all -o accepted.docx
   python scripts/tracked_changes_resolve.py input.docx --reject-all -o rejected.docx
   python scripts/tracked_changes_resolve.py input.docx --accept --author "Jane Doe" -o jane_accepted.docx
   ```

3. **Resolve or delete comments** — **destructive: confirm with user before running**:
   ```bash
   python scripts/tracked_changes_resolve.py input.docx --resolve-comments -o comments_resolved.docx
   python scripts/tracked_changes_resolve.py input.docx --delete-comments -o comments_deleted.docx
   ```

Read: `references/tracked-changes.md` for the OOXML model and safe patterns.

---

## Visual validation (rendering to images)

For layout review, render DOCX → PDF → images:

```bash
# Resolve soffice path (macOS app bundle vs PATH)
SOFFICE=$(command -v soffice 2>/dev/null \
  || echo "/Applications/LibreOffice.app/Contents/MacOS/soffice")
[ -x "$SOFFICE" ] || { echo "ERROR: LibreOffice not found at $SOFFICE"; exit 1; }

OUTDIR=$(mktemp -d /tmp/docx_render_XXXXXX)
INPUT_DOCX="$1"   # pass the docx path
BASENAME=$(basename "$INPUT_DOCX" .docx)

# Convert to PDF
"$SOFFICE" -env:UserInstallation="file:///tmp/lo_profile_$$" \
  --headless --convert-to pdf --outdir "$OUTDIR" "$INPUT_DOCX"
[ -f "$OUTDIR/$BASENAME.pdf" ] || { echo "FAILED: PDF not produced"; exit 1; }

# PDF to PNG (one file per page)
pdftoppm -png -r 150 "$OUTDIR/$BASENAME.pdf" "$OUTDIR/$BASENAME"
ls "$OUTDIR/$BASENAME"*.png 2>/dev/null | wc -l | xargs -I{} echo "{} page(s) rendered"

# Bundled helper (equivalent):
# python3 scripts/render_docx.py /path/to/file.docx --output_dir /tmp/docx_pages
```

Re-render and inspect every page at 100% zoom before final delivery.

**LibreOffice failure recovery**: If `--convert-to pdf` silently produces no output, check `$SOFFICE --version` — older LibreOffice versions (pre-7) have known headless conversion bugs. Update to 7.x or later via `brew upgrade --cask libreoffice`.

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
uv pip install python-docx pdf2image markitdown
# Or:
python3 -m pip install python-docx pdf2image markitdown

# Node
npm install docx  # for docx-js creation

# System (macOS)
brew install poppler pandoc
brew install --cask libreoffice  # note: --cask, not formula

# System (Ubuntu/Debian)
sudo apt-get install -y libreoffice poppler-utils pandoc
```

**macOS note**: LibreOffice installs to `/Applications/LibreOffice.app/`. The `soffice` binary is at `Contents/MacOS/soffice` inside the bundle and may not be on `$PATH`. Use the path resolution pattern in the Visual validation section above.

## Environment (temp/output conventions)

- Use `tmp/docs/` for intermediate files; delete when done.
- Write final artifacts under `output/doc/` when working in a project repo.
- Keep filenames stable and descriptive.
- Always clean up temp unpack dirs (`rm -rf "$UNPACK_DIR"`) after packing.
