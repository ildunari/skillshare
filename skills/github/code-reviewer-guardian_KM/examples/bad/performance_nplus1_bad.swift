
struct Comment { let id: Int; let postID: Int }
struct Post { let id: Int }

func loadPostsWithComments(posts: [Post], fetch: (Int) -> [Comment]) -> [Int: [Comment]] {
    var map: [Int: [Comment]] = [:]
    for p in posts {
        map[p.id] = fetch(p.id) // N+1
    }
    return map
}
