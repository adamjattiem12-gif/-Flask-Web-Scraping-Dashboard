import json
import shutil
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import services.storage as storage


@pytest.fixture
def isolated_data(tmp_path, monkeypatch):
    """Point the storage module at a throwaway data folder seeded with
    copies of the real sample data, so tests never touch the real
    backend/data files."""
    real_data_dir = BACKEND_DIR / "data"
    temp_data_dir = tmp_path / "data"
    shutil.copytree(real_data_dir, temp_data_dir)

    monkeypatch.setattr(storage, "DATA_FOLDER", temp_data_dir)
    monkeypatch.setattr(storage, "ITEMS_FILE", temp_data_dir / "items.json")
    monkeypatch.setattr(storage, "ITEMS_HISTORY_FILE", temp_data_dir / "items_history.json")
    monkeypatch.setattr(storage, "WEBSITES_FILE", temp_data_dir / "websites.json")
    monkeypatch.setattr(storage, "HISTORY_FILE", temp_data_dir / "history.json")
    monkeypatch.setattr(storage, "STATISTICS_FILE", temp_data_dir / "statistics.json")

    return temp_data_dir
