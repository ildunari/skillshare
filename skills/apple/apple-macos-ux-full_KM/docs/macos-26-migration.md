# Migrating to Liquid Glass on macOS 26

macOS 26 introduces Liquid Glass, replacing the older vibrancy system
implemented via `NSVisualEffectView`.  Migrating to Liquid Glass improves
visual coherence with the system, provides adaptive contrast automatically
and offers new morphing behaviors.  This guide outlines how to update
existing macOS 25 and earlier apps to adopt Liquid Glass while maintaining
backwards compatibility.

## Assess your surfaces

Begin by auditing where you currently use custom blur layers, backdrop
materials or `NSVisualEffectView`.  Common areas include:

* Toolbars, navigation bars, search bars and header views.
* Sidebars and panels that separate content from controls.
* Popovers, sheets, inspectors and floating palettes.

For each surface, determine whether it benefits from Liquid Glass.  Dense
tables or text‑heavy views might remain on solid backgrounds.

## Replace `NSVisualEffectView` with `NSGlassEffectView`

`NSGlassEffectView` is the drop‑in replacement for `NSVisualEffectView`
when you want to adopt Liquid Glass.  Instead of setting a material and
blending mode, you configure corner radius and tint:

```swift
// Before: vibrancy using NSVisualEffectView
let effect = NSVisualEffectView()
effect.material = .sidebar
effect.blendingMode = .behindWindow
effect.state = .followsWindowActiveState

// After: Liquid Glass using NSGlassEffectView
let glass = NSGlassEffectView()
glass.cornerRadius = 12
glass.tintColor = .controlAccentColor // optional for prominent glass
```

* Do **not** set `.material` or `.blendingMode` on `NSGlassEffectView` — the
  system manages those properties.
* Always embed your existing content into `glass.contentView`.  Do not
  attempt to layer your previous content behind or in front of the glass
  manually.

## Group adjacent glass views

If your UI includes multiple adjacent effect views (e.g. sidebars next to
toolbars), wrap them in an `NSGlassEffectContainerView`.  This reduces
rendering overhead and enables seamless morphing.  Replace sibling
view constraints with a single container that holds a stack view of your
panels.  Adjust the `spacing` on the stack so that corners merge at
appropriate distances.

## Migrate toolbars

Update `NSToolbarItem` usage to opt in to Liquid Glass styles:

* Set `item.style = .prominent` for primary actions and `.plain` for
  secondary tools.
* Use `item.backgroundTintColor` to indicate meaning (primary, destructive,
  etc.).
* Ensure your window uses a unified toolbar style (`window.toolbarStyle = .unified`).

When customizing a toolbar, avoid adding your own translucent backgrounds
behind items — the system provides the glass surface.

## Respect system preferences

macOS 26 introduces a **Clear/Tinted** preference for Liquid Glass under
**System Settings → Appearance → Liquid Glass**.  Apps that use
`NSGlassEffectView` automatically adopt the current preference.  If your
application provided a custom translucency toggle before, remove it or
delegate to the system preference.

In addition, support **Reduce transparency**, **Increase contrast** and
**Reduce motion** under **Accessibility → Display**.  When these toggles
are enabled, fall back to solid surfaces and disable glass animations.

## Maintain backwards compatibility

Apps targeting macOS 25 and earlier should continue using
`NSVisualEffectView` when `NSGlassEffectView` is unavailable.  Wrap new
code paths in availability checks:

```swift
if #available(macOS 26.0, *) {
    let glass = NSGlassEffectView()
    glass.cornerRadius = 12
    // … configure and assign to contentView
} else {
    let effect = NSVisualEffectView()
    effect.material = .sidebar
    effect.state = .followsWindowActiveState
    // … configure and add as subview
}
```

Consider providing your own enumerations or helper functions to centralize
material selection.  This keeps your views agnostic of the underlying
material implementation.

## Performance improvements

Liquid Glass is more efficient than layered blur effects because it
performs a single sampling pass when grouped in containers.  Nevertheless,
profile your application using Instruments after migration:

* Test with Clear and Tinted glass across light and dark wallpapers.
* Measure frame rate when opening and closing floating palettes or
  collapsing sidebars — morphing should remain smooth.
* Group surfaces wherever possible to reduce compositing costs.

Adopting Liquid Glass not only aligns your app with the macOS 26 aesthetic
but also simplifies your codebase by offloading vibrancy, contrast and
tinting decisions to the system.  Use this migration as an opportunity
to clean up bespoke blur implementations and unify your UI surfaces.