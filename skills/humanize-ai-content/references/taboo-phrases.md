# Taboo Phrases (AI-isms)

Purpose: catch “AI voice” patterns that reliably make text sound generated.

Three levels:

- **HARD_BANNED**: remove or replace unless it appears in a direct quote, code, or a proper noun.
- **SOFT_FLAGS**: not always wrong, but often a smell. Use judgment.
- **STRUCTURAL_FLAGS**: structure-ish patterns that are common in LLM prose. These are not always wrong, but repeated use is a tell.

This file contains machine-readable blocks used by `scripts/banned_phrase_scan.py`.

---

## HARD_BANNED (machine-readable)
leverage
utilize
delve
robust
seamless
cutting-edge
game-changer
revolutionize
synergy
synergize
unlock the potential
harness the power
in today's fast-paced world
in the ever-evolving landscape
it is important to note
let's dive in
in conclusion
to summarize
moreover
furthermore
additionally
as we explore
at the end of the day
not only that
with that being said
this begs the question
holistic approach
key takeaway
moving forward
deep dive
a testament to
it's worth noting
it is worth noting
it's important to consider
it's important to remember
aims to
plays a crucial role
plays a vital role
plays a pivotal role
notable figures
notable works
tapestry
realm
beacon
cacophony
intricate
nuanced
multifaceted
unparalleled
invaluable
groundbreaking
transformative
embark
embark on a journey
meticulous
commendable
in the realm of
navigating the complexities
navigating the landscape
at its core
at the forefront
this underscores
i hope this email finds you well
certainly, here
## /HARD_BANNED

---

## SOFT_FLAGS (machine-readable)
empower
optimize
streamline
enhance
elevate
facilitate
transform
impactful
innovative
state-of-the-art
best-in-class
world-class
mission-critical
paradigm shift
value proposition
scalable
robustness
utilization
spearhead
drive growth
needle mover
customer-centric
actionable insights
thought leadership
seamlessly
dynamic environment
resonate
foster
holistic
pivotal
testament
landscape
underscore
illuminate
bolster
advent
burgeoning
plethora
myriad
aforementioned
herein
foray
glean
shed light
thrive
flourishing
compelling
captivating
## /SOFT_FLAGS

---

## STRUCTURAL_FLAGS (machine-readable)
not only...but also
from x to y
whether...or not
it is worth noting that
as we navigate
in this digital age
in an increasingly connected world
plays a vital role in shaping
continues to evolve
has emerged as
## /STRUCTURAL_FLAGS

---

## Common replacements (quick reference)

- leverage / utilize → **use**
- facilitate → **help**
- optimize → **improve / speed up / simplify** (pick the real verb)
- enhance / elevate → **improve**
- seamless → **smooth / straightforward** (or delete)
- cutting-edge / state-of-the-art → **new / latest** (or delete)
- in conclusion / to summarize → **(delete)** or a simple final line
- it's worth noting / it is important to note → **(usually delete)** or make the uncertainty specific

---

## Notes

- If the user’s text is quoting someone (press quotes, testimonials), keep the quote as-is.
- If a phrase is part of a legal clause, contract, or compliance language, do not change it without explicit instruction.
