"""Permission-gated Windows desktop operations. No shell or arbitrary process tools."""

from __future__ import annotations

import io
import platform
from typing import Any

from .security import require_local_permission, require_permission


def _require_windows() -> None:
    if platform.system() != "Windows":
        raise RuntimeError("Desktop interaction is currently supported on Windows only.")


def list_windows() -> list[dict[str, Any]]:
    _require_windows()
    require_local_permission("window_control")
    import pygetwindow as gw

    windows = []
    for window in gw.getAllWindows():
        title = (window.title or "").strip()
        if title:
            windows.append({
                "title": title[:300],
                "left": int(window.left),
                "top": int(window.top),
                "width": int(window.width),
                "height": int(window.height),
                "visible": bool(window.visible),
            })
    return windows[:100]


def focus_window(title: str, confirm: bool) -> dict[str, object]:
    _require_windows()
    require_permission("window_control", confirm)
    if not title.strip() or len(title) > 300:
        raise ValueError("Provide an exact window title (up to 300 characters).")
    import pygetwindow as gw

    matches = [w for w in gw.getAllWindows() if (w.title or "").strip() == title.strip()]
    if len(matches) != 1:
        raise ValueError(f"Expected one exact window match; found {len(matches)}.")
    matches[0].activate()
    return {"focused": True, "title": title}


def capture_screen(confirm: bool):
    _require_windows()
    require_permission("screen_capture", confirm)
    import pyautogui

    image = pyautogui.screenshot()
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    from mcp.types import Image

    return Image(data=buffer.getvalue(), mimeType="image/png")


def click_mouse(x: int, y: int, button: str, confirm: bool) -> dict[str, object]:
    _require_windows()
    require_permission("mouse_input", confirm)
    import pyautogui

    width, height = pyautogui.size()
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"Coordinates must be inside the primary display ({width}x{height}).")
    if button not in {"left", "right", "middle"}:
        raise ValueError("button must be left, right, or middle.")
    pyautogui.click(x=x, y=y, button=button)
    return {"clicked": True, "x": x, "y": y, "button": button}


def type_text(text: str, confirm: bool) -> dict[str, object]:
    _require_windows()
    require_permission("keyboard_input", confirm)
    if not text or len(text) > 4000:
        raise ValueError("Text must contain 1–4,000 characters.")
    if any(ord(char) > 127 for char in text):
        raise ValueError("Keyboard typing currently accepts ASCII text only.")
    import pyautogui

    pyautogui.write(text, interval=0.01)
    return {"typed_characters": len(text)}


_ALLOWED_HOTKEYS = {
    "ctrl+c", "ctrl+v", "ctrl+x", "ctrl+a", "ctrl+z", "ctrl+y",
    "ctrl+s", "ctrl+f", "ctrl+p", "ctrl+w", "alt+tab",
    "enter", "escape", "tab",
}


def press_hotkey(keys: str, confirm: bool) -> dict[str, object]:
    _require_windows()
    require_permission("keyboard_input", confirm)
    normalized = "+".join(part.strip().lower() for part in keys.split("+"))
    if normalized not in _ALLOWED_HOTKEYS:
        raise ValueError("That shortcut is not in the built-in safe allowlist.")
    import pyautogui

    pyautogui.hotkey(*normalized.split("+"))
    return {"pressed": normalized}
