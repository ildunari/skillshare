# Video Motion Extraction Module — GUIDE

> **Purpose:** Extract implementable motion tokens (timing, easing, choreography,
> triggers, scroll behaviors) from UI screen recordings. Outputs machine-readable
> specs that coding agents can implement in CSS/GSAP/Framer Motion/SwiftUI/Compose.

> **Core principle:** Gemini = semantic director (what/when/why).
> CV scripts = measurement layer (how much/how fast/what curve).
> Instrumentation = ground truth (use when available, fall back to video).

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    INPUT                             │
│  Video file / URL / GIF / Figma recording            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  INGEST (scripts/video/ingest.py)                          │
│  • FFprobe metadata • CFR normalize • Proxy gen      │
└──────────────────────┬───────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌─────────────────┐    ┌───────────────────────────┐
│ PASS 0: INVENTORY│    │ SEGMENT DETECT             │
│ Gemini on proxy  │    │ (scripts/video/segment_detect.py)│
│ references/prompts-video/pass0_inventory    │    │ Frame diff + energy windows│
└────────┬────────┘    └─────────────┬─────────────┘
         │                           │
         └─────────┬─────────────────┘
                   ▼
         ┌─────────────────┐
         │ MERGE: inventory │
         │ + computed segs  │
         │ = work queue     │
         └────────┬────────┘
                  │
          ┌───────┴──────────────────────┐
          │  FOR EACH SEGMENT:            │
          │                               │
          │  ┌─────────────────────────┐  │
          │  │ PASS 1: SEMANTIC        │  │
          │  │ Gemini on clipped video │  │
          │  │ references/prompts-video/pass1_segment_semantic           │  │
          │  └───────────┬─────────────┘  │
          │              │                │
          │              ▼                │
          │  ┌─────────────────────────┐  │
          │  │ COMPUTE: MEASURE        │  │
          │  │ track_element.py        │  │
          │  │ + easing_fit.py         │  │
          │  └───────────┬─────────────┘  │
          │              │                │
          │              ▼                │
          │  ┌─────────────────────────┐  │
          │  │ VALIDATE                │  │
          │  │ scripts/validate_motion.py           │  │
          │  │ + confidence_config     │  │
          │  └───────────┬─────────────┘  │
          │              │                │
          │         pass?─┤── fail ──→ RE-MEASURE    │
          │              │         (higher FPS /     │
          │              │          different method) │
          │              ▼                │
          │  ┌─────────────────────────┐  │
          │  │ PASS 2: IMPLEMENTATION  │  │
          │  │ Map to frameworks       │  │
          │  │ references/prompts-video/pass2_implementation_map           │  │
          │  └─────────────────────────┘  │
          └───────────────────────────────┘
                         │
                         ▼
         ┌──────────────────────────────┐
         │ ASSEMBLE: MotionSpec JSON     │
         │ + merge with static tokens    │
         │ + final validation            │
         └──────────────────────────────┘
```

---

## File Locations (within visual-analyzer skill)

```
scripts/video/
├── ingest.py                         # Video download, normalize, proxy
├── segment_detect.py                 # Motion boundary detection
├── track_element.py                  # Element tracking (template + LK flow)
├── easing_fit.py                     # Bezier/spring curve fitting
└── flow_analysis.py                  # Dense optical flow + parallax

references/prompts-video/
├── pass0_inventory.md                # Full video → motion inventory
├── pass1_segment_semantic.md         # Per-clip → element decomposition
├── pass1b_scroll_analysis.md         # Scroll-specific analysis
└── pass2_implementation_map.md       # Measured data → framework mapping

references/schemas/
├── motion_tokens.ts                  # TypeScript schema (source of truth)
└── example_motion_spec.json          # Realistic example output

scripts/validate_motion.py            # Timing/easing/orchestration checks
assets/config/motion_confidence.json  # Canonical thresholds
```

---

## Motion Taxonomy (10 Categories)

Every detected motion is classified into one of these:

| Category | Examples | Typical Duration |
|---|---|---|
| **entrance_exit** | Fade in, slide up, scale from 0, blur reveal, mask wipe | 150–400ms |
| **state_transition** | Color change, size change, elevation shift, radius morph | 100–300ms |
| **navigation** | Route push/pop, shared element, hero transition | 200–500ms |
| **scroll_linked** | Parallax, reveal-on-scroll, scrub, snap, sticky | Scroll-driven |
| **micro_interaction** | Button press, hover, toggle, ripple, focus ring, shake | 50–200ms |
| **loading_progress** | Spinner, skeleton shimmer, progress bar | 500ms–3s (looping) |
| **gesture_physics** | Drag, swipe, inertia, spring settle, bounce, overscroll | Physics-driven |
| **ambient** | Background gradient, particles, subtle loop | Continuous |
| **text_number** | Count-up, typewriter, character morph | 200ms–2s |
| **media** | Image crossfade, blur-up, poster transition | 200–600ms |

---

## Property → Extraction Method

| Property | Best Method | Fallback | Expected Precision |
|---|---|---|---|
| Start/end timestamps | Frame diff energy threshold | Gemini timestamp | ±1 frame at 60fps |
| Duration (ms) | Frame count × (1/FPS) | Gemini estimate | Exact if CFR |
| Delay (ms) | Idle→motion onset detection | Gemini | ±2 frames |
| Position trajectory | Template matching or point tracking | Optical flow | High if track stable |
| Scale trajectory | Bbox corner tracking | Feature spread measurement | Medium-High |
| Opacity | Mean luminance in element region | Gemini label | Medium (compression) |
| Color change | Region pixel sampling over time | Gemini label | Medium |
| Blur/shadow | Edge energy metric | Gemini qualitative | Low-Medium |
| Stagger offsets | Multi-track onset comparison | Gemini | ±2 frames |
| Easing (bezier) | Curve fit on progress vs time | Snap to nearest preset | High with ≥8 samples |
| Spring params | Damped oscillator fit | Bucket classify | Medium-High |
| Scroll linkage | Property vs scroll-offset regression | Velocity cues | Medium |
| Trigger type | Gemini semantic analysis | Temporal heuristics | Medium-High |

---

## Gemini Operational Notes

**Sampling:** Default File API = ~1 FPS. Enough for inventory, NOT enough for easing.
Use custom FPS on clipped segments when detail is needed.

**Token cost:** ~300 tokens/sec at default resolution, ~100 at low res.

**Context caching:** Use explicit caching (TTL-based) when running multiple passes
on the same video — reuse system prompt + video across clip queries.

**Length:** ~1hr at default res, ~3hr at low res within 1M context window.

**What Gemini is good at:** Semantic labeling, trigger identification, element naming,
qualitative easing ("springy", "ease-out"), approximate timestamps.

**What Gemini is bad at:** Exact ms timing, exact easing parameters, simultaneous
animation decomposition (unless forced with structured prompts).

---

## Easing Extraction: The Critical Path

### Step 1: Get a property time-series
Track an element's position/opacity/scale per frame in the animation segment.

### Step 2: Normalize to [0,1] × [0,1]
- Time: `t_norm = (frame - start) / (end - start)`
- Progress: `p_norm = (value - value_start) / (value_end - value_start)`

### Step 3: Classify
- Monotonic, no overshoot → candidate **cubic-bezier**
- Overshoot/oscillation → candidate **spring**
- Flat plateaus + sudden jumps → candidate **steps**
- Straight line → **linear**

### Step 4: Fit
- **Cubic-bezier:** Optimize (x1,y1,x2,y2) minimizing error vs observed progress.
  Snap to known presets if distance < 0.15.
- **Spring:** Fit damped oscillator (stiffness, damping, mass=1).
  Store platform-native mappings (iOS response/dampingFraction, Android dampingRatio).

### Step 5: Validate
- Check fit residual against thresholds in `confidence_config.json`.
- If residual too high: re-track at higher FPS, try alternative tracking method,
  or consider that this may be a multi-phase animation needing keyframes.

### Frame Rate Requirements
- 200-300ms animation at 60fps = 12-18 samples → sufficient for bezier fit
- 200-300ms at 30fps = 6-9 samples → marginal, prefer 60fps
- At 1fps (Gemini default) = 0-1 samples → **impossible**, must use CV

---

## Library Fingerprinting

Output as probability distribution, not single guess:

```json
"libraryGuess": {
  "swiftUI": 0.45,
  "framerMotion": 0.25,
  "compose": 0.15,
  "cssTransition": 0.10,
  "gsap": 0.05
}
```

### Heuristics

| Signal | Points toward |
|---|---|
| Spring overshoot + velocity continuity | SwiftUI / Framer Motion / React Spring |
| Easing matches Material presets (0.4,0,0.2,1) | Android Compose / Material Web |
| Complex scroll-pinning + timeline stagger | GSAP ScrollTrigger |
| Simple from→to, no overshoot, 150-300ms | CSS transitions |
| Perfect vector morphing, illustrated assets | Lottie / Rive |
| Consistent iOS navigation patterns | SwiftUI |

---

## Known Easing Presets (for snap-to matching)

### Material Design
- standard: `cubic-bezier(0.4, 0.0, 0.2, 1.0)`
- decelerate: `cubic-bezier(0.0, 0.0, 0.2, 1.0)`
- accelerate: `cubic-bezier(0.4, 0.0, 1.0, 1.0)`
- emphasized-decelerate: `cubic-bezier(0.05, 0.7, 0.1, 1.0)`

### CSS Named
- ease: `cubic-bezier(0.25, 0.1, 0.25, 1.0)`
- ease-in-out: `cubic-bezier(0.42, 0, 0.58, 1)`

### Apple (approximate)
- ios-default: `cubic-bezier(0.25, 0.46, 0.45, 0.94)`
- ios-spring-default: `spring(response: 0.55, dampingFraction: 0.825)`

---

## Convergence Loop (Pseudocode)

```python
config = load_confidence_config()

for token in work_queue:
    iteration = 0
    while iteration < config.stopConditions.maxIterations:

        # Measure
        tracking = track_element(video, token.bbox, token.segment)
        t_norm, progress = extract_timeseries(tracking)
        fit = fit_easing(t_norm, progress, token.durationSec)

        # Validate
        report = validate_token(token_with_fit)

        if report.passed and token.overallConfidence >= config.perToken.accept:
            break  # Accept

        if iteration > 0 and no_improvement(report, prev_report):
            break  # Stuck, accept best so far

        # Determine fix action
        action = config.failureActions[report.worst_issue]
        apply_fix(action)  # e.g., increase FPS, switch tracker, tighter crop

        iteration += 1
```

---

## Input Type Handling

| Input | Preprocessing | Notes |
|---|---|---|
| Local video file | Normalize to CFR | Preferred path |
| YouTube/Vimeo URL | Download via yt-dlp, then normalize | Check legal/policy |
| GIF | Treat as video, watch for low FPS / palette artifacts | Often 10-15fps |
| Figma prototype recording | Usually clean 60fps, ideal for tracking | Best non-instrumented source |
| Lottie/Rive preview | Detect asset type → switch to asset extraction if possible | Exact if you get the .json/.riv |
| Screen share recording | Often VFR, may have cursor/overlays | Normalize aggressively |

---

## Accessibility: Reduced Motion

Every motion token should include a `reducedMotion` strategy:

| Strategy | When to use |
|---|---|
| `remove` | Decorative animations (shimmer, ambient, micro-interactions) |
| `crossfade` | Navigation transitions, entrance/exit |
| `shorten` | Important functional feedback (button press) |
| `simplify` | Complex springs → simple ease-out |

Reference: `prefers-reduced-motion` media query (web),
`UIAccessibility.isReduceMotionEnabled` (iOS),
`Settings.Global.ANIMATOR_DURATION_SCALE` (Android).

---

## Merging with Static Design Spec

Motion tokens reference static tokens by name:
- `colorToken: "color.brand.primary"` → links to palette extraction
- `spacingToken: "space.4"` → links to spacing scale
- `targetId: "PrimaryButton"` → links to component inventory

When assembling the combined spec:
1. Validate all token refs resolve to static spec entries.
2. Validate `targetId` values match component inventory IDs.
3. Flag color transitions where `from` value doesn't match the resting palette.
4. Flag spacing values not on the extracted grid scale.

---

## Sources

### Gemini Video
- Video understanding docs: https://ai.google.dev/gemini-api/docs/video-understanding
- Context caching: https://ai.google.dev/gemini-api/docs/caching

### Computer Vision
- OpenCV optical flow: https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html
- RAFT deep flow: https://arxiv.org/abs/2003.12039
- TAPIR point tracking: https://arxiv.org/pdf/2306.08637.pdf
- CoTracker: https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/07890.pdf

### Motion Standards
- Material duration/easing: https://m1.material.io/motion/duration-easing.html
- CSS cubic-bezier spec: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/cubic-bezier
- Scroll-linked animations spec: https://www.w3.org/TR/scroll-animations-1/
- Cubic-bezier math: https://blog.maximeheckel.com/posts/cubic-bezier-from-math-to-motion/

### Spring Parameterizations
- React Spring configs: https://react-spring.dev/common/configs
- Android Compose easing: https://android.googlesource.com/platform/frameworks/support/+/7451a357/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/Easing.kt

### Research
- Waken (UI reverse engineering from video): https://www.research.autodesk.com/app/uploads/2023/03/waken-reverse-engineering-usage.pdf
- SeeAction (reverse engineering actions from screencasts): https://arxiv.org/html/2503.12873v1

### Tools
- FFmpeg: https://ffmpeg.org/ffmpeg-all.html
- PySceneDetect: https://github.com/Breakthrough/PySceneDetect
- Motion vector extraction: https://github.com/LukasBommes/mv-extractor
- Lottie web: https://github.com/airbnb/lottie-web
