# Research sources and evidence notes

## Contents

- [Research date](#research-date)
- [Primary official sources](#primary-official-sources)
- [Community and social signals](#community-and-social-signals)
- [How to treat these sources](#how-to-treat-these-sources)
- [Facts carried into this skill](#facts-carried-into-this-skill)

## Research date

Last researched: 2026-05-11.

This skill is based on public OpenAI documentation and community discussions available at research time. Treat official OpenAI product, Help Center, API, and developer documentation as authoritative. Treat forum/social posts as useful reports of edge cases, prompting practices, and workflows, not as guaranteed product behavior.

## Primary official sources

1. OpenAI product announcement, `Introducing ChatGPT Images 2.0`, dated 2026-04-21.
   - URL: https://openai.com/index/introducing-chatgpt-images-2-0/
   - Relevant evidence: OpenAI's example gallery demonstrates ChatGPT Images 2.0 across editorial posters, multilingual text, manga/comics, photorealism, product/brand layouts, academic posters, infographics, educational math proofs, and flexible aspect ratios.

2. ChatGPT Release Notes, `ChatGPT Images 2.0 in ChatGPT`, dated 2026-04-21.
   - URL: https://help.openai.com/en/articles/6825453-chatgpt-release-notes
   - Relevant evidence: ChatGPT Images 2.0 is the new image generation model in ChatGPT, available on all ChatGPT plans. Images with thinking are available on paid plans when selecting Thinking and Pro models.

3. OpenAI developer model page, `GPT Image 2`.
   - URL: https://developers.openai.com/api/docs/models/gpt-image-2
   - Relevant evidence: `gpt-image-2` is the default state-of-the-art image generation model, supports text and image input, outputs images, and has snapshot `gpt-image-2-2026-04-21`.

4. OpenAI API guide, `Image generation`.
   - URL: https://developers.openai.com/api/docs/guides/image-generation
   - Relevant evidence: The API can generate and edit images with GPT Image models, including `gpt-image-2`; Image API is best for single prompt generation/editing, Responses API is best for conversational/multi-turn image experiences. It also documents sizes, quality options, output formats, streaming, limitations, and moderation.

5. OpenAI Cookbook, `GPT Image Generation Models Prompting Guide`, dated 2026-04-21.
   - URL: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
   - Relevant evidence: Prompting fundamentals emphasize structure plus goal, concrete visual details, photorealism cues, iteration, quality selection, and use cases including infographics, translation, photorealism, logos, ads, UI mockups, scientific visuals, diagrams/charts, style transfer, virtual try-on, product mockups, marketing creatives, lighting/weather, object removal, person-in-scene, interiors, merch, and children's book continuity.

6. OpenAI Help Center, `C2PA in ChatGPT Images`.
   - URL: https://help.openai.com/en/articles/8912793-c2pa-in-chatgpt-images
   - Relevant evidence: C2PA is a provenance standard used to embed metadata for verifying media origin and history.

7. OpenAI API reference, `Create image edit`.
   - URL: https://developers.openai.com/api/reference/python/resources/images/methods/edit/
   - Relevant evidence: Image edits can take source images and prompts, support masks, up to 16 images for GPT image models, output format choices, quality choices, partial image streaming, and `gpt-image-2` size constraints. It also states that `gpt-image-2` and its snapshot do not support `background: transparent`.

## Community and social signals

1. OpenAI Developer Community announcement, `Introducing gpt-image-2 - available today in the API and Codex`, dated 2026-04-21.
   - URL: https://community.openai.com/t/introducing-gpt-image-2-available-today-in-the-api-and-codex/1379479
   - Use in this skill: Confirms community-facing announcement language around stronger editing, layouts, text rendering, and instruction following. Also points to early independent leaderboard results; the skill does not rely on those as official quality guarantees.

2. OpenAI Developer Community, `Collection of GPT-image-generator 2.0 issues, bugs, and work-around tips`, opened 2026-04-22.
   - URL: https://community.openai.com/t/collection-of-gpt-image-generator-2-0-issues-bugs-and-work-around-tips-check-first-post/1379535
   - Use in this skill: Treats user reports as troubleshooting leads, especially around technical image-generation failure modes.

3. OpenAI Developer Community, `May 2026 — ChatGPT / API Image Gallery, Prompt Tips, and Help: Generative Art Theme: Science`, opened 2026-04-01.
   - URL: https://community.openai.com/t/may-2026-chatgpt-api-image-gallery-prompt-tips-and-help-generative-art-theme-science/1378298
   - Use in this skill: Provides community prompt examples and emphasizes sharing prompts, vocabulary, science-themed image generation, and iteration.

4. OpenAI Developer Community, `Having trouble getting transparent backgrounds in ChatGPT images`, opened 2026-05-01.
   - URL: https://community.openai.com/t/having-trouble-getting-transparent-backgrounds-in-chatgpt-images/1380143
   - Use in this skill: Reinforces a practical caveat: users report unreliable true alpha transparency in ChatGPT UI. The authoritative basis remains the API documentation stating `gpt-image-2` does not support transparent backgrounds.

## How to treat these sources

- Official documentation beats community reports when they conflict.
- Community reports are useful for prompting caveats, test ideas, and troubleshooting warnings.
- Do not present leaderboard claims, forum experiments, or social posts as guaranteed performance.
- If a future release changes model names, parameter behavior, transparency support, or safety policy, update this file and `model-and-workflow.md` first.

## Facts carried into this skill

- ChatGPT Images 2.0 was introduced on 2026-04-21 and was described in ChatGPT release notes as available on all ChatGPT plans.
- Images with thinking are available on paid ChatGPT plans when using Thinking and Pro models.
- `gpt-image-2` is the recommended default for new GPT Image API workflows at research time.
- `gpt-image-2` supports flexible sizes within constraints, quality levels `low`, `medium`, `high`, and image generation/editing workflows.
- For GPT Image 2, true transparent background should not be promised; use opaque backgrounds plus downstream removal or a supported fallback workflow.
- Image generation remains imperfect for exact text placement, character/brand consistency, and precise composition, so high-stakes outputs need inspection and iteration.
