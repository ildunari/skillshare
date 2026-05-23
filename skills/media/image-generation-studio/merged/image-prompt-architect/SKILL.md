---
name: image-prompt-architect
description: >
  Write optimized image generation prompts for GPT Image 1.5, Gemini Nano Banana Pro/2, Grok Aurora,
  and Adobe Firefly 4 — calibrated for UI/UX assets (icons, thumbnails, illustrations, animation
  frames, SVG-ready graphics) and general image production. Covers all modes: text-to-image,
  image-to-image editing, style transfer, and multi-image fusion. Use whenever the user wants AI
  image gen prompts for any model, UI assets, icon packs, design system visuals, animation keyframes,
  product mockups, or any visual asset. Also triggers on: "image prompt," "make me icons with AI,"
  "SVG-ready," "flat design," "write a prompt for ChatGPT/Gemini/Grok/Firefly image gen," or when
  the output is a prompt for an image generation model. Supersedes generic prompting skills for
  image gen targets.
---

# Image Prompt Architect

Write production-grade image generation prompts calibrated per-model, per-mode, and per-asset-type. Every prompt targets a specific model's strengths and a specific deliverable — not generic "make me a picture" output.

## Three Principles

**1. Model-aware prompting.** GPT Image 1.5, Gemini Nano Banana Pro/2, Grok Aurora, and Adobe Firefly 4 have fundamentally different architectures and respond to different prompt structures. A prompt optimized for one model produces mediocre results on another. Always know your target model before writing.

**2. Asset-type determines prompt structure.** An icon prompt and a hero image prompt share almost nothing. Icon prompts need geometric constraints, limited palettes, and SVG-readiness language. Hero images need compositional direction, lighting, and emotional narrative. The asset type dictates which prompt elements matter.

**3. Design system context is the consistency lever.** Isolated prompts produce isolated results. When generating assets for a cohesive product, feed the design system's tokens (palette hex codes, typography direction, spacing philosophy, brand personality) into every prompt. Consistency comes from shared constraints, not from hoping the model remembers.

## Mode Detection

Before drafting, identify which generation mode applies:

| Mode | Trigger | Key Pattern |
|---|---|---|
| **A: Text→Image** | User describes something to create from scratch | Full prompt construction from the pipeline |
| **B: Image→Image (global)** | User wants to transform/restyle an existing image | Preserve anchors (faces, logos, features), change style/time/mood globally |
| **C: Image Edit (local)** | User wants surgical changes to part of an image | "Change only [target]. Do not alter [protected]. Operation: [sequence]." |
| **D: Multi-Image Fusion** | User wants elements from 2-3 images combined | "Take [element] from A; place in [location] of B; apply [texture] from C. Match B's perspective/lighting." |
| **E: Style Transfer** | User wants an image rendered in a different style | "Render in the style of [genre/movement], preserving original composition and details." |

For modes B-E, the prompt structure shifts from scene-building to **edit directives** — specify what changes, what's protected, and how to harmonize the result. Load `references/editing-patterns.md` when available, or use the edit templates in each model's guide.

## Feedback Loop

**Read `FEEDBACK.md` before every use** to apply lessons from prior runs.

1. **Detect** — After producing prompts, note what didn't land: model ignored a constraint, style drifted, asset wasn't usable for intended purpose.
2. **Search** — Check `FEEDBACK.md` for existing entries on the same issue.
3. **Scope** — One actionable observation per entry.
4. **Draft-and-ask** — Propose the entry: "I noticed [issue]. Want me to log this?"
5. **Write-on-approval** — Append with date and category tag.
6. **Compact-at-75** — Merge duplicates, promote patterns to reference files, archive resolved. Reset to ~30 entries.

## Progressive Disclosure: What to Load

Load only what you need. Use this routing table.

| Reference | Load when... |
|---|---|
| `FEEDBACK.md` | **Always** — before every use |
| `references/gpt-image-guide.md` | Targeting ChatGPT / GPT Image 1.5 / gpt-image-1 API |
| `references/gemini-image-guide.md` | Targeting Gemini / Nano Banana Pro / Nano Banana 2 / Imagen 3 |
| `references/grok-image-guide.md` | Targeting Grok / Aurora / xAI image generation |
| `references/firefly-guide.md` | Targeting Adobe Firefly Image Model 4 / 4 Ultra |
| `references/ui-asset-patterns.md` | Generating any UI/UX asset (icons, thumbnails, illustrations, animation frames, empty states, hero images) |
| `references/enrichment-patterns.md` | Writing detailed subject descriptions (people, landscapes, products, buildings, animals, food) — micro-prompter templates |
| `references/design-system-integration.md` | Working with an existing design system, brand guidelines, or token set; or when consistency across multiple assets matters |

**Typical loading patterns:**
- "Make me app icons with ChatGPT" → `gpt-image-guide.md` + `ui-asset-patterns.md`
- "Generate a consistent icon set for my design system" → model guide + `ui-asset-patterns.md` + `design-system-integration.md`
- "Write a prompt for Gemini to make onboarding illustrations" → `gemini-image-guide.md` + `ui-asset-patterns.md`
- "I need animation start/end frames" → model guide + `ui-asset-patterns.md`

## The Pipeline

Every prompt goes through these steps:

```
1. MODEL SELECTION     → Identify target model, load model-specific guide
2. ASSET CLASSIFICATION → Identify asset type, load asset patterns
3. CONTEXT INTAKE      → Gather design system tokens, brand direction, use case
4. PROMPT DRAFTING     → Assemble prompt using model-specific structure
5. CONSTRAINT PASS     → Add exclusions, format specs, technical requirements
6. VARIANT GENERATION  → Produce 2-3 prompt variants for the user to test
7. POST-GEN GUIDANCE   → SVG conversion steps, batch workflow tips, edit prompts
```

### Step 1: Model Selection

If the user hasn't specified a model, ask — or recommend based on the asset type:

| Asset Type | Recommended Model | Why |
|---|---|---|
| **Icons, flat design, SVG-ready** | Gemini Nano Banana 2 | Best geometric precision, strong text, fast iteration |
| **UI mockups, wireframes, text-heavy** | GPT Image 1.5 | Superior text rendering, pixel-perfect layouts |
| **Photorealistic product shots** | Gemini Nano Banana Pro | Hyper-realistic texture and lighting |
| **Stylized illustrations, concept art** | GPT Image 1.5 | Broadest stylistic range, bold artistic output |
| **Rapid iteration / exploration** | Gemini Nano Banana 2 | Fastest generation (3-4 sec), good conversational editing |
| **Creative/experimental** | Grok Aurora | Strong creative latitude, good for exploration |
| **Commercially safe / stock-style** | Adobe Firefly 4 | Trained on licensed content, safe for commercial use |
| **Product photography** | Adobe Firefly 4 Ultra | Excellent product shots, integrates with Creative Cloud |

### Step 2: Asset Classification

Identify which asset type the user needs. Each type has specific prompt requirements documented in `references/ui-asset-patterns.md`:

| Category | Asset Types |
|---|---|
| **Icons** | App icons, navigation icons, icon packs, system icons, tab bar icons |
| **Illustrations** | Onboarding, empty states, error states, feature highlights, hero illustrations |
| **Thumbnails** | Card thumbnails, list thumbnails, preview images, social media cards |
| **UI Mockups** | Dashboard layouts, mobile screens, landing pages, component mockups |
| **Animation Frames** | Start/end keyframes, state transition frames, loading animation frames |
| **Textures & Patterns** | Background textures, decorative patterns, gradient meshes |
| **Logos & Marks** | Wordmarks, logomarks, app launcher icons |

### Step 3: Context Intake

Use `ask_user_input` to gather what you need. Adapt questions to what's already known.

**Always ask:**
- Target model (or let me recommend)?
- Asset type and quantity?
- Where will this be used? (app, web, specific screen/component)

**Ask if relevant:**
- Existing design system or brand guidelines? (colors, fonts, mood)
- Specific dimensions or aspect ratio?
- Light mode, dark mode, or both?
- Any reference images or style inspirations?
- Will these be converted to SVG?

**Don't over-interrogate.** Two rounds max. If the user gives a clear brief, skip straight to drafting.

### Step 4: Prompt Drafting

Load the target model's reference guide and follow its prompt structure. Each model has a different optimal format:

**GPT Image 1.5:** Natural prose paragraphs. Most important element first. Emotional/scenario direction in quotes. Hex codes as advisory backup alongside color names. Aspect ratio early in prompt.

**Gemini Nano Banana:** Narrative descriptions, not keyword lists. Camera/lens terminology for photorealism. Shorter than GPT (~60-100 words). Conversational editing after initial generation.

**Grok Aurora:** Natural language, 3-4 core elements max. Camera/lighting terminology. Prompt order matters (autoregressive). Keep concise.

**Adobe Firefly 4:** Follows the construction formula: [Subject] [Action] [Angle] [Lighting] [Background] [Color palette] [Style] [Image type]. Works with Visual Intensity slider (snapshot↔stylized), Effects presets, and Style/Composition references. Commercially safe — trained on licensed content.

### Step 5: Constraint Pass

Append technical constraints based on the asset's intended use:

| Use Case | Constraints to Add |
|---|---|
| **SVG conversion** | "Flat design, geometric shapes, no gradients, no texture, limited palette (3-5 colors), clean edges, high contrast, solid fills or uniform stroke, white/transparent background" |
| **App icon** | "Square 1:1, centered composition, 20% padding, no text, simple silhouette, reads at 32px" |
| **Animation frame** | "Consistent style across frames, same character/element proportions, clear state difference, flat lighting (no dramatic shadows that shift)" |
| **Dark mode asset** | "Works on dark backgrounds, no white bleeds, adequate contrast against #0a0a0a-#1a1a2e range" |
| **Print/retina** | "High detail, sharp edges, 4K resolution, no compression artifacts" |

### Step 6: Variant Generation — The Triad System

Always produce **3 prompt variants** using the Triad system. Each variant is a **complete, self-contained prompt** — not a suffix or modifier. The user should be able to paste any single variant and get a coherent result.

| Variant | Strategy |
|---|---|
| **1 — Cinematic Photoreal** | Optics, physically accurate light, materials, micro-detail. Camera/lens language woven into narrative. Best for photorealism and product shots. |
| **2 — Painterly / Illustrative** | Named medium (oil/watercolor/cel-shade/digital painting), line/shading treatment, palette scheme, stylized environment. Best for illustrations and creative assets. |
| **3 — Graphic / Design** | Minimalist or vector structure, negative space or geometric layout, precise palette and typographic logic. Best for icons, flat design, SVG-ready output. |

If the user's request clearly fits only one style category (e.g., "flat design icons"), produce 3 variants within that category instead — varying composition, palette emphasis, or detail level.

Present each variant in its own fenced `text` code block. Include a one-line summary above each block describing what makes it different.

### Step 7: Post-Generation Guidance

After delivering prompts, include actionable next-step guidance:

- **For SVG conversion:** Recommend vectorization tools (Vectorizer.AI, Vector Magic, Inkscape Trace Bitmap) and SVGO optimization
- **For batch consistency:** Suggest session-based workflow (same chat, reference images, style DNA template)
- **For animation frames:** Suggest interpolation tools (Neural Frames, KomikoAI) for in-betweening
- **For iterative editing:** Provide model-specific edit prompt templates

## Prompt Length Budgets

Image gen models lose coherence with long prompts. Respect these limits:

| Model | Target Length | Hard Max | Notes |
|---|---|---|---|
| GPT Image 1.5 | 80-150 words | 200 words | Handles longer prompts better than others |
| Gemini Nano Banana | 60-100 words | 130 words | Concise > verbose |
| Grok Aurora | 50-80 words | 120 words | Prompt order critical; front-load important elements |
| Adobe Firefly 4 | 60-120 words | 150 words | Single focal subject preferred; stage complexity across iterations |

## Cross-Model Prompt Translation

When a user has a prompt for one model and wants to adapt it:

**GPT → Gemini:** Shorten by ~30%. Convert emotional narrative to camera/composition language. Drop hex codes (use descriptive color names + swatch reference image). Add "no text" explicitly.

**GPT → Grok:** Shorten by ~40%. Front-load the subject. Convert detailed scene description to 3-4 core elements. Drop hex codes.

**Gemini → GPT:** Expand with emotional/narrative detail. Add style references. Include hex codes as advisory. Can handle more complex multi-element scenes.

## Design System Pairing

This skill is most powerful when paired with design system context. When the user has an established design system (Figma tokens, CSS variables, brand guidelines), load `references/design-system-integration.md` for the protocol on translating design tokens into image gen prompt constraints.

The key insight: **design tokens become prompt constraints.** `--color-primary: #2563EB` becomes "primary blue (#2563EB)." `font-family: Inter` becomes "clean sans-serif typography, Inter-style geometric letterforms." `border-radius: 12px` becomes "rounded corners, soft geometry."

## When This Skill Pairs With Others

| Skill | When to pair |
|---|---|
| **design-maestro** | When the generated assets will be used in a frontend build — use design-maestro for the UI, this skill for the image assets |
| **ui-spec-extractor** | When extracting design tokens from an existing UI to feed into image gen prompts |
| **canvas-design** | When the user wants a static poster/art piece rather than UI assets |
| **scientific-schematics** | When generating scientific diagrams (that skill has its own Nano Banana pipeline) |
| **claude-prompt-architect / gpt-prompt-architect** | When writing system prompts for AI, not image gen prompts — different domain entirely |
