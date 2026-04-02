# Stage 3: Prompt Review

Evaluate the quality of the skill's instructions, constraints, and behavioral
directives as prompting for Claude 4.5/4.6. This is typically the highest-leverage
stage. A skill can have perfect structure and clean code but still produce poor
results if its instructions are miscalibrated.

Re-read the skill's SKILL.md and all reference files with prompt-quality eyes
during this stage.

## The Three Meta-Principles

<!-- Calibration principles derived from prompt-architect — sync periodically -->

Everything in this stage flows from three principles that define effective
prompting on Claude 4.5/4.6:

1. **Literalism is the default.** These models follow instructions as written,
   not as intended. They will not infer unstated requirements or go "above and
   beyond" unless explicitly told to. If the skill expects thoroughness, creative
   latitude, or implicit completeness, those must be stated.

2. **Softer language produces better results.** The calibration spectrum has
   shifted. Aggressive emphasis (CRITICAL, MUST, ALWAYS, NEVER) causes
   overtriggering — the model obsessively follows the emphasized instruction at
   the expense of judgment. Conditional guidance with rationale ("Use X when Y,
   because Z") consistently outperforms imperative commands.

3. **Context minimalism outperforms context maximalism.** Frontier models reliably
   follow approximately 150-200 individual instructions. Beyond this, compliance
   degrades uniformly. Every unnecessary instruction dilutes attention on what
   matters.

## Checklist

### 3.1 Instruction Calibration

The most impactful check. Scan the entire skill for intensity markers and evaluate
each one.

**The calibration spectrum (optimal → harmful on 4.5/4.6):**

| Level | Pattern | When to use |
|---|---|---|
| Explained conditional | "Use X when Y, because Z" | **Default — optimal for all models** |
| Normal imperative | "Use X when Y" | Acceptable baseline |
| Conditional | "If Y, then use X" | Good, may slightly undertrigger on ambiguous cases |
| Strong imperative | "Always use X" | Only for genuine hard stops |
| Aggressive imperative | "CRITICAL: MUST ALWAYS X" | **Avoid** — causes overtriggering |

**Scan for these markers:**
ALL CAPS words, exclamation marks for emphasis, CRITICAL, MUST, ALWAYS, NEVER,
MANDATORY, IMPORTANT, DO NOT, YOU MUST, UNDER NO CIRCUMSTANCES.

**For each marker, classify:**
- Is this a genuine safety-critical hard stop? → Keep, but consider rewriting in
  third-person descriptive form ("Claude does not...")
- Is this a strong preference? → Rewrite as explained conditional
- Is this anti-laziness language ("be thorough", "think carefully", "explore all
  possibilities")? → Remove entirely. These cause Opus 4.6 to over-explore,
  burning tokens and adding latency without improving quality.

**Count total instructions.** Each discrete behavioral directive is one
instruction. A five-item checklist = 5. A paragraph with three behavioral
expectations = 3. Flag if the skill (including all reference files that would
be loaded together) approaches 150 instructions.

### 3.2 Constraint Quality

Evaluate every constraint, prohibition, and behavioral rule in the skill.

**Pattern 1 — Positive framing:** Constraints should tell the model what to do,
not what not to do. Negative instructions highlight the forbidden concept, keeping
it active in the attention window (the "pink elephant effect").

| Negative (flag) | Positive (suggest) |
|---|---|
| "Do not use markdown" | "Write in flowing prose paragraphs" |
| "Don't use bullet points" | "Incorporate items naturally into sentences" |
| "Never use filler phrases" | "Begin responses by addressing the substance directly" |
| "Don't speculate" | "State what you can confirm, then note what remains uncertain" |

If a constraint can't be easily reframed positively, it may be too vague. "Don't
be boring" has no clear positive equivalent because it doesn't define what the
skill actually wants. Flag vague constraints.

**Pattern 2 — Motivated constraints:** Rules with rationale generalize better.

Without motivation (brittle):
```
Avoid ellipses in output.
```

With motivation (generalizable):
```
Avoid ellipses — the TTS engine processing this output cannot handle them.
```

The model now understands the underlying constraint (TTS compatibility) and can
apply the same reasoning to analogous situations.

Check: Does each non-obvious rule explain WHY it exists?

**Pattern 3 — Prohibition + alternative:** Hard prohibitions should pair with an
explicit approved alternative. Without the alternative, the model may freeze,
refuse entirely, or find creative workarounds that are worse.

```
Do not fabricate citations. When you cannot verify a source, flag it as
"NEEDS VERIFICATION" and provide the claim without attribution.
```

Check: Does every prohibition tell the model what to do INSTEAD?

**Pattern 4 — Framing selection:** Different content types need different framing.

| Content type | Optimal framing |
|---|---|
| Core identity / role definition | Third-person descriptive: "This assistant is..." |
| Safety and ethical boundaries | Third-person descriptive: "Claude does not..." |
| Hard prohibitions | Third-person descriptive + alternative |
| Tool usage, formatting, workflow | Explained conditional: "Use X when Y, because Z" |
| Task-specific directives | Normal imperative or conditional |

Check: Are safety-critical constraints in third-person descriptive form? Are
behavioral instructions using explained conditionals? Is identity framing
overused for routine rules (wastes signal)?

**Pattern 5 — Conflict resolution:** When two constraints can plausibly conflict,
there should be explicit priority guidance.

Check: Are there constraint pairs that could conflict without resolution?
("Be concise" + "Be thorough", "Follow the template exactly" + "Use your
judgment to improve the output")

### 3.3 Failure Mode Hardening

Check whether the skill is vulnerable to these systematic failure patterns.

**Sycophancy:** Does the skill involve evaluation, feedback, or review? If so,
does it include anti-sycophancy measures? (Process requirements that force
analytical behavior, explicit instructions to present counterarguments, confidence
level requirements)

**Literalism / Under-specification:** Does the skill expect the model to go
"above and beyond" the literal instructions? If so, does it explicitly grant
creative latitude or completeness expectations? ("Include as many relevant
features as possible", "Use your judgment to add polish that would make this
production-ready")

**Overthinking (Opus 4.6):** Does the skill contain anti-laziness language that
would cause Opus 4.6 to over-explore? ("Be thorough", "Consider every angle",
"Explore all possibilities") These should be removed.

**Format drift:** For skills used in long conversations, are formatting rules
positioned to survive context compaction? (System prompt or Project instructions
persist; early user-turn instructions get displaced)

**Hallucinated compliance:** Does the skill ask the model to verify its own work?
If so, does it use investigation-before-answering patterns rather than trusting
self-reports? ("Read the relevant sources before answering" rather than "Make sure
you verified everything")

### 3.4 Agentic Flow

For skills that define multi-step workflows:

**Decision gates:** Are there clear decision points where the model should stop
and evaluate before proceeding? Or does the skill assume a linear path?

**Error recovery:** When a step fails, does the skill define what to do? Or does
it assume every step succeeds?

**State management:** For multi-turn workflows, how does the skill maintain state?
Is there a risk of the model losing track of where it is in the process?

**Checkpoint behavior:** Does the skill batch work and report progress, or does
it try to do everything in one shot?

### 3.5 Determinism and Reproducibility

**Check:**
- For tasks with objectively correct outputs, are the instructions precise
  enough that two invocations would produce consistent results?
- Are there ambiguous instructions that different model runs might interpret
  differently? ("Make it look good" vs "Use 16px body text, 1.5 line height,
  and the skill's color palette")
- Where judgment IS appropriate (creative tasks, analysis), is it clear what
  the model has latitude on and what's fixed?

### 3.6 Instruction Efficiency

**Check:**
- Are there redundant instructions? (Same directive stated differently in
  multiple places)
- Are there instructions the model would follow anyway without being told?
  (Basic capabilities like "read the file before responding")
- Could multiple related instructions be consolidated without losing meaning?
- Are there instructions that are never relevant? (Edge cases so rare they
  waste budget on every invocation)

### 3.7 Supplementary Material (if provided)

If the user provided research reports, reference implementations, or competitor
skills, evaluate the skill's instructions against those findings:

- Do the research findings suggest calibration adjustments the skill doesn't
  implement? (e.g., research shows softer emphasis works better but the skill
  uses aggressive markers)
- Does the supplementary material reveal prompt patterns the skill should adopt?
- Are there contradictions between the research and the skill's instruction
  approach?

## Severity Guide for Prompt Issues

| Severity | Threshold |
|---|---|
| **Critical** | Miscalibration that causes systematic wrong behavior (aggressive emphasis causing overtriggering, missing instructions causing the model to skip core functionality, conflicting constraints with no resolution) |
| **Important** | Calibration issues that degrade quality (unnecessary emphasis, missing rationale on non-obvious rules, negative framing, missing failure mode hardening) |
| **Minor** | Polish (instruction consolidation opportunities, minor framing improvements, redundancy) |

## Output

Update the Scratchpad with all prompt-quality findings. Each finding:
- Tag: `[PROMPTING]`
- Severity: Critical / Important / Minor
- What: specific issue with the exact text from the skill
- Where: file, section, and the problematic instruction
- Why it matters (what behavior this causes)
- Suggested rewrite (provide the improved text, not just "rewrite this")

Then proceed to Stage 4.
