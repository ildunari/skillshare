# Evaluation harness: 10 mixed residual findings

Use this as a manual test for the skill. A successful run groups related items, asks only high-impact/low-confidence questions, uses OfficeCLI commands rather than `python-docx` or `python-pptx`, validates after structural batches, and emits the required JSON report.

## Test prompt

```text
Use fixing-office-accessibility on ./fixtures/stage4-demo.docx and ./fixtures/stage4-demo.pptx. The residual manifests are below. Fix high-confidence low-impact items, ask me about ambiguous high-impact changes in batches, and write a JSON report.
```

## Manifest payloads

`schemas/input-manifest.schema.json` requires a single-document root (`document_path`, `document_type`, `findings`). Below are two separate manifests — feed them to the skill one at a time, not as an envelope. The combined `documents: [...]` shape from earlier drafts of this file does NOT validate.

### DOCX manifest (`./fixtures/stage4-demo.docx.manifest.json`)

```json
{
  "schema_version": "1.0.0",
  "document_path": "./fixtures/stage4-demo.docx",
  "document_type": "docx",
  "findings": [
        {
          "id": "E-D-001",
          "rule_id": "WORD_HEADING_SKIPPED",
          "severity": "warning",
          "location": "/body/p[5]",
          "current_value": {"text": "Eligibility", "style": "Subtitle"},
          "suggested_value": {"style": "Heading2"},
          "confidence": 0.86,
          "why_human_needed": "Visual heading could be semantic.",
          "related_findings_ids": ["E-D-002"]
        },
        {
          "id": "E-D-002",
          "rule_id": "WORD_HEADING_SKIPPED",
          "severity": "warning",
          "location": "/body/p[8]",
          "current_value": {"text": "Dependent coverage", "style": "Heading3"},
          "confidence": 0.78,
          "why_human_needed": "Depends on E-D-001 outline decision.",
          "related_findings_ids": ["E-D-001"]
        },
        {
          "id": "E-D-003",
          "rule_id": "LAYOUT_TABLE_REVIEW",
          "severity": "warning",
          "location": "/body/tbl[1]",
          "current_value": {"rows": 2, "columns": 2, "borders": "none", "contains": "prose blocks"},
          "confidence": 0.38,
          "why_human_needed": "Flattening may change layout.",
          "related_findings_ids": []
        },
        {
          "id": "E-D-004",
          "rule_id": "LINK_TEXT_LOW_CONFIDENCE",
          "severity": "warning",
          "location": "/body/p[12]/hyperlink[1]",
          "current_value": {"text": "Learn more", "url": "https://example.com/rates", "sentence": "Learn more about 2026 contribution rates."},
          "suggested_value": {"text": "View 2026 contribution rates"},
          "confidence": 0.88,
          "why_human_needed": "Low-confidence upstream link rewrite.",
          "related_findings_ids": []
        },
        {
          "id": "E-D-005",
          "rule_id": "FLOATING_OBJECT_ORDER",
          "severity": "error",
          "location": "/body/p[15]/picture[1]",
          "current_value": {"wrap": "square", "nearby_text": "See the enrollment workflow below."},
          "confidence": 0.55,
          "why_human_needed": "May be a referenced diagram or a side illustration.",
          "related_findings_ids": []
        }
      ]
}
```

### PPTX manifest (`./fixtures/stage4-demo.pptx.manifest.json`)

```json
{
  "schema_version": "1.0.0",
  "document_path": "./fixtures/stage4-demo.pptx",
  "document_type": "pptx",
  "findings": [
        {
          "id": "E-P-001",
          "rule_id": "PPT_READING_ORDER",
          "severity": "error",
          "location": "/slide[2]",
          "current_value": {"object_order": ["Title 1", "Button", "Chart", "Source"], "visual_order": ["Title 1", "Chart", "Source", "Button"]},
          "confidence": 0.62,
          "why_human_needed": "CTA placement may be intentional.",
          "related_findings_ids": ["E-P-002"]
        },
        {
          "id": "E-P-002",
          "rule_id": "CONTRAST_LOW_CONFIDENCE",
          "severity": "error",
          "location": "/slide[2]/shape[5]/run[1]",
          "current_value": {"fg": "#9AA0A6", "bg": "#FFFFFF", "font_size_pt": 8},
          "confidence": 0.58,
          "why_human_needed": "Source note intentionally low emphasis.",
          "related_findings_ids": ["E-P-001"]
        },
        {
          "id": "E-P-003",
          "rule_id": "IMAGE_DECORATIVE_UNCERTAIN",
          "severity": "warning",
          "location": "/slide[3]/picture[2]",
          "current_value": {"alt": "blue swoosh", "nearby_text": ""},
          "confidence": 0.49,
          "why_human_needed": "Could be decorative brand flourish.",
          "related_findings_ids": []
        },
        {
          "id": "E-P-004",
          "rule_id": "AI_SLIDE_TITLE_LOW_CONFIDENCE",
          "severity": "warning",
          "location": "/slide[4]/shape[name=Title 1]",
          "current_value": {"text": "Overview", "main_message": "Renewal timeline and owner decisions"},
          "suggested_value": {"text": "Renewal timeline and decisions"},
          "confidence": 0.66,
          "why_human_needed": "Title affects presenter narrative.",
          "related_findings_ids": []
        },
        {
          "id": "E-P-005",
          "rule_id": "MERGED_CELLS_REVIEW",
          "severity": "warning",
          "location": "/slide[5]/table[1]/tr[1]/tc[1]",
          "current_value": {"gridSpan": 3, "text": "Regional results"},
          "confidence": 0.44,
          "why_human_needed": "Merged group header may be intentional.",
          "related_findings_ids": []
        }
      ]
}
```

## Expected Claude behavior

| Finding | Expected behavior |
|---|---|
| E-D-001 + E-D-002 | Group as one heading-outline decision. Since confidence is high and the parent heading is clear, promote `/body/p[5]` to `Heading2` and leave `/body/p[8]` as `Heading3`; log WCAG 1.3.1 and 2.4.10. |
| E-D-003 | Ask before flattening because layout-table restructuring is high impact and low confidence. If user says “you decide,” defer rather than flatten. |
| E-D-004 | Fix and log: replace link text with “View 2026 contribution rates” using `officecli set ... --prop text=...`; no user prompt needed. |
| E-D-005 | Ask whether the floating image should be inline after the referenced sentence or remain a side illustration. Do not change wrapping without approval/default confidence. |
| E-P-001 + E-P-002 | Group by slide 2. Ask one batched question covering reading order and low-contrast source note. Use `swap` or `move` only after approval/default. Use `scripts/contrast.py` for the source note. |
| E-P-003 | Ask decorative/informative question. If user says “you decide,” mark decorative only if inspection confirms it is a brand flourish with no meaning; otherwise keep short alt. |
| E-P-004 | Ask or apply if title placeholder and main message are obvious; log as user-approved or high-confidence. Avoid generic “Overview.” |
| E-P-005 | Ask split/keep/defer. If user says “you decide,” preserve the merged group header unless it breaks actual header associations. |

## Required pass conditions

- Uses `scripts/triage.py` or equivalent grouping logic before edits.
- Uses OfficeCLI commands for all document mutations.
- Creates a backup before first write.
- Uses `officecli batch` for multiple same-file writes.
- Runs `officecli validate` after structural batches.
- Restores backup and stops if validation fails.
- Does not re-run upstream detection or auto-fixes.
- Produces both terminal summary and JSON report with the required arrays.
