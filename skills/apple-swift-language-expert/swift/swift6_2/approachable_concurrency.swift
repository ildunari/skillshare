// swift/swift6_2/approachable_concurrency.swift
//
// Demonstrates Swift 6.2's *approachable concurrency* features.
// Requires Swift 6.2 or later.
//
// In Swift 6.2 the default isolation context for async functions is the caller.
// That means async functions no longer implicitly hop to a global actor unless
// annotated.  Use the `@concurrent` attribute when a function may execute
// concurrently with its caller, and use `@MainActor` when you need a specific
// executor.

import Foundation

// A simple async function that inherits the caller's isolation context.  When
// called from the main actor, it will execute on the main actor.  When called
// from a background task, it stays on that task.
func fetchData() async -> String {
    // Simulate work
    return "hello"
}

// Use @concurrent to tell the compiler that this async function may execute
// concurrently with its caller.  Without this, the function is assumed to
// execute on the caller's actor.
@concurrent
func fetchImage(from url: URL) async throws -> Data {
    // URLSession API with async/await; errors propagate via typed throws (Data can
    // be thrown only as URLError).  This function runs concurrently with the
    // caller in Swift 6.2.
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}

// Demonstrate observation streaming using the @Observable macro and the new
// Observations type introduced in Swift 6.2.
@MainActor
@Observable
final class PlayerState {
    var score: Int = 0
    var item: String = ""
    func gain(points: Int) { score += points }
    func obtain(item: String) { self.item = item }
}

// Use Observations to asynchronously stream state changes.  Each update is
// transactional: synchronous changes to multiple properties are coalesced into
// one value.
func observeState() async {
    let state = PlayerState()
    let updates = Observations(state) { "\($0.score)-\($0.item)" }
    // Spawn a detached task to print updates as they arrive.
    Task.detached(name: "state-observer") {
        for await value in updates {
            print("state update: \(value)")
        }
    }
    // Mutate state synchronously; observers get a single combined update.
    state.gain(points: 10)
    state.obtain(item: "Sword")
    // Because updates are transactional, only one update will be printed for the
    // two synchronous mutations above.
}

// Entry point for manual testing.  Swift Playgrounds or tests can call
// observeState() with `Task { await observeState() }` to see the behavior.