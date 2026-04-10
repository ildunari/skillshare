// swift/swift5_9/task_group_tasklocal.swift
import Foundation

@TaskLocal static var requestID: UUID?

func withRequest<T>(_ id: UUID, _ body: () async throws -> T) async rethrows -> T {
    try await requestID.withValue(id) {
        try await body()
    }
}

func log(_ message: String) {
    let id = requestID ?? UUID(uuidString: "00000000-0000-0000-0000-000000000000")
    print("[\(id?.uuidString ?? "-")] \(message)")
}

func runBatch(urls: [URL]) async {
    await withRequest(UUID()) {
        await withTaskGroup(of: Void.self) { group in
            for u in urls {
                group.addTask {
                    log("Fetching \(u.absoluteString)")
                    _ = try? await URLSession.shared.data(from: u)
                }
            }
        }
    }
}
