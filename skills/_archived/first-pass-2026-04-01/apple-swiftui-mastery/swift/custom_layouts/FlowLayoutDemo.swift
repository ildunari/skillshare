import SwiftUI

/// A simple flow layout that wraps views horizontally.
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

/// Demonstrates the custom FlowLayout defined in docs.
struct FlowLayoutDemo: View {
    let items = (1...20).map { "Item \($0)" }
    var body: some View {
        ScrollView {
            FlowLayout(spacing: 8) {
                ForEach(items, id: \ .self) { item in
                    Text(item)
                        .padding(8)
                        .background(Color.blue.opacity(0.2))
                        .cornerRadius(6)
                }
            }
            .padding()
        }
    }
}

struct FlowLayoutDemo_Previews: PreviewProvider {
    static var previews: some View {
        FlowLayoutDemo()
    }
}