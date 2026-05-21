# AppKit Gotchas (Field Notes)

- `validateMenuItem` isn't called if your controller isn't in the responder chain.
- Focus rings can be clipped on layer‑backed views — implement `drawFocusRingMask` and call `noteFocusRingMaskChanged()`.
- Window tabbing can leak into apps — disable globally or per window if it harms UX.
- When hiding the Dock icon for status bar apps, **always** provide a Quit affordance.
