import SwiftUI

@available(iOS 26.0, *)
public struct LiquidGlassPreviewHarnessRecipe: View {
    public init() {}

    public var body: some View {
        NavigationStack {
            List {
                Section("Core") {
                    NavigationLink("Chat composer") { ChatComposerRecipe() }
                    NavigationLink("Thread list") { ThreadListRecipe() }
                    NavigationLink("Tab bar + FAB") { BottomTabBarFABRecipe() }
                    NavigationLink("Native search + accessory") { NativeSearchAccessoryRecipe() }
                    NavigationLink("Floating toolbar") { FloatingToolbarRecipe() }
                }
                Section("Advanced") {
                    NavigationLink("Tool panel") { ToolCallReasoningPanelRecipe() }
                    NavigationLink("Gallery") { GalleryBrowserRecipe() }
                    NavigationLink("Media canvas") { MediaCanvasControlsRecipe() }
                    NavigationLink("Morphing cluster") { MorphingButtonClusterRecipe() }
                }
            }
            .navigationTitle("Liquid Glass Harness")
        }
    }
}

#Preview {
    if #available(iOS 26.0, *) { LiquidGlassPreviewHarnessRecipe() }
}
