import UIKit
import AppKit

#if canImport(UIKit)
public extension UIView {
    func nearestViewController() -> UIViewController? {
        sequence(first: self.next, next: { $0?.next }).first { $0 is UIViewController } as? UIViewController
    }
}
#endif

#if canImport(AppKit)
public extension NSView {
    func nearestViewController() -> NSViewController? {
        sequence(first: self.nextResponder, next: { $0?.nextResponder }).first { $0 is NSViewController } as? NSViewController
    }
}
#endif
