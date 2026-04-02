# Layout Deep Dive

Layout determines how views are sized and positioned.  SwiftUI provides many built‑in containers such as `HStack`, `VStack`, `ZStack`, `Grid`, `LazyVStack`, `LazyHGrid`, `Form` and `List`.  When these aren’t enough, create your own layout using the `Layout` protocol or read geometry from a `GeometryReader`.  This guide dives into advanced layout patterns, including measurement, alignment, preferences and custom layout algorithms.

## Basics: Stacks and Grids

**Stacks** align views along an axis.  `HStack` arranges children horizontally, `VStack` vertically, and `ZStack` overlays them.  You can specify alignment (e.g., `.leading`, `.center`) and spacing.  Use `.alignmentGuide` to override alignment for individual children.

**Lazy Stacks** load children on demand.  Use `LazyVStack` or `LazyHStack` within a `ScrollView` for lists of arbitrary length.  They improve performance by only instantiating visible rows.

**Grids**: `LazyVGrid` and `LazyHGrid` let you define columns or rows with flexible, fixed or adaptive sizing.  iOS 26 introduces `Grid` and `GridRow` which automatically size cells based on content.  Use `Grid(alignment:.leading, horizontalSpacing: 8, verticalSpacing: 8) {}` to create complex table layouts.

## Custom Layouts with the `Layout` Protocol

The `Layout` protocol gives you complete control over measurement and placement.  It requires two methods:

```swift
func sizeThatFits(_ proposal: ProposedViewSize, subviews: Subviews, cache: inout Cache?) -> CGSize
func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout Cache?)
```

`sizeThatFits` computes the final size of the container given a proposed size from the parent.  It can measure child subviews using `subview.sizeThatFits(proposal)`.  `placeSubviews` positions each subview within the given bounds【540782554707304†L21-L43】.  Use the optional `Cache` to store expensive calculations.

**Example: FlowLayout**

```swift
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
                // wrap to new row
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
                // wrap
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
```

This layout wraps child views onto new rows when they would exceed the available width.  The `sizeThatFits` method measures children and the `placeSubviews` method positions them accordingly.

## GeometryReader Best Practices

`GeometryReader` gives a closure with `GeometryProxy` containing the size and coordinate space information for its parent.  Use it sparingly: a `GeometryReader` takes up all available space by default, which may lead to unwanted stretching.  To constrain it, embed it in a `frame` or overlay【45585243622685†L37-L46】.  Prefer `Shape` or `Layout` for drawing and positioning instead of `GeometryReader` when possible【45585243622685†L73-L86】.

**Measuring Child Size:** Use `PreferenceKey` to report child sizes up to parents.  For example, to align a tooltip with an anchor, you can measure the anchor’s global frame using `GeometryReader` and propagate it via a preference key.  The parent then reads the preference and positions the tooltip accordingly.

## PreferenceKey Pattern

Preferences send information from children to ancestors.  Define a `PreferenceKey` with a default value and a `reduce` method to combine multiple values.  Children emit preferences with `.preference(key:value:)`.  Ancestors read them with `.onPreferenceChange` or `.backgroundPreferenceValue`.  This mechanism avoids prop drilling and allows cross‑view communication.  Apple notes that preferences complement the environment: environment configures children, preferences inform parents【233209377127931†L30-L58】.

**Example:** Passing a child’s height to a parent to align siblings.

```swift
struct ChildHeightKey: PreferenceKey {
    static var defaultValue: CGFloat = 0
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}

struct ChildView: View {
    var body: some View {
        Text("Dynamic")
            .background(GeometryReader { proxy in
                Color.clear
                    .preference(key: ChildHeightKey.self, value: proxy.size.height)
            })
    }
}

struct ParentView: View {
    @State private var childHeight: CGFloat = 0
    var body: some View {
        VStack {
            ChildView()
            Rectangle()
                .frame(height: childHeight)
        }
        .onPreferenceChange(ChildHeightKey.self) { value in
            childHeight = value
        }
    }
}
```

## Alignment and Anchors

SwiftUI’s `Alignment` values (like `.topLeading`, `.center`) align children within containers.  Use `alignmentGuide` to override a specific alignment for a child relative to a custom anchor.  `Anchor` values let you capture positions within a coordinate space and use them later for positioning or transitions.  For example, `matchedGeometryEffect` uses anchors under the hood to synchronise frames during animations【257252862286697†L30-L43】.

## Layout Priority

When space is limited, SwiftUI gives each view a default priority of 0.  Use `.layoutPriority()` to hint which view should expand or shrink first.  A higher priority view will take available space before lower ones.

## Advanced Techniques

* **ViewThatFits:** Introduced in iOS 16, this container displays the first child that fits into the available space.  Use it to provide multiple layout options for different device sizes.
* **GeometryGroup:** Synchronises geometry across multiple views for animations; mostly internal but accessible through `matchedGeometryEffect`.
* **Hiding Views:** Use `.hidden()` or conditionally return `EmptyView()` to remove a view.  Be mindful that replacing a view with a different type affects identity and animations【152934397403680†L510-L567】.

For more examples of custom layouts, including waterfall columns and masonry grids, see the Swift files in `swift/custom_layouts/`.