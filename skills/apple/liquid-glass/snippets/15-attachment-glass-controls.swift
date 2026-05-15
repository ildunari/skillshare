import SwiftUI

@available(iOS 26.0, *)
struct AttachmentGlassControls: View {
    let name: String
    let kind: String
    let progress: Double?

    var body: some View {
        HStack(spacing: 10) {
            Image(systemName: icon)
                .frame(width: 34, height: 34)
                .glassEffect(.regular, in: Circle())

            VStack(alignment: .leading, spacing: 2) {
                Text(name).font(.subheadline.weight(.semibold)).lineLimit(1)
                if let progress {
                    ProgressView(value: progress).controlSize(.mini)
                } else {
                    Text(kind).font(.caption).foregroundStyle(.secondary)
                }
            }

            Spacer(minLength: 8)

            Button("Remove", systemImage: "xmark") {}
                .buttonStyle(.glass)
                .labelStyle(.iconOnly)
        }
        .padding(10)
        .background(.background.opacity(0.82), in: RoundedRectangle(cornerRadius: 18, style: .continuous))
    }

    private var icon: String { kind == "pdf" ? "doc.richtext" : kind == "image" ? "photo" : "paperclip" }
}
