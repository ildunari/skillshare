import SwiftUI

@available(iOS 26.0, *)
struct SourceLinkedCommandPaletteSnippet: View {
    @State private var showingPalette = false
    @State private var selectedCommand = "Ask"

    var body: some View {
        VStack(spacing: 18) {
            Button("Open commands", systemImage: "command") {
                showingPalette = true
            }
            .buttonStyle(.glassProminent)

            Text("Selected: \(selectedCommand)")
                .font(.headline)
        }
        .sheet(isPresented: $showingPalette) {
            CommandPaletteSheet(selectedCommand: $selectedCommand)
                .presentationDetents([.medium, .large])
                .presentationDragIndicator(.visible)
        }
    }
}

@available(iOS 26.0, *)
private struct CommandPaletteSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Binding var selectedCommand: String

    private let commands = [
        ("Ask", "sparkles"),
        ("Search web", "magnifyingglass"),
        ("Attach file", "paperclip"),
        ("Run tool", "hammer"),
        ("Create image", "photo")
    ]

    var body: some View {
        NavigationStack {
            List(commands, id: \.0) { command in
                Button {
                    selectedCommand = command.0
                    dismiss()
                } label: {
                    Label(command.0, systemImage: command.1)
                        .padding(.vertical, 6)
                }
            }
            .navigationTitle("Command Palette")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
            }
            .safeAreaInset(edge: .bottom) {
                GlassEffectContainer(spacing: 8) {
                    HStack(spacing: 8) {
                        Button("Reason", systemImage: "brain") {}
                            .buttonStyle(.glass)
                        Button("Search", systemImage: "magnifyingglass") {}
                            .buttonStyle(.glass)
                        Button("Done", systemImage: "checkmark") { dismiss() }
                            .buttonStyle(.glassProminent)
                    }
                    .padding(.bottom, 8)
                }
            }
        }
    }
}

@available(iOS 26.0, *)
#Preview("Source-linked command palette") {
    SourceLinkedCommandPaletteSnippet()
}
