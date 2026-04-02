---
name: plain-english-explainer
description: >
  Translate technical code output, error messages, architectural decisions, and development
  workflows into structured plain-English explanations for non-proficient coders. Triggered
  by /explain command. Also use this skill whenever the user says "explain this," "what does
  this mean," "I don't understand," "break this down," "what did you just do," "what happened,"
  or any variant asking for clarification of technical output. Use it proactively when the user
  is a known vibe coder and the output involves complex pipelines, architecture, or multi-step
  debugging. Produces a markdown summary covering what happened, what the code does, what went
  wrong, what the options are, and what the agent recommends, all without code jargon.
---

# Plain English Explainer

Turn code output into something a human can actually read.

## Feedback Loop

This skill improves over time. **MUST read `FEEDBACK.md` before every use** to apply lessons from prior runs.

**Cycle:**
1. **Detect** — After generating an explanation, note anything that felt off: too much jargon leaked through, analogy was confusing, user had to ask follow-ups that should have been covered, recommendation was unclear, structure was too long or too short.
2. **Search** — Check `FEEDBACK.md` for prior entries on the same issue.
3. **Scope** — Decide if this is a new entry or an update to an existing one.
4. **Draft-and-ask** — Draft a short feedback entry: *"I noticed [issue]. Want me to log this?"*
5. **Write-on-approval** — Append to `FEEDBACK.md` with category tag and date.
6. **Compact-at-75** — At 75 entries, merge duplicates, promote patterns to SKILL.md, archive resolved. Reset to ~30.

## When to Use

This skill triggers on:
- `/explain` command (primary trigger)
- User says "explain this in plain English," "what does this mean," "I don't understand"
- User asks "what did you just do," "what happened," "break this down for me"
- After any complex code operation when the user is known to be a vibe coder

## Core Philosophy

The user is smart but not a programmer. They understand systems, logic, cause-and-effect, and can make good decisions — they just don't speak the language. Your job is to be the translator, not the teacher. Don't explain programming concepts abstractly. Explain what THIS code does in THIS situation using concrete analogies.

**Critical rule:** The explanation must NEVER degrade the quality of any code output. This skill applies ONLY to the explanatory summary section. All code, commands, configs, and technical output remain at full professional quality. The translation layer is additive, not a replacement.

## Load Order

| Resource | When |
|---|---|
| `FEEDBACK.md` | **Always** — before every use |
| `references/jargon-dictionary.md` | Always — the translation reference |
| `references/explanation-templates.md` | When structuring the output |

## Output Structure

Every `/explain` output follows this structure. Adapt section depth to complexity — a one-line fix gets a short version, a major refactor gets the full treatment.

### The Template

```markdown
## Plain English Summary

### What just happened
[1-3 sentences. What did the agent do? What changed? Frame it as actions
on things the user can see or interact with — files, the app, the screen,
the database.]

### What this code/system does
[Explain the relevant piece using an analogy. Compare it to something
physical, organizational, or from everyday life. Name the specific files
or components involved but explain what each one DOES, not what it IS.]

### The situation right now
[What's working? What's broken? What's the current state? Be specific.
"The login page loads but clicking the button does nothing" not "the
onClick handler isn't bound to the submit event."]

### What the options are
[Present 2-3 paths forward as choices with tradeoffs. Frame each as:
"We could [action] — this would [outcome] but [tradeoff]."]

### What I recommend (and why)
[Pick one option. Explain why it's the best fit for THIS situation.
Explain why the alternatives are worse HERE, not in general. End with
what the user needs to decide or approve before proceeding.]

### Things to keep in mind
[Optional. Gotchas, timeline implications, things that might break later,
dependencies on other people or services. Only include if genuinely useful.]
```

### Scaling Rules

| Complexity | Sections to include |
|---|---|
| **Simple fix** (typo, config tweak, one-liner) | "What just happened" + "The situation right now" (2-3 sentences total) |
| **Medium task** (bug fix, feature addition, refactor) | All sections, moderate depth |
| **Complex/architectural** (migration, new system, multi-file overhaul) | All sections, full depth, multiple analogies |

## Translation Rules

These are the core rules for converting technical language into plain English. See `references/jargon-dictionary.md` for the full lookup table.

### Rule 1: Name the thing by what it does, not what it's called

| Instead of... | Say... |
|---|---|
| "The API endpoint" | "The part of the server that handles login requests" |
| "The React component" | "The piece of code that draws the settings panel" |
| "The middleware" | "The checkpoint that every request passes through before reaching the main code" |
| "The ORM" | "The translator that converts your app's data requests into database language" |
| "The webhook" | "An automatic notification that fires when something happens on the other service" |

### Rule 2: Explain errors by what went wrong in the real world

| Instead of... | Say... |
|---|---|
| "TypeError: Cannot read properties of undefined" | "The code tried to use a piece of data that doesn't exist yet — like opening a filing cabinet drawer that was never installed" |
| "CORS error" | "The browser blocked the request because the app and the server are on different addresses, and the server hasn't said 'yes, I trust that address'" |
| "Race condition" | "Two things tried to happen at the same time and stepped on each other — like two people trying to edit the same cell in a spreadsheet simultaneously" |
| "Memory leak" | "The app is holding onto old data it no longer needs, like never closing browser tabs — eventually it runs out of room" |

### Rule 3: Frame decisions as tradeoffs, not technical preferences

| Instead of... | Say... |
|---|---|
| "We should use a queue instead of synchronous processing" | "Right now, every request waits in line and gets handled one at a time. We could switch to a system where requests drop off their work and come back for results later — faster for users, but harder for us to track if something fails" |
| "We need to add caching" | "The app asks the database the same questions over and over. We could save recent answers in a notepad so it doesn't have to ask again — much faster, but the notepad might have stale info" |

### Rule 4: Use consistent analogy families

Pick one analogy family per explanation and stick with it. Don't mix metaphors.

| Domain | Good analogy family |
|---|---|
| **Web requests / APIs** | Restaurant: kitchen (server), waiter (API), menu (docs), order (request), meal (response) |
| **Databases** | Filing system: cabinets (tables), folders (rows), labels (columns), index (table of contents) |
| **Build systems / CI/CD** | Assembly line: raw materials (source code), stations (build steps), quality check (tests), shipping (deploy) |
| **Auth / Security** | Building security: ID badge (token), front desk (auth server), guest list (permissions), expired pass (token expiry) |
| **State management** | Whiteboard: what's written on it (state), who can erase/write (actions), taking a photo of it (snapshot) |
| **Version control** | Drafts of a document: save a copy (commit), make a new version to try something (branch), combine two versions (merge), undo to a previous draft (revert) |

### Rule 5: Quantify when possible

Don't say "it's slow." Say "it takes 4 seconds when it should take under 1." Don't say "the file is too big." Say "the file is 200MB — most hosting services cap at 50MB."

### Rule 6: Always explain WHY something matters

Every technical observation must connect to something the user cares about: speed, cost, user experience, reliability, or "will this break later."

## Anti-Patterns (Things to Never Do)

1. **Never use acronyms without expanding them AND explaining what the expanded version means.** "API (Application Programming Interface)" is not enough. Say "the connection point where your app talks to another service."
2. **Never say "it's a common pattern" or "this is standard."** The user doesn't know what's common. Explain why this approach exists.
3. **Never list code jargon with parenthetical definitions as a substitute for actually explaining.** Bad: "The hook (a React pattern for managing data) fires on mount (when the component first appears)." Good: "When the settings panel first appears on screen, it immediately fetches your saved preferences."
4. **Never assume familiarity with the filesystem or terminal.** "Run this in your terminal" needs "open Terminal (the black window with the text cursor), paste this command, and press Enter."
5. **Never skip the recommendation.** The user is trusting you to have an opinion. "It depends" is not helpful. Pick the best option and say why.
6. **Never condescend.** The user is a PhD researcher, not a child. They understand complex systems — they just don't speak this particular technical dialect. Match their intelligence, not their code vocabulary.
