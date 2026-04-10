// swift/swift5_9/memory_management.swift
import Foundation

final class Owner {
    var child: Child?
    deinit { print("Owner deinit") }
}

final class Child {
    weak var owner: Owner?
    var onTick: (() -> Void)?
    deinit { print("Child deinit") }
}

func demoRetainCycle() {
    let owner = Owner()
    let child = Child()
    owner.child = child
    child.owner = owner
    child.onTick = { [weak child] in
        guard let c = child else { return }
        print("tick \(String(describing: c.owner))")
    }
}
