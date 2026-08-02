def test_search_returns_paginated_shape(client):
    res = client.get("/api/search?q=laptop")
    assert res.status_code == 200
    body = res.get_json()
    assert set(["items", "total", "page", "per_page"]).issubset(body.keys())


def test_search_rejects_bad_pagination(client):
    res = client.get("/api/search?q=laptop&page=0")
    assert res.status_code == 400


def test_search_empty_query_does_not_crash(client):
    res = client.get("/api/search")
    assert res.status_code == 200
