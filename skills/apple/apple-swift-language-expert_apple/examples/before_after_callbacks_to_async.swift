// examples/before_after_callbacks_to_async.swift
// BEFORE
func fetchUser(id: Int, completion: @escaping (Result<String, Error>) -> Void) {
    DispatchQueue.global().async { completion(.success("User \(id)")) }
}
// AFTER
func fetchUser(id: Int) async throws -> String {
    try await Task.sleep(nanoseconds: 1_000_000)
    return "User \(id)"
}
