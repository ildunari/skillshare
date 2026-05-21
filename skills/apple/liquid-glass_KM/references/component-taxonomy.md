# Component taxonomy

Use this file to choose the right Liquid Glass pattern before writing code. The goal is native iOS 26 chrome, not generic glassmorphism.

## Root navigation

- Native `TabView`
- Search-role tab
- Tab bar minimization on scroll
- Tab view bottom accessory
- UIKit tab bottom accessory
- Navigation zoom from list/grid/source to detail
- Native toolbar/search items before custom tab recreation

## Local action chrome

- Floating toolbar
- Bottom composer shell
- Quick actions strip
- Contextual segmented controls
- Morphing action cluster
- Edge handle for collapsible panel
- Command palette launcher

## Search and filtering

- Native `.searchable`
- Bottom search toolbar item
- Search-role tab for first-class search surfaces
- Filter pill row
- Scope control
- Sort/menu capsule

## Agent UI

- Bottom composer
- Attachment chip strip
- Send/stop/voice trailing action
- Tool row
- Thread/session list overlay controls
- Agent status pills
- Tool-call chips
- Reasoning collapse controls
- Active tool summary strip
- Active-agent tab accessory

## Content accompaniment

- Markdown action chrome
- Inline copy/share/save controls
- Selection/action pills
- Lightweight status metadata
- Plain content body with glass controls nearby

## Media and canvas

- Image/PDF/video edge toolbar
- Zoom/fit/page controls
- Annotation/action cluster
- Thumbnail selection strip
- Canvas mode switcher
- Floating export/share buttons
- Thumbnail-to-canvas zoom transition

## Transient UI

- Popovers
- Partial-detent sheets
- Source-linked menus
- Dialog actions
- Command palette
- Radial menu
- Teaching overlays

## Motion system

- Symbol replacement
- Glass morphing through `glassEffectID`
- Zoom navigation
- Interruptible drag springs
- Streaming/thinking microinteractions
- Selection state transitions
- Optional, public-API shader-inspired highlight

## Avoid patterns

- Glass every list row
- Glass every chat bubble
- Glass around dense markdown/code blocks
- Custom tab bar before native tab/search/accessory APIs
- Always-on shader effects over scrolling content
- Private UIKit class/layer probing
