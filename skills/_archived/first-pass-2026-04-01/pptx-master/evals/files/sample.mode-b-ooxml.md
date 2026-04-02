# Mode B eval: OOXML editing — fix overflow and speaker notes

## Scenario
User provides a 6-slide client deck that has: (a) two slides with text overflowing their boxes, (b) missing speaker notes on all slides, and (c) one slide with a logo positioned outside the safe margin zone.

## Input
- `client.pptx`: existing branded deck with the three issues above
- Request: "Fix the overflow, add speaker notes summarizing each slide's key point, and move the logo inside safe margins."

## Expected behavior

1. Read `ooxml.md` fully before touching any XML.
2. Unpack: `python ooxml/scripts/unpack.py client.pptx workspace/`
3. Inspect `ppt/slides/slide*.xml` for overflow shapes and the logo shape's position (in EMUs).
4. Fix overflow on affected slides using the overflow ladder from `references/constraints-qa.md`: micro-edit first, layout upgrade if needed, split slide as last resort. Never shrink below 18pt.
5. Fix logo position: convert 0.5in safe margin to EMU (`0.5 × 914400 = 457200`); adjust `<a:off x="..." y="..."/>` accordingly.
6. Add speaker notes: for each slide, create or edit `ppt/notesSlides/notesSlide{N}.xml` with a 2–3 sentence summary.
7. Validate after each structural change: `python ooxml/scripts/validate.py workspace/ --original client.pptx`
8. Repack: `python ooxml/scripts/pack.py workspace/ output.pptx`
9. Run `python scripts/preflight_pptx.py output.pptx --out qa.pptx.json --md qa.pptx.md`

## Assertions
- `ooxml.md` is read before any XML is touched
- Validation is run after each edit, not just at the end
- Overflow is resolved without font reduction below 18pt
- Logo x and y positions are ≥ 457200 EMU from all edges
- Speaker notes XML is well-formed and validates cleanly
- `preflight_pptx.py` reports 0 hard fails on the output file
- A diff summary is produced listing what changed per slide

## What would fail this eval
- Editing XML without reading ooxml.md first
- Skipping validation between edits (letting one bad edit compound)
- Shrinking font to fix overflow instead of using the overflow ladder
- Producing malformed notes XML that breaks the file on open
- Reporting "done" without running preflight_pptx.py on the output
