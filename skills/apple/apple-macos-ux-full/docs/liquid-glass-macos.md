# Liquid Glass on macOS 26

Liquid Glass is one of the headline visual updates in macOS 26 (Tahoe).  It replaces
the traditional vibrancy materials found in previous releases with a new,
physics‑inspired surface that bends light, preserves content legibility and
morphs organically when elements are grouped together.  This document focuses
on **AppKit** usage of Liquid Glass and how it integrates with the rest of the
macOS UX primitives in this skill.

## What is Liquid Glass?

Liquid Glass is a *transparent yet legible* material that adapts its appearance
to the underlying content.  Unlike the older vibrancy and blur materials,
Liquid Glass does not simply scatter light; it refracts and concentrates it
to maintain definition even over busy backgrounds.  The surface subtly
flexes and morphs in response to user interaction and when adjacent glass
elements are grouped together.  Developers adopt Liquid Glass by using
`NSGlassEffectView` or SwiftUIʼs `glassEffect` modifier rather than building
their own blur layers.

Liquid Glass should be used for:

* **Toolbars and navigation surfaces** — unified and floating toolbars look
  weightless while clearly separated from content.
* **Sidebars and grouped controls** — sidebars adopt concentric rounded
  corners and morph when collapsed/expanded.
* **Popovers, sheets and palettes** — transient elements gain subtle depth
  without heavy chrome.
* **Grouped controls** — grouping multiple buttons into one glass plane reduces
  visual seams and improves morphing.

Avoid placing large bodies of text or dense tables directly on glass.
When legibility is paramount, switch to a **prominent** (tinted) glass style
or a solid surface.

## Core AppKit APIs

### `NSGlassEffectView`

`NSGlassEffectView` is the primary AppKit API for Liquid Glass.  It manages
the glass material and automatically applies adaptive shadows, tinting and
contrast adjustments to its content.  You embed your own views inside the
`contentView` rather than layering glass behind content.  This ensures the
system applies vibrancy and legibility correctly.

```swift
import AppKit

let glass = NSGlassEffectView()
glass.cornerRadius = 14
glass.tintColor = .controlAccentColor

// Place your custom view inside the contentView
let stack = NSStackView()
stack.orientation = .vertical
// populate stack…
glass.contentView = stack

// Add glass to your window’s view hierarchy
window.contentView?.addSubview(glass)
glass.translatesAutoresizingMaskIntoConstraints = false
NSLayoutConstraint.activate([
    glass.leadingAnchor.constraint(equalTo: window.contentView!.leadingAnchor),
    glass.trailingAnchor.constraint(equalTo: window.contentView!.trailingAnchor),
    glass.topAnchor.constraint(equalTo: window.contentView!.topAnchor),
    glass.bottomAnchor.constraint(equalTo: window.contentView!.bottomAnchor)
])
```

**Guidelines**

* Always set `contentView` instead of adding siblings behind your glass view.
* Use rounded corners (`cornerRadius`) that echo your window’s geometry.
* Don’t hard‑code text colors; rely on vibrancy and `tintColor` for accent.

### `NSGlassEffectContainerView`

Multiple glass surfaces that are near each other should be grouped using
`NSGlassEffectContainerView`.  Grouping reduces the number of sampling passes
and allows nearby panes to **morph** into a unified shape when spacing is
small.  Place your layout stack inside the container’s `contentView` and let
the system manage merging and tint propagation.

```swift
// Create left and right panels with glass
let left = NSGlassEffectView()
left.cornerRadius = 12
let right = NSGlassEffectView()
right.cornerRadius = 12

let hstack = NSStackView(views: [left, right])
hstack.spacing = 18
// Each panel hosts its own content in its contentView

let container = NSGlassEffectContainerView()
container.contentView = hstack

rootView.addSubview(container)
// constrain container as needed
```

**When to group**

* Group toolbars with their contextual palette when they float together.
* Group sidebars and adjacent filter panels so their corners merge when
  collapsed.
* Use a container to reduce GPU cost when several glass buttons sit next to
  each other (e.g. toolbars or floating palettes).

### Glass‑aware toolbars

macOS 26 introduces glass styling for `NSToolbarItem`.  Set
`item.style = .prominent` or `.plain` and adjust `backgroundTintColor` to
indicate importance.  A prominent style increases opacity and contrast for
primary commands.

```swift
let item = NSToolbarItem(itemIdentifier: .init("compose"))
item.label = "Compose"
item.style = .prominent
item.backgroundTintColor = .systemBlue
```

**Guidelines**

* Use **prominent** style sparingly for your primary call‑to‑action; keep
  secondary items plain.
* Avoid placing text labels directly on glass; rely on icons for concise
  toolbars.
* Let the toolbar participate in the glass container when it floats next to
  other glass elements.

### Unified glass surfaces

Liquid Glass encourages unifying surfaces across the window chrome.  A
window’s unified toolbar, sidebar and floating palettes should share a
single glass plane when visually adjacent.  Achieve this by embedding
adjacent toolbars, sidebars or palettes inside a shared
`NSGlassEffectContainerView` and aligning their corners (concentricity).

### Morphing behaviors

When spacing between panes in a container is small, Liquid Glass will
**morph** those panes together with a subtle organic animation.  You can
control the spacing to determine when morphing starts.  For toolbars or
palettes that appear/disappear, assign consistent identities so that the
morphs animate smoothly.  AppKit handles morphing automatically when
surfaces are grouped in a container; you just need to keep the order and
layout stable across state changes.

### Clear vs. Tinted preference

Users can choose between **Clear** and **Tinted** glass system‑wide under
**System Settings → Appearance → Liquid Glass**.  Clear glass is airy and
translucent; Tinted adds opacity and contrast for better legibility.  If
your app uses system APIs (`NSGlassEffectView`, `NSToolbarItem.style`), it
inherits this preference automatically.  Only expose an in‑app toggle if
your domain has very specific legibility needs; otherwise defer to the
system.

**Accessibility & preferences**

* Respect **Reduce transparency** and **Increase contrast** in **System
  Settings → Accessibility → Display**.  When transparency is reduced,
  replace glass with a solid fill.
* Respect **Reduce motion** by disabling bounce and flex animations on
  glass surfaces.
* Test your controls on both Clear and Tinted with varying backgrounds to
  ensure contrast.  Use the built‑in color contrast checker in Xcodeʼs
  accessibility inspector.

## Design patterns

### Toolbar integration

* Adopt unified toolbars (`window.toolbarStyle = .unified`) and place your
  primary commands on glass.  Use `NSToolbarItem.style = .prominent` for a
  key action and `.plain` for secondary controls.
* Avoid piling toggles and segmented controls; group related tools into
  a single glass container to reduce visual clutter.
* Let the toolbar share a container with adjacent search fields or filter
  palettes so that morphing feels intentional.

### Sidebar patterns

* Implement sidebars using `NSSplitView` and wrap the sidebar list in
  `NSGlassEffectView`.  Match the window’s corner radius on the outer edge
  of the sidebar for concentricity.  Avoid glass inside your detail area;
  it should remain on a solid or tinted surface.
* When a sidebar collapses or expands, group it with adjacent panels in
  `NSGlassEffectContainerView` so that the glass morphs seamlessly.

### Floating palettes & HUD windows

* Use `NSPanel` with `isFloatingPanel = true` and embed your content in
  `NSGlassEffectView` for inspectors, color pickers or mini‑toolbars.
* For heads‑up displays (HUD), set the panel’s style mask to `.hudWindow`
  and apply a tinted glass effect via `NSGlassEffectView`’s `tintColor`.
* Provide a **Close** affordance and ensure the panel participates in
  the responder chain like any other window.

### Popovers & sheets

* On macOS 26, popovers and sheets automatically adopt Liquid Glass when
  built with SwiftUI’s `.popover` or `.sheet` modifiers.  For AppKit
  popovers, embed the content view in `NSGlassEffectView` manually.
* Keep popovers concise; avoid dense toolbars on glass surfaces.  If the
  background competes with the content, use a **prominent** (tinted)
  style for the glass.

## Performance considerations

Liquid Glass incurs a small GPU cost for sampling the underlying content
and animating morphs.  To keep your app responsive:

* Group related glass views into a single `NSGlassEffectContainerView` to
  reduce sampling passes.
* Avoid animating blur radius or other expensive effects; animate
  transforms, opacity or `tintColor` instead.
* Test on older hardware (e.g. 2018 MacBook Air) to ensure frame rates
  remain smooth when glass surfaces are present.

## Migration from `NSVisualEffectView`

`NSVisualEffectView` remains available for backwards compatibility, but
Liquid Glass should replace it in most cases.  When migrating:

* Remove custom background layers or blur shaders; adopt
  `NSGlassEffectView` instead.
* For groups of `NSVisualEffectView`, replace them with a single
  `NSGlassEffectContainerView` wrapping individual `NSGlassEffectView`s.
* Adjust your corner radii and spacing so that morphing triggers at the
  appropriate point.
* Keep your legacy code paths behind availability checks (`if #available`)
  to support macOS 25 and earlier.

Refer to the migration document (`macos-26-migration.md`) for a
step‑by‑step checklist.