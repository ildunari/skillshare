
struct Comment { let id: Int; let postID: Int }
struct Post { let id: Int }

func loadPostsWithComments(posts: [Post], fetchBatch: ([Int]) -> [Int: [Comment]]) -> [Int: [Comment]] {
    let ids = posts.map { $0.id }
    return fetchBatch(ids) // batched
}
