# Coordinator Pattern

A nested class that owns bridging logic like delegates/data sources.

```swift
final class Coordinator: NSObject, UITableViewDelegate, UITableViewDataSource {
    weak var parent: TableBridge?
    init(_ parent: TableBridge) { self.parent = parent }
}
```
