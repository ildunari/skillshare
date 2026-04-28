---
name: gpt-image-2-uiux-prompting
description: Use before generating or editing UI/UX images with GPT Image 2, OpenAI image generation, Hermes image_generate, or Codex image generation. Especially use for mobile app mockups, iOS screenshots, Liquid Glass concepts, composer/input-bar designs, design directions, or when prior image outputs look stretched, poster-like, weird, overstuffed, duplicated, or non-native. Guides the agent to think like a product designer and write realistic shipped-app screenshot prompts instead of vague concept-art prompts.
version: 0.1.0
author: Hermes Agent
license: MIT
---

# GPT Image 2 UI/UX Prompting

Use this skill before calling image generation for UI/UX work. The goal is to get images that look like believable shipped product screenshots, not AI concept posters.

This skill is especially important for:
- mobile app UI mockups
- iOS 26 / Liquid Glass concepts
- chat composers, input bars, nav chrome, sheets, popovers, toolbars
- generating multiple distinct design directions
- fixing failures like stretched UI, warped phones, poster/collage layouts, duplicate controls, unreadable tiny text, or sci-fi glass

## Core rule

Prompt the image model as if you are art-directing a real app screenshot.

Bad:
```text
Create 10 futuristic Liquid Glass composer concepts.
```

Better:
```text
Generate one straight-on iPhone portrait screenshot of a native iOS chat screen. The screen should look like a real shipped app, with practical hierarchy, safe-area spacing, SF Pro-like typography, and a compact Liquid Glass composer anchored above the home indicator.
```

Words like “concept,” “futuristic,” “cinematic,” “beautiful,” “award-winning,” and “ultra detailed” often pull the model toward poster art. Prefer “realistic screenshot,” “native iOS,” “production UI,” “practical,” “content-first,” and “shipped app.”

## Prompt structure

Use labeled sections. Keep the prompt specific but not bloated.

```text
Generate one realistic mobile UI screenshot.

Device / canvas:
- One straight-on iPhone portrait screenshot, normal iPhone proportions.
- Full-screen app UI only. No floating device render, collage, contact sheet, or design-board presentation.

Product intent:
- [One sentence: what this screen helps the user do.]

Screen state:
- [Specific screen and state, e.g. “chat screen with composer active and one approval pending.”]

Layout:
- [Top nav, content area, bottom composer/sheet/popover.]
- Use native iOS safe areas, 8pt spacing rhythm, realistic touch targets, and aligned controls.

Visual style:
- Native Apple iOS, SF Pro-like typography, light/dark mode as specified.
- Restrained Liquid Glass only on [composer / toolbar / sheet / popover].
- Subtle translucency, blur, faint refraction, and high contrast text.

Exact visible text:
- [Short required labels only.]
- No other decorative text.

Constraints:
- No stretched UI, no warped phone, no perspective tilt, no poster composition.
- No duplicate controls, no random extra toolbars, no redundant model pickers.
- No neon sci-fi glass, fake logos, app-store badges, watermarks, annotations, or callouts.
```

## Canvas and proportion rules

For a single mobile screen:
- Use portrait, never square or landscape.
- Ask for a straight-on screenshot, not an angled phone mockup.
- If the tool only exposes `portrait`, explicitly say “normal iPhone proportions” and “not stretched.”
- For individual concepts, generate one image per concept. Do not ask for a contact sheet unless the user explicitly wants one.

For component-only interaction specs:
- Use landscape when the image should show a spec sheet of several states/frames.
- Ask for “composer-only UI component,” “neutral canvas,” “no phone frame,” “no full chat screen,” and “same composer design across all frames.”
- If the user wants multiple actions per composer, produce one image per composer design with 1–5 frames inside that image. Do not produce one image per state.
- Label frames lightly, e.g. “Idle”, “Slash”, “Pick”, “Committed”; avoid giant annotations that dominate the UI.

Useful wording:
```text
Use a single tall iPhone portrait canvas with normal iPhone proportions. The UI fills the screen naturally. Do not stretch, skew, bend, tilt, widen, or fisheye the interface. Show a straight-on screenshot, not a 3D device render.
```

## Liquid Glass guidance

Apple’s Liquid Glass works best when it supports hierarchy, not when everything is glass.

Use wording like:
```text
Use Liquid Glass sparingly as a functional material for the bottom composer and small floating controls. It should have subtle translucency, soft background blur, faint refraction, and a little reflected background color. Do not make every content card glass. Do not use neon glow, holograms, chrome bubbles, or abstract glass shards.
```

Good cues:
- translucent material
- soft blur
- faint refraction
- native toolbar/tab/composer surfaces
- restrained tint
- content remains readable

Bad cues:
- glass everywhere
- heavy reflections
- neon glow
- sci-fi holograms
- illegible transparent text
- floating shards or decorative blobs

## Component inventory discipline

Define exactly what may appear. This prevents duplicate model pickers, extra tool rows, and random controls.

Example for a chat composer:
```text
Composer inventory:
- One mode selector: “Explore”, “Plan”, “Edit”
- One text input with placeholder “Ask Craft…”
- One consolidated “+” menu button
- One purple send button
- Optional compact status/approval chip only when active

Do not include a model picker in the composer; the model picker is already in the top nav. Do not expose attach/tools/actions as separate permanent buttons; they live behind the + menu.
```

If the screen already has a control elsewhere, say so explicitly:
```text
Top nav already contains the model picker. The composer must not include model, context, or workspace controls.
```

## Text rules

UI image models still struggle with dense text. Keep exact text short.

Good:
```text
Exact visible text:
- Top model pill: “Sonnet 4.6”
- Composer placeholder: “Ask Craft…”
- Mode labels: “Explore”, “Plan”, “Edit”
- Status chip: “1 approval”
```

Avoid paragraphs of readable UI copy. Use blurred/representative chat content if content is not the focus.

## Negative constraints block

Include a short “Avoid” block when quality matters:

```text
Avoid:
- stretched or warped UI
- tilted phone mockup
- poster layout
- multiple screens or side-by-side variants
- duplicate controls
- redundant model pickers
- exposed individual tool buttons when a + menu is specified
- extra toolbars
- dense unreadable text
- neon sci-fi glass
- fake logos, badges, watermarks, annotations, or callout labels
- Android-style navigation for iOS work
```

## Iteration workflow

1. Generate a small batch only after the structure is well specified.
2. Judge structure before taste:
   - Is it a real straight-on screenshot?
   - Are proportions normal?
   - Is there exactly one concept?
   - Are controls duplicated?
   - Is Liquid Glass restrained and functional?
3. If structure is wrong, regenerate with stronger structural constraints. Do not tweak color first.
4. If close, edit one thing at a time:
   ```text
   Edit the previous image. Change only the bottom composer: make it 20% shorter and remove the duplicate model picker. Keep the same screen, camera angle, typography, colors, and iPhone proportions.
   ```
5. Repeat preservation constraints on every edit.
6. Use higher quality only after layout is good.

## Bulk generation with Codex app-server parallelism

Codex's built-in image generation uses `gpt-image-2` and counts against general Codex usage limits. It is fast and included in Codex usage, but a single Codex agent generates images serially, so large batches are slow if one agent does all the work.

When the user asks for many independent images and the prompt is already mostly fixed, parallelize across multiple Codex app-server agents instead of asking one Codex session to produce the whole batch.

Use this workflow:

1. First use one agent to refine the master prompt and generate 2–4 samples. Do not fan out until the structural prompt is good.
2. Put the final prompt template and per-image variables in a CSV or JSONL file. Include fields like `id`, `title`, `screen_state`, `layout_variant`, `style_notes`, and `output_path`.
3. Ask Codex to run multiple app-server workers over that input file, with each worker responsible for a shard of rows and each row producing one image. Phrase it explicitly, e.g.:
   ```text
   Generate the images described in prompts.csv using 16 Codex app-server workers. Each worker should process a non-overlapping shard, generate one image per row, save to the row's output_path, and write a manifest with prompt, status, image path, and error if any.
   ```
4. If the per-row prompt needs little reasoning, tell Codex to use a cheaper/faster low-reasoning worker model where available, for example “use a mini model with low reasoning for the app-server workers; the prompt is fixed and workers should not redesign it.”
5. Cap concurrency deliberately. Start with 8–16 workers for normal UI batches; only go higher after a small run succeeds. Very high concurrency can fail or stall depending on local limits, Codex limits, and image backend availability.
6. Make failures bounded: each row gets at most 1–2 retries, then records the error and moves on. Do not let a stuck image block the whole batch.
7. After the batch, inspect the manifest and regenerate only failed or structurally bad rows. Do not rerun the whole batch unless the master prompt itself changed.

Keep the normal UI quality constraints from this skill in every per-row prompt. Parallelism speeds up throughput; it does not fix bad prompting.

Notes from the source discussion:
- Codex image generation is `gpt-image-2` through Codex, not the standalone image API.
- Codex image generation was described by OpenAI docs as using included limits roughly 3–5x faster on average than similar turns without image generation, depending on quality and size.
- Codex image generation appears limited to about 1K output in this path; use the standalone API if a task truly needs higher-resolution outputs.
- If parallel image calls fail, prefer bounded retry / manifest logging over infinite retries.

## Practical templates

### Single iOS UI screenshot
```text
Generate one realistic iPhone portrait screenshot of a native iOS app.

Product intent:
[Job to be done.]

Screen state:
[Specific screen and state.]

Layout:
Top safe-area navigation, content area, and bottom [composer/sheet/toolbar]. Use native iOS spacing, safe areas, aligned controls, and SF Pro-like typography.

Visual style:
Modern Apple iOS with restrained Liquid Glass only on [specific surfaces]. Soft blur, faint refraction, subtle tint, high text contrast.

Exact visible text:
[Short required labels.]

Constraints:
Straight-on screenshot with normal iPhone proportions. No perspective tilt, no stretched UI, no poster/collage, no multiple screens, no duplicate controls, no extra text, no fake logos, no watermarks.
```

### Craft Companion composer concept
```text
Generate one realistic iPhone portrait screenshot of Craft Companion’s chat screen.

Context:
The top navigation already has the model picker, so the composer must not include model, workspace, or context controls.

UX intent:
The composer should feel calm, native, and powerful without exposing too many controls.

Composer inventory:
- Explore / Plan / Edit mode selector
- text input with placeholder “Ask Craft…”
- one consolidated + menu button
- one purple sparkle send button
- optional compact approval/status chip only when active

Layout:
The composer is compact and anchored above the home indicator. Normal iPhone proportions, realistic touch targets, safe-area spacing. Chat content remains visible above it.

Visual style:
Native iOS 26 Liquid Glass, subtle translucent composer surface, soft blur, faint refraction, restrained purple accent, light mode, SF Pro-like typography.

Avoid:
stretched UI, poster layout, duplicate controls, model picker in composer, exposed attach/tools buttons, extra toolbars, dense text, neon sci-fi glass, fake logos, annotations, multiple screens.
```

## References

- OpenAI Academy: Creating images with ChatGPT — https://openai.com/academy/image-generation
- OpenAI image generation docs — https://platform.openai.com/docs/guides/tools-image-generation/
- OpenAI Cookbook image prompting guide — https://cookbook.openai.com/examples/multimodal/image-gen-1.5-prompting_guide
- Apple Liquid Glass overview — https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- Apple adopting Liquid Glass — https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- Apple applying Liquid Glass to custom views — https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views
