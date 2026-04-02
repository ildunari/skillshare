# Static Pipeline — Detailed Reference

## Table of Contents

1. [End-to-End Walkthrough](#walkthrough)
2. [Platform Detection Heuristics](#platform-detection)
3. [Confidence Convergence Loop](#convergence-loop)
4. [MCP Integration](#mcp-integration)
5. [Claude Code / Codex Usage](#claude-code)
6. [Figma Integration](#figma)

---

## End-to-End Walkthrough <a name="walkthrough"></a>

### Step 1: Platform Detection + Inventory

Feed the screenshot to a vision model with `references/prompts-static/pass0_inventory.md`. The model should:
- Detect platform (iOS / Android / Web / design tool / unknown) with confidence
- List all visible UI elements with normalized bboxes (0–1 range)
- Classify visual hierarchy (primary, secondary, tertiary)
- Note repeated patterns (lists, grids, card groups)

Force structured JSON output. Require `"unknown"` for uncertain values instead of hallucinated guesses.

### Step 2: Run Computational Tools

Run all tools in parallel — they're independent:

```bash
python scripts/static/palette_extract.py screenshot.png > palette.json
python scripts/static/ocr_extract.py screenshot.png > text.json
python scripts/static/segment_ui.py screenshot.png > segments.json
python scripts/static/grid_detect.py screenshot.png > grid.json
python scripts/static/corner_detect.py screenshot.png > corners.json
python scripts/static/gradient_fit.py screenshot.png > gradients.json
```

### Step 3: Token Extraction

Feed inventory + all tool outputs to `references/prompts-static/pass1_tokens.md`. The model should:
- Map measured colors to semantic roles (surface, text, brand, etc.)
- Assign spacing values to a consistent scale
- Use OCR-detected sizes for typography tokens
- Use tool-measured corners for radius tokens
- Flag anything without computational backing as low confidence

### Step 4: Component Detection

Feed tokens + inventory to `references/prompts-static/pass2_components.md`. Group elements into components:
- Button = text + background + border + radius
- TextField = label + input area + border + placeholder text
- Card = container + content + shadow
- NavBar = container + icons + text labels

Each component gets `tokenRefs` pointing to tokens from step 3, plus `raw` fallback values for properties that don't map to tokens.

### Step 5: Layout Analysis

`references/prompts-static/pass3_layout.md` builds:
- Hierarchy tree (root → sections → containers → elements)
- Grid parameters (column count, gutters, margins)
- Spacing constraints between siblings
- Alignment constraints (centered, edge-aligned)

### Step 6: Validation

`references/prompts-static/pass4_validation.md` cross-checks everything:
- Token consistency (near-duplicate colors, on-grid spacing)
- Component sanity (token refs resolve, bbox valid)
- Layout completeness (all components in hierarchy)
- Confidence scoring (per-token and overall)

Output includes `"decision": "finalize" | "iterate" | "human_review"` with reasoning.

### Step 7: Output + Transforms

Final JSON matches `references/schemas/design-spec.schema.json`. To generate platform code:

```bash
python scripts/dtcg_to_sd.py output.json --output tokens/ --expand-composites --split
node scripts/sd_build.mjs
# → dist/css/tokens.css, dist/tailwind/tokens.cjs, dist/swift/Tokens.swift, etc.
```

---

## Platform Detection <a name="platform-detection"></a>

| Platform | Visual Cues | Default Font | Spacing Grid | Unit |
|----------|-------------|-------------|--------------|------|
| iOS | Status bar (time + signal/wifi/battery), home indicator, SF Symbols | SF Pro Display/Text | 8pt | pt |
| Android | Material nav bar (back/home/recents), status bar icons, Material You shapes | Roboto | 4dp/8dp | dp |
| Web | Browser chrome, scrollbars, cursor styles, custom fonts | system-ui | varies | px |
| Figma/Design | Artboard borders, frame names, grid overlays | varies | varies | px |

**Retina handling**: iOS @2x/@3x screenshots have physical pixels = pt × devicePixelRatio. Divide measured pixel distances by DPR to get design units.

**Android density**: Common densities are mdpi (1x), hdpi (1.5x), xhdpi (2x), xxhdpi (3x). Divide physical pixels by density factor to get dp.

---

## Confidence Convergence Loop <a name="convergence-loop"></a>

```python
spec = run_pass0(screenshot)
tool_outputs = run_all_tools(screenshot)  # parallel
spec = run_pass1(spec, tool_outputs)      # tokens
spec = run_pass2(spec)                    # components
spec = run_pass3(spec)                    # layout

for iteration in range(max_iterations):
    validation = run_pass4(spec, tool_outputs)

    if validation["decision"] == "finalize":
        break
    elif validation["decision"] == "human_review":
        spec["openQuestions"] = validation["open_questions"]
        break
    else:  # iterate
        low_items = [c for c in validation["checks"] if c["score"] < 0.65]
        for item in low_items:
            action = lookup_failure_action(item, config)
            if action["type"] == "run_tool":
                tool_result = run_tool(action["tool"], screenshot, item["context"])
                spec = update_spec(spec, tool_result)
            elif action["type"] == "re_crop":
                crop = crop_region(screenshot, item["bbox"])
                crop_result = run_vision_pass(crop, item["question"])
                spec = update_spec(spec, crop_result)
            elif action["type"] == "request_ground_truth":
                spec["openQuestions"].append(action["description"])

    if validation["overallScore"] - prev_score < 0.02:
        break  # Not improving, stop
    prev_score = validation["overallScore"]
```

---

## MCP Integration <a name="mcp-integration"></a>

Claude Code, Codex CLI, and claude.ai all have native vision — no MCP needed for image input. MCP adds ground-truth sources:

**Figma MCP** (`figma_mcp_server`):
- `get_variable_defs` → Ground truth design tokens (confidence 0.95+)
- `get_screenshot` → Specific component screenshots
- `get_metadata` → Component names, constraints, auto-layout info

**Chrome DevTools MCP**:
- `get_computed_styles` → Ground truth CSS for web screenshots
- `get_dom_tree` → Component hierarchy

**Tool I/O pattern** for MCP wrappers:
```json
{
  "input": {
    "oneOf": [
      {"type": "object", "properties": {"path": {"type": "string"}}},
      {"type": "object", "properties": {"url": {"type": "string"}}},
      {"type": "object", "properties": {"data": {"type": "string"}, "mimeType": {"type": "string"}}}
    ]
  }
}
```

For payloads >100KB: write to file, return `resource_link` instead of inline content.

---

## Claude Code / Codex Usage <a name="claude-code"></a>

No plugin manifest or MCP server needed — the skill's scripts are just Python CLI tools.

```bash
# Claude Code has native vision — just reference the image
claude "Extract design tokens from this screenshot: ./screenshot.png"

# Multi-step pipeline
claude "Run palette_extract.py on screenshot.png, then use the results to build DTCG tokens"
```

Multi-step orchestration: Claude Code runs computational tools as subprocess calls, collects JSON outputs, uses its own vision to run the prompt passes, outputs final spec.

---

## Figma Integration <a name="figma"></a>

When Figma access is available (via Figma MCP or exported file):

1. Use Figma as ground truth for tokens → confidence 0.95+
2. Screenshot as validation — compare Figma values with screenshot measurements
3. Export workflow: Figma variables → DTCG JSON → Style Dictionary build

This inverts the pipeline: instead of extracting from screenshots, you validate existing tokens against visual output.
