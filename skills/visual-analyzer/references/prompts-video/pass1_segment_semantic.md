# Pass 1 — Segment Semantic Analysis (Per Clip)

**Model:** Gemini (video mode, higher FPS if available) or frame sequence to any vision model
**Input:** Clipped video segment (2-10 seconds), plus inventory context from Pass 0
**Goal:** Detailed semantic decomposition of what animates, with element IDs and property hypotheses

---

## System Prompt

You are analyzing a short clip of a UI animation. This clip was identified during
an inventory pass as containing motion at approximately {timestamp}.

Context from inventory:
- Category: {category}
- Description: {description}
- Platform: {platform}

Your job is to decompose this clip into individual animation tracks.

For EACH element that animates, output:
```json
{
  "elementDescription": "human-readable description",
  "suggestedId": "ComponentName.Part",
  "properties": [
    {
      "property": "opacity|transform.translateX|transform.translateY|transform.scale|transform.rotate|filter.blur|backgroundColor|borderRadius|shadow.elevation|width|height|clipPath",
      "fromDescription": "describe starting state",
      "toDescription": "describe ending state",
      "fromEstimate": "rough value if visible (e.g., '0', '~20px left')",
      "toEstimate": "rough value if visible",
      "confidence": 0.0-1.0
    }
  ],
  "approximateDurationMs": null,
  "qualitativeEasing": "linear|ease-out|ease-in|ease-in-out|spring-no-overshoot|spring-mild-overshoot|spring-bouncy|steps|unknown",
  "hasOvershoot": true/false,
  "triggerType": "click|hover|scroll|load|route|gesture|toggle|unknown",
  "triggerElement": "what was interacted with (if visible)",
  "startsAt": "relative to clip start, e.g., 'immediately' or '~200ms after clip start'",
  "relationship": "first|concurrent_with:elementId|follows:elementId|stagger_member"
}
```

Rules:
- If you see overshoot (element goes past its target then settles), mark hasOvershoot: true.
- If multiple elements animate together, describe their relationship (parallel, sequence, stagger).
- Do NOT invent exact pixel values or ms durations — mark as approximate or null.
- If you can't determine a property's start/end value, say "unknown" with confidence 0.
- Pay special attention to: opacity changes, position shifts, scale changes, color transitions.

## User Prompt

Analyze this {duration}s clip. The inventory pass identified this as:
"{inventoryDescription}"

Decompose every animated element and property. Be especially careful to:
1. Separate concurrent animations into distinct tracks
2. Note any stagger patterns (same animation on multiple items with offset)
3. Identify the trigger (what user action or event causes this)
4. Note if any element overshoots its final position (spring behavior)

## Expected Output

```json
{
  "clipAnalysis": {
    "segmentStartSec": 6.35,
    "segmentEndSec": 6.95,
    "triggerType": "click",
    "triggerElement": "Tab 2 in tab bar",
    "animationCount": 3,
    "isOrchestrated": true,
    "orchestrationType": "parallel"
  },
  "tracks": [
    {
      "elementDescription": "Tab bar active indicator (underline)",
      "suggestedId": "TabBar.Indicator",
      "properties": [
        {
          "property": "transform.translateX",
          "fromDescription": "aligned under Tab 1",
          "toDescription": "aligned under Tab 2",
          "fromEstimate": "0px",
          "toEstimate": "~96px",
          "confidence": 0.85
        }
      ],
      "qualitativeEasing": "spring-mild-overshoot",
      "hasOvershoot": true,
      "triggerType": "click",
      "startsAt": "immediately",
      "relationship": "concurrent_with:TabContent.exit"
    }
  ]
}
```

## Post-Processing

1. Assign stable IDs to elements (merge with static component inventory if available).
2. Feed each track to the computational measurement pipeline for exact values.
3. Use relationships to build orchestration groups.
