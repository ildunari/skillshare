---
name: hermes-subagents_Hermes
description: "Umbrella router for spawning specialized Hermes subagents. Use whenever a task should be delegated to a focused lane: Hermes internals, macOS operations, browser/computer use, iOS/Swift, web/X search, papers, product finding, prompt design, UI polish, or voice/audio. Pick the lane, start child context with Lane: <lane-name>, and pass complete context."
version: 0.3.0
author: Hermes Agent
license: MIT
targets:
- hermes-default
- hermes-gpt
- claude-hermes
metadata:
  hermes:
    tags:
    - hermes
    - subagent
    - delegation
    - router
---
# Hermes Subagents

Use this skill when the main Hermes session should delegate focused work to an isolated subagent.

## Routing rule

Every delegated child prompt must name the lane. Start the child context with:

```text
Lane: <lane-name>
```

This makes subagent usage auditable in session history instead of showing up as anonymous `delegate_task` calls.

## Lane map

- **hermes-mechanic**: Hermes config, gateways, skills, profiles, logs, repo troubleshooting.
- **mac-operator**: local files, processes, launch agents, cron, logs, setup checks, macOS state.
- **computer-use**: GUI/browser workflows, interaction-heavy websites, visual verification.
- **ios-swift**: Swift, SwiftUI/UIKit, Xcode, TestFlight, App Store workflows.
- **web-searcher**: current facts, source triage, concise cited web answers. Use modern surfaces: `web`, `web_search`, `grok_research`/`x_search` for Grok/X-current search, `x_twitter`/xurl for exact X post/user reads, `github_repo_brief` for GitHub repos, and browser only for JS/auth-heavy pages. For deep research: broad map → targeted follow-ups → community/deep-thread checks → gaps vs confirmed negatives.
- **paper-scout**: academic papers, methods, datasets, authors, citation trails.
- **product-finder**: shopping/product research, pricing, availability, tradeoffs. For products/tools: verify official specs/pricing, check real-user reports, include repo health for software, rank by fit not popularity, and include an underdog when credible.
- **prompt-designer**: system prompts, skills, agent briefs, output contracts.
- **ui-polish**: product surface critique, screenshots, CSS/SwiftUI/layout, UX copy.
- **voice-audio**: TTS, transcripts, voice notes, speech workflow debugging.

## Delegation rules

Pass the child all relevant context, paths, constraints, and expected output shape. Subagents have no memory of the current conversation. Require verifiable handles for side effects and verify important claims yourself before reporting success.

When auditing “background subagents” in Hermes, first separate gateway background tasks from actual delegated subagent lanes. Gateway `/background` work should preserve `SessionSource`, resolve runtime/config normally, and report back through the platform adapter with correct metadata; that is not the same surface as spawning a hermes-mechanic/mac-operator/etc. lane.

## Output contract for children

Ask each subagent to return:

1. **Answer/result** — direct conclusion or completed action.
2. **Evidence/actions** — sources, files, commands, screenshots, or route/tool used.
3. **Issues/blockers** — uncertainty, missing access, unavailable toolsets, or confirmation needed.
4. **Next step** — only if it changes what the parent should do.
