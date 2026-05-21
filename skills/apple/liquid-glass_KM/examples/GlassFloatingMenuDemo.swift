import SwiftUI

@available(iOS 26.0, *)
struct GlassFloatingMenuDemo: View {
    @State private var expanded = false
    private let actions = [("Web", "network"), ("File", "paperclip"), ("Canvas", "rectangle.on.rectangle"), ("Code", "curlybraces")]

    var body: some View {
        ZStack {
            GlassShowcaseBackground()
            VStack { Text("Floating menus should be short-lived and control-focused.").font(.title2.bold()).multilineTextAlignment(.center).padding(); Spacer() }
            ZStack {
                ForEach(Array(actions.enumerated()), id: \.offset) { index, action in
                    Button(action.0, systemImage: action.1) {}
                        .buttonStyle(.glass)
                        .offset(expanded ? radialOffset(index) : .zero)
                        .opacity(expanded ? 1 : 0)
                        .scaleEffect(expanded ? 1 : 0.5)
                }
                Button(expanded ? "Close" : "Agent", systemImage: expanded ? "xmark" : "sparkles") { withAnimation(.spring(response: 0.38, dampingFraction: 0.72)) { expanded.toggle() } }
                    .buttonStyle(.glassProminent)
                    .contentTransition(.symbolEffect(.replace))
            }
        }
        .navigationTitle("Floating Menu")
    }

    private func radialOffset(_ index: Int) -> CGSize {
        let angle = Double(index) / Double(actions.count) * .pi * 2 - .pi / 2
        return CGSize(width: cos(angle) * 92, height: sin(angle) * 92)
    }
}

#Preview { if #available(iOS 26.0, *) { NavigationStack { GlassFloatingMenuDemo() } } }
