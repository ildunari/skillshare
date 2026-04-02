# Computational Tool Reference

Each tool is a standalone Python CLI that reads an image and outputs JSON to stdout. All tools depend only on `numpy` and `Pillow`; optional dependencies noted below.

## Table of Contents

1. [palette_extract.py](#palette)
2. [ocr_extract.py](#ocr)
3. [segment_ui.py](#segment)
4. [grid_detect.py](#grid)
5. [corner_detect.py](#corner)
6. [gradient_fit.py](#gradient)
7. [visual_diff.py](#diff)
8. [Video tools](#video)

---

## palette_extract.py <a name="palette"></a>

K-means clustering in CIE LAB color space.

**Accuracy**: ±ΔE 3 for dominant colors; ΔE 5–10 for rare/accent colors.

**Method**:
- Downsample to 256px max for speed/stability
- CIE LAB conversion for perceptual clustering
- Elbow method for optimal K (range 4–14)
- ΔE2000 < 5 merge threshold for near-duplicates
- Semantic role guessing: surface, primary, accent, text-primary, text-secondary, neutral, error, success, warning

**Output**: `[{hex, rgb, lab, frequency, role_guess, confidence, samples}]`

**Confidence formula**: `min(0.95, 0.7 + frequency * 2)`

**Handles well**: Solid fills, flat UI.
**Struggles with**: Gradients (flattened to midpoint), photos (too many clusters), low-contrast designs.

**Tuning**: For minimalist UIs, narrow the range: `k_min=3, k_max=8`. For complex dashboards: `k_min=8, k_max=20`.

---

## ocr_extract.py <a name="ocr"></a>

Text extraction with font size and weight estimation.

**Accuracy**: Tesseract is reliable for 12px+ text on clean backgrounds. Font size within ±15%, weight within ±100.

**Method**:
- Tesseract OCR via subprocess (preferred)
- Fallback: basic contour-based text detection if Tesseract unavailable
- Font size estimation: `fontSize ≈ bbox_height * 0.75 / dpr`
- Weight estimation: stroke thickness via horizontal run-length analysis (100–900 scale)
- Role guessing: display, heading, title, subtitle, body-large, body, caption, overline

**Output**: `[{id, text, bbox_px, bbox_norm, fontSize_px, fontWeight_guess, lineHeight_px, role_hint, confidence}]`

**Confidence**: `OCR_conf * 0.8 + weight_conf * 0.2`

**Optional dependency**: `pytesseract` + Tesseract binary.

**Handles well**: Latin text, standard fonts, clean backgrounds.
**Struggles with**: Decorative fonts, text on complex backgrounds, <10px text, non-Latin scripts (without language packs).

---

## segment_ui.py <a name="segment"></a>

Non-text UI element detection via edge analysis.

**Accuracy**: 60–80% element detection rate. Good for rectangles, buttons. Misses overlapping or transparent elements.

**Method**:
- Auto-threshold Canny edge detection
- Contour detection via flood fill on edge image
- Rectangle fitting with area/aspect ratio filtering
- Type classification heuristics: icon (small, square), button (wide, short), input (very wide, short), container (large area), image (low edge density), navigation (very wide, top/bottom), scrollbar (tall, narrow), divider (wide, thin)
- IoU-based overlap removal (threshold 0.5)

**Output**: `[{id, bbox_px, bbox_norm, area, aspect_ratio, type_guess, confidence}]`

**Handles well**: Clean, high-contrast UIs with clear rectangular elements.
**Struggles with**: Overlapping layers, low-contrast designs, complex illustrations, glassmorphism effects.

---

## grid_detect.py <a name="grid"></a>

Layout grid detection via horizontal/vertical projection profiles.

**Accuracy**: Column count ±1, spacing ±4px. Very reliable for grid-based layouts.

**Method**:
- Grayscale conversion + edge detection
- Projection profiles: sum pixel intensity along each axis
- Gap detection: low-activity zones between content
- Cluster gap distances to find modal spacing values
- Snap to common grid systems (4px, 8px)

**Output**: `{columns, columnGap_px, rowGap_px, margins, spacingScale, alignmentGrid, confidence}`

**Handles well**: Standard column-based layouts, consistent spacing.
**Struggles with**: Overlapping layouts, non-grid designs, hero sections with full-bleed images.

---

## corner_detect.py <a name="corner"></a>

Border radius estimation via Harris corners + circle fitting.

**Accuracy**: ±2px due to anti-aliasing. Works best on high-contrast borders.

**Method**:
- Harris corner detection on edge image
- Cluster corners by proximity to rectangular shapes
- Fit circles to corner point groups
- Extract radius from circle fit
- Snap to common values (4, 8, 12, 16, 24, 9999)

**Output**: `[{element_id, bbox, radius_px, snapped_radius, fit_quality, confidence}]`

**Handles well**: Buttons, cards, inputs with clear borders.
**Struggles with**: Subtle rounded corners, <4px radius, full-circle (`border-radius: 50%`), anti-aliased edges.

---

## gradient_fit.py <a name="gradient"></a>

Linear and radial gradient fitting via directional variance analysis.

**Accuracy**: 2-stop linear gradients within ±5° angle and ±3% stop positions. Radial and multi-stop gradients less reliable.

**Method**:
- Detect regions with directional color change
- Sample color along candidate axis directions
- Fit linear model: determine angle + 2-stop colors
- Fit radial model: determine center + radius + stops
- Compare fit quality to classify type

**Output**: `[{region_bbox, type, angle, center, stops, fit_r_squared, confidence}]`

**Handles well**: Simple 2-stop linear gradients.
**Struggles with**: Multi-stop gradients (>3 stops), conic gradients, image-based backgrounds that look like gradients. Confidence < 0.5 usually means it's an image, not a CSS gradient.

---

## visual_diff.py <a name="diff"></a>

Rendered spec vs original screenshot comparison using SSIM.

**Accuracy**: SSIM > 0.90 = good match, 0.80–0.90 = acceptable, <0.80 = significant differences.

**Method**:
- Load both images, resize to match dimensions
- Compute structural similarity index (SSIM) per channel
- Generate diff heatmap highlighting divergent regions
- Classify diff regions by magnitude

**Output**: `{ssim_score, diff_regions: [{bbox, magnitude, suggested_check}], notes}`

**Optional dependency**: `scikit-image` for SSIM. Falls back to simpler MSE comparison if unavailable.

**Requires**: A rendered version of the extracted spec (via Playwright/Puppeteer) to compare against the original screenshot.

---

## Video Tools <a name="video"></a>

See `references/video-pipeline.md` for detailed video tool documentation.

| Tool | Purpose | Key dependency |
|------|---------|---------------|
| `scripts/video/ingest.py` | FFprobe metadata + frame extraction | `ffmpeg` |
| `scripts/video/segment_detect.py` | Frame-diff energy + motion window detection | — |
| `scripts/video/track_element.py` | Template matching + optical flow tracking | — |
| `scripts/video/easing_fit.py` | Cubic-bezier + spring parameter fitting | `scipy` |
| `scripts/video/flow_analysis.py` | Dense optical flow + parallax detection | — |
