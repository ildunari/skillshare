---
name: apple-ios-liquid-glass-ux
user-invocable: false
description: "Use when an iOS app should adopt or be reviewed against Apple's Liquid Glass design language on iOS 26+, including SwiftUI glassEffect APIs, UIKit glass surfaces, glass cards, buttons, sheets, tab bars, translucency behavior, accessibility, and fallback behavior. Do not use for general iOS UI work that is not specifically about Liquid Glass."
version: 1.0.0
tags:
  - apple
  - ios26
  - swiftui
  - liquid-glass
  - design-system
  - accessibility
  - animations
  - components
  - tokens
---

# apple-ios-liquid-glass-ux

> **Purpose**

Package a complete, production‑ready Liquid Glass UX kit for iOS 26+. This skill teaches Claude how to build translucent, dynamic UI using Apple’s Liquid Glass APIs. It bundles design tokens, SwiftUI components, accessibility checks, animation presets and thorough documentation. UIKit interop examples demonstrate `UIGlassEffect` for hybrid apps.

> **What this skill does**

• Generates SwiftUI components (cards, buttons, sheets, tab bars, toolbars and navigation views) using Liquid Glass primitives (`glassEffect`, `GlassEffectContainer`, `glassEffectID`).  
• Groups surfaces and coordinates morphing transitions via `glassEffectID`.  
• Produces semantic colour systems, spacing scales and animation presets tuned for glass.  
• Checks accessibility (contrast, Reduce Transparency, Dynamic Type, Clear vs Tinted preference).  
• Provides UIKit examples (`UIGlassEffect`, `UIGlassContainerEffect`) for hybrid apps.  
• Supplies documentation distilling Apple’s guidance from WWDC 2025 sessions 219 (Meet Liquid Glass) and 323 (Build a SwiftUI app with the new design).

> **When to load**

Use this skill in any SwiftUI or UIKit project targeting iOS 26 or later where you want to adopt Liquid Glass. Components include fallbacks for earlier OS versions (iOS 17–25) where feasible.

---

## Overview

Liquid Glass is Apple’s latest translucent design language. It supersedes the older `Material` API by providing a glass surface that refracts and concentrates light, yielding crisper backgrounds and more adaptive contrast. iOS 26 introduces grouping via `GlassEffectContainer`, morphing transitions through `glassEffectID`, and glass‑aware button styles (`.glass`, `.glassProminent`). This skill operationalizes those patterns through reusable components, tokens and guidance.

**Outputs**

- **Components:** SwiftUI views implementing cards, buttons, sheets, tab bars, toolbars, navigation patterns, grouped buttons, morphing transitions and UIKit glass examples.
- **Demo app:** A sample app in `examples/DemoApp` demonstrating the components in context.
- **Design tokens:** JSON and Swift definitions of colours, spacing and animation presets in `design-tokens/`.
- **Scripts:** Python utilities in `scripts/` to generate colours, spacing and animations and validate accessibility.
- **Documentation:** Guides in `docs/` covering principles, component usage, migration, morphing and system integration.
- **Accessibility checklist:** A markdown checklist in `accessibility/` for verifying contrast and preferences.

**Supported stack**

- Swift 5.10+ and SwiftUI targeting iOS 26 or later.
- UIKit interop using `UIGlassEffect` and `UIGlassContainerEffect`.
- JSON tokens compiled into Swift for type‑safe usage.

---

## When to Use Liquid Glass

Liquid Glass is ideal for separating foreground content from rich or dynamic backdrops while keeping context visible. Use it for navigation bars, toolbars, tab bars, cards, panels and sheets. Group related elements so they sample the same background and can morph into one another. Prefer solid surfaces for long‑form text, dense tables or when readability is paramount. Honour accessibility settings—when **Reduce Transparency** is enabled, replace glass with opaque fills.

---

## Design Principles

1. **Hierarchy via style** – Express elevation by choosing the appropriate glass style: `.clear` for light surfaces, `.regular` for standard panels, and `.regular.tint(...)` (`prominent`) for high‑contrast zones. Reserve tints for meaning (primary calls to action or destructive actions).
2. **Group related elements** – Wrap adjacent glass elements in `GlassEffectContainer` to unify sampling and tint. Grouping reduces performance overhead and enables surfaces to merge gracefully.
3. **Coordinate transitions** – Use `glassEffectID` with a shared `@Namespace` to morph surfaces during navigation or state changes. Without IDs, SwiftUI fades surfaces instead of morphing them.
4. **Vibrancy through dynamic colours** – Use `.foregroundStyle(.primary, .secondary, .tertiary)` so the system adjusts contrast on glass. Avoid hardcoded colours.
5. **Motion for meaning** – Animate glass surfaces using springs and effect assignment. Keep interactions subtle (< 250 ms for micro‑interactions) and disable flex/bounce when **Reduce Motion** is on.
6. **Accessibility by design** – Honour **Reduce Transparency**, **Increase Contrast**, **Reduce Motion**, **Clear vs Tinted** preferences and Dynamic Type.

---

## Liquid Glass API Quick Reference

| API | Purpose | Notes |
|---|---|---|
| `glassEffect(_ style: Glass = .regular, in shape: some InsettableShape)` | Apply Liquid Glass to a view with a specific style (`.clear`, `.regular`, `.regular.tint(color)`) and shape (capsule, rounded rect, etc.). | Replaces `.fill(.thinMaterial)` and other Material fills. |
| `GlassEffectContainer(spacing:)` | Group multiple glass elements so they share a sampling region, unify tint and can morph when spacing collapses. | Specify `spacing` to control merge distance. |
| `glassEffectID(_ id: some Hashable, in namespace: Namespace.ID)` | Tag a glass surface for coordinated morphing across views or states. | Source and destination must share the same ID and namespace. |
| `.buttonStyle(.glass)` / `.buttonStyle(.glassProminent)` | Glass‑aware button styles; the prominent variant applies a tint for increased contrast. | Use `.tint(_:)` to override the default accent colour. |
| `UIGlassEffect(style:)` | UIKit class for adding Liquid Glass to `UIView`s. | Set `tintColor` or `isInteractive` for variations. |
| `UIGlassContainerEffect()` | UIKit container that groups multiple glass effect views. | Use to unify sampling and merge surfaces in UIKit hierarchies. |

### Backwards Compatibility

For iOS 17–25, fallback to `.ultraThinMaterial` or `.thinMaterial` and add a light stroke to define edges. The `glassOrMaterial(style:in:)` helper in the documentation shows how to encapsulate this fallback logic.

---

## Components & Examples

The following components illustrate best practices for adopting Liquid Glass:

- **GlassCard** – A flexible card presented on a rounded glass surface. Supports `clear`, `tinted` and `prominent` variants with configurable corner radius and tint opacity.
- **GlassButton** – Semantic buttons using `.glass` and `.glassProminent` styles. Kinds (`primary`, `secondary`, `destructive`) map to tints. Built‑in spring animations handle pressed state.
- **GlassSheet** – A convenience wrapper around `sheet(isPresented:)` that uses the system Liquid Glass background. Compose your sheet’s content inside a `GlassEffectContainer` when grouping controls.
- **GlassTabBar** – A floating tab bar with a glass background and glass‑styled buttons. The selected tab uses `.glassProminent` and the accent colour.
- **GlassToolbarDemo** – Demonstrates navigation and toolbars adopting glass automatically. Buttons use `.glass` styles; avoid painting backgrounds behind system bars.
- **GlassNavigationDemo** – Showcases navigation within a `NavigationStack` with a glass navigation bar and a scrolling list of `GlassCard` items.
- **GlassEffectContainerExample** – Groups multiple glass buttons in a container to illustrate unified sampling and merging.
- **GlassMorphingExample** – Demonstrates morphing between a compact and an expanded glass surface using `glassEffectID` and a spring animation.
- **MaterialVibrancyExamples** – Contrasts correct use of dynamic foreground styles on glass with incorrect hardcoded colours, and provides a UIKit glass example.
- **UIKitGlassExamples** – Embeds `UIGlassEffect` and `UIGlassContainerEffect` in SwiftUI. Shows single and grouped glass surfaces using UIKit.
- **AccessibilityExamples** – Respects **Reduce Transparency** and reports current accessibility settings on glass surfaces.

Explore the demo app (`examples/DemoApp`) to see these components in context.

---

## Migration & Backwards Compatibility

If you’re upgrading from iOS 25 or earlier, follow these steps:

1. **Audit and purge.** Remove old `Material` fills (e.g., `.thinMaterial`, `.regularMaterial`) and any custom blur shaders. Eliminate redundant backgrounds on bars and sheets.
2. **Adopt `glassEffect`.** Replace material fills with `glassEffect` and choose a style (`.clear`, `.regular`, `.regular.tint`). For clusters of controls, use `GlassEffectContainer`.
3. **Coordinate morphs.** Use `glassEffectID` with a shared namespace to morph surfaces during state changes or navigation. Without IDs, SwiftUI will fade surfaces.
4. **Fallback gracefully.** Guard your glass code with `if #available(iOS 26, *)` and provide `.ultraThinMaterial` or solid fills for earlier OS versions.
5. **Respect preferences.** Honour the system’s **Clear vs Tinted** setting, **Reduce Transparency**, **Increase Contrast**, **Reduce Motion** and Dynamic Type. Components in this skill handle these automatically.

For a more detailed migration plan, see `docs/ios26-migration.md`.

---

## System Integration

iOS 26 applies Liquid Glass to system UI elements automatically. Navigation bars, toolbars, tab bars and partial sheets all use glass backgrounds. Avoid painting custom backgrounds behind these bars—doing so can conflict with the system’s scroll‑edge effect. Place your bar buttons and controls using `.buttonStyle(.glass)` or `.glassProminent`. The system’s **Clear vs Tinted** preference adjusts glass opacity across the OS. More details are available in `docs/system-integration.md`.

---

## Further Reading

To deepen your understanding of Liquid Glass, watch Apple’s WWDC 2025 sessions:

- **Session 219 – Meet Liquid Glass:** Introduction to the design language, its physics and high‑level guidelines. 【11843478910321†screenshot】
- **Session 323 – Build a SwiftUI app with the new design:** Walkthrough of the SwiftUI APIs (`glassEffect`, `GlassEffectContainer`, `glassEffectID`) and migration strategies. 【11843478910321†screenshot】
- **Session 284 – Build a UIKit app with the new design:** Guidance on integrating `UIGlassEffect` and `UIGlassContainerEffect` into existing UIKit codebases.

Refer to the bundled document `Liquid_Glass_Complete_Guide_iOS26_macOS26.md` for comprehensive coverage of core concepts, SwiftUI and UIKit APIs, design principles, system preferences, performance advice and migration checklists.
