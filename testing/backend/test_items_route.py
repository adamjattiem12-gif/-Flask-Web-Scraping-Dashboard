from flask import Flask
from routes.items import items_bp


def make_client():
    app = Flask(__name__)
    app.register_blueprint(items_bp)
    return app.test_client()


def test_get_items_default_pagination(isolated_data):
    resp = make_client().get("/api/items")
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["total"] == 21
    assert body["page"] == 1
    assert body["per_page"] == 20
    assert len(body["items"]) == 20


def test_get_items_second_page(isolated_data):
    resp = make_client().get("/api/items?page=2&per_page=20")
    body = resp.get_json()
    assert len(body["items"]) == 1  # 21 items total, 1 left on page 2


def test_get_items_filtered_by_market(isolated_data):
    resp = make_client().get("/api/items?market=Retail Goods")
    body = resp.get_json()
    assert all(i["market"] == "Retail Goods" for i in body["items"])


def test_get_items_filtered_by_nonexistent_market_returns_empty(isolated_data):
    resp = make_client().get("/api/items?market=Nonexistent Market")
    body = resp.get_json()
    assert body["items"] == []
    assert body["total"] == 0


def test_get_items_non_integer_page_returns_400(isolated_data):
    resp = make_client().get("/api/items?page=abc")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_get_items_zero_page_returns_400(isolated_data):
    resp = make_client().get("/api/items?page=0")
    assert resp.status_code == 400


def test_get_items_negative_per_page_returns_400(isolated_data):
    resp = make_client().get("/api/items?per_page=-5")
    assert resp.status_code == 400


def test_get_items_per_page_over_100_returns_400(isolated_data):
    resp = make_client().get("/api/items?per_page=101")
    assert resp.status_code == 400


def test_get_items_per_page_exactly_100_is_allowed(isolated_data):
    resp = make_client().get("/api/items?per_page=100")
    assert resp.status_code == 200


def test_get_items_market_filter_is_case_sensitive(isolated_data):
    """Documents current behaviour: lowercase 'retail goods' does NOT match
    the stored 'Retail Goods' market value, since the filter uses `==`
    with no case normalisation."""
    resp = make_client().get("/api/items?market=retail goods")
    body = resp.get_json()
    assert body["items"] == []
