import datetime
import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "memory.db"
def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    return conn


def store_fact(fact: str) -> int:
    """Permanently remember a fact. Returns the new row's id."""
    with _conn() as conn:
        cur = conn.execute(
            "INSERT INTO facts (fact, created_at) VALUES (?, ?)",
            (fact, datetime.datetime.now().isoformat()),
        )
        return cur.lastrowid
def search_facts(query: str, limit: int = 5) -> list[str]:
    words = [w.lower() for w in query.split() if len(w) > 2]
    with _conn() as conn:
        rows = conn.execute(
            "SELECT fact FROM facts ORDER BY id DESC"
        ).fetchall()
    all_facts = [row[0] for row in rows]
    if not words:
        return all_facts[:limit]
    matches = [f for f in all_facts if any(w in f.lower() for w in words)]
    return matches[:limit] if matches else all_facts[:limit]
def all_facts() -> list[str]:
    with _conn() as conn:
        rows = conn.execute("SELECT fact FROM facts ORDER BY id DESC").fetchall()
    return [row[0] for row in rows]
if __name__ == "__main__":
    store_fact("Prefers studying in the morning")
    print("Stored. All facts:", all_facts())
    print("Search 'study preference':", search_facts("study preference"))