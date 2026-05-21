# Library evaluation and dependency guidance

Audit date: 2026-05-14. Use this to decide whether to recommend a package. Apple native APIs remain the source of truth for production iOS 26+ apps.

## Classification summary

| Source | Classification | Recommendation |
|---|---|---|
| Apple docs, WWDC, HIG | Production source of truth | Use first. |
| 1amageek/Toolbar | Production-ready candidate for AI composer | Consider if the project wants a package and accepts its API. Strong alignment with iOS 26 composer needs. |
| unionst/union-tab-view | Reference only / avoid unless audited | Consider only when native `TabView`, search role tabs, and bottom accessories cannot express the product requirement. |
| ryanashcraft/FabBar | Snippet/reference only; avoid default dependency | Strong visual idea, but explicitly relies on UIKit internals/hierarchy manipulation. |
| DnV1eX/LiquidGlassKit | Shader inspiration / backport-only / avoid default | Uses private/internal-class-style techniques and older-iOS goal. Not primary for iOS 26. |
| valzevul/Theseus | Shader/backport inspiration only | Good structure and demos, but purpose is iOS 13+ backport, not native iOS 26. |
| muhittincamdali/LiquidGlassKit | Avoid unless audited | README marketing does not match package/platform/code quality enough for production recommendation. |
| muhittincamdali/LiquidGlass-Playground | Reference/playground only | Useful because it claims real iOS 26 APIs; not a dependency. |
| muhittincamdali/SwiftUI-iOS26-Showcase | Reference only | Broad examples; verify snippets before reuse. |
| GetStream/awesome-liquid-glass | Visual gallery/snippet index | Do not treat as dependency advice. |
| conorluddy/LiquidGlassReference | Reference only | Helpful API notes; verify against Apple/Xcode. |
| jaikrishnavj/LiquidGlass-Handbook | Reference/tutorial only | Good learning material; inspect code before copying. |
| artemnovichkov/iOS-26-by-Examples | Reference only | Useful for broad iOS 26 API patterns. |
| mertozseven/LiquidGlassSwiftUI | Reference/sample only | Good sample ideas for expandable buttons and symbol transitions. |
| EmergeTools/Pow | Supporting animation library | Use sparingly for change effects, not as Liquid Glass replacement. |
| twostraws/Inferno | Shader inspiration/support | Educational Metal/SwiftUI shaders; keep separate from core controls. |
| jtrivedi/Wave | Supporting animation library | Useful for UIKit retargetable springs; not needed for standard SwiftUI state animations. |

## Apple native docs and guidance

Production-grade choice. Use `glassEffect`, `GlassEffectContainer`, `glassEffectID`, native button styles, standard tab/search/navigation/sheet APIs, and UIKit public glass APIs. Treat `glassEffectUnion` as an optional SDK-verified refinement rather than a default dependency. Apple guidance frames Liquid Glass as a functional layer for controls and navigation. That matches this skill’s default.

Risk: some documentation pages require JavaScript, and SDK spellings can shift across seeds. Verify code in the installed Xcode 26 SDK.

## 1amageek/Toolbar

Classification: production-ready candidate for an AI composer.

Why:

- Package targets iOS/iPadOS/macOS 26+ and Swift 6.2, matching the primary priority.
- README describes AI chat primitives: multiline editor, attachments, slash commands, voice input, send/stop buttons, waveform, popup, and one continuous glass slab.
- The design philosophy says one slab/one morph domain, which aligns with Apple-style Liquid Glass grouping.
- Useful as either a dependency or design reference when building a ChatGPT/agent composer.

Cautions:

- Review public API stability and exact dependency footprint before adding.
- Still generate native self-contained code first unless the user asks for a package.

## unionst/union-tab-view

Classification: reference only / avoid unless audited.

Why:

- Solves a specific problem: custom tab item rendering in a Liquid Glass-style bar.
- Still recreates tab behavior instead of using the native iOS 26 tab/search/accessory system.
- Useful only if native `TabView`, search-role tabs, bottom accessories, and toolbar search items cannot support the product requirement.

Cautions:

- Native `TabView` should remain default for app navigation.
- Audit accessibility semantics, tab reselection, VoiceOver focus, search semantics, safe-area behavior, and OS update resilience before shipping.

## Ryan Ashcraft FabBar

Classification: snippet/reference only; avoid default dependency.

Why:

- Strong visual and product thinking for a floating tab bar plus FAB.
- README and source are transparent about using UIKit internals and hierarchy manipulation.
- Source inspects internal classes such as `_UILiquidLensView`, which is brittle and risky for production.
- Known limitations include VoiceOver focus, native tab reselection, hardcoded dimensions, and Large Content Viewer behavior.

Use it for:

- Visual composition ideas.
- Understanding why native `.role(.search)` tab abuse can be semantically wrong.
- Sketching a custom tab bar if the project accepts the risk and runs a full accessibility audit.

Do not use it as the default recommendation.

## DnV1eX/LiquidGlassKit

Classification: shader inspiration / backport-only / avoid default dependency.

Why:

- Purpose is bringing an iOS 26-like effect to iOS 13–18, which conflicts with this skill’s iOS 26-native priority.
- Repository includes Metal/refraction/chromatic dispersion/Fresnel/glare ideas that are useful for inspiration.
- Code references private/internal-class-style approaches and CABackdrop-like behavior. That raises App Store and maintenance risk.
- Small commit history and no broad demo structure observed.

Use it for:

- Math ideas around dispersion, Fresnel, glare, and shape merging.
- Understanding GPU cost tradeoffs.

Do not ship it as a default dependency for iOS 26+ native Liquid Glass.

## valzevul/Theseus

Classification: shader/backport inspiration only.

Why:

- Purpose is iOS 13+ backport with Metal rendering and UIKit components.
- Better structure than many backport repos: Sources, Tests, UIKit demo, SwiftUI demo, accessibility/low-power notes.
- Still not primary for iOS 26 because native APIs should own the interaction and material.

Use it for:

- UIKit/Metal architecture ideas.
- Backport-only projects when the user explicitly asks for old OS support.

## muhittincamdali/LiquidGlassKit

Classification: avoid unless audited.

Concrete findings:

- README claims “iOS 26.0+,” “Swift 6.0,” “25+ production-ready components,” CI, coverage, and broad component surface.
- Package.swift actually lists iOS 15, macOS 12, tvOS 15, watchOS 8, visionOS 1, and Swift language version 5.
- Source files observed were compressed/minified into very long lines, which hurts reviewability.
- Core implementation uses `.ultraThinMaterial` overlays, blur-style abstractions, and custom cards rather than native iOS 26 `glassEffect` as the primary path.
- README encourages glass cards/lists/grids broadly, which conflicts with Apple’s “controls/navigation layer” design guidance.
- Low star/fork count is not itself a problem, but the mismatch between claims, package metadata, and implementation is.

Recommendation: do not recommend as a production dependency. If a user already depends on it, audit every symbol, platform target, tests, private API usage, and accessibility behavior before continuing.

## Pow, Inferno, and Wave

Pow: supporting SwiftUI transitions and change effects. Useful for delight on likes, success, small state changes. Prefer native symbol transitions and springs for core Liquid Glass behavior.

Inferno: shader education and optional Metal effects. Good for isolated hero/canvas effects. Do not use for ordinary glass controls.

Wave: retargetable spring engine for UIKit/SwiftUI/AppKit. Useful for custom drag-heavy UIKit components. Standard SwiftUI springs are enough for most generated code.

## Dependency decision tree

1. Can native SwiftUI/UIKit express the component? Use native.
2. Is the requested component an AI composer and the user accepts a package? Consider 1amageek/Toolbar.
3. Is the requested component a custom tab bar beyond native `TabView`? Consider union-tab-view after accessibility audit.
4. Is the user asking for old iOS backports? Consider Theseus only after explaining tradeoffs.
5. Is the request for shader look only? Use Inferno/DnV1eX/Theseus/Shadertoy as inspiration, not a default dependency.
6. Does the package use private classes, KVC on private layers, or hidden UIKit hierarchy assumptions? Avoid unless the user explicitly accepts the risk.

## Uploaded research artifacts

The uploaded `deep-research-report.md`, `deep-research-report-1.md`, and alternate package zips were summarized in `references/research-addendum.md` rather than shipped as bulky raw artifacts. Their useful additions were folded into API routing, search/tab/sheet guidance, and dependency classification. They are not direct runtime dependencies.
