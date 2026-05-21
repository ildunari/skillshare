# d3-viz Feedback Log

Read this file every time the d3-viz skill is loaded. Entries are lessons learned from real usage.

## Format
`[CATEGORY] YYYY-MM-DD: description`

Categories: CDN, RENDERING, INTERACTION, LAYOUT, DATA, PERFORMANCE, ACCESSIBILITY, INTEGRATION

---

[CDN] 2025-02-18: CRITICAL — d3js.org is CSP-blocked in Claude artifact sandboxes. Always use `https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js` or `https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js`. Never use `https://d3js.org/d3.v7.min.js`. This causes silent failure with "d3 is not defined" error. The SKILL.md example previously used the blocked URL and was corrected.

[LAYOUT] 2025-02-18: Chord diagram — tick number labels (0, 200, 400) overlapped with institute name labels because both text systems were placed at nearly the same radial offset (~outerRadius + 8-14px). Fix: separate into distinct radial lanes (ticks at +6px, names at +34px) and gate tick rendering by minimum arc span (0.3 rad for tick marks, 0.5 rad for tick text). See Principle 3 and 4 in SKILL.md best practices.

[LAYOUT] 2025-02-18: Sunburst — breadcrumb text overlapped the top of the chart because breadcrumb used `position: absolute; top: 90px` while the SVG radius was computed from viewport width without subtracting header/breadcrumb height. The SVG centered itself in the flex container which extended under the absolute element. Fix: use flow layout for all chart chrome, compute SVG size from remaining space via getBoundingClientRect(). See Principle 1 and 2 in SKILL.md best practices.

[LAYOUT] 2025-02-18: General — LLMs consistently produce label overlaps because they compute positions mathematically without rendering feedback. All label placement must include: (1) space reservation before chart sizing, (2) flow layout for chrome, (3) separate spatial lanes for different label types, (4) arc/size gating, (5) post-render collision checks when density is high. Added comprehensive label collision section to both SKILL.md and d3-patterns.md.
