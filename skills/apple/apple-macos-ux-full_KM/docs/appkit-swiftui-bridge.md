# AppKit ↔ SwiftUI Bridge

## SwiftUI inside AppKit

- Use `NSHostingController` or `NSHostingView` to embed SwiftUI views in AppKit hierarchies.
- Adjust sizing via `NSHostingController.sizingOptions` when necessary.

## AppKit inside SwiftUI

- Use `NSViewRepresentable` / `NSViewControllerRepresentable` for advanced controls (e.g., `NSTableView`).
- Use a `Coordinator` to forward delegate callbacks back into SwiftUI state models.
