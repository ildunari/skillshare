---
name: imessage-imemory-backfill
category: hermes
---
# iMessage Guest Contact Memory Backfill

Use this when you need to ingest a new guest contact's approved iMessage chat history into
`mem0` the same way the Steve pipeline is currently done.

This is the safe/repeatable flow, including dedupe + quota-aware loading.

## Preconditions

- Contact is already approved in `/Users/Kosta/.hermes/profiles/guest/contacts.yaml`.
- Snapshot of Messages DB exists as `/Users/Kosta/.hermes/shared/mom_backfill/chat_snapshot.db` style source.
- `mem0` provider and local cli proxy are healthy.

## Paths

- Source DB snapshot: `/Users/Kosta/.hermes/shared/<CONTACT>_backfill/chat_snapshot.db`
- Pipeline dir: `/Users/Kosta/.hermes/shared/<CONTACT>_backfill/`
- Corpus: `<dir>/...</` and chunks/fragments under same root.
- Final fact files: `<dir>/<CONTACT_UPPER>_PROFILE.json`, `<dir>/KOSTA_WITH_<CONTACT_UPPER>_FACTS.json`.

## 0) Add approved contact

Update `~/.hermes/profiles/guest/contacts.yaml` with a new entry under `contacts:`.
At minimum provide:

- `identities.bluebubbles.handles` for phone variants used by this person.
- `display_name`, `id`, `role`, `allowed_surfaces` (`bluebubbles`), and outbound recipient policy.

## 1) Stage 1: Extract corpus

Create/prepare `/Users/Kosta/.hermes/shared/<contact>_backfill/extract_corpus.py` with the existing logic.
Run:

```bash
python3 /Users/Kosta/.hermes/shared/<contact>_backfill/extract_corpus.py
```

This should produce `<contact>_corpus.txt` and `<contact>_backfill/corpus_stats.txt`.

## 2) Stage 2: Chunk

Run:

```bash
python3 /Users/Kosta/.hermes/shared/<contact>_backfill/chunk_corpus.py
```

Expect `chunks/chunk_###.txt` and `chunks/manifest.json`.

## 3) Stage 3/4: Extract facts (GPT-5.5)

```bash
python3 /Users/Kosta/.hermes/shared/<contact>_backfill/extract_facts.py --all --workers 4
```

Outputs:

- `fragments/frag_###.json`

## 4) Stage 5: Merge + dedupe

```bash
python3 /Users/Kosta/.hermes/shared/<contact>_backfill/merge_facts.py
```

Outputs reviewed markdown + JSON summaries:

- `<CONTACT_UPPER>_PROFILE.md/.json`
- `KOSTA_WITH_<CONTACT_UPPER>_FACTS.md/.json`

## 5) Stage 6: Load into mem0

```bash
python3 /Users/Kosta/.hermes/shared/<contact>_backfill/load_facts_mem0.py
```

Use namespace mapping:

- contact facts -> `guest:<contact_id>`
- kosta facts -> default account namespace used by the contact job.

## Safety checks

- Verify endpoint auth before running fact extraction.
- Keep extraction prompts requiring `evidence` and `date` to prevent hallucinations.
- Check for `ok` and `err` counts before declaring done.
- Keep contact identity metadata in `contacts.yaml` as the approval gate.
