// swift/swift5_9/async_await_examples.swift
import Foundation

struct User: Decodable { let id: Int; let name: String }
struct Post: Decodable { let id: Int; let title: String }

enum API {
    static func fetchUser(id: Int) async throws -> User {
        let url = URL(string: "https://example.com/users/\(id)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(User.self, from: data)
    }

    static func fetchPosts(userID: Int) async throws -> [Post] {
        let url = URL(string: "https://example.com/users/\(userID)/posts")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode([Post].self, from: data)
    }
}

@MainActor
final class ViewModel: ObservableObject {
    @Published private(set) var posts: [Post] = []
    @Published private(set) var userName: String = ""
    @Published private(set) var isLoading = false

    func load(id: Int) async {
        isLoading = true
        defer { isLoading = false }

        async let user = API.fetchUser(id: id)
        async let userPosts = API.fetchPosts(userID: id)

        do {
            let (u, p) = try await (user, userPosts)
            self.userName = u.name
            self.posts = p
        } catch {
            if Task.isCancelled { return }
            print("Failed: \(error)")
        }
    }

    func prefetch(ids: [Int]) async {
        posts.removeAll()
        do {
            try await withThrowingTaskGroup(of: [Post].self) { group in
                for i in ids {
                    group.addTask {
                        try Task.checkCancellation()
                        return try await API.fetchPosts(userID: i)
                    }
                }
                for try await chunk in group {
                    self.posts.append(contentsOf: chunk)
                }
            }
        } catch { print("group error: \(error)") }
    }
}
