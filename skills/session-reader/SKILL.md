---
name: "Session Reader"
description: "Use when you need to read or analyze Craft Agent session JSONL files by extracting the user and assistant dialogue while stripping tool calls, tool results, and other session noise. Trigger on requests to inspect a Craft session transcript, recover conversation text from session logs, summarize dialogue from a session file, or compare conversations across Craft sessions."
alwaysAllow: ["Bash", "Read"]
---

# Session Reader

Extract clean user/assistant dialogue from Craft Agent session `.jsonl` files, removing tool calls and results that dominate the raw data (typically 50-90% of session size).

## Session JSONL Format

Each session lives at `~/.craft-agent/workspaces/{workspace}/sessions/{session-id}/session.jsonl`:

- **Line 1**: Session metadata (no `type` field) — contains `name`, `model`, `labels`, `permissionMode`, etc.
- **Remaining lines**: Messages with `type` = `user` | `assistant` | `tool`

### Key Fields

| Field | On Types | Description |
|-------|----------|-------------|
| `type` | all | `user`, `assistant`, or `tool` |
| `content` | all | The text content |
| `isIntermediate` | assistant | `true` if this is a brief preamble before tool calls (not a final response) |
| `toolName` | tool | Which tool was called |
| `toolResult` | tool | The tool's output (often huge) |
| `turnId` | assistant, tool | Groups tool calls with their originating assistant turn |
| `timestamp` | all | Unix timestamp in milliseconds |

## Extraction Script

Use this Python script to extract dialogue. Adjust parameters as needed:

```python
import json, sys, os
from datetime import datetime

def extract_session_dialogue(session_path, include_intermediate=False, output_format="markdown"):
    """Extract user/assistant dialogue from a session JSONL file.

    Args:
        session_path: Path to session.jsonl
        include_intermediate: Include assistant messages before tool calls
        output_format: "markdown" for readable output, "json" for structured data

    Returns:
        Tuple of (output_text, stats_dict)
    """
    messages = []
    meta = {}

    with open(session_path) as f:
        for line in f:
            obj = json.loads(line)
            t = obj.get('type')
            content = obj.get('content', '').strip()

            # First line is metadata
            if not t:
                meta = obj
                continue

            if not content:
                continue

            if t == 'user':
                messages.append({
                    'role': 'user',
                    'content': content,
                    'timestamp': obj.get('timestamp', 0)
                })
            elif t == 'assistant':
                is_intermediate = obj.get('isIntermediate', False)
                if not is_intermediate or include_intermediate:
                    messages.append({
                        'role': 'assistant',
                        'intermediate': is_intermediate,
                        'content': content,
                        'timestamp': obj.get('timestamp', 0)
                    })

    # Stats
    stats = {
        'session_name': meta.get('name', 'Unknown'),
        'session_id': meta.get('id', 'Unknown'),
        'model': meta.get('model', 'Unknown'),
        'user_messages': sum(1 for m in messages if m['role'] == 'user'),
        'assistant_final': sum(1 for m in messages if m['role'] == 'assistant' and not m.get('intermediate')),
        'assistant_intermediate': sum(1 for m in messages if m.get('intermediate')),
        'total_chars': sum(len(m['content']) for m in messages),
    }
    stats['approx_tokens'] = stats['total_chars'] // 4

    if output_format == "json":
        return json.dumps({'meta': meta, 'messages': messages, 'stats': stats}, indent=2), stats

    # Markdown output
    lines = []
    lines.append(f"# Session: {stats['session_name']}")
    lines.append(f"**ID:** {stats['session_id']} | **Model:** {stats['model']}")
    lines.append(f"**Turns:** {stats['user_messages']} user, {stats['assistant_final']} assistant")
    lines.append(f"**Size:** ~{stats['approx_tokens']:,} tokens\n")
    lines.append("---\n")

    for m in messages:
        ts = m.get('timestamp', 0)
        time_str = datetime.fromtimestamp(ts / 1000).strftime('%H:%M') if ts else ''
        role_label = m['role'].upper()
        if m.get('intermediate'):
            role_label += ' (before tools)'
        lines.append(f"## [{role_label}] {time_str}\n")
        lines.append(m['content'])
        lines.append("\n---\n")

    return '\n'.join(lines), stats


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract dialogue from Craft Agent sessions')
    parser.add_argument('session_path', help='Path to session.jsonl or session directory')
    parser.add_argument('--intermediate', '-i', action='store_true', help='Include intermediate assistant messages')
    parser.add_argument('--format', '-f', choices=['markdown', 'json'], default='markdown')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--stats-only', action='store_true', help='Print only stats, no dialogue')
    args = parser.parse_args()

    path = args.session_path
    if os.path.isdir(path):
        path = os.path.join(path, 'session.jsonl')

    output, stats = extract_session_dialogue(path, args.intermediate, args.format)

    if args.stats_only:
        for k, v in stats.items():
            print(f'{k}: {v}')
    elif args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Written to {args.output}")
        for k, v in stats.items():
            print(f'  {k}: {v}')
    else:
        print(output)
```

## Usage

### Quick extraction via Bash

```bash
# Stats only
python3 /path/to/script.py /path/to/session/  --stats-only

# Full dialogue to stdout
python3 /path/to/script.py /path/to/session/

# With intermediate messages, to file
python3 /path/to/script.py /path/to/session/ -i -o dialogue.md

# JSON format for programmatic use
python3 /path/to/script.py /path/to/session/ -f json -o dialogue.json
```

### Inline extraction (no script file needed)

```bash
python3 -c "
import json
with open('SESSION_PATH/session.jsonl') as f:
    for line in f:
        obj = json.loads(line)
        t = obj.get('type')
        c = obj.get('content','').strip()
        if t == 'user' and c:
            print(f'\n## [USER]\n{c}\n---')
        elif t == 'assistant' and c and not obj.get('isIntermediate'):
            print(f'\n## [ASSISTANT]\n{c}\n---')
"
```

### Reading into context efficiently

For large sessions (~40K+ tokens of dialogue), consider:

1. **Extract to file first**, then read specific sections with `Read` tool's `offset`/`limit` params
2. **Use `--stats-only`** to check size before loading
3. **Skip intermediate messages** (default) — they're usually brief tool preambles
4. **Use `call_llm`** to summarize sections if the full dialogue exceeds what you need

## Typical Compression Ratios

| Session Type | Raw JSONL | Dialogue Only | Ratio |
|---|---|---|---|
| Tool-heavy (coding) | ~600K tokens | ~8K tokens | 70-80x |
| Conversational | ~150K tokens | ~40K tokens | 3-5x |
| Mixed | ~300K tokens | ~15K tokens | 15-25x |
