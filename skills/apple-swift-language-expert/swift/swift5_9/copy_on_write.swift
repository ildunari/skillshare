// swift/swift5_9/copy_on_write.swift
import Foundation
public struct CoWBuffer<Element> {
    final class Storage {
        var array: [Element]
        init(_ a: [Element]) { self.array = a }
    }
    private var storage: Storage
    public init(_ a: [Element] = []) { self.storage = Storage(a) }
    public var elements: [Element] { storage.array }
    public mutating func append(_ x: Element) {
        ensureUnique()
        storage.array.append(x)
    }
    private mutating func ensureUnique() {
        if !isKnownUniquelyReferenced(&storage) {
            storage = Storage(storage.array)
        }
    }
}
