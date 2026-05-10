# mem0 suite benchmark — 2026-05-10

## Bottom line

The self-hosted mem0 stack is usable and should remain the canonical long-term memory store for deliberate writes. The reliable paths are explicit writes and explicit retrieval: `mem0_conclude`, `mem0_add_document`, `mem0_search`, `mem0_profile`, and `mem0_recall_recent`.

The weak path is passive conversation capture through organic `sync_turn` inference. During benchmarking it returned graph-side activity but did not create vector-searchable memories and logged `Error in new_retrieved_facts: Expecting value...`. Treat that as a known degraded path until fixed and re-benchmarked.

## Benchmarked behavior

- Backend services healthy: `mem0-api`, `mem0-postgres`, `mem0-neo4j`, `mem0-autoheal`.
- Explicit API create with `infer=false`: searchable after write.
- `mem0_conclude`: returns real memory IDs after the plugin fix and writes searchable explicit memories.
- `mem0_add_document`: works for document-derived text; slower because extraction/embedding work is heavier.
- `mem0_profile` and `mem0_recall_recent`: fast metadata/read paths.
- Search repeated over the API/plugin: usable latency for interactive recall.

Representative benchmark from the 2026-05-10 run:

- API explicit create with `infer=false`: about 7.7s, then searchable.
- API search median: about 1.83s; p95 about 4.20s.
- Plugin `mem0_search` median: about 1.67s; p95 about 2.01s.
- `mem0_profile`: about 8–18ms.
- `mem0_recall_recent`: about 11ms.
- `mem0_add_document`: about 13.7s.
- `mem0_conclude`: about 10.6s, returning real `memory_ids`.

Benchmark artifact from that run: `/tmp/mem0-bench-hermes-mem0-bench-1778421260.json`. It is a temp artifact, not durable source of truth.

## Operational policy

- Use `mem0_conclude` for durable facts that matter.
- Search/dedupe before writing.
- For critical facts, verify with a focused `mem0_search` after writing.
- Keep built-in Hermes `memory` as a tiny hot cache for ultra-stable prompt-worthy facts.
- Put procedures, command sequences, and debugging playbooks in Skillshare skills, not mem0.
- Do not rely on `sync_turn` to preserve important facts until the extraction path is fixed and re-tested.

## Regression signal

After future plugin/backend edits, run at least:

```bash
python -m pytest tests/plugins/memory/test_mem0_v2.py -q
```

Then run a live disposable write/search smoke through `mem0_conclude` and `mem0_search`. Unit tests are necessary but not enough for this integration because the backend and extractor can fail independently.
