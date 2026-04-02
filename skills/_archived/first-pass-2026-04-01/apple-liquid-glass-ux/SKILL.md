---
name: apple-liquid-glass-ux
user-invocable: false
description: "Use when an Apple-platform app should adopt or be reviewed against Liquid Glass across iOS 26+, macOS 26+, tvOS 26+, or watchOS 26+, including SwiftUI glassEffect APIs, UIKit or AppKit glass surfaces, cross-platform glass components, transitions, tokens, and accessibility. Prefer the platform-specific Liquid Glass skills when the request is only for iOS or only for one platform."
version: 2.0.0
tags:
  - apple
  - ios26
  - macos26
  - tvos26
  - watchos26
  - swiftui
  - uikit
  - appkit
  - liquid-glass
  - design-system
  - accessibility
  - animations
  - components
  - tokens
  - cross-platform
---

# apple-liquid-glass-ux

> **Purpose**

Package a complete, production‑ready Liquid Glass UX kit for iOS 26+, macOS 26+, tvOS 26+, and watchOS 26+. This skill teaches Claude how to build translucent, dynamic UI using Apple's Liquid Glass APIs across all Apple platforms. It bundles design tokens, SwiftUI components, accessibility checks, animation presets and thorough documentation. UIKit interop examples demonstrate `UIGlassEffect` for iOS hybrid apps, and AppKit examples show `NSGlassEffectView` for macOS apps.

> **What this skill does**

• Generates SwiftUI components (cards, buttons, sheets, tab bars, toolbars and navigation views) using Liquid Glass primitives (`glassEffect`, `GlassEffectContainer`, `glassEffectID`) that work across all Apple platforms.
• Groups surfaces and coordinates morphing transitions via `glassEffectID`.
• Produces semantic colour systems, spacing scales and animation presets tuned for glass.
• Checks accessibility (contrast, Reduce Transparency, Dynamic Type, Clear vs Tinted preference).
• Provides UIKit examples (`UIGlassEffect`, `UIGlassContainerEffect`) for iOS/iPadOS hybrid apps.
• Provides AppKit examples (`NSGlassEffectView`, `NSBackgroundExtensionView`) for macOS apps.
• Supplies documentation distilling Apple's guidance from WWDC 2025 sessions 219 (Meet Liquid Glass) and 323 (Build a SwiftUI app with the new design).

> **When to load**

Use this skill in any SwiftUI, UIKit, or AppKit project targeting iOS 26+, macOS 26+, tvOS 26+, or watchOS 26+ where you want to adopt Liquid Glass. Components include fallbacks for earlier OS versions where feasible.

---

## Overview

Liquid Glass is Apple's latest translucent design language available across all Apple platforms. It supersedes the older `Material` API by providing a glass surface that refracts and concentrates light, yielding crisper backgrounds and more adaptive contrast. iOS 26, macOS 26, tvOS 26, and watchOS 26 introduce grouping via `GlassEffectContainer`, morphing transitions through `glassEffectID`, and glass‑aware button styles (`.glass`, `.glassProminent`). This skill operationalizes those patterns through reusable components, tokens and guidance.

**Supported Platforms:**
- iOS 26.0+ / iPadOS 26.0+
- macOS 26.0+
- tvOS 26.0+
- watchOS 26.0+

All core SwiftUI APIs work across platforms with automatic platform adaptation.
Platform-specific APIs: UIKit (iOS/iPadOS), AppKit (macOS).

**Outputs**

- **Components:** SwiftUI views implementing cards, buttons, sheets, tab bars, toolbars, navigation patterns, grouped buttons, morphing transitions, UIKit glass examples, and AppKit glass examples.
- **Demo app:** A sample app in `examples/DemoApp` demonstrating the components in context across platforms.
- **Design tokens:** JSON and Swift definitions of colours, spacing and animation presets in `design-tokens/`.
- **Scripts:** Python utilities in `scripts/` to generate colours, spacing and animations and validate accessibility.
- **Documentation:** Guides in `docs/` covering principles, component usage, migration, morphing, system integration, and platform-specific patterns.
- **Accessibility checklist:** A markdown checklist in `accessibility/` for verifying contrast and preferences.

**Supported stack**

- Swift 5.10+ and SwiftUI targeting iOS 26+, macOS 26+, tvOS 26+, or watchOS 26+
- UIKit interop using `UIGlassEffect` and `UIGlassContainerEffect` (iOS/iPadOS)
- AppKit interop using `NSGlassEffectView` and `NSBackgroundExtensionView` (macOS)
- Cross-platform SwiftUI components with availability checks
- JSON tokens compiled into Swift for type‑safe usage

---

## When to Use Liquid Glass

Liquid Glass is ideal for separating foreground content from rich or dynamic backdrops while keeping context visible. Use it for navigation bars, toolbars, tab bars, cards, panels and sheets. Group related elements so they sample the same background and can morph into one another. Prefer solid surfaces for long‑form text, dense tables or when readability is paramount. Honour accessibility settings—when **Reduce Transparency** is enabled, replace glass with opaque fills.

---

## Design Principles

1. **Hierarchy via style** – Express elevation by choosing the appropriate glass style: `.clear` for light surfaces, `.regular` for standard panels, and `.regular.tint(...)` (`prominent`) for high‑contrast zones. Reserve tints for meaning (primary calls to action or destructive actions).
2. **Group related elements** – Wrap adjacent glass elements in `GlassEffectContainer` to unify sampling and tint. Grouping reduces performance overhead and enables surfaces to merge gracefully.
3. **Coordinate transitions** – Use `glassEffectID` with a shared `@Namespace` to morph surfaces during navigation or state changes. Without IDs, SwiftUI fades surfaces instead of morphing them.
4. **Vibrancy through dynamic colours** – Use `.foregroundStyle(.primary, .secondary, .tertiary)` so the system adjusts contrast on glass. Avoid hardcoded colours.
5. **Motion for meaning** – Animate glass surfaces using springs and effect assignment. Keep interactions subtle (< 250 ms for micro‑interactions) and disable flex/bounce when **Reduce Motion** is on.
6. **Accessibility by design** – Honour **Reduce Transparency**, **Increase Contrast**, **Reduce Motion**, **Clear vs Tinted** preferences and Dynamic Type.

---

## Liquid Glass API Quick Reference

### SwiftUI APIs (Cross-Platform)

| API | Purpose | Availability | Notes |
|---|---|---|---|
| `glassEffect(_ style: Glass = .regular, in shape: some InsettableShape)` | Apply Liquid Glass to a view with a specific style (`.clear`, `.regular`, `.regular.tint(color)`) and shape (capsule, rounded rect, etc.). | iOS 26+, macOS 26+, tvOS 26+, watchOS 26+ | Replaces `.fill(.thinMaterial)` and other Material fills. |
| `GlassEffectContainer(spacing:)` | Group multiple glass elements so they share a sampling region, unify tint and can morph when spacing collapses. | iOS 26+, macOS 26+, tvOS 26+, watchOS 26+ | Specify `spacing` to control merge distance. |
| `glassEffectID(_ id: some Hashable, in namespace: Namespace.ID)` | Tag a glass surface for coordinated morphing across views or states. | iOS 26+, macOS 26+, tvOS 26+, watchOS 26+ | Source and destination must share the same ID and namespace. |
| `.buttonStyle(.glass)` / `.buttonStyle(.glassProminent)` | Glass‑aware button styles; the prominent variant applies a tint for increased contrast. | iOS 26+, macOS 26+, tvOS 26+, watchOS 26+ | Use `.tint(_:)` to override the default accent colour. |
| `ConcentricRectangle` | Shape that creates concentric rounded rectangles matching container curvature. | iOS 26+, macOS 26+, tvOS 26+, watchOS 26+ | Use for controls that should nest concentrically in panels. |
| `backgroundExtensionEffect()` | Extends content appearance under sidebars/inspectors without scrolling. | iOS 26+, macOS 26+ | Creates edge-to-edge content feel with legibility. |
| `safeAreaBar(edge:alignment:spacing:content:)` | Register custom bars to use scroll edge effects. | iOS 26+, macOS 26+ | Maintains legibility when content scrolls beneath bars. |

### UIKit APIs (iOS/iPadOS)

| API | Purpose | Availability | Notes |
|---|---|---|---|
| `UIGlassEffect(style:)` | UIKit class for adding Liquid Glass to `UIView`s. | iOS 26+, iPadOS 26+ | Set `tintColor` or `isInteractive` for variations. |
| `UIGlassContainerEffect()` | UIKit container that groups multiple glass effect views. | iOS 26+, iPadOS 26+ | Use to unify sampling and merge surfaces in UIKit hierarchies. |
| `UIButton.Configuration.glass()` | Glass button configuration for UIKit buttons. | iOS 26+, iPadOS 26+ | Standard glass appearance. |
| `UIButton.Configuration.prominentGlass()` | Prominent glass button configuration. | iOS 26+, iPadOS 26+ | High-contrast variant. |
| `UIBackgroundExtensionView` | UIKit view for background extension effects. | iOS 26+, iPadOS 26+ | Extends backgrounds under sidebars. |

### AppKit APIs (macOS)

| API | Purpose | Availability | Notes |
|---|---|---|---|
| `NSGlassEffectView` | AppKit view for adding Liquid Glass to macOS windows and views. | macOS 26+ | NSView subclass for native macOS glass integration. |
| `NSBackgroundExtensionView` | Extends backgrounds under sidebars and inspectors. | macOS 26+ | Creates seamless edge-to-edge content in split views. |
| `NSButton.BezelStyle.glass` | Glass button style for AppKit. | macOS 26+ | Native macOS button appearance with glass. |

### Backwards Compatibility

For iOS 17–25 and macOS 14-15, fallback to `.ultraThinMaterial` or `.thinMaterial` and add a light stroke to define edges. The `glassOrMaterial(style:in:)` helper shows how to encapsulate this fallback logic.

```swift
extension View {
    func glassOrMaterial(style: Glass = .regular, shape: some InsettableShape = RoundedRectangle(cornerRadius: 12)) -> some View {
        if #available(iOS 26, macOS 26, *) {
            self.glassEffect(style, in: shape)
        } else {
            self
                .background(.ultraThinMaterial, in: shape)
                .overlay {
                    shape.strokeBorder(.white.opacity(0.2), lineWidth: 0.5)
                }
        }
    }
}
```

---

## Platform-Specific Guidance

### iOS/iPadOS Patterns

**Navigation & Bars:**
- Tab bars automatically adopt glass with adaptive behavior
- Navigation bars use glass backgrounds
- Toolbars integrate glass with scroll edge effects
- Use `.buttonStyle(.glass)` for toolbar buttons

**Sheets & Modals:**
- Sheets automatically use glass backgrounds
- Half sheets are inset to show content beneath
- Action sheets originate from source view
- Use `GlassEffectContainer` to group controls in sheets

**Search:**
- Search fields in toolbars adopt glass
- Separate search tabs in tab bars
- Use semantic search tab role

### macOS Patterns

**Window Chrome:**
- Windows adopt rounder corners automatically
- Glass integrates with standard window controls (traffic lights)
- Sidebars and inspectors use glass backgrounds
- Use `.windowStyle(.hiddenTitleBar)` for modern glass windows

**Split Views:**
- `NavigationSplitView` supports glass sidebars and inspectors
- Use `backgroundExtensionEffect()` for content extending under sidebars
- Split views support continuous resizing
- Use `inspector(isPresented:content:)` for glass inspector panels

**AppKit Integration:**
```swift
import AppKit

class GlassViewController: NSViewController {
    override func loadView() {
        let glassView = NSGlassEffectView(frame: NSRect(x: 0, y: 0, width: 300, height: 400))
        self.view = glassView

        // Add content on top of glass
        let label = NSTextField(labelWithString: "macOS Glass Surface")
        glassView.addSubview(label)
    }
}
```

**Sidebar Patterns:**
- Use `NSGlassEffectView` for sidebar backgrounds
- Combine with `NSSplitViewController` for glass split views
- Traffic lights automatically position over glass surfaces
- Use `NSBackgroundExtensionView` for edge-to-edge content

### tvOS Patterns

**Focus-Aware Effects:**
- Glass activates when elements gain focus
- Standard buttons automatically adopt glass on focus
- Use `.focusable()` for custom controls
- Requires Apple TV 4K (2nd generation) or newer

**Implementation:**
```swift
Button("Action") {
    // action
}
.buttonStyle(.glass)
.focusable()  // Enables glass effect on focus
```

### watchOS Patterns

**Minimal Glass Effects:**
- Glass limited to system controls
- Standard button styles include subtle glass
- Most glass effects automatic via system
- Focus on accessibility over decoration

---

## Components & Examples

The following components illustrate best practices for adopting Liquid Glass:

### SwiftUI Components (Cross-Platform)

- **GlassCard** – A flexible card presented on a rounded glass surface. Supports `clear`, `tinted` and `prominent` variants with configurable corner radius and tint opacity.
- **GlassButton** – Semantic buttons using `.glass` and `.glassProminent` styles. Kinds (`primary`, `secondary`, `destructive`) map to tints. Built‑in spring animations handle pressed state.
- **GlassSheet** – A convenience wrapper around `sheet(isPresented:)` that uses the system Liquid Glass background. Compose your sheet's content inside a `GlassEffectContainer` when grouping controls.
- **GlassTabBar** – A floating tab bar with a glass background and glass‑styled buttons. The selected tab uses `.glassProminent` and the accent colour.
- **GlassToolbarDemo** – Demonstrates navigation and toolbars adopting glass automatically. Buttons use `.glass` styles; avoid painting backgrounds behind system bars.
- **GlassNavigationDemo** – Showcases navigation within a `NavigationStack` with a glass navigation bar and a scrolling list of `GlassCard` items.
- **GlassEffectContainerExample** – Groups multiple glass buttons in a container to illustrate unified sampling and merging.
- **GlassMorphingExample** – Demonstrates morphing between a compact and an expanded glass surface using `glassEffectID` and a spring animation.
- **MaterialVibrancyExamples** – Contrasts correct use of dynamic foreground styles on glass with incorrect hardcoded colours.
- **AccessibilityExamples** – Respects **Reduce Transparency** and reports current accessibility settings on glass surfaces.

### UIKit Components (iOS/iPadOS)

- **UIKitGlassExamples** – Embeds `UIGlassEffect` and `UIGlassContainerEffect` in SwiftUI. Shows single and grouped glass surfaces using UIKit.
- **UIKitGlassButton** – Demonstrates `UIButton.Configuration.glass()` and `.prominentGlass()` styles.
- **UIKitBackgroundExtension** – Shows `UIBackgroundExtensionView` for sidebar content extension.

### AppKit Components (macOS)

- **NSGlassEffectViewExample** – Demonstrates AppKit glass integration in macOS apps using `NSGlassEffectView`.
- **SidebarGlassExample** – macOS sidebar with glass background in `NSSplitViewController`.
- **InspectorGlassExample** – Inspector panel with glass surface using `NSGlassEffectView`.
- **WindowChromeExample** – macOS window with glass titlebar and automatic traffic light positioning.
- **BackgroundExtensionExample** – Content extending under glass sidebars using `NSBackgroundExtensionView`.
- **AppKitGlassButton** – Native macOS buttons with `NSButton.BezelStyle.glass`.

Explore the demo app (`examples/DemoApp`) to see these components in context across platforms.

---

## Cross-Platform Implementation Example

```swift
import SwiftUI
#if os(macOS)
import AppKit
#elseif os(iOS)
import UIKit
#endif

struct GlassPanelView: View {
    var body: some View {
        if #available(iOS 26, macOS 26, *) {
            content
                .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
        } else {
            // Fallback for iOS 17-25, macOS 14-15
            content
                .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                .overlay {
                    RoundedRectangle(cornerRadius: 12, style: .continuous)
                        .strokeBorder(.white.opacity(0.2), lineWidth: 0.5)
                }
        }
    }

    var content: some View {
        VStack {
            Text("Cross-Platform Glass")
                .font(.headline)
            Text("Works on iOS, macOS, tvOS, and watchOS")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}

// Platform-specific usage
#if os(macOS)
struct MacOSGlassExample: View {
    var body: some View {
        NavigationSplitView {
            // Sidebar with glass
            List {
                Text("Item 1")
                Text("Item 2")
            }
            .background {
                if #available(macOS 26, *) {
                    Rectangle()
                        .glassEffect(.regular)
                } else {
                    Rectangle()
                        .fill(.ultraThinMaterial)
                }
            }
        } detail: {
            // Content with background extension
            Text("Detail View")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(Color.blue.gradient)
                .backgroundExtensionEffect()  // Extends under sidebar
        }
    }
}
#endif
```

---

## Migration & Backwards Compatibility

If you're upgrading from iOS 25/macOS 15 or earlier, follow these steps:

1. **Audit and purge.** Remove old `Material` fills (e.g., `.thinMaterial`, `.regularMaterial`) and any custom blur shaders. Eliminate redundant backgrounds on bars and sheets.
2. **Adopt `glassEffect`.** Replace material fills with `glassEffect` and choose a style (`.clear`, `.regular`, `.regular.tint`). For clusters of controls, use `GlassEffectContainer`.
3. **Coordinate morphs.** Use `glassEffectID` with a shared namespace to morph surfaces during state changes or navigation. Without IDs, SwiftUI will fade surfaces.
4. **Fallback gracefully.** Guard your glass code with `if #available(iOS 26, macOS 26, *)` and provide `.ultraThinMaterial` or solid fills for earlier OS versions.
5. **Respect preferences.** Honour the system's **Clear vs Tinted** setting, **Reduce Transparency**, **Increase Contrast**, **Reduce Motion** and Dynamic Type. Components in this skill handle these automatically.
6. **Platform-specific updates.** On macOS, migrate `NSVisualEffectView` to `NSGlassEffectView`. On iOS, update `UIVisualEffectView` to `UIGlassEffect`.

For a more detailed migration plan, see `docs/ios26-migration.md` and `docs/macos26-migration.md`.

---

## System Integration

**iOS 26** applies Liquid Glass to system UI elements automatically. Navigation bars, toolbars, tab bars and partial sheets all use glass backgrounds. Avoid painting custom backgrounds behind these bars—doing so can conflict with the system's scroll‑edge effect. Place your bar buttons and controls using `.buttonStyle(.glass)` or `.glassProminent`. The system's **Clear vs Tinted** preference adjusts glass opacity across the OS.

**macOS 26** applies Liquid Glass to window chrome, sidebars, toolbars, and inspectors. Windows adopt rounder corners. Use standard system APIs (`NavigationSplitView`, `NSSplitViewController`) to get automatic glass integration. The system manages window controls (traffic lights) positioning over glass surfaces.

**tvOS 26** applies glass to focused elements automatically. Use standard focus APIs to get glass effects when controls gain focus.

**watchOS 26** applies minimal glass effects to system controls automatically. Focus on using standard system components.

More details are available in `docs/system-integration.md` and platform-specific guides.

---

## Further Reading

To deepen your understanding of Liquid Glass, watch Apple's WWDC 2025 sessions:

- **Session 219 – Meet Liquid Glass:** Introduction to the design language, its physics and high‑level guidelines.
- **Session 323 – Build a SwiftUI app with the new design:** Walkthrough of the SwiftUI APIs (`glassEffect`, `GlassEffectContainer`, `glassEffectID`) and migration strategies.
- **Session 284 – Build a UIKit app with the new design:** Guidance on integrating `UIGlassEffect` and `UIGlassContainerEffect` into existing UIKit codebases.
- **Session 310 – Build an AppKit app with the new design:** macOS-specific guidance for `NSGlassEffectView` and AppKit integration patterns.

### Official Documentation

- [Adopting Liquid Glass (Apple Developer)](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass)
- [Applying Liquid Glass to custom views (Tutorial)](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views)
- [Materials (Human Interface Guidelines)](https://developer.apple.com/design/Human-Interface-Guidelines/materials)

Refer to the bundled document `Liquid_Glass_Complete_Guide_iOS26_macOS26.md` for comprehensive coverage of core concepts, SwiftUI, UIKit, and AppKit APIs, design principles, system preferences, performance advice and migration checklists.
