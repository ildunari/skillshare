# Composer Patterns for Liquid Glass

Bottom composers and chat input bars are one of the easiest places to overdo Liquid Glass.

The rule of thumb is simple: treat the composer like app chrome, not like content cards.

## Best default

If the composer behaves like persistent navigation chrome, place it in a bottom toolbar item or a `safeAreaBar(edge: .bottom)` so the system can give it the right scroll-edge behaviour.

- Use `toolbar` / `.bottomBar` when the layout is simple and maps cleanly to bar items.
- Use `safeAreaBar(edge: .bottom)` when you need a richer custom composition.

## What to glass

Prefer one shared outer glass surface for the composer.

Good pattern:
- one rounded glass shell
- controls grouped inside it
- send / attach buttons using `.glass` or `.glassProminent`
- text input styled to sit inside the shell without adding another full-strength glass bubble

Avoid:
- separate glass bubbles on every child control
- stacking `.glassEffect()` on a `TextField` that already lives in a toolbar glass context
- making a dense multiline editor fully translucent if legibility suffers

## Toolbar vs custom safeAreaBar

### In a toolbar / `.bottomBar`

A text field already participates in the bar styling. Do not add another `.glassEffect()` to the field.

```swift
.toolbar {
    ToolbarItem(placement: .bottomBar) {
        TextField("Message", text: $draft)
    }
}
```

### In a custom `safeAreaBar`

You own the bar surface, so add glass to the outer composer shell.

```swift
.safeAreaBar(edge: .bottom) {
    GlassEffectContainer(spacing: 10) {
        HStack(spacing: 10) {
            Button {
                // attach
            } label: {
                Image(systemName: "plus")
            }
            .buttonStyle(.glass)

            TextField("Message", text: $draft, axis: .vertical)
                .textFieldStyle(.plain)
                .padding(.horizontal, 14)
                .padding(.vertical, 12)
                .frame(minHeight: 44)

            Button("Send") {
                // send
            }
            .buttonStyle(.glassProminent)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 10)
        .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 24, style: .continuous))
    }
    .padding(.horizontal)
}
```

## Interaction and readability

- Use `.interactive()` only on tappable controls, not the entire static composer shell.
- For multiline or long drafting, preserve readability first. A slightly more solid text-entry region inside a glass shell is often better than a fully translucent editor.
- Respect Reduce Transparency by replacing the shell with a solid fill.
- Let semantic foreground styles drive contrast; avoid hardcoded text colours.

## Anti-patterns

- Building the composer as an overlay with custom blur when `safeAreaBar` or toolbar placement would give you the right system behaviour
- Giving the text field its own glass bubble inside an already-glass toolbar
- Treating the composer like a stack of cards instead of one coherent surface
- Using glass for long-form editable regions where the background competes with the text
