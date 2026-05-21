# Gallery index

Use this as a visual scan guide before opening snippets or recipes.

| Component | Looks like | Use when | Primary file |
|---|---|---|---|
| AI chat composer | Bottom glass slab with attach/tools/input/send/stop/voice | AI chat and agent prompting | `recipes/ChatComposerRecipe.swift` |
| Thread list controls | Plain rows with floating search/filter/action chrome | Session switching, thread management | `recipes/ThreadListRecipe.swift` |
| Native search + accessory | Native tabs/search with compact active-agent strip | Root navigation that needs search and status | `recipes/NativeSearchAccessoryRecipe.swift` |
| Glass tab bar + FAB | Native tab flow with one floating primary action | Root nav plus compose/create action | `recipes/BottomTabBarFABRecipe.swift` |
| Floating toolbar | Compact bottom/edge action capsule over content | Readers, feeds, canvases | `recipes/FloatingToolbarRecipe.swift` |
| Tool-call/reasoning panel | Glass header/edge controls with mostly plain body | Agent reasoning, tool logs, retries | `recipes/ToolCallReasoningPanelRecipe.swift` |
| Media canvas controls | Glass edge controls over images/PDF/video | Preview, annotate, share, zoom | `recipes/MediaCanvasControlsRecipe.swift` |
| Morphing button cluster | Single action expands into related controls | Attachments, tools, command menus | `recipes/MorphingButtonClusterRecipe.swift` |
| Command palette sheet | Partial-detent sheet with glass bottom command row | Agent command surfaces | `snippets/28-source-linked-sheet-command-palette.swift` |
| Adaptive glass shell | Glass that becomes opaque/restrained for accessibility | Any reusable custom glass component | `snippets/26-adaptive-glass-accessibility.swift` |
| UIKit bridge | UIKit glass accessory / tab accessory bridge | Existing UIKit screens | `snippets/27-uikit-glass-effect-bridge.swift` |
| Shader-inspired accents | Subtle glare, rim, chromatic edge using public APIs | Hero controls only | `snippets/20-shader-inspired-highlights.swift` |

## Source inspiration

- Apple docs and WWDC: system truth for component behavior.
- Donny Wals / Swift with Majid / Nil Coalescing / SerialCoder: practical SwiftUI routing and presentation patterns.
- 1amageek/Toolbar: AI composer reference.
- Pow/Wave/Inferno: optional motion or shader inspiration, not base glass implementations.

## Visual rule of thumb

A screen should usually read as: content layer + one glass control layer + transient overlay layer. If it reads as glass everywhere, remove surfaces before adding polish.

| Background extension bar | Media/detail view whose image backdrop continues under sidebars/inspectors plus a bottom composer bar | Split views, canvases, media previews | `snippets/29-background-extension-safe-area-bars.swift` |
