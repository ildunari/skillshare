---
title: Data visualization
scope: pptx-master
version: 1.0
---

# Data visualization

pptx-master’s data-viz rules are tuned for **executive readability**: clear labels, controlled color, and a single “story” highlight.

This doc covers:

- chart type selection (what to use when)
- chart styling (theme-aware)
- how to represent charts/tables in IR
- rendering notes for PptxGenJS

---

## Chart selection guidelines

| Goal | Recommended chart | Avoid |
|---|---|---|
| Compare categories | bar/column | pie (unless very few categories) |
| Trend over time | line / area | crowded stacked area with many series |
| Part-to-whole | 100% stacked bar, donut (≤ 5 slices) | complex multi-slice pie |
| Distribution | histogram (as bar) | overdecorated boxplots |
| Relationship | scatter | 3D charts |

### “One story color” rule

Even if a chart has multiple series, keep **one** visually dominant series:

- story series: `primary`
- context series: `muted` (or gray)
- extra categorical: `series_1..series_6` (only when needed)

---

## Theme-aware styling rules

Colors come from the palette tokens:

- axes/ticks: `axis`
- gridlines: `gridline` (very light; low opacity)
- annotation region fill: `annotation`
- data highlight: `primary`
- status deltas: `good`, `warn`, `bad`

Typography:

- axis labels: 12–14 pt
- data labels: 12–14 pt (only if needed)
- chart title: 16–18 pt (often omitted if the slide headline is the title)

---

## IR representation

### Chart element

A chart can be represented either as:

1) a native PPT chart (`semantic_type: "chart"` + `data`), or  
2) a pre-rendered image (still `semantic_type: "chart"` but with `src`).

Minimal example:

```json
{
  "id": "chart:0",
  "semantic_type": "chart",
  "bbox": { "x": 0.7, "y": 1.7, "w": 9.0, "h": 5.1 },
  "data": {
    "chartType": "bar",
    "series": [
      { "name": "Current", "labels": ["A","B","C"], "values": [10, 12, 7] }
    ]
  },
  "style_tokens": {
    "chart": { "story_series_index": 0 }
  }
}
```

### Table element

Tables should be kept *simple*:

- 4–8 columns max (depending on density)
- 6–12 rows max per slide

```json
{
  "id": "table:0",
  "semantic_type": "table",
  "bbox": { "x": 0.7, "y": 1.7, "w": 11.9, "h": 4.9 },
  "data": {
    "columns": ["Metric","Q1","Q2","Q3","Q4"],
    "rows": [
      ["Revenue", 10, 12, 14, 15],
      ["GM%", "52%", "54%", "53%", "55%"]
    ]
  },
  "style_tokens": {
    "table": { "zebra": true, "header_fill": "surface" }
  }
}
```

---

## Renderer notes (PptxGenJS)

PptxGenJS supports native charts via `slide.addChart(type, data, options)`.

Supported chart types include:

- `area`, `bar`, `bar3D`, `bubble`, `doughnut`, `line`, `pie`, `radar`, `scatter`, `stock`

Data format (single-series example):

```js
slide.addChart(
  pptx.ChartType.bar,
  [{ name: "Sales", labels: ["Jan","Feb"], values: [10,20] }],
  { x: 0.7, y: 1.7, w: 9.0, h: 5.1 }
);
```

Reference implementation lives in the upstream library source (see comments around `addChart(...)`):
- https://github.com/gitbrent/PptxGenJS

### Image resolution rule

If the renderer rasterizes charts (SVG/PNG):

- target **≥ 150 DPI effective** at the final displayed size
- small charts can be lower, but avoid visible blur

(See `scripts/preflight_pptx.py` image DPI checks.)

