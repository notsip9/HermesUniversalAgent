from __future__ import annotations
import platform
from typing import Any
from mcp.server.fastmcp import FastMCP
from . import __version__
from .config import load_settings, workspace_path
from .desktop import click as desktop_click, focus_window, list_windows, screenshot, type_text
from .memory import save_note, search_notes
from .security import MAX_TEXT_BYTES, require_confirmation, resolve_workspace_path

mcp = FastMCP("Hermes Universal Agent")
def _settings(): return load_settings()

@mcp.tool()
def agent_status() -> dict[str, Any]:
    """Report product version, workspace, and local permission switches."""
    s=_settings()
    return {"name":"Hermes Universal Agent","version":__version__,"workspace":s.workspace_root,
            "file_writes_enabled":s.allow_file_writes,"desktop_control_enabled":s.allow_desktop_control,
            "screen_capture_enabled":s.allow_screen_capture,"transport":"stdio"}

@mcp.tool()
def workspace_list(relative_path: str=".", limit: int=200) -> list[dict[str, Any]]:
    """List files and folders inside the configured workspace."""
    root=workspace_path(_settings())
    target=root if relative_path in {"","."} else resolve_workspace_path(root,relative_path)
    if not target.exists() or not target.is_dir(): raise ValueError("Requested workspace folder does not exist.")
    limit=max(1,min(int(limit),500))
    return [{"name":p.name,"path":str(p.relative_to(root)),"is_directory":p.is_dir()}
            for p in sorted(target.iterdir(),key=lambda p:(not p.is_dir(),p.name.casefold()))[:limit]]

@mcp.tool()
def workspace_read(relative_path: str) -> str:
    """Read a UTF-8 text file inside the workspace (maximum 512 KB)."""
    target=resolve_workspace_path(workspace_path(_settings()),relative_path)
    if not target.is_file(): raise ValueError("Requested file does not exist.")
    if target.stat().st_size>MAX_TEXT_BYTES: raise ValueError("File exceeds the 512 KB read limit.")
    data=target.read_bytes()
    if len(data)>MAX_TEXT_BYTES: raise ValueError("File exceeds the 512 KB read limit.")
    return data.decode("utf-8")

@mcp.tool()
def workspace_write(relative_path: str, content: str, confirm: bool=False) -> dict[str,Any]:
    """Create or replace a workspace text file; local permission and confirm=true are both required."""
    s=_settings(); require_confirmation(confirm,s.allow_file_writes,"File writes")
    if not isinstance(content,str) or len(content.encode("utf-8"))>MAX_TEXT_BYTES:
        raise ValueError("Content must be UTF-8 text no larger than 512 KB.")
    root=workspace_path(s); target=resolve_workspace_path(root,relative_path)
    target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content,encoding="utf-8")
    return {"written":True,"path":str(target.relative_to(root)),"bytes":len(content.encode("utf-8"))}

@mcp.tool()
def memory_save(content: str) -> dict[str,int]:
    """Save a private note in the local SQLite memory database."""
    return {"id":save_note(content)}

@mcp.tool()
def memory_search(query: str, limit: int=20) -> list[dict[str,Any]]:
    """Search notes stored in local SQLite memory."""
    return search_notes(query,limit)

@mcp.tool()
def system_info() -> dict[str,str]:
    """Return basic operating-system and Python runtime information."""
    return {"os":platform.platform(),"python":platform.python_version(),"architecture":platform.machine()}

@mcp.tool()
def desktop_windows(confirm: bool=False) -> list[dict[str,Any]]:
    """List visible windows; local desktop permission and confirm=true are required."""
    s=_settings(); require_confirmation(confirm,s.allow_desktop_control,"Desktop control")
    return list_windows(s)

@mcp.tool()
def desktop_screenshot(confirm: bool=False):
    """Capture desktop image; separate local screen-capture permission and confirm=true are required."""
    return screenshot(_settings(),confirm)

@mcp.tool()
def desktop_focus_window(handle: int, confirm: bool=False) -> dict[str,Any]:
    """Focus a window by handle after explicit confirmation."""
    return focus_window(_settings(),handle,confirm)

@mcp.tool()
def desktop_click(x: int,y: int,button: str="left",confirm: bool=False) -> dict[str,Any]:
    """Click a screen coordinate after explicit confirmation."""
    return desktop_click(_settings(),x,y,button,confirm)

@mcp.tool()
def desktop_type_text(text: str,confirm: bool=False) -> dict[str,Any]:
    """Type up to 500 characters into the focused control after explicit confirmation."""
    return type_text(_settings(),text,confirm)

def main() -> None:
    mcp.run(transport="stdio")
if __name__=="__main__": main()
