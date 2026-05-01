# Contrast calculation and design-system fixes

Use this when a residual finding involves text contrast, chart/icon contrast, or ambiguity caused by theme colors or layered backgrounds.

## WCAG thresholds

- Normal text: WCAG 1.4.3 requires at least 4.5:1.
- Large text: at least 3:1 when text is 18 pt or larger, or 14 pt or larger and bold.
- Meaningful non-text graphics and UI-like controls: WCAG 1.4.11 requires at least 3:1 against adjacent colors.
- Logos and purely decorative graphics are exceptions, but do not overuse exceptions for charts, icons, labels, or callouts.
- Do not round ratios up. A computed 4.499 fails 4.5.

## Effective color resolution

Before proposing a fix, determine the effective foreground and background:

1. Inspect the element: `officecli get file path --json`.
2. Resolve inherited text color from run, paragraph, shape, placeholder, layout, master, or theme.
3. Resolve background from shape fill, table cell fill, slide background, image/gradient overlay, or document page background.
4. If the object is over a photo or gradient, use the local area behind the text. When exact sampling is unavailable, ask the user or choose a conservative fix such as an accessible solid overlay.
5. Resolve Office theme slots (`accent1`, `accent2`, `lt1`, `dk1`, `hlink`, etc.) from the relevant theme XML when available.

Use the script for deterministic math:

```bash
python scripts/contrast.py --fg "#777777" --bg "#FFFFFF"
python scripts/contrast.py --fg-theme accent2 --bg-theme lt1 --theme path/to/theme1.xml
python scripts/contrast.py --fg "#888888" --bg "#FFFFFF" --font-size-pt 14 --bold
python scripts/contrast.py --fg "#9AA0A6" --bg "#FFFFFF" --non-text
```

The script returns JSON with resolved colors, ratio, threshold, and pass/fail.

## Preferred fix order

Make the smallest change that restores accessible contrast while preserving the design system.

1. Use a nearby approved theme color with sufficient contrast.
2. Adjust the background token/fill if the foreground is a brand color that should stay fixed.
3. Add or strengthen a solid/semitransparent shape behind text over photos.
4. For charts, change the specific low-contrast series, marker, or label, not the whole chart palette.
5. For UI-like icons and lines, adjust stroke/fill or adjacent background to 3:1.
6. Avoid “just darken the text” when it breaks brand hierarchy or makes only one instance inconsistent.

## Commands

Word text color or cell background:

```bash
officecli set report.docx /body/p[14] --prop color=1F1F1F
officecli set report.docx /body/tbl[2]/tr[1]/tc[1] --prop shd=FFFFFF --prop color=1F1F1F
```

PowerPoint shape or run:

```bash
officecli set deck.pptx /slide[6]/shape[3]/run[1] --prop color=1F1F1F
officecli set deck.pptx /slide[6]/shape[3] --prop fill=FFFFFF
```

When color is controlled by a theme, prefer changing the local element unless the manifest explicitly targets the theme. Theme-level changes can affect many unrelated elements and are high impact.
