# Animation Patterns

Animations breathe life into apps by conveying continuity, focus, and feedback.  SwiftUI’s declarative model makes it easy to animate state changes, but crafting nuanced interactions requires understanding the underlying mechanisms.  This guide explores animation curves, implicit vs explicit animations, transitions, matched geometry effects and timeline‑driven animations.

## Implicit vs Explicit Animations

**Implicit Animations** are triggered by state changes.  Attach `.animation(_:value:)` to a view to animate when a bound value changes, or wrap state mutations in `withAnimation {}`.  Implicit animations rely on view identity: if a view’s structural identity remains the same, SwiftUI animates property changes (opacity, scale, offset, etc.).

**Explicit Animations** use `withAnimation` around state changes.  This guarantees that all changes within the closure animate using the specified curve or spring.  For custom transitions, you can also use `.transaction` to modify the animation applied to individual views.

## Animation Curves

SwiftUI provides several built‑in curves:

* `.linear` – constant speed from start to finish.
* `.easeIn` / `.easeOut` / `.easeInOut` – accelerate or decelerate at the beginning or end.
* `.spring(response:dampingFraction:blendDuration:)` – spring physics with overshoot and oscillation.
* `.interactiveSpring()` – tuned for interactive gestures.
* `.bouncy`, `.snappy` and `.smooth` – new curves in iOS 17 offering playful, responsive motions.

You can chain animations using `.delay()` or compose them with `.repeatCount(_:autoreverses:)`.  For complex sequences, create a custom `Animation` and assign it to `.animation()`.

## Transitions

Transitions describe how a view appears or disappears.  Use `.transition()` modifier with built‑in effects:

* `.opacity` – fade in/out.
* `.scale` – scale up or down from a pivot.
* `.move(edge:)` – slide from a specified edge.
* `.offset(x:y:)` – custom offset.
* `.asymmetric(insertion:removal:)` – different transitions for appearing and disappearing.

Combining transitions and animations yields powerful results:

```swift
if isVisible {
    Text("Hello")
        .transition(.move(edge: .trailing))
        .animation(.easeOut(duration: 0.3), value: isVisible)
}
```

## Matched Geometry Effect

`matchedGeometryEffect(id: namespace:isSource:)` links the frames of two or more views so SwiftUI can animate their positions and sizes in sync.  This is useful when swapping views or moving items between containers【257252862286697†L30-L43】.  All participating views must share the same namespace.  The `id` identifies corresponding views; `isSource` marks the original view.

**Example:** Animated tab bar indicator.

```swift
@Namespace private var ns
@State private var selection = 0

var body: some View {
    HStack(spacing: 0) {
        ForEach(0..<3) { index in
            VStack {
                Button(action: { withAnimation { selection = index } }) {
                    Text(["Home", "Search", "Profile"][index])
                        .padding()
                }
                if selection == index {
                    Color.blue
                        .frame(height: 3)
                        .matchedGeometryEffect(id: "indicator", in: ns)
                } else {
                    Color.clear.frame(height: 3)
                }
            }
        }
    }
}
```

When `selection` changes, the indicator view moves smoothly between tabs by matching geometry across containers【257252862286697†L100-L124】.

## Timeline‑Driven Animations

`TimelineView` allows you to drive animations based on a schedule rather than state changes.  For example, you can update a progress bar every second or animate a clock smoothly:

```swift
struct AnalogClock: View {
    var body: some View {
        TimelineView(.animation) { context in
            let date = context.date
            ZStack {
                ClockFace()
                SecondHand(angle: Angle.degrees(Double(Calendar.current.component(.second, from: date)) * 6))
                    .animation(.linear(duration: 1), value: date)
            }
        }
    }
}
```

The `.animation` scheduler triggers the closure at the screen’s refresh rate, providing a smooth motion【871986411204682†L23-L49】.  Use other schedulers like `.everyMinute` or `.periodic(from:by:)` for coarse updates【871986411204682†L94-L117】.

## Canvas Drawing

Combine `TimelineView` with `Canvas` to perform immediate‑mode drawing.  `Canvas` provides a `GraphicsContext` and a size parameter.  You can draw shapes, images, gradients, and even text by resolving `Text` objects into images【429239476571212†L23-L50】.  Use `context.opacity` and `context.blendMode` to customise rendering.  For example, animate particles by updating their positions in a timeline and drawing them in `Canvas`.  See `swift/canvas_examples.swift` for working code.

## Keyframe Animations

While SwiftUI doesn’t provide built‑in keyframe timelines, you can approximate them with combined delays or by using `TimelineView` to drive values.  For complex sequences, consider splitting animations into multiple phases or using third‑party libraries.

## Testing Animations

Use Xcode previews with animation speed adjustments (`environment(\.animationSpeed, 0.1)`) to slow down animations for inspection.  Combine `.transaction` with `Animation` to debug transitions.  For accessibility, provide reduced motion alternatives by checking `accessibilityReduceMotion` environment value and disabling or simplifying animations accordingly.