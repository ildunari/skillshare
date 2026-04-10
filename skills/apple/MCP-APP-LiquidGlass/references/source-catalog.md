# Source catalog and extracted takeaways

This file condenses the linked inspiration into a working reference set for AI
agents building liquid-glass apps.

## 1) FreeFrontend collection: 16 CSS Liquid Glass Effects

Source:
- https://freefrontend.com/css-liquid-glass/

Why it matters:
- Good catalog of mainstream implementation styles in 2025–2026.
- Shows the split between lightweight CSS/SVG glass and heavier GSAP/WebGL demos.
- Useful for identifying what to borrow vs what to avoid in production apps.

Extracted patterns from the collection:
- **backdrop blur + SVG displacement** is the most common “real” web recipe.
- **Specular highlights** and **edge distortion** are what make liquid glass feel
  more convincing than ordinary glassmorphism.
- **GSAP draggable** appears in interactive toggle/menu demos when the visual goal
  is playful physics.
- **WebGL/React Three Fiber** shows up for shader-heavy hero pieces, not everyday UI.
- Several demos are strongest as **single hero surfaces** rather than whole-page
  design systems.

Named examples worth knowing:
- Liquid Glass Effect
- Liquid Toggle Switch
- Apple Liquid Glass Effect
- Liquid Glass Shader
- Slider Button with Liquid Glass Effect
- Liquid Glass Theme Switcher
- Liquid Glass Menu with GSAP
- Apple Liquid Glass UI (2025)
- CSS Liquid Glass Effect
- Liquid Glass Effect (WWDC25 Style)
- Liquid Glass with Scroll and Drag

How to use this collection:
- Borrow **structure**, **layering**, and **interaction patterns**.
- Do not blindly port every visual flourish into app UI.
- Use the collection to pick the right tier:
  - CSS/SVG for serious app surfaces
  - GSAP for playful one-off controls
  - WebGL only for showcase areas

## 2) LogRocket: How to create Liquid Glass effects with CSS and SVG

Source:
- https://blog.logrocket.com/how-create-liquid-glass-effects-css-and-svg/

Why it matters:
- Strong explanation of the actual optical ideas behind the trend.
- Most useful reference here for agents that need to build liquid-glass code,
  not just mimic a screenshot.

Key extracted ideas:
- Liquid Glass is “glassmorphism plus **refraction** and **reflection**.”
- Refraction on the web is simulated with **displacement maps** and
  `feDisplacementMap`.
- Reflection is approximated with **specular rim maps**, blur, and composition.
- The article recommends a layered architecture:
  1. base element
  2. filter layer
  3. content layer
  4. inline SVG `<defs>`
- Their example uses **React + TypeScript + Tailwind CSS + SVG filters**.
- The article explicitly warns that production UIs should restrict liquid glass
  to a **small number of floating UI elements**.

What to copy into production:
- A reusable surface component.
- Tight token control for blur, radius, shine, and distortion strength.
- Progressive enhancement and browser fallbacks.

## 3) Framer resources and marketplace

Sources:
- https://framer.university/blog/how-to-create-liquid-glass-in-framer
- https://framer.university/resources/liquid-glass-element-in-framer
- https://www.framer.com/marketplace/components/tags/liquid-glass/
- https://www.framer.com/marketplace/components/liquid-glass-button/

Why they matter:
- Good evidence for how designers are using the effect in practice.
- Helpful for translating “Framer vibe” into React code for real apps.

Extracted takeaways:
- Framer creators frequently use liquid glass as a **single draggable element**,
  full-bleed within a frame, or as an **absolute-positioned overlay** inside a
  button/panel.
- The common pattern is: create a normal frame, place content inside it, then pin
  a liquid-glass layer behind or around the content.
- Marketplace descriptions emphasize:
  - layered blur
  - gradients and lighting
  - hover and press motion
  - customizability
- This maps cleanly to `motion/react` in code: pointer-tracked highlight,
  spring hover scale, spring press compression, and occasional drag.

Practical translation rule:
- If the user says “make it feel like a Framer liquid glass component,” build a
  stable React component with a glass shell, then layer Motion interactions on top.

## 4) Motion docs

Sources:
- https://motion.dev/docs/react-motion-component
- https://motion.dev/docs/react-use-spring

Why they matter:
- They define the safest interaction substrate for liquid-glass app UI.

Extracted takeaways:
- Use `motion.div`, `motion.button`, and friends as drop-in animated elements.
- Prefer transform and opacity animations for performance.
- Use `useSpring` to smooth pointer-driven motion values and avoid jitter.
- Use spring-linked motion values for tilt, sheen, pointer tracking, and dock motion.

Recommended Motion pattern for liquid-glass UI:
- raw pointer values with `useMotionValue`
- smoothing with `useSpring`
- derived transforms via inline style or `useTransform`
- `whileHover` / `whileTap` for quick tactile feedback

## 5) React liquid-glass libraries

Sources:
- https://github.com/rdev/liquid-glass-react
- https://github.com/naughtyduk/liquidGL
- https://github.com/remiangelo/reactGlass
- https://github.com/glincker/glinui
- https://mks2508.github.io/liquid-svg-glass/

What each one is useful for:

### liquid-glass-react
Good for:
- quick React drop-in
- studying feature knobs like frostiness, aberration, and elasticity

Steal these ideas:
- configurable distortion strength
- separate hover/click tuning
- browser support note for Safari/Firefox

### liquidGL
Good for:
- DOM-targeted refraction with WebGL
- real-time dynamic backgrounds when the glass needs to bend live content

Use only when:
- the user explicitly wants premium hero realism
- the app can tolerate extra complexity

### reactGlass
Good for:
- understanding the top-end aspiration of “real” liquid glass
- feature vocabulary: Fresnel, chromatic dispersion, caustics, realistic refraction

Use carefully:
- great as inspiration, often heavier than most app shells need

### glinui
Good for:
- seeing how liquid-glass ideas scale into a broader component system
- borrowing surface variants, semantic color variants, and app-shell discipline

### liquid-svg-glass
Good for:
- SVG displacement-driven React effects without jumping straight to shaders

## 6) What to borrow vs avoid

Borrow:
- layered surfaces
- strong radii and inner highlight rims
- subtle chromatic edges only when requested
- spring hover/press states
- a small number of premium glass surfaces
- progressive enhancement

Avoid by default:
- full-screen constant distortion
- heavy blur on every card
- long slow hover animations
- unreadable text on busy backgrounds
- shader stacks for ordinary panels and forms
- huge hero-only effects pasted into utilitarian dashboards
