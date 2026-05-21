import SwiftUI

@available(iOS 26.0, *)
struct GlassComposerDemo: View {
    @Environment(\.accessibilityReduceTransparency) private var reduceTransparency
    @State private var text = ""
    @State private var streaming = true
    @State private var tools = false

    var body: some View {
        ZStack { GlassShowcaseBackground(); content }
            .navigationTitle("Composer")
            .safeAreaInset(edge: .bottom) { composer.padding(.bottom, 8) }
    }

    private var content: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                ForEach(DemoMessage.sample) { message in
                    Text(message.text)
                        .padding(12)
                        .frame(maxWidth: .infinity, alignment: message.isUser ? .trailing : .leading)
                        .foregroundStyle(.primary)
                }
            }
            .padding()
            .padding(.bottom, 160)
        }
    }

    private var composer: some View {
        VStack(spacing: 10) {
            if tools {
                HStack(spacing: 8) {
                    Button("Web", systemImage: "network") {}.buttonStyle(.glassProminent)
                    Button("Files", systemImage: "paperclip") {}.buttonStyle(.glass)
                    Button("Canvas", systemImage: "rectangle.on.rectangle") {}.buttonStyle(.glass)
                    Spacer()
                }.padding(.horizontal).transition(.move(edge: .bottom).combined(with: .opacity))
            }
            GlassEffectContainer(spacing: 10) {
                HStack(alignment: .bottom, spacing: 10) {
                    Button("Tools", systemImage: tools ? "xmark" : "plus") { withAnimation(.spring(response: 0.32, dampingFraction: 0.78)) { tools.toggle() } }
                        .buttonStyle(.glass)
                        .contentTransition(.symbolEffect(.replace))
                    TextField("Ask anything…", text: $text, axis: .vertical)
                        .lineLimit(1...5)
                        .padding(.horizontal, 14)
                        .padding(.vertical, 12)
                        .background(fieldBackground)
                    Button(streaming ? "Stop" : "Send", systemImage: streaming ? "stop.fill" : "arrow.up") { streaming.toggle() }
                        .buttonStyle(.glassProminent)
                        .tint(streaming ? .red : .accentColor)
                        .contentTransition(.symbolEffect(.replace))
                }
            }.padding(.horizontal)
        }.padding(.vertical, 10)
    }

    @ViewBuilder private var fieldBackground: some View {
        let shape = RoundedRectangle(cornerRadius: 24, style: .continuous)
        if reduceTransparency { shape.fill(.background).overlay(shape.stroke(.separator)) }
        else { shape.glassEffect(.regular.interactive(), in: shape) }
    }
}

#Preview { if #available(iOS 26.0, *) { NavigationStack { GlassComposerDemo() } } }
