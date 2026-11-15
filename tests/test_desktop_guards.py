import pytest
from hermes_universal_agent.config import Settings
from hermes_universal_agent.desktop import screenshot,focus_window

def test_screenshot_denied_without_local_permission():
    with pytest.raises(PermissionError): screenshot(Settings(allow_screen_capture=False),confirm=True)

def test_focus_denied_without_local_permission():
    with pytest.raises(PermissionError): focus_window(Settings(allow_desktop_control=False),123,confirm=True)
