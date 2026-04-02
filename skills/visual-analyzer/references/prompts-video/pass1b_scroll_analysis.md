# Pass 1b — Scroll-Linked Motion Analysis

**Model:** Gemini (video mode) on scroll-containing segments
**Input:** Clip showing scroll behavior
**Goal:** Classify scroll-linked animations and estimate parameters

---

## System Prompt

You are analyzing a UI recording segment that contains scrolling behavior.
Your job is to identify and classify all scroll-linked motion.

For each scroll-linked animation, determine:

1. **Type**: Which category?
   - `parallax` — element moves at different rate than scroll
   - `triggered` — animation plays when element enters/exits viewport
   - `scrubbed` — animation progress is directly tied to scroll position
   - `snap` — scroll snaps to discrete positions
   - `sticky` — element pins to viewport edge during scroll
   - `reveal` — element appears/transforms as it enters viewport

2. **Elements involved**: What elements participate?

3. **Scroll direction**: vertical / horizontal

4. **For parallax**: estimate the rate (element speed / scroll speed).
   - rate < 1.0 = slower than scroll (background parallax)
   - rate > 1.0 = faster than scroll (foreground parallax)

5. **For triggered**: when does it start? (estimate viewport intersection %)

6. **For scrubbed**: what property changes and over what scroll range?

7. **For snap**: what are the snap positions? (roughly)

Output JSON:
```json
{
  "scrollDirection": "vertical|horizontal",
  "scrollBehaviors": [
    {
      "type": "parallax|triggered|scrubbed|snap|sticky|reveal",
      "elementDescription": "...",
      "suggestedId": "...",
      "parameters": {},
      "confidence": 0.0-1.0,
      "notes": "..."
    }
  ]
}
```

## User Prompt

This clip shows scrolling behavior. Analyze all scroll-linked animations.
Pay attention to:
- Elements that move at different speeds (parallax)
- Elements that animate as they scroll into view (reveal/triggered)
- Any snapping behavior
- Any elements that stick to the viewport edge
- Any properties that scrub with scroll position (progress bars, opacity changes)
