"""stdio MCP server entry point."""

from __future__ import annotations

import os
import platform

from mcp.server.fastmcp import FastMCP

from . import __version__
from .config import load_config
from .desktop import (
    capture_screen,
    click_mouse,
    focus_window,
    list_windows,
    press_hotkey,
    type_text,
)
from .memory import save_note, search_notes
from .security import require_permission, resolve_workspace_path, workspace_root

mcp = FastMCP("Hermes Universal Agent")

@mcp.tool()
def agent_status() -> dict[str, object]:
    """Show companion version, workspace, and local permission state."""
    config = load_config()
    return {
        "name": "Hermes Universal Agent",
        "version": __version__,
        "platform": platform.platform(),
        "workspace": config["workspace"],
        "permissions": config["permissions"],
        "transport": "stdio",
    }

@mcp.tool()
def workspace_list(relative_path: str = ".") -> list[dict[str, object]]:
    """List entries in the configured workspace; paths cannot escape its root."""
    folder = workspace_root() if relative_path in {"", "."} else resolve_workspace_path(relative_path)
    if not folder.exists() or not folder.is_dir():
        raise ValueError("Directory does not exist inside the configured workspace.")
    entries = []
    for item in sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.casefold()))[:500]:
        entries.append({"name": item.name, "type": "directory" if item.is_dir() else "file"})
    return entries

@mcp.tool()
def workspace_read(relative_path: str) -> str:
    """Read a UTF-8 text file from the configured workspace (maximum 512 KB)."""
    path = resolve_workspace_path(relative_path)
    if not path.is_file():
        raise ValueError("File does not exist.")
    maximum = load_config()["max_text_bytes"]
    if path.stat().st_size > maximum:
        raise ValueError(f"File exceeds the {maximum}-byte read limit.")
    return path.read_text(encoding="utf-8")

@mcp.tool()
def workspace_write(relative_path: str, content: str, confirm: bool = False) -> dict[str, object]:
    """Write a UTF-8 text file. Requires local file_writes permission and confirm=true."""
    require_permission("file_writes", confirm)
    if len(content.encode("utf-8")) > load_config()["max_text_bytes"]:
        raise ValueError("Content exceeds the configured 512 KB limit.")
    path = resolve_workspace_path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"written": True, "path": str(path), "bytes": path.stat().st_size}

@mcp.tool()
def memory_save(content: str) -> dict[str, object]:
    """Save a private note in the local SQLite database."""
    return save_note(content)

@mcp.tool()
def memory_search(query: str, limit: int = 20) -> list[dict[str, object]]:
    """Search private notes stored locally on this computer."""
    return search_notes(query, limit)

@mcp.tool()
def system_info() -> dict[str, str]:
    """Return basic operating-system information; no environment secrets are collected."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    }

@mcp.tool()
def desktop_windows_list() -> list[dict[str, object]]:
    """List visible Windows windows and their bounds (read-only)."""
    return list_windows()

@mcp.tool()
def desktop_window_focus(title: str, confirm: bool = False) -> dict[str, object]:
    """Focus one exact window title. Requires local window_control permission and confirmation."""
    return focus_window(title, confirm)

@mcp.tool()
def desktop_screen_capture(confirm: bool = False):
    """Capture the current screen as an image. Requires local screen_capture permission and confirmation."""
    return capture_screen(confirm)

@mcp.tool()
def desktop_mouse_click(x: int, y: int, button: str = "left", confirm: bool = False) -> dict[str, object]:
    """Click the primary display at explicit coordinates. Requires local permission and confirmation."""
    return click_mouse(x, y, button, confirm)

@mcp.tool()
def desktop_keyboard_type(text: str, confirm: bool = False) -> dict[str, object]:
    """Type up to 4,000 ASCII characters into the focused app. Requires local permission and confirmation."""
    return type_text(text, confirm)

@mcp.tool()
def desktop_keyboard_hotkey(keys: str, confirm: bool = False) -> dict[str, object]:
    """Press a built-in allowlisted shortcut. Requires local keyboard permission and confirmation."""
    return press_hotkey(keys, confirm)

def main() -> None:
    os.environ.setdefault("PYTHONUTF8", "1")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
