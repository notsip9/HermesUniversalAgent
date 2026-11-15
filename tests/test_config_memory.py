from pathlib import Path
from hermes_universal_agent.config import Settings,load_settings,save_settings
from hermes_universal_agent.memory import save_note,search_notes

def test_settings_default_deny(tmp_path: Path):
    s=load_settings(tmp_path/"missing.json")
    assert not s.allow_file_writes and not s.allow_desktop_control and not s.allow_screen_capture

def test_settings_round_trip(tmp_path: Path):
    path=tmp_path/"settings.json"; expected=Settings(str(tmp_path),True,True,False)
    save_settings(expected,path)
    assert load_settings(path)==expected

def test_local_memory_save_and_search(tmp_path: Path):
    db=tmp_path/"memory.sqlite3"; note_id=save_note("Hermes desktop safety test",db)
    found=search_notes("desktop safety",path=db)
    assert found and found[0]["id"]==note_id
