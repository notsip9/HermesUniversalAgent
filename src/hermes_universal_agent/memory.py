"""Private local SQLite notes."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

from . import config


def connect() -> sqlite3.Connection:
    config.APP_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(config.MEMORY_PATH, timeout=10)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    return db


def save_note(content: str) -> dict[str, object]:
    clean = content.strip()
    if not clean or len(clean.encode("utf-8")) > 32_000:
        raise ValueError("Note must contain 1–32,000 UTF-8 bytes.")
    with connect() as db:
        cursor = db.execute(
            "INSERT INTO notes(content, created_at) VALUES (?, ?)",
            (clean, datetime.now(UTC).isoformat()),
        )
        return {"id": cursor.lastrowid, "saved": True}


def search_notes(query: str, limit: int = 20) -> list[dict[str, object]]:
    clean = query.strip()
    if not clean:
        raise ValueError("Search query cannot be empty.")
    limit = max(1, min(int(limit), 50))
    with connect() as db:
        rows = db.execute(
            "SELECT id, content, created_at FROM notes WHERE content LIKE ? "
            "ORDER BY id DESC LIMIT ?",
            (f"%{clean}%", limit),
        ).fetchall()
    return [{"id": row[0], "content": row[1], "created_at": row[2]} for row in rows]
