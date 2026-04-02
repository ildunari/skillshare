import SwiftUI
import Observation

/// A combined demo showcasing state management, navigation, layout and animation.
@Observable
class CombinedModel {
    var count: Int = 0
    func increment() { count += 1 }
}

enum CombinedScreen: Hashable {
    case counter
    case detail
}

struct CombinedDemo: View {
    @State private var path: [CombinedScreen] = []
    @State private var model = CombinedModel()
    @Namespace private var ns
    var body: some View {
        NavigationStack(path: $path) {
            VStack(spacing: 20) {
                Text("Count: \(model.count)")
                    .matchedGeometryEffect(id: "label", in: ns)
                    .font(.largeTitle)
                Button("Increment") { model.increment() }
                    .buttonStyle(.borderedProminent)
                Button("Show Detail") {
                    withAnimation { path.append(.detail) }
                }
            }
            .navigationDestination(for: CombinedScreen.self) { screen in
                switch screen {
                case .counter: EmptyView()
                case .detail: CombinedDetailView(model: model, namespace: ns)
                }
            }
            .padding()
        }
    }
}

struct CombinedDetailView: View {
    @Bindable var model: CombinedModel
    var namespace: Namespace.ID
    var body: some View {
        VStack(spacing: 20) {
            Text("Detail Count: \(model.count)")
                .matchedGeometryEffect(id: "label", in: namespace)
                .font(.title)
            Button("Increment Again") { model.increment() }
            FlowLayout(spacing: 8) {
                ForEach(0..<model.count, id: \ .self) { idx in
                    Circle()
                        .fill(Color.pink)
                        .frame(width: 20, height: 20)
                }
            }
        }
        .padding()
        .navigationTitle("Detail")
    }
}

/// A simple horizontal flow layout used in the combined demo.
struct FlowLayout: Layout {
    var spacing: CGFloat = 8
    func sizeThatFits(_ proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        var width: CGFloat = 0
        var height: CGFloat = 0
        var rowWidth: CGFloat = 0
        var rowHeight: CGFloat = 0
        let maxWidth = proposal.width ?? .infinity
        for subview in subviews {
            let size = subview.sizeThatFits(proposal)
            if rowWidth + size.width + spacing > maxWidth {
                width = max(width, rowWidth)
                height += rowHeight + spacing
                rowWidth = size.width
                rowHeight = size.height
            } else {
                rowWidth += size.width + spacing
                rowHeight = max(rowHeight, size.height)
            }
        }
        width = max(width, rowWidth)
        height += rowHeight
        return CGSize(width: width, height: height)
    }
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var x: CGFloat = bounds.minX
        var y: CGFloat = bounds.minY
        var rowHeight: CGFloat = 0
        for subview in subviews {
            let size = subview.sizeThatFits(proposal)
            if x + size.width > bounds.maxX {
                x = bounds.minX
                y += rowHeight + spacing
                rowHeight = 0
            }
            subview.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))
            x += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }
    }
}

struct CombinedDemo_Previews: PreviewProvider {
    static var previews: some View {
        CombinedDemo()
    }
}