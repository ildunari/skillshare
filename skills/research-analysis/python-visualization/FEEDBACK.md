# Feedback Log — Python Visualization

> **MUST-READ** when loading this skill. Max 75 entries. Category-tagged.
> Categories: [matplotlib] [seaborn] [publication] [export] [styling] [accessibility] [general] [plotly] [animation] [pandas-styler] [rdkit] [biomedical] [latex]

---

2025-02-18 [biomedical] **D10/D50/D90 label collision — FIXED.** All three percentile labels were placed at the same y-level (`ax.get_ylim()[1]*0.95`), colliding for narrow distributions (low PDI). Fixed by staggering labels at 0.92/0.76/0.60 of y-range with white bbox background. Affected `biomedical-plots.md` and `scripts/biomedical_templates.py`.

2025-02-18 [biomedical] **IC50 annotation hardcoded y-offset — FIXED.** `mid_y + 15` was in data units assuming 0–100% response scale. Breaks silently for 0–1 or 0–10000 scales. Replaced with `mid_y + 0.15 * (yhi - ylo)`. Affected `biomedical-plots.md` and `scripts/biomedical_templates.py`.

2025-02-18 [biomedical] **Cmax/Tmax annotation hardcoded data-unit offset — FIXED.** `xytext=(tmax+5, cmax+10)` fails for minute-scale or μg/mL-scale data. Replaced with `textcoords='axes fraction'` at `(0.6, 0.82)` so annotation stays on-canvas regardless of axis range. Affected `biomedical-plots.md` and `scripts/biomedical_templates.py`.

2025-02-18 [publication] **Significance bracket hardcoded y-positions — FIXED.** `add_significance_bar(ax, ..., 135, 3)` used magic numbers valid only for the example's `ylim(0, 180)`. Replaced with data-derived positions: `bar_top + 0.04 * yhi`. Affected `references/publication-examples.md`.

2025-02-18 [matplotlib] **Heatmap cell annotation without size gate — FIXED.** Template annotated every cell unconditionally. For matrices >15×15 (common in gene expression), this produces 2,500+ overlapping labels. Added guard: only annotate if rows ≤ 15 and cols ≤ 15, with adaptive fontsize. Affected `references/matplotlib-plot-types.md`.

2025-02-18 [general] **Label Placement Rules section added to SKILL.md.** Covers: relative offsets, staggered labels, matrix annotation gates, significance bracket derivation, panel label x-offset guidance. Root cause documented: LLMs have no render loop, so all label positions are predictions — defensive patterns must be the default, not an afterthought.

