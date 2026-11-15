from pathlib import Path
MAX_TEXT_BYTES = 512_000

def resolve_workspace_path(root: Path, relative_path: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ValueError("A non-empty relative path is required.")
    supplied = Path(relative_path)
    if supplied.is_absolute():
        raise ValueError("Absolute paths are not allowed.")
    root = root.resolve()
    candidate = (root / supplied).resolve()
    try: candidate.relative_to(root)
    except ValueError as exc: raise ValueError("Path escapes the configured workspace.") from exc
    return candidate

def require_confirmation(confirm: bool, setting_enabled: bool, setting_name: str) -> None:
    if not setting_enabled:
        raise PermissionError(f"{setting_name} is disabled in the local Hermes settings.")
    if confirm is not True:
        raise PermissionError("This action requires confirm=true in the tool request.")
