---
name: kosta-contextual-voice_KM
description: >-
  Use when drafting or revising messages in Kosta's contextual voice: school/lab emails, official/admin emails, personal logistics emails, direct texts, or group texts. Also use when the user asks to make a draft sound more like Kosta without changing facts. Do not use for long essays, scientific prose, legal advice, or sending anything without confirmation.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
---
# Kosta Contextual Voice

Draft messages in Kosta's voice by matching the channel and relationship first. Preserve facts and intent more strongly than style. If the user has not provided enough information for a sendable message, ask one compact clarification instead of inventing details.

## Pick the register

- **School/lab email**: advisors, lab members, university staff, vendors in research context, training, shipping, purchasing, experiments. Friendly-professional, practical, enough operational detail to avoid back-and-forth.
- **Official/admin email**: medical offices, immigration/visa, legal/data, financial/admin services, unknown institutional offices. Plain, factual, slightly more formal, restrained warmth.
- **Personal logistics email**: non-Brown scheduling, shipments, forms, services, consumer/business contacts. Casual-professional, brief, cooperative.
- **Direct text**: one-on-one iMessage/SMS/RCS. Short, fragment-friendly, immediate, no email ceremony.
- **Group text**: shared update or coordination. Short and safe; less intimate, less teasing, less shorthand than direct texts.

## Email voice

Kosta's email style is practical, warm, and low-ceremony. Usually: simple greeting, one compact body paragraph with the reason/context/ask, then compact thanks/signature. Split into multiple paragraphs only when several operational details genuinely need separation. Use fuller structure for cold, official, or detail-heavy messages; use shorter thread-style replies when the context and ask are simple. For announcements or updates where no favor is being asked, do not force a request-style closing; end cleanly with the next step, compact thanks, or `-Kosta`.

Keep the voice plain and slightly conversational. Prefer direct coordination language over perfectly smoothed assistant prose, especially for lab, school, and personal-business logistics. Before returning an email, do a light naturalness pass: remove over-balanced clauses, broad extra offers, and helper phrases that make it sound like an assistant cleaned it up.

Default patterns:

```text
Hi [Name],

[Brief context]. [Constraint or what was already tried]. Would you be able to [specific ask]?

Thank you!
-Kosta
```

```text
Hi [Name],

I just wanted to check [status/requirement]. I [already did/noticed/am scheduled for] [specific detail], so I think [current understanding]. Let me know if I need to [next action].

Thank you!
-Kosta
```

For official/admin messages to an office rather than a known person, prefer `Dear [Office],` or `Hi [Office],` only when that office/team is actually named as the addressee. Choose greeting and close by stakes: use `Dear [Office/Title],` and `Sincerely, Kosta Milovanovic` for higher-stakes or clearly formal handling; for routine record checks or simple admin follow-up, `Hi [Office],` with `Thank you!` and `-Kosta` is enough. For normal lab/school emails, prefer `Hi` and `-Kosta`. If no recipient is identifiable, use `Hi,` or a natural generic team phrase only if it would sound sendable; do not invent stiff placeholders like `Hi Professor`, `Hi Scheduling Office`, or treat a department/category label as a person.

Use calibrated uncertainty when appropriate: `I think`, `not sure if`, `probably`, `if needed`, `in case`. Do not fake confidence. For official/admin messages, stay factual without becoming legalistic or template-like; use plain chronology, one compact ask, and one close. Use one short privacy/safety constraint when needed, but do not stack boilerplate or repeat `let me know` when the facts are simple. `I wanted to check` and `please let me know if...` often sound more natural than institutional wording. For personal logistics emails, keep a little conversational roughness: fewer perfectly balanced clauses, avoid polished punctuation such as em dashes by default, and use a short close or no close when the thread is obviously casual. Once the ask or next step is clear, stop instead of adding a second polite closing sentence.

## Text voice

Texts should usually be much shorter than emails. Most direct texts are fragments, not polished paragraphs. Do not add greetings, signoffs, bullets, markdown, or email phrases.

Good text shapes:

- `yeah that works`
- `ok perfect I can send it later`
- `no worries you're good`
- `I think it should be fine but let me check`
- `can you send me the address again?`

Use punctuation lightly. Questions get `?`; short statements often have no final period. Prefer commas, fragments, line breaks, or no punctuation over em dashes; for longer direct texts, two snapped-off clauses usually sound more natural than one polished sentence. Reserve em dashes for occasional longer explanatory texts. Bias toward lowercase fragments and sparse punctuation when constraints allow it; avoid making coordination texts look like polished two-sentence messages. Start aggressively short, then add only facts the prompt requires; labmate or work texts should still read as texts, not miniature status reports. Emoji, exclamation marks, `u/ur`, profanity, teasing, and Serbian/Balkan Latin-script are relationship-specific — use them only when the prompt makes that context clear.

Before returning a direct or group text, do a compression pass: if it is short, remove greetings, signoffs, markdown, excess politeness, filler setup, and most terminal punctuation unless it is a real question.

For group texts, be safer and more general: one compact context sentence, the update/ask, and the next step. Keep shared asks casual and direct; prefer `can everyone check...` or `try not to...` over email-courtesy phrasing. Do not make group texts sound like intimate one-on-one banter. If several facts are required, prefer short sentence breaks or dropped helper words over one long comma-chained sentence.

## What to preserve

Always preserve:

- names, dates, times, amounts, room numbers, attachments, IDs, deadlines, and exact constraints supplied by the user;
- the user's intended ask/update/refusal/apology;
- the stakes and relationship;
- uncertainty when the user is uncertain.

Never invent official details, diagnoses, medications, legal/visa facts, addresses, phone numbers, case numbers, deadlines, or private background.

## Anti-patterns

Avoid:

- `I hope this message finds you well`, `circling back`, `touch base`, generic customer-support voice, and corporate filler;
- assistant-polish phrases like `I'd be happy to`, `comprehensive`, and broad `anything else` add-ons unless the user explicitly wants that tone;
- over-apologizing or groveling when a simple acknowledgement works;
- hiding the actual ask under social padding;
- making every message perfectly polished;
- stacking multiple polite closers after the ask is already clear;
- excessive bullets for a simple email;
- exclamation-heavy warmth or forced enthusiasm;
- turning texts into emails;
- importing intimate shorthand or jokes into professional contexts.

Output only the message draft unless the user asks for alternatives or explanation.
