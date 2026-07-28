from flask import Flask
from routes.search import search_bp


def make_client():
    app = Flask(__name__)
    app.register_blueprint(search_bp)
    return app.test_client()


def test_search_no_query_returns_all_items(isolated_data):
    resp = make_client().get("/api/search")
    body = resp.get_json()
    assert resp.status_code == 200
    assert len(body) == 21


def test_search_matches_partial_name_case_insensitive(isolated_data):
    resp = make_client().get("/api/search?q=IDEATAB")
    body = resp.get_json()
    assert len(body) >= 1
    assert all("ideatab" in item["name"].lower() for item in body)


def test_search_with_market_filter(isolated_data):
    resp = make_client().get("/api/search?q=&market=retail goods")
    body = resp.get_json()
    assert all(item["market"].lower() == "retail goods" for item in body)


def test_search_no_match_returns_empty_list(isolated_data):
    resp = make_client().get("/api/search?q=zzz_no_such_product_zzz")
    assert resp.get_json() == []


def test_search_missing_name_field_raises_500(isolated_data):
    """If a stored item is missing the 'name' field, the route currently
    raises an unhandled KeyError (surfaced by Flask as HTTP 500) instead of
    skipping the malformed record."""
    import services.storage as storage
    items = storage.load_items()
    items.append({"market": "Retail Goods", "price": 1})  # no 'name' key
    storage.save_items(items)

    resp = make_client().get("/api/search?q=anything")
    assert resp.status_code == 500
