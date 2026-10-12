import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DB_PATH = "history.db"


@contextmanager
def connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                input_text TEXT NOT NULL,
                status TEXT NOT NULL,
                estimated_price INTEGER,
                range_low INTEGER,
                range_high INTEGER,
                listed_price INTEGER,
                verdict TEXT,
                unsure INTEGER
            )
        """)


def save_query(text, result):
    facts = result.get("facts") or {}
    fair = facts.get("fair_range") or [None, None]
    with connection() as conn:
        conn.execute(
            """INSERT INTO queries
               (created_at, input_text, status, estimated_price, range_low,
                range_high, listed_price, verdict, unsure)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now(timezone.utc).isoformat(),
                text,
                result["status"],
                facts.get("estimated_price"),
                fair[0],
                fair[1],
                facts.get("listed_price"),
                facts.get("verdict"),
                int(facts["unsure"]) if "unsure" in facts else None,
            ),
        )


def get_history(limit=20):
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM queries ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]