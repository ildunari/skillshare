---
title: Animations
scope: pptx-master
version: 1.0
---

# Animations

pptx-master supports **subtle, professional build animations** to guide the viewer’s attention and to control narrative pacing.

This document defines:

1. The **animation design rules** (what to do / what not to do)
2. The **IR animation model** (what the generator emits)
3. The **OOXML mapping** (how `scripts/inject_animations.py` writes `p:timing`)
4. Smart defaults per archetype (so most slides animate well without hand-authoring)

---

## Animation design rules

### Principles

- **Purposeful:** animations should reveal structure or emphasize the story—not add “motion for motion’s sake”.
- **Fast and subtle:** typical duration **250–450 ms** per build.
- **One idea per click:** don’t dump 6 unrelated items at once; also don’t use 30 micro-builds.
- **Prefer fades and short wipes:** avoid bounces, spins, and long-duration effects.
- **Don’t animate everything:** headlines usually stay static; animate the *content that changes*.

### Defaults

| Effect | Use | Default duration |
|---|---|---|
| `fade` | general entrance | 320 ms |
| `wipe` (directional) | process steps / timelines | 360 ms |
| `zoom` | KPI tiles / hero metrics (sparingly) | 360 ms |
| `appear` | minimal decks (Paper / Mono) | 1 ms |

### Click model

- **Click to advance** is the default in professional decks.
- Only use “auto” builds (after previous) for supporting, non-critical micro details.

---

## IR animation model

The IR adds an optional `animations` block per slide:

```json
{
  "slide": {
    "id": "S03",
    "archetype": "A9_card_grid",
    "animations": {
      "preset": "auto",
      "defaults": { "effect": "fade", "duration_ms": 320, "stagger_ms": 60 },
      "steps": [
        { "targets": ["el:card:0"], "effect": "fade" },
        { "targets": ["el:card:1"], "effect": "fade" }
      ]
    }
  }
}
```

### Target selectors

`targets` can be any of:

- A renderer-stamped shape name (recommended): `name:"el:S03:card:0"`
- A direct shape id: `spid: 7`
- A fallback geometry selector (least preferred): `{bbox:{x,y,w,h}, text_contains:"Revenue"}`

The injection script will try selectors in this order:

1. `spid`
2. `name` / `name_regex`
3. `bbox` + `text_contains` matching (best-effort)

---

## Smart defaults per archetype

When `animations.preset = "auto"`, pptx-master generates a build sequence:

- **A8 Icon grid** → reveal cells in reading order (L→R, top→bottom), `fade`
- **A9 Card grid** → reveal cards in reading order, `fade`
- **A12 Timeline horizontal** → reveal nodes left→right, `wipe:right`
- **A13 Timeline vertical** → reveal nodes top→bottom, `fade`
- **A14 Process flow** → reveal steps left→right, `wipe:right`
- **A15 Cycle** → reveal nodes clockwise starting at top, `fade`
- **A23 Team** → reveal people in reading order, `fade`

Slides with heavy charts (A17/A18) default to **no per-series animation**; only callouts may build.

---

## OOXML mapping

### Where animations live

PowerPoint shape animations are stored on each slide in:

- `ppt/slides/slideN.xml` under `<p:timing> ... </p:timing>`

A minimal timing skeleton looks like:

```xml
<p:timing>
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
        <p:childTnLst>
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" restart="whenNotActive" fill="hold" nodeType="mainSeq">
              <p:stCondLst><p:cond evt="onBegin" delay="0"/></p:stCondLst>
              <p:childTnLst>
                <!-- one <p:par> per click/build step -->
              </p:childTnLst>
            </p:cTn>
            <!-- click advances to the next child -->
            <p:nextCondLst><p:cond evt="onClick" delay="0"/></p:nextCondLst>
          </p:seq>
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>
```

> Reference structures appear in multiple Open XML SDK / OOXML walkthroughs (e.g., Open XML SDK “Working with animation” and schema references like ooxml.info).  
> Practical note: PowerPoint is picky; stick to known-good structures.

### Entrance effects

pptx-master uses these OOXML behaviors:

- **Fade / Wipe:** `<p:animEffect transition="in" filter="fade|wipe(right)|wipe(left)|wipe(up)|wipe(down)">`
- **Zoom:** `<p:animScale>` (with required `attrNameLst` entries for PowerPoint compatibility)
- **Appear:** implemented as a **0–1 ms fade-in** so the shape starts hidden (because `transition="in"` implies hidden-at-start behavior).

#### Fade in (example)

```xml
<p:animEffect transition="in" filter="fade">
  <p:cBhvr>
    <p:cTn id="10" dur="320" fill="hold">
      <p:stCondLst><p:cond delay="0"/></p:stCondLst>
    </p:cTn>
    <p:tgtEl><p:spTgt spid="7"/></p:tgtEl>
  </p:cBhvr>
</p:animEffect>
```

#### Wipe right (example)

```xml
<p:animEffect transition="in" filter="wipe(right)">
  <p:cBhvr>
    <p:cTn id="11" dur="360" fill="hold">
      <p:stCondLst><p:cond delay="0"/></p:stCondLst>
    </p:cTn>
    <p:tgtEl><p:spTgt spid="8"/></p:tgtEl>
  </p:cBhvr>
</p:animEffect>
```

#### Zoom (scale) in (example)

Zoom is implemented as a parallel behavior inside the step’s `<p:par>`:

- a near-instant fade-in (dur=1) to get hidden-at-start semantics
- a scale from 0% → 100%

```xml
<p:animScale>
  <p:cBhvr>
    <p:cTn id="12" dur="360" fill="hold">
      <p:stCondLst><p:cond delay="0"/></p:stCondLst>
    </p:cTn>
    <p:tgtEl><p:spTgt spid="9"/></p:tgtEl>
    <p:attrNameLst>
      <p:attrName>ppt_x</p:attrName>
      <p:attrName>ppt_y</p:attrName>
    </p:attrNameLst>
  </p:cBhvr>
  <p:from><p:xfrm><p:off x="0" y="0"/><p:ext cx="0" cy="0"/></p:xfrm></p:from>
  <p:to><p:xfrm><p:off x="0" y="0"/><p:ext cx="100000" cy="100000"/></p:xfrm></p:to>
</p:animScale>
```

> The exact internal representation of scale can differ across authoring tools; PowerPoint generally requires `attrNameLst` entries for scale behaviors (see MS-OE376 notes).

---

## Implementation notes for `inject_animations.py`

- The script unpacks the PPTX, edits slide XML with `lxml`, then repacks with the skill’s `ooxml/scripts/pack.py` (including LibreOffice validation).
- If a slide already contains `<p:timing>`, the script merges by **adding a new main sequence** unless `--replace-existing` is provided.
- Shape targeting is best when the renderer stamps stable names (Phase 3 recommendation): `name="el:{slide_id}:{element_id}"`.

---

## References (technical)

- Open XML SDK — “Working with animation in presentations”: https://learn.microsoft.com/en-us/office/open-xml/presentation/working-with-animation-in-presentations
- OOXML timing / set / animate effect examples: https://ooxml.info/docs/pptx/animations/
- [MS-OE376] Office Implementation Information for OOXML — `animEffect` (filter list) and `animScale` constraints:  
  https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/

