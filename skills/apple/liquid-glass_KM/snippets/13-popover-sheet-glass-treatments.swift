import SwiftUI

@available(iOS 26.0, *)
struct GlassPopoverTrigger: View {
    @State private var showing = false

    var body: some View {
        Button("Agent options", systemImage: "slider.horizontal.3") { showing.toggle() }
            .buttonStyle(.glass)
            .popover(isPresented: $showing) {
                VStack(alignment: .leading, spacing: 12) {
                    Text("Agent options").font(.headline)
                    Button("Use web", systemImage: "network") {}
                    Button("Attach file", systemImage: "paperclip") {}
                    Button("Open canvas", systemImage: "rectangle.on.rectangle") {}
                }
                .buttonStyle(.glass)
                .padding(16)
                .presentationCompactAdaptation(.popover)
            }
    }
}

@available(iOS 26.0, *)
struct GlassSheetTrigger: View {
    @State private var showing = false

    var body: some View {
        Button("Show sources", systemImage: "text.quote") { showing = true }
            .buttonStyle(.glass)
            .sheet(isPresented: $showing) {
                NavigationStack {
                    List(0..<8) { item in
                        Text("Source \(item + 1)")
                    }
                    .navigationTitle("Sources")
                    .toolbar {
                        ToolbarItem(placement: .topBarTrailing) {
                            Button("Done") { showing = false }.buttonStyle(.glass)
                        }
                    }
                }
            }
    }
}
