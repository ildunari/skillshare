# Regression testing

The repo includes a lightweight regression test runner: `tests/regression_test.py`.

It exists to prevent “silent” breaks in the two areas that tend to regress when changing layout/style code:
- **Cover pages / section breaks** (page numbering restarts, header/footer bindings)
- **Tables** (borders and repeating header rows)

## What it does

When you run the test, it:
1. Calls `node scripts/create_template.js` to generate one DOCX per style (currently `academic`, `business`, `technical`).
2. Opens the DOCX as a zip and reads OOXML parts.
3. Asserts invariants:
   - **Business / technical** templates have **≥2 sections** (cover + body), and the last section restarts page numbering at 1 (`w:pgNumType w:start='1'`).
   - Templates contain at least one table.
   - For tables with visible borders and ≥2 rows:
     - First row is a repeating header (`w:tblHeader` in first row’s `w:trPr`).
     - No vertical inside borders (`insideV` should be `nil/none`).
   - Business template: the body section’s default header part contains the word `Confidential` (basic header/footer wiring sanity).

## Run it

From repo root:

```bash
python tests/regression_test.py
```

Expected output on success:

```text
All regression tests passed.
```

## If it fails

You’ll get one or more lines like:

```text
[FAIL] business: Visible-bordered data table is missing repeating header row (w:tblHeader).
```

Fix strategy:
1. **Regenerate the template by hand** to reproduce the failure:
   ```bash
   node scripts/create_template.js --style business --output /tmp/repro.docx
   ```
2. **Unzip and inspect** the relevant OOXML:
   ```bash
   python ooxml/scripts/unpack.py /tmp/repro.docx /tmp/repro
   # inspect /tmp/repro/word/document.xml and /tmp/repro/word/header*.xml
   ```
3. If the failure is table-related, search for `w:tblHeader`, `w:tblBorders`, and `w:insideV`.
4. If the failure is cover/section-related, search for `w:sectPr` and `w:pgNumType`.

## Add new cases

This test runner is intentionally dependency-free (no pytest). To add coverage:

1. Add a new `test_*` function that takes `(style, docx_path)` and returns a list of failures.
2. Call it from `main()`.

Common extensions:
- **NIH profile**: after adding `nih_grant_basic`, you can include it in the style loop and assert “no header/footer content” invariants.
- **Pandoc fast path**: generate a small markdown → docx sample with `--reference-doc`, then verify key style names appear in `word/styles.xml`.
- **Tracked changes**: add a fixture docx with known `w:ins/w:del` and verify `scripts/tracked_changes_resolve.py` produces the expected flattened output.
