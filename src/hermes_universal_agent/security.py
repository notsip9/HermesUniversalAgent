"""Path and permission guards shared by MCP tools."""

from __future__ import annotations

from pathlib import Path

from .config import load_config


class PermissionDenied(PermissionError):
    """Raised when a local opt-in or per-action confirmation is missing."""


def require_local_permission(name: str) -> None:
    if not load_config()["permissions"].get(name, False):
        raise PermissionDenied(
            f"The '{name}' permission is disabled. Enable it locally in Hermes Settings first."
        )


def require_permission(name: str, confirm: bool) -> None:
    require_local_permission(name)
    if not confirm:
        raise PermissionDenied("This action requires confirm=true in the tool request.")


def workspace_root() -> Path:
    config = load_config()
    root = Path(config["workspace"]).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def resolve_workspace_path(relative_path: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ValueError("A non-empty relative path is required.")
    root = workspace_root()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise PermissionDenied("Path is outside the configured workspace.") from exc
    return candidate
