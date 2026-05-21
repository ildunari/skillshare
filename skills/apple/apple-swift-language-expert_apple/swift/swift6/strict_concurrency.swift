// swift/swift6/strict_concurrency.swift
import Foundation

struct NonSendableResource { var buffer: [Int] = [] }

@MainActor
final class Controller {
    var resource = NonSendableResource()

    func start() {
        Task { // risk: captures main-actor isolated state implicitly
            print(resource.buffer.count)
        }
        Task { @MainActor in
            print(self.resource.buffer.count)
        }
    }
}

struct SafeResource: Sendable { let buffer: [Int] }

actor Repo {
    private var store: [Int] = []
    func append(_ x: Int) { store.append(x) }
    func snapshot() -> [Int] { store }
}

func demo(repo: Repo) async {
    await withTaskGroup(of: Void.self) { group in
        for i in 0..<10 { group.addTask { await repo.append(i) } }
    }
    let snap = await repo.snapshot()
    print(snap)
}
