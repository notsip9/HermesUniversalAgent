from pathlib import Path
import pytest
from hermes_universal_agent.security import resolve_workspace_path,require_confirmation

def test_resolve_normal_path(tmp_path: Path):
    assert resolve_workspace_path(tmp_path,"notes/today.txt")== (tmp_path/"notes/today.txt").resolve()

@pytest.mark.parametrize("candidate",["../secret.txt","..\\secret.txt","C:\\Windows\\win.ini","/etc/passwd"])
def test_reject_path_escape(tmp_path: Path,candidate: str):
    with pytest.raises(ValueError): resolve_workspace_path(tmp_path,candidate)

def test_reject_symlink_escape(tmp_path: Path):
    outside=tmp_path.parent/"outside-hermes-test"; outside.mkdir(exist_ok=True)
    link=tmp_path/"escape"
    try: link.symlink_to(outside,target_is_directory=True)
    except (OSError,NotImplementedError): pytest.skip("Symlink creation unavailable")
    with pytest.raises(ValueError): resolve_workspace_path(tmp_path,"escape/file.txt")

def test_permissions_require_both_switch_and_confirmation():
    with pytest.raises(PermissionError): require_confirmation(True,False,"Feature")
    with pytest.raises(PermissionError): require_confirmation(False,True,"Feature")
    require_confirmation(True,True,"Feature")
