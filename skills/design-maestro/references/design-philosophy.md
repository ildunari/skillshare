# Design Philosophy

> Conditionally loaded for from-scratch builds and full design explorations. Contains the intent-first process, domain exploration framework, component checkpoint, and self-critique protocol.

---

## Intent First

Before touching code, answer three questions with specifics — not generic labels.

1. **Who is this person?** Not "users." Where are they, what's on their mind, what did they do 5 minutes ago? A teacher at 7am with coffee shapes a different interface than a developer debugging at midnight.

2. **What must they accomplish?** The verb. Grade submissions. Find the broken deployment. Approve the payment. This determines what leads, what follows, what hides.

3. **What should this feel like?** "Clean and modern" is not an answer. Warm like a notebook? Cold like a terminal? Dense like a trading floor? Calm like a reading app? The answer shapes color, type, spacing, density.

If you can't answer these with specifics, ask the user. When context is sufficient, infer and state your assumptions in the component checkpoint.

### Every choice needs a reason

For layout, color temperature, typeface, spacing scale, and information hierarchy — be able to explain why this choice and not another. "It's common" or "it works" means you picked a default, not made a decision.

**The swap test:** If you replaced your choices with the most common alternatives and the design didn't feel meaningfully different, the choices weren't real.

### Intent must be systemic

Intent is a constraint that shapes every decision, not a label you apply once. If the intent is warm: surfaces, text, borders, accents, semantic colors, typography — all warm. If the intent is dense: spacing, type size, information architecture — all dense. Check your output against your stated intent — every token should reinforce it.

---

## Product Domain Exploration

Run this for from-scratch builds. Skip for iterations, minor edits, and builds where the user has already specified direction.

The path to crafted output: Task type → Product domain → Signature → Structure + Expression. The path to generic output: Task type → Visual template → Theme.

### Four required outputs (produce all four before proposing direction)

**Domain:** Concepts, metaphors, vocabulary from this product's world. Not features — territory. Minimum 5.

**Color world:** What colors exist naturally in this product's domain? If this product were a physical space, what would you see? What colors belong there that don't belong elsewhere? List 5+.

**Signature:** One element — visual, structural, or interaction — that could only exist for this product. If you can't name one, keep exploring.

**Defaults to reject:** 3 obvious choices for this interface type — visual and structural. Name what the template would do so you can deliberately choose something else.

### Proposal requirements

Your direction must explicitly reference all four outputs: domain concepts, colors from your color world, your signature element, and what replaces each rejected default.

**The identity test:** Read your proposal, remove the product name. Could someone identify what this is for? If not, explore deeper.

---

## Component Checkpoint

Run when starting a new component or changing design direction — not on every minor edit.

```
Intent: [who is this person, what must they do, how should it feel]
Palette: [colors from your exploration — why they fit this product's world]
Depth: [borders / shadows / layered — why this fits the intent]
Surfaces: [your elevation scale — why this color temperature]
Typography: [your typeface — why it fits the intent]
Spacing: [your base unit]
```

Connect every technical choice back to intent. If you can't explain why for a choice, reconsider it.

---

## Self-Critique Protocol

Run silently before presenting. Apply fixes directly — report findings only when they changed something the user would have expected differently.

### Four checks

- **The swap test:** If you swapped the typeface for your usual one, would anyone notice? If you swapped the layout for a standard template, would it feel different? Places where swapping wouldn't matter are places you defaulted.

- **The squint test:** Can you still perceive hierarchy with blurred eyes? Is anything jumping out harshly? Craft whispers.

- **The signature test:** Can you point to five specific elements where your signature appears? Not "the overall feel" — actual components.

- **The token test:** Do your CSS variable names sound like they belong to this product's world, or could they belong to any project?

If any check fails, iterate before showing.

### Post-build critique

Review as a design lead:

- **Composition:** Does the layout have rhythm? Dense areas giving way to open content?
- **Proportions:** Do your proportions declare what matters? (280px sidebar = "navigation serves content"; 360px = "these are peers")
- **Focal point:** Does the primary action dominate through size, position, contrast, or surrounding space?
- **Surface independence:** Remove every border mentally — can you still perceive structure through surface color alone?
- **Content coherence:** Could a real person at a real company be looking at exactly this data right now?
- **Structure honesty:** Any negative margins, `calc()` workarounds, or absolute positioning escaping layout flow? The correct answer is simpler than the hack.

---

## Where Defaults Hide — Quick Reference

Design decisions that feel structural but aren't:

- **Typography** — not a container. The weight, personality, and texture of type IS the design. A bakery tool and a trading terminal both need "readable type" — completely different type.
- **Navigation** — not scaffolding. Where you are, where you can go, what matters most. A page floating in space is a component demo, not software.
- **Data display** — not just presentation. What does this number mean to the person? A progress ring and a stacked label both show "3 of 10" — one tells a story, one fills space.
- **Token names** — not implementation detail. `--ink` and `--parchment` evoke a world. `--gray-700` and `--surface-2` evoke a template.
