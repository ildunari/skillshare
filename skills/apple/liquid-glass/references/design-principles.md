# Design principles

## Core stance

Liquid Glass is a functional overlay layer. It belongs where users act, navigate, search, inspect, or dismiss. It usually does not belong behind every piece of content.

Use it for:

- navigation chrome
- bottom composers
- floating toolbars
- search/filter affordances
- context menus
- compact inspector panels
- media/canvas controls
- status chips and tool-call controls

Avoid defaulting it to:

- every card
- every chat bubble
- every list row
- long markdown sections
- code blocks or tables
- dense forms/logs/reasoning bodies

## Hierarchy

Content remains primary. Glass floats above content and clarifies what can be acted on.

For AI products:

- messages and markdown stay mostly clean
- thread rows stay plain
- glass composer, filters, tool metadata, and media controls carry the new visual language

## Harmony

Use rounded, hardware-aligned forms. Prefer capsules, circles, and continuous rounded rectangles. Keep glass close to the physical logic of the screen:

- bottom reach on phones
- safe-edge controls over media
- source-linked transitions from the element that triggered the action
- one coherent group for related controls

## Restraint

If you can remove one glass surface, remove it. If two glass surfaces are adjacent, consider one container. If text readability drops, simplify or darken the background before adding more glass.

## Focus

Use glass to indicate:

- this is actionable
- this floats above the content
- this came from that source
- this is the current navigation/control layer

Use dimming layers for modal focus. Use source-linked motion for locality. Use tab minimization or fading controls when chrome should recede.

## Search, tabs, and sheets

Native search, tab bars, tab accessories, and sheets should be the first pass. They already participate in the iOS 26 design language and handle many accessibility and platform behaviors automatically.

Custom tab/search bars are justified only when the native system cannot express a real product requirement. When custom-building, replicate accessibility semantics, selection state, reselection behavior, safe areas, and search behavior intentionally.

Sheets and popovers usually need glass only in their controls. Dense sheet content should stay legible and structured.

## AI-client-specific guidance

### Chat

- keep the composer glassy
- keep message bodies mostly plain
- use subtle glass only for per-message utility controls if needed
- use symbol replacement for send/stop/voice state

### Thread list

- plain rows
- native search or compact search/filter chrome
- glass only for trailing controls, active filters, or global actions

### Tool calls

- keep the panel chrome glassy
- the dense, text-heavy body should lean more solid/plain
- collapse/expand controls should be compact and labeled

### Media / canvas

- floating glass controls are ideal
- add dimming where icons sit over busy media
- use clear-ish treatments only when foreground icons remain bold and contrasty

## Tint and polish

Use tint with meaning: selected, primary, destructive, recording, streaming, or failed. Avoid decorative brand tint on every surface.

Shader-inspired glare, rims, and chromatic edges are optional hero polish. Keep them public-API-first, subtle, and disabled when accessibility or power conditions require it.


## Background extension is not a glass card

Use `backgroundExtensionEffect()` when a hero image, document preview, or media surface should visually continue under a sidebar or inspector. It supports spatial continuity around system chrome; it does not mean the content itself should become a translucent card. Keep readable content on stable backgrounds and reserve Liquid Glass for controls layered above it.
