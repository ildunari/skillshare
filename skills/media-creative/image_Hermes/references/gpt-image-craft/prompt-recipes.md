# Prompt recipes

## Contents

- [How to use these recipes](#how-to-use-these-recipes)
- [Education and science](#education-and-science)
- [Charts and information design](#charts-and-information-design)
- [Realism and photography](#realism-and-photography)
- [Marketing and design](#marketing-and-design)
- [Games, icons, and small assets](#games-icons-and-small-assets)
- [Illustration, comics, and characters](#illustration-comics-and-characters)
- [Editing and transformation](#editing-and-transformation)
- [Prompt remix patterns](#prompt-remix-patterns)

## How to use these recipes

Treat each recipe as a starting point. Replace bracketed fields, delete irrelevant details, and keep the final prompt focused. Add exact copy, labels, data, or preservation constraints only when they matter. For API use, pair the prompt with model, size, quality, and format settings.

When the user asks for multiple variants, vary only one or two dimensions per batch. For example, test three lighting treatments while keeping the subject, layout, and text constant. This makes iteration readable instead of random.

## Education and science

### 1. Scientific textbook figure

```text
Goal: Create a scientific textbook figure for [audience level].
Canvas: Landscape 1536x1024, white background, print-readable.
Subject: [process/system/anatomy/device].
Visual system: clean flat scientific illustration, muted academic palette, consistent stroke weight, readable sans-serif labels.
Composition: [left-to-right flow / cutaway / labeled cross-section / 3-panel comparison].
Required content: Title "[exact title]". Labels: [label list].
Accuracy constraints: show only [required structures]; omit [known confusers]; use arrows only for [causal flow/movement].
Quality bar: clear enough for a textbook page, no decorative clutter, no tiny labels.
```

Use for biology, chemistry, physics, engineering, medicine, geology, and classroom explainers. Add a factual warning if the user has not supplied enough domain detail for accuracy.

### 2. Academic paper figure concept

```text
Goal: Visual concept for a journal-style Figure [number], not final data visualization.
Canvas: 1536x1024, white background, 3 panels labeled A, B, C.
Panel A: [experimental setup or schematic].
Panel B: [conceptual mechanism].
Panel C: [expected qualitative trend, not exact data].
Style: restrained academic vector figure, thin lines, neutral palette, publication-style typography.
Constraints: no invented numerical values, no unsupported claims, no fake p-values, no fabricated author names.
```

Use when the figure is conceptual. For exact plots, generate the chart with code and only use image generation for a surrounding explanatory illustration.

### 3. Medical or anatomical plate

```text
Goal: Educational anatomical plate for [students/patient handout/public audience].
Canvas: Portrait 1024x1536, white background.
Subject: [organ/system/procedure] shown as [cutaway/anterior view/comparison].
Visual system: precise medical illustration, muted anatomical colors, clean leader lines, non-gory educational presentation.
Required labels: [exact label list].
Constraints: avoid diagnosis, avoid treatment instructions, avoid alarming gore, no extra labels.
```

### 4. Whiteboard explainer

```text
Create a clear whiteboard-style teaching diagram explaining [topic].
Use hand-drawn marker lines, simple arrows, three numbered steps, and concise labels.
Canvas: 16:9 landscape.
Exact text to include: "[title]", "1. [step]", "2. [step]", "3. [step]".
Keep the board uncluttered, high contrast, and readable from a classroom projector.
```

## Charts and information design

### 5. Exact chart handoff

```text
Do not invent the chart. First create the chart from this data using code or a charting tool: [data/table].
Then create an image prompt for a styled frame around the completed chart:
Goal: [audience and message].
Canvas: [size].
Use the supplied chart image as the central object. Preserve all data, labels, ticks, colors, and line positions exactly.
Add surrounding visual context: [headline/callouts/background/brand treatment].
Constraints: no changes to plotted values, no new axis labels, no fake source notes.
```

This recipe keeps numeric truth outside the image model and uses image generation only for art direction.

### 6. Infographic poster

```text
Goal: Create an infographic poster for [audience] explaining [topic].
Canvas: Portrait 1024x1536.
Structure: title at top, 5 content blocks, one central hero diagram, small footer note.
Visual system: modern editorial infographic, flat icons, limited palette, readable hierarchy, generous margins.
Exact text: Title "[title]". Section headings: [headings].
Required visuals: [icons/diagram/map/timeline].
Constraints: use short labels, no paragraphs, no fake statistics, no extra claims beyond supplied facts.
```

### 7. Dashboard-style hero image

```text
Create a high-fidelity analytics dashboard hero image for [product/use case].
Canvas: 16:9 landscape 2048x1152.
Visual system: modern SaaS dashboard, polished UI, realistic cards, charts, filters, sidebar navigation.
Content: dashboard title "[exact title]"; cards for [metric names]; charts showing plausible but unlabeled illustrative trends.
Composition: browser window mockup centered on a clean gradient or office background.
Constraints: if numbers are shown, mark them as illustrative; no impossible chart scales; no clutter.
```

### 8. Timeline or roadmap graphic

```text
Goal: Create a [timeline/roadmap] graphic for [topic].
Canvas: Landscape 1536x1024.
Layout: horizontal timeline with [number] milestones.
Milestones: [date/title list].
Visual style: clean editorial timeline, icons per milestone, consistent spacing, high legibility.
Constraints: preserve dates exactly, no extra milestones, no tiny footnotes.
```

### 9. Map or wayfinding graphic

```text
Goal: Create a wayfinding-style map for [place/system], conceptual not navigationally exact unless a verified map is supplied.
Canvas: [size].
Visual system: accessible transit-map clarity, color-coded zones, clear symbols, large labels.
Required labels: [label list].
Constraints: do not fabricate exact geography; label as conceptual if not based on source map; no decorative clutter.
```

## Realism and photography

### 10. Photorealistic everyday scene

```text
Create a photorealistic image of [subject/action] in [setting].
Camera: natural eye-level composition, [lens/focal length if known], realistic depth of field.
Lighting: [window light/overcast daylight/direct flash/golden hour], physically plausible shadows.
Details: ordinary imperfections, believable materials, natural color, no over-polished CGI look.
Constraints: no extra fingers, no warped objects, no text unless specified, no watermark.
```

### 11. Candid flash photo

```text
Create a candid direct-flash photo of [subject] at [event/location].
Style: imperfect snapshot, natural expression, slight motion or framing imperfection, realistic skin texture, visible flash falloff.
Lighting: direct on-camera flash with darkened background.
Composition: [close-up / waist-up / group shot], casual and believable.
Constraints: no glamour retouching, no surreal lighting, no studio backdrop.
```

### 12. Product hero photo

```text
Create a premium product hero photo for [product].
Canvas: [size], [background].
Product: [shape/material/color/key features].
Lighting: controlled studio softbox, crisp edge highlights, realistic contact shadow.
Composition: product centered or rule-of-thirds, enough negative space for copy on [side].
Constraints: preserve label text exactly if supplied; no invented brand marks; no distorted geometry.
```

### 13. Interior design visualization

```text
Create a photorealistic interior design visualization of [room].
Style: [modern warm minimalist / Japandi / industrial / luxury hospitality].
Architecture: [room size, windows, flooring, fixed features].
Furniture and decor: [list].
Lighting: [time of day], realistic shadows, natural materials.
Constraints: keep layout plausible, no floating furniture, no impossible reflections, no extra rooms.
```

### 14. Cinematic still

```text
Create a cinematic still from an original [genre] film.
Scene: [character/action/location].
Camera: [shot type], [lens feel], intentional framing.
Lighting: [noir/neon/practical lamp/moonlight], strong mood but physically believable.
Color grade: [palette].
Constraints: original characters only, no existing film franchise, no text, no poster credits.
```

## Marketing and design

### 15. Social mini-thumbnail

```text
Goal: Create a thumbnail image for [platform] about [topic].
Canvas: [16:9 1536x864 / square 1024x1024 / 9:16 1024x1536].
Composition: one bold focal image, 3 to 5-word headline, high contrast, readable at phone size.
Exact headline: "[headline]".
Visual system: [style], large shapes, clean negative space, no tiny details.
Constraints: no extra text, no misleading clickbait, no clutter near edges.
```

### 16. Ad campaign concept

```text
Create a polished ad concept for [brand/product/category].
Audience: [audience].
Message: [single promise].
Canvas: [billboard/poster/social/ad].
Scene: [setting and subject].
Exact copy: "[headline]" and optional subhead "[subhead]".
Art direction: [premium/minimal/playful/editorial/streetwear/etc.].
Constraints: original brand only, no existing logos, no watermark, no extra copy.
```

### 17. Logo direction board

```text
Create a logo direction board for an original brand called [name].
Canvas: 1536x1024.
Include: three distinct logo directions, each with a mark, wordmark, palette chips, and one-sentence visual rationale.
Brand attributes: [attributes].
Constraints: original design, no imitation of existing logos, clear scalable marks, minimal mockup noise.
```

For production logos, generate concepts, then rebuild the final vector manually.

### 18. UI mockup

```text
Create a high-fidelity UI mockup for [app/product].
Canvas: [desktop 1536x1024 / mobile 1024x1536].
Screen: [specific screen].
Visual system: modern product design, accessible contrast, consistent spacing, realistic components.
Exact UI labels: [label list].
Content hierarchy: [primary action, cards, navigation, empty states].
Constraints: no lorem ipsum, no unreadable microtext, no impossible controls.
```

### 19. Pitch-slide hero visual

```text
Create a polished 16:9 hero visual for a pitch deck slide about [topic].
Canvas: 2048x1152.
Composition: left side reserved for title text, right side visual metaphor [subject].
Style: [enterprise SaaS / climate tech / biotech / fintech], premium but not generic.
Exact title placeholder: "[title]".
Constraints: no dense text, no fake logos, no chart data unless provided.
```

## Games, icons, and small assets

### 20. Sprite sheet

```text
Create a sprite sheet for an original [character/object].
Canvas: square 1024x1024.
Grid: [columns] x [rows], equal cells, one centered sprite per cell.
Poses/actions: [list].
Style: [pixel art/hand-painted/cartoon/low-poly render], crisp silhouette, limited palette.
Technical constraints: plain solid background for extraction, no anti-aliasing if pixel art, no blur, no text, no shadows crossing cells.
```

### 21. Isometric game asset

```text
Create an isometric game asset of [object/building/tile].
Canvas: square 1024x1024, centered asset, plain background.
Style: [cozy farming sim / low-poly / detailed fantasy / sci-fi modular].
View: 3/4 isometric, consistent top-left light source.
Constraints: readable silhouette, no UI, no text, no cropped edges, extraction-friendly background.
```

### 22. Icon set

```text
Create a cohesive icon set for [domain].
Canvas: 1536x1024 with a grid of [number] icons.
Icon subjects: [list].
Style: simple vector-like icons, consistent stroke width, limited palette, rounded geometry.
Constraints: no text, no tiny decoration, each icon readable at 32px, equal visual weight.
```

### 23. Sticker sheet

```text
Create a sticker sheet of [theme/character].
Canvas: square 1024x1024.
Include [number] stickers, each separated with space, bold white sticker border, playful expressions.
Constraints: no overlapping stickers, no text unless specified, extraction-friendly plain background.
```

## Illustration, comics, and characters

### 24. Character reference sheet

```text
Create a character reference sheet for an original character named [name].
Canvas: landscape 1536x1024.
Include: front view, side view, back view, three expressions, two prop callouts, palette swatches.
Character details: [age range, body type, clothing, colors, personality cues].
Style: clean concept-art reference sheet, consistent proportions, readable notes.
Constraints: original character, no existing IP, no extra text beyond labels.
```

### 25. Comic page

```text
Create a comic page for an original story.
Canvas: portrait 1024x1536.
Layout: [number] panels with clear gutters.
Scene summary: [story beats per panel].
Style: [indie comic / manga / pulp / European album], consistent characters, expressive acting.
Text: either no speech bubbles, or use only these exact short lines: [lines].
Constraints: no unreadable bubbles, no extra dialogue, no copied characters.
```

### 26. Storyboard sheet

```text
Create a storyboard sheet for [scene].
Canvas: landscape 1536x1024.
Layout: 6 panels in a 3x2 grid.
Each panel: simple grayscale sketch, clear camera angle, action readable.
Panel beats: [list].
Labels: panel numbers only unless user supplies captions.
Constraints: no polished final art; prioritize composition and action clarity.
```

### 27. Children's book spread

```text
Create a children's picture-book spread about [scene].
Canvas: landscape 1536x1024.
Style: warm watercolor and pencil texture, gentle expressions, soft paper grain.
Composition: leave a clear text-safe area on [left/right/top].
Characters: [description].
Constraints: no scary details, no extra text, no copied book characters.
```

## Editing and transformation

### 28. Object edit with preservation locks

```text
Edit the supplied image.
Allowed change: [exact change].
Preserve unchanged: camera angle, lighting, background, subject identity, clothing, pose, product label, geometry, and all other objects.
Visual match: the new/changed object should match scene perspective, shadows, material texture, and color temperature.
Constraints: do not restyle the whole image, do not add unrelated objects, do not change text unless requested.
```

### 29. Product extraction / ecommerce cleanup

```text
Edit the supplied product photo for ecommerce use.
Goal: clean centered product image on [white/light gray/brand-color] background.
Preserve: exact product geometry, label text, color, material finish, proportions.
Improve: remove dust, improve lighting, add realistic soft contact shadow.
Constraints: no label rewriting, no invented accessories, no transparent background promise for gpt-image-2.
```

### 30. Style transfer without identity drift

```text
Transform the supplied image into [target style].
Preserve: subject identity, pose, facial features, clothing silhouette, composition, and key objects.
Change only: rendering medium, color palette, texture, and lighting style.
Constraints: no new people, no changed facial structure, no extra text, no background replacement unless requested.
```

### 31. Before/after comparison

```text
Create a before-and-after comparison image showing [change].
Canvas: landscape 1536x1024 split into two equal panels.
Left panel: before state. Right panel: after state.
Use matching camera angle, scale, lighting, and object positions so the difference is easy to compare.
Labels: "Before" and "After" only.
Constraints: do not exaggerate beyond the requested change, no extra claims.
```

## Prompt remix patterns

Use these compact remixes when the user wants alternatives:

- **Cleaner:** reduce background objects, simplify palette, increase margins, use one focal subject.
- **More premium:** warmer controlled lighting, refined materials, subtle texture, less copy, stronger negative space.
- **More scientific:** white background, numbered labels, consistent stroke weight, restrained palette, fewer decorative elements.
- **More social-thumbnail:** larger headline, bigger focal object, stronger contrast, less detail, phone-size readability.
- **More realistic:** natural lens, everyday imperfections, plausible lighting, less cinematic grading, no CGI gloss.
- **More playful:** rounder forms, brighter palette, expressive posture, charming props, soft shadows.
- **More game-ready:** clear silhouette, extraction-friendly background, consistent light source, no overlapping elements.
- **More print-ready:** margins, hierarchy, restrained palette, no tiny text, exact copy, safe areas.
