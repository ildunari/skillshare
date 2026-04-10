# Comment Patterns

> Maps user comment phrases to automation actions. When Kosta adds text below a captured link, it contains intent that should drive how the note is processed.

## Pattern Categories

### Enthusiasm / Priority Signals → Set priority tag

**Trigger phrases:** "important", "def wanna", "super cool", "must have", "amazing", "need this", "game changer", "insane", "holy shit", "wow", "this is it", "perfect"

**Action:**
- Set `status: evaluating` in frontmatter
- Add a `priority` tag
- Include the enthusiasm in the Kosta's Notes section

**Example:**
```
[Some Tool](https://example.com)

Def wanna try this, looks perfect for the vault workflow
```
→ Status: `evaluating`, tags include `priority`, Kosta's Notes preserves the comment.

### Research Requests → Spawn sub-agent

**Trigger phrases:** "research this", "look into this", "research more", "dig deeper", "find out more", "what's the deal with", "investigate"

**Action:**
- Spawn a research sub-agent with detailed instructions
- The sub-agent should do thorough research beyond just reading the README
- Include findings in the note's Overview and Key Points sections

### Questions → Research and answer

**Trigger phrases:** Any sentence ending in `?`, or phrases like "no idea why", "wonder if", "not sure how", "curious about", "what makes this different"

**Action:**
- Research the answer to the question
- Weave the answer naturally into the note's Overview section
- Don't create a separate Q&A section — integrate it into the narrative

**Example:**
```
[MCP Gateway](https://github.com/user/mcp-gateway)

No idea why this is better than openclaw
```
→ The note should compare MCP Gateway to OpenClaw and explain the differences.

### Dedup Checks → Search vault first

**Trigger phrases:** "not sure if we have this", "might be a dupe", "do we have this already", "check if exists"

**Action:**
- Do a thorough dedup check (search by URL, title, and related terms)
- If found: skip the item, log as duplicate with the path to the existing note
- If not found: process normally

### Reminders → Create daily note task

**Trigger phrases:** "remind me [date/day]", "follow up on", "check back", "revisit"

**Action:**
- Process the note normally
- Also create a task entry in the daily note for the specified date
- Format: `- [ ] Follow up on [[note-title]] — {context}`

### Batch Instructions → Split into multiple notes

**Trigger phrases:** "add individually", "each one separately", "process each", "one note per"

**Action:**
- Split multi-link captures into individual notes
- Process each URL as a separate item
- This is the default behavior for multi-link files, but the comment confirms it

### Comparison Requests → Include comparison section

**Trigger phrases:** "compare to", "vs", "versus", "better than", "how does this stack up", "alternative to"

**Action:**
- Research both the captured item AND the comparison target
- Include a `## Comparison` section in the note
- Format as a table or bullet points showing key differences

### Brief Descriptions → Use as note context

**Trigger phrases:** Short descriptive comments without action words — "for voice chat animations", "python testing framework", "obsidian plugin for graphs"

**Action:**
- Use the description to inform categorization and filing
- Include it in the note's one-line summary
- Don't create a separate section — weave it into the Overview

### Filing Instructions → Override default filing

**Trigger phrases:** "put this in [folder]", "file under", "this goes in", "for the [project] project"

**Action:**
- Override the default filing rules with the user's explicit instruction
- If the specified folder doesn't exist, create it
- Log the override in the daily report

## Comment Parsing Rules

1. Comments appear after the first link line, usually separated by a blank line
2. Comments can be multi-line — read the full text
3. Multiple patterns can appear in a single comment (e.g., enthusiasm + question)
4. When multiple patterns conflict, prioritize: explicit filing instructions > research requests > questions > enthusiasm
5. If the comment is just a single emoji or "." — treat as no comment (enthusiasm neutral)
