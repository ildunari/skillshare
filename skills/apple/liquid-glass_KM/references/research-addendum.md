# Research addendum from uploaded artifacts

This addendum records the useful deltas from the two uploaded deep-research reports and alternate package zips. It is background context, not a replacement for Apple docs or the active Xcode 26 SDK.

## Integrated conclusions

- Treat Liquid Glass as a system-native control, navigation, and overlay layer. This reinforces the existing skill rule against boxing every chat message, markdown block, card, or list row in glass.
- Prefer standard bars, sheets, search, tab bars, segmented controls, and buttons before custom glass. Custom glass should usually be compact and actionable.
- Use `GlassEffectContainer` plus `glassEffectID` as the default morphing/coherence path. Treat `glassEffectUnion` as SDK-verified/optional rather than the default because community writeups surfaced it more inconsistently than Apple’s core container and ID APIs.
- Add search/tab/bottom-accessory guidance: `Tab(role: .search)`, `.searchable`, `tabViewBottomAccessory`, `tabBarMinimizeBehavior`, bottom search toolbar items, and toolbar spacers are first-class native options before custom tab/search bars.
- Add sheet/popover guidance: partial-detent sheets and source-linked presentations usually get the new system treatment automatically; avoid overriding sheet backgrounds unless the design intentionally opts out.
- Keep UIKit bridge snippets conservative: `UIGlassEffect`, `UIGlassContainerEffect`, `UIVisualEffectView`, and glass button configurations are safer defaults than beta-era or forum-contested corner-shaping APIs.
- Keep shader-inspired effects public-API-first and decorative. Use Metal snippets only for isolated hero/canvas effects, never as the base Liquid Glass implementation.

## Uploaded artifact handling

The uploaded markdown reports were inspected as source material, but bulky raw research artifacts stay outside the shipped skill package. The alternate package zips were summarized rather than copied wholesale, because duplicating competing SKILL.md files inside the active skill would create confusing trigger and implementation guidance.

## Package deltas applied

- Updated `SKILL.md` to de-emphasize `glassEffectUnion` and add native tab/search/sheet priorities.
- Expanded `references/api-map.md` with search-role tabs, bottom accessories, bottom search items, partial-detent sheets, and UIKit glass mapping.
- Expanded `references/sources.md` with additional practical sources: Swift with Majid, Nil Coalescing, SerialCoder, Create with Swift, WWDC new design sessions, and the new Apple design gallery links from the reports.
- Added snippets for native search/tabs/accessories, adaptive accessibility glass, and UIKit bridge usage.
- Added a recipe for native search/accessory composition and expanded eval/trigger coverage.

## Caution notes

- Do not import alternate package snippets blindly. Some snippets use broad glass backgrounds, aggressive `.glassEffectUnion`, or older fallback mental models that are weaker than the native-first defaults in this skill.
- Do not downgrade an iOS 26-first implementation to `.ultraThinMaterial` backports unless the user explicitly asks for older OS support.
- Verify API spelling against the installed Xcode 26 SDK before shipping, especially for newly documented or beta-era SwiftUI modifiers.


## Second follow-up upload integration

The latest pasted markdown and `files-1f1f93fe.zip` were handled as reference input rather than as a replacement skill. The active skill kept its validated frontmatter and existing native-first structure.

Integrated deltas:

- Added `references/source-evaluation.md` to separate official docs, practical tutorials, creative animation references, and community pitfall sources.
- Added `backgroundExtensionEffect()` guidance for sidebars/inspectors and media surfaces. Apple documents it as a SwiftUI view modifier that duplicates a view into mirrored copies around edges, and the Landmarks guide uses it to blur and extend imagery under a sidebar or inspector.
- Strengthened `safeAreaBar` guidance for iOS 26 bottom composers and floating bars, while keeping `safeAreaInset` as the broad, stable fallback path.
- Added `UIDesignRequiresCompatibility` as a migration/temporary opt-out note. It should not be used as an implementation strategy for generated Liquid Glass components.
- Added `snippets/29-background-extension-safe-area-bars.swift` to show public-API usage for media/sidebar continuity and bottom composer chrome.

Rejected deltas:

- Did not import the uploaded package’s `SKILL.md` because its frontmatter uses unsupported keys and a non-kebab-case name.
- Did not replace existing composer snippets with the alternate versions because some mix native Liquid Glass with older material-underlay thinking. The active package keeps native glass first and fallback material only behind availability/adaptive branches.
