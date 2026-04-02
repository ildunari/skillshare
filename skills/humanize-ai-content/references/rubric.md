# Humanization Rubric (9 traits, 1–5)

Use this rubric to evaluate whether output sounds like a competent human wrote it *without changing the facts*.

## Scoring scale

- **5**: indistinguishable from a good human writer in this context
- **4**: solid human; minor rough edges
- **3**: mixed; still noticeably “LLM-ish”
- **2**: robotic, templated, or salesy
- **1**: clearly machine-generated / generic filler

**Pass target:** average **>= 4.0** AND no individual trait below **4** (unless the user explicitly wants a rigid template).

---

## 1) Natural rhythm & cadence

**What to look for:** varied sentence length, varied syntax, natural transitions, no metronome pacing.

- **5:** effortless pacing; occasional punchy short lines; no repeated sentence scaffolds
- **4:** mostly varied; a few samey sentences
- **3:** noticeable sameness (similar length/structure), listicle cadence
- **2:** “template voice” (intro + 3 bullets + conclusion every time)
- **1:** stilted; repetitive; reads like a prompt response

## 2) Specificity & concreteness

**What to look for:** concrete verbs, tangible nouns, precise modifiers.

- **5:** clear actions and specifics; avoids abstraction unless needed
- **4:** mostly concrete; a few vague verbs (“improve,” “support”)
- **3:** generic (“enhance,” “optimize,” “solutions”) without substance
- **2:** buzzword soup
- **1:** empty claims / meaningless filler

## 3) Voice consistency

**What to look for:** consistent POV, tone, formality level.

- **5:** coherent voice end-to-end; feels authored
- **4:** consistent with small slips
- **3:** tone shifts (formal → casual → formal)
- **2:** voice conflicts (salesy hype + academic hedging)
- **1:** incoherent persona

## 4) Audience fit

**What to look for:** language and structure match reader expectations.

- **5:** perfectly tuned for reader (exec, peer, customer, friend)
- **4:** good fit; minor mismatches
- **3:** “average internet voice” regardless of audience
- **2:** wrong register (too casual/formal/technical)
- **1:** ignores audience entirely

## 5) Clarity & directness

**What to look for:** strong topic sentences, no throat-clearing, minimal hedging.

- **5:** immediately clear; no wasted words
- **4:** clear; some trimming possible
- **3:** meanders; soft commitments (“may,” “might,” “could”)
- **2:** buried point; lots of qualifiers
- **1:** unclear or self-contradictory

## 6) Flow & cohesion

**What to look for:** each paragraph earns its place; ideas connect logically.

- **5:** smooth progression; transitions feel earned
- **4:** mostly smooth; a couple jumps
- **3:** choppy; stitched-together feel
- **2:** scattered; weak structure
- **1:** incoherent

## 7) Anti-template / anti-cliché

**What to look for:** avoids stock openings/closings, forced transitions, AI tells.

- **5:** original phrasing; no “in conclusion” energy
- **4:** few clichés
- **3:** multiple generic phrases / predictable structure
- **2:** lots of canned language (“delve,” “leverage,” “robust”)
- **1:** reads like a corporate template generator

## 8) Fact integrity (non-negotiable)

**What to look for:** numbers, names, dates, quotes, code, URLs preserved exactly.

- **5:** all facts preserved; no accidental drift
- **4:** preserved; trivial formatting only (and allowed)
- **3:** one minor factual drift or a suspicious paraphrase
- **2:** multiple changes to concrete details
- **1:** meaning/facts changed


## 9) Structural naturalness

**What to look for:** varied paragraph lengths, no hyper-symmetry, no five-paragraph template, limited participial chains, minimal em dash overuse.

- **5:** organic structure; paragraphs vary naturally; no template feel
- **4:** mostly varied; one or two symmetric sections
- **3:** blocky; paragraphs suspiciously similar in length; tricolons everywhere
- **2:** five-paragraph essay template; every paragraph has the same shape
- **1:** rigid outline with intro/body/conclusion scaffolding visible


---

## Quick acceptance checklist

- [ ] No hard-banned phrases remain (see `references/taboo-phrases.md`)
- [ ] “Must-keep” facts are present verbatim (numbers/dates/URLs/quotes/code)
- [ ] Sentence lengths vary (not all ~12–16 words)
- [ ] No canned framing (“In today’s world…”, “Let’s dive in…”, “In conclusion…”)
- [ ] Structural patterns look natural (no overuse of em dashes, -ing chains, tricolon spam)
- [ ] Output matches the chosen preset and audience intent
