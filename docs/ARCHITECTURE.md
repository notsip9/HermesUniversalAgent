# Architecture

## Process model

The desktop companion consists of two local processes:

1. Settings UI — a Tkinter application that edits %LOCALAPPDATA%\HermesUniversalAgent\settings.json.
2. MCP server — launched by a supported AI desktop host over stdio. It exposes narrowly scoped tools and never opens a network listener.

The server reads the same local settings file. Sensitive operations fail closed if settings are missing, malformed, or disabled.

## Trust boundaries

- The AI client is not treated as the authority for local permission. Every sensitive operation checks both the local permission and a per-call confirmation value.
- The configured workspace is the only file-access root. Paths are resolved before use to prevent parent traversal and symlink escapes.
- Local memory is stored in SQLite under the app's local data directory.
- Desktop operations are limited to screen capture, exact-title window focus, coordinate clicks, ASCII typing, and a small keyboard shortcut allowlist.
- No arbitrary shell, PowerShell, process launch, persistence, remote endpoint, or background surveillance tool is exposed.

## Permissions

| Permission | Tools | Default |
| --- | --- | --- |
| file_writes | workspace_write | Off |
| screen_capture | desktop_screen_capture | Off |
| window_control | desktop_windows_list, desktop_window_focus | Off |
| mouse_input | desktop_mouse_click | Off |
| keyboard_input | desktop_keyboard_type, desktop_keyboard_hotkey | Off |

A user must enable each permission in the local Settings UI. Every mutating or privacy-sensitive tool call must additionally set confirm=true.

## Local data

- Settings: %LOCALAPPDATA%\HermesUniversalAgent\settings.json
- Memory: %LOCALAPPDATA%\HermesUniversalAgent\memory.sqlite3

No cloud synchronization is implemented.
