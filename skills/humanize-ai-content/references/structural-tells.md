# Structural tells (AI patterns)

Purpose: detect and fix **structure-level** signals that make writing feel machine-generated even when vocabulary is clean.

This file is used as a checklist during Diagnosis, and as guidance during Reconstruction.

---

## C1) Participial phrase pattern (“main clause, -ing clause”)

**The tell:** repeated use of “..., enabling/creating/revealing/allowing ...” as a universal connector.

One or two is normal. A chain (3+ in a short piece) reads like a model stitching clauses.

**Before**
> The platform processes data in real time, enabling teams to make faster decisions.  
> It flags anomalies early, reducing downtime.  
> It centralizes logs, improving visibility across services.

**After**
> The platform processes data in real time. Teams can make faster decisions.  
> It flags anomalies early, so downtime drops.  
> It centralizes logs, which makes cross-service debugging easier.

**Fix moves**
- Split into two sentences.
- Replace “-ing connector” with a concrete causal link (“so”, “which means”, “as a result”) sparingly.
- Sometimes delete the second clause entirely if it’s a restatement.

---

## C2) Em dash overuse

**The tell:** em dashes as the default glue for every aside, clarification, or emphasis.

Humans use them, but models tend to use them everywhere.

**Heuristic:** **>2 em dashes per 500 words** is a structural smell.

**Fix moves**
- Replace with a period + new sentence (best default).
- Replace with a comma (light aside).
- Replace with a colon (explanation).
- Replace with parentheses (true aside).
- Or restructure to remove the aside.

---

## C3) Rule of three / tricolon abuse

**The tell:** every paragraph contains “X, Y, and Z” lists (three adjectives, three benefits, three clauses).

Tricolons are powerful when rare. When constant, they look templated.

**Before**
> The tool is fast, reliable, and easy to use. It saves time, reduces errors, and improves quality.

**After**
> The tool is fast and reliable. It saves time and catches errors that manual review misses.

**Fix moves**
- Vary list lengths: 2, 4, or inline prose.
- Replace a list with one concrete example.
- Merge “three benefits” into one sentence that names the real payoff.

---

## C4) Hyper-symmetry (blocky paragraphs)

**The tell:** paragraphs that are suspiciously similar in length and sentence count. It looks like an outline filled in.

**Fix moves**
- Mix paragraph lengths on purpose.
- Use 1-sentence paragraphs occasionally (especially for emphasis).
- Combine two short paragraphs if they feel chopped for rhythm.

**Heuristic:** if paragraph word-count standard deviation is **< 5**, it’s probably too uniform.

---

## C5) Five-paragraph essay template

**The tell:** intro-thesis, 3 body sections, recap conclusion.

Even in short content, models often default to this scaffold.

**Fix moves**
- Cut the recap conclusion entirely (especially under ~1000 words).
- End on the last substantive point, or on a specific next step.
- If a conclusion is needed, make it new information (a decision, a constraint, a call to action), not a restatement.

---

## C6) “From X to Y” range constructions

**The tell:** generic range phrases like:
- “From beginners to experts”
- “From bustling cities to serene landscapes”

These are highly model-ish because they’re low-effort “coverage” signals.

**Fix moves**
- Replace with concrete examples (“Beginners can start with…, experienced users can…”).
- Or name the range directly (“This works for beginners and experienced users.”).
- Or delete if it’s filler.

---

## C7) Correlative conjunction stacking

**The tell:** lots of “not only…but also”, “both…and”, “whether…or”.

They’re fine in moderation. Repeating them reads like rhetorical autopilot.

**Fix moves**
- Use at most one correlative pair per piece (usually).
- Replace others with simple statements.
- Prefer concrete verbs over rhetorical framing.

---

## C8) Participial opener / dangling modifier

**The tell:** sentences that start with an “-ing” opener that doesn’t clearly attach to the subject.

**Before**
> Leveraging advanced technology, the team improved performance.

**After**
> The team used a faster pipeline and improved performance.

**Fix moves**
- Lead with the subject.
- Replace the opener with a concrete verb.
- If the opener adds nothing, delete it.

---

## C9) Emotional flatness / excessive hedging

**The tell:** “statistical average voice” + constant hedging:
- “It’s worth noting…”
- “Generally speaking…”
- “To some extent…”
- “From a broader perspective…”

Humans hedge when uncertainty is real. Models hedge as a default safety posture.

**Fix moves**
- Delete empty hedges.
- Commit to a position when the input already commits.
- If uncertainty is real, make it specific (“early data suggests…”, “we haven’t tested X yet”).

---

## C10) Over-positive / promotional tone

**The tell:** everything is upbeat, “transformative,” and “exciting,” even when the content is neutral.

Models skew positive in sentiment unless guided otherwise.

**Fix moves**
- Add honest caveats *only if the input already implies them* (don’t invent downsides).
- Cut cheerleading and replace with concrete outcomes.
- Prefer “here’s what changed” over “we’re thrilled to announce”.

---
