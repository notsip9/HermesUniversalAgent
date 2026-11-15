# Hermes Universal Agent 0.4.0 — Development Preview

This is a reconstructed source preview created after the original development checkout was removed. It is not yet a stable release and does not replace the published 0.3.0 binary.

## New desktop tools
- List visible windows.
- Capture a screenshot with a separate local permission.
- Focus a window by handle.
- Click a screen coordinate.
- Type up to 500 characters into the focused control.

All desktop and screen permissions are disabled by default. Each action requires an explicit per-call confirmation. No arbitrary shell execution or background monitoring is included.

## Verification status
Automated tests and Windows packaging must pass before this preview is promoted or published as a new binary release.
