# Source evaluation addendum

This file records how to use community articles, videos, discussions, and uploaded draft packages. It complements `references/library-evaluation.md`, which focuses on third-party packages.

## Evaluation frame

Score sources by API accuracy, production usefulness, maintenance risk, and whether the source demonstrates real SwiftUI/UIKit code or only visual hype. Engagement and star counts are weak signals unless source quality also checks out.

## Apple official material

Classification: source of truth.

Use Apple docs, WWDC sessions, HIG material guidance, and Landmarks samples to settle API and design conflicts. Prefer standard components first because they inherit the system design and accessibility behavior with less custom code.

## Focused implementation articles

Classification: implementation guidance.

Donny Wals, Swift with Majid, Nil Coalescing, SerialCoder, and Create with Swift are useful for concrete SwiftUI patterns: glass variants, grouping, tabs/search/accessories, sheets/forms, and source-linked transitions. Treat these as practical explanations, not replacements for the active SDK.

## Kavsoft and visual tutorials

Classification: creative animation inspiration.

Use for motion timing, morphing menu ideas, expandable toolbars, toasts, and state choreography. Adapt the ideas into native `GlassEffectContainer`, `glassEffectID`, native button styles, and standard presentations. Do not copy raw custom-path or shader-heavy code as the default production implementation.

## Reddit, forums, and X posts

Classification: pitfalls and reality checks.

Use these sources to identify recurring pain points: keyboard overlap around composers, per-row glass performance, cold-start GPU spikes from many independent glass layers, tint readability on light backgrounds, and Reduce Motion/Reduce Transparency surprises. Cross-check technical claims with Apple docs before turning them into skill rules.

## Uploaded pasted markdown

Classification: reference-only.

The pasted markdown reinforces the active skill’s core stance: native iOS 26 APIs, AI-chat focus, Liquid Glass for navigation/control/overlay chrome, accessibility safeguards, `GlassEffectContainer`, and `glassEffectID`. It also mentions `backgroundExtensionEffect()`, which is now explicitly mapped in `references/api-map.md`. Do not copy its sample frontmatter because it uses fields and names that do not satisfy the open-skill validator.

## Uploaded `files-1f1f93fe.zip`

Classification: reference-only / partially integrated.

Useful deltas integrated:

- `safeAreaBar` as a native iOS 26 bar-placement option beside `safeAreaInset`.
- `backgroundExtensionEffect()` for extending media/image backgrounds under sidebars or inspectors.
- `UIDesignRequiresCompatibility` as a temporary migration/compatibility switch, not a Liquid Glass implementation strategy.
- A source-evaluation habit that separates Apple/docs/articles from community hype.

Not copied wholesale:

- Its `SKILL.md` frontmatter contains unsupported keys and a non-kebab-case name.
- Several snippets combine glass buttons with legacy material underlays or broad `.glassEffect()` usage that is less disciplined than the active skill.
- The package would duplicate competing guidance if imported directly.

## Practical recommendation

When a new source appears, integrate only durable ideas into `SKILL.md`, `references/`, snippets, or recipes. Keep bulky raw artifacts outside the shipped skill package, then keep the active skill concise and native-first.
