// swift/swift6/actor_isolation.swift
import Foundation

actor Counter {
    private var value: Int = 0
    func increment() { value += 1 }
    func get() -> Int { value }
    nonisolated var description: String { "Counter(...)" }
}

@MainActor
final class ScreenModel {
    private let counter = Counter()
    func tapped() async {
        await counter.increment()
        let v = await counter.get()
        print("value: \(v)")
    }
    nonisolated func format(_ n: Int) -> String { "n=\(n)" }
}
