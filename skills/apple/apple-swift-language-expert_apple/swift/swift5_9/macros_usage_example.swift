// swift/swift5_9/macros_usage_example.swift
import Observation

@Observable
final class Store { var count: Int = 0 }

func macroDemo() {
    let s = Store()
    s.count += 1
}
