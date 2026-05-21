// swift/swift5_9/result_builder_example.swift
@resultBuilder
struct QueryBuilder {
    static func buildBlock(_ parts: String...) -> String { parts.joined(separator: " ") }
    static func buildOptional(_ part: String?) -> String { part ?? "" }
    static func buildEither(first: String) -> String { first }
    static func buildEither(second: String) -> String { second }
    static func buildArray(_ parts: [String]) -> String { parts.joined(separator: " ") }
    static func buildPartialBlock(first: String) -> String { first }
    static func buildPartialBlock(accumulated: String, next: String) -> String { accumulated + " " + next }
}

func SELECT(@QueryBuilder _ make: () -> String) -> String { make() }

func demoQuery() {
    let country = "us"
    let q = SELECT {
        "SELECT *"
        "FROM events"
        if country == "us" {
            "WHERE country = 'US'"
        } else {
            "WHERE country <> 'US'"
        }
        ["ORDER BY timestamp DESC", "LIMIT 100"]
    }
    print(q)
}
