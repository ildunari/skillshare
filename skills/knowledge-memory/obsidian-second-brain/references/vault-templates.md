# Vault Templates Reference

Complete template definitions for the Brain vault. Each template shows the frontmatter schema and content structure. When creating notes programmatically, substitute Templater expressions (`<% ... %>`) with actual values.

## Table of Contents

- [Daily Note](#daily-note)
- [Tool Note](#tool-note)
- [Reference Note](#reference-note)
- [Knowledge Doc](#knowledge-doc)
- [Literature Note](#literature-note)
- [Meeting Note](#meeting-note)
- [Project Note](#project-note)
- [Person Note](#person-note)
- [Output Note](#output-note)
- [MCP Server](#mcp-server)
- [Skill Reference](#skill-reference)
- [Agent Profile](#agent-profile)
- [NSFW Website](#nsfw-website)
- [NSFW Creator](#nsfw-creator)
- [NSFW Subreddit](#nsfw-subreddit)
- [NSFW Bodybuilder](#nsfw-bodybuilder)
- [NSFW LPSG Thread](#nsfw-lpsg-thread)

---

## Daily Note

**Path:** `daily/YYYY-MM-DD.md`

```yaml
---
type: daily
date: YYYY-MM-DD
tags:
  - type/daily
---
```

**Sections:** Tasks, Captures, Meetings, Notes, End of day

---

## Tool Note

**Path:** `tech/{subcategory}/{tool-name}.md`

```yaml
---
type: tool
status: active | inactive | evaluating
tool_category: cli | gui-app | system-extension | mcp-server | shell-tool | app | shortcut | browser-extension | library | framework | service
install_method: homebrew | manual | app-store | npm | pip | cargo | n/a
install_command: ""
url: ""
tags:
  - type/catalog
  - domain/<relevant-domain>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Description, Install, Usage, Links

---

## Reference Note

**Path:** `tech/{subcategory}/{name}.md` or `brown/concepts/{name}.md`

```yaml
---
type: reference
status: draft | stable | outdated
topic: []
sources: []
tags:
  - type/reference
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Content, Related concepts, Sources

---

## Knowledge Doc

**Path:** `tech/docs/{name}.md`

```yaml
---
type: knowledge
status: current | outdated | archived
doc_category: guide | reference | audit | prompt-pack | tool-doc | design
provider: anthropic | openai | google | xai | meta | mistral | n/a
source_url: ""
tags:
  - type/reference
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** TL;DR, Content, Source, Related

---

## Literature Note

**Path:** `brown/literature/{citekey}.md`

```yaml
---
type: literature
status: to_read | reading | done
citekey: "author2025-keyword"
title: "Paper title"
authors:
  - "Last, F."
year: 2025
venue: "Journal Name"
doi: ""
url: ""
projects: []
tags:
  - type/reference
  - domain/research
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Key findings, Methods, Relevance to my work, Questions / follow-ups, Raw notes

---

## Meeting Note

**Path:** `brown/meetings/{date}-{topic}.md`

```yaml
---
type: meeting
status: raw | processed
project: ""
people: []
date: YYYY-MM-DD
tags:
  - type/reference
created: YYYY-MM-DD
---
```

**Sections:** Attendees, Agenda, Discussion, Decisions, Action items

---

## Project Note

**Path:** `brown/projects/{name}/{name}.md` (PhD) or `tech/projects/{name}/{name}.md` (software)

```yaml
---
type: project
status: active | paused | completed | archived
area: phd | software | personal
priority: low | medium | high
start: YYYY-MM-DD
milestone_next: ""
stakeholders: []
tags:
  - type/config
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Objective, Background, Current status, Key resources, Tasks, Open questions, Log

---

## Person Note

**Path:** `brown/people/{name}.md`

```yaml
---
type: person
role: advisor | collaborator | student | contact | personal
institution: ""
email: ""
tags:
  - type/reference
created: YYYY-MM-DD
---
```

**Sections:** Role & context, Notes, Meetings

---

## Output Note

**Path:** `brown/outputs/{type}/{name}.md`

```yaml
---
type: output
status: draft | in_review | submitted | published
output_type: manuscript | grant | presentation | figure
project: ""
target: ""
deadline: ""
tags:
  - type/config
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Outline, Key points, Status / progress, Feedback

---

## MCP Server

**Path:** `tech/agent-tools/mcp-servers/{name}.md`

```yaml
---
type: mcp-server
status: active | inactive
protocol: stdio | http | sse | streamable-http
url: ""
tags:
  - type/config
  - domain/mcp
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** What it connects to, Configuration (JSON block), Tools provided, Notes

---

## Skill Reference

**Path:** `tech/agent-tools/skills/{name}.md`

```yaml
---
type: skill-ref
skill_category: design | research | code-quality | automation | documents | testing | data-science | process | games | web | apple-ios
platforms:
  - claude-code
status: installed | available | archived
tags:
  - type/skill
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Description, Usage, Platforms, Related docs

---

## Agent Profile

**Path:** `tech/agent-tools/agent-profiles/{name}.md`

```yaml
---
type: agent-profile
agent_domain: backend | frontend | ios | devops | security | data | research | design | process | language
platforms:
  - claude-code
tags:
  - type/agent-profile
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Specialization, When to use, System prompt summary, Related skills

---

## NSFW Website

**Path:** `nsfw/websites/{category}/{name}.md`

Categories: `tubes`, `niche`, `premium`, `cams`, `aggregators`, `forums`, `creator-platforms`

```yaml
---
type: nsfw-website
status: active | inactive
site_category: tube | niche | onlyfans | creator | forum | aggregator | cam | premium
url: ""
free_tier: true
tags:
  - type/catalog
  - domain/nsfw
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Overview, Content Focus, Access (URL, Free tier, Premium), Notes

---

## NSFW Creator

**Path:** `nsfw/{platform}/{category}/{name}.md`

Used across Twitter, Instagram, OnlyFans, Fansly, Reddit users.

```yaml
---
type: nsfw-creator
status: active
platform: twitter | reddit | instagram | onlyfans | fansly | manyvids | pornhub | other
handle: ""
url: ""
content_type: []
tags:
  - type/catalog
  - domain/nsfw
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Profile (Platform, Handle, URL), Content, Notes

---

## NSFW Subreddit

**Path:** `nsfw/reddit/{category}/{name}.md`

Categories: `subs-general`, `subs-niche`, `subs-fitness`, `subs-celebrity`

```yaml
---
type: nsfw-subreddit
status: active
subreddit: ""
url: ""
content_focus: []
nsfw_verified: true
tags:
  - type/catalog
  - domain/nsfw
  - topic/reddit
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Overview (Subreddit, URL, Subscribers), Content Focus, Notable Posts/Creators, Notes

---

## NSFW Bodybuilder

**Path:** `nsfw/bodybuilders/{category}/{name}.md`

Categories: `pro`, `classic`, `physique`, `influencers`, `powerlifting`

```yaml
---
type: nsfw-bodybuilder
status: active
division: bodybuilding | classic-physique | mens-physique | figure | bikini | wellness | powerlifting | crossfit | fitness-model
competition_level: pro | amateur | recreational | influencer
socials: []
tags:
  - type/catalog
  - domain/nsfw
  - topic/bodybuilding
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Profile (Division, Level, Height/Weight), Social Media, Competition History, Content/Media, Notes

---

## NSFW LPSG Thread

**Path:** `nsfw/lpsg/{category}/{name}.md`

Categories: `celebrity`, `verified`, `amateur`, `discussion`

```yaml
---
type: nsfw-lpsg
status: active
thread_type: celebrity | amateur | discussion | verified | ethnicity | general
url: ""
subject: ""
tags:
  - type/catalog
  - domain/nsfw
  - topic/lpsg
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Sections:** Thread (URL, Subject, Type), Key Content, Notes
