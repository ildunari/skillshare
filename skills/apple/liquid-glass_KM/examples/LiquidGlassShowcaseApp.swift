import SwiftUI

@main
@available(iOS 26.0, *)
struct LiquidGlassShowcaseApp: App {
    var body: some Scene {
        WindowGroup { LiquidGlassShowcaseHome() }
    }
}

@available(iOS 26.0, *)
struct LiquidGlassShowcaseHome: View {
    var body: some View {
        NavigationStack {
            List {
                NavigationLink("Glass Composer Demo") { GlassComposerDemo() }
                NavigationLink("Glass Tab Bar Demo") { GlassTabBarDemo() }
                NavigationLink("Glass Floating Menu Demo") { GlassFloatingMenuDemo() }
                NavigationLink("Glass Tool Call Panel Demo") { GlassToolCallPanelDemo() }
                NavigationLink("Glass Canvas Controls Demo") { GlassCanvasControlsDemo() }
                NavigationLink("Glass Shader-Inspired Demo") { GlassShaderInspiredDemo() }
            }
            .navigationTitle("Liquid Glass")
        }
    }
}

@available(iOS 26.0, *)
struct GlassShowcaseBackground: View {
    var body: some View {
        LinearGradient(colors: [.blue.opacity(0.85), .purple.opacity(0.75), .pink.opacity(0.7)], startPoint: .topLeading, endPoint: .bottomTrailing)
            .ignoresSafeArea()
            .overlay {
                Circle().fill(.white.opacity(0.18)).frame(width: 220).blur(radius: 30).offset(x: -130, y: -210)
                Circle().fill(.cyan.opacity(0.16)).frame(width: 260).blur(radius: 36).offset(x: 140, y: 220)
            }
    }
}

struct DemoMessage: Identifiable {
    let id = UUID()
    let text: String
    let isUser: Bool
}

extension DemoMessage {
    static let sample: [DemoMessage] = [
        .init(text: "Build me an iOS 26 Liquid Glass composer.", isUser: true),
        .init(text: "I’ll keep the markdown readable and use glass only for controls, attachments, and agent status.", isUser: false)
    ]
}


@available(iOS 26.0, *)
extension View {
    @ViewBuilder
    func showcaseGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }

    @ViewBuilder
    func showcaseSelectedTrait(_ isSelected: Bool) -> some View {
        if isSelected {
            self.accessibilityAddTraits(.isSelected)
        } else {
            self
        }
    }
}
