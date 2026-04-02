# Visual Specs

Use visuals aggressively. This skill is fundamentally about relationship mapping, not just prose.

## Recommended visual set

### 1. Load-stack chain
Use for: "what loads together?"

Format: Mermaid graph TD/LR

### 2. Duplicate cluster map
Use for: one exact duplicate group

Format: Mermaid graph with one canonical/source candidate and copies around it

### 3. Session-impact matrix
Use for: runtime × project comparison

Format: datatable or spreadsheet

### 4. Delete safety ladder
Use for: cleanup planning

Format: ranked table with bucket + score + why

### 5. Skill topology map
Use for: source vs runtime installs vs mirrors

Format: Mermaid graph

### 6. Before/after savings chart
Use for: proving payoff of the cleanup plan

Format: xychart-beta or datatable

## Reporting rule

When the user asks where the pain actually is, show runtime/session visuals first. When the user asks what can be cleaned up safely, show delete ladder and duplicate map first.
