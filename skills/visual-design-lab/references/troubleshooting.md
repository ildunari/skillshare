# Troubleshooting

## palette_extract returns too many/few colors

Adjust K-means range internally or re-run with a cropped region. For minimalist UIs, the tool over-segments similar grays. For complex dashboards, it may under-count accent colors. Crop to a specific region of interest for better per-component extraction.

## OCR can't detect small text

Text must be at least 10px high for Tesseract to detect reliably. Crop the region of interest and upscale 2× before passing to `ocr_extract.py`. If Tesseract isn't installed, the fallback contour method is less accurate — install Tesseract for production use.

## Grid detection finds wrong column count

The projection profile method works best with clear content boundaries. For complex layouts with full-bleed images or overlapping sections, the tool may miscount. Manually specify the grid in the vision prompt (pass 3) and use the tool output as validation rather than the source of truth.

## Corner radius is off by 2-3px

Expected behavior due to anti-aliasing. The tool reports a fitted value plus tolerance. Use the snapped value (nearest 4px/8px multiple). For sub-pixel precision, request Figma access or DevTools computed styles.

## Shadow parameters are wildly wrong

Shadow extraction from screenshots is inherently unreliable (confidence 0.35–0.55). The vision model estimates rough params but can't measure blur radius or spread accurately. If accurate shadows are critical:
- Request Figma MCP access for ground truth
- Use Chrome DevTools MCP to read `box-shadow` computed style
- Accept the low confidence and flag for manual review

## Gradient fitting returns low confidence

Confidence < 0.5 usually means the region is an image, not a CSS gradient. Check if the element has uniform directional color change (gradient) or complex patterns (image). The tool works well for 2-stop linear gradients but struggles with multi-stop or conic gradients.

## Font family detection is wrong

Font family can't be reliably detected from screenshots — this is a known limitation (confidence 0.40–0.60). The pipeline applies platform priors:
- iOS → SF Pro Display / SF Pro Text
- Android → Roboto
- Web → system-ui (flag as unknown)
- Figma → look for font metadata in the exported file

For accurate font family, use Figma MCP, DevTools MCP, or ask the user.

## Style Dictionary build fails

Common causes:
- **Wrong token format**: SD v4 expects DTCG (`$value`), not legacy (`value`). Run `dtcg_to_sd.py` first.
- **ESM import issue**: SD v4 uses ESM. Ensure your Node.js version supports `import` and your `package.json` has `"type": "module"`.
- **sd-transforms version mismatch**: Use `@tokens-studio/sd-transforms@^1` for SD v4. v2.x targets SD v5.
- **Empty token files**: If `dtcg_to_sd.py --split` produces empty files, the source spec may have tokens nested differently than expected. Check with `--output tokens/tokens.json` (no split) first.

## Validation says "iterate" but score isn't improving

The convergence check stops iteration if score doesn't improve by ≥ 0.02 between passes. If stuck:
- Check which specific checks are failing in the validation output
- The `suggestedActions` array has concrete next steps
- Some properties (shadows, gradients) have hard confidence ceilings — they won't improve without ground truth
- Consider switching to `human_review` and providing the open questions to the user

## Component type detection is ambiguous

The pipeline stores top-2 hypotheses with confidence in the `componentHypotheses` array. Common ambiguities:
- Image vs Container (both large rectangular elements)
- Button vs Link (both clickable, but different styling patterns)
- TextField vs Container (inputs without visible borders)

When ambiguous, check the component's children and token refs. Buttons usually have text children + background color. Containers have multiple children of different types.

## Video: easing_fit returns poor R² values

Common causes:
- **Noisy tracking data**: The element tracker may have jitter. Increase the smoothing window.
- **Non-standard easing**: Some animations use custom curves that don't fit cubic-bezier or spring models. The tool reports what it can fit; check the residual plot.
- **Too few frames**: Animations shorter than ~10 frames don't have enough data points for reliable fitting. Increase video frame rate or slow down the recording.

## Video: segment_detect misses transitions

The frame-diff energy method has a threshold that may be too high for subtle transitions (fades, color shifts). It works best for movement-based transitions. For fade/opacity transitions, the energy change is smaller and may fall below the detection threshold.
