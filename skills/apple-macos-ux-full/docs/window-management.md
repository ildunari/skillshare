# Window Management

This guide covers frame autosave, restoration, tabbing, and multi-window orchestration.

## Autosave & Restoration

- Set a unique `window.setFrameAutosaveName("MainWindow")` for each window role.
- To participate in system restoration:
  - Set `window.isRestorable = true`.
  - Implement `NSWindowRestoration` or encode state in `willEncodeRestorableState` / `didDecodeRestorableState`.
- Avoid surprises: restore **positions**, **split ratios**, and **visibility** explicitly.

## Tabbing

- Disable globally if it conflicts with your UX: `NSWindow.allowsAutomaticWindowTabbing = false`.
- Prefer role‑based tab groups only when it improves workflows; otherwise keep windows independent.

## Roles & Registry

Maintain a central registry keyed by **role** (Main, Inspector, Library). See `WindowManager.swift` in `scripts/` generator output.
