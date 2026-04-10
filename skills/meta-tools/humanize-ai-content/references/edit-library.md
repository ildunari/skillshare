# Edit Library

This file is a menu of **rewrite moves**. In Diagnosis, identify the 3–6 moves the text needs most. In Reconstruction, apply those moves deliberately.

Principle: **Rewrite the delivery, not the facts.** If a detail is not in the input, don’t invent it.

---

## 1) Delete throat-clearing intros

**Cut** openings that don’t add information.

**Before**
> In today’s fast-paced world, it’s important to note that…

**After**
> Here’s what changed and what to do next.

---

## 2) Replace abstract verbs with concrete verbs

Abstract verbs make text feel like a memo generator.

| Abstract | Better defaults |
|---|---|
| leverage | use |
| utilize | use |
| facilitate | help |
| implement | put in place / roll out |
| optimize | improve / tighten / speed up |
| enhance | improve / strengthen |
| ensure | make sure |
| drive | increase / reduce / cause / lead to (pick one) |

**Before**
> We will leverage this framework to optimize throughput.

**After**
> We’ll use this framework to speed up throughput.

---

## 3) Kill corporate filler and empty intensifiers

Delete words that pretend to add meaning.

**Cut list (common)**
- robust, seamless, innovative, cutting-edge, game-changing
- very, really, extremely (unless it changes meaning)
- “it’s important to note,” “in order to,” “the fact that”

**Before**
> This robust solution will seamlessly deliver incredible results.

**After**
> This approach reduces errors and saves time.

---

## 4) Break the “template sentence” pattern

LLM text often repeats the same sentence shape.

**Fixes**
- Mix simple and compound sentences
- Vary sentence starters (not every line begins with “This” or “We”)
- Use the occasional fragment *only* in `crisp-human` or `story-lean`

**Before**
> This improves quality. This increases speed. This reduces costs.

**After**
> Quality goes up. Work moves faster. Costs drop.

---

## 5) Use natural transitions (or none)

Forced transitions sound artificial.

**Avoid**
- Moreover, Furthermore, Additionally, In conclusion, To summarize

**Prefer**
- But / So / That said / Here’s the catch / The point is
- Or just move to the next idea without a transition

---

## 6) Tighten sentences (remove “padding words”)

**Before**
> We are able to provide support in a way that helps you achieve your goals.

**After**
> We can help you reach your goals.

---

## 7) Reduce hedging (unless uncertainty is real)

Too many qualifiers makes writing feel evasive.

**Before**
> It may potentially help to consider possibly adjusting…

**After**
> Consider adjusting…

If the input contains uncertainty (estimates, “likely,” “preliminary”), keep it.

---

## 8) Prefer active voice (unless actor is unknown)

**Before**
> The report was delivered by the team.

**After**
> The team delivered the report.

---

## 9) Make lists feel human

A wall of bullets can feel AI-ish if every bullet is same length.

**Fixes**
- Mix bullet lengths
- Use parallel structure when it helps
- Don’t over-label every section

---

## 10) Keep the author’s intent, not your own

If the input is:
- **sales**: keep the CTA but remove hype
- **technical**: keep precision, cut fluff
- **apology**: keep accountability, avoid corporate legalese
- **announcement**: keep clarity and timing, avoid cheerleading

---

## 11) Do-not-do list

- Don’t add new facts, numbers, names, dates, or claims.
- Don’t “correct” facts unless the user asked.
- Don’t change quoted text or code.
- Don’t make it sound like marketing unless it’s supposed to be marketing.

---

## 12) Break the participial chain

AI loves: “main clause, -ing phrase.”

**Before**
> The platform processes data in real time, enabling teams to make faster decisions.

**After**
> The platform processes data in real time. Teams make faster decisions as a result.

One or two per piece is fine. Three or more in quick succession is a tell.

---

## 13) Reduce em dash density

Em dashes are legitimate punctuation, but AI uses them as a universal connector.
Limit to **1–2 per 500 words**. Replace others with:

- Period + new sentence (most common fix)
- Comma (for light asides)
- Colon (for explanations)
- Parentheses (for true asides)

**Before**
> The results were clear—teams moved faster—and costs dropped—proving the approach worked.

**After**
> The results were clear: teams moved faster, and costs dropped. The approach worked.

---

## 14) Vary list lengths (break the tricolon habit)

AI defaults to groups of three. Mix it up.

**Before**
> The tool is fast, reliable, and easy to use. It saves time, reduces errors, and improves quality.

**After**
> The tool is fast and reliable. It saves time and catches errors that manual review misses.

---

## 15) Kill the recap conclusion

AI always wants to “wrap up” with a summary paragraph. If the piece is under ~1000 words, cut the recap conclusion entirely. If longer, end with a forward-looking statement or a call to action — not a restatement.

**Before**
> In conclusion, by leveraging these strategies, teams can optimize their workflows and drive better outcomes.

**After**
> [Delete. The piece is done.]

---

## 16) Match the author’s actual register

If the input has slang, humor, profanity, or deliberate informality, keep it. Don’t “correct” casual writing into business prose. AI has a strong pull toward the professional middle ground.
