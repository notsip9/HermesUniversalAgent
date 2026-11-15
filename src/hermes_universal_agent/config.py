"""Local configuration with safe, opt-in desktop permissions."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

APP_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "HermesUniversalAgent"
CONFIG_PATH = APP_DIR / "settings.json"
MEMORY_PATH = APP_DIR / "memory.sqlite3"

DEFAULT_PERMISSIONS = {
    "file_writes": False,
    "screen_capture": False,
    "window_control": False,
    "mouse_input": False,
    "keyboard_input": False,
}

DEFAULT_CONFIG: dict[str, Any] = {
    "workspace": str(Path.home() / "Documents" / "HermesWorkspace"),
    "permissions": DEFAULT_PERMISSIONS.copy(),
    "max_text_bytes": 512_000,
}


def load_config() -> dict[str, Any]:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        return json.loads(json.dumps(DEFAULT_CONFIG))
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise TypeError("Settings must be a JSON object")
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        # Fail closed: corrupt settings must never grant permissions.
        return json.loads(json.dumps(DEFAULT_CONFIG))
    merged = json.loads(json.dumps(DEFAULT_CONFIG))
    if isinstance(data.get("workspace"), str) and data["workspace"].strip():
        merged["workspace"] = data["workspace"]
    if isinstance(data.get("permissions"), dict):
        for key in DEFAULT_PERMISSIONS:
            merged["permissions"][key] = data["permissions"].get(key) is True
    if isinstance(data.get("max_text_bytes"), int):
        merged["max_text_bytes"] = max(1024, min(data["max_text_bytes"], 512_000))
    return merged


def save_config(config: dict[str, Any]) -> None:
    """Atomically persist known settings; unknown keys are discarded."""
    APP_DIR.mkdir(parents=True, exist_ok=True)
    safe = {
        "workspace": str(Path(str(config.get("workspace", DEFAULT_CONFIG["workspace"]))).expanduser()),
        "permissions": {
            key: config.get("permissions", {}).get(key) is True
            for key in DEFAULT_PERMISSIONS
        },
        "max_text_bytes": max(1024, min(int(config.get("max_text_bytes", 512_000)), 512_000)),
    }
    fd, temp_name = tempfile.mkstemp(prefix="settings-", suffix=".tmp", dir=APP_DIR)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(safe, handle, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, CONFIG_PATH)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def permission_enabled(name: str) -> bool:
    return load_config()["permissions"].get(name) is True
