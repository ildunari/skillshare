# Menu Design

## Principles

- Every command must be reachable via the **menu bar**. Use consistent labels (verbs) and positions.
- Target actions to **nil**, allowing the **first responder** to handle them.
- Use **keyboard equivalents** extensively for frequent actions.

## Validation

Implement `NSMenuItemValidation.validateMenuItem(_:)` to enable/disable and retitle items contextually.
