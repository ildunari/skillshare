# Sources and research notes

Use Apple documents and videos as source of truth. Community repos are inspiration unless their code is public-API-safe, actively maintained, and aligned with iOS 26 native behavior.

## Apple native docs and official guidance

- Apple Developer Documentation — `glassEffect`: https://developer.apple.com/documentation/swiftui/glasseffect
  - Native SwiftUI entry point for applying Liquid Glass to custom views.
- Apple Developer Documentation — `GlassEffectContainer`: https://developer.apple.com/documentation/swiftui/glasseffectcontainer
  - Group multiple glass views so the system can blend/morph them coherently.
- Apple Developer Documentation — `NavigationTransition`: https://developer.apple.com/documentation/swiftui/navigationtransition
  - Use zoom transitions and matched transition sources for continuity between list/grid and detail views.
- Apple Developer Documentation — previews in Xcode: https://developer.apple.com/documentation/swiftui/previews-in-xcode
  - Generate previews for every reusable component.
- Apple Developer Documentation — Applying Liquid Glass to custom views: https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views
  - Custom view guidance for `glassEffect`, containers, IDs, and transitions.
- Apple Technology Overview — Liquid Glass: https://developer.apple.com/documentation/technologyoverviews/liquid-glass
  - Use for the platform-level design rationale.
- Apple Technology Overview — Adopting Liquid Glass: https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
  - Adoption and migration framing; standard components first.
- Apple Landmarks tutorial with Liquid Glass: https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass
  - Useful for practical SwiftUI composition and previews.
- Apple Landmarks — Refining the system-provided glass effect in toolbars: https://developer.apple.com/documentation/SwiftUI/Landmarks-Refining-the-system-provided-glass-effect-in-toolbars
  - Toolbar grouping and refinements.
- WWDC25 — Meet Liquid Glass: https://developer.apple.com/videos/play/wwdc2025/219/
  - Best source for where Liquid Glass belongs: controls/navigation/overlays, not every content card.
- WWDC25 — Build a SwiftUI app with the new design: https://developer.apple.com/videos/play/wwdc2025/323/
  - App migration, tab bars, sidebar/toolbars, sheet morphing, scroll edge behavior.
- WWDC25 — Build a UIKit app with the new design: https://developer.apple.com/videos/play/wwdc2025/284/
  - UIKit glass effects, interruptible navigation transitions, UIKit symbol transitions.
- WWDC25 — Get to know the new design system: https://developer.apple.com/videos/play/wwdc2025/356/
  - Design-system framing, hierarchy, and Liquid Glass restraint.
- Apple HIG materials: https://developer.apple.com/design/human-interface-guidelines/materials
  - Use for accessibility and contrast behavior around transparency.
- Apple New Design Gallery: https://developer.apple.com/design/new-design-gallery/
  - Visual examples from production apps using Liquid Glass controls and navigation.
- Apple New Design Gallery 2026: https://developer.apple.com/design/new-design-gallery-2026/
  - Real app examples and source-linked/floating control patterns.

- Apple Developer Documentation — `safeAreaBar(edge:alignment:spacing:content:)`: https://developer.apple.com/documentation/swiftui/view/safeareabar%28edge%3Aalignment%3Aspacing%3Acontent%3A%29
  - Native iOS 26 custom bar placement. Useful for composers and bottom controls when the SDK exposes the overload.
- Apple Developer Documentation — `backgroundExtensionEffect()`: https://developer.apple.com/documentation/SwiftUI/View/backgroundExtensionEffect%28%29
  - Extends and mirrors a view around its edges so imagery can continue under sidebars/inspectors.
- Apple Landmarks — Applying a background extension effect: https://developer.apple.com/documentation/SwiftUI/Landmarks-Applying-a-background-extension-effect
  - Practical image/header use case for `backgroundExtensionEffect()`.
- Apple Developer Documentation — `UIDesignRequiresCompatibility`: https://developer.apple.com/documentation/BundleResources/Information-Property-List/UIDesignRequiresCompatibility
  - Temporary compatibility-mode key for migration planning; not a normal generated-UI path.

## Practical tutorials and articles

- Donny Wals — Designing custom UI with Liquid Glass on iOS 26: https://www.donnywals.com/designing-custom-ui-with-liquid-glass-on-ios-26/
  - Practical SwiftUI examples for `glassEffect`, interactive glass, tint, and custom controls.
- Donny Wals — Grouping Liquid Glass components using `glassEffectUnion`: https://www.donnywals.com/grouping-liquid-glass-components-using-glasseffectunion-on-ios-26/
  - Useful for unioning separated controls into one visual domain. Verify API spelling in the active SDK and prefer `GlassEffectContainer` + `glassEffectID` for default generated code.
- Donny Wals — Exploring tab bars on iOS 26 with Liquid Glass: https://www.donnywals.com/exploring-tab-bars-on-ios-26-with-liquid-glass/
  - Tab behavior and native tab bar adaptation.
- Swift with Majid — Glassifying tabs in SwiftUI: https://swiftwithmajid.com/2025/06/24/glassifying-tabs-in-swiftui/
  - Native tab APIs, bottom accessories, search-role tab patterns.
- Swift with Majid — Glassifying custom SwiftUI views: https://swiftwithmajid.com/2025/07/16/glassifying-custom-swiftui-views/
  - Compact custom glass view examples.
- Nil Coalescing — Presenting Liquid Glass sheets in SwiftUI: https://nilcoalescing.com/blog/PresentingLiquidGlassSheetsInSwiftUI/
  - Sheet presentation behavior and system backgrounds.
- Nil Coalescing — Liquid Glass sheets with NavigationStack and Form: https://nilcoalescing.com/blog/LiquidGlassSheetsWithNavigationStackAndForm/
  - Form/navigation caveats inside sheets.
- Nil Coalescing — SwiftUI search enhancements in iOS and iPadOS 26: https://nilcoalescing.com/blog/SwiftUISearchEnhancementsIniOSAndiPadOS26/
  - Search placement changes and bottom toolbar search.
- SerialCoder — Transforming glass views with `glassEffectID`: https://serialcoder.dev/text-tutorials/swiftui/transforming-glass-views-with-the-glasseffectid-modifier-in-swiftui/
  - Morphing mechanics and identity continuity.
- SerialCoder — Morphing sheets out of buttons in SwiftUI: https://serialcoder.dev/text-tutorials/swiftui/morphing-sheets-out-of-buttons-in-swiftui/
  - Source-linked presentation patterns.
- Create with Swift — Exploring a new visual language: Liquid Glass: https://www.createwithswift.com/exploring-a-new-visual-language-liquid-glass/
  - Design-language framing.
- Create with Swift — Liquid Glass hierarchy, harmony, and consistency: https://www.createwithswift.com/liquid-glass-redefining-design-through-hierarchy-harmony-and-consistency/
  - Useful design summary.
- Ryan Ashcraft — Introducing FabBar: https://ryanashcraft.com/introducing-fabbar/
  - Useful visual exploration of floating tab bar plus FAB. Treat implementation carefully because the package manipulates UIKit internals.

## Visual/sample/gallery/reference sources

- liquidglass-kit.dev: https://liquidglass-kit.dev/
  - Visual component inspiration only; translate into native SwiftUI/UIKit.
- GetStream awesome-liquid-glass: https://github.com/GetStream/awesome-liquid-glass
  - Gallery/snippet collection. Do not treat as a production dependency list.
- LiquidGlass Handbook: https://github.com/jaikrishnavj/LiquidGlass-Handbook
  - Reference/tutorial value; inspect code before copying.
- LiquidGlassReference: https://github.com/conorluddy/LiquidGlassReference
  - API reference-style notes; verify against Apple docs/Xcode SDK.
- iOS 26 by Examples: https://github.com/artemnovichkov/iOS-26-by-Examples
  - Broad iOS 26 examples; use to compare API usage patterns.
- LiquidGlassSwiftUI: https://github.com/mertozseven/LiquidGlassSwiftUI
  - Sample app with quote card, expandable buttons, symbol transitions.
- LiquidGlass Playground: https://github.com/muhittincamdali/LiquidGlass-Playground
  - Playground using real iOS 26 APIs; useful for quick experiments.
- SwiftUI iOS26 Showcase: https://github.com/muhittincamdali/SwiftUI-iOS26-Showcase
  - Broad API showcase. Use selectively; verify every snippet.

## Component libraries

- DnV1eX/LiquidGlassKit: https://github.com/DnV1eX/LiquidGlassKit
  - Backport/shader inspiration. Avoid as a default production dependency because it uses private/internal-class-style techniques.
- valzevul/Theseus: https://github.com/valzevul/Theseus
  - Backport and shader/motion reference. Not a replacement for native iOS 26 APIs.
- ryanashcraft/FabBar: https://github.com/ryanashcraft/FabBar
  - Visual/API inspiration for tab bar plus FAB. Avoid default dependency without project-specific audit due internal UIKit hierarchy manipulation.
- 1amageek/Toolbar: https://github.com/1amageek/Toolbar
  - Strong AI composer reference. iOS 26+ Swift package with a coherent glass slab and composer primitives.
- unionst/union-tab-view: https://github.com/unionst/union-tab-view
  - Custom SwiftUI tab item package for Liquid Glass-style tab bars. Consider only when native `TabView` cannot express the design.
- muhittincamdali/LiquidGlassKit: https://github.com/muhittincamdali/LiquidGlassKit
  - Marketing-heavy; README claims do not match Package.swift platform targets and code quality. Treat as avoid unless audited.

## Animation / morph / shader libraries

- EmergeTools/Pow: https://github.com/EmergeTools/Pow and https://movingparts.io/pow
  - SwiftUI transitions/change effects. Use sparingly for delight; not a Liquid Glass replacement.
- twostraws/Inferno: https://github.com/twostraws/Inferno
  - Metal shader education and effect snippets. Keep separate from core Liquid Glass controls.
- jtrivedi/Wave: https://github.com/jtrivedi/Wave
  - Retargetable spring animation ideas, especially for UIKit-driven drag interactions.
- Shadertoy: https://www.shadertoy.com/
  - Shader inspiration only; never paste GLSL into production SwiftUI without porting, testing, and accessibility review.

## Community and learning

- Kavsoft: https://www.youtube.com/@Kavsoft
- DesignCode SwiftUI Handbook: https://designcode.io/swiftui-handbook
- Swift Playgrounds: https://apps.apple.com/us/app/swift-playgrounds/id1496833156

Use these for learning and visual language, not as authoritative API references.

## Uploaded research artifacts

- external deep-research report artifact
  - Added for long-form context on tab/search/sheet APIs, UIKit mapping, and conservative library classification.
- external follow-up deep-research report artifact
  - Added for long-form context on AI-agent UI recipes, component taxonomy, and visual/design guidance.
- `references/research-addendum.md`
  - Concise summary of what was integrated from the uploaded reports and package zips.
- `references/source-evaluation.md`
  - Additional classification for official docs, tutorials, visual references, community discussions, and the latest pasted/zip artifact.
