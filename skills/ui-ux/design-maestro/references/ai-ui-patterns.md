# AI-Native UI Patterns

> Patterns for building interfaces where AI is the product — chat UIs, streaming responses, tool use indicators, citation systems, and agent orchestration.

## Streaming Text Display

| Aspect | Pattern | Key Technique |
|---|---|---|
| Token rendering | Append tokens to a buffer, render via React state | `useState` with string concatenation. Never `innerHTML` — XSS risk. |
| Cursor | Blinking pipe `|` at end of streaming text | CSS `@keyframes blink` on a `<span>`. Remove when stream completes. |
| Smooth reveal | Fade-in per word or sentence | `animation: fadeIn 150ms ease-out` on each new `<span>`. Chunked, not per-character (too many DOM nodes). |
| Auto-scroll | Scroll to bottom during streaming, pause if user scrolls up | Track `scrollTop + clientHeight >= scrollHeight - threshold`. Set a `userScrolled` flag on manual scroll. |
| Stop button | "Stop generating" during active stream | Positioned bottom-center of the message area. `AbortController` on the fetch. Fades in on stream start, out on completion. |

### Message container structure

```
<div class="message-stream">
  <div class="message-content prose">
    {rendered markdown}
    <span class="cursor" aria-hidden="true">|</span>
  </div>
</div>
```

Don't use `white-space: pre-wrap` for AI text — it breaks markdown rendering. Parse markdown to HTML as tokens arrive. For Claude artifacts, use a simple markdown-to-HTML converter or render as styled prose.

## Tool Use / Function Calling Indicators

When an AI is performing an action (searching, reading, computing), the user needs to know what's happening and that the system isn't stuck.

| State | Visual Pattern | Implementation |
|---|---|---|
| Tool invoked | Status pill: icon + tool name + "Running..." | Animated shimmer on the pill background. Icon matches the tool (search, file, globe). |
| Tool progress | Expandable detail panel below the pill | Collapsible `<details>` or click-to-expand. Show parameters sent. |
| Tool complete | Pill transitions to "Done" state, muted | Fade shimmer, change icon to checkmark, reduce opacity to ~0.6. |
| Tool chain | Stacked pills with connecting line | Vertical line between pills. Each pill independent. Active pill pulses. |

**Key detail:** Show *what* the tool is doing, not just *that* it's doing something. "Searching the web for 'OKLCH color generation'..." is useful. "Thinking..." is not.

Avoid spinners — they imply a binary loading/done state. AI tool use is a process with intermediate visibility.

## Citation / Source Display

| Pattern | When to Use | Key Technique |
|---|---|---|
| Inline superscript | Academic style, dense content | `<sup>[1]</sup>` linked to footnote. Small, non-intrusive. |
| Inline pill | Chat UIs, conversational | Small badge: `[Source Name]` with subtle background. Click to expand. |
| Side panel | Research tools, reference-heavy | Split view: content left, sources right. Highlight source on hover. |
| Expandable card | Moderate citation density | Click citation number → card expands below the paragraph showing title, URL, excerpt. |

**Source quality indicator:** If you have confidence data, show it. A small dot (green/amber) next to the source or a "Verified" badge. Don't show raw confidence scores — humans don't think in percentages.

## Conversation UI

| Decision | Option A | Option B | When to Use |
|---|---|---|---|
| Message style | Bubbles (colored background) | Full-width (no bubble) | Bubbles for casual chat. Full-width for work tools and long-form content. |
| User vs assistant | Right-aligned + colored | Left-aligned + neutral | Right/left for chat. For full-width, use subtle background tint or left accent border. |
| Avatars | Show them | Don't | Show if multi-user or if the AI has a brand identity. Skip for single-user focused tools. |
| Timestamps | Visible always | On hover / grouped | Always for async (email-like). Hover for synchronous (chat-like). Group by time block (not per-message). |

### Visual distinction between roles

Don't rely on position alone. The assistant should feel visually distinct:

- **Background tint:** User messages on `surface-100`, assistant on `surface-0` (or vice versa)
- **Typography:** Consider a slightly different text color or opacity
- **Accent border:** Subtle left border on assistant messages in the brand color
- **Width:** Assistant messages can be wider than user messages (they're the content; user messages are the query)

## Confidence / Uncertainty Display

When an AI qualifies its output, the UI should support that:

| Confidence level | Visual treatment |
|---|---|
| High | Normal text rendering |
| Medium | Slightly muted text color (`--text-secondary`). Optional "Verify" micro-badge. |
| Low | Muted text + amber left border. "Unverified" badge. |
| Speculative | Italic text, `--text-muted` color, dashed left border |

Don't over-instrument this. Most text should render normally. Flag uncertainty only where it changes how the user should act on the information.

## Artifact / File Preview

| Content type | Preview pattern |
|---|---|
| Code | Syntax-highlighted block with language badge, copy button top-right, line numbers optional |
| React component | Live preview in iframe/sandbox, code toggle below |
| Document (PDF, DOCX) | File card: icon + filename + size + "Download" button. Preview thumbnail if available. |
| Image | Inline render at constrained width, click-to-expand lightbox |
| Data (CSV, JSON) | First 5 rows in a mini-table, "Show all" expander |

**File cards should feel like objects.** Border, subtle shadow, icon matching file type, filename in mono. Not just a text link.

## Loading States for LLM Responses

Skeleton screens are wrong for AI — the content shape is unknown. Use states that convey active processing:

| Pattern | Visual | When |
|---|---|---|
| Typing indicator | Three pulsing dots (offset timing) | Short expected waits (<3s) |
| Streaming shimmer | Horizontal shimmer bar at full message width | Medium waits, before first token arrives |
| Status text | "Analyzing your document..." / "Searching..." | When specific work is happening (tool use) |
| Progress stages | Stepped indicator: "Reading → Analyzing → Writing" | Multi-step operations |

**Never:** A spinner with "Loading..." on an AI response. It tells the user nothing and feels broken after 5 seconds.

**The first token should kill the loading state.** The moment text starts streaming, all loading indicators vanish and the content takes over. No awkward transition — immediate swap.

## Multi-Agent / Orchestration UI

When multiple AI agents or processes run in parallel:

| Pattern | Use |
|---|---|
| Agent cards | Named cards with avatar/icon, status badge (idle/running/done/error), last action summary |
| Task timeline | Vertical timeline showing delegation, execution, completion across agents |
| Parallel lanes | Swim lanes showing concurrent agent work, merging at synthesis points |
| Status dashboard | Grid of agent status cards with real-time updates, expandable logs |

Agent identity matters. Each agent should have a distinct name, icon/color, and role description. "Agent 1" and "Agent 2" is lazy. "Researcher" and "Editor" tells the user what's happening.
