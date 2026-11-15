# Hermes Universal Agent 0.4.0 — Windows Desktop Preview

**Windows x64 · Proprietary software · Local-first MCP companion**

Hermes Universal Agent runs locally on Windows and exposes a Model Context Protocol (MCP) server over standard input/output. It is a companion for an MCP-compatible AI client, not a standalone AI assistant.

## Capabilities

- List and read UTF-8 text files inside one configured workspace.
- Optional file creation and replacement, protected by a local setting and per-call confirmation.
- Save and search private notes in a local SQLite database.
- Report basic operating-system information.
- List visible windows, focus a window, click coordinates, and type text — only when desktop interaction is enabled locally and the individual tool call includes `confirm=true`.
- Capture a desktop screenshot — only when the separate screen-capture setting is enabled and the individual call includes `confirm=true`.

## Important limitations

- Windows 10/11 x64 is the supported target.
- Requires a compatible MCP client that can launch a local stdio process.
- Desktop actions operate on the currently interactive Windows session. Windows may deny foreground focus requests.
- This preview does not provide arbitrary shell execution, background monitoring, unattended control, or remote access.
- A user should never enable screen capture or desktop control on a shared or unattended computer without understanding the privacy implications.

## Install from source

1. Install Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Run `python -m pip install -e .`.
4. Launch `hermes-settings` to choose a workspace and permissions.
5. Configure your MCP client to launch `hermes-agent` (or the packaged MCP executable) over stdio.

For a developer build, run `scripts/build_windows.ps1` from PowerShell.

## Safe defaults

All permission switches default to off. File writes require both local permission and `confirm=true`. Desktop interaction requires its own local permission and per-call confirmation. Screen capture has a separate local permission and per-call confirmation. Settings and SQLite memory remain under `%LOCALAPPDATA%\\HermesUniversalAgent`.

## MCP tools

- `agent_status`, `workspace_list`, `workspace_read`, `workspace_write`
- `memory_save`, `memory_search`, `system_info`
- `desktop_windows`, `desktop_screenshot`, `desktop_focus_window`, `desktop_click`, `desktop_type_text`

## Licence

This is proprietary software. See [LICENSE.txt](LICENSE.txt). Third-party dependencies remain subject to their own licences.
