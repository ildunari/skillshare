# Architecture and layout reference

Document structure, page layout, table design, figure placement, callout recipes, and domain-specific constraints.

## Table of contents

1. [Document tree](#document-tree)
2. [Heading depth and section balance](#heading-depth-and-section-balance)
3. [Navigation components](#navigation-components)
4. [Organizational patterns](#organizational-patterns)
5. [Page layout and geometry](#page-layout-and-geometry)
6. [Table design](#table-design)
7. [Figures and visual elements](#figures-and-visual-elements)
8. [Domain constraints](#domain-constraints)
9. [Lists and numbering](#lists-and-numbering)

---

## Document tree

Every professional document follows a tree structure:

```text
Document
├── Front matter (optional)
│   ├── Cover / title page
│   ├── Executive summary / abstract
│   └── Table of contents / lists of figures & tables
├── Body
│   ├── Section (H1)
│   │   ├── Subsection (H2)
│   │   │   └── Sub-subsection (H3)
│   │   └── ...
│   └── ...
└── Back matter (optional)
    ├── References
    ├── Appendices
    └── Glossary / abbreviations
```

This lets you enforce constraints like "no orphan heading at page bottom," "TOC if > N headings," and "appendices after references."

---

## Heading depth and section balance

### Depth rules

- **Default max depth = 3 (H1–H3).** PLOS submission guidelines explicitly limit to 3 heading levels.
- Allow H4 only as a run-in heading or for controlled patterns (e.g., "Assumptions." "Limitations." inside a subsection).
- If a section needs H5/H6: refactor. Split the section, or convert micro-headings into bold lead-ins.
- Structural smell test: if you need Heading 5, you probably need a table, a definition list, or a restructuring into fewer sections.

### Section length balance

Readers experience documents as chunks. Professional docs have roughly balanced chunks.

- **H1 target size:** 1–4 pages (report) or 0.5–2 pages (memo)
- **Avoid runts:** don't allow a 15-page section followed by three 1-page sections
- **Min content per heading:** if a heading has < 2 paragraphs or < 150 words, consider merging or converting to a lead-in sentence
- If an H1 section exceeds ~5 pages, add H2 subsections or split into multiple H1 sections

---

## Navigation components

### Decision heuristics

| Component | Include when |
|---|---|
| **Table of contents** | Estimated pages ≥ 6, OR heading count ≥ 12, OR > 2 heading levels used |
| **Executive summary** | Primary audience is a decision-maker; signals: "recommendation," "proposal," "strategy," "cost," "risk," "timeline" |
| **Appendices** | Large tables, raw data, protocol details, or compliance materials would disrupt narrative flow |
| **Glossary** | Defined terms count ≥ 10 and are reused; common in legal/technical docs |
| **List of figures/tables** | Documents with ≥ 5 figures or ≥ 5 tables |

Long docs without navigational scaffolding look like "auto-generated dumps" even if typography is fine.

---

## Organizational patterns

Choose a document "shape" based on content type and audience:

| Pattern | Use when |
|---|---|
| Problem → context → options → recommendation → plan | Business strategy, proposals |
| Background → methods → results → discussion (IMRaD) | Scientific manuscripts |
| Specific Aims → Significance → Innovation → Approach | NIH grants |
| Overview → requirements → design → implementation → operations | Technical reports |
| Chronological narrative | Project updates, incident reports |
| Comparative matrix | Vendor selection, experimental comparisons |

Selection heuristic: if ≥ 30% of headings are verbs → procedural/spec pattern. "Aim 1/2/3" → grant. "Methods/Results/Discussion" → manuscript. Heavily comparative content → comparative matrix.

---

## Page layout and geometry

### Margins by domain

| Domain | Margins | Notes |
|---|---|---|
| NIH grants | ≥ 0.5in all sides | Nothing in margins; letter-sized pages only |
| Academic manuscripts | 1in all sides | Most common convention |
| Business reports | 0.9–1.0in | Can increase to 1.25–1.5in for longer narratives |
| Bound/print documents | Inner (gutter): 0.75–0.9in; outer: 0.5–0.75in | Enable mirror margins |
| Typography-optimized | 1.25–1.5in left/right at 12pt | Wider margins for readable line lengths |

Word's default 1in margins on letter paper produce lines approximately 6.5in wide (80–95 chars at 11pt), which can be slightly long.

### Sections

Sections are the only real page layout primitive in Word. Use a section break whenever any of these changes: margins, orientation, header/footer content, page numbering format, column layout.

Use a **page break** only for "start next page" within a stable layout. Use a **section break** for layout changes. Never fake layout changes with manual spacing.

### Headers, footers, and page numbering

Each section can have a default, even, and first-page header (same for footers).

**Common professional numbering scheme:**
- Front matter: Roman numerals (i, ii, iii) with no page number on title page
- Body: Arabic numerals restarting at 1
- Appendices: continue Arabic or restart per appendix

This requires at least two sections with different page number settings.

**Rules:**
- Professional reports: first page often has no header; body has running header with short title; footer has page number
- NIH grants: **NO headers or footers** in attachments
- For "Page X of Y": use PAGE/NUMPAGES fields. Set `updateFieldsOnOpen` in settings.
- Be cautious with python-docx — it can disturb existing fields if footer paragraphs are overwritten

### Mirror margins (bound documents)

If binding/print facing → enable mirror margins + inside gutter (0.25–0.5in). If purely digital → standard symmetric margins, no gutter.

### Orphans/widows and "keep" controls

| Element | Behavior |
|---|---|
| All headings | `keep_with_next = True` |
| Captions | `keep_with_next = True` (if above table) or `keep_together = True` |
| Code blocks | `keep_lines_together = True` |
| Signature blocks | `keep_lines_together = True` |
| Body text | `widow_control = True` |

---

## Table design

Tables are where most auto-generated DOCX documents look the worst. A professional table is not "cells with borders" — it's a visual encoding of hierarchy.

### Table vs list vs prose

| Use | When |
|---|---|
| **Table** | Data has ≥ 2 dimensions; ≥ 2 attributes compared across ≥ 3 items; values have units/precision; repeated schema (parameter / value / notes) |
| **Bulleted list** | 3–9 short items of similar type; ordering not meaningful |
| **Numbered list** | Ordering matters (steps, priority, chronology); items referenced later |
| **Definition list** | Repeated "term: definition" patterns |
| **Prose** | Relationships matter more than fields; narrative or argument |

**Heuristics:**
- Table with > 8 columns → layout problem. Switch to landscape, split, or convert to smaller tables.
- Cells with long paragraphs → table is a layout crutch. Convert to subheadings + prose.
- If generated content mentions parameters with values → convert to table.
- If content lists tasks to perform → convert to numbered list.

### Professional table typography

Publication-grade Word tables follow these rules:

1. **Header row is visually distinct** — semibold text (10pt), light shaded background (#E8EEF7), single strong bottom rule (not full grid), centered or left-aligned
2. **Body rows are readable** — generous cell padding (6pt internal margins vs Word's cramped defaults), minimal borders (horizontal rules only), consistent alignment: numbers right-aligned, text left-aligned, units centered
3. **Row banding is subtle or absent** — if used, very light zebra shading (2–4% tint). Use for tables with ≥ 6 rows
4. **Table caption exists** — above table, Table Caption style, keep_with_next
5. **Repeat header on multi-page tables** — `tableHeader: true` on first row
6. **No merged cells or nested tables** unless absolutely necessary

### Wide table strategies

Decision order:
1. **Adjust column widths** — fixed for numeric, auto for text
2. **Landscape section** — insert landscape section for the table only
3. **Reduce font** — from 10pt to 9pt inside the table
4. **Split** — repeated header + "continued" labels

Heuristics: columns ≤ 6 and content short → portrait. Columns 7–10 → landscape. Columns > 10 → split, pivot, or move to appendix.

### Table style library

Define a small set of table styles (don't let the agent invent table looks):

| Style ID | Use case | Borders | Header | Banding |
|---|---|---|---|---|
| **TableProfessional** (default) | Standard data tables | Minimal horizontal rules only | Shaded, semibold, bottom rule | None or very light |
| **TableMatrix** | Comparison/evaluation | Light horizontal; stronger rules | Shaded, semibold | Alternating row banding |
| **TableKeyValue** | 2-column key/value | No borders | Left column semibold | None |

### Table accessibility

- Use tables only for data, not page layout (exception: callout box constructs)
- Provide title/caption
- Keep simple and regular — single header row, single header column
- Mark header row to repeat; uncheck "Allow row to break across pages"
- No blank or merged cells. Use dashes/zeros instead.
- Avoid mid-table titles. Split into two tables if needed.

---

## Figures and visual elements

### Inline vs floating images

python-docx supports inline pictures only at the high-level API. Floating/anchored pictures require XML workarounds. docx-js also uses inline images primarily.

**Rule:** treat images as block-level (centered inline) with captions. Don't promise complex wrap layouts. For side-by-side layouts, use a 2-column table (image left, text right).

### Figure placement rules

1. **Width rules** (pick one): full width = 6.0–6.5in on letter with 1in margins; half width = 3.0–3.2in
2. **Alignment:** align to text margins; never random widths
3. **Spacing:** 6pt before figure, 6pt after; caption: 6pt before, 10–12pt after
4. **Caption consistency:** same style and prefix format everywhere ("Figure 1." or "Figure 1:" — pick one)
5. **Avoid orphan captions:** keep_with_next / keep_together between figure and caption
6. **Resolution:** 300 DPI for print; 150 DPI for screen. Never stretch beyond native resolution.

### Generating figures for embedding

Charts and diagrams can be generated programmatically and embedded:

```bash
# matplotlib chart → PNG (available in this environment)
python3 -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.savefig('chart.png', dpi=300, bbox_inches='tight')"

# graphviz diagram → PNG (available in this environment)
echo 'digraph { A -> B -> C }' | dot -Tpng -o diagram.png
```

Embed via docx-js `ImageRun` (always specify `type` parameter) or python-docx `document.add_picture()`.

### Callout boxes (1×1 table construct)

Word text boxes are hard to generate reliably. Use tables instead:

**Callout box recipe:**
- 1×1 table
- Fixed left/right padding (6–10pt)
- Light background shading (#F3F6FA)
- Subtle border (or left border only for accent)
- Callout paragraph style inside
- Stays aligned, resizes with content, breaks predictably

**Sidebar recipe (1×2 table):**
- Left column: thin accent bar (0.12–0.2in) with solid fill
- Right column: sidebar text (Callout style)
- Mimics InDesign-style sidebars without shapes

**Rule:** use callouts for anything labeled NOTE/WARNING/IMPORTANT and style consistently. In technical docs, callouts dramatically increase perceived professionalism.

### Diagrams and charts

For programmatic pipelines, generate diagrams as SVG/PNG externally (Graphviz, matplotlib — both available in this environment) and embed as inline figures with captions. This is more reliable than authoring Word drawing objects.

---

## Domain constraints

### NIH grant attachments (compliance-critical)

| Parameter | Requirement |
|---|---|
| Paper size | 8.5 × 11in (letter), no larger |
| Margins | ≥ 0.5in all sides; nothing in margins |
| Font size | ≥ 11pt |
| Type density | ≤ 15 characters per linear inch |
| Line spacing | ≤ 6 lines per vertical inch |
| Headers/footers | **Do not include** — NIH system adds them during assembly |
| Page limits | Specified per attachment type; NIH maintains a page limits table |
| Recommended fonts | Arial, Georgia, Helvetica, Palatino Linotype |

**Rules:**
- Build an NIH-specific template with compliant margins and font settings
- Enforce line spacing; avoid "exact 10pt at 11pt font" hacks
- Treat page limits as constraints: estimate pages early and allocate content
- NIAID warns against manipulating character density (letter spacing/tracking)
- Figures/tables may use smaller text if legible at 100%
- Structure: Specific Aims (1 page), Research Strategy (Significance → Innovation → Approach), Biosketches

### Scientific manuscripts

- **Generic:** Times New Roman 12pt, double-spaced, 1in margins
- **Journal template mode:** import the journal's `.dotx`/`.docx` and fill styles. Never override with custom styles.
- **Structure:** Abstract, Introduction, Methods, Results, Discussion, References
- Heading depth typically limited to 3 levels
- Some journals disallow multi-column formatting

### Business reports / white papers

- Cover page, branded heading styles, executive summary, consistent table/figure system, running headers/footers
- More tolerance for color and layout, but still restrained
- Template-first approach whenever brand matters
- Style profile: sans-serif, H1 at 18–20pt bold with accent color, body at 11pt 1.15 spacing, 6pt space after

### Technical documentation

- Procedures (numbered lists), callouts (notes/warnings), code blocks, consistent headings
- Accessibility: proper heading styles improve navigation
- Dedicated InlineCode and CodeBlock styles with monospace font
- Parameter tables with consistent formatting

### Legal documents

- Multilevel numbering defined centrally in template
- Defined terms capitalized consistently, sometimes styled (small caps)
- Signature blocks must not split across pages: keep-lines-together + keep-with-next
- Body text double-spaced; headings single-spaced
- Body font: Times New Roman 12pt
- Heading 1: 14pt bold, all caps
- Treat "Defined term:" patterns as definition lists, not just bold text

---

## Lists and numbering

Lists are structurally important and visually diagnostic: if numbered steps don't align and restart correctly, the doc immediately feels generated.

### Agent rules for lists

- **Bullet lists:** dedicated bullet list style (hanging indent, consistent symbol, consistent spacing)
- **Procedure steps:** numbered list style with fixed number alignment and text indent
- **Multilevel numbering:** only when the document demands it (legal outlines, standards). Define once in template, reuse consistently.
- **For high-stakes docs:** define all list styles in the template; the agent only chooses among them

### Implementation reality

python-docx supports applying list styles by naming existing styles ("List Number", "List Bullet"), but numbering behaviors like restarting and multilevel patterns often require understanding the numbering definitions behind those styles.

In docx-js, each `numbering.config` reference creates an independent numbered list. Same reference = continues numbering. Different reference = restarts at 1.
