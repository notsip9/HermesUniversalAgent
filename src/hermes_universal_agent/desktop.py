from __future__ import annotations
import ctypes, io, os
from ctypes import wintypes
from typing import Any
from .config import Settings
from .security import require_confirmation

user32 = ctypes.WinDLL("user32", use_last_error=True) if os.name == "nt" else None

def _api() -> Any:
    if user32 is None: raise OSError("Desktop controls are available only on Windows.")
    return user32

def list_windows(settings: Settings) -> list[dict[str, Any]]:
    if not settings.allow_desktop_control: raise PermissionError("Desktop control is disabled in local settings.")
    api = _api()
    result: list[dict[str, Any]] = []
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def visit(hwnd: int, _param: int) -> bool:
        if not api.IsWindowVisible(hwnd): return True
        length = api.GetWindowTextLengthW(hwnd)
        if length <= 0: return True
        title = ctypes.create_unicode_buffer(min(length + 1, 2048))
        api.GetWindowTextW(hwnd, title, len(title))
        if title.value.strip():
            pid = wintypes.DWORD()
            api.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            result.append({"handle": int(hwnd), "title": title.value, "process_id": int(pid.value)})
        return True
    api.EnumWindows(callback_type(visit), 0)
    return result[:200]

def focus_window(settings: Settings, handle: int, confirm: bool) -> dict[str, Any]:
    require_confirmation(confirm, settings.allow_desktop_control, "Desktop control")
    api, hwnd = _api(), wintypes.HWND(int(handle))
    if not api.IsWindow(hwnd): raise ValueError("The requested window handle is no longer valid.")
    api.ShowWindow(hwnd, 9)
    if not api.SetForegroundWindow(hwnd): raise PermissionError("Windows refused to focus that window.")
    return {"focused": True, "handle": int(handle)}

def screenshot(settings: Settings, confirm: bool) -> Any:
    require_confirmation(confirm, settings.allow_screen_capture, "Screen capture")
    _api()
    from PIL import ImageGrab
    from mcp.server.fastmcp.utilities.types import Image
    frame = ImageGrab.grab(all_screens=True)
    output = io.BytesIO()
    frame.save(output, format="PNG")
    return Image(data=output.getvalue(), format="png")

def click(settings: Settings, x: int, y: int, button: str, confirm: bool) -> dict[str, Any]:
    require_confirmation(confirm, settings.allow_desktop_control, "Desktop control")
    api = _api()
    if button not in {"left", "right", "middle"}: raise ValueError("button must be left, right, or middle.")
    width, height = api.GetSystemMetrics(0), api.GetSystemMetrics(1)
    if not (0 <= x < width and 0 <= y < height): raise ValueError("Click coordinates are outside the primary display.")
    api.SetCursorPos(int(x), int(y))
    down, up = {"left": (0x0002,0x0004), "right": (0x0008,0x0010), "middle": (0x0020,0x0040)}[button]
    api.mouse_event(down,0,0,0,0); api.mouse_event(up,0,0,0,0)
    return {"clicked": True, "x": x, "y": y, "button": button}

def type_text(settings: Settings, text: str, confirm: bool) -> dict[str, Any]:
    require_confirmation(confirm, settings.allow_desktop_control, "Desktop control")
    api = _api()
    if not isinstance(text, str) or not text: raise ValueError("Text must not be empty.")
    if len(text) > 500: raise ValueError("A single typing operation is limited to 500 characters.")
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk",wintypes.WORD),("wScan",wintypes.WORD),("dwFlags",wintypes.DWORD),
                    ("time",wintypes.DWORD),("dwExtraInfo",ctypes.c_size_t)]
    class U(ctypes.Union): _fields_ = [("ki",KEYBDINPUT)]
    class INPUT(ctypes.Structure):
        _anonymous_ = ("u",)
        _fields_ = [("type",wintypes.DWORD),("u",U)]
    sent = 0
    for char in text:
        for flags in (0x0004,0x0004|0x0002):
            item = INPUT(type=1, ki=KEYBDINPUT(0,ord(char),flags,0,0))
            sent += api.SendInput(1,ctypes.byref(item),ctypes.sizeof(INPUT))
    if sent != len(text)*2: raise OSError("Windows accepted only part of the requested text input.")
    return {"typed_characters":len(text)}
