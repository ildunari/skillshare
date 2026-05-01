# WCAG, Section 508, ADA, and rule mapping

Use this file when explaining why a fix matters. Keep the explanation plain: accessibility remediation is about preserving meaning, navigation, and operability for people using screen readers, keyboard navigation, high contrast modes, or magnification.

Primary references:

- Microsoft Accessibility Checker rule catalog: https://support.microsoft.com/en-us/office/rules-for-the-accessibility-checker-651e08f2-0fc3-4e10-aaca-74b4a67101c1
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WCAG 2.2 Quick Reference: https://www.w3.org/WAI/WCAG22/quickref/
- Revised Section 508 E205 Electronic Content: https://www.access-board.gov/ict/
- ADA Title II web and mobile accessibility rule: https://www.ada.gov/resources/2024-03-08-web-rule/

## Grounding

- Section 508 Revised Standards E205 require covered federal electronic content to conform to WCAG Level A and AA, with specific non-web document provisions and exceptions.
- ADA Title II and Title III obligations are broader than any single technical checklist. For public-facing documents, accessible Office files reduce effective-communication risk and avoid forcing users to request alternate formats for routine access.
- Microsoft Accessibility Checker is useful but incomplete: it flags many structural problems and warnings, while ambiguous issues still require human/AI judgment.

## Rule mapping

| Manifest `rule_id` pattern | WCAG 2.2 SC | Plain-English impact | Typical stage 4 action |
|---|---|---|---|
| `MSO_ALT_MISSING`, `MSO_ALT_REVIEW`, `AI_ALT_LOW_CONFIDENCE`, `IMAGE_DECORATIVE_UNCERTAIN` | 1.1.1 Non-text Content | Screen reader users need text for meaningful images; purely decorative images should not create noise. | Decide informative vs decorative; set concise alt or decorative state. |
| `MSO_OBJECT_DECORATIVE_CONFLICT`, `DECORATIVE_HAS_CONTEXT` | 1.1.1 | A wrong decorative flag hides meaningful content; wrong alt forces irrelevant content. | Inspect nearby text and author intent before changing. |
| `MSO_TABLE_HEADER_MISSING`, `TABLE_HEADER_UNCLEAR`, `TABLE_SIMPLE_STRUCTURE` | 1.3.1 Info and Relationships | Table headers and relationships must survive assistive technology linearization. | Set header row, simplify table, or defer if structural change would alter meaning. |
| `COMPLEX_TABLE`, `LAYOUT_TABLE`, `MERGED_CELLS_REVIEW` | 1.3.1, sometimes 1.3.2 | Merged, nested, or layout tables can scramble reading and header associations. | Split only problematic merges; flatten layout tables when safe. |
| `READING_ORDER`, `PPT_READING_ORDER`, `FLOATING_OBJECT_ORDER` | 1.3.2 Meaningful Sequence | Users who cannot perceive the visual page need the same logical sequence. | Reorder shapes/objects or set wrapping/inline placement. |
| `WORD_HEADING_SKIPPED`, `HEADING_VISUAL_ONLY`, `PPT_SECTION_TITLE_REVIEW` | 1.3.1, 2.4.6, 2.4.10 | Headings support navigation and reveal document structure. | Promote/demote semantic headings; do not style decorative text as headings. |
| `MSO_CONTRAST_TEXT`, `CONTRAST_LOW_CONFIDENCE` | 1.4.3 Contrast Minimum | Low-vision users need sufficient contrast for text and text in images. | Resolve theme/background, calculate ratio, apply minimal design-system fix. |
| `NON_TEXT_CONTRAST`, `CHART_CONTRAST`, `ICON_CONTRAST` | 1.4.11 Non-text Contrast | Meaningful graphics and UI-like controls need visible boundaries and states. | Adjust chart/shape/icon color or surrounding fill, not unrelated design. |
| `LINK_TEXT_LOW_CONFIDENCE`, `MSO_LINK_TEXT_UNCLEAR` | 2.4.4 Link Purpose by practice, 2.4.6 Headings and Labels | Links such as “click here” make navigation lists useless. | Replace with destination/purpose-specific text when context proves it. |
| `SLIDE_TITLE_MISSING`, `SLIDE_TITLE_DUPLICATE`, `AI_SLIDE_TITLE_LOW_CONFIDENCE` | 2.4.6, 2.4.10 | Unique slide titles help users navigate decks quickly. | Set or revise title placeholder; ask if title changes messaging. |
| `DOCUMENT_TITLE_MISSING`, `CORE_TITLE_REVIEW` | 2.4.2 Page Titled by analogy, 2.4.6 | Document title metadata gives users orientation in file lists and windows. | Set core property title from cover/title page when obvious. |
| `LANGUAGE_MISSING`, `LANGUAGE_REVIEW` | 3.1.1 Language of Page | Correct language lets assistive tech choose pronunciation and dictionaries. | Set document language only when the document language is clear. |
| `FORM_FIELD_NAME`, `CONTROL_NAME_ROLE` | 4.1.2 Name, Role, Value | Controls need programmatic names and roles to be operable. | Add accessible names or defer if OfficeCLI schema cannot safely express it. |

## Explaining fixes to users

Good explanation: “I set the first row as a repeating table header so screen readers can associate each data cell with Name, Plan, and Cost. This addresses WCAG 1.3.1 because the relationship was visible but not programmatic.”

Weak explanation: “Fixed table accessibility.”
