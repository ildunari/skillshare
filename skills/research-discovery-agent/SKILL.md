---
name: research-discovery-agent
user-invocable: false
description: >
  Use when researching Apple-platform engineering topics such as iOS, macOS, Swift, Xcode,
  WWDC changes, Apple APIs, library choices, migration risk, or best practices, and the user needs
  a structured evidence-backed discovery workflow. Prefer this for open-ended Apple developer research
  that should end in citations, weighted findings, and actionable recommendations, not for generic
  web research outside the Apple ecosystem.
version: 1.0.0
tags:
  - ios
  - macos
  - swift
  - apple
  - research
  - discovery
  - wwdc
  - documentation
  - libraries
  - design
---

# research-discovery-agent

> **Purpose:** Make professional-grade iOS/macOS research repeatable, auditable, and fast by combining
> disciplined methodology with focused tools and templates.

## Overview

- **What this Skill is**: A meta-skill that teaches Claude _how_ to research Apple-platform topics like a senior iOS engineer,
  and equips it with ready-to-run scripts that gather primary data from Apple docs, WWDC transcripts, GitHub, Reddit,
  Stack Overflow, Twitter/X, and design communities. The outputs are structured notes, citations, and decision-ready insights.
- **What this Skill is not**: A generic web searcher. It is optimized for Apple developer contexts: APIs, frameworks,
  build systems, release notes, migration plans, and library selection.
- **Philosophy**: Prefer primary sources, show work, capture uncertainty, and extract actionable next steps.
- **Deliverables**: Research logs, evidence-backed conclusions, risk registers, migration checklists, and suggested experiments.

### How Claude uses this Skill

- Claude reads this `SKILL.md` and the `docs/`, `templates/`, `scripts/`, and `resources/` folders to learn workflows,
  commands, and evaluation criteria. It then proposes a plan, runs tools (when allowed), and synthesizes findings into
  succinct briefs or long-form reports.
- Skills are **model-invoked**, so good frontmatter and section naming help Claude decide when to activate the Skill.
  Keep the description specific to Apple-platform research to prevent overuse on unrelated tasks.

## When to Use

Use this Skill when you need to:
- Investigate new Apple APIs (e.g., SwiftData, Observation, WidgetKit, App Intents, RealityKit).
- Plan OS or Xcode upgrades and assess breaking changes.
- Evaluate third-party libraries or compare in-house options.
- Triage performance regressions or toolchain issues.
- Discover best practices for architecture, testing, and CI on Apple platforms.
- Prepare design and UX references for a new app or feature.
- Summarize community sentiment (pain points, workarounds, patterns).
- Produce an evidence-backed recommendation with citations.

## Research Methodology (Field-tested)

**Phases**
1. **Intent framing** – Convert the question into a testable decision with constraints and success criteria.
2. **Source mapping** – Identify primary sources (Apple docs, headers, release notes, WWDC) and secondary sources (Swift Forums, SO, Reddit, blogs).
3. **Signal collection** – Run the scripts to collect structured data (repos, sessions, threads, questions, design examples).
4. **Evidence weighting** – Score sources on recency, authority, internal consistency, cross-source agreement.
5. **Synthesis** – Normalize conflicting claims, identify deltas between docs and observed behavior, capture risks.
6. **Action extraction** – Produce migration plans, experiments, and checklists.
7. **Review & iterate** – Validate with peers; update notes and citations.

**Principles**
- Prefer **first-party** documentation and headers; treat community content as hypotheses until verified.
- Seek **triangulation**: require at least two independent sources for contentious claims.
- Separate **facts** (observations) from **interpretations** (hypotheses) and **decisions** (actions).
- Capture **unknowns** and propose measurable experiments.

## Apple Documentation Navigation (developer.apple.com strategies)

- Start with `documentation/` pages; use left-nav “Topics” and “See Also” to map the API surface.
- Use **search operators**: `site:developer.apple.com <keyword>`, filter by “API Reference” vs “Articles”.
- Cross-check **headers** in Xcode (Quick Help) to confirm availability, deprecations, and platform conditions.
- For **sample code**, examine build settings, entitlements, and Info.plist keys to ensure completeness.
- Keep a **glossary** of framework/language terms per project.
- Record **availability annotations** (e.g., `@available(iOS 18, *)`) and conditional compilation flags.
- Save links using `resources/bookmarks.json` and note any **breaking changes** between minor OS updates.

## WWDC Session Discovery

- Begin at the yearly WWDC index; filter by **platform**, **framework**, and **level**.
- Use transcripts to keyword-search precise phrases and timecodes.
- Compare sessions across years to detect **API evolution** and **guideline shifts**.
- Prioritize **“What’s new in …”** sessions for high-level deltas; follow with deep dives.
- Extract **do/don’t** lists and implementation details demoed in code labs.
- Use the `scripts/wwdc_session_searcher.py` to search transcripts and export timecoded quotes.

## Release Notes Analysis

- Track **Xcode**, **iOS/iPadOS**, **macOS**, **watchOS**, **visionOS** release notes.
- Encode a checklist: new APIs, removed APIs, behavior changes, compiler changes, linker flags, Swift version, SDK diffs.
- Map known issues to **workarounds** and record **radar/Feedback** IDs when available.
- Note **binary compatibility** and **ABI stability** implications for libraries and plugins.

## GitHub Research Strategies

- Scrape **Trending** for `Swift`, `Objective-C`, and **iOS** topics (daily/weekly).
- Use the API to fetch **stars**, **releases**, **issues/PR velocity**, and **bus factor** (core maintainers).
- Read **Issues** and **PRs** qualitatively: look for maintainers’ tone, response speed, and roadmap clarity.
- Analyze **star history** and **commit cadence**; beware of sudden spikes without maintenance depth.
- Prefer libraries with **SPM** support, CI badges, semantic versioning, and recent **tags**.
- Use `scripts/github_trends_analyzer.py` and `scripts/repo_analyzer.py` to build comparative tables.

## Twitter/X Monitoring

- Follow maintainers and Apple engineers; monitor hashtags: `#SwiftLang`, `#SwiftUI`, `#iOSDev`, `#macOS`, `#WWDC`.
- Track spikes around betas, RCs, and major releases; these often surface **breaking changes** early.
- Use `scripts/twitter_monitor.py` to stream/search by keywords and export a daily brief.

## Swift Forums Research

- Monitor **Evolution** proposals and **Pitch** threads for upcoming changes.
- Identify patterns in objections and alternatives; note rough consensus vs. split viewpoints.
- Correlate accepted proposals with **Swift releases** and Xcode toolchains.
- Summarize **diagnostics**, **migration** notes, and **source-breaking changes**.

## Reddit Strategies

- Subreddits: r/swift, r/iOSProgramming, r/SwiftUI, r/macprogramming, r/applehelp (for user pain signals).
- Sort by **Top this month** and **New** for a balanced view of durable topics vs. emergent pain.
- Extract reproducible bug reports and link to **radars** or **Feedback Assistant** references when present.

## Stack Overflow Patterns

- Query top tags: `swift`, `swiftui`, `ios`, `xcode`, `uikit`, `combine`, `core-data`.
- Identify **unanswered** or **highly-viewed** questions—good signals for documentation gaps.
- Spot recurring **XY-problems** and propose precise rephrasings for better answers.
- Use `scripts/stackoverflow_analyzer.py` to cluster pain points and output a heatmap (via matplotlib).

## Design Resource Discovery

- Browse Figma Community, Sketch resources, Dribbble, Behance, and Mobbin for **UI patterns**.
- Collect **teardowns** of high-quality apps; note **navigation**, **empty states**, **dark mode**, **accessibility**.
- Cross-check against **Human Interface Guidelines (HIG)** and SF Symbols usage.
- Use `scripts/design_resource_crawler.py` to gather references with license notes.

## Library Evaluation

- Metrics: stars, recent releases, dependency graph, open issues ratio, time-to-first-response, CI status, SPM support.
- Signals of maintenance: release cadence, code ownership distribution, test coverage, docs completeness.
- Run `scripts/library_comparator.py` to compute a composite **adoption-readiness score** and a radar chart.
- Prefer **small, composable** libraries over monoliths; verify transitive dependency risks.

## Synthesizing Conflicting Information

- Create an **evidence table**: claim, supporting sources, contradicting sources, strength, notes.
- State hypotheses as **conditional** (“if Xcode 17.4 beta uses Swift 6.0 snapshot, then …”) and design experiments.
- Use **small repro projects** to test behavior; attach scripts and logs.

## Identifying Signal vs Noise

- Prioritize:
  1. First-party docs and headers
  2. WWDC sessions and sample code
  3. Maintainer posts and issue comments
  4. Aggregated community threads
- Down-weight:
  - Unverified blog posts
  - Older posts predating relevant releases
  - Benchmarks without methodology/code

## Source Quality Evaluation (Checklist)

- **Authority**: Who publishes? Apple team? Maintainer? Veteran dev?
- **Recency**: Does it match current OS/Xcode/Swift versions?
- **Reproducibility**: Code sample builds? Steps are complete?
- **Consistency**: Aligns across docs, headers, and behavior?
- **Biases**: Commercial incentives? Framework advocacy?
- **License**: Legal to use sample assets/code?

## Citation and Tracking

- Log every source in `scripts/citation_tracker.py` store (CSV/JSONL/SQLite).
- Include: title, URL, author, accessed date, tags, summary, quote, reliability score.
- Render footnotes and a **bibliography** block in generated reports.

## Bias Detection

- Look for confirmation bias in library selection (“familiar equals best”).
- Balance front-end excitement (SwiftUI) with operational reality (CI, snapshots, UI testing).
- Watch survivorship bias in GitHub trends (stars vs production usage).
- Ensure diversity of sources (forums, regions, company sizes).

## Research Note-Taking

- Use `templates/research-plan.md` to define scope and criteria.
- Capture **Findings**, **Evidence**, **Decisions**, and **Next Actions** separately.
- Keep **verbatim quotes** limited and clearly marked.
- Store all notes with **permalinks** to sources.

## Actionable Insight Extraction

- For each finding, propose at least one **action** (experiment, migration, refactor, alert, deprecation).
- Attach **owner** and **due window** (internal team practice).
- Provide **risk level** and **impact estimate** qualitatively.

## Best Practices

- Automate routine collection; spend human time on synthesis.
- Keep a stable **baseline** environment for repro (Xcode, SDKs).
- Version control both **notes** and **data**; prefer plain text/CSV/JSON.
- Regularly **archive** reports; annotate with major OS/Xcode updates.

## Anti-Patterns

- “Cargo-cult” adopting libraries without reading source or sample code.
- Relying on Twitter/X sentiment as truth without reproducing.
- Ignoring release notes and SDK diffs when upgrading toolchains.
- Treating Stack Overflow answers as authoritative without testing.

## Tool Reference

- Scripts live in `scripts/`, shared utilities in `tools/`, checklists and templates in `templates/`.
- See `tools/report_generator.py` for assembling a Markdown/HTML report from collected JSON artifacts.
- Configure API keys via environment variables documented in `README.md`.

## Complete Research Workflows

### Workflow A: Evaluate a SwiftUI Persistence Library
1. Define criteria (platforms, offline requirements, migration cost).
2. Run `github_trends_analyzer.py --topic swift --since weekly` to gather candidates.
3. Run `repo_analyzer.py --repo owner/name --repo owner/name ...` for quality signals.
4. Compare with `library_comparator.py --repos ... --metrics default`.
5. Search WWDC for persistence patterns with `wwdc_session_searcher.py --query SwiftData`.
6. Pull pain points via `stackoverflow_analyzer.py --tags swiftui,core-data --days 90`.
7. Synthesize findings and export a report.

### Workflow B: Plan an iOS Major Upgrade
1. Scrape release notes and Xcode changes; log issues.
2. Search WWDC “What’s New” + framework sessions for migration cues.
3. Cluster Stack Overflow and Reddit threads from the last 90 days.
4. Draft a migration plan with risk mitigation and test strategy.
5. Produce a stakeholder brief with evidence and recommended timeline.

---

## Appendix: References & Inspiration

- Anthropic “Agent Skills” docs describe Skills as discoverable capabilities with `SKILL.md` plus optional scripts/templates.
- Skills are **model-invoked** and can be versioned and deployed across Claude surfaces; keep descriptions specific.
- Custom agents and subagents often use Markdown with **YAML frontmatter** to define behavior.

_Last updated: 2025-10-28_
