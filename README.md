# Hermes Universal Agent

**Windows x64 | Proprietary software | Development rebuild**

Hermes Universal Agent is a local-first Windows companion that exposes carefully scoped computer capabilities to a compatible AI client through a local Model Context Protocol (MCP) server.

> **Development status:** The original 0.3.0 release remains unchanged. This branch is a source reconstruction for the next development line. It is not yet a supported end-user release.

## Goals

- One locally installed companion with a small Settings application.
- Local stdio MCP transport; no public endpoint, tunnel client, port forwarding, bearer token, or scheduled task.
- Workspace access confined to a user-selected folder.
- Local SQLite memory.
- Optional Windows desktop observation and interaction, with every sensitive permission disabled by default.
- Reproducible Windows builds and automated tests.

## Current source implementation

- agent_status, system_info
- workspace_list, workspace_read, workspace_write
- memory_save, memory_search
- desktop_windows_list, desktop_window_focus
- desktop_screen_capture
- desktop_mouse_click
- desktop_keyboard_type, desktop_keyboard_hotkey

The desktop interaction tools are guarded by local settings and per-action confirm=true. Keyboard shortcuts use a built-in allowlist. There is no arbitrary shell or command-execution tool.

## Security defaults

- All permissions, including file writes and desktop control, default to **off**.
- File writes require local opt-in and confirm=true on each call.
- Screen capture, window focus, mouse clicks, and keyboard input each require their own local opt-in and per-call confirmation.
- Workspace paths are resolved and checked against the configured root, including symlink resolution.
- Text reads and writes are limited to 512,000 bytes.
- Local settings and memory stay under %LOCALAPPDATA%\HermesUniversalAgent.
- No telemetry or remote control endpoint is implemented.

Screen contents, window titles, and keyboard input can expose private information. Enable only the permissions needed for a task. Do not use this software for covert monitoring or unattended control.

## Development setup

Requires Windows 10/11 x64 and Python 3.11 or newer.

    py -3.12 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install -e ".[dev]"
    python -m pytest
    python -m ruff check src tests

Run the MCP server with hermes-agent. Run the local Settings app with hermes-agent-settings.

Both entry points are also available through python -m hermes_universal_agent.server and python -m hermes_universal_agent.settings_app after installation.

## Packaging

Windows binaries will be produced by the release workflow only after the source and integration tests are validated. Development builds must not replace the 0.3.0 public release.

## Integration note

The intended ChatGPT Desktop experience is a desktop-only, approved plugin with the bundled local stdio server. Public GitHub binaries do not bypass OpenAI approval or allowlisting. Other MCP-compatible desktop clients may use their own supported local stdio integration.

## Licence

Use and distribution are governed by LICENSE.txt and any applicable third-party licences. This repository's source rebuild is under active development; obtain legal review before public distribution.
