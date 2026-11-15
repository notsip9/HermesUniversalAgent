from __future__ import annotations

import pytest

from hermes_universal_agent import config, memory
from hermes_universal_agent.desktop import (
    capture_screen,
    click_mouse,
    focus_window,
    press_hotkey,
    type_text,
)
from hermes_universal_agent.security import (
    PermissionDenied,
    require_permission,
    resolve_workspace_path,
)


@pytest.fixture()
def isolated_app(tmp_path, monkeypatch):
    app_dir = tmp_path / "appdata"
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.setattr(config, "APP_DIR", app_dir)
    monkeypatch.setattr(config, "CONFIG_PATH", app_dir / "settings.json")
    monkeypatch.setattr(config, "MEMORY_PATH", app_dir / "memory.sqlite3")
    config.save_config({"workspace": str(workspace), "permissions": config.DEFAULT_PERMISSIONS})
    return workspace


def test_permissions_default_off(isolated_app):
    assert all(value is False for value in config.load_config()["permissions"].values())


def test_corrupt_config_fails_closed(isolated_app):
    config.CONFIG_PATH.write_text("{broken", encoding="utf-8")
    assert all(value is False for value in config.load_config()["permissions"].values())


def test_permission_requires_both_local_opt_in_and_confirm(isolated_app):
    with pytest.raises(PermissionDenied):
        require_permission("mouse_input", True)
    cfg = config.load_config()
    cfg["permissions"]["mouse_input"] = True
    config.save_config(cfg)
    with pytest.raises(PermissionDenied):
        require_permission("mouse_input", False)
    require_permission("mouse_input", True)


def test_workspace_rejects_parent_traversal(isolated_app):
    with pytest.raises(PermissionDenied):
        resolve_workspace_path("../outside.txt")


def test_workspace_allows_nested_file(isolated_app):
    target = resolve_workspace_path("notes/today.txt")
    assert target == isolated_app / "notes" / "today.txt"


def test_workspace_rejects_symlink_escape(isolated_app, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    link = isolated_app / "escape"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlink creation is unavailable in this Windows environment.")
    with pytest.raises(PermissionDenied):
        resolve_workspace_path("escape/secret.txt")


def test_desktop_operations_are_blocked_by_default(isolated_app):
    for action in (
        lambda: capture_screen(False),
        lambda: click_mouse(1, 1, "left", False),
        lambda: focus_window("Notepad", False),
        lambda: type_text("hello", False),
        lambda: press_hotkey("ctrl+s", False),
    ):
        with pytest.raises(PermissionDenied):
            action()


def test_memory_uses_parameterized_search(isolated_app):
    saved = memory.save_note("Remember the blue notebook")
    assert saved["saved"] is True
    found = memory.search_notes("blue")
    assert len(found) == 1
    assert found[0]["content"] == "Remember the blue notebook"
