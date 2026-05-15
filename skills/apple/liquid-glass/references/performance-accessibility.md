# Performance and accessibility

## Accessibility environment values

Read these in reusable components:

```swift
@Environment(\.accessibilityReduceTransparency) private var reduceTransparency
@Environment(\.accessibilityReduceMotion) private var reduceMotion
@Environment(\.accessibilityContrast) private var accessibilityContrast
@Environment(\.accessibilityDifferentiateWithoutColor) private var differentiateWithoutColor
```

When transparency is reduced, use `.background`, `.secondarySystemBackground`, or another opaque system color with a subtle border. When motion is reduced, replace morphs and bouncy springs with opacity, scale-free transitions, or short ease animations. When contrast is increased or color differentiation is required, pair tint with labels, icons, shape, or text state.

## Legibility

- Avoid glass behind dense text, code blocks, long markdown, forms, logs, tables, or multi-paragraph reasoning.
- Add a dimming gradient under overlay controls on bright media.
- Keep labels and icons high-contrast; verify light/dark modes and busy photo/video/PDF backdrops.
- Prefer `.foregroundStyle(.primary)` and `.secondary` instead of fixed white/black text.
- For tiny status chips, include text plus icon when state matters.
- For AI chat output, keep markdown mostly plain and put glass around controls, metadata toggles, and composer chrome.

## VoiceOver and semantics

- Icon-only buttons need `.accessibilityLabel` and often `.accessibilityHint`.
- Send/stop, record/stop, play/pause, pin/unpin, and expand/collapse must update labels with state.
- Custom tab bars must expose tab semantics, selection state, and reselection behavior. If that is hard, prefer native `TabView`.
- Search tabs should behave like search, not like unlabeled action buttons.
- Radial menus should be reachable linearly for VoiceOver; do not rely on spatial position alone.

## Dynamic Type and layout

- Minimum hit target: about 44 x 44 points.
- Let composer and chips wrap or scroll horizontally under large Dynamic Type.
- Avoid fixed heights for multi-line input; use min/max heights.
- Keep bottom controls above keyboard and home indicator with `safeAreaInset` or native toolbar placement.
- Test long localized strings in glass pills; truncation should not hide critical state.

## Motion

Use spring motion for direct manipulation and state changes. Prefer interruptible SwiftUI state animations or UIKit retargetable springs. Avoid infinite glare sweeps, particle loops, or display-link animations for normal controls.

Good defaults:

```swift
let liquidSpring = Animation.spring(response: 0.34, dampingFraction: 0.78, blendDuration: 0.08)
let settleSpring = Animation.interpolatingSpring(stiffness: 260, damping: 28)
```

Under Reduce Motion:

```swift
withAnimation(reduceMotion ? .easeOut(duration: 0.12) : liquidSpring) {
    isExpanded.toggle()
}
```

## GPU and overdraw

- Avoid nested glass/blur layers. One glass domain per group.
- Clip glass to compact shapes instead of full-screen materials.
- Avoid shader effects over scrolling lists; use them on isolated previews or hero controls.
- Do not animate blur radius every frame. Animate scale/opacity/offset instead.
- Avoid full-screen glass plus inner glass plus separate blur/shadow overlays.
- Use `GlassEffectContainer` for nearby controls rather than many isolated glass islands.
- Test with the Debug View Hierarchy and Instruments if a screen has many translucent overlays.

## ProMotion, battery, and offscreen work

ProMotion can make drag and morph interactions feel excellent, but do not depend on 120Hz. If using UIKit display links, Wave, or custom Metal, pause effects when offscreen and consider Low Power Mode.

```swift
let isLowPower = ProcessInfo.processInfo.isLowPowerModeEnabled
```

In Low Power Mode, prefer static highlights, simpler shadows, and lower-frequency animations. Keep custom shader effects opt-in and local to focal surfaces.

## Scrolling content

Liquid Glass usually belongs above scrolling content, not inside every scrolled row. Prefer:

- fixed bottom composer over a transcript
- floating toolbar over a reader/canvas
- tab/search accessories outside list rows
- edge controls over media

Avoid:

- glass cards for every message
- shader glare on every list cell
- glass text panels inside fast-scrolling content

## Snapshot/testing caution

Liquid Glass is environment-reactive, so pixel snapshots can be fragile. Prefer behavior tests and previews for layout. When snapshot-testing, use stable backgrounds, fixed color scheme, fixed Dynamic Type, and simulator OS matching the production SDK.

## Audit checklist

- Does glass appear only on controls/navigation/overlays?
- Is there no glass-on-glass stacking?
- Does Reduce Transparency produce an opaque readable surface?
- Does Reduce Motion remove morph-heavy or looping animations?
- Does Increase Contrast still read clearly?
- Are icon-only controls labeled?
- Are hit targets large enough?
- Does the design survive bright media backgrounds?
- Is any shader isolated, optional, and safe to disable?
- Are all APIs public and Xcode 26-native?


## Keyboard and bar placement

For bottom composers, prefer a native bar/inset path over manual `ignoresSafeArea(.keyboard)` hacks. Use `safeAreaBar` when the active iOS 26 SDK supports the desired bar behavior; otherwise use `safeAreaInset(edge: .bottom)` with padding that keeps scroll content visible. This prevents the glass composer from covering the last message or fighting the keyboard transition.

Use `backgroundExtensionEffect()` for imagery that should visually continue under sidebars or inspectors. It is a content-extension effect, not a substitute for glass controls and not a reason to put dense text over glass.
