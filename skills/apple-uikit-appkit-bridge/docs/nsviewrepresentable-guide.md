# NSViewRepresentable Guide

## Purpose
`NSViewRepresentable` adapts an `NSView` into SwiftUI. Implement `makeNSView`, `updateNSView`, optional `makeCoordinator`, and `dismantleNSView`.

## Sizing
Implement `sizeThatFits(_:nsView:context:)` for fine control when necessary.
