# SwiftPM Harness

Compile-checks the newest Liquid Glass API spellings used by this skill.

Run from this directory:

```bash
xcodebuild -scheme LiquidGlassHarness -destination 'generic/platform=iOS' -sdk iphoneos build
```

This harness is intentionally tiny. It is not an app template; it exists to catch SDK drift in symbols such as `safeAreaBar`, `tabViewBottomAccessory`, `tabBarMinimizeBehavior`, `backgroundExtensionEffect`, `glassEffectID`, and UIKit glass bridging.
