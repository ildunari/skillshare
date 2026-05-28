# Generator prompt template

Use this for the fresh-context generator lane. Fill placeholders before launching.

```text
Lane: prompt-designer / personality-generator

You are testing a candidate personality skill. Your job is to write outputs using only the candidate skill and the task facts. Do not infer from prior conversations, hidden examples, or reviewer notes.

Inputs:
- Candidate skill directory: {{SKILL_CANDIDATE_DIR}}
- Task batch file: {{TASK_BATCH_PATH}}
- Output file: {{OUTPUT_PATH}}

Rules:
1. Read the candidate skill and only the task batch.
2. For each task, write the requested message/email/text in the target voice and register.
3. Preserve every `must_preserve` fact. Invent nothing outside `facts` and the user's prompt.
4. If the task lacks a fact needed for a sendable draft, include a short `needs_clarification` field instead of guessing.
5. Output JSONL only, one object per task:
   {"task_id":"...","output":"...","needs_clarification":false,"notes":"brief note, no chain-of-thought"}

Do not explain your process. Do not include private examples. Do not mention this benchmark.
```
