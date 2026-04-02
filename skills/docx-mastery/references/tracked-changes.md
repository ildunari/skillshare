# Tracked changes (OOXML) — analysis + resolution

This skill can **author** new tracked changes in a clean document (see `scripts/document.py`).

These additions cover the other direction:

- **Inspect** a document that already has tracked changes + comments.
- **Accept / reject** existing changes (optionally by author/date/id).
- **Resolve / delete** comments.

Everything here works at the OOXML level (unzip → edit XML → rezip), because `python-docx` does not expose full revision operations.

---

## What Word “tracked changes” are in OOXML

Word stores revisions as *wrapper elements* (and a few “property-change” elements) in `word/document.xml` and other “story parts” (headers, footers, footnotes, endnotes).

### Insertions / deletions

- **Insertions**: `<w:ins>` wraps the content that was inserted.
- **Deletions**: `<w:del>` wraps the content that was deleted.

Common attributes on both:

- `w:id` — revision id (integer-like string)
- `w:author` — author name
- `w:date` — ISO timestamp (often UTC `...Z`)
- some docs also include `w16du:dateUtc` for a normalized UTC timestamp

Text nodes differ:

- Insertions contain normal `<w:t>` text runs.
- Deletions typically contain `<w:delText>` (and sometimes `<w:delInstrText>` for field instructions).

### Formatting / property changes

Tracked formatting changes don’t use `<w:ins>/<w:del>`. Instead, Word keeps the *current* properties on the parent, and stores the *previous* properties inside a `*Change` element:

- `<w:rPrChange>` inside `<w:rPr>` — run formatting changes
- `<w:pPrChange>` inside `<w:pPr>` — paragraph formatting changes
- `<w:tblPrChange>`, `<w:trPrChange>`, `<w:tcPrChange>` — table/row/cell property changes
- `<w:sectPrChange>` inside `<w:sectPr>` — section property changes

Semantics:

- **Accept** property change → keep current parent properties, remove the `*Change` element.
- **Reject** property change → restore properties from inside the `*Change` element, remove the `*Change` element.

### Moves

Word can represent moved text using:

- `<w:moveFrom>` — like a deletion at the source location
- `<w:moveTo>` — like an insertion at the destination

This repo’s resolver treats them the same way:

- accept moveTo = unwrap; reject moveTo = remove
- accept moveFrom = remove; reject moveFrom = unwrap

### RSIDs

You’ll see revision session ids all over WordprocessingML:

- `w:rsidR`, `w:rsidRPr`, `w:rsidP`, `w:rsidDel` …

They’re *session / edit provenance* identifiers, not the revision ids used by `<w:ins w:id=...>`.

When you add **new** tracked changes into a doc that already has them, RSIDs are one of the easiest ways to create “this file is corrupt” situations if you copy/paste XML fragments without updating ids.

---

## Comments in OOXML

A comment has two pieces:

1. **Anchors in the story part** (`word/document.xml`, etc.)
   - `<w:commentRangeStart w:id="X"/>`
   - (content being commented)
   - `<w:commentRangeEnd w:id="X"/>`
   - `<w:commentReference w:id="X"/>` (usually in a run immediately after)

2. **The comment body** in `word/comments.xml`
   - `<w:comment w:id="X" w:author="..." w:date="..."> ... </w:comment>`

Modern Word also adds metadata parts:

- `word/commentsExtended.xml` (`w15:commentEx`) includes `w15:done="0|1"` (resolved-ish) and optional thread parent pointers (`w15:paraIdParent`).
- `word/commentsIds.xml` maps `paraId → durableId`.
- `word/commentsExtensible.xml` stores extensible metadata by durableId.

---

## Script: tracked changes report

`scripts/tracked_changes_report.py` reads a `.docx` and outputs a JSON report:

```bash
python scripts/tracked_changes_report.py input.docx --pretty -o report.json
```

What you get:

- `tracked_changes[]`
  - `type`: `ins`, `del`, `moveTo`, `moveFrom`, `rPrChange`, ...
  - `id`, `author`, `date`, `dateUtc`
  - `text`: inserted/deleted text (best-effort)
  - `paragraph_context`: paragraph-level view with `[+inserted+]` and `[-deleted-]`
  - `part`: which story XML part the change is in

- `comments[]`
  - `id`, `author`, `date`, `initials`
  - `done` when `commentsExtended.xml` is present
  - `text`: comment body
  - `range_text`: best-effort extraction of the text inside the commented range

---

## Script: accept/reject + comment resolution

`scripts/tracked_changes_resolve.py` makes a **new** `.docx` with selected operations applied.

### Accept / reject changes

Accept everything:

```bash
python scripts/tracked_changes_resolve.py in.docx --accept-all -o out.docx
```

Reject everything:

```bash
python scripts/tracked_changes_resolve.py in.docx --reject-all -o out.docx
```

Accept only changes by an author:

```bash
python scripts/tracked_changes_resolve.py in.docx --accept --author "Alice" -o out.docx
```

Reject a specific revision id:

```bash
python scripts/tracked_changes_resolve.py in.docx --reject --id 17 -o out.docx
```

Filter by date:

```bash
python scripts/tracked_changes_resolve.py in.docx \
  --accept \
  --since "2026-02-01T00:00:00Z" \
  --until "2026-02-15T23:59:59Z" \
  -o out.docx
```

### Resolve or delete comments

Mark all comments as resolved (modern comments only):

```bash
python scripts/tracked_changes_resolve.py in.docx --resolve-comments -o out.docx
```

Delete comments and strip their range markers:

```bash
python scripts/tracked_changes_resolve.py in.docx --delete-comments -o out.docx
```

Comment selection filters:

- `--comment-id X` (repeatable)
- `--comment-author "Name"` (repeatable)

---

## Adding NEW tracked changes to a doc that already has them

If you need to *redline* a document that already contains revisions/comments, do **not** blindly insert new `<w:ins>/<w:del>` wrappers without checking:

### 1) Change id collisions

`w:id` values are not guaranteed to be globally unique if the document has been merged / round-tripped.

**Safe pattern**:

- scan the document for all `w:id` attributes on revision-bearing elements
- choose `max(existing)+1` (or a high random id) for new changes

### 2) Overlapping revisions

Word’s model allows nesting, but some nests are invalid or fragile:

- rejecting someone’s insertion is commonly represented as `<w:ins> ... <w:del>...</w:del> ...</w:ins>`
- restoring someone’s deletion is commonly represented as adding a new `<w:ins>` *after* their `<w:del>`

If you insert a `<w:ins>` that crosses a paragraph boundary or a table cell boundary, you can easily create invalid WordprocessingML.

### 3) RSID / provenance problems

When you copy XML fragments, you may copy rsid attributes or `w14:paraId` values that are supposed to be unique.

If Word claims the document is corrupted after your edit:

- validate the OOXML package
- ensure `w14:paraId` values are unique per part
- avoid copying paragraph elements verbatim; prefer creating new elements with fresh ids

---

## Common failure modes + fixes

**Word opens the file in repair mode**

- you broke XML well-formedness
- you created unbalanced comment range markers (start without end)
- you removed a comment body without removing `commentReference` / range markers

Fix:

- run `ooxml/scripts/validate.py` on the unpacked doc
- rerun `scripts/tracked_changes_report.py` to ensure counts make sense

**After acceptance/rejection, some text disappears**

- nested ins/del were resolved in the wrong order
- a deletion contained `<w:delText>` that wasn’t converted back to `<w:t>` when rejecting

Fix:

- resolve deepest changes first (this resolver does)
- confirm `delText → t` conversion happened

**Resolve comments “does nothing”**

- the doc does not have `word/commentsExtended.xml` (common for older Word versions)

Fix:

- use `--delete-comments` instead, or accept that “resolved” can’t be represented for that document.

---

## Pointers to primary specs / docs

- ECMA-376 (Office Open XML) — WordprocessingML revision elements
- Pandoc / python-docx docs are not tracked-changes-authoritative; WordprocessingML is.
