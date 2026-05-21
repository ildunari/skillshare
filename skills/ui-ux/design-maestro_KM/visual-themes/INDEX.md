# Visual Themes

> 21 production-grade visual themes (Schema v2) + a research-backed knowledge base. Each theme is a complete design system with 15 mandatory sections covering color, typography, elevation, borders, component states, motion, layout, accessibility, overlays, and implementation guidance.

## How Theme Files Are Organized

Each theme lives in its own directory with two files:

| File | Size | When to Read | What It Contains |
|---|---|---|---|
| `index.md` | 3-8K | **Always read first.** Quick styling, theme selection confirmation, basic implementation. | Identity, complete color tokens, font stack + key weights, elevation strategy summary, motion personality, section index for full.md |
| `full.md` | 720-1200 lines | **Read when you need deep specs.** Full component builds, complete state machines, detailed animation CSS. | Complete Schema v2 spec — all 15 sections with every token, every state, every transition |

### Reading Strategy
- **Theme selection:** Read SKILL.md catalog only (you're already here)
- **Quick styling** (colors, fonts, basic shadows): Read `index.md`
- **Specific deep section** (e.g., just component states): Read `index.md` for the section index, then use `offset`/`limit` to read only that section from `full.md`
- **Full UI build from scratch:** Read `full.md` entirely (rare — only when building a complete app/site)

## Routing

### Theme Files

| Resource | Path |
|---|---|
| Theme index (read first) | `references/themes/NN-theme-name/index.md` |
| Theme full spec | `references/themes/NN-theme-name/full.md` |
| Animation patterns | `references/animation-patterns.md` |

### Knowledge Base

Load these when making design decisions or answering design questions — not for every themed artifact.

| Topic | Path | When to load |
|---|---|---|
| Color science & perception | `references/knowledge-base/01-color-science.md` | Palette construction, contrast decisions, wide-gamut, OKLCH |
| Typography & tokens | `references/knowledge-base/02-typography-tokens.md` | Font selection, type scale, design token architecture |
| Motion, texture & materiality | `references/knowledge-base/03-motion-texture.md` | Animation philosophy, easing, texture techniques, glass/noise |
| Global aesthetics & culture | `references/knowledge-base/04-global-aesthetics.md` | Non-Western design, cultural sensitivity, trend context |
| Generative & data viz | `references/knowledge-base/05-generative-dataviz.md` | Generative art principles, data color, chart theming |
| Quick-reference checklists | `references/knowledge-base/06-checklists.md` | Pre-flight checks for palette, type, tokens, motion, a11y |
| Bibliography | `references/knowledge-base/07-bibliography.md` | Source URLs, further reading |
| Theme generation schema v2 | `references/knowledge-base/theme-schema-v2.md` | JSON schema for AI-assisted theme creation, section definitions |

### Cross-Skill References

| Resource | Location |
|---|---|
| Font pairings | design-maestro `references/themes.md` |
| Advanced CSS/WebGL effects | design-maestro `references/advanced-effects.md` |
| Anti-slop checklist | design-maestro `references/aesthetic-principles.md` |
| Motion library | design-maestro `references/motion-library.md` |

## Feedback Loop

**FEEDBACK.md lives at the skill root.** Read it at the start of every task that uses this skill.

**Cycle:**

1. **Detect** — After delivering a themed artifact, watch for user corrections, preferences, or complaints about any theme element.
2. **Search** — Check `FEEDBACK.md` for prior entries on the same theme or issue category.
3. **Scope** — Determine if the feedback is theme-specific or cross-cutting.
4. **Draft & Ask** — Draft a FEEDBACK.md entry with category tag and theme tag. Confirm with the user before writing.
5. **Write on Approval** — Append the entry to FEEDBACK.md using the tagged format.
6. **Compact at 75** — When entries reach 75, consolidate: merge duplicates, promote recurring feedback into the relevant theme file as a permanent rule, and reset the log.

## Theme Catalog

Read the descriptions below to select the right theme. Then load the theme's `index.md` for quick implementation or `full.md` for deep specs.

---

### 1. Editorial Calm
**Path:** `references/themes/01-editorial-calm/`
**Best for:** Anthropic-style UIs, editorial apps, reading experiences, dashboards, generative art
**Vibe:** Warm editorial matte — sunlit magazine spread, terracotta ink, matte watercolor
**Palette:** Warm beige/cream, terracotta-orange accent (`#D97757`), warm neutrals
**Typography:** Plus Jakarta Sans + DM Sans + Geist Mono
**Motion:** Nearly invisible — editorial stagger, gentle springs, 150ms UI / 300ms reveals
**Modes:** Canvas (warm beige, generative art) + Dashboard (warm white, SaaS/analytics)

---

### 2. Ethereal Porcelain
**Path:** `references/themes/02-ethereal-porcelain/`
**Best for:** Fluid dynamics, fractals, gallery UIs, art portfolios, generative simulations
**Vibe:** Cool gallery neutrals with subsurface scattering — surfaces glow faintly from within, like porcelain held to light
**Palette:** Cool linen/dove grey, kintsugi gold accent (`#C4A265`), muted slate
**Typography:** DM Serif Display + Instrument Sans + Geist Mono
**Motion:** Gentle springs, 200ms UI / 500ms reveals, subtle float
**Signature:** Subsurface scattering glow effect on hover

---

### 3. Manuscript
**Path:** `references/themes/03-manuscript/`
**Best for:** Reading apps, documentation, knowledge bases, blogs, longform editorial
**Vibe:** Living manuscripts — serif typography as identity, paper as material metaphor
**Palette:** Warm parchment/vellum, copper-gold accents, warm ink tones
**Typography:** EB Garamond (Alchemical) / Newsreader (Editorial) + sans UI fallback
**Motion:** Ink-smooth easings, 200ms UI / 400ms page transitions
**Modes:** Alchemical (organic, experimental) + Editorial (reading-optimized, precise)

---

### 4. Kintsugi
**Path:** `references/themes/04-kintsugi/`
**Best for:** Meditation apps, journaling, CJK content, contemplative UIs, minimal dashboards
**Vibe:** Broken vessels mended with gold — extreme negative space, washi paper warmth, quiet beauty of imperfection
**Palette:** Washi neutrals, gold repair lines (`#C4A44A`), tatami undertones
**Typography:** Shippori Mincho (CJK serif) + Zen Kaku Gothic (CJK sans) + IBM Plex Mono
**Motion:** Slowest theme (300-1000ms), contemplative easings, no springs
**Signature:** Gold as structural repair only — 1px lines, never fill

---

### 5. Liquid Glass
**Path:** `references/themes/05-liquid-glass/`
**Best for:** Apple-style UIs, settings panels, system utilities, music apps, translucent overlays
**Vibe:** Frosted surfaces floating in light — precision depth through translucency
**Palette:** System greys, semi-transparent whites, blue accent (`#007AFF`), backdrop blur
**Typography:** SF Pro Display + SF Pro Text + SF Mono (system) / Inter + Geist Mono (web)
**Motion:** Snappy springs, 150ms UI / 350ms modals, rubber-band physics
**Signature:** `backdrop-filter: blur()` + `rgba()` layering, vibrancy

---

### 6. Midnight Observatory
**Path:** `references/themes/06-midnight-observatory/`
**Best for:** Data visualization, astronomy tools, scientific dashboards, analytics, dark IDE themes
**Vibe:** Deep space meets scientific cartography — warm gold constellations on infinite navy
**Palette:** Navy/indigo depths, gold emission (`#D4A854`), instrument panel blues
**Typography:** Instrument Sans + Albert Sans + JetBrains Mono
**Motion:** Gravitational/orbital easings, 200ms UI / 600ms reveals, telescope zoom
**Signature:** Star field background (Canvas 2D), constellation grid overlay, gold glow bloom

---

### 7. Monochrome Terminal
**Path:** `references/themes/07-monochrome-terminal/`
**Best for:** Dev tools, IDE themes, terminal apps, monitoring dashboards, technical documentation
**Vibe:** Single-accent monochrome — exposed structure, zero decoration, maximum density
**Palette:** Concrete greys (warm) or clinical greys (cool), single accent (red or cyan)
**Typography:** Space Grotesk + JetBrains Mono (warm) / Inter + Geist Mono (cool)
**Motion:** Mechanical, linear, no springs — 80ms UI / 150ms reveals
**Modes:** Warm (concrete, red accent) + Cool (clinical, cyan accent)
**Signature:** Borders-only elevation, 0px radius, visible grid

---

### 8. Abyssal Glow
**Path:** `references/themes/08-abyssal-glow/`
**Best for:** Creative dashboards, music production, cyberpunk UIs, AI chat, gaming interfaces
**Vibe:** Darkness as canvas, light as language — glow-based depth on near-black surfaces
**Palette:** Near-black bases, colored glow accents (cyan/teal/pink per mode)
**Typography:** Outfit + Inter + JetBrains Mono
**Motion:** Mode-dependent — snappy cyberpunk, breathing organic, or precise signal
**Modes:** Electric (cyberpunk cyan) + Organic (bioluminescent teal) + Signal (urban pink/blue)
**Signature:** Additive glow blending, 3-layer glow pipeline, no traditional shadows

---

### 9. Vapor Silk
**Path:** `references/themes/09-vapor-silk/`
**Best for:** Meditation apps, wellness platforms, ambient music, journaling, calm productivity
**Vibe:** Pastel ambient mesh — silk scarves drifting through warm light, the calmest possible interface
**Palette:** Warm cream base, soft pastels (lavender, blush, sage), muted accents
**Typography:** Outfit + DM Sans + Geist Mono
**Motion:** Ultra-slow (200-800ms), silk-smooth easings, 25-second ambient mesh drift
**Signature:** Ambient mesh gradient background, generous radius, extreme blur shadows

---

### 10. Solarpunk Brass
**Path:** `references/themes/10-solarpunk-brass/`
**Best for:** Environmental dashboards, botanical databases, sustainable tech, IoT sensor displays
**Vibe:** A greenhouse full of technology — vine-covered circuits, polished brass, warm sunlight through green glass
**Palette:** Greenhouse linen, brass gold (`#C49A3C`), botanical green (`#4A7C59`)
**Typography:** Fraunces (display) + Albert Sans (body) + JetBrains Mono
**Motion:** Dual language — organic (growth curves) + mechanical (brass clicks)
**Signature:** Organic + mechanical coexistence, dual shadow system, botanical data viz

---

### 11. Print & Paper
**Path:** `references/themes/11-print-and-paper/`
**Best for:** Portfolio sites, art projects, educational tools, playful apps, physical-craft digital
**Vibe:** Physical craft made digital — paint, paper, ink with pixel-perfect engineering
**Palette:** Mode-dependent craft colors; shared rule: ZERO gradients, flat fills only
**Typography:** Bricolage Grotesque + DM Sans + JetBrains Mono
**Motion:** Snappy overshoot, stamped/physical feel, hard shadow transitions
**Modes:** Gouache (matte paint) + Paper Cut (layered parallax) + Riso (halftone overprint)
**Signature:** Hard directional shadows (0 blur), die-cut edges, registration offset

---

### 12. Crystalline Matrix
**Path:** `references/themes/12-crystalline-matrix/`
**Best for:** Data visualization, scientific tools, CAD viewers, financial modeling, algorithmic art
**Vibe:** Geometric prismatic precision — light splitting through faceted crystal, rainbow spectra at structural edges
**Palette:** Cool platinum whites, prismatic rainbow borders (accent only), sapphire blue
**Typography:** Instrument Sans + Albert Sans + Geist Mono
**Motion:** Geometric-ease (computed feel), 120ms UI / 300ms reveals, facet transitions
**Signature:** Conic-gradient prismatic borders, faceted surface gradients, wireframe overlays

---

### 13. Warm Darkroom
**Path:** `references/themes/13-warm-darkroom/`
**Best for:** Photography portfolios, editorial longform, journal apps, analog-aesthetic tools
**Vibe:** Chemical patience — images emerge from darkness the way trust emerges from silence
**Palette:** Sepia-warm darks, amber safe-light (`#D4883C`), warm paper highlights
**Typography:** Playfair Display + Source Sans 3 + JetBrains Mono
**Motion:** Chemical-slow reveals (400-1200ms), developer-fluid easings
**Signature:** Safe-light amber illumination, surface-shift elevation, chemical reveal animations

---

### 14. Ceramic Glaze
**Path:** `references/themes/14-ceramic-glaze/`
**Best for:** Lifestyle apps, wellness platforms, note-taking, recipe apps, cozy SaaS
**Vibe:** Soft tactile ceramic — viscous spring animation, rounded surfaces, cobalt glaze pooling in curves
**Palette:** Warm bisque/cream, cobalt blue accent (`#2B5EA7`), terracotta undertones
**Typography:** Nunito + DM Sans + Geist Mono
**Motion:** Viscous springs (250-400ms settle), weighted damping, no floaty motion
**Signature:** 12px minimum radius, cobalt glaze pooling effect, weighted-but-soft tension

---

### 15. Sunlit Concrete
**Path:** `references/themes/15-sunlit-concrete/`
**Best for:** Manufacturing dashboards, SCADA/HMI, industrial IoT, safety compliance, factory control
**Vibe:** Industrial daylight — safety colors carry meaning, condensed type carries density, readable from across the room
**Palette:** Raw concrete, OSHA orange (`#E87B35`), safety yellow, caution red
**Typography:** Barlow Condensed + Barlow + JetBrains Mono
**Motion:** Pneumatic (instant + brake), mechanical snap, industrial precision
**Signature:** Massive KPI readouts, condensed industrial typography, safety-color semantics

---

### 16. Iridescent
**Path:** `references/themes/16-iridescent/`
**Best for:** Consumer tech, portfolios, product pages, creative tools, futuristic landing pages
**Vibe:** Futuristic chrome surfaces refracting light through conic-gradient halos
**Palette:** Cool whites (holographic) or warm platinums (chrome), prismatic accents
**Typography:** Sora + Inter + Geist Mono
**Motion:** Spring physics with magnetic snap, 150ms UI / 400ms reveals
**Modes:** Holographic (cool, prismatic, soap-bubble) + Chrome (warm, metallic, brushed)
**Signature:** Conic-gradient borders, iridescent sweeps, specular highlights

---

### 17. Pixel Grid
**Path:** `references/themes/17-pixel-grid/`
**Best for:** Data dashboards, analytics, developer monitoring, terminal-adjacent apps, telemetry
**Vibe:** Quantized data on a grid — if it feels smooth, step it; if it feels round, square it
**Palette:** Warm earthy (Gazette) or true black (Terminal), 6 per-agent accent colors
**Typography:** Space Grotesk + JetBrains Mono (warm) / Inter + Geist Mono (cool)
**Motion:** Quantized `steps(n)` timing — no cubic-bezier curves, tick-based animation
**Modes:** Warm "Gazette" (newspaper broadsheet) + Cool "Terminal" (Vercel-grade)
**Signature:** 0px radius everywhere, borders-only, ALL CAPS headlines (warm)

---

### 18. Mashrabiya Matrix
**Path:** `references/themes/18-mashrabiya-matrix/`
**Best for:** RTL-first apps, Arabic/Farsi/Hebrew platforms, Islamic art, calligraphy tools, geometric pattern generators
**Vibe:** Light filtered through geometric lattice — bilateral symmetry, mathematical ornament, sacred pattern architecture
**Palette:** Desert sand, turquoise action (`#1A8A7D`), gold emphasis (`#C49A3C`), deep lapis
**Typography:** IBM Plex Sans Arabic + Noto Kufi Arabic + IBM Plex Mono Arabic
**Motion:** No springs — only smooth mathematical curves, bilateral symmetry in transitions
**Signature:** Pattern-based elevation (lattice overlays), RTL-native `direction: rtl` default

---

### 19. Monsoon Bazaar
**Path:** `references/themes/19-monsoon-bazaar/`
**Best for:** Event marketing, festival pages, music platforms, food delivery, cultural showcases
**Vibe:** South Asian poster energy — saturated inks, registration offset depth, controlled chaos at maximum volume
**Palette:** Deep indigo, marigold (`#E8A317`), vermillion, emerald, maximum saturation
**Typography:** Teko (display) + Work Sans (body) + JetBrains Mono
**Motion:** Stamped/printed feel, registration offset, energetic overshoot
**Signature:** Registration offset depth (multi-layer color shift), poster-grade typography

---

### 20. Future Medieval
**Path:** `references/themes/20-future-medieval/`
**Best for:** Fantasy apps, tabletop RPG tools, worldbuilding wikis, grimoire-style docs, interactive fiction
**Vibe:** Arcane precision — an enchanted library where illuminated manuscripts meet modern interfaces
**Palette:** Deep oak/parchment darks, gilt gold (`#C9A84C`), oxblood (`#8B2E2E`), vellum
**Typography:** Cinzel (display) + Cormorant Garamond (body) + JetBrains Mono
**Motion:** Ceremonial (300-600ms), page-turn transitions, candlelight flicker
**Signature:** Illuminated initial caps, arcane glow effects, parchment texture overlays

---

### 21. Cartographer's Desk
**Path:** `references/themes/21-cartographers-desk/`
**Best for:** Spatial data apps, geographic dashboards, project management, topology views, knowledge graphs
**Vibe:** Layered topographic surfaces — spatial UI where every element has map coordinates and elevation is literal
**Palette:** Chart paper yellows, drafting vellum, contour blue (`#3D7AB5`), survey orange
**Typography:** Overpass + Source Sans 3 + IBM Plex Mono
**Motion:** Cartographic pan/zoom, layered parallax, compass-needle settle
**Signature:** Topographic contour lines, paper-stacking depth model, coordinate overlays
