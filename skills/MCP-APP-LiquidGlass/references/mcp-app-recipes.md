# MCP app recipes

These are opinionated layout patterns for tool-driven apps.

## Recipe 1: chat + tool runner

Use when the app has:
- a conversation thread
- a composer
- a row of tool actions
- tool result cards or attachments

Recommended glass hierarchy:
- strongest glass: composer shell and floating action row
- medium glass: selected result cards and side inspector
- lightest treatment: conversation bubbles

Suggested structure:
- sticky bottom composer dock
- transcript area with restrained backgrounds
- expandable tool result side sheet
- status chip for MCP server connection

## Recipe 2: multi-tool dashboard

Use when the app feels like a control room.

Recommended glass hierarchy:
- strongest glass: top command/navigation shell
- medium glass: hero KPI cards or central action panel
- flatter inner surfaces: tables, logs, JSON, settings

Reason:
- dashboards need hierarchy and legibility more than spectacle

## Recipe 3: floating assistant palette

Use when the UI is mostly an overlay.

Recommended elements:
- floating pill dock
- detachable glass result panel
- command search input
- drag handle for playful but controlled movement

This is where stronger distortion and drag feel appropriate.

## Recipe 4: media / preview tool

Use when the MCP app works with images, video, design assets, or generated files.

Recommended elements:
- preview stage with minimal glass around controls
- glass transport or action controls
- inspector drawer with flatter content layer

## Component checklist

When generating MCP UI, consider whether the user needs:
- server status badge
- active model badge
- tool run history list
- result provenance / source pills
- retry / cancel / rerun controls
- latency or streaming state indicator
- attachment well / preview area

Wrap the workflow-critical controls in the premium visual treatment first.

## Restraint rule

If the app contains dense reading or debugging output, glass should mainly live on
navigation and controls. Dense logs and code blocks should sit on calmer, darker,
more stable surfaces inside the glass shell.
