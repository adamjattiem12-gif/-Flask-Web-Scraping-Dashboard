from flask import Flask
from routes.history import history_bp
import services.storage as storage


def make_client():
    app = Flask(__name__)
    app.register_blueprint(history_bp)
    return app.test_client()


def test_history_returns_all_records_by_default(isolated_data):
    resp = make_client().get("/api/history")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 20


def test_history_limit_returns_newest_n_records(isolated_data):
    all_records = storage.load_history()
    resp = make_client().get("/api/history?limit=5")
    body = resp.get_json()
    assert len(body) == 5
    assert body == all_records[-5:]


def test_history_limit_zero_is_ignored_by_falsy_check(isolated_data):
    """`if limit:` treats limit=0 as falsy, so ?limit=0 is silently ignored
    and all records are returned instead of zero records."""
    resp = make_client().get("/api/history?limit=0")
    assert len(resp.get_json()) == 20


def test_history_filtered_by_market(isolated_data):
    storage.add_history({"timestamp": "2026-01-01T00:00:00",
                          "market": "Retail Goods", "success": True})
    resp = make_client().get("/api/history?market=Retail Goods")
    body = resp.get_json()
    assert len(body) == 1
    assert body[0]["market"] == "Retail Goods"


def test_history_market_filter_no_match_returns_empty(isolated_data):
    resp = make_client().get("/api/history?market=Nonexistent")
    assert resp.get_json() == []
