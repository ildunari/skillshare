# Science, education, and figures

## Contents

- [General rules](#general-rules)
- [Scientific textbook style](#scientific-textbook-style)
- [Biology pathway diagram](#biology-pathway-diagram)
- [Anatomical or medical plate](#anatomical-or-medical-plate)
- [Chemistry mechanism or lab visual](#chemistry-mechanism-or-lab-visual)
- [Physics concept diagram](#physics-concept-diagram)
- [Math proof visual](#math-proof-visual)
- [Engineering cutaway](#engineering-cutaway)
- [Astronomy or geology explainer](#astronomy-or-geology-explainer)
- [Academic poster](#academic-poster)
- [Lab safety or procedural poster](#lab-safety-or-procedural-poster)

## General rules

Scientific visuals should be prompt-written like instructional design briefs. Define the learner, the lesson objective, required labels, scientific constraints, and what must not be shown. Use clean white space and consistent visual language before adding style.

Use `quality: high` for dense labels, publication figures, diagrams, and any output intended for slides or course materials.

When accuracy matters, provide the facts. Do not ask the image model to invent data, molecular structures, medical claims, or causal mechanisms.

## Scientific textbook style

Best for classroom figures, study guides, handouts, and explainer visuals.

Prompt levers:

- “clean textbook figure”, “white background”, “flat scientific icon system”;
- audience level: middle school, high school, undergraduate, expert;
- readable labels with simple arrows;
- avoid decoration, tiny text, and extra objects.

Template:

```text
Create a clean textbook-style figure for [audience] explaining [concept].
Use a white background, flat scientific illustration, consistent line weight, muted academic colors, clear arrows, and readable sans-serif labels.
Show only these components: [list].
Title: "[exact title]".
Avoid tiny text, decorative clutter, inaccurate anatomy/structures, and extra unlabeled elements.
```

## Biology pathway diagram

Best for metabolic pathways, signaling cascades, cell biology, ecology cycles, and gene-expression summaries.

Prompt levers:

- group pathway stages into zones;
- specify inputs, outputs, arrows, and compartments;
- explicitly name molecules to avoid hallucinated labels;
- request “not a full biochemical map” when the goal is a simplified handout.

Template:

```text
Create a simplified biology pathway diagram for [audience] showing [pathway].
Layout: left-to-right flow with grouped zones: [zone 1], [zone 2], [zone 3].
Required labels: [molecules, organelles, products].
Visual system: clean classroom handout, white background, flat icons, readable labels, consistent arrows.
Scientific constraints: [what is true / what to omit].
Avoid dense biochemical notation, tiny text, extra pathways, and decorative backgrounds.
```

## Anatomical or medical plate

Best for anatomy, physiology, medical education, patient-friendly explainers, and non-diagnostic visuals.

Prompt levers:

- label anatomical structures explicitly;
- choose between realistic medical illustration and simplified patient education;
- avoid gore unless requested and safe;
- do not imply diagnosis, treatment, or clinical certainty.

Template:

```text
Create a medical textbook illustration of [body system/structure] for [audience].
View: [cross-section, anterior, sagittal, close-up].
Style: clean anatomical plate, muted medical palette, precise labels, subtle shading, white background.
Required labels: [list].
Constraints: educational, non-gory, no diagnosis text, no treatment recommendations, no extra structures.
```

## Chemistry mechanism or lab visual

Best for reaction overviews, lab apparatus, molecular-scale explainers, and process diagrams.

Prompt levers:

- specify whether to show molecular structures, apparatus, or conceptual particles;
- give exact labels and formulae if needed;
- ask for “conceptual not publication-accurate structure” if exact chemistry is not supplied;
- for lab apparatus, name each glassware item.

Template:

```text
Create a clean chemistry classroom diagram explaining [process/reaction].
Show: [apparatus or molecules].
Required labels and formulae: [exact labels].
Layout: numbered steps with arrows, white background, consistent blue-gray line art.
Constraints: no invented chemical names, no extra equations, no tiny text, no unsafe procedural instructions beyond the educational overview.
```

## Physics concept diagram

Best for forces, fields, optics, circuits, thermodynamics, mechanics, and wave behavior.

Prompt levers:

- make vectors and coordinate systems explicit;
- provide equations only if exact;
- request clean arrows and symbols;
- specify what should be qualitative vs quantitative.

Template:

```text
Create a physics concept diagram for [audience] explaining [concept].
Visual: clean vector-style classroom figure on a white background.
Include: [objects], force arrows labeled [labels], coordinate axes [if needed], and short callouts.
Use accurate relative arrow directions. Avoid clutter, tiny labels, decorative effects, and extra formulas.
```

## Math proof visual

Best for visual proofs, blackboard images, infographics explaining a theorem, and conceptual diagrams.

Prompt levers:

- provide exact symbolic text;
- keep equations short;
- split complex proofs into panels;
- specify “visual proof, not a dense derivation”.

Template:

```text
Create a visual math proof poster titled "[title]" for [audience].
Use [blackboard / whiteboard / clean infographic] style.
Panels: [panel 1], [panel 2], [panel 3].
Exact symbols/labels: [list].
The layout should emphasize the intuition: [intuition].
Avoid long equations, invented notation, and hard-to-read handwriting.
```

## Engineering cutaway

Best for machines, devices, systems, architecture, manufacturing, and hardware explainers.

Prompt levers:

- request exploded view, cutaway, or flow diagram;
- name subcomponents and material cues;
- use arrows for flow/energy/material;
- avoid “cool sci-fi” unless the system is fictional.

Template:

```text
Create a technical cutaway diagram of [device/system] for [audience].
View: [exploded / cross-section / isometric cutaway].
Show and label: [components].
Use precise clean line art, subtle material colors, arrows showing [flow], and generous spacing.
Avoid decorative clutter, invented components, and tiny labels.
```

## Astronomy or geology explainer

Best for planetary science, rock cycles, layers of Earth, eclipses, weather, climate, and spatial scale.

Prompt levers:

- specify scale relationships when important;
- use cross-sections for layers;
- add legends only with exact labels;
- avoid pseudo-realistic space imagery when the goal is explanation.

Template:

```text
Create an educational infographic explaining [astronomy/geology concept] for [audience].
Layout: [cross-section / sequence / scale comparison].
Required labels: [list].
Style: polished science museum exhibit graphic, dark or white background as appropriate, readable labels, clear arrows.
Constraints: show scale qualitatively unless exact numbers are provided, no invented facts, no clutter.
```

## Academic poster

Best for paper summaries, conference posters, research explainers, and literature-review visuals.

Prompt levers:

- use title, sections, method/results/impact blocks;
- avoid text-heavy paragraphs;
- include chart-like shapes only with supplied data;
- specify “poster mockup” if not final readable content.

Template:

```text
Create a polished academic poster-style infographic summarizing [topic/paper].
Sections: Motivation, Method, Key Result, Impact.
Use a clean conference-poster layout, readable section headers, restrained color palette, diagram placeholders, and concise callout boxes.
Exact text to include: [short text].
Avoid fabricated citations, tiny paragraphs, and fake data.
```

## Lab safety or procedural poster

Best for visual instructions, public health explainers, safety signage, and process reminders.

Prompt levers:

- use numbered steps;
- include icons and short labels;
- do not include unsafe procedural details;
- make hazards and PPE clear.

Template:

```text
Create a lab safety poster for [audience/context].
Format: vertical poster, numbered steps, simple icons, high-contrast headings.
Include: [PPE, hazard icons, safety reminders].
Exact text: [short phrases].
Avoid complex procedural instructions, tiny text, alarming imagery, and unrelated decorations.
```
