import SwiftUI

@available(iOS 26.0, *)
public struct ChatComposerRecipe: View {
    @Environment(\.accessibilityReduceTransparency) private var reduceTransparency
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var prompt = ""
    @State private var isStreaming = false
    @State private var isRecording = false
    @State private var toolsExpanded = false
    @State private var attachments: [ComposerAttachment] = [
        .init(name: "Research.pdf", kind: "pdf", progress: nil),
        .init(name: "mockup.png", kind: "image", progress: 0.64)
    ]

    public init() {}

    public var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 18) {
                Text("Markdown/chat content stays readable and mostly plain.")
                    .font(.title2.weight(.semibold))
                Text("Liquid Glass is reserved for the composer, action chips, and transient agent metadata rather than every message bubble.")
                    .foregroundStyle(.secondary)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            .padding()
            .padding(.bottom, 160)
        }
        .safeAreaInset(edge: .bottom) {
            composer
                .padding(.bottom, 8)
        }
    }

    private var composer: some View {
        VStack(spacing: 10) {
            if !attachments.isEmpty {
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(attachments) { attachment in
                            AttachmentChip(attachment: attachment) {
                                attachments.removeAll { $0.id == attachment.id }
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                .transition(.move(edge: .bottom).combined(with: .opacity))
            }

            if toolsExpanded {
                toolsRow
                    .padding(.horizontal)
                    .transition(.move(edge: .bottom).combined(with: .opacity))
            }

            GlassEffectContainer(spacing: 10) {
                HStack(alignment: .bottom, spacing: 10) {
                    Button("Tools", systemImage: toolsExpanded ? "xmark" : "plus") { toggleTools() }
                        .buttonStyle(.glass)
                        .contentTransition(.symbolEffect(.replace))
                        .accessibilityLabel(toolsExpanded ? "Hide tools" : "Show tools")

                    TextField("Ask, search, or delegate…", text: $prompt, axis: .vertical)
                        .lineLimit(1...6)
                        .textFieldStyle(.plain)
                        .padding(.horizontal, 14)
                        .padding(.vertical, 12)
                        .background(fieldBackground)

                    Button(isRecording ? "Stop voice" : "Voice", systemImage: isRecording ? "waveform.circle.fill" : "mic.fill") {
                        withAnimation(animation) { isRecording.toggle() }
                    }
                    .buttonStyle(.glass)
                    .tint(isRecording ? .red : .primary)
                    .contentTransition(.symbolEffect(.replace))
                    .accessibilityLabel(isRecording ? "Stop voice input" : "Start voice input")

                    Button(isStreaming ? "Stop" : "Send", systemImage: isStreaming ? "stop.fill" : "arrow.up") {
                        withAnimation(animation) { isStreaming.toggle() }
                    }
                    .buttonStyle(.glassProminent)
                    .tint(isStreaming ? .red : .accentColor)
                    .contentTransition(.symbolEffect(.replace))
                    .disabled(prompt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && !isStreaming)
                }
            }
            .padding(.horizontal)
        }
        .padding(.vertical, 10)
        .background(alignment: .bottom) {
            LinearGradient(colors: [.clear, .background.opacity(0.75), .background], startPoint: .top, endPoint: .bottom)
                .ignoresSafeArea()
        }
    }

    private var toolsRow: some View {
        GlassEffectContainer(spacing: 8) {
            HStack(spacing: 8) {
                ToolButton(title: "Web", symbol: "network", selected: true)
                ToolButton(title: "Files", symbol: "paperclip", selected: false)
                ToolButton(title: "Canvas", symbol: "rectangle.on.rectangle", selected: false)
                ToolButton(title: "Code", symbol: "curlybraces", selected: false)
                Spacer(minLength: 0)
            }
        }
    }

    @ViewBuilder private var fieldBackground: some View {
        let shape = RoundedRectangle(cornerRadius: 24, style: .continuous)
        if reduceTransparency {
            shape.fill(.background).overlay(shape.stroke(.separator.opacity(0.7)))
        } else {
            shape.glassEffect(.regular.interactive(), in: shape)
        }
    }

    private var animation: Animation { reduceMotion ? .easeOut(duration: 0.12) : .spring(response: 0.34, dampingFraction: 0.78) }
    private func toggleTools() { withAnimation(animation) { toolsExpanded.toggle() } }
}

@available(iOS 26.0, *)
private struct ToolButton: View {
    let title: String
    let symbol: String
    let selected: Bool
    var body: some View {
        Button(title, systemImage: symbol) {}
            .composerRecipeGlassStyle(selected)
    }
}

private struct ComposerAttachment: Identifiable {
    let id = UUID()
    let name: String
    let kind: String
    let progress: Double?
}

@available(iOS 26.0, *)
private struct AttachmentChip: View {
    let attachment: ComposerAttachment
    let remove: () -> Void

    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: attachment.kind == "pdf" ? "doc.richtext" : "photo")
            VStack(alignment: .leading, spacing: 2) {
                Text(attachment.name).font(.caption.weight(.semibold)).lineLimit(1)
                if let progress = attachment.progress {
                    ProgressView(value: progress).controlSize(.mini).frame(width: 82)
                } else {
                    Text(attachment.kind.uppercased()).font(.caption2).foregroundStyle(.secondary)
                }
            }
            Button("Remove", systemImage: "xmark", action: remove)
                .buttonStyle(.glass)
                .labelStyle(.iconOnly)
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 8)
        .glassEffect(.regular, in: Capsule())
    }
}



@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func composerRecipeGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}

#Preview {
    if #available(iOS 26.0, *) { ChatComposerRecipe() }
}
