---
name: document-to-tts-transcript
description: Use when the user wants a full document turned into a faithful plain-text transcript for text-to-speech, especially for academic PDFs with figures, charts, tables, equations, or other visuals that must be described rather than summarized. Trigger on requests to make a paper listenable, create an audio-ready transcript, narrate a PDF, or preserve all document content in TTS-friendly prose.
---

# Document-to-TTS Transcript

Transform academic documents into complete audio-ready transcripts with interpretive visual analysis.

## When to Use

Trigger phrases:
- "Convert to TTS transcript"
- "Make this listenable" / "narrate this paper"
- "Audio-ready version with visual descriptions"
- "TTS transcript - describe all figures"

## Core Requirements

### 1. Complete Fidelity - No Omissions
- Include every sentence, data point, equation, table, figure, and reference
- No summarization or paraphrasing to shorten
- If content is unreadable, mark it: "[Page X requires OCR]"

### 2. Visual Analysis - Interpret What You See
**You have vision capabilities.** Look at every figure, graph, chart, and image. Don't just mechanically describe axes and values - **interpret patterns, trends, and relationships.**

**Be analytical:**
- Identify trends not explicitly stated in captions
- Note correlations, anomalies, and patterns
- Compare data across conditions
- Point out what stands out visually
- Describe the story the data tells

**Example - Mechanical (don't do this):**
> "Figure 1 shows a bar chart. X-axis has groups A, B, C. Y-axis ranges from 0 to 100. Bar A is 42, bar B is 73, bar C is 51."

**Example - Interpretive (do this):**
> "Figure 1 reveals that Treatment B achieves substantially higher response compared to control and other treatments, with nearly 75 percent efficacy. This represents a 30-point improvement over control. Notably, Treatment C shows only modest improvement, suggesting the mechanism in Treatment B may be unique. The error bars indicate Treatment B's effect is consistent across replicates."

### 3. Plain Text Output
Output **only plain text** - no markdown, no formatting.
- Don't use: `**bold**`, `#headers`, `- bullets`, `> quotes`, ` ``` `, `[links]`
- Do use: "Section: Title" not `## Title`
- Simple punctuation only: periods, commas, semicolons, colons

### 4. Jargon-Free Language
Avoid: "leverage," "unlock," "dive deep," "unpack," "paradigm shift," "synergy," "ecosystem," "at the end of the day," "in this space"

Use: Direct, clear, factual narration

## Visual Content Analysis Protocol

### For Every Figure, Graph, Chart, Image:

**Step 1: Announce**
```
Figure 3: Cell viability under different conditions.
```

**Step 2: Look and Interpret**
Use your visual analysis to examine the visual. Identify:
- **Patterns**: trends, correlations, groupings
- **Comparisons**: which is highest/lowest, differences between groups
- **Anomalies**: outliers, unexpected results
- **Relationships**: how variables relate to each other
- **Key findings**: what the visual reveals

**Step 3: Provide Interpretive Description**

Describe both WHAT is shown and WHAT IT MEANS:

```
Example: Bar Chart

Figure 2: Response rates across treatments.

This figure demonstrates that Treatment B produces markedly superior results, achieving approximately 73 percent response rate compared to only 42 percent in control. Treatment A shows moderate improvement at 58 percent, while Treatment C performs similarly at 51 percent. 

The data suggests a dose-response relationship may exist, though Treatment C's lower-than-expected performance is notable. Error bars indicate reasonable consistency within groups, though Treatment B shows slightly more variability, possibly due to individual response differences.

An interesting pattern not explicitly discussed in the text is the roughly 15-point gap between Treatment A and C, despite similar mechanisms, suggesting C's delivery method may be less effective.
```

### Visual Content Types

**Bar Charts / Column Graphs:**
- Compare heights - which dominates, which lags
- Identify patterns (increasing, decreasing, grouped)
- Note outliers or exceptions
- Describe magnitude of differences

**Line Graphs:**
- Describe trajectories - rising, falling, stable, oscillating
- Identify inflection points and phase transitions
- Compare curves - parallel, diverging, converging
- Note rate of change - gradual vs. steep

**Scatter Plots:**
- Identify correlations - positive, negative, none
- Note clustering or distinct populations
- Point out outliers and their significance
- Describe distribution density

**Heatmaps:**
- Identify hot/cold regions
- Describe gradients and boundaries
- Note symmetry or asymmetry patterns
- Point out unexpected cold spots in hot regions

**Microscopy / Photos:**
- Describe morphology changes
- Compare control vs. treatment
- Quantify prevalence (approximately X percent show...)
- Note spatial patterns

**Multi-Panel Figures:**
- Describe progression across panels
- Identify what changes panel-to-panel
- Note consistent vs. varying elements

### Interpretive Principles

**Go beyond mechanical description:**
- Not just "line goes up" but "exhibits exponential growth"
- Not just "bars differ" but "demonstrates clear dose-dependent effect"
- Not just "points scattered" but "shows weak correlation suggesting other factors dominate"

**Make observations:**
- "Interestingly..."
- "Notably..."
- "This suggests..."
- "The data reveal..."
- "An unexpected pattern emerges..."

**But stay grounded:**
- Base interpretations on visible data
- Don't invent values not shown
- Qualify uncertainties: "approximately," "appears to," "suggests"
- Don't contradict explicit paper conclusions

## Tables

Narrate row-by-row with interpretive context:

```
Table 1: Kinetic parameters for enzyme variants.

This table reveals how mutations affect enzyme efficiency. 

Wild Type shows moderate activity with Km of 12.3 micromolar and kcat of 45.6 per second, establishing the baseline at 100 percent relative activity.

The A123G mutation demonstrates improved performance, achieving 162 percent relative activity through both reduced Km at 8.7 micromolar, indicating stronger substrate binding, and increased kcat at 52.1 per second, indicating faster turnover.

In contrast, the L456P mutation impairs function, dropping to only 68 percent activity. The elevated Km of 18.9 micromolar suggests weaker substrate affinity, while decreased kcat of 31.2 per second indicates slower catalysis. This mutation appears to disrupt both binding and catalytic steps.
```

## Equations

Provide spoken form plus interpretation:

```
Equation 1: v equals V max times S, divided by K m plus S.

This is the Michaelis-Menten equation describing enzyme kinetics. It shows that reaction velocity approaches maximum velocity as substrate concentration increases, with Km representing the substrate concentration at half-maximal velocity. The hyperbolic relationship means enzyme efficiency increases rapidly at low substrate but plateaus at saturation.
```

## Numbers and Units

Speak naturally:
- "2.3 micrometers" for 2.3 μm
- "ten to the minus three" for 10⁻³
- "plus or minus 4.2 percent" for ±4.2%
- "thirty-two degrees Celsius" for 32°C

## Document Structure

Process in order, announcing sections:

```
Title: [Title]
Authors: [Names and affiliations]
Published: [Venue, year]

Section: Abstract
[Complete abstract]

Section: Introduction
[Full introduction]

Figure 1: [Caption]
[Interpretive visual description]

Section: Methods
[Complete methods]

Table 1: [Caption]
[Interpretive table narration]

[Continue through all sections]

Section: References
Reference 1: [Full citation]
Reference 2: [Full citation]
[All references]
```

## Output Example

```
Title: Machine Learning for Drug Discovery
Authors: Jane Smith, MIT; John Doe, Stanford
Published: Nature, 2024

Section: Abstract

Recent advances in machine learning have transformed drug discovery...

Section: Introduction

Traditional drug development requires extensive screening...

Figure 1: Overview of ML pipeline.

This figure illustrates the five-stage workflow. The pipeline begins with data collection from multiple compound databases, proceeds through feature extraction focusing on molecular descriptors, applies neural network training with cross-validation, performs virtual screening on candidate libraries, and concludes with experimental validation. 

A key insight from this diagram is the feedback loop between experimental results and model retraining, suggesting an iterative improvement strategy. The parallel processing indicated in the screening stage explains the computational efficiency claims made in the introduction.

Section: Methods

Subsection: Dataset Preparation

We compiled 150,000 compounds from PubChem...
```

## Quality Checklist

Before finalizing:
- [ ] All sections included (abstract → references)
- [ ] Every figure visually analyzed with interpretation
- [ ] Tables narrated with context
- [ ] Plain text output (no markdown)
- [ ] No jargon or buzzwords
- [ ] Natural spoken language

## Examples of Interpretive vs. Mechanical

**Mechanical (avoid):**
> "Figure shows x-axis labeled dose, y-axis labeled response, with three data points at coordinates 1,20 and 5,60 and 10,85."

**Interpretive (preferred):**
> "Figure demonstrates a clear dose-response relationship, with efficacy increasing from 20 percent at low dose to 85 percent at high dose. The steeper rise between mid and high doses suggests a threshold effect may be operating."

**Mechanical (avoid):**
> "Table has four rows. Row 1: control, 12.3, 45.6. Row 2: treatment, 8.7, 52.1."

**Interpretive (preferred):**
> "Table reveals that treatment improves both substrate binding, evidenced by the 30 percent reduction in Km, and catalytic efficiency, shown by the 14 percent increase in kcat. These combined effects explain the 62 percent improvement in overall activity."

## Special Cases

**Multi-column PDFs:** Reconstruct logical reading order
**Scanned PDFs:** Use OCR or mark as "[Page X needs OCR]"
**Long documents:** Process in continuous flow, state page ranges if breaking into parts
**Multiple languages:** Narrate all language versions present

## Time Estimates

Provide listening time: word count ÷ 150 words/minute
- 6,000-word paper ≈ 40 minutes
- 50,000-word thesis ≈ 5.5 hours

## Final Reminders

1. **LOOK at visuals** - use your vision capabilities
2. **INTERPRET patterns** - don't just mechanically describe
3. **STAY GROUNDED** - base interpretations on visible data
4. **PLAIN TEXT** - no markdown formatting
5. **COMPLETE** - include everything, no omissions
6. **NATURAL LANGUAGE** - speak like a knowledgeable narrator explaining findings to an interested listener
