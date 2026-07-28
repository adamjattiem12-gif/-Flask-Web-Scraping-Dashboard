from flask import Flask
from routes.statistics import statistics_bp
import services.storage as storage


def make_client():
    app = Flask(__name__)
    app.register_blueprint(statistics_bp)
    return app.test_client()


def test_statistics_returns_persisted_stats_when_present(isolated_data):
    persisted = {"total_items": 42, "active_sites": 2, "success_rate": 99.9,
                 "last_scrape": "2026-01-01T00:00:00", "markets": {}}
    storage.save_statistics(persisted)

    resp = make_client().get("/api/statistics")
    assert resp.status_code == 200
    assert resp.get_json() == persisted


def test_statistics_falls_back_to_calculation_when_file_empty(isolated_data):
    # Sample statistics.json ships as "{}", so the fallback path runs
    resp = make_client().get("/api/statistics")
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["total_items"] == 21
    assert body["active_sites"] == 2
    assert "markets" in body
    assert "Retail Goods" in body["markets"]


def test_statistics_fallback_success_rate_from_history(isolated_data):
    resp = make_client().get("/api/statistics")
    body = resp.get_json()
    # All 20 seeded history records have success: true
    assert body["success_rate"] == 100.0


def test_statistics_fallback_with_no_items_or_history(isolated_data):
    (isolated_data / "items.json").write_text("[]")
    (isolated_data / "history.json").write_text("[]")

    resp = make_client().get("/api/statistics")
    body = resp.get_json()
    assert body["total_items"] == 0
    assert body["success_rate"] == 100.0
    assert body["markets"] == {}
