# Security

This development branch reconstructs Hermes Universal Agent as a local Windows MCP companion. The server uses stdio and does not open a network listener.

## Security boundaries

- Workspace access is confined to the locally configured root. Resolved paths are checked to prevent parent traversal and symlink escapes.
- File writes are disabled by default and require both local opt-in and confirm=true on each request.
- Screen capture, window enumeration/focus, mouse input, and keyboard input each have separate local permissions. All default to off.
- Desktop actions require confirm=true on the individual request.
- Keyboard shortcuts are restricted to a small built-in allowlist.
- There is no arbitrary shell execution, process launch, remote endpoint, persistence mechanism, or unattended screen monitoring.
- Text file operations are limited to 512,000 bytes.
- Local settings and notes are stored under %LOCALAPPDATA%\HermesUniversalAgent.

Screen images, window titles, and typed text can contain sensitive information. Enable only the permissions required for a task. A connected AI client may receive tool output and process it under its own terms.

## Reporting a vulnerability

Do not publish exploitable vulnerability details in a public issue. Use GitHub's private vulnerability reporting feature for this repository if it is enabled. If private reporting is unavailable, open a public issue asking for a private reporting channel without including exploit details, secrets, personal data, or private files.

Include the affected version, concise reproduction steps, and impact in a private report. Do not include passwords, API keys, private files, or personal data.
