# Style profiles (quick reference)

This file is a **domain-indexed** cheat sheet so an agent can load *only* the style guidance it needs.

Profiles are defined as JSON in `assets/style-specs/` and consumed by:
- **docx-js** creation (via `scripts/stylekit.js`, `scripts/tablekit.js`, `scripts/coverkit.js`, `scripts/listkit.js`)
- **Matplotlib** figure styling (via `scripts/figures/mpl_style.py`)
- **Pandoc fast path** reference docs (via `scripts/build_pandoc_reference.py` → `assets/pandoc/reference_*.docx`)

---

## Business report

**Use when:** external/internal reports, memos, proposals, exec summaries.

- **Style spec:** `assets/style-specs/business_report_modern.json`
- **Pandoc reference:** `assets/pandoc/reference_business_report_modern.docx`
- **Fonts:** Aptos Display (headings) + Aptos Body (body). Fallback: Calibri/Arial.
- **Page:** Letter, 1.0" margins.
- **Heading scale:** H1 20pt bold (accent color), H2 14pt bold, H3 11pt bold.
- **Body:** 11pt, 1.15 line spacing, 6pt after paragraphs.
- **Palette:** muted text + an accent color for headings and rules.
- **Tables:** `TableModern` — light horizontal rules, header row shading.
- **Cover page:** `scripts/coverkit.js` recipe `business` (title block + key-value meta).
- **Lists:** prefer `listkit.simpleNumbered` or `listkit.simpleBullet`.
- **Figures:** use `scripts/figures/mpl_style.py` with `mpl_style_context("business")`.

**Domain constraints / conventions:**
- Prefer short paragraphs, clear headings, and tables over dense prose.
- Avoid academic double-spacing and first-line indents.

---

## Academic manuscript

**Use when:** papers, theses, manuscripts, academic reports.

- **Style spec:** `assets/style-specs/academic_manuscript_generic.json`
- **Pandoc reference:** `assets/pandoc/reference_academic_manuscript_generic.docx`
- **Fonts:** Times New Roman 12pt body; Courier New 10pt mono.
- **Page:** Letter, 1.0" margins.
- **Heading scale:** H1/H2/H3 = 12pt bold with generous spacing.
- **Body:** 12pt, **double-spaced** (2.0), first-line indent 0.5".
- **Tables:** `TableAcademic` — thin rules, restrained shading, readable captions.
- **Cover page:** `scripts/coverkit.js` recipe `academic` (title + authors + affiliations).
- **Figures:** `mpl_style_context("academic")`.

**Domain constraints / conventions:**
- Default to double-spacing unless a journal/PI says otherwise.
- Use numbered figure/table captions and keep them close to the object.

---

## Technical engineering report

**Use when:** specs, design docs, runbooks, lab protocols, engineering reports.

- **Style spec:** `assets/style-specs/technical_report_engineering.json`
- **Pandoc reference:** `assets/pandoc/reference_technical_report_engineering.docx`
- **Fonts:** Aptos 11pt body (fallback Calibri/Arial), Consolas 9.5pt mono.
- **Page:** Letter, ~0.95" left/right, 1.0" top/bottom.
- **Heading scale:** H1 16pt bold, H2 13pt bold, H3 11pt bold.
- **Body:** 11pt, 1.15 line spacing.
- **Callouts:** `NoteCallout`, `WarningCallout` paragraph styles.
- **Tables:** `TableEngineering` — clear header row + grid tuned for technical data.
- **Cover page:** `scripts/coverkit.js` recipe `technical` (title + document meta).
- **Lists:** procedures should use `listkit.procedureNumbered`.
- **Figures:** `mpl_style_context("technical")`.

**Domain constraints / conventions:**
- Code blocks: use `CodeBlock` / `InlineCode`.
- Prefer labeled steps + expected outputs.

---

## NIH grant

**Use when:** NIH-style proposals (Specific Aims, Research Strategy), attachments.

- **Style spec:** `assets/style-specs/nih_grant_basic.json`
- **Pandoc reference:** `assets/pandoc/reference_nih_grant_basic.docx`
- **Fonts:** Arial 11pt body (NIH-allowed family) + Courier New 10pt mono.
- **Page:** Letter, **0.5" margins**.
- **Body:** 11pt, 1.15 line spacing, minimal paragraph spacing.
- **Tables:** `TableNIH` — readable, conservative styling (avoid tiny text).
- **Cover page:** typically not used for NIH attachments. If you need a front matter page, use `coverkit` `minimal` recipe and **do not** add headers/footers.
- **Figures:** use `mpl_style_context("nih_grant_basic")`.

**NIH constraints to keep in mind:**
- **Font size:** ≥11pt for common NIH-allowed fonts (Arial/Georgia/Palatino Linotype). Don’t use condensed/narrow fonts.
- **Margins:** ≥0.5" all around.
- **Text density:** don’t compress line spacing; keep readability.
- **Headers/footers:** avoid running headers/footers for attachments unless explicitly allowed; don’t add “clever” space-saving tricks.

**Content scaffolding:** see `references/grant-scaffolds.md`.

---

## Legal

Not yet a dedicated profile. Use `business_report_modern` as a base:
- Increase body spacing slightly.
- Avoid accent colors.
- Use numbered headings and consistent clause numbering (`listkit.legalOutline`).
