from __future__ import annotations
import json, os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

def app_data_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    return (Path(base) / "HermesUniversalAgent") if base else (Path.home() / ".hermes-universal-agent")

def config_path() -> Path:
    return app_data_dir() / "settings.json"

@dataclass
class Settings:
    workspace_root: str = str(Path.home() / "Documents")
    allow_file_writes: bool = False
    allow_desktop_control: bool = False
    allow_screen_capture: bool = False

def load_settings(path: Path | None = None) -> Settings:
    target, defaults = path or config_path(), Settings()
    try:
        raw: Any = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(raw, dict): return defaults
        root = raw.get("workspace_root", defaults.workspace_root)
        if not isinstance(root, str) or not root.strip(): root = defaults.workspace_root
        return Settings(root, raw.get("allow_file_writes") is True,
                        raw.get("allow_desktop_control") is True,
                        raw.get("allow_screen_capture") is True)
    except (OSError, ValueError, TypeError):
        return defaults

def save_settings(settings: Settings, path: Path | None = None) -> Path:
    target = path or config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")
    temporary.replace(target)
    return target

def workspace_path(settings: Settings) -> Path:
    root = Path(settings.workspace_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError("The configured workspace folder does not exist.")
    return root
