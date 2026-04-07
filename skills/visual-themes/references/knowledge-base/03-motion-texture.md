
## 3. Motion, texture & materiality

### 3.1 Motion as a design system dimension

Apple, Material, IBM Carbon, and Salesforce all converge on the same core idea: motion should communicate relationships, outcomes, and affordances — not just decorate. A visual theme's motion philosophy defines the physics of the digital world the user inhabits.

**The key distinction is between meaningful and decorative motion.** Meaningful animation reduces cognitive load and clarifies spatial relationships through:

- **Orientation and continuity:** Motion answers "where did this come from, where did it go?" via object constancy — elements persist and morph rather than disappearing and reappearing.
- **Feedback and status:** The interface reacts instantly to input (low latency) and animation is interruptible — if the user changes their mind mid-gesture, the interface redirects from current position rather than snapping to start/end.
- **Attention guidance:** Choreographed staggered sequences guide reading order rather than overwhelming with simultaneous movement.

**References:**
- Apple HIG Motion: https://developer.apple.com/design/human-interface-guidelines/motion
- Material 3 motion: https://m3.material.io/styles/motion/overview/how-it-works
- Material easing & duration: https://m3.material.io/styles/motion/easing-and-duration

### 3.2 A practical framework for motion philosophy

Define your theme's motion in five parts:

1. **Intent classes:** Feedback (hover/press), Transition (view changes), Attention (toasts/alerts), Ambient (background).
2. **Timing ranges:** Fast feedback (80–150ms) vs slower transitions (200–500ms).
3. **Easing family:** Mechanical (sharp cubic-bezier), Physical (springs), Organic (overshoot, asymmetry), Stepped (retro/pixel).
4. **Choreography rules:** What leads vs follows; stagger timing; spatial continuity rules.
5. **Accessibility rules:** Reduced motion strategy; `prefers-reduced-motion` handling; no vestibular-triggering effects.

A good motion system yields coherence the same way a color system does: repeated constraints.

### 3.3 Motion identity frameworks from major design systems

| System | Core Philosophy | Characteristics |
|--------|----------------|-----------------|
| **Material Design 3** | Expressive vs Standard | Expressive: hero moments, expansive, dramatic curves. Standard: micro-interactions, efficient, productivity-focused. |
| **IBM Carbon** | Productive vs Expressive | Productive: grid-adherent, invisible/functional. Expressive: breathing room, rhythmic breaks for significant moments. |
| **Salesforce Kinetics** | Personality Attributes | Motion defined via traits ("Nimble," "Sensible," "Charismatic") for brand consistency. |
| **Apple HIG** | Fluidity & Physics | Liquid Glass behaviors — continuous, inertia-responsive, spring/friction-grounded. |

### 3.4 Easing, springs, and physics: how they feel different

- **Standard easing (cubic-bezier):** Feels designed and controlled. Deterministic and time-based. Best for opacity fades, color changes, or continuous loops where physics is irrelevant.
- **Spring physics:** Defined by mass, stiffness, and damping — non-deterministic regarding time (duration is calculated from physics). Creates natural overshoot and settling. A stiff spring feels snappy; a loose spring feels heavy and lazy. Makes interfaces feel alive and tactile. Historically required JS (React Spring, Framer Motion).
- **Stepped motion:** Feels retro or mechanical. Useful for terminal/pixel aesthetics.

### 3.5 The `linear()` revolution

The CSS `linear()` easing function (supported in major browsers since late 2023) allows complex spring-like, bounce, and elastic effects without JavaScript overhead. Instead of `ease-out`, you can define `linear(0, 0.9, 1.1, 0.95, 1)` — a curve that bounces past the target and settles. This bridges CSS performance with JS physics aesthetics.

**References:**
- CSS Easing Functions Level 2: https://drafts.csswg.org/css-easing/
- MDN on linear(): https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/linear
- Josh Comeau (2025), springs with linear(): https://www.joshwcomeau.com/animation/linear-timing-function/

### 3.6 Interruptible animation

A hallmark of high-quality "fluid" interfaces (like iOS) is interruptibility. If a user triggers an animation and changes their mind mid-motion, the element should maintain current velocity and redirect toward the new target — not snap to start or end. This is difficult with standard CSS transitions but is a core feature of Framer Motion and React Spring, and increasingly expected in app-like web experiences.

**The FLIP technique** (First, Last, Invert, Play) enables morphing layouts (card expanding to full page) by calculating start/end positions and using `transform` to animate between them, avoiding expensive layout recalculations. Framer Motion handles this automatically via the `layout` prop.

### 3.7 Motion accessibility

Even if your compliance target is WCAG AA, motion can be a major usability issue. Define a reduced-motion mode as a **first-class theme mode**, not an afterthought:

- Replace complex physics with simple opacity fades or instant transitions
- Disable all ambient/background animation
- Keep functional feedback animations (button press confirmation) but simplify them

**References:**
- WCAG SC 2.3.3 (Animation from Interactions): https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- W3C technique for reduced motion: https://www.w3.org/WAI/WCAG21/Techniques/css/C39

### 3.8 Texture and materiality in the browser

"Materiality" is the feeling that surfaces have physical properties. In browsers you create this with:

| Technique | Implementation | Performance |
|-----------|---------------|-------------|
| Raster textures (noise, grain) | Tiny repeating background images | Cheap, reliable |
| SVG filters (`feTurbulence`) | Procedural noise without image assets | Expressive; CPU-heavy if animated |
| CSS effects (shadows, gradients, blend modes) | `backdrop-filter`, `mix-blend-mode` | Varies; blur is expensive |
| Canvas (procedural noise, particles) | 2D rendering context | Flexible; heavy if full-screen at 60fps |
| WebGL/WebGPU shaders (grain, caustics, reaction-diffusion) | Fragment shaders | Very powerful; requires performance discipline |

#### Glass / blur surfaces

Glassmorphism relies on `backdrop-filter: blur()` with translucency. It evolved in 2025 into "Liquid Glass" (Apple's term) — high refraction, specular highlights, and edge distortions that mimic thick curved glass rather than simple frosted panels. The advanced version uses SVG `<feDisplacementMap>` or WebGL for refraction effects, plus multiple box-shadows with `mix-blend-mode: overlay` for specular highlights.

**Rule of thumb:** Treat real-time blur as a premium, constrained effect — keep blurred layers small, avoid large animated backdrops, and ensure text contrast via overlays and/or fallback solid surfaces.

**References:**
- MDN backdrop-filter: https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter
- web.dev performance caution: https://web.dev/articles/backdrop-filter

#### Noise and grain

Grain breaks "flat vector perfection," adds depth cues, and reduces banding in gradients. Production techniques use SVG `<feTurbulence>` for procedural noise or CSS "grainy gradients" patterns. Static overlays are performant; animated noise is CPU-heavy and should be used sparingly.

**References:**
- CSS grainy gradients: https://css-tricks.com/grainy-gradients/
- SVG turbulence (Codrops): https://tympanus.net/codrops/2019/02/19/svg-filter-effects-creating-texture-with-feturbulence/

#### Holographic / iridescent surfaces

A rising 2025 trend for premium/futuristic feel. Stack multiple gradients (linear, radial, conic) with `mix-blend-mode` (color-dodge, overlay) and animate `background-position` for a shimmering oil-slick effect. OKLCH is essential here — it prevents the "muddy" transitions that kill iridescent effects in HSL.

#### The neumorphism/claymorphism arc

**Neumorphism (Soft UI):** Elements extrude from same-color background using soft shadows. Largely failed as a primary style due to severe contrast issues. Persists only in subtle hybrid micro-elements.

**Claymorphism:** A 2024–2025 evolution — inflated 3D shapes with vibrant colors and strong inner shadows. Unlike neumorphism, elements float above the background (drop shadows), maintaining better accessibility and hierarchy. Popular in Web3 and Gen Z-targeted branding.

### 3.9 Emerging web motion capabilities

Two platform shifts that affect theme design:

- **View Transition API:** Animated transitions between DOM states and between documents. Moves "polished page transitions" into the browser natively.
  MDN: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API

- **CSS scroll-driven animations (`animation-timeline`):** Scroll-linked timelines without JS libraries. Animations run on the compositor thread (no jitter even if main thread is busy). Replaces JS scroll listeners for parallax, reveal, and morphing effects.
  MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations

