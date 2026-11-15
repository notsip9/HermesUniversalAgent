import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from .config import app_data_dir

def database_path() -> Path:
    return app_data_dir() / "memory.sqlite3"

def _connect(path: Path | None = None) -> sqlite3.Connection:
    target = path or database_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(target)
    db.execute("""CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL, created_at TEXT NOT NULL)""")
    return db

def save_note(content: str, path: Path | None = None) -> int:
    if not isinstance(content, str) or not content.strip(): raise ValueError("Note content cannot be empty.")
    if len(content.encode("utf-8")) > 100_000: raise ValueError("Note exceeds the 100 KB limit.")
    with _connect(path) as db:
        cur = db.execute("INSERT INTO notes(content, created_at) VALUES (?, ?)",
                         (content, datetime.now(timezone.utc).isoformat()))
        return int(cur.lastrowid)

def search_notes(query: str, limit: int = 20, path: Path | None = None) -> list[dict[str, str | int]]:
    if not isinstance(query, str): raise ValueError("Query must be text.")
    limit = max(1, min(int(limit), 100))
    with _connect(path) as db:
        rows = db.execute("SELECT id, content, created_at FROM notes WHERE content LIKE ? ORDER BY id DESC LIMIT ?",
                          (f"%{query.strip()}%", limit)).fetchall()
    return [{"id": r[0], "content": r[1], "created_at": r[2]} for r in rows]
