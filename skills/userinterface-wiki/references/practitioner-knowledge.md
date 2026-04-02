# Practitioner Knowledge

> The community knowledge that doesn't live in docs. Failure triggers, ecosystem patterns, taste formation, and the gap between "technically correct" and "ships well." Sourced from GSAP forum threads, Motion GitHub issues, Codrops/Awwwards case studies, and production post-mortems.

---

## Where Community "Taste" Forms

The JavaScript animation ecosystem isn't organized around documentation — it's organized around **feedback loops**: impressive demos that circulate (and get copied), communities where production failures get debugged in public, and curators who spotlight work that feels *inevitable* rather than merely *correct*.

### Knowledge sources by signal quality

| Source | What it's good for | Signal quality |
|---|---|---|
| **GSAP forum** | Solved threads encode maintainer wisdom on what actually works | Very high — moderators are the library authors |
| **Motion GitHub Issues** | Real constraints of WAAPI adoption, browser quirks, feature detection failures | High — bug reports are unfiltered production reality |
| **Codrops** | Production breakdowns with tool/trade-off explanations | High — curated for creativity + craftsmanship |
| **Awwwards** | "What the industry rewards" — technology tags show tool signatures | Medium-high — showcase bias toward novelty |
| **CodePen** | Trend emergence — what people collectively iterate on | Medium — demo ≠ production, but reveals affordances |
| **Reddit / Twitter** | Community sentiment, workarounds, tool comparisons | Medium — noisy but captures real practitioner opinions |
| **Official docs** | API surface, basic usage | Necessary but often misses edge cases and failure modes |

### What makes animation "share-worthy" vs merely correct

The community's quality judgment tracks **choreography, intent, and continuity** — not "did you animate opacity and transform."

Good motion:
1. Clarifies state change (you know what happened)
2. Preserves context across transitions (this thing is the same thing)
3. Feels physically consistent (timing/easing family is coherent)
4. Respects performance and attention (doesn't fight the platform)

Bad motion:
- Default easing, uniform durations, fade+translate reveals everywhere
- Motion that fights the platform (scroll-jank, resize misalignment, layout snapping)
- No attention to interruption, velocity, or state

---

## The "Technically Correct but Forgettable" Trap

An AI coding agent will be "correct" far more often than it will be "good." The gap is exactly where practitioner knowledge lives:

### Default patterns to avoid (AI tells)
- Same `ease-in-out` everywhere (use `ease-out` or spring for arrivals — things should arrive fast and settle)
- Uniform 300ms duration on everything (vary by element size and importance)
- Every reveal is `opacity: 0, translateY(20px)` → `opacity: 1, translateY(0)` (vary the reveal — scale, clip-path, mask, stagger direction)
- Stagger follows DOM order (stagger from center, edges, or based on content importance)
- Reduced motion = `animation: none` (replace, don't remove)

### What separates "solid" from "impressive"
- **Solid:** Readable, restrained. Motion supports hierarchy. Reduced motion works. Selection/copy not broken.
- **Impressive:** Typography motion integrates with layout and interaction. Effects reuse a consistent motion language rather than one-off stunts. The interface feels designed for its purpose, not templated.

---

## Documented Production Failures

These are real failure reports from forums, issues, and post-mortems — not theoretical concerns.

### GSAP: CSS smooth-scrolling conflict
**Source:** GSAP forum moderator guidance
**Problem:** `scroll-behavior: smooth` creates a CSS transition on scroll position. ScrollTrigger also controls scroll-linked behavior. The two fight — sluggish scrolling, refresh weirdness.
**Lesson:** Remove `scroll-behavior: smooth` from pages using ScrollTrigger. Use GSAP ScrollTo for anchor navigation.

### GSAP: ScrollTrigger "auto refresh on resize" isn't enough
**Source:** 2024 production post-mortem
**Problem:** Multiple pinned ScrollTrigger sections interfere/overlap after window resize despite documentation saying refresh happens automatically.
**Lesson:** Test resize as a first-class concern. Use `invalidateOnRefresh: true`. Consider manual `ScrollTrigger.refresh()` after dynamic content changes. Don't promise "it handles resize" without verifying.

### GSAP: once: true + kill = scroll jump
**Source:** GSAP forum thread
**Problem:** User wants animation to run once. `once: true` leaves spacer on scroll-back. Killing the ScrollTrigger removes spacer but causes visible jump. "AI advised disabling ScrollTrigger" — which made it worse.
**Lesson:** ScrollTrigger adds spacer elements for pinning. Killing without compensation causes jumps. "Seamless kill" is complex. Often better to let the trigger stay alive but inactive.

### GSAP: `immediateRender` with ScrollTrigger
**Source:** GSAP forum recurring question
**Problem:** `gsap.from()` with ScrollTrigger flashes the "from" state before the trigger fires because `from()` sets starting state immediately by default.
**Lesson:** Use `immediateRender: false` on ScrollTrigger-driven `from()` tweens.

### Motion: ScrollTimeline opacity bug
**Source:** Motion GitHub issue, Feb 2026
**Problem:** Since Motion ~v12.30, native `ScrollTimeline` detection causes scroll-linked opacity animations to break — Safari never reaches full opacity, Firefox jumps immediately. Transforms work fine.
**Lesson:** `window.ScrollTimeline !== undefined` doesn't mean all properties work correctly. Test opacity specifically with scroll-linked animations.

### Motion: autoplay: false ignored with opacity
**Source:** Motion GitHub issue, May 2025
**Problem:** `animate()` with `autoplay: false` plays anyway when opacity is involved. Opting out of WAAPI (via `repeatDelay` hack) fixes it.
**Lesson:** WAAPI driver and JS driver have subtly different semantics. If sequencing breaks, check which driver is active.

### WAAPI: fill: forwards leaks animation objects
**Source:** Motion One discussion, community knowledge
**Problem:** After animation finishes with `fill: "forwards"`, the animation object stays alive holding styles. Multiple animations accumulate, causing style conflicts and memory pressure.
**Lesson:** Use `commitStyles()` → `cancel()` pattern instead of relying on `fill: "forwards"`.

### View Transitions: hover triggers break mouse events
**Source:** Chrome e-commerce case studies
**Problem:** Triggering a view transition on hover creates a new transition layer above the UI during the transition, which fires `mouseleave` on the original element.
**Lesson:** Don't trigger view transitions on hover. Use click/navigation triggers instead.

---

## Ecosystem Shifts an AI Agent Must Know

### GSAP is free now
Webflow acquired GSAP Oct 2024. April 30, 2025: "100% free to all users." Including formerly paid plugins. Any recommendation that avoids GSAP due to licensing is outdated.

### Motion is not React-only
Nov 2024: Framer Motion became independent as Motion (motion.dev). Now includes vanilla JS APIs. "React-only" heuristics are outdated.

### Scroll animation is three-way
No longer "GSAP or nothing." The landscape is:
1. CSS scroll-driven animations (best performance, limited browser support)
2. GSAP ScrollTrigger (best ecosystem, cross-browser, JS-based)
3. WAAPI + ScrollTimeline polyfill (middle ground)

Choose based on support requirements and complexity.

### CSS absorbed entry/exit
`@starting-style` + `transition-behavior: allow-discrete` (Baseline 2024) handle what used to require JS double-rAF hacks. CSS-first is now credible for dialog/popover/accordion entry.

### CSS absorbed accordion animation
`interpolate-size: allow-keywords` lets you transition to/from `auto` height. Many accordion patterns no longer need JS measurement.

### View transitions became cross-engine baseline
Same-document view transitions: Baseline Oct 2025 (Chrome, Safari, Firefox). Credible default for route/view transitions. Cross-document transitions remain experimental.

---

## How Production Teams Actually Mix Tools

From Codrops case studies and Awwwards breakdowns:

- **Lottie** for baked designer-authored animations
- **GSAP timelines** for page transition masking and sequenced reveals
- **Lenis** for smooth scroll (custom smooth scrolling layer)
- **Rapier** or similar for physics interactions (drag, throw)
- **CSS-native** for hover states, simple transitions, utility motion

The pattern: different motion problems → different optimal representations. Don't force one tool to handle everything.

---

## "Not in the List" Tools

### VFX-JS
Attaches WebGL shader effects to normal DOM elements (images, videos) without full Three.js scene setup. Good for glitch, distortion, and cinematic effects on existing content.

### Lenis
Smooth scroll library. Often paired with GSAP ScrollTrigger in production sites. Provides custom smooth scrolling that integrates with scroll-driven animation.

### Barba.js / Swup
Page transition managers. Handle the "between pages" lifecycle that GSAP/View Transitions animate. Still common in 2026 portfolio/agency sites, especially with Astro.

### Theatre.js
Visual timeline editor for animations. Lets designers/developers scrub and edit animation parameters visually, then export to runtime code.

---

## The Taste Test

Before shipping an animated interface, ask:

1. **Does every animation have a reason?** (state change, feedback, narrative, ornament — not "because I can")
2. **Is there a consistent timing language?** (easing family, duration scale, stagger rhythm)
3. **Does the reduced-motion version communicate the same information?**
4. **Would removing any animation make the interface worse?** (if no, remove it)
5. **Does the animation survive resize, interruption, and slow networks?**
6. **Would a designer look at this and think "someone made choices" rather than "defaults"?**
