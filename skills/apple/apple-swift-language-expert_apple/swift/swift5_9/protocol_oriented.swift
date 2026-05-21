// swift/swift5_9/protocol_oriented.swift
protocol Cache {
    associatedtype Key: Hashable
    associatedtype Value
    mutating func insert(_ v: Value, for k: Key)
    func value(for k: Key) -> Value?
}

struct LRUCache<K: Hashable, V>: Cache {
    typealias Key = K; typealias Value = V
    private var store: [K: V] = [:]
    mutating func insert(_ v: V, for k: K) { store[k] = v }
    func value(for k: K) -> V? { store[k] }
}

struct Repository<R: Cache> where R.Value == Data {
    var cache: R
    mutating func put(_ key: R.Key, _ data: Data) { cache.insert(data, for: key) }
}
