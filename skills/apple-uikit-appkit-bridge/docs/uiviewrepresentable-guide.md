# UIViewRepresentable Guide

## Purpose
`UIViewRepresentable` adapts a `UIView` into SwiftUI. Implement `makeUIView`, `updateUIView`, optional `makeCoordinator`, and `dismantleUIView` for cleanup.

## Lifecycle
```mermaid
stateDiagram-v2
    [*] --> makeUIView
    makeUIView --> updateUIView: initial
    updateUIView --> updateUIView: state changes
    updateUIView --> dismantleUIView: removal
```

## Tips
- Keep identity stable; only update what changed.
- Use a `Coordinator` for delegates or target–action.
- Remove observers/delegates in `dismantleUIView`.
