import json
import services.storage as storage


def test_load_items_returns_seeded_items(isolated_data):
    items = storage.load_items()
    assert isinstance(items, list)
    assert len(items) == 21


def test_load_items_missing_file_returns_empty_list(isolated_data):
    (isolated_data / "items.json").unlink()
    assert storage.load_items() == []


def test_load_items_empty_file_returns_empty_list(isolated_data):
    (isolated_data / "items.json").write_text("")
    assert storage.load_items() == []


def test_save_items_then_load_round_trip(isolated_data):
    new_items = [{"id": 1, "name": "Test Widget", "price": 9.99}]
    storage.save_items(new_items)
    assert storage.load_items() == new_items


def test_save_items_versions_previous_snapshot_into_history(isolated_data):
    original = storage.load_items()
    storage.save_items([{"id": 999, "name": "New Snapshot Item", "price": 1.0}])
    history = storage.load_items_history()
    assert len(history) == 1
    assert history[0]["items"] == original
    assert "snapshot_at" in history[0]


def test_save_items_does_not_version_when_no_prior_items(isolated_data):
    (isolated_data / "items.json").write_text("[]")
    storage.save_items([{"id": 1, "name": "First Ever Item", "price": 5.0}])
    assert storage.load_items_history() == []


def test_load_websites_returns_seeded_list(isolated_data):
    sites = storage.load_websites()
    assert len(sites) == 2
    assert {s["market"] for s in sites} == {"E-Commerce", "Cryptocurrency"}


def test_load_websites_seeds_defaults_when_file_missing(isolated_data):
    (isolated_data / "websites.json").unlink()
    sites = storage.load_websites()
    assert len(sites) == 2
    # File should now exist on disk after auto-seeding
    assert (isolated_data / "websites.json").exists()


def test_load_history_returns_seeded_records(isolated_data):
    history = storage.load_history()
    assert isinstance(history, list)
    assert len(history) == 20


def test_add_history_appends_record(isolated_data):
    before = len(storage.load_history())
    storage.add_history({"timestamp": "2026-01-01T00:00:00", "success": True})
    after = storage.load_history()
    assert len(after) == before + 1
    assert after[-1]["success"] is True


def test_load_statistics_empty_object_returns_empty_dict(isolated_data):
    # Sample statistics.json ships as "{}"
    assert storage.load_statistics() == {}


def test_save_statistics_then_load_round_trip(isolated_data):
    stats = {"total_items": 5, "active_sites": 2}
    storage.save_statistics(stats)
    assert storage.load_statistics() == stats


def test_ensure_data_folder_creates_missing_directory(isolated_data, tmp_path):
    fresh_dir = tmp_path / "brand_new_data_dir"
    storage.DATA_FOLDER = fresh_dir
    assert not fresh_dir.exists()
    storage.ensure_data_folder()
    assert fresh_dir.exists()
