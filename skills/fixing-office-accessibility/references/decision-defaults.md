# Decision defaults when the user says “you decide” or goes silent

These defaults keep remediation moving while reducing the chance of deleting meaning or changing author intent.

## Global defaults

- Favor inclusion over omission. A concise accessible name is safer than hiding meaningful content.
- Prefer reversible, localized fixes over broad document-wide changes.
- Preserve author intent and visual design unless the finding directly requires a structural or contrast fix.
- Defer destructive restructures when the accessibility benefit is plausible but not certain.
- Record every defaulted decision in the report as `decision_source: default_policy`.

## By issue type

| Issue | Default |
|---|---|
| Decorative vs informative image | Treat as informative unless it is purely ornament, redundant logo next to same text, divider, texture, or background. Use concise alt; do not mark decorative if the image conveys data, process, identity, action, or emotional tone relevant to the document. |
| Reading order | Use the sequence that best preserves visible narrative: title, subtitle, primary content, supporting explanation, footnote/source, call to action. If two narratives are equally plausible, defer instead of moving objects. |
| Heading structure | Promote visual headings that introduce a section and have following content. Do not promote captions, labels, pull quotes, or isolated emphasis. Fix skipped levels when the surrounding outline makes the missing level obvious. |
| Contrast | Apply the smallest local change that passes WCAG and fits theme tokens. Prefer local text/fill changes over theme-wide changes. Defer when text overlays a complex photo and no safe local fill is obvious. |
| Complex tables | For data tables, add/keep header rows and preserve useful grouping. For layout tables, defer flattening unless the table clearly contains prose/images arranged for visual layout and not tabular data. |
| Merged cells | Keep merges that express a group heading, subtotal, or intentional category. Split merges that obscure row/column headers or create empty continuation cells read as content. |
| Floating objects | Preserve floats that are side callouts, watermarks, or decorative layout elements. Set inline when the object is referenced by a nearby sentence and must be read at that point. |
| Link text | Replace only when context and destination prove the purpose. Otherwise defer or keep existing text with report note. |
| Slide titles | Use the visible title if present. For missing titles, derive from the slide’s main message, not a generic label like “Slide 4.” If a hidden title would be better than visible design change, use the base `pptx` skill to add a proper title placeholder. |

## Idempotency defaults

Before writing, compare the current value to the intended value. If already correct, log as no-op and do not write. For batch commands, omit no-op commands so reruns do not duplicate additions or churn XML.
