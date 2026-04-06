# Stage 2: Technical Review

Evaluate the skill's scripts, bundled resources, code quality, and technical
architecture. This stage answers: "Does the skill's code and tooling actually
work well, and is it well-engineered for its purpose?"

Read the skill's scripts and reference files during this stage. If the user
provided supplementary material (research reports, competitor analysis, reference
implementations), cross-reference against the skill's current approach.

## Checklist

### 2.1 Script Quality

For each script in the skill, evaluate:

**Correctness:**
- Does the script do what the skill says it does?
- Are there obvious bugs or logic errors?
- Does error handling cover likely failure modes? (not just the happy path)
- Are edge cases handled? (empty input, malformed data, missing files,
  unexpected types)

**Robustness:**
- Does it fail gracefully with useful error messages?
- Are file paths handled portably? (no hardcoded absolute paths, proper
  path joining)
- Does it handle missing dependencies or unavailable tools?
- Are there race conditions or ordering assumptions that could break?

**Maintainability:**
- Are variable and function names descriptive?
- Is the code DRY without being over-abstracted?
- Could someone unfamiliar with the skill understand what the script does?
- Are there magic numbers or unexplained constants?

**Performance (when relevant):**
- Are there O(n²) loops on potentially large data?
- Are there unnecessary file reads or network calls?
- Could expensive operations be cached or batched?

### 2.2 Reference File Quality

For each reference file:

**Relevance:**
- Does this reference file earn its place? Would removing it degrade skill
  performance?
- Is the content actionable (instructions, checklists, decision trees) or
  is it just background reading that doesn't change behavior?
- Could this content be condensed without losing value?

**Organization:**
- Is the file well-structured with clear sections?
- If over 300 lines, does it have a table of contents?
- Can the model find what it needs quickly, or does it need to read the
  whole file to extract the relevant part?

**Accuracy:**
- Are technical claims correct?
- Are examples valid and current?
- Do code snippets actually work?
- Are version numbers, API references, or tool names current?

### 2.3 Architecture

**Separation of concerns:**
- Do scripts handle deterministic/repetitive work while SKILL.md handles
  judgment-requiring decisions?
- Are there instructions in SKILL.md that should be scripts? (Anything
  the model does identically every invocation is a candidate)
- Are there scripts that embed too much decision-making that should be
  in the instructions?

**Dependencies:**
- Does the skill require specific tools, libraries, or system capabilities?
- Are dependencies documented?
- Are there implicit dependencies (assumes a browser, assumes internet
  access, assumes specific file structure) that aren't stated?
- Could the skill fail silently if a dependency is missing?

**Compatibility:**
- Does the skill work in its intended environment? (Claude.ai vs Claude Code
  vs API — the environment affects available tools)
- Are there features that only work with subagents that the skill doesn't
  acknowledge?
- Does it assume capabilities the model might not have? (e.g., assuming
  `present_files` is available, assuming bash access)

### 2.4 Asset Quality

For template files, fonts, images, or other assets:

- Are assets actually used by the skill? (Dead assets waste package size)
- Are assets in appropriate formats?
- Do templates match the skill's output specifications?
- Are there licensing concerns with bundled assets?

### 2.5 Missing Automation

This is about opportunities, not problems. Identify cases where:

- The skill relies on the model to perform a task that a script could do
  more reliably (data validation, format conversion, file generation)
- Multiple reference files share patterns that could be consolidated
- The model would benefit from a helper script for common operations
- External tools or APIs could improve the skill's output quality

### 2.6 Supplementary Material Integration

If the user provided research reports, competitor skills, or reference material:

- Does the skill implement the key findings from the research?
- Are there techniques or approaches in the supplementary material that
  the skill should adopt?
- Does the research reveal gaps in the skill's coverage?
- Are there contradictions between the supplementary material and the
  skill's current approach?

## Severity Guide for Technical Issues

| Severity | Threshold |
|---|---|
| **Critical** | Script bug that produces wrong output, security vulnerability, data loss risk, dependency that silently fails |
| **Important** | Missing error handling on likely failure paths, missing edge cases, poor performance on realistic inputs, outdated references |
| **Minor** | Code style, naming, documentation gaps, optimization opportunities |

## Output

Update the Scratchpad with all technical findings. Each finding should include:
- Tag: `[TECHNICAL]`
- Severity: Critical / Important / Minor
- What: specific issue
- Where: file, function, or line
- Why it matters
- Suggested fix

Then proceed to Stage 3.
