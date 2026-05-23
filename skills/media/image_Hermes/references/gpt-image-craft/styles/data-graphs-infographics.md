# Data, graphs, dashboards, and infographics

## Contents

- [Precision rule](#precision-rule)
- [Graph and chart style](#graph-and-chart-style)
- [Dashboard screenshot style](#dashboard-screenshot-style)
- [Infographic poster](#infographic-poster)
- [Visual wiki](#visual-wiki)
- [Timeline](#timeline)
- [Process flow](#process-flow)
- [Comparison matrix](#comparison-matrix)
- [Map and location graphic](#map-and-location-graphic)
- [Executive slide chart](#executive-slide-chart)

## Precision rule

For exact chart outputs, use deterministic charting code first. Image generation can create a polished chart-like visual, but it may invent values, misplace axes, or render labels incorrectly. When the user supplies exact data, either generate the chart with code and use image generation only for surrounding design, or include the exact numbers and inspect the output.

## Graph and chart style

Best for visually explaining trends when exact precision is less important or when the generated output is a concept mockup.

Prompt levers:

- name the chart type: bar, line, scatter, slope, Sankey, funnel, heatmap;
- provide exact data and labels;
- specify axis titles, legend, units, and source note;
- use high quality for labels.

Template:

```text
Create a clean [chart type] visualization as a polished editorial graphic.
Data: [list exact values].
Axes: x-axis [label], y-axis [label and units].
Title: "[exact title]".
Style: white background, high-contrast readable labels, restrained palette, clear legend, no decorative clutter.
Source note: "[exact source note]".
Quality bar: labels and numbers must be readable.
```

## Dashboard screenshot style

Best for SaaS concepts, analytics UIs, investor slides, product mockups, and internal tools.

Prompt levers:

- describe it like a real app, not concept art;
- specify navigation, cards, widgets, tables, charts;
- include realistic but not misleading dummy data;
- request no lorem ipsum.

Template:

```text
Create a realistic web analytics dashboard UI mockup for [product/team].
Canvas: landscape 1536x1024.
Layout: left sidebar navigation, top filter bar, KPI cards, main line chart, small table, status panel.
Data labels: [short labels].
Style: clean production SaaS UI, modern sans-serif, generous spacing, accessible contrast, subtle borders.
Constraints: no lorem ipsum, no unreadable microtext, no fake brand logos, no decorative stock art.
```

## Infographic poster

Best for public explainers, educational summaries, marketing reports, and trend visuals.

Prompt levers:

- define audience and reading path;
- use sections with clear hierarchy;
- use exact text in short chunks;
- request icons, callouts, and white space.

Template:

```text
Create a vertical infographic poster explaining [topic] for [audience].
Reading path: top headline, three numbered sections, bottom takeaway.
Exact headline: "[headline]".
Sections: [section names and one-sentence content].
Visual system: clean editorial infographic, readable typography, simple icons, consistent colors, generous white space.
Avoid tiny paragraphs, invented statistics, and decorative clutter.
```

## Visual wiki

Best for dense but organized topic pages, species cards, history explainers, and encyclopedia-style spreads.

Prompt levers:

- use a central hero image with surrounding fact cards;
- provide fact content;
- use map/photo/diagram placeholders only if supplied or clearly generic;
- avoid invented facts.

Template:

```text
Create a magazine-style visual wiki spread about [topic].
Audience: [audience].
Layout: central illustration/photo area, surrounding fact cards, small timeline, key terms box.
Exact facts to include: [facts].
Style: polished educational magazine design, strong hierarchy, readable labels, restrained colors.
Constraints: no invented statistics, no fake citations, no tiny text.
```

## Timeline

Best for history, product roadmaps, project plans, scientific processes, and narrative sequences.

Prompt levers:

- provide exact dates and milestones;
- specify horizontal or vertical;
- limit copy per milestone;
- use icons only as supportive markers.

Template:

```text
Create a [horizontal/vertical] timeline graphic titled "[title]".
Milestones: [date — label — short note].
Style: clean editorial timeline, clear date hierarchy, simple icons, readable text, ample spacing.
Avoid extra dates, invented events, cramped labels, and decorative backgrounds.
```

## Process flow

Best for workflows, pipelines, causal chains, user journeys, and system architecture concepts.

Prompt levers:

- name each node;
- specify arrow direction;
- choose swimlanes when multiple actors are involved;
- use simple shapes and labels.

Template:

```text
Create a process-flow diagram for [workflow].
Layout: [left-to-right / top-to-bottom / swimlane].
Nodes: [ordered list].
Arrows: show [flow type].
Style: clean product documentation diagram, rounded rectangles, readable labels, minimal icons.
Constraints: no extra steps, no unlabeled arrows, no tiny text.
```

## Comparison matrix

Best for feature comparisons, buyer guides, teaching contrasts, and strategy slides.

Prompt levers:

- provide row/column headers;
- keep entries short;
- use checkmarks sparingly;
- prefer clarity over decoration.

Template:

```text
Create a clean comparison matrix titled "[title]".
Columns: [list].
Rows: [list].
Cell content: [short values].
Style: polished report graphic, white background, subtle grid, high readability.
Avoid invented entries, tiny text, and decorative illustrations.
```

## Map and location graphic

Best for route concepts, neighborhood explainers, fantasy maps, wayfinding, and geographic infographics.

Prompt levers:

- distinguish real maps from illustrative maps;
- provide labels and locations;
- use “not geographically exact” when appropriate;
- avoid false precision.

Template:

```text
Create an illustrative map-style graphic of [place/concept].
Purpose: [travel guide / wayfinding / fantasy map / data map].
Required labels: [list].
Visual system: clean cartographic illustration, readable place names, simple icons, muted palette.
Constraints: if not using exact GIS data, make it clearly illustrative rather than authoritative.
```

## Executive slide chart

Best for pitch decks, strategy memos, board updates, and executive summaries.

Prompt levers:

- choose 16:9 landscape;
- limit to one message;
- provide data and exact footnotes;
- request deck-style spacing and hierarchy.

Template:

```text
Create one 16:9 executive slide titled "[title]".
Main message: [one sentence].
Visual: [chart/diagram] using these values: [data].
Include footnote: "[source]".
Style: real consulting/startup deck slide, white background, modern sans-serif, clear hierarchy, polished spacing.
Avoid clip art, fake logos, gradients, and generic stock-photo treatment.
```
