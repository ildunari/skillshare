import SwiftUI

/// A custom layout that makes all children the same width based on the widest child.
struct EqualWidthLayout: Layout {
    func sizeThatFits(_ proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        // Determine max width and sum of heights
        var maxWidth: CGFloat = 0
        var totalHeight: CGFloat = 0
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            maxWidth = max(maxWidth, size.width)
            totalHeight += size.height
        }
        totalHeight += CGFloat(subviews.count - 1) * 8
        return CGSize(width: maxWidth, height: totalHeight)
    }
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var y = bounds.minY
        let maxWidth = sizeThatFits(proposal, subviews: subviews, cache: &cache).width
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            let x = bounds.minX + (maxWidth - size.width) / 2
            subview.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(width: size.width, height: size.height))
            y += size.height + 8
        }
    }
}

struct EqualWidthLayoutDemo: View {
    var body: some View {
        EqualWidthLayout {
            Text("Short")
                .padding()
                .background(Color.green.opacity(0.3))
            Text("This is a longer text view")
                .padding()
                .background(Color.yellow.opacity(0.3))
            Text("Medium")
                .padding()
                .background(Color.blue.opacity(0.3))
        }
        .padding()
    }
}

struct EqualWidthLayoutDemo_Previews: PreviewProvider {
    static var previews: some View {
        EqualWidthLayoutDemo()
    }
}