# Prompt recipes

Use these examples to calibrate how an agent should apply this skill.

## Chat and composer prompts

**User prompt:** “Build a Liquid Glass composer for an iOS 26 agent app with attachments, voice, send/stop, and a tools row.”

**Skill response:** Produce a SwiftUI bottom composer first. Use one glass slab, `GlassEffectContainer`, `.buttonStyle(.glass)` for secondary controls, `.buttonStyle(.glassProminent)` for send/stop, symbol replacement, adaptive Reduce Motion/Transparency behavior, and a preview.

**User prompt:** “My chat transcript feels too cardy; make it iOS 26 Liquid Glass.”

**Skill response:** Remove glass from message bodies. Keep markdown content plain and move Liquid Glass to composer, tool metadata, filter controls, and media overlays.

## Navigation/search prompts

**User prompt:** “Add search and an active-agent mini strip to my iOS 26 tab app.”

**Skill response:** Use native `TabView`, `.searchable`, `tabViewBottomAccessory`, and `tabBarMinimizeBehavior` before a custom tab bar. Add a compact glass accessory only for active status/actions.

**User prompt:** “Make a custom Liquid Glass tab bar with a center FAB.”

**Skill response:** First ask whether native `TabView` plus accessory/FAB overlay is sufficient. If not, warn about custom tab semantics and generate accessible SwiftUI with clear selection state.

## Agent/tool prompts

**User prompt:** “Make this tool-call panel feel native.”

**Skill response:** Use a glass header/edge handle and status chips. Keep dense logs/reasoning body plain or opaque. Add collapse/expand symbol replacement.

**User prompt:** “Add streaming/thinking UI for the agent.”

**Skill response:** Use compact status pills, dots, and icon transitions. Avoid full-screen shimmer or looping shader effects.

## Media/canvas prompts

**User prompt:** “Build glass controls over an image/PDF/video preview.”

**Skill response:** Anchor controls to safe edges, use compact regular/clear glass, add dimming behind icons over busy media, and keep the canvas itself unboxed.

**User prompt:** “Make thumbnails zoom into a detail viewer.”

**Skill response:** Use `matchedTransitionSource` and `NavigationTransition.zoom`; add glass overlay controls in the destination.

## Shader/polish prompts

**User prompt:** “Can you add refraction/glare/chromatic Liquid Glass polish?”

**Skill response:** Start with public-API overlays/rims/highlights. Offer Metal only as isolated optional hero/canvas polish and include accessibility/power disable paths.

## Dependency/audit prompts

**User prompt:** “Should we use this LiquidGlassKit package?”

**Skill response:** Apply `references/library-evaluation.md`: inspect package targets, public APIs, source quality, examples, tests, maintenance, private API usage, and alignment with native iOS 26. Do not rely on stars or README claims alone.

## Background extension / safe-area bar

**User prompt:** “My iPad detail view has a big generated image and an inspector/sidebar. Make it feel iOS 26-native and add a bottom composer.”

**Skill response:** Use `backgroundExtensionEffect()` on the hero/media surface so it continues under sidebars or inspectors, then use `safeAreaBar` or `safeAreaInset` for the bottom composer. Keep the composer/actions glassy and keep dense content readable on stable backgrounds.
