"""
SQLite connection & schema management.

Centralizes the database file location and table creation so storage.py
can focus purely on read/write operations instead of connection plumbing.

The DB path can be overridden via the SCRAPER_DB_PATH environment variable,
which is how the pytest suite points this at a temporary file instead of
the real data/app.db.
"""
import os
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

DB_PATH = Path(os.environ.get("SCRAPER_DB_PATH", str(DATA_FOLDER / "app.db")))


def get_connection():
    """Return a new SQLite connection with dict-like row access."""
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


SCHEMA = """
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    market TEXT NOT NULL,
    path_keywords TEXT
);

CREATE TABLE IF NOT EXISTS items (
    row_id INTEGER PRIMARY KEY AUTOINCREMENT,
    market TEXT,
    payload TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS items_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_at TEXT NOT NULL,
    items_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    scraper_type TEXT,
    market TEXT,
    items_found INTEGER DEFAULT 0,
    success INTEGER DEFAULT 0,
    error TEXT
);

CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    payload TEXT NOT NULL
);
"""


def init_db():
    """Create tables if they don't exist yet. Safe to call on every boot."""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
