# Reference outputs

This directory exists to answer one question: **“What does ‘correct’ output look like?”**

For each style profile (business / academic / technical / NIH), you get:

- `*_reference.docx` — Word document you can open in Word/LibreOffice.
- `*_reference.pdf` — rendered PDF for quick viewing / diffing.
- `*_pages/page-1.png` etc — page renders for pixel-level comparisons.

These are meant as **golden references** for agents and QA: when you generate a docx, you can compare typography and layout against these artifacts.

## What's inside each reference doc

Each reference document includes (at minimum):

- Title + short intro
- Heading hierarchy (`Heading 1 → Heading 2 → Heading 3`)
- Body paragraphs (including inline emphasis + inline code)
- Block quote
- Lists (bulleted + numbered)
- A table (header row + 2 data rows)
- A figure (profile-matched sample figure) + caption

## How these were generated

They were generated via Pandoc using the repo’s prebuilt reference documents:

- `assets/pandoc/reference_business_report_modern.docx`
- `assets/pandoc/reference_academic_manuscript_generic.docx`
- `assets/pandoc/reference_technical_report_engineering.docx`
- `assets/pandoc/reference_nih_grant_basic.docx`

Generation pattern:

```bash
pandoc assets/reference-outputs/_reference_source.md \
  --reference-doc=assets/pandoc/reference_<profile>.docx \
  -o assets/reference-outputs/<profile>_reference.docx
```

PDF rendering uses LibreOffice headless; PNGs are produced via `pdftoppm`.

If you want the **docx-js** path instead (for cover pages, custom tables, etc.), treat these as *visual targets* and rely on `scripts/create_template.js` + the QA pipeline.

## What to check when comparing

### Typography
- Correct font family for the profile.
- Correct body size and line spacing.
- Heading scale: sizes, boldness, spacing.

### Layout
- Margins match the profile.
- Paragraph spacing is consistent (no random extra whitespace).

### Tables
- Header row: bold and filled/shaded (where applicable).
- Borders: match profile (grid vs light horizontal vs minimal).
- Cell padding looks intentional (not cramped).

### Figures
- Caption style matches profile.
- Figure is sized to page width and centered.

