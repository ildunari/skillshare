---
name: mlx-embedding-reranker
description: >
  Use, validate, or convert embedding and reranker models for Apple MLX workflows. Trigger when the user mentions mlx-embeddings, text or multimodal embeddings, Qwen3 embedding or reranker models, vector search, similarity scoring, document reranking, or embedding quality checks on Apple Silicon. Do not use this for generative chat, VLM image-to-text generation, or LLM conversion unless embeddings or reranking are the actual task.
compatibility: Cross-platform open skill format. Intended for MLX embedding and reranking workflows using mlx-embeddings and Hugging Face model repos.
targets: [hermes-default, hermes-gpt]
---

## Context

Embedding and reranker models are evaluated differently from chat models. Success means stable vector shapes, sensible similarity or ranking behavior, correct pooling/normalization, and compatibility with downstream vector stores or retrieval pipelines.

## Task

Help an agent run, convert, and validate embedding or reranker models on Apple Silicon using `mlx-embeddings` or a current task-specific MLX library.

## Inputs

- Model ID or local path.
- Task: text embedding, multimodal embedding, cross-encoder reranking, or retrieval evaluation.
- Query/document examples, including at least one positive and one negative pair.
- Expected output: vectors, similarity matrix, ranking scores, or top-k documents.
- Downstream constraints: vector dimension, normalization, batch size, metric, vector database.

## Workflow

1. **Confirm task type.** Distinguish generative “answer this” tasks from “embed/rerank this” tasks.
2. **Check support.** Inspect `mlx-embeddings` supported architectures and current model cards. For Qwen3-VL embedding/reranking, use the model-specific processor path if documented.
3. **Preserve tokenizer and processor behavior.** Text-only embeddings depend on tokenizer and pooling conventions; multimodal embeddings depend on image processor and model-specific input structure.
4. **Run shape and dtype checks.** Confirm batch dimension, embedding dimension, dtype, and device behavior.
5. **Run semantic sanity checks.** Positive query-document pairs should score higher than unrelated negatives. For rerankers, scores should order known-relevant documents above distractors.
6. **Check normalization and metric.** Record whether vectors are normalized and which similarity metric is expected.
7. **Benchmark only after correctness.** Measure throughput and memory after shape and ranking sanity pass.

## Command and API patterns

Verify installed package help/docs first:

```bash
python -m pip install -U mlx mlx-embeddings transformers pillow huggingface_hub
python - <<'PY'
import mlx_embeddings, mlx
print('mlx_embeddings', getattr(mlx_embeddings, '__version__', 'unknown'))
print('mlx', getattr(mlx, '__version__', 'unknown'))
PY
```

Text embedding pattern:

```python
import mlx.core as mx
from mlx_embeddings import load

model, tokenizer = load("mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ")
texts = ["scientific plot with labeled axes", "a recipe for soup", "line chart with legend"]
inputs = tokenizer(texts, padding=True, return_tensors="np")
outputs = model(**inputs)
embeddings = outputs.text_embeds
mx.eval(embeddings)
print(embeddings.shape)
```

Multimodal embedding or reranking pattern:

```python
from mlx_embeddings import load

model, processor = load("mlx-community/Qwen3-VL-Embedding-4B-8bit")
inputs = [
    {"image": "./figure.png", "text": "Does this image contain a line chart?"},
    {"text": "unrelated cooking text"},
]
outputs = model.process(inputs, processor=processor)
print(outputs.embeddings.shape)
```

The exact model IDs and method names may change. Treat model cards as source of truth and test in the active environment.

## Validation checklist

- Model and tokenizer or processor load without falling back to an unintended class.
- Output shape matches the expected batch size and embedding dimension.
- Dtype and normalization are recorded.
- Known-positive examples score above known negatives.
- Batch and single-item results are consistent within tolerance.
- Reranker scores are monotonic for a hand-labeled mini set.
- Downstream vector store settings match dimension and metric.
- Run notes include exact examples and scores.

## Failure modes and recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Shape differs from expected | Wrong pooling head, wrong model variant, multimodal processor path skipped | Check model card and processor usage |
| Similarity scores look inverted or flat | Missing normalization, wrong metric, prompt format mismatch | Test cosine vs dot product; inspect normalization |
| Reranker returns nonsensical ordering | Query/document format wrong or generation model used as reranker | Use documented reranker API and labeled mini set |
| Multimodal model ignores images | Text-only path used accidentally | Use model-specific processor and media inputs |
| Works on one item but fails in batch | Padding/truncation or processor batching issue | Test single and batch paths; record max length/resolution |

## Done condition

Stop when vector or score outputs are shape-correct, semantically sane on a labeled mini set, and documented enough for downstream reuse. Do not claim embedding quality from successful loading alone.
