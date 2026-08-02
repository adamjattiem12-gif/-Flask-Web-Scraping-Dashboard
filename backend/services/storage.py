"""
Storage layer.

Persists application data to a local SQLite database (data/app.db)
instead of loose JSON files. This gives us safe concurrent writes (two
overlapping /api/scrape calls can no longer corrupt shared state the way
plain file overwrites could) and a foundation for real querying later.

Every function keeps the exact same name/signature/return shape it had
under the old JSON-file implementation, so routes, scrapers, and tests
that call load_items(), save_items(), add_history(), etc. did not need
to change.

It manages five types of data:
- Items (scraped products, current snapshot)
- Items History (versioned snapshots of items for Top Movers calculation)
- Websites (registered websites to scrape)
- History (records of previous scraping sessions)
- Statistics (the latest computed summary stats)
"""

import json
import logging
from datetime import datetime

from services.db import get_connection, init_db

logger = logging.getLogger(__name__)

MAX_HISTORY_SNAPSHOTS = 50

DEFAULT_WEBSITES = [
    {
        "name": "WebScraper E-Commerce Sandbox",
        "url": "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
        "market": "Retail Goods",
    },
    {
        "name": "CoinPaprika API",
        "url": "https://api.coinpaprika.com/v1/tickers",
        "market": "Digital Assets",
    },
]

# Ensure tables exist as soon as this module is imported.
init_db()


# ==========================
# ITEM STORAGE
# ==========================

def load_items():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT payload FROM items ORDER BY row_id").fetchall()
        return [json.loads(row["payload"]) for row in rows]
    finally:
        conn.close()


def save_items(items):
    """
    Replace the current items snapshot with `items`.

    Before overwriting, the existing items are versioned into the
    items_history table (pruned to the most recent 50 snapshots) so the
    frontend can calculate Top Movers by comparing price changes across
    scrape runs.
    """
    conn = get_connection()
    try:
        existing_rows = conn.execute("SELECT payload FROM items ORDER BY row_id").fetchall()
        existing_items = [json.loads(row["payload"]) for row in existing_rows]

        if existing_items:
            conn.execute(
                "INSERT INTO items_history (snapshot_at, items_json) VALUES (?, ?)",
                (datetime.now().isoformat(), json.dumps(existing_items)),
            )
            # Prune old snapshots, keep only the most recent MAX_HISTORY_SNAPSHOTS
            ids = [r["id"] for r in conn.execute(
                "SELECT id FROM items_history ORDER BY id DESC"
            ).fetchall()]
            stale_ids = ids[MAX_HISTORY_SNAPSHOTS:]
            if stale_ids:
                conn.executemany("DELETE FROM items_history WHERE id = ?", [(i,) for i in stale_ids])

        conn.execute("DELETE FROM items")
        conn.executemany(
            "INSERT INTO items (market, payload) VALUES (?, ?)",
            [(item.get("market", "Unknown"), json.dumps(item)) for item in items],
        )
        conn.commit()
    finally:
        conn.close()


def load_items_history():
    """
    Load all versioned item snapshots.

    Returns a list of snapshot objects, each with:
        - "snapshot_at" (str): ISO timestamp when the snapshot was taken.
        - "items" (list): The item list at that point in time.
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT snapshot_at, items_json FROM items_history ORDER BY id"
        ).fetchall()
        return [
            {"snapshot_at": row["snapshot_at"], "items": json.loads(row["items_json"])}
            for row in rows
        ]
    finally:
        conn.close()


# ==========================
# WEBSITE STORAGE
# ==========================

def _website_row_to_dict(row):
    d = {"id": row["id"], "name": row["name"], "url": row["url"], "market": row["market"]}
    if row["path_keywords"]:
        d["path_keywords"] = json.loads(row["path_keywords"])
    return d


def load_websites():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM websites ORDER BY id").fetchall()
        if not rows:
            for w in DEFAULT_WEBSITES:
                conn.execute(
                    "INSERT INTO websites (name, url, market, path_keywords) VALUES (?, ?, ?, ?)",
                    (w["name"], w["url"], w["market"], None),
                )
            conn.commit()
            rows = conn.execute("SELECT * FROM websites ORDER BY id").fetchall()
        return [_website_row_to_dict(row) for row in rows]
    finally:
        conn.close()


def save_websites(websites):
    """
    Replace the full website registry. Preserves ids on entries that have
    one (so URL edits round-trip correctly); entries without an id are
    inserted fresh.
    """
    conn = get_connection()
    try:
        conn.execute("DELETE FROM websites")
        for w in websites:
            path_keywords = json.dumps(w["path_keywords"]) if w.get("path_keywords") else None
            if w.get("id") is not None:
                conn.execute(
                    "INSERT INTO websites (id, name, url, market, path_keywords) VALUES (?, ?, ?, ?, ?)",
                    (w["id"], w["name"], w["url"], w["market"], path_keywords),
                )
            else:
                conn.execute(
                    "INSERT INTO websites (name, url, market, path_keywords) VALUES (?, ?, ?, ?)",
                    (w["name"], w["url"], w["market"], path_keywords),
                )
        conn.commit()
    finally:
        conn.close()


def add_website(name, url, market, path_keywords=None):
    """Insert a single new website and return it (with its new id)."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO websites (name, url, market, path_keywords) VALUES (?, ?, ?, ?)",
            (name, url, market, json.dumps(path_keywords) if path_keywords else None),
        )
        conn.commit()
        new_id = cur.lastrowid
        row = conn.execute("SELECT * FROM websites WHERE id = ?", (new_id,)).fetchone()
        return _website_row_to_dict(row)
    finally:
        conn.close()


def delete_website(website_id):
    """Delete a website by id. Returns True if a row was deleted."""
    conn = get_connection()
    try:
        cur = conn.execute("DELETE FROM websites WHERE id = ?", (website_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


# ==========================
# HISTORY STORAGE
# ==========================

def _history_row_to_dict(row):
    return {
        "id": row["id"],
        "timestamp": row["timestamp"],
        "scraper_type": row["scraper_type"],
        "market": row["market"],
        "items_found": row["items_found"],
        "success": bool(row["success"]),
        "error": row["error"],
    }


def load_history():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM history ORDER BY id").fetchall()
        return [_history_row_to_dict(row) for row in rows]
    finally:
        conn.close()


def save_history(history):
    """Replace the complete scraping history (used by tests/back-compat)."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM history")
        conn.executemany(
            "INSERT INTO history (timestamp, scraper_type, market, items_found, success, error) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    r.get("timestamp"),
                    r.get("scraper_type"),
                    r.get("market"),
                    r.get("items_found", 0),
                    1 if r.get("success") else 0,
                    r.get("error"),
                )
                for r in history
            ],
        )
        conn.commit()
    finally:
        conn.close()


def add_history(record):
    """Add a single scraping record to the history table."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO history (timestamp, scraper_type, market, items_found, success, error) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                record.get("timestamp"),
                record.get("scraper_type"),
                record.get("market"),
                record.get("items_found", 0),
                1 if record.get("success") else 0,
                record.get("error"),
            ),
        )
        conn.commit()
    finally:
        conn.close()


# ==========================
# STATISTICS STORAGE
# ==========================

def load_statistics():
    conn = get_connection()
    try:
        row = conn.execute("SELECT payload FROM statistics WHERE id = 1").fetchone()
        return json.loads(row["payload"]) if row else {}
    finally:
        conn.close()


def save_statistics(statistics):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO statistics (id, payload) VALUES (1, ?) "
            "ON CONFLICT(id) DO UPDATE SET payload = excluded.payload",
            (json.dumps(statistics),),
        )
        conn.commit()
    finally:
        conn.close()
