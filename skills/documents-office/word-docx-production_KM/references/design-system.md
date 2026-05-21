# Design system reference

Element taxonomy, style specifications, and typographic rules for professional DOCX output.

## Table of contents

1. [Body text rules](#body-text-rules)
2. [Heading scale and spacing](#heading-scale-and-spacing)
3. [Vertical rhythm](#vertical-rhythm)
4. [Fonts and color](#fonts-and-color)
5. [Line length](#line-length)
6. [Element taxonomy](#element-taxonomy)
7. [Style inheritance](#style-inheritance)
8. [Style system JSON specifications](#style-system-json-specifications)

---

## Body text rules

- **Font size:** 10–12pt for long-form reading. 11pt is the modern default.
- **Line spacing (leading):** 120–145% of font size. For 11pt body: 1.15–1.25 multiple (approximately 12.65–13.75pt exact). Single spacing is too tight; 1.5 is too loose.
- **Paragraph spacing:** use `SpaceAfter` in the 4–10pt range. Never use blank lines.
- **Indent rule:** choose *either* first-line indent *or* paragraph spacing, not both. Academic manuscripts use first-line indent (0.5in) with no inter-paragraph spacing. Business/technical documents use paragraph spacing with no first-line indent.
- **Widow/orphan control:** always enabled on body styles.

## Heading scale and spacing

A coherent hierarchy means consistent size, spacing, and behavior across all heading levels.

### Business/technical reports (default)

| Element | Size | Weight | Space before | Space after | Behavior |
|---|---|---|---|---|---|
| Title | 24–30pt | Semibold | 0 | 12–18 | Centered; keep together |
| Heading 1 | 16–18pt | Semibold/Bold | 18–24 | 6–10 | Outline level 1; keep with next; optional page break before |
| Heading 2 | 13–14pt | Semibold/Bold | 12–18 | 4–8 | Outline level 2; keep with next |
| Heading 3 | 11–12pt | Semibold/Bold | 10–12 | 4–6 | Keep with next |
| Body | 11pt | Regular | 0 | 6 | Left-aligned; widow/orphan control |

### Layout rules for headings

- Apply `keep_with_next` on ALL headings to prevent stranding at page bottom
- Consider `page_break_before` for H1 in formal reports (not memos)
- Heading color: use one accent color for H1/H2 (brand-derived or muted blue like #1F4E79 / #2F5597); black for H3

### Academic manuscripts

All headings are 12pt bold (same as body), differentiated by spacing and alignment per journal style. Double-spaced throughout.

### NIH grants

Same as business/technical but with ≥11pt minimum, ≤15 characters per inch, ≤6 lines per vertical inch. No headers or footers in attachments.

## Vertical rhythm

Professional documents feel like they sit on a grid. Approximate rhythm by using a small set of spacing values consistently.

**Rule:** pick a base vertical unit (6pt is standard) and express all spacing as multiples: 0, 2, 4, 6, 8, 12, 18, 24.

Example (business report): body space-after = 6; H3 before 12/after 4; H2 before 18/after 6; H1 before 24/after 8; table caption before 12/after 3; figure caption after 10.

Amateur docs have random spacing (10pt here, 8pt there, blank lines elsewhere) because formatting was applied ad hoc.

## Fonts and color

### Font selection by domain

| Domain | Body | Heading | Code |
|---|---|---|---|
| Business/technical | Aptos, Calibri, or Arial 11pt | Same family or matching sans | Consolas 9.5pt |
| Academic manuscript | Times New Roman 12pt | Same | Courier New 10pt |
| NIH grant | Arial, Helvetica, Palatino Linotype, or Georgia ≥11pt | Same | — |
| Legal | Times New Roman 12pt | Same, bold/caps | — |

**Two font families maximum.** Mixing fonts inconsistently (headings in Calibri, body in Times, tables in Arial) is the most visible "generated doc" tell.

### Professional font combinations for docx-js

- **Arial (headers) + Arial (body)** — most universally supported, clean
- **Times New Roman (headers) + Arial (body)** — classic serif/sans contrast
- **Georgia (headers) + Verdana (body)** — optimized for screen

> **Sandbox font note:** Aptos and Aptos Display are Windows-only (Office 2024+). In the Claude sandbox, LibreOffice headless renders DOCX files using its own font stack — Aptos will silently fall back to Liberation Sans or DejaVu Sans, which affects visual QA renders. When using the `business_report_modern` JSON spec, substitute `"Calibri"` (heading) and `"Calibri"` (body) for any LibreOffice-rendered output; reserve Aptos Display for final Word-rendered deliverables. The fallback array `["Calibri", "Arial"]` in the JSON spec handles this — always use the first fallback when targeting the sandbox renderer.

### Color rules

Use color sparingly — typically a single accent for:
- Heading 1/2 text
- Rule lines or callout accent bars
- Table header background (light tint)

Safe accent defaults: #1F4E79 (dark blue), #2F5597 (medium blue), #404040 (dark gray).

Avoid multi-colored headings, heavy fills, and borders everywhere. Enforce brand colors through the template theme.

## Line length

Average line length should be 45–90 characters including spaces.

- At 11pt sans with 1in margins on letter paper: approximately 70–95 characters (can be slightly long)
- If estimated line length > 90 chars: increase margins or increase line spacing to 1.25
- If estimated line length < 45 chars: reduce margins or increase font size

---

## Element taxonomy

This taxonomy is a design system contract. The agent chooses an element type, applies the matching style, and writes content. Values are baseline for **business/technical reports**; domain-specific overrides are noted.

**Units:** font size in points (pt); page geometry in inches (in); paragraph spacing in points; colors as hex RGB.

| Element / Style ID | Use | Font | Size | Line spacing | Space before/after | Indent | Notes |
|---|---|---|---|---|---|---|---|
| **Title** | Cover page main title | Heading family, semibold | 24–30 | 1.0 | 0 / 12–18 | 0 | Centered; keep together |
| **Subtitle** | Cover page subtitle | Heading family | 14–16 | 1.0–1.1 | 0 / 18–24 | 0 | Centered; muted color |
| **DocMeta** | Author, org, date | Body family | 10–11 | 1.0 | 0 / 6 | 0 | Small caps or muted color |
| **AbstractTitle** | Abstract heading | Body family, semibold | 12–13 | 1.0 | 12 / 6 | 0 | Keep with next |
| **Abstract** | Abstract body | Body family | 11 | 1.15 | 0 / 6 | 0 | No first-line indent |
| **ExecSummaryTitle** | Exec summary heading | Heading family, semibold | 14–16 | 1.0 | 18 / 6 | 0 | Page break before (optional) |
| **ExecSummary** | Exec summary body | Body family | 11 | 1.15 | 0 / 6 | 0 | — |
| **Heading1** | Major section | Heading family, semibold | 16–18 | 1.0 | 18–24 / 6–10 | 0 | Outline level 1; keep with next; accent color |
| **Heading2** | Subsection | Heading family, semibold | 13–14 | 1.0 | 12–18 / 4–8 | 0 | Outline level 2; keep with next |
| **Heading3** | Sub-subsection | Body family, semibold | 11–12 | 1.0 | 10–12 / 4–6 | 0 | Keep with next |
| **Heading4** | Run-in heading | Body family, semibold | 11 | 1.0 | 8 / 2 | 0 | Ends with period, text continues |
| **Body** | Default paragraphs | Body family | 11 | 1.15–1.25 | 0 / 6 | 0 | Left-aligned; widow/orphan |
| **BodyFirst** | First para after heading | Body family | 11 | 1.15 | 0 / 6 | 0 | No first-line indent |
| **BodyCompact** | Tight paragraphs (appendix) | Body family | 10.5 | 1.05–1.15 | 0 / 3 | 0 | — |
| **ListBullet** | Bullet list L1 | Body family | 11 | 1.15 | 0 / 2–4 | L: 0.25in | Hanging indent 0.25in |
| **ListBullet2** | Bullet list L2 | Body family | 11 | 1.15 | 0 / 2 | L: 0.5in | Hanging indent 0.25in |
| **ListNumber** | Numbered list L1 | Body family | 11 | 1.15 | 0 / 2–4 | L: 0.25in | Hanging indent 0.25in |
| **ListNumber2** | Numbered list L2 | Body family | 11 | 1.15 | 0 / 2 | L: 0.5in | — |
| **ProcedureStep** | Numbered procedure | Body family | 11 | 1.15 | 0 / 2 | Hanging 0.25in | Dedicated list numbering |
| **DefTerm** | Definition term | Body family, semibold | 11 | 1.15 | 6 / 0–2 | 0 | Followed by DefBody |
| **DefBody** | Definition body | Body family | 11 | 1.15 | 0 / 4–6 | L: 0.25in | Keep with term |
| **Quote** | Block quote | Body family | 10.5 | 1.15 | 6 / 6 | L: 0.25–0.5in | Left border 2pt accent; light shading optional |
| **CalloutTitle** | Callout box title | Body family, semibold | 11 | 1.0 | 6 / 2 | Pad: 0.15in | Inside 1×1 table with shading |
| **CalloutBody** | Callout box body | Body family | 10.5 | 1.15 | 0 / 6 | Pad: 0.15in | 1×1 table; shading #F3F6FA |
| **CodeBlock** | Code / preformatted | Monospace (Consolas) | 9–10 | 1.0 | 6 / 6 | Pad: 0.15in | Shading #F2F2F2; keep lines together |
| **InlineCode** | Inline code (char style) | Monospace | 9.5–10 | — | — | — | Subtle shading optional |
| **FigureCaption** | Figure caption | Body family | 9.5–10 | 1.0 | 6 / 10–12 | 0 | "Figure N." prefix; keep with figure |
| **TableCaption** | Table caption | Body family | 9.5–10 | 1.0 | 12 / 3–6 | 0 | Above table; keep with next |
| **TblHeader** | Table header cell | Body family, semibold | 10 | 1.0 | — | — | Shading #E8EEF7; bottom border; repeat header |
| **TblBody** | Table body cell | Body family | 10 | 1.0 | — | — | Cell padding 0.06–0.1in; minimal borders |
| **TblNote** | Notes under table | Body family | 9 | 1.0 | 4 / 0 | 0 | Prefix "Note:" |
| **Header** | Running header | Body family | 9 | 1.0 | 0 / 0 | 0 | Optional rule line |
| **Footer** | Page number | Body family | 9 | 1.0 | 0 / 0 | 0 | PAGE/NUMPAGES field |
| **TOC1** | TOC level 1 | Body family | 11 | 1.0 | 0 / 2 | 0 | Tab leader dots; right-aligned page numbers |
| **TOC2** | TOC level 2 | Body family | 10 | 1.0 | 0 / 1 | L: 0.15in | Indent per level |
| **TOC3** | TOC level 3 | Body family | 10 | 1.0 | 0 / 1 | L: 0.3in | — |
| **Bibliography** | Reference list | Body family | 10.5 | 1.15 | 6 / 0 | Hanging: 0.25in | — |
| **FootnoteText** | Footnotes | Body family | 9 | 1.0 | 0 / 0 | 0 | In Word footnote area |
| **AppendixHeading** | Appendix heading | Like Heading1 | Like H1 | Like H1 | Like H1 | 0 | "Appendix A" prefix |

---

## Style inheritance

Build a shallow tree (2 levels deep) to reduce accidental overrides:

```text
Body (base)
├── BodyCompact
├── BodyFirst
├── Quote
├── Callout
└── DefBody

HeadingBase (base)
├── Heading1
├── Heading2
└── Heading3

CaptionBase
├── FigureCaption
└── TableCaption
```

In docx-js, use `basedOn` in style definitions. In OOXML, use `<w:basedOn>`.

---

## Style system JSON specifications

Three complete, implementable style specs. Use as starting points — select one based on domain, then customize.

### Academic manuscript (generic)

Times New Roman 12pt, double-spaced, 1in margins.

```json
{
  "name": "academic_manuscript_generic",
  "page": {
    "size": "Letter",
    "margins_in": { "top": 1.0, "bottom": 1.0, "left": 1.0, "right": 1.0 }
  },
  "fonts": {
    "body": { "family": "Times New Roman", "size_pt": 12 },
    "mono": { "family": "Courier New", "size_pt": 10 }
  },
  "paragraphStyles": {
    "Title": { "font": { "size_pt": 16, "bold": true }, "alignment": "center", "space_after_pt": 12, "line_spacing_multiple": 2.0 },
    "Heading1": { "font": { "size_pt": 12, "bold": true }, "space_before_pt": 24, "space_after_pt": 6, "keep_with_next": true, "outline_level": 1 },
    "Heading2": { "font": { "size_pt": 12, "bold": true }, "space_before_pt": 18, "space_after_pt": 6, "keep_with_next": true, "outline_level": 2 },
    "Heading3": { "font": { "size_pt": 12, "bold": true }, "space_before_pt": 12, "space_after_pt": 6, "keep_with_next": true, "outline_level": 3 },
    "Body": { "font": { "size_pt": 12 }, "first_line_indent_in": 0.5, "space_after_pt": 0, "line_spacing_multiple": 2.0, "widow_control": true },
    "BlockQuote": { "font": { "size_pt": 12 }, "left_indent_in": 0.5, "right_indent_in": 0.5, "space_before_pt": 6, "space_after_pt": 6, "line_spacing_multiple": 2.0 },
    "FigureCaption": { "font": { "size_pt": 10 }, "space_before_pt": 6, "space_after_pt": 12, "keep_together": true },
    "TableCaption": { "font": { "size_pt": 10, "bold": true }, "space_before_pt": 12, "space_after_pt": 3, "keep_with_next": true },
    "References": { "font": { "size_pt": 12 }, "hanging_indent_in": 0.5, "line_spacing_multiple": 2.0 }
  },
  "characterStyles": {
    "Emphasis": { "italic": true },
    "Strong": { "bold": true },
    "InlineCode": { "font": { "family": "Courier New", "size_pt": 10 }, "shading": "F2F2F2" }
  },
  "tableStyles": {
    "TableBase": {
      "font": { "family": "Times New Roman", "size_pt": 11 },
      "cell_padding_pt": { "top": 4, "bottom": 4, "left": 4, "right": 4 },
      "borders": "minimal_horizontal",
      "header_row": { "bold": true, "shading": "EDEDED" },
      "banded_rows": false
    }
  }
}
```

### Business report (modern)

11pt body, 1.15 line spacing, single accent color, running headers.

```json
{
  "name": "business_report_modern",
  "page": {
    "size": "Letter",
    "margins_in": { "top": 1.0, "bottom": 1.0, "left": 0.9, "right": 0.9 }
  },
  "fonts": {
    "heading": { "family": "Aptos Display", "fallback": ["Calibri", "Arial"] },
    "body": { "family": "Aptos", "fallback": ["Calibri", "Arial"], "size_pt": 11 },
    "mono": { "family": "Consolas", "fallback": ["Courier New"], "size_pt": 9.5 }
  },
  "colors": {
    "accent": "#2F5597",
    "mutedText": "#444444",
    "lightFill": "#F2F4F8",
    "tableHeaderFill": "#E9EEF7"
  },
  "paragraphStyles": {
    "Title": { "font": { "size_pt": 30, "bold": true, "family": "heading" }, "alignment": "center", "space_after_pt": 18 },
    "Subtitle": { "font": { "size_pt": 16, "family": "heading" }, "alignment": "center", "space_after_pt": 24, "color": "mutedText" },
    "Heading1": { "font": { "size_pt": 18, "bold": true, "family": "heading" }, "space_before_pt": 24, "space_after_pt": 8, "keep_with_next": true, "outline_level": 1, "color": "accent" },
    "Heading2": { "font": { "size_pt": 14, "bold": true, "family": "heading" }, "space_before_pt": 18, "space_after_pt": 6, "keep_with_next": true, "outline_level": 2 },
    "Heading3": { "font": { "size_pt": 11, "bold": true }, "space_before_pt": 12, "space_after_pt": 4, "keep_with_next": true, "outline_level": 3 },
    "Body": { "font": { "size_pt": 11 }, "space_after_pt": 6, "line_spacing_multiple": 1.15, "widow_control": true },
    "BodyCompact": { "font": { "size_pt": 10.5 }, "space_after_pt": 3, "line_spacing_multiple": 1.05 },
    "Quote": { "font": { "size_pt": 10.5, "italic": true }, "left_indent_in": 0.35, "space_before_pt": 6, "space_after_pt": 6 },
    "Callout": { "font": { "size_pt": 10.5 }, "space_before_pt": 6, "space_after_pt": 6 },
    "TableCaption": { "font": { "size_pt": 10, "bold": true }, "space_before_pt": 12, "space_after_pt": 3, "keep_with_next": true },
    "FigureCaption": { "font": { "size_pt": 9.5 }, "space_after_pt": 10, "keep_together": true }
  },
  "characterStyles": {
    "Emphasis": { "italic": true },
    "Strong": { "bold": true },
    "InlineCode": { "font": { "family": "mono" }, "shading": "lightFill" }
  },
  "tableStyles": {
    "TableModern": {
      "font": { "size_pt": 10.5 },
      "cell_padding_pt": { "top": 6, "bottom": 6, "left": 6, "right": 6 },
      "borders": "light_horizontal",
      "table_look": { "firstRow": true, "bandedRows": true },
      "header_row": { "bold": true, "shading": "tableHeaderFill" },
      "numeric_alignment": "right"
    }
  },
  "headersFooters": {
    "running_header": { "font_size_pt": 9, "content": "ShortTitle — {SectionTitle}" },
    "footer": { "font_size_pt": 9, "content": "Page {PAGE} of {NUMPAGES}" }
  }
}
```

### Technical report (procedures + code + callouts)

```json
{
  "name": "technical_report_engineering",
  "page": {
    "size": "Letter",
    "margins_in": { "top": 1.0, "bottom": 1.0, "left": 0.95, "right": 0.95 }
  },
  "fonts": {
    "body": { "family": "Aptos", "fallback": ["Calibri", "Arial"], "size_pt": 11 },
    "mono": { "family": "Consolas", "fallback": ["Courier New"], "size_pt": 9.5 }
  },
  "paragraphStyles": {
    "Heading1": { "font": { "size_pt": 16, "bold": true }, "space_before_pt": 20, "space_after_pt": 6, "keep_with_next": true, "outline_level": 1 },
    "Heading2": { "font": { "size_pt": 13, "bold": true }, "space_before_pt": 16, "space_after_pt": 6, "keep_with_next": true, "outline_level": 2 },
    "Heading3": { "font": { "size_pt": 11, "bold": true }, "space_before_pt": 12, "space_after_pt": 4, "keep_with_next": true, "outline_level": 3 },
    "Body": { "font": { "size_pt": 11 }, "space_after_pt": 6, "line_spacing_multiple": 1.15, "widow_control": true },
    "ProcedureStep": { "based_on": "Body", "hanging_indent_in": 0.25, "space_after_pt": 2 },
    "NoteCallout": { "based_on": "Body", "space_before_pt": 6, "space_after_pt": 6 },
    "WarningCallout": { "based_on": "Body", "space_before_pt": 6, "space_after_pt": 6 },
    "CodeBlock": { "font": { "family": "mono", "size_pt": 9.5 }, "space_before_pt": 6, "space_after_pt": 6, "line_spacing_multiple": 1.0, "shading": "F2F2F2" },
    "TableCaption": { "font": { "size_pt": 10, "bold": true }, "space_before_pt": 12, "space_after_pt": 3, "keep_with_next": true }
  },
  "characterStyles": {
    "InlineCode": { "font": { "family": "mono", "size_pt": 9.5 }, "shading": "F2F2F2" },
    "UILabel": { "bold": true }
  },
  "tableStyles": {
    "TableTech": {
      "font": { "size_pt": 10.5 },
      "cell_padding_pt": { "top": 5, "bottom": 5, "left": 6, "right": 6 },
      "table_look": { "firstRow": true, "bandedRows": true },
      "header_row": { "bold": true, "shading": "EDEDED" }
    }
  }
}
```

### Translating JSON specs to docx-js code

Map the JSON spec to docx-js `styles.paragraphStyles` and `styles.default.document.run`:

- `size_pt` → `size` in half-points (multiply by 2, e.g., 11pt → `size: 22`)
- `space_before_pt` / `space_after_pt` → `spacing.before` / `spacing.after` in twips (multiply by 20, e.g., 24pt → `480`)
- `line_spacing_multiple` → use `spacing.line` in 240ths (1.15 → `276`)
- `margins_in` → margins in twips (multiply by 1440, e.g., 1.0in → `1440`)
- `outline_level` → `outlineLevel` property on paragraph style (0 for H1, 1 for H2, etc.)
- `keep_with_next` → `keepNext: true`
- `widow_control` → `widowControl: true`
