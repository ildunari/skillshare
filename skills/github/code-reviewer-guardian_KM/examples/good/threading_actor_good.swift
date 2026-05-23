
actor Counter {
    private var value = 0
    func increment() { value += 1 }
    func current() -> Int { value }
}
