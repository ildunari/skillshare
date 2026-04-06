# Image Gen Platform Reference

## ChatGPT Image Gen 1.5 (Primary Platform)

### Access
Native image generation inside the ChatGPT app (web, iOS, Android). Requires a ChatGPT Plus/Pro/Team subscription. No API — all usage is through the app interface.

### Strengths
- Excellent at following detailed prose descriptions
- Understands emotional/character direction well (expression is "just solved a hard bug")
- Respects hex color codes reasonably well (treat as advisory, not guaranteed)
- Good at maintaining style consistency when given a reference image alongside the prompt
- Handles square format and composition constraints reliably

### Prompt Engineering Tips
- Write prompts as natural English paragraphs, not keyword lists
- Put the most important visual element first (the voxel crab)
- Emotional direction in quotes helps: expression is "I already know the fix"
- Specify "1:1 square" explicitly — don't assume it
- Include color names as primary descriptors, hex codes as parenthetical backup
- Include negative constraints at the end: "No text, no UI, no watermark"
- Front-load the style description (voxel, chunky cubes) to anchor the model before it processes details

### Prompt Rewriting Behavior
ChatGPT rewrites your prompt internally before sending it to the image model. This is not optional and cannot be disabled. Implications:
- Detailed, specific prompts are rewritten less aggressively — the more complete your prompt, the less the rewriter changes
- Vague or short prompts get expanded significantly, often adding unwanted detail
- If the model keeps adding elements you didn't ask for (environments, extra detail), try the anti-rewrite wrapper: "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS:"
- Use this wrapper sparingly — it's a workaround, not a default strategy

### Reference Image Workflow (Recommended)
For character family consistency:
1. Generate the Anchor Crab (neutral, no signifiers) as the first image
2. For each agent variant, upload the Anchor Crab alongside the new prompt
3. Include the instruction: "Use this character as the base. Keep the same voxel style, proportions, and rendering. Apply only the changes described below."
4. If style drifts across generations, prepend "Maintain the exact same voxel art style" to the next prompt

### Common Failures
- **Voxel smoothing**: May render smooth surfaces instead of blocky cubes. Fix: reinforce "chunky visible cubes with faceted edges" — mention it early and prominently.
- **Environment injection**: Adds backgrounds, scenes, or ground planes even when told not to. Fix: "solid matte [color] background" + "no environment" in constraints.
- **Unwanted text/labels**: Sometimes adds text to the image unprompted. Fix: always include "no text" in constraints.
- **Anatomy drift**: Exact counting is unreliable — crab may get wrong number of legs or claws. Fix: regenerate rather than trying to prompt-fix anatomy.
- **Palette drift**: Colors may shift from what was described, especially on sequential generations. Fix: upload a palette swatch reference image for critical color accuracy.

### Length Guidelines
- Target: 80–120 words
- Hard max: 150 words
- Beyond 150 words, the model starts ignoring later constraints and conflating details

---

## Gemini 3 Pro / Nano Banana Pro (Secondary Platform)

### Access
Native image generation inside the Gemini app (web, iOS, Android). Select "Create images" then choose the "Thinking" model for Nano Banana Pro quality (the non-thinking mode uses the base Nano Banana model). Requires a Google One AI Premium or Gemini Advanced subscription. No API.

### Strengths
- Strong at retaining "visual DNA" — palette, texture, composition stay consistent across edits
- Excellent iterative editing: change one element while preserving everything else
- Multi-image composition: can blend multiple reference inputs with clear role assignments
- Spot-color correction without distorting the image structure
- Doodle/draw-to-edit: mark areas on an image to target spatial edits
- Descriptive/narrative prompting outperforms keyword lists

### Prompt Engineering Tips
- Structure prompts as: subject + composition + action/pose + style + constraints
- Prefer descriptive prose over keyword lists
- Specify camera angle, lighting, and aspect ratio explicitly
- Keep prompts concise (~60–100 words) — Gemini responds well to specific, focused direction
- For reference images, always specify the role: "Use this for character style" vs "Use this for color palette"

### Iterative Edit Workflow (Key Differentiator)
Gemini is designed for refinement, not one-shot perfection. The production workflow is:

1. **Generate** the base avatar with a full prompt
2. **Evaluate** against the 7 Anchors checklist
3. **Edit atomically** — one change per edit prompt, using the template:
   "Using the provided image, change only [X] to [Y]. Keep everything else exactly the same."
4. **Correct palette** — use spot-color edits to fix individual colors without regenerating
5. **Use doodle edits** for spatial precision — circle an area and describe the change

### Edit Prompt Templates

Background change:
"Using the provided image, change only the solid background color to [new color]. Keep everything else exactly the same."

Signifier swap:
"Using the provided image, change only the [left/right] claw into [new signifier description]. Keep everything else exactly the same."

Color correction:
"Using the provided image, change only the [accent/shell/eye] color to [new color]. Keep everything else exactly the same."

Expression adjustment:
"Using the provided image, change only the facial expression to [new expression]. Keep everything else exactly the same."

### Doodle Edit Guide
When text descriptions are too imprecise for spatial edits:
- Circle the claw area → request signifier swap
- Circle the forehead → request headgear addition/removal
- Circle the background → request color change
- Draw over shell area → request pattern/texture modification

### Reference Image Best Practices
- Assign clear roles to each uploaded image: style reference, color reference, pose reference
- For palette accuracy, upload a simple swatch image (flat color blocks) alongside the prompt
- The Anchor Crab works as both a style and a proportion reference — specify which role it plays

### Common Failures
- **Complex edit artifacts**: Multi-element changes in one edit can produce glitches. Fix: break into multiple atomic edits.
- **Consistency drift**: After 4–5 sequential edits, cumulative changes can drift from the original. Fix: regenerate from prompt if drift is significant rather than patching.
- **Mechanical detail fidelity**: Thin, intricate signifiers (wire antennas, fine gears) may render poorly. Fix: use bold geometric shapes as signifiers.
- **Aspect ratio changes**: Edits sometimes subtly change the aspect ratio. Fix: always include "Do not change the aspect ratio" in edit prompts.

### Length Guidelines
- Target: 60–100 words for generation prompts
- Hard max: 130 words
- Edit prompts should be 15–30 words — extremely focused
