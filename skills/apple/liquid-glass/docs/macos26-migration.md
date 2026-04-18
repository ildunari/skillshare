# Migrating to Liquid Glass on macOS 26

macOS 26 brings Liquid Glass into window chrome, sidebars, inspectors, toolbars, and custom glass surfaces. The migration is less about recreating iOS frosted panels and more about letting standard macOS structures adopt the new system material naturally.

## Audit first

1. Remove custom blur or translucency layers used to fake sidebar, toolbar, or inspector glass.
2. Delete redundant backgrounds behind system toolbars, title areas, and split-view chrome.
3. Find views that really belong to window chrome versus normal document content.

If a view is regular content, do not force Liquid Glass onto it just because the surrounding window uses it.

## Prefer system structure

Start by moving toward the standard macOS app structure that gets glass automatically:

- `NavigationSplitView` for sidebar + detail layouts
- `NSSplitViewController` / SwiftUI inspectors for side panels
- standard toolbars instead of hand-rolled titlebar containers
- `backgroundExtensionEffect()` where content should continue beneath floating glass sidebars

The more you use the built-in structure, the less custom glass work you need.

## Adopt glass APIs deliberately

- For custom AppKit surfaces, migrate `NSVisualEffectView` patterns to `NSGlassEffectView` where true Liquid Glass is the right fit.
- For SwiftUI-hosted custom panels, prefer `glassEffect(_:in:)` on bounded controls and floating panels rather than large document regions.
- Use tinted/prominent glass only where hierarchy or emphasis actually needs it.

## Sidebars, inspectors, and toolbars

- Let sidebars and inspectors float above content instead of painting opaque slabs behind them.
- Avoid adding extra blur behind system toolbars or traffic-light regions.
- Keep toolbar items simple and semantic; glass works best when the chrome is clean.

## Accessibility and legibility

- Respect Reduce Transparency by switching custom glass surfaces to solid fills.
- Avoid putting dense editable text, long tables, or document-heavy regions on glass.
- Use semantic foreground styles so the system can maintain contrast as the backdrop changes.

## Test pass

Before calling the migration done, verify:

- Light and Dark Mode
- Reduce Transparency and Increase Contrast
- window resizing and sidebar collapse/expand behaviour
- toolbar legibility over bright and dark document content
- split-view layouts with content extending under glass chrome

## Common mistakes

- Porting iOS-style floating glass cards directly into macOS document layouts
- Leaving old `NSVisualEffectView` layers behind system chrome
- Using custom titlebar backgrounds that fight the new window material
- Applying glass to content-heavy panes where an opaque surface reads better
