"""
Shared pytest fixtures.

Every test gets a fresh, isolated SQLite database (a temp file, one per
test) so tests never share state or touch the real data/app.db.
"""
import importlib
import os
import sys

import pytest

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A Flask test client backed by a throwaway SQLite DB file."""
    db_path = tmp_path / "test_app.db"
    monkeypatch.setenv("SCRAPER_DB_PATH", str(db_path))
    monkeypatch.setenv("SCRAPE_SCHEDULER_ENABLED", "0")

    # storage.py runs init_db() at import time and app.py starts the
    # scheduler at import time, so both modules (and anything that already
    # imported them) must be reloaded fresh under the new env vars.
    for mod_name in list(sys.modules):
        if mod_name in ("app",) or mod_name.startswith("routes.") or mod_name.startswith("services."):
            del sys.modules[mod_name]

    app_module = importlib.import_module("app")
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client
