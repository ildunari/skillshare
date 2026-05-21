# iOS 26 Liquid Glass API map

## Selection rule

Choose the smallest native API that achieves the interaction. Use a standard component first, then glass button styles, then `glassEffect`, then `GlassEffectContainer`/IDs for coordinated groups, then SDK-verified unioning only when needed, then custom shaders only for isolated decorative effects.

## SwiftUI core glass APIs

| API | Use for | Notes |
|---|---|---|
| `.glassEffect(_:in:)` | Custom glass controls, compact overlays, bars, pills | Apply to the shape that should refract. Avoid text-heavy blocks. |
| `.glassEffect(_:in:isEnabled:)` | Conditional glass enablement | Prefer to toggling legacy materials when the active SDK exposes this overload. |
| `Glass.regular` | Most controls and navigation overlays | Default choice. Works well with clear content hierarchy. |
| `Glass.clear` | Minimal glass over media/canvas | Needs contrast/dimming behind text and icons. Do not mix visually with Regular in one group unless intentional. |
| `Glass.identity` | Inactive cell in a morphing-selection group (filter pills, tab rail, segmented control) | **SDK-verified real Glass variant** — present in `SwiftUICore.swiftinterface` as `public static var identity: Glass { get }`. Renders no visible effect but keeps the view in the morph graph so `GlassEffectContainer` + `glassEffectID` can morph the selection between cells. Render the glass for every cell (`.identity` inactive, `.regular.tint(...)` active) instead of `if isSelected { Glass() }` — the conditional form destroys + re-creates the view and breaks the morph. Many third-party docs incorrectly claim `.identity` doesn't exist; trust the SDK header. |
| `.tint(_:)` on glass | Selected, destructive, recording, primary, or status semantics | Tint should communicate state, not branding decoration. |
| `.interactive()` on glass | Buttons, draggable knobs, pressable chips | Gives native touch response. Avoid on static labels. |
| `GlassEffectContainer(spacing:)` | Related controls that should blend/morph as one group | Use around composer controls, FAB clusters, toolbar groups, and segmented controls. Spacing 20–24 lets glass blobs flow between sibling cells for selection morph; spacing 0 prevents merging. Don't wrap glass-on-glass: if the container itself needs a backdrop, use `.ultraThinMaterial`, not another `.glassEffect`. |
| `.glassEffectID(_:in:)` | Morphing a glass element between compact/expanded states or between sibling cells | IDs should be stable per logical morph target — for a cross-cell selection morph, use the SAME id (e.g. `"selection"`) on every cell with the same namespace, so the morph target is identical and only the active cell renders visible glass. |
| `.glassEffectUnion(id:namespace:)` | Optional connected rendering for separated controls | Use only when the active SDK supports it and separated elements truly need to read as one glass group. The default generated path is container + ID. |
| `.glassEffectTransition(...)` | Materializing or matched glass transitions | Use when the system should animate glass material as views appear/disappear. Verify exact SDK spelling. |

## SwiftUI controls and motion

| API | Use for | Notes |
|---|---|---|
| `.buttonStyle(.glass)` | Secondary icon/text controls | Prefer before custom button backgrounds. |
| `.buttonStyle(.glassProminent)` | Primary/send/confirm controls | Use sparingly so prominence remains meaningful. |
| `.contentTransition(.symbolEffect(.replace))` | Icon changes like send to stop, mic to waveform, expand to collapse | Pair with state changes and accessibility labels. |
| `NavigationTransition.zoom` + `matchedTransitionSource` | List/grid/card to detail continuity | Ideal for threads, media gallery, previews, and agent sessions. |
| Springs / predicted drag translation | Direct manipulation and state changes | Prefer interruptible state-based animation; simplify when Reduce Motion is on. |

## Tabs, search, and bottom chrome

| API | Use for | Notes |
|---|---|---|
| Native `TabView` iOS 26 styling | Main app navigation | Prefer native tab bars before custom bars. Use custom only for FAB or bespoke item content. |
| `Tab(role: .search)` | Dedicated search tab or mode | Use when search is a first-class root surface. Do not fake search with an action-only tab. |
| `tabBarMinimizeBehavior` | Let tab bar minimize while scrolling | Good for content-heavy screens where the bar should get out of the way. |
| `tabViewBottomAccessory` | Mini active-agent/player/status strip above tab bar | Use for global running-agent status, compact composer launcher, or queue state. |
| `.searchable(...)` | Standard app and list search | Default choice for search fields. Scope search to the nearest meaningful navigation/list surface. |
| `DefaultToolbarItem(kind: .search, placement: .bottomBar)` | iPhone bottom-bar search beside local tools | Use when the active SDK exposes it and the product needs bottom-reachable search. |
| `ToolbarSpacer(.flexible, placement: .bottomBar)` | Search + compose/filter/sort layouts | Keeps bottom toolbar groups breathable. Verify exact SDK spelling. |
| `safeAreaInset` / `safeAreaBar` | Bottom composers, floating controls | Prefer `safeAreaBar` for an iOS 26 custom bar that should participate in the new bar model; use `safeAreaInset` when compatibility or exact SDK spelling is uncertain. |
| `backgroundExtensionEffect()` | Images/media/header content under sidebars or inspectors | Extends and blurs the source visual around its edges. Use for continuity behind system panels, not as a replacement for `glassEffect`. |

## Sheets, popovers, and source-linked presentation

| API | Use for | Notes |
|---|---|---|
| Native `.sheet(...)` | Settings, command palettes, tool inspectors | Prefer system sheet glass and morphing before custom backgrounds. |
| Partial detents such as `.presentationDetents([.medium, .large])` | Floating sheet behavior | Useful for command palettes and filters. Avoid overriding system background unless intentional. |
| `.popover(...)` / menus | Compact local commands | Glass belongs on controls inside the popover, not on dense text bodies. |
| Source-linked sheet/menu/navigation transitions | Button-to-panel continuity | Use when a sheet or detail expands from a visible control. |

## UIKit APIs

| API | Use for | Notes |
|---|---|---|
| `UIGlassEffect` | UIKit glass material | Use public constructors/properties only. Avoid private class probing. |
| `UIGlassEffect.isInteractive` | Pressable UIKit glass controls | Match SwiftUI `.interactive()` intent. |
| `UIGlassEffect.tintColor` | UIKit semantic tint | Use for selected/primary/status semantics, not blanket branding. |
| `UIGlassContainerEffect` | Multiple UIKit glass views in one domain | Useful for custom UIKit toolbars or segmented controls. |
| `UIVisualEffectView(effect: UIGlassEffect())` | Hosting UIKit glass effects | Keep layers shallow and sized to the control. |
| `UIButton.Configuration.glass()` | UIKit secondary buttons | Prefer over manual blur backgrounds when available. |
| `UIButton.Configuration.prominentGlass()` | UIKit primary buttons | Use for confirm/send/primary local action. |
| `UISymbolContentTransition(.replace)` | UIKit icon swaps | Use for send/stop, play/pause, expand/collapse. |
| `UITabBarController.setBottomAccessory(_:animated:)` | UIKit tab apps needing a global accessory | Use for active agent status, mini player, queue state. |
| Standard `UITabBar`, `UINavigationBar`, `UISheetPresentationController` | App navigation and presentations | Prefer native refreshed components before custom reconstruction. |

## AI-client mapping

| Product need | API pattern |
|---|---|
| Chat composer | `safeAreaInset` + `GlassEffectContainer` + `.glassEffect(.regular.interactive())` + `.buttonStyle(.glassProminent)` |
| Tool row / attachments | Horizontal chips with `.glassEffect`, `glassEffectID` when expanded/collapsed |
| Agent status | Small tinted glass pills; plain text outside glass for logs/markdown |
| Thread list filters | Native `.searchable` plus filter pills in one container; keep rows mostly plain |
| Canvas/media controls | Clear or regular glass capsules over media; add dimming gradient behind text |
| Floating toolbar | One container with icon buttons; minimize or fade on scroll/drag |
| Radial menu | GlassEffectContainer, springy scale/opacity, stable IDs for items |
| Gallery detail | `matchedTransitionSource` and `NavigationTransition.zoom` |
| Reasoning panel | Plain content body; glass edge controls and status header |
| Global active-agent indicator | `tabViewBottomAccessory` or UIKit bottom accessory before a custom tab bar |

## Fallbacks

This skill is iOS 26-first. If the deployment target includes older OS versions, add an availability wrapper that uses `.regularMaterial`, opaque backgrounds, or standard controls below iOS 26. Do not replace native iOS 26 behavior with a backport library by default.


## Migration and compatibility keys

| API/key | Use for | Notes |
|---|---|---|
| `UIDesignRequiresCompatibility` | Temporary migration opt-out from the new design when rebuilding older apps with the iOS 26 SDK | Do not use as a generated component strategy. Mention only when auditing adoption risk or planning a phased migration. |
| Availability fallbacks | Apps that still deploy below iOS 26 | Use `.regularMaterial`, opaque system backgrounds, or standard controls below iOS 26. Keep native iOS 26 code as the primary path. |
