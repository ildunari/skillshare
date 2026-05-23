
/// Represents a Widget in the system.
public struct Widget {
    /// The stable identifier.
    public let id: String
    /// Builds a display string for the widget.
    /// - Returns: A human-readable description.
    public func make() -> String { return id }
}
