---
name: openclaw-avatar-gen
description: Generate image prompts for OpenClaw agent avatars that maintain brand consistency with the voxel crab mascot while differentiating individual agents. Use when creating avatars for new OpenClaw agents, redesigning existing agent avatars, or when the user mentions agent identity, avatar, agent icon, profile picture, or OpenClaw branding. Also triggers on the `/avatar` command. Covers style analysis, palette derivation, identity-to-visual translation, and prompt generation for ChatGPT Image Gen 1.5 and Gemini 3 Pro (Nano Banana Pro).
---

# OpenClaw Avatar Generator

Generate production-ready image prompts for OpenClaw agent avatars. Every avatar stays in the voxel crab family while being instantly distinguishable at 64px in a Discord sidebar.

Target platforms: **ChatGPT Image Gen 1.5** (primary) and **Gemini 3 Pro / Nano Banana Pro** (secondary). Both are used through their respective apps with a subscription — no API.

## `/avatar` Command

When the user writes `/avatar` followed by a prompt, description, or any text — or just `/avatar` with no arguments in a conversation that has relevant context — treat it as an invocation of this skill. Specifically:

1. **`/avatar [text]`** — Use `[text]` as the identity intake input. Extract agent name, role, personality, and domain from the provided text. If the text is sparse (e.g., just a name or a vibe), fill gaps by asking the Step 1 interview questions.
2. **`/avatar`** (no arguments) — Pull context from the current conversation. Look for any agent descriptions, role definitions, personality traits, or identity details discussed so far. Synthesize those into the identity intake and run the full pipeline.
3. In both cases, run the complete pipeline (Steps 1–8) and output the 3 prompt variants for the user's target platform (default to ChatGPT Image Gen 1.5 if not specified).

## Prompt Output Formatting

All generated image prompts MUST be presented inside fenced code blocks — never blockquotes, never inline text, never any other markdown element. This lets the user copy-paste the entire prompt in one click.

### Code Block Safety Rules

Prompts often contain quotes, backticks, colons, brackets, and special characters that can break out of a fenced code block or trigger unintended markdown rendering. Follow these rules strictly:

1. **Use ` ```text ` as the fence language** — this disables all syntax highlighting and markdown interpretation inside the block.
2. **Never use triple backticks inside a prompt.** If you need to represent backticks in the prompt text, use single or double backticks only.
3. **Escape or rephrase problematic sequences** — if the prompt text would contain ` ``` ` (three+ consecutive backticks), reword that section.
4. **Keep quotes as plain ASCII** — use straight quotes (`"` `'`), not curly/smart quotes, to avoid encoding issues when pasting into image gen UIs.
5. **No leading `>` on any line** inside the code block (some renderers still interpret it).
6. **Close the code fence on its own line** with a blank line after it, separated from any surrounding text.
7. **One prompt per code block** — don't combine multiple variants in a single fence. Each variant (A, B, C) gets its own code block with a label above it.
8. **Before finalizing**, mentally scan the prompt text for any sequence that could terminate the fence or trigger markdown — colons at line starts, hash symbols, triple dashes, etc. Inside ` ```text ` these are safe, but stay vigilant.

## Prompt Length Management

Image gen models lose coherence as prompt length increases. Overly long prompts cause style drift, ignored constraints, and muddled compositions. Follow these limits:

| Platform | Target Length | Hard Max |
|---|---|---|
| ChatGPT Image Gen 1.5 | 80–120 words | 150 words |
| Gemini 3 Pro | 60–100 words | 130 words |

**Rules for staying within budget:**

- The Base Spec (brand constants) is ~40 words. That leaves ~60–80 words for identity deltas + constraints.
- Signifier descriptions get ONE clause each, not a full sentence. "One claw is a bronze gear-claw" not "One claw is a mechanical gear-claw made of interlocking bronze cog pieces that resemble industrial machinery."
- Expression direction is ONE phrase. "Subtle confident smirk" not a full scenario paragraph.
- Color names beat hex codes for word economy. Use hex only as a parenthetical backup: "dark navy (#1a1a2e)."
- If a prompt exceeds the hard max, cut adjectives and adverbs first, then merge the two signifier descriptions into one compound clause.
- Never repeat information. If the base spec says "no text," don't say it again in constraints.

## Feedback Loop

This skill uses a feedback log to improve over time. The cycle:

1. **Detect** — After completing a task using this skill, note anything that went wrong, was suboptimal, or could be improved (bad prompt phrasing, style drift, palette issues, platform rendering problems, missing modifiers).
2. **Search** — Check `FEEDBACK.md` for prior entries on the same topic to avoid duplicates.
3. **Scope** — Keep the feedback entry to 1–3 lines: category tag, what happened, what should change.
4. **Draft & Ask** — Draft the feedback entry and show it to the user before writing.
5. **Write on Approval** — Append the approved entry to `FEEDBACK.md`.
6. **Compact at 75** — When FEEDBACK.md reaches 75 entries, summarize and compact older entries to keep the file useful.

**Always read `FEEDBACK.md` when reading this skill.**

---

## When to Use

| Situation | Action |
|---|---|
| New OpenClaw agent needs an avatar | Full pipeline: analyze role → derive palette → generate prompt |
| Redesigning an existing agent avatar | Start from current identity, adjust parameters |
| User says "make me an avatar/icon for my agent" | Trigger this skill |
| User shares the OpenClaw crab image for reference | Analyze it, then run the pipeline |
| User wants avatars for multiple agents at once | Batch mode: shared style bible, per-agent variations |

---

## The Pipeline

Every avatar goes through these steps in order:

```
1. IDENTITY INTAKE       → Read the agent's role, name, emoji, personality
2. BASELINE ASSET PACK   → Generate/designate the anchor crab + palette swatch
3. STYLE BIBLE           → Lock the shared visual rules (voxel, lighting, composition)
4. PALETTE DERIVATION    → Map agent identity to a color scheme via Color Lock Ladder
5. SIGNIFIER DESIGN      → Choose 1–2 bold, geometric visual props
6. EXPRESSION + POSE     → Set emotional direction and body language
7. PROMPT ASSEMBLY       → Build prompt as Base Spec + Deltas + Constraints
8. VARIANT PASS          → Generate 3 prompt variants for selection
```

---

## Step 1: Identity Intake

Read the agent's workspace files (IDENTITY.md, SOUL.md, AGENTS.md) or ask the user directly. Extract:

| Field | Source | Example |
|---|---|---|
| **Name** | IDENTITY.md | Koder |
| **Emoji** | IDENTITY.md | ⚙️ |
| **Role** | IDENTITY.md creature + AGENTS.md mission | Coding agent, polyglot dev |
| **Personality** | SOUL.md vibe | Direct, technical, dry-humored |
| **Domain** | AGENTS.md scope | Code, builds, PRs, delegation |
| **Distinguisher** | What makes this agent NOT the default agent? | Dedicated dev arm vs. general assistant |

If files aren't available, interview the user with these exact questions:
1. What's the agent's name and emoji?
2. What does it do? (one sentence)
3. What's its personality in 3 words?
4. What should people feel when they see the avatar? (e.g., "trustworthy engineer" vs. "chaotic tinkerer")

---

## Step 2: Baseline Asset Pack

Before generating any agent-specific variants, establish the **anchor assets** that lock visual consistency across the entire crab family. This is the single biggest lever for consistent avatars — reference-anchored generation dramatically outperforms text-only prompting for character families.

### The Pack

| Asset | Purpose | When to Create |
|---|---|---|
| **Anchor Crab** | Neutral pose, baseline red palette, no signifiers. The "plain" family member. | Once, reused across all agents. |
| **Palette Swatch** | 4–6 flat color blocks for the target agent's palette. | Per agent, before variant generation. |

### How to Use

- **ChatGPT Image Gen 1.5:** Upload the Anchor Crab image alongside the variant prompt. Say "Use this character as the base — keep the same voxel style, proportions, and rendering. Apply only the changes described below."
- **Gemini 3 Pro:** Upload the Anchor Crab as a reference image. Gemini's multi-image composition and "visual DNA" retention work best when given a concrete reference rather than pure text description.

If no anchor image exists yet, generate one first using the Anchor Crab prompt from the Platform Adapters section.

### Anchor Crab Prompt (use this to generate the baseline)

```text
3D voxel-art crab mascot made of chunky visible cubes with faceted edges. Classic warm red shell, pink-red belly, black bead eyes with white specular highlights. Tiny smug smile. Claws raised symmetrically in a ready pose. Solid matte light blue background, soft contact shadow only. Single soft key light from upper-left, diffuse fill. Centered 1:1 square, slightly below eye-level camera. Cute but competent mascot, not realistic, not chibi. No text, no UI, no watermark.
```

---

## Step 3: Style Bible (Shared Across All Agents)

These rules are constant for every OpenClaw avatar. They maintain brand family consistency.

### Rendering Style
- **3D voxel art** — chunky, Minecraft-adjacent cubes with visible faceted edges
- Not flat pixel art — actual 3D depth with lighting and shadow
- Subtle anti-aliasing softens edges without losing the blocky identity
- Each surface facet is a visible cube/block

### Subject
- **Always a crab** — the OpenClaw mascot. Every agent is a crab variant.
- Anthropomorphized just enough for expression (eyes, mouth-line, posed claws)
- Not realistic, not chibi — mascot-grade character design

### Lighting
- Single soft key light from upper-left
- Diffuse fill, no harsh shadows
- Soft contact shadow on ground plane
- No rim lights, no dramatic contrast

### Composition & Safe Area
- Dead center, symmetrical (or near-symmetrical if pose breaks it)
- Slightly below eye-level camera (looking slightly up at the crab)
- Tight crop with breathing room on all sides
- Square format (1:1 aspect ratio for Discord/profile use)
- **Keep all important details within the inner 85% of the canvas** — no props touching the frame edge, no signifiers in corners that get cropped by circular avatar masks

### Background
- Solid matte color, no gradients, no environment
- Color should complement (not match) the crab's palette
- Soft contact shadow is the only ground reference

### Size Constraints
- Must read clearly at **64x64 px** (Discord sidebar)
- Must look good at **256x256 px** (profile modal)
- Silhouette should be recognizable without color (squint test)
- Generate at 1024x1024 minimum, then verify it works downscaled

### Exclusions
- No text, no UI elements, no watermarks
- No environment/scene — just the character on a backdrop
- No accessories that obscure the crab silhouette
- No more than 2 props/signifiers (clutter kills readability at small sizes)

---

## Step 4: Palette Derivation

Map the agent's identity to a color scheme. The palette has 4 slots:

| Slot | Role | Derivation |
|---|---|---|
| **Shell primary** | Main body color | Derived from agent's domain (see palette map) |
| **Shell secondary** | Belly, underside, depth shading | Darker or desaturated variant of primary |
| **Accent** | Signifier props, edge glow, eye highlights | Derived from agent's emoji color or energy |
| **Background** | Solid backdrop | Complementary to shell primary, muted |

### Color Lock Ladder

Image gen models do NOT reliably follow hex codes. Use the strongest color control method available, in this order:

| Priority | Method | When to Use |
|---|---|---|
| **A (best)** | Upload a palette swatch reference image (4–6 flat color blocks) | Always, if you have time to make the swatch |
| **B** | Upload the Anchor Crab as style/color reference | When you want the model to match the family look |
| **C** | Use descriptive color names + "limited palette of 5–6 hues total" | When no reference images are available |
| **D (weakest)** | Add hex codes as advisory hints in parentheses | As a backup alongside color names, never as the sole method |

For Gemini 3 Pro specifically: generate first, then use spot-color edit prompts to correct any palette drift without regenerating from scratch.

### Palette Map (domain to color direction)

| Agent Domain | Shell Primary | Accent | Background | Rationale |
|---|---|---|---|---|
| Coding / Dev | Gunmetal grey, dark steel blue | Amber, orange | Dark navy | Terminal/IDE aesthetic |
| Research / Docs | Deep forest green | Gold | Warm grey | Academic, knowledge |
| Chat / Social | Warm coral, soft red | Sky blue | Light cream | Approachable, friendly |
| Ops / Infra | Dark slate | Electric green | Charcoal | Dashboard/monitoring |
| Creative / Design | Deep purple | Hot pink | Soft black | Artistic, expressive |
| Security / Auth | Matte black | Red | Dark grey | Alert, controlled |
| Data / Analytics | Navy | Cyan | Dark teal | Data viz aesthetic |
| General / Default | Classic red (brand) | White highlights | Light blue | The original mascot |

These are starting points. The user can override any slot.

### Emoji-to-Accent Fallback

If the palette map doesn't fit, derive accent from the agent's emoji:

| Emoji | Accent Color |
|---|---|
| ⚙️ | Amber/orange |
| 🔬 | Neon green |
| 🎨 | Hot pink / magenta |
| 🛡️ | Steel blue |
| 📊 | Cyan |
| 🤖 | Electric blue |
| 🔥 | Red-orange |
| 💬 | Sky blue |

---

## Step 5: Signifier Design

Choose **1–2 visual props** that encode the agent's role. These are the things that make this crab NOT the default crab.

### Rules
- Max 2 signifiers: 1 body modification + 1 accessory/prop
- Each signifier must be **bold and geometric** — avoid thin wires, sticks, textures, or tiny details that vanish at small sizes
- Each must be readable as a silhouette at 64px
- Place signifiers in priority zones: **head** (best), **claws** (best), **shell center** (ok). Avoid tiny side details.
- Add a subtle darker edge stroke on signifiers for icon-like contrast separation
- No text on props

### Signifier Menu

| Domain | Good Signifiers | Avoid |
|---|---|---|
| Coding | Mechanical gear-claw, welding goggles, terminal-green eye glow | Keyboard (too small at 64px), laptop (too generic) |
| Research | Magnifying glass claw, reading spectacles, glowing scroll | Stack of books (unreadable small) |
| Chat | Speech bubble emerging from claw, headset | Phone (generic) |
| Ops | Antenna on shell, status-light eyes (green/amber/red), hardhat | Dashboard (too complex) |
| Creative | Paint-splatter on shell, one prismatic/rainbow claw | Paintbrush (too thin) |
| Security | Visor/eyeshield, lock-shaped claw tip, scar across shell | Shield (too fantasy) |
| Data | One eye replaced with chart/graph lens, glowing data-lines on shell | Calculator (dated) |

### Custom Signifier Template

If nothing in the menu fits:
- Pick one **body modification** (claw swap, eye change, shell marking, headgear)
- Pick one **held/attached prop** (tool, accessory, glow effect)
- Test: "If I described this to someone who can't see the image, could they guess the agent's role?"
- Test: "Is this signifier a simple bold shape, or does it have fiddly detail that disappears at 64px?"

---

## Step 6: Expression + Pose

### Expression Direction

Don't say "happy" or "confident" — give the image gen model a *scenario* it can translate to micro-expressions:

| Agent Personality | Expression Direction |
|---|---|
| Terse, senior, competent | "Already knows the fix — subtle smirk, slightly narrowed eyes" |
| Friendly, helpful, warm | "Just heard a good question — bright eyes, slight head tilt" |
| Paranoid, careful, precise | "Inspecting something closely — one eye slightly squinted, claws positioned carefully" |
| Chaotic, fast, experimental | "About to try something wild — wide eyes, open-claw gesture, slight lean forward" |
| Calm, authoritative, steady | "Waiting patiently — neutral mouth, even gaze, weight centered" |

### Pose Direction

| Energy | Pose |
|---|---|
| Ready to work | Leaning forward, one claw on surface, weight on front legs |
| Completed / reporting | Standing tall, claws at sides, slight upward chin |
| Thinking / planning | One claw raised to chin area, head slightly tilted |
| Active / building | Both claws engaged with prop/tool, dynamic angle |
| Default / neutral | The original mascot pose — claws raised, symmetrical |

---

## Step 7: Prompt Assembly

### Architecture: Base Spec + Deltas + Constraints

Prompts are built from three blocks, not a monolithic paragraph. This structure keeps brand constants locked, makes variants easy to produce (only the Deltas block changes), and respects prompt length budgets.

**Block 1 — Base Spec (brand constants, never changes):**
The voxel crab identity, lighting, composition, and background. This block is identical across every agent and every variant. ~40 words.

**Block 2 — Identity Deltas (per-agent, per-variant):**
Palette, signifiers, expression, pose. This is what makes each avatar unique. ~40–60 words.

**Block 3 — Hard Constraints (exclusions):**
What the model must NOT do. Keep this short — don't repeat anything already stated in the base spec. ~15–20 words.

### Assembled Prompt Template

The final assembled prompt MUST be output inside a ` ```text ` fenced code block — never a blockquote or raw markdown. Review the Prompt Output Formatting and Code Block Safety rules before writing.

```
[BASE SPEC]
3D voxel-art crab mascot made of chunky visible cubes with faceted edges.
[BODY_DESCRIPTION]. [SIGNIFIER_1]. [SIGNIFIER_2]. Eyes: black with white
specular highlights, [EXPRESSION_DIRECTION]. Pose: [POSE_DIRECTION].
Solid matte [BG_COLOR] background, soft contact shadow only. Soft key
light from upper-left. Centered 1:1 square, slightly below eye-level
camera. Cute but competent [DOMAIN] mascot.

[CONSTRAINTS]
No text, no UI, no watermark, no environment, no extra props.
```

### Slot Definitions

| Slot | What to Write | Example |
|---|---|---|
| `BODY_DESCRIPTION` | Shell color + accent, ONE clause | "Dark gunmetal-grey shell with amber accent lines" |
| `SIGNIFIER_1` | Body mod, ONE clause | "One claw is a bronze gear-claw" |
| `SIGNIFIER_2` | Prop/accessory, ONE clause | "Amber welding goggles pushed up on forehead" |
| `EXPRESSION_DIRECTION` | Short phrase from Step 6 | "subtle confident smirk" |
| `POSE_DIRECTION` | Short phrase from Step 6 | "leaning forward, gear-claw resting on surface" |
| `BG_COLOR` | Color name + optional hex | "dark navy (#1a1a2e)" |
| `DOMAIN` | One word | "engineer" |

### Anti-Rewrite Tip (ChatGPT Image Gen)

ChatGPT's image gen rewrites your prompt internally before generating. If your prompts are detailed enough (which they should be following this skill), the rewriting usually helps. But if the model keeps adding unwanted elements (environments, extra detail, stylistic drift), prepend this wrapper:

```
I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:
```

Use this sparingly — only when the model is fighting your intent.

---

## Step 8: Variant Pass

Always generate **3 prompt variants** so the user can pick or mix:

| Variant | What Changes |
|---|---|
| **A — Faithful** | Closest to brand crab. Minimal signifiers, classic pose, palette shift only. |
| **B — Signature** | Full identity treatment. Custom signifiers, expression, pose. The recommended pick. |
| **C — Bold** | Pushes further. Stronger color contrast, more dramatic signifier, slightly different angle. |

Present all three with a one-line summary of what makes each different. Each variant's prompt goes in its own ` ```text ` code block (see Prompt Output Formatting rules above). Never combine variants into a single code block or use blockquotes.

**Only the Identity Deltas block changes between variants.** The Base Spec and Constraints blocks stay identical. This is what keeps the family consistent while allowing per-variant exploration.

---

## Platform Adapters

### ChatGPT Image Gen 1.5 (Primary)

ChatGPT's native image generation handles detailed prose well and is the default target for this skill.

**Prompt style:**
- Write prompts as natural English prose, not keyword lists
- Put the most important visual element first (the voxel crab)
- Emotional direction in quotes works well: expression is "just solved a hard bug"
- Specify "1:1 square" explicitly
- Include color names as primary, hex codes as advisory parenthetical backup
- Include negative constraints at the end: "No text, no UI, no watermark"

**Consistency workflow:**
- Generate the Anchor Crab first (Step 2)
- For each agent variant, upload the Anchor Crab alongside the prompt
- Say: "Use this character as the base. Keep the same voxel style, proportions, and rendering. Apply only the changes described below."
- If the model drifts, regenerate with "Maintain the exact same voxel art style" prepended

**Common failures and fixes:**
- May smooth out voxel edges: reinforce "chunky visible cubes with faceted edges"
- Adds environment details even when told not to: reinforce "solid matte [color] background"
- Sometimes adds text/labels unprompted: always include "no text" exclusion
- Exact counting can be unreliable (crab legs/claws may drift): if anatomy is wrong, regenerate rather than trying to fix via prompt tweaks

### Gemini 3 Pro / Nano Banana Pro (Secondary)

Use in the Gemini app. Select "Create images" then choose the "Thinking" model for Nano Banana Pro quality.

**Prompt style:**
- Structure prompts as: subject + composition + action/pose + style + constraints
- Prefer descriptive prose over keyword lists
- Specify camera angle, lighting, and aspect ratio explicitly
- Keep prompts slightly shorter than ChatGPT (~60–100 words) — Gemini responds well to concise, specific direction

**Consistency workflow (the key differentiator):**
Gemini is designed for iterative refinement, not one-shot perfection. The recommended workflow is:

1. **Generate** the base avatar with the full prompt
2. **Edit iteratively** using tightly scoped edit prompts (change one thing at a time)
3. **Correct palette** using spot-color edit prompts — Gemini excels at tweaking individual colors without distorting the rest of the image

**Edit prompt template (use after initial generation):**

```
Using the provided image, change only [specific element] to [new description].
Keep everything else exactly the same — same style, lighting, composition, and proportions.
Do not change the aspect ratio.
```

**Example edit prompts:**

```
Using the provided image, change only the background color to dark navy. Keep everything else exactly the same.
```

```
Using the provided image, change only the left claw into a chunky voxel gear-claw. Keep everything else exactly the same.
```

```
Using the provided image, change only the accent lines to amber-orange. Keep everything else exactly the same.
```

**Doodle edits (when text is too imprecise):**
Gemini supports drawing/marking directly on images to target edits. For signifier changes, circle the claw area and request a swap. For background changes, circle the background and request a color change. This is often more precise than text-only editing for spatial modifications.

**Reference inputs:**
If uploading reference images, specify what each one is for: "Use this image for the character style and proportions" vs "Use this image for the color palette only." Gemini handles multi-image composition well when given clear role assignments.

**Known limitations:**
- Complex edits can produce artifacts — prefer simple, atomic changes
- Consistency across many sequential edits may drift — if it drifts too far, regenerate from the prompt rather than continuing to patch
- Fidelity issues are possible with mechanical/detailed signifiers — use bold geometric shapes

---

## Example: Koder (Coding Agent)

### Identity Intake
- Name: Koder, Emoji: ⚙️, Role: Polyglot coding agent
- Personality: Direct, technical, dry-humored
- Distinguisher: Dedicated dev arm, not general assistant

### Palette
- Shell: Dark gunmetal grey
- Secondary: Darker steel
- Accent: Amber-orange (from ⚙️)
- Background: Dark navy

### Signifiers
1. One claw is a bronze gear-claw — body mod
2. Amber welding goggles on forehead — prop

### Expression + Pose
- Expression: "subtle confident smirk"
- Pose: leaning forward, gear-claw resting on surface

### Final Prompt — Variant B Signature (ChatGPT Image Gen 1.5)

```text
3D voxel-art crab mascot made of chunky visible cubes with faceted edges. Dark gunmetal-grey shell with amber-orange accent lines along segment edges. One claw is a bronze gear-claw. Amber welding goggles pushed up on forehead. Eyes: black with white specular highlights, subtle confident smirk. Pose: leaning forward, gear-claw resting on surface, ready-to-work energy. Solid matte dark navy (#1a1a2e) background, soft contact shadow only. Soft key light from upper-left. Centered 1:1 square, slightly below eye-level camera. Cute but competent engineer mascot. No text, no UI, no watermark, no environment.
```

### Gemini 3 Pro — Generation + Edit Pack

**Generation prompt:**

```text
3D voxel-art crab mascot, chunky visible cubes with faceted edges. Dark gunmetal-grey shell, amber-orange accents. Bronze gear-claw on one side, amber goggles on forehead. Subtle confident smirk, leaning forward. Solid dark navy background, soft shadow. Soft upper-left key light. Centered 1:1 square, below eye-level camera. Cute competent engineer mascot. No text, no watermark.
```

**Follow-up edit prompts (use after generation if needed):**

```text
Using the provided image, change only the background color to dark navy. Keep everything else exactly the same.
```

```text
Using the provided image, change only the accent lines to amber-orange. Keep everything else exactly the same.
```

---

## Quick Reference: The 7 Anchors

When reviewing any generated avatar, check these. If any fail, iterate:

1. **Crab?** — Is it recognizably a crab (not a lobster, spider, or robot)?
2. **Voxel?** — Are the cube facets visible? Not smooth, not flat pixel art?
3. **64px test** — Can you tell which agent this is at 64x64?
4. **Silhouette** — Does the shape read without color?
5. **Family** — Would this look like it belongs next to the brand red crab?
6. **Role** — Can a stranger guess the agent's domain from the visual?
7. **Clean** — No text, no clutter, no environment?
