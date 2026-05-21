# Animation And Visual Patterns

Use animation to explain continuity, state, and direct manipulation. Keep it short, interruptible, and tied to the surface the person is touching.

## Motion Hierarchy

Prefer these patterns in order:

1. System transitions: native sheets, popovers, menus, tab behavior, and navigation transitions.
2. Morphing: `GlassEffectContainer` plus `glassEffectID` for compact-to-expanded surfaces.
3. Symbol replacement: `.contentTransition(.symbolEffect(.replace))` for icon state changes.
4. Direct manipulation: drag translation, predicted end translation, and snap points.
5. Decorative effects: tiny highlights or shader-inspired effects only on isolated preview/hero surfaces.

Avoid constant shimmer, looping glare, bouncing controls that do not reflect user input, and motion that competes with content.

## Timing Defaults

Use state-based SwiftUI animation values that can be interrupted:

```swift
private var glassAnimation: Animation {
    reduceMotion ? .easeOut(duration: 0.12) : .spring(response: 0.32, dampingFraction: 0.82)
}
```

For small icon swaps, keep the transition under about 200 ms. For sheet or cluster expansion, a spring around 300-360 ms usually feels lively without becoming theatrical. When Reduce Motion is enabled, replace scale, morphing, and large movement with opacity or a short ease.

## Morphing Glass Surfaces

Use one namespace per local interaction domain:

```swift
@Namespace private var glassNamespace

GlassEffectContainer(spacing: 8) {
    Group {
        if isExpanded {
            ToolPanel()
                .glassEffect(.regular, in: .rect(cornerRadius: 24))
                .glassEffectID("tools", in: glassNamespace)
        } else {
            Button("Tools", systemImage: "slider.horizontal.3") { isExpanded = true }
                .buttonStyle(.glass)
                .glassEffectID("tools", in: glassNamespace)
        }
    }
}
.animation(glassAnimation, value: isExpanded)
```

Use stable IDs and keep source/destination shapes visually related. If the expanded surface is unrelated in position or shape, use a sheet/popover instead of forcing a morph.

## Direct Manipulation

Floating bars, command menus, and canvas controls should react to drag intent:

- Track translation for live offset.
- Use predicted end translation to choose open, collapsed, or dismissed states.
- Snap to stable positions; do not leave controls half-interactive.
- Keep controls reachable above the home indicator and keyboard.

## Visual Polish

Use real content under glass so the effect has something to sample. Media, canvas, maps, gradients, or image headers can support clear glass; plain lists usually need regular glass or opaque surfaces.

For text over media, add a local contrast layer:

```swift
LinearGradient(
    colors: [.clear, .black.opacity(0.28)],
    startPoint: .top,
    endPoint: .bottom
)
.allowsHitTesting(false)
```

Tint sparingly. Selected filters, active recording, streaming status, destructive actions, and primary submit controls are good candidates. Brand-colored glass everywhere makes the system material feel like decoration instead of interface.

## Agent UI Patterns

For agent clients:

- Composer: morph attachment/tools rows in and out of one bottom glass domain.
- Tool calls: animate chips into a compact status header; keep long reasoning text on a plain background.
- Canvas controls: fade controls while manipulating the canvas, then restore them on idle.
- Active-agent strip: use `tabViewBottomAccessory` for global state before custom tab bars.
- Command palette: use native sheets with partial detents; put glass on controls, not the command list body.

## Anti-Patterns

- Glass on every message, markdown block, table row, or settings cell.
- Multiple independent glass backgrounds stacked inside each other.
- Custom Metal/refraction effects for normal buttons.
- Private UIKit class probing for stronger effects.
- Motion that continues while Reduce Motion is enabled.
