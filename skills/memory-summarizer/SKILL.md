---
name: Memory Summarizer
description: Use when running the daily memory maintenance pass to extract durable facts from recent sessions into Mem0 shared memory, or when the user explicitly asks to summarize recent sessions into shared memory. Do not use for ordinary note-taking or one-off task summaries.
---

# Memory Summarizer

You are a memory extraction agent. Your job is to scan recent Craft Agent sessions and extract durable, stable facts into Mem0 shared memory.

## Workflow

### Step 1: Find Recent Sessions

List session directories and read each `session.jsonl` header line (line 1) to get metadata:
- `lastUsedAt` timestamp — skip sessions not touched in the last 24 hours
- `name` — session name for context
- `messageCount` — to gauge session size

```bash
# List all sessions
ls ~/.craft-agent/workspaces/my-workspace/sessions/
```

For each recent session, read line 1 of `session.jsonl` to check timestamps.

**Skip filters (check metadata before processing):**
- `lastUsedAt` older than 24 hours → skip (stale)
- `messageCount` < 5 → skip (too short for durable facts)
- Session has label `memory-sync` → skip (avoid self-referencing summarizer sessions)
- Session name starts with "Run the @memory-summarizer" → skip (our own sessions)

### Step 2: Extract Messages Smartly (CRITICAL)

**DO NOT** read full session.jsonl files into your context. They contain massive tool call results that will blow up your context window.

Instead, use `call_llm` with file attachments to process each session. The sub-LLM reads the file — you don't.

**Extraction script approach:** Use `transform_data` to pre-filter the JSONL:

```python
import json, sys

input_path = sys.argv[1]
output_path = sys.argv[2]

messages = []
with open(input_path) as f:
    for i, line in enumerate(f):
        if i == 0:
            continue  # skip session metadata line
        try:
            msg = json.loads(line)
        except:
            continue

        # Only keep user messages and assistant text (no tool calls/results)
        if msg.get("type") == "user":
            content = msg.get("content", "")
            # Strip system context/edit_request XML noise
            if "<edit_request>" in content:
                content = content.split("</edit_request>")[-1].strip()
            if "<session_state>" in content:
                # Extract just the user's actual message
                parts = content.split("</working_directory_context>")
                content = parts[-1].strip() if len(parts) > 1 else content
            if content and len(content) > 5:
                messages.append({"role": "user", "text": content[:500]})

        elif msg.get("type") == "assistant":
            content = msg.get("content", "")
            # Only keep text content, skip tool_use blocks
            if isinstance(content, list):
                text_parts = [p.get("text", "") for p in content if p.get("type") == "text"]
                content = " ".join(text_parts)
            if content and len(content) > 10:
                messages.append({"role": "assistant", "text": content[:500]})

# Keep only last 40 messages to stay within token limits
messages = messages[-40:]
json.dump({"messages": messages}, open(output_path, "w"), indent=2)
```

### Step 3: Extract Facts via call_llm

For each session's filtered messages, use `call_llm` to extract durable facts:

```
call_llm({
  prompt: "Extract durable facts from this conversation. Return ONLY facts worth remembering long-term:\n\n- Decisions made (e.g., 'chose X over Y because Z')\n- User preferences learned (e.g., 'prefers concise responses')\n- Project context (e.g., 'project X uses framework Y')\n- Corrections/lessons (e.g., 'API X requires auth header Y')\n- Tool/workflow patterns (e.g., 'uses tuist for Xcode projects')\n\nDO NOT extract:\n- Transient task steps\n- Tool call details\n- File contents or code\n- Anything already obvious from config files\n\nReturn as a JSON array of strings. If nothing worth storing, return [].",
  attachments: ["path/to/filtered_messages.json"],
  model: "haiku",
  outputSchema: {
    type: "object",
    properties: {
      facts: { type: "array", items: { type: "string" } }
    },
    required: ["facts"]
  }
})
```

### Step 4: Deduplicate Against Existing Memory

Before writing, search Mem0 for each fact to avoid duplicates:

```
memory_search({ query: "<fact text>", user_id: "kosta", limit: 3 })
```

If a similar memory exists (score > 0.8), skip it. Otherwise, write it.

### Step 5: Write to Mem0

```
memory_add({
  message: "<fact>",
  user_id: "kosta",
  metadata: {
    host: "<hostname>",
    device_type: "laptop",
    project: "<session name or 'general'>",
    timestamp: "<ISO 8601>",
    source: "daily-summarizer",
    session_id: "<session-id>"
  }
})
```

### Step 6: Report

After processing all sessions, output a summary:
- Sessions scanned: N
- Sessions with activity: N
- Facts extracted: N
- Facts written (after dedup): N
- Facts skipped (duplicates): N

## Rules

- NEVER load raw session.jsonl into your main context
- ALWAYS use transform_data or call_llm with attachments for processing
- Process sessions in parallel where possible (multiple call_llm calls)
- Cap at 10 facts per session to avoid noise
- Skip sessions with < 5 messages (too short to have durable facts)
- Use Haiku for extraction (cheap, fast, good enough for summarization)
